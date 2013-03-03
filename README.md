Base64 Fold
===========

Base64-encoded Data URIs are notoriously long and look ugly in text editors:

![](http://i.imgur.com/r7wHI.png)

Since you never edit these embeds, they are just sitting there, wasting space and irritating you by going beyond your screen width or wrapping to many lines.
This little plug-in makes use of Sublime Text folding to hide them:

![](http://i.imgur.com/YcTH6.png)

Problem solved: the URI is still there, but it's neatly folded and can be unfolded for inspection.

Installation
------------

You can install Base64 Fold through [Sublime Package Control](http://wbond.net/sublime_packages/package_control).

Don't forget about these default Sublime key shortcuts:

Fold:   ```ctrl+shift+]```

Unfold: ```ctrl+shift+[```

Settings
--------

By default, only Base64 code in CSS and HTML files (recognized by file extensions) will be folded. You can set it to fold in any file, or limit to specific file extensions, by adding your settings to user preferences file, which can be opened from menu `Preferences > Settings - User`.

For details, see `Packages/Base64 Fold/Base64 Fold.sublime-settings`, or the latest version [here](Base64 Fold.sublime-settings).
