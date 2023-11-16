from fastapi import APIRouter, Depends, status

from api.constants import ErrorCodes
from api.exceptions import ObjectNotFoundException, UniqueKeyViolationException
from api.schemas import ResourceCreatedResponse, ResourceDeletedResponse
from api.users.dependencies import get_user_service
from api.users.schemas import InUserSchema, OutUserSchema, OutUsersSchema
from api.users.services import UserService

from logger import logger

router = APIRouter()


@router.get("/", tags=["Get all intents"], response_model=list[OutUsersSchema], status_code=status.HTTP_200_OK)
async def get_all_users(user_service: UserService = Depends(get_user_service)) -> list[OutUsersSchema]:
    """returns all intents"""
    logger.debug(f"Get all intents endpoint hit")
    return await user_service.list()


@router.get("/{id}", tags=["Get user by id"], response_model=OutUserSchema, status_code=status.HTTP_200_OK)
async def get_user_by_id(id: str, user_service: UserService = Depends(get_user_service)) -> OutUserSchema:
    """return single user by id"""
    logger.info(f"Fetching user with id {id}")
    try:
        user = await user_service.get(id=id)
    except ObjectNotFoundException as e:
        logger.debug(f"User with id {id} not found. Throwing 404 Not Found error")
        e.detail = ErrorCodes.USER_NOT_FOUND
        raise e
    return user


@router.post("/", tags=["Create user"], response_model=ResourceCreatedResponse, status_code=status.HTTP_201_CREATED)
async def create_user(user: InUserSchema, user_service: UserService = Depends(get_user_service)):
    """check and create user. If user already exists, return 409 Conflict error"""
    if await user_service.user_exists(username=user.username, email=user.email):
        logger.debug(
            f"User with this username {user.username} or email {user.email} already exists. "
            f"Throwing 409 Conflict error"
        )
        raise UniqueKeyViolationException(
            status_code=status.HTTP_409_CONFLICT, detail=ErrorCodes.USERNAME_OR_EMAIL_ALREADY_EXISTS
        )
    new_user = await user_service.create(user)
    logger.info(f"User created with id: {new_user.id}")
    return ResourceCreatedResponse(detail="User created successfully", id=new_user.id)


@router.put("/{id}", tags=["Update user"], response_model=OutUserSchema, status_code=status.HTTP_200_OK)
async def update_user(id: str, user: InUserSchema, user_service: UserService = Depends(get_user_service)):
    """update user by id. Also soft delete user if is_deleted is True"""
    try:
        await user_service.update(id=id, obj=user)
    except UniqueKeyViolationException as e:
        logger.debug(
            f"User with this username {user.username} or email {user.email} already exists. "
            f"Throwing 409 Conflict error"
        )
        e.detail = ErrorCodes.USERNAME_OR_EMAIL_ALREADY_EXISTS
        raise e
    except ObjectNotFoundException as e:
        logger.debug(f"User with id {id} not found. Throwing 404 Not Found error")
        e.detail = ErrorCodes.USER_NOT_FOUND
        raise e
    logger.info(f"User with id {id} updated")
    return await user_service.get(id=id)


@router.delete("/{id}", tags=["Delete User"], response_model=ResourceDeletedResponse, status_code=status.HTTP_200_OK)
async def delete_user(id: str, user_service: UserService = Depends(get_user_service)) -> OutUserSchema:
    """soft delete user by id"""
    await user_service.delete(id=id)
    logger.info(f"User with {id} deleted")
    return ResourceDeletedResponse(detail="User deleted successfully", id=id)
