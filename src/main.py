import getpass
import socket
username=getpass.getuser()
hostname=socket.gethostname()

while True:
    prompt=f"{username}@{hostname}:~$ "
    command = input(prompt)
    parts=command.split()

    if command.strip() == "exit":
        print("Выход из эмулятора...")
        break
    #print("Вы ввели:", command)
    elif parts[0]== "echo":
        print(" ".join(parts[1:]))
    else:
        print("Command not found")
