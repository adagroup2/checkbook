










































print('~~~ Welcome to your terminal checkbook! ~~~\n')

action_choice = input('''What would you like to do?
1) View current balance
2) record a debit (withdraw)
3) record a credit (deposit)
4) exit 
''')
while not action_choice in('1234'):
    action_choice = input('Invalid choice. Please enter 1-4: ')

if int(action_choice) == 1:
    print(action_choice)
    # view_balance()
elif int(action_choice) == 2:
    print(action_choice)
    # debit()
elif int(action_choice) == 3:
    print(action_choice)
    # credit()
elif int(action_choice) == 4:
    exit()

action_choice = input('Would you like to make another transaction (y/n)? ')
while action_choice == 'y' or action_choice.lower() == 'yes':
    action_choice = input(
        'What would you like to do? \n1) View current balance\n2) record a debit withdraw\n3) record a credit deposit\n4) exit \n ')
    while not action_choice in('1234'):
        action_choice = input('Invalid choice. Please enter 1-4: ')

    if int(action_choice) == 1:
        print(action_choice)
        # view_balance()
    elif int(action_choice) == 2:
        print(action_choice)
        # debit()
    elif int(action_choice) == 3:
        print(action_choice)
        # credit()
    elif int(action_choice) == 4:
        exit()
    action_choice = input('Would you like to make another transaction (y/n)? ')
