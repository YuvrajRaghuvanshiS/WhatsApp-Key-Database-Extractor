import tarfile
import zlib
import io

with open('D:\\Yuvraj\\Work\\GitHub\\WA-KDBE\\extracted\\crashed\\whatsapp.ab', 'rb') as f:
    f.seek(24)  # skip 24 bytes
    data = f.read()  # read the rest

tarstream = zlib.decompress(data)
with open('D:\\Yuvraj\\Work\\GitHub\\WA-KDBE\\extracted\\crashed\\whatsapp.tar', 'wb') as f:
    f.write(tarstream)
