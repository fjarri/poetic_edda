import json
import codecs


def sequence(contents):

	res = u""

	for i, stanza in enumerate(contents):
		number = stanza['number']
		original = u" \\\\\n".join(stanza['original'])
		translation = u" \\\\\n".join(stanza['translation'])
		comment = u"\n".join(stanza['comment']) if stanza['comment'] is not None else None

		res += u"\\mystanzapair % Stanza " + unicode(number) + u"\n" + \
			(u"[" + comment + u"]\n" if comment is not None else u"") + \
			u"{\n" + original + u"}\n{\n" + translation + u"}\n\n"

	return res

voluspo = json.load(open("stanzas/voluspo.json"))
f = codecs.open("voluspo.tex", "w", "utf-8")
f.write(sequence(voluspo))
f.close()

