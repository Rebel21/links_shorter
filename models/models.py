from typing import List

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.database import Base


class UrlOrm(Base):
    __tablename__ = "url"
    id: Mapped[int] = mapped_column(primary_key=True)
    original_url: Mapped[str] = mapped_column(nullable=False)
    short_urls: Mapped[list["ShortUrlsOrm"]] = relationship(back_populates="url", uselist=True, lazy="selectin")


class ShortUrlsOrm(Base):
    __tablename__ = "short_url"
    id: Mapped[int] = mapped_column(primary_key=True)
    url_id: Mapped[int] = mapped_column(ForeignKey("url.id", ondelete="CASCADE"))
    url: Mapped["UrlOrm"] = relationship(back_populates="short_urls", uselist=False)
    number_of_transitions: Mapped[int] = mapped_column(nullable=True)
    short_url: Mapped[str] = mapped_column(nullable=False)
    qr_code: Mapped[str] = mapped_column(nullable=False)
    is_activ: Mapped[bool] = mapped_column(default=True)
