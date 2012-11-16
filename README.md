python-gists
============

A command line python gist-posting app. Very much a work in progress

Usage
=====

  $ python python-gist.py --help
  Usage: python-gist.py [options]

  Options:
   -h, --help            show this help message and exit
   -f FILE, --type=FILE  File to post as a Gist

  $ python python-gist.py  -f python-gist.py 
  Loaded saved access token, I'm good to go.
  https://gist.github.com/08f1252d14fb8d3bdcd4
  $ python python-gist.py
  Loaded saved access token, I'm good to go.
  foobar
  https://gist.github.com/98ef5cc3e341ff59def8

Todos
=====

* Code refactoring
* Make the script installable
* Multiple file support
* Document?
 