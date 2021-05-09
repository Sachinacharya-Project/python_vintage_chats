from database import database, Session, error, userassign
from colorama import init, Fore
from os import system

init(autoreset=True)
mydb, cursor = database()
session = Session()

def give_menu():
    print("""{}Choose Options
        1. Change Receipent
        2. Clear Screen
        3. Exit
    """.format(Fore.BLUE))
    index = input("Index: ")
    if index.isdigit():
        index = int(index)
        if index == 1:
            while True:
                if userassign():
                    return True
        elif index == 2:
            system("cls")
            return True
        elif index == 3:
            session.update("close", "True")
            session.update("uid", "None")
            session.update("isLogged", "False")
            session.update("messagewith_id", "None")
            session.update("messagewith_name", "None")
            session.update("fullname", "None")
            exit()
    else:
        error("Non-Integer in not supported")
while True:
    session = Session()
    if session.get("isLogged"):
        myuid = session.get("uid")
        receiver_id = session.get("messagewith_id")
        receiver_name = session.get("messagewith_name")
        if receiver_id is not None:
            print("""Information
            You can have your Conversation started
            type '->menu' to Choose Menu
            """)
            while True:
                session = Session()
                receiver_id = session.get("messagewith_id")
                receiver_name = session.get("messagewith_name")
                message = input("Your message[to: {}]]\n".format(receiver_name))
                if message == '->menu':
                    while True:
                        if give_menu():
                            break
                else:
                    cursor.execute("INSERT INTO `messages`(`from_id`, `to_id`, `messages`) VALUES('{}', '{}', '{}')".format(myuid, receiver_id, message))
                    mydb.commit()
        else:
            error("Conversation Halted", "You need to Open Conversation in chats\nPlease Press <Return> when Done!")
            input("")
    else:
        error("LoggedIn Error", "It Looks Like you are not logged\nPlease Login to Continue")
        input("Press <Return> When Ready")