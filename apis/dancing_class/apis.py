from flask_restx import Namespace, Resource, fields, abort
from models import login_required
from models import DancingClass, Person, DancingClassPerson, DancingClassCouple, Couple
from ext import db
import dateutil.parser as datetime_parser
from sqlalchemy import desc


api = Namespace("dancing_class", description="Classes")


def all_dancing_classes():
    return [d.json() for d in DancingClass.query.order_by(desc(DancingClass.datetime)).all()]


model_dancing_class = api.model("DancingClass", {
    "name": fields.String(required=True),
    "datetime": fields.DateTime(required=True),
})
model_dancing_class_person = api.model("DancingClassPerson", {
    "person_id": fields.Integer(required=True),
    "notes": fields.String(required=False),
})
model_dancing_class_couple = api.model("DancingClassCouple", {
    "person_id": fields.Integer(required=True),
    "partner_id": fields.Integer(required=True),
})
model_couple = api.model("Couple", {
    "couple_id": fields.Integer(required=True),
})


@api.route("/")
class DancingClassRoot(Resource):

    @api.response(200, "All dancing classes")
    @login_required
    def get(self):
        """Get all dancing classes"""
        return all_dancing_classes()

    @api.response(200, "All dancing classes")
    @api.expect(model_dancing_class, validate=True)
    @login_required
    def post(self):
        """Create new dancing class"""
        dancing_class = DancingClass()
        dancing_class.name = api.payload["name"]
        dancing_class.datetime = datetime_parser.parse(api.payload["datetime"])
        db.session.add(dancing_class)
        db.session.commit()
        return all_dancing_classes()


@api.route("/<int:dancing_class_id>")
@api.response(404, "Dancing class not found")
class DancingClassSpecific(Resource):

    @api.response(200, "Dancing class")
    @login_required
    def get(self, dancing_class_id):
        """Get dancing class"""
        dancing_class: DancingClass = DancingClass.query.filter(DancingClass.id == dancing_class_id).first()
        if dancing_class:
            return dancing_class.json(include_attendees=True)
        return abort(404)

    @api.response(200, "Dancing class")
    @api.expect(model_dancing_class, validate=True)
    @login_required
    def put(self, dancing_class_id):
        """Update dancing class"""
        dancing_class: DancingClass = DancingClass.query.filter(DancingClass.id == dancing_class_id).first()
        if dancing_class:
            dancing_class.name = api.payload["name"]
            dancing_class.datetime = datetime_parser.parse(api.payload["datetime"])
            db.session.commit()
            return dancing_class.json()
        return abort(404)

    @api.response(200, "Dancing class deleted")
    @login_required
    def delete(self, dancing_class_id):
        """Delete dancing class"""
        dancing_class: DancingClass = DancingClass.query.filter(DancingClass.id == dancing_class_id).first()
        if dancing_class:
            db.session.delete(dancing_class)
            db.session.commit()
            return
        return abort(404)


@api.route("/<int:dancing_class_id>/add_attendee")
class DancingClassSpecificAddAttendee(Resource):

    @api.response(200, "Dancing class")
    @api.response(404, "Dancing class or person not found")
    @api.expect(model_dancing_class_person, validate=True)
    @login_required
    def post(self, dancing_class_id):
        """Add attendee"""
        dancing_class: DancingClass = DancingClass.query.filter(DancingClass.id == dancing_class_id).first()
        person: Person = Person.query.filter(Person.id == api.payload["person_id"]).first()
        if dancing_class and person:
            dcp = DancingClassPerson()
            dcp.dancing_class = dancing_class
            dcp.person = person
            if "notes" in api.payload:
                dcp.notes = api.payload["notes"]
            db.session.add(dcp)
            db.session.commit()
            return dancing_class.json(include_attendees=True)
        return abort(404)


