import pathlib
import subprocess


class Repo:
    def __init__(self, path):
        self.path = pathlib.Path(path)

    def add(self, *filenames):
        paths = [self.path.joinpath(filename) for filename in filenames]
        subprocess.call(['git', 'add'] + paths, shell=True)

    def rm(self, *filenames):
        paths = [self.path.joinpath(filename) for filename in filenames]
        subprocess.call(['git', 'rm', '-rf'] + paths, shell=True)

    def commit(self, commit_message, commit_description=''):
        subprocess.call('git', 'commit', '-m', commit_message, '-m', commit_description)

    def push(self, branch='master', remote='origin', force=False):
        force = '-f' if force else ''
        subprocess.call('git', 'push', force, remote, branch)

    def pull(self, branch='master', remote='origin', force=False):
        force = '-f' if force else ''
        subprocess.call('git', 'pull', force, remote, branch)