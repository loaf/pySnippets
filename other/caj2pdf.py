from pynput.keyboard import Key, Controller
import time

keyboard = Controller()
total = 365 #��ҳ��
number = 1 #��ʼҳ
time.sleep(5) #5sʱ�������е�CAJ�Ķ���
while number < total:
    with keyboard.pressed(Key.ctrl):
        keyboard.press('p')
        keyboard.release('p')
    for a in range(3):
        keyboard.press(Key.tab)
        keyboard.release(Key.tab)
    keyboard.type(str(number))
    keyboard.press(Key.tab)
    keyboard.release(Key.tab)
    keyboard.type(str(number + 1))
    keyboard.press(Key.enter)
    keyboard.release(Key.enter)
    time.sleep(2)
    keyboard.type(str(number) + '-' + str(number + 1))
    keyboard.press(Key.enter)
    keyboard.release(Key.enter)
    number = number + 2
    time.sleep(5) #�ȴ���ӡ5s,���ʱ����ˣ���ӡ���ɹ����ߴ�ӡҳ�治��������ȫ�����ʱ������15s
    with keyboard.pressed(Key.alt):
        keyboard.press('f')
        keyboard.release('f')
        time.sleep(0.5)
        keyboard.press('c')
        keyboard.release('c')
        time.sleep(0.5)
        keyboard.press('f')
        keyboard.release('f')
        time.sleep(0.5)
        keyboard.press('1')
        keyboard.release('1')
        time.sleep(0.5)
    time.sleep(3)
