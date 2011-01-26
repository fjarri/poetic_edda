# coding=utf-8

from xml.etree.ElementTree import ElementTree
import codecs
import sys
import re

input = sys.argv[1]

if len(sys.argv) > 2:
	output = sys.argv[2]
else:
	output = input

substitutions = [
	(u"a_e`", u"ǣ"),
	(u"a_e", u"æ"),
	(u"o_e", u"œ"),
	(u"O_E", u"Œ"),
	(u"A_E", u"Æ"),

	(u"a`", u"ā"),
	(u"A`", u"Ā"),
	(u"e`", u"ē"),
	(u"e::", u"ë"),
	(u"E`", u"Ē"),
	(u"o`", u"ō"),
	(u"O`", u"Ō"),
	(u"y`", u"ȳ"),
	(u"Y`", u"Ȳ"),
	(u"u`", u"ū"),
	(u"i`", u"ī"),
	(u"i::", u"ï"),
	(u"I`", u"Ī"),

	(u"o/`", u"ø̄"),
	(u"o/", u"ø"),

	(u"O/`", u"Ø̄"),
	(u"O/", u"Ø"),

	(u"o~`", u"ǭ"),
	(u"o~", u"ǫ"),

	(u"O~`", u"Ǭ"),
	(u"O~", u"Ǫ"),

	(u"---", u"\u2014"),
	(u"--", u"\u2013"),
	(u"``", u"\u201c"),
	(u"''", u"\u201d")
]

def substituteText(s, tag):
	if s is None:
		return s

	for src, dst in substitutions:
		s = s.replace(src, dst)

	s = re.sub(ur"`([^']+)'", ur"‘\1’", s)
	s = s.replace(u"“ ‘", u"“‘")
	s = s.replace(u"’ ”", u"’”")

	if tag in ('original', 'translation'):
		s = s.replace(u'(', u'[')
		s = s.replace(u')', u']')

	return s

def substitute(elem, chapter=None):
	elem.text = substituteText(elem.text, elem.tag)
	elem.tail = substituteText(elem.tail, elem.tag)

	if elem.tag == 'chapter':
		chapter = elem.attrib['english_name']

	if elem.tag == 'src':
		elem.tag = 'source'

	if elem.tag == 'cr':
		elem.tag = 'chapterref'

	if elem.tag == 'pr':
		elem.tag = 'proseref'

	if elem.tag == 'proseref' and 'chapter' not in elem.attrib:
		elem.attrib['chapter'] = chapter

	if elem.tag == 'sr':
		elem.tag = 'stanzaref'

	if elem.tag == 'stanzaref' and 'chapter' not in elem.attrib:
		elem.attrib['chapter'] = chapter

	for e in elem:
		substitute(e, chapter)


tree = ElementTree(file=input)
substitute(tree.getroot())
tree.write(open(output, mode='wb'), encoding='utf-8')
