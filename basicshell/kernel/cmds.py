from ..tools.error import *
from ..tools.parser import Parse
from hashlib import sha256
from ..kernel import utils
import version
from shutil import rmtree
from os import mkdir, remove, path, walk, getcwd
import sys
import os
import platform
import importlib.util
from pathlib import Path
from basicshell.tools import text_editor

cmds = [
    "cd",
    "rsetu",
    "stop",
    "udateu",
    "github",
    "ver",
    "setenv",
    "mkenv",
    "dlenv",
    "help",
    "arth",
    "new",
    "dlete",
    "edit",
    "lidir",
]


def stop(cmd_set_seq, instance):
    sys.exit()


def cd(cmd_set_seq, instance):
    """`instance` must be of type Shell"""
    if instance.cd:
        try:
            p = instance.cd + "\\" + cmd_set_seq[1]
            if cmd_set_seq[1] == "../":
                back_p = Path(instance.cd).parent.absolute().__str__()
                if not back_p:
                    return instance.cd

                if path.isdir(back_p):
                    return f"{back_p}"
                else:
                    instance.pipe.stdout(
                        ERROR, DIR_NOT_FOUND, back_p + ".", "Cannot cd into dir"
                    )
                    return instance.cd

            if path.isdir(p):
                return f"{instance.cd}\\{cmd_set_seq[1]}"
            else:
                print("called")
                instance.pipe.stdout(
                    ERROR,
                    DIR_NOT_FOUND,
                    instance.cd + "\\" + cmd_set_seq[1] + ".",
                    "Cannot cd into dir",
                )
                return instance.cd
        except IndexError:
            pass
    else:
        raise ShellInstanceError(FATAL_ERR, instance, IS_NOT, OF_TYPE, SHELL)


def rsetu(cmd_set_seq, instance):
    """`instance` must be of type Shell"""
    if instance.json:
        d = instance.json
        del d["user"]["username"]
        del d["user"]["password"]
    else:
        raise ShellInstanceError(FATAL_ERR, instance, IS_NOT, OF_TYPE, SHELL)


def udateu(cmd_set_seq, instance):
    """`instance` must be of type Shell"""
    # TODO fix if user did not make any paramerters
    if instance.json:
        d = instance.json
        try:
            d["user"]["username"] = cmd_set_seq[1]
            d["user"]["password"] = sha256(cmd_set_seq[2].encode("utf-8")).hexdigest()
        except IndexError:
            d["user"]["username"] = input("Username: ")
            d["user"]["password"] = sha256(
                input("Password (it will be hashed): ").encode("utf-8")
            ).hexdigest()
    else:
        raise ShellInstanceError(FATAL_ERR, instance, IS_NOT, OF_TYPE, SHELL)


def ver(cmd_set_seq, instance):
    instance.pipe.stdout(version.version)


def github(cmd_set_seq, instance):
    instance.pipe.stdout(version.github_link)


def setenv(cmd_set_seq, instance):
    if instance.json:
        try:
            env_var_name = cmd_set_seq[1]
            val = cmd_set_seq[2]
            d = instance.json
            try:
                if instance.json["env"][env_var_name]:
                    d["env"][env_var_name] = val
                    instance._dump(d, instance.data_j)
            except KeyError:
                instance.pipe.stdout(
                    ERROR, INVALID_ENV_VAR, QUOTE + env_var_name + QUOTE
                )
        except IndexError:
            instance.pipe.stdout(
                ERROR, "No environment variable name and value not defined"
            )
    else:
        raise ShellInstanceError(FATAL_ERR, instance, IS_NOT, OF_TYPE, SHELL)


def mkenv(cmd_set_seq, instance):
    if instance.json:
        try:
            try:
                env_var_name = cmd_set_seq[1]
                val = cmd_set_seq[2]
                d = instance.json
                d["env"][env_var_name] = val

            except KeyError:
                d["env"] = {}
                env_var_name = cmd_set_seq[1]
                val = cmd_set_seq[2]
                d = instance.json
                d["env"][env_var_name] = val
            instance._dump(d, instance.data_j)
        except IndexError:
            instance.pipe.stdout(
                ERROR, "No environment variable name and value not defined"
            )
    else:
        raise ShellInstanceError(FATAL_ERR, instance, IS_NOT, OF_TYPE, SHELL)


def dlenv(cmd_set_seq, instance):
    if instance.json:
        d = instance.json
        ensure_password_is_right(instance)
        try:
            try:
                env_var_name = cmd_set_seq[1]
                del d["env"][env_var_name]
            except KeyError:
                d["env"] = {}
                env_var_name = cmd_set_seq[1]
                del d["env"][env_var_name]
        except IndexError:
            instance.pipe.stdout(
                ERROR, "No environment variable name and value not defined"
            )
    else:
        raise ShellInstanceError(FATAL_ERR, instance, IS_NOT, OF_TYPE, SHELL)


def run_py_exe(cmd_set_seq, instance):
    try:
        spec = importlib.util.spec_from_file_location(
            cmd_set_seq[1], instance.cd+'\\'+cmd_set_seq[1]
        )

        # importing the module as foo
        try:
            exe = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(exe)
            params = []
            for i, param in enumerate(cmd_set_seq[2:]):
                params.append(param.replace('*', ''))
            exe.run(*params, instance=instance)
        except:
            print('your file has an error')
    except AttributeError:
        print('err')


