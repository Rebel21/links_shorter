from fastapi import APIRouter, Depends

from repository import TokenRepository
from schemes import SUrl, SShortUrl, SToken

router = APIRouter(
    prefix="/token",
    tags=["Tokens"]
)


@router.post("")
async def create_token(url: SUrl) -> SToken:
    token = await TokenRepository.create_token(url)
    return token


@router.get("")
async def get_tokens() -> list[SToken]:
    tokens = await TokenRepository.get_all_tokens()
    return tokens


@router.patch("")
async def disable_token(short_url: SShortUrl) -> SToken:
    token = await TokenRepository.disable_token(short_url)
    return token


@router.delete("")
async def delete_token(short_url: SShortUrl):
    result = await TokenRepository.delete_token(short_url.short_url)
    if result:
        return {"status": "ok"}
    return {"status": "error"}
