#!/bin/sh

jq -s 'flatten' tests/*.json > merged-endpoints.json