import sublime, sublime_plugin
import sally
import os

class SearchConceptsCommand(sublime_plugin.TextCommand):
  def msg(msg):
    print msg

  def run(self, edit):
    client = sally.conn
    id = client.registerCallback(self.msg)
    url = "http://mathhub.info:8983/defindexer/app/search?forward_destination="+client.myqueue+"&forward_correlation="+id;
    
    pass

