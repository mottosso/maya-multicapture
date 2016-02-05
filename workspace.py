import os
import sys
import shutil
import tempfile
import contextlib

from PySide import QtGui, QtCore

from maya import (
    cmds,
    OpenMaya as api,
    OpenMayaUI as apiUI
)

class Editor(QtGui.QDialog):
    def __init__(self, parent=None):
        super(Editor, self).__init__(parent)
        self.setWindowTitle("multicapture")
        self.setAcceptDrops(True)
        self.resize(500, 400)
    
        # Setup default dropzones
        self.setup_dropzones(self)

        self.show_dropzones = False

    def setup_dropzones(self, widget):
        left = QtGui.QWidget()
        top = QtGui.QWidget()
        right = QtGui.QWidget()
        bottom = QtGui.QWidget()
        center = QtGui.QWidget()
    
        widget.dropzones = list()
        for w in (left, top, right, bottom, center):
            w.setAttribute(QtCore.Qt.WA_StyledBackground)
            w.setMinimumSize(50, 50)
            widget.dropzones.append(w)

        layout = QtGui.QGridLayout(widget)
        layout.addWidget(left, 0, 1)
        layout.addWidget(top, 1, 0)
        layout.addWidget(right, 2, 1)
        layout.addWidget(bottom, 1, 2)
        layout.addWidget(center, 1, 1)

    def teardown_dropzones(self, widget):
        pass

    def dragEnterEvent(self, event):
        self.show_dropzones = False
        if event.mimeData().hasFormat("application/x-maya-data"):
            event.acceptProposedAction()
            self.show_dropzones = True
    
    def dragLeaveEvent(self, event):
        for zone in self.dropzones:
            zone.setStyleSheet("""
                QWidget {
                    border: none;
                    background: transparent;
                }
            """)

    def dragMoveEvent(self, event):
        self.clear_dropzones()

        if self.show_dropzones:
            self.update_dropzones()
    
    def update_dropzones(self):
        global_pos = QtGui.QCursor.pos()
        local_pos = self.mapFromGlobal(global_pos)

        widget = self.childAt(local_pos)
        if not widget:
            return

        widget.setStyleSheet("""
            QWidget {
                border: 2px dashed gray;
                border-radius: 5px;
                background: steelblue;
            }
            """)

    def clear_dropzones(self):
        for zone in self.dropzones:
            zone.setStyleSheet("""
                QWidget {
                    border: 2px dashed gray;
                    border-radius: 5px;
                    background: transparent;
                }
            """)

    def dropEvent(self, event):
        selection = cmds.ls(selection=True)

        if not selection:
            return

        selection += cmds.listRelatives(selection, shapes=True)
        cameras = cmds.ls(selection, cameras=True)
        print("Adding %s" % cameras)


window = Editor()
window.show()
