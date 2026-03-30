import json


def extract_selected_module_data(selected_modules: list[str]) -> dict:
    if "Default" not in selected_modules:
        selected_modules.append("Default")  # Ensure default attributes are applied 
    
    # Initialize variables
    loaded_module_data = {
        "devcontainer": {
            "runArgs": [],
            "mounts": [],
            "postCreateCommand": "",
            "postStartCommand": "",
            "features": {},
            "extensions": [],
            "settings": {}
        },
        "environment": [],
        "module_dependencies": [],
        "scripts": []
    }
    postCreateCommands = [] 
    postStartCommands = []

    with open("data/modules.json") as file:
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
            loaded_module_data["devcontainer"]["runArgs"].extend(dev_config.get("runArgs", []))
            loaded_module_data["devcontainer"]["extensions"].extend(dev_config.get("extensions", []))
            loaded_module_data["devcontainer"]["mounts"].extend(dev_config.get("mounts", []))
            loaded_module_data["environment"].extend(module.get("environment", []))
            loaded_module_data["module_dependencies"].extend(module.get("module_dependencies", []))
            loaded_module_data["scripts"].extend(module.get("scripts", []))
            
            # Update dictionaries 
            loaded_module_data["devcontainer"]["features"].update(dev_config.get("features", {}))
            loaded_module_data["devcontainer"]["settings"].update(dev_config.get("settings", {}))

    # Deduplicate items
    loaded_module_data["devcontainer"]["runArgs"] = list(dict.fromkeys(loaded_module_data["devcontainer"]["runArgs"]))
    loaded_module_data["devcontainer"]["extensions"] = list(dict.fromkeys(loaded_module_data["devcontainer"]["extensions"]))
    loaded_module_data["devcontainer"]["mounts"] = list(dict.fromkeys(loaded_module_data["devcontainer"]["mounts"]))
    loaded_module_data["environment"] = list(dict.fromkeys(loaded_module_data["environment"]))
    loaded_module_data["module_dependencies"] = list(dict.fromkeys(loaded_module_data["module_dependencies"]))
    loaded_module_data["scripts"] = list(dict.fromkeys(loaded_module_data["scripts"]))

    # Join command lists
    loaded_module_data["devcontainer"]["postCreateCommand"] = " && ".join(postCreateCommands)
    loaded_module_data["devcontainer"]["postStartCommand"] = " && ".join(postStartCommands)

    return loaded_module_data


def extract_selected_image_data(selected_name: str) -> tuple[str, str, list[str]]:
    with open("data/images.json", "r") as file:
        images = json.load(file)
    
    for image in images["images"]:
        if image.get("name") == selected_name:
            selected_image = image.get("image", "")
            remote_user = image.get("remoteUser", "") 
            build_prerequisites = image.get("build", [])
            break

    return (selected_image, remote_user, build_prerequisites)


def get_build_commands(build_prerequisites: list[str]) -> str:
    build_commands = []

    for prereq in build_prerequisites:
        with open(f"build/{prereq}") as file:
            prereq_contents = json.load(file)
        build_commands.extend(prereq_contents.get("build_commands", []))
   
    return "\n".join(build_commands)


def get_setup_scripts(selected_module_data: dict) -> list[str]:
    setup_scripts = []

    with open("data/modules.json") as file:
        data = json.load(file)
        scripts_map = {m["name"]: m["scripts"] for m in data["modules"]}

    for dependency in selected_module_data.get("module_dependencies", []):
        # Get the list of scripts for this dependency name
        dep_scripts = scripts_map.get(dependency, [])
        
        for script in dep_scripts:
            # Avoid duplicates from other dependencies or the current module
            if script not in setup_scripts:
                setup_scripts.append(script)

    # Add the selected module's own scripts at the end
    for script in selected_module_data["scripts"]:
        if script not in setup_scripts:
            setup_scripts.append(script)

    return setup_scripts


