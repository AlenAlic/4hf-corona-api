from flask_restx import Namespace, Resource, fields, abort
from models import login_required
from models import Couple, Person
from ext import db


api = Namespace("couple", description="Couples")


def all_couples():
    return [c.json() for c in Couple.query.join(Person, Couple.lead_id == Person.id).order_by(Person.first_name).all()]


@api.route("/")
class CoupleRoot(Resource):

    @api.response(200, "All couples")
    @login_required
    def get(self):
        """Get all couples"""
        return all_couples()

    @api.response(200, "All couples")
    @api.expect(api.model("Couple", {
        "lead_id": fields.Integer(required=True),
        "follow_id": fields.Integer(required=True),
    }), validate=True)
    @login_required
    def post(self):
        """Create new couple"""
        couple = Couple()
        couple.lead_id = api.payload["lead_id"]
        couple.follow_id = api.payload["follow_id"]
        db.session.add(couple)
        db.session.commit()
        return all_couples()


@api.route("/<int:couple_id>")
@api.response(404, "Couple not found")
class CoupleSpecific(Resource):

    @api.response(200, "Couple")
    @login_required
    def get(self, couple_id):
        """Get person"""
        couple: Couple = Couple.query.filter(Couple.id == couple_id).first()
        if couple:
            return couple.json()
        return abort(404)

    @api.response(200, "Couple")
    @api.expect(api.model("Couple", {
        "lead_id": fields.Integer(required=True),
        "follow_id": fields.Integer(required=True),
    }), validate=True)
    @login_required
    def put(self, couple_id):
        """Update couple"""
        couple: Couple = Couple.query.filter(Couple.id == couple_id).first()
        if couple:
            couple.lead_id = api.payload["lead_id"]
            couple.follow_id = api.payload["follow_id"]
            db.session.commit()
            return couple.json()
        return abort(404)

    @api.response(200, "Couple deleted")
    @login_required
    def delete(self, couple_id):
        """Delete couple"""
        couple: Couple = Couple.query.filter(Couple.id == couple_id).first()
        if couple:
            db.session.delete(couple)
            db.session.commit()
            return
        return abort(404)
