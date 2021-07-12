
from test_this import get_displayed_slice
from napari.layers import Shapes
from napari.layers import Image
from PyQt5.QtWidgets import QGridLayout, QPushButton
from qtpy.QtWidgets import QWidget
import pyqtgraph as pg
import numpy as np
from skimage.measure import profile_line

from napari_plugin_engine import napari_hook_implementation

class ProfileWidget(QWidget):
    
    def __init__(self, napari_viewer):
        self.viewer = napari_viewer
        super().__init__()
       
        layout = QGridLayout()
        self.plot_widget = pg.PlotWidget(name="Line Profile")
        self.hist_button = QPushButton('Plot Profile', self)
        self.hist_button.clicked.connect(self.plot_line_profile)
        layout.addWidget(self.plot_widget)
        layout.addWidget(self.hist_button)
        self.setLayout(layout) 
        self.plot = self.plot_widget.plot()
        
        self.viewer.dims.events.connect(self.on_slider)

    def plot_line_profile(self):
        if len(self.viewer.layers.selected) < 1:
            return
        self.plot.clear()
        profile = self.get_profile()
        if profile is None:
            return

        x = np.arange(len(profile))
        self.plot.setPen((255,255,0))
        self.plot.setData(x=x, y=profile)
        
    def get_profile(self):
        line, images = self.get_layers()
        if line is None:
            return None
       
        pt0 = line[0][-2:]
        pt1 = line[1][-2:] 
        profile = profile_line(images[0].data, pt0, pt1)       
        return profile
        
    def on_slider(self, event):
        self.plot_line_profile()

    def get_layers(self):
        selected = self.viewer.layers.selected
        print(selected)
        shape = [s for s in selected if isinstance(s, Shapes)]
        if len(shape) == 0:
            return None, None

        shape = shape[0]
        line = None
        for ei, s in enumerate(shape.shape_type):
            if s == 'line':
                line = shape.data[ei]
                break
       
        images = [i for i in selected if isinstance(i, Image)]
        print(images)  
        return line, images
    
@napari_hook_implementation
def napari_experimental_provide_dock_widget():
    return ProfileWidget 