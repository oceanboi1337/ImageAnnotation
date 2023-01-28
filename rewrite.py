import argparse, pathlib, os, time, keyboard
import cv2 as cv
import pascal_voc, gui, helpers, graphics, input_handler

def process_image(path):
    image = cv.imread(path, cv.IMREAD_UNCHANGED)

    window = graphics.ImageHandler('Image Display')
    window.set_image(image)
    
    keyboard = input_handler.Keyboard(window_name='Image Display')

    while 1:
        for rect in window.markings:
            window.draw_rect(rect)

        if window.drawing:
            window.draw_rect(window.tmp_rect)

        if keyboard.keydown('s'):
            break

        window.update()

def main(args : argparse.Namespace):
    if pathlib.Path.exists(args.images):
        for root, dirs, files in os.walk(args.images):
            for file in [file for file in files if helpers.is_image(file)]:

                path = os.path.abspath(os.path.join(root, file))

                config = process_image(path)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--images', type=pathlib.Path, required=True)
    main(parser.parse_args())