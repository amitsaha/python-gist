python-gists
============

A command line GitHub gist posting application in Python. 

Usage
=====
	$ python python-gist.py --help
	Usage: python-gist.py [options]

	Options:
	-h, --help            show this help message and exit
	-d DESC, --description=DESC
        Description for the gist
	-f FILES, --files=FILES
        Comma seperated list of file(s) to post as a gist
	-p, --private         Use to post a private gist

	$ python python-gist.py 
	Loaded saved access token, I'm good to go.
	Enter your Gist contents
	***********************
	****^D  when done******
	This is a gist
	https://gist.github.com/4096470

	$ python python-gist.py -d 'Multi file gist' -f python-gist.py,README.md
	Loaded saved access token, I'm good to go.
	Uploading files..
	https://gist.github.com/4096475
	
	$ python python-gist.py -d 'Multi file gist' -f python-gist.py,README.md -p
	Loaded saved access token, I'm good to go.
	Uploading files..
	https://gist.github.com/b766c2becf1874b1665b

Todos
=====

* Code refactoring
* Make the script installable
* External editor? 

Thanks
======
Thanks to Voltagex for having the OAuth part already setup. This gave me
a very good platform to finally implement the other features.
