import random
import re
import pandas as pd


class TextGenerator:
    def __init__(self, state_size):
        self.state_size = state_size
        self.pairs = {}
        self.words = []

    def load_data(self, file_path):
        df = pd.read_csv(file_path)
        self.words = df['quote'].astype(str).dropna().tolist()

    def create_word_pairs(self):
        for word in self.words:
            split_words = word.split()
            for i in range(len(split_words) - self.state_size):
                current_pair = tuple(split_words[i:i + self.state_size])

                if current_pair in self.pairs:
                    self.pairs[current_pair] += 1
                else:
                    self.pairs[current_pair] = 1

    def generate_text(self, length):
        output_words = []
        starting_pairs = [pair for pair in self.pairs.keys() if pair[0].istitle()]
        current_pair = random.choice(starting_pairs)

        output_words.extend(current_pair)
        used_words = set(current_pair)

        num_sentences = 0

        while True:
            next_word_options = [(pair[self.state_size - 1], freq) for pair, freq in self.pairs.items() if
                                 pair[:self.state_size - 1] == current_pair[1:]]
            next_word_options = [(word, freq) for word, freq in next_word_options if word not in used_words]

            if next_word_options:
                current_word = max(next_word_options, key=lambda x: x[1])[0]
            else:
                current_word = random.choice(list(self.pairs.keys()))[self.state_size - 1]

            output_words.append(current_word)
            used_words.add(current_word)

            if re.match(r'.+[.!?]$', current_word):
                num_sentences += 1

                if num_sentences == 1:
                    break

                starting_pairs = [pair for pair in self.pairs.keys() if pair[0].istitle()]
                current_pair = random.choice(starting_pairs)
                output_words.extend(current_pair)
                used_words = set(current_pair)

            current_pair = tuple(output_words[-self.state_size:])

        output_text = ' '.join(output_words)
        output_text = output_text[0].upper() + output_text[1:]

        if not re.match(r'.+[.!?]$', output_text):
            output_text += '.'

        return output_text
