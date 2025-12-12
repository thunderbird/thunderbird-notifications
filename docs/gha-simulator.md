# Testing GitHub actions locally

Note: These docs are older and might not be valid for the current version of thunderbird-notifications.

## Install github action simulator

Follow the [installation documentation](https://nektosact.com/installation/index.html) for your OS

Note: this tool depends on having Docker (e.g., Docker Desktop on MacOS or Docker Engine on Linux) installed.

## Simulate validation

To test the validate workflow in standalone mode.
```sh
act pull_request
```

## Simulate a conversion

To the the convert workflow (which calls validate before attempting to commit):

```sh
act push --artifact-server-path /tmp
```

This action uses the artifact server, which requires the `--artifact-server-path` option. (Re [this comment in the `act` repo](https://github.com/nektos/act/issues/329#issuecomment-1187246629).)
