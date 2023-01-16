from addressrecords import  AddressBook, Record, Name, Phone, Birthday

address_book = AddressBook()

# decorator for exceptions
def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return 'This contact doesnt exist, please try again.'

        except ValueError as exception:
            return exception.args[0]
        except IndexError:
            return 'This contact cannot be added, it already exists.'
        except TypeError:
            return 'Unknown command or parametrs, please try again.'
    return inner


#blocks for input commands:

def hello():
    result = 'How can I help you?'
    return result

@input_error
def add_contact(name, phone = None, birthday = None):
    
    if  address_book.search_record(name):
        return 'This contact cannot be added, it already exists.'
    
   # if phone and (not birthday):
    #    record = Record(Name(name), None, Birthday(birthday))
    if phone and  (not birthday):
        record = Record(Name(name), Phone(phone), None)
    elif (not phone) and (not birthday):
        record = Record(Name(name), None, None)
    else:
        record = Record(Name(name), Phone(phone), Birthday(birthday))    
    address_book.add_record(record)
   
    return f'{record}'

@input_error
def add_phone(*args):
    name, phone = args
    if  not address_book.search_record(name):
        return "This phone cann't be added, contact doesn't exist."
    record = address_book.search_record(name)
    record.add_phone(Phone(phone))
    
    return f'Added {phone} in contact: {name}'

@input_error
def del_phone(*args):
    name, phone = args
    record = address_book.search_record(name)
    if  not address_book.search_record(name):
        return "This phone cann't be deleted, contact doesn't exist."
    record = address_book.search_record(name)
    result = record.del_phone(Phone(phone))
    
    return result

@input_error
def change_phone(*args):
    name, old_phone, new_phone = args
    record = address_book[name]
    result = record.change_phone(Phone(old_phone), Phone(new_phone))
   
    return result

@input_error
def phone_from_name(name):
       
    if not address_book.search_record(name):
        return f'This contact is not the book.'
    record = address_book.search_record(name)
    return f'{record.show_all_phones()}'


def  show_all_contacts(num_contacts_on_page = 5):
    result = ''
    num = 1
    if not address_book:
        return f'There are no contacts in the book.'

    iterator =  address_book.iterator(int(num_contacts_on_page))
    is_continue = 'y'  
    for page in iterator:
        print(f'page {num}')
        for line in page:
            print(line)
        num += 1
        is_continue = input('Do you want to continue? (Y/n)) ')
        if is_continue == 'y':
            continue
        elif is_continue == 'n':
            break
        else:
            raise ValueError("You must write 'y' or 'n'")

    return  result

@input_error
def add_birthday(*args):
    name, date = args
    record = address_book.search_record(name)
    record.add_birthday(date)
    return f'Added {date} in contact: {name}'

@input_error
def get_days_to_birthday(name):
    if  not address_book.search_record(name):
        return "This command cann't be completed, contact doesn't exist."
    record = address_book.search_record(name)
    result = record.days_to_birthday()
    return f'Days to {name} birthday is {result}'

def exit(): 
    return 'exit'
    
    

HANDLERS = {
    "hello": hello,
    "good bye": exit,
    "close": exit,
    "exit": exit,
    "add contact": add_contact,
    "add phone": add_phone,
    "del phone": del_phone,
    "change": change_phone,
    "show contacts": show_all_contacts,
    "phone": phone_from_name,
    "add birthday": add_birthday,
    "days to birthday": get_days_to_birthday,
    }

def parser_input(user_input):
    command, *args = user_input.split()
    handler = None
    command = command.lower()
    if command in HANDLERS:
        handler = HANDLERS[command]
    else:
        if args:
            command = command + ' ' + args[0]
            args = args[1:]
            if command in HANDLERS:
                handler = HANDLERS.get(command)
            else:
                command = command + ' ' + args[0]
                args = args[1:]
                if command in HANDLERS:
                    handler = HANDLERS.get(command)
    return handler, *args


def main():
    while True:
        user_input = input("Input command: ")
        handler, *args = parser_input(user_input)
        if handler:
            result = handler(*args)
        else:
            result = f'Unknown command'    
        
        if result == 'exit':
            print("Good bye!")
            break
        print(result)
        


if __name__ == "__main__":
   

    main()

# if __name__ == '__main__':
#     name = Name('Bill')
#     phone = Phone('1234567890')
#     rec = Record(name, phone)
#     ab = AddressBook()
#     ab.add_record(rec)
    
#     assert isinstance(ab['Bill'], Record)
#     assert isinstance(ab['Bill'].name, Name)
#     assert isinstance(ab['Bill'].phones, list)
#     assert isinstance(ab['Bill'].phones[0], Phone)
#     assert ab['Bill'].phones[0].value == '1234567890'
    
#     print('All Ok)')

 # n1 = Name('k')
    # p1 = Phone('1234567890')
    # bir1 = Birthday('24.08.1900')
    # record1 = Record(n1, p1, bir1)
    # n2 = Name('bo')
    # p2 = Phone('111111111')
    # bir2 = Birthday('26.09.1978')
    # record2 = Record(n2, p2, bir2)
    # n3 = Name('foo')
    # p3 = Phone('2222222222')
    # record3 = Record(n3, p3)
    # n4 = Name('kop')
    # p4 = Phone('44444444444')
    # bir4 = Birthday('24.06.1954')
    # record4 = Record(n4, p4, bir4)
    # n5 = Name('nul')
    # p5 = Phone('55555555555')
    # bir5 = Birthday('03.08.1999')
    # record5 = Record(n5, p5, bir5)
    # n6 = Name('tu')
    # p6 = Phone('6666666666666')
    # bir6 = Birthday('01.01.2013')
    # record6 = Record(n6, p6, bir6)
    # address_book.add_record(record1)
    # address_book.add_record(record2)
    # address_book.add_record(record3)
    # address_book.add_record(record4)
    # address_book.add_record(record5)
    # address_book.add_record(record6)