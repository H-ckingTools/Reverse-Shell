from os import system
from sys import argv

# file_name = str(input('Enter your payload filename : '))
if argv[1] == 'make':
    file_name = 'maingame.py'

    if file_name:
        system(f'wine pyinstaller --onefile --noconsole --icon=app.ico {file_name}')
        try:
            system('cp dist/maingame.exe /media/mohamed/54B633F1B633D26A/Linux+Windows10/')
            system('clear')
            print('successfully copied')
        except Exception as e:
            print(f'File failed to copy to destination : {e}')
    else:
        print('Failed to build malware payload')
elif argv[1] == 'clean':
    system('rm -rf build/ dist/ maingame.spec')
else:
    print(f'Inavlid command {argv[1]}')