#!/usr/bin/python

# This script will define an automated email function
import sendgrid

def send_email():
    sg = sendgrid.SendGridClient('hophacks14', 'hopkins13')

    message = sendgrid.Mail()
    message.add_to('Henry Lessen <aggiefan13@gmail.com>')
    message.set_subject('Job Complete')
    alert = '''
Dear Valued Individual,

This is an automatic message to show that the job you submitted 
to the remote version of <insert name here>.  The files generated are
attached to the email.  Have a great day and stay classy San Diego.

Sincerely,
Someone who cares
'''
    message.set_text(alert)
    message.set_from('Henry Lessen <leknerchief13@gmail.com>')
    message.add_attachment('./sendgrid.txt')
    sg.send(message)
    return

