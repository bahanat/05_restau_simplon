from sqlalchemy.engine import URL


class TestSettings:
    @property
    def DATABASE_URL(self) -> str:
        return "sqlite://"


settings = TestSettings()
