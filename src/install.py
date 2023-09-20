#!/bin/python
#
# This script will guide you through the installation of the
# (global) pre-commit hook which will ensure that your
# user.name and user.email is locally set for every repo before
# commiting a change. This way you will be able to avoid the
# frustration of having the wrong (global) user.name and
# user.email used in a commit.

import sys
import os
import stat
import shutil

from common import *

ensure_module_availability("git", "GitPython")

import git
from git.config import GitConfigParser

#############################################################################################################################################

def print_welcome() -> None:
    print("Welcome!")
    print("This script will guide you through the installation of the (global) pre-commit hook which will ensure that your user.name and user.email is locally set for every repo before commiting a change.")
    print("This way you will be able to avoid the frustration of having the wrong (global) user.name and user.email used in a commit.")

def print_steps() -> None:
    print("The following steps will be made:")
    print("")
    print("     1. Setting up the git templates folder.")
    print("     2. Copy the script there")
    print("     3. ???")
    print("     4. PROFIT")
    print("")
    
    if not yes_no_question_accepted("Would you like to continue?"):
        sys.exit(0)

def get_global_git_settings(section: str, option: str, default_return_value: str) -> str:
    git_config = GitConfigParser(
    file_or_files=git.config.get_config_path("global"),
    read_only=True)
    
    return git_config.get_value(section, option, default_return_value)

def set_global_git_settings(section: str, option: str, new_value: str) -> None:
    git_config = GitConfigParser(
    file_or_files=git.config.get_config_path("global"),
    read_only=False)

    git_config.set_value(section, option, new_value)

def ensure_path_exists(path: str):
    path = get_full_path(path)
    print("Ensuring the following directory exists: ", path)
    is_exist = os.path.exists(path)
    if not is_exist:
        try:
            print("Couldn't find path, attempting to create it...", end=" ")
            os.makedirs(path)
            print("Done.")
        except:
            eprint("Couldn't create path. Ensure you have enough rights and if path is valid. Exiting.")
            sys.exit(3)
    else:
        print("Directory exists.")
            
def get_init_templatedir() -> str:
    _init_templatedir = get_full_path(get_global_git_settings("init", "templateDir", ""))

    if _init_templatedir == "":
        print("No 'init templateDir' is set yet. Please provide a path. Directory will be created.")
        _init_templatedir = input("Target folder: ").lstrip().rstrip()
    else:
        print("Template directory detected at '", _init_templatedir, "'.")
        _new_init_templatedir = input("Press ENTER to continue using this or type in a new folder:").lstrip().rstrip()
        _init_templatedir = get_full_path(_new_init_templatedir) if not _new_init_templatedir == '' else _init_templatedir
    
    return _init_templatedir

def set_init_template_dir_in_git(templatedir_path: str) -> None:
    print("Setting global git settings 'init.templatedir'...", end=" ")
    set_global_git_settings("init", "templatedir", templatedir_path)
    print("Done")
    
def copy_file(src_path: str, dst_path: str):
    print(f"Copying: '{src_path}' to '{dst_path}'...", end=" ")
    try:
        shutil.copy(src_path, dst_path)
    except IOError as e:
        print("Failed.")
        eprint("Couldn't copy file. Check your rights and if source file is available.", e)
        sys.exit(4)
    print("Done.")
    
def make_file_executable(file_path: str):
    try:
        print(f"Making '{file_path}' executable...", end=" ")
        st = os.stat(file_path)
        os.chmod(file_path, st.st_mode | stat.S_IEXEC)
    except:
        print("Failed.")
        eprint(f"Couldn't make '{file_path}' executable. You may need to do this manually.")
        sys.exit(5)
    print("Done.")
    
def copy_hook_script_to_template_dir(destination_directory) -> None:
    print("Copying files.")
    
    script_src_path = get_full_path("pre-commit.py")
    script_dst_path = get_full_path(os.path.join(destination_directory, "hooks", "pre-commit"))
    
    common_src_path = get_full_path("common.py")
    common_dst_path = get_full_path(os.path.join(destination_directory, "hooks", "common.py"))
    
    copy_file(script_src_path, script_dst_path)
    copy_file(common_src_path, common_dst_path)
    make_file_executable(script_dst_path)
    
   
def print_good_bye_message():
    print("Script installed.\nIn already cloned repositories run 'git init'.\nExiting.")

#############################################################################################################################################

def main() -> int:
    check_min_python()
    print_welcome()
    print_steps()
    init_templatedir = get_init_templatedir()
    ensure_path_exists(init_templatedir)
    set_init_template_dir_in_git(init_templatedir)
    copy_hook_script_to_template_dir(init_templatedir)
    print_good_bye_message()
    
    return 0

#############################################################################################################################################

if __name__ == '__main__':
    raise SystemExit(main())