
import smtplib

from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText 
from email.mime.base import MIMEBase 
from email import encoders 


# fromaddr = "from@domain.com"
fromaddr = "signspotter"
toaddr = "luisgruiz@ufl.edu"

def emailSender(filename):
   
    # instance of MIMEMultipart 
    msg = MIMEMultipart()
    
    # storing the senders email address   
    msg['From'] = 'signspotter@yahoo.com'
    
    # storing the receivers email address  
    msg['To'] = 'luisgruiz@ufl.edu'
    
    # storing the subject  
    msg['Subject'] = "SignSpotter : Submission Status Report"
    
    # string to store the body of the mail 
    body = "Hello user"
    
    # attach the body with the msg instance 
    msg.attach(MIMEText(body, 'plain')) 
    




    # open the file to be sent  
    # filename = "Email.txt"
    attachment = open(filename, "rb") 
    
    # Instance of MIMEBase named as payload 
    payload = MIMEBase('application', 'octet-stream') 
    
    # Encoding the payload
    payload.set_payload((attachment).read()) 
    
    # Encoding the payload into base64 
    encoders.encode_base64(payload) 
    
    payload.add_header('Content-Disposition', "attachment; filename= %s" % filename) 
    
    # Attaching the instance of the 'payload' to the instance of the 'msg'
    msg.attach(payload) 
    
    # Creating SMTP session 
    # stmp = smtplib.SMTP('smtp.yahoo.com', 587) 
    stmp = smtplib.SMTP('imap.mail.yahoo.com', 587) 
    
    # start security 
    stmp.starttls() 
    
    # Authentication 
    stmp.login(fromaddr, "password) 
    
    # Converts the Multipart msg into a string 
    text = msg.as_string() 
    
    # sending the mail 
    stmp.sendmail(fromaddr, toaddr, text) 
    
    # terminating the session 
    stmp.quit() 

if __name__ == '__main__':


   emailSender("/home/lil-as/sign-spotter/backend/Emailfiles/Email.txt")