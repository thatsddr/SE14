from utils import Status
import os


class Display:
    def __init__(self):
        self.colors = {
            "white": "\u001b[37;1m",
            "black": "\u001b[30;1m",
            "green": "\u001b[32;1m",
            "reset_text": "\u001b[0m"
        }
        self.bg_colors = {
            "yellow": "\u001b[43;1m",
            "green": "\u001b[42;1m",
            "black": "\u001b[40;1m",
            "gray": "\u001b[48;5;8;1m",
            "reset": "\u001b[0m"
        }

    @staticmethod
    def clear():
        os.system('clear')

    def show(self, word: list[tuple[str, Status]]):
        output = ""
        for l in word:
            if l[1] == Status.CORRECT:
                bg = self.bg_colors['green']
            elif l[1] == Status.MISPLACED:
                bg = self.bg_colors['yellow']
            else:
                bg = self.bg_colors['gray']
            output += f"{bg} {l[0].upper()} "
        print(f"{output}{self.bg_colors['reset']}")
