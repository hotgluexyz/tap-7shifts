# tap-7shifts

`tap-7shifts` is a Singer tap for [7shifts](https://www.7shifts.com/), a workforce and labor management platform for restaurants.

Built with the [Hotglue Singer SDK](https://github.com/hotgluexyz/HotglueSingerSDK) for Singer Taps.

## Installation

```bash
pip install tap-7shifts
```

Or install directly from the repository:

```bash
pip install git+https://github.com/hotgluexyz/tap-7shifts.git
```

## Configuration

### Accepted Config Options

| Setting         | Required | Description                                                                 |
|-----------------|----------|-----------------------------------------------------------------------------|
| `client_id`     | Yes      | 7shifts OAuth2 client ID                                                    |
| `client_secret` | Yes      | 7shifts OAuth2 client secret                                                |
| `guid`          | Yes      | Company GUID from 7shifts Company Settings                                  |
| `company_id`    | Yes      | 7shifts company ID (used for company-scoped endpoints such as locations)    |
| `start_date`    | No       | The earliest record date to sync (ISO 8601 / datetime format)               |

Example `config.json`:

```json
{
  "client_id": "your_client_id",
  "client_secret": "your_client_secret",
  "guid": "your-company-guid-uuid",
  "company_id": 123456,
  "start_date": "2024-01-01T00:00:00Z"
}
```

A full list of supported settings and capabilities for this tap is available by running:

```bash
tap-7shifts --about
```

### Configure using environment variables

This Singer tap will automatically import any environment variables within the working directory's
`.env` if the `--config=ENV` is provided, such that config values will be considered if a matching
environment variable is set either in the terminal context or in the `.env` file.

### Source Authentication and Authorization

This tap uses OAuth2 client credentials authentication. You can obtain API credentials (client ID, client secret, and company GUID) from 7shifts via Company Settings → Developer Tools, or use OAuth 2.0 for partner integrations.

## Supported Streams

| Stream            | Replication Key | Primary Key | Description                                                                 |
|-------------------|-----------------|-------------|-----------------------------------------------------------------------------|
| `companies`       | `modified`      | `id`        | List of companies from the 7shifts API                                     |
| `locations`       | `modified`      | `id`        | List of locations for the configured company                               |
| `departments`     | `modified`      | `id`        | List of departments for the configured company                             |
| `shifts`          | `modified`      | `id`        | List of shifts for the configured company                                  |
| `users`           | `modified`      | `id`        | List of users for the configured company                                   |
| `user_wages`      | —               | `user_id`   | Wages per user (current and upcoming); child of `users`                    |
| `user_assignments`| —               | `user_id`   | Location, department, and role assignments per user; child of `users`      |

## Usage

You can easily run `tap-7shifts` by itself or in a pipeline.

### Executing the Tap Directly

```bash
tap-7shifts --version
tap-7shifts --help
tap-7shifts --config CONFIG --discover > ./catalog.json
tap-7shifts --config CONFIG --catalog CATALOG > ./data.singer
```

## Developer Resources

### Initialize your Development Environment

```bash
pipx install poetry
poetry install
```

### Create and Run Tests

Create tests within the `tap_7shifts/tests` subfolder and then run:

```bash
poetry run pytest
```

You can also test the `tap-7shifts` CLI interface directly using `poetry run`:

```bash
poetry run tap-7shifts --help
```
