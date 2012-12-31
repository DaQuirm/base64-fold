import re
import sublime, sublime_plugin

class FoldBase64Command(sublime_plugin.TextCommand):
  def run(self, edit):
    regions = self.view.find_all('(?<=base64\,)[\w\d\+\/=]+(?=\);)')
    if regions:
      self.view.fold(regions)

class Base64Fold(sublime_plugin.EventListener):
  def on_load(self, view):
    style_files_exts = ['.css', '.less', '.sass', '.scss']
    file_name = view.file_name()
    if file_name:
      match = re.search('\.[0-9a-z]+$', file_name, re.IGNORECASE)
      if match:
        extension = match.group(0)
        if extension in style_files_exts:
          view.run_command('fold_base64')
