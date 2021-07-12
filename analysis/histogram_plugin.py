
from PyQt5.QtWidgets import QGridLayout, QPushButton
from qtpy.QtWidgets import QWidget
import pyqtgraph as pg
import numpy as np

from napari_plugin_engine import napari_hook_implementation

class HistWidget(QWidget):
    
    def __init__(self, napari_viewer):
        self.viewer = napari_viewer
        super().__init__()
       
        layout = QGridLayout()
        self.plot_widget = pg.PlotWidget(name="Histogram")
        self.hist_button = QPushButton('Plot Histogram', self)
        self.hist_button.clicked.connect(self.plot_histogram)
        layout.addWidget(self.plot_widget)
        layout.addWidget(self.hist_button)
        self.setLayout(layout) 
        self.plot = self.plot_widget.plot()
        self.plot_histogram()
        
        self.viewer.dims.events.connect(self.on_slider)

    def plot_histogram(self):
        if self.viewer.active_layer is None:
            return
        self.plot.clear()
        try:
            data = self.viewer.active_layer._data_view
        except:
            data = self.viewer.active_layer.data

        h, hx = np.histogram(data, bins=256)
        green = (0,255,0)
        #self.plot = self.plot_widget.plot()
        self.plot.setPen(green)
        self.plot.setData(x=hx[:-1], y=h)

    def on_slider(self, event):
        print("Slider change")
        print(event.source)
        self.plot_histogram()
        

@napari_hook_implementation
def napari_experimental_provide_dock_widget():
    return HistWidget

        