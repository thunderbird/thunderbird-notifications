# thunderbird-notifications

This repo contains:
- JSON schema for Thunderbird notifications
- scripts for converting from YAML to JSON
- scripts for validating JSON against the schema
- GitHub actions to run conversion and validation

## Quick Start

Before you begin make sure you at least have python 3.12 installed. You can do this via:
```shell
python --version
```

### With Python 3.12+ or Without UV

Create a virtualenv with python 3.12

```shell
# Create a virtual env
python -m venv .venv

# Activate virtual env
source ./venv/bin/activate

# Install the requirements
pip install -r requirements.txt

# Run the conversion script for stage
./scripts/convert_yaml.py stage/yaml stage/json/notifications.json

# Run the conversion script for prod
./scripts/convert_yaml.py prod/yaml prod/json/notifications.json
```

### Without Python 3.12+ or With UV

If your system install of Python is not 3.12, you can use uv to specially create a 3.12 virtual environment.

You'll first need to setup [uv](https://docs.astral.sh/uv/getting-started/installation/), and make sure the folder if 
free of any .venv or venv folders. (Delete them if they exist.)

```shell
# Download python 3.12
uv python install 3.12

# Create the virtual environment
uv venv

# Install the requirements
uv sync

# Run the conversion script for stage
uv run ./scripts/convert_yaml.py stage/yaml stage/json/notifications.json

# Run the conversion script for prod
uv run ./scripts/convert_yaml.py prod/yaml prod/json/notifications.json
```

## Deploying

Check out the [dedicated documentation for deploying](./docs/deploying.rst).
