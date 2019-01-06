#!/bin/env python
import os
from shutil import rmtree
from typing import Dict

import yaml

from project_generator.exceptions import TypeMissingFromConfiguration,\
    UnsupportedConfigurationFileType,\
    RequiredKeyMissingFromConfiguration


__generic_template = {
        "projectName": "<project name here>",
        "structure": [
            {
                "name": "<folder name here>",
                "type": "folder",
                "children": [
                    {
                        "name": "<child file name here>",
                        "type": "file",
                        "content": "<file content or leave empty>"
                    }
                ]
            },
            {
                "name": "<name of second folder",
                "type": "folder",
                "children": []
            },
        ]
    }


def generate_generic_template(output_path: str):
    if output_path.endswith(".yml") or output_path.endswith(".yaml"):
        with open(output_path, "w") as template_file:
            yaml.dump(__generic_template, template_file, default_flow_style=False)
    else:
        raise UnsupportedConfigurationFileType("Configuration file is not in YAML format!")


def load_generic_template(configuration_path: str) -> Dict:
    with open(configuration_path, "r") as src:
        configuration = yaml.load(src)
    if 'projectName' not in configuration:
        raise RequiredKeyMissingFromConfiguration("Missing projectName key!")
    if not configuration['projectName']:
        raise RequiredKeyMissingFromConfiguration("Missing value for key projectName!")
    return configuration


def __create_structure_item(structure: Dict, root_path: str, level: int):
    if level < 3:
        for item in structure:
            path = os.path.join(root_path, item['name'])
            if 'type' not in item:
                raise TypeMissingFromConfiguration(f"Item {item['name']} is missing 'type' key!")
            if item['type'] == 'folder':
                os.mkdir(path=path)
                if 'children' in item and item['children']:
                    __create_structure_item(item['children'], path, level+1)
            elif item['type'] == 'file':
                with open(path, "w") as dest:
                    dest.write(item['content'])


def generate_generic_project(configuration: Dict, destination: str, delete_existing=False):
    if not os.path.exists(destination):
        os.mkdir(path=destination)

    root_path = os.path.join(destination, configuration['projectName'])
    if os.path.exists(root_path) and delete_existing:
        rmtree(root_path)

    os.mkdir(path=root_path)
    __create_structure_item(configuration['structure'], root_path, 1)
