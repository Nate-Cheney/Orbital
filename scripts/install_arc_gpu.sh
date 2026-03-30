#########################
# Intel Arc GPU Setup   #
#########################

echo "Installing software-properties-common..."
sudo apt-get update
sudo apt-get install -y software-properties-common

echo "Adding Intel's repository for Battlemage drivers (Canonical dist)..."
sudo add-apt-repository -y ppa:kobuk-team/intel-graphics 
sudo apt-get update

echo "Updating existing drivers and installing Xe2 drivers..."
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

