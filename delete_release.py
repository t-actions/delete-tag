#!/usr/bin/env python3
import os
import sys
import json
import logging
import requests


def delete_release(repo: str, tag: str, sess = requests.Session()):
    r = sess.get('https://api.github.com/repos/{0}/releases/tags/{1}'.format(
        repo, tag))
    r.raise_for_status()

    release_id = r.json().get('id')
    if not release_id:
        logging.warning('Cannot find release with tag named "{0}"\n{1}'.format(
            tag, json.dumps(r.json(), indent = 2)))
        return

    r = sess.delete('https://api.github.com/repos/{0}/releases/{1}'.format(
        repo, release_id))
    r.raise_for_status()
    logging.info('Deleted release "{0}"'.format(tag))


def main():
    token = os.environ.get('GITHUB_TOKEN')
    if not token:
        logging.error('Cannot find env "GITHUB_TOKEN"')
        sys.exit(1)

    repo = os.environ.get('GITHUB_REPOSITORY')
    if not repo:
        logging.error('Cannot find env "GITHUB_REPOSITORY"')
        sys.exit(1)

    tag = os.environ.get('TAG')
    if not tag:
        logging.error('Cannot find env "TAG"')
        sys.exit(1)

    with requests.Session() as sess:
        sess.headers['Authorization'] = 'token {0}'.format(token)
        delete_release(repo, tag, sess)


if __name__ == "__main__":
    logging.basicConfig(
        level = logging.INFO,
        format = '%(asctime)s %(levelname)s %(message)s',
        datefmt = '%Y-%m-%d %X')
    main()
