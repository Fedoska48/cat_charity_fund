from pydantic import BaseSettings


class Setting(BaseSettings):
    app_title: str = 'QRKot'
    app_description: str = (
        'Приложение для Благотворительного фонда поддержки котиков'
    )
    database_url: str = 'sqlite+aiosqlite:///./fastapi.db'

    class Config:
        # ссылка на .env файл, откуда будут забираться переменные
        # работает через вызов uvicorn в терминале
        env_file = '.env'


settings = Setting()
