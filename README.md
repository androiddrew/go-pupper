# go-pupper
Software for the Pupper robot

## Features

Dashboard used for configuring and monitoring your pupper via a web browser.

## Development

Each service will have it's own dependencies. To prevent having to build multiple virtualenvs to develop each service 
you should use the `env_sync` function provided by `scripts/profile`.

```
source scripts/profile
env_sync ./services/app/requirements.txt
```
