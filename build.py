# coding=utf-8

from xml.etree.ElementTree import ElementTree, dump
import codecs
import os, os.path
import re

def deprettify(elem):
	divs = ['chapter', 'block', 'original', 'translation', 'comment',
		'original_prelude', 'translation_prelude', 'textstanza']

	delete_spaces = lambda s: re.sub(ur'\s+', ' ', s, flags=re.UNICODE)

	if elem.text is not None:
		elem.text = elem.text.lstrip()
		elem.text = delete_spaces(elem.text)

	if len(elem) > 0:

		for e in elem:
			deprettify(e)

			if e.tail is not None:
				e.tail = delete_spaces(e.tail)
				if e.tail == '':
					e.tail = None

		if elem[-1].tail is not None:
			elem[-1].tail = elem[-1].tail.rstrip()
			if elem[-1].tail == '':
				elem[-1].tail = None

	else:
		if elem.text is not None:
			elem.text = elem.text.rstrip()

	if elem.text == '':
		elem.text = None


# Function for printing paired stanzas as multi-row tables
def printStanzaTable(block):

	# helper functions for wrapping table cells
	leftField = lambda x: u"\\eddastanzaleft{" + x + u"}"
	rightField = lambda x: u"\\eddastanzaright{" + x + u"}"
	textit = lambda x: u"\\eddastanzaprelude{\\textit{" + x + u"}}"

	# get info from block
	number = block.attrib['number']
	original = printText(block.find('original')).split(u'\\\\\n')
	translation = printText(block.find('translation')).split(u'\\\\\n')
	comment = printText(block.find('comment')) if block.find('comment') is not None else None

	original_prelude = printText(block.find('original_prelude')).split(u'\n') \
		if block.find('original_prelude') is not None else None
	translation_prelude = printText(block.find('translation_prelude')).split(u'\n') \
		if block.find('translation_prelude') is not None else None

	# check if both preludes are present, or both absent
	assert not ((original_prelude is None) ^ (translation_prelude is None))

	# check that original and translation have same number of lines
	# (we are using multirow table, which is sensitive to this)
	assert len(original) == len(translation)

	# Add main table cells
	table_elems = []
	for i in xrange(len(original)):
		assert not ((u'{\\sep}' in original[i]) ^ (u'{\\sep}' in translation[i])), \
			"Non-matching separators at line " + str(i + 1) + " of stanza " + str(number)
		table_elems.append([u" ", leftField(original[i]), rightField(translation[i])])

	# Add a table cell with stanza number
	table_elems[0][0] = u"\\eddastanzanumber{" + unicode(number) + u"}"

	# Add table cells with prelude
	if original_prelude is not None:
		assert len(original_prelude) == len(translation_prelude)

		prelude = []
		for i in xrange(len(original_prelude)):
			prelude.append([u" ", leftField(textit(original_prelude[i])),
				rightField(textit(translation_prelude[i]))])
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
		line = table_lines[i] + u" \\\\" # base ending for all lines

		if i == len(table_lines) - 1 and comment is not None:
		# disable page break after last line (does not work, actually, just here for reference)
			line += u"*"
		if u"{\\sep}" in table_lines[i]:
		# additional space between rows for multiline stanza lines (yeah, sounds bad)
		# workaround for strange longtable behavior
			line += u"[\\baselineskip]"
		elif i < len(table_lines) - 1 and u"\\eddastanzanumber" in table_lines[i + 1]:
		# disable page break after prelude
			line += u"*"

		table_lines[i] = line

	table_contents = u"\n".join(table_lines)
	return "\\eddastanza % Stanza " + unicode(number) + u"\n" + \
		(u"[" + comment + u"]\n" if comment is not None else u"") + \
		u"{" + unicode(number) + u"}\n" + \
		u"{\\eddastanzatable{" + table_contents + u"}}\n\n"

def printProseTable(block):

	# helper functions for wrapping table cells
	leftField = lambda x: u"\\eddaproseleft{" + x + u"}"
	rightField = lambda x: u"\\eddaproseright{" + x + u"}"

	# get info from block
	original = printText(block.find('original')).split(u'\\\\\n')
	translation = printText(block.find('translation')).split(u'\\\\\n')
	comment = printText(block.find('comment')) if block.find('comment') is not None else None

	# check that original and translation have same number of lines
	# (we are using multirow table, which is sensitive to this)
	assert len(original) == len(translation), str(len(original)) + " " + str(len(translation))

	# Add main table cells
	table_elems = []
	for i in xrange(len(original)):
		table_elems.append([leftField(original[i]), rightField(translation[i])])

	table_lines = [u"\\vskip0.5\\baselineskip \n \\eddaprosetable{" + u" & ".join(line) + u"}" for line in table_elems]
	table_contents = u"\n".join(table_lines)
	return "\\eddastanza\n" + \
		(u"[" + comment + u"]\n" if comment is not None else u"") + \
		u"{" + block.attrib['label'] + u"}\n" + \
		u"{" + table_contents + u"}\n\n"

