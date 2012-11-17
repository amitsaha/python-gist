#!/usr/bin/env python
import atexit
import configpaths
import ConfigParser
import getpass
import sys
import optparse


try:
	import requests
except ImportError:
	print "Please pip install requests (and probably requests_oauth2)"
	sys.exit(1)
try:
	from requests_oauth2 import OAuth2
except ImportError:
	print "Please pip install requests_oauth2"
	sys.exit(1)

import json

from github_auth import GitHubAuth

class Gist(object):
	"""
	Methods for working with GitHub Gists
	"""
	OAUTH_CONFIG_FILENAME = configpaths.get_config_path('python-gist','oauth.cfg')
	
	def choose_authmethod(self):
		choice = None
		try:
			choice = raw_input('Please select an authorisation method.\r\n \t 1. Open a web browser, cut and paste the access token.\r\n \t2. Use your GitHub username and password to get a token automagically.\r\n \t(Default is 2): ')
		except EOFError:
			pass

		choice = choice.strip()

		if choice == '2' or not choice:
			self.authorise_password() 
			return
		if choice == '1':
			self.authorise_web()
			return
		else: self.choose_authmethod()

	def __init__(self):
		"""
		Read and set up config, set up authentication
		"""
		atexit.register(self.cleanup)

		self.config = ConfigParser.RawConfigParser()
		self.config.read([self.OAUTH_CONFIG_FILENAME])
		self.config.filehandle = open(self.OAUTH_CONFIG_FILENAME, 'a')
		
		if not self.config.has_section('Credentials'):
			self.config.add_section('Credentials')

		self.client_token = self.config.get_quiet('Credentials', 'client_token')
		self.client_id = self.config.get_quiet('Credentials', 'client_id')
		self.client_secret = self.config.get_quiet('Credentials', 'client_secret')

		self.auth = GitHubAuth(app_name="python-gist", app_url="http://github.com/amitsaha/python-gist", \
					       client_id=self.client_id, client_secret=self.client_secret)

		if (self.client_token is None or self.client_id is None) and sys.stdin.isatty():
			self.choose_authmethod()

		elif not sys.stdin.isatty() and self.client_id is None:
			# In case a pipe is trying to write to us
			print "Sorry, can't accept anything on stdin until I have some GitHub credentials to work with"
			sys.exit(1)

		else:
			print "Loaded saved access token, I'm good to go." 
	
	def authorise_web(self):
		"""
		Authorise this script via web browser
		"""
		return self.auth.authorise_web(redir=self.redir_url, scopes="gist")

	def authorise_password(self):
		"""
		Authorise this script via GitHub username and password
		"""
		username = raw_input("Please enter your username: ")
		password = getpass.getpass("Please enter your password: ")
		
		try:
			token = self.auth.authorise_password('gist', username, password)
			self.client_token = token
			print "Saved your token, start this script again to post gists"
			sys.exit(0)
		except Exception as ex:
			print ex.message
			print
			self.choose_authmethod()

	def post_gist(self, description, public, gist_files, content):
		"""
		Post a gist, either single text string or a dictionary of files in the form of
		{"filename.ext": {"content": "some text"}}

		:param description: Gist description
		:type: str.
		
		:param public: Post a public or private Gist 
		:type: bool.
		
		:param gist_files: dictionary of files for Gist
		:type: dict.
		
		:param content: string content for Gist
		:type: str.
		"""
		if content is not None:
			files = {"gist.txt": {"content": content}}
		elif gist_files is not None: 
			files = gist_files 
		else:
			raise("Either content or gist_files must be set")
		payload = {
			"description": description,
			"public": public,
			"files": files,
			}
		response = self.auth.get_session(self.client_token). \
		    post("https://api.github.com/gists", data=json.dumps(payload))
		if response.ok:
			return response.json['html_url']
		else: 
			print "Error " + response.text
			return

	def cleanup(self):
		"""
		Cleanup, set config and flush before exisiting
		"""
		#don't write the config file if we don't have enough data or we don't need to
		#todo, handle updates
		if (self.client_token and not self.config.get_quiet('Credentials', 'client_token')): 
			self.config.set('Credentials', 'Client_Token', self.client_token)	
			if (self.client_id):
				self.config.set('Credentials', 'Client_ID', self.client_id)
			if (self.client_secret):
				self.config.set('Credentials', 'Client_Secret', self.client_secret)
		
			self.config.write(self.config.filehandle)			
			self.config.filehandle.flush()
			self.config.filehandle.close()
		
if __name__ == "__main__":
	def get_quiet(self, section, value):
		if self.has_option(section, value):
			return self.get(section, value)
		return None
	ConfigParser.RawConfigParser.get_quiet = get_quiet
	


# setup options
parser = optparse.OptionParser()
parser.add_option('-d', '--description',help='Description for the gist',dest='desc')
parser.add_option('-f', '--files', help='Comma seperated list of file(s) to post as a gist', dest='files')
parser.add_option('-p', '--private',help='Use to post a private gist', action='store_true',dest='private')


#parse
(opts, args) = parser.parse_args()

#check for authentication
gist=Gist()

#check the options
if opts.__dict__['desc'] is not None:
	description=opts.__dict__['desc']
else:
	description = 'A Gist'

if opts.__dict__['private'] is not None:
	public = False
else:
	public = True

gist_files=None
if opts.__dict__['files']:
	content=None
	gist_files={}
	for fname in opts.__dict__['files'].split(','):
		with open(fname) as f:
			gist_files[fname]={'content':f.read()}

	print 'Uploading files..'

else:
	print 'Enter your Gist contents'
	print '***********************'
	print '****^D  when done******'
	content=sys.stdin.readlines()

# Upload gist
print gist.post_gist(description, public, gist_files, content)
