# 🔍 File Duplicate Finder

A simple command-line tool to find and optionally remove duplicate files in your directories.

## ✨ Features

- 🔎 Find duplicate files by comparing file content
- 🚀 Fast comparison using file size and optional hash
- 📁 Recursive directory scanning
- 🗑️ Delete duplicates with different retention strategies
- 💾 Cache file hashes for faster subsequent scans
- 🔧 Filter by file size and extension
- 🧪 Dry-run mode to preview what would be deleted
- 📊 Show wasted disk space statistics

## 🚀 Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/file-duplicate-finder.git
cd file-duplicate-finder
```

2. Make the script executable (Unix/Linux/macOS):
```bash
chmod +x main.py
```

## 🔍 Usage

```bash
python main.py [directory] [options]
```

## ⚙️ Options

Basic Options:

- `directory`: Directory to search (default: current directory)
- `-r, --recursive`: Search recursively in subdirectories
- `-d, --delete`: Delete duplicate files
- `--dry-run`: Show what would be deleted without actually deleting

Filtering Options:

- `--min-size`: Minimum file size in bytes
- `--max-size`: Maximum file size in bytes
- `-e, --extensions`: Comma-separated list of file extensions (e.g., .jpg,.png)
- `-a, --include-hidden`: Include hidden files and directories

Hash Options:

- `--no-hash`: Don't use hash comparison (faster but less accurate)
- `--size-only`: Compare files by size only
- `--no-cache`: Don't use or create hash cache

Display Options:

- `-s, --sort`: Sort duplicates by size or count

Deletion Options:

- `--keep`: Which file to keep when deleting duplicates (newest, oldest, first)
