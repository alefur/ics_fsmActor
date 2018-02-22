import logging
import time

from fsmActor.Controllers.device import PfsDevice
from functools import partial

class ccd(PfsDevice):
    def __init__(self, actor, name, loglevel=logging.DEBUG):
        # This sets up the connections to/from the hub, the logger, and the twisted reactor.
        #

        events = [{'name': 'wipe', 'src': 'IDLE', 'dst': 'WIPED'},
                  {'name': 'integrating', 'src': 'WIPED', 'dst': 'INTEGRATING'},
                  {'name': 'read', 'src': 'INTEGRATING', 'dst': 'READING'},
                  {'name': 'idle', 'src': 'READING', 'dst': 'IDLE'},
                  {'name': 'abort', 'src': ['WIPED', 'INTEGRATING', 'READING'], 'dst': 'ABORTED'},
                  {'name': 'clear', 'src': 'ABORTED', 'dst': 'IDLE'}
                  ]
        substates = ['IDLE', 'WIPED', 'INTEGRATING', 'READING', 'ABORTED']

        PfsDevice.__init__(self, actor, name, events, substates)

        self.start = partial(PfsDevice.start, self, doInit=True)

    def loadCfg(self):
        print ('Loading Config')
        time.sleep(0.5)

    def startComm(self):
        print ('Starting Communication')
        time.sleep(0.5)

    def init(self):
        print ('INITIALISATION')
        time.sleep(0.5)
