from collections import UserDict
import  datetime 
import re

class Field():
    def __init__(self, value):
        self._value = None
        self.value = value
        
    @property
    def value(self):
        return self._value
         
    @value.setter
    def value(self, value):
        self._value = value

class Name(Field):

    @Field.value.setter
    def value(self, value):
        if not value.isalnum():
            raise ValueError("Name must contain only letters and numbers")
        self._value = value
        
      

class Phone(Field):

    @Field.value.setter
    def value(self, value):
        if not (len(value) >= 10 or len(value) <= 12):
            raise ValueError("Phone must have 10-12 numbers")

        if not value.isnumeric():
            raise ValueError('Phone must include only numbers')
        self._value = value

    def __eq__(self, other):
       return self.value == other.value
    
    def __str__(self) -> str:
        return self.value
             
class Birthday(Field): 
 #birthday must be string in format suitable for transformation in data-object 
    # %d Day of the month as a zero-padded decimal number.
    # %m Month as a zero-padded decimal number.
    # %Y Year with century as a decimal number.

    @Field.value.setter
    def value(self, value):
        if not re.fullmatch(r'\d{2}\.\d{2}\.\d{4}', value):
            raise ValueError("Birthday must be dd.mm.yyyy")

        birthday = (datetime.datetime.strptime(value, '%d.%m.%Y')).date()   
        current_day = datetime.date.today()
        if birthday > current_day:
            raise ValueError('Bad date of birthday')
        self._value = value
    
    def __str__(self) -> str:
        return self.value         

class Record():
    def __init__(self, name: Name, phone: Phone = None, birthday: Birthday = None):
    #def __init__(self, name):
        self.name = name
        self.phone_list = []
        if phone:
            self.phone_list.append(phone)
        self.birthday = birthday
        

      
    def add_phone(self, phone: Phone):
        self.phone_list.append(phone)
        return  

    def del_phone(self, phone: Phone):
        if phone in self.phone_list:
            self.phone_list.remove(phone) 
            return  f'{phone} in contact is deleted.'
        return "This phone doesn't exist, please try again."
        
    def change_phone(self, old_phone: Phone, new_phone: Phone):
        if old_phone in self.phone_list:
            self.phone_list.remove(old_phone)
            self.phone_list.append(new_phone)     
            return "Phone changed"
        return "This contact doesn't exist, please try again."  
    
    def  show_all_phones(self):
        phones = ', '.join(str(p) for p in self.phone_list)
       
        return f'{phones}'
    
    def __str__(self) -> str:
        if not self.birthday:
            birthday = "empty"
        else:
            birthday =  self.birthday.value
        if not self.phone_list: 
            phones = 'empty'
        else:
            phones =  self.show_all_phones()  
            
        return  f'In class Record str-method. Name: {self.name.value}, birthday: {birthday},  phones: {phones}'    
        
    def add_birthday(self, date):
        self.birthday = Birthday(date)
        return  

    def days_to_birthday(self):
        if not self.birthday:
            return "Birthday date is absent"
        birthday = (datetime.datetime.strptime(self.birthday.value, '%d.%m.%Y')).date()   
        current_day = datetime.date.today()
        current_year = current_day.year    
        birthday_nearest = birthday.replace(year = current_year)   
        interval = (birthday_nearest - current_day).days
        if interval < 0:
            birthday_nearest = birthday.replace(year = current_year + 1)   
            interval = (birthday_nearest - current_day).days
    
        return interval

    

class AddressBook(UserDict):
    def __init__(self):
        self.data = {}

    def add_record(self, record: Record):
        self.data[record.name.value] = record
        return 
        
    def search_record(self, name: str):
        return self.data.get(name)

    #def get_one_record(self, name):
    #    return self.data.get(name)  
    
    #def show_all_contacts(self):
    #    return self.data

    def iterator(self, number_of_rec):
        page = []
        keys_len = len(list(self.data.keys()))
        for i in  range(0, keys_len, number_of_rec):
            slice = list(self.data.keys())[i:i+number_of_rec]
            for key in slice:
               page.append(self.data[key])
            yield page
            page = []
            slice = []

    def __str__(self):
        book = ''
        for page in self.iterator():
            book = book +'\n' + '\n'.join(str(record) for record in page)
        return book

    
# tests for classes:
#
# n1 = Name('k')
# p1 = Phone('1234567890')
# bir1 = Birthday('24.08.1900')
# record1 = Record(n1, bir1, p1)
##n2 = Name('bo')
#p2 = Phone('111111111')
#bir2 = Birthday('26.09.1978')
#record2 = Record(n2, bir2, p2)
#n3 = Name('foo')
#p3 = Phone('2222222222')
##record3 = Record(n3, bir3, p3)
#n4 = Name('kop')
#p4 = Phone('44444444444')
#bir4 = Birthday('24.06.1954')
#record4 = Record(n4, bir4, p4)
#n5 = Name('nul')
#p5 = Phone('55555555555')
#bir5 = Birthday('03.08.1999')
#record5 = Record(n5, bir5, p5)
#n6 = Name('tu')
#p6 = Phone('6666666666666')
#bir6 = Birthday('01.01.2013')
#record6 = Record(n6, bir6, p6)
#
#record = Record("```")
#phone = Phone('1234567')
#print(record.add_phone(phone))
#print(record.del_phone('12'))
#print(record.add_phone('343434872934'))
#print(record.add_phone('1'))
#print(record.change_phone('343434872934', '9876543'))
#print(record.show_all_phones())
# adress = AddressBook()
# adress.add_record(record1)
#adress.add_record(record2)
##adress.add_record(record3)
#adress.add_record(record4)
#adress.add_record(record5)
#adress.add_record(record6)
#print(adress)
#print(record.del_phone('13'))
#print(record.change_phone('343434872934'))
#print(adress.show_all_contacts())
#print(n.value)
#print(p.value)
#print(bir.value)
#rint(adress.search_record('k'))

