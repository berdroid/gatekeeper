'''
Created on Mar 18, 2013

@author: ber
'''
import sys
import datetime
import StringIO
import syslog
import smtplib
import email.mime.text


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
        self.do_syslog = False


    def open_syslog(self, ident='LOG', facility=syslog.LOG_LOCAL0):
        syslog.openlog(ident=ident, facility=facility)
        self.do_syslog = True
        
        
    def write_log(self, ts, msg):
        if self.out is not None:
            super(SyslogLogger, self).write_log(ts, msg)
            
        syslog.syslog(msg)


    def close(self):
        syslog.closelog()
        self.do_syslog = False
        
        

class SyslogMailLogger (SyslogLogger):
    
    def __init__(self, logfile=None):
        super(SyslogMailLogger, self).__init__(logfile)
        self.mail_server = None
        
        
    def open_maillog(self, host, port=0, username=None, password=None, body='', sender='bernhard.bender@web.de', recvr='ber.droid@googlemail.com', smtp_debug=False):
        self.mail_server = host
        self.port = port
        self.username = username
        self.password = password
        self.body = body
        self.sender = sender
        self.recvr = recvr
        self.smtp_debug = smtp_debug
        
        
    def mail_log(self, ts, log_msg):
        msg = email.mime.text.MIMEText(self.body)
        msg['Subject'] = log_msg + ' ' + ts
        msg['From'] = self.sender
        msg['To'] = self.recvr
        
        smtp = smtplib.SMTP(self.mail_server)
        smtp.set_debuglevel(self.smtp_debug)
        if self.username:
            smtp.login(self.username, self.password)
        smtp.sendmail(self.sender, [self.recvr], msg.as_string())
        smtp.quit()
        
        
    def write_log(self, ts, msg):
        super(SyslogMailLogger, self).write_log(ts, msg)
        
        if self.mail_server is not None:
            try:
                self.mail_log(ts, msg)
                super(SyslogMailLogger, self).write_log(ts, 'MailLog succeded')
            except Exception, e:
                super(SyslogMailLogger, self).write_log(ts, 'MailLog failed with %s' % e)
                
            
    def close(self):
        super(SyslogMailLogger).close()
        self.mail_server = None
        
        
        
if __name__ == '__main__':
    
    sm = SyslogMailLogger()
    sm.open_maillog('smtp.web.de', port=465, username='***', password='***')
    sm.log('Test from stargate')
    

        