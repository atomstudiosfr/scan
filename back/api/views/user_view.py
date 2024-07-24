from fastapi import APIRouter
from fastapi.params import Depends

from core.schema import User
from api.security.authentication import get_current_active_user

router = APIRouter(
    prefix="/user",
    tags=["User"],
)


# Example protected endpoint
@router.get("/users/me")
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user
