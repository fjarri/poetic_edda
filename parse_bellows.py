# coding: utf-8

import codecs
import re
import sys
from xml.etree.ElementTree import Element, ElementTree, XML


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

def processBlock(b):

	if b.startswith(u'['):
		b = b[1:]
	if b.endswith(u']'):
		b = b[:-1]

	lines = b.split(u"\n")

	mo = re.match(ur'^Prose\. ', lines[0])
	if mo is not None:
		return {'type': 'prose comment', 'text': b[7:]}

	mo = re.match(ur'^(\d+)\. ', lines[0])

	if mo is not None:
		number = mo.group(1)
		return {'type': 'stanza', 'number': number,
			'text': u"\n".join([lines[0][len(number) + 2:]] + lines[1:]), 'comment': None}

	if len(lines) > 1:
		mo = re.match(ur'^(\d+)\. ', lines[1])
		if mo is not None:
			number = mo.group(1)
			return {'type': 'stanza', 'number': number,
				'text': u"\n".join([lines[1][len(number) + 2:]] + lines[2:]),
				'prelude': lines[0], 'comment': None}

	return {'type': 'text', 'text': b}

def processStanza(t):
	t = re.sub(ur'"([^"]+)"', ur"``\1''", t)
	return t.replace(u" | ", u"<sep />").split(u'\n')

def processProse(t):
	t = re.sub(ur'"([^"]+)"', ur"``\1''", t)
	t = re.sub(ur'\.\s+', u'.\n', t)
	return t.split(u'\n')

def processComment(t):

	chapters = [u'Voluspo', u'Hovamol', u'Vafthruthnismol', u'Grimnismol',
		u'Skirnismol', u'Harbarthsljoth', u'Hymiskvitha', u'Lokasenna',
		u'Thrymskvitha', u'Alvissmol', u'Baldrs Draumar', u'Rigsthula',
		u'Hyndluljoth', u'Svipdagsmol', u'Lays of the Heroes', u'Völundarkvitha',
		u'Helgakvitha Hjorvarthssonar', u'Helgakvitha Hundingsbana I',
		u'Helgakvitha Hundingsbana II', u'Fra Dautha Sinfjotla',
		u'Gripisspo', u'Reginsmol', u'Fafnismol', u'Sigrdrifumol',
		u'Brot af Sigurtharkvithu', u'Guthrunarkvitha I',
		u'Sigurtharkvitha en Skamma', u'Helreith Brynhildar',
		u'Drap Niflunga', u'Guthrunarkvitha II', u'Guthrunarkvitha III',
		u'Oddrunargratr', u'Atlakvitha en Grönlenzka', u'Atlamol en Grönlenzku',
		u'Guthrunarhvot', u'Hamthesmol']

	t = re.sub(ur'\s*\[fp\. \d+\]\s*', u' ', t) # remove [fp. ##]
	t = re.sub(ur'"([^"]+)"', ur"``\1''", t) # replace " by `` and ''

	for chapter in chapters:
		t = re.sub(chapter + ur', (\d+)',
			ur'<chapterref>' + chapter + ur'</chapterref>, <stanzaref chapter="' +
			chapter + ur'">\1</stanzaref>', t)
		t = re.sub(ur'([^">])' + chapter, ur'\1<chapterref>' + chapter + ur'</chapterref>', t)

	def findcf(mo):
		if mo.group(1) == u'cf':
			return u'cf. '
		elif mo.group(1) == u'Cf':
			return u'Cf. '
		else:
			return mo.group(1) + u'.\n'

	t = re.sub(ur"([\w\)\>\']+)\. ", findcf, t)
	return t.split(u'\n')



