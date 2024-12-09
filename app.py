from fastapi import FastAPI
from sqlmodel import Field, Session, SQLModel, create_engine, select
from config import settings
from bs4 import BeautifulSoup
import requests


class Hero(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    secret_name: str
    age: int | None = Field(default=None, index=True)


engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI))


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


app = FastAPI()


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.get("/")
def hello():
    return "Hello, Deckard!"

@app.post("/heroes/")
def create_hero(hero: Hero):
    with Session(engine) as session:
        session.add(hero)
        session.commit()
        session.refresh(hero)
        return hero


@app.get("/heroes/")
def read_heroes():
    with Session(engine) as session:
        heroes = session.exec(select(Hero)).all()
        return heroes

@app.get("/heroes/{hero_id}")
def read_hero(hero_id: int):
    with Session(engine) as session:
        hero = session.get(Hero, hero_id)
        return hero

@app.get("/beautiful-soup/")
def read_beautiful_soup():
    url = "https://www.eldestapeweb.com/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Suponiendo que los titulares están en <h2> con clase 'headline'
    titulares = soup.find_all('h2', class_='headline')

    # for i, titular in enumerate(titulares, 1):
    #     print(f"{i}. {titular.text.strip()}")
    return titulares