#!/bin/env python
import click


@click.group()
def cli():
    pass


@cli.command()
def generate():
    """Generates the project stub."""
    click.echo('Not yet implemented!')


def main():
    cli()
