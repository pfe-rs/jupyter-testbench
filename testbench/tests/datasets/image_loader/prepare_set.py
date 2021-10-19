import torch
torch.__version__
import cv2
import numpy as np
from os import listdir

def prepare_set(path: str) -> torch.Tensor:
    image = (cv2.imread(path).astype("float32") / 255.0)[:, :, ::-1].copy()
    return torch.from_numpy(image.transpose(2, 0, 1))

print('test')

if __name__ == '__main__':
    print('test')
    for filename in listdir('input'):
        if not filename.endswith('.jpg'):
            continue
        name = filename.split()[0]
        path = f'input/{filename}'
        tensor = prepare_set(path)
        torch.save(tensor, f'output/{name}.pt')