from turtle import Turtle, Screen
from threading import Thread
import random
import time
import sys

# It is needed to enable ansi escape character in windows
# Colorama makes this work on Windows by wrapping stdout, stripping ANSI sequences it finds
# and converting them into the appropriate win32 calls to modify the state of the terminal.
# On other platforms, Colorama does nothing.
from colorama import init

init() # enable colorama to listening output

car_progress_dict = {0: 0, 1: 0, 2: 0, 3: 0}
result_time = {0: 0.0, 1: 0.0, 2: 0.0, 3: 0.0}

selected_car = None


def print_progress_bar(title, current_bar_index, total_bar_len):
    full_bar_str = '░' * int(total_bar_len-current_bar_index)
    temporary_bar_str = '█' * int(current_bar_index)

    percent_done = current_bar_index * 100 / total_bar_len
    percent_done_str = f'{percent_done} %'
    if percent_done == 100:
        percent_done_str = "Arrived!"

    print(f'{title}-> {temporary_bar_str}{full_bar_str}  {percent_done_str}')


def print_race_progress():

    print_progress_bar("Car 1", car_progress_dict[0], 20)
    print()

    print_progress_bar("Car 2", car_progress_dict[1], 20)
    print()

    print_progress_bar("Car 3", car_progress_dict[2], 20)
    print()

    print_progress_bar("Car 4", car_progress_dict[3], 20)
    print()

    # ansi escape character
    # return up of 8 terminal lines
    sys.stdout.write("\033[8A")


def print_race_result():
    print()
    print("-----------END------------")
    print("")
    print("Here the results: ")

    final_result = sorted(result_time, key=result_time.get)
    for i in range(4):
        print(f"{i+1}°-> Car {final_result[i]+1}  --  {round(result_time[final_result[i]], 3)}")

    if final_result[0] == selected_car:
        print("YOU HAVE WIN! :) ")
    else:
        print("YOU HAVE LOSE! :(")


def start_car(car_number):
    start = time.time()

    for i in range(20):
        delay_time = random.random()
        time.sleep(delay_time)
        car_progress_dict[car_number] += 1

    result_time[car_number] = time.time() - start


def main():
    print("  --- Car Game ---")
    print("On which car do you want to bet?")

    while True:
        selected = input("Please, choose car 1,2,3,4: ")
        if selected.isnumeric() and 1 <= int(selected) <= 4:
            global selected_car
            selected_car = int(selected) - 1
            break

    print()
    print(f"You have choose car number {selected_car + 1} ")

    print()
    input("Press any key to start the race...")
    print()

    t0 = Thread(target=start_car, args=(0,))
    t1 = Thread(target=start_car, args=(1,))
    t2 = Thread(target=start_car, args=(2,))
    t3 = Thread(target=start_car, args=(3,))

    t0.start()
    t1.start()
    t2.start()
    t3.start()

    while True:
        if t0.is_alive() or t1.is_alive() or t2.is_alive() or t3.is_alive():
            print_race_progress()
        else:
            break

    print_race_progress()
    print("\n\n\n\n\n\n")

    print_race_result()


main()