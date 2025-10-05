import getpass
import socket
import argparse
import sys
import json
username=getpass.getuser()
hostname=socket.gethostname()

parser = argparse.ArgumentParser(description='эмулятор shell')
parser.add_argument("--vfs-path", help="путь к vfs")
parser.add_argument("--script", help="путь к стартовому скрипту")
parser.add_argument("--debug", action="store_true", help="включить отладочный вывод")

args = parser.parse_args()
def load_vfs(path):
    try:
        with open(path, "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"VFS load error: file not found: {path}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"VFS load error: invalid JSON in {path}: {e}")
        sys.exit(1)

    # Простая проверка структуры
    if not isinstance(data, dict) or data.get("type") != "dir":
        print("VFS load error: root must be a directory")
        sys.exit(1)

    print(f"VFS loaded successfully from {path}")
    return data

vfs_path=args.vfs_path
script=args.script
debug=args.debug

vfs = None
if vfs_path:
    vfs = load_vfs(vfs_path)

current_dir = vfs  #корень(где мы сейчас находимся(в виде словаря из json))
path_stack = []    #имена директорий, чтобы pwd показывал путь (список названий папок))


if args.script:
    line_number=0
    with open(args.script,"r") as f:
        for line in f:
            line_number+=1
            if not line or line.startswith("#"):
                continue
            command = line.strip()
            print(command)
            parts = command.split()
            if parts[0] == "exit":
                break
            elif parts[0] == "echo":
                print(" ".join(parts[1:]))
            elif parts[0] == "cd":
                if len(parts) == 1:
            # Переход в корень
                    current_dir = vfs
                    path_stack = []
                    continue
                target = parts[1]
                found = None
                if target == "..":  # # cd .. вернуться на уровень выше
                    if path_stack:
                        path_stack.pop()
                                    # пересобираем текущую директорию по стеку
                        temp = vfs
                        for folder in path_stack:
                            for child in temp.get("children", []):
                                if child["name"] == folder and child["type"] == "dir":
                                    temp = child
                                    break
                        current_dir = temp
                    else:
                                # уже в корне
                        print("cd: уже в корне")
                    continue
            # cd <папка> например cd level12
                for child in current_dir.get("children", []):
                    if child["name"] == target and child["type"] == "dir":
                        found = child
                        break
                if found:
                    current_dir = found
                    path_stack.append(target)
                else:
                    print(f"cd: нет такой директории: {target}")
            elif parts[0] == "ls":
                if current_dir.get("type") != "dir":
                    print("Ошибка: не директория")  # проверяем, что переменная это папка dir
                    continue

                children = current_dir.get("children", [])  # берем содержимое папки
                if not children:
                    print("(пусто)")
                else:
                    for child in children:
                        print(child["name"])  # выводим имена всех папок или файлов

            elif parts[0] == "pwd":
                if not path_stack:
                    print("/")
                else:  # например ["level1","level2"]
                    print("/" + "/".join(path_stack))  # превращаем список в строку и выводим
            elif parts[0] == "rev":
                if len(parts) < 2:
                    print("rev: нет аргумента")
                    continue
                name = parts[1]
                content = None  # сюда запишем текст, который нужно перевернуть
                if "children" in current_dir:  # проверим, есть ли файл с таким именем в текущей папке
                    for item in current_dir["children"]:
                        if item["name"] == name and item["type"] == "file":
                            content = item.get("content", "")
                            break
                # если нашли файл, то переворачиваем содержимое
                if content is not None:
                    print(content[::-1])
                else:
                            # иначе просто переворачиваем то, что ввёл пользователь
                    print(name[::-1])
            else:
                print(f"error: {args.script} at line {line_number}: command not found")


if args.debug:
    print("DEBUG: vfs_path =", vfs_path)
    print("DEBUG: script =", script)
    print("DEBUG: debug =", debug)

while True:
    prompt=f"{username}@{hostname}:~$ "
    command = input(prompt)
    parts=command.split()
    #cmd, cmd2, args = parts[1, 2, 3,]
    if len(parts)==0:
        continue

    if parts[0] == "exit":
        break
    #print("Вы ввели:", command)
    elif parts[0]== "echo":
        print(" ".join(parts[1:]))
    elif parts[0] == "cd":
        if len(parts) == 1:
            # Переход в корень
            current_dir = vfs
            path_stack = []
            continue
        target = parts[1]
        found = None
        if target == "..":               # # cd .. вернуться на уровень выше
            if path_stack:
                path_stack.pop()
                                        #пересобираем текущую директорию по стеку
                temp = vfs
                for folder in path_stack:
                    for child in temp.get("children", []):
                        if child["name"] == folder and child["type"] == "dir":
                            temp = child
                            break
                current_dir = temp
            else:
                                                            #уже в корне
                print("cd: уже в корне")
            continue

                                                    #cd <папка> например cd level12
        for child in current_dir.get("children", []):
            if child["name"] == target and child["type"] == "dir":
                found = child
                break

        if found:
            current_dir = found
            path_stack.append(target)
        else:
            print(f"cd: нет такой директории: {target}")

    elif parts[0] == "ls":
        if current_dir.get("type") != "dir":
            print("Ошибка: не директория") #проверяем, что переменная это папка dir
            continue

        children = current_dir.get("children", []) #берем содержимое папки
        if not children:
            print("(пусто)")
        else:
            for child in children:
                print(child["name"]) #выводим имена всех папок или файлов

    elif parts[0] == "pwd":
        if not path_stack:
            print("/")
        else:           #например ["level1","level2"]
            print("/" + "/".join(path_stack))   #превращаем список в строку и выводим
    elif parts[0] == "rev":
        if len(parts) < 2:
            print("rev: нет аргумента")
            continue
        name = parts[1]
        content = None  # сюда запишем текст, который нужно перевернуть
        if "children" in current_dir:      #проверим, есть ли файл с таким именем в текущей папке
            for item in current_dir["children"]:
                if item["name"] == name and item["type"] == "file":
                    content = item.get("content", "")
                    break
        #если нашли файл, то переворачиваем содержимое
        if content is not None:
            print(content[::-1])
        else:
            # иначе просто переворачиваем то, что ввёл пользователь
            print(name[::-1])

    else:
        print("Command not found")