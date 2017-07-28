#######################################################
# tout ce qui est en relation avec l'envoi de mail
#######################################################

import smtplib
from email.mime.text import MIMEText

class Envoi_mail:

    #dictionnaire contennant les paramètres serveurs
    ParamMail = {
        'serveur' : 'localhost',
        'emmetteur' : ''

        }
    


    """ constructeur"""
    def __init__ (self,ParamMail):
        self.ParamMail = ParamMail


    def Envoyer_mail(self,sujet,corps_message,mail_a):

        un_message = MIMEText(corps_message)
        un_message['Subject'] = sujet
        un_message['From'] = self.ParamMail['emmetteur']
        un_message['To'] = mail_a

        un_envoi = smtplib.SMTP(self.ParamMail['serveur'])
        un_envoi.sendmail(self.ParamMail['emmetteur'],mail_a,un_message.as_string())
        un_envoi.quit()

        
