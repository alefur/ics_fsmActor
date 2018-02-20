import logging

from fsmActor.Controllers.device import PfsDevice


class ccd(PfsDevice):
    def __init__(self, actor, name, loglevel=logging.DEBUG):
        # This sets up the connections to/from the hub, the logger, and the twisted reactor.
        #
        PfsDevice.__init__(self, actor, name)

    def start(self):
        pass

    def stop(self):
        pass