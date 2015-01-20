#!/bin/bash

openssl req -new -newkey rsa:2048 -days 3650 -nodes -x509 -keyout ../bpbroker/dummy_api.key -out ../bpbroker/dummy_api.crt

