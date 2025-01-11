from django.db import models

class Batch(models.Model):
    id = models.AutoField(primary_key=True)
    batchName = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)
    batchStatus = models.BooleanField("Batch Status", default=True)
    createdAt = models.DateTimeField("Created At", auto_now_add=True)
    batchIncharge = models.ForeignKey("Teacher", on_delete=models.SET_NULL, null=True, blank=True, related_name='batches')

    def __str__(self):
        return self.batchName