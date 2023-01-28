class Vector2:
    def __init__(self, x : int | float, y : int | float) -> None:
        self.x = x
        self.y = y

    def update(self, x, y):
        self.x = x
        self.y = y

    @property
    def value(self):
        return [self.x, self.y]

class Rect:
    def __init__(self, start : Vector2=None, end : Vector2=None) -> None:
        self.start = start
        self.end = end
        
        if start != None and end != None:
            self.order()

    def order(self):
        ax = min(self.start.x, self.end.x)
        ay = min(self.start.y, self.end.y)
        bx = max(self.start.x, self.end.x)
        by = max(self.start.y, self.end.y)
        self.start.x = ax
        self.start.y = ay
        self.end.x = bx
        self.end.y = by

    def update(self, start : Vector2, end : Vector2):
        self.start = start
        self.end = end

    def point_in_area(self, point : Vector2) -> bool:
        return self.start.x < point.x < self.end.x and self.start.y < point.y < self.end.y

    def __str__(self) -> str:
        return f'{self.start.x} {self.start.y} {self.end.x} {self.end.y}'