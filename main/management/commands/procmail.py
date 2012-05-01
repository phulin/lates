from django.core.management.base import NoArgsCommand
from lates.main.models import Late
from email.parser import Parser
import sys, re

# Automatically process late emails sent in through Procmail
invalid = ['plate', 'be late', 'minutes late', 'late dinner', 'later', 'late notice', 'late by']

class Command(NoArgsCommand):
    args = ''
    help = 'Process incoming mail'

    def handle_noargs(self, **options):
        message = Parser().parse(sys.stdin)

        if 'Auto-Late' in message['from']: return
        if not ('tepco' in message['to'] or 'tep-haus-fud' in message['to']):
            self.stderr.write('Not to tepco: ' + message['to'] + '\n')
            # return
        if message.is_multipart():
            contents = ''
            self.stderr.write('multipart!\n')
            for part in message.walk():
                if part.get_content_type() == 'text/plain':
                    contents = part.get_payload()
                    break
        else:
            contents = message.get_payload()

        s = message['subject'] + '\n' + contents
        s = s.lower()
        sep = '\n' + '-' * 10 + '\n'
        # self.stderr.write(sep + s + sep)
        s = '\n'.join(filter(lambda l: not l.startswith('>'), s.splitlines()))
        if 'late' in s and not ('plate' in s or 'be late' in s or 'minutes late' in s or 'late dinner' in s or 'later' in s or 'late notice' in s or 'late by' in s):
            self.stderr.write('late email!\n')
            if 'dnr' in s or 'unrefrigerate' in s or 'not refrigerate' in s:
                self.stderr.write('unrefrigeration detected\n')
                refrigerated = False
            else:
                refrigerated = True
            late = Late(name=message['from'], refrigerated=refrigerated)
            late.save()
            sep2 = '\n' + '-' * 20 + '\n'
            self.stderr.write('  saved successfully we think!\n' + sep2)
