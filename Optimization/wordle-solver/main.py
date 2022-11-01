import sys
from Wordle import Wordle
from Solver import Solver


def solve_wordle(automatic=False, word=None):
    wordle = Wordle(word)
    solver = Solver(wordle.return_words())

    while not wordle.is_game_over():
        solver.update()
        a = ""
        if automatic:
            a = wordle.guess(solver.pick_guess())
        else:
            print("Suggested: ", solver.pick_guess())
            a = wordle.guess(input("Guess: "))
        solver.add_guess(a)
    return wordle.stats()


def main():
    automatic = True if len(sys.argv) > 1 and sys.argv[1].lower() == "true" else False
    word = sys.argv[2].upper() if len(sys.argv) > 2 and len(sys.argv[2]) == 5 else None
    solve_wordle(automatic, word)


if __name__ == "__main__":
    main()

