from dishka import Provider, Scope, provide

from domain.protocols.c3_gateway import IC3GateWay
from domain.protocols.memes_interactor import IMemesInteractor
from infra.db.uow import UnitOfWork
from logic.interactors.memes import MemesInteractor


class LogicProvider(Provider):
    scope = Scope.APP

    @provide(scope=Scope.REQUEST)
    def _memes_interactor(self, uow: UnitOfWork, c3_gateway: IC3GateWay) -> IMemesInteractor:
        return MemesInteractor(uow, c3_gateway)
