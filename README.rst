PythonBrasil[8] website - An Amazing Project
=======================

This is the source-code of PythonBrasil[8]'s website. The 8th edition of the conference will happen during November 2012, in Rio de Janeiro, Brazil.

The official website is under-construction and can be seen at:
http://www.pythonbrasil.org.br

Since its begining, this website has been developed as open-source by volunteers, using mainly:

- Python
- Django

One of our major concerns was reusability of code. Due to this, we decided to develop and improve a conference Django app, called Mittun:
https://github.com/flaviamissi/mittun

The aim of this app is to provide features useful to any conference website. One of the qualities of Mittun, when compared to other similar projects, is its test coverage. Whenever possible, TDD (Test Driven Development) was used.


Install
-------

From the command line: ::

    $ make deps


Running tests
-------------
This is an amazing project which helps you lot
This project has both server side and client side tests. To run the test suites do: ::

    make test
    make jasmine

Contribute
----------

We need your help! Please, report bugs and share patches, based on our `Issues <https://github.com/PythonBrasil8/pythonbrasil8/issues>`_.

Don't worry if you can't assign an issue to yourself, simply comment that you'll be working on it.

Please, if we don't do it, add or remind us of adding your name to the contributors.txt. Thank you!

Build status
------------
.. image:: https://secure.travis-ci.org/pythonbrasil/pythonbrasil8.png?branch=master
   :target: http://travis-ci.org/pythonbrasil/pythonbrasil8/
