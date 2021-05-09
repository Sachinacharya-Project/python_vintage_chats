from database import Session, error, database, userassign
from getpass import getpass
from colorama import init, Fore
import os
init(autoreset=True)
# Global Values
isUserNotAssigned = True
mydb, cursor = database()
# Checking if use is logged in or not
session = Session()
# RESETING
session.update("close", "False")
session.update("isLogged", "False")
session.update("messagewith_id", "None")
session.update("messagewith_name", "None")
def account_handle(tsk='login'):
    print(tsk.capitalize())
    username = input("Username:\n")
    password = getpass(prompt="Password:\n")
    cursor.execute("SELECT * FROM `user` WHERE `username`='{}' AND `password`='{}'".format(username, password))
    results = cursor.fetchall()
    if len(results) > 0:
        if tsk == 'login':
            uid = results[0][0]
            fullname = results[0][1]
            session.update("uid", uid)
            session.update("isLogged", "True")
            session.update("fullname", fullname)
            return True
        else:
            error("User Already Exist")
    else:
        if tsk == 'login':
            error("User doesnot exist")
        else:
            email = input("Email Address:\n")
            fullname = input("Fullname:\n")
            cursor.execute("INSERT INTO `user`(`name`, `username`, `password`, `email`) VALUES('{}', '{}', '{}', '{}')".format(fullname, username, password, email))
            mydb.commit()
            cursor.execute("SELECT * FROM `user` WHERE `username`='{}'".format(username))
            uid = cursor.fetchall()[0][0]
            session.update("isLogged", "True")
            session.update("uid", uid)
            session.update("fullname", fullname)
            return True
while True:
    session = Session()
    if session.get("isLogged"):
        myuid = session.get("uid")
        myname = session.get("fullname")
        if isUserNotAssigned:
            cursor.execute("SELECT * FROM `messages` WHERE `from_id`='{}' OR `to_id`='{}'".format(myuid, myuid))
            bucket_uid = []
            bucket_name = []
            resultss = cursor.fetchall()
            if len(resultss) > 0:
                for result in resultss:
                    if result[1] == myuid or result[2] == myuid:
                        temp_user = result[1]
                        if temp_user == myuid:
                            temp_user = result[2]
                        cursor.execute("SELECT * FROM `user` WHERE `uid`='{}'".format(temp_user))
                        res = cursor.fetchall()
                        bucket_uid.append(res[0][0])
                        bucket_name.append(res[0][1])
                bucket_uid = list(set(bucket_uid))
                bucket_name = list(set(bucket_name))
                count = 0
                print("""Choose User
                    Choose Following Users to Start Conversation with
                """)
                for name_ in bucket_name:
                    print("{})".format(count+1) ,name_)
                    count +=1
                index = input("Enter index: ")
                if index.isdigit():
                    index = int(index)
                    session.update("messagewith_id", bucket_uid[index - 1])
                    session.update("messagewith_name", bucket_name[index - 1])
                    isUserNotAssigned = False
                else:
                    error("Non-Integer is Prohibited")
            else:
                print("""
                    You don't Have any conversations Going On
                    Choose User
                """)
                cursor.close()
                mydb.close()
                while True:
                    mydb, cursor = database()
                    username = input("Username: ")
                    cursor.execute("SELECT * FROM `user` WHERE `username`='{}'".format(username))
                    resultss = cursor.fetchall()
                    if len(resultss) > 0:
                        session.update("messagewith_id", resultss[0][0])
                        session.update("messagewith_name", resultss[0][1])
                        isUserNotAssigned = False
                        break
                    else:
                        error("Sorry, User doesnot exist")
                        cursor.close()
                        mydb.close()
        else:
            receiver_id = session.get("messagewith_id")
            receiver_name = session.get("messagewith_name")
            # Collecting all the messages
            cursor.execute("SELECT * FROM `messages` WHERE `from_id`='{}' AND `to_id`='{}' OR `from_id`='{}' AND `to_id`='{}'".format(myuid, receiver_id, receiver_id, myuid))
            print("""Messages
            Showing your Conversation with {}
            """.format(receiver_name))
            for result in cursor.fetchall():
                from_name = myname
                to_name = receiver_name
                if result[1] == receiver_id and result[2] == myuid:
                    from_name = receiver_name
                    to_name = myname
                print("""
    [{}
        From: {}
        To: {}
    ]
    {}{}
        """.format(Fore.BLUE, from_name, to_name, Fore.GREEN, result[3]))
                cursor.execute("UPDATE `messages` SET `isnew`='no' WHERE `ID`='{}'".format(result[0]))
                mydb.commit()
            cursor.close()
            mydb.close()
            while True:
                session = Session()
                mydb, cursor = database()
                if session.get("close"):
                    exit()
                if session.get("messagewith_id") != receiver_id:
                    print("""
                    Conversation Recepient has been changed
                    <Return> to continue
                    Clearing Screen
                    """)
                    input("")
                    os.system("cls")
                    # mydb, cursor = database()
                    receiver_id = session.get("messagewith_id")
                    receiver_name = session.get("messagewith_name")
                cursor.execute("SELECT * FROM `messages` WHERE `from_id`='{}' AND `to_id`='{}' OR `from_id`='{}' AND `to_id`='{}'".format(myuid, receiver_id, receiver_id, myuid))
                for result in cursor.fetchall():
                    if result[4] == 'yes':
                        from_name = myname
                        to_name = receiver_name
                        if result[1] == receiver_id and result[2] == myuid:
                            from_name = receiver_name
                            to_name = myname
                        print("""
    [{}
        From: {}
        To: {}
    ]
    {}{}
                        """.format(Fore.BLUE, from_name, to_name, Fore.GREEN, result[3]))
                        cursor.execute("UPDATE `messages` SET `isnew`='no' WHERE `ID`='{}'".format(result[0]))
                        mydb.commit()
                cursor.close()
                mydb.close()
    else:
        """
            Ain't Logged in
            Check if user wants to Logged in or signup
        """
        print("""Choose Options
            1. Login
            2. Signup
        """)
        opt = input("Index: ")
        if opt.isdigit():
            opt = int(opt)
            while True:
                if opt == 1:
                    if account_handle():
                        break
                elif opt == 2:
                    if account_handle("signup"):
                        break
        else:
            error("Non-Integer type in Invalid")