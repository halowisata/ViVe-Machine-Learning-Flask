import csv


def get_last_id_from_csv(filename):
    last_id = 0

    with open(filename, 'r') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            user_id = int(row[0])
            if user_id > last_id:
                last_id = user_id

    return last_id


def append_user_to_csv(filename, user_id, address, age):
    with open(filename, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([user_id, address, age])


def create_user_main(address, age):
    filename = './datasets/raw/user.csv'
    last_id = get_last_id_from_csv(filename)
    user = {}
    user['User_Id'] = last_id+1
    user['address'] = address
    user['age'] = age

    return user
