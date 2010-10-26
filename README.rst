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
from JSON data in ``stanzas`` directory by ``build.py`` script.
This will help if I ever decide to start using ``ledmac`` and ``ledpar`` packages again.

---------------
Release history
---------------

~~~~~~~~~~~~~~~~~
Voluspo (planned)
~~~~~~~~~~~~~~~~~

* Create base structure of the document (select fonts, write macros, build script etc);
* Support only A4 format
* Add introduction and Voluspo chapter.

~~~~~~~~~~~~~~~~~~~~~~~~
Tasks for distant future
~~~~~~~~~~~~~~~~~~~~~~~~

* Add all remaining chapters;
* Add pronounciation guide;
* Add support for different paper sizes (in particular, try to typeset a proper book);
* Try to use footnotes instead of normal text for comments.

