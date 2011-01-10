import json, codecs
import re
import sys

f = codecs.open(sys.argv[1], 'r', 'utf-8')
lines = f.read().split("\n")
f.close()

c = [{"type": "text", "text": lines}]

json.dump(c, codecs.open(sys.argv[2], 'w', 'utf-8'), ensure_ascii=False, indent=4)

