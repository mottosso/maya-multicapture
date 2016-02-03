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
        panel2 = QtGui.QLabel()
        panel3 = QtGui.QLabel()
        panel4 = QtGui.QLabel()

        layout = QtGui.QGridLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(5)
        layout.addWidget(panel1, 0, 0)
        layout.addWidget(panel2, 0, 1)
        layout.addWidget(panel3, 1, 0)
        layout.addWidget(panel4, 1, 1)

        # Public members
        self.is_running = False
        self.filename = filename
        self.tempdir = tempfile.mkdtemp()

        self.panel1 = panel1
        self.panel2 = panel2
        self.panel3 = panel3
        self.panel4 = panel4

        QtGui.QShortcut(QtGui.QKeySequence("Escape"), self, self.stop)

        self.update()

    def snap(self):
        """Write four viewports to disk

        Returns:
            (list) paths to resulting 4 files

        """

        images = list()

        for index in range(4):
            # Panels start at index 1
            index += 1

            cmds.setFocus("modelPanel%i" % index)

            # Force a refresh, otherwise the setting
            # of the focus might not have time to come
            # into effect, resulting in duplicate
            # captures from the below.
            cmds.refresh()

            view = apiUI.M3dView.active3dView()

            image = api.MImage()
            view.readColorBuffer(
                image,
                True  # BGRA -> RGBA
            )

        fname = os.path.join(self.tempdir, "temp_%i.jpg" % index)
        image.writeToFile(fname, "jpg")

        images.append(fname)

        return images

    def start(self):
        """Initiate capture"""
        self.is_running = True
        start_frame = int(cmds.playbackOptions(minTime=True, query=True))
        end_frame = int(cmds.playbackOptions(maxTime=True, query=True))
        for frame in range(start_frame, end_frame, 1):
            if not self.is_running:
                break

            cmds.currentTime(frame)
            self.update()
            self.save(frame)

        # Close once finished
        self.close()

    def stop(self):
        print("Stopping..")
        self.is_running = False

    def update(self):
        images = self.snap()
        for i, pane in enumerate([self.panel1,
                                  self.panel2,
                                  self.panel3,
                                  self.panel4]):
            pixmap = QtGui.QPixmap(images[i])
            pane.setPixmap(pixmap)

    def save(self, frame):
        """Save the current frame to disk

        Arguments:
            frame (int): Number of current frame

        """

        fname = self.filename % frame
        pixmap = QtGui.QPixmap.grabWidget(self)

        # Force a refresh of the file on disk.
        # Otherwise, it may pick up an older
        # version due to filesystem caching.
        try:
            os.remove(fname)
        except OSError:
            pass

        if pixmap.save(fname):
            print("Wrote %s" % fname)
        else:
            print("Could not write %s" % fname)
            self.is_running = False

    def closeEvent(self, event):
        try:
            shutil.rmtree(self.tempdir)
        except OSError:
            print("Had some problems cleaning up @ %s" % self.tempdir)
        super(Window, self).closeEvent(event)


@contextlib.contextmanager
def no_undo():
    undo_is_on = cmds.undoInfo(state=True, query=True)
    if undo_is_on:
        try:
            cmds.undoInfo(state=False)
            yield
        finally:
            cmds.undoInfo(state=True)
    else:
        yield


def capture():
    """Initiate capture"""

    try:
        parent = next(w for w in QtGui.qApp.topLevelWidgets()
                      if w.objectName() == "MayaWindow")
    except StopIteration:
        print("Main Maya window not found")
        parent = None

    scene = os.path.basename(
        cmds.file(sceneName=True, query=True) or "unsaved")

    name, _ = os.path.splitext(scene)
    workspace = cmds.workspace(fullName=True)
    fname = os.path.join(workspace, "images", name, "{}.%04d.jpg".format(name))

    if not os.path.exists(os.path.dirname(fname)):
        os.makedirs(os.path.dirname(fname))

    window = Window(fname, parent=parent)
    window.show()

    with no_undo():
        window.start()
