import json
import codecs


def sequence(contents, pair_limit=10):

	res = u""

	#res += u"\\begin{pairs}\n\n"

	for i, stanza in enumerate(contents):
		number = stanza['number']
		original = " \\\\\n".join(stanza['original'])
		translation = " \\\\\n".join(stanza['translation'])
		comment = u"\n".join(stanza['comment']) if stanza['comment'] is not None else None

		#if (i + 1) % pair_limit == 0:
		#	res += u"\\end{pairs}\n\n\\begin{pairs}\n\n"

		res += u"\\mystanzapair % Stanza " + unicode(number) + u"\n" + \
			(u"[" + comment + u"]\n" if comment is not None else u"") + \
			u"{\n" + original + u"}\n{\n" + translation + u"}\n\n"

	#res += u"\\end{pairs}"
	return res

voluspo = json.load(open("stanzas/voluspo.json"))
f = codecs.open("voluspo.tex", "w", "utf-8")
f.write(sequence(voluspo))
f.close()

