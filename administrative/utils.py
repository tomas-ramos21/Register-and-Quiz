import csv

def register_lecturer(csv_path):

    columns = ['id', 'password', 'first_name', 'last_name', 'email', 'department', 'position']

    with open(csv_path, 'r') as csv_file:
        reader = csv.DictReader(csv_file, fieldnames=columns)

        for idx, row in enumerate(reader):  # For each row
            if idx != 0:                    # If row isn't the header
                for column in columns:      
                    print(row[column])
