from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.database import Base


class UrlModel(Base):
    __tablename__ = "url"
    id: Mapped[int] = mapped_column(primary_key=True)
    original_url: Mapped[str] = mapped_column(nullable=False)
    short_urls: Mapped[list["ShortUrlsModel"]] = relationship(back_populates="url", uselist=True)


class ShortUrlsModel(Base):
    __tablename__ = "short_url"
    id: Mapped[int] = mapped_column(primary_key=True)
    url_id: Mapped[int] = mapped_column(ForeignKey("url.id", ondelete="CASCADE"))
    url: Mapped["UrlModel"] = relationship(back_populates="short_urls", uselist=True)
    number_of_transitions: Mapped[int] = mapped_column(nullable=True)
    short_url: Mapped[str] = mapped_column(nullable=False, unique=True)
    qr_code: Mapped[str] = mapped_column(nullable=False)
    three_words: Mapped[str] = mapped_column(nullable=False)
    is_activ: Mapped[bool] = mapped_column(default=True)
