from flask import Flask, render_template, request, jsonify
import json
import compile

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/options", methods=["GET"])
def get_options():
    try:
        with open("images.json", "r") as file:
            images_data = json.load(file)
        
        with open("modules.json", "r") as file:
            modules_data = json.load(file)
        
        options = {
            "images": [img.get("name") for img in images_data.get("images", [])],
            "modules": [mod.get("name") for mod in modules_data.get("modules", []) if mod.get("name") != "Default"]
        }
        return jsonify(options)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/generate", methods=["POST"])
def generate():
    data = request.json
    
    project_name = data.get("project_name", "Test Project")
    selected_name = data.get("selected_name")
    selected_modules = data.get("selected_modules", [])
    
    if not selected_name:
        return jsonify({"error": "An image name must be provided."}), 400
        
    try:
        dockerfile_string, devcontainer_string = compile.main(
            project_name=project_name, 
            selected_name=selected_name, 
            selected_modules=selected_modules
        )
        
        # Inject the project name correctly if needed, compile.py devcontainer output hardcodes "Project Name"
        # We can do a simple replace since it was returned as string
        devcontainer_dict = json.loads(devcontainer_string)
        devcontainer_dict["name"] = project_name
        devcontainer_string = json.dumps(devcontainer_dict, indent=4)
        
        return jsonify({
            "dockerfile": dockerfile_string,
            "devcontainer": devcontainer_string
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)