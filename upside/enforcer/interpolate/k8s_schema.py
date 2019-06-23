import base64
import io
from collections import ChainMap as _ChainMap
from copy import deepcopy
from pathlib import Path
from string import Template

from colorama import init, Fore
from ruamel.yaml import YAML

from .util import lookup_secrets

init(autoreset=True)

'''
Mutates the secret template to only sync keys that exist in parameter store in the format `/secret_dir/secret_name`.
e.g
Secret Template
   - data
      - A
      - B
      - C
Parameter Store
    - A
    - C
Mutated Template to be applied
    - data
        - A
        - C
'''


class K8s(Template):
    delimiter = '$'
    pattern = r"""
    \$\(\((?:
      (?P<escaped>$) |   # Escape sequence of two delimiters
      (?P<secret>(?a:[-_a-zA-Z0-9]*))      |   # delimiter and a Python identifier
      (?P<secret_base64>(?a:[-_a-zA-Z0-9]*))\|base64  |   # delimiter and a braced identifier
      (?P<invalid>)              # Other ill-formed delimiter exprs
    )\)\)
    """

    def substitute(*args, **kws):
        if not args:
            raise TypeError("descriptor 'substitute' of 'Template' object "
                            "needs an argument")
        self, *args = args  # allow the "self" keyword be passed
        if len(args) > 1:
            raise TypeError('Too many positional arguments')
        if not args:
            mapping = kws
        elif kws:
            mapping = _ChainMap(kws, args[0])
        else:
            mapping = args[0]

        # Helper function for .sub()
        def convert(mo):
            # Check the most common path first.
            secret = mo.group('secret')
            secret_base64 = mo.group('secret_base64')
            if secret is not None:
                return str(mapping[secret])
            if secret_base64 is not None:
                utf8_encoded = str(mapping[secret_base64]).encode('utf-8')
                base64_encoded = base64.b64encode(utf8_encoded)
                return base64_encoded.decode('utf-8')
            if mo.group('escaped') is not None:
                return self.delimiter
            if mo.group('invalid') is not None:
                self._invalid(mo)
            raise ValueError('Unrecognized named group in pattern',
                             self.pattern)

        return self.pattern.sub(convert, self.template)


def remove_any_keys_not_in_secret_store(secret_template_yaml, secrets_store, secret_dir):
    secret_template_yaml_sans_extra_keys = deepcopy(secret_template_yaml)
    for secret_key in secret_template_yaml['data']:
        if secret_key not in secrets_store[secret_dir]:
            del secret_template_yaml_sans_extra_keys['data'][secret_key]
            print(Fore.RED + f'{secret_key} is missing from {secret_dir} Secret Vault')

    if len(secret_template_yaml_sans_extra_keys['data']) == 0:
        print('INFO: No keys to sync'.format(secret_dir))
        exit(1)

    return secret_template_yaml_sans_extra_keys


def interpolate_secrets_template(client, template_path, secret_dir: str = None):
    path = Path(template_path)
    file = open(str(path))
    if not secret_dir:
        # If secret_dir is not passed in by the user, then default to the files prefix
        if '.' in path.name:
            secret_dir = path.name.split('.')[0]

    yaml = YAML()

    template = yaml.load(file.read())

    secrets_store = lookup_secrets(client, secret_dir)

    sanitized_template = remove_any_keys_not_in_secret_store(template, secrets_store, secret_dir)

    dump_stream = io.StringIO()
    yaml.dump(sanitized_template, dump_stream)
    secret_tmpl = K8s(dump_stream.getvalue())

    try:
        return secret_tmpl.substitute(secrets_store[secret_dir])
    except Exception as err:
        print('Error: failed syncing secret {}'.format(secret_dir))
        print(err)
        exit(1)
