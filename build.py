# coding=utf-8

import json
import codecs
import os, os.path


def printStanzaPair(block):

	number = block['number']
	original = u" \\\\\n".join(block['original'])
	translation = u" \\\\\n".join(block['translation'])
	comment = u"\n".join(block['comment']) if block['comment'] is not None else None

	assert not (('original_prelude' in block) ^ ('translation_prelude' in block))

	if 'original_prelude' in block:
		original_p = u"\n".join(block['original_prelude'])
		translation_p = u"\n".join(block['translation_prelude'])
		postfix = u"{" + original_p + u"}{" + translation_p + u"}"
		command = u"\\eddastanzaprelude"
	else:
		postfix = u""
		command = u"\\eddastanzasimple"

	return command + u" % Stanza " + unicode(number) + u"\n" + \
		(u"[" + comment + u"]\n" if comment is not None else u"") + \
		u"{" + unicode(number) + u"}" + \
		u"{\n" + original + u"}\n{\n" + translation + u"}\n" + postfix + u"\n"

def printStanzaTable(block):

	leftField = lambda x: u"\\eddaleftfield{" + x + u"}"
	rightField = lambda x: u"\\eddarightfield{" + x + u"}"
	textit = lambda x: u"\\textit{" + x + u"}"

	number = block['number']
	original = block['original']
	translation = block['translation']
	comment = u"\n".join(block['comment']) if block['comment'] is not None else None

	assert not (('original_prelude' in block) ^ ('translation_prelude' in block))
	assert len(original) == len(translation)

	table_elems = []

	for i in xrange(len(original)):
		table_elems.append([u" ", leftField(original[i]), rightField(translation[i])])

	table_elems[0][0] = u"\\eddanumberfield{" + unicode(number) + u"}"

	if 'original_prelude' in block:
		original_p = block['original_prelude']
		translation_p = block['translation_prelude']
		assert len(original_p) == len(translation_p)

		prelude = []
		for i in xrange(len(original_p)):
			prelude.append([u" ", leftField(textit(original_p[i])),
				rightField(textit(translation_p[i]))])
		table_elems = prelude + table_elems

	table_lines = [u" & ".join(line) for line in table_elems]

	# Because of the strange behavior of tabular environment,
	# I have to apply additional skip after multiline rows to make all lines look evenly spaced.

	# FIXME: Line can be broken in two cases: if it's too long or if it has \sep
	# I can detect the latter case, but not the former.
	# But I will try to avoid it anyway (and TeX will complain about overfull hbox,
	# so I'll let it slide for now)
	# FIXME: Yes, and it's not to good to rely on \sep breaking the line, but
	# if at some point in future it changes behaviour, I will remove this line anyway

	for i in xrange(len(table_lines)):
		line = table_lines[i] + u" \\\\"
		if i == len(table_lines) - 1 and comment is not None:
			line += u"*"
		if u"{\\sep}" in table_lines[i]:
			line += u"[\\baselineskip]"
		elif i < len(table_lines) - 1 and u"\\eddanumberfield" in table_lines[i + 1]:
			line += u"*"
		table_lines[i] = line

	table_contents = u"\n".join(table_lines)
	return "\\eddastanza % Stanza " + unicode(number) + u"\n" + \
		(u"[" + comment + u"]\n" if comment is not None else u"") + \
		u"{" + unicode(number) + u"}\n" + \
		u"{" + table_contents + u"}\n\n"

def printText(block):
	return u"\n".join(block['text'])

handlers = {
	'stanza pair': printStanzaTable,
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

	print "Processing: " + str(filename)

	blocks = json.load(codecs.open("chapters/" + filename, "r", "utf-8"))
	res = u"\n\n".join([handlers[block['type']](block) for block in blocks])

	f = codecs.open("build/" + name + ".tex", "w", "utf-8")
	f.write(res)
	f.close()

