import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column

load_dotenv()


class Base(DeclarativeBase):
    pass


db_url = os.getenv("DB_URL")
if db_url is not None:
    engine = create_engine(db_url, echo=True)
else:
    raise Exception("DB_URL variable not set")


class Item(Base):
    __tablename__ = "items"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    checked: Mapped[bool] = mapped_column(nullable=True, default=False)


def insert_item(name: str):
    with Session(engine) as session:
        item = Item()
        item.name = name
        session.add(item)
        session.commit()


def select_all_items():
    with Session(engine) as session:
        items = session.query(Item).order_by(Item.checked.asc(), Item.id.desc()).all()
        return items


def update_item_toggle_checked(item_id: int):
    with Session(engine) as session:
        item: Item | None = session.query(Item).get(item_id)
        if item:
            item.checked = not item.checked
            session.commit()


def delete_item(item_id: int):
    with Session(engine) as session:
        item: Item | None = session.query(Item).get(item_id)
        if item:
            session.delete(item)
            session.commit()
