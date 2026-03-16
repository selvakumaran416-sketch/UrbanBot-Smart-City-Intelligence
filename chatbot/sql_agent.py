import os
from sqlalchemy import create_engine, text, URL
from sqlalchemy.exc import SQLAlchemyError
from dotenv import load_dotenv
from typing import List, Any, Union

load_dotenv() 

def get_engine():
    url_object = URL.create(
        "mysql+mysqlconnector",
        username=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT", 3306)),
        database=os.getenv("DB_NAME")
    )
    return create_engine(
        url_object,
        pool_pre_ping=True,
        pool_recycle=3600,
        pool_size=5,
        max_overflow=10
    )

engine = get_engine()

def run_query(query: str) -> Union[List[Any], str]:
    """Execute SQL and return results or error string."""
    try:
        with engine.connect() as conn:
            result = conn.execute(text(query))
            if result.returns_rows:
                return result.fetchall()
            conn.commit()
            return []
    except SQLAlchemyError as e:
        return f"Database Error: {str(e)}"

def execute_query(query: str):
    """Alias for analytics engine compatibility."""
    return run_query(query)
