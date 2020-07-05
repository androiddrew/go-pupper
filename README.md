# go-pupper
Software for the Pupper robot

## Development

Each service will have it's own dependencies. To prevent having to build multiple virtualenvs to develop each service 
you should use the `env_sync` function provided by `scripts/profile`.

```
source scripts/profile
env_sync service/app/requirements.txt
```