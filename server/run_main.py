import subprocess
import multiprocessing
import sys

def monitor_logs(process):
    """ Continuously reads logs from assistant_process """
    while process.poll() is None:  # Check if the process is still running
        output = process.stdout.readline()
        if output:
            sys.stdout.write(f"[LOG] {output}")  # Print logs in real-time
        error = process.stderr.readline()
        if error:
            sys.stderr.write(f"[ERROR] {error}")  # Print errors in real-time

def start_server():
    """ Start the assistant process and keep it running """
    assistant_process = subprocess.Popen(
        ["py", "main.py", "start"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1,
        universal_newlines=True
    )

    # Create and start a separate process for monitoring logs
    log_process = multiprocessing.Process(target=monitor_logs, args=(assistant_process,))
    log_process.start()

    assistant_process.wait()  # Wait for server to exit
    log_process.terminate()  # Stop log monitoring when server stops

