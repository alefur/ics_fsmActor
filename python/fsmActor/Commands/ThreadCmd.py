#!/usr/bin/env python

import opscore.protocols.keys as keys
import opscore.protocols.types as types

from fsmActor.wrap import threaded
import time

class ThreadCmd(object):
    def __init__(self, actor):
        # This lets us access the rest of the actor.
        self.actor = actor

        # Declare the commands we implement. When the actor is started
        # these are registered with the parser, which will call the
        # associated methods when matched. The callbacks will be
        # passed a single argument, the parsed and typed command.
        #
        self.vocab = [
            ('thread', 'status', self.status),
            ('thread', 'move', self.move)

        ]

        # Define typed command arguments for the above commands.
        self.keys = keys.KeysDictionary("fsm_ccd", (1, 1),
                                        keys.Key("obstime", types.String(),
                                                 help='official DATE-OBS string'),
                                        keys.Key("exptime", types.Float(),
                                                 help='official EXPTIME'),
                                        keys.Key("nbias", types.Int(),
                                                 help='number of biases to take'), )
        self.name = 'thread'

    @property
    def controller(self):
        try:
            return self.actor.controllers['thread']
        except KeyError:
            raise RuntimeError('ccd controller is not connected.')

    def ping(self, cmd):
        """Query the actor for liveness/happiness."""
        cmd.finish("text='Present and (probably) well'")

    @threaded
    def status(self, cmd):
        """Report status and version; obtain and send current data"""

        self.controller.updateStates(cmd=cmd)
        time.sleep(10)
        cmd.finish()


    @threaded
    def move(self, cmd):
        """Report status and version; obtain and send current data"""

        self.controller.substates.move(cmd=cmd)
        self.controller.updateStates(cmd=cmd)
        cmd.finish()