from django.db import models

# TODO: Question: Should there be two tables? raw and embedded? 
class Artifact(models.Model):
    # TODO: Add fields for full_entry
    title = models.CharField(max_length=50)
    description = models.TextField()
    descriptionWC = models.PositiveIntegerField()
    description_cleaned = models.TextField()
    description_tokenized = models.TextField()
    embed_raw = models.FloatField()

    def __str__(self):
        return str(self.id)