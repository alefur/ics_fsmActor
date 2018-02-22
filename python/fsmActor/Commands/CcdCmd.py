#!/usr/bin/env python

import opscore.protocols.keys as keys
import opscore.protocols.types as types
import time

class CcdCmd(object):
    def __init__(self, actor):
        # This lets us access the rest of the actor.
        self.actor = actor

        # Declare the commands we implement. When the actor is started
        # these are registered with the parser, which will call the
        # associated methods when matched. The callbacks will be
        # passed a single argument, the parsed and typed command.
        #
        self.vocab = [
            ('ccd', 'status', self.status),
            ('ccd', 'wipe', self.wipe),
            ('ccd', 'read [@(bias|dark|flat|arc|object|junk)] [<exptime>] [<obstime>]', self.read),
            ('ccd', 'expose <nbias>', self.exposeBiases),
            ('ccd', 'temps', self.fetchTemps),

        ]

        # Define typed command arguments for the above commands.
        self.keys = keys.KeysDictionary("fsm_ccd", (1, 1),
                                        keys.Key("obstime", types.String(),
                                                 help='official DATE-OBS string'),
                                        keys.Key("exptime", types.Float(),
                                                 help='official EXPTIME'),
                                        keys.Key("nbias", types.Int(),
                                                 help='number of biases to take'), )

    @property
    def controller(self):
        try:
            return self.actor.controllers['ccd']
        except KeyError:
            raise RuntimeError('ccd controller is not connected.')

    def ping(self, cmd):
        """Query the actor for liveness/happiness."""
        cmd.finish("text='Present and (probably) well'")

    def status(self, cmd):
        """Report status and version; obtain and send current data"""

        self.controller.updateStates(cmd=cmd)
        cmd.finish()

    def wipe(self, cmd):
        """Report status and version; obtain and send current data"""
        self.controller.substates.wipe(cmd=cmd)
        time.sleep(3)
        self.controller.substates.integrate(cmd=cmd)
        cmd.finish("text='wiped'")

    def read(self, cmd):
        """Report status and version; obtain and send current data"""
        self.controller.substates.read(cmd=cmd)
        time.sleep(5)
        self.controller.substates.idle(cmd=cmd)
        cmd.finish("text='read done'")

    def exposeBiases(self, cmd):
        """Report status and version; obtain and send current data"""

        cmd.finish("text='ok'")

    def fetchTemps(self, cmd):
        """Report status and version; obtain and send current data"""

        cmd.finish("text='ok'")
