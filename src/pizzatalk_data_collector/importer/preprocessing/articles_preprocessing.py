import os

import nltk
import pandas as pd

nltk.download("wordnet")
nltk.download("punkt")
nltk.download("averaged_perceptron_tagger")
dir_path = os.path.dirname(os.path.realpath(__file__))


def remove_space_and_break_line(article):
    return " ".join(article.split()).replace("\n", " ")


def decode_abbreviations(article):
    standardizing_dict = {}
    file_path = os.path.join(dir_path, "en-abbreviations.txt")
    with open(file_path, "r", encoding="utf-8") as f:
        for row in f:
            row = row.strip().replace("\t\t\t", "\t").replace("\t\t", "\t")
            parts = row.split("\t")
            if len(parts) < 2:
                continue
            acronym, word = parts[:2]
            acronym = acronym.replace(" ", "")
            word = word.split(",")[0].replace(" ", "")
            standardizing_dict[acronym] = word

    def replace_abbreviations(article):
        return " ".join(
            [standardizing_dict.get(word, word) for word in article.split()]
        )

    return replace_abbreviations(article)


def tokenize_text(article):
    return nltk.sent_tokenize(article)


def text_preprocessing(article):
    article = remove_space_and_break_line(article)
    article = decode_abbreviations(article)
    article = tokenize_text(article)
    return article


def pos_tagging(text):
    sentences = text_preprocessing(text)
    df = pd.DataFrame(columns=["Sentence #", "Word", "POS"])

    for i, sentence in enumerate(sentences, start=1):
        words = nltk.word_tokenize(sentence)
        pos_tags = nltk.pos_tag(words)
        new_df = pd.DataFrame(pos_tags, columns=["Word", "POS"])
        new_df["Sentence #"] = i
        df = pd.concat([df, new_df], ignore_index=True)

    return df
