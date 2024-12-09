from fastapi import FastAPI
from sqlmodel import Field, Session, SQLModel, create_engine, select
from config import settings


class Hero(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    secret_name: str
    age: int | None = Field(default=None, index=True)


engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI))


def create_db_and_tables():
    """
    Create the database and tables.

    This function creates the database and tables if they do not exist.
    It is called when the FastAPI application starts.
    """
    SQLModel.metadata.create_all(engine)


app = FastAPI()


@app.on_event("startup")
def on_startup():
    """
    Create the database and tables when the application starts.

    This function is called when the FastAPI application starts.
    It creates the database and tables if they do not exist.
    """
    create_db_and_tables()


@app.get("/")
def hello():
"""
Return a greeting message.

Returns:
    str: A greeting message indicating the application is running.
"""
    return "Hello, Docker!"


@app.post("/heroes/")
def create_hero(hero: Hero):
    """
    Create a hero

    Args:
        hero (Hero): The hero to create

    Returns:
        Hero: The created hero
    """

    with Session(engine) as session:
        session.add(hero)
        session.commit()
        session.refresh(hero)
        return hero


@app.get("/heroes/")
def read_heroes():
    """
    Retrieve a list of all heroes.

    Returns:
        List[Hero]: A list of all heroes in the database.
    """
    with Session(engine) as session:
        heroes = session.exec(select(Hero)).all()
        return heroes

@app.get("/heroes/{hero_id}")
def read_hero(hero_id: int):
    """
    Read a hero by ID

    Args:
        hero_id (int): The ID of the hero to read

    Returns:
        Hero: The hero with the specified ID
    """
    with Session(engine) as session:
        hero = session.get(Hero, hero_id)
        return hero