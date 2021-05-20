import sys

from pyqtgraph.Qt import QtGui, QtCore
import numpy as np
import pyqtgraph as pg
import napari
from skimage.measure import profile_line

'''
do this with 
v.window.add_dock_widget
'''
def pw():
    w = pg.PlotWidget(name="MyPlot")
    p1 = w.plot()
    p1.setPen((200,200,50))
    x = np.linspace(0, 10, 50)
    y = np.random.randn(50)
    p1.setData(x=x, y=y)
    return w, p1

def update_plot(p):
    x = np.linspace(0, 10, 100)
    y = np.random.randn(100)
    p.setData(x=x, y=y)

def profile(image_layer, line_layer):
    line = line_layer.data[0]
    src = line[0][-2:]
    dst = line[1][-2:]
    profile = profile_line(image_layer.data, src, dst)
    profile_widget = pg.PlotWidget(name="Line Profile")
    p = profile_widget.plot()
    color = color_triplet(image_layer.colormap.name)
    p.setPen(color)
    x = np.arange(0, len(profile))
    p.setData(x=x, y=profile)
    return profile_widget, p
    
def get_displayed_slice(image_layer):

    data = image_layer.data

    if image_layer.ndim < 3:
        return data

    c = image_layer.coordinates

    nd = list(reversed(image_layer.dims.not_displayed))
    ns = [c[b] for b in nd]

    image = None
    for i, s in enumerate(nd):
        if image is None:
            image = np.take(data, ns[i], axis=s)
        else:
            image = np.take(image, ns[i], axis=s)
    return image


def histogram(image_layer, only_displayed=True):
    image = get_displayed_slice(image_layer)
    print(image.shape)
    h,  hx = np.histogram(image.reshape(-1), bins=255)
    return h, hx

def plot_histogram(image_layer):
    color = color_triplet(image_layer.colormap.name)
    h, hx = histogram(image_layer)
    hist_w = pg.PlotWidget(name="Histogram")
    p1 = hist_w.plot()
    p1.setPen(color)
    p1.setData(x=hx[:-1], y=h)
    return hist_w, p1

def color_triplet(color):
    trips = {
        'red': (255, 0, 0),
        'green': (0, 255, 0),
        'blue': (0, 0, 255),
        'magenta': (255, 0, 255),
        'gray': (128, 128, 128),
        'yellow': (255, 255, 0),
        'cyan': (0, 255, 255),
    }

    return trips[color]