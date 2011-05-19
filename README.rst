==================
Poetic Edda diglot
==================

This project aims at producing the book with parallel Old Norse and English texts of Poetic Edda.
I am using the `translation by Henry Adams Bellows <http://www.archive.org/details/poeticedda00belluoft>`_,
because it is considered to be quite accurate and has detailed comments.
As for the original text, at the moment of writing this I am using
`"Die Lieder der älteren Edda" <http://www.archive.org/details/dieliederderlt00hilduoft>`_
by Karl Hildebrand and Hugo Gering (this book was the main source for Bellows).

I will appreciate any proofreading (chapter, part of the chapter, only English or only Old Norse) ---
there are still lots of typos out there.

This book is built by XeLaTeX, with most of the .tex files produced
from XML data in ``chapters`` directory by ``build.py`` script.
This will help if I ever decide to start using ``ledmac`` and ``ledpar`` packages again.

----------
Used fonts
----------

* `Gentium Plus <http://scripts.sil.org/cms/scripts/page.php?item_id=Gentium_download#801ab246>`_
  and `Charis <http://scripts.sil.org/cms/scripts/page.php?item_id=CharisSIL_download#c7cc4bf5>`_ by SIL;
* Lucida Grande and Optima from standard Snow Leopard font pack;
* Cover page: `Vidir Futhark <http://www.fontspace.com/vidir-thorisson/vidir-futhark>`_

------------------------------
Modifications of Gering source
------------------------------

I tried to copy Old Norse stanzas from Gering's book as accurate as possible,
but I had to make a few modifications in order to make them conform to
Bellows's book.

First, Gering and Bellows use slightly different glyphs for Old Norse: the main difference is
that Gering uses acute mark for long vowels, when Bellows uses macron.
The latter approach seems logical, because it helps to distinguish between long vowel marks and accent marks.
In addition, Bellows uses "o with diaeresis" instead of "o with stroke"
and "o with double acute" instead of "o with stroke and acute".
But since Gering uses diaeresis with i and e to mark the separate pronounciation in a diphthong,
this can become confusing; so I kept "o with stroke", but used macron instead of acute sign
to mark the longetivity.
It may be incorrect from the linguistic point of view, but it helps to read the Old Norse text.
I will be glad to hear any professional opinion about this.

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

~~~~~~~~~~~~~~~~~~~~~
Hovamol (15 Nov 2010)
~~~~~~~~~~~~~~~~~~~~~

* Added Hovamol chapter;
* Added pronounciation guide (without the proper names index);
* Generalized build script;
* Reworked book design (still far from perfect, but at least not too ugly);
* Used Gering's book as source for Voluspo;
* Added cover page.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Vafthruthnismol (20 Nov 2010)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* Added Vafthruthnismol chapter;
* Fixed quotation marks in Voluspo, 28;
* Added rendering for stanza preludes;
* Refactored macros;
* Voluspo, 54: removed line folding from inline stanza;
* Voluspo, 35: fixed Old Norse stanza in comment (took it from Gering);
* Reworked stanza macros to allow page breaks in stanzas;
* Fixed non-matching separators in Hovamol 79, 80, 131 and Voluspo, 12;
* Added protrusion config for Charis SIL to repository

~~~~~~~~~~~~~~~~~~~~~~~~
Grimnismol (27 Nov 2010)
~~~~~~~~~~~~~~~~~~~~~~~~

* Now controlling whitespace from top and bottom of longtable manually;
* Introduction: fixed case of letter thorn;
* Added Grimnismol chapter;
* Added rendering for prose parts;
* Added macro for referring to prose in chapters

~~~~~~~~~~~~~~~~~~~~~~~~
Skirnismol (30 Nov 2010)
~~~~~~~~~~~~~~~~~~~~~~~~

* Added Skirnismol chapter

~~~~~~~~~~~~~~~~~~~~~~~~~~~
Harbarthsljoth (7 Dec 2010)
~~~~~~~~~~~~~~~~~~~~~~~~~~~

* Added Harbarthsljoth chapter

~~~~~~~~~~~~~~~~~~~~~~~~~
Hymiskvitha (11 Dec 2010)
~~~~~~~~~~~~~~~~~~~~~~~~~

* Add Hymiskvitha chapter

~~~~~~~~~~~~~~~~~~~~~~~
Lokasenna (14 Jan 2011)
~~~~~~~~~~~~~~~~~~~~~~~

