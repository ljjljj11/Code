import smtplib
import csv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def read_target_list(file_path='mail_target_list.csv'):
    """CSV 파일에서 이름과 이메일을 읽어 리스트로 반환합니다."""
    target_list = []
    try:
        with open(file_path, mode='r', encoding='utf-8-sig') as file:
            reader = csv.DictReader(file)
            for row in reader:
                name = row.get('이름')
                email = row.get('이메일')
                if name and email:
                    target_list.append((name, email))
    except FileNotFoundError:
        print(f'❌ 파일을 찾을 수 없습니다: {file_path}')
    return target_list


def send_html_mail():
    """HTML 형식의 메일을 전체 또는 개별로 전송합니다."""
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587

    sender_email = input('보내는 Gmail 주소를 입력하세요: ')
    sender_password = input('앱 비밀번호를 입력하세요 (16자리): ')

    target_list = read_target_list()

    if not target_list:
        print('❌ 전송할 대상이 없습니다.')
        return

    html_body = (
        '<html>'
        '<body>'
        '<h2>기지로부터의 테스트 메일</h2>'
        '<p>이것은 <strong>SMTP</strong>를 이용한 자동 발신 메일입니다.<br>'
        '회신 여부를 확인합니다.</p>'
        '</body>'
        '</html>'
    )

    email_list = [email for _, email in target_list]

    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = ', '.join(email_list)
    message['Subject'] = '기지로부터의 HTML 테스트 메일'
    message.attach(MIMEText(html_body, 'html'))

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.ehlo()
            server.starttls()
            server.login(sender_email, sender_password)

            # 방법 1: 여러 수신자에게 한 번에 전송
            server.sendmail(
                sender_email,
                email_list,
                message.as_string()
            )
            print('✅ 전체 수신자에게 메일 전송 완료')

            # 방법 2: 한 명씩 반복하여 개별 전송
            print('\n📤 개별 전송 시작:')
            for name, email in target_list:
                personal_message = MIMEMultipart()
                personal_message['From'] = sender_email
                personal_message['To'] = email
                personal_message['Subject'] = f'{name}님께 보내는 HTML 메일'

                personalized_html = (
                    '<html>'
                    '<body>'
                    f'<h2>{name}님께</h2>'
                    '<p>이것은 <strong>SMTP</strong>를 이용한 자동 발신 메일입니다.<br>'
                    '회신 여부를 확인합니다.</p>'
                    '</body>'
                    '</html>'
                )

                personal_message.attach(MIMEText(personalized_html, 'html'))

                server.sendmail(
                    sender_email,
                    email,
                    personal_message.as_string()
                )
                print(f'✅ {name} ({email}) 전송 완료')

    except smtplib.SMTPAuthenticationError:
        print('❌ 인증 실패: 이메일 또는 앱 비밀번호를 확인하세요.')
    except smtplib.SMTPException as error:
        print('❌ 이메일 전송 실패:', error)
    except Exception as error:
        print('⚠️ 알 수 없는 오류 발생:', error)


if __name__ == '__main__':
    send_html_mail()
