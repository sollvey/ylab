from sqlalchemy import Column, Integer, String, BigInteger, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class MenuPy(Base):
    __tablename__ = "menu"

    id = Column(Integer, nullable=False, primary_key=True)
    title = Column(String(256), nullable=False)
    description = Column(String(1024), nullable=False)


class SubmenuPy(Base):
    __tablename__ = "submenu"

    id = Column(Integer, nullable=False, primary_key=True)
    title = Column(String(256), nullable=False)
    description = Column(String(1024), nullable=False)
    menu_id = Column(BigInteger, ForeignKey("Menu.id", ondelete="CASCADE"), nullable=False)


class DishPy(Base):
    __tablename__ = "dish"

    id = Column(Integer, nullable=False, primary_key=True)
    title = Column(String(256), nullable=False)
    description = Column(String(1024), nullable=False)
    price = Column(Float(10, 3), nullable=False)
    submenu_id = Column(BigInteger, ForeignKey("Submenu.id", ondelete="CASCADE"), nullable=False)