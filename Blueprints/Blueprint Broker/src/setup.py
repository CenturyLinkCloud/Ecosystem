

from setuptools import setup, find_packages

setup(
	name = "bpbroker",
	version = "0.21",
	packages = find_packages("."),

	package_data = {
		"bpbroker": ["dummy_api.crt","dummy_api.key"],
	},

	install_requires = ['argparse','requests','premailer'],

	entry_points = {
		'console_scripts': [
			'bpbroker  = bpbroker.cli:BPBroker',
			'bpclient  = bpclient.cli:BPClient',
			'bpmailer  = bpmailer.cli:BPMailer',
		],
	},


	# metadata for upload to PyPI
	author = "Keith Resar",
	author_email = "Keith.Resar@CenturyLinkCloud.com",
	description = "CenturyLink Cloud Blueprint Broker Service Tools",
	keywords = "CenturyLink Cloud Blueprint Broker",
	url = "https://github.com/CenturyLinkCloud/Ecosystem/tree/master/Blueprints/Blueprint%20Broker",

	# could also include long_description, download_url, classifiers, etc.
)

