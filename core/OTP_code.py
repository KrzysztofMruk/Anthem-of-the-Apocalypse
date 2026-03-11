import os, sys, string, random,json


class Encode:
    def __init__(self):
        self.alfabetUP = string.ascii_uppercase  # 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        self.alfabetCoded = {}  # Słownik zakodowanego alfabetu

        new_message = ""
        new_messeage_list = []
        for i in range(0,35):
            x = random.randint(0,25)
            new_messeage_list.append(str(self.alfabetUP[x]))

        new_message = "".join(new_messeage_list)
        print(new_message)

        self.messages = {0: new_message} # Słownik wiadomości (wiadomość testowa: "XPLWMJQEZTRNAGVBOCKDSHUIFPYXEMQRWDJ")

        self.messOP1 = {0: new_message} # Słownik wiadomości (wiadomość testowa: "XPLWMJQEZTRNAGVBOCKDSHUIFPYXEMQRWDJ")
        self.messOP2 = {0: new_message} # Słownik wiadomości (wiadomość testowa: "XPLWMJQEZTRNAGVBOCKDSHUIFPYXEMQRWDJ")

        self.packOP1 = {} #zakodowana wiadomość i klucz dla gracza OP1
        self.packOP2 = {} #zakodowana wiadomość i klucz dla gracza OP2

        self.alfabet_OTP()
        self.MaK_path = '../AOA/core/json/messages_and_keys.json'
        self.pack_operators_coded_message()
        self.write_to_file()
        #self.new_message()

    def alfabet_OTP(self):  # nowy kod One-Time Pad
        alpha = random.sample(range(0, 26), 26)  # Generowanie 26 unikalnych liczb
        print(alpha)

        for i, l in enumerate(self.alfabetUP):  # Kodowanie wartości
            self.alfabetCoded[l] = alpha[i]  # Przypisanie wartości do słownika
        print(self.alfabetCoded)

    def new_message(self):
        message_length = 35
        #for j in range(len(self.messOP1)):
        self.coded_messages = {0: []}  # Słownik zakodowanych wiadomości (zainicjalizowane klucze)
        self.keys = {0: []}  # Słownik zakodowanych kluczy (zainicjalizowane klucze)
        message = self.messages[0]
        # self.alfabet_OTP()  # Inicjalizacja nowego kodu One-Time Pad
        for i in range(message_length):
            m = message[i]
            k = random.choice(self.alfabetUP)
            value_mess_alfa = self.alfabetCoded[m]
            value_key_alfa = self.alfabetCoded[k]
            value_mess = (value_mess_alfa + value_key_alfa) % 26
            self.coded_messages[0].append(value_mess)
            self.keys[0].append(value_key_alfa)

    def pack_operators_coded_message(self):
        self.new_message()

        self.packOP1["cdmess"] = self.coded_messages[0]
        self.packOP1["key"] = self.keys[0]
        print("Wiadomość:", self.messOP1[0])
        print("Zakodowana wiadomość: ", self.packOP1["cdmess"])
        print("Klucz:", self.packOP1["key"])
        print("----------------------------------------------------------------")
        self.new_message()
        self.packOP2["cdmess"] = self.coded_messages[0]
        self.packOP2["key"] = self.keys[0]
        print("Wiadomość:", self.messOP2[0])
        print("Zakodowana wiadomość: ", self.packOP2["cdmess"])
        print("Klucz:", self.packOP2["key"])
    def write_to_file(self):
        with open(self.MaK_path, 'r') as plik_mess_and_keys:
            mess_and_keys_parameters = json.load(plik_mess_and_keys)
            # Modyfikacja odpowiedniego wpisu
            for message in mess_and_keys_parameters['messages']:
                if message ['id'] == 0:
                    message['value'] = self.messOP1[0]
                elif message ['id'] == 1:
                    message['value'] = self.messOP2[0]
            for coded_message in mess_and_keys_parameters['coded_messages']:
                if coded_message ['id'] == 0:
                    coded_message['value'] = self.packOP1["cdmess"]
                elif coded_message ['id'] == 1:
                    coded_message['value'] = self.packOP2["cdmess"]
            for coded_alphabet in mess_and_keys_parameters['coded_alphabet']:
                if coded_alphabet ['id'] == 0:
                    coded_alphabet['value'] = self.alfabetCoded
            for key in mess_and_keys_parameters['keys']:
                if key['id'] == 0:
                    key['value'] = self.packOP1["key"]
                elif key['id'] == 1:
                    key['value'] = self.packOP2["key"]



        with open('../AOA/core/json/messages_and_keys.json', 'w') as plik_mess_and_keys:
            json.dump(mess_and_keys_parameters, plik_mess_and_keys, indent=4)

# Uruchomienie klasy
#encoder = Encode()
