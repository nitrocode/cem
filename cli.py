#!/usr/bin/env python3
import click


def print_version(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    click.echo('Version 1.0')
    ctx.exit()


@click.group()
@click.option('--version', is_flag=True, callback=print_version,
              expose_value=False, is_eager=True)
def cli():
    pass


@click.command()
@click.argument('term')
def search(term):
    click.echo(f'Searching database for {term}')


@click.command()
@click.option('--dry-run', '-d',
              is_flag=True,
              help='Fake the install.')
# this could be a click.Choice(['firefox', 'chrome', 'chromium'])
@click.option('--browser', '-b',
              help='Choose a well known browser.')
@click.argument('extension')
def install(browser, extension, dry_run):
    click.echo(f'Opening {browser} to install {extension} right now.')
    if dry_run:
        click.echo('dry-run')


if __name__ == '__main__':
    cli.add_command(search)
    cli.add_command(install)
    cli()
