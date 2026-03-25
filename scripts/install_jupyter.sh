#########################
# Jupyter Setup         # 
#########################

# Create venv if it doesn't exist
if [ ! -d ".venv" ]; then
    python3 -m venv .venv
fi

# Activate the virtual environment
source .venv/bin/activate

# Install packages
python3 -m pip install --upgrade pip 
pip3 install jupyter ipykernel
python3 -m ipykernel install --user --name=venv_python --display-name="Python 3"

# Install required libraries
pip3 install -r .devcontainer/requirements.txt

