#########################
# Jupyter Setup         # 
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

# Install packages
echo "Installing Jupyter..."
python3 -m pip install --upgrade pip 
pip3 install jupyter ipykernel
python3 -m ipykernel install --user --name=venv_python --display-name="Python 3"

# Install required libraries
echo "Installing packages..."
pip3 install -r .devcontainer/requirements.txt

