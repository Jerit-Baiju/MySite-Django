import os
import sys
while True:
    main = input('--> ')
    if main  in ['ssh', 'server', 'jerit.ml']:
        os.system(
            'ssh -i "server.pem" ubuntu@ec2-35-154-177-74.ap-south-1.compute.amazonaws.com')
    elif main == "run":
        os.system('clear')
        os.system('python manage.py runserver')
    elif main in ['exit', 'quit', 'x']:
        sys.exit()
    elif main == 'clear' or main == 'clr':
        os.system('clear')
    elif main == 'push':
        os.system('git push')
    elif main == 'status':
        os.system('git status')
    elif main == 'pull':
        os.system('git pull')
    else:
        print('>>> Unknown command')
