def check_missing_and_prep_msg(missing):
    msg = ''
    files, docs = ['Driver License', 'Employment Letter', 'Credit Score'], []

    for i in range(len(missing)):
        if missing[i] == 1:
            docs.append(files[i])

    if len(docs) >=1:
        msg += 'Following Documents are missing in your email:\n'
        for i in range(len(docs)):
            msg += f'{i+1}. {docs[i]}\n'
    
    if len(msg) == 0:
        msg = 'All your Documents are successfully received!!!\n'
    
    msg += '\nThanks and Regards,\nClient'
    print(msg)
    return msg