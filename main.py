#!/usr/bin/env python3

import argparse
import os
import hashlib
import json
import sys
from collections import defaultdict
from datetime import datetime

# Constants
BLOCK_SIZE = 65536  # 64KB
CACHE_FILE = ".dup_cache.json"

def calculate_hash(file_path, algorithm='md5'):
    """Calculate hash of a file"""
    hasher = hashlib.new(algorithm)
    try:
        with open(file_path, 'rb') as f:
            while True:
                data = f.read(BLOCK_SIZE)
                if not data:
                    break
                hasher.update(data)
        return hasher.hexdigest()
    except Exception as e:
        print(f"Error hashing {file_path}: {e}")
        return None

def get_file_size(file_path):
    """Get file size in bytes"""
    try:
        return os.path.getsize(file_path)
    except Exception as e:
        print(f"Error getting size of {file_path}: {e}")
        return 0

def format_size(size_bytes):
    """Format file size in human-readable format"""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.1f} PB"

def find_duplicates(directory, recursive=True, use_hash=True, size_only=False, 
                   min_size=0, max_size=None, include_hidden=False, 
                   extensions=None, cache=True):
    """Find duplicate files in a directory"""
    
    # Load cache if enabled
    cache_file = os.path.join(directory, CACHE_FILE)
    file_cache = {}
    
    if cache and os.path.exists(cache_file):
        try:
            with open(cache_file, 'r') as f:
                file_cache = json.load(f)
        except:
            pass
    
    # Group files by size first
    size_groups = defaultdict(list)
    total_files = 0
    
    # Scan directory
    if recursive:
        for root, dirs, files in os.walk(directory):
            # Skip hidden directories if not include_hidden
            if not include_hidden:
                dirs[:] = [d for d in dirs if not d.startswith('.')]
            
            for file in files:
                # Skip hidden files if not include_hidden
                if not include_hidden and file.startswith('.'):
                    continue
                
                file_path = os.path.join(root, file)
                
                # Skip cache file
                if file == CACHE_FILE:
                    continue
                
                # Filter by extension
                if extensions:
                    file_ext = os.path.splitext(file)[1].lower()
                    if file_ext not in extensions:
                        continue
                
                # Get file size
                file_size = get_file_size(file_path)
                
                # Filter by size
                if file_size < min_size:
                    continue
                if max_size is not None and file_size > max_size:
                    continue
                
                size_groups[file_size].append(file_path)
                total_files += 1
    else:
        try:
            files = os.listdir(directory)
            for file in files:
                # Skip hidden files if not include_hidden
                if not include_hidden and file.startswith('.'):
                    continue
                
                file_path = os.path.join(directory, file)
                
                # Skip cache file
                if file == CACHE_FILE:
                    continue
                
                # Only process files
                if not os.path.isfile(file_path):
                    continue
                
                # Filter by extension
                if extensions:
                    file_ext = os.path.splitext(file)[1].lower()
                    if file_ext not in extensions:
                        continue
                
                # Get file size
                file_size = get_file_size(file_path)
                
                # Filter by size
                if file_size < min_size:
                    continue
                if max_size is not None and file_size > max_size:
                    continue
                
                size_groups[file_size].append(file_path)
                total_files += 1
        except Exception as e:
            print(f"Error reading directory: {e}")
            return []
    
    # Find duplicates
    duplicates = []
    files_processed = 0
    
    for size, files in size_groups.items():
        if len(files) < 2:
            continue
        
        # For small files, we can just use size as identifier
        if size_only or (size < 1024 and not use_hash):
            duplicates.append((size, files))
            continue
        
        # Group by hash
        if use_hash:
            hash_groups = defaultdict(list)
            
            for file_path in files:
                # Check cache first
                cache_key = f"{file_path}:{size}"
                file_hash = file_cache.get(cache_key)
                
                if file_hash is None:
                    file_hash = calculate_hash(file_path)
                    if file_hash:
                        file_cache[cache_key] = file_hash
                
                if file_hash:
                    hash_groups[file_hash].append(file_path)
                
                files_processed += 1
                # Show progress
                progress = (files_processed / total_files) * 100
                print(f"\rProcessing: {progress:.1f}%", end='')
            
            # Add groups with multiple files
            for hash_value, hash_files in hash_groups.items():
                if len(hash_files) > 1:
                    duplicates.append((hash_value, hash_files))
    
    # Save cache
    if cache:
        try:
            with open(cache_file, 'w') as f:
                json.dump(file_cache, f)
        except:
            pass
    
    print("\rProcessing: 100.0%")
    return duplicates

