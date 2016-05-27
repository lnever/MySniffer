# -*- coding: utf-8 -*-
from PyQt4.QtCore import *
from PyQt4.QtGui import *


class ChooseNetifaceDialog(QDialog):
    def __init__(self, options, parent=None):
        super(ChooseNetifaceDialog, self).__init__(parent)
        self.setWindowTitle("choose netiface")
        layout = QVBoxLayout(self)

        self.radios = []
        for option in options:
            self.radios.append(QRadioButton(option))
            layout.addWidget(self.radios[-1])

        # OK and Cancel buttons
        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
            Qt.Horizontal, self)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)


    @staticmethod
    def getCheckedOption(options, parent=None):
        dialog = ChooseNetifaceDialog(options, parent)
        result = dialog.exec_()
        checked = ''
        for radio in dialog.radios:
            if radio.isChecked():
                checked = radio.text()
        return checked, result == QDialog.Accepted
