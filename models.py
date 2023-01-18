import uuid
from database import Base
from sqlalchemy import Column, ForeignKey, String, Float
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship


class Menu(Base):
    __tablename__ = 'menus'
    id = Column(UUID(as_uuid=True), primary_key=True, nullable=False,
                default=uuid.uuid4)
    title = Column(String,  nullable=False)
    description = Column(String, nullable=False)


class Submenu(Base):
    __tablename__ = 'submenus'
    id = Column(UUID(as_uuid=True), primary_key=True, nullable=False,
                default=uuid.uuid4)
    menu_id = Column(UUID(as_uuid=True), ForeignKey(
        'menus.id', ondelete='CASCADE'), nullable=False)
    title = Column(String,  nullable=False)
    description = Column(String, nullable=False)
    menu = relationship('Menu')


class Dish(Base):
    __tablename__ = 'dishes'
    id = Column(UUID(as_uuid=True), primary_key=True, nullable=False,
                default=uuid.uuid4)
    submenu_id = Column(UUID(as_uuid=True), ForeignKey(
        'submenus.id', ondelete='CASCADE'), nullable=False)
    title = Column(String,  nullable=False)
    description = Column(String, nullable=False)
    price = Column(Float(precision=2), nullable=False)
    submenu = relationship('Submenu')
