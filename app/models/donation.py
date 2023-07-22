from sqlalchemy import Column, Text, Integer, ForeignKey

from app.core.db import BaseDonationCharityProject


class Donation(BaseDonationCharityProject):
    """Модель пожертвований в фонд."""
    user_id = Column(Integer,
                     ForeignKey('user.id', name='fk_donation_user_id_user'))
    comment = Column(Text)
