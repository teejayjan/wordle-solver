import string


class WordDictionary:
    def __init__(self, file):
        self.words_list = self.read_file(file)
        self.words = self.convert_to_dictionary(self.words_list)

    def get_words(self, letter, index):
        """Returns words with a given letter at a given index."""
        return self.words[letter][index]

    def read_file(self, file):
        """Reads in text file of newline separated words and returns list."""
        word_list = []
        with open(file) as f:
            for line in f:
                word_list.append(line.rstrip())
        return word_list

    def convert_to_dictionary(self, list):
        """Takes list of words and stores in dictionary:
        { letter : { letter_position: word } }"""
        alphabet = string.ascii_lowercase
        word_dict = dict.fromkeys(alphabet)
        for key in word_dict:
            word_dict[key] = {new_list: [] for new_list in range(5)}
        for word in list:
            for i in range(5):
                word_dict[word[i]][i].append(word)
        return word_dict


class Solver:
    def __init__(self, file):
        self.words = WordDictionary(file)
        self.possibilities = self.words.words_list
        self.green_and_grey_guesses = []
        self.green_guesses = ["", "", "", "", ""]
        self.num_guesses = 1

    def get_possibilities(self):
        """Returns sorted list of possibilities."""
        self.possibilities.sort()
        return self.possibilities

    def get_green_guesses(self):
        """Returns green guesses."""
        return self.green_guesses

    def get_num_guesses(self):
        """Returns number of guesses."""
        return self.num_guesses

    def user_input(self, pairs):
        """Wrapper function to call internal functions from user inputs."""

        for i in range(5):
            color = pairs[i][0].upper()
            letter = pairs[i][1].lower()

            self.possibilities = \
                self.generate_possibilities(color, (letter, i))

            if color == "G" or color == "X":
                self.green_and_grey_guesses.append(letter)
            if color == "G":
                self.green_guesses[i] = "*" + letter + "*"

        self.num_guesses += 1
        # print(self.count_patterns())
        return self.generate_next_guess(letter)

    def generate_possibilities(self, color, pair):
        """Receives color, letter, and index to update possibilities."""
        letter = pair[0]
        index = pair[1]

        # removes all words without letter in index
        if color == "G":
            possible_words = self.words.get_words(letter, index)
            self.possibilities = [
                w for w in possible_words if w in self.possibilities
            ]
            return self.possibilities

        # removes all words without letter
        if color == "Y":
            possible_words = []
            for i in range(5):
                if i != index:
                    possible_words = possible_words + \
                        self.words.get_words(letter, i)

            # removes words without yellow letter
            self.possibilities = [
                w for w in self.possibilities if w in possible_words
            ]
            possible_words = self.words.get_words(letter, index)

            # removes words with yellow letter at given index
            self.possibilities = [
                w for w in self.possibilities if w not in possible_words
            ]

            return self.possibilities

        # removes all words with letter
        else:
            self.possibilities = [
                w for w in self.possibilities if letter not in w
            ]
            return self.possibilities

    def generate_next_guess(self, guess):
        """Counts occurrences of remaining letters to generate most likely
        next guess by position."""
        prob_display = ["" for x in range(5)]

        for i in range(5):
            if self.green_guesses[i] == "":
                prob_display[i] = self.count_letters(i)
            else:
                prob_display[i] = self.green_guesses[i]

        return prob_display

    def count_letters(self, index):
        """Counts occurences of letters at given index."""
        probabilities = {}
        alphabet = string.ascii_lowercase
        probabilities = dict.fromkeys(alphabet, 0)
        for word in self.possibilities:
            probabilities[word[index]] += 1

        probabilities = sorted(probabilities.items(),
                               key=lambda x: x[1], reverse=True)

        return (probabilities[0][0],
                "{0:.0%}".format(probabilities[0][1]/len(self.possibilities)))

    def count_patterns(self):
        """Counts occurences of patterns in remaining possibilities."""
        # 1: word[0:3] 2: word[2:5]
        probabilities = {1: {}, 2: {}}
        sub_dict_lower = probabilities[1]
        sub_dict_upper = probabilities[2]

        # fill pattern dictionaries
        for word in self.possibilities:
            pattern_lower = word[0:3]
            pattern_upper = word[2:5]
            if pattern_lower not in sub_dict_lower.keys():
                sub_dict_lower[pattern_lower] = 1
            elif pattern_lower in sub_dict_lower.keys():
                sub_dict_lower[pattern_lower] += 1
            if pattern_upper not in sub_dict_upper.keys():
                sub_dict_upper[pattern_upper] = 1
            elif pattern_upper not in sub_dict_upper.keys():
                sub_dict_upper[pattern_upper] += 1

        # sort sub dictionaries
        patterns_lower = sorted(sub_dict_lower.items(),
                                key=lambda x: x[1], reverse=True)
        patterns_upper = sorted(sub_dict_upper.items(),
                                key=lambda x: x[1], reverse=True)

        n = len(self.possibilities)
        return probabilities


if __name__ == "__main__":
    user_input = ""
    solver_instance = Solver("words.txt")

    while True:
        # print("Enter color, letter, and index or type exit.")
        print("Enter color and letter as comma separated tuples or type 'exit' to exit")
        print("G for green, Y for yellow, and X for grey.")

        user_input = input("Guess #" + str(solver_instance.get_num_guesses())
                           + ": ")
        user_input_list = []
        for tup in user_input.split('),('):
            tup = tup.replace(")", "").replace("(", "")
            user_input_list.append(tuple(tup.split(",")))
        if user_input.lower() == "exit":
            break
        # print(user_input_list)
        # user_input = user_input.split(", ")
        # color = user_input[0].upper()
        # letter = user_input[1].lower()
        # index = int(user_input[2])
        # print(solver_instance.user_input(color, (letter, index)))
        print(solver_instance.user_input(user_input_list))
        # print(solver_instance.get_possibilities())
        print("\n")
