# coding: utf-8

from xml.etree.ElementTree import ElementTree, Element, dump, XML, XMLParser
import codecs
import sys
import json
import re, os

#input = sys.argv[1]
#output = sys.argv[2]

def makePretty(elem, depth=0):
	divs = ['chapter', 'block', 'original', 'translation', 'comment',
		'original_prelude', 'translation_prelude', 'textstanza']

	if elem.tag not in divs:
		return

	prefix = u"\n" + u"\t" * (depth + 1)

	if len(elem) > 0 or elem.text is not None:

		elem.text = prefix + (elem.text.replace(u"\n", prefix) if elem.text is not None else u"")

		if len(elem) == 0:
			elem.text = elem.text + prefix[:-1]
		else:
			for e in elem:

				if e.tail is not None:
					e.tail = e.tail.replace(u"\n", prefix)

				if e.tag in divs:
					makePretty(e, depth + 1)
					e.tail = (e.tail if e.tail is not None else "") + prefix

			if elem[-1].tail is None:
				elem[-1].tail = prefix[:-1]
			else:
				if elem[-1].tail.endswith(u'\t'):
					elem[-1].tail = elem[-1].tail[:-1]
				else:
					elem[-1].tail += prefix[:-1]


def detexifyText(s, chapter, tag):

	s = s.replace(u' \\\\', u'<br />')
	s = s.replace(u'{\\sep}', u'<sep />')
	s = s.replace(u'\\sep', u'<sep />')
	s = s.replace(u'{\\ndash}', u'\u2013')
	s = s.replace(u'\\ndash', u'\u2013')
	s = s.replace(u'{\\mdash}', u'\u2014')
	s = s.replace(u'\\mdash', u'\u2014')
	s = s.replace(u'{\\sdash}', u'\u2014')
	s = s.replace(u'\\sdash', u'\u2014')
	s = s.replace(u'{\\commamdash}', u'\u2014')
	s = s.replace(u'\\commamdash', u'\u2014')
	s = s.replace(u'``', u'\u201c')
	s = s.replace(u"''", u'\u201d')

	s = s.replace(u'{[}', u'[')
	s = s.replace(u'{]}', u']')

	if s.startswith(u'\\eddainlinestanza{'):
		s = s.replace(u'\\eddainlinestanza{', u'')[:-1]

	s = re.sub(ur'\\addsec\*\{([\w\- ?.]+)\}',
		ur'<section>\1</section>', s, flags=re.UNICODE)

	intro_stanza = u'\\textit' in s
	s = re.sub(ur'\\textit\{([\w .,;]+)\}', ur'<stress>\1</stress>', s, flags=re.UNICODE)
	s = s.replace(u'\\hskip 1.5em ', u'')

	s = re.sub(ur'\\textsc\{([\w .]+)\}', ur'<inlinesection>\1</inlinesection>', s, flags=re.UNICODE)

	s = s.replace(u'\\noindent', u'')
	s = s.replace(u'&', u'&amp;')
	s = s.replace(u'\\begin{tabular}{@{} p{0.4\\textwidth} @{} p{0.5\\textwidth}}',
		u'<table>')
	s = s.replace(u'\\begin{tabular}{@{} p{0.4\\textwidth} @{} p{8em} @{} p{1.5em} @{} p{0.3\\textwidth}}',
		u'<table>')
	s = re.sub(ur'\\multirow\{2\}\{\*\}\{\\Large \\\}}', ur'<multirow><large>}</large></multirow>', s)
	s = re.sub(ur'\\multirow\{2\}\{0.3\\textwidth\}\{([^{}]+)\}', ur'<multirow>\1</multirow>', s)
	s = s.replace(u'\\end{tabular}', u'</table>')
	s = s.replace(u'\\vskip 0.5em', u'')

	s = s.replace(u'{\\eddadagger} ', u'<dagger /> ')
	s = s.replace(u'\\eddadagger\\, ', u'<dagger /> ')

	s = s.replace(u'{\\eddalacuna} \\,', u'<lacuna />')
	s = s.replace(u'{\\eddalacuna}', u'<lacuna />')
	s = s.replace(u'\\eddalacuna \\,', u'<lacuna />')
	s = s.replace(u'\\eddalacuna', u'<lacuna />')

	s = s.replace(u'\\textstanzastart', u'<textstanza>')
	s = s.replace(u'\\textstanzaend', u'</textstanza>')

	s = re.sub(ur'\\eddastanzaprelude\{([\w :]+)\}',
		ur'<stanzaprelude>\1</stanzaprelude>', s, flags=re.UNICODE)

	# catch explanations in the beginning of the line
	if tag == 'comment':
		s = re.sub(ur'^\\emph\{([\w!,.\-\'() ]+?)([.:;,?]?)\}',
			ur'<expl>\1</expl>\2', s, flags=re.UNICODE)

	def emph_parser(mo):
		sentence_start = (mo.group(1) == u'\n')
		contents = mo.group(2)
		punctuation = mo.group(3)

		if contents in (u'Regius', u'Hauksbok', u'Corpus Poeticum Boreale',
				u'Poetic Edda', u'Nibelungenlied', u'Uppsalabok', u'Edda', u'Younger Edda',
				u'Elder Edda', u'Poetic Edda', u'Codex Regius', u'Grougaldr', u'Prose Edda',
				u'Fjolsvinnsmol', u'Gǫterdämmerung', u'Arnamagnæan Codex', u'Poetic',
				u'Loddfafnismol', u'Ljothatal', u'Iliad', u'Egilssaga'):
			s = ur'<source>{name}</source>{punc}'
		elif tag in ('original', 'translation'):
			s = ur'{fold}<conj>{name}</conj>{punc}'
		elif tag == 'comment' and sentence_start:
			s = ur'{fold}<expl>{name}</expl>{punc}'
		else:
			s = ur'{fold}<emph>{name}</emph>{punc}'

		return s.format(name=contents, punc=punctuation, fold=mo.group(1))

	s = re.sub(ur'(\n?)\\emph\{([\w!,.\-\'() ]+?)([.:;,?]?)\}', emph_parser, s, flags=re.UNICODE)

	s = re.sub(ur'\\eddastanzaref\{(\d+)\}', ur'<stanzaref>\1</stanzaref>', s, flags=re.UNICODE)
	s = re.sub(ur'\{\\eddastanzaref\[([\w ]+)\]\{(\d+)\}\}', ur'<stanzaref chapter="\1">\2</stanzaref>', s, flags=re.UNICODE)

	s = re.sub(ur'\\eddastanzarangeref\{(\d+)\}\{(\d+)\}', ur'<stanzaref>\1</stanzaref>\u2013<stanzaref>\2</stanzaref>', s, flags=re.UNICODE)
	s = re.sub(ur'\{\\eddastanzarangeref\[([\w ]+)\]\{(\d+)\}\{(\d+)\}\}',
		ur'<stanzaref chapter="\1">\2</stanzaref>\u2013<stanzaref chapter="\1">\3</stanzaref>', s, flags=re.UNICODE)

	s = re.sub(ur'\\eddaproseref\{([\w ]+)\}\{([\w ]+)\}',
		ur'<proseref chapter="\1">\2</proseref>', s, flags=re.UNICODE)
	s = re.sub(ur'\{\\eddaproseref\[([\w ]+)\]\{([\w ]+)\}\{([\w ]+)\}\}',
		ur'<proseref chapter="\2" label="\3">\1</proseref>', s, flags=re.UNICODE)

	s = re.sub(ur'\\eddacombinedproseref\{([\w ]+)\}\{([\w ]+)\}',
		ur'<chapterref>\1</chapterref>, <proseref chapter="\1">\2</proseref>', s, flags=re.UNICODE)

	s = re.sub(ur'\{\\eddacombinedproseref\[([\w ]+)\]\{([\w ]+)\}\{([\w ]+)\}\}',
		ur'<chapterref>\2</chapterref>, <proseref chapter="\2" prose="\3">\1</proseref>', s, flags=re.UNICODE)

	s = re.sub(ur"\\eddachapterref\{([\w ]+)'s([.:;,]?)\}", ur'<chapterref label="\1">\1' + ur"'s"  + ur'</chapterref>\2', s, flags=re.UNICODE)
	s = re.sub(ur"\\eddachapterref\{([\w ]+)([.:;,]?)\}", ur'<chapterref>\1</chapterref>\2', s, flags=re.UNICODE)

	s = re.sub(ur"\\eddacombinedref\{([\w ]+)\}\{(\d+)\}", ur'<chapterref>\1</chapterref>, <stanzaref chapter="\1">\2</stanzaref>', s, flags=re.UNICODE)
	s = re.sub(ur"\\eddacombinedrangeref\{([\w ]+)\}\{(\d+)\}\{(\d+)\}",
		ur'<chapterref>\1</chapterref>, <stanzaref chapter="\1">\2</stanzaref>\u2013<stanzaref chapter="\1">\3</stanzaref>', s, flags=re.UNICODE)

	s = re.sub(ur'\{\\hyperref\[\\eddachapterlabel\]\{([\w ]+)\}\}',
		ur'<ref chapter="'  + chapter + ur'">\1</ref>', s, flags=re.UNICODE)

	s = re.sub(ur'\{\\hyperref\[General Introduction\]\{General Introduction\}\}',
		ur'<ref chapter="General Introduction">General Introduction</ref>', s, flags=re.UNICODE)

	s = s.replace(u'\\chapterref{Grimnismol}{introductory note}',
		u'<chapterref chapter="Grimnismol">introductory note</chapterref>')

	if u'\\' in s or u'{' in s:
		print s
		raise Exception(s)

	if intro_stanza:
		s = u'<textstanza>' + s + u'</textstanza>'

	t = XML((u'<temp>' + s + u'</temp>').encode('utf-8'))

	for e in t:
		if e.tag in ('stanzaref', 'proseref') and 'chapter' not in e.attrib:
			e.attrib['chapter'] = chapter

	return t

