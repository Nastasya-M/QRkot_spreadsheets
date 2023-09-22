from datetime import datetime
from typing import List, Union

from app.models import CharityProject, Donation


def invest(
    target: Union[CharityProject, Donation],
    sources: List[Union[CharityProject, Donation]]
) -> List[Union[CharityProject, Donation]]:
    modified_sources = []
    target.invested_amount = int(target.invested_amount or 0)
    for source in sources:
        investing_volume = min(
            source.full_amount - source.invested_amount,
            target.full_amount - target.invested_amount
        )
        for object in (source, target):
            object.invested_amount += investing_volume
            if object.invested_amount == object.full_amount:
                object.fully_invested = True
                object.close_date = datetime.now()
        if target.fully_invested:
            break
        modified_sources.append(source)
    return modified_sources