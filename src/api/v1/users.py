from uuid import UUID

from fastapi import APIRouter, HTTPException, status

from src.domain.services.users import UserServiceDep
from src.schemas.users import UserCreate, UserPatch, UserPut, UserResponse

router = APIRouter(prefix="/users", tags=["users"])


@router.get("", response_model=list[UserResponse])
async def get_users(service: UserServiceDep):
    return await service.get_all()


@router.get("/{id}", response_model=UserResponse)
async def get_user(id: UUID, service: UserServiceDep):
    user = await service.get(id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return user


@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(data: UserCreate, service: UserServiceDep):
    return await service.create(data)


@router.put("/{id}", response_model=UserResponse)
async def put_user(id: UUID, data: UserPut, service: UserServiceDep):
    user = await service.update(id, data)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return user


@router.patch("/{id}", response_model=UserResponse)
async def patch_user(id: UUID, data: UserPatch, service: UserServiceDep):
    user = await service.update(id, data)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return user


@router.delete("/{id}", response_model=UserResponse)
async def delete_user(id: UUID, service: UserServiceDep):
    user = await service.delete(id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return user
