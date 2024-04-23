import base64
import io
import os

import qrcode
from sqlalchemy import select, delete

from config import SERVER_HOST_ADDR
from database.database import new_session
from models.models import UrlOrm, ShortUrlsOrm
from schemes import SUrl, SShortUrl, SCreateUrlAndShortUrl


class TokenRepository:

    @classmethod
    async def create_token(cls, url_and_hort_url: SCreateUrlAndShortUrl) -> SUrl:
        async with new_session() as session:
            short_url = url_and_hort_url.short_url if url_and_hort_url.short_url else os.urandom(8).hex()
            qr_code = qrcode.make(SERVER_HOST_ADDR + short_url)
            buffer = io.BytesIO()
            qr_code.save(buffer, "PNG")
            qr_code_str = base64.b64encode(buffer.getvalue()).decode("utf-8")

            short_url_obj = ShortUrlsOrm(
                number_of_transitions=0,
                short_url=short_url,
                qr_code=qr_code_str,
                is_activ=True
            )

            url = UrlOrm(
                original_url=url_and_hort_url.url,
            )
            url.short_urls.append(short_url_obj)

            session.add(url)
            await session.commit()
            return SUrl.model_validate(url, from_attributes=True)

    @classmethod
    async def get_all_urls(cls) -> [SUrl]:
        async with new_session() as session:
            query = select(UrlOrm)
            result = await session.execute(query)
            urls = result.scalars().all()
            url_list = [SUrl.model_validate(url, from_attributes=True) for url in urls]
            return url_list

    @classmethod
    async def get_url(cls, short_url: str) -> SShortUrl | None:
        async with new_session() as session:
            short_url_object = await session.scalar(select(ShortUrlsOrm).where(ShortUrlsOrm.short_url == short_url))
            # short_url_object = await session.scalar(select(ShortUrlsOrm).where(ShortUrlsOrm.short_url == short_url))
            if short_url_object is None:
                return short_url_object
            if short_url_object.is_activ:
                short_url_object.number_of_transitions += 1
                session.add(short_url_object)
            await session.commit()
            return short_url_object
    #
    # @classmethod
    # async def disable_token(cls, short_url: SShortUrl) -> TokensOrm | None:
    #     async with new_session() as session:
    #         token = await session.scalar(select(TokensOrm).where(TokensOrm.short_url == short_url.short_url))
    #         if token is None:
    #             return token
    #         token.is_activ = False
    #         session.add(token)
    #         await session.commit()
    #         return token
    #
    # @classmethod
    # async def delete_token(cls, short_url: str):
    #     async with new_session() as session:
    #         token = await session.scalar(select(TokensOrm).where(TokensOrm.short_url == short_url))
    #         if token:
    #             await session.execute(delete(TokensOrm).where(TokensOrm.short_url == short_url))
    #             await session.commit()
    #             return True
    #         else:
    #             return False
    #
