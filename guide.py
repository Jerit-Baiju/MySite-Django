import os
while True:
    main = input('--> ')
    if main == 'ssh' or main == 'server':
        os.system(
            'ssh -i "server.pem" ubuntu@ec2-13-114-210-67.ap-northeast-1.compute.amazonaws.com')
    elif main == "run":
        os.system('python manage.py runserver')
    elif main == 'x' or main == 'exit':
        exit()
    elif main == 'clear' or main == 'clr':
        os.system('clear')
    else:
        print('>>> Unknown command')
