from setuptools import setup

setup(
	name = 'CodeShow',
	version = '0.1.0',
	url = 'http://codeshow.site44.com',
	license = open('LICENSE').read(),
	author = 'Steve Marx',
	author_email = 'smarx@smarx.com',
	description = 'CodeShow turns a directory of code into a static website suitable for use in presentations.',
	long_description = open('README.md').read(),
	packages = ['codeshow'],
	entry_points = { 'console_scripts': ['codeshow = codeshow.cmdline:main']},
	install_requires = map(str.rstrip, open('requirements.txt').readlines()),
	package_data = {'templates': ['templates/*']},
	include_package_data = True
)
