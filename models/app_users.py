from sqlalchemy.dialects.postgresql import UUID
import marshmallow as ma
import uuid

from db import db


class AppUsers(db.Model):
    __tablename__ = 'AppUsers'

    user_id = db.Column(UUID(as_uuid=True),primary_key=True, default=uuid.uuid4)
    email = db.Column(db.String(), nullable=False, unique=True)
    password = db.Column(db.String(), nullable=False)
    is_admin = db.Column(db.Boolean(), default=False)

    auth = db.relationship("AuthTokens", back_populates="user", uselist=False, cascade="all")
    

    def __init__(self, email, password, is_admin=False):
        self.email = email
        self.password = password
        self.is_admin = is_admin


    def new_user_obj():
        return AppUsers('', '', False)
    

class AppUsersSchema(ma.Schema):
    class Meta:
        fields = ['user_id', 'email', 'is_admin', 'auth']

    user_id = ma.fields.UUID()
    email = ma.fields.String(required=True)
    is_admin = ma.fields.Boolean(dump_default=False)

    auth = ma.fields.Nested("AuthTokensSchema", exclude=['user'])


app_user_schema = AppUsersSchema()
app_users_schema = AppUsersSchema(many=True)