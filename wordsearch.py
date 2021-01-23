"""Look up Russian nouns in dictionary.

See http://bokrcorpora.narod.ru/frqlist/frqlist-en.html
"""
import io
import os
import sys
import urllib.request
import zipfile

URL = 'http://bokrcorpora.narod.ru/frqlist/lemma.al.zip'
LEMMA = 'lemma.al'

if not os.path.isfile(LEMMA):
    #
    # Not sure why zifile cannot read from fin directly, but it
    # appears to think the stream does not contain a zip file.
    #
    buf = io.BytesIO()
    with urllib.request.urlopen(URL) as fin:
        buf.write(fin.read())

    with zipfile.ZipFile(buf) as zf:
        with zf.open(LEMMA, 'r') as fin, open(LEMMA, 'wb') as fout:
            fout.write(fin.read())


assert os.path.isfile(LEMMA)


nouns = []

with open(LEMMA, encoding='windows-1251') as fin:
    fin.readline()
    for line in fin:
        word_rank, frequency, word, pos = line.strip().split(' ')
        if pos == 'noun':
            nouns.append(word)

for line in sys.stdin:
    prefix = line.strip()
    hits = [n for n in nouns if n.startswith(prefix)][:20]
    # hits = sorted([n for n in nouns if n.startswith(prefix)], key=lambda x: len(x))[:20]
    print(prefix, hits)
