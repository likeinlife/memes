from domain.entities.memes import Meme
from domain.values.meme_text import MemeText
from infra.db.models import MemeORM


class MemeORMDomainMapper:
    @staticmethod
    def from_orm(orm: MemeORM) -> Meme:
        return Meme(
            id=orm.id,
            created_at=orm.created_at,
            image_name=orm.image_name,
            text=MemeText(orm.text),
            deleted=orm.deleted,
        )

    @staticmethod
    def to_orm(domain: Meme) -> MemeORM:
        return MemeORM(
            id=domain.id,
            image_name=domain.image_name,
            text=domain.text.as_generic_type(),
            deleted=domain.deleted,
        )
