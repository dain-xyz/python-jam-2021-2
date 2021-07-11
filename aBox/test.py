import os
import psutil
parent_pid = os.getppid()
print(psutil.Process(parent_pid).name())
input("Press any key to continue...")