"""Look up Russian nouns in dictionary.

See http://bokrcorpora.narod.ru/frqlist/frqlist-en.html
"""
import sys

nouns = []

with open('lemma.al', encoding='windows-1251') as fin:
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
