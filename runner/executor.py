import subprocess
def run_command(command,path="."):
    if not command:
        print("No command found.")
        return 
    try:
        print("\nRunning in {path}...\n")
        process=subprocess.Popen(
            command,
            shell=True,
            cwd=path
        )
        process.communicate()

    except Exception as e:
        print("Error:",e)
        