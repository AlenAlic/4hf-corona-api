from flask_restx import Namespace, Resource, fields, abort
from models import login_required
from models import Person
from ext import db


api = Namespace("person", description="People")


def all_persons(include_active_partners=False):
    return [
        p.json(include_active_partners=include_active_partners) for p in Person.query.order_by(Person.first_name).all()
    ]


@api.route("/")
class PersonRoot(Resource):

    @api.response(200, "All dancing classes")
    @login_required
    def get(self):
        """Get all persons"""
        return all_persons(include_active_partners=True)

    @api.response(200, "All dancing classes")
    @api.expect(api.model("DancingClass", {
        "first_name": fields.String(required=True),
        "last_name": fields.String(required=True),
        "email": fields.String(required=True),
        "student_number": fields.String(required=False),
    }), validate=True)
    @login_required
    def post(self):
        """Create new person"""
        person = Person()
        person.first_name = api.payload["first_name"]
        person.last_name = api.payload["last_name"]
        person.email = api.payload["email"]
        if "student_number" in api.payload:
            person.student_number = api.payload["student_number"]
        db.session.add(person)
        db.session.commit()
        return all_persons(include_active_partners=True)


@api.route("/<int:person_id>")
@api.response(404, "Person not found")
class PersonSpecific(Resource):

    @api.response(200, "Person")
    @login_required
    def get(self, person_id):
        """Get person"""
        person: Person = Person.query.filter(Person.id == person_id).first()
        if person:
            return person.json(include_active_partners=True)
        return abort(404)

    @api.response(200, "Person")
    @api.expect(api.model("DancingClass", {
        "first_name": fields.String(required=True),
        "last_name": fields.String(required=True),
        "email": fields.String(required=True),
        "student_number": fields.String(required=False),
    }), validate=True)
    @login_required
    def put(self, person_id):
        """Update person"""
        person: Person = Person.query.filter(Person.id == person_id).first()
        if person:
            person.first_name = api.payload["first_name"]
            person.last_name = api.payload["last_name"]
            person.email = api.payload["email"]
            if "student_number" in api.payload:
                person.student_number = api.payload["student_number"]
            db.session.commit()
            return person.json(include_active_partners=True)
        return abort(404)

    @api.response(200, "Person")
    @login_required
    def delete(self, person_id):
        """Delete person"""
        person: Person = Person.query.filter(Person.id == person_id).first()
        if person:
            db.session.delete(person)
            db.session.commit()
            return
        return abort(404)
