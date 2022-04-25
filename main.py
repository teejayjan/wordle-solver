import string


class WordDictionary:
    def __init__(self, file):
        self.words_list = self.read_file(file)
        self.words = self.convert_to_dictionary(self.words_list)
        self.letter_frequencies = self.convert_to_frequencies(self.words_list)

    def get_words(self, letter, index):
        """Returns words with a given letter at a given index."""
        return self.words[letter][index]

    def get_frequencies_at_index(self, index):
        """Returns a dictionary of letter frequences at a given index."""
        return self.letter_frequencies[index]

    def read_file(self, file):
        """Reads in text file of newline separated words and returns list."""
        word_list = []
        with open(file) as f:
            for line in f:
                word_list.append(line.rstrip())
        return word_list

    def convert_to_dictionary(self, l):
        """Takes list of words and stores in dictionary:
        { letter : { letter_position: word } }"""
        alphabet = string.ascii_lowercase
        word_dict = dict.fromkeys(alphabet)
        for key in word_dict:
            word_dict[key] = {new_list: [] for new_list in range(5)}
        for word in l:
            for i in range(5):
                word_dict[word[i]][i].append(word)
        return word_dict

    def convert_to_frequencies(self, l):
        """Takes list of words and stores count of letters in each index:
        { index: { letter: frequency } }"""
        alphabet = string.ascii_lowercase
        frequencies = dict.fromkeys(
            [0, 1, 2, 3, 4], dict.fromkeys(alphabet, 0))
        for word in l:
            for i in range(5):
                frequencies[i][word[i]] += 1
        return frequencies


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

        pairs = self.parse_user_input(pairs)

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
        pattern_guesses = self.next_guess_by_pattern()
        for i in range(5):
            if self.green_guesses[i] != "":
                pattern_guesses[i] = self.green_guesses[i]

        index_guesses = self.next_guess_by_index()
        next_word_by_pattern = self.get_guess_word_by_pattern(pattern_guesses)
        # message_pattern = "By pattern: " + next_word_by_pattern

        next_word_by_index = self.get_guess_word_by_index(index_guesses)
        # message_index = "By index: " + next_word_by_index

        # return message_pattern, message_index
        return [next_word_by_pattern, next_word_by_index]

    def parse_user_input(self, in_str):
        """Parses input string."""
        user_input_list = []
        for tup in in_str.split('),('):
            tup = tup.replace(")", "").replace("(", "")
            user_input_list.append(tuple(tup.split(",")))
        return user_input_list

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

    def get_highest_letter_prob_at_index(self, index):
        """Returns highest occuring letter and its probability
        at given index."""
        probabilities = {}
        alphabet = string.ascii_lowercase
        probabilities = dict.fromkeys(alphabet, 0)
        for word in self.possibilities:
            probabilities[word[index]] += 1

        probabilities = sorted(probabilities.items(),
                               key=lambda x: x[1], reverse=True)

        return (probabilities[0][0],
                "{0:.0%}".format(probabilities[0][1]/len(self.possibilities)))

    def get_letter_count_at_index(self, letter, index):
        """Returns the number of occurences of a letter at index."""
        count = {}
        alphabet = string.ascii_lowercase
        count = dict.fromkeys(alphabet, 0)
        for word in self.possibilities:
            count[word[index]] += 1

        return count[letter]

    def get_all_letter_counts_at_index(self, index):
        """Returns number of occurences of all letters at given index."""
        count = {}
        alphabet = string.ascii_lowercase
        count = dict.fromkeys(alphabet, 0)
        for word in self.possibilities:
            count[word[index]] += 1

        return count

    def x_next_guess_by_index(self, guess):
        """Counts occurrences of remaining letters to generate most likely
        next guess by position."""
        prob_display = ["" for x in range(5)]

        for i in range(5):
            if self.green_guesses[i] == "":
                prob_display[i] = self.get_highest_letter_prob_at_index(i)
            else:
                prob_display[i] = self.green_guesses[i]

        return prob_display

    def get_guess_word_by_pattern(self, letter_list):
        """Returns word from possibilities that most closely matches
        incoming list of letters."""
        words = dict.fromkeys(self.get_possibilities(), 0)
        for word in words:
            for i in range(5):
                if word[i] == letter_list[i][0]:
                    words[word] += 1

        words = sorted(words.items(), key=lambda x: x[1], reverse=True)

        return words[0][0].upper()

    def get_guess_word_by_index(self, letter_dict):
        """Returns word from possibilities that most closely matches
        incoming dictionary of letter frequencies at index."""
        words = dict.fromkeys(self.get_possibilities(), 0)
        n = len(self.possibilities)
        for word in words:
            for key in letter_dict:
                for letter in letter_dict[key]:
                    if word[key] == letter[0]:
                        # adds frequency of letter occuring in possibilities
                        words[word] += letter[1] / n

        words = sorted(words.items(), key=lambda x: x[1], reverse=True)

        # find word without repeated letters
        ret_word = words[0][0].upper()
        i = 1
        while len(set(ret_word)) != len(ret_word):
            # iterated through all possibilities and didn't find a word
            # without repeated letters
            if i >= len(words):
                ret_word = words[0][0].upper()
                break
            ret_word = words[i][0].upper()
            i += 1

        return ret_word

    def next_guess_by_index(self):
        """Returns most frequently occuring letter in each index of remaining
        possibilities, removing duplicates."""
        # get sorted count at each index
        probabilities = dict.fromkeys([0, 1, 2, 3, 4])

        for key in probabilities:
            frequencies_at_index = self.get_all_letter_counts_at_index(key)
            frequencies_at_index = sorted(frequencies_at_index.items(),
                                          key=lambda x: x[1], reverse=True)
            probabilities[key] = frequencies_at_index

        return probabilities

    def next_guess_by_pattern(self):
        """Counts occurences of patterns in remaining possibilities."""
        # 1: word[0:3] 2: word[2:5]
        probabilities = {1: {}, 2: {}}
        sub_dict_lower = probabilities[1]
        sub_dict_upper = probabilities[2]

        # fill pattern dictionaries
        for word in self.possibilities:
            pattern_lower = word[0:3]
            pattern_upper = word[2:5]
            if pattern_lower not in sub_dict_lower:
                sub_dict_lower[pattern_lower] = 1
            elif pattern_lower in sub_dict_lower:
                sub_dict_lower[pattern_lower] += 1
            if pattern_upper not in sub_dict_upper:
                sub_dict_upper[pattern_upper] = 1
            elif pattern_upper in sub_dict_upper:
                sub_dict_upper[pattern_upper] += 1

        # sort sub dictionaries
        patterns_lower_sorted = sorted(sub_dict_lower.items(),
                                       key=lambda x: x[1], reverse=True)
        patterns_upper_sorted = sorted(sub_dict_upper.items(),
                                       key=lambda x: x[1], reverse=True)

        # get top options for each slot
        top_lower_pattern = patterns_lower_sorted[0]
        top_upper_pattern = patterns_upper_sorted[0]

        # print(patterns_lower_sorted, patterns_upper_sorted)
        # print(top_lower_pattern, top_upper_pattern)

        max_frequency = max(top_lower_pattern[1], top_upper_pattern[1])

        # increment lesser pattern if choosing both patterns results in
        # duplicated letters in guess
        # TODO: skip all this if there aren't any duplicates in pattern

        # exit condition when there are letter duplicates but only one
        # option in each
        if len(patterns_lower_sorted) == 1 and len(patterns_upper_sorted) == 1:
            pass

        elif top_lower_pattern[1] < max_frequency:
            lower_letter_one = top_lower_pattern[0][0]
            lower_letter_two = top_lower_pattern[0][1]
            upper_pattern = top_upper_pattern[0]
            i = 0
            while lower_letter_one in upper_pattern \
                    or lower_letter_two in upper_pattern:
                top_lower_pattern = patterns_lower_sorted[i]
                i += 1
                lower_letter_one = top_lower_pattern[0][0]
                lower_letter_two = top_lower_pattern[0][1]
        else:
            upper_letter_one = top_upper_pattern[0][1]
            upper_letter_two = top_upper_pattern[0][2]
            lower_pattern = top_lower_pattern[0]
            i = 0
            while upper_letter_one in lower_pattern \
                    or upper_letter_two in lower_pattern:
                top_upper_pattern = patterns_upper_sorted[i]
                i += 1
                upper_letter_one = top_upper_pattern[0][1]
                upper_letter_two = top_upper_pattern[0][2]

        # calculate probabilities
        n = len(self.possibilities)
        lower_pattern_prob = top_lower_pattern[1] / n
        upper_pattern_prob = top_upper_pattern[1] / n

        ret_probs = []

        # takes middle letter from more common pattern
        if lower_pattern_prob > upper_pattern_prob:
            smashed = top_lower_pattern[0][0:3] + top_upper_pattern[0][1:3]
            for i in range(5):
                letter = smashed[i]
                frequency = self.get_letter_count_at_index(letter, i)
                prob = "{0:.0%}".format(frequency/n)
                ret_probs.append((letter, prob))
        else:
            smashed = top_lower_pattern[0][0:2] + top_upper_pattern[0][0:3]
            for i in range(5):
                letter = smashed[i]
                frequency = self.get_letter_count_at_index(letter, i)
                prob = "{0:.0%}".format(frequency/n)
                ret_probs.append((letter, prob))

        return ret_probs


if __name__ == "__main__":
    user_input = ""
    solver_instance = Solver("words.txt")

    while True:
        # print("Enter color, letter, and index or type exit.")
        print("Enter color and letter as comma separated tuples or type 'exit' to exit")
        print("G for green, Y for yellow, and X for grey.")

        user_input = input("Guess #" + str(solver_instance.get_num_guesses())
                           + ": ")
        # user_input_list = []
        # for tup in user_input.split('),('):
        #     tup = tup.replace(")", "").replace("(", "")
        #     user_input_list.append(tuple(tup.split(",")))
        # if user_input.lower() == "exit":
        #     break
        print(solver_instance.user_input(user_input))
        print(solver_instance.get_possibilities())
        print("\n")
