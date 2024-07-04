
def print_stdout(process):
    for line in iter(process.stdout.readline, ''):
        if line:
            print("Blender Logs:", line.strip())

def print_stderr(process):
    for line in iter(process.stderr.readline, ''):
        if line:
            print("Error Blender Logs:", line.strip())
