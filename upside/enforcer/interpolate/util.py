import re
from collections import defaultdict

chunk_regex = re.compile(r'_chunk_\d*', re.IGNORECASE)


def update_secret_store(secrets, store, chunks_found):
    for secret in secrets['Parameters']:
        secret_dir_filename = secret['Name'].split('/')
        secret_dir = secret_dir_filename[1]
        secret_name = secret_dir_filename[2]

        if '_chunk_' in secret_name:
            chunks_found = True

        store[secret_dir][secret_name] = secret['Value']

    return chunks_found


def merge_chunks_if_applicable(store, secret_directory):
    keylist = sorted(store[secret_directory].keys())
    merged_values = {}
    for key in keylist:
        if '_chunk_' in key:
            name = chunk_regex.sub('', key)
            if name in merged_values:
                merged_values[name] += store[secret_directory][key]
            else:
                merged_values[name] = store[secret_directory][key]
        else:
            merged_values[key] = store[secret_directory][key]
    del store[secret_directory]  # delete references to individual chunks
    store[secret_directory] = merged_values


def lookup_secrets(client, secret_directory: str):
    store = defaultdict(dict)
    chunks_found = False

    secrets = client.get_parameters_by_path(
        Path='/' + secret_directory,
        Recursive=True,
        WithDecryption=True)

    if len(secrets['Parameters']):
        chunks_found = update_secret_store(secrets, store, chunks_found)
        # if there are greater than 10 secrets in the directory keep fetching
        while 'NextToken' in secrets:
            secrets = client.get_parameters_by_path(
                Path='/' + secret_directory,
                Recursive=True,
                WithDecryption=True,
                NextToken=secrets['NextToken'])
            chunks_found = update_secret_store(secrets, store, chunks_found)
        else:
            # update store with the last pagination request
            chunks_found = update_secret_store(secrets, store, chunks_found)

    if chunks_found:
        merge_chunks_if_applicable(store, secret_directory)

    return store
