# thunderbird-notifications

Server-side notification definitions for Thunderbird's [in-app notification system](https://source-docs.thunderbird.net/en/latest/inappnotifications/index.html). This repo contains:

- YAML notification definitions for stage and production
- JSON schema describing the notification data format
- Scripts for converting YAML to JSON and validating against the schema
- CI/CD pipeline that validates, converts, and deploys notifications via Pulumi

## Contributing

1. Create a branch and add or edit YAML files in `stage/yaml/`.
2. Run the conversion and validation scripts locally to verify your changes (see [Development Setup](#development-setup)).
3. Open a pull request — CI will automatically validate the YAML.
4. Once merged to `main`, the stage environment is deployed automatically.
5. To promote to production, copy the YAML file into `prod/yaml/` and open another PR. The production deploy requires manual approval in GitHub Actions.

### Development Setup

You'll first need to setup [uv](https://docs.astral.sh/uv/getting-started/installation/).

```shell
# Download python 3.12
uv python install 3.12

# Create the virtual environment
uv venv

# Install the requirements
uv sync

# Run the conversion script
uv run python scripts/convert_yaml.py stage/yaml stage/json/notifications.json

# Validate the output
uv run python scripts/validate_json.py ./schema.json stage/json
```

Replace `stage` with `prod` to convert and validate production notifications.

## Deploying

Deployment is handled automatically by GitHub Actions when changes are merged to `main`. See the [dedicated deployment documentation](./docs/deploying.rst) for details on the automated workflow, environment protection rules, manual Pulumi usage, and cache clearing.

## Notification Format

Each notification is a YAML file in `stage/yaml/` or `prod/yaml/`. Files can contain one or more notifications as a YAML list. For a full explanation of the format, types, targeting, and client behavior, see the [Thunderbird source documentation](https://source-docs.thunderbird.net/en/latest/inappnotifications/index.html).

### Example

```yaml
- id: my-notification-en
  start_at: 2025-12-01T00:00:00.000Z
  end_at: 2025-12-19T00:00:00.000Z
  title: "Upcoming Account Change"
  description: "We're switching to a more secure login system."
  CTA: "Learn More"
  URL: https://example.com
  severity: 1
  type: security
  targeting:
    include:
      - { channels: [release], locales: [en-US, en-GB] }
    percent_chance: 100
```

### Schema Reference

#### Notification

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | string | yes | Unique ID set by the server. |
| `start_at` | datetime | yes | UTC timestamp after which Thunderbird will show the notification. |
| `end_at` | datetime | yes | UTC timestamp after which the notification is never shown. |
| `title` | string | yes | Short sentence displayed in the Thunderbird UI. |
| `description` | string | no | A short paragraph displayed in the Thunderbird UI. |
| `URL` | url \| null | no | URL to open from the CTA, if any. |
| `CTA` | string \| null | no | Link text to show for the URL. |
| `severity` | integer | yes | 1 (most urgent) through 5 (least urgent). |
| `type` | string | yes | One of: `donation`, `donation_tab`, `donation_browser`, `message`, `security`, `blog`. |
| `position` | string \| null | no | Where the notification appears: `bottom-today-pane` or `bottom-spaces-toolbar`. No effect for tab/browser types. |
| `targeting` | object | yes | Targeting criteria (see below). |

#### Targeting

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `percent_chance` | number (0–100) \| null | null | Percentage of users who should see the notification. |
| `exclude` | array \| null | null | Profiles to exclude (objects are ORed, keys within are ANDed). |
| `include` | array \| null | null | Profiles to include (objects are ORed, keys within are ANDed). |

#### Profile (used in `exclude`/`include`)

| Field | Type | Description |
|-------|------|-------------|
| `locales` | string[] \| null | BCP 47 locale tags (e.g. `en-US`, `de`, `fr`). |
| `versions` | string[] \| null | Application version strings. |
| `channels` | string[] \| null | One of: `default`, `esr`, `release`, `beta`, `nightly`. |
| `operating_systems` | string[] \| null | One of: `win`, `macosx`, `linux`, `freebsd`, `openbsd`, `netbsd`, `solaris`, `other`. |
| `displayed_notifications` | string[] \| null | IDs of notifications previously displayed to the user. |
| `pref_true` | string[] \| null | Thunderbird boolean prefs that must be true. |
| `pref_false` | string[] \| null | Thunderbird boolean prefs that must be false. |
