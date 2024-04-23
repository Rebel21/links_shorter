from fastapi import APIRouter, Depends

from repository import TokenRepository
from schemes import SCreateUrlAndShortUrl, SCreateShortUrl, SUrl

router = APIRouter(
    prefix="/token",
    tags=["Tokens"]
)


@router.post("")
async def create_token(url_and_short_url: SCreateUrlAndShortUrl) -> SUrl:
    token = await TokenRepository.create_token(url_and_short_url)
    return token


@router.get("")
async def get_tokens() -> list[SUrl]:
    tokens = await TokenRepository.get_all_urls()
    return tokens


# @router.patch("")
# async def disable_token(short_url: SShortUrl) -> SToken:
#     token = await TokenRepository.disable_token(short_url)
#     return token
#
#
# @router.delete("")
# async def delete_token(short_url: SShortUrl):
#     result = await TokenRepository.delete_token(short_url.short_url)
#     if result:
#         return {"status": "ok"}
#     return {"status": "error"}
