import subprocess


# params
access_log_path = './logs/access.log'
#####

proc = subprocess.Popen(['tail', '-F', access_log_path],
                        stdout=subprocess.PIPE, stderr=subprocess.PIPE)
while True:
    line = proc.stdout.readline()
    print(line)
