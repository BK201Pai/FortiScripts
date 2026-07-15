import os
import re

# Add timestamp in format [YYYY-MM-DD-HH-MM-SS] taken from execute date and execute time in script loop

if __name__ == '__main__':
    files = [f for f in os.listdir() if f.endswith(".log")]
    for file in files:
        time = ""
        date = ""
        f = open(file, "r")
        converted = open(file+"-converted.txt", "w")
        while 1:
            line=f.readline()
            if not line:
                break
            if "execute time" in line:
                f.readline()
                time = f.readline().split(":",1)
                while "current time is" not in time[0]:
                    time = f.readline().split(":",1)
                time = time[1]
                time = str(time).replace("\n","")
                time = time.replace(" ", "")
                continue
            if "execute date" in line:
                date = f.readline().split(":",1)
                while "current date is" not in date[0]:
                    date = f.readline().split(":",1)
                date = date[1]
                date = str(date).replace("\n","")
                date = date.replace(" ", "")
                continue
            line = f"[{date}-{time}]" +" " + line
            converted.write(line)
        f.close()
        converted.close()

