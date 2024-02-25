import sys
from cs50 import SQL
from tabulate import tabulate
import cowsay

db = SQL("sqlite:///courses.db")

DASH = "-" * 100

def main():
    print(DASH)
    welcome()
    while True:
        userchoice = input("\n    Choose 1 option below to proceed:\n    1 = Show registered courses\n    2 = Register a course\n    3 = Deregister a course\n    4 = Update course status\n    5 = Show completion status\n    6 = exit\n\n    Your choice: ")
        if userchoice == '1':# Show all registered courses
            show_registered_courses()
            print(DASH)

        elif userchoice == '2': # Register
            print(DASH)
            while True:
                count_registered_courses = db.execute("SELECT COUNT(*) FROM registered_courses")
                count_available_courses = db.execute("SELECT COUNT(*) FROM courses")
                if count_registered_courses == count_available_courses:
                    userchoice = print("\n    You registered all available courses\n    Please select another option")
                    print(DASH)
                    break
                else:
                    show_registered_courses()
                    show_all_courses()
                    id = input("\nEnter Course ID to register: ")
                    if exists_in_db(id) == True:
                        if registered_before(id) == False:
                            title = db.execute("SELECT * FROM courses WHERE id=?;", id)[0]['title']
                            db.execute("INSERT INTO registered_courses VALUES(?, ?, ?);", id, title, 'Ongoing')
                            print(DASH)
                            print(f'\nCourse ID of {id} has been registered successfully!')
                            show_registered_courses()
                            print(DASH)
                            break
                        else:
                            print(DASH)
                            print(f'\nCourse ID of {id} was registered before. Please select a different Course ID\n')

                    else:
                        print(DASH)
                        print('\nWrong course ID. Please enter course ID as list below')



        elif userchoice == '3': # Deregister a course
            print(DASH)
            while True:
                show_registered_courses()
                id = input("\nEnter Course ID to deregister: ")
                if registered_before(id) == False:
                    print(f'\nYou entered a wrong course ID of {id}')
                    print('This course was not registered before')
                else:
                    db.execute("DELETE FROM registered_courses WHERE id = ?", id)
                    print('\nCourse deregistered successfully')
                    show_registered_courses()
                    print(DASH)
                    break

        elif userchoice == '4': # Update a course status
            print(DASH)
            show_registered_courses()
            id = input("\nEnter course ID to update status: ")
            if registered_before(id) == True: # Registered before
                while True:
                    userchoice = input("\nSelect: \n1 = Ongoing\n2 = Completed\n\nYour choice: ")
                    if validate_status(userchoice):
                        status = get_status(userchoice)
                        db.execute("UPDATE registered_courses SET status = ? WHERE id = ?", status, id)
                        print(f'Status of course ID of {id} has been updated to {status} successfully')
                        show_registered_courses()
                        print(DASH)
                        break
                    else:
                        print(DASH)
                        print('\nWrong input. Please enter 1 or 2')

            else:
                print(DASH)
                print(f'\nCourse ID of {id} not registered before')


        elif userchoice == '5': # Show completion status
            print(DASH)
            print('')
            percentage = get_percentage()
            print(showresult(percentage))

        elif userchoice == '6': # Eixt
            print(DASH)
            print("\n    Thank you for visiting and have a great day! Bye! 👋👋👋\n")
            cowsay.cow('THIS WAS CS50P')
            sys.exit()

        else:
            print(DASH)
            print(f"\n    Your entered {userchoice.upper()}. It's wrong input. Please enter only 1, 2, 3, 4, 5 or 6")


def get_percentage():
    total_registered_courses = db.execute("SELECT COUNT(*) FROM registered_courses")[0]['COUNT(*)']
    count_completed_courses = db.execute("SELECT COUNT(*) FROM registered_courses WHERE status = 'Completed'")[0]['COUNT(*)']
    percentage = (count_completed_courses / total_registered_courses) * 100
    return percentage


def showresult(percentage):
    if percentage == 100:
      return f"You have completed {percentage:.0f}%. Congratulations! Keep it up!"
    elif percentage == 0:
      return f"You have completed {percentage:.0f}%. Please start studying hard!"
    else:
      return f"You have completed {percentage:.0f}%"


def validate_status(status):
    if status in ['1', '2']:
        return True


def get_status(userchoice):
    if userchoice == '1':
        return 'Ongoing'
    else:
        return 'Completed'


def registered_before(id):
    if len(db.execute("SELECT * FROM registered_courses WHERE id=?;", id)) != 0:
        return True
    else:
        return False


def exists_in_db(id):
    if len(db.execute("SELECT * FROM courses WHERE id=?;", id)) != 0:
        return True
    else:
        return False

def show_all_courses():
	print('\nList of courses available for registration')
	print(tabulate(db.execute("SELECT * FROM courses;"), headers='keys',tablefmt="fancy_grid"))

def show_registered_courses():
	table = db.execute("SELECT * FROM registered_courses ORDER BY id;")
	if len(table) == 0:
		print('\nYou have no registered course')
	else:
		print('\nBelow is list of your registered courses:')
		print(tabulate(table, headers='keys',tablefmt="fancy_grid"))


def welcome():
    print('')
    print("*******************************************")
    print("*                                         *")
    print("*     WELCOME TO CS50 COURSES TRACKER     *")
    print("*                                         *")
    print("*******************************************")


if __name__ == "__main__":
    main()
