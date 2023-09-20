import sys
import os
import importlib
import subprocess
import platform

#############################################################################################################################################

'''
Tries to install a module.
'''
def try_install_package(name_of_package):
    try:
        subprocess.check_call(["pip", "install", name_of_package])
    except:
        print("Couldn't install package, exiting.")
        sys.exit(2)

'''
Ensures a module is available. If not, then tries to install it.
'''
def ensure_module_availability(name_of_module: str, container_package_name: str = None) -> None:
    try:
        module = importlib.import_module(name_of_module, container_package_name)
    except ImportError:
        container_package_name = container_package_name if container_package_name != None else name_of_module
        print("Module not found. The following command will be ran to install the container package of it:")
        print()
        print("     pip", "install", container_package_name)
        print()
        
        if not yes_no_question_accepted("Do you want to continue with installation?", yes_message=None, no_message="Ok, exiting."):
            sys.exit(1)
        
        try_install_package(container_package_name)

def yes_no_question_accepted(question: str, yes_message:str = None, no_message:str = None) -> bool:
        answer = ""
        while answer != "yes" and answer != "no":
            answer = input(f"{question} (yes/no): ").rstrip().lstrip().lower()
        
        if answer == "no":
            if no_message != None:
                print(no_message)
            return False
        
        if yes_message != None:
            print(yes_message)
        return True

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)
      
def get_full_path(path: str) -> str:
    return os.path.abspath(os.path.expanduser(path))

def check_min_python():
    py_ver = platform.sys.version_info
    can_run = py_ver.major >= 3 and py_ver.minor >= 8

    if not can_run:
        eprint("Script requires 3.8 as a minimum Python version.\n",
               "Found python version:", platform.python_version())
        sys.exit(2)

#############################################################################################################################################
        
if __name__ == "__main__":
    print("common.py is not intended to be ran separately.")
    pass