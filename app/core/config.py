from pydantic_settings import BaseSettings


# database settings
class DBSettings(BaseSettings):
    db_name: str = "eurodental"
    db_user: str = "api_app"
    db_host: str = "ec2-35-180-66-24.eu-west-3.compute.amazonaws.com"
    db_password: str = "0dental0"

class TokenSettings(BaseSettings):
    secret_key : str = "637d7ae22429851c08a0846ba4a6b908d693585e949ceacf60316eeb2d539158"
    algorithm : str = "HS256"
    access_token_expire_minutes : int = 30
    refresh_token_expire_minutes : int = 24 * 7 * 60


db_settings = DBSettings()
token_settings = TokenSettings()
