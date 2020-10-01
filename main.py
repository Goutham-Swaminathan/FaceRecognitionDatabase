import os
import Dataset
import Encoding

pwd = os.path.dirname(os.path.realpath(__file__)) //specify the path of the file

if not os.path.isfile(pwd+'/Face_database.db'):
    Encoding.Make_Table()

Status = input('Enter 1 to add new face.\n Enter 2 to scan face.\n Enter 3 to quit.\n')
if Status == '1':
    Name = input('Enter Your Name:')
    Dataset.Dataset(Name)
elif Status == '2':
    data = Encoding.unlock()
    print(data)
elif Status =='3':
    print('Quitting')
else:
    print("Invalid Entry")


