import os
import sys
import shutil
import tempfile
import contextlib

from PySide import QtGui

from maya import (
  cmds,
  OpenMaya as api,
  OpenMayaUI as apiUI
)

class Window(QtGui.QDialog):
  def __init__(self, filename, parent=None):
    super(Window, self).__init__(parent)
    
    panel1 = QtGui.QLabel()
