# Introduction #

This document explains how to install libraries, tools and other dependencies required for development.

# Development Environment #

## Dependencies Overview ##

  * **Python 2.6**
    * **[virtualenv](http://pypi.python.org/pypi/virtualenv)**: A tool to create isolated Python environments
    * **[ipython](http://ipython.scipy.org/moin/Documentation)**: An interactive Python shell
    * **[SQLAlchemy>=2.6](http://www.sqlalchemy.org/docs/)**: An Object-Relational Mapping framework for the Data Access Layer
    * **[mod\_pywebsocket>=0.5](http://code.google.com/p/pywebsocket/)**: Utilities for a standalone Web Socket server
    * **[controlfreak>=1.1.3](http://blog.code.zauber.com.ar/2009/04/controlfreak-python-inversion-of.html)**: An Inversion of Control framework for connecting loosely coupled components
    * **[pycommons>=0.3.7](http://blog.code.zauber.com.ar/2009/04/controlfreak-python-inversion-of.html)**: Common Python utilities (indirect dependency due to controlfreak)
    * **[PyYAML>=3.09](http://pyyaml.org/wiki/PyYAMLDocumentation)**: A Python YAML parser (indirect dependency due to controlfreak)
    * **[nose>=0.11](http://somethingaboutorange.com/mrl/projects/nose/0.11.3/)**: A testing framework (only for testing)
    * **[pmock>=0.3](http://pmock.sourceforge.net/)**: Utilities for mocking objects in tests (only for testing)
  * **PostgreSQL**
    * **pgAdmin III**
  * **Memcached** ... not yet

## Setup ##

This is a step-by-step description of how to setup a development environment. You will find the commands you may run in [DevelopmentEnvironmentSetup#Platform-specific\_instructions](DevelopmentEnvironmentSetup#Platform-specific_instructions.md).

  1. Create a virtualenv for galaktia. It is highly recommended that you read the [virtualenv documentation](http://pypi.python.org/pypi/virtualenv) to understand how it works.
  1. Activate the galaktia virtualenv.
  1. Install setuptools (latest version) and ipython.
  1. Checkout galaktia source code.
  1. Go to the root galaktia source code directory.
  1. Run `galaktia` setup for development.
  1. Run `galaktia` server.
  1. Run `galaktia` client (separately).
  1. Optionally, run `galaktia` shell for playing with its components in an interactive shell.


# Platform-specific instructions #

## Linux ##

### Required packages ###

Use your package manager to install them; e.g.: `sudo apt-get install...` in Ubuntu.
  * python2.6
  * python-dev
  * python-virtualenv
  * subversion

### Commands ###

**IMPORTANT**: Replace the environment variables for your custom values:
  * `$VIRTUALENV`: path where you install virtualenvs, e.g.: `~/python-envs`
  * `$WORKSPACE`: path where you checkout projects, e.g.: `~/workspace`
  * `$USERNAME`: your username in the source code repository. Check [DevelopmentEnvironmentSetup#Source\_Code\_Management](DevelopmentEnvironmentSetup#Source_Code_Management.md) for instructions on authentication.

```
$ virtualenv -p /usr/bin/python2.6 --no-site-packages $VIRTUALENV/galaktia
$ source $VIRTUALENV/galaktia/bin/activate
$ easy_install -U setuptools ipython
$ svn checkout https://galaktia.googlecode.com/svn/trunk/ $WORKSPACE/galaktia --username $USERNAME
$ cd $WORKSPACE/galaktia/galaktia
$ python setup.py develop
$ galaktia server
$ galaktia client
$ galaktia shell
```

## Mac OS X (Leopard) ##

### Requirements ###
  * Xcode
  * Python 2.6
  * virtualenv

### Commands ###

Same as in Linux.

Additionally, it is recommended to `easy_install readline` for a better experience in the `ipython` shell.

## Windows ##

> _Oh, please! Get an operating system!_

Anyway, once you get Python 2.6 and virtualenv working on Windows (read the corresponding documentation), it should be very similar to the commands described above.

# Source Code Management #

## Source checkout ##

To check out the code (at the repository trunk) as a developer:

```
$ svn checkout https://galaktia.googlecode.com/svn/trunk/ galaktia --username PUT_YOUR_USERNAME_HERE
```

When prompted, enter your [generated Google Code password](http://code.google.com/hosting/settings).

## Tools ##

  * **Subversion**
  * **[svnmerge.py](http://www.orcaware.com/svn/wiki/Svnmerge.py)**: Script for _branch_ management


# IDEs _(OPTIONAL)_ #

One of the following is recommended:

  * **vim**
  * **Emacs**
  * **Eclipse** with **Py Dev** plug-in

In the case of _vim_, make sure to include this configuration in your `~/.vimrc` (that applies, among others, style rules for indentation, for example):
```
" vimrc file for following the coding standards specified in PEP 7 & 8.
"
" To use this file, source it in your own personal .vimrc file (``source
" <filename>``) or, if you don't have a .vimrc file, you can just symlink to it
" (``ln -s <this file> ~/.vimrc``).  All options are protected by autocmds
" (read below for an explanation of the command) so blind sourcing of this file
" is safe and will not affect your settings for non-Python or non-C files.
"
"
" All setting are protected by 'au' ('autocmd') statements.  Only files ending
" in .py or .pyw will trigger the Python settings while files ending in *.c or
" *.h will trigger the C settings.  This makes the file "safe" in terms of only
" adjusting settings for Python and C files.
"
" Only basic settings needed to enforce the style guidelines are set.
" Some suggested options are listed but commented out at the end of this file.


" Number of spaces to use for an indent.
" This will affect Ctrl-T and 'autoindent'.
" Python: 4 spaces
" C: 8 spaces (pre-existing files) or 4 spaces (new files)
au BufRead,BufNewFile *.py,*pyw set shiftwidth=4
au BufRead *.c,*.h set shiftwidth=8
au BufNewFile *.c,*.h set shiftwidth=4

" Number of spaces that a pre-existing tab is equal to.
" For the amount of space used for a new tab use shiftwidth.
" Python: 8
" C: 8
au BufRead,BufNewFile *py,*pyw set tabstop=4
au BufRead,BufNewFile *.c,*.h set tabstop=8

" Replace tabs with the equivalent number of spaces.
" Also have an autocmd for Makefiles since they require hard tabs.
" Python: yes
" C: no
" Makefile: no
au BufRead,BufNewFile *.py,*.pyw set expandtab
au BufRead,BufNewFile *.c,*.h set noexpandtab
au BufRead,BufNewFile Makefile* set noexpandtab

" Use the below highlight group when displaying bad whitespace is desired
highlight BadWhitespace ctermbg=red guibg=red

" Display tabs at the beginning of a line in Python mode as bad.
au BufRead,BufNewFile *.py,*.pyw match BadWhitespace /^\t\+/
" Make trailing whitespace be flagged as bad.
au BufRead,BufNewFile *.py,*.pyw,*.c,*.h match BadWhitespace /\s\+$/

" Wrap text after a certain number of characters
" Python: 79 
" C: 79
au BufRead,BufNewFile *.py,*.pyw,*.c,*.h set textwidth=79

" Turn off settings in 'formatoptions' relating to comment formatting.
" - c : do not automatically insert the comment leader when wrapping based on
"    'textwidth'
" - o : do not insert the comment leader when using 'o' or 'O' from command mode
" - r : do not insert the comment leader when hitting <Enter> in insert mode
" Python: not needed
" C: prevents insertion of '*' at the beginning of every line in a comment
au BufRead,BufNewFile *.c,*.h set formatoptions-=c formatoptions-=o formatoptions-=r

" Use UNIX (\n) line endings.
" Only used for new files so as to not force existing files to change their
" line endings.
" Python: yes
" C: yes
au BufNewFile *.py,*.pyw,*.c,*.h set fileformat=unix

```