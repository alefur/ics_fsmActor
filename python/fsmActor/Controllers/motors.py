import logging
import time

from fsmActor.Controllers.device import PfsDevice
from fsmActor.fsm import stateCB

class motors(PfsDevice):
    def __init__(self, actor, name, loglevel=logging.DEBUG):
        # This sets up the connections to/from the hub, the logger, and the twisted reactor.
        #

        # here you define your substates available when device in ONLINE

        substates = ['IDLE', 'MOVING', 'HOMING', 'FAILED']

        # here you define  your event to pass from from substate to another
        events = [{'name': 'move', 'src': 'IDLE', 'dst': 'MOVING'},
                  {'name': 'rehome', 'src': 'IDLE', 'dst': 'HOMING'},
                  {'name': 'idle', 'src': ['MOVING', 'HOMING'], 'dst': 'IDLE'},
                  {'name': 'fail', 'src': ['MOVING', 'HOMING'], 'dst': 'FAILED'},
                  ]

        PfsDevice.__init__(self, actor, name, events, substates)
        self.substates.onHOMING = self.reHomeCcd
        self.substates.onMOVING = self.moveCcd

    def loadCfg(self, cmd):
        time.sleep(1)
        cmd.inform("text='Config Loaded'")

    def startComm(self, cmd):
        time.sleep(1)
        cmd.inform("text='Communication established with controller'")

    def init(self, cmd):

        self.initAxes(cmd=cmd, axes=[1, 2, 3])
        self.homeCcd(cmd=cmd, axes=[1, 2, 3])

        cmd.inform("text='Init Device OK'")

    def initAxes(self, cmd, axes):
        for m in axes:
            time.sleep(0.5)
            cmd.inform("text='init axes%i'" % m)

    def homeCcd(self, cmd, axes):
        for m in axes:
            time.sleep(2)
            cmd.inform("text='homing axes%i'" % m)

    @stateCB
    def reHomeCcd(self, e):
        try:
            self.homeCcd(cmd=e.cmd, axes=e.axes)
            self.substates.idle()
        except:
            self.substates.fail()
            raise

    @stateCB
    def moveCcd(self, e):
        try:
            time.sleep(2)
            e.cmd.inform("text='moving motors %s'" % e.cmdStr)
            self.substates.idle()
        except:
            self.substates.fail()
            raise
