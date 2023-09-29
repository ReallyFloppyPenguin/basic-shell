from kernel.utils import Shell
from tools.pipes import DefaultPipe, SpeakPipe, ColourPipe, Fore


if __name__ == "__main__":
    pipe = DefaultPipe()
    shell = Shell(pipe)
    while True:
        shell.execute()
