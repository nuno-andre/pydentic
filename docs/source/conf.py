# Configuration file for the Sphinx documentation builder.
# https://www.sphinx-doc.org/en/master/usage/configuration.html
import sphinx_automodapi

# -- Path setup --------------------------------------------------------

# Add to sys.path the absolute paths of extensions (or modules to
#   document with autodoc) that are in another directory.
import os
import sys
sys.path.insert(0, os.path.abspath('../../src'))


# -- Project information -----------------------------------------------

project = 'Pydentic'
copyright = '2021, Nuno André Novo'
author = 'Nuno André Novo'
release = '0.0.1'

# -- General configuration ---------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = ['sphinx.ext.autodoc',
              'sphinx_automodapi.automodapi']

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']
source_suffix = '.rst'

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []

# Cross-reference to Python objects marked up `like this`
default_role = 'py:obj'

# For debugging: warns about not found ref targets.
# nitpicky = True

# -- Options for HTML output -------------------------------------------

# The theme to use for HTML and HTML Help pages.
html_theme = 'alabaster'

# Paths (relative to this directory) that contain custom static files.
# They are copied after the builtin static files, so a file named
#   "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# -- ext.extlinks options ----------------------------------------------

extlinks = {'rfc': ('https://tools.ietf.org/html/rfc%s', 'rfc:')}
