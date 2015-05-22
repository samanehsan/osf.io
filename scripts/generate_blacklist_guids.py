import itertools, re
from website.app import init_app


BLACKLIST_WORDS = ['bad']
ALPHABET = '23456789abcdefghijkmnpqrstuvwxyz'


def main():
    init_app(set_backends=True)
    all_combinations = itertools.combinations_with_replacement(ALPHABET, 5)
    blacklist_guids = []
    for word in BLACKLIST_WORDS:
        for guid in list(all_combinations):
            guid = ''.join(guid)
            for i in range(0, n_positions(word, 5)):
                blacklist_guid = put(word, guid, i)
                blacklist_guids.append(blacklist_guid)

    print blacklist_guids

def put(word, guid, i):
    return guid[0:i] + word + guid[len(word) + i:]


def n_positions(word, n):
    return n - len(word) + 1


if __name__ == '__main__':
    main()