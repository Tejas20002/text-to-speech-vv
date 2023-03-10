import sys
import os
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QInputDialog
from design import Ui_MainWindow

class Main(QtWidgets.QMainWindow):
    def __init__(self,parent=None):
        super(Main, self).__init__(parent=parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.btn_active = False
        self.ui.translat_button.clicked.connect(self.translate)
    
    def translate(self):
        print("hello")

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