* Transformed chapter data to XML format, added some semantic info;
* Renamed and committed parsing scripts;
* Added chapter/combined references recognition to substitute.py;
* Skirnismol, introductory note: fixed reference to Grimnismol's introductory note;
* Skirnismol, 3, 5: added missing colons to preludes;
* Introduction: added missing space between two sentences, fixed typo (in stead -> instead),
  fixed typo (ndash -> mdash), added missing reference to Baldrs Draumar;
* Introduction: unified diacritics scheme with the rest of the book;
* Voluspo, 42: fixed typo in comment (comma -> colon);
* Voluspo, 4: fixed typo (diacritics);
* Voluspo, 65: added original to stanza in comment;
* Hovamol: added inline stanza originals in comments for stanzas 65, 87, 102, 133;
* Vafthruthnismol: added inline stanza originals in comments for stanzas 27, 54;
* Hymiskvitha: marked one-line stanzas with their own tag;
* Added color-coding for draft mode;
* Marking conjectures with "[]" in both original and translation (Bellows originally used "()");
* Added Lokasenna chapter

~~~~~~~~~~~~~~~~~~~~~~~~~~
Thrymskvitha (22 Jan 2011)
~~~~~~~~~~~~~~~~~~~~~~~~~~

* Added Thrymskvitha chapter;
* Fixed many typos in Voluspo (it was the first chapter and the process
  of adding it was rather messy);
* Inserting unbreakable spaces during build:

  * "cf.~", "i.~e.",
  * "stanza~NN",
  * "Chapter,~NN",
  * "line~N",
  * "stanza NN,~N" (line reference);

