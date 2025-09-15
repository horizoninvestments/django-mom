from django.core.management.commands import makemigrations
from django_mom.migration_utils import write_migration_order


class Command(makemigrations.Command):
    def handle(self, *app_labels, **options):
        if options.get("merge"):
            print(
                "WARNING: Using --merge is discouraged. Instead, adjust your branch's new migration "
                "dependencies to follow the latest migrations from the other branch to avoid conflicts.\n\n"
                "To do so, run `./do manage rewritemigrations` and identify the leaf nodes in the error "
                "output with conflicting migrations. Typically, these come in pairs per app: one which "
                "represents the latest migration from your branch, and one which is the latest from the "
                "branch you're rebasing onto or merging from\n\n"
                "For each app with migration conflicts, run:\n"
                "`git diff [rebase/merge target] -- [appname]/migrations/`\n\n"
                "The migrations that appear in that output are the ones your branch added. "
                "Open the first new migration your branch added and update its dependencies to point to the latest "
                "leaf node from the other branch (found in the earlier output from `rewritemigrations`).\n\n"
                "If you're feeling extra diligent, update the numbering of your branch's migrations to follow after "
                "the newly rebased/merged migrations and adjust their dependencies accordingly.\n\n"
                "Once your conflicts have been resolved, re-run `python manage.py rewritemigrations` and "
                "commit the changes.\n\n"
                "If you really need a merge migration, type:\n"
                "'I really need a merge migration'"
            )

            confirmation = input("Type your response here: ")

            if confirmation != "I really need a merge migration":
                print("Aborted: Merge migration not confirmed.")
                return

        super().handle(*app_labels, **options)

        if not options.get("check_changes"):
            write_migration_order(".migration-order")
