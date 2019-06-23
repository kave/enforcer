from colorama import init, Fore
from tabulate import tabulate

from upside.enforcer.util.secret import Secret

init(autoreset=True)


# TODO handle chunked secret case
def get_secret(client, fq_secret_key: str = None, decrypt: bool = False):
    equals_filter = [
        {
            'Key': 'Name',
            'Option': 'Equals',
            'Values': [
                fq_secret_key,
            ]
        }]

    extra_details = client.describe_parameters(ParameterFilters=equals_filter)
    parameter = client.get_parameter(Name=fq_secret_key, WithDecryption=decrypt)

    return populate_secret(parameter['Parameter'], extra_details['Parameters'][0])


def populate_secret(secret_value, extra_details):
    secret = Secret(key=secret_value['Name'],
                    value=secret_value['Value'],
                    version=secret_value['Version'],
                    description=extra_details.get('Description', None),
                    encryption_key=extra_details.get('KeyId', None),
                    last_modified=secret_value['LastModifiedDate'],
                    last_modified_user=extra_details['LastModifiedUser'])

    return secret


def format_secret(secret: Secret):
    output = [[secret.key, secret.description, secret.version, secret.last_modified, secret.last_modified_user, secret.encryption_key]]
    print('\n' + tabulate(output, headers=['Key', 'Description', 'Version', 'Last Modified Date', 'Last Modified User', 'Encryption Key ID']))
    print(Fore.GREEN + '\n' + tabulate([[secret.value]], headers=['Value']))
