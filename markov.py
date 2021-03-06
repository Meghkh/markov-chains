"""Generate markov text from text files.

    to run from command line:
    python markov.py gettysburg.txt
"""

import os
from random import choice
import re
import sys
import twitter


# get n-gram size from command line input

MAX_GRAM_SIZE = 5


def open_and_read_file(file_path):
    """Takes file path as string; returns text as string.

    Takes a string that is a file path, opens the file, and turns
    the file's contents as one string of text.
    """

    f = open(file_path)
    return f.read()


def produce_n_gram_dict(text_corpus):
    """Produce dictionary of n-grams"""

    n_dict = {}

    for char in text_corpus:
        if char in ["(", ")", "\"", "\'", "\'", "`", "_", "*", "__", "--", "[", "]"]:
            text_corpus.replace(char,'')

    text_corpus = text_corpus.split()

    for n in range(2, MAX_GRAM_SIZE + 1):
        for i in range(len(text_corpus) - n):
            current_n_words = tuple(text_corpus[i:i+n])

            next_word = [text_corpus[i + n]]

            if n_dict.get(current_n_words) is None:
                n_dict[current_n_words] = next_word
            else:
                n_dict[current_n_words] += next_word

    return n_dict


def generate_tweet(dictionary):
    """Generate random 140 chars tweet"""

    while True:
        current_seed = choice(dictionary.keys())
        if len(current_seed) >= 3:
            break

    window_limit = len(current_seed)
    window_size = window_limit

    message = []
    message.extend(current_seed)
    message[0] = message[0].capitalize()

    while True:
        if window_size == 1:
            break

        current_n_gram = tuple(message[-1*window_size:])

        try:
            next_word = choice(dictionary[current_n_gram])
            if (len(" ".join(message)) + len(next_word) + 12) > 140:
                return output_message(message)
            else:
                message.append(next_word)
                window_size = window_limit
        except KeyError:
            window_size -= 1
            continue

    return output_message(message)


def output_message(message_list):
    """Produce meaningful ending for message"""

    result = " ".join(message_list)

    if result[-1] in ["!", "?", "."]:
        return result + " #aug17kat"
    if result[-1] in [",", "-", " ", ":", ";"]:
        result = result[:-1] + "."
    elif result[-2:] is "--":
        result = result[:-2] + "."
    else:
        result += "."

    return result + " #aug17kat"


def tweet(file_name = "green-eggs.txt"):
    """Generate tweet from given text file """

    input_text = open_and_read_file(file_name)
    n_grams = produce_n_gram_dict(input_text)

    api = twitter.Api(
        consumer_key=os.environ['TWITTER_CONSUMER_KEY'],
        consumer_secret=os.environ['TWITTER_CONSUMER_SECRET'],
        access_token_key=os.environ['TWITTER_ACCESS_TOKEN_KEY'],
        access_token_secret=os.environ['TWITTER_ACCESS_TOKEN_SECRET'])

    twt = generate_tweet(n_grams)
    status = api.PostUpdate(twt)
    return twt


if __name__ == '__main__':
    try:
        text_path = sys.argv[1]
    except IndexError:
        text_path = "join.txt"

    print tweet(text_path)

# #aug17kat
