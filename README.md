# thunderbird-notifications

This repo contains:
- JSON schema for Thunderbird notifications
- scripts for converting from YAML to JSON
- scripts for validating JSON against the schema
- GitHub actions to run conversion and validation

## Quick Start

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

If your system install of Python is not 3.12, you can use uv to specially create a 3.12 virtual environment.

You'll first need to setup [uv](https://docs.astral.sh/uv/getting-started/installation/), and make sure the folder if 
free of any .venv or venv folders. (Delete them if they exist.)

```shell
# Download python 3.12
uv python install 3.12

# Create the virtual environment
uv sync

# Install the requirements
uv pip install -r requirements.txt

# Run the conversion script for stage
uv run ./scripts/convert_yaml.py stage/yaml stage/json/notifications.json

# Run the conversion script for prod
uv run ./scripts/convert_yaml.py prod/yaml prod/json/notifications.json
```

## Local setup

To run the scripts locally (and/or to test the GitHub actions locally), follow these instructions to install the dependencies.

Here's a cheat sheet for running the commands after you've completed the installation steps:

```sh
# Activate virtualenv
source ./venv/bin/activate

# Manually convert yaml/*.yaml to JSON
# (default output is json/notifications.json)
python ./scripts/convert_yaml.py yaml

# Manually convert YAML to JSON, specifying output file
python ./scripts/convert_yaml.py yaml output.json

# Manually validate JSON files in the `json` directory
python ./scripts/validate_json.py schema.json json
```

```sh
# Simulate pull request (to validate JSON)
act pull_request --artifact-server-path /tmp

# Simulate push (to convert YAML to JSON)
act push --artifact-server-path /tmp
```


### Create and activate virtual environment

```sh
python3 -m venv venv
source ./venv/bin/activate    # for bash-like shells
```

### Install the dependencies

```sh
pip install -r requirements.txt
```

## Manual YAML-to-JSON conversion

Run the `convert-yaml.py` script like so:

```sh
python ./scripts/convert_yaml.py yaml json
```

If there's a single `yaml/example.yaml` file,
running this command should produce a corresponding `json/example.json` file.

## Manual JSON schema validation

The `validate-json.py` script uses this tool written in Go: `https://github.com/santhosh-tekuri/jsonschema`.

You'll need to install it (and Go) in order to run the validator locally.

### Install Go runtime

Follow the [official docs](https://go.dev/doc/install) for installing for your OS.

### Install santhosh-tekuri/jsonschema

```sh
go install github.com/santhosh-tekuri/jsonschema/cmd/jv@latest
```

### Validate the schema and any JSON files in `json/`

```sh
python validate-json.py schema.json json
```

## Testing GitHub actions locally



### Install github action simulator

Follow the [installation documentation](https://nektosact.com/installation/index.html) for your OS

Note: this tool depends on having Docker (e.g., Docker Desktop on MacOS or Docker Engine on Linux) installed.

### Simulate validation

To test the validate workflow in standalone mode.
```sh
act pull_request
```

### Simulate a conversion

To the the convert workflow (which calls validate before attempting to commit):

```sh
act push --artifact-server-path /tmp
```

This action uses the artifact server, which requires the `--artifact-server-path` option. (Re [this comment in the `act` repo](https://github.com/nektos/act/issues/329#issuecomment-1187246629).)
