#!/bin/python
#
# This script ensures the local user.name and user.email
# is set to avoid accidently using wrong user.name and user.email
# when commiting a change.
#
# To enable this hook, rename this file to "pre-commit" and copy it
# to your hooks folder among with common.py.

import sys
from common import *
ensure_module_availability("git", "GitPython")
import git

#############################################################################################################################################

def get_local_git_settings(section: str, option: str, path_to_repo: str = ".") -> str | None:
    value = None
    try:
        repo = git.Repo(get_full_path(path_to_repo))
        config = repo.config_reader(config_level="repository")
        value = config.get_value(section, option, None)
    except:
        return None
    repo.close()
    return value

def get_local_git_user_name(path_to_repo: str = None) -> str | None:
    user_name = get_local_git_settings("user", "name", path_to_repo)
    user_name = user_name.lstrip().rstrip() if user_name != None else None
    return user_name

def get_local_git_user_email(path_to_repo: str = None) -> str | None:
    user_email = get_local_git_settings("user", "email", path_to_repo)
    user_email = user_email.lstrip().rstrip() if user_email != None else None
    return user_email

def check_if_locals_are_set(path_to_repo: str = None) -> bool:
    return get_local_git_user_email(path_to_repo) != None and get_local_git_user_name(path_to_repo) != None

#############################################################################################################################################

def main() -> int:
    args = sys.argv[1:]
    path_to_repo = "."
    
    if len(args) > 1:
        eprint("Scrips accepts only zero or one argument.")
        return 2
    
    if len(args) == 1:
        path_to_repo = args[0]
    
    path_to_repo = get_full_path(path_to_repo)
    
    print("Checking whether local user information is set...", end=" ")
    if not check_if_locals_are_set(path_to_repo):
        print("Failed.")
        print("")
        print("Repo level local user.name and/or user.email is not set. This may lead to using wrong user.name and/or user-email in commits to this repo.")
        print("You can use the following commands while in the repo's directory to set the local user name and e-mail for this repo:")
        print("")
        print("     git config --local user.name 'USER NAME'")
        print("     git config --local user.email 'USER EMAIL'")
        print("")
        print("After you set these please retry git commit.")
        return 1
    
    print("Done.")
    return 0

#############################################################################################################################################

if __name__ == '__main__':
    raise SystemExit(main())
