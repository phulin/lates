from django.core.management.base import NoArgsCommand
from lates.main.models import Late
from email.parser import Parser
import sys

# Automatically process late emails sent in through Procmail

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
        if 'late' in s and not ('be late' in s or 'minutes late' in s or 'late dinner' in s or 'later' in s or 'late notice' in s or 'late by' in s):
            self.stderr.write('late email!\n')
            if 'dnr' in s or 'unrefrigerate' in s or 'not refrigerate' in s:
                refrigerated = False
            else:
                refrigerated = True
            late = Late(name=message['from'], refrigerated=refrigerated)
            late.save()
            self.stderr.write('  saved successfully we think!\n')
