import logging
import re
from collections import Counter
import csv
import os
from pathlib import Path
from datetime import datetime


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

#Assignment 1
"""
Find & Replace
Write replace_in_file(filename, old, new) that reads a text file, replaces all occurrences of old with new, and writes back.
"""

def replace_in_file(input_path="./Input_files/ip1.txt", text1 = "old", text2 = "new", output_path="./outputs/op1.txt"):
    with open(input_path, 'r') as file:
        content = file.read()
    
    content = content.replace(text1, text2)
    
    with open(output_path, 'w') as file:
        file.write(content)
    logger.info(f"Replaced '{text1}' with '{text2}' in {input_path} and saved to {output_path}")

    

#Assignment 2
"""
Word Frequency Counter
Read a text file, count how often each word appears (ignore punctuation, case-fold words), and print the top 10 most frequent.
"""


def word_frequency_counter(input_path="./Input_files/ip2.txt"):

    with open(input_path, 'r') as file:
        content = file.read()
    # Remove punctuation and convert to lowercase
    content = re.sub(r'[^\w\s]', '', content).lower()
    # Split into words
    words = content.split()
    # Count word frequencies
    word_counts = Counter(words)
    
    most_common = word_counts.most_common(10)
    
    for word, count in most_common:
        print(f'{word}: {count}')


#Assignment 3
"""
Merge Two Files Line-by-Line
Given file1.txt and file2.txt, produce merged.txt where each line is line_from_file1 + " " + line_from_file2. Handle differing lengths gracefully.
"""
def merge_files(file1_path= "./Input_files/ip3a.txt", file2_path="./Input_files/ip3b.txt", output_path="./outputs/op3.txt"):
    with open(file1_path, 'r') as f1, open(file2_path, 'r') as f2:
        lines1 = f1.readlines()
        lines2 = f2.readlines()
    
    with open(output_path, 'w') as out_file:
        max_lines = max(len(lines1), len(lines2))
        
        for i in range(max_lines):
            # Get line from each file (or empty string if file has fewer lines)
            line1 = lines1[i].strip() if i < len(lines1) else ''
            line2 = lines2[i].strip() if i < len(lines2) else ''
            
            # Write merged line
            merged_line = f"{line1} {line2}".strip()
            out_file.write(merged_line + '\n')
    
    logger.info(f"Merged {file1_path} and {file2_path} into {output_path}")


#Assignment 4
"""
Partial File Reader
Implement read_chunk(filename, start_byte, length) using seek and read that returns exactly length bytes starting from start_byte.
"""
def read_chunk(filename="./Input_files/ip3a.txt", start_byte=0, length=10):
    if start_byte < 0 or length < 0:
            raise ValueError("start_byte and length must be non-negative")
    
    try:
        with open(filename, 'rb') as file:
            file.seek(start_byte)
            chunk = file.read(length)

        # If we didn't get enough bytes (hit EOF), pad with zeros
        if len(chunk) < length:
            chunk += b'\x00' * (length - len(chunk))

        logger.info(f"Read {length} bytes from {filename} starting at byte {start_byte}")
        return chunk
    except FileNotFoundError:
        logger.error(f"File not found: {filename}")
    except Exception as e:
        logger.error(f"Error reading file: {str(e)}")
    
    

#Assignment 5
"""
Directory Snapshot
Write a script that walks through a given directory tree (using os.walk or pathlib) and writes a CSV of relative_path,size_bytes,last_modified for every file.
"""

def create_directory_snapshot(root_dir="./", output_csv="./outputs/directory_snapshot.csv"):
    
    root_path = Path(root_dir)
    
    with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['relative_path', 'size_bytes', 'last_modified'])
        
        for current_dir, _, files in os.walk(root_dir):
            current_path = Path(current_dir)
            
            for file in files:
                file_path = current_path / file
                try:
                    # Get file stats
                    stat = file_path.stat()
                    relative_path = file_path.relative_to(root_path).as_posix()
                    size_bytes = stat.st_size
                    last_modified = datetime.fromtimestamp(stat.st_mtime).isoformat()
                    
                    writer.writerow([relative_path, size_bytes, last_modified])
                except (PermissionError, FileNotFoundError) as e:
                    print(f"Skipping {file_path}: {str(e)}")
                    logger.warning(f"Skipping {file_path}: {str(e)}")
    logger.info(f"Directory snapshot saved to {output_csv}")