from django.db import models
import datetime

class Late(models.Model):
    name = models.CharField(max_length=200)
    request_date = models.DateField('Date requested', default=datetime.date.today)
    refrigerated = models.BooleanField('Refrigerated?')

    def is_today(self):
        return self.request_date == datetime.date.today()

    def __unicode__(self):
        return self.name

    def refrigerated_str(self):
        if self.refrigerated:
            return 'Refrigerated'
        else:
            return 'Unrefrigerated'

    def readable(self):
        return '%s (%s)' % (self.name, self.refrigerated_str())

    def to_dict(self):
        return {'id' : self.id,
                'name' : self.name,
                'refrigerated' : self.refrigerated}
