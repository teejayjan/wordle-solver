from types import new_class


class GramFinder:
    def __init__(self, file):
        self.words = self.read_file(file)

    def read_file(self, file):
        """Reads in text file of newline separated words and returns list."""
        word_list = []
        with open(file) as f:
            for line in f:
                word_list.append(line.rstrip())
        return word_list

    def write_file(self):
        """Writes self.words to file."""
        file = open("grams.txt", "w+")
        for line in self.words:
            file.write(line)
            file.write("\n")

    def find_bigrams(self):
        """Finds bigram frequencies for each index in a given word."""
        bigrams = dict.fromkeys([0, 1, 2, 3, 4], {})
        ranges = [(0, 1), (1, 2), (2, 3), (3, 4)]


        # this is currently duplicating a bunch of shit and not indexing or storing properly
        for slices in ranges:
            lower = slices[0]
            upper = slices[1]

            for word in self.words:
                new_bigram = word[lower:upper + 1]
                sub_dictionary_lower = bigrams[lower]
                sub_dictionary_upper = bigrams[upper]
                
                if new_bigram not in sub_dictionary_lower.keys():
                    sub_dictionary_lower[new_bigram] = 0
                elif new_bigram in sub_dictionary_lower.keys():
                    sub_dictionary_lower[new_bigram] += 1
                    
                if new_bigram not in sub_dictionary_upper.keys():
                    sub_dictionary_upper[new_bigram] = 0
                elif new_bigram in sub_dictionary_upper.keys():
                    sub_dictionary_upper[new_bigram] += 1
                
                # bigrams[lower].append(word[lower:upper + 1])
                # bigrams[upper].append(word[lower:upper + 1])

        # bigram_counts = dict.fromkeys([0, 1, 2, 3, 4], {})
        # for key in bigrams:
        #     for bigram in bigrams[key]:
        #         if bigram in bigram_counts.keys():
        #             bigram_counts[bigram] += 1
        #         else:
        #             bigram_counts[bigram] = 0

        return bigrams


if __name__ == "__main__":
    finder_instance = GramFinder("words.txt")
    # finder_instance.write_file()
    bigrams = finder_instance.find_bigrams()
    print(bigrams[0])
