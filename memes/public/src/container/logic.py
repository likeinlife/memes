from dishka import Provider, Scope, provide

from domain.protocols.c3_gateway import IC3GateWay
from infra.db.uow import UnitOfWork
from logic.interactors.memes import MemesInteractor


class LogicProvider(Provider):
    scope = Scope.APP

    @provide
    def _memes_interactor(self, uow: UnitOfWork, c3_gateway: IC3GateWay) -> MemesInteractor:
        return MemesInteractor(uow, c3_gateway)
