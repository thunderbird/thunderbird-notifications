# thunderbird-notifications

This repo contains:
- JSON schema for Thunderbird notifications
- scripts for converting from YAML to JSON
- scripts for validating JSON against the schema
- GitHub actions to run conversion and validation



## Local setup

To run the scripts locally (and/or to test the GitHub actions locally), follow these instructions to install the dependencies.

Here's a cheat sheet for running the commands after you've completed the installation steps:

```sh
# Activate virtualenv
source ./venv/bin/activate

# Manually convert YAML to JSON
python convert-yaml.py yaml json

# Manually validate JSON
python validate-json.py schema.json json
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
python convert-yaml.py yaml json
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
