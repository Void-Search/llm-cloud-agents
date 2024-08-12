In order to use ollama with runpod you will have to add the following to the pod spec:

```yaml
PORT: 11434
OLLAMA_HOST: 0.0.0.0
```

and you SSH key to the pod. You can do this by adding the following to the pod spec, also update the pod to atleast 60GB of disk space
