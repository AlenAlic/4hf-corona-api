from flask_restx import Namespace, Resource, fields
from flask_login import current_user
from ext import db
from models import login_required


api = Namespace("user", description="User")


profile = api.model("ProfileResponse", {
    "id": fields.Integer,
    "email": fields.String,
    "first_name": fields.String,
    "last_name": fields.String,
    "full_name": fields.String,
})


@api.route("/profile")
class UserAPIProfile(Resource):

    @api.response(200, "Profile", profile)
    @login_required
    def get(self):
        """Get user profile"""
        return current_user.profile

    @api.expect(api.model("Profile", {
        "first_name": fields.String(required=True),
        "last_name": fields.String(required=True),
    }), validate=True)
    @api.response(200, "Profile", profile)
    @login_required
    def patch(self):
        """Update user profile"""
        current_user.first_name = api.payload["first_name"]
        current_user.last_name = api.payload["last_name"]
        db.session.commit()
        return current_user.profile

