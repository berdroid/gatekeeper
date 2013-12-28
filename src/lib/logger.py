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
import multiprocessing



class Logger (object):
    
    def __init__(self, logfile=sys.stdout):
        self.out = logfile
    
    
    def log(self, *args, **kwargs):
        ts = datetime.datetime.now().isoformat()
        msg = self.msg(args)
        self.write_log(ts, msg, **kwargs)
        
        
    def msg(self, args):
        return ' '.join(args) + '\n'
    
    
    def write_log(self, ts, msg, **kwargs):
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
        
        
    def write_log(self, ts, msg, do_syslog=True, **kwargs):
        if self.out is not None:
            super(SyslogLogger, self).write_log(ts, msg, **kwargs)
          
        if do_syslog:
            syslog.syslog(msg)


    def close(self):
        syslog.closelog()
        self.do_syslog = False
        
        

class SyslogMailLogger (SyslogLogger):
    
    def __init__(self, logfile=None):
        super(SyslogMailLogger, self).__init__(logfile)
        self.mail_server = None
        
        
    def open_maillog(self, host, port=0, username=None, password=None, body='', sender='bernhard.bender@web.de', recvr='ber.droid@googlemail.com', smtp_debug=False, starttls=False):
        self.mail_server = host
        self.port = port
        self.starttls = starttls
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
        
        try:
            smtp = smtplib.SMTP(host=self.mail_server, port=self.port)
            smtp.set_debuglevel(self.smtp_debug)
            
            if self.starttls:
                smtp.ehlo()
                smtp.starttls()
                smtp.ehlo()

            if self.username:
                smtp.login(self.username, self.password)
            smtp.sendmail(self.sender, [self.recvr], msg.as_string())
            smtp.quit()
        except Exception, e:
            super(SyslogMailLogger, self).write_log(ts, 'MailLog failed with %s' % e)
        
        
    def write_log(self, ts, msg, do_maillog=True, **kwargs):
        super(SyslogMailLogger, self).write_log(ts, msg, **kwargs)
        
        if do_maillog and self.mail_server is not None:
            try:
                mp = multiprocessing.Process(target=self.mail_log, name='SyslogMailLogger', kwargs={'ts':ts, 'log_msg':msg})
                mp.start()
                
                super(SyslogMailLogger, self).write_log(ts, 'MailLog succeeded', **kwargs)
            except Exception, e:
                super(SyslogMailLogger, self).write_log(ts, 'MailLog failed with %s' % e, **kwargs)
                
            
    def close(self):
        super(SyslogMailLogger).close()
        self.mail_server = None
        
        
        
if __name__ == '__main__':
    
    sm = SyslogMailLogger()
    sm.open_maillog('smtp.web.de', port=587, starttls=True, username='***', password='***')
    print '1', datetime.datetime.now().isoformat()
    sm.log('Test from stargate')
    print '2', datetime.datetime.now().isoformat()
    

