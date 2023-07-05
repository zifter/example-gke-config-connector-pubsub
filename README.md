# Example: Usage Config Connector to manage PubSub

## Before you start
You need:
* GKE with Config Connector enabled
* helm

If you wish to change code:
* docker
* python (optional)

## How To Run
```
make prepare
```

In created file `test-values.yaml` change `gcpProjectID` variable to you GCP Project ID.

```
make deploy
```

## Cleanup
```
make destroy
```