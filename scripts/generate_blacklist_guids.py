import itertools, re
from website.app import init_app


BLACKLIST_WORDS = ['bad']
ALPHABET = '23456789abcdefghijkmnpqrstuvwxyz'


def main():
    init_app(set_backends=True)
    blacklist = generate_blacklist(BLACKLIST_WORDS)
    all_combinations = itertools.combinations_with_replacement(ALPHABET, 5)
    blacklist_guids = []
    for word in blacklist:
        for guid in list(all_combinations):
            guid = ''.join(guid)
            for i in range(0, n_positions(word, 5)):
                blacklist_guid = put(word, guid, i)
                blacklist_guids.append(blacklist_guid)


def generate_blacklist(blacklist):
    result = []
    result += BLACKLIST_WORDS
    for word in blacklist:
        result += drop_vowel(word)
        result += words_with_ck(word)
    return result


def drop_vowel(word, minimum=3):
    result = []
    vowels = 'aeiou'
    found_indexes = get_matched_letters_index(word, vowels)

    # generate all possible combinations of vowel locations
    positions = list(itertools.product(range(0, 2), repeat=len(found_indexes)))
    for item in positions:
        word_list = [w for w in word]
        for idx, value in enumerate(item):
            if value == 1:
                word_list[found_indexes[idx]] = ''

        final = ''.join(word_list)
        if len(final) >= minimum:
            result.append(final)

    return result


def get_matched_letters_index(word, letters):
    found_indices = []
    for found in re.finditer('[' + letters + ']', word):
        found_indices.append(found.span()[0])
    return found_indices


def words_with_ck(word):
    result = []
    if 'ck' in word:
        result.append(word)
        substitutions = ['c', 'cc', 'k', 'kk']
        for s in substitutions:
            new_word = word.replace('ck', s)
            new_word.append(result)
    return result


def put(word, guid, i):
    return guid[0:i] + word + guid[len(word) + i:]


def n_positions(word, n):
    return n - len(word) + 1


if __name__ == '__main__':
    main()