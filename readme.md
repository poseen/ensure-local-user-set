# ensure-local-user-set

This repository contains a git pre-hook script which will not let you commit anything until you have set your `user.name` and `user.email` locally in your repository. This is to avoid data leakage where your globally set username and email may make its way to other repositories.

This hook disciplines you to always have locally set username and email.

## Prerequisites

Scripts need 3.8 Python to run. It may run with older versions too.

## Installation

### Automatic (using installer script)

1. Get source code by downloading or cloning.
1. Change current directory to `src`.
1. ``chmod +x install.py``
1. ``install.py``
1. Follow instructions in terminal.

### Manual Installation

1. Get source code by downloading or cloning.

1. Change current directory to `src`.

1. Check the `init.templateDir`:
   ```
   $ git config --global init.templateDir
   ```

1. If nothing is returned, you have to create a directory.
   ```
   $ mkdir ~/.git_template
   $ mkdir ~/.git_template/hooks
   ```

1. Now you have to set it in the global settings.
   ```
   $ git config --global init.templateDir "git config --global init.templateDir "~/.git_template"
   ```

1. Copy `common.py` and `pre-commit.py` to `~/.git_template/hooks` directory.
   ```
   $ cp ./common.py ~/.git_template/hooks/common.py
   $ cp ./pre-commit.py ~/.git_template/hooks/pre-commit
   ```
   Please note the renaming of `pre-commit.py` to `pre-commit`.

1. Make `pre-commit` executable.
   ```
   $ chmod +x ~/.git_template/hooks/pre-commit
   ```
1. In already cloned local repositories re-initialize git.
   ```
   $ cd ~/work/my_super_project
   $ git init
   ```
   Repositories cloned in the future will have the pre-commit hook automatically.

## Usage
After installing you don't have to do anything, the script will run every time before commiting any changes. It will check if the ``user.name`` and ``user.email`` is set on the local repository level and won't let the commit happen if any of these are missing.

If the script stops commiting, you can set these variables in your repository using the following commands:

```
$ git config --local user.name 'USER NAME'
$ git config --local user.email 'USER EMAIL'
```

### Example outputs
```
$ git commit -m "Test"

Checking whether local user information is set... Failed.

Repo level local user.name and/or user.email is not set. This may lead to using wrong user.name and/or user-email in commits to this repo.
You can use the following commands while in the repo's directory to set the local user name and e-mail for this repo:

     git config --local user.name 'USER NAME'
     git config --local user.email 'USER EMAIL'

After you set these please retry git commit.

$ git config --local user.name "User Name"

$ git config --local user.email "username@example.com"

$ git commit -m "Test"

Checking whether local user information is set... Done.
[main 0f5fd75] Test
 1 file changed, 2 insertions(+), 1 deletion(-)
```
