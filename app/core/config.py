from pydantic_settings import BaseSettings


# database settings
class DBSettings(BaseSettings):
    db_name: str = "eurodental_test"
<<<<<<< HEAD
    db_user: str = "api_app"
    db_host: str = "ec2-35-180-66-24.eu-west-3.compute.amazonaws.com"
    db_password: str = "0dental0"
=======
    db_user: str = ""
    db_host: str = ""
    db_password: str = ""
>>>>>>> master

class TokenSettings(BaseSettings):
    secret_key : str = "637d7ae22429851c08a0846ba4a6b908d693585e949ceacf60316eeb2d539158"
    algorithm : str = "HS256"
    access_token_expire_minutes : int = 15
    refresh_token_expire_minutes : int = 2 * 24 * 60

class EmailSettings(BaseSettings):
    email : str = ""
    e_password : str = ""
    e_port : int = 465
    smtp_server : str = "smtp.gmail.com"



db_settings = DBSettings()
token_settings = TokenSettings()
