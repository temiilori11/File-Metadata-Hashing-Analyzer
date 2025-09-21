import os             # Provides functions to interact with the operating system (files/folders)
import shutil         # Allows copying files and preserving metadata like timestamps
import hashlib        # Used to compute SHA-256 hashes of files for integrity checks
import subprocess     # Used to run external programs like ExifTool
import time           # For converting timestamps into readable format
from datetime import datetime  # For logging exact acquisition times


# Config: Define source and working folders


# Folder where original “evidence” files are located
source_folder = r"C:\Users\temii\Documents\ForensicProject\source_files"

# Folder where working copies and forensic outputs will be stored
working_folder = r"C:\Users\temii\Documents\ForensicProject\working_files"

# Full path to ExifTool executable (used for metadata extraction)
exiftool_path = r"C:\Users\temii\Documents\ForensicProject\exiftool.exe"


# Step 1: Acquire files (Safe Copy)


# Create working folder if it doesn't exist
os.makedirs(working_folder, exist_ok=True)

# Path for acquisition log file
log_path = os.path.join(working_folder, "acq_log.txt")

# Open log file in append mode (creates if not exist)
with open(log_path, "a") as log:
    # Write a header with timestamp
    log.write(f"\n--- Acquisition started: {datetime.now()} ---\n")
    log.write(f"Source: {source_folder}\n")
    log.write(f"Destination: {working_folder}\n")

    # Loop through each file in the source folder
    for filename in os.listdir(source_folder):
        src_file = os.path.join(source_folder, filename)  # Full path to source file
        dst_file = os.path.join(working_folder, filename)  # Full path to copy destination

        # Only copy files (ignore subfolders)
        if os.path.isfile(src_file):
            shutil.copy2(src_file, dst_file)  # Copy file and preserve timestamps
            log.write(f"Copied {filename} at {datetime.now()}\n")  # Log each copied file

    # Write acquisition completion timestamp
    log.write(f"--- Acquisition complete: {datetime.now()} ---\n")

print(f"Files acquired and logged to {log_path}")


# Step 2: Compute SHA-256 Hashes


# Path for the hash output file
hash_file = os.path.join(working_folder, "hashes.txt")

# Open hashes.txt in write mode
with open(hash_file, "w") as f:
    # Loop through all files in the working folder
    for filename in os.listdir(working_folder):
        path = os.path.join(working_folder, filename)
        if os.path.isfile(path):
            h = hashlib.sha256()  # Create a new SHA-256 hash object
            # Read file in chunks to handle large files efficiently
            with open(path, "rb") as file:
                for block in iter(lambda: file.read(65536), b""):
                    h.update(block)  # Update hash with each block

            # Write the hash and filename to the hashes.txt file
            f.write(f"{h.hexdigest()}  {filename}\n")

print(f"SHA-256 hashes saved to {hash_file}")


# Step 3: Extract metadata + filesystem info


# Path for metadata output file
metadata_file = os.path.join(working_folder, "metadata.txt")

# Open metadata.txt in write mode
with open(metadata_file, "w") as out:
    # Loop through all files in the working folder
    for filename in os.listdir(working_folder):
        path = os.path.join(working_folder, filename)
        if os.path.isfile(path):
            # Run ExifTool to extract embedded metadata
            result = subprocess.run(
                [exiftool_path, path], capture_output=True, text=True
            )

            # Get filesystem info using os.stat
            stats = os.stat(path)
            fs_info = (
                f"File Size: {stats.st_size} bytes\n"  # Size in bytes
                f"Creation Time: {time.ctime(stats.st_ctime)}\n"  # Human-readable creation time
                f"Modification Time: {time.ctime(stats.st_mtime)}\n"  # Human-readable modification time
            )

            # Write a header for each file
            header = f"--- Metadata for {filename} ---\n"

            # Write header, ExifTool output, and filesystem info to metadata.txt
            out.write(header)
            out.write(result.stdout)
            out.write(fs_info)
            out.write("\n" + "-"*50 + "\n\n")  # Separator for clarity

            # Also print to terminal for live feedback
            print(header)
            print(result.stdout)
            print(fs_info)
            print("-"*50)

print(f"All metadata saved to {metadata_file}")