#!/usr/bin/env python

import opscore.protocols.keys as keys
import opscore.protocols.types as types


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
            raise RuntimeError('%s controller is not connected.' % (self.name))

    def ping(self, cmd):
        """Query the actor for liveness/happiness."""
        cmd.finish("text='Present and (probably) well'")

    def status(self, cmd):
        """Report status and version; obtain and send current data"""

        cmd.finish("text='ok'")

    def wipe(self, cmd):
        """Report status and version; obtain and send current data"""

        cmd.finish("text='ok'")

    def read(self, cmd):
        """Report status and version; obtain and send current data"""

        cmd.finish("text='ok'")

    def exposeBiases(self, cmd):
        """Report status and version; obtain and send current data"""

        cmd.finish("text='ok'")

    def fetchTemps(self, cmd):
        """Report status and version; obtain and send current data"""

        cmd.finish("text='ok'")
