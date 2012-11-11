#!/usr/bin/env python
# coding: utf-8

import getpass
import smtplib
import sys
import time

from pythonbrasil8.schedule.models import Session


remetente = u'"Organização PythonBrasil[8]" <organizacao@python.org.br>'
msg = u'''Subject: Confirmação de palestra: "{PALESTRA}"
From: {REMETENTE}
To: {EMAIL}

Olá,

Parabéns! A palestra abaixo foi aprovada na PythonBrasil[8]:
    {PALESTRA}

Em breve enviaremos dia e horário da palestra.

Necessitamos da confirmação dessa palestra no evento - para isso, basta
responder a esse email com "sim" ou "não".

Lembramos que sua inscrição no evento será confirmada quando o pagamento for
efetuado (o valor promocional para palestrantes é de R$ 150,00).  Pedimos a
gentileza que verifique o estado de sua inscrição em:
    http://2012.pythonbrasil.org.br/dashboard/

Em caso de dúvidas, por favor, entre em contato com o time da organização do
evento através do email <organizacao@python.org.br>.

Até breve!

Atenciosamente,
  Organização PythonBrasil[8]
  http://2012.pythonbrasil.org.br
  http://twitter.com/PythonBrasil
  http://facebook.com/pythonbrasil8'''


class EmailConnection(object):
    def connect(self, smtp_host, smtp_port):
        self.connection = smtplib.SMTP(smtp_host, smtp_port)
        self.connection.ehlo()
        self.connection.starttls()
        self.connection.ehlo()

    def auth(self, username, password):
        self.connection.login(username, password)

    def send_mail(self, from_, to, message):
        return self.connection.sendmail(from_, to, message)

    def close(self):
        self.connection.close()


if __name__ == '__main__':
    smtp_host = 'smtp.gmail.com'
    smtp_port = 587
    #username = raw_input('Digite o username do email: ')
    username = 'organizacao@python.org.br'
    password = getpass.getpass('Digite a senha para <{}>: '.format(username))

    email_connection = EmailConnection()
    email_connection.connect(smtp_host, smtp_port)
    email_connection.auth(username, password)

    i = 0
    for session in Session.objects.filter(type='talk', status='accepted'):
        speakers = session.speakers.all()
        emails = [speaker.email for speaker in speakers]

        a_substituir = {u'EMAIL': u','.join(emails), u'REMETENTE': remetente,
                        u'PALESTRA': session.title}
        mensagem = msg
        for key, value in a_substituir.iteritems():
            mensagem = mensagem.replace(u'{' + key + u'}', value)
        mensagem = mensagem.encode('utf-8')

        i += 1
        sys.stdout.write(u'Enviando email {:02d} sobre "{}" para <{}> ...  '\
                         .format(i, session.title, emails).encode('utf-8'))
        response = email_connection.send_mail(remetente, emails, mensagem)
        print 'OK' if response == {} else response
        time.sleep(1)

    email_connection.close()
