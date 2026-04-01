from Hotelguru.models.User import User
from Hotelguru.extensions import db
from Hotelguru.blueprints.user.schemas import UserSchema




class UserService:
    @staticmethod
    def user_login(data):
        email = data.get("email")
        password = data.get("password")
        user = db.session.execute(db.select(User).filter_by(email=email)).scalar_one_or_none()
        if user and user.check_password(password):
            return True, UserSchema().dump(user)
        else:
            return False, "Invalid email or password"
        
        
