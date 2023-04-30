import os.path
import sys
from PySide6 import QtCore, QtWidgets


class ListView(QtWidgets.QListWidget):
    # Todo: change item order using drag and drop
    def __init__(self, parent=None):
        super().__init__(parent)
        self.paths = []
        self.setStyleSheet("""
        QListWidget {
        color: rgb(0,0,0);
        background-color: rgb(200, 200, 200);
        border: 2px solid black;
        alternate-background-color: rgb(190, 190, 210);
        }
        QScrollBar:vertical {              
            border: 1px solid black;
            background:rgb(200,200,200);
            width:15px;
            margin: 0px 0px 0px 0px;
        }
        QScrollBar::handle:vertical {
            background: #242d3d;
            min-height: 0px;
            width:5px;
        }
        QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {
            background: #242d3d;
            border: 1px solid black;
        }    
        """)

        self.setDragDropMode(QtWidgets.QAbstractItemView.InternalMove)
        self.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.setSelectionRectVisible(True)
        self.setDragDropOverwriteMode(False)
        self.setAlternatingRowColors(True)
        self.setWordWrap(True)

    # Events

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls:
            event.accept()
        else:
            event.ignore()

    def dragLeaveEvent(self, event):
        event.accept()
        self.removeSelected()

    # def dragMoveEvent(self, event):
    #     if event.mimeData().hasUrls:
    #         event.setDropAction(QtCore.Qt.CopyAction)
    #         event.accept()
    #     else:
    #         event.setDropAction(QtCore.Qt.MoveAction)
    #         event.accept()

    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            event.setDropAction(QtCore.Qt.CopyAction)
            event.accept()
            valid_urls = [str(url.toLocalFile()) for url in event.mimeData().urls() if
                          url.isLocalFile() and url.url()[-4:] == '.pdf']
            self.addItems(valid_urls)
        else:
            super().dropEvent(event)

    # Other methods

    def removeSelected(self):
        list_items = self.selectedItems()
        if list_items:
            for item in list_items:
                self.takeItem(self.row(item))
        self.selectionModel().clear()

    def getItemsText(self):
        items = []

        for i in range(self.count()):
            items.append(self.item(i).text())

        print("Teste: ")
        for item in items:
            print(f"Item {item}")
        return items


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.setWindowTitle("Simple PDF")

        self.central_widget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.vbox_ext = QtWidgets.QVBoxLayout(self.central_widget)
        self.list_view = ListView(self.central_widget)
        self.vbox_ext.addWidget(self.list_view)

        self.vspacer_1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.vbox_ext.addItem(self.vspacer_1)

        self.output_path = QtWidgets.QLineEdit(self.central_widget)
        self.output_path.setPlaceholderText(u"Output Path: folder/filename.pdf")
        self.output_path.setStyleSheet("color: rgb(255, 255, 255)")
        self.output_path.setMinimumSize(500, 0)

        self.vbox_ext.addWidget(self.output_path, 0, QtCore.Qt.AlignHCenter)

        self.push_button = QtWidgets.QPushButton("Merge PDFs", self.central_widget, clicked=lambda: self.mergePdfs())
        self.vbox_ext.addWidget(self.push_button, 0, QtCore.Qt.AlignHCenter)

        self.vspacer_2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.vbox_ext.addItem(self.vspacer_2)

        self.status_bar = QtWidgets.QStatusBar(self)
        self.setStatusBar(self.status_bar)

    def mergePdfs(self):
        items = self.list_view.getItemsText()
        input_string = ""
        for item in items:
            input_string += f" \"{item}\""
        print(input_string)

        self.statusBar().showMessage(f"{self.output_path.text()}")


if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    demo = MainWindow(app)
    demo.resize(800, 600)
    demo.show()

    sys.exit(app.exec())
