import os
from io import StringIO
from unittest import TestCase, mock
from upside.enforcer.interpolate.k8s_schema import interpolate_secrets_template

secret_store_with_email = {
    "account": {
        "username": "YWRtaW4=",
        "password": "password",
        "email": "email"
    }
}

secret_store = {
    "account": {
        "username": "YWRtaW4=",
        "password": "password"
    }
}

script_dir = os.path.dirname(__file__)


@mock.patch('upside.enforcer.interpolate.k8s_schema.lookup_secrets', return_value=secret_store_with_email)
def test_interpolate(mock):
    correct_format = open(script_dir + '/result_with_email.yaml').read()
    result = interpolate_secrets_template(None, script_dir + '/account.yaml')
    assert result == correct_format
    print(result)


@mock.patch('sys.stdout', new_callable=StringIO)
@mock.patch('upside.enforcer.interpolate.k8s_schema.lookup_secrets', return_value=secret_store)
def test_exclude_missing_key(mock, mock_stdout):
    correct_format = open(script_dir + '/result_sans_email.yaml').read()
    result = interpolate_secrets_template(None, script_dir + '/account.yaml')
    assert 'email is missing from account Secret Vault' in mock_stdout.getvalue().strip()
    assert result == correct_format
    print(result)
