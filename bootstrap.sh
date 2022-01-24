#!/bin/bash

curl -OL https://github.com/flexible-address-space/flexspace/archive/refs/tags/artifact-snapshot.tar.gz
tar --skip-old-files --strip-components=1 -xv -f artifact-snapshot.tar.gz
rm artifact-snapshot.tar.gz
