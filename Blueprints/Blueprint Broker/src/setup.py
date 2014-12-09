
#
# python setup.py sdist
# python setup.py bdist_dumb
# python setup.py bdist_rpm
#

from setuptools import setup, find_packages

setup(
	name = "bp-broker",
	version = "0.1",
	packages = find_packages("."),

	install_requires = ['argparse','requests'],

	entry_points = {
		'console_scripts': [
			#'clc  = clc.cli:main',
		],
	},


	# metadata for upload to PyPI
	author = "Keith Resar",
	author_email = "Keith.Resar@CenturyLinkCloud.com",
	description = "CenturyLink Cloud Blueprint Broker Service",
	keywords = "CenturyLink Cloud Blueprint Broker",
	url = "https://github.com/CenturyLinkCloud/",

	# could also include long_description, download_url, classifiers, etc.
)

