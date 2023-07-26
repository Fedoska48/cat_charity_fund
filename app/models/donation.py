from sqlalchemy import Column, Text, Integer, ForeignKey

from app.models.base import BaseCharity, MAX_REPR_LENGTH

REPR_TEXT = ('Индентификатор пользователя: {user_id};'
             'Комментарий: {comment};'
             '{super}')


class Donation(BaseCharity):
    """Модель пожертвований в фонд."""
    user_id = Column(Integer,
                     ForeignKey('user.id', name='fk_donation_user_id_user'))
    comment = Column(Text)

    def __repr__(self):
        return REPR_TEXT.format(
            user_id=self.user_id,
            comment=self.comment[:MAX_REPR_LENGTH],
            super=super().__repr__()
        )
