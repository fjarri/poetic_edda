import re, codecs
import sys
from xml.etree.ElementTree import Element, ElementTree
from detexify_json import makePretty

f = codecs.open(sys.argv[1], 'r', 'utf-8')
intro = f.read()
f.close()

root = Element('chapter', icelandic_name="", english_name="", translation="")

for block in intro.split(u'\n\n'):
	e = Element('block', attrib={'class': 'text'})
	e.text = block
	root.append(e)

tree = ElementTree(element=root)
makePretty(tree.getroot())
tree.write(open(sys.argv[2], mode='wb'), encoding='utf-8')
