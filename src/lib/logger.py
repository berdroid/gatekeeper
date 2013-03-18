'''
Created on Mar 18, 2013

@author: ber
'''
import sys
import datetime


class Logger (object):
    
    def __init__(self):
        self.out = sys.stdout
    
    
    def log(self, *args):
        ts = datetime.datetime.now().isoformat()
        self.out.write(ts + ': ' + ' '.join(args) + '\n')
        
