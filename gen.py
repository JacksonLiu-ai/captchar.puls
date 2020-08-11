import os
import random
import pandas as pd
from tqdm import tqdm

from gen_captchar import ImageCaptcha

file = 'train_data'
nums = 200000

if not os.path.exists(file):
    os.mkdir(file)
capitals = []
pos = list(range(48, 58)) + list(range(65, 91)) + list(range(97, 123))
capitals = [chr(i) for i in pos]

images = []
labels = []
chosen_ttfs = ['./ttf/simhei.ttf']
height = 70
img = ImageCaptcha(width=107*2, height=height, fonts = chosen_ttfs, font_sizes=[height-6, height-4, height-2])
for num in tqdm(range(nums)):
    value = ''.join(c for c in random.choices(capitals, k=4))
    img.write(value, os.path.join(file, str(num)+'.jpg'))
    images.append(str(num)+'.jpg')
    labels.append(value)

df = pd.DataFrame()
df['image'] = images
df['value'] = labels
df.to_csv('train.csv', index=False)