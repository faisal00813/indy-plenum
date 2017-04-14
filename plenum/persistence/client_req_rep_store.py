from abc import abstractmethod, abstractproperty
from typing import Any, Sequence

from ledger.serializers.compact_serializer import CompactSerializer
from plenum.common.request import Request


class ClientReqRepStore:
    @abstractmethod
    def __init__(self, *args, **kwargs):
        pass

    @abstractproperty
    def lastReqId(self) -> int:
        pass

    @abstractmethod
    def addRequest(self, req: Request):
        pass

    @abstractmethod
    def addAck(self, msg: Any, sender: str):
        pass

    @abstractmethod
    def addNack(self, msg: Any, sender: str):
        pass

    @abstractmethod
    def addReject(self, msg: Any, sender: str):
        pass

    @abstractmethod
    def addReply(self, identifier: str, reqId: int, sender: str,
                 result: Any) -> Sequence[str]:
        pass

    @abstractmethod
    def hasRequest(self, identifier: str, reqId: int) -> bool:
        pass

    @abstractmethod
    def getRequest(self, identifier: str, reqId: int) -> Request:
        pass

    @abstractmethod
    def getReplies(self, identifier: str, reqId: int):
        pass

    @abstractmethod
    def getAcks(self, identifier: str, reqId: int) -> dict:
        pass

    @abstractmethod
    def getNacks(self, identifier: str, reqId: int) -> dict:
        pass

    @abstractmethod
    def getRejects(self, identifier: str, reqId: int) -> dict:
        pass

    def getAllReplies(self, identifier: str, reqId: int):
        replies = self.getReplies(identifier, reqId)
        errors = self.getNacks(identifier, reqId)
        if not errors:
            errors = {**errors, **self.getRejects(identifier, reqId)}
        return replies, errors

    @abstractproperty
    def txnFieldOrdering(self):
        raise NotImplementedError

    # noinspection PyAttributeOutsideInit
    @property
    def txnSerializer(self):
        # if not self._serializer:
        #     self._serializer = CompactSerializer(fields=self.txnFieldOrdering)
        # return self._serializer
        return CompactSerializer(fields=self.txnFieldOrdering)
