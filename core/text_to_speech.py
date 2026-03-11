# Import the required module for text
# to speech conversion
from gtts import gTTS
from core import OTP_code as otp

# This module is imported so that we can
# play the converted audio
import os, json

class Main():
    def __init__(self):
        otp.Encode()
        self.read_MaK_file()
        self.text_to_speech()

    def text_to_speech(self):
        #OTP = otp.Encode()
        # The text that you want to convert to audio
        OP1text = "This is not a drill. Code for the first operator:"+str(self.coded_message_OP1)
        OP2text = "This is not a drill. Code for the second operator:"+str(self.coded_message_OP2)

        # Language in which you want to convert
        language = 'en'

        # Passing the text and language to the engine,
        # here we have marked slow=False. Which tells
        # the module that the converted audio should
        # have a high speed
        myobj = gTTS(text=OP1text, lang=language, slow=False)
        myobj1 = gTTS(text=OP2text, lang=language, slow=False)

        # Saving the converted audio in a mp3 file named
        # welcome
        relative_path = os.path.join('.', 'sounds')  # Ścieżka względna do folderu sounds

        file_name = "op1Order.mp3"  # Nazwa pliku
        file_name1 = "op2Order.mp3"  # Nazwa pliku

        # Upewnij się, że folder sounds istnieje
        os.makedirs(relative_path, exist_ok=True)

        # Zapisz plik w określonym folderze
        file_path = os.path.join(relative_path, file_name)
        file_path1 = os.path.join(relative_path, file_name1)
        myobj.save(file_path)
        myobj1.save(file_path1)
        print(file_path)
        print(file_path1)
        print("check")
    def read_MaK_file(self):
        self.MaK_path = '../AOA/core/json/messages_and_keys.json'
        with open(self.MaK_path, 'r') as plik_mess_and_keys:
            mess_and_keys_parameters = json.load(plik_mess_and_keys)
            # Odczytywanie odpowiedniego wpisu
            for coded_message in mess_and_keys_parameters['coded_messages']:
                if coded_message ['id'] == 0:
                    self.coded_message_OP1 = coded_message['value']
                elif coded_message ['id'] == 1:
                    self.coded_message_OP2 = coded_message['value']

#text_to_speech()
# Playing the converted file
#os.system(file_path)