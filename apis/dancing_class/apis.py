from flask_restx import Namespace, Resource, fields, abort
from models import login_required
from models import DancingClass, Person, DancingClassPerson, DancingClassCouple
from ext import db
import dateutil.parser as datetime_parser


api = Namespace("dancing_class", description="Classes")


def all_dancing_classes():
    return [d.json() for d in DancingClass.query.order_by(DancingClass.datetime).all()]


@api.route("/")
class DancingClassRoot(Resource):

    @api.response(200, "All dancing classes")
    @login_required
    def get(self):
        """Get all dancing classes"""
        return all_dancing_classes()

    @api.response(200, "All dancing classes")
    @api.expect(api.model("DancingClass", {
        "name": fields.String(required=True),
        "datetime": fields.DateTime(required=True),
    }), validate=True)
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
class DancingClassSpecific(Resource):

    @api.response(200, "Dancing classes")
    @api.response(404, "Dancing class not found")
    @login_required
    def get(self, dancing_class_id):
        """Get dancing class"""
        dancing_class: DancingClass = DancingClass.query.filter(DancingClass.id == dancing_class_id).first()
        if dancing_class:
            return dancing_class.json(include_attendees=True)
        return abort(404)


@api.route("/<int:dancing_class_id>/add_attendee")
class DancingClassSpecificAddAttendee(Resource):

    @api.response(200, "Dancing classes")
    @api.response(404, "Dancing class or Person not found")
    @api.expect(api.model("DancingClass", {
        "person_id": fields.Integer(required=True),
        "notes": fields.String(required=False),
    }), validate=True)
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


@api.route("/<int:dancing_class_id>/create_couple")
class DancingClassSpecificCreateCouple(Resource):

    @api.response(200, "Dancing classes")
    @api.response(404, "Dancing class or people not found")
    @api.expect(api.model("DancingClass", {
        "person_id": fields.Integer(required=True),
        "partner_id": fields.Integer(required=True),
    }), validate=True)
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
