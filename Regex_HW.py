import re
import csv

def text_processing(contacts_list):
    new_contact_list = []
    new_contact_list.append(contacts_list[0])

    pat_phone = r'(\+7|8)?[\s]?\(?(\d{3})\)?[-\s]?(\d{3})[-\s]?(\d{2})[-\s]?(\d{2})([\s]?\(?доб\.\s)?(\d*)\)?'
    repl_phone = r'+7(\2)\3-\4-\5 \7'
    pat_fio = r'(^\w*).(\w*).(\w*)'
    repl_fio = r'\1,\2,\3'

    t_list = []
    for elem in contacts_list[1:]:
        temp = (re.sub(pat_fio, repl_fio, (' '.join(elem[:3])))).split(',')
        temp.insert(2, temp.pop(2).rstrip())
        temp.extend(elem[3:7])
        phone_norm = (re.sub(pat_phone, repl_phone, temp.pop(5))).split()
        temp.insert(5,' доп.'.join(phone_norm))
        t_list.append(temp)
    count = 0
    for person in t_list:
        fi = person[0] + person[1]
        count += 1
        for new_person in t_list[int(f'{count}'):]:
            new_fi = new_person[0] + new_person[1]
            if fi == new_fi:
                if person[2] == '': person[2] = new_person[2]
                if person[3] == '': person[3] = new_person[3]
                if person[4] == '': person[4] = new_person[4]
                if person[5] == '': person[5] = new_person[5]
                if person[6] == '': person[6] = new_person[6]
                t_list.remove(new_person)
    for person in t_list:
        if person not in new_contact_list:
            new_contact_list.append(person)

    return new_contact_list

def rewrite():
    csv.register_dialect('no_transfer', lineterminator='\n')

    with open("phonebook.csv", "w", encoding = 'utf-8') as f:
        datawriter = csv.writer(f, 'no_transfer')
        datawriter.writerows(text_processing(contacts_list))

if __name__ == '__main__':
    with open('phonebook_raw.csv', 'r', encoding='utf-8') as f:
        rows = csv.reader(f, delimiter=',')
        contacts_list = list(rows)
    rewrite()