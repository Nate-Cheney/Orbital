#########################
# Intel Arc GPU Setup   #
#########################

sudo apt-get update
sudo apt-get install -y software-properties-common

# Add Intel's official Canonical PPA for Ubuntu 24.04 Battlemage drivers
sudo add-apt-repository -y ppa:kobuk-team/intel-graphics 
sudo apt-get update

# Upgrade underlying DRM libraries and install the modern Xe2 packages
sudo apt-get upgrade -y
sudo apt-get install -y \
    intel-opencl-icd \
    libze-intel-gpu1 \
    libze1 \
    libze-dev \
    intel-ocloc \
    intel-media-va-driver-non-free \
    libmfx-gen1 \
    libvpl2
sudo rm -rf /var/lib/apt/lists/*

