# coding=utf-8

import json
import codecs
import sys

input = sys.argv[1]
output = sys.argv[2]
c = json.load(codecs.open(input, 'r', 'utf-8'))

substitutions = [
	(u"a_e`", u"ǣ"),
	(u"a_e", u"æ"),
	(u"o_e", u"œ"),
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

	(u"--", u"\u2013"),
	(u"---", u"\u2014"),
	(u"``", u"\u201c"),
	(u"''", u"\u201d")
]

def substitute(obj):
	if isinstance(obj, unicode):
		for fr, to in substitutions:
			obj = obj.replace(fr, to)
		return obj
	elif isinstance(obj, list):
		return [substitute(x) for x in obj]
	else:
		raise Exception("Wrong object: " + repr(obj))

for block in c:
	if not block['type'] == "stanza pair" and not block['type'] == "prose":
		continue

	block['original'] = substitute(block['original'])
	if 'original_prelude' in block:
		block['original_prelude'] = substitute(block['original_prelude'])

json.dump(c, codecs.open(output, 'w', 'utf-8'), indent=4, ensure_ascii=False)
