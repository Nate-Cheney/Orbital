# Orbital - Devcontainer Generator

Orbital is a lightweight, customizable web application and CLI tool that generates `Dockerfile` and `devcontainer.json` configurations. It allows you to rapidly bootstrap a Devcontainer by dynamically combining base images with modular tools and extensions.

## File Structure

*   **`build/`** - Contains declarative JSON build steps required by the base images.
*   **`data/`** - Contains images.json and modules.json which define available base OS images and available modular add ons.
*   **`scripts/`** - Shell scripts that are injected into the Docker setup process for specific modules.
*   **`compile.py`** - The core Python engine that parses the JSON files to orchestrate and output the raw Devcontainer configurations. 
*   **`app.py`** & **`templates/`** - A Flask web application that provides a graphic interface over the python backend.

## How to Use

You can run Orbital either through the Web UI or via the Command Line Interface.

### 1. Web UI (Recommended)

**Using Docker**
1. Run the server on port 5000:
   ```bash
   docker run -p 5000:5000 ghcr.io/nate-cheney/orbital:master 
   ```
2. Open `http://localhost:5000` in your browser.

**Using Docker Compose**
1. Create a `docker-compose.yaml`:
```docker-compose.yaml
services:
    orbital:
        container_name: orbital
        image: ghcr.io/nate-cheney/orbital:latest
        ports:
         - 5000:5000 
        restart: unless-stopped
```
2. Run `docker compose pull && docker compose pull -d`.
3. Open `http://localhost:5000` in your browser.

**Using Python (Virtual Environment)**
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
flask run --debug
```

### 2. Command Line Interface (CLI)
You can bypass the web app and use the backend script directly:

```bash
python3 compile.py --project-name "My App" --image "Ubuntu" --modules "Python" "Jupyter Notebook"
```
*(Running `python3 compile.py --help` will show all available options).*
