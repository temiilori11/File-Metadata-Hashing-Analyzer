# File Metadata & Hashing Analyzer

## Overview
This is a beginner-level **digital forensics project** that safely acquires files, computes SHA-256 hashes for integrity verification, and extracts metadata (creation/modification dates, embedded info) using Python and ExifTool.  

It demonstrates key forensic principles: **acquisition, verification, and analysis**.

---

## Features
- **Safe File Acquisition:** Copies files from a source folder to a working folder while preserving timestamps.  
- **SHA-256 Hashing:** Computes hashes for all files to verify integrity later.  
- **Metadata Extraction:** Extracts embedded metadata and filesystem info for images, documents, and text files.  
- **Logging:** Records acquisition and processing steps in log files.  

---

## Requirements
- Python 3.x  
- [ExifTool](https://exiftool.org/)  
- Windows OS (tested)  

---

## Usage
1. Place your files in the `source_files` folder.  
2. Run the Python script:  

```bash
python forensic_workflow.py
