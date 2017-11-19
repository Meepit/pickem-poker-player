from Bot import Bot
from Screen import Screen
from Hand import Hand
from queue import Queue
from threading import Thread
import win32api
import win32con
import time

if __name__ == '__main__':
    q = Queue()
    screen1 = Screen(1)
    hand1 = Hand(screen1)
    bot1 = Bot(hand1, screen1, q)
    thread1 = Thread(target=bot1.start)
    thread1.start()

    screen2 = Screen(2)
    hand2 = Hand(screen2)
    bot2 = Bot(hand2, screen2, q)
    thread2 = Thread(target=bot2.start)
    thread2.start()

    screen3 = Screen(3)
    hand3 = Hand(screen3)
    bot3 = Bot(hand3, screen3, q)
    thread3 = Thread(target=bot3.start)
    thread3.start()

    screen4 = Screen(4)
    hand4 = Hand(screen4)
    bot4 = Bot(hand4, screen4, q)
    thread4 = Thread(target=bot4.start)
    thread4.start()

    hands_played = 0
    while True:
        next_action = q.get()
        win32api.SetCursorPos(next_action)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
        time.sleep(0.1)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)
        time.sleep(0.1)
        if next_action not in [i._screen.deal_button for i in [bot1, bot2, bot3, bot4]]:
            hands_played += 1
            print("Total  hands played: {0}".format(hands_played))
