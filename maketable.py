"""Make a HTML table from a list of syllables.

Inject words and images where possible.
"""

import json
import os
import sys

if not os.path.isdir('img'):
    os.mkdir('img')


def read_input():
    for line in sys.stdin:
        try:
            syllable, word = line.strip().split(' ', 1)
        except ValueError:
            syllable = line.strip()
            word = ''
        yield syllable, word


def tabulate(contents, rows=6, columns=5):
    row = []
    table = []

    for c in contents:
        if len(table) == rows:
            yield table
            row = []
            table = []
        if len(row) == columns:
            table.append(row)
            row = []

        row.append(c)

    if table:
        yield table


def find_image(word, subdir='img'):
    if word:
        for filename in os.listdir(subdir):
            name, ext = os.path.splitext(filename)
            if name == word:
                return os.path.join(subdir, filename)

    return os.path.join(subdir, 'placeholder.png')


if os.path.isfile('img/style.json'):
    with open('img/style.json') as fin:
        image_style = json.load(fin)
else:
    image_style = {}


def print_table(table):
    indent = 4
    print(' ' * indent + '<table>')
    indent += 2
    for row in table:
        print(' ' * indent + '<tr>')
        indent += 2
        for syllable, word in row:
            print(' ' * indent + '<td>')
            print(' ' * indent + '<div class="container">')
            indent += 2
            print(' ' * indent + '<span class="text top-left syllable">%s</span>' % syllable)
            if word:
                print(' ' * indent + '<span class="text bottom-left word">%s</span>' % word)
            imgpath = find_image(word)
            if imgpath:
                print(' ' * indent + '<img src="%s" style="%s">' % (imgpath, image_style.get(word)))
            indent -= 2
            print(' ' * indent + '</div>')
            print(' ' * indent + '</td>')
        indent -= 2
        print(' ' * indent + '</tr>')
    indent -= 2
    print(' ' * indent + '</table>')


print("""
<html>
  <head>
    <style>
      table td { border: 1px solid #333; }
      td { width: 145px; height: 145px; }
      img { max-width: 145px; max-height: 145px; width: 100%; height: auto; z-index: -1; }
      .text { z-index: 1; }

      .container { position: relative; text-align: center; height: 100%; }

      .syllable {
        position: absolute; top: 2px; left: 4px;
        font-size: xxx-large;
        color: red;
        text-shadow: -1px 1px 0 #fff, 1px 1px 0 #fff, 1px -1px 0 #fff, -1px -1px 0 #fff;
      }

      .word {
        position: absolute; bottom: 2px; right: 4px;
        font-size: x-large;
        color: gray;
        text-shadow: -1px 1px 0 #fff, 1px 1px 0 #fff, 1px -1px 0 #fff, -1px -1px 0 #fff;
      }
    </style>
  </head>
  <body>
""")

for table in tabulate(read_input()):
    print_table(table)
    print('\n      <hr><p style="page-break-before: always">')

print("""
  </body>
</html>
""")
