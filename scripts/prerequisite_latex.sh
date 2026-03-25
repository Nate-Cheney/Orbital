#!/bin/bash

tlmgr update --self && tlmgr update --all

apt-get update && apt-get install -y tree-sitter-cli && rm -rf /var/lib/apt/lists/*

