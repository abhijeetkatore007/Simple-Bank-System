# Write your code here
from random import randint


import sqlite3
conn = sqlite3.connect('card.s3db')
cur = conn.cursor()

# TABLE card creation
lst = {}

cur.execute('CREATE TABLE IF NOT EXISTS card ('
                'id INTEGER,'
                'number TEXT,'
                'pin TEXT, '
                'balance INTEGER DEFAULT 0);')
conn.commit()

bal = 0

global str

# str = str(mar)
def new_card():
    key = '400000' + ''.join([str(randint(0, 9)) for x in range(9)])
    pin = list(str(key))
    lst1 = []
    lst2 = []
    '''print(pin)'''
    for i in range(0, len(pin), 2):
        d = int(pin[i])*2
        if d //10 != 0:
            d = d // 10 + d % 10
        '''print(d) '''
        lst1.append(d)
    # print(lst1)

    for i in range(1, len(pin) - 1, 2):
        d = int(pin[i])
        lst2.append(d)
    # print(lst2)
    t = sum(lst1 + lst2)
    # print(t)
    checksum = (10 - t % 10) if t % 10 != 0 else t
    if checksum % 10 == 0:
        checksum = 0
    key = key + str(checksum)
    # print(checksum)
    lst[key] = ''.join([str(randint(0, 9)) for x in range(4)])
    cur.execute(f"""
                INSERT INTO card (id, number, pin)
                VALUES({len(lst)},{key},{lst[key]});    
    """), conn.commit()
    print(cur.fetchall())
    print(f"\nYour card has been created\nYour card number:\n{int(key)}\nYour card PIN:\n{lst[key]}")
    print(f"{lst.keys()}\n{lst.values()}")
    # return lst


def acc_login():
    print(cur.fetchall())
    card_no = input("Enter your card number:\n")
    inp = input("Enter your PIN:\n")
    cur.execute(f"""Select number, pin from card where number = {str(card_no)} and pin = {str(inp)}""")
    try:
        a,b = cur.fetchone()
        print(a, b)
        print(card_no, inp)
        if str(card_no) == str(a):

            # if not lst.get(card_no) == inp:
            if not str(b) == str(inp):
                print("\nWrong card number or PIN!")
            else:
                print(f"\nYou have successfully logged in!")
                print(f"{lst.keys()}\n{lst.values()}")
                while True:
                    # command = input(f"\n1. Balance\n2. Log out\n0. Exit\n")
                    command = input("""1. Balance
2. Add income
3. Do transfer
4. Close account
5. Log out
0. Exit
""")
                    if command == "1":
                        cur.execute(f"""
                        Select balance from card where number = {card_no};                    
                        """)
                        # bal, *_ = cur.fetchone() 
                        bal = cur.fetchone()[0] 
                        
                        # print(f"\nBalance: {ball} type: {type(ball)}")
                        print(f"\nBalance: {bal}")

                    elif command == "2":
                        # Enter income:
                        # >10000
                        # Income was added!
                        money = input("Enter income:")
                        cur.execute(f"""

                        UPDATE CARD SET balance = balance + {money} WHERE number = {card_no}
                        ;
                        """)
                        conn.commit()
                        print(f"Income was added!")
                        

                    elif command == "3":
                        try:
                            acct_no = input(f"\nTransfer\nEnter card number:\n")
                            pin1 = acct_no
                            lst1 = []
                            lst2 = []
                            '''print(pin)'''
                            for i in range(0, 16, 2):
                                d = int(pin1[i])*2
                                if d //10 != 0:
                                    d = d // 10 + d % 10
                                '''print(d) '''
                                lst1.append(d)
                            # print(lst1)

                            for i in range(1, 16 - 1, 2):
                                d = int(pin1[i])
                                lst2.append(d)
                            # print(lst2)
                            t_sum = sum(lst1 + lst2)
                            # print(t_sum)
                            # checksum = 10 - t_sum % 10
                            checksum = (10 - t_sum % 10) if t_sum % 10 != 0 else t_sum
                            if checksum % 10 == 0:
                                checksum = 0
                            # print(f"checksum:{checksum} {acct_no}") # IMPORTANT
                            # key =str(400000089919446) + str(checksum)
                            # print(key)
                            if f"{acct_no}"[-1] == str(checksum):
                                if acct_no not in lst.keys():
                                    print("Such a card does not exist.\n")
                                    
                                else:
                                # b, *_=cur.execute(f"""Select number from card where number = {str(acct_no)}""")
                                    cur.execute(f"""Select number from card where number = {str(acct_no)}""")
                                    b = cur.fetchone()[0]
                                    print(f"From data base: \n{b} {type(b)}")
                                    money = input(f"Enter how much money you want to transfer:\n")

                                    cur.execute(f"""
                                    Select balance from card where number = {card_no};                    
                                    """)
                                    # bal, *_ = cur.fetchone() 
                                    bal = cur.fetchone()[0]
                                    # print(card_no,bal,type(bal), money, type(money))
    ##### update                    
                                    if bal < int(money):
                                        print("Not enough money!")
                                    else:    
                                        cur.execute(f"""

                                        UPDATE CARD SET balance = balance + {money} 
                                        WHERE number = {acct_no}
                                        ;
                                        
                                        """)
                                        conn.commit()
                                        
                                        cur.execute(f"""

                                        UPDATE CARD SET balance = balance - {money} 
                                        WHERE number = {card_no}
                                        ;
                                        
                                        """)
                                        conn.commit()

                                        print("Success!")
                                # elif:
                                #     print()         
                            else:
                                print("Probably you made a mistake in the card number. Please try again!")                  

                        except IndexError:
                            print("Probably you made a mistake in the card number. Please try again!")

                        
                        # Enter card number:
                        # >4000003305160034
                        # Enter how much money you want to transfer:
                        # >5000
                        # Success!
                    

                    elif command == "4":
                        print(a,b)
                        
                        cur.execute(f"DELETE FROM card WHERE number = {a} ")
                        conn.commit()
                        print(f"The account has been closed!")
                        break
                    

                    elif command == "5":
                        print(f"You have successfully logged out!")
                        break
                    
                    elif command == "0":
                        print("\nBye!")
                        cur.execute("""DELETE FROM card""")
                        conn.commit()
                        conn.close()
                        exit()

        
    except TypeError:
        print("\nWrong card number or PIN!")
    
    # for i,b in objects:
    #     a = i
    #     c = b
    #     print(f"Acc no: {i} Pin :{b}")
    #     print(a,c)
    # for i in objects:
    #     print(i)
    #     a, b = i
        # print(a, b)
        # print(card_no, inp)
    # print(a, b)
    # print(card_no, inp)
    # if card_no in lst.keys():
    else:
        print("\nYou have successfully logged out!")
            



# def balance():
command = ""
while command.lower() != "0":
    command = input("\n1. Create an account\n2. Log into account\n0. Exit\n3. Clear\n")
    if command == "1":
        new_card()
    elif command == "2":
        acc_login()
    elif command == "3":
        cur.execute("""DELETE FROM card""")
        conn.commit()
conn.close()