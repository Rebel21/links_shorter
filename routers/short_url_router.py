from fastapi import APIRouter, Depends

from repository import UrlRepository
from schemes import ShortUrlSchema, DisableShortUrlSchema

router = APIRouter(
    prefix="/short_url",
    tags=["Short_urls"]
)


@router.patch("/disable/{short_url_id}")
async def disable_url(short_url_id: int) -> ShortUrlSchema:
    url = await UrlRepository.change_availability_short_url(short_url_id=short_url_id, is_active=False)
    return url


@router.patch("/enable/{short_url_id}")
async def enable_short_url(short_url_id: int) -> ShortUrlSchema:
    url = await UrlRepository.change_availability_short_url(short_url_id=short_url_id, is_active=True)
    return url


@router.delete("")
async def delete_short_url(short_url: DisableShortUrlSchema):
    result = await UrlRepository.delete_short_url(short_url.short_url)
    if result:
        return {"status": "ok"}
    return {"status": "error"}
