import main


class AutoSolver:
    def __init__(self, target_word, starting_word):
        self.target = target_word
        self.starting_word = starting_word

    def primary_loop(self):
        """Uses solver in main.py to find target word."""
        solver_instance = main.Solver("words.txt")

        guess = self.generate_input(self.starting_word)
        print("Guess #1: " + self.starting_word.upper())
        print("Results for guess: " + guess)

        if self.starting_word.upper() == self.target.upper():
            print("Congrats! You solved it in one guess!")

        else:
            while solver_instance.get_num_guesses() < 6:
                next_guess = solver_instance.user_input(guess)
                print("Guess #" + str(solver_instance.get_num_guesses()) +
                      ": " + next_guess[0].upper())
                guess = self.generate_input(next_guess[0])
                print("Results for guess: " + guess)
                if next_guess[0].upper() == self.target.upper():
                    print("Solved wordle in " +
                          str(solver_instance.get_num_guesses()) +
                          " guess(es)")
                    break
            if solver_instance.get_num_guesses() > 6:
                print("Unable to solve wordle.")

        # return self.generate_input(self.target)a

    def generate_input(self, word):
        """Converts five letter string into tuples for program input."""
        ret = [[] for _ in range(5)]

        for i in range(5):
            guess_letter = word[i].lower()
            target_letter = self.target[i].lower()
            if guess_letter == target_letter:
                ret[i].append("g")
                ret[i].append(guess_letter)
            elif guess_letter in self.target:
                ret[i].append("y")
                ret[i].append(guess_letter)
            else:
                ret[i].append("x")
                ret[i].append(guess_letter)

        ret_string = ""
        for i in range(5):
            ret_string = ret_string + \
                "(" + ret[i][0] + "," + str(ret[i][1]) + ")"
            if i != 4:
                ret_string = ret_string + ","

        return ret_string


if __name__ == "__main__":
    target_word = input("Enter target word: ")
    new_solver = AutoSolver(target_word, "trace")
    new_solver.primary_loop()
