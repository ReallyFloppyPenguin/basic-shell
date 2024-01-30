from hashlib import sha256
from json import load as l, dump as d
from basicshell.tools.parser import Parse
from basicshell.kernel.cmds import *
from basicshell.tools.error import ERROR, INVALID_CMD, QUOTE
from subprocess import Popen, PIPE
from typing import List
import basicshell.tools.pipes as pipes
import copy
from pwinput import pwinput


def call_cmd(cmd_set_seq, instance, cmds: str) -> List[str]:
    try:
        try:
            is_special = cmds[2]
        except IndexError:
            is_special = False

        modified_cmd_list = []
        # self.pipe.stdout("----------------------------------------------------------------")
        # self.pipe.stdout(1, len(cmds))

        for i in range(1, len(cmd_set_seq)):
            # self.pipe.stdout("replace", i)
            # self.pipe.stdout(cmds[1].replace(f"*{i}*", f'{cmd_set_seq[i].replace("*", "")}'))
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
        instance.pipe.stdout(ERROR, INVALID_CMD, QUOTE + cmd + QUOTE)
        return "ERROR", "ERROR"


class Shell:
    def __init__(self, pipe, data_j: str = None, data_c: str = None) -> None:
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
        self.cd = os.getcwd()
        if data_j is None:
            self.data_j = os.getcwd() + "\\data_j.json"
        else:
            self.data_j = data_j

        if data_c is None:
            self.data_c = os.getcwd() + "\\data_c.json"
        else:
            self.data_c = data_c
        self.json = self._load(self.data_j)
        self.call = self._load(self.data_c)
        self._init_data_c()
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
            "run": run_py_exe,
            "reload": self.reload,
            "pyrun": pyrun,
            "launch": launch,
            "delete": delete
        }
        try:
            if not self.json["user"]["username"]:
                self._create_user()
        except:
            self._create_user()
        self._username = self.json["user"]["username"]
        self._passw = self.json["user"]["password"]
        self.inp_start = f"{self._username}@{self.cd}$ "
        clear([], self)
        self._print_info()

    def _print_info(self):
        print("+-------------------------------+")
        print("|-----Welcome to basicshell-----|")
        print(f"|-------------{version.version}-------------|")
        print("+-------------------------------+")

    def _create_user(self):
        self.pipe.stdout("Please fill this form to create a user")

        _username = self.pipe.stdin("Username: ")
        _passw = self.pipe.secure_stdin("Password (it will be hashed): ")
        data_to_dump = {
            "user": {
                "username": _username,
                "password": sha256(_passw.encode()).hexdigest(),
            }
        }
        self._dump(data_to_dump, self.data_j)
        self.json = self._load(self.data_j)

    def execute(self, inp=None):
        if not inp:
            inp = self.pipe.stdin(self.inp_start)
        self._handle(inp)

    def _handle(self, inp):
        cmd_set_seq = Parse().parse(inp.strip())
        call = self.cmds_to_call_default_set.get(cmd_set_seq[0])
        if call is not None:
            if cmd_set_seq[0] == "cd":
                c_d = call(cmd_set_seq, self)
                self.reload(c_d)
            if cmd_set_seq[0] == "reload":
                call(self.cd)
            else:
                call(cmd_set_seq, self)
        else:
            cmd = self._query_call(cmd_set_seq)
            if cmd is not None:
                out, err = call_cmd(cmd_set_seq, self, cmd)
                if out:
                    self.pipe.stdout("OUTPUT", "\n", out)
                else:
                    self.pipe.stdout("ERROR", "\n", err)
            else:
                self.pipe.stdout(ERROR, INVALID_CMD, QUOTE + cmd_set_seq[0] + QUOTE)

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

    def _init_data_c(self):
        data_c = self._load(self.data_c)
        if data_c.get("cmds") is None:
            temp_copy = copy.deepcopy(data_c)
            temp_copy["cmds"] = []
            self._dump(temp_copy, self.data_c)

    def _dump(self, data: dict, path: str):
        with open(path, "w") as tempf:
            d(data, tempf)
            tempf.close()

    def reload(self, cd):
        self.cd = cd
        self.json = self._load(self.data_j)
        self.call = self._load(self.data_c)
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
        try:
            for cmd in self.call["cmds"]:
                if cmd_set_seq[0] == cmd[0][0]:
                    # has_found_command = True
                    try:
                        return [cmd[0], cmd[1], cmd[2]]
                    except:
                        return [cmd[0], cmd[1], False]
        except:
            pass
        # if has_found_command == False:
        ##    self.pipe.stdout("nah")
        #    return None

    def ensure_password_is_right(self, password = None):
        if not password:
            password = pwinput("Password: ")
            print(password)
        if sha256(password.encode()).hexdigest() == self.json['user']['password']:
            return True
        else:
            return False

    def __delattr__(self, __name: str) -> None:
        self.reload(self.cd)
