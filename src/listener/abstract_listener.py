'''
Created on Mar 17, 2013

@author: ber
'''
import multiprocessing




class AbstractListener (multiprocessing.Process):
    '''
    An abstract base class for gate listeners
    '''
    name = '*'


    def __init__(self, gate, port, queue, logger):
        '''
        Constructor
        '''
        super(AbstractListener, self).__init__()
        self.gate = gate
        self.portname = port
        self.queue = queue
        self.active = True
        self.logger = logger
        
        
    def open_port(self):
        raise NotImplemented()
    
    
    def read_port(self):
        raise NotImplemented()
    
    
    def read_id(self):
        raise NotImplemented()


    def read_msg(self):
        return (self.gate, self.read_id())


    def run(self):
        self.open_port()
        
        while self.active:
            msg = self.read_msg()
            if msg is not None:
                self.queue.put(msg)
                self.logger.log('Listener %(name)s on %(gate)s: %(msg)s' % 
                    { 'name':self.name, 'gate':self.gate, 'msg':msg }
                )
                
            
    def stop(self):
        self.active = False
