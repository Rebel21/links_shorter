import base64
import io

import qrcode
from fastapi import HTTPException
from sqlalchemy import select, delete
from sqlalchemy.orm import selectinload
from starlette.requests import Request

from config import SERVER_HOST_ADDR
from database.database import new_session
from models.url_models import UrlModel, ShortUrlsModel
from repositories.free_words import generate_three_words
from schemes import UrlSchema, ShortUrlSchema, CreateUrlAndShortUrlSchema, AddShortUrlSchema


async def verify_unique_short_url(request: Request):
    body = await request.json()
    async with new_session() as session:
        short_url_object = await session.scalar(
            select(ShortUrlsModel)
            .where(ShortUrlsModel.short_url == body["short_url"])
            .options(selectinload(ShortUrlsModel.url)))
        if short_url_object:
            raise HTTPException(status_code=400, detail="Duplicate short url")


class UrlRepository:

    @classmethod
    async def _create_short_url_object(cls, short_url: str):
        short_url = short_url
        qr_code = qrcode.make(SERVER_HOST_ADDR + short_url)
        buffer = io.BytesIO()
        qr_code.save(buffer, "PNG")
        qr_code_str = base64.b64encode(buffer.getvalue()).decode("utf-8")
        three_words_str = generate_three_words()

        return ShortUrlsModel(
            number_of_transitions=0,
            short_url=short_url,
            qr_code=qr_code_str,
            three_words=three_words_str,
            is_activ=True
        )

    @classmethod
    async def create_url(cls, url_and_hort_url: CreateUrlAndShortUrlSchema) -> UrlSchema:
        async with new_session() as session:
            short_url = await cls._create_short_url_object(url_and_hort_url.short_url)

            url = UrlModel(
                original_url=url_and_hort_url.url,
            )
            url.short_urls.append(short_url)

            session.add(url)
            await session.commit()
            return UrlSchema.model_validate(url, from_attributes=True)

    @classmethod
    async def get_all_urls(cls) -> [UrlSchema]:
        async with new_session() as session:
            result = await session.execute(select(UrlModel).options(selectinload(UrlModel.short_urls)))
            urls = result.scalars().all()
            url_list = [UrlSchema.model_validate(url, from_attributes=True) for url in urls]
            return url_list

    @classmethod
    async def get_url(cls, short_url: str) -> ShortUrlSchema | None:
        async with new_session() as session:
            short_url_object = await session.scalar(select(ShortUrlsModel).where(ShortUrlsModel.short_url == short_url)
                                                    .options(selectinload(ShortUrlsModel.url)))
            if short_url_object is None:
                return short_url_object
            if short_url_object.is_activ:
                short_url_object.number_of_transitions += 1
                session.add(short_url_object)
            await session.commit()
            return short_url_object

    #
    @classmethod
    async def change_availability_short_url(cls, short_url_id: int, is_active: bool) -> ShortUrlSchema | None:
        async with new_session() as session:
            _short_url = await session.scalar(select(ShortUrlsModel).where(ShortUrlsModel.id == short_url_id))
            if _short_url is None:
                return _short_url
            _short_url.is_activ = is_active
            session.add(_short_url)
            await session.commit()
            return _short_url

    @classmethod
    async def delete_short_url(cls, short_url: str):
        async with new_session() as session:
            _short_url = await session.scalar(select(ShortUrlsModel).where(ShortUrlsModel.short_url == short_url)
                                              .options(selectinload(ShortUrlsModel.url)))
            _url = await session.scalar(select(UrlModel).where(UrlModel.id == _short_url.url_id)
                                        .options(selectinload(UrlModel.short_urls)))

            if len(_url.short_urls) > 1:
                await session.execute(delete(ShortUrlsModel).where(ShortUrlsModel.id == _short_url.id))
                await session.commit()
                return True
            elif len(_url.short_urls) == 1:
                await session.execute(delete(ShortUrlsModel).where(ShortUrlsModel.id == _short_url.id))
                await session.execute(delete(UrlModel).where(UrlModel.id == _short_url.url_id))
                await session.commit()
                return True
            else:
                return False

    @classmethod
    async def add_short_url(cls, url_id_and_hort_url: AddShortUrlSchema) -> UrlSchema:
        async with new_session() as session:
            short_url = await cls._create_short_url_object(url_id_and_hort_url.short_url)
            _url = await session.scalar(select(UrlModel).where(UrlModel.id == url_id_and_hort_url.url_id)
                                        .options(selectinload(UrlModel.short_urls)))
            _url.short_urls.append(short_url)
            session.add(_url)
            await session.commit()
            return UrlSchema.model_validate(_url, from_attributes=True)
