# -*- coding: utf-8 -*-
from PyQt4.QtCore import *
from PyQt4.QtGui import *


class InputDialog(QDialog):
    def __init__(self, title, parent=None):
        super(InputDialog, self).__init__(parent)
        self.setWindowTitle( title )

        layout = QVBoxLayout(self)

        self.textArea = QLineEdit()
        self.textArea.setText( title )
        

        button = QDialogButtonBox(QDialogButtonBox.Ok )
        button.accepted.connect(self.accept)

        layout.addWidget( self.textArea )
        layout.addWidget( button )


    @staticmethod
    def getInputResult(title, parent=None):
        dialog = InputDialog(title, parent)
        result = dialog.exec_()
        return dialog.textArea.text()
