import os
while True:
    main = input('--> ')
    if main == 'ssh' or main == 'server' or main == 'jerit.ml':
        os.system(
            'ssh -i "server.pem" ubuntu@ec2-13-232-66-6.ap-south-1.compute.amazonaws.com')
    elif main == "run":
        os.system('python manage.py runserver')
    elif main == 'x' or main == 'exit':
        exit()
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
