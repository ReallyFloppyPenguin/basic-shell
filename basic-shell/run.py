
from kernel.utils import Shell
from tools.pipes import SpeakPipe



if __name__ == "__main__":
    pipe = SpeakPipe()
    shell = Shell(pipe,"datac.json", "dataj.json")
    while True:
        shell.execute()
