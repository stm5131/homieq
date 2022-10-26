#!/usr/bin/env python3
import datetime
import time
from statistics import mean
try:
    # Transitional fix for breaking change in LTR559
    from ltr559 import LTR559
    ltr559 = LTR559()
except ImportError:
    import ltr559

# Calulate avg and return bool for occupant
def user_present(time_to_observe) -> bool:
    try:
        time_before_start = datetime.datetime.now()
        present = False
        prox_list = []
        while present is False:
            prox = ltr559.get_proximity()
            current_time = datetime.datetime.now()
            time_diff = current_time - time_before_start
            print(time_diff.seconds)
            prox_list.append(prox)
            if int(time_diff.seconds) >= time_to_observe:
                if mean(prox_list) >= 2:
                    present = True
                else:
                    break
            time.sleep(1.0)
        return present
    except KeyboardInterrupt:
        pass

def main():
    print(user_present(300))

if __name__ == '__main__':
    main()