from pydantic_settings import BaseSettings


# database settings
class DBSettings(BaseSettings):
    db_name: str = "EuroDental"
    db_user: str = "postgres"
    db_host: str = "localhost"
    db_password: str = "031900"

class TokenSettings(BaseSettings):
    secret_key : str = "637d7ae22429851c08a0846ba4a6b908d693585e949ceacf60316eeb2d539158"
    algorithm : str = "HS256"
    access_token_expire_minutes : int = 30
    refresh_token_expire_minutes : int = 24 * 7 *60

class EmailSettings(BaseSettings):
    email : str = ""
    e_password : str = ""
    e_port : int = 465
    smtp_server : str = "smtp.gmail.com"



db_settings = DBSettings()
token_settings = TokenSettings()
