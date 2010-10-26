==================
Poetic Edda diglot
==================

This project aims at producing the book with parallel Icelandic and English texts of Poetic Edda.
I am using the translation by Henry Adams Bellows,
because it is considered to be quite accurate and has detailed comments.
As for the original text, at the moment of writing this I am using
`this page <http://notendur.hi.is/eybjorn/>`_ as a primary source,
and `Saemunar Edda <http://etext.old.no/Bugge/>`_ by Sophus Bugge as a secondary one
(although, since I am by no means a specialist in Icelandic literature, this choice may be wrong;
if this is the case, do not hesitate to tell me about it).

This book is built by XeLaTeX, with most of the .tex files produced
from JSON data in ``chapters`` directory by ``build.py`` script.
This will help if I ever decide to start using ``ledmac`` and ``ledpar`` packages again.

------------------
Sources by chapter
------------------

* Voluspo: http://notendur.hi.is/eybjorn/ugm/voluspa/vsp3.html
* Hovamol:

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
* Try to find better font combination.

~~~~~~~~~~~~~~~~~~~~~~~~
Tasks for distant future
~~~~~~~~~~~~~~~~~~~~~~~~

* Add all remaining chapters;
* Add support for different paper sizes (in particular, try to typeset a proper book);
* Try to use footnotes instead of normal text for comments;
* Probably make build script run xelatex too?
