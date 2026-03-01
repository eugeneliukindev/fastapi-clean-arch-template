from uuid import UUID

from fastapi import APIRouter, status

from src.domain.services.users import UserServiceDep
from src.schemas.common.pagination import Pagination
from src.schemas.common.response import ApiResponse, Meta
from src.schemas.users import UserCreate, UserPatch, UserPut, UserResponse

router = APIRouter(prefix="/users", tags=["users"])


@router.get("")
async def get_users(service: UserServiceDep, pagination: Pagination) -> ApiResponse[list[UserResponse]]:
    users = await service.get_all(offset=pagination.offset, limit=pagination.per_page)
    total = await service.count()
    return ApiResponse(data=users, meta=Meta(total=total, page=pagination.page, per_page=pagination.per_page))


@router.get("/{id}")
async def get_user(id: UUID, service: UserServiceDep) -> ApiResponse[UserResponse]:
    return ApiResponse(data=await service.get(id))


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_user(data: UserCreate, service: UserServiceDep) -> ApiResponse[UserResponse]:
    return ApiResponse(data=await service.create(data))


@router.put("/{id}")
async def put_user(id: UUID, data: UserPut, service: UserServiceDep) -> ApiResponse[UserResponse]:
    return ApiResponse(data=await service.update(id, data))


@router.patch("/{id}")
async def patch_user(id: UUID, data: UserPatch, service: UserServiceDep) -> ApiResponse[UserResponse]:
    return ApiResponse(data=await service.update(id, data))


@router.delete("/{id}")
async def delete_user(id: UUID, service: UserServiceDep) -> ApiResponse[UserResponse]:
    return ApiResponse(data=await service.delete(id))
