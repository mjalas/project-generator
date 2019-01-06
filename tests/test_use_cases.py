import os
from shutil import rmtree
import pytest
import yaml

from project_generator.use_cases import generate_generic_project, generate_generic_template, load_generic_template
from project_generator.exceptions import TypeMissingFromConfiguration, \
    RequiredKeyMissingFromConfiguration, \
    UnsupportedConfigurationFileType

TEST_OUTPUT_FOLDER = os.path.join(os.path.dirname(os.path.realpath(__file__)), "test_output")
TEST_CONFIGURATION = {
        "projectName": "generic",
        "structure": [
            {
                "name": "generic",
                "type": "folder",
                "children": [
                    {
                        "name": "app.py",
                        "type": "file",
                        "content": "print('Hello')"
                    }
                ]
            },
            {
                "name": "tests",
                "type": "folder",
                "children": []
            },
            {
                "name": "setup.py",
                "type": "file",
                "content": ""
            },
            {
                "name": ".gitignore",
                "type": "file",
                "content": ""
            }
        ]
    }


def test_generate_generic_structure():
    project_root = os.path.join(TEST_OUTPUT_FOLDER, TEST_CONFIGURATION['projectName'])

    generate_generic_project(configuration=TEST_CONFIGURATION, destination=TEST_OUTPUT_FOLDER, delete_existing=True)
    assert os.path.exists(project_root)
    path_to_test = os.path.join(project_root, TEST_CONFIGURATION['structure'][0]['name'])
    assert os.path.exists(path_to_test)
    path_to_test = os.path.join(project_root, TEST_CONFIGURATION['structure'][1]['name'])
    assert os.path.exists(path_to_test)

    # Cleanup
    rmtree(project_root)


def test_generate_generic_structure__to_new_sub_folder():
    new_location = os.path.join(TEST_OUTPUT_FOLDER, "test_sub_folder")
    project_root = os.path.join(new_location, TEST_CONFIGURATION['projectName'])

    generate_generic_project(configuration=TEST_CONFIGURATION, destination=new_location, delete_existing=True)
    assert os.path.exists(project_root)
    path_to_test = os.path.join(project_root, TEST_CONFIGURATION['structure'][0]['name'])
    assert os.path.exists(path_to_test)
    path_to_test = os.path.join(project_root, TEST_CONFIGURATION['structure'][1]['name'])
    assert os.path.exists(path_to_test)

    # Cleanup
    rmtree(new_location)


def test_generate_generic_structure_when_destination_exists__delete_existing_is_not_used():
    project_root = os.path.join(TEST_OUTPUT_FOLDER, TEST_CONFIGURATION['projectName'])
    if not os.path.exists(project_root):
        os.mkdir(project_root)
    with pytest.raises(FileExistsError):
        generate_generic_project(configuration=TEST_CONFIGURATION, destination=TEST_OUTPUT_FOLDER)

    # Cleanup
    rmtree(project_root)


def test_generate_generic_structure_when_destination_exists__delete_existing_is_used():
    project_root = os.path.join(TEST_OUTPUT_FOLDER, TEST_CONFIGURATION['projectName'])
    if not os.path.exists(project_root):
        os.mkdir(project_root)

    generate_generic_project(configuration=TEST_CONFIGURATION, destination=TEST_OUTPUT_FOLDER, delete_existing=True)

    assert os.path.exists(project_root)
    path_to_test = os.path.join(project_root, TEST_CONFIGURATION['structure'][0]['name'])
    assert os.path.exists(path_to_test)
    path_to_test = os.path.join(project_root, TEST_CONFIGURATION['structure'][1]['name'])
    assert os.path.exists(path_to_test)

    # Cleanup
    rmtree(project_root)


def test_generate_generic_structure__with_error_in_configuration():
    poorly_constructed_configuration = {
        "projectName": "generic",
        "structure": [
            {
                "name": "generic",
            }
        ]
    }

    project_root = os.path.join(TEST_OUTPUT_FOLDER, poorly_constructed_configuration['projectName'])

    with pytest.raises(TypeMissingFromConfiguration):
        generate_generic_project(configuration=poorly_constructed_configuration, destination=TEST_OUTPUT_FOLDER,
                                 delete_existing=True)

    # Cleanup
    rmtree(project_root)


def test_generate_generic_template():
    template_path = os.path.join(TEST_OUTPUT_FOLDER, "test_template.yml")
    generate_generic_template(template_path)
    assert os.path.exists(template_path)
    with open(template_path, "r") as src:
        template = yaml.load(src)
    assert 'projectName' in template and '<project name here>' in template['projectName']

    # Cleanup
    os.remove(template_path)


def test_generate_generic_template__fail_when_using_non_supported_file_extension():
    template_path = os.path.join(TEST_OUTPUT_FOLDER, "test_template.txt")
    with pytest.raises(UnsupportedConfigurationFileType):
        generate_generic_template(template_path)


def test_load_configuration():
    template_path = os.path.join(TEST_OUTPUT_FOLDER, "test_template2.yml")
    with open(template_path, "w") as dest:
        yaml.dump(TEST_CONFIGURATION, dest, default_flow_style=False)

    configuration = load_generic_template(template_path)

    assert 'generic' in configuration['projectName']

    # Cleanup
    os.remove(template_path)


def test_load_configuration__with_required_key_missing():
    configuration = {
        "structure": [
            {
                "name": "generic",
                "type": "folder",
                "children": [
                    {
                        "name": "app.py",
                        "type": "file",
                        "content": "print('Hello')"
                    }
                ]
            }
        ]
    }

    template_path = os.path.join(TEST_OUTPUT_FOLDER, "test_template_missing_key.yml")
    with open(template_path, "w") as dest:
        yaml.dump(configuration, dest, default_flow_style=False)

    with pytest.raises(RequiredKeyMissingFromConfiguration):
        configuration = load_generic_template(template_path)

    # Cleanup
    os.remove(template_path)


def test_load_configuration__with_required_value_missing():
    configuration = {
        "projectName": "",
        "structure": [
            {
                "name": "generic",
                "type": "folder",
                "children": [
                    {
                        "name": "app.py",
                        "type": "file",
                        "content": "print('Hello')"
                    }
                ]
            }
        ]
    }

    template_path = os.path.join(TEST_OUTPUT_FOLDER, "test_template_missing_key.yml")
    with open(template_path, "w") as dest:
        yaml.dump(configuration, dest, default_flow_style=False)

    with pytest.raises(RequiredKeyMissingFromConfiguration):
        configuration = load_generic_template(template_path)

    # Cleanup
    os.remove(template_path)
