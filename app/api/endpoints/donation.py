from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud.charity_project import charityproject_crud
from app.crud.donation import donation_crud
from app.models import User
from app.schemas.donation import DonationCreate, DonationDB
from app.services.investments import invest

router = APIRouter()

EXCLUDE_FIELDS = (
    'user_id',
    'invested_amount',
    'fully_invested',
    'close_date'
)


@router.get(
    '/',
    response_model=List[DonationDB],
    dependencies=[Depends(current_superuser)],
    response_model_exclude_none=True
)
async def get_all_donations(
    session: AsyncSession = Depends(get_async_session),
):
    donations = await donation_crud.get_multi(session)
    return donations


@router.get(
    '/my',
    response_model=List[DonationDB],
    response_model_exclude={*EXCLUDE_FIELDS})
async def get_my_donations(
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user)
):
    donations = await donation_crud.get_by_user(
        session=session, user=user
    )
    return donations


@router.post(
    '/',
    response_model=DonationDB,
    response_model_exclude_none=True,
    response_model_exclude={*EXCLUDE_FIELDS},
)
async def create_new_donation(
    donation: DonationCreate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user)
):
    new_donation = await donation_crud.create(
        donation,
        session,
        user,
        add_commit=False
    )
    model_objects = (
        await charityproject_crud.get_open_object(
            session
        )
    )
    if model_objects:
        new_donations = invest(
            target=new_donation,
            sources=model_objects
        )
        session.add_all(new_donations)
    await session.commit()
    await session.refresh(new_donation)
    return new_donation