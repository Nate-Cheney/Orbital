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
        "scripts": [

        ]
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

    # Deduplicate items
    loaded_modules["devcontainer"]["runArgs"] = list(dict.fromkeys(loaded_modules["devcontainer"]["runArgs"]))
    loaded_modules["devcontainer"]["extensions"] = list(dict.fromkeys(loaded_modules["devcontainer"]["extensions"]))
    loaded_modules["scripts"] = list(dict.fromkeys(loaded_modules["scripts"]))
    
    return loaded_modules


if __name__ == "__main__":
    selected_image, image_scripts = get_selected_image("Ubuntu")

    # Demo output
    print(selected_image)
    for script in image_scripts:
        print(script)

    selected_modules = ["Intel Arc GPU", "Jupyter Notebook"]  # Test input
    print(get_selected_modules(selected_modules))

