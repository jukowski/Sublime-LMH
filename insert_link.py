import sublime, sublime_plugin
import sally
import os
from subprocess import call
import thread
import json
import functools 
import urllib

path = os.path.dirname(os.path.realpath(__file__))

class InsertLinkCommand(sublime_plugin.TextCommand):
  def msg(self, edit, body):
    data = json.loads(body);
    if data["action"] == "select":
        target_region = sublime.Region(data["offset_begin"], data["offset_end"])
        self.view.sel().clear()
        self.view.sel().add(target_region)
        return True
    if data["action"] == "insert":
        target_region = sublime.Region(data["offset_begin"], data["offset_end"])
        self.view.replace(edit, target_region, data["replaceString"])
        return True

  def doexec(self, url, data):
    args = ["java","-jar", "theoexec.jar" ,"--url", url, "--width", "530", "--height", "380", "--data"] + data
    call(args, cwd=path)

  def run(self, edit):
    client = sally.conn
    part = functools.partial(self.msg, edit);
    #part({"action":"select","offset_begin":394,"offset_end":402});
    id = client.registerCallback(part)
    text = self.view.substr(sublime.Region(0, self.view.size()))
    data = ["forward_destination=%s"%client.myqueue, "forward_correlation=%s"%id, "body=%s"%text];
    url = "http://mathhub.info:8983/sider-nnexus/app/link";
    thread.start_new_thread(self.doexec, (url, data))
    pass