@api.route("/<int:dancing_class_id>/add_couple")
class DancingClassSpecificAddCouple(Resource):

    @api.response(200, "Dancing class")
    @api.response(404, "Dancing class or couple not found")
    @api.expect(model_couple, validate=True)
    @login_required
    def post(self, dancing_class_id):
        """Add couple"""
        dancing_class: DancingClass = DancingClass.query.filter(DancingClass.id == dancing_class_id).first()
        couple: Couple = Couple.query.filter(Couple.id == api.payload["couple_id"]).first()
        if dancing_class and couple:
            dcp_lead = DancingClassPerson()
            dcp_lead.dancing_class = dancing_class
            dcp_lead.person = couple.lead
            dcp_follow = DancingClassPerson()
            dcp_follow.dancing_class = dancing_class
            dcp_follow.person = couple.follow
            dcc = DancingClassCouple()
            dcc.person = dcp_lead
            dcc.partner = dcp_follow
            db.session.add(dcp_lead)
            db.session.add(dcp_follow)
            db.session.add(dcc)
            db.session.commit()
            return dancing_class.json(include_attendees=True)
        return abort(404)


@api.route("/<int:dancing_class_id>/create_couple")
class DancingClassSpecificCreateCouple(Resource):

    @api.response(200, "Dancing class")
    @api.response(404, "Dancing class or people not found")
    @api.expect(model_dancing_class_couple, validate=True)
    @login_required
    def post(self, dancing_class_id):
        """Create couple"""
        dancing_class: DancingClass = DancingClass.query.filter(DancingClass.id == dancing_class_id).first()
        person: DancingClassPerson = DancingClassPerson.query\
            .filter(DancingClassPerson.id == api.payload["person_id"]).first()
        partner: DancingClassPerson = DancingClassPerson.query\
            .filter(DancingClassPerson.id == api.payload["partner_id"]).first()
        if dancing_class and person and partner:
            dcc = DancingClassCouple()
            dcc.dancing_class = dancing_class
            dcc.person = person
            dcc.partner = partner
            db.session.add(dcc)
            db.session.commit()
            return dancing_class.json(include_attendees=True)
        return abort(404)


@api.response(200, "Dancing class")
@api.response(404, "Dancing class or person not found")
@api.route("/<int:dancing_class_id>/attendee/<int:dancing_class_person_id>")
class DancingClassSpecificPerson(Resource):

    @api.expect(model_dancing_class_person, validate=True)
    @login_required
    def put(self, dancing_class_id, dancing_class_person_id):
        """Update dancing class attendee"""
        dancing_class: DancingClass = DancingClass.query.filter(DancingClass.id == dancing_class_id).first()
        attendee: DancingClassPerson = DancingClassPerson.query\
            .filter(DancingClassPerson.id == dancing_class_person_id,
                    DancingClassPerson.dancing_class_id == dancing_class_id).first()
        person: Person = Person.query.filter(Person.id == api.payload["person_id"]).first()
        if dancing_class and attendee and person:
            attendee.person = person
            if "notes" in api.payload:
                attendee.notes = api.payload["notes"]
            db.session.commit()
            return dancing_class.json(include_attendees=True)
        return abort(404)

    @login_required
    def delete(self, dancing_class_id, dancing_class_person_id):
        """Delete dancing class attendee"""
        dancing_class: DancingClass = DancingClass.query.filter(DancingClass.id == dancing_class_id).first()
        attendee: DancingClassPerson = DancingClassPerson.query \
            .filter(DancingClassPerson.id == dancing_class_person_id,
                    DancingClassPerson.dancing_class_id == dancing_class_id).first()
        if dancing_class and attendee:
            db.session.delete(attendee)
            db.session.commit()
            return dancing_class.json(include_attendees=True)
        return abort(404)


@api.response(200, "Dancing class")
@api.route("/<int:dancing_class_id>/couple/<int:dancing_class_couple_id>")
class DancingClassSpecificCouple(Resource):

    @api.response(404, "Dancing class or couple not found")
    @login_required
    def delete(self, dancing_class_id, dancing_class_couple_id):
        """Delete dancing class couple"""
        couple: DancingClassCouple = DancingClassCouple.query \
            .filter(DancingClassCouple.id == dancing_class_couple_id,
                    DancingClassCouple.dancing_class_id == dancing_class_id).first()
        dancing_class: DancingClass = DancingClass.query.filter(DancingClass.id == dancing_class_id).first()
        if dancing_class and couple:
            db.session.delete(couple)
            db.session.commit()
            return dancing_class.json(include_attendees=True)
        return abort(404)
