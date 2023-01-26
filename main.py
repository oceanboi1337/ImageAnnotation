import argparse, pathlib, os, time, keyboard
import cv2 as cv

parser = argparse.ArgumentParser()

def resize_image(image : cv.Mat, width=None, height=None, interpolation=cv.INTER_AREA):
    dim = None
    image_height, image_width = image.shape[:2]
    
    if width == None and height == None:
        return image

    if width == None:
        ratio = height / float(image_height)
        dim = (int(image_width * ratio), height)
    else:
        ratio = width / float(image_width)
        dim = (width, int(image_height * ratio))

    return cv.resize(image, dim, interpolation=interpolation)

def order_rect(start, end):
    start_x = min(start[0], end[0])
    start_y = min(start[1], end[1])
    end_x = max(start[0], end[0])
    end_y = max(start[1], end[1])

    return [[start_x, start_y], [end_x, end_y]]

def is_image(file_name : str) -> bool:
    return file_name.split('.')[-1] in ['png', 'jpg', 'jpeg', 'bmp']

def is_within(start, end, point):
    return start[0] < point[0] < end[0] and start[1] < point[1] < end[1]

def process_image(image : str):
    mouse_points = {'down': None, 'up': None}
    current_point = [None, None]
    markers = []
    drawing = True

    def mouse_callback(event, x, y, flags, params):
        nonlocal current_point, markers
        current_point = [x, y]

        if event == cv.EVENT_LBUTTONDOWN:
            mouse_points['down'] = [x, y]

        elif event == cv.EVENT_LBUTTONUP:
            mouse_points['up'] = [x, y]

        elif event == cv.EVENT_RBUTTONDOWN:
            for i, (start, end) in enumerate(markers):
                if is_within(start, end, current_point):
                    del markers[i]

    def next_image():
        nonlocal drawing
        drawing = False

    cv_image = cv.imread(image, cv.IMREAD_UNCHANGED)
    cv_image = resize_image(cv_image, width=1920)
    cv.imshow('Image Display', cv_image)
    cv.setMouseCallback('Image Display', mouse_callback)

    while drawing:
        cv_draw_image = cv_image.copy()

        for start, end in markers:
            cv.rectangle(cv_draw_image, start, end, [0, 255, 0], thickness=2)

        #print(mouse_points, current_point, markers)

        if (mouse_points['down'] and not mouse_points['up']) and (current_point[0] != None and current_point[1] != None):
            cv.rectangle(cv_draw_image, mouse_points['down'], current_point, [0, 0, 255], thickness=2)
            cv.imshow('Image Display', cv_draw_image)
        elif mouse_points['up'] != None:
            start, end = order_rect(mouse_points['down'], mouse_points['up'])
            markers.append([start, end])
            mouse_points['down'] = None
            mouse_points['up'] = None
        else:
            cv.imshow('Image Display', cv_draw_image)

        keyboard.add_hotkey('space', timeout=1, callback=next_image)
            
        cv.waitKey(1)

    return markers

def main():
    args = parser.parse_args()

    if pathlib.Path.exists(args.images):
        for root, dirs, files in os.walk(args.images):
            for file in files:
                path = os.path.join(root, file)
                print(path)
                if is_image(path):
                    process_image(path)

if __name__ == '__main__':
    parser.add_argument('--images', type=pathlib.Path, required=True)
    main()