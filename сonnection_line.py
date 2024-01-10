from PyQt6.QtGui import QPen, QColor
from PyQt6.QtWidgets import QGraphicsLineItem
from PyQt6.QtCore import QLineF

class ConnectionLine(QGraphicsLineItem):
    def __init__(self, startItem, endItem):
        super().__init__()
        self.startItem = startItem
        self.endItem = endItem

        # Установка пера для линии
        pen = QPen(QColor(0, 0, 0))  # Черный цвет для линии
        pen.setWidth(2)  # Установка толщины линии
        self.setPen(pen)

        self.updatePosition()

    def updatePosition(self):
        line = QLineF(self.startItem.sceneBoundingRect().center(),
                      self.endItem.sceneBoundingRect().center())
        self.setLine(line)