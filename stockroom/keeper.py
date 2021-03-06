from pathlib import Path
from hangar import Repository


def init_repo(name=None, email=None, overwrite=False):
    """ init hangar repo, create stock file and add details to .gitignore """
    if not Path.cwd().joinpath('.git').exists():
        raise RuntimeError("stock init should execute only in a"
                           " git repository. Try running stock "
                           "init after git init")
    repo = Repository(Path.cwd(), exists=False)
    if not overwrite and repo.initialized:
        commit_hash = repo.log(return_contents=True)['head']
        print(f'Hangar Repo already exists at {repo.path}. '
              f'Initializing it as stock repository')
    else:
        if name is None or email is None:
            raise ValueError("Both ``name`` and ``email`` cannot be None")
        commit_hash = ''
        repo.init(user_name=name, user_email=email, remove_old=overwrite)
    # closing the environment for avoiding issues in windows
    repo._env._close_environments()

    stock_file = Path.cwd()/'head.stock'
    if not stock_file.exists():
        # str() because of typing
        with open(str(stock_file), 'w+') as f:
            f.write(commit_hash)
        print("Stock file created")

    gitignore = Path.cwd()/'.gitignore'
    # str() because of typing
    with open(str(gitignore), 'a+') as f:
        f.seek(0)
        if '.hangar' not in f.read():
            f.write('\n# hangar artifacts\n.hangar\n')
