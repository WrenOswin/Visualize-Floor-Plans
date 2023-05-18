import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QFileDialog
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
import subprocess
import os

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Floor Plans to VR Converter")
        self.setGeometry(100, 100, 600, 600)

        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setGeometry(50, 50, 200, 200)

        self.directory_label = QLabel(self)
        self.directory_label.setGeometry(350, 50, 580, 100)

        self.select_button = QPushButton("Select Floor Plan Image", self)
        self.select_button.setGeometry(50, 10, 200, 30)
        self.select_button.clicked.connect(self.select_image)

        self.message_label = QLabel(self)
        self.message_label.setGeometry(10, 300, 580, 30)
        self.message_label.setAlignment(Qt.AlignCenter)

        self.file_list_widget = QPushButton("Refresh Models", self)
        self.file_list_widget.setGeometry(350, 10, 200, 30)
        self.file_list_widget.clicked.connect(self.list_files)

    def select_image(self):
        file_dialog = QFileDialog(self)
        file_dialog.setNameFilter("Images (*.png *.xpm *.jpg *.bmp)")
        if file_dialog.exec_():
            file_path = file_dialog.selectedFiles()[0]
            self.display_image(file_path)
            self.execute_script(file_path)

    def display_image(self, file_path):
        pixmap = QPixmap(file_path)
        pixmap = pixmap.scaled(300, 200, Qt.KeepAspectRatio)
        self.image_label.setPixmap(pixmap)

    def execute_script(self, file_path):
        self.message_label.setText("Executing script... will launch blender model soon")
        script_path = "main.py"
        subprocess.Popen(["python", script_path, file_path])  # Change "python" to your Python interpreter if needed

    def list_files(self):
        current_dir = os.getcwd()
        directory_path = os.path.join(current_dir, "Target")
        file_list = os.listdir(directory_path)
        filestring = ""
        for filename in file_list:
            filestring += "   "
            filestring += filename
            filestring += "\n"
        if(filestring == ""):
            filestring = "   No models available!"
        self.directory_label.setText(f"    Files listed from: {directory_path}: \n\n {filestring}")


        #open directory
        #show all files there

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
