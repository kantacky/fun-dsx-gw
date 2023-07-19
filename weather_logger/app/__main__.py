from core import core
from datetime import datetime

if __name__ == '__main__':
    dtstr = str(datetime.now())
    try:
        core()
        print(f"{dtstr}: Success")
    except Exception as e:
        print(f"{dtstr}: Error")
        print(f"{' ' * (len(dtstr) + 2)}{e}")