def new(cmd_set_seq, instance):
    if instance.cd:
        try:
            if len(path.splitext(cmd_set_seq[1])[1]) >= 1:
                p = instance.cd + "\\" + cmd_set_seq[1]
                try:
                    with open(p, "x") as tempf:
                        pass
                except FileExistsError:
                    instance.pipe.stdout(
                        ERROR,
                        FILE_EXISTS,
                        instance.cd + "\\" + cmd_set_seq[1] + ".",
                        "Cannot create new file",
                    )
            else:
                p = instance.cd + "\\" + cmd_set_seq[1]
                try:
                    Path(p).mkdir()
                except FileExistsError:
                    instance.pipe.stdout(
                        ERROR, FILE_EXISTS, p + ".", "Cannot create new file"
                    )
        except IndexError:
            instance.pipe.stdout(ERROR, MISSING_ARG, "1.", "Cannot run new")
    else:
        raise ShellInstanceError(FATAL_ERR, instance, IS_NOT, OF_TYPE, SHELL)


def dlete(cmd_set_seq, instance):
    if instance.cd:
        try:
            try:
                p = "centrl\\" + instance.cd + "\\" + cmd_set_seq[1]
                if path.splitext(cmd_set_seq[1])[1]:
                    remove(p)
                else:
                    rmtree(p, ignore_errors=True)
            except FileNotFoundError:
                instance.pipe.stdout(
                    ERROR,
                    FILE_NOT_FOUND,
                    instance.cd + "\\" + cmd_set_seq[1],
                    "Cannot run dlete",
                )
        except IndexError:
            instance.pipe.stdout(ERROR, MISSING_ARG, "1.", "Cannot run dlete")
    else:
        raise ShellInstanceError(FATAL_ERR, instance, IS_NOT, OF_TYPE, SHELL)


def edit(cmd_set_seq, instance):
    text_ed = text_editor.TextEditor()
    print(cmd_set_seq[1])
    text_ed.run(path=cmd_set_seq[1])


def _edit(cmd_set_seq, instance):
    if instance.cd:
        try:
            p = version.path + instance.cd + "\\" + cmd_set_seq[1]
            if path.splitext(cmd_set_seq[1])[1]:
                try:
                    with open(p, "w") as tempf:
                        lines = []
                        instance.pipe.stdout("-------- edit --------")
                        while True:
                            line = input()
                            if line == "*done*":
                                break
                            else:
                                lines.append(line + "\n")
                        tempf.writelines(lines)

                except FileNotFoundError:
                    instance.pipe.stdout(
                        ERROR,
                        FILE_NOT_FOUND,
                        instance.cd + "\\" + cmd_set_seq[1] + ".",
                        "Cannot edit file",
                    )
            else:
                instance.pipe.stdout(
                    ERROR, CANNOT_EDIT, p, "is a directory. Cannot edit"
                )
        except IndexError:
            instance.pipe.stdout(ERROR, MISSING_ARG, "1.", "Cannot run new")
    else:
        raise ShellInstanceError(FATAL_ERR, instance, IS_NOT, OF_TYPE, SHELL)


def help(cmd_set_seq, instance):
    try:
        if cmd_set_seq[1] in cmds:
            instance.pipe.stdout(
                "Find help here:", version.github_link + "/wiki/" + "Commands/"
            )
    except:
        instance.pipe.stdout(ERROR, MISSING_ARG)


def clear(cmd_set_seq, instance):
    if platform.uname().system == "Windows":
        os.system("cls")
    else:
        instance.pipe.stdout(f"System ({platform.uname().system}) is not supported yet")


def arth(cmd_set_seq, instance):
    try:
        if cmd_set_seq[2] == "+":
            instance.pipe.stdout(int(cmd_set_seq[1]) + int(cmd_set_seq[3]))
    except Exception as e:
        instance.pipe.stdout(e)


def lidir(cmd_set_seq, instance):
    p = instance.cd
    instance.pipe.stdout(f"Inside {p}")
    for file in os.listdir(p):
        instance.pipe.stdout("--" + file)


def _lidir(cmd_set_seq, instance):
    if instance.cd:
        try:
            p = version.path + instance.cd + "\\"
            instance.pipe.stdout(f"Inside {p}")
            for root, dirs, files in walk(p, topdown=False):
                for name in files:
                    instance.pipe.stdout(f"{p}\\{name}")
                for name in dirs:
                    instance.pipe.stdout(f"{p}\\{name}")
                    for root2, dirs2, files2 in walk(f"{p}\\{name}", topdown=True):
                        for fname in files2:
                            instance.pipe.stdout(f"{p}\\{name}\\{fname}")
        except IndexError:
            instance.pipe.stdout(ERROR, MISSING_ARG, "1.", "Cannot run new")
    else:
        raise ShellInstanceError(FATAL_ERR, instance, IS_NOT, OF_TYPE, SHELL)


def ensure_password_is_right(instance):
    json = instance.json
    getting_password = True
    while getting_password:
        pss = input("Password: ")
        if not sha256(pss.encode()).hexdigest() == json["user"]["password"]:
            instance.pipe.stdout("Wrong password")
            continue
        else:
            getting_password = False
