import json


def get_selected_image(selected_name: str) -> tuple(str, list(str)):
    with open("images.json", "r") as file:
        images = json.load(file)
    
    for image in images["images"]:
        if image.get("name") == selected_name:
            selected_image = image.get("image")
            image_scripts = image.get("scripts")

    return (selected_image, image_scripts)


def get_selected_modules(selected_modules: list):
    selected_modules.append("Default")  # Ensure default attributes are appended
    loaded_modules = {
        "devcontainer": {
            "runArgs": [],
            "features": {},
            "extensions": [],
            "settings": {}
        },
        "scripts": [],
        "environment": []
    }

    with open("modules.json") as file:
        modules = json.load(file)

    for module in modules["modules"]:
        if module.get("name") in selected_modules:
            # Extract the devcontainer object from the current module
            dev_config = module.get("devcontainer", {})
            
            # Extend lists (runArgs, extensions, and scripts)
            loaded_modules["devcontainer"]["runArgs"].extend(dev_config.get("runArgs", []))
            loaded_modules["devcontainer"]["extensions"].extend(dev_config.get("extensions", []))
            loaded_modules["scripts"].extend(module.get("scripts", []))
            
            # Update dictionaries (features and settings)
            loaded_modules["devcontainer"]["features"].update(dev_config.get("features", {}))
            loaded_modules["devcontainer"]["settings"].update(dev_config.get("settings", {}))
            loaded_modules["devcontainer"]["environment"].update(dev_config.get("environment", {}))

    # Deduplicate items
    loaded_modules["devcontainer"]["runArgs"] = list(dict.fromkeys(loaded_modules["devcontainer"]["runArgs"]))
    loaded_modules["devcontainer"]["extensions"] = list(dict.fromkeys(loaded_modules["devcontainer"]["extensions"]))
    loaded_modules["scripts"] = list(dict.fromkeys(loaded_modules["scripts"]))
    loaded_modules["environment"] = list(dict.fromkeys(loaded_modules["environment"]))
    
    return loaded_modules


def main(selected_name: str, selected_modules: list(str)):
    PROJECT_NAME = "test"
    selected_image, image_scripts = get_selected_image(selected_name)
    selected_modules = get_selected_modules(selected_modules)

    copy_script_string = ""
    run_script_string = ""

    for script in image_scripts:
        copy_script_string += f"COPY scripts/{script} .\n"
        run_script_string += f"RUN ./scripts/{script}\n"

    dockerfile=f"""FROM {selected_image}

{copy_script_string}
{run_script_string}
# Passwordless sudo
RUN echo '%sudo ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers
"""
    print(f"DOCKERFILE:\n{dockerfile}END OF DOCKERFILE\n")


    devcontainer=f"""{{
    "name": "{PROJECT_NAME}",
    "build": {{
        "context": "..",
        "dockerfile": "Dockerfile"
    }},
    {selected_modules}
}}\n"""
    print(f"DEVCONTAINER.JSON:\n{devcontainer} \nEND OF DEVCONTAINER.JSON")


if __name__ == "__main__":
    #selected_image, image_scripts = get_selected_image("Ubuntu")
    #selected_modules = get_selected_modules(["Intel Arc GPU", "Jupyter Notebook"])

    main(selected_name="Ubuntu", selected_modules=["Intel Arc GPU", "Python", "Jupyter Notebook"])
