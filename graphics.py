import cv2 as cv
from win32gui import GetWindowText, GetForegroundWindow
from geometry import *

class ImageHandler:
    def __init__(self, window_name : str = __name__) -> None:
        self.window_name = window_name
        self.original_image = None
        self.display_image = None
        self.mouse_position = Vector2(0, 0)
        self.tmp_rect = Rect()
        self.drawing = False
        self.markings: list[Rect] = []

    def update(self):
        cv.imshow(self.window_name, self.display_image)
        cv.waitKey(1 if self.drawing else 10)
        self.display_image = self.original_image.copy()

    def set_image(self, image : cv.Mat=None):
        self.original_image = image.copy()
        self.display_image = image.copy()

        cv.imshow(self.window_name, self.display_image)
        cv.setMouseCallback(self.window_name, self.mouse_callback)

    def mouse_callback(self, event, x, y, flags, params):
        self.mouse_position.update(x, y)

        if event == cv.EVENT_LBUTTONDOWN:
            self.tmp_rect.start = Vector2(self.mouse_position.x, self.mouse_position.y)
            self.drawing = True
        
        elif event == cv.EVENT_LBUTTONUP:
            self.tmp_rect.end = Vector2(self.mouse_position.x, self.mouse_position.y)
            self.drawing = False
            self.markings.append(Rect(self.tmp_rect.start, self.tmp_rect.end))

        elif event == cv.EVENT_RBUTTONDOWN:
            for i, rect in enumerate(self.markings):
                if rect.point_in_area(self.mouse_position):
                    removed_marking = self.markings.pop(i)

        if self.drawing:
            self.tmp_rect.end = Vector2(self.mouse_position.x, self.mouse_position.y)

    def draw_rect(self, rect : Rect, flush=False, color=[0, 255, 0]):
        cv.rectangle(self.display_image, rect.start.value, rect.end.value, color, thickness=2)