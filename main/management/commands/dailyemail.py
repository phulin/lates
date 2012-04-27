from django.core.management.base import NoArgsCommand
from django.core.urlresolvers import reverse
from django.core.mail import send_mail
from lates.main.models import Late
import datetime

class Command(NoArgsCommand):
    args = ''
    help = 'Send the daily lates email'
    
    def handle_noargs(self, **options):
        todays_lates = Late.objects.filter(request_date=datetime.date.today())

        subject = 'Daily lates for ' + str(datetime.date.today())
        message = 'Lates for:\n' + '\n'.join([ l.name for l in todays_lates ])
        from_addr = 'Auto-Late <phulin@mit.edu>'
        to_addrs = ['tepco@mit.edu']
        send_mail(subject, message, from_addr, to_addrs, fail_silently=False)
        self.stdout.write('Email sent.\n')
