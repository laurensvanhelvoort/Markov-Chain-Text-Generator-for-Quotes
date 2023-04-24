from text_generator import TextGenerator

state_size = 10
text_length = 15
num_iterations = 10


def main():
    text_generator = TextGenerator(state_size=state_size)
    text_generator.load_data('data/quotes.csv')
    text_generator.create_word_pairs()

    for i in range(num_iterations):
        generated_text = text_generator.generate_text(length=text_length)
        print(i + 1, ":", generated_text)


if __name__ == '__main__':
    main()
