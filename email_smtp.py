from smtplib import SMTP
from email.message import Message

def enviar_email(assunto, origem, destino, corpo_email):
    
    try:

        msg = Message()
    
        msg['Subject'] = assunto
        msg['From'] = origem
        msg['To'] = destino
        
        password = 'senha' # senha de app do google cadastrada para o email de origem
        
        msg.add_header('Content-Type', 'text/html')
        msg.set_payload(corpo_email)

        s = SMTP('smtp.gmail.com: 587')
        
        s.starttls()

        s.login(msg['From'], password)
        
        s.sendmail(msg['From'], [msg['To']], msg.as_string().encode('utf-8'))
        
        print("email enviado")

    except Exception as e:
        print(e)

    finally:
        s.quit() # fecha a conexão com o servidor