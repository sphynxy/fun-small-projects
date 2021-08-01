# Little steganography doodle
# This changes the least significant digit for each RGB channel value to the bit to encode.
# For example, a byte can be 182 which can be broken down to 1, 8, and 2. We take these numbers and change
# the color [92, 146, 68] to [91, 148, 62]. We don't change the alpha channel because that could possibly
# be spotted.

from PIL import Image
import random
import zlib
import pickle

# Loading the message (in this case, this file) as a bytearray.
with open('encode_test.py', 'rb') as f:
    message = bytearray(f.read())

im = Image.open('TheMoon!.png')  # My choice of encoding image.
pix = im.load()

size = im.size

# Getting a random selection of point indices in the image in which we will store the message.
d = list(im.getdata())
indices = random.sample(list(range(len(d))), len(message))

# Saving the random points as a pickled string. Not very secure, but storing it this way makes the resulting
# encrypted image look identical to the original to a human.
lock = pickle.dumps(indices)

print(size)
print('key:', zlib.compress(lock, 4))

bytes_saved = 0
y = -1

for i in indices:
    x = i % size[0]
    y = i // size[0]

    if bytes_saved < len(message):
        if i in indices:
            
            color = list(pix[x, y])
            digit = str(message[bytes_saved])
            
            # Make sure digit to be encoded is normalized to be 3 in length.
            digit = digit.rjust(3, '0')

            p1, p2, p3 = digit
            o_p1, o_p2, o_p3 = [list(str(value)) for value in color[:3]]

            o_p1[-1], o_p2[-1], o_p3[-1] = p1, p2, p3

            color[0], color[1], color[2] = int(''.join(o_p1)), int(''.join(o_p2)), int(''.join(o_p3))

            pix[x, y] = tuple(color)
            bytes_saved += 1

print(len(message), bytes_saved)
im.save('t2.png')
