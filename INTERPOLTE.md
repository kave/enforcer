# Kubernetes

This tool assumes you are using the default [kubernetes secret template syntax](https://kubernetes.io/docs/concepts/configuration/secret/) 
```
apiVersion: v1
kind: Secret
metadata:
  name: mysecret
type: Opaque
data:
  username: YWRtaW4=
  password: MWYyZDFlMmU2N2Rm
```

Values to be interpolated with will signal replacement with `$((value))`
```
apiVersion: v1
kind: Secret
metadata:
  name: mysecret
type: Opaque
data:
  username: $((username))
  password: $((password))
```
- the tool will search for secrets in `/secret_directory/username` & `/secret_directory/password` for values

To sync with kubernetes you would pipeline the output into an apply function
   - `reloaded interpolate <template_path> --secret_directory <secret_directory> --kubernetes | kubectl apply -`