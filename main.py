import sys
import os
from googletrans import Translator
import googletrans
import speech_recognition as sr
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QInputDialog, QMessageBox
from design import Ui_MainWindow

class Main(QtWidgets.QMainWindow):
    def __init__(self,parent=None):
        super(Main, self).__init__(parent=parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.addLanguange()
        self.ui.translat_button.clicked.connect(self.translate)

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
            self.ui.output_text.setText(translate.text)
        except Exception as e:
            self.errorMessage(e)

    def errorMessage(self, message):
        print(message)
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setWindowTitle('Error!!')
        msg.setText(str(message))
        msg.exec_()

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

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = Main()
    window.show()
    sys.exit(app.exec_())
