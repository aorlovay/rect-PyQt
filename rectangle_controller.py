import random
from PyQt6.QtCore import QRectF
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import QGraphicsRectItem
from rectangle_Item import RectangleItem

class RectangleController:
    DEFAULT_WIDTH = 100
    DEFAULT_HEIGHT = DEFAULT_WIDTH // 2

    def __init__(self, view):
        self.view = view

    def on_double_click(self, x, y):
        """Добавляет новый прямоугольник при двойном клике."""
        color = QColor(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
         # Проверяем достаточно ли места для создания прямогольника
        if x + self.DEFAULT_WIDTH > self.view.width() or y + self.DEFAULT_HEIGHT > self.view.height():
            print("Недостаточно места на сцене для создания прямоугольника.")
            return False  # Нет места
        if self.is_space_available(x, y, self.DEFAULT_WIDTH, self.DEFAULT_HEIGHT):
            rect_item = RectangleItem(x, y, self.DEFAULT_WIDTH, self.DEFAULT_HEIGHT, color)
            self.view.addItem(rect_item)
        else:
            print("Недостаточно места для создания прямоугольника.")

    def is_space_available(self, x, y, width, height):
        """Проверяет, доступно ли место для создания прямоугольника."""
        temp_rect = QRectF(x, y, width, height)

        for item in self.view.items():
            if isinstance(item, QGraphicsRectItem):
                # Получаем текущую геометрию элемента с учетом его положения на сцене
                item_rect = item.rect().translated(item.pos())
                if temp_rect.intersects(item_rect):
                    return False  # Область занята

        return True  # Область свободна

    def createConnection(self):
        """Создает связь между двумя выбранными прямоугольниками."""
        selected_items = self._getSelectedItems()
        if len(selected_items) == 2:
            selected_items[0].addConnection(selected_items[1])

    def removeConnection(self):
        """Удаляет связь между двумя выбранными прямоугольниками."""
        selected_items = self._getSelectedItems()
        if len(selected_items) == 2:
            self._removeConnectionBetweenItems(selected_items[0], selected_items[1])

    def _removeConnectionBetweenItems(self, item1, item2):
        """Удаляет связь между двумя выбранными прямоугольниками."""
        if hasattr(item1, 'connections') and hasattr(item2, 'connections'):
            # Ищем общие связи между двумя элементами
            common_connections = set(item1.connections) & set(item2.connections)
            for connection in common_connections:
                # Удаляем связь с сцены
                self.view.removeItem(connection)
                # Удаляем связь из списков связей прямоугольников
                item1.connections.remove(connection)
                item2.connections.remove(connection)

    def _getSelectedItems(self):
        """Возвращает список выбранных прямоугольников."""
        return [item for item in self.view.items() if isinstance(item, RectangleItem) and item.isSelected()]