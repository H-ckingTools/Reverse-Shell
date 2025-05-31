from os import system,path
from sys import argv

# file_name = str(input('Enter your payload filename : '))
if argv[1] == 'make':
    file_name = 'Malware-Detector.py'

    if file_name:
        system(f'wine pyinstaller --onefile --noconsole --icon=app.ico {file_name}')
        try:
            system(f'cp dist/{path.splitext(file_name)[0]}.exe /media/mohamed/54B633F1B633D26A/Linux+Windows10/')
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