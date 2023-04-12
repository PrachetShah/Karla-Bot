# !pip install email_listener
# !pip install sentence-transformers

import email_listener
import re
import nltk
# nltk.download('all')
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer,WordNetLemmatizer
wl=WordNetLemmatizer()

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from decouple import config

API_KEY = config('KEY')

## Subject Checker
sub_keywords=['Rental','Lease','Condo Rental','Unit For Lease','Rental Unit','Condo for Rent', 'buy', 'property', 'application']  ## STD

## Preprocessing
corpus=[]
for i in range(0,len(sub_keywords)):
    sent=re.sub('[^a-zA-Z0-9]',' ',sub_keywords[i])
    sent=sent.lower()
    sent=sent.split()
    sent=[wl.lemmatize(word) for word in sent if word not in set(stopwords.words('english'))]
    sent=' '.join(sent)
    corpus.append(sent)
# print(corpus)

## Flag Model
from sklearn.metrics.pairwise import cosine_similarity
def subject_flag_sys_(x,y):
  sbert_model = SentenceTransformer('bert-base-nli-mean-tokens') #SentenceBERT
  sentence_embeddings1 = sbert_model.encode(x)
  sentence_embeddings2 = sbert_model.encode(y)
  for i in sentence_embeddings1:
    return cosine_similarity(sentence_embeddings1,sentence_embeddings2)



sub=['documents for a buying house']
def sub_lead_or_not(sub):
  op=[]
  corpus_ot=[]
  for i in range(0,len(sub)):
      sent=re.sub('[^a-zA-Z0-9]',' ',sub[i])
      sent=sent.lower()
      sent=sent.split()
      sent=[wl.lemmatize(word) for word in sent if word not in set(stopwords.words('english'))]
      sent=' '.join(sent)
      corpus_ot.append(sent)
  # print(corpus_ot)

  for i in subject_flag_sys_(corpus,sub):
    if i >=0.60:
      op.append(1)
    else:
      op.append(0)
  # print(op)

  if sum(op) >= 2:
    print('Lead')
    return True
  else:
    print('Not Lead')
    return False

# print(sub_lead_or_not(sub))

## BODY 

body_keyword=['''Hi Kanika, please find attached my documents for 506 loury. We would like to book a viewing as soon as possible. Thank you.
              I just spoke to you on chat. It is me, John Doe. Please find my documents for the unit we have discussed. I look forward to booking a viewing.
              I would like to rent the condo for August 1st, how can we proceed? See attached the documents. thanks.
              Hey Agent,I atteched the documents you required, please let me know aything you want further
              It was nice chatting with you over chat. Here are my requested files.My credit score is somewhat lower because of an unpaid Gym Membership, it should be higher than that in reality.
              If you have any questions please let me know and I will clarify. I look forward to moving quickly forward on the LakeShore unit. Thank you,Client
              See attached my Drivers and Credit Report. What do next steps look like?'''] #STD

## Body Preprocessing
std_body=[]

for i in range(0,len(body_keyword)):
    sent=re.sub('[^a-zA-Z 0-9]',' ',body_keyword[i])
    sent=sent.lower()
    sent=sent.split()
    sent=[wl.lemmatize(word) for word in sent if word not in set(stopwords.words('english'))]
    sent=' '.join(sent)
    std_body.append(sent)

## Flag Model
def body_flag(x,y):
  sbert_model = SentenceTransformer('bert-base-nli-mean-tokens') #SentenceBERT
  sentence_embeddings1 = sbert_model.encode(x)
  sentence_embeddings2 = sbert_model.encode(y)
  return (cosine_similarity(sentence_embeddings1,sentence_embeddings2))

sent3=['''hi kanika please find attached document 506 loury would like book viewing soon possible''']

def body_lead_or_not(sent3):
  output=[]
  for i in range(0,len(sent3)):
        senty=re.sub('[^a-zA-Z 0-9]',' ',sent3[i])
        senty=senty.lower()
        senty=senty.split()
        senty=[wl.lemmatize(word) for word in senty if word not in set(stopwords.words('english'))]
        senty=' '.join(senty)
        output.append(senty)


  body_flag(std_body,output)

  for i in body_flag(std_body,output):
    if i >= 0.55:
      print(i)
      print('Lead')
      return True
    else:
      print(i)
      print('Not Lead')
      return False

# body_lead_or_not(sent3)

"""## Email Listening"""

