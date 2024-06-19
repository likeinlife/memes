import uuid

from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class MemeORM(Base):
    __tablename__ = "meme"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, index=True, nullable=False)
    text: Mapped[str]
    image_name: Mapped[str]
    deleted: Mapped[bool]
