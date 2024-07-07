import os
import time
import random

class idk:
    def randomChoice(self):
        return random.choice([0, 1])

    def pulseCount(self):
        count = 0
        interval = 2  # seconds

        startTime = time.time()

        while time.time() - startTime < interval:
            pulse = self.randomChoice()
            if (pulse == 1):
                count += 1
                print(f"Pulse #{count}")

            time.sleep(0.1)  # Sleep for a short duration to prevent a tight loop

        return count


    def calcSpeed(self):
        rpm = self.pulseCount()
        r = 43.18 / 2
        speed = (2 * 3.142 * r / 60) * rpm

        return f"{speed:.2f}"

if __name__ == "__main__":
    idk = idk()
    print(idk.calcSpeed())


