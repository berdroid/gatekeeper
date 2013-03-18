'''
Created on Mar 18, 2013

@author: ber
'''

from connection import ConnectionError



class AbstractConnection (object):
    """
    abstract super class for connection objects
    """

    def __init__(self, name, params, logger):
        self.connection_name = name
        self.params = params
        self.log = logger
        
        self.log.log('Connection %s@%s: %s' % (self.name, self.connection_name, self.params))
        
        self.port = None


    def _fail(self, e):
        raise ConnectionError(self.connection_name + ' ' + str(e))


    def init_string(self):
        try:
            self.write(self.params.init_string)
        except AttributeError:
            pass


    def open(self, **kw):
        raise NotImplementedError('implement the connection methods')


    def close(self):
        raise NotImplementedError('implement the connection methods')


    def read(self):
        return self.port.read(1)


    def readline(self, timer=None, ui_update=lambda: None):
        ln = []
        while timer is None or not timer.expired():
            try:
                ui_update()

                c = self.read()
                ln.append(c)

                if c == '\r':
                    del ln[-1]
                elif c == '\n':
                    return ''.join(ln)

            except Exception, e:
                raise IOError(e)

        raise CommTimeOutError('timer expired')


    def write(self, data):
        self.port.write(data)



