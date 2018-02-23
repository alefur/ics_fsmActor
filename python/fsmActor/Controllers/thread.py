import logging
import time
from functools import partial
from actorcore.QThread import QThread

from fsmActor.Controllers.device import PfsDevice


class thread(PfsDevice, QThread):
    def __init__(self, actor, name, loglevel=logging.DEBUG):
        # This sets up the connections to/from the hub, the logger, and the twisted reactor.
        #

        # here you define your substates available when device in ONLINE
        QThread.__init__(self, actor, name)
        QThread.start(self)

        substates = ['IDLE', 'MOVING', 'FAILED']

        # here you define  your event to pass from from substate to another
        events = [{'name': 'move', 'src': 'IDLE', 'dst': 'MOVING'},
                  {'name': 'rehome', 'src': 'IDLE', 'dst': 'HOMING'},
                  {'name': 'idle', 'src': ['MOVING', 'HOMING'], 'dst': 'IDLE'},
                  {'name': 'fail', 'src': ['MOVING', 'HOMING'], 'dst': 'FAILED'},
                  ]

        PfsDevice.__init__(self, actor, name, events, substates)

        self.addStateCB('MOVING', self.move)

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

    def move(self, e):
        try:
            e.cmd.inform("text='moving'")
            time.sleep(2)
            self.substates.idle()
        except:
            self.substates.fail()
            raise


    def handleTimeout(self):
        if self.exitASAP:
            raise SystemExit()