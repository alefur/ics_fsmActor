import fysom


class States(fysom.Fysom):
    def __init__(self, stateChangeCB):
        fysom.Fysom.__init__(self, {'initial': 'none',
                                    'events': [{'name': 'start', 'src': 'none', 'dst': 'OFF'},
                                               {'name': 'toLoaded', 'src': ['OFF', 'ONLINE'], 'dst': 'LOADED'},
                                               {'name': 'toOnline', 'src': 'LOADED', 'dst': 'ONLINE'},
                                               {'name': 'toOff', 'src': ['LOADED', 'ONLINE'], 'dst': 'OFF'}],
                                    })
        self.onOFF = stateChangeCB
        self.onLOADED = stateChangeCB
        self.onONLINE = stateChangeCB


class Substates(fysom.Fysom):
    def __init__(self, topState, substates, events, stateChangeCB):
        self.topState = topState
        self.dictState = {'OFF': ['IDLE', 'LOADING', 'FAILED'],
                          'LOADED': ['IDLE', 'INITIALISING', 'FAILED'],
                          'ONLINE': substates}

        events += [{'name': 'start', 'src': 'none', 'dst': 'IDLE'},
                   {'name': 'load', 'src': 'IDLE', 'dst': 'LOADING'},
                   {'name': 'init', 'src': 'IDLE', 'dst': 'INITIALISING'},
                   {'name': 'idle', 'src': ['LOADING', 'INITIALISING'], 'dst': 'IDLE'},
                   {'name': 'fail', 'src': ['LOADING', 'INITIALISING'], 'dst': 'FAILED'}]

        fysom.Fysom.__init__(self, {'initial': 'none', 'events': events})

        for state in substates:
            setattr(self, 'on%s' % state.upper(), stateChangeCB)

        for event in events:
            setattr(self, 'onbefore%s' % event['name'], self.checkTransition)

    def checkTransition(self, e):
        if e.dst not in self.dictState[self.topState.current]:
            raise fysom.FysomError('FysomError: event %s inappropriate in top state %s' % (e.event,
                                                                                           self.topState.current))

def stateCB(func):
    def wrapper(self, *args, **kwargs):
        self.statesCB(*args, **kwargs)

        return func(self, *args, **kwargs)
    return wrapper