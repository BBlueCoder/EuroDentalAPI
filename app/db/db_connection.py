from sqlmodel import create_engine

from app.core.config import db_settings

db_name = db_settings.db_name
db_user = db_settings.db_user
db_password = db_settings.db_password
db_host = db_settings.db_host
db_url = f"postgresql://{db_user}:{db_password}@{db_host}/{db_name}"

connect_args = {"check_same_thread": True}
engine = create_engine(db_url, echo=True)