def check_missing_and_prep_msg(missing):
    msg = ''
    files, docs, letter = ['driver', 'employment', 'credit'], [], ['Driver License', 'Employment Letter', 'Credit Score']

    for file in files:
      for names in missing:
        if file in names:
          docs.append(file)
    print()

    if len(docs) != 3:
        msg += 'Karla Bot Notification\n\nFollowing Documents are missing in your email:\n'
        for i in range(len(files)):
          if files[i] not in docs:
            msg += f'{i+1}. {letter[i]}\n'
    
    if len(msg) == 0:
        msg = 'Karla Bot Notification\n\nAll your Documents are successfully received!!!\n'
    
    msg += '\nThanks and Regards,\nClient'
    return msg

# input = ['./GAMEL PROJECT PROPOSAL - Gamel Gray - Chatbot & Automation (1) (1).pdf', 'credit score.png', 'employment letter.png']
# check_missing_and_prep_msg(input)


import os
# try:
#   os.mkdir('temp')
#   # print('Temp Created')
# except Exception as e:
#   print(e)

def retrieve_email_contents():
  # Set your email, password, what folder you want to listen to, and where to save attachments
  email = "testpythondays@gmail.com"
  app_password = API_KEY
  folder = "Inbox"
  try:
    os.mkdir('temp')
    # print('Temp Created')
  except Exception as e:
    print(e)
  attachment_dir = 'temp/'
  el = email_listener.EmailListener(email, app_password, folder, attachment_dir)

  # Log into the IMAP server
  el.login()

  # Get the emails currently unread in the inbox
  messages = el.scrape()
  # print(messages)

  # Start listening to the inbox and timeout after an hour
  timeout = 0
  el.listen(timeout)
  # sendreply(messages)

  # Returning storing all data in dictionary/object
  output = {}
  emails, body, subject = [], [], []
  for value in messages.items():
    if 'attachments' in value[1].keys():
      output[value[0]] = {
                          'Subject':value[1]['Subject'],
                          'Body':value[1]['Plain_Text'],
                          'email':value[0].split('_')[-1],
                          'num_attachments':len(value[1]['attachments']),
                          'attachments':value[1]['attachments']
                          }
    else:
      output[value[0]] = {
                          'Subject':value[1]['Subject'],
                          'Body':value[1]['Plain_Text'],
                          'email':value[0].split('_')[-1],
                          'num_attachments':0,
                          'attachments':[]
                          }
  return output

# output = retrieve_email_contents()
# print('Email Content Retrieved')
# print(output)

"""## Flagging Lead or Not"""

def flag_email(output):
  flag = {}
  for key, value in output.items():
    # CHECK NAME and EMAIL IN DB
    # |>>>>>>>>>>>>>>>>>>>>>>>>>|
    
    # Check whether subject is lead or not
    if value['Subject']:
      sub_check = sub_lead_or_not([value['Subject']])
    else:
      sub_check = False
    
    # Flag as true if subject is a lead
    if sub_check:
      flag[key] = sub_check
      continue

    # Check whether body is lead or not
    if value['Body'] and value['num_attachments']>=1:
      # print(value['Body'])
      body_check = body_lead_or_not([value['Body']])
    else:
      # goto OCR
      body_check = False
    if body_check:
      flag[key] = body_check
    else:
      flag[key] = False

  # print(flag)
  try:
    shutil.rmtree('temp')
    # print('Temp Deleted')
  except Exception as e:
    print(e)
  return flag

# flag = flag_email(output)

"""## Sending Mail"""

import smtplib
def sendreply(messages, output):
    # initialize connection to our
  # email server, we will use gmail here
  with smtplib.SMTP('smtp.gmail.com', port = 587) as smtp:
    try:
      smtp.starttls()
        
      # Login with your email and password
      smtp.login('testpythondays@gmail.com', API_KEY)
      emaladdr=[]
      for email, value in output.items():
        emailaddr=email.split('_',1)#considered if underscore in emailid

        # Call the message function
        # msg =  check_missing_and_prep_msg(value['attachments'])
        msg = ''''''

        # Make a list of emails, where you wanna send mail
        to = emailaddr[1]
        print(to)
        # Provide some data to the sendmail function!
        if flag[email]: 
          var = 'a Lead' 
        else:
          var ='not a Lead'
        smtp.sendmail(from_addr="testpythondays@gmail.com",
                      to_addrs=to, msg=f'''Subject:Karla Bot Notification\n\n
                                        Hello, his is a test email, meant for checking potential leads.\n
                                        You are {var}\n
                                        Regards,
                                        Karla Bot''')
                                        # {emailaddr[1]}''')
        print("Notification sent successfully")
    except Exception as e:
      print(e)

# sendreply(flag, output)

import time
import shutil

while True:
  output = retrieve_email_contents()
  print('Email Content Retrieved')
  flag = flag_email(output)
  sendreply(flag, output)
  try:
    shutil.rmtree('temp')
    # print('Temp Deleted')
  except Exception as e:
    print(e)
  time.sleep(25)