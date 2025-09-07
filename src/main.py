import getpass
import socket
username=getpass.getuser()
hostname=socket.gethostname()

while True:
    prompt=f"{username}@{hostname}:~$ "
    command = input(prompt)

    if command.strip() == "exit":
        print("Выход из эмулятора...")
        break
    print("Вы ввели:", command)

