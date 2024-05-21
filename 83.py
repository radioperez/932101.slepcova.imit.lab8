import sys
import random
import numpy as np
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QPushButton,
    QSpinBox,
    QLabel,
    QLineEdit,
    QVBoxLayout,
    QHBoxLayout,
    QFormLayout,
)
import pyqtgraph as QtGraph

class Graph(QtGraph.PlotWidget):
    def __init__(self):
        super().__init__()
        self.setBackground("w")

class MainWindow(QMainWindow):
    n_events = 1
    startable: bool = False
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Сбор статистики вероятностей')

        settings = QVBoxLayout()
        # probabilities
        self.probabilities = QFormLayout()
        self.probabilities.addRow("Вероятность 1:", QLineEdit())
        self.probabilities.itemAt(1).widget().textChanged.connect(self.auto_remainder)
        settings.addLayout(self.probabilities)

        # remainder probability
        self.remainder_probability_label = QLabel("Остаточная вероятность: ")
        settings.addWidget(self.remainder_probability_label)

        # add button
        add_event_button = QPushButton("Добавить событие")
        add_event_button.clicked.connect(self.add_event)
        settings.addWidget(add_event_button)
        # remove button
        remove_event_button = QPushButton("Удалить событие")
        remove_event_button.clicked.connect(self.remove_event)
        settings.addWidget(remove_event_button)
        # n of trials
        self.n_trials = QSpinBox(minimum=10, maximum=100_000, singleStep=10)
        settings.addWidget(self.n_trials)

        # start button
        start_button = QPushButton("СТАРТ")
        start_button.clicked.connect(self.start)
        settings.addWidget(start_button)

        # graph
        self.graph = Graph()

        layout = QHBoxLayout()
        layout.addLayout(settings)
        layout.addWidget(self.graph)
        root = QWidget()
        root.setLayout(layout)
        self.setCentralWidget(root)
        
    def add_event(self):
        self.n_events += 1
        event_line = QLineEdit()
        self.probabilities.addRow(f"Вероятность {self.n_events}:", event_line)
        event_line.textChanged.connect(self.auto_remainder)
    def remove_event(self):
        if self.n_events > 1:
            self.n_events -= 1
            self.probabilities.removeRow(self.n_events)
    def auto_remainder(self):
        self.remainder_probability: float = 1
        for itemindex in range(self.n_events):
            item = self.probabilities.itemAt(itemindex, QFormLayout.ItemRole.FieldRole).widget().text()
            try:
                self.remainder_probability -= float(item)
            except ValueError:
                pass
        if self.remainder_probability > 0 and self.remainder_probability <= 1:
            self.startable: bool = True
            self.remainder_probability_label.setText(f"Остаточная вероятность: {self.remainder_probability:.4f}")
        else:
            self.startable: bool = False
            self.remainder_probability_label.setText("Ошибка ввода")
    def start(self):
        if self.startable == False: return

        PROBABILITIES = []
        for itemindex in range(self.n_events):
            item = self.probabilities.itemAt(itemindex, QFormLayout.ItemRole.FieldRole).widget().text()
            try:
                PROBABILITIES.append(float(item))
            except ValueError:
                PROBABILITIES.append(0)
        PROBABILITIES.append(self.remainder_probability)
        BINS = list(range(1, self.n_events+2))
        N_TRIALS = self.n_trials.value()
        
        # generate numbers and collect statistics
        RESULT = random.choices(population = BINS, weights = PROBABILITIES, k = N_TRIALS)
        STATISTICS, _ = np.histogram(RESULT, range = (1, len(BINS)), bins = len(BINS))
        FREQUENCY = [stat/N_TRIALS for stat in STATISTICS]
        print(BINS, FREQUENCY)
        self.draw(BINS, FREQUENCY)
    def draw(self, x, y):
        self.graph.clear()
        hist = QtGraph.BarGraphItem(x = x, height = y, width = 0.9, brush='b')
        self.graph.addItem(hist)
        for index, _ in enumerate(x):
            text = QtGraph.TextItem(f'{y[index]}', color='b')
            text.setPos(x[index],y[index]+0.05)
            self.graph.addItem(text)
    def ping(self):
        print("PING")

random.seed()
app = QApplication(sys.argv)
main = MainWindow()
main.show()
app.exec()
