import sys
import os
from googletrans import Translator
import googletrans
import speech_recognition as sr
import pyttsx3
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QInputDialog, QMessageBox
from design import Ui_MainWindow

class Main(QtWidgets.QMainWindow):
    outText=None
    def __init__(self,parent=None):
        super(Main, self).__init__(parent=parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.addLanguange()
        self.ui.translat_button.clicked.connect(self.translate)
        self.ui.texttospeech.clicked.connect(self.textToSpeech)

    def addLanguange(self):
        self.ui.outLan.addItems(googletrans.LANGUAGES.values())
    
    def translate(self):
        try:
            inputText = self.ui.input_text.toPlainText()
            print(inputText)
            lang_out = self.ui.outLan.currentText()
            print(lang_out)
            translator = Translator()
            translate = translator.translate(inputText, dest=f'{lang_out}')
            print(translate)
            self.ui.output_text.setText(f"{translate.text}\n{translate.pronunciation}")
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
                print("Audio Recorded Successfully \n ")
            except Exception as e:
                print("Error :  " + str(e))
            # write audio
            with open("recorded.wav", "wb") as f:
                f.write(audio.get_wav_data())

    def textToSpeech(self):
        inText = self.ui.input_text.toPlainText()
        outText = self.ui.output_text.toPlainText()
        self.SpeakText(inText)
        self.SpeakText(outText)
        self.SpeakText(self.outText)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = Main()
    window.show()
    sys.exit(app.exec_())
