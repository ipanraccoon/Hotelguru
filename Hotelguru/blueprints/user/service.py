from Hotelguru.models.User import User
from Hotelguru.extensions import db
from Hotelguru.blueprints.user.schemas import UserSchema, RoleSchema
from Hotelguru.models.Role import Role




class UserService:
    @staticmethod
    def user_login(data):
        email = data["email"]
        password = data["password"]
        user = db.session.execute(db.select(User).filter_by(email=email)).scalar_one_or_none()
        if user and user.check_password(password):
            return True, UserSchema().dump(user)
        else:
            return False, "Invalid email or password"
    
    @staticmethod
    def user_register(data):
        try:
            if db.session.execute(db.select(User).filter_by(email=data["email"])).scalar_one_or_none():
                return False, "User already exists"
            password = data["password"]

            new_user = User(email=data["email"], phone=data["phone"], name=data["name"])
            new_user.set_password(password)
            new_user.roles.append(db.session.execute(db.select(Role).filter_by(name="Vendég")).scalar_one())
            db.session.add(new_user)
            db.session.commit()
            return True, UserSchema().dump(new_user)
        except Exception as e:
            db.session.rollback()
            return False, f"Something went wrong: {str(e)}"

    @staticmethod
    def get_all_roles():
        roles = db.session.execute(db.select(Role)).scalars().all()
        return True, RoleSchema().dump(roles,many=True)

    @staticmethod
    def get_user_roles(userid):
        user=db.session.execute(db.select(User).filter_by(id=userid)).scalar_one_or_none()
        if not user:
            return False, "User not found"
        return True, RoleSchema().dump(user.roles,many=True)

    
    @staticmethod
    def get_user(userid):
        user=db.session.execute(db.select(User).filter_by(id=userid)).scalar_one_or_none()
        if not user:
            return False, "User not found"
        return True, UserSchema().dump(user)
    
    @staticmethod    
    def update_user(userid, data):
        user=db.session.execute(db.select(User).filter_by(id=userid)).scalar_one_or_none()
        if not user:
            return False, "User not found"
        if "email" in data:
            existing_user = db.session.execute(db.select(User).filter_by(email=data["email"])).scalar_one_or_none()
            if existing_user and existing_user.id != user.id:
                return False, "Email already exists"
        for key, value in data.items():
            setattr(user, key, value)
        db.session.commit()
        return True, UserSchema().dump(user)