* Using en and em dashes with proper linebreaking;
* Fixed bug in TeX replacements, which gave '{[}' instead of '[' in the final text;
* Added colors for explanations, references and stanza preludes
  in final mode (we'll see how it goes);
* Removed text indentation after inline stanzas

~~~~~~~~~~~~~~~~~~~~~~~
Alvissmol (26 Jan 2011)
~~~~~~~~~~~~~~~~~~~~~~~

* Disabled page breaks before and after \eddasepline;
* Added Alvissmol chapter;
* Performed forgotten substitutions for inline stanza in Vafthruthnismol;
* Added processing of adjacent single and double quotation marks in build script

~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Baldrs Draumar (27 Jan 2011)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* Added Baldrs Draumar chapter;
* Added missing prelude to Thrymskvitha, 4;
* Fixed original/translation preludes confusion in Thrymskvitha and Alvissmol

~~~~~~~~~~~~~~~~~~~~~~~
Rigsthula (12 Feb 2011)
~~~~~~~~~~~~~~~~~~~~~~~

* Added Rigsthula chapter;
* Fixed references to Global Introduction;
* Added 'Introductory note' section in the beginning of each chapter

~~~~~~~~~~~~~~~~~~~~~~~~~
Hyndluljoth (17 Feb 2011)
~~~~~~~~~~~~~~~~~~~~~~~~~

* Added Hyndluljoth chapter;
* Printing references like "<cr>Guthrunarkvitha II</cr>" in form
  "<i>Guthrunarkvitha</i> II" (i.e., not italicising part number);
* Fixed reference in Harbarthsljoth introduction

~~~~~~~~~~~~~~~~~~~~~~~~~
Svipdagsmol (26 Feb 2011)
~~~~~~~~~~~~~~~~~~~~~~~~~

* Added Svipdagsmol chapter;
* Printing headings in English instead of Old Norse (like in Bellows)

~~~~~~~~~~~~~~~~~~~~~~~~~~~
Volundarkvitha (4 Mar 2011)
~~~~~~~~~~~~~~~~~~~~~~~~~~~

* Added Volundarkvitha chapter;
* Fixed some non-substituted 'U+macron' symbols in Svipdagsmol;
* Fixed disappeared running headings (the bug was introduced in Rigsthula)

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Helgakvitha Hjorvarthssonar (14 Mar 2011)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* Added Helgakvitha Hjorvarthssonar chapter;
* Made text in stanzas left justified;
* Enabled protrusion in stanzas to handle some badly typeset lines

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Helgakvitha Hundingsbana I (19 Mar 2011)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* Added Helgakvitha Hundingsbana I chapter

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Helgakvitha Hundingsbana II (28 Mar 2011)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* Added Helgakvitha Hundingsbana II chapter

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Fra Dautha Sinfjotla (28 Mar 2011)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* Added Fra Dautha Sinfjotla chapter;
* Made all prose labels uniform ('pN' for those before stanzas
  and 'conclusion' for the last ones);
* Voluspo, 8: fixed typo (in stead -> instead);
* Fixed the problem with not working \nopagebreak between \addsec and longtable:
  putting section titles in tables now;
* Using asterisks instead of seplines inside chapters (like Bellows did).
  Also added two missing seplines in Helgakvitha Hjorvarthssonar and Svipdagsmol
  for consistency

~~~~~~~~~~~~~~~~~~~~~~
Gripisspo (8 Apr 2011)
~~~~~~~~~~~~~~~~~~~~~~

* Added Gripisspo chapter;
* Fixed case in Svipdagsmol subtitle;
* Bellow's book parser now watches for unmatched comments and comments with the
  same identifiers (in order not to lose them)

~~~~~~~~~~~~~~~~~~~~~~~
Reginsmol (14 Apr 2011)
~~~~~~~~~~~~~~~~~~~~~~~

* Added Reginsmol chapter;
* Fixed bug in punctuation moving logic in build.py;
* Skirnismol, 21: fixed reference to prose in Reginsmol

~~~~~~~~~~~~~~~~~~~~~~~
Fafnismol (22 Apr 2011)
~~~~~~~~~~~~~~~~~~~~~~~

* Added Fafnismol chapter

~~~~~~~~~~~~~~~~~~~~~~~~~
Sigrdrifumol (1 May 2011)
~~~~~~~~~~~~~~~~~~~~~~~~~

* Added Sigrdrifumol chapter

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Brot af Sigurtharkvithu (6 May 2011)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* Voluspo, 28: added missing space between sentences;
* General introduction: marked Old Norse stanzas as 'translation' too,
  because this corresponds to their book of origin, not to contents;
* Added Brot af Sigurtharkvithu chapter

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Guthrunarkvitha I (13 May 2011)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* Added Guthrunarkvitha I chapter;
* General Introduction: fixed reference to Guthrunarkvitha

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Sigurtharkivtha en skamma (planned)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* Add Sigurtharkivtha en skamma chapter
* Vafthruthnismol, 27: removed redundant indent from the phrase
  separating two inline stanzas

~~~~~~~~~~~~~~~~~~~~~~~~
Tasks for distant future
~~~~~~~~~~~~~~~~~~~~~~~~

* Add all remaining chapters;
* Add support for different paper sizes (in particular, try to typeset a proper book);
* Try to use footnotes instead of normal text for comments;
* Probably make build script run xelatex too?
* Check all overfull hboxes (I'm leaving this check for the future, becasue I do not
  know how long the stanza names in other chapters will be).
* Proofread everything
* Find a way to disable page breaks between comments and stanzas (seems to be the issue of longtable)
* Find a way to not typeset \eddasepline if it is at the end of the page (can TeX even do that?)
* Find a way to keep line separation in stanzas even when the line is too long
  (or just tune the column widths to avoid oversized hboxes in stanzas)
* Do not break the line after ndash separating two numbers
* Refactor scripts
* Add all missing text from paperback (i.e., Acknowledgement and
  list of proper names)
* Make the vertical space inside the stanza before <stanzaprelude>
  a bit bigger than between two normal lines.
  See any <stanzaprelude> usage in Bellows book.
* Check spaces between single and double quotes and between double quotes and apostrophes
  (thin space needed?)
* Put original and translated textstanzas in comments side-by-side
  (and delete parentheses from original stanzas)
* Check that phrases like 'prose after stanza 5' are single references to prose,
  not one ref to prose and one to stanza
* Draw just <lacuna> instead of <lacuna><sep><lacuna>, unless <sep>
  is just a long space (or maybe draw some "long" lacuna)
* HHII: probably make separate style for in-prose stanza (p17, class="prosestanza"),
  so that the whole prose would be enclosed in a single block
* Add hyphenation helpers for all chapter names (TODO: can't remember why
  I mentioned this; have to find place where TeX's hyphenation algorithm fails)
  Need to add non-breakable spaces in chapter names too (like Smth~II)
* Try to use two cells separated by \nopagebreaks for stanza lines with <sep />
  (this may help to avoid uneven cell spacing)
* Probably make second-level square brackets bold
  (see how it's done in Sigrdrifumol in Gering source)
* Check the style of "Some chapter II" references throughout the Bellows' book:
  sometimes "II" are in italics (introduction to Guthrunarkvitha I),
  sometimes not.
* Sometimes when <textstanza-original> goes after <textstanza-translation> there is no need in '.' in the first one: it was put there in Bellows' book, just because it finished the sentence.
  Need to check all such places in the book and remove
  unnecessary '.'.