import sublime, sublime_plugin
import sally
import os
from subprocess import call
import thread
import json
import functools 

path = os.path.dirname(os.path.realpath(__file__))

class SearchConceptsCommand(sublime_plugin.TextCommand):
  def msg(self, edit, body):
    data = json.loads(body);
    strInsert = "\\termref{"+data["symbol"]+"}{}{"+data["symbol"]+"}";

    the_sels = self.view.sel()
    for a_sel in the_sels:
      self.view.replace(edit, a_sel, strInsert)

  def doexec(self, url):
    call(["java","-jar", "theoexec.jar" ,"--url", url], cwd=path)

  def run(self, edit):
    client = sally.conn
    part = functools.partial(self.msg, edit);
    id = client.registerCallback(part)
    url = "http://mathhub.info:8983/defindexer/app/search?forward_destination=%s&forward_correlation=%s"%(client.myqueue,id);
    thread.start_new_thread(self.doexec, (url, ))
    pass

