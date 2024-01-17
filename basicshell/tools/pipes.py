from click import secho
from colorama import init as colorama_init
from colorama import Fore

class BasePipe:
    def __init__(self):...

    def stdout(self, *out) -> None:
        if not isinstance(out, list):
            out = ' '.join(out)
        print(out)

try:
    import pyttsx3
    class SpeakPipe(BasePipe):
        def __init__(self):
            super().__init__()
            self.e = pyttsx3.init()
            
        def stdout(self, *out) -> None:
            out = ' '.join(out)
            pyttsx3.speak(out)
except ModuleNotFoundError:
    pass




class DefaultPipe(BasePipe):
    def __init__(self):
        super().__init__()


class ColourPipe(BasePipe):
    def __init__(self, colour=Fore.LIGHTRED_EX):
        super().__init__()
        colorama_init()
        self.colour = colour

    def stdout(self, *out):
        
        out = ' '.join(out)
        print(f"{self.colour}{out}{Fore.RESET}")




class PipeError(Exception):...