"""Generate syllables of two letters (consonant-vowel pairs)."""

vowels = 'аеёиоуыэюя'
consonants = 'бвгдзжйклмнпрстфхцчшщ'

for c in consonants:
    for v in vowels:
        print(c+v)
