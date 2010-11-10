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
