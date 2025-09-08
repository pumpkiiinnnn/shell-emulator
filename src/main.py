import getpass
import socket
username=getpass.getuser()
hostname=socket.gethostname()

while True:
    prompt=f"{username}@{hostname}:~$ "
    command = input(prompt)
    parts=command.split()

    if parts[0] == "exit":
        break
    #print("Вы ввели:", command)
    elif parts[0]== "echo":
        print(" ".join(parts[1:]))
    elif parts[0] == "cd":
        print("cd " + parts[1])
    elif parts[0] == "ls":
        print("ls " + parts[1])
    #elif parts[0] == "pwd":
    else:
        print("Command not found")