def display_duplicates(duplicates, sort_by='size', show_total=True):
    """Display found duplicates"""
    if not duplicates:
        print("\nNo duplicates found!")
        return
    
    # Sort duplicates
    if sort_by == 'size':
        duplicates.sort(key=lambda x: len(x[1]), reverse=True)
    elif sort_by == 'count':
        duplicates.sort(key=lambda x: len(x[1]), reverse=True)
    
    total_files = sum(len(files) for _, files in duplicates)
    total_size = sum(get_file_size(files[0]) * (len(files) - 1) for _, files in duplicates)
    
    print(f"\nFound {len(duplicates)} sets of duplicates")
    print(f"Total duplicate files: {total_files}")
    print(f"Total wasted space: {format_size(total_size)}")
    print("=" * 50)
    
    for i, (identifier, files) in enumerate(duplicates, 1):
        file_size = get_file_size(files[0])
        print(f"\nDuplicate set #{i} (Size: {format_size(file_size)})")
        
        for j, file_path in enumerate(files, 1):
            file_time = datetime.fromtimestamp(os.path.getmtime(file_path))
            print(f"  {j}. {file_path} - Modified: {file_time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    print("=" * 50)

def delete_duplicates(duplicates, keep='newest', dry_run=True):
    """Delete duplicate files (keeping one copy)"""
    deleted_count = 0
    skipped_count = 0
    total_removed_size = 0
    
    print(f"\n{'DRY RUN:' if dry_run else 'DELETING'} Removing duplicates...")
    
    for _, files in duplicates:
        if len(files) < 2:
            continue
        
        # Determine which file to keep
        files_with_time = [(f, os.path.getmtime(f)) for f in files]
        
        if keep == 'newest':
            files_with_time.sort(key=lambda x: x[1], reverse=True)
        elif keep == 'oldest':
            files_with_time.sort(key=lambda x: x[1])
        elif keep == 'first':
            pass  # Keep the order as is
        
        # Keep the first file, delete the rest
        keep_file = files_with_time[0][0]
        
        for i in range(1, len(files_with_time)):
            delete_file = files_with_time[i][0]
            file_size = get_file_size(delete_file)
            
            if dry_run:
                print(f"Would delete: {delete_file}")
            else:
                try:
                    os.remove(delete_file)
                    print(f"Deleted: {delete_file}")
                    deleted_count += 1
                    total_removed_size += file_size
                except Exception as e:
                    print(f"Error deleting {delete_file}: {e}")
                    skipped_count += 1
    
    if dry_run:
        print(f"\nWould delete {deleted_count} files")
    else:
        print(f"\nDeleted {deleted_count} files")
        print(f"Freed up: {format_size(total_removed_size)}")
        if skipped_count > 0:
            print(f"Skipped {skipped_count} files due to errors")

def main():
    parser = argparse.ArgumentParser(description="Find and optionally remove duplicate files")
    
    # Basic arguments
    parser.add_argument("directory", nargs="?", default=".", help="Directory to search (default: current)")
    parser.add_argument("-r", "--recursive", action="store_true", help="Search recursively in subdirectories")
    parser.add_argument("-d", "--delete", action="store_true", help="Delete duplicate files")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be deleted without actually deleting")
    
    # Filtering options
    parser.add_argument("--min-size", type=int, default=0, help="Minimum file size in bytes")
    parser.add_argument("--max-size", type=int, help="Maximum file size in bytes")
    parser.add_argument("-e", "--extensions", help="Comma-separated list of file extensions (e.g., .jpg,.png)")
    parser.add_argument("-a", "--include-hidden", action="store_true", help="Include hidden files and directories")
    
    # Hash options
    parser.add_argument("--no-hash", action="store_true", help="Don't use hash comparison (faster but less accurate)")
    parser.add_argument("--size-only", action="store_true", help="Compare files by size only")
    parser.add_argument("--no-cache", action="store_true", help="Don't use or create hash cache")
    
    # Display options
    parser.add_argument("-s", "--sort", choices=['size', 'count'], default='size', help="Sort duplicates by size or count")
    
    # Deletion options
    parser.add_argument("--keep", choices=['newest', 'oldest', 'first'], default='newest', 
                       help="Which file to keep when deleting duplicates")
    
    args = parser.parse_args()
    
    # Parse extensions
    extensions = None
    if args.extensions:
        extensions = [ext.strip() if ext.startswith('.') else f".{ext.strip()}" 
                     for ext in args.extensions.split(',')]
    
    # Find duplicates
    duplicates = find_duplicates(
        directory=args.directory,
        recursive=args.recursive,
        use_hash=not args.no_hash,
        size_only=args.size_only,
        min_size=args.min_size,
        max_size=args.max_size,
        include_hidden=args.include_hidden,
        extensions=extensions,
        cache=not args.no_cache
    )
    
    # Display results
    display_duplicates(duplicates, sort_by=args.sort)
    
    # Delete duplicates if requested
    if args.delete or args.dry_run:
        delete_duplicates(duplicates, keep=args.keep, dry_run=not args.delete)

if __name__ == "__main__":
    main()
