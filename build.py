# coding=utf-8

import json
import codecs
import os, os.path


def printStanzaPair(block):

	number = block['number']
	original = u" \\\\\n".join(block['original'])
	translation = u" \\\\\n".join(block['translation'])
	comment = u"\n".join(block['comment']) if block['comment'] is not None else None

	return u"\\mystanzapair % Stanza " + unicode(number) + u"\n" + \
		(u"[" + comment + u"]\n" if comment is not None else u"") + \
		u"{" + unicode(number) + u"}" + \
		u"{\n" + original + u"}\n{\n" + translation + u"}"

def printText(block):
	return u"\n".join(block['text'])

handlers = {
	'stanza pair': printStanzaPair,
	'text': printText
}

filenames = os.listdir('chapters')

if not os.path.exists('build'):
	os.mkdir('build')
elif not os.path.isdir('build'):
	print "Build directory name is taken"
	exit(1)

for filename in filenames:
	name, ext = os.path.splitext(filename)
	if ext != '.json':
		continue

	blocks = json.load(codecs.open("chapters/" + filename, "r", "utf-8"))
	res = u"\n\n".join([handlers[block['type']](block) for block in blocks])

	f = codecs.open("build/" + name + ".tex", "w", "utf-8")
	f.write(res)
	f.close()

