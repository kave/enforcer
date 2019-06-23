import click

from upside.enforcer.interpolate.cli import interpolate_k8s_secrets
from upside.enforcer.ls.cli import list_secrets
from upside.enforcer.show.cli import show_secret
from upside.enforcer.upload.cli import upload


@click.group(commands={'upload': upload,
                       'ls': list_secrets,
                       'show': show_secret,
                       'interpolate': interpolate_k8s_secrets},
             help='UPLOAD - uploads secrets to AWS parameter store.\n\n'
                  + 'LS - list secrets from AWS parameter store.\n\n'
                  + 'SHOW - Show secret details from AWS parameter store.\n\n'
                  + 'INTERPOLATE - Takes a kubernetes secret template and interpolates values from secret store.\n\n')
def enforcer():
    pass


if __name__ == '__main__':
    enforcer()
