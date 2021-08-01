from PIL import Image
import random
import zlib
import pickle

# Loading the message (in this case, this file) as a bytearray.
with open('encode_test.py', 'rb') as f:
    message = bytearray(f.read())

im = Image.open('TheMoon!.png')
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

            if 10 <= message[bytes_saved] < 100:
                digit = '0' + digit

            if message[bytes_saved] < 10:
                digit = '00' + digit

            p1, p2, p3 = digit
            o_p1, o_p2, o_p3 = [list(str(value)) for value in color[:3]]

            o_p1[-1], o_p2[-1], o_p3[-1] = p1, p2, p3

            color[0], color[1], color[2] = int(''.join(o_p1)), int(''.join(o_p2)), int(''.join(o_p3))

            pix[x, y] = tuple(color)
            bytes_saved += 1

print(len(message), bytes_saved)
im.save('t2.png')
