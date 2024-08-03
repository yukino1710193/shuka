# Some notes

## 1. Create Secret

```bash
kubectl create secret docker-registry shuka-private \
  --docker-server=https://index.docker.io/v1/ \
  --docker-username=bonavadeur \
  --docker-password='naninani' \
  --docker-email=email@gmail.com \
  --save-config -o yaml > shuka-secret.yaml
```
