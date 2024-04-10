import sys
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QLabel, QLineEdit, QVBoxLayout, QHBoxLayout
import random

class MainWindow(QMainWindow):
    def __init__(self, name, options):
        super().__init__()
        self.setFixedSize(QSize(500,900))
        self.setWindowTitle(f'{name}')

        self.input = QLineEdit()
        self.output = QLabel()
        self.output.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.output.setStyleSheet("border-image: url(8ball.jpg); color: white;")
        self.options = options
        self.input.returnPressed.connect(self.query)
        qbutton = QPushButton('Ответить')
        qbutton.clicked.connect(self.query)
        rbutton = QPushButton('Сначала')
        rbutton.clicked.connect(self.restart)
        
        buttonpanel_layout = QHBoxLayout()
        buttonpanel_layout.addWidget(qbutton)
        buttonpanel_layout.addWidget(rbutton)
        buttonpanel = QWidget()
        buttonpanel.setLayout(buttonpanel_layout)

        layout = QVBoxLayout()
        layout.addWidget(self.input)
        layout.addWidget(self.output)
        layout.addWidget(buttonpanel)

        root = QWidget()
        root.setLayout(layout)
        self.setCentralWidget(root)
    def query(self):
        if self.input.text() != "":
            self.output.setText(random.choice(self.options))
        else:
            self.output.setText("Сначала задай вопрос!")
    def restart(self):
        self.input.clear()
        self.output.clear()
    def mouseDoubleClickEvent(self, e):
        display = ("Идти сегодня в университет?", "Выступить на семинаре?", "Купить пельмени?")
        self.input.setText(random.choice(display))

random.seed()
app = QApplication(sys.argv)
app.setStyleSheet("QLabel, QLineEdit, QPushButton { font-size: 24pt;}")

dmjr = MainWindow("Вопросы да/нет", ('Да', 'Нет'))
dmjr.show()
dmsr = MainWindow("Шар судьбы", 
                  ('Бесспорно',
                   'Предрешено',
                   'Никаких\nсомнений',
                   'Определенно да',
                   'Можешь быть\nуверен в этом',
                   'Мне кажется - да',
                   'Вероятнее всего',
                   'Хорошие перспективы',
                   'Знаки говорят - да',
                   'Да',
                   'Пока не ясно,\nпопробуй снова',
                   'Спроси позже',
                   'Лучше\nне рассказывать',
                   'Сейчас нельзя\nпредсказать',
                   'Сконцентрируйся\nи спроси опять',
                   'Даже не думай',
                   'Мой ответ - нет',
                   'По моим данным - нет',
                   'Перспективы\nне очень хорошие',
                   'Весьма сомнительно'))
dmsr.show()
app.exec()