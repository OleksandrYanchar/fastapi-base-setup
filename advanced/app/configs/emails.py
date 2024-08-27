from app.configs.general import GeneralSettings


class EmailSettings(GeneralSettings):
    EMAIL_HOST_USER: str
    EMAIL_HOST_PASSWORD: str
    EMAIL_HOST_USERNAME: str
