from PyQt5.QtWidgets import QApplication

from models import Camera
from view import StartWindow

if __name__ == "__main__":
    camera = Camera(1)
    camera.initialize()
    app = QApplication([])
    start_window = StartWindow(camera)
    start_window.show()
    app.exit(app.exec_())