def tableToTex(elem):

	def sizeToTex(s):
		if s.endswith(u"em"):
			return c
		elif s.endswith(u"%"):
			return str(float(s[:-1]) / 100) + u"\\textwidth"
		else:
			raise Exception("Unknown units: " + s)

	columns = elem.attrib['columns'].split()
	columns = [sizeToTex(c) for c in columns]

	column_counter = [0] * len(columns)

	columns = " ".join([u'@{} p{' + c + u'}' for c in columns])
	header = u'\\noindent\\begin{tabular}{' + columns + u'}\n'

	lines = []

	for tr in elem:
		line = []
		local_id = 0

		for global_id in xrange(len(column_counter)):
			if column_counter[global_id] == 0:
				td = tr[local_id]

				if 'rowspan' in td.attrib:
					column_counter[global_id] = int(td.attrib['rowspan']) - 1
					line.append(u'\\multirow{{{span}}}{{{width}}}{{{text}}}'.format(
						span=td.attrib['rowspan'],
						text=printText(td),
						width=("*" if 'width' not in td.attrib else sizeToTex(td.attrib['width']))
					))
				else:
					line.append(printText(td))

				local_id += 1
			else:
				line.append('')
				column_counter[global_id] -= 1

		lines.append(line)

	res = header + u" \\\\\n".join([u" & ".join(line) for line in lines]) + \
		" \\\\\n\\end{tabular}\n\n"

	return res

def blockToList(block):

	if block.text is not None:
		res = [[block.text, None, None]]
	else:
		res = []

	for elem in block:
		if elem.tag == 'table':
			res.append([tableToTex(elem), elem.tag, None])
		elif elem.tag in ('textstanza', 'linestanza'):
			res.append([blockToList(elem), elem.tag, elem.attrib])
		else:
			# save reference, because the text can be changed during movePunctuation
			if elem.tag == 'chapterref' and 'chapter' not in elem.attrib:
				elem.attrib['chapter'] = elem.text

			res.append([elem.text, elem.tag, elem.attrib])
		if elem.tail is not None:
			res.append([elem.tail, None, None])

	return res

def movePunctuation(l):

	for i, e in enumerate(l):
		text, tag, attrib = tuple(e)

		if i == len(l):
			continue

		if tag not in ('emph', 'chapterref', 'source', 'conj', 'expl'):
			continue

		if l[i+1][0] is None or l[i+1][0][0] not in ('.', ',', ';', ':', '?', '!'):
			continue

		e[0] = e[0] + l[i+1][0][0] # add punctuation to wrapped text
		l[i+1][0] = l[i+1][0][1:] # remove punctuation from tail

	# Insert nonbreakable spaces
	# FIXME: using TeX symbols here, needs to be generalized
	for i, e in enumerate(l):
		text, tag, attrib = tuple(e)

		if text is None or isinstance(text, list):
			continue

		# abbreviations

		if u'q. v.' in text:
			e[0] = e[0].replace('q. v.', 'q.~v.')

		if u'Q. v.' in text:
			e[0] = e[0].replace('Q. v.', 'Q.~v.')

		if u'i. e.' in text:
			e[0] = e[0].replace('i. e.', 'i.~e.')

		# "lines~4--5"
		if re.search(r'(l|L)ines? \d', text) is not None:
			e[0] = re.sub(r'(l|L)ine(s?) (\d)', r'\1ine\2~\3', e[0])

		# "cf.~Voluspo"
		if text.endswith('cf. ') or text.endswith('Cf. '):
			e[0] = e[0][:-1] + u"~"

		# "stanza~21"
		if i < len(l) - 1 and (text.endswith('tanza ') or text.endswith('tanzas ')) and \
				l[i + 1][1] == 'stanzaref':
			e[0] = e[0][:-1] + u"~"

		# "Voluspo,~33"
		if i > 0 and i < len(l) - 1 and l[i - 1][1] == 'chapterref' and \
				l[i + 1][1] == 'stanzaref' and text == ' ':
			e[0] = '~'

		# "stanza 22,~1" (reference to a line)
		if i > 0 and l[i - 1][1] == 'stanzaref' and re.match(r', \d', text) is not None:
			e[0] = u",~" + e[0][2:]


