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

	(u"a`", u"ā"),
	(u"A`", u"Ā"),
	(u"e`", u"ē"),
	(u"e::", u"ë"),
	(u"E`", u"Ē"),
	(u"o`", u"ō"),
	(u"O`", u"Ō"),
	(u"y`", u"ȳ"),
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
	(u"O~", u"Ǫ")
]

for block in c:
	if not block['type'] == "stanza pair":
		continue

	new_lines = []
	for line in block['original']:
		for fr, to in substitutions:
			line = line.replace(fr, to)
		new_lines.append(line)

	block['original'] = new_lines

json.dump(c, codecs.open(output, 'w', 'utf-8'), indent=4, ensure_ascii=False)
