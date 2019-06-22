"""
Script to display secret information
"""

import click
from colorama import init, Fore

from upside.enforcer.show.util import get_secret, format_secret
from upside.enforcer.util.auth import session

init(autoreset=True)


@click.command(help='FQ_SECRET_KEY = fully qualified secret Key [/secret_directory/secret_name]')
@click.argument('fq_secret_key')
@click.option('--decrypt', '-d', flag_value=True, help='show decrypted secret value')
@click.option('--profile', '-p', default=None, help='aws profile')
@click.option('--region', '-r', default=None, help='aws region name')
def show_secret(fq_secret_key, decrypt, profile, region):
    client = session(profile, region).client('ssm')

    print('Region: ' + Fore.GREEN + (region or client.meta.region_name))

    if profile:
        print('Profile: ' + Fore.GREEN + profile)

    format_secret(get_secret(client, fq_secret_key, decrypt))
