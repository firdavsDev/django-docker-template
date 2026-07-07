import yaml
from django.core.management.base import BaseCommand, CommandError

from ...models import User


class Command(BaseCommand):
    help = "Import users from a yaml file"

    def add_arguments(self, parser):
        parser.add_argument(
            "--delete",
            action="store_true",
            help="Delete all existing users before importing",
        )

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.HTTP_NOT_MODIFIED(
                "Import users... wait...",
            )
        )
        if options["delete"]:
            deleted, _ = User.objects.all().delete()
            self.stdout.write(self.style.WARNING(f"{deleted} existing users deleted"))
        try:
            with open(
                "src/apps/common/fixtures/users.yml",
            ) as yaml_file:
                data = yaml.safe_load(yaml_file)
                i = 0
                for item in data:
                    User.objects.create_user(
                        email=item["fields"]["email"],
                        password=item["fields"]["password"],
                        role=item["fields"]["role"],
                    )
                    i += 1
        except FileNotFoundError as e:
            raise CommandError("File users yaml doesn't exists") from e

        self.stdout.write(self.style.SUCCESS(f"{str(i)} users successfully imported"))
