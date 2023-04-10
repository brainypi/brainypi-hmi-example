# This Python file uses the following encoding: utf-8
import sys
import os
from random import randint

from PySide2.QtWidgets import QApplication, QWidget
from PySide2.QtCore import QFile, Slot, QTimer
from PySide2.QtUiTools import QUiLoader
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
import RPi.GPIO as GPIO


class hmi(QWidget):
    LED_value = False
    LED_GPIO_PIN = 40
    TEMP_value = 0
    def __init__(self):
        super(hmi, self).__init__()
        self.load_ui()
        self.init_ui()
        self.init_gpio()

    def load_ui(self):
        loader = QUiLoader()
        path = os.path.join(os.path.dirname(__file__), "form.ui")
        ui_file = QFile(path)
        ui_file.open(QFile.ReadOnly)
        self.ui = loader.load(ui_file, self)
        ui_file.close()

    def init_ui(self):
        """ Intialize the QT UI 
        """
        # Set Window Title
        self.setWindowTitle("HMI Display")

        # Set the slot for the Pushbutton click
        self.ui.pushButton.clicked.connect(self.gpio_toggle)
        # Set the slot for the Vertical sliders moved
        self.ui.verticalSlider.sliderMoved.connect(self.slider1Moved)
        self.ui.verticalSlider_2.sliderMoved.connect(self.slider2Moved)
        # Set the slot for the Dial moved
        self.ui.dial.sliderMoved.connect(self.dialMoved)
        # Initialize the Graph
        self.initialize_graph1()
        self.initialize_graph2()
        # Set the timers for graph
        self.initialize_timer_for_graph1(100, self.update_graph1_data)
        self.initialize_timer_for_graph2(500, self.update_graph2_data)

    def init_gpio(self):
        """ Intialize GPIO 

        Function initializes GPIO for UI usage later on in the code
        """
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.LED_GPIO_PIN, GPIO.OUT)

    @Slot()
    def gpio_toggle(self):
        """Toggle GPIO on or off 

        Toggles GPIO on or off based on the current state of the GPIO.
        If on the function will turn it off. 
        If off the function will turn it on. 
        """
        if self.LED_value:
            GPIO.output(self.LED_GPIO_PIN, GPIO.LOW)
            self.LED_value = False
            self.ui.pushButton.setText("OFF")
            self.ui.label.setText("LED is OFF")
        else:
            GPIO.output(self.LED_GPIO_PIN, GPIO.HIGH)
            self.LED_value = True
            self.ui.pushButton.setText("ON")
            self.ui.label.setText("LED is ON")

    @Slot()
    def slider1Moved(self, value):
        """Update the LCD value when the slider1 moves
        """
        self.ui.lcdNumber.display((value/10)%20 + 0.01)

    @Slot()
    def slider2Moved(self, value):
        """Update the LCD value when the slider2 moves
        """
        self.TEMP_value = value + 0.01
        self.ui.lcdNumber_2.display(((value)) + 0.01)

    @Slot()
    def dialMoved(self, value):
        """Update the LCD value when the dial moves
        """
        self.ui.lcdNumber_2.display(self.TEMP_value + (value/100))

    def initialize_timer_for_graph1(self, updateTime, updateFunction):
        """Initiallize the timer for graph

        Args:
            1.  updateTime - Time interval in ms for updating the graph value
            2.  updateFunction - The update data function for the graph

        """
        self.timer1 = QTimer()
        self.timer1.setInterval(updateTime)
        self.timer1.timeout.connect(updateFunction)
        self.timer1.start()

    def initialize_timer_for_graph2(self, updateTime, updateFunction):
        """Initiallize the timer for graph

        Args:
            1.  updateTime - Time interval in ms for updating the graph value
            2.  updateFunction - The update data function for the graph

        """
        self.timer2 = QTimer()
        self.timer2.setInterval(updateTime)
        self.timer2.timeout.connect(updateFunction)
        self.timer2.start()

    def initialize_graph1(self):
        """Initialize the Graph1
        """
        pen = pg.mkPen(color=(0, 255, 0), width=2)
        self.ui.graphWidget1 = pg.PlotWidget(self.ui.widget)
        # Set Background colour to white
        self.ui.graphWidget1.setBackground('w')
        # Set Graph Title
        self.ui.graphWidget1.setTitle("CPU Temperature", color="b", size="20pt")
        # Set Graph Axis Labels
        self.ui.graphWidget1.setLabel('left', "Temperature (C)")
        self.ui.graphWidget1.setLabel('bottom', "Time (s)")
        # Set Graph size
        self.ui.graphWidget1.setFixedSize(461, 201)
        # Set Initial Graph points
        self.graph1x = list(range(100))  # 100 time points
        self.graph1y = [0 for _ in range(100)]  # 100 data points
        self.graph1data_line = self.ui.graphWidget1.plot(self.graph1x, self.graph1y, pen=pen)

    def initialize_graph2(self):
        """Initialize the Graph2
        """
        pen = pg.mkPen(color=(255, 0, 0), width=2)
        self.ui.graphWidget2 = pg.PlotWidget(self.ui.widget_2)
        # Set Background colour to white
        self.ui.graphWidget2.setBackground('w')
        # Set Graph Title
        self.ui.graphWidget2.setTitle("Random Value - Pressure", color="b", size="20pt")
        # Set Graph Axis Labels
        self.ui.graphWidget2.setLabel('left', "Pressure (ba)")
        self.ui.graphWidget2.setLabel('bottom', "Hour (H)")
        # Set Graph size
        self.ui.graphWidget2.setFixedSize(461, 201)
        # Set Initial Graph points
        self.graph2x = list(range(100))  # 100 time points
        self.graph2y = [randint(0, 100) for _ in range(100)]  # 100 data points
        self.graph2data_line = self.ui.graphWidget2.plot(self.graph2x, self.graph2y, pen=pen)

    def update_graph1_data(self):
        """Update the Graph1
        """
        self.graph1x = self.graph1x[1:]  # Remove the first x element.
        self.graph1x.append(self.graph1x[-1] + 1)  # Add a new value 1 higher than the last.

        self.graph1y = self.graph1y[1:]  # Remove the first
        temperature = self.get_cpu_temperature()
        self.graph1y.append(temperature)  # Add a new temperature value.

        self.graph1data_line.setData(self.graph1x, self.graph1y)  # Update the data.

    def update_graph2_data(self):
        """Update the Graph2
        """
        self.graph2x = self.graph2x[1:]  # Remove the first x element.
        self.graph2x.append(self.graph2x[-1] + 1)  # Add a new value 1 higher than the last.

        self.graph2y = self.graph2y[1:]  # Remove the first
        self.graph2y.append(randint(0, 100))  # Add a new random value.

        self.graph2data_line.setData(self.graph2x, self.graph2y)  # Update the data.

    def get_cpu_temperature(self):
        """Helper function which gets the live system CPU Temperature value
        """
        file1 = open("/sys/devices/virtual/thermal/thermal_zone0/temp", "r")
        CPU_temp = str(file1.readline())
        file1.close()
        CPU_temp = float(int(CPU_temp)/1000)
        return CPU_temp

if __name__ == "__main__":
    app = QApplication([])
    widget = hmi()
    widget.show()
    sys.exit(app.exec_())
