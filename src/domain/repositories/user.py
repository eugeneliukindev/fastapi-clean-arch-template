from src.models.users import User
from src.schemas.users import UserCreate, UserPatch

from .base import BaseRepository


class UserRepository(BaseRepository[User, UserCreate, UserPatch]):
    model = User
