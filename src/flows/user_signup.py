"""
User login flow implementation.
Generates fake user data when a user sign up.
"""

from uuid import uuid1
from .flow import Flow

from model.user import UserFactory, AddressFactory
from sqlalchemy.orm import Session


class UserSignupFlow(Flow):
    """
    Generate User information in database.
    """

    def __init__(self, db_conn: str, name=uuid1()):
        self.__db_conn = db_conn
        super().__init__(f"user_signup_flow_{name}")

    def execute(self, session: Session):
        # Create address first
        address = AddressFactory()
        session.add(address)
        session.flush()  # Get address ID
        self.logger.info(f"Address created: {address}")

        # Create user with the address ID
        user = UserFactory(address_id=address.id)
        session.add(user)
        session.flush()  # Get user ID
        self.logger.info(f"User created: {user}")

        # Commit to save to database
        session.commit()
        self.logger.info("User and Address committed to database successfully")

        self.logger.log(
            25,  # Custom log level APPFLOW
            f"User {user.name} signed up successfully with email {user.email}",
        )

    @property
    def db_conn(self) -> str:
        return self.__db_conn
