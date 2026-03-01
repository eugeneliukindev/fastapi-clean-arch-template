from src.models.users import User
from src.schemas.users import UserCreate, UserPatch, UserPut

from .base import BaseRepository


class UserRepository(BaseRepository[User, UserCreate, UserPut | UserPatch]):
    model = User
