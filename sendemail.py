import smtplib
class SendEmail:
    email = "popeyeapisite@gmail.com"
    password = "jyppgszdnpnrincl"
    def send_email(self, recipients, body):
        try:
            smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', port=465)
            smtp_server.login(self.email, self.password)
            smtp_server.sendmail(self.email, recipients, body)
            smtp_server.quit()
            print("Send Successfully!!!")
            return True
        except Exception:
            print("Error in Sending!!!!!")
            return False

if __name__ == "__main__":
    send = SendEmail()