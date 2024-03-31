import base64
import io
import os

import qrcode
from sqlalchemy import select, delete

from config import SERVER_HOST_ADDR
from database import new_session
from models.models import TokensOrm
from schemes import SToken, SUrl, SShortUrl


class TokenRepository:

    @classmethod
    async def create_token(cls, original_url: SUrl) -> SToken:
        async with new_session() as session:
            short_url = os.urandom(8).hex()
            qr_code = qrcode.make(SERVER_HOST_ADDR + short_url)
            buffer = io.BytesIO()
            qr_code.save(buffer, "PNG")
            qr_code_str = base64.b64encode(buffer.getvalue()).decode("utf-8")

            token = TokensOrm(
                number_of_transitions=0,
                original_url=original_url.url,
                short_url=short_url,
                qr_code=qr_code_str
            )
            session.add(token)
            await session.commit()
            return SToken.model_validate(token)

    @classmethod
    async def get_all_tokens(cls) -> [SToken]:
        async with new_session() as session:
            query = select(TokensOrm)
            result = await session.execute(query)
            token_models = result.scalars().all()
            tokens = [SToken.model_validate(token_model) for token_model in token_models]
            return tokens

    @classmethod
    async def get_url(cls, short_url: str) -> SToken | None:
        async with new_session() as session:
            token = await session.scalar(select(TokensOrm).where(TokensOrm.short_url == short_url))
            if token is None:
                return token
            if token.is_activ:
                token.number_of_transitions += 1
                session.add(token)
            await session.commit()
            return token

    @classmethod
    async def disable_token(cls, short_url: SShortUrl) -> TokensOrm | None:
        async with new_session() as session:
            token = await session.scalar(select(TokensOrm).where(TokensOrm.short_url == short_url.short_url))
            if token is None:
                return token
            token.is_activ = False
            session.add(token)
            await session.commit()
            return token

    @classmethod
    async def delete_token(cls, short_url: str):
        async with new_session() as session:
            token = await session.scalar(select(TokensOrm).where(TokensOrm.short_url == short_url))
            if token:
                await session.execute(delete(TokensOrm).where(TokensOrm.short_url == short_url))
                await session.commit()
                return True
            else:
                return False

