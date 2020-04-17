
import smtplib
import textwrap

from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText 
from email.mime.base import MIMEBase 
from email import encoders 

import os
from pathlib import Path
from dotenv import load_dotenv

env_dir = Path(os.path.dirname(__file__)).parent
env_path = os.path.join(env_dir, '.env')
load_dotenv(dotenv_path=env_path)

def statusSwitch(statusType, receiversName):

    switcher = {

        # Confirmation of submission
        0:
        "Hello " + receiversName + ",\n"
        """
        We at SignSpotter would like to confirm 
        the success of your recent video submission.
        We will send you an email of the status of your
        submission once it is finished processing.
        Thank you for choosing SignSpotter for your
        road sign detection utility.

        Thank you again
        -Signspotter 

        signspotter.com
        """,

        # Successfully processed and signs found
        1:
        "Hello " + receiversName + ",\n"
        """
        We at SignSpotter would like to let you know
        your recently submitted video has finished being
        processed.Your Sign Detection Analysis is 
        ready for download. Also, please use the following 
        link to a map showcasing the detected signs.

        **[Link_to_map]**

        Thank you 
        -Signspotter 

        signspotter.com
        """,

        # Successfully processed and No Signs Detected
        3:
        "Hello " + receiversName + ",\n"
        """
        Your recent submission processed succseffully, however no 
        signs were detected. If you have any questions please 
        review our Q/A section.

        Thank You 
        -Signspotter 

        signspotter.com
        """,

        # Thank you after service is used
        4:
        "Hello " + receiversName + ",\n"
        """
        We at SignSpotter would like to thank you for using out service
        and hope your experience was satisfactory.

        again Thank You 
        -Signspotter 

        signspotter.com
        """,

        # Error: No GPS in video file
        5:
        "Hello " + receiversName + ",\n"
        """
        We at SignSpotter would like to inform you that the video(s) you
        submitted did not have properly encoded GPS data. Please verify
        your equipment and try again.

        Thank You 
        -Signspotter 

        signspotter.com
        """
    }
    return switcher.get(statusType, "Invalide Status!!!")


def emailSender(receivers, receiversName,  status):
    from email.mime.text import MIMEText
    SMTP_SERVER = "smtp.mail.yahoo.com"
    SMTP_PORT = 587
    SMTP_USERNAME = os.getenv('EMAIL_USER')
    SMTP_PASSWORD = os.getenv('EMAIL_PSWD')
    EMAIL_FROM = os.getenv('EMAIL_USER') + '@yahoo.com'
    EMAIL_SUBJECT = "SignSpotter: "
    EMAIL_TO = receivers

    # Population our message 
    msg = MIMEText(statusSwitch(status, receiversName))
    msg['Subject'] = EMAIL_SUBJECT + "Submission Status"
    msg['From'] = EMAIL_FROM 
    msg['To'] = EMAIL_TO
    debuglevel = True

    mail = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    mail.set_debuglevel(debuglevel)
    mail.starttls()
    mail.login(SMTP_USERNAME, SMTP_PASSWORD)
    mail.sendmail(EMAIL_FROM, EMAIL_TO, msg.as_string())
    mail.quit()


if __name__=='__main__':

    receiverList = ['signspotter@yahoo.com', 'jgreen.architect@gmail.com', 'luisgruiz@ufl.edu']
    
    receiverName = 'Jeremy Green'

    # 0 = Confirmation of submission
    # 1 = Successfully processed and signs found
    # 2 = Successfully processed and No Signs Detected
    # 3 = Thank you after service is used
    status = 0

    emailSender(receiverList[2], receiverName,  status)

