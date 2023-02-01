import pandas

test = pandas.read_csv(r'C:\Users\itsgo\Desktop\hydra-export-1.csv')

for index, row in test.iterrows():
    isConfirmed = row['Confirmed']
    date = row['Date']
    type = row['Type']
    label = row['Label']
    address = row['Address']
    amount = row['Amount (HYDRA)']
    ID = row['ID']

    print(str(isConfirmed) + ' ' +
              str(date) + ' ' +
                  str(type) + ' ' +
                      str(label) + ' ' +
                          str(address) + ' ' +
                              str(amount) + ' ' +
                                  str(ID))
    print('-------')

