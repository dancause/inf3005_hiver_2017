# coding: utf8

import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from os.path import exists


def message_courriel(destination, token, body, subject):
    fichier = open("info_courriel.txt")
    source = fichier.readline()
    motpasse = fichier.readline()
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = source
    msg['To'] = destination
    msg.attach(MIMEText(body, 'html'))
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(source, motpasse)
    text = msg.as_string()
    server.sendmail(source, destination, text)
    server.quit()
