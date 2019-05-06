import click
from cli import utils


@click.group()
def cli():
    pass


@cli.command()
@click.argument('name')
def add_contract(name):
    click.echo("adding contract: {}".format(name))
    utils.new_contract(name)


@cli.command()
def list_contracts():
    click.echo("list contracts:")
    contracts = utils.list_contracts()
    for contract in contracts:
        click.echo("* {}".format(contract))


@cli.command()
@click.argument("name")
@click.argument("contract_name")
def add_event(name, contract_name):
    click.echo('adding event: {} to contract: {}'.format(name, contract_name))
    utils.new_event(name, contract_name)


if __name__ == '__main__':
    cli()
