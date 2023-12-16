import time
import random
import statistics
import re
import string

from ppadb.client import Client as AdbClient
from bs4 import BeautifulSoup


chars = '+-/*!&$#?=@<>abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'


def check_device():
    client = AdbClient(host="127.0.0.1", port=5037)  # Default is "127.0.0.1" and 5037
    devices = client.devices()
    if len(devices) == 0:
        print('No devices')
        exit(11)
    device = devices[0]
    print(f'Connected to {device}')
    return device, client


def start_tt(device):
    packages_list = device.shell("pm list packages")
    if "com.zhiliaoapp.musically" in packages_list:
        device.shell("pm clear com.zhiliaoapp.musically")
        device.shell("monkey -p com.zhiliaoapp.musically -c android.intent.category.LAUNCHER 1")
    else:
        device.install(f"C:\\Users\\89096\\PycharmProjects\\seopars\\apks\\tt.apk")
        device.shell("monkey -p com.zhiliaoapp.musically -c android.intent.category.LAUNCHER 1")
    time.sleep(2.5)


def create_assets(device=check_device()[0]):
    with open('C:\\Users\\89096\\PycharmProjects\seopars\\uni\\assets\\buttons\\aa', "r") as f:
        lists = f.readlines()
    for i in lists:
        print(i)
        with open(f"C:\\Users\\89096\\PycharmProjects\seopars\\uni\\assets\\elements.xml", "w+",
                  encoding="utf-8") as file:
            file.write(str(device.shell("uiautomator dump /dev/tty"))[:-33])
        fd = open(f"C:\\Users\\89096\\PycharmProjects\seopars\\uni\\assets\\elements.xml", 'r', encoding="utf-8")
        xml_file = fd.read()
        soup = BeautifulSoup(xml_file, 'lxml')
        btn = soup.find(name="node", attrs={'resource-id': i.replace("\n", "")})
        bounds = re.sub('\D', ' ', btn["bounds"]).split(" ")
        x, y = [statistics.mean([int(bounds[1]), int(bounds[4])]), statistics.mean([int(bounds[2]), int(bounds[5])])]
        fd.close()
        btns = open("C:\\Users\\89096\\PycharmProjects\\seopars\\uni\\assets\\buttons\\tt", "a")
        if "android.widget.FrameLayout" in str(btn['class']) or "android.widget.Button" in str(
                btn['class']) or "android.widget.TextView" in str(btn['class']):
            print(f"{btn['resource-id']} | tap {x} {y}")
            btns.write(f"{btn['resource-id']} | tap {x} {y}\n")
            device.shell(f"input tap {x} {y}")
        if "android:id/button3" == str(btn['resource-id']):
            print(f"{btn['resource-id']} | swipe 221.5 1811 221 1111 100")
            btns.write(f"{btn['resource-id']} | swipe 221.5 1811 221 1111 100\n")
            device.shell(f"input swipe 221.5 1811 221 1111 100")
        elif 'android.view.View' in str(btn['class']):
            print(f"{btn['resource-id']} | swipe {x} {bounds[5]} {x} {bounds[2]} {random.randint(53, 56)}")
            btns.write(f"{btn['resource-id']} | swipe {x} {bounds[5]} {x} {bounds[2]} {random.randint(53, 56)}\n")
            device.shell(f"input swipe {x} {bounds[2]} {x} {bounds[5]} {random.randint(53, 56)}")
        elif 'android.widget.EditText' in str(btn['class']):
            if 'true' in str(btn['password']):
                print(f"{btn['resource-id']} | input text [RANDOM_LETTERS]\n")
                btns.write(f"{btn['resource-id']} | input text [RANDOM_password]\n")
                device.shell(f"input text {random.sample(chars, 10)}")
            elif 'nickname' in str(btn['text']):
                with open("C:\\Users\\89096\\PycharmProjects\\seopars\\uni\\res\\names", "r") as n:
                    name = random.sample(n.readlines())
                btns.write(f"{btn['resource-id']} | input text [name]\n")
                device.shell(f"input text {name}")
            elif 'Email' in str(btn['text']):
                btns.write(f"{btn['resource-id']} | input text [RANDOM_mail]\n")
                device.shell(f"input text {random.sample(string.ascii_letters, 5)}@mail.ru")

        else:
            pass
        btns.close()
        print(2)


if __name__ == '__main__':
    device, client = check_device()
    start_tt(device)
    create_assets()
