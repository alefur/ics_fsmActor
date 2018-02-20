__author__ = 'alefur'
import logging


class PfsDevice(object):
    def __init__(self, actor, name, loglevel=logging.DEBUG):
        # This sets up the connections to/from the hub, the logger, and the twisted reactor.
        #

        self.actor = actor
        self.name = name
        self.logger = logging.getLogger(self.name)
        self.logger.setLevel(loglevel)

        self.sock = None

    def formatException(self, e, traceback=""):
        return "%s %s %s" % (str(type(e)).replace("'", ""), str(type(e)(*e.args)).replace("'", ""), traceback)
