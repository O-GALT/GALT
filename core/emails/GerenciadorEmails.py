import smtplib
import  os
from email.message import EmailMessage

from core.essenciais import TipoUsuario

EMAIL = os.getenv('EMAIL')
SENHA = os.getenv('SENHA')


class GerenciadorEmails:
    def __init__(self):
        self.mensagem = EmailMessage()
        self.mensagem['Subject'] = 'Conta criada no GALT'
        self.mensagem['From'] = EMAIL

    def enviar_email(self, email_pessoal:str, email_escolar:str, senha:str, tipo_usuario: TipoUsuario):
        self.mensagem['To'] = email_pessoal
        self.mensagem.set_content(f'Acesso autorizado para o sistema GALT\nconta criada para {tipo_usuario}\nCredenciais:\nEmail: {email_escolar}\nSenha: {senha}')

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(EMAIL, SENHA)
            smtp.send_message(self.mensagem)
