from PyQt6.QtWidgets import QApplication, QMainWindow, QGraphicsScene, QGraphicsView
from PyQt6.QtCore import QRectF, Qt
from rectangle_controller import RectangleController


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Настройка окна
        self.setWindowTitle("Rectangles")
        self.setGeometry(100, 100, 800, 600)

        # Создание и настройка сцены
        self.scene = QGraphicsScene()
        self.scene.setSceneRect(QRectF(0, 0, 800, 600))

        # Создание и настройка виджета просмотра
        self.view = QGraphicsView(self.scene, self)
        self.view.setGeometry(0, 0, 800, 600)

        # Инициализация контроллера с созданной сценой
        self.controller = RectangleController(self.scene)

    def mouseDoubleClickEvent(self, event):
        """ Обработка двойного клика мыши для добавления прямоугольника """
        scenePos = self.view.mapToScene(event.pos())
        self.controller.on_double_click(scenePos.x(), scenePos.y())

    def keyPressEvent(self, event):
        # Обработка нажатий клавиш для управления связями
        if event.key() == Qt.Key.Key_Enter or event.key() == Qt.Key.Key_Return:
            self.controller.createConnection()
        elif event.key() == Qt.Key.Key_Delete:
            self.controller.removeConnection()
        else:
            super().keyPressEvent(event)


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec())
