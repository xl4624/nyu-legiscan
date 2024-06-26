import builtins
import datetime
from src.config import LOCAL_TIMEZONE

# Save the original print function
original_print = builtins.print

def custom_print(*args, **kwargs):
    # Get the current timezone and timestamp
    timestamp = datetime.datetime.now(LOCAL_TIMEZONE).strftime("%Y-%m-%d %H:%M:%S %Z%z")

    message = " ".join(map(str, args))
    log_entry = f"\n[{timestamp}] {message}"
    
    # Write the log entry to a file
    with open("logfile.log", "a") as log_file:
        log_file.write(log_entry)
    
    if kwargs.get("print_to_console", True): # Optionally, call the original print function to also print to console
        original_print(log_entry.strip())

builtins.print = custom_print

# Example usage
# print("This is a test message.")
# print("Another message with more details.", print_to_console=False)
