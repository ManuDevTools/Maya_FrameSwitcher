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


class FrameSwitcherForm(QtWidgets.QDialog):
    '''
    Class that defines the main form of the frame switch 
    '''

    def __init__(self, parent=maya_main_window()):
        super(FrameSwitcherForm, self).__init__(parent)

        self.setWindowTitle("Frames")
        self.setFixedWidth(110)
        self.setFixedHeight(178)
        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)

        self.create_widgets()
        self.create_layout()
        self.create_connections()

        self.main_window = maya_main_window()
        self.main_window.installEventFilter(self)

    def create_widgets(self):
        '''
        Definitions for the form widgets.
        '''

        self.instructions_label = QtWidgets.QLabel()
        self.instructions_label.setText("Use cursors:")
        self.instructions_label.setAlignment(QtCore.Qt.AlignCenter)

        self.cursor_label = QtWidgets.QLabel()
        self.cursor_label.setText("<-  ->")
        self.cursor_label.setAlignment(QtCore.Qt.AlignCenter)

        self.plus_button = QtWidgets.QPushButton()
        self.plus_button.setText('+')

        self.minus_button = QtWidgets.QPushButton()
        self.minus_button.setText('-')

        self.frame_list_widget = QtWidgets.QListWidget()

    def create_layout(self):
        '''
        Layout form definitions
        '''

        label_and_list_layout = QtWidgets.QVBoxLayout()
        label_and_list_layout.addWidget(self.instructions_label)
        label_and_list_layout.addWidget(self.cursor_label)
        label_and_list_layout.addWidget(self.frame_list_widget)
        label_and_list_layout.setSpacing(2)

        horizontal_layout = QtWidgets.QHBoxLayout()
        horizontal_layout.addWidget(self.plus_button)
        horizontal_layout.addWidget(self.minus_button)

        label_and_list_layout.addLayout(horizontal_layout)

        main_layout = QtWidgets.QHBoxLayout(self)
        main_layout.addStretch()
        main_layout.setContentsMargins(2,2,2,2)
        main_layout.addLayout(label_and_list_layout)

    def create_connections(self):
        '''
        QT connections definitions.
        '''
        self.plus_button.clicked.connect(self.add_frame_to_list)
        self.minus_button.clicked.connect(self.remove_frame_from_list)



    def add_frame_to_list(self):
        '''
        Function for adding an item to QtListWidget.
        It will retrieve the existing items, sort them by value, clear the list, and set them again.
        '''
        items = []

        for index in range(self.frame_list_widget.count()):
            items.append(int(float(self.frame_list_widget.item(index).text())))

        current_frame = cmds.currentTime( query=True )

        if current_frame in items:
            return

        items.append(int(float(current_frame)))
        items.sort(key = int)

        self.frame_list_widget.clear()

        for item in items:
            self.frame_list_widget.addItem(str(item))



    def remove_frame_from_list(self):
        '''
        Removes the selected item on the list.
        '''
        selected_row = self.frame_list_widget.currentRow()
        self.frame_list_widget.takeItem(selected_row)



    def eventFilter(self, obj, event):
        '''
        Qt even filter to catch if the left or right key is pressed.
        '''
        if obj == self.main_window:
            if not self.isVisible():
                return

            if event.type() == QtCore.QEvent.KeyPress and event.key() == QtCore.Qt.Key_Left:
                current_row = self.frame_list_widget.currentRow()

                try:
                    self.frame_list_widget.setCurrentRow(current_row - 1)
                    new_value = self.frame_list_widget.currentItem().text()
                    cmds.currentTime( int(new_value), edit=True )
                except Exception:
                    self.frame_list_widget.setCurrentRow(self.frame_list_widget.count()-1)
                    new_value = self.frame_list_widget.currentItem().text()
                    cmds.currentTime( int(new_value), edit=True )

                return True


            if event.type() == QtCore.QEvent.KeyPress and event.key() == QtCore.Qt.Key_Right:
                current_row = self.frame_list_widget.currentRow()

                try:
                    self.frame_list_widget.setCurrentRow(current_row + 1)
                    new_value = self.frame_list_widget.currentItem().text()
                    cmds.currentTime( int(new_value), edit=True )
                except Exception:
                    self.frame_list_widget.setCurrentRow(0)
                    new_value = self.frame_list_widget.currentItem().text()
                    cmds.currentTime( int(new_value), edit=True )

                return True
        return False


if __name__ == "__main__":

    try:
        qtTemplateDialog.close() # pylint: disable=E0601
        qtTemplateDialog.deleteLater()
    except Exception:
        pass

    qtTemplateDialog = FrameSwitcherForm()
    qtTemplateDialog.show()