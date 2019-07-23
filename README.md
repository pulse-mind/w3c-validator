# W3C Command-line Validator

Forked from https://github.com/srackham/w3c-validator

A command-line script (written in Python) for validating HTML and CSS
files and URLs using the WC3 validators. It can convert all the CSS files of a directory and subdirectories.

The `w3c-validator.py` script uses the `curl(1)` command to submit HTML files and URLs to the http://validator.w3.org/[W3C Markup
Validation Service] and CSS files and URLs to the http://jigsaw.w3.org/css-validator/[W3C CSS Validation Service]. 
The script parses and reports the JSON results returned by the validators.

NOTE: Currently the CSS validator's JSON output option is experimental
and not formally documented.

## Usage
The script command syntax is:

  python w3c-validator.py [--verbose] [--cssonly] --file_url_or_directory=FILE|URL|DIRECTORY

- The optional `--verbose` option will print information about what is
  going on internally.
- The optional `--cssonly` option will retrieve only '*.css' extension files. 
- Names with a `.css` extension are treated as CSS, all other names
  are assumed to contain HTML.
- Names starting with `http://` are assumed to be publically
  accessible URLs, all other names are assumed to be local file names.
- Any mix of one or more local files or HTTP URLs can be specified.
- If one or more files fail validation then the exit status will be 1,
  if no errors occurs the exits status will be zero.

Examples (`w3c-validator` is just a convenient symbolic link in the shell 'PATH' to the executable `w3c-validator.py` script):

```
--------------------------------------------------------------
$ w3c-validator tests/css/common.css
validating: tests/css/common.css ...
| errors: 2
|-- Ligne 316 : “compact” is not a “display” value :
|       #search_s .submit
|-- Ligne 1321 : Parse Error
|
| warnings: 36
--------------------------------------------------------------
```

## Resources
- http://validator.w3.org/docs/users.html[User's guide for the W3C Markup Validator].
- http://jigsaw.w3.org/css-validator/manual.html[CSS Validator User's Manual].


## Prerequisites
- Python.
- Curl (the `curl(1)` command must be in the shell 'PATH').
- An Internet connection.

Written and tested on ubuntu 16.04 with Python 2.7.12, should work on other Python platforms.
