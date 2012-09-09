import argparse
import os
from . import Generator
import errno
import sys
import shutil

def main():
	parser = argparse.ArgumentParser(version='0.1.0', description='CodeShow turns a directory of code into a static website suitable for use in presentations.', usage='codeshow [path] [<options>]')
	parser.add_argument(metavar='PATH', dest='source_directory', default='.', nargs='?', help='path to the code project')
	parser.add_argument('-o, --output', metavar='PATH', dest='output_directory', required=False, default='output', help='output path for generated website')
	parser.add_argument('-i, --ignore', metavar='PATH', dest='ignore_paths', required=False, help='relative path to skip (can be specified multiple times)', action='append', default=[])
	parser.add_argument('-f, --force', dest='force', required=False, action='store_true', default=False, help='if the output directory already exists, delete it first')
	parser.add_argument('-s, --site44', dest='site44', action='store_true', required=False, default=False, help='generate output for Site44 (generate mimetypes.site44.txt instead of using file extensions)')

	arguments = parser.parse_args()
	try: os.mkdir(arguments.output_directory)
	except OSError, e:
		if e.errno == errno.EEXIST:
			if arguments.force:
				shutil.rmtree(arguments.output_directory)
				os.mkdir(arguments.output_directory)
			else:
				print 'ERROR: Output directory "%s" already exists. Pass -f to delete the output directory before generating.' % arguments.output_directory
				sys.exit(1)
		else:
			raise e

	source_directory = os.path.abspath(arguments.source_directory)
	output_directory = os.path.abspath(arguments.output_directory)

	Generator(
		source_directory,
		output_directory,
		# convert relative ignore paths into absolute paths, and add output directory
		map(lambda path: os.path.join(source_directory, path), arguments.ignore_paths)
		+ [output_directory],
		arguments.site44).generate()
