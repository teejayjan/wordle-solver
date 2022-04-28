import string


class WordDictionary:
    def __init__(self, file: str):
        self.word_list = self.read_file(file)
        self.word_dictionary = self.convert_to_dict(self.word_list)
        self.letter_frequencies = self.convert_to_frequencies(self.word_list)

    def get_words_by_letter_and_index(self, letter: str, index: int) -> list:
        """Returns a list of words containing letter at index."""
        return self.word_dictionary[letter][index]

    def get_frequencies_at_index(self, index: int) -> dict:
        """Returns a dictionary of letter frequencies at index."""
        return self.letter_frequencies[index]

    def get_word_list(self) -> list:
        """Returns list of words."""
        return self.word_list

    def read_file(self, file: str) -> list:
        """Reads in a text file of newline separated words."""
        word_list = []
        with open(file) as f:
            for line in f:
                word_list.append(line.rstrip())
        return word_list

    def convert_to_dict(self, word_list: list) -> dict:
        """Takes a list of words and stores them in dictionary:
        { letter : { letter_index : [words] } }"""
        alphabet = string.ascii_lowercase
        word_dict = dict.fromkeys(alphabet)

        # initialize sub-dictionaries of words with letter at index
        for key in word_dict:
            word_dict[key] = {new_list: [] for new_list in range(5)}

        # fill dictionary
        for word in word_list:
            for i in range(5):
                word_dict[word[i]][i].append(word)

        return word_dict

    def convert_to_frequencies(self, word_list) -> dict:
        """Takes a list of words and stores count of letters in each index:
        {index : { letter: frequency } }"""
        alphabet = string.ascii_lowercase
        frequencies = dict.fromkeys([0, 1, 2, 3, 4])
        for key in frequencies:
            frequencies[key] = dict.fromkeys(alphabet, 0)
        for word in word_list:
            for i in range(5):
                frequencies[i][word[i]] += 1
        return frequencies


