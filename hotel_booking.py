from datetime import datetime
import json


#this is for mysql and python connectivity
import mysql
import mysql.connector
conn=mysql.connector.connect(
    host="localhost",
    user="root",
    password="1234",
    database="mk_hotel"
)
mycursor=conn.cursor()



# total_rooms_in_hotel={'1':'available','2':'available','3':'available','4':'available','5':'available'}



with open('room_details.json','r') as file:
    total_rooms_in_hotel=json.load(file)


def room_detailes_file():
    with open('room_details.json','w') as file:
        json.dump(total_rooms_in_hotel,file)




def check_availability():
    aviable_room_list=[]
    for key,value in total_rooms_in_hotel.items():
        if value=='available':
            aviable_room_list.append('room_no_'+key)
        elif value=='booked':
            continue
        
    if aviable_room_list!=[]:
        print('\n------------************---------------\n')
        print(f'\nthis rooms are avaible {aviable_room_list}')

    if all(value == "booked" for value in total_rooms_in_hotel.values()):
        print('\n------------************---------------\n')
        print("Sorry All rooms are booked.")
        print('to logout press Q')




def book_room():
        check_availability()
        print('\n------------************---------------\n')
        choose_room=input('choose room number from the above:-')

        if total_rooms_in_hotel[choose_room]=='available':
            user_name=input('\nenter your name:-')
            user_age=int(input('\nenter your age:-'))
            user_address=input('\nenter your address:-')
            total_member=int(input('\nbooking for how many member:-'))
            current_date = datetime.now().date() 
            booking_date = current_date.strftime("%Y-%m-%d") # is for take date in string format

            total_rooms_in_hotel.update({choose_room:'booked'})
            room_detailes_file()

            print('\n------------************---------------\n')
            print(f'\nyour room number {choose_room} is booked enjoy🤗')


            # this for store the above data to the table in backend in mysql database kwoun as mk_hotel and in the booking_details table 
            mycursor.execute(
                    "INSERT INTO booking_details (user_name, user_age, user_address, total_member, booking_date) VALUES (%s, %s, %s, %s, %s)",
                        (user_name, user_age, user_address, total_member, booking_date)
            )
            conn.commit()

        else:
            print('\n------------************---------------\n')
            print(f'room number {choose_room} is already booked choose any one from the above avaible rooms')


def to_see_booking_data():
    mycursor.execute("SELECT * FROM booking_details")
    data=mycursor.fetchall()
    for rows in data:
        print(rows)



def check_out():
    print('\n')
    user_input=input('enter your room number:-')
    if total_rooms_in_hotel[user_input]=='booked':
        total_rooms_in_hotel.update({user_input:'available'})
        room_detailes_file()

        print('\n------------************---------------\n')
        print('Thankyou! please visit again🤗')
    else:
        print('enter correct room number')



def main():
    login=input('\nType login to enjoy MK Hotel Service:-')
    while login=='login':
        print('\n------------************---------------\n')
        print('To check avaible rooms press 1')
        print('To book room press 2')
        print('To checkout press 3')
        print('To logout press Q')
        
        print()
        process=input('choose any one option from the above:-')
        if process=='1':
            check_availability()
        elif process=='2':
            book_room()
        elif process=='3':
            check_out()
        elif process=='boss':
            to_see_booking_data()
        else:
            login='quite'



main()































