from fastapi import APIRouter, Depends

from repository import UrlRepository, verify_unique_short_url
from schemes import CreateUrlAndShortUrlSchema, UrlSchema, AddShortUrlSchema

router = APIRouter(
    prefix="/url",
    tags=["Urls"]
)


@router.post("")
async def create_url(url_and_short_url: CreateUrlAndShortUrlSchema) -> UrlSchema:
    url = await UrlRepository.create_url(url_and_short_url)
    return url


@router.get("")
async def get_url() -> list[UrlSchema]:
    urls = await UrlRepository.get_all_urls()
    return urls


@router.put("", dependencies=[Depends(verify_unique_short_url)])
async def add_short_url(url_and_short_url: AddShortUrlSchema) -> UrlSchema:
    url = await UrlRepository.add_short_url(url_and_short_url)
    return url
