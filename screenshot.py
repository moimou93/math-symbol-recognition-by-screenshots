from PyQt5.QtGui import QPainter, QKeySequence,QFont
from PyQt5.QtWidgets import QLabel, QVBoxLayout,QMainWindow, QApplication, QPushButton, QFileDialog, QWidget, QMessageBox, QShortcut
from PyQt5.QtCore import Qt, pyqtSignal
from predict import judge
# 全局变量
img = None
img_path = ""  # 新增的全局变量，用于存储图片路径

latex_symbols = {
    '!': '!',
    '(': '(',
    '(_printing': '(',
    ')': ')',
    ')_printing': ')',
    '+': '+',
    '+_printing': '+',
    ',': ',',
    '-': '-',
    '-_printing': '-',
    '0': '0',
    '0_printing': '0',
    '1': '1',
    '1_printing': '1',
    '2': '2',
    '2_printing': '2',
    '3': '3',
    '3_printing': '3',
    '4': '4',
    '4_printing': '4',
    '5': '5',
    '5_printing': '5',
    '6': '6',
    '6_printing': '6',
    '7': '7',
    '7_printing': '7',
    '8': '8',
    '8_printing': '8',
    '9': '9',
    '9_printing': '9',
    '=': '=',
    '=_printing': '=',
    'A': 'A',
    'alpha': '\\alpha',
    'ascii_124': '\\vert',
    'a_printing': 'a',
    'b': 'b',
    'beta': '\\beta',
    'b_printing': 'b',
    'C': 'C',
    'cos': '\\cos',
    'c_printing': 'c',
    'd': 'd',
    'Delta': '\\Delta',
    'div': '\\div',
    'div_printing': '\\',
    'e': 'e',
    'exists': '\\exists',
    'f': 'f',
    'forall': '\\forall',
    'forward_slash': '/',
    'G': 'G',
    'gamma': '\\gamma',
    'geq': '\\geq',
    'gt': '>',
    'H': 'H',
    'i': 'i',
    'in': '\\in',
    'infty': '\\infty',
    'int': '\\int',
    'int_printing': '\\int',
    'j': 'j',
    'k': 'k',
    'l': 'l',
    'lambda': '\\lambda',
    'ldots': '\\ldots',
    'leq': '\\leq',
    'lim': '\\lim',
    'log': '\\log',
    'lt': '<',
    'M': 'M',
    'mu': '\\mu',
    'N': 'N',
    'neq': '\\neq',
    'neq_printing': '\\neq',
    'o': 'o',
    'p': 'p',
    'phi': '\\phi',
    'pi': '\\pi',
    'pm': '\\pm',
    'prime': '\\prime',
    'p_printing': 'p',
    'q': 'q',
    'q_printing': 'q',
    'R': 'R',
    'rightarrow': '\\rightarrow',
    'S': 'S',
    'sigma': '\\sigma',
    'sin': '\\sin',
    'sqrt': '\\sqrt',
    'sqrt_printing': '\\sqrt',
    'star_printing': '*',
    'sum': '\\sum',
    'sum_printing': '\\sum',
    'T': 'T',
    'tan': '\\tan',
    'theta': '\\theta',
    'times': '\\times',
    'u': 'u',
    'v': 'v',
    'w': 'w',
    'x': 'x',
    'x_printing': 'x',
    'y': 'y',
    'y_printing': 'y',
    'z': 'z',
    'z_printing': 'z',
    '[': '[',
    '[_printing': '[',
    ']': ']',
    ']_printing': ']',
    '{': '{',
    '}': '}',
}


class MyWin(QMainWindow):
    def __init__(self):
        super(MyWin, self).__init__()
        self.initUi()
    def initUi(self):
        self.setWindowTitle("截图")
        self.resize(200, 100)
        self.move(2360, 1280)
        self.btn = QPushButton('截图', self)
        self.btn.setGeometry(20, 20, 60, 60)
        self.btn.clicked.connect(self.click_btn)
        shortcut = QShortcut(QKeySequence('Alt+Z'), self)
        shortcut.activated.connect(self.click_btn)

    def click_btn(self):
        self.showMinimized()
        self.screenshot = ScreenShotsWin()
        self.screenshot.showFullScreen()