def detexify(elem, chapter):

	if elem.tag == 'chapter':
		chapter = elem.attrib['english_name']

	if len(elem) > 0:
		for child in elem:
			detexify(child, chapter)
		return

	if elem.text is not None:
		t = detexifyText(elem.text, chapter, elem.tag)

		elem.text = t.text
		for e in t:
			elem.append(e)


def textToElements(s):
	return s, []

def transformJSON(c):
	# Process introduction
	intro = "\n".join(c[0]['text'])
	blocks = intro.split("\n\n")
	header = blocks[0]

	if 'eddasepline' in blocks[-1]:
		paragraphs = blocks[1:-1]
	else:
		paragraphs = blocks[1:]

	mo = re.match(r'\\eddachapter\{([^{}]+)\}\{([^{}]+)\}\{([^{}]+)\}', header)

	if mo is None:
		mo = re.match(ur'\\addchap\{([\w ]+)\}', header)
		root = Element('chapter', english_name=mo.group(1))
	else:
		root = Element('chapter', icelandic_name=mo.group(1),
			english_name=mo.group(2), translation=mo.group(3))

	for par in paragraphs:
		text, elements = textToElements(par)
		par_elem = Element('block', attrib={'class': 'text'})
		par_elem.text = text

		for elem in elements:
			par_elem.append(elements)

		root.append(par_elem)

	if 'eddasepline' in blocks[-1]:
		root.append(Element('block', attrib={'class': 'sepline'}))

	for block in c[1:]:

		if block['type'] == 'text' and block['text'][0] == u"\\eddasepline":
			elem = Element('block', attrib={'class': 'sepline'})

		elif block['type'] == 'prose':

			elem = Element('block', attrib={'class': 'prose', 'label': str(block['label'])})

			original = Element('original')
			original.text = u" \\\\\n".join(block['original'])
			elem.append(original)

			translation = Element('translation')
			translation.text = u" \\\\\n".join(block['translation'])
			elem.append(translation)

			if block['comment'] is not None:
				comment = Element('comment')
				comment.text = u"\n".join(block['comment'])
				elem.append(comment)

		elif block['type'] == 'stanza pair':

			elem = Element('block', attrib={'class': 'stanza', 'number': str(block['number'])})

			if 'original_prelude' in block:
				original_prelude = Element('original_prelude')
				original_prelude.text = u"\n".join(block['original_prelude'])
				elem.append(original_prelude)

			original = Element('original')
			original.text = u" \\\\\n".join(block['original'])
			elem.append(original)

			if 'original_prelude' in block:
				translation_prelude = Element('translation_prelude')
				translation_prelude.text = u"\n".join(block['translation_prelude'])
				elem.append(translation_prelude)

			translation = Element('translation')
			translation.text = u" \\\\\n".join(block['translation'])
			elem.append(translation)

			if block['comment'] is not None:
				lines = []
				inlinestanza = False

				for line in block['comment']:
					if line.startswith(u'\\eddainlinestanza'):
						inlinestanza = True
						line = line.replace(u'\\eddainlinestanza{', u'\\textstanzastart')

					if inlinestanza and line.endswith(u'}'):
						inlinestanza = False
						line = line[:-1] + u'\\textstanzaend'

					lines.append(line)

				s = u'\n'.join(lines)
				s = s.replace(u'\\textstanzaend\n\\textstanzastart',
					u'\\textstanzaend\\textstanzastart')
				comment = XML((u'<comment>' + s + u'</comment>').encode('utf-8'))
				elem.append(comment)

		else:
			raise Exception(repr(block))

		root.append(elem)

	detexify(root, None)
	tree = ElementTree(element=root)
	return tree

if __name__ == '__main__':

	filenames = os.listdir('chapters')

	for filename in filenames:
		name, ext = os.path.splitext(filename)
		if ext != '.json':
			continue

		print
		print "Processing: " + str(filename)
		print

		c = json.load(codecs.open("chapters/" + filename, 'r', 'utf-8'))
		tree = transformJSON(c)
		makePretty(tree.getroot())
		tree.write(open('chapters/' + name + '.xml', mode='wb'), encoding='utf-8')
