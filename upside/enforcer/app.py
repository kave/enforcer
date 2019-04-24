import click

from upside.enforcer.upload.cli import upload
from upside.enforcer.ls.cli import list_secrets


@click.group(commands={'upload': upload, 'ls': list_secrets}, help='UPLOAD - uploads secrets to AWS parameter store.\n\n' +
                                                                   'LS - list secrets from AWS parameter store.\n')
def enforcer():
    pass


if __name__ == '__main__':
    enforcer()
