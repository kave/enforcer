from collections import defaultdict

from tabulate import tabulate

from upside.enforcer.util.secret import Secret


def lookup_secrets(client, contains: str = None, begins_with: str = None):
    store = defaultdict(list)
    begins_with_filter = []

    if begins_with:
        begins_with_filter = [
            {
                'Key': 'Name',
                'Option': 'BeginsWith',
                'Values': [
                    begins_with,
                ]
            }]

    secrets = client.describe_parameters(ParameterFilters=begins_with_filter)
    add_secrets_to_secret_store(secrets, store, contains)
    if len(secrets['Parameters']) and 'NextToken' in secrets:
        # if there are greater than 10 secrets in the directory keep fetching
        while 'NextToken' in secrets:
            existing_secrets = secrets = client.describe_parameters(ParameterFilters=begins_with_filter, NextToken=secrets['NextToken'])
            add_secrets_to_secret_store(existing_secrets, store, contains)
        else:
            # update store with the last pagination request
            add_secrets_to_secret_store(secrets, store, contains)

    return store


def add_secrets_to_secret_store(secrets, store, contains: str):
    for existing_secret in secrets['Parameters']:
        secret = Secret(key=existing_secret['Name'],
                        version=existing_secret['Version'],
                        last_modified=existing_secret['LastModifiedDate'],
                        last_modified_user=existing_secret['LastModifiedUser'])
        if contains:
            if contains in secret.key:
                store[secret.key].append(secret)
        else:
            store[secret.key].append(secret)


def format_secret_store(store: dict):
    output = []

    for key, secrets in store.items():
        for secret in secrets:
            output.append([secret.key, secret.version, secret.last_modified, secret.last_modified_user])

    return tabulate(output, headers=['Key', 'Version', 'Last Modified Date', 'Last Modified User'])
