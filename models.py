import uuid
from database import Base
from sqlalchemy import Column, ForeignKey, String, DECIMAL
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship


class Menu(Base):
    __tablename__ = 'menus'
    id = Column(UUID(as_uuid=True), primary_key=True, nullable=False,
                default=uuid.uuid4)
    title = Column(String,  nullable=False)
    description = Column(String, nullable=False)
    submenus = relationship("Submenu", back_populates="menu", cascade="all, delete-orphan")


class Submenu(Base):
    __tablename__ = 'submenus'
    id = Column(UUID(as_uuid=True), primary_key=True, nullable=False,
                default=uuid.uuid4)
    menu_id = Column(UUID(as_uuid=True), ForeignKey('menus.id'), nullable=False)
    title = Column(String,  nullable=False)
    description = Column(String, nullable=False)
    menu = relationship('Menu', back_populates="submenus")
    dishes = relationship("Dish", back_populates="submenu", cascade="all, delete-orphan")


class Dish(Base):
    __tablename__ = 'dishes'
    id = Column(UUID(as_uuid=True), primary_key=True, nullable=False,
                default=uuid.uuid4)
    submenu_id = Column(UUID(as_uuid=True), ForeignKey('submenus.id'), nullable=False)
    title = Column(String,  nullable=False)
    description = Column(String, nullable=False)
    price = Column(DECIMAL(precision=8, scale=2), nullable=False)
    submenu = relationship('Submenu', back_populates="dishes")
