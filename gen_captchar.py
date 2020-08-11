import os
import random
from PIL import Image
from PIL import ImageFilter
from PIL.ImageDraw import Draw
from PIL.ImageFont import truetype
try:
    from cStringIO import StringIO as BytesIO
except ImportError:
    from io import BytesIO

# producted by Liu Jingkang of ICBC Compus
# forked from https://github.com/lepture/captcha then make some changes    

DEFAULT_FONTS = ['./ttf/arial.ttf']
    
    
class _Captcha(object):
    def generate(self, chars, format='png'):
        """Generate an Image Captcha of the given characters.

        :param chars: text to be generated.
        :param format: image file format
        """
        im = self.generate_image(chars)
        out = BytesIO()
        im.save(out, format=format)
        out.seek(0)
        return out

    def write(self, chars, output, format='png'):
        """Generate and write an image CAPTCHA data to the output.

        :param chars: text to be generated.
        :param output: output destination.
        :param format: image file format
        """
        im = self.generate_image(chars)
        return im.save(output, format=format)


table  =  []
for i in range(256):
    table.append(i * 1.97)



class ImageCaptcha(_Captcha):

    def __init__(self, width=200, height=70, fonts=None, font_sizes=None):
        self._width = width
        self._height = height
        self._fonts = fonts or DEFAULT_FONTS
        self._font_sizes = font_sizes or (62, 66, 68)
        self._truefonts = []
        
    @property
    def truefonts(self):
        if self._truefonts:
            return self._truefonts
        self._truefonts = tuple([
            truetype(n, s)
            for n in self._fonts
            for s in self._font_sizes
        ])
        return self._truefonts

#     @staticmethod
    def random_color(self, start, end, opacity=None, channels=3):
        red = random.randint(start, end)
        green = random.randint(start, end)
        blue = random.randint(start, end)
        color = [red, green, blue]
        if channels == 2:
            i = random.randint(0, 2)
            color[i] = random.randint(start, end-40)
        if opacity is None:
            return tuple(color)
        return tuple([*color, opacity])
    

    def create_image(self, bgcolor):
        image = Image.new(mode='RGB', size=(self._width, self._height), color=bgcolor)
        return image
    

#     def create_noise_curve(self, image, color):
#         w, h = image.size
#         x1 = random.randint(0, int(w / 5))
#         x2 = random.randint(w - int(w / 5), w)
#         y1 = random.randint(int(h / 5), h - int(h / 5))
#         y2 = random.randint(y1, h - int(h / 5))
#         points = [x1, y1, x2, y2]
#         end = random.randint(160, 200)
#         start = random.randint(0, 20)
#         Draw(image).arc(points, start, end, fill=color)
#         return image

    
    def create_noise_line(self, image, width=3, number=5):
        w, h = image.size
        line_nums = random.randint(2, number)
        for _ in range(line_nums):
            line_color = self.random_color(128, 233, random.randint(64, 188), channels=2)
            part_w = random.randint(2, 8)
            x1 = random.randint(0, int(w / part_w))
            x2 = random.randint(int(w / part_w), w)
            y1 = random.randint(0, h)
            y2 = random.randint(0, h)
            points = [x1, y1, x2, y2]
            Draw(image).line(points, fill=line_color, width=width)
        return image

    
    def create_noise_dots(self, image, width=3, number=18):
        w, h = image.size
        nums = random.randint(number-5, number+5)
        for _ in range(nums):
            dot_color = self.random_color(50, 220, random.randint(188, 233), channels=2)
            x = random.randint(1, w-1)
            y = random.randint(1, h-1)
            if width == 3:
                points = [(x, y), (x-1, y-1), (x-1, y), (x-1, y+1), (x, y-1), (x, y+1), (x+1, y-1), (x+1, y), (x+1, y+1)]
            else:
                points = [(x, y), (x, y+1), (x+1, y), (x+1, y+1)]
            Draw(image).point(points, fill=dot_color)
        return image

    
    def create_captcha_image(self, chars, image):
        
        def _draw_character(c, image):
            font = random.choice(self.truefonts)
            w, h = Draw(image).textsize(c, font=font)

            dx = random.randint(0, 2)
            dy = random.randint(0, 2)
            im = Image.new('RGBA', (w + dx, h + dy))
            font_color = self.random_color(50, 160, channels=2)
            Draw(im).text((dx, dy), c, font=font, fill=font_color, width=3)

            # rotate
            im = im.rotate(random.uniform(-40, 40), Image.BILINEAR, expand=1)
            return im

        images = []
        for c in chars:
            images.append(_draw_character(c, image))
            
        text_width = sum([im.size[0] for im in images])
        width = max(text_width, self._width)
        image = image.resize((width, self._height))

        average = int(text_width / len(chars))
        rand = int(0.25 * average)
        offset = int(average * 0.2)

        for im in images:
            w, h = im.size
            mask = im.convert('L').point(table)
            image.paste(im, (offset, -5), mask)
            offset = offset + w + random.randint(-rand, 0)
            
        if width > self._width:
            image = image.resize((self._width, self._height))
        return image

    
    def generate_image(self, chars):

        bgcolor = self.random_color(220, 255)
        im = self.create_image(bgcolor = bgcolor)
        im = self.create_captcha_image(chars, im)
        self.create_noise_dots(im, width=3, number=25)
        self.create_noise_line(im, width=3, number=5)
#         im = im.filter(ImageFilter.SMOOTH)
        im = im.filter(ImageFilter.Kernel((3, 3), kernel=[1, 1, 1, 1, 1, 1, 1, 1, 1]))
        im = im.resize((107, 35))
        return im
    
