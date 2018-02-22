#!/usr/bin/env python

from builtins import object
import opscore.protocols.keys as keys
import opscore.protocols.types as types
from opscore.utility.qstr import qstr

class TopCmd(object):

    def __init__(self, actor):
        # This lets us access the rest of the actor.
        self.actor = actor

        # Declare the commands we implement. When the actor is started
        # these are registered with the parser, which will call the
        # associated methods when matched. The callbacks will be
        # passed a single argument, the parsed and typed command.
        #
        self.vocab = [
            ('ping', '', self.ping),
            ('status', '[@all]', self.status),
            ('monitor', '<controllers> <period>', self.monitor),
         ]

        # Define typed command arguments for the above commands.
        self.keys = keys.KeysDictionary("xcu_xcu", (1, 1),
                                        keys.Key("name", types.String(),
                                                 help='an optional name to assign to a controller instance'),
                                        keys.Key("controllers", types.String()*(1,None),
                                                 help='the names of 1 or more controllers to load'),
                                        keys.Key("controller", types.String(),
                                                 help='the names a controller.'),
                                        keys.Key("period", types.Int(),
                                                 help='the period to sample at.'),
                                        )

    def monitor(self, cmd):
        """ Enable/disable/adjust period controller monitors. """
        
        period = cmd.cmd.keywords['period'].values[0]
        controllers = cmd.cmd.keywords['controllers'].values

        knownControllers = ["gauge", "rough1", "heaters", "power"]
        for c in self.actor.config.get(self.actor.name, 'controllers').split(','):
            c = c.strip()
            knownControllers.append(c)
        
        foundOne = False
        for c in controllers:
            if c not in knownControllers:
                cmd.warn('text="not starting monitor for %s: unknown controller"' % (c))
                continue
                
            self.actor.monitor(c, period, cmd=cmd)
            foundOne = True

        if foundOne:
            cmd.finish()
        else:
            cmd.fail('text="no controllers found"')

    def controllerKey(self):
        controllerNames = list(self.actor.controllers.keys())
        key = 'controllers=%s' % (','.join([c for c in controllerNames]))

        return key
    

    def ping(self, cmd):
        """Query the actor for liveness/happiness."""

        cmd.inform("text='Present and (probably) well'")
        self.actor.startAllControllers()
        cmd.finish()

    def status(self, cmd):
        """Report camera status and actor version. """

        self.actor.sendVersionKey(cmd)
        
        cmd.inform('text=%s' % ("Present!"))
        cmd.inform('text="monitors: %s"' % (self.actor.monitors))
        cmd.inform('text="config id=0x%08x %r"' % (id(self.actor.config),
                                                   self.actor.config.sections()))

        if 'all' in cmd.cmd.keywords:
            for c in self.actor.controllers:
                self.actor.callCommand("%s status" % (c))
            
        cmd.finish(self.controllerKey())

