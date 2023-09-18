"""
Django command to wait for database available
"""

import time
from psycopg2 import OperationalError as psycopg2Error
from django.db.utils import OperationalError
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Django command wait for database"""

    def handle(self, *args, **kwargs):
        """Entrypoint for command"""
        self.stdout.write("Waiting for Database")
        db_up = False
        while db_up is False:
            try:
                self.check(databases=['default'])
                db_up = True
            except (psycopg2Error, OperationalError):
                self.stdout.write("Database unavailable...!")
                time.sleep(1)
        self.stdout.write(self.style.SUCCESS("DB is connected"))
