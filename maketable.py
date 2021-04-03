"""Make a HTML table from a list of syllables.

Inject words and images where possible.
"""

import argparse
import json
import os
import sys
import unicodedata

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


def tabulate(contents, rows=7, columns=10):
    row = []
    table = []

    for c in contents:
        if len(table) == rows:
            yield table
            row = []
            table = []

        row.append(c)

        if len(row) == columns:
            table.append(row)
            row = []

    if row:
        table.append(row)

    if table:
        yield table


def find_image(word, subdir='img'):
    word = unicodedata.normalize('NFC', word)
    if word:
        for filename in os.listdir(subdir):
            filename = unicodedata.normalize('NFC', filename)
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


#
# https://stackoverflow.com/questions/18746538/how-to-add-text-over-a-overlapping-div-tag#18746701
# https://stackoverflow.com/questions/7273338/how-to-vertically-align-an-image-inside-a-div#7310398
#
print("""
<!DOCTYPE html>
<html>
  <head>
    <style>
      table td { border: 1px solid #999; }
      td { width: 110px; height: 110px; }
      img {
        max-width: 100%; max-height: 100%;
        width: auto; height: auto; margin: auto;
        position: absolute; left: 0; right: 0; top: 0; bottom: 0;
        z-index: -1;
      }
      .text { z-index: 1; }

      .container { position: relative; text-align: center; height: 100%; }

      .syllable {
        position: absolute; top: 0; left: 2px;
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


def transpose(table):
    cols = len(table[0])
    newtable = []

    def safeindex(row, i):
        try:
            return row[i]
        except IndexError:
            return '', ''

    for i in range(cols):
        newtable.append([safeindex(row, i) for row in table])
    return newtable


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--rows', default=5, type=int)
    parser.add_argument('--columns', default=5, type=int)
    parser.add_argument('--order', choices=('row', 'column'), default='row')
    args = parser.parse_args()

    rows, columns = args.rows, args.columns
    if args.order == 'column':
        rows, columns = columns, rows

    for table in tabulate(read_input(), rows=rows, columns=columns):
        if args.order == 'column':
            table = transpose(table)
        print_table(table)
        print('\n      <hr><p style="page-break-before: always">')

    print("""
      </body>
    </html>
    """)


if __name__ == '__main__':
    main()
