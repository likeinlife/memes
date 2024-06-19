from functools import lru_cache

from dishka import Container, Provider, Scope, make_container, provide

from domain.protocols.c3_gateway import IC3GateWay
from domain.protocols.memes_interactor import IMemesInteractor
from infra.services.c3.mock import MockC3Gateway

from .dependencies.mock_interactor import MockMemesInteractor


class MockProvider(Provider):
    scope = Scope.APP

    @provide
    def _c3(self) -> IC3GateWay:
        return MockC3Gateway()

    @provide
    def _memes_interactor(self, c3_gateway: IC3GateWay) -> IMemesInteractor:
        return MockMemesInteractor(c3_gateway)


@lru_cache(1)
def get_test_container() -> Container:
    return make_container(MockProvider())
