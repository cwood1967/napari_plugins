
from PyQt5.QtWidgets import QGridLayout
from qtpy.QtWidgets import QWidget
import pyqtgraph as pg
import numpy as np

from napari_plugin_engine import napari_hook_implementation

class HistWidget(QWidget):
    
    def __init(self, napari_viewer):
        self.viewer = napari_viewer
        super().__init__()
        
        layout = QGridLayout()
        self.lot_widget = pfg.PlotWidget(name="Histogram")
        layout.addWidget(self.plot_widget)
       
        self.setLayout(layout) 

@napari_hook_implementation
def napari_experimental_provide_dock_widget():
    return HistWidget

        