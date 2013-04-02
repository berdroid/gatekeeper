'''
Created on Mar 18, 2013

@author: ber
'''
import sys
import datetime
import StringIO
import syslog


class Logger (object):
    
    def __init__(self, logfile=sys.stdout):
        self.out = logfile
    
    
    def log(self, *args):
        ts = datetime.datetime.now().isoformat()
        msg = self.msg(args)
        self.write_log(ts, msg)
        
        
    def msg(self, args):
        return ' '.join(args) + '\n'
    
    
    def write_log(self, ts, msg):
        self.out.write(ts + ': ' + msg)
        
        
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
        


class SyslogLogger (Logger):
    
    def __init__(self, logfile=None):
        super(SyslogLogger, self).__init__(logfile=logfile)


    def open_syslog(self, ident='LOG', facility=syslog.LOG_LOCAL0):
        syslog.openlog(ident=ident, facility=facility)
        
        
    def write_log(self, ts, msg):
        if self.out is not None:
            super(SyslogLogger, self).write_log(ts, msg)
            
        syslog.syslog(msg)


    def close(self):
        syslog.closelog()
        
        
        