# To decode, we simply reverse the change.
from PIL import Image
import pickle
import zlib

# Loading the encoded image this time
im = Image.open('encoded.png')
pix = im.load()
size = im.size

d = list(im.getdata())

array = bytearray()
key = b''  # This is where you would put the key printed from the encode file. Not elegant. 
indices = pickle.loads(zlib.decompress(key))

bytes_saved = 0
y = -1
for i in indices:
    x = i % size[0]
    y = i // size[0]

    color = list(pix[x, y])
    digit = ''

    o_p1, o_p2, o_p3 = [str(value)[-1] for value in color[:3]]
    digit += o_p1 + o_p2 + o_p3

    bytes_saved += 1
    array.append(int(digit))

print(array)
