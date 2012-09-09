import pygments.formatters
import jinja2
import util
import os
import re
from . import templates

class CodeShowFormatter(pygments.formatters.html.HtmlFormatter):
	def __init__(self, **options):
		pygments.formatters.html.HtmlFormatter.__init__(self, **options)
		self.raw_path = options['raw_path']
		self.use_extensions = options['use_extensions']

	def _format_lines(self, tokensource):
		for i, t in pygments.formatters.html.HtmlFormatter._format_lines(self, tokensource):
			if i == 1:
				indent_level = len(re.match('^\s*', t).group(0).replace('\t', '    '))/2
				t = t.strip()
				t = '<p class="i%d%s">%s</p>\n' % (indent_level, len(t) == 0 and ' blank' or '', t)
			yield i, t

	def wrap(self, source, outfile):
		return self._wrap_code(source)

	def _wrap_code(self, source):
		yield 0, templates['top'].render(
			name=util.truncate(self.title),
			cssfile=self.cssfile,
			raw_path=self.raw_path,
			use_extensions=self.use_extensions)
		for i, t in source: yield i, t
		yield 0, templates['bottom'].render()
