# 

from mastodon import Mastodon
from pathlib import PosixPath
import os.path
import argparse
from datetime import datetime, timedelta, timezone
import dateparser

python_gsoc_url = 'https://social.python-gsoc.org/'
client_id = 'psf-gsoc-bot'
cred_path = PosixPath('~/.psf-gsoc-bot/clientcred.secret').expanduser()

def check_recent_posts(client: Mastodon, account_name: str, deadline: datetime):
    today = datetime.now(timezone.utc)

    week = timedelta(weeks=1)
    initial_window = deadline - week

    # take an account name
    account = client.account_lookup(account_name)

    # look up the posts, in order. Find the most recent.
    posts = client.account_statuses(account['id'], exclude_reblogs = True, exclude_replies = True, limit=10)
    print(f'Returned {len(posts)} posts.')

    for post in posts:
        print(post)

    if (len(posts) > 0):
        post = posts[0]
        postdate = post['created_at']
        print()
        # Record when the most recent post was
        print(f"Most recent post posted on: ({type(postdate)}) {postdate}, contents: {post['content']}")

        # check the current date against the most recent deadline date.
        # if the most recent post is not within a week of the most recent deadline,
        if (today > deadline and postdate < initial_window):
            # log that they're behind.
            print(f"{account_name} hasn't posted in over a week.")
            # send them a message and flag them in a list to the mentors & admins



def register_app():
    print("Checking for registration.")
    if not cred_path.exists():
        print('No registration found.')
        if not cred_path.parent.exists():
            print(f'Config directory {cred_path.parent} missing.')
            cred_path.parent.mkdir()
        print(f'Registering as {client_id}.')
        Mastodon.create_app(
            client_id,
            api_base_url = python_gsoc_url,
            to_file = cred_path
        )

register_app()
cred = cred_path.read_text()

mastodon = Mastodon(
    client_id,
    cred,
    api_base_url = python_gsoc_url
)

parser = argparse.ArgumentParser(prog='python-gsoc bot',
                                 description='Checks up on users.')

parser.add_argument('-d', '--deadline')

args = parser.parse_args()

deadline = dateparser.parse(args.deadline)
if deadline is None:
    print(f'{args.deadline} is not a correctly-formatted datetime.')
    exit(1)

print(f'Deadline: {args.deadline} parsed as {deadline}')

check_recent_posts(mastodon, 'ben@social.python-gsoc.org', deadline)

