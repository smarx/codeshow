import pygments.lexers
import pygments.formatters.html
import pygments.styles.monokai
import os
import jinja2
import errno
import util
import markdown

# need to define templates before importing format (which depends on them)
templates = {}
templates_dir = os.path.join(os.path.dirname(__file__), 'templates')
for name in os.listdir(templates_dir):
	with file(os.path.join(templates_dir, name)) as f:
		templates[name] = jinja2.Template(f.read())

import format

class Generator:
	def __init__(self, source_directory, output_directory, ignore_paths, site44, custom_types):
		self.source_directory = source_directory
		self.output_directory = output_directory
		self.ignore_paths = ignore_paths
		self.site44 = site44
		self.use_extensions = not site44
		self.custom_types = custom_types

	def generate(self):
		if self.site44:
			with file(os.path.join(self.output_directory, 'mimetypes.site44.txt'), 'wt') as f:
				f.write('/raw/**/* text/plain\n/file/**/* text/html\n')

		for d in ['tree', 'file', 'raw']: os.mkdir(os.path.join(self.output_directory, d))

		self.css_file = os.path.join(self.output_directory, 'styles.css')
		with file(self.css_file, 'wt') as f:
			f.write(templates['css'].render(pygments_styles = pygments.formatters.html.HtmlFormatter(style=pygments.styles.monokai.MonokaiStyle).get_style_defs('.highlight')))

		for dirpath, dirnames, filenames in os.walk(self.source_directory):
			# weed out ignored paths
			dirnames[:] = filter(lambda dirname: os.path.abspath(os.path.join(dirpath, dirname)) not in self.ignore_paths and not dirname.startswith('.'), dirnames)

			reldir = os.path.relpath(dirpath, self.source_directory)

			if reldir != '.': os.mkdir(os.path.join(self.output_directory, 'tree', reldir))
			for d in ['file', 'raw']:
				try: os.mkdir(os.path.join(self.output_directory, d, reldir))
				except OSError, e:
					if e.errno != errno.EEXIST:
						raise e

			included_files = []
			for filename in filenames:
				file_path = os.path.join(dirpath, filename)
				print 'Processing %s' % file_path
				if util.is_binary(file_path): continue
				included_files.append(filename)
				self.generate_file(file_path)
			self.generate_index(dirpath, dirnames, filenames, included_files)

	def generate_file(self, source_file):
		relpath = os.path.relpath(source_file, self.source_directory)
		output_file = os.path.join(self.output_directory, 'file', relpath)
		output_raw = os.path.join(self.output_directory, 'raw', relpath)

		html_extension = self.use_extensions and '.html' or ''
		raw_extension = self.use_extensions and '.txt' or ''

		relcss = os.path.relpath(self.css_file, os.path.dirname(output_file)).replace('\\', '/')

		formatter = format.CodeShowFormatter(encoding='utf-8',
			style=pygments.styles.monokai.MonokaiStyle,
			cssfile=relcss,
			noclobber_cssfile=True,
			title=relpath.replace('\\', '/'),
			raw_path=os.path.relpath(output_raw, os.path.dirname(output_file)).replace('\\', '/')+raw_extension,
			use_extensions=self.use_extensions)

		name_for_lexer = source_file
		extension = os.path.splitext(source_file)[1].lstrip('.').lower()
		if extension in self.custom_types: name_for_lexer = '.' + self.custom_types[extension]
		try: lexer = pygments.lexers.get_lexer_for_filename(name_for_lexer)
		except: lexer = pygments.lexers.TextLexer()

		with file(source_file) as infile: code = infile.read().decode('utf-8-sig')

		with file(output_file+html_extension, 'wt') as outfile:
			pygments.highlight(code, lexer, formatter, outfile)

		with file(output_raw+raw_extension, 'wt') as outfile:
			outfile.write(code.encode('utf-8'))

	def generate_index(self, dirpath, dirnames, filenames, included_files):
		reldir = os.path.relpath(dirpath, self.source_directory)

		if reldir == '.':
			index_path = os.path.join(self.output_directory, 'index.html')
		else:
			index_path = os.path.join(self.output_directory, 'tree', reldir + '.html')

		readme = None
		is_markdown = False
		if os.path.isfile(os.path.join(dirpath, 'readme.md')):
			is_markdown = True
			with file(os.path.join(dirpath, 'readme.md')) as f:
				readme = markdown.markdown(f.read())
		else:
			filename = None
			for name in ['readme', 'readme.txt']:
				if os.path.isfile(os.path.join(dirpath, name)):
					filename = name
			if filename is not None:
				with file(os.path.join(dirpath, filename)) as f:
					formatter = format.CodeShowFormatter(encoding='utf-8', style=pygments.styles.monokai.MonokaiStyle, nowrap=True)
					readme = pygments.highlight(f.read().decode('utf-8-sig'), pygments.lexers.TextLexer(), formatter)

		with file(index_path, 'wt') as f:
			f.write(templates['directory'].render(
				reldir = reldir != '.' and reldir.replace('\\', '/') + '/' or '',
				relroot = os.path.relpath(self.output_directory, os.path.dirname(index_path)).replace('\\', '/'),
				relcss = os.path.relpath(self.css_file, os.path.dirname(index_path)).replace('\\', '/'),
				directories = [(name, not os.path.islink(os.path.join(dirpath, name))) for name in dirnames],
				files = [(name, name in included_files) for name in filenames],
				readme = readme,
				is_markdown = is_markdown,
				use_extensions = self.use_extensions
			))

def generate(source_directory, output_directory, ignore_paths, site44):
	Generator(source_directory, output_directory, ignore_paths, site44).generate()
