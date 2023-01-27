import cv2 as cv
import os, json

class Config:
    def __init__(self, image_path : str, base_image : cv.Mat) -> None:
        self.image_path = image_path
        height, width, depth = base_image.shape
        self.config = {
            'annotation': {
                'folder': image_path.split(os.sep)[-2],
                'filename': image_path.split(os.sep)[-1],
                'path': image_path,
                'size': {
                    'width': width,
                    'height': height,
                    'depth': depth
                },
                'segmented': 0
            },
        }
        self.object_count = 0

    def add_boundbox(self, label : str, box : list[list[int, int], list[int, int]]):
        self.config[f'object_{self.object_count}'] = {
                'name': label,
                'bndbox': {
                    'xmin': box[0][0],
                    'ymin': box[0][1],
                    'xmax': box[1][0],
                    'ymax': box[1][1]
                }
            }
        self.object_count += 1

    def __str__(self) -> str:
        return json.dumps(self.config, indent=4)

    def walk(self, data : dict, depth=0):
        for k, v in data.items():
            if type(v) == dict:
                yield depth, k, None
                depth += 1
                yield from self.walk(v, depth=depth)
                depth -= 1
            else:
                yield depth, k, v

    def to_xml(self):
        output = ''
        last = [[], 0] # Previous parent keys, Depth

        for depth, k, v in self.walk(self.config):

            indent = '\t' * depth

            k = 'object' if 'object_' in k else k

            if depth < last[1]:
                output += f'{indent}</{last[0].pop()}>\n'

            if k and v == None:
                output += f'{indent}<{k}>\n'
                last[0].append(k)
            elif k and v != None:
                output += f'{indent}<{k}>{v}</{k}>\n'
            
            last[1] = depth

        output += f'</{last[0].pop()}>'

        return output