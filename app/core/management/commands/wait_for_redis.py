from django.core.management.base import BaseCommand
import time
from django.db.utils import OperationalError
import redis


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        self.stdout.write("Waiting for redis")
        db_up = False
        while db_up is False:
            try:
                r = redis.StrictRedis(
                    host='redis',
                    port=6379,
                    decode_responses=True
                )
                r.set("message", "Redis is connected")
                db_up = True
            except OperationalError:
                self.stdout.write("redis unavailable...!")
                time.sleep(1)
            self.stdout.write(self.style.SUCCESS("Redis is connected"))
