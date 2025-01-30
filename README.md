# psf-gsoc-fedibot

A bot for Python-GSOC's Fediverse presence.

Making it easier to keep track of our participants, and inviting both participants and mentors to engage more in the community. Plus, it's written in Python! We figure we should be able to hack on our own infrastructure, in the project language.

## Features (goals)

- Keep track of participants' regular posts
- Link participants, projects, and mentors
- Produce reports
- Promote projects?

## Usage

```bash
usage: python-gsoc-bot [-h] -d DEADLINE (-i INPUT_FILE | -a ACCOUNT) [-v]

Checks up on users.

options:
  -h, --help            show this help message and exit
  -d DEADLINE, --deadline DEADLINE
                        The date/time (prefer RFC 3339, indicating UTC with a +0.)
  -i INPUT, --input INPUT_FILE
                        Path to a file containing a list of accounts, not yet implemented.
  -a ACCOUNT, --account ACCOUNT
                        Account name for a single account to look up. For the local server, omit the server address.
  -v, --verbose         Log while running
```

Notes:

File input support isn't yet ready at all, and reporting's not at all there yet. Actual posting has
yet to be designed.

## Contribute?

We're not really ready for outside contributions yet; so far, this is a proof of concept more than anything else. This project is run by [Ben](https://social.python-gsoc.org/@ben) in spare time.
