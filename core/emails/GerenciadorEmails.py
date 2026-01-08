import smtplib
import  os
from email.message import EmailMessage

EMAIL = os.getenv('EMAIL')
SENHA = os.getenv('SENHA')

class GerenciadorEmails:
    @staticmethod
    def enviar_email(email_pessoal:str, email_escolar:str, senha:str, tipo_usuario):
        mensagem = EmailMessage()
        mensagem['Subject'] = 'Conta criada no GALT'
        mensagem['From'] = EMAIL

        mensagem['To'] = email_pessoal
        mensagem.set_content(f'Acesso autorizado para o sistema GALT\nconta criada com nível de acesso de: {[tipo.name for tipo in tipo_usuario.all()]}\nCredenciais:\nEmail: {email_escolar}\nSenha: {senha}')

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(EMAIL, SENHA)
            smtp.send_message(mensagem)
