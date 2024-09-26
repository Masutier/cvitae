import io
import cryptocode
import msoffcrypto
import pandas as pd


def private_keys():
    encKey = "Death,_the_greatest_of_adventures"
    passcrypt = 'eQf8ER9hXwwHVdw=*m0417Q6iM2nk33hmT8LzDA==*ZtTjgIVMBRUmzTCWnWx8VQ==*v2y/ExEaZPbGB4Ah5ZxzRA=='
    dictData = []
    decrypted_workbook = io.BytesIO()
    with open('instance/private_keys.xlsx', 'rb') as file:
        office_file = msoffcrypto.OfficeFile(file)
        passdecrypt = cryptocode.decrypt(passcrypt, encKey)
        office_file.load_key(password=passdecrypt)
        office_file.decrypt(decrypted_workbook)
    data = pd.read_excel(decrypted_workbook)
    for i, row in data.iterrows():
        VARIABLE = str(row['VARIABLE'])
        CLAVE = row['CLAVE']
        saveToDic = (VARIABLE, CLAVE)
        dictData.append(saveToDic)
    dictData = dict(dictData)
    return dictData


def decrypting_key(encryption, encKey):
    decryption = cryptocode.decrypt(encryption, encKey)
    return decryption

