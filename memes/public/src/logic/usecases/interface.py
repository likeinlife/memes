import typing as tp

T_co = tp.TypeVar("T_co", covariant=True)


class IUseCase(tp.Protocol, tp.Generic[T_co]):
    async def __call__(self) -> T_co: ...
