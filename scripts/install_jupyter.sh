#########################
# Jupyter Setup         # 
#########################

echo "Installing Jupyter..."
.venv/bin/python3 -m pip install --upgrade pip
.venv/bin/python3 -m pip install jupyter ipykernel
.venv/bin/python3 -m ipykernel install --user --name=venv_python --display-name="Python 3"

