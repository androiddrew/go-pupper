# App service

Provides a simple web application for monitoring your Robot.

## Features

- Reboot / Power down
- Resource Utilization Monitoring
- Service Log monitoring

## Development

After running  `env_sync` from the top directory, start a development server:
```
FLASK_APP=./app/app.py flask run --reload -h 0.0.0.0 -p 5000
```