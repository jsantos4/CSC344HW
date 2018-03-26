import os
import smtplib
import subprocess
import sys
import re
import shutil
import email
from os import listdir
from os.path import isfile, join
from email import encoders
from email.message import Message
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart 

path1 = '/home/jsantos4/Documents/csc344/'
files = [f for f in os.listdir(path1) if isfile(join(path1, f))]
files.sort()

def file_len(fname):    
    if os.path.isfile(fname):
        with open(fname) as f:
            for j, l in enumerate(f):
                pass
    return j + 1

def getIdentifiers(fname, path ):
    filepath = path + '/' + fname
    matcher = re.compile(r'\W+')
    nmatcher = re.compile(r'\d')
    identifiers = set()
    
    if(fname == 'hw01.c'):
        ignore = ['struct','include','stdio','h','a','if','else','nGoodbye','char','return','NULL','int','for','void','n','DIR','do','while','Enter','a','directory','name','Now','in','enter','quit','to','close','program','EOF','_']
        comment = '/'
        
    elif(fname == 'hw02.clj'):
        ignore = ['assignment2','main','use','micro','a2Micro','defn','if','default','fn','listProcessing','lp','nil']
        comment = ';'
        
    elif(fname == 'hw03.txt'):
        ignore = ['def','case','class','exit','no','string','String','var','val','pattern','StdIn','Parser','extends','import','scala','util','parsing','combinator','_','Any','Boolean','if','do','Some','None','io','b','c','d','g','h','i','j','k','m','n','o','p','q','s','u','v','w','x','y','z','do','while','true','false','abstract']
        comment = '/'
        
    elif(fname == 'hw04.txt'):
        ignore = ['is','r','u','d','_']
        comment = '%'
        
    elif(fname == 'hw05.py'):
        ignore = ['a','b','c','d','e','g','h','i','j','k','l','m','n','o','q','r','s','t','u','v','w','x','y','z','struct','include','stdio','if','else','nGoodbye','char','return','NULL','int','for','void','DIR','do','while','Enter','a','directory','name','Now','in','enter','quit','to','close','program','EOF','_','assignment2','main','use','micro','a2Micro','defn','if','default','fn','listProcessing','lp','nil''is','def','case','class','exit','no','string','String','var','val','pattern','StdIn','Parser','extends','import','scala','util','parsing','combinator','Any','Boolean','if','do','Some','None','io','Doctype','a1','a2','a3','a4','a5','meta','content','Tyler','Moson','CSC','Summary','summary','li','Assignment','ul','body','h1','h2','Files','Identifiers','href','not','and','utf','equiv','title','lines','as','with','in','for','W','re','os','listdir','sys','Subject','From','from','zipfile','tempfile','smtplib','I','am','using','MIME','aware','reader','application','attatchement','Content','Disposition','To','home','tyler','projects','csc','Assignments','MegaMan3','Please','enter','a1_summary','a2_summary','a3_summary','a4_summary','a5_summary','ozcsc344','Frickin','Scala','Clojure','C','Python','MIMEBase','MIMEMultipart','mime','base','tempfile','message','Message','Beams','Laser','div','an','edu','com','gmail','nil','is','http','type','Summaries','csc344','container',]
        comment = '#'
        
    with open(filepath, 'r') as searchfile:
        for line in searchfile:
            text = line.strip()
            if (len(text) > 0 and text[0] != comment):
                strings = matcher.split(text)
                for string in strings:
                    if (not nmatcher.match(string)) and (string not in ignore):
                        identifiers.add(string)
                        
    for identifier in identifiers:
        if identifier == "'":
            identifiers.remove(identifier)
    return identifiers
            

cIds = list(getIdentifiers('hw01.c', path1))
cljIds = list(getIdentifiers('hw02.clj', path1))
sclIds = list(getIdentifiers('hw03.txt', path1))
prlgIds = list(getIdentifiers('hw04.txt', path1))
pyIds = list(getIdentifiers('hw05.py', path1))

shutil.make_archive('outzip', 'zip', path1)


html = open('index.html', 'w')

html05 = '''
<html>
<head></head>
<body><p>Index</p></body>
<a href=hw01.c>HW01</a>
<a href=hw02.clj>HW02</a>
<a href=hw03.txt>HW03</a>
<a href=hw04.txt>HW04</a>
<a href=hw05.py>HW05</a>
<a href=Symbols.txt>Symbols</a>
</html>
'''
html.write(html05)



symbols = open('Symbols.txt', 'w')

text ='''--------------------HW01---------------------
Lines: ''' + str(file_len('hw01.c')) + '''
Identifiers: '''
for i in cIds:
    text = text + i + '\n'
    
text = text + '''
--------------------HW02---------------------
Lines: ''' + str(file_len('hw02.clj')) + '''
Identifiers: '''
for i in cljIds:
    text = text + i + '\n'

text = text + '''
--------------------HW03---------------------
Lines: ''' + str(file_len('hw03.txt')) + '''
Identifiers: '''
for i in sclIds:
    text = text + i + '\n'

text = text + '''
--------------------HW04---------------------
Lines: ''' + str(file_len('hw04.txt')) + '''
Identifiers: ''' 
for i in prlgIds:
    text = text + i + '\n'

text = text + '''
--------------------HW05---------------------
Lines: ''' + str(file_len('hw05.py')) + '''
Identifiers: '''
for i in pyIds:
    text = text + i + '\n'


symbols.write(text)
symbols.close()
html.close()
recieving = raw_input(' To: ')

message = MIMEMultipart()
message['Subject'] = 'Zipped Assignments'
message['To'] = recieving
message['From'] = 'jsantos4@oswego.edu'
message.preamble = 'Find attached assignments 1-4 in a compressed folder. /n'

attachment = MIMEBase('application', 'zip')
attachment.set_payload(open(path1 + 'outzip.zip', 'rb').read())
encoders.encode_base64(attachment)

message.attach(attachment)
message = message.as_string()

email = 'jsantos4@oswego.edu'
password = raw_input('Password: ')

server = smtplib.SMTP('smtp.gmail.com', 587)
server.ehlo()
server.starttls()
server.login(email, password)
server.sendmail(email, 'super5t4rSANTS@gmail.com', message)
server.close

