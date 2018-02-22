import logging
import time
from functools import partial

from fsmActor.Controllers.device import PfsDevice


class ccd(PfsDevice):
    def __init__(self, actor, name, loglevel=logging.DEBUG):
        # This sets up the connections to/from the hub, the logger, and the twisted reactor.
        #

        # here you define your substates available when device in ONLINE

        substates = ['IDLE', 'WIPING', 'INTEGRATING', 'READING', 'ABORTED']

        # here you define  your event to pass from from substate to another
        events = [{'name': 'wipe', 'src': 'IDLE', 'dst': 'WIPING'},
                  {'name': 'integrate', 'src': 'WIPING', 'dst': 'INTEGRATING'},
                  {'name': 'read', 'src': 'INTEGRATING', 'dst': 'READING'},
                  {'name': 'idle', 'src': 'READING', 'dst': 'IDLE'},
                  {'name': 'abort', 'src': ['WIPED', 'INTEGRATING', 'READING'], 'dst': 'ABORTED'},
                  {'name': 'clear', 'src': 'ABORTED', 'dst': 'IDLE'}
                  ]

        PfsDevice.__init__(self, actor, name, events, substates)

        # not all devices need to have a manual init command, in that case the initialision is done automatically
        self.start = partial(PfsDevice.start, self, doInit=True)

    def loadCfg(self, cmd):
        time.sleep(1)
        cmd.inform("text='Config Loaded'")

    def startComm(self, cmd):
        time.sleep(1)
        cmd.inform("text='Communication established with controller'")

    def init(self, cmd):
        time.sleep(1)
        cmd.inform("text='Init Device OK'")
