import sys
import os
from googletrans import Translator
import googletrans
import speech_recognition as sr
import pyttsx3
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QInputDialog, QMessageBox, QLineEdit
from design import Ui_MainWindow
from sendemail import SendEmail

class Main(QtWidgets.QMainWindow):
    outText=None
    def __init__(self,parent=None):
        super(Main, self).__init__(parent=parent)
        self.ui = Ui_MainWindow()
        self.send = SendEmail()
        self.ui.setupUi(self)
        self.addLanguange()
        self.ui.translat_button.clicked.connect(self.translate)
        self.ui.texttospeech.clicked.connect(self.textToSpeech)
        self.ui.speechtotext.clicked.connect(self.speechToText)
        self.ui.email.clicked.connect(self.toSendmail)

    def addLanguange(self):
        self.ui.outLan.addItems(googletrans.LANGUAGES.values())

    def getText(self):
        text, okPressed = QInputDialog.getText(self, "Get text", "Your Email:", QLineEdit.Normal, "")
        if okPressed and text != '':
            return text
    
    def translate(self):
        inputText = self.ui.input_text.toPlainText()
        if inputText == "":
            self.errorMessage("Please enter value!")
        else:
            try:
                print(inputText)
                lang_out = self.ui.outLan.currentText()
                print(lang_out)
                translator = Translator()
                translate = translator.translate(inputText, dest=f'{lang_out}')
                print(translate)
                self.ui.output_text.setText(f"{translate.text}")
                self.ui.output_text_2.setText(f"{translate.pronunciation}")
                self.outText = translate.pronunciation
            except Exception as e:
                self.errorMessage(e)

    def errorMessage(self, message):
        print(message)
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setWindowTitle('Error!!')
        msg.setText(str(message))
        msg.exec_()

    def SpeakText(self, command):
        engine = pyttsx3.init()
        engine.say(command)
        engine.runAndWait()

    def speechToText(self):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source)
            print("Please say something")
            audio = r.listen(source)
            print("Recognizing Now .... ")     
            # recognize speech using google    
            try:
                print("You have said \n" + r.recognize_google(audio))
                self.ui.input_text.setText(r.recognize_google(audio))
                self.translate()
                print("Audio Recorded Successfully \n ")
            except Exception as e:
                print("Error :  " + str(e))
            # write audio
            # with open("recorded.wav", "wb") as f:
            #     f.write(audio.get_wav_data())

    def textToSpeech(self):
        inText = self.ui.input_text.toPlainText()
        if inText == "":
            self.errorMessage("Please enter value!")
        else:
            outText = self.ui.output_text.toPlainText()
            self.SpeakText(inText)
            self.SpeakText(outText)
            self.SpeakText(self.outText)

    def toSendmail(self):
        inText = self.ui.input_text.toPlainText()
        if inText == "":
            self.errorMessage("Please enter value!")
        else:
            outText = self.ui.output_text.toPlainText()
            email=self.getText()
            # print(email)
            body = f'''
            Translate Application Result.
            
            Input:- {inText}
            
            Output:- {outText}
            pronunciation:- {self.outText}
            
            Thankyou for using this Application!!!
            '''
            bol = self.send.send_email(recipients=email, body=body)
            if bol:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setWindowTitle('Email Sent!!')
                msg.setText("Send mail Successfully!!!")
                msg.exec_()
            else:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setWindowTitle('Error!!')
                msg.setText("Please Use Different Mail!!\nExample: hello.dev@gmail.com")
                msg.exec_()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = Main()
    window.show()
    sys.exit(app.exec_())
