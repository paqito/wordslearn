ENG_WORD_TYPES = [
    ('noun', 'Noun'),
    ('verb', 'Verb'),
    ('adjective', 'Adjective'),
    ('adverb', 'Adverb'),
    ('preposition', 'Preposition'),
    ('Conjunctions', 'Conjunctions'),
    ('other', 'Other')]

POL_WORD_TYPES = [
    ('Noun', 'rzeczownik'),
    ('Verb', 'czasownik'),
    ('Adjective', 'przymiotnik'),
    ('Adverb', 'przyslowek'),
    ('Preposition', 'przyimek'),
    ('Conjunctions', 'spójnik'),
    ('Other', 'inne')]


# translation from wordDetail to Module type
wordType_conversion = {
        'noun': 'Noun',
        'verb': 'Verb',
        'adjective': 'Adjective',
        'adverb': 'Adverb',
        'preposition': 'Preposition',
        'conjunctions': 'Conjunctions',
        'other': 'Other'
}