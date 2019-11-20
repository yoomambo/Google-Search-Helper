# Google API 사용
import os
import sys

dirPath = sys.argv[1]
if not os.path.isdir(dirPath):
    os.makedirs(os.path.join(dirPath))
