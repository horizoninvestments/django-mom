import os
import subprocess
from io import StringIO

from django.core.management import call_command


def write_migration_order(filename, check=False):
    result = subprocess.run(['python', 'manage.py', 'migrate', '--check'], capture_output=True, text=True)

    # unapplied migrations result in non-zero return code but no stderr.
    # we still want to write the migrations in that case.
    if result.returncode > 0 and result.stderr:
        if "UserWarning" not in result.stderr:
            print("\n\nERROR!\n")
            print("Please review the above output and rerun.\n\n")
            raise (Exception("Subprocess has stderr"))
        else:
            print("\n\nWARNING!\n")
            print("A warning occurred during migrate --check.")
            print("Look at the output above and confirm there were no other failures.")

    output = StringIO()
    call_command('showmigrations', '--plan', stdout=output)
    file_path = os.path.join(filename)

    preface = "WARNING: This file only exists to create merge conflicts to prevent migration errors.\n" \
              "DO NOT UPDATE THIS FILE MANUALLY. If you're in a rebase right now and hit a conflict in this file, run the following:\n" \
              "`python manage.py rewritemigrations` and stage the changes to the file and proceed.\n\n"

    migration_order = '\n'.join(line[5:] for line in output.getvalue().split('\n'))

    new = preface + migration_order

    open(file_path, 'a').close()  # create if missing
    with open(file_path, 'r') as f:
        existing = f.read()
    if check and existing != new:
        raise Exception(".migration-order file needs updating")
    with open(file_path, 'w') as f:
        f.write(new)
