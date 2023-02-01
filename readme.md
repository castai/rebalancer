# Rebalancer will rebalnce the cluster on schedule

This utility currently is on best effort support by @Phil Andrews through community slack

### Install Rebalancer

Run this command to install Rebalancer CronJobs

```shell
kubectl apply -f https://raw.githubusercontent.com/castai/rebalancer/main/deploy.yaml
```

### Change API key

Create API token with Full Access permissions and encode base64

```shell
echo -n "98349587234524jh523452435kj2h4k5h2k34j5h2kj34h5k23h5k2345jhk2" | base64
```

use this value to update Secret

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: castai-rebalancer
  namespace: castai-agent
type: Opaque
data:
  API_KEY: >-
    CASTAI-API-KEY-REPLACE-ME-WITH-ABOVE==
```
 
OR for convenience use one liner

```shell
kubectl get secret castai-rebalancer -n castai-agent -o json | jq --arg API_KEY "$(echo -n 9834958-CASTAI-API-KEY-REPLACE-ME-5k2345jhk2 | base64)" '.data["API_KEY"]=$API_KEY' | kubectl apply -f -
```

## How it works

Rebalancer Job will
 - Query the CAST AI estimated savings on whether a rebalance is recommended
 - If recommended, rebalance plan will be created with all nodes
 - Rebalance will be run against all existing nodes
 - Default schedule is every 6 hours. 
