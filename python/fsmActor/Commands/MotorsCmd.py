#!/usr/bin/env python

import opscore.protocols.keys as keys
import opscore.protocols.types as types


class MotorsCmd(object):
    def __init__(self, actor):
        # This lets us access the rest of the actor.
        self.actor = actor

        # Declare the commands we implement. When the actor is started
        # these are registered with the parser, which will call the
        # associated methods when matched. The callbacks will be
        # passed a single argument, the parsed and typed command.
        #
        self.vocab = [
            ('motors', 'status', self.status),
            ('motors', 'initialise', self.fullInit),
            ('motors', 'home [<axes>]', self.homeCcd),
            ('motors', 'moveCcd [<a>] [<b>] [<c>] [<piston>]', self.moveCcd),
        ]

        # Define typed command arguments for the above commands.
        self.keys = keys.KeysDictionary("fsm_motor", (1, 1),
                                        keys.Key("axes", types.String() * (1, 3),
                                                 help='list of motor names'),
                                        keys.Key("a", types.Float(),
                                                 help='the number of ticks/microns to move actuator A'),
                                        keys.Key("b", types.Float(),
                                                 help='the number of ticks/microns to move actuator B'),
                                        keys.Key("c", types.Float(),
                                                 help='the number of ticks/microns to move actuator C'),
                                        keys.Key("piston", types.Float(),
                                                 help='the number of ticks/microns to move actuators A,B, and C'),
                                        )

    @property
    def controller(self):
        try:
            return self.actor.controllers['motors']
        except KeyError:
            raise RuntimeError('motors controller is not connected.')

    def motorID(self, motorName):
        """ Translate from all plausible motor/axis IDs to the controller IDs. """

        motorNames = {'a':1, '1':1, 1:1,
                      'b':2, '2':2, 2:2,
                      'c':3, '3':3, 3:3}

        return motorNames[motorName]

    def initCcd(self, cmd):

        self.controller.initAxis(cmd, [1, 2, 3])
        self.status(cmd)

    def homeCcd(self, cmd):
        cmdKeys = cmd.cmd.keywords
        axes = cmdKeys['axes'].values if 'axes' in cmdKeys else [1, 2, 3]

        axes = [self.motorID(a) for a in axes]

        self.controller.substates.rehome(cmd=cmd, axes=axes)
        self.status(cmd)

    def fullInit(self, cmd):
        self.controller.substates.init(cmd=cmd)
        self.status(cmd)

    def moveCcd(self, cmd):
        cmdKeys = cmd.cmd.keywords

        a = cmdKeys['a'].values[0] if 'a' in cmdKeys else None
        b = cmdKeys['b'].values[0] if 'b' in cmdKeys else None
        c = cmdKeys['c'].values[0] if 'c' in cmdKeys else None
        piston = cmdKeys['piston'].values[0] if 'piston' in cmdKeys else None

        if piston is not None:
            a = b = c = piston

        cmdStr = "P%s,%s,%s,R" % (int(a) if a is not None else '',
                                  int(b) if b is not None else '',
                                  int(c) if c is not None else '')

        self.controller.substates.move(cmd=cmd, cmdStr=cmdStr)
        self.status(cmd)

    def status(self, cmd):
        """Report status and version; obtain and send current data"""

        self.controller.updateStates(cmd=cmd)
        for m_i in range(3):
            m = m_i + 1
            cmd.inform('ccdMotor%d=%s,%s,%s,%s,%0.2f' % (m,
                                                         'OK',
                                                         '0',
                                                         '0',
                                                         '100',
                                                         0.00))

        cmd.finish()