def listToTex(l):

	modifying_tags = ['emph', 'chapterref']
	res = []

	for e in l:
		text, tag, attrib = tuple(e)

		if tag == 'table':
			res.append(text)
			continue

		if isinstance(text, unicode) or isinstance(text, str):
			text = text.replace('}', '\\}')
			text = text.replace('{', '\\{')
			text = text.replace('[', '{[}')
			text = text.replace(']', '{]}')

			# macros from 'extdash' package - dashes with tuned linebreaks
			text = text.replace(u'—', u'\---')
			text = text.replace(u'–', u'\--')

		if tag is None:
			res.append(text)

		elif tag == 'ref':
			res.append(u'\\eddachapterref{{{chapter}}}{{{text}}}'.format(
				chapter=attrib['chapter'], text=text))

		elif tag == 'chapterref':
			res.append(u'\\eddachapterref{{{chapter}}}{{\\textit{{{text}}}}}'.format(
				chapter=text if 'chapter' not in attrib else attrib['chapter'],	text=text))

		elif tag == 'stanzaref':
			res.append(u'\\eddastanzaref{{{chapter}}}{{{stanza}}}'.format(
				chapter=attrib['chapter'],
				stanza=text if 'stanza' not in attrib else attrib['stanza']))

		elif tag == 'proseref':
			res.append(u'\\eddaproseref{{{chapter}}}{{{label}}}{{{text}}}'.format(
				chapter=attrib['chapter'],
				label=attrib['prose'] if 'prose' in attrib else text,
				text=text
			))

		elif tag == 'stanzaprelude':
			res.append(u'\\eddastanzaprelude{\\textit{' + text + u'}}')

		elif tag == 'emph':
			res.append(u'\\myemph{' + text + u'}')

		elif tag == 'source':
			res.append(u'\\mysource{' + text + u'}')

		elif tag == 'br':
			res.append(u'\\\\\n')

		elif tag == 'sep':
			res.append(u'{\\sep}')

		elif tag == 'lacuna':
			res.append(u'{\\eddalacuna}')

		elif tag == 'dagger':
			res.append(u'{\\eddadagger}')

		elif tag == 'section':
			res.append(u'\\addsec*{' + text + u'}')

		elif tag == 'stress':
			res.append(u'\\textit{' + text + u'}')

		elif tag == 'conj':
			res.append(u'\\myconj{' + text + u'}')

		elif tag == 'expl':
			res.append(u'\\myexpl{' + text + u'}')

		elif tag == 'inlinesection':
			res.append(u'\\textsc{' + text + u'}')

		elif tag == 'large':
			res.append(u'\\Large{' + text + u'}')

		elif tag == 'textstanza':
			res.append(u'\n\\eddainlinestanza{' + listToTex(text) + u'}\n')

		elif tag == 'linestanza':
			res.append(listToTex(text))

		else:
			raise Exception("Wrong markup tag: " + tag)

	return u"".join(res)

def printText(block):
	l = blockToList(block)
	movePunctuation(l)
	res = listToTex(l)

	if 'vmargins' in block.attrib:
		vskip = u'\\vskip ' + block.attrib['vmargins']
		return u'{vskip}\n{res}\n{vskip}'.format(vskip=vskip, res=res)
	else:
		return res

def printChapterHeader(block):
	if 'icelandic_name' in block.attrib:
		return u"\\eddachapter{" + block.attrib['icelandic_name'] + \
			u"}{" + block.attrib['english_name'] + u"}{" + block.attrib['translation'] + u"}"
	else:
		return u"\\addchap{" + block.attrib['english_name'] + u'}'

def printSepline(block):
	return u"\\eddasepline"


if __name__ == '__main__':

	handlers = {
		'stanza': printStanzaTable,
		'text': printText,
		'prose': printProseTable,
		'chapter': printChapterHeader,
		'sepline': printSepline
	}

	filenames = os.listdir('chapters')

	if not os.path.exists('build'):
		os.mkdir('build')
	elif not os.path.isdir('build'):
		print "Build directory name is taken"
		exit(1)

	for filename in filenames:
		name, ext = os.path.splitext(filename)
		if ext != '.xml':
			continue

		print "Processing: " + str(filename)

		f = open("chapters/" + filename)
		tree = ElementTree(file=f)

		root = tree.getroot()
		deprettify(root)

		res = handlers['chapter'](root) + u"\n\n" + \
			u"\n\n".join([handlers[block.attrib['class']](block) for block in root])

		f = codecs.open("build/" + name + ".tex", "w", "utf-8")
		f.write(res)
		f.close()

