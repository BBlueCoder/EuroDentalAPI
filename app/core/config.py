from pydantic_settings import BaseSettings

# database settings
class DBSettings(BaseSettings):
    db_name : str = "eurodental"
    db_user : str = "api_app"
    db_host : str = "localhost"
    db_password : str = "0dental0"

db_settings = DBSettings()
