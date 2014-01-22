import sublime, sublime_plugin
import httplib, urllib
import json
import stomp

class ShowSallyFramesCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    view = self.view;
    (line, col) = view.rowcol(locations[0])
    request = {"file" : view.file_name(), "line" : line, "col" : col, "content": view.substr(sublime.Region(0, view.size()))}

class STeXAutocomplete(sublime_plugin.EventListener):
  def __init__(self):
    self.url = "http://localhost:8082"

  def post(self, service, data):
    params = json.dumps(data);
    res = None
    try:
      conn = httplib.HTTPConnection("localhost", 8082)
      headers = {"Content-type": "application/json", "Accept": "application/json"}
      conn.request("POST", "/"+service, params, headers)
      res = conn.getresponse()
      res = json.loads(res.read())
    except Exception, e:
      return [];
    return res

  def on_query_completions(self, view, prefix, locations):
    if view.settings().get('syntax') != "Packages/LaTeX/LaTeX.tmLanguage":
      return [];
    (line, col) = view.rowcol(locations[0])
    request = {"file" : view.file_name(), "line" : line, "col" : col, "content": view.substr(sublime.Region(0, view.size()))}

    res = [(prefix+auto,)*2 for auto in self.post("autocomplete", request)]

    return res;
