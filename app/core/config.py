from pydantic import BaseSettings


class Settings(BaseSettings):
    app_title: str = 'QRKot'
    app_description: str = 'Кошачий благотворительный фонд (0.1.0)'
    database_url: str = 'sqlite+aiosqlite:///./fastapi.db'

    class Config:
        # ссылка на .env файл, откуда будут забираться переменные
        # работает через вызов uvicorn в терминале
        env_file = '.env'


settings = Settings()
