from fastapi import APIRouter, Depends, status

from api.constants import ErrorCodes
from api.exceptions import ObjectNotFoundException, UniqueKeyViolationException
from api.schemas import ResourceCreatedResponse, ResourceDeletedResponse
from api.bots.dependencies import get_bot_service
from api.bots.schemas import InBotSchema, OutBotSchema, OutBotsSchema
from api.bots.services import BotService

from logger import logger

router = APIRouter()


@router.get("/", tags=["Get all bots"], response_model=list[OutBotsSchema], status_code=status.HTTP_200_OK)
async def get_all_bots(bot_service: BotService = Depends(get_bot_service)) -> list[OutBotsSchema]:
    """returns all bots"""
    logger.debug(f"Get all bots endpoint hit")
    return await bot_service.list()


@router.get("/{id}", tags=["Get bot by id"], response_model=OutBotSchema, status_code=status.HTTP_200_OK)
async def get_bot_by_id(id: str, bot_service: BotService = Depends(get_bot_service)) -> OutBotSchema:
    """return single bot by id"""
    logger.info(f"Fetching bot with id {id}")
    try:
        bot = await bot_service.get(id=id)
    except ObjectNotFoundException as e:
        logger.debug(f"Bot with id {id} not found. Throwing 404 Not Found error")
        e.detail = ErrorCodes.BOT_NOT_FOUND
        raise e
    return bot


@router.post("/", tags=["Create bot"], response_model=ResourceCreatedResponse, status_code=status.HTTP_201_CREATED)
async def create_bot(bot: InBotSchema, bot_service: BotService = Depends(get_bot_service)):
    """check and create bot. If bot already exists, return 409 Conflict error"""
    if await bot_service.bot_exists(name=bot.name):
        logger.debug(
            f"Bot with this name {bot.name} already exists. "
            f"Throwing 409 Conflict error"
        )
        raise UniqueKeyViolationException(
            status_code=status.HTTP_409_CONFLICT, detail=ErrorCodes.USERNAME_OR_EMAIL_ALREADY_EXISTS
        )
    new_bot = await bot_service.create(bot)
    logger.info(f"Bot created with id: {new_bot.id}")
    return ResourceCreatedResponse(detail="Bot created successfully", id=new_bot.id)


@router.put("/{id}", tags=["Update bot"], response_model=OutBotSchema, status_code=status.HTTP_200_OK)
async def update_bot(id: str, bot: InBotSchema, bot_service: BotService = Depends(get_bot_service)):
    """update bot by id, Also soft delete bot if is_deleted is True"""
    try:
        await bot_service.update(id=id, obj=bot)
    except UniqueKeyViolationException as e:
        logger.debug(
            f"Bot with this name {bot.name} already exists. "
            f"Throwing 409 Conflict error"
        )
        e.detail = ErrorCodes.BOT_ALREADY_EXISTS
        raise e
    except ObjectNotFoundException as e:
        logger.debug(f"Bot with id {id} not found. Throwing 404 Not Found error")
        e.detail = ErrorCodes.BOT_NOT_FOUND
        raise e
    logger.info(f"Bot with id {id} updated")
    return bot_service.get(id=id)


@router.delete("/{id}", tags=["Delete Bot"], response_model=ResourceDeletedResponse, status_code=status.HTTP_200_OK)
async def delete_user(id: str, bot_service: BotService = Depends(get_bot_service)) -> OutBotSchema:
    """soft delete user by id"""
    await bot_service.delete(id=id)
    logger.info(f"Bot with {id} deleted")
    return ResourceDeletedResponse(detail="Bot deleted successfully", id=id)
