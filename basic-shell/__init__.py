
from kernel.utils import Shell


if __name__ == "__main__":
    shell = Shell('a',"datac.json", "dataj.json")
    while True:
        shell.execute()