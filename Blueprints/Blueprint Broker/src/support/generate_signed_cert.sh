#!/bin/bash

openssl req -new -newkey rsa:2048 -days 3650 -nodes -x509 -keyout ../bp-broker/dummy_api.key -out ../bp-broker/dummy_api.crt

