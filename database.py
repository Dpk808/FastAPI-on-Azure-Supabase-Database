from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine 
import os
from dotenv import load_dotenv

load_dotenv()

def _get_database_url() -> str:
    db_url = os.getenv("DATABASE_URL", "").strip()

    if not db_url:
        raise RuntimeError(
            "DATABASE_URL is not set. Configure it as an environment variable."
        )

    # Azure or other providers may return postgres://, but SQLAlchemy expects postgresql://.
    if db_url.startswith("postgres://"):
        db_url = db_url.replace("postgres://", "postgresql+psycopg://", 1)
    elif db_url.startswith("postgresql://"):
        db_url = db_url.replace("postgresql://", "postgresql+psycopg://", 1)

    # Azure Database for PostgreSQL often requires SSL. Add it when missing.
    if "sslmode=" not in db_url:
        separator = "&" if "?" in db_url else "?"
        db_url = f"{db_url}{separator}sslmode=require"

    return db_url


db_url = _get_database_url()

engine = create_engine(db_url, pool_pre_ping=True)

session = sessionmaker(autocommit=False, autoflush=False, bind=engine)