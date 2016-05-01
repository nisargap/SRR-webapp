__author__ = 'Cody Giles'
__license__ = "Creative Commons Attribution-ShareAlike 3.0 Unported License"
__version__ = "1.0"
__maintainer__ = "Cody Giles"
__status__ = "Production"

from subprocess import *
import smtplib
from email.mime.text import MIMEText
import datetime

def connect_type(word_list):
    """ This function takes a list of words, then, depeding which key word, returns the corresponding
    internet connection type as a string. ie) 'ethernet'.
    """
    if 'wlan0' in word_list or 'wlan1' in word_list:
        con_type = 'wifi'
    elif 'eth0' in word_list:
        con_type = 'ethernet'
    else:
        con_type = 'current'

    return con_type

# Change to your own account information
# Account Information
to = 'sumanth42gold@gmail.com' # Email to send to.
gmail_user = 'sumanth42gold@gmail.com' # Email to send from. (MUST BE GMAIL)
gmail_password = 'enterPasswordHere' # Gmail password.
smtpserver = smtplib.SMTP('smtp.gmail.com', 587) # Server to use.

smtpserver.ehlo()  # Says 'hello' to the server
smtpserver.starttls()  # Start TLS encryption
smtpserver.ehlo()
smtpserver.login(gmail_user, gmail_password)  # Log in to server
today = datetime.date.today()  # Get current time/date

arg='ip route list'  # Linux command to retrieve ip addresses.
# Runs 'arg' in a 'hidden terminal'.
p=Popen(['ip route list'],shell=True,stdout=PIPE,stderr=PIPE)
p.wait()
data = p.communicate()  # Get data from 'p terminal'.

# Split IP text block into three, and divide the two containing IPs into words.
fullResponse = ""
ifconfigResponse = ""

for i in data[0].split('\n'):
    fullResponse = fullResponse + str(i) + '\n'

arg = 'ifconfig'
q =Popen(['ifconfig'],shell=True,stdout=PIPE,stderr=PIPE)
q.wait()
secondData = q.communicate()


for i in secondData[0].split('\n'):
    ifconfigResponse = ifconfigResponse + str(i) + '\n'

# con_type variables for the message text. ex) 'ethernet', 'wifi', etc.

"""Because the text 'src' is always followed by an ip address,
we can use the 'index' function to find 'src' and add one to
get the index position of our ip.
"""

# Creates a sentence for each ip address.

# Creates the text, subject, 'from', and 'to' of the message.
msg = MIMEText( fullResponse + "\n" + ifconfigResponse)
msg['Subject'] = 'IPs For RaspberryPi on %s' % today.strftime('%b %d %Y')
msg['From'] = gmail_user
msg['To'] = to
# Sends the message
smtpserver.sendmail(gmail_user, [to], msg.as_string())
# Closes the smtp server.
smtpserver.quit()
