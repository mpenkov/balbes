"""Fire up the browser to search for missing images."""

import os
import sys
import urllib.parse
import webbrowser
import unicodedata

import pyperclip

duckduckgo = 'https://duckduckgo.com/?t=canonical&q=%s&iax=images&ia=images&iaf=type%%3Aclipart'

images = {
    unicodedata.normalize('NFC', os.path.splitext(f)[0])
    for f in os.listdir('img')
}

with open(sys.argv[1]) as fin:
    for line in fin:
        try:
            syllable, word = line.strip().split(' ')
        except ValueError:
            continue

        word = unicodedata.normalize('NFC', word)
        if word not in images:
            pyperclip.copy(word)
            url = duckduckgo % urllib.parse.quote(word)
            webbrowser.open(url)
            input('searched for %r, press Enter to continue or Ctrl+C to exit' % word)
