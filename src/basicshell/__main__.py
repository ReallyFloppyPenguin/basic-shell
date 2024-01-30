from basicshell.kernel.utils import *
from basicshell.tools.pipes import *

if __name__ == "__main__":
    pipe = DefaultPipe()
    shell = Shell(pipe)
    try:
        while True:
            shell.execute()
    except KeyboardInterrupt:
        pass
