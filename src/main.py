import getpass
import socket
import argparse
username=getpass.getuser()
hostname=socket.gethostname()

parser = argparse.ArgumentParser(description='эмулятор shell')
parser.add_argument("--vfs-path", help="путь к vfs")
parser.add_argument("--script", help="путь к стартовому скрипту")
parser.add_argument("--debug", action="store_true", help="включить отладочный вывод")

args = parser.parse_args()
vfs_path=args.vfs_path
script=args.script
debug=args.debug

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
                print("cd", " ".join(parts[1:]))
            elif parts[0] == "ls":
                print("ls", " ".join(parts[1:]))
            elif parts[0] == "pwd":
                print("[stub] pwd")
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
        print("cd", " ".join(parts[1:]))
    elif parts[0] == "ls":
        print("ls", " ".join(parts[1:]))
    elif parts[0] == "pwd":
        print("[stub] pwd")
    else:
        print("Command not found")
