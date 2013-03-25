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
        super(AbstractListener, self).__init__(name=self.name + '@' + gate)
        self.gate = gate
        self.port = port
        self.queue = queue
        self.active = True
        self.logger = logger
        
        
    def read_id(self):
        raise NotImplemented()


    def read_msg(self):
        msg_id = self.read_id()
        if msg_id is not None:
            return (self.gate, msg_id)
        else:
            return None


    def run(self):
        self.port.open()
        
        while self.active:
            msg = self.read_msg()
            if msg is not None:
                self.queue.put(msg)
                self.logger.log('Listener %(name)s on %(gate)s: %(msg)s' % 
                    { 'name':self.name, 'gate':self.gate, 'msg':msg }
                )
                
        self.port.close()
        
            
    def stop(self):
        self.active = False
