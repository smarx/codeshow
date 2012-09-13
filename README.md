# CodeShow

CodeShow turns a directory of code into a static website suitable for use in presentations. It uses [pygments](http://pygments.org) for syntax highlighting. In directories that include a `readme.md` or `readme.txt`, the readme contents will be displayed under the directory listing.

Passing `--site44` generates content optimized for hosting on Site44:

1. No .html or .txt file extensions are appended to files. This makes for prettier URLs.
2. A `mimetypes.site44.txt` file is generated that enforces HTML and plain text content types for those pretty URLs.

See [codeshow.site44.com](http://codeshow.site44.com) for an example of the output, or get the code at [github.com/smarx/codeshow](https://github.com/smarx/codeshow).

## Installation

Use `pip install codeshow` to install.

## Usage

	usage: codeshow [path] [<options>]

	CodeShow turns a directory of code into a static website suitable for use in
	presentations.

	positional arguments:
	  PATH               path to the code project

	optional arguments:
	  -h, --help         show this help message and exit
	  -v, --version      show program's version number and exit
	  -o, --output PATH  output path for generated website
	  -i, --ignore PATH  relative path to skip (can be specified multiple times)
	  -f, --force        if the output directory already exists, delete it first
	  -s, --site44       generate output for Site44 (generate mimetypes.site44.txt
	                     instead of using file extensions)
