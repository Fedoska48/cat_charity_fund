from sqlalchemy import Column, String, Text

from app.models.base import BaseCharity, MAX_REPR_LENGTH

REPR_TEXT = ('Название проекта: {name};'
             'Описание проекта: {description};'
             '{super}')


class CharityProject(BaseCharity):
    """Модель благотворительных проектов фонда."""
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=False)

    def __repr__(self):
        return REPR_TEXT.format(
            name=self.name[:MAX_REPR_LENGTH],
            description=self.description[:MAX_REPR_LENGTH],
            super=super().__repr__()
        )
