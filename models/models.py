from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class TokensOrm(Base):
    __tablename__ = "tokens"
    id: Mapped[int] = mapped_column(primary_key=True)
    number_of_transitions: Mapped[int] = mapped_column(nullable=True)
    original_url: Mapped[str] = mapped_column(nullable=False)
    short_url: Mapped[str] = mapped_column(nullable=False)
    qr_code: Mapped[str] = mapped_column(nullable=False)
    is_activ: Mapped[bool] = mapped_column(default=True)


