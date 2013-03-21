'''
Created on Mar 18, 2013

@author: ber
'''
import sys
import datetime
import StringIO


class Logger (object):
    
    def __init__(self, logfile=sys.stdout):
        self.out = logfile
    
    
    def log(self, *args):
        ts = datetime.datetime.now().isoformat()
        self.out.write(ts + ': ' + ' '.join(args) + '\n')
        
        
    def close(self):
        pass
        
        

class StringIOLogger (Logger):
    
    def __init__(self):
        self.io = StringIO.StringIO()
        super(StringIOLogger, self).__init__(self.io)
        
        
    def close(self):
        self.io.close()
        
        
    def value(self):
        return self.io.getvalue()
        
