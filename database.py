from sqlmodel import create_engine, SQLModel

DATABASE_URL = "sqlite:///./address.db"
connect_args = {"check_same_thread": False}
engine = create_engine(DATABASE_URL, echo=True, connect_args=connect_args)

def create_db_and_tables() -> None:
    """ Creation of Database and Tables"""
    SQLModel.metadata.create_all(engine)
