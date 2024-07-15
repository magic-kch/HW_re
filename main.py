import csv
import re


def read_csv(file):
    with open(file, encoding="utf-8") as f:
        rows = csv.reader(f, delimiter=",")
        contacts_list = list(rows)
    return contacts_list


def write_csv(file, data):
    with open(file, "w", encoding="utf-8", newline='') as f:
        datawriter = csv.writer(f, delimiter=',')
        datawriter.writerows(data)


def convert_phone(phone):
    if phone:
        pattern_phone = r"(\+7|8){1}\s*[(]*(\d{3})[)]*\s*\-*(\d{3})\s*\-*(\d{2})\s*\-*(\d{2})([ (]*(\w+\.)\s*(\d+)[)]*)*"
        pattern_phone_new = r"+7(\2)\3-\4-\5 \7\8"
        return re.sub(pattern_phone, pattern_phone_new, phone)
    else:
        return phone


if __name__ == '__main__':
    contact_list = read_csv("phonebook_raw.csv")
    new_list = dict()

    for fio in contact_list[1:]:
        fio[5] = convert_phone(fio[5]).strip()

        fio_new = " ".join(fio[:3]).split()
        if len(fio_new) < 3:
            fio_new.append("")
        fio_new = fio_new + fio[3:]
        fi_key = " ".join(fio_new[:2])
        if fi_key not in new_list.keys():
            new_list[fi_key] = {'surname': fio_new[2], 'organization': fio_new[3], 'position': fio_new[4],
                                'phone': fio_new[5], 'email': fio_new[6]}
        else:
            count = 0
            for key, value in new_list[fi_key].items():
                if not value:
                    new_list[fi_key].update({key: fio_new[count + 2]})
                count += 1
    contact_list_new = list()
    contact_list_new.append(contact_list[0])

    for key, value in new_list.items():
        contact_list_new.append(key.split()+list(value.values()))

    write_csv("phonebook.csv", contact_list_new)
