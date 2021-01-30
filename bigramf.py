"""Calculate bigram frequency of a text.

You can get some text here::

    https://getlib.ru/detskoe/skazka/1057-sbornik-russkie-narodnye-skazki.html

Example usage::

    iconv -f cp1251 -t utf-8 ~/Downloads/sbornik_._klassikavshko._russkie_narodnyie_skazki.txt | python bigramf.py | head -n 25

"""
import collections
import re
import sys

counter = collections.Counter()


def extract_bigrams(text):
    words = re.sub(r'\s+', ' ', text).lower().strip().split(' ')
    for word in words:
        for i in range(1, len(word)):
            yield word[i-1:i+1]


for line in sys.stdin:
    for bigram in extract_bigrams(line):
        counter[bigram] += 1

for bigram, count in counter.most_common(100):
    print(bigram, count)
