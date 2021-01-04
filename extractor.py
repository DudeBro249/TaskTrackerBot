import os
import re

file = open("all-messages.txt", encoding="utf-8")
texts = ''.join(file.readlines()).split("<|endoftext|>\n")
file.close()

def extract_data(message: str) -> tuple:
    user_id, colon, rest = message.partition("::")
    date, colon, message = rest.partition("::")
    return user_id, message, date

member_names = ['DudeBro']
member_files =  {}
for member_name in member_names:
    if os.path.exists(f'{member_name}-messages.txt'):
        member_files[member_name] = open(f'{member_name}-messages.txt', mode='w+', encoding='utf-8')
    else:
        member_files[member_name] = open(f'{member_name}-messages.txt', mode='x', encoding='utf-8')

count = 0
quote_as_reply = False
        
for text in texts:
    user_id, message, date = extract_data(text)
    
    if re.search(r"^\> (.+)\n\<\@\!\d+\> (.+)", message):
        quoted, reply = re.search(r"^\> (.+)\n\<\@\!\d+\> (.+)", message).groups()
        
        if not quote_as_reply:
            message = reply

    message = message.replace('*', '').replace('~', '').replace('/spoiler', '').replace('\n', '')
    for member_name in member_names:
        if member_name in user_id and not message.isspace():
            if count < 1:
                member_files[member_name].write(message + '\n')
                count += 1
            else:
                member_files[member_name].write(message + "\n" + r'<|endoftext|>' + '\n')
                count = 0
            break
    
    
for member_file in member_files.keys():
    member_files[member_file].close()
    
