scenes = []
for i in range(4):
  with open(f'email_inputs/text{i+1}.txt', 'r') as txt:
    text = txt.read()
    scenes.append(text)
# for scene in scenes:
#   print(scene)

attachments = 3
body = 'present'

def check_keywords(body):
  keywords = ['attachment', 'credit', 'drivers', 'government', 'file', 'files', 'requested', 'waiting', 'application', 'apply', 'payment', 'employment', 'reports', 'score', 'attached', 'provided', 'provide']
  output = []
  body.replace(r'\n', '')
  body = body.split(" ")
  
  for char in body:
    if char.lower() in keywords:
      output.append(char)
  return len(output) > 0


def check_attachments():
    pass

def flag_email(attachments, body):
    if attachments == 3:
        if len(body) > 0:
            # Checking Keywords
            keys_present = check_keywords(body)
            if keys_present:
                print('Email contains correct doc and 3 attachements based on keywords in body')
                return True
            else:
                print('Email has no keywords in body but has 3 attachments')
                check_attachments()
                return True
        else:
            print('Body Empty but has 3 attachments')
            check_attachments()
            return True
    else:
        print('Num of attachments are less')
        return False

for i in range(len(scenes)+1):
    if i == 4:
        print(flag_email(2, scenes[0]), end="\n\n")
    else:
        print(flag_email(3, scenes[i]), end="\n\n")