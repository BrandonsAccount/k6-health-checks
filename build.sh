#!/bin/bash

#!/bin/bash
jq -s 'flatten' tests/*.json > merged-endpoints.json