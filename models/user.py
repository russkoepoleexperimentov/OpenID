from sqlalchemy import Integer, Column, String, Boolean

from configs.database import Base


class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)

    access_token = Column(String, unique=True, index=True, default="")

    name = Column(String, nullable=True)
    surname = Column(String, nullable=True)

    disabled = Column(Boolean, default=False)
