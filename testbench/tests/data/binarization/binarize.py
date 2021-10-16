from cv2 import cvtColor, imread, imwrite, threshold, COLOR_RGB2GRAY, THRESH_BINARY
from os import listdir

if __name__ == '__main__':
    for filename in listdir('input'):
        if not filename.endswith('.png'):
            continue
        image_in = imread(f'input/{filename}')
        image_in = cvtColor(image_in, COLOR_RGB2GRAY)
        _, image_out = threshold(image_in, 128, 255, THRESH_BINARY)
        imwrite(f'output/{filename}', image_out)
