__author__ = 'alefur'
import logging

from fsmActor.fsm import States, Substates


class PfsDevice(object):
    def __init__(self, actor, name, events, substates, loglevel=logging.DEBUG):
        # This sets up the connections to/from the hub, the logger, and the twisted reactor.
        #

        self.actor = actor
        self.name = name
        self.logger = logging.getLogger(self.name)
        self.logger.setLevel(loglevel)

        self.states = States(stateChangeCB=self.statesCB)

        self.substates = Substates(topState=self.states,
                                   substates=substates,
                                   events=events,
                                   stateChangeCB=self.statesCB)

        self.substates.onLOADING = self.loadDevice
        self.substates.onINITIALISING = self.initDevice

        self.states.start()
        self.substates.start()

    def loadDevice(self, e):
        self.statesCB(e)
        try:
            self.loadCfg()
            self.startComm()

            self.states.toLoaded()
            self.substates.idle()
        except:
            self.substates.fail()
            raise

    def initDevice(self, e):
        self.statesCB(e)

        try:
            self.init()

            self.states.toOnline()
            self.substates.idle()
        except:
            self.substates.fail()
            raise

    def start(self, doInit=False):
        self.substates.load()
        if doInit:
            self.substates.init()

    def stop(self):
        self.states.toOff()


    def statesCB(self, e):

        try:
            cmd = e.cmd
        except AttributeError:
            cmd = self.actor.bcast

        self.updateStates(cmd=cmd)

    def updateStates(self, cmd):
        cmd.inform('%sFSM=%s,%s' % (self.name, self.states.current,  self.substates.current))


    def loadCfg(self):
        pass

    def startComm(self):
        pass

    def init(self):
        pass
