import time
import sys

import stomp 
import uuid
import random 

class SallyClient(object):
  def on_error(self, headers, message):
    print('received an error %s' % message)

  def on_message(self, headers, message):
    corrid = headers["correlation-id"];
    callback = self.corrMap[corrid]
    self.corrMap[corrid] = None

    if callback == None:
      print "No callback for correlation id %s"%corrid;

    callback(message) 

  def gen_correlation(self):
    return str(self.rand.randint(0, 1000000));

  def __init__(self): 
    conn = stomp.Connection(host_and_ports=[("mathhub.info", 61613)])
    conn.set_listener('', self)
    conn.start() 
    conn.connect(username="admin", passcode="password")
    self.corrMap = {};
    self.conn = conn;
    self.rand = random.Random();
    self.myqueue = "/queue/sublime_client_"+str(uuid.uuid4());
    self.headers = {"reply-to" : self.myqueue};
    conn.subscribe(destination=self.myqueue, id=1, ack='auto')
    pass

  def __del__(self):
    self.conn.unsubscribe(destination=self.myqueue, id=1)

  def registerCallback(self, callback):
    self.gen_correlation();
    self.corrMap[corr] = callback;

  def send(self, body, destination, callback = None):
    newHeaders = self.headers.copy();
    if callback:
      corr = self.registerCallback(callback)
      newHeaders["correlation-id"] = corr;
    self.conn.send(body=body, destination=destination, headers=newHeaders)
    pass

conn = SallyClient() 