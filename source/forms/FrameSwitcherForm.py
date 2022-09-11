import sys

from PySide2 import QtCore
from PySide2 import QtWidgets
from shiboken2 import wrapInstance

import maya.OpenMaya as om
import maya.OpenMayaUI as omui
import maya.cmds as cmds


def maya_main_window():
    """
    Return the Maya main window widget as a Python object
    """
    main_window_ptr = omui.MQtUtil.mainWindow()
    if sys.version_info.major >= 3:
        return wrapInstance(int(main_window_ptr), QtWidgets.QWidget)
    else:
        return wrapInstance(long(main_window_ptr), QtWidgets.QWidget)


class frameSwitcherForm(QtWidgets.QDialog):

    def __init__(self, parent=maya_main_window()):
        super(frameSwitcherForm, self).__init__(parent)

        self.setWindowTitle("Frames")
        self.setFixedWidth(110)
        self.setFixedHeight(178)
        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)

        self.create_widgets()
        self.create_layout()
        self.create_connections()

    def create_widgets(self):
        self.instructionsLabel = QtWidgets.QLabel()
        self.instructionsLabel.setText(u"Use cursors:")
        self.instructionsLabel.setAlignment(QtCore.Qt.AlignCenter)

        self.cursorLabel = QtWidgets.QLabel()
        self.cursorLabel.setText(u"<-  ->")
        self.cursorLabel.setAlignment(QtCore.Qt.AlignCenter)

        self.plusButton = QtWidgets.QPushButton()
        self.plusButton.setText('+')

        self.minusButton = QtWidgets.QPushButton()
        self.minusButton.setText('-')

        self.frameListWidget = QtWidgets.QListWidget()

    def create_layout(self):
        labelAndListLayout = QtWidgets.QVBoxLayout()
        labelAndListLayout.addWidget(self.instructionsLabel)
        labelAndListLayout.addWidget(self.cursorLabel)
        labelAndListLayout.addWidget(self.frameListWidget)
        labelAndListLayout.setSpacing(2)

        horizontalLayout = QtWidgets.QHBoxLayout()
        horizontalLayout.addWidget(self.plusButton)
        horizontalLayout.addWidget(self.minusButton)

        labelAndListLayout.addLayout(horizontalLayout)

        main_layout = QtWidgets.QHBoxLayout(self)
        main_layout.addStretch()
        main_layout.setContentsMargins(2,2,2,2)
        main_layout.addLayout(labelAndListLayout)

    def create_connections(self):
        self.plusButton.clicked.connect(self.addFrameToList)
        self.minusButton.clicked.connect(self.removeFrameFromList)

    def addFrameToList(self):
        items = []

        for index in range(self.frameListWidget.count()):
            items.append(int(float(self.frameListWidget.item(index).text())))

        currentFrame = cmds.currentTime( query=True )

        if currentFrame in items:
            return

        items.append(int(float(currentFrame)))
        items.sort(key = int)

        self.frameListWidget.clear()

        for item in items:
            self.frameListWidget.addItem(str(item))


    def removeFrameFromList(self):
        selectedRow = self.frameListWidget.currentRow()
        self.frameListWidget.takeItem(selectedRow)


if __name__ == "__main__":

    try:
        qtTemplateDialog.close() # pylint: disable=E0601
        qtTemplateDialog.deleteLater()
    except:
        pass

    qtTemplateDialog = frameSwitcherForm()
    qtTemplateDialog.show()