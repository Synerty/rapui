import logging

from twisted.internet.threads import deferToThread

logger = logging.getLogger()

__author__ = 'synerty'


def printFailure(failure):
    logger.error(failure)
    return failure


def deferToThreadWrap(funcToWrap):
    def func(*args, **kwargs):
        d = deferToThread(funcToWrap, *args, **kwargs)
        d.addErrback(printFailure)
        return d

    return func

