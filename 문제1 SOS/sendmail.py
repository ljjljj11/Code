import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def send_email():
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587

    sender_email = input('보내는 Gmail 주소를 입력하세요: ')
    sender_password = input('앱 비밀번호를 입력하세요 (16자리): ')
    receiver_email = input('받는 사람 이메일 주소를 입력하세요: ')

    subject = '기지로부터의 테스트 메일'
    body = '이것은 SMTP를 이용한 자동 발신 메일입니다. 회신 여부를 확인합니다.'

    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = receiver_email
    message['Subject'] = subject
    message.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.ehlo()
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(
                sender_email,
                receiver_email,
                message.as_string()
            )
            print('✅ 이메일 전송 성공!')
    except smtplib.SMTPAuthenticationError:
        print('❌ 인증 실패: 이메일 또는 앱 비밀번호를 확인하세요.')
    except smtplib.SMTPException as error:
        print('❌ 이메일 전송 실패:', error)
    except Exception as error:
        print('⚠️ 알 수 없는 오류 발생:', error)


if __name__ == '__main__':
    send_email()