def concat_dockerfile(selected_image: str, selected_module_data: dict, build_commands: str) -> str:
    environment_string = ""
    for var in selected_module_data["environment"]:
        environment_string += f"ENV {var}\n"

    dockerfile_string = f"""FROM {selected_image}

{build_commands}

# Passwordless sudo
RUN echo '%sudo ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers

{environment_string}
""".rstrip()

    return dockerfile_string


def concat_devcontainer(selected_module_data: dict, remote_user: str) -> str:
    devcontainer_dict = {
        "name": "Project Name",
        "build": {
            "context": "..",
            "dockerfile": "Dockerfile"
        },
        "remoteUser": remote_user,
        "mounts": selected_module_data["devcontainer"].get("mounts", []),
        "postCreateCommand": selected_module_data["devcontainer"].get("postCreateCommand", ""),
        "postStartCommand": selected_module_data["devcontainer"].get("postStartCommand", ""),
        "runArgs": selected_module_data["devcontainer"].get("runArgs", []),
        "features": selected_module_data["devcontainer"].get("features", {}),
        
        "customizations": {
            "vscode": {
                "settings": selected_module_data["devcontainer"].get("settings", {}),
                "extensions": selected_module_data["devcontainer"].get("extensions", [])
            }
        }
    }

    return json.dumps(devcontainer_dict, indent=4)


def concat_setup_script(setup_scripts) -> str:
    setup_script_string = "#!/bin/bash\nset -e\n\n"

    for script in setup_scripts:
    # for script in selected_module_data["scripts"]:
        with open(f"scripts/{script}", "r") as file:
            script_contents = file.read()
        
        setup_script_string += f"{script_contents}\n"
    
    return setup_script_string.rstrip()


def main(project_name: str, selected_name: str, selected_modules: list):
    # Extract necessary info based on input
    selected_image, remote_user, build_prerequisites = extract_selected_image_data(selected_name)
    selected_module_data = extract_selected_module_data(selected_modules)

    # Get info based on extracted info
    build_commands = get_build_commands(build_prerequisites) 
    setup_scripts = get_setup_scripts(selected_module_data)

    # Concatenate output strings
    setup_script_string = concat_setup_script(setup_scripts)
    
    if setup_script_string.strip() != "#!/bin/bash":
        setup_cmd = "chmod +x ./.devcontainer/setup.sh && ./.devcontainer/setup.sh"
        if selected_module_data["devcontainer"]["postCreateCommand"]:
            selected_module_data["devcontainer"]["postCreateCommand"] += f" && {setup_cmd}"
        else:
            selected_module_data["devcontainer"]["postCreateCommand"] = setup_cmd
    
    dockerfile_string = concat_dockerfile(selected_image, selected_module_data, build_commands)
    devcontainer_string = concat_devcontainer(selected_module_data, remote_user)

    return (dockerfile_string, devcontainer_string, setup_script_string)


if __name__ == "__main__":
    import argparse
    import sys
    
    parser = argparse.ArgumentParser(description="Generate Devcontainer Configurations")
    
    parser.add_argument("--project-name", "-p", default="My Devcontainer", help="Name of the project")
    parser.add_argument("--image", "-i", default="Ubuntu", help="Selected image name")
    parser.add_argument("--modules", "-m", nargs="*", default=["SSH Agent", "CLI Dev Apps"], help="List of selected modules")
    
    args = parser.parse_args()
    
    if args.modules is not None and len(args.modules) == 0:
        with open("data/modules.json", "r") as f:
            modules_data = json.load(f)
        print("Available modules:")
        for mod in modules_data.get("modules", []):
            print(f"  - {mod.get('name')}: {mod.get('description', 'No description available')}")
        sys.exit(0)
    
    dockerfile_string, devcontainer_string, setup_script_string = main(project_name=args.project_name, selected_name=args.image, selected_modules=args.modules)

    print(dockerfile_string)
    print(devcontainer_string)
    print(setup_script_string)
