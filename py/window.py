from PyQt5.QtWidgets import QApplication, QWidget
import sys

class WindowTest(QWidget):
    
    def __init__(self, parent=None):
        super(WindowTest, self).__init__(parent)
        self.setWindowTitle("Traffic Sign Recognition Test")
        self.setFixedSize(800, 600)
        self.show()

if __name__=="__main__":
    app = QApplication(sys.argv)
    windowTest = WindowTest()
    sys.exit(app.exec_())