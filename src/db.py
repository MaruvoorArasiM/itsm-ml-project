import os
from getpass import getpass
from dotenv import load_dotenv, find_dotenv
from sqlalchemy import create_engine
from sqlalchemy.engine import URL


def get_engine():
    """Engine for the read-only ITSM database.

    Host, user and database name come from .env, which is git-ignored.
    The password is always asked for in a hidden prompt; it is never
    stored in a file or printed.
    """
    load_dotenv(find_dotenv(usecwd=True))
    missing = [k for k in ("DB_HOST", "DB_USER", "DB_NAME") if not os.getenv(k)]
    if missing:
        raise RuntimeError("Set " + ", ".join(missing) + " in .env")
    url = URL.create("mysql+pymysql",
                     username=os.getenv("DB_USER"),
                     password=getpass("Database password: "),
                     host=os.getenv("DB_HOST"),
                     database=os.getenv("DB_NAME"))
    return create_engine(url, pool_pre_ping=True,
                         connect_args={"charset": "utf8mb4", "connect_timeout": 15})
