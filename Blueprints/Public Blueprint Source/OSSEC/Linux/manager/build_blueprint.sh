#!/bin/bash

cp ../../noarch/* .

zip ../../Blueprints_Completed_Packages/Linux_ossec_manager.zip  \
	install_ossec_manager.sh \
	package.manifest \
	preloaded-vars.conf \
	ossec.*

rm ossec.*

