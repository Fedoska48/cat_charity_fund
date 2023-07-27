from datetime import datetime
from typing import List

from app.models.base import BaseCharity


def investing(
        target: BaseCharity,  # объект
        sources: List[BaseCharity]  # субъект
) -> List[BaseCharity]:
    """
    Процесс инвестирования.
    Увеличение invested_amount, как в проектах, так и в пожертвованиях.
    Установка значений fully_invested и close_date, при необходимости.
    """
    changed = []
    if target.invested_amount is None:
        target.invested_amount = 0
    for source in sources:
        available_for_invest = min(
            source.full_amount - source.invested_amount,
            target.full_amount - target.invested_amount
        )
        changed.append(source)
        for investment in [target, source]:
            investment.invested_amount += available_for_invest
            if investment.invested_amount == investment.full_amount:
                investment.fully_invested = True
                investment.close_date = datetime.utcnow()
        if target.fully_invested:
            break
    return changed
