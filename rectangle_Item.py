from PyQt6.QtCore import QPointF, Qt
from PyQt6.QtGui import QBrush, QPen, QColor
from PyQt6.QtWidgets import QGraphicsRectItem, QGraphicsItem
from сonnection_line import ConnectionLine


class RectangleItem(QGraphicsRectItem):
    def __init__(self, x, y, width, height, color):
        super().__init__(x, y, width, height)
        self.initVisuals(color)
        self.initFlags()
        self.connections = []

    def initVisuals(self, color):
        """Инициализирует визуальные настройки прямоугольника."""
        self.setBrush(QBrush(color))
        pen = QPen(QColor(0, 0, 0))
        pen.setWidth(2)
        self.setPen(pen)

    def initFlags(self):
        """Инициализирует флаги для прямоугольника."""
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable)
        self.setFlag(self.GraphicsItemFlag.ItemSendsGeometryChanges)
        self.setFlag(self.GraphicsItemFlag.ItemIsSelectable)

    def itemChange(self, change, value):
        if change == QGraphicsItem.GraphicsItemChange.ItemPositionChange:
            # Проверяем, не пересекается ли прямоугольник с другими элементами
            collision_detected = any(
                item != self and isinstance(item, QGraphicsRectItem) and self.collidesWithItem(item)
                for item in self.scene().items()
            )

            if collision_detected:
                # Обработка столкновения и корректировка положения и обновление связи
                new_x, new_y = self.adjustPosition(value)
                self.updateConnections()
                return QPointF(new_x, new_y)

            self.updateConnections()  # Обновляем связи, если нет столкновений

        return super().itemChange(change, value)

    def updateConnections(self):
        """Обновляет позиции всех связей."""
        for line in self.connections:
            line.updatePosition()

    def adjustPosition(self, newPos):
        """"Обработка столкновений"""
        newPosX, newPosY = newPos.x(), newPos.y()

        for item in self.scene().items():
            if item == self or not isinstance(item, QGraphicsRectItem):
                continue

            collide_rect = item.rect().translated(item.pos())
            self_rect = self.rect().translated(newPos)

            if self_rect.intersects(collide_rect):
                # Вычисляем перекрытие и корректируем позицию
                newPosX, newPosY = self.calculateNewPosition(newPosX, newPosY, self_rect, collide_rect)

        return newPosX, newPosY

    def calculateNewPosition(self, newPosX, newPosY, self_rect, collide_rect):
        overlap_top = abs(self_rect.bottom() - collide_rect.top())
        overlap_bottom = abs(self_rect.top() - collide_rect.bottom())
        overlap_left = abs(self_rect.right() - collide_rect.left())
        overlap_right = abs(self_rect.left() - collide_rect.right())

        min_overlap = min(overlap_top, overlap_bottom, overlap_left, overlap_right)
        if min_overlap == overlap_top:
            newPosY = collide_rect.top() - self.rect().height() - self.rect().top()
        elif min_overlap == overlap_bottom:
            newPosY = collide_rect.bottom() - self.rect().top()
        elif min_overlap == overlap_left:
            newPosX = collide_rect.left() - self.rect().width() - self.rect().left()
        elif min_overlap == overlap_right:
            newPosX = collide_rect.right() - self.rect().left()

        return newPosX, newPosY

    def mousePressEvent(self, event):
        """Выбор прямоугольников правой кнопкой мыши"""
        if event.button() == Qt.MouseButton.RightButton:
            self.setSelected(not self.isSelected())
            event.accept()
        else:
            super().mousePressEvent(event)

    def addConnection(self, otherItem):
        # Создаем объект связи между текущим и другим прямоугольником
        connection = ConnectionLine(self, otherItem)
        # Добавляем линию связи на сцену
        self.scene().addItem(connection)
        # сохраняем связи
        self.connections.append(connection)
        otherItem.connections.append(connection)

