import base64


def is_base64(k8s_secret_key, k8_secret_value):
    """https://stackoverflow.com/questions/12315398/verify-is-a-string-is-encoded-in-base64-python"""
    try:
        if type(k8_secret_value) == str:
            # If there's any unicode here, an exception will be thrown and the function will return false
            sb_bytes = bytes(k8_secret_value, 'ascii')
        elif type(k8_secret_value) == bytes:
            sb_bytes = k8_secret_value
        else:
            raise ValueError("Argument must be string or bytes")
        return base64.b64encode(base64.b64decode(sb_bytes)) == sb_bytes
    except Exception:
        raise ValueError(f'Secret {k8s_secret_key} is not valid base64')
