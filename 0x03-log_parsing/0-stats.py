#!/usr/bin/python3

import sys
import signal
from collections import defaultdict

class LogProcessor:
    def __init__(self):
        self.total_size = 0
        self.status_counts = defaultdict(int)
        self.line_count = 0
        self.valid_status_codes = {200, 301, 400, 401, 403, 404, 405, 500}
    
    def parse_line(self, line):
        """Parse a single log line and extract status code and file size."""
        try:
            # Split the line into parts
            parts = line.split('"')
            if len(parts) != 3:
                return None, None
            
            # Extract status code and file size from the last part
            metadata = parts[2].strip().split()
            if len(metadata) != 2:
                return None, None
                
            status_code = int(metadata[0])
            file_size = int(metadata[1])
            
            # Validate format using the first part
            ip_date = parts[0].strip()
            if not (ip_date.endswith(']') and '[' in ip_date):
                return None, None
                
            # Validate request format
            request = parts[1].strip()
            if not request.startswith('GET /projects/260 HTTP/1.1'):
                return None, None
            
            return status_code, file_size
            
        except (ValueError, IndexError):
            return None, None
    
    def process_line(self, line):
        """Process a single line of log data."""
        status_code, file_size = self.parse_line(line)
        
        if status_code is not None and file_size is not None:
            if status_code in self.valid_status_codes:
                self.status_counts[status_code] += 1
            self.total_size += file_size
            self.line_count += 1
            
            if self.line_count % 10 == 0:
                self.print_stats()
    
    def print_stats(self):
        """Print the current statistics."""
        print(f"File size: {self.total_size}")
        for code in sorted(self.valid_status_codes):
            if self.status_counts[code] > 0:
                print(f"{code}: {self.status_counts[code]}")

def signal_handler(signum, frame):
    """Handle the CTRL+C signal."""
    processor.print_stats()
    sys.exit(0)

# Create global processor instance for signal handler access
processor = LogProcessor()

def main():
    # Register signal handler
    signal.signal(signal.SIGINT, signal_handler)
    
    # Process stdin line by line
    try:
        for line in sys.stdin:
            processor.process_line(line.strip())
    except KeyboardInterrupt:
        processor.print_stats()
        sys.exit(0)

if __name__ == "__main__":
    main()
