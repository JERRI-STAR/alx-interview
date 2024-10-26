#!/usr/bin/python3
import sys
import signal
import re

def print_statistics(total_size, status_codes):
    """Print the required statistics."""
    print(f"File size: {total_size}")
    for code in sorted(status_codes.keys()):
        if status_codes[code] > 0:
            print(f"{code}: {status_codes[code]}")

def main():
    # Initialize metrics
    total_size = 0
    status_codes = {
        200: 0, 301: 0, 400: 0, 401: 0,
        403: 0, 404: 0, 405: 0, 500: 0
    }
    line_count = 0

    # Regular expression pattern for valid log entries
    pattern = r'^\S+ - \[\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{6}\] "GET /projects/260 HTTP/1.1" (\d+) (\d+)$'

    def signal_handler(sig, frame):
        """Handle CTRL+C interrupt."""
        print_statistics(total_size, status_codes)
        sys.exit(0)

    # Register signal handler for CTRL+C
    signal.signal(signal.SIGINT, signal_handler)

    try:
        for line in sys.stdin:
            try:
                # Process each line
                match = re.match(pattern, line.strip())
                if match:
                    status_code = int(match.group(1))
                    file_size = int(match.group(2))

                    # Update metrics
                    if status_code in status_codes:
                        status_codes[status_code] += 1
                    total_size += file_size

                    # Increment line counter
                    line_count += 1

                    # Print statistics every 10 lines
                    if line_count % 10 == 0:
                        print_statistics(total_size, status_codes)

            except ValueError:
                # Skip lines that can't be properly parsed
                continue

    except KeyboardInterrupt:
        # Handle CTRL+C
        print_statistics(total_size, status_codes)
        sys.exit(0)

if __name__ == "__main__":
    main()
