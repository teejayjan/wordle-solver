import string


class WordDictionary:
    def __init__(self, file):
        self.words = self.convert_to_dictionary(self.read_file(file))

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
        self.possibilities = []

    def get_possibilities(self):
        """Returns sorted list of possibilities."""
        self.possibilities.sort()
        return self.possibilities

    def test_generate_possibilities(self, tuples):
        """Test function assuming all inputs are green letters."""

        for pair in tuples:
            self.possibilities = self.possibilities + \
                (self.words.get_words(pair[0], pair[1]))

        self.possibilities = [
            word for word in self.possibilities if self.possibilities.count(word) > len(tuples) - 1]

        self.possibilities = list(set(self.possibilities))
        
    def generate_next_guess(self):
        """Counts occurences of remaining letters to generate most likely
        next guess."""
        probabilities = []
        


if __name__ == "__main__":
    # words = WordDictionary("words.txt")
    # print(words.words)
    new_solver = Solver("words.txt")
    # print(new_solver.words.get_words("a", 2))
    new_solver.test_generate_possibilities([("g", 0), ("r", 1), ("o", 2)])
    print(new_solver.get_possibilities())
