import solver


class AutoSolver:
    def __init__(self, target_word, starting_word):
        self.target = target_word
        self.starting_word = starting_word

    def test_loop(self):
        """Runs through every word in the list as a goal to test solver
        algorithms."""
        dict_instance = wordle.WordDictionary("words.txt")
        words = dict_instance.get_word_list()
        results = {0: 0, 1: 0}
        for word in words:
            for i in range(2):
                auto_solver_instance = AutoSolver(word, "trace")
                solver_instance = wordle.Solver("words.txt")
                guess = self.generate_input(auto_solver_instance.starting_word)
                if auto_solver_instance.starting_word.upper() == \
                        auto_solver_instance.target.upper():
                    results[i] += 1
                    print(word + " solved in 1 guess")
                else:
                    while solver_instance.get_num_guesses() < 6:
                        next_guess = solver_instance.user_input(guess)
                        guess = self.generate_input(next_guess[i])
                        if next_guess[0].upper() == \
                                auto_solver_instance.target.upper():
                            results[i] += solver_instance.get_num_guesses()
                            print(
                                word + " solved in " + str(solver_instance.get_num_guesses()) + " guesses")
                            break
                    if solver_instance.get_num_guesses() > 6:
                        results[i] += 7

        for key in results:
            results[key] = results[key] // len(words)

        return results

    def primary_loop(self):
        """Uses solver in solver.py to find target word."""
        for i in range(2):
            if i == 0:
                print("Solving by index")
            elif i == 1:
                print("Solving by pattern")
            solver_instance = solver.Solver("words.txt")

            guess = self.generate_input(self.starting_word)
            print("Guess #1: " + self.starting_word.upper())
            print("Results for guess: " + guess)

            if self.starting_word.upper() == self.target.upper():
                print("Congrats! You solved it in one guess!")

            else:
                while solver_instance.get_num_guesses() < 6:
                    next_guess = solver_instance.user_input(guess)
                    print("Guess #" + str(solver_instance.get_num_guesses()) +
                          ": " + next_guess[i].upper())
                    guess = self.generate_input(next_guess[i])
                    print("Results for guess: " + guess)
                    if next_guess[0].upper() == self.target.upper():
                        print("Solved wordle in " +
                              str(solver_instance.get_num_guesses()) +
                              " guess(es)")
                        break
                if solver_instance.get_num_guesses() > 6:
                    print("Unable to solve wordle.")

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
    # target_word = input("Enter target word: ")
    # new_solver = AutoSolver(target_word, "trace")
    # new_solver.primary_loop()
    
    dict_instance = solver.WordDictionary("words.txt")
    words = dict_instance.get_word_list()
    results = {0: 0, 1: 0}
    for word in words:
        for i in range(2):
            robot = AutoSolver(word, "trace")
            wordle = solver.Solver(words)
            formatted_guess = robot.generate_input(robot.starting_word)
            if robot.starting_word.upper() == robot.target.upper():
                results[i] += 1
                print(word + " in 1")
            else:
                while True:
                    guess = wordle.user_input(formatted_guess)
                    formatted_guess = robot.generate_input(guess[i])
                    if wordle.get_num_guesses() >= 7:
                        results[i] += wordle.get_num_guesses()
                        print(word + " failed")
                        break
                    elif guess[i].upper() == robot.target.upper():
                        results[i] += wordle.get_num_guesses()
                        print(word + " in " + str(wordle.get_num_guesses()))
                        break
    for key in results:
        results[key] = results[key] // len(words)

    print(results)
