import smtplib
from email.message import EmailMessage

EMAIL = 'o.galtsystem@gmail.com'
SENHA = 'uwhc izlc ugof eosz'

class GerenciadorEmails:
    @staticmethod
    def enviar_email(email_pessoal:str, email_escolar:str, senha:str, tipo_usuario):
        mensagem = EmailMessage()
        mensagem['Subject'] = 'Conta criada no GALT'
        mensagem['From'] = EMAIL

        mensagem['To'] = email_pessoal
        mensagem.set_content(f'Acesso autorizado para o sistema GALT\nconta criada com nível de acesso de: {[tipo for tipo in tipo_usuario]}\nCredenciais:\nEmail: {email_escolar}\nSenha: {senha}')

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(EMAIL, SENHA)
            smtp.send_message(mensagem)

    @staticmethod
    def enviar_email_fechamento_report(email_pessoal, email_escolar):
        mensagem = EmailMessage()
        mensagem['Subject'] = 'Reporte fechado!'
        mensagem['From'] = EMAIL

        mensagem['To'] = email_pessoal
        mensagem.set_content(
            f'{email_escolar}, O equipamento que você reportou com mau funcionamento já foi reparado e encontra-se novamente em operação. Agradecemos pelo registro da ocorrência.')

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(EMAIL, SENHA)
            smtp.send_message(mensagem)
