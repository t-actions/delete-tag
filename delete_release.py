#!/usr/bin/env python3
import os
import sys
import json
import logging
import requests


def delete_release(repo: str, tag: str, sess = requests.Session()):
    r = sess.get('https://api.github.com/repos/{0}/releases/tags/{1}'.format(
        repo, tag))

    if not (r.ok and r.json().get('id')):
        if r.status_code < 400 or r.status_code == 404:
            logging.warning(
                'Cannot find release with tag named "{0}"\n{1}'.format(
                    tag, json.dumps(r.json(), indent = 2)))
        elif os.environ.get('IGNORE_ERROR'):
            r.raise_for_status()
        else:
            logging.error('{0} Error: {1} for url: {2}'.format(
                r.status_code, r.reason, r.url))
            logging.error(r.content)
        return

    release_id = r.json().get('id')
    r = sess.delete('https://api.github.com/repos/{0}/releases/{1}'.format(
        repo, release_id))
    if not os.environ.get('IGNORE_ERROR'):
        r.raise_for_status()
    elif not r.ok:
        logging.error('{0} Error: {1} for url: {2}'.format(
            r.status_code, r.reason, r.url))
        logging.error(r.content)
    else:
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
        level = logging.DEBUG,
        format = '%(asctime)s %(levelname)s %(message)s',
        datefmt = '%Y-%m-%d %X',
    )
    main()
