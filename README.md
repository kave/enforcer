# Enforcer-Reloaded: AWS SSM Parameter Store Management CLI
## This time.. Its Personal >:l
[![image](https://img.shields.io/pypi/v/enforcer-reloaded.svg)](https://pypi.org/project/enforcer-reloaded)
[![CircleCI](https://circleci.com/gh/kave/enforcer/tree/master.svg?style=svg)](https://circleci.com/gh/kave/enforcer/tree/master)
-------------------

# Docs
Helper script to upload secrets to AWS SSM Parameter Store.
Any secrets greater than the AWS Parameter store value limit 4096 characters will be broken up into chunks and suffixed `_chunk_<index>`
This script will read your secret value from the clipboard automagically
- [Chunking logic deep dive](CHUNKS.md)


# Assumptions
This tool does not currently support nested directories in Parameter Store. It assumes you are follow the convention of `/secret_dir/secret_name`

# Usage
`pip install enforcer-reloaded`

```
reloaded --help
```

# Interpolation
- [Kubernetes](INTERPOLTE.md)

# AWS Authentication
We follow [boto3 conventions](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/configuration.html) for AWS authentication

# Pyperclip dependency
*Not Implemented Error*
- https://pyperclip.readthedocs.io/en/latest/introduction.html#not-implemented-error

Formatting
==========

This repo includes `yapf`, which will format code to our style. It's currently integrated into the lint step, so `make pep8` will
also reformat code.

Versioning
==========
Uses [semantic versioning](https://semver.org/), expecting that we'll start our
versions at 1.0 (to signal that they're used in production. If they aren't, feel
free to use <1.0).
- MAJOR version when you make incompatible API changes,
- MINOR version when you add functionality in a backwards-compatible manner, and
- PATCH version when you make backwards-compatible bug fixes.

Licenses
====
- [Apache 2.0](LICENSE)
- [3rd party licenses](3RD_PARTY_DEPENDENCIES.md)
