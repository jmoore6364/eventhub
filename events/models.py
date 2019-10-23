from django.db import models

class Event(models.Model):
    def __str__(self):
        return self.name
    event_id = models.IntegerField()
    name = models.CharField(max_length=120, db_index=True)
    summary = models.TextField()
    description = models.TextField()
    url = models.CharField(max_length=400)
    start = models.DateTimeField(db_index=True)
    end = models.DateTimeField()
    created = models.DateTimeField()
    changed = models.DateTimeField()
    published = models.DateTimeField()
    status = models.CharField(max_length=15)
    organizer = models.CharField(max_length=200, db_index=True)
    cost = models.DecimalField(max_digits=6, decimal_places=2, db_index=True)

    class meta:
        index_together = [
            ['name', 'start', 'cost', 'organizer']
        ]