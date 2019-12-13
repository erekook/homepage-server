import smtplib
from email import encoders
from email.mime.text import MIMEText
from email.header import Header
from email.utils import parseaddr, formataddr

class EmailUtil():
    def __init__(self, receiver):
        self.sender = "tlj122@126.com"
        self.receiver = receiver

    # 发送邮箱验证码
    def send_email_code(self,code):
        msg = MIMEText('您好，您的验证码是 %s' % code, 'plain', 'utf-8')
        msg['From'] = self._format_addr(self.sender)
        msg['To'] = self._format_addr(self.receiver)
        msg['subject'] = Header('LONGJIE LOGIN', 'utf-8').encode()
        try:
            self.server = smtplib.SMTP_SSL("smtp.126.com", 465)
            self.server.set_debuglevel(1)
            self.server.login(self.sender, "TLJaiziji122")
            self.server.sendmail(self.sender, [self.receiver], msg.as_string())
        except exception:
            print(exception)
        finally:
            self.server.quit()

    def _format_addr(self,s):
        name, addr = parseaddr(s)
        return formataddr((Header(name, 'utf-8').encode(), addr))
