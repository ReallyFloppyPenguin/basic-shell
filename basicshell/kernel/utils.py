from hashlib import sha256
from json import load as l, dump as d
from ..tools.parser import Parse
from .cmds import *
from ..tools.error import ERROR, INVALID_CMD, QUOTE
from subprocess import Popen, PIPE
from typing import Optional, List, TypeVar
from ..tools import pipes


def call_cmd(cmd_set_seq, instance, cmds: str) -> List[str]:
    try:
        try:
            is_special = cmds[2]
        except IndexError:
            is_special = False

        modified_cmd_list = []
        #print("----------------------------------------------------------------")
        #print(1, len(cmds))

        for i in range(1, len(cmd_set_seq)):
            #print("replace", i)
            #print(cmds[1].replace(f"*{i}*", f'{cmd_set_seq[i].replace("*", "")}'))
            modified_cmd_list.append(
                cmds[1].replace(f"*{i}*", f'{cmd_set_seq[i].replace("*", "")}')
            )
        if len(modified_cmd_list) == 0:
            modified_cmd_list.append(cmds[1])
        cmd = "".join(modified_cmd_list)
        if is_special:
            os.system(cmd)
            return "-----Special-----", "-----Special-----"
        else:
            process = Popen(cmd, stdout=PIPE, stderr=PIPE)
            stdout, stderr = process.communicate()
            return stdout.decode(), stderr.decode()

    except FileNotFoundError:
        print(ERROR, INVALID_CMD, QUOTE + cmd + QUOTE)
        return "ERROR", "ERROR"


class Shell:
    def __init__(
        self,
        pipe,
        data_j: str = "data_j.json",
        data_c: str = "data_c.json",
    ) -> None:
        """
        This is the main part, or code that is in this package\n
        here is the usage example:
        ```
        import basicshell as shell
        my_shell = shell.Shell()
        if __name__ == '__main__':
            while True:
                my_shell.execute()
        ```
        If you want a better documentation, head over \n
        to my [GitHub](https://github.com/potato-pack/basic-shell/tree/main#documentation) README
        """
        if isinstance(pipe, pipes.BasePipe):
            self.pipe = pipe
        else:
            raise pipes.PipeError(
                f"Pipe must be of type BasePipe, not {pipe.__class__.__name__}"
            )
        self.cd: str = version.path
        self.data_j: str = data_j
        self.data_c: str = data_c
        self.json = self._load(self.data_j)
        self.call = self._load(self.data_c)
        self.cmds_to_call_default_set = {
            "cd": cd,
            "lidir": lidir,
            "new": new,
            "mkenv": mkenv,
            "setenv": setenv,
            "udateu": udateu,
            "rsetu": rsetu,
            "dlenv": dlenv,
            "ver": ver,
            "github": github,
            "quit": stop,
            "help": help,
            "edit": edit,
            "arth": arth,
            "clear": clear,
            "reload": self.reload
        }
        try:
            if not self.json["user"]["username"]:
                self._create_user()
        except:
            self._create_user()
        self._username = self.json["user"]["username"]
        self._passw = self.json["user"]["password"]
        self.inp_start = f"{self._username}@{self.cd}$ "
        self._jp = data_j.encode("utf-8")
        clear([], self)

    def _create_user(self):
        print("Please fill this form to create a user")

        _username = input("Username: ")
        _passw = input("Password (it will be hashed): ")
        data_to_dump = {
            "user": {
                "username": _username,
                "password": sha256(_passw.encode("utf-8")).hexdigest(),
            }
        }
        self._dump(data_to_dump, self.data_j)
        self.json = self._load(self.data_j)

    def execute(self, inp=None):
        if not inp:
            inp = input(self.inp_start)
        self._handle(inp)

    def _handle(self, inp):
        cmd_set_seq = Parse().parse(inp.strip())
        print(cmd_set_seq[0])
        call = self.cmds_to_call_default_set.get(cmd_set_seq[0])
        if call is not None:
            print('oj')
            if cmd_set_seq[0] == 'cd':
                c_d = call(cmd_set_seq, self)
                self.reload(c_d)
            if cmd_set_seq[0] == 'reload':
                call(self.cd)
            else:
                call(cmd_set_seq, self)
        else:
            cmd = self._query_call(cmd_set_seq)
            if cmd is not None:
                out, err = call_cmd(cmd_set_seq, self, cmd)
                if out:
                    print("OUTPUT", "\n", out)
                else:
                    print("ERROR", "\n", err)
            else:
                print(ERROR, INVALID_CMD, QUOTE + cmd_set_seq[0] + QUOTE)

        self.reload(self.cd)
        

    def _load(self, path: str, rebuild: bool = True):
        try:
            with open(path, "r") as tempf:
                data = l(tempf)
        except FileNotFoundError:
            if rebuild:
                temp_path = open(path, "x")
                temp_path.write(r"{}")
                temp_path.close()
                with open(path, "r") as tempf:
                    data = l(tempf)
            else:
                raise FileNotFoundError
        return data

    def _dump(self, data: dict, path: str):
        with open(path, "w") as tempf:
            d(data, tempf)
            tempf.close()

    def reload(self, cd):
        self.cd = cd
        self.json = self._load(self.data_j, False)
        self.call = self._load(self.data_c, False)
        try:
            if not self.json["user"]["username"]:
                self._create_user()
        except KeyError:
            self._create_user()
        self._username = self.json["user"]["username"]
        self._passw = self.json["user"]["password"]
        self.inp_start = f"{self._username}@{self.cd}$ "

    def _query_call(self, cmd_set_seq):
        """
        Check if command is in 'data_c'\n
        Assuming the structure of commands is:\n
        ```
        cmds: {
            [
               [['<your-activator>'], '<your-command>', <is-special>]
            ]
        }
        ```
        """
        has_found_command = False
        for cmd in self.call["cmds"]:
            if cmd_set_seq[0] == cmd[0][0]:
                # has_found_command = True
                try:
                    return [cmd[0], cmd[1], cmd[2]]
                except:
                    return [cmd[0], cmd[1], False]
        # if has_found_command == False:
        ##    print("nah")
        #    return None

    def __delattr__(self, __name: str) -> None:
        self.reload(self.cd)