# compiles the EasyTl-CLI to EasyTl-Core
# must be run from main directory

import os
import sys
import subprocess
import traceback


def run_script(script_path: str, args: list):
    try:
        # run the script
        subprocess.check_call(
            [sys.executable, script_path, ] + args,
            stdout=sys.stdout
        )
    except Exception as e:
        print(f'While running script {script_path} occurred the error:')
        traceback.print_exception(e)
        exit('Build script returned error')

####

if __name__ == "__main__":

    # check for the arguments
    if not len(sys.argv) > 1:
        raise ValueError('First argument must be path to the output directory path')

    dest_path = sys.argv[1]
    build_path = os.path.join(os.getcwd(), 'easytl-cli', 'build')

    # scripts to be executed
    scripts = [
        [os.path.join(build_path, 'compile.py'), [dest_path]],
        [os.path.join(build_path, 'build_initiator.py'), [dest_path]]
    ]

    ####

    print('NOTE: You must manually set "is_gui = true" in easytl-cli/config.toml file!')
    print('To continue press ENTER')
    input()

    for s in scripts:
        print('Run script:', *s)
        run_script(*s)
