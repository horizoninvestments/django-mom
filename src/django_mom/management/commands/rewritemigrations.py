from django.core.management.base import BaseCommand
from django_mom.migration_utils import write_migration_order


class Command(BaseCommand):
    help = "Write the current migration order to a file"

    def add_arguments(self, parser):
        parser.add_argument(
            '--check',
            action='store_true',
            help='Check if the migration order file is up to date without writing changes.'
        )

    def handle(self, *app_labels, **options):
        check = options.get('check', False)
        write_migration_order(".migration-order", check=check)
