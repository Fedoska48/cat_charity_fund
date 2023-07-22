from sqlalchemy import Column, String, Text

from app.core.db import BaseDonationCharityProject


class CharityProject(BaseDonationCharityProject):
    """Модель благотворительных проектов фонда."""
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=False)
