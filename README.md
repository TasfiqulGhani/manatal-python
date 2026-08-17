# manatal

The easiest way to use the [Manatal](https://app.manatal.com/) Open API from Python.

[Manatal](https://app.manatal.com/) is an AI-powered ATS built for modern recruiting teams. Use this SDK to connect Manatal with your own tools — sync candidates and jobs, automate workflows, and integrate one of the best ATS platforms into your stack — with auth, pagination, and retries handled for you.

> **Note:** Community-maintained package. Not affiliated with or officially supported by Manatal.

## Why use this package?

Whether you are extending an AI-powered ATS workflow or connecting Manatal to HRIS/payroll systems, calling the Open API raw means handling tokens, pagination, and retries yourself. `manatal` wraps that into a small, predictable client:

- One line to authenticate
- Simple resource methods (`candidates`, `jobs`, `matches`, …)
- Automatic pagination
- Automatic retries on temporary errors
- Clear Python exceptions for common API errors

## Installation

```bash
pip install manatal
```

Requires Python 3.9+.

## How to get an Open API token

Open API access depends on your Manatal plan. Follow the official guide:
[Manatal Open API](https://support.manatal.com/docs/manatal-api).

### 1. Enable Open API

1. Sign in to [Manatal](https://app.manatal.com/).
2. Go to **Administration → Features → Open API**, or open  
   [Open API settings](https://app.manatal.com/administration/features/open-api).
3. If it is not enabled yet, click **Contact our support** to request access.

> Open API is available by default on the **Enterprise Plus** plan. See the [support article](https://support.manatal.com/docs/manatal-api) for details.

### 2. Generate a token

1. Open the same [Open API settings](https://app.manatal.com/administration/features/open-api) page.
2. Click **Generate new token**.
3. Copy the token and store it securely (you will use it as `api_key`).

You can also copy or delete existing tokens from that page.

### 3. Use the token in Python

```python
from manatal import Manatal

client = Manatal(api_key="YOUR_OPEN_API_TOKEN")
```

Or set an environment variable:

```bash
export MANATAL_API_KEY="YOUR_OPEN_API_TOKEN"
```

```python
from manatal import Manatal

client = Manatal()  # reads MANATAL_API_KEY
```

## Quick start

```python
from manatal import Manatal

client = Manatal(api_key="YOUR_OPEN_API_TOKEN")

# Create a candidate
candidate = client.candidates.create(
    full_name="Jane Doe",
    email="jane@example.com",
)
print(candidate.id)

# List jobs (automatically walks every page)
for job in client.jobs.list():
    print(job.id, job.position_name)

# Fetch one record
job = client.jobs.retrieve(123)
print(job.id)
```

API responses support both styles:

```python
job = client.jobs.create(organization=2208123, position_name="pyp")
print(job.id)          # recommended
print(job["id"])       # still works
print(job.position_name)
```

## What you can access

| Resource | Example |
|----------|---------|
| Candidates | `client.candidates.list(email="jane@example.com")` |
| Jobs | `client.jobs.create(organization=1, position_name="Engineer")` |
| Organizations | `client.organizations.list()` |
| Matches | `client.matches.create(candidate=123, job=456)` |
| Contacts | `client.contacts.list()` |
| Users | `client.users.list()` |
| Skills & lookups | `client.skills.list()`, `client.currencies.list()`, `client.match_stages.list()` |

Nested data works the same way:

```python
client.candidates.notes(123).create(info="Called candidate")
client.candidates.experiences(123).list()
client.jobs.attachments(456).list()
```

## Pagination

By default, `.list()` returns **all** matching results. Need a single page?

```python
page = client.candidates.list_page(page=1)
print(page.count)         # total matching records
print(len(page.results))  # records on this page
```

## Error handling

```python
from manatal import (
    Manatal,
    AuthenticationError,
    NotFoundError,
    RateLimitError,
    ValidationError,
)

client = Manatal(api_key="...")

try:
    client.candidates.retrieve(999999)
except NotFoundError as exc:
    print("Missing record:", exc.status_code, exc.body)
except ValidationError as exc:
    print("Invalid payload:", exc.body)
except RateLimitError:
    print("Too many requests — try again later")
except AuthenticationError:
    print("Check your API token")
```

## Useful links

| Resource | Link |
|----------|------|
| Manatal app | https://app.manatal.com/ |
| Enable Open API & generate tokens | https://support.manatal.com/docs/manatal-api |
| Open API settings | https://app.manatal.com/administration/features/open-api |
| API reference (developers) | https://developers.manatal.com/reference/getting-started |
| Base URL used by this client | `https://api.manatal.com/open/v3` |

## Contributing

Issues and pull requests are welcome:  
https://github.com/TasfiqulGhani/manatal-python

## License

MIT
