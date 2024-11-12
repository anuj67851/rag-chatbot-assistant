import os
import logging
import threading
import csv


class CSVFormatter(logging.Formatter):
    def __init__(self, fields):
        super().__init__()
        self.fields = fields

    def format(self, record):
        # Ensure `asctime` is populated by calling `formatTime`
        record.asctime = self.formatTime(record, self.datefmt)
        # Use `getMessage()` to ensure the `message` field is captured correctly
        record.message = record.getMessage()

        # Create a log entry with specified fields
        log_entry = {field: getattr(record, field, "") for field in self.fields}
        return ",".join(f'"{log_entry[field]}"' for field in self.fields)


class LoggingUtility:
    def __init__(self, log_dir="logs"):
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        # Define the fields you want in the CSV log file
        self.fields = [
            "asctime",
            "levelname",
            "message",
            "filename",
            "funcName",
            "lineno",
        ]

        # Set up the log file path in CSV format
        self.log_file_path = os.path.join(log_dir, "file_processor_log.csv")

        # Create a logging handler that writes to the CSV file
        csv_handler = logging.FileHandler(
            self.log_file_path, mode="a", encoding="utf-8"
        )
        csv_formatter = CSVFormatter(self.fields)
        csv_handler.setFormatter(csv_formatter)

        # Set up the logger
        self.logger = logging.getLogger("CSVLogger")
        self.logger.setLevel(logging.INFO)
        self.logger.addHandler(csv_handler)

        # Write CSV headers if the log file is empty
        if os.stat(self.log_file_path).st_size == 0:
            with open(self.log_file_path, mode="w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(self.fields)

        # Initialize a lock for thread-safe logging
        self.log_lock = threading.Lock()

    def log_success(self, file_name):
        with self.log_lock:
            self.logger.info(f"Successfully processed file: {file_name}")

    def log_error(self, file_name, error_message):
        with self.log_lock:
            self.logger.error(
                f"Failed to process file: {file_name} - Error: {error_message}"
            )
