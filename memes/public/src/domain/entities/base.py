import uuid
from dataclasses import dataclass, field
from datetime import datetime


@dataclass(eq=False)
class BaseEntity:
    """Base entity class."""

    id: uuid.UUID = field(default_factory=uuid.uuid4, kw_only=True)
    created_at: datetime = field(default_factory=datetime.now, kw_only=True)

    def __hash__(self) -> int:
        """Entity hash base on id."""
        return hash(self.id)

    def __eq__(self, __value: "BaseEntity") -> bool:  # type: ignore
        """Compare entity id."""
        return self.id == __value.id
