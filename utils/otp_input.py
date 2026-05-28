"""
Pauses the test and waits for the user to manually type the OTP
received on their phone. Shows a live countdown so you know how
much time is left before the OTP expires.
"""
import sys
import time
import threading


def _countdown(seconds_total, stop_event):
    """Runs in a background thread — prints the countdown every second."""
    start = time.time()
    while not stop_event.is_set():
        elapsed = time.time() - start
        remaining = max(0, seconds_total - int(elapsed))
        mins, secs = divmod(remaining, 60)
        bar_filled = int((remaining / seconds_total) * 20)
        bar = "#" * bar_filled + "-" * (20 - bar_filled)
        sys.stdout.write(f"\r  OTP expires in: {mins:02d}:{secs:02d}  [{bar}]  ")
        sys.stdout.flush()
        if remaining == 0:
            break
        time.sleep(1)


def prompt_for_otp(expiry_seconds=300, label="OTP"):
    """
    Pauses execution, shows a countdown, and returns whatever
    the user types.

    Args:
        expiry_seconds: How long the OTP is valid (default 300 = 5 min)
        label:          What to call the code in the prompt message

    Returns:
        str: The OTP entered by the user (stripped, digits only)

    Raises:
        TimeoutError: If the user takes longer than expiry_seconds
        ValueError:   If the user enters an empty string
    """
    print("\n" + "=" * 55)
    print(f"  ACTION REQUIRED: Check your phone for the {label}")
    print(f"  You have {expiry_seconds // 60} minutes to enter it below.")
    print("=" * 55)

    stop_event = threading.Event()
    timer_thread = threading.Thread(
        target=_countdown, args=(expiry_seconds, stop_event), daemon=True
    )
    timer_thread.start()

    try:
        code = input(f"\n  Enter {label} here and press Enter: ").strip()
    finally:
        stop_event.set()
        sys.stdout.write("\n")

    if not code:
        raise ValueError(f"{label} cannot be empty.")

    digits = "".join(filter(str.isdigit, code))
    if not digits:
        raise ValueError(f"'{code}' does not look like a valid {label}.")

    print(f"  Got {label}: {digits}  — submitting...\n")
    return digits
