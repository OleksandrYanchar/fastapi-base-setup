from app.configs.general import GeneralSettings


class AuthSettings(GeneralSettings):
    SECRET: str
    REFRESH_SECRET: str

    ALGORITHM: str

    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_DAYS: int

    @property
    def REFRESH_TOKEN_EXPIRE_MINUTES(self):
        return self.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60
