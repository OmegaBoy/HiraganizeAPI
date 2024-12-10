from fastapi import FastAPI, Response
from sqlmodel import Field, Session, SQLModel, create_engine, select
from config import settings
from bs4 import BeautifulSoup
import requests
import re
import feedparser
from yakinori import Yakinori

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

@app.get("/hiraganize/")
def read_beautiful_soup():
    yakinori = Yakinori()

    rss_url = "https://news.google.com/rss/search?q=digimon&hl=ja&gl=JP&ceid=JP:ja"
    feed = feedparser.parse(rss_url)
    output = []
    for entry in feed.entries:
        title = entry.get("title", "No Title")
        parsed_title = yakinori.get_parsed_list(title)
        hiragana_sentence = yakinori.get_hiragana_sentence(parsed_title, is_hatsuon=True)
        link = entry.get("link", "No Link")
        output.append({"title": hiragana_sentence, "link": link})
    return output