#!/bin/bash

# Table 2 pt.1 - 4k 1G
./micro.sh 4096 262144

# Table 2 pt.2 - 64k 16G
./micro.sh 65536 262144

# Fig. 10
./multi.sh 4096 262144
