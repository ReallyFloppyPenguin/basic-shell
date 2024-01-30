from basicshell.tools.error import *
from hashlib import sha256
import basicshell.version as version
from shutil import rmtree
from os import mkdir, remove, path, walk, getcwd, chdir
import sys
import os
import webbrowser
import platform
import importlib.util
from pathlib import Path
import basicshell.tools.text_editor as text_editor

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
        if not (os.path.isfile(cmd_set_seq[1]) and os.path.isdir(cmd_set_seq[1])):
            chdir(cmd_set_seq[1])
        else:
            chdir(instance.cd + f"\\{cmd_set_seq[1]}")
        return os.getcwd()
    else:
        raise ShellInstanceError(FATAL_ERR, instance, IS_NOT, OF_TYPE, SHELL)


def _cd(cmd_set_seq, instance):
    """`instance` must be of type Shell"""
    if instance.cd:  #
        cwd = Path(instance.cd).parent.absolute().__str__()
        chdir(cwd + f"\\{cmd_set_seq[1]}")
        print(os.getcwd())
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
                return os.getcwd()
                return f"{instance.cd}\\{cmd_set_seq[1]}"
            else:
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


def pyrun(cmd_set_seq, instance):
    try:
        params = cmd_set_seq[1:]
        instance.pipe.stdout(
            f"Running application '{cmd_set_seq[1]}' with {len(params)-1} params"
        )
        instance.pipe.stdout("-"*len(f'Running application \'{cmd_set_seq[1]}\' with 0 params'))
        os.system(f'python {" ".join(params)}')
    except (AttributeError, FileNotFoundError):
        instance.pipe.stdout(ERROR, FILE_NOT_FOUND, cmd_set_seq[1])

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


def launch(cmd_set_seq, instance):
    if instance.cd:
        os.system(" ".join(cmd_set_seq[1:]))
    else:
        raise ShellInstanceError(FATAL_ERR, instance, IS_NOT, OF_TYPE, SHELL)



def dlenv(cmd_set_seq, instance):
    if instance.json:
        d = instance.json
        if ensure_password_is_right(instance):
            pass
        else:
            return
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
        cmd_set_seq[1] = cmd_set_seq[1].replace(".py", '')
        spec = importlib.util.spec_from_file_location(
            cmd_set_seq[1], instance.cd + "\\" + cmd_set_seq[1]+".py"
        )
        exe = importlib.util.module_from_spec(spec)
        try:
            params = []
            for i, param in enumerate(cmd_set_seq[2:]):
                params.append(param.replace("*", ""))
            instance.pipe.stdout(
                f"Running application '{cmd_set_seq[1]}' with {len(params)} params"
            )
            instance.pipe.stdout("-"*len(f'Running application \'{cmd_set_seq[1]}\' with {len(params)} params'))

            spec.loader.exec_module(exe)
            exe.run(*params, instance=instance)
        except:
            instance.pipe.stdout(ERROR, PARSING_EXE)
    except (AttributeError, FileNotFoundError):
        instance.pipe.stdout(ERROR, FILE_NOT_FOUND, cmd_set_seq[1])


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


def delete(cmd_set_seq, instance):
    if instance.cd:
        if instance.json['env'].get("PASS_TO_DEL") == "True":
            if ensure_password_is_right(instance):
                pass
            else:
                instance.pipe.stdout("Wrong password")
                return
        try:
            try:
                p = instance.cd + "\\" + cmd_set_seq[1]
                if path.splitext(cmd_set_seq[1])[1]:
                    remove(p)
                else:
                    rmtree(p)
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
            webbrowser.open(
                f"https://github.com/potato-pack/basic-shell/wiki/Commands#{cmd_set_seq[1]}"
            )
    except:
        webbrowser.open(f"https://github.com/potato-pack/basic-shell/wiki/Commands")


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
    pss = instance.pipe.secure_stdin("Password: ")
    if not sha256(pss.encode()).hexdigest() == json["user"]["password"]:
        instance.pipe.stdout("Wrong password")
        return False
    else:
        return True