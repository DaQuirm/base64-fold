import re
import sublime, sublime_plugin

class FoldBase64Command(sublime_plugin.TextCommand):
  def run(self, edit, fold_all_uris):

    whitespace = r'(?:\\?\n|[\t ])+'
    # Only fold Base64 code that has a valid length - ignoring whitespace
    base64_filter = lambda region: len(re.sub(whitespace, '', self.view.substr(region))) % 4 == 0
    if fold_all_uris:
      # fold all URIs if the option is enabled
      regexp = r'url\(([\'"])?[^;]+;([^,]+),([^\n\\]+?(?:\\\n[^\n\\]*?)*?)(?=\1?\))'
      match_index = 3 # third group
      base64_index = 2 # second group
      self.fold_by_pattern(regexp, base64_index, match_index, base64_filter)

    # fold the base64 URIs
    base64 = r'[\w\d+/]{2,}'
    # Base64 decodes each 4 encoded characters into 3 octects. The padding '='
    # character might appear 1 or 2 times only at the end of the Base64 code,
    # and only if there are fewer than 3 octects to be decoded. We don't need to
    # match what (["');], etc) is after the code, as they are not being folded.
    regexp = r'(base64),(' + base64 + r'(?:' + whitespace + base64 + r')*={0,2})'
    match_index = 2 # second group
    base64_index = 1 # first group

    self.fold_by_pattern(regexp, base64_index, match_index, base64_filter)

  def fold_by_pattern(self, regexp, base64_index, match_index, base64_region_filter):
    view_text = self.view.substr(sublime.Region(0, self.view.size()))

    def get_region_from_group(match, group_index):
      start = match.start(group_index)
      end = start + len(match.group(group_index))
      return sublime.Region(start, end)

    pattern = re.compile(regexp)
    for match in pattern.finditer(view_text):
      is_base64 = self.view.substr(get_region_from_group(match, base64_index)) == 'base64'
      fold_region = get_region_from_group(match, match_index)
      if not is_base64 or base64_region_filter(fold_region):
        self.view.fold(fold_region)

class Base64Fold(sublime_plugin.EventListener):
  def init_(self):
    active_view = sublime.active_window().active_view()
    self.on_load(active_view)
    for window in sublime.windows():
      self.on_load(window.active_view())

  def load_settings(self, view):
    fold_any_file = False
    fold_file_extensions = []
    fold_all_uris = False
    scope_package = 'package'
    scope_sublime = 'sublime'
    settings = {
      scope_package: sublime.load_settings('Base64 Fold.sublime-settings'),
      scope_sublime: view.settings()
    }
    # Settings override order:
    #   User/Preferences > User/Base64 Fold > Base64 Fold/Base64 Fold
    for scope in [scope_package, scope_sublime]:
      if settings[scope]:
        fold_any_file = settings[scope].get('base64fold_any_file', fold_any_file)
        fold_file_extensions = settings[scope].get(
          'base64fold_file_extensions',
          fold_file_extensions
        )
        fold_all_uris = settings[scope].get('base64fold_all_uris', fold_all_uris)

    return {
      'fold_any_file': fold_any_file,
      'fold_file_extensions': fold_file_extensions,
      'fold_all_uris': fold_all_uris
    }

  def on_load(self, view):
    active_view = sublime.active_window().active_view()
    self.settings = self.load_settings(active_view)
    self.fold(view)

  def on_pre_save(self, view):
    active_view = sublime.active_window().active_view()
    self.settings = self.load_settings(active_view)
    self.fold(view)

  def fold(self, view):
    gotta_fold = False
    # to fold or not to fold
    if self.settings.get('fold_any_file'):
      gotta_fold = True
    elif len(self.settings.get('fold_file_extensions')) > 0:
      file_name = view.file_name()
      if file_name:
        match = re.search('(?<=\.)[0-9a-z]+$', file_name, re.IGNORECASE)
        if match:
          extension = match.group(0)
          if extension in self.settings.get('fold_file_extensions'):
            gotta_fold = True

    if gotta_fold:
      view.run_command('fold_base64', { 'fold_all_uris': self.settings.get('fold_all_uris') })

def plugin_loaded():
  Base64Fold().init_()
