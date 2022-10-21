import threading
import os
import hashlib
from time import sleep

mark = False


def str_hash(password: str) -> str:
    hash = hashlib.sha512(password.strip().encode())
    hex_hash = hash.hexdigest()
    return hex_hash


def unlock(path_to_file: str) -> None:
    os.system(f'sudo chattr -i {path_to_file}')
    os.system(f"sudo chmod 644 {path_to_file}")


def lock(path_to_file: str) -> None:
    os.system(f'sudo chmod 000 {path_to_file}')
    os.system(f'sudo chattr +i {path_to_file}')


def checker(path: str, template: list[str], default_list: list[str]) -> bool:
    global mark

    while True:

        if not mark:
            break
        current_files = os.listdir()

        new_list = list(set(current_files) ^ set(default_list))
        to_remove = list(set(new_list) & set(template))

        for file in to_remove:
            os.remove(path=path + "/" + file)
        sleep(1)


def password(template: list[str]) -> bool:
    word = input("Enter the password: ")
    hash = str_hash(word)
    return (hash == template[0])


def main():
    arr = os.listdir(path=".")

    template = open(file="./template.tbl", mode="r")
    template_data = template.readlines()
    template_stripped = list(map(str.strip, template_data))
    os.system(f'sudo chmod 400 template.tbl')
    os.system(f'sudo chattr +i template.tbl')

    while True:
        global mark
        message = input(f"Что вы хотите?")
        if message == "lock":
            mark = True
            thr = threading.Thread(target=checker, args=(".", template_stripped, arr)).start()

        elif message == "unlock":
            if password(template_stripped):
                print("Password is correct")
                mark = False
        elif message == "stop":
            mark = False
            break
        if message == "lock" or message == "unlock":
            for template_file in template_stripped[1:]:
                for file in arr:
                    if (template_file == file):
                        print(f"Found {file}")
                        if mark:
                            lock("./" + file)
                        else:
                            unlock("./" + file)

    os.system(f'sudo chattr -i template.tbl')
    os.system(f'sudo chmod 644 template.tbl')


if __name__ == "__main__":
    main()
