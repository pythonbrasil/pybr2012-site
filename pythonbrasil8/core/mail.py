# -*- coding: utf-8 -*-
import threading

from django.core import mail


class MailSender(object):

    def __init__(self, sender, receivers, subject, body):
        self.sender = sender
        self.receivers = receivers
        self.subject = subject
        self.body = body

    def send_mail(self):
        kw = {
            "subject": self.subject,
            "message": self.body,
            "recipient_list": self.receivers,
            "from_email": self.sender,
            "fail_silently": True,
        }
        self.t = threading.Thread(target=mail.send_mail, kwargs=kw)
        self.t.start()

    def wait(self, timeout=None):
        if timeout is None:
            self.t.join()
            return True
        self.t.join(timeout)
        return not self.t.isAlive()


def send(sender, receivers, subject, body):
    m = MailSender(sender, receivers, subject, body)
    m.send_mail()
    return m
