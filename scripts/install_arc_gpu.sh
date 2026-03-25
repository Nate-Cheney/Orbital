#!/bin/bash

# Add Intel's official Canonical PPA for Ubuntu 24.04 Battlemage drivers
add-apt-repository -y ppa:kobuk-team/intel-graphics && \
    apt-get update

# Upgrade underlying DRM libraries and install the modern Xe2 packages
apt-get upgrade -y && \
    apt-get install -y \
    intel-opencl-icd \
    libze-intel-gpu1 \
    libze1 \
    libze-dev \
    intel-ocloc \
    intel-media-va-driver-non-free \
    libmfx-gen1 \
    libvpl2 \
    && rm -rf /var/lib/apt/lists/*