if __name__ == '__main__':

	input = sys.argv[1]
	output = sys.argv[2]

	answers = None
	if len(sys.argv) > 3:
		answers = list(sys.argv[3])

	f = codecs.open(input, 'r', 'utf-8')
	blocks = f.read().split(u"\n\n")
	f.close()

	c = Element('chapter', icelandic_name="", english_name="", translation="")

	# Add block with 'Introductory Note' header
	intro_block = Element('block', attrib={'class': 'text'})
	intro_section = Element('section')
	intro_section.text = 'Introductory Note'
	intro_block.append(intro_section)
	c.append(intro_block)

	# remove page marks
	blocks = [x for x in blocks if not re.match(ur'^p\. \d+', x)]

	# get introductory note
	for i, block in enumerate(blocks):
		if re.match(ur'^_+$', block) is None:
			e = Element('block', attrib={'class': 'text'})
			e.text = block
			c.append(e)
		else:
			break

	blocks = blocks[i+1:]

	c.append(Element('block', attrib={'class': 'sepline'}))

	# glue blocks, mark stanzas and comments
	new_blocks = []
	comments = []

	comment_area = False
	for block in blocks:
		if block.startswith(u'['):
			comment_area = True

		obj = processBlock(block)

		if not comment_area:
			if obj['type'] == 'stanza':
				new_blocks.append(obj)
			elif u'|' in obj['text'] or len(obj['text'].split('\n')) > 1:
				new_blocks[-1]['text'] += u'\n' + obj['text']
			elif len(new_blocks) == 0:
				new_blocks.append({'type': 'prose', 'text': obj['text'], 'comment': None})
			else:
				if answers is not None:
					s = answers.pop(0)
				else:
					print "* Previous text:\n" + new_blocks[-1]['text'] + \
						"\n* Current text:\n" + obj['text']

					s = raw_input("(p) new prose, (c) continuation? ")
				if s.startswith('p'):
					new_blocks.append({'type': 'prose', 'text': obj['text'], 'comment': None})
				else:
					new_blocks[-1]['text'] += u'\n' + obj['text']
		else:
			if obj['type'] == 'prose comment':
				for i in xrange(len(new_blocks) - 1, -1, -1):
					if new_blocks[i]['type'] == 'prose':
						new_blocks[i]['comment'] = obj['text']
						break
			elif obj['type'] == 'stanza':
				comments.append(obj)
			else:
				comments[-1]['text'] = comments[-1]['text'] + "\n" + obj['text']

		if block.endswith(u']'):
			comment_area = False

	for obj in comments:
		for block in new_blocks:
			if 'number' in block and block['number'] == obj['number']:
				block['comment'] = obj['text']
				break
		else:
			raise Exception(obj)

	for block in new_blocks:
		if 'text' in block:
			if block['type'] == 'stanza':
				block['text'] = processStanza(block['text'])
			else:
				block['text'] = processProse(block['text'])

		if 'comment' in block and block['comment'] is not None:
			block['comment'] = processComment(block['comment'])

		if block['type'] == 'stanza':

			translation = block['text']
			original = []

			for line in translation:
				if u'<sep />' in line:
					original.append(u"<sep />")
				else:
					original.append(u"")

			elem = Element('block', attrib={'class': 'stanza', 'number': block['number']})
			original = XML((u'<original>' + "<br />\n".join(original) +
				u'</original>').encode('utf-8'))
			translation = XML((u'<translation>' + "<br />\n".join(translation) +
				u'</translation>').encode('utf-8'))

			if 'prelude' in block:
				original_prelude = Element('original_prelude')
				original_prelude.text = u""
				translation_prelude = Element('translation_prelude')
				translation_prelude.text = block['prelude']

				elem.append(original_prelude)
				elem.append(original)
				elem.append(translation_prelude)
				elem.append(translation)
			else:
				elem.append(original)
				elem.append(translation)

			if 'comment' in block and block['comment'] is not None:
				comment = XML((u'<comment>' + "\n".join(block['comment']) +
					u'</comment>').encode('utf-8'))
				elem.append(comment)

			c.append(elem)

		elif block['type'] == 'prose':
			translation = block['text']
			original = [u""] * len(translation)

			elem = Element('block', attrib={'class': 'prose'})
			original = XML((u'<original>' + "<br />\n".join(original) +
				u'</original>').encode('utf-8'))
			translation = XML((u'<translation>' + "<br />\n".join(translation) +
				u'</translation>').encode('utf-8'))

			elem.append(original)
			elem.append(translation)

			if 'comment' in block and block['comment'] is not None:
				comment = XML((u'<comment>' + "\n".join(block['comment']) +
					u'</comment>').encode('utf-8'))
				elem.append(comment)

			c.append(elem)

		else:
			raise Exception(repr(block))

	tree = ElementTree(element=c)
	makePretty(tree.getroot())
	tree.write(open(sys.argv[2], mode='wb'), encoding='utf-8')
