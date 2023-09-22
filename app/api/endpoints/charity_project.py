from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (check_charity_project_before_edit,
                                check_name_duplicate)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charity_project import charityproject_crud
from app.crud.donation import donation_crud
from app.schemas.charity_project import (CharityProjectCreate,
                                         CharityProjectDB,
                                         CharityProjectUpdate)
from app.services.investments import invest

router = APIRouter()


@router.get(
    '/',
    response_model=List[CharityProjectDB],
    response_model_exclude_none=True,
)
async def get_all_charity_projects(
    session: AsyncSession = Depends(get_async_session),
):
    projects = await charityproject_crud.get_multi(session)
    return projects


@router.post(
    '/',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def create_new_charity_project(
        charity_project: CharityProjectCreate,
        session: AsyncSession = Depends(get_async_session),
):
    await check_name_duplicate(charity_project.name, session)
    new_project = await charityproject_crud.create(
        charity_project,
        session,
        add_commit=False)
    model_objects = await donation_crud.get_open_object(session)
    if model_objects:
        new_donations = invest(
            target=new_project,
            sources=model_objects,
        )
        session.add_all(new_donations)
    await session.commit()
    await session.refresh(new_project)
    return new_project


@router.patch(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)]
)
async def update_charity_project(
    project_id: int,
    obj_in: CharityProjectUpdate,
    session: AsyncSession = Depends(get_async_session),
):
    full_amount = (
        obj_in.full_amount if obj_in.full_amount is not None else None
    )
    charity_project = await check_charity_project_before_edit(
        project_id,
        session,
        full_amount=full_amount
    )
    if obj_in.name is not None:
        await check_name_duplicate(obj_in.name, session)
    return await charityproject_crud.update(
        charity_project,
        obj_in,
        session
    )


@router.delete(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)]
)
async def delete_charity_project(
    project_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    charity_project = await check_charity_project_before_edit(
        project_id,
        session,
        delete=True
    )
    return await charityproject_crud.remove(
        charity_project,
        session
    )