# django-mom (migration order manager)

**django-mom** piggybacks on the existing `makemigration` command to put the authoritative order of migrations into the source code in the form of a file called **.migration-order**. This plaintext file gets automatically updated with the full migration order when new migrations are created, so you get explicit conflicts in git pre-merge instead of surprise failures in the CI or production build after merging, allowing you to resolve them gracefully before they become a problem.

## Install
```bash
pip install django-mom
```

Enable the app:
```python
# settings.py
INSTALLED_APPS = [
    # ...
    "django_mom",
]
```

## Commands
- **makemigrations** (standard Django): create migrations; **django-mom** updates **.migration-order**.
- **rewritemigrations**: after choosing an order (e.g., resolving a merge/rebase conflict), rewrite the **.migration-order** file.

## Typical workflow

### Creating new migrations
```bash
python manage.py makemigrations
git add */migrations/*.py .migration-order # make sure to commit this!
git commit -m "your commit message"
```

### Rebase / merge a branch that also touched migrations
- If Git shows conflicts in **.migration-order**, edit the migration dependencies in the conflicting source branch migration files until the order is what you intend.
- Then align the dependency graph:
```bash
python manage.py rewritemigrations
git add */migrations/*.py .migration-order # don't forget!
git commit -m "rewrite migration deps to match .migration-order"
```

Remember: always commit changes to **.migration-order** and never manually resolve conflicts. Use `rewritemigrations` if you have altered the migration order and want it reflected in `.migration-order`.
