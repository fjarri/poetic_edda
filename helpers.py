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
