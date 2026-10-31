import os
from getpass import getpass
from dotenv import load_dotenv, find_dotenv
from sqlalchemy import create_engine
from sqlalchemy.engine import URL

def get_engine(ask_password=False):
    load_dotenv(find_dotenv(usecwd=True))
    password = getpass("DB password: ") if ask_password else os.getenv("DB_PASSWORD")
    if not password:
        password = getpass("DB password: ")
    url = URL.create(
        "mysql+pymysql",
        username=os.getenv("DB_USER"),
        password=password,
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
    )
    return create_engine(url)
