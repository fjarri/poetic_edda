==================
Poetic Edda diglot
==================

This project aims at producing the book with parallel Old Norse and English texts of Poetic Edda.
I am using the `translation by Henry Adams Bellows <http://www.archive.org/details/poeticedda00belluoft>`_,
because it is considered to be quite accurate and has detailed comments.
As for the original text, at the moment of writing this I am using
`"Die Lieder der älteren Edda" <http://www.archive.org/details/dieliederderedda0301geriuoft>`_
by Karl Hildebrand and Hugo Gering (this book was the main source for Bellows).

I will appreciate any proofreading (chapter, part of the chapter, only English or only Old Norse) ---
there are still lots of typos out there.

This book is built by XeLaTeX, with most of the .tex files produced
from JSON data in ``chapters`` directory by ``build.py`` script.
This will help if I ever decide to start using ``ledmac`` and ``ledpar`` packages again.

------------------
Sources by chapter
------------------

Sources: **Gering** ("Die Lieder der alteren Edda" by by Karl Hildebrand and Hugo Gering)

* Voluspo: Gering,
* Hovamol: Gering.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Modifications of Gering source
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

I tried to copy Old Norse stanzas from Gering's book as accurate as possible,
but I had to make a few modifications in order to make them conform to
Bellows's book.

First, in some places in Gering proper name starts from the lowercase letter;
I guess it was like this in the manuscripts, but I did not manage to find any system in this
and just capitalized first letters names (this creates better connection between
Old Norse and English texts).

Second, Gering and Bellows use slightly different glyphs for Old Norse: the main difference is
that Gering uses acute mark for long vowels, when Bellows uses macron.
This seems logical, because it helps to distinguish between long vowel marks and accent marks.
In addition, Bellows uses "o with diaeresis" instead of "o with stroke"
and "o with double acute" instead of "o with stroke and acute".
But since Gering uses diaeresis with i and e to mark the separate pronounciation in a diphthong,
this can become confusing; so I kept "o with stroke", but used macron instead of acute sign
to mark the longetivity.
It may be incorrect from the linguistic point of view, but it helps to read the Old Norse text.

Since the reader can see the Old Norse original near the translation, I omitted the
proper names index from Bellows's book (although I can include it later,
because it shows the accented syllables in names), leaving only the pronounciation guide
(where I made modifications according to the set of glyphs I use).
I have not cut any references to the index though, because that would require rearranging the text,
and I do not want to do that yet.

---------------
Release history
---------------

~~~~~~~~~~~~~~~~~~~~~
Voluspo (26 Oct 2010)
~~~~~~~~~~~~~~~~~~~~~

* Created base structure of the document;
* Only A4 format is supported;
* Added introduction and Voluspo chapter.

~~~~~~~~~~~~~~~~~
Hovamol (planned)
~~~~~~~~~~~~~~~~~

* Add Hovamol chapter and pronounciation guide;
* Generalize build script;
* Try to find better font combination. (kind of done)
* Use Gering's book as source for Voluspo (done)

~~~~~~~~~~~~~~~~~~~~~~~~
Tasks for distant future
~~~~~~~~~~~~~~~~~~~~~~~~

* Add all remaining chapters;
* Add support for different paper sizes (in particular, try to typeset a proper book);
* Try to use footnotes instead of normal text for comments;
* Probably make build script run xelatex too?
