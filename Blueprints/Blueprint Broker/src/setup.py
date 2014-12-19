
#
# python setup.py sdist
# python setup.py bdist_dumb
# python setup.py bdist_rpm
#

from setuptools import setup, find_packages

setup(
	name = "bpbroker",
	version = "0.1",
	packages = find_packages("."),

	install_requires = ['argparse','requests','premailer'],

	entry_points = {
		'console_scripts': [
			'bpbroker  = bpbroker.cli:BPBroker',
			'bpclient  = bpclient.cli:BPClient',
			'bpmailer  = bpclient.cli:BPMailer',
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

