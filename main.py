import sys
from PyQt5.QtWidgets import QApplication
from screenshot import MyWin

app = QApplication(sys.argv)
ScreenShot = MyWin()
ScreenShot.show()
app.exec()