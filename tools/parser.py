class Parse:
    def __init__(self):
        self.chars = []

    
    def parse(self, arg:str, sep=' '):
        arg += ' '
        seq = ''
        for char in arg:
            if char == sep:
                self.chars.append(seq)
                seq =''
            else:
                seq += char
        if len(self.chars) == 0:
            return arg
        else:
            return self.chars