class Solver:
    def __init__(self, words: list):
        # self.words_instance = WordDictionary(file)
        # self.possibilites = self.words_instance.get_word_list()
        self.possibilites = words
        self.green_and_grey_guesses = []
        self.green_guesses = ["", "", "", "", ""]
        self.num_guesses = 1

    def get_possibilities(self) -> list:
        """Returns sorted list of possibilites."""
        self.possibilites.sort()
        return self.possibilites

    def get_green_guesses(self) -> list:
        """Returns green guesses."""
        return self.green_guesses

    def get_num_guesses(self) -> int:
        return self.num_guesses

    def user_input(self, guess: str) -> list:
        """Wrapper function to call internal functions from user input."""

        # parse incoming string to store as usable list
        guess = self.parse_user_input(guess)

        # store guessed letters
        self.store_guesses(guess)

        # update possibilities
        self.update_possibilities(guess)

        # increment guess number
        self.increment_num_guesses()

        # get suggested next guess by pattern
        pattern_guess = self.get_guess_word(self.next_guess_by_pattern())

        # get suggested next guess by index
        index_guess = self.get_guess_word(self.next_guess_by_index())

        # return list of suggested next guesses
        return [index_guess, pattern_guess]

    def increment_num_guesses(self) -> None:
        """Increments number of guesses made."""
        self.num_guesses += 1

    def parse_user_input(self, in_string: str) -> list:
        """Parses input string.
        (color,letter),(c,l),(c,l),(c,l),(c,l)"""
        user_input_list = []
        for tup in in_string.split('),('):
            tup = tup.replace(")", "").replace("(", "")
            user_input_list.append(tuple(tup.split(",")))
        return user_input_list

    def store_guesses(self, guess: list) -> None:
        """Stores guesses."""
        for i in range(5):
            color = guess[i][0].upper()
            letter = guess[i][1].upper()

            if color == "G" or color == "X":
                self.green_and_grey_guesses.append(letter)
            if color == "G":
                self.green_guesses[i] = "*{}*".format(letter)

    def update_possibilities(self, guess: list) -> None:
        """Receives guess to update list of possible words."""

        bad_words = []
        for word in self.possibilites:
            for i in range(5):
                color = guess[i][0].upper()
                letter = guess[i][1]

                if self.update_helper(word, color, letter, i):
                    bad_words.append(word)

        bad_words = set(bad_words)
        self.possibilites = [
            w for w in self.possibilites if w not in bad_words
        ]

    def update_helper(self, word: str, color: str, letter: str, index: int) -> bool:
        """Receives word, color, letter, and index to determine whether
        to remove word from within update function."""
        if color == "G":
            if word[index] != letter:
                return True

        if color == "Y":
            if word[index] == letter:
                return True
            if letter not in word:
                return True

        if color == "X":
            if letter in word:
                return True

    def get_guess_word(self, frequencies: dict) -> str:
        """Receives dictionary of letter frequencies to determine best guess
        from remaining possibilities."""
        words = dict.fromkeys(self.get_possibilities(), 0)
        n = len(self.possibilites)
        for word in words:
            for key in frequencies:
                for letter in frequencies[key]:
                    if word[key] == letter[0]:
                        words[word] += letter[1] / n

        words = sorted(words.items(), key=lambda x: x[1], reverse=True)

        # find word without repeated letters
        return self.get_word_no_repeats(words)

    def get_word_no_repeats(self, words: list) -> str:
        """Receives list of tuples of words and frequencies to find
        best matching word without duplicate letters."""
        # search for word with no repeated letters
        for word in words:
            if len(set(word[0])) == len(word[0]):
                return word[0].upper()

        # search for word with one repeated letter
        for word in words:
            if len(word[0]) - len(set(word[0])) == 1:
                return word[0].upper()

        # no conditions satisfied, return most likely
        return words[0][0].upper()

    def next_guess_by_index(self) -> dict:
        """Counts occurences of letters in each index of possibilities,
        returning dictionary { index : [(letter, count)]"""
        counts = dict.fromkeys([0, 1, 2, 3, 4])

        for key in counts:
            count_at_index = self.get_counts_at_index(key)
            count_at_index = sorted(count_at_index.items(),
                                    key=lambda x: x[1], reverse=True)
            counts[key] = count_at_index

        return counts

    def get_counts_at_index(self, index: int) -> dict:
        """Returns number of occurences of all letters at given index."""
        count = {}
        alphabet = string.ascii_lowercase
        count = dict.fromkeys(alphabet, 0)
        for word in self.possibilites:
            count[word[index]] += 1

        return count

    def next_guess_by_pattern(self) -> dict:
        """Counts occurences of patterns in possibilities, returning
        dictionary { index : [(letter, count)]"""
        # 1: word[0:3] 2: word[2:5]
        patterns = {1: {}, 2: {}}
        sub_dict_lower = patterns[1]
        sub_dict_upper = patterns[2]

        # fill pattern dictionaries with occurences
        for word in self.possibilites:
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
        sub_dict_lower = sorted(sub_dict_lower.items(),
                                key=lambda x: x[1], reverse=True)
        sub_dict_upper = sorted(sub_dict_upper.items(),
                                key=lambda x: x[1], reverse=True)

        # initialize top pattern options: (pattern, frequency)
        top_lower = sub_dict_lower[0]
        top_upper = sub_dict_upper[0]

        # no duplicates in top patterns (except middle letter)
        if len(set(top_lower[0][0:2] + top_upper[0])) == 5:
            return self.convert_patterns_to_sorted_dict(top_lower, top_upper)

        # increment lesser pattern until we find two without duplicate letters
        else:
            i = 1
            while len(set(top_lower[0][0:2] + top_upper[0])) < 5:
                # can't find unique, return top of both
                if i >= len(sub_dict_lower) or i >= len(sub_dict_upper):
                    return self.convert_patterns_to_sorted_dict(
                        sub_dict_lower[0], sub_dict_upper[0]
                    )
                # upper pattern occurs more frequently
                elif top_lower[1] < top_upper[1]:
                    top_lower = sub_dict_lower[i]
                # lower pattern occurs more frequently
                elif top_lower[1] > top_upper[1]:
                    top_upper = sub_dict_upper[i]
                i += 1
            return self.convert_patterns_to_sorted_dict(top_lower, top_upper)

    def convert_patterns_to_sorted_dict(self, lower: tuple, upper: tuple) -> dict:
        """Helper function to convert list of tuples to indexed dictionary."""
        alphabet = string.ascii_lowercase
        counts = dict.fromkeys([0, 1, 2, 3, 4])
        for key in counts:
            counts[key] = dict.fromkeys(alphabet, 0)

        zero = lower[0][0]
        one = lower[0][1]
        two = lower[0][2]
        counts[0][zero] += 1
        counts[1][one] += 1
        counts[2][two] += 1

        two = upper[0][0]
        three = upper[0][1]
        four = upper[0][2]
        counts[2][two] += 1
        counts[3][three] += 1
        counts[4][four] += 1

        for letter in counts[2]:
            counts[2][letter] = counts[2][letter] // 2

        for key in counts:
            count_at_index = counts[key]
            count_at_index = sorted(count_at_index.items(),
                                    key=lambda x: x[1], reverse=True)
            counts[key] = count_at_index

        return counts


if __name__ == "__main__":
    user_input = ""
    solver_instance = Solver("words.txt")
    print(solver_instance.user_input("(y,t),(x,r),(x,a),(x,c),(y,e)"))

    while True:
        user_input = input()
        print(solver_instance.user_input(user_input))
        # print(solver_instance.get_possibilities())
        print('\n')
