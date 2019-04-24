"""
Script to list secrets from AWS SSM Parameter Store
"""

import click
from colorama import init, Fore

from upside.enforcer.ls.util import lookup_secrets, format_secret_store
from upside.enforcer.util.auth import session

init(autoreset=True)


@click.command()
@click.option('--contains', default=None, help='returns secrets containing the value')
@click.option('--begins_with', default=None, help='returns secrets beginning with the value')
@click.option('--profile', default=None, help='aws profile')
@click.option('--region', default=None, help='aws region name')
def list_secrets(contains, begins_with, profile, region):
    client = session(profile, region).client('ssm')

    print('Region: ' + Fore.GREEN + (region or client.meta.region_name))

    if profile:
        print('Profile: ' + Fore.GREEN + profile)

    print(format_secret_store(lookup_secrets(client, contains, begins_with)))
