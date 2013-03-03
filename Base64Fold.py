import re
import sublime, sublime_plugin

class FoldBase64Command(sublime_plugin.TextCommand):
  def run(self, edit):
    # Base64 decodes each 4 encoded characters into 3 octects. The padding '='
    # character might appear 1 or 2 times only at the end of the Base64 code,
    # and only if there are less than 3 octects to be decoded. We don't need to
    # match what (["');], etc) is behind the code, as we are not folding them.
    regions = self.view.find_all('(?<=base64\,)[\w\d\+\/]{2,}={0,2}')
    if regions:
      # Only fold Base64 code that has a valid length
      self.view.fold([r for r in regions if r.size() % 4 == 0])

class Base64Fold(sublime_plugin.EventListener):
  def on_load(self, view):
    prepare_fold(view)

  def on_pre_save(self, view):
    prepare_fold(view)

def prepare_fold(view):
  fold_any_file = False
  fold_file_extensions = []
  scope_package = "package"
  scope_sublime = "sublime"
  settings = {
    scope_package: sublime.load_settings("Base64 Fold.sublime-settings"),
    scope_sublime: view.settings()
  }
  # Settings override order:
  #   User/Preferences > User/Base64 Fold > Base64 Fold/Base64 Fold
  for scope in [scope_package, scope_sublime]:
    if settings[scope]:
      fold_any_file = settings[scope].get("base64fold_any_file", fold_any_file)
      fold_file_extensions = settings[scope].get("base64fold_file_extensions",
        fold_file_extensions)
  if fold_any_file:
    view.run_command('fold_base64')
  elif len(fold_file_extensions) > 0:
    file_name = view.file_name()
    if file_name:
      match = re.search('(?<=\.)[0-9a-z]+$', file_name, re.IGNORECASE)
      if match:
        extension = match.group(0)
        if extension in fold_file_extensions:
          view.run_command('fold_base64')
