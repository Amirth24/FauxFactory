"""
User model and factory for generating fake user data.
Includes User and Address models with proper relationships and factories.
"""

import factory
from typing import TYPE_CHECKING
from faker.providers import BaseProvider
from . import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship, Session
from sqlalchemy import String, Integer, DateTime, ForeignKey
from sqlalchemy.sql import func
from datetime import datetime

if TYPE_CHECKING:
    from typing import List


class Address(Base):
    """Address model representing user addresses."""

    __tablename__ = "addresses"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    street: Mapped[str] = mapped_column(String(200), nullable=False)
    city: Mapped[str] = mapped_column(String(100), nullable=False)
    state: Mapped[str] = mapped_column(String(100), nullable=False)
    zip_code: Mapped[str] = mapped_column(String(20), nullable=False)
    country: Mapped[str] = mapped_column(String(100), nullable=False, default="USA")

    # Relationship back to users
    users: Mapped["List[User]"] = relationship("User", back_populates="address")

    def __repr__(self):
        return f"Address(id={self.id}, street='{self.street}', city='{self.city}', state='{self.state}', zip_code='{self.zip_code}')"

    def __str__(self):
        return f"{self.street}, {self.city}, {self.state} {self.zip_code}"


class User(Base):
    """User model representing application users."""

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    phone: Mapped[str] = mapped_column(String(30), nullable=True)
    address_id: Mapped[int] = mapped_column(ForeignKey("addresses.id"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=func.now(), onupdate=func.now()
    )

    # Relationship to address
    address: Mapped[Address] = relationship("Address", back_populates="users")

    def __repr__(self):
        return f"User(id={self.id}, name='{self.name}', email='{self.email}')"

    def __str__(self):
        return f"{self.name} ({self.email})"

    @property
    def full_address(self):
        """Get the full address as a formatted string."""
        return str(self.address) if self.address else "No address"


class AddressFactory(factory.Factory):
    """Factory for creating Address instances with fake data."""

    class Meta:
        model = Address

    street = factory.Faker("street_address")
    city = factory.Faker("city")
    state = factory.Faker("state")
    zip_code = factory.Faker("postcode")
    country = "USA"


class UserFactory(factory.Factory):
    """Factory for creating User instances with fake data."""

    class Meta:
        model = User

    name = factory.Faker("name")
    email = factory.Faker("email")
    phone = factory.Faker("phone_number")


class UserProvider(BaseProvider):
    """
    A Faker provider for generating and retrieving User instances from the database.
    """

    def __init__(self, generator, session: Session):
        self.session = session
        super().__init__(generator)

    def create_user(self) -> User:
        """Create a new user with address and save to database."""
        # Create address first
        address = AddressFactory()
        self.session.add(address)
        self.session.flush()  # Get the address ID

        # Create user with the address ID
        user = UserFactory(address_id=address.id)
        self.session.add(user)
        self.session.flush()  # Get the user ID

        return user

    def random_user(self) -> User:
        """Get a random existing user from the database."""
        return self.session.query(User).order_by(func.random()).first()

    def all_users(self) -> "List[User]":
        """Get all users from the database."""
        return self.session.query(User).all()
