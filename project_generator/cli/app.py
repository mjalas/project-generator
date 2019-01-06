#!/bin/env python
import click
import os
import sys

from project_generator.use_cases import generate_generic_template
from project_generator.use_cases import generate_generic_project
from project_generator.use_cases import load_generic_template
from project_generator.exceptions import UnsupportedConfigurationFileType
from project_generator.exceptions import RequiredKeyMissingFromConfiguration


@click.group()
def cli():
    pass


@cli.group()
def generate():
    pass


@generate.command()
@click.option('--output', default=None, help="Path of the generated template.")
def template(output):
    """Generates the base template for a generic project."""
    click.echo(f"Generating template...", nl=False)
    if not output or output == ".":
        output = os.path.join(os.getcwd(), "project.yml")
    try:
        generate_generic_template(output)
        click.echo(" Done")
    except UnsupportedConfigurationFileType:
        click.echo(" Failed! (YAML format is only supported)")


@generate.command()
@click.argument('configuration')
@click.option('--output', default=None, help="Destination to generate project structure.")
def generic(configuration, output):
    """Generates project structure based on given configuration file."""
    click.echo("Loading configuration...", nl=False)
    try:
        configuration = load_generic_template(configuration_path=configuration)
        click.echo(" Done")
    except RequiredKeyMissingFromConfiguration as rkmfc:
        click.echo(f" Failed ({rkmfc.message})")
        click.echo("Exiting program...")
        sys.exit()

    if not output or output == ".":
        output = os.getcwd()

    project_root = os.path.join(output, configuration['projectName'])
    if os.path.exists(project_root):
        selection = click.prompt(f'Project root ({project_root}) already exists, should it be overwritten? (y/N)', default="n")
        if selection is "y" or selection is "yes":
            click.echo("Generating project structure...", nl=False)
            generate_generic_project(configuration=configuration, destination=output, delete_existing=True)
            click.echo(" Done")
            click.echo("Project structure generated successfully!")
        else:
            click.echo("Can't complete project structure generation. Exiting program...")
    else:
        click.echo("Generating project structure...", nl=False)
        generate_generic_project(configuration=configuration, destination=output)
        click.echo(" Done")
        click.echo("Project structure generated successfully!")


def main():
    cli()
