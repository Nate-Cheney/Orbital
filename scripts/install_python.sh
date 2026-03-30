#########################
# Python Setup          #
#########################

echo "Installing Python via apt..."
sudo apt-get update
sudo apt-get install -y  python3 \
    python3-dev \
    python3-pip \
    python3-venv
sudo rm -rf /var/lib/apt/lists/*

if [ ! -d ".venv/" ]; then 
    echo "Creating Python virtual environment..."
    python3 -m venv .venv/
fi

source ".venv/bin/activate"
echo "Installing packages..."
python3 -m pip install --upgrade pip 
pip3 install -r .devcontainer/requirements.txt

