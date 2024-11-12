import shutil
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import threading
import queue
import time
import os


class FileEventHandler(FileSystemEventHandler):
    def __init__(self, file_queue):
        self.file_queue = file_queue

    def on_created(self, event):
        if not event.is_directory:
            print(f"File detected: {event.src_path}")
            # A small delay to avoid multiple rapid triggers
            time.sleep(0.1)  # You can adjust the sleep duration if needed
            self.file_queue.put(event.src_path)


class FolderMonitor:
    def __init__(
        self,
        input_folder,
        processed_folder,
        error_folder,
        file_handler,
        vector_store_manager,
        logger,
        checking_timer=1,
    ):
        self.input_folder = input_folder
        self.processed_folder = processed_folder
        self.error_folder = error_folder
        self._initialize_folders()
        self.checking_timer = checking_timer
        self.file_handler = file_handler
        self.vector_store_manager = vector_store_manager
        self.logger = logger
        self.file_queue = queue.Queue()

    def _initialize_folders(self):
        os.makedirs(self.input_folder, exist_ok=True)
        os.makedirs(self.processed_folder, exist_ok=True)
        os.makedirs(self.error_folder, exist_ok=True)

    def start_monitoring(self):
        observer = Observer()
        event_handler = FileEventHandler(self.file_queue)
        observer.schedule(event_handler, self.input_folder, recursive=False)
        observer.start()

        threading.Thread(target=self._process_files_from_queue, daemon=True).start()

        try:
            while True:
                time.sleep(self.checking_timer)
        except KeyboardInterrupt:
            observer.stop()
        observer.join()

    def _process_files_from_queue(self):
        while True:
            file_path = self.file_queue.get()
            if file_path is None:  # Graceful exit
                break
            self._process_file(file_path)
            self.file_queue.task_done()

    def _process_file(self, file_path):
        try:
            # Adding a file lock to ensure no other thread can modify the file
            with open(file_path, "rb") as f:
                content = self.file_handler.read_file_contents(file_path)
                self.vector_store_manager.add_content_to_vectordb(content)

            # Move file after it has been processed
            shutil.move(
                file_path,
                os.path.join(self.processed_folder, os.path.basename(file_path)),
            )
            self.logger.log_success(file_path)

        except Exception as e:
            shutil.move(
                file_path, os.path.join(self.error_folder, os.path.basename(file_path))
            )
            self.logger.log_error(file_path, str(e))
