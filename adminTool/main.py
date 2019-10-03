import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QFormLayout, QDialogButtonBox
from PyQt5.QtGui import QIcon
from PyQt5.uic import loadUi


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self._ui = None

        self._init_ui()
        self._init_connections()

    def _init_ui(self):
        self._ui = loadUi('ui/main.ui', self)  # Hier Pfad zu Qt Designer *.ui-file angeben
        self.setWindowTitle('PyoT Orchestra Administration Tool')
        self.setWindowIcon(QIcon("ui/music.ico"))
        self.show()

        self.client_list.insertItem(1,"1.1.1.255\tmusician")

        self.gridLayout.setContentsMargins(9, 9, 9, 9)

    def _init_connections(self):
        self.actionSettings.triggered.connect(self._show_dialog_settings)
        self.actionExit.triggered.connect(self._exit_app)
        self.client_list.clicked.connect(self.get_details)

    def get_details(self):
        print("get details")

    def _show_dialog_settings(self):
        d = DialogSettings(self)

        if d.exec_() == QDialog.Accepted:
            values = d.get_values()

    def _exit_app(self):
        self.close()


class DialogSettings(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self._init_ui()
        self._init_connections()

    def _init_ui(self):
        self.setWindowTitle("Settings")
        layout = QFormLayout()
        self.setLayout(layout)

        self.buttonbox = QDialogButtonBox()
        self.buttonbox.addButton("Cancel", QDialogButtonBox.RejectRole)
        self.buttonbox.addButton("Accept", QDialogButtonBox.AcceptRole)
        layout.addWidget(self.buttonbox)

    def _init_connections(self):
        self.buttonbox.accepted.connect(self.accept)
        self.buttonbox.rejected.connect(self.reject)

    def get_values(self):
        pass


def main():
    """
    Execute main program.

    :return: No return value
    """
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
