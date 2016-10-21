from django.db import models

class Location(models.Model):
    entity_id = models.IntegerField()
    entity_type = models.CharField(max_length=100, help_text='Entity Type')
    address = models.CharField(max_length=100, default='', help_text='Address')
    lat = models.FloatField(help_text='Lattitude')
    lon = models.FloatField(help_text='Longitude')
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return unicode(self.pk)

    class Meta:
        ordering = ('-modified',)

