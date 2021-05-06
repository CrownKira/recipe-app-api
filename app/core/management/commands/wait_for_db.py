import time

from django.db import connections
from django.db.utils import OperationalError
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Django command to pause execution until database is available"""

    def handle(self, *args, **options):
        # print to the screen
        self.stdout.write("Waiting for database...")
        db_conn = None
        while not db_conn:
            try:
                # assign connections["default"] to db_conn
                # if connections["default"] not available, will raise error ?
                # connections is a dictionary
                db_conn = connections["default"]
            except OperationalError:
                self.stdout.write("Database unavailable, waiting 1 second...")
                time.sleep(1)

        self.stdout.write(self.style.SUCCESS("Database available!"))
