from django.db import models

# TODO: Question: Should there be two tables? raw and embedded? 
class Artifact(models.Model):
    # TODO: Add fields for full_entry
    title = models.CharField(max_length=50, default='None')
    description = models.TextField(default='None')
    descriptionWC = models.PositiveIntegerField(default=0)
    description_cleaned = models.TextField(default='None')
    description_tokenized = models.TextField(default='None')
    embed_raw = models.FloatField(default=0.0)

    def __str__(self):
        return str(self.id)