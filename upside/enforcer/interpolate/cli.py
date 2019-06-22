"""
Script to interpolate kubernetes secret template with secrets from AWS SSM Parameter Store
"""

import click
from colorama import init, Fore

from upside.enforcer.interpolate.k8s_schema import interpolate_secrets_template
from upside.enforcer.util.auth import session

init(autoreset=True)


@click.command(help='TEMPLATE_PATH = secret template file path')
@click.argument('template_path')
@click.option('-d', '--secret_directory', default=None, help='aws parameter directory name. If not provided, it will use the templates file prefix')
@click.option('-k', '--kubernetes', flag_value=True, help='kuberntes secret template type with $((value))')
@click.option('-p', '--profile', default=None, help='aws profile')
@click.option('-r', '--region', default=None, help='aws region name')
def interpolate_k8s_secrets(template_path, secret_directory, kubernetes, profile, region):
    client = session(profile, region).client('ssm')

    print('Region: ' + Fore.GREEN + (region or client.meta.region_name))

    if profile:
        print('Profile: ' + Fore.GREEN + profile)

    if kubernetes:
        print(Fore.GREEN + interpolate_secrets_template(client, template_path, secret_directory))
    else:
        print(Fore.RED + 'Please select the template type!')
