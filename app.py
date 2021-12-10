import pandas as pd

def checkInit(commandStr):

    if commandStr == '':
        print('Tidak ada command')
        return False
    split = commandStr.split()
    if split[0] != 'init':
        print(
            'Masukkan perintah "init [jumlah loker]" untuk memulai program\n')
        return False
    elif len(split) != 2:
        print('[Input Error]format perintah init adalah "init [jumlah_loker]"\n')
        return False
    elif split[1].isnumeric():
        return True
    else:
        print('[Input Error]Perintah init hanya menerima angka\n')
        return False


def checkInput(command):

    if command == 'init':
        print('Program sudah berjalan\n')
        return False

    split = command.split()
    commandLower = split[0].lower()
    commandList = ['input', 'status', 'leave', 'find', 'search']
    isCommandExist = [ele for ele in commandList if(ele in commandLower)]

    if not isCommandExist:
        print("[Input Error]Command tidak diketahui. command yang tersedia ['input', 'status', 'leave', 'find', 'search']\n")
        return False

    elif commandLower == 'input':
        if len(split) != 3:
            print(
                '[Input Error]format command input adalah "input [tipe identitas] [no identitas]"\n')
            return False
        elif not split[2].isnumeric():
            print('[Input Error]No identitas harus numeric\n')
            return False

    elif commandLower == 'leave':
        if len(split) != 2:
            print('[Input Error]format command leave adalah "leave [no loker]"\n')
            return False

        elif not split[1].isnumeric():
            print('[Input Error]no loker harus numeric\n')
            return False

    elif commandLower == 'find':
        if len(split) != 2:
            print('[Input Error]format command find adalah "find [no identitas]"\n')
            return False

        elif not split[1].isnumeric():
            print('[Input Error]no loker harus numeric\n')
            return False

    elif commandLower == 'search':
        if len(split) != 2:
            print('[Input Error]format command find adalah "find [no identitas]"\n')
            return False

    return True


def executeCommand(data, command, limit):
    if command == '':
        print('Tidak ada command')
        return data
    split = command.split()
    commandLower = split[0].lower()
    insert = {}
    if checkInput(command):
        if commandLower == 'input':
            if len(data) < int(limit):

                insert['No Loker'] = ''
                insert['Tipe Identitas'] = split[1]
                insert['No Identitas'] = split[2]

                found = False
                for i in range(len(data)):
                    curr = data[i]
                    if curr['No Loker'] == 'empty':
                        found = True
                        insert['No Loker'] = i+1
                        data.insert(i, insert)
                        break
                if found == False:
                    if len(data) > 0:
                        last = data[len(data)-1]
                        noLoker = last['No Loker'] + 1
                    else:
                        noLoker = 1
                    insert['No Loker'] = noLoker
                    data.append(insert)
                print(
                    f"Kartu identitas tersimpan di loker nomor {insert['No Loker']}\n")
            else:
                print('Maaf loker sudah penuh\n')

        elif commandLower == 'status':
            if len(data) > 0:
                df = pd.json_normalize(data)
                dfClean = df.loc[df['No Loker'] != 'empty']
                print(dfClean.to_string(index=False))
                print('')
            else:
                print('Data masih kosong\n')

        elif commandLower == 'leave':
            if len(data) == 0:
                print('Data masih kosong\n')
            else:
                found = False
                for i in range(len(data)):
                    curr = data[i]
                    if curr['No Loker'] == int(split[1]):
                        found = True
                        curr['No Loker'] = 'empty'
                        data[i] = curr
                        print(f"Loker nomor {split[1]} berhasil dihapus\n")
                        break
                if found == False:
                    print('No loker tidak ditemukan\n')

        elif commandLower == 'find':
            if len(data) == 0:
                print('Data masih kosong\n')
            else:
                for d in data:
                    found = False
                    if d['No Identitas'] == split[1]:
                        found = True
                        print(
                            f"Kartu identitas tersebut berada di loker nomor {d['No Loker']}\n")
                        break
                if found == False:
                    print('Nomor Identitas tidak ditemukan\n')
        elif commandLower == 'search':
            if len(data) == 0:
                print('Data masih kosong\n')
            else:
                noId = []
                for d in data:
                    if d['Tipe Identitas'] == split[1]:
                        noId.append(d['No Identitas'])
                if len(noId) > 0:
                    print(','.join(noId))
                    print('')
                else:
                    print('Data tipe identitas tidak ditemukan\n')

    return data


while(True):
    command_init = str(input())

    data = []
    noLoker = 1

    if checkInit(command_init):
        split = command_init.split()
        print(f'=== {split[1]} slot loker telah dibuat ===\n')
        while(True):
            command = str(input())
            data = executeCommand(data, command, split[1])
