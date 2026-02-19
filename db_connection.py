import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import streamlit as st


# -------------------------------------
# GET DATABASE URL (Cloud + Local)
# -------------------------------------
def get_database_url():
    """
    Works both locally and on Streamlit Cloud.
    """

    # 1️⃣ Streamlit Cloud Secrets
    if "DATABASE_URL" in st.secrets:
        return st.secrets["DATABASE_URL"]

    # 2️⃣ Local .env or system environment
    env_url = os.getenv("DATABASE_URL")
    if env_url:
        return env_url

    # 3️⃣ Safety
    raise ValueError(
        "DATABASE_URL not found. Set it in Streamlit secrets or environment variables."
    )


# -------------------------------------
# CREATE ENGINE
# -------------------------------------
DATABASE_URL = get_database_url()

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,   # prevents stale connection errors
    echo=False
)

SessionLocal = sessionmaker(bind=engine)


# -------------------------------------
# ENGINE ACCESS
# -------------------------------------
def get_engine():
    return engine


# -------------------------------------
# HELPER FUNCTIONS
# -------------------------------------
def get_connection():
    return engine.connect()


def execute_query(query, params=None):
    with engine.begin() as conn:   # safer than manual commit
        result = conn.execute(text(query), params or {})
        return result


def fetch_all(query, params=None):
    with engine.connect() as conn:
        result = conn.execute(text(query), params or {})
        return result.fetchall()


def fetch_one(query, params=None):
    with engine.connect() as conn:
        result = conn.execute(text(query), params or {})
        return result.fetchone()
