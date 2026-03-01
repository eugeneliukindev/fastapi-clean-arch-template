from uuid import UUID

from fastapi import APIRouter, status

from src.domain.services.users import UserServiceDep
from src.schemas.common.pagination import Pagination
from src.schemas.common.response import ApiResponse, Meta
from src.schemas.users import UserCreate, UserPatch, UserPut, UserResponse

router = APIRouter(prefix="/users", tags=["users"])


@router.get("", response_model=ApiResponse[list[UserResponse]])
async def get_users(service: UserServiceDep, pagination: Pagination):
    users = await service.get_all(offset=pagination.offset, limit=pagination.per_page)
    total = await service.count()
    return ApiResponse(data=users, meta=Meta(total=total, page=pagination.page, per_page=pagination.per_page))


@router.get("/{id}", response_model=ApiResponse[UserResponse])
async def get_user(id: UUID, service: UserServiceDep):
    return ApiResponse(data=await service.get(id))


@router.post("", response_model=ApiResponse[UserResponse], status_code=status.HTTP_201_CREATED)
async def create_user(data: UserCreate, service: UserServiceDep):
    return ApiResponse(data=await service.create(data))


@router.put("/{id}", response_model=ApiResponse[UserResponse])
async def put_user(id: UUID, data: UserPut, service: UserServiceDep):
    return ApiResponse(data=await service.update(id, data))


@router.patch("/{id}", response_model=ApiResponse[UserResponse])
async def patch_user(id: UUID, data: UserPatch, service: UserServiceDep):
    return ApiResponse(data=await service.update(id, data))


@router.delete("/{id}", response_model=ApiResponse[UserResponse])
async def delete_user(id: UUID, service: UserServiceDep):
    return ApiResponse(data=await service.delete(id))
