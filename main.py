import random
import sqlite3
import time

conn = sqlite3.connect('card.s3db')  # making of DB
cur = conn.cursor()  # DB cursor for SQlite3 operations

log_ins = dict("")
balances = dict("")
accountID = dict("")
# here we are making a DB table to collect cards info
cur.execute('''         
CREATE TABLE IF NOT EXISTS card(
        id INTEGER,
        number TEXT,
        pin TEXT,
        balance INTEGER DEFAULT 0
);
''')


class Card:

    def __init__(self):  # main body of card creator
        self.spin = random.randint(000000000, 999999999)
        Card.luhnCreate(self)
        cur.execute(f'SELECT pin FROM card WHERE number = {self.cardnumber};')
        self.newchecker = cur.fetchone()
        if self.newchecker == None:
            pass
        else:
            time.sleep(1)
            spin = random.randint(000000000, 999999999)
            Card.luhnCreate(self)
        self.pin = ""
        self.createpin = random.sample(range(10), 4)
        for i in range(4):
            self.pin += str(self.sample[i])
        print("Your card has been created")
        print("Your card number:")
        print(self.cardnumber)
        print("Your card PIN:")
        print(self.pin)
        Card.saveclient(self)

    def luhnCreate(self):  # creates luhn correct card number
        self.numb_luhn = random.sample(range(10), 9)
        self.sample = self.numb_luhn.copy()
        self.counter = 8
        for i in range(0, 9, 2):
            self.sample[i] *= 2
            if self.sample[i] > 9:
                self.sample[i] -= 9
        for i in range(9):
            self.counter += int(self.sample[i])
        if (self.counter % 10) != 0:
            self.numb_luhn.append(- (self.counter % 10) + 10)
        else:
            self.numb_luhn.append(0)
        self.cardnumber = "400000"
        for i in range(10):
            self.cardnumber += str(self.numb_luhn[i])

    def saveclient(self):   # client saving process
        self.x = int(self.cardnumber)
        self.y = int(self.pin)
        self.clientID = self.spin
        cur.execute(f'''
        INSERT INTO card (id, number, pin) VALUES ({self.clientID}, {self.x}, {self.y});
        ''')
        conn.commit()


tmp_check = int()  # tmp checksum for luhn checker
luhn_checksum = int() # luhn checksum for luhn checker

# checks if lg1 is luhn correct or not, returns tmp check with same card num if OK
# for luhn checker debug you can use: 4000001376082491


def luhnChecker(lg1):           # luhn checker body
    global tmp_check, luhn_checksum
    tmp_check = int(0)
    if len(str(lg1)) == 16:
        tmp_luhn = list.copy(list(str(lg1)))
        luhn_checksum = int(tmp_luhn[-1])
        for i in range(0, 15, 2):
            tmp_luhn[i] = int(tmp_luhn[i]) * 2
            if int(tmp_luhn[i]) > 9:
                tmp_luhn[i] = int(tmp_luhn[i]) - 9
        for i in range(0, 15, 1):
            tmp_check += int(tmp_luhn[i])
        if tmp_check % 10 != 0:
            tmp_check = -(tmp_check % 10) + 10
        else:
            tmp_check = 0
        if int(tmp_check) == int(luhn_checksum):
            tmp_check = int(lg1)
            return tmp_check
        else:
            tmp_check = int(lg1)-1000000000000000000
            return tmp_check
    else:
        tmp_check = int(123123)
        return tmp_check


