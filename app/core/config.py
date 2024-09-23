from pydantic_settings import BaseSettings

# database settings
class DBSettings(BaseSettings):
    db_name : str = "EuroDental"
    db_user : str = "postgres"
    db_host : str = "localhost"
    db_password : str = "031900"

db_settings = DBSettings()