class ScreenShotsWin(QMainWindow):
    oksignal = pyqtSignal()

    def __init__(self):
        super(ScreenShotsWin, self).__init__()
        self.initUI()
        self.start = (0, 0)
        self.end = (0, 0)

    def initUI(self):
        self.setWindowOpacity(0.2)
        self.oksignal.connect(lambda: self.screenshots(self.start, self.end))

    def screenshots(self, start, end):
        global img, img_path  # 声明使用全局变量img_path
        x = min(start[0], end[0])
        y = min(start[1], end[1])
        width = abs(end[0] - start[0])
        height = abs(end[1] - start[1])

        des = QApplication.desktop()
        screen = QApplication.primaryScreen()
        if screen:
            self.setWindowOpacity(0.0)
            pix = screen.grabWindow(des.winId(), x, y, width, height)
            img = pix  # 更新全局变量 img
            # 获取并保存截图文件路径
            fileName, _ = QFileDialog.getSaveFileName(self, '保存图片', '.', ".jpg")
            if fileName:
                pix.save(fileName + ".jpg")
                img_path = fileName + ".jpg"  # 更新全局变量 img_path
        else:
            pix = None

        ans = judge(img_path)

        self.result_win = ResultWin(ans)
        self.result_win.show()

        self.close()

    def paintEvent(self, event):
        x = self.start[0]
        y = self.start[1]
        w = self.end[0] - x
        h = self.end[1] - y

        pp = QPainter(self)
        pp.drawRect(x, y, w, h)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.start = (event.pos().x(), event.pos().y())

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.end = (event.pos().x(), event.pos().y())
            self.oksignal.emit()
            self.update()

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton:
            self.end = (event.pos().x(), event.pos().y())
            self.update()

class ResultWin(QMainWindow):
    def __init__(self, result_text):
        super(ResultWin, self).__init__()
        self.result_text = result_text
        self.initUI()

    def initUI(self):
        if '_printing' in self.result_text:
            self.result_text = self.result_text[:-9]

        self.setWindowTitle("结果")
        self.resize(300, 200)  # 增加了窗口高度以容纳按钮

        # 创建 QLabel 用于显示结果
        self.label = QLabel(self.result_text, self)

        # 设置字体和字号
        font = QFont('Arial', 16)  # 设置字体为 Arial，字号为 16
        self.label.setFont(font)

        # 创建“复制到剪贴板”按钮
        copy_button = QPushButton('复制到剪贴板', self)
        copy_button.clicked.connect(self.copy_to_clipboard)

        # 创建“转换为Latex格式”按钮
        latex_button = QPushButton('转换为Latex格式',self)
        latex_button.clicked.connect(self.trans_to_latex)

        # 创建布局并将 QLabel 和按钮添加到布局中
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.label)
        self.layout.addWidget(copy_button)
        self.layout.addWidget(latex_button)

        # 创建中央窗口部件并设置布局
        central_widget = QWidget()
        central_widget.setLayout(self.layout)
        self.setCentralWidget(central_widget)

    def copy_to_clipboard(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.result_text)
        QMessageBox.information(self, "提示", "你已将结果复制到剪贴板上")

    def trans_to_latex(self):
        self.layout.removeWidget(self.label)
        self.label = QLabel(latex_symbols[self.result_text], self)
        font = QFont('Arial', 16)  # 设置字体为 Arial，字号为 16
        self.label.setFont(font)
        self.layout.addWidget(self.label)
        self.result_text = latex_symbols[self.result_text]

# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     ScreenShot = MyWin()
#     ScreenShot.show()
#     sys.exit(app.exec_())
