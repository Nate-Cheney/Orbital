#########################
# Jupyter Setup         # 
#########################

source ".venv/bin/activate"

echo "Installing Jupyter..."
python3 -m pip install --upgrade pip 
pip3 install jupyter ipykernel
python3 -m ipykernel install --user --name=venv_python --display-name="Python 3"

