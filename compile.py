import json


def get_selected_modules(selected_modules: list[str]) -> dict:
    if "Default" not in selected_modules:
        selected_modules.append("Default")  # Ensure default attributes are applied 
    loaded_modules = {
        "devcontainer": {
            "runArgs": [],
            "mounts": [],
            "postCreateCommand": "",
            "postStartCommand": "",
            "features": {},
            "extensions": [],
            "settings": {}
        },
        "scripts": [],
        "environment": []
    }

    postCreateCommands = [] 
    postStartCommands = []

    with open("modules.json") as file:
        modules = json.load(file)

    for module in modules["modules"]:
        if module.get("name") in selected_modules:
            # Extract the devcontainer object from the current module
            dev_config = module.get("devcontainer", {})
          
            # Extract the post commands to a list 
            createCmd = dev_config.get("postCreateCommand")
            if createCmd:
                postCreateCommands.append(createCmd)
            startCmd = dev_config.get("postStartCommand")
            if startCmd:
                postStartCommands.append(startCmd)

            # Extend lists 
            loaded_modules["devcontainer"]["runArgs"].extend(dev_config.get("runArgs", []))
            loaded_modules["devcontainer"]["extensions"].extend(dev_config.get("extensions", []))
            loaded_modules["devcontainer"]["mounts"].extend(dev_config.get("mounts", []))
            loaded_modules["scripts"].extend(module.get("scripts", []))
            loaded_modules["environment"].extend(module.get("environment", []))
            
            # Update dictionaries 
            loaded_modules["devcontainer"]["features"].update(dev_config.get("features", {}))
            loaded_modules["devcontainer"]["settings"].update(dev_config.get("settings", {}))

    # Deduplicate items
    loaded_modules["devcontainer"]["runArgs"] = list(dict.fromkeys(loaded_modules["devcontainer"]["runArgs"]))
    loaded_modules["devcontainer"]["extensions"] = list(dict.fromkeys(loaded_modules["devcontainer"]["extensions"]))
    loaded_modules["devcontainer"]["mounts"] = list(dict.fromkeys(loaded_modules["devcontainer"]["mounts"]))
    loaded_modules["scripts"] = list(dict.fromkeys(loaded_modules["scripts"]))
    loaded_modules["environment"] = list(dict.fromkeys(loaded_modules["environment"]))
    
    # Join command lists
    loaded_modules["devcontainer"]["postCreateCommand"] = " && ".join(postCreateCommands)
    loaded_modules["devcontainer"]["postStartCommand"] = " && ".join(postStartCommands)

    return loaded_modules


def get_selected_image(selected_name: str) -> tuple[str, list[str]]:
    with open("images.json", "r") as file:
        images = json.load(file)
    
    selected_image = ""
    image_scripts = []

    for image in images["images"]:
        if image.get("name") == selected_name:
            selected_image = image.get("image", "")
            build_prerequisites = image.get("build", [])
            break

    return (selected_image, build_prerequisites)


def get_build_commands(build_prerequisites: list(str)) -> str:
    build_commands = []

    for prereq in build_prerequisites:
        with open(f"build/{prereq}") as file:
            prereq_contents = json.load(file)
        build_commands.extend(prereq_contents.get("build_commands", []))
   
    return "\n".join(build_commands)



def concat_dockerfile(selected_image: str, selected_modules_data: dict, build_commands: str) -> str:
    environment_string = ""
    for var in selected_modules_data["environment"]:
        environment_string += f"{var}\n"

    dockerfile_string = f"""FROM {selected_image}

{build_commands}

# Passwordless sudo
RUN echo '%sudo ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers

{environment_string}
""".rstrip()

    return dockerfile_string


def concat_devcontainer(selected_modules_data: dict) -> str:
    devcontainer_dict = {
        "name": "Project Name",
        "build": {
            "context": "..",
            "dockerfile": "Dockerfile"
        },
        "mounts": selected_modules_data["devcontainer"].get("mounts", []),
        "postCreateCommand": selected_modules_data["devcontainer"].get("postCreateCommand", ""),
        "postStartCommand": selected_modules_data["devcontainer"].get("postStartCommand", ""),
        "runArgs": selected_modules_data["devcontainer"].get("runArgs", []),
        "features": selected_modules_data["devcontainer"].get("features", {}),
        
        "customizations": {
            "vscode": {
                "settings": selected_modules_data["devcontainer"].get("settings", {}),
                "extensions": selected_modules_data["devcontainer"].get("extensions", [])
            }
        }
    }

    return json.dumps(devcontainer_dict, indent=4)


def main(project_name: str, selected_name: str, selected_modules: list):
    selected_image, build_prerequisites = get_selected_image(selected_name)
    selected_modules_data = get_selected_modules(selected_modules)
    
    build_commands = get_build_commands(build_prerequisites) 
    
    dockerfile_string = concat_dockerfile(selected_image, selected_modules_data, build_commands)
    devcontainer_string = concat_devcontainer(selected_modules_data)
    
    return (dockerfile_string, devcontainer_string)


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Generate Devcontainer Configurations")
    
    parser.add_argument("--project-name", "-p", default="My Devcontainer", help="Name of the project")
    parser.add_argument("--image", "-i", default="Ubuntu", help="Selected image name")
    parser.add_argument("--modules", "-m", nargs="+", default=["SSH Agent", "CLI Dev Apps"], help="List of selected modules")
    
    args = parser.parse_args()
    
    dockerfile_string, devcontainer_string = main(project_name=args.project_name, selected_name=args.image, selected_modules=args.modules)

    print(dockerfile_string)
    print(devcontainer_string)
