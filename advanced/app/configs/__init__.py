from app.configs.database import PostgresSettings
from app.configs.general import GeneralSettings
from app.configs.auth import AuthSettings
from app.configs.emails import EmailSettings
from app.configs.logger import LoggerSettings


class Settings(
    PostgresSettings,
    AuthSettings,
    LoggerSettings,
    EmailSettings,
    GeneralSettings,
):
    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()