def logged_out(chInt):  # main menu
    if chInt == 1:  # create new card
        spin = Card()  # spin is a cliend ID
    elif chInt == 2:  # login process
        print("Enter your card number:")
        lg1 = str(input())
        luhnChecker(lg1)
        if int(tmp_check) == int(lg1):
            pass
        else:
            print(tmp_check)
            print("Wrong card number!")
            return
        print("Enter your PIN:")
        lg2 = str(input())
        cur.execute(f'SELECT number FROM card WHERE number = {lg1};')
        login_number_token = str(cur.fetchone())
        if login_number_token == 'None':
            pass
        cur.execute(f'SELECT pin FROM card WHERE number = {lg1};')
        login_pin_token = str(cur.fetchone())
        login_pin_token = login_pin_token[2:6]
        if login_pin_token == lg2:
            print("You have successfully logged in!")
            logged_in(lg1)
        else:
            print("""
    Wrong card number or PIN!""")
    elif chInt == 0:  # exit
        print("Bye!")
        conn.commit()
        exit()
    elif chInt == 7:    # debug, deletes all clients to re-create table
        cur.execute('DROP TABLE card;')
        print("table 'card' deleted, please restart this program")
        conn.commit()
        exit()
    elif chInt == 9:  # debug, clients list prints in console
        print("clients:")
        cur.execute('SELECT * FROM card;')
        print(cur.fetchall())
    elif chInt == "":
        print("Wrong input!")
    else:  # wrong num
        print("Wrong input! Please, try again.")


def logged_in(lg1):  # logged in using card num
    cur.execute(f'SELECT balance FROM card WHERE number = {lg1};')
    logged_in_balance = str(cur.fetchone())     # we store balance untill logged out
    logged_in_balance = int(logged_in_balance[1:(len(logged_in_balance) - 2)]) # here we make data look good

    print(f"""
    1. Balance
    2. Add income
    3. Do transfer
    4. Close account
    5. Log out
    0. Exit
                """)
    chInt = int(input())
    if chInt == 1:  # balance
        print("Balance: ", logged_in_balance)
        logged_in(lg1)
    elif chInt == 2:    # add income
        print("""
    Enter income:""")
        logged_in_balance += int(input())
        cur.execute(f'UPDATE card SET balance = {logged_in_balance} WHERE number = {lg1};')
        print("Income was added!")
        conn.commit()
        logged_in(lg1)
    elif chInt == 3:    # transfer
        print("""
    Transfer
    Enter card number:""")
        transfer_card_num = int(input())
        luhnChecker(transfer_card_num)
        if int(transfer_card_num) == int(tmp_check):
            cur.execute(f'SELECT balance FROM card WHERE number = {transfer_card_num};')
            transfer_card_token = str(cur.fetchone())
            if transfer_card_token == "None":
                print("""
    Such a card does not exist.""")
            else:
                transfer_card_token = int(transfer_card_token[1:(len(transfer_card_token) - 2)])
                print("""
    Enter how much money you want to transfer:""")
                transfer_card_value = int(input())
                if (transfer_card_value >= 0) and (transfer_card_value <= logged_in_balance):
                    transfer_card_token += transfer_card_value
                    cur.execute(f'UPDATE card SET balance = balance + {transfer_card_token} WHERE number = {transfer_card_num};')
                    logged_in_balance -= transfer_card_value
                    cur.execute(f'UPDATE card SET balance = {logged_in_balance} WHERE number = {lg1};')
                    print("""
    Success!""")
                    conn.commit()
                elif transfer_card_value > logged_in_balance:
                    print("""
    Not enough money!""")
                else:
                    print("""
    Incorrect transfer value.""")
            logged_in(lg1)
        else:
            print("""
    Probably you made a mistake in the card number. Please try again!""")
            logged_in(lg1)
    elif chInt == 4:    # deletes account
        cur.execute(f'DELETE FROM card WHERE number = {lg1};')
        conn.commit()
        print('The account has been closed!')
        pass
    elif chInt == 5:  # log out
        print("You have successfully logged out!")
        conn.commit()
        pass
    elif chInt == 0:  # exit
        print("Bye!")
        conn.commit()
        exit()
    else:  # wrong input
        print("Wrong")


while True: # infinite roller
    print("""
    1. Create an account
    2. Log into account
    0. Exit""")
    logged_out(int(input()))