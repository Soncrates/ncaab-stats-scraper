import csv
import smtplib
from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formatdate
import logging as log

class CLIENTS :

    @staticmethod
    def load(**arg) :
        fields = []
        rows = []
        ret = arg.get('filename',"email.csv")
        with open(ret, 'r') as csvfile:
            csvreader = csv.reader(csvfile)
            fields = next(csvreader)
            for row in csvreader:
                row = dict(zip(fields,row))
                rows.append(row)
        return rows

    @staticmethod
    def personalize(message,**args) :
        ret = message.format(**args).encode('ascii','ignore')
        log.debug(ret)
        return ret

    @staticmethod
    def _transform(_from, subject, *client_list) :
        default = {"FROM": _from}
        for client in client_list:
            default['TO'] = client['user_email']
            default['SUBJECT'] = subject.format(**client)
            client.update(default)
            log.debug(client)
            yield client

    @staticmethod
    def transform(SenderAddress,subject,body,*client_list) :
        for client in CLIENTS._transform(SenderAddress,subject,*client_list):
            msg = CLIENTS.personalize(body, **client)
            yield client["FROM"], client["TO"], client["SUBJECT"],msg

class EMAIL :

    @staticmethod
    def add_attachments(text,*file_list) :
        ret = MIMEMultipart()
        ret['Date'] = formatdate(localtime=True)
        if isinstance(text,bytes) :
            text = text.decode()
        ret.attach(MIMEText(text))
        for part in EMAIL.find_attachments(*file_list) :
            ret.attach(part)
        log.debug(ret)
        return ret
    @staticmethod
    def find_attachments(*file_list) :
        for f in file_list or []:
            with open(f, "rb") as fil:
                part = MIMEApplication(
                    fil.read(),
                    Name=basename(f)
                )
            # After the file is closed
            part['Content-Disposition'] = 'attachment; filename="%s"' % basename(f)
            yield part
    @staticmethod
    def gmail(**args) :
        user = args.get("user")
        pswd = args.get("pswd")
        ret = smtplib.SMTP("smtp.gmail.com", 587)
        ret.starttls()
        ret.login(user, pswd)
        return ret
