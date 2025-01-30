# 

import mastodon
from mastodon import Mastodon
from pathlib import Path,PosixPath

import argparse
from datetime import datetime, timedelta, timezone
import dateparser

trace_level = None

python_gsoc_url = 'https://social.python-gsoc.org/'
client_id = 'psf-gsoc-bot'
cred_path = PosixPath('~/.psf-gsoc-bot/clientcred.secret').expanduser()

def trace(message: str):
    if trace_level is not None:
        print(message)

def check_recent_posts(client: Mastodon, account_name: str, deadline: datetime):
    week = timedelta(weeks=1)
    initial_window = deadline - week

    try:
        # take an account name
        account = client.account_lookup(account_name)
        print(f"{account_name}:")

        # look up the posts, in order. Find the most recent.
        # TODO: Extend this to keep finding until posts are outside the interval.
        posts = client.account_statuses(account['id'], exclude_reblogs = True, exclude_replies = True, limit=10)
        trace(f'Returned {len(posts)} posts.')

        if len(posts) == 0:
            print(f"{account_name} has no posts.")
            return

        for post in posts:
            trace(post)

        window_posts = [p for p in posts if p['created_at'] >= initial_window and p['created_at'] <= deadline]
        if len(window_posts) > 0:
            print(f'{account_name} has {len(window_posts)} posts in the window (between {initial_window} and {deadline}). The most recent is on {window_posts[0]['created_at']}.')
            # Record when the most recent post was
            print(f"Most recent post timestamp: {window_posts[0]['created_at']}, link: {window_posts[0]['url']}, size: {len(window_posts[0]['content'])}")

        else:
            print(f"{account_name} didn't post between {initial_window} and {deadline}.")
        

        if (posts[0]['created_at'] > deadline):
            print(f"{account_name} has posts after the deadline.")

    except mastodon.errors.MastodonNotFoundError:
        print(f"{account_name} is not present on the server.")

def register_app():
    trace("Checking for registration.")
    if not cred_path.exists():
        trace('No registration found.')
        if not cred_path.parent.exists():
            trace(f'Config directory {cred_path.parent} missing.')
            cred_path.parent.mkdir()
        trace(f'Registering as {client_id}.')
        Mastodon.create_app(
            client_id,
            api_base_url = python_gsoc_url,
            to_file = cred_path
        )

parser = argparse.ArgumentParser(prog='python-gsoc-bot',
                                 description='Checks up on users.')

parser.add_argument('-d', '--deadline', required=True,
                    help="The date/time (prefer RFC 3339, indicating UTC with a +0.)")
input_group = parser.add_mutually_exclusive_group(required=True)
input_group.add_argument('-i', '--input', metavar='INPUT_FILE',
                         help="Path to a file containing a list of accounts, see notes.")
input_group.add_argument('-a', '--account',
                         help="Account name for a single account to look up. For the local server, omit the server address.")
parser.add_argument('-v', '--verbose', action='store_const', const=True,
                    help="Log while running")

args = parser.parse_args()

if args.verbose is not None:
    trace_level = args.verbose

deadline = dateparser.parse(args.deadline)
if deadline is None:
    print(f'{args.deadline} is not a correctly-formatted datetime.')
    exit(1)

trace(f'Deadline: {args.deadline} parsed as {deadline}')

register_app()
cred = cred_path.read_text()

masto = Mastodon(
    client_id,
    cred,
    api_base_url = python_gsoc_url
)

if args.account is not None:
    # input validation?
    check_recent_posts(masto, args.account, deadline)
elif args.input is not None:
    input_file = Path(args.input).resolve()
    trace(f"Loading settings from {input_file}")
    if not input_file.exists():
        print(f"No such data source: '{input_file}'")
        exit(1)

    account_list_str = input_file.read_text()
    account_list = account_list_str.splitlines()

    for account in account_list:
        trace(f'Calling check_recent_posts(...,{account},{deadline})')
        check_recent_posts(masto, account, deadline)

    print("Not ready for all the file decoding shenanigans yet!")
