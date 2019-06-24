import os, sys
import zlib

def crc(fileName):
    fd = open(fileName,"rb")
    content = fd.readlines()
    fd.close()
    for eachLine in content:
        zlib.crc32(eachLine)
