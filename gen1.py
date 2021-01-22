"""Generate syllables of two letters (consonant-vowel pairs)."""

vowels = 'аеёиоуэя'
consonants = 'бгдзжйклмнпрстфхчшщ'

for c in consonants:
    for v in vowels:
        print(c+v)
