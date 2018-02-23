from functools import partial
from opscore.utility.qstr import qstr


def threaded(func):
    @putMsg
    def wrapper(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except Exception as e:
            cmd = args[0]
            oneLiner = self.actor.cmdTraceback(e)
            cmd.fail('text=%s' % (qstr("command failed: %s" % oneLiner)))

    return wrapper


def putMsg(func):
    def wrapper(self, *args, **kwargs):
        self.actor.controllers[self.name].putMsg(partial(func, self, *args, **kwargs))

    return wrapper

