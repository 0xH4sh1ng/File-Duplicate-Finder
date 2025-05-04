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
git clone https://github.com/0xH4sh1ng/file-duplicate-finder.git
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

## 📝 Examples

### Find duplicates in current directory:
```bash
python main.py
```

### Find duplicates recursively in a specific directory:
```bash
python main.py ~/Downloads -r
```

### Find duplicates of specific file types:
```bash
python main.py /path/to/photos -r -e .jpg,.png,.gif
```

### Find large duplicate files:
```bash
python main.py --min-size 1048576 -r  # Files larger than 1MB
```

### Dry run to see what would be deleted:
```bash
python main.py -r --dry-run
```

### Delete duplicates keeping the newest version:
```bash
python main.py -r -d --keep newest
```

### Find duplicates by size only (faster):
```bash
python main.py -r --size-only
```

### Include hidden files in search:
```bash
python main.py -a
```

### Sort results by number of duplicates:
```bash
python main.py -r -s count
```

## 🔧 How It Works

The tool uses a multi-step approach to find duplicates efficiently:

1. **Size Grouping**: First groups files by size (files of different sizes can't be duplicates)
2. **Hash Calculation**: For files of the same size, calculates MD5 hash to verify content
3. **Comparison**: Files with the same hash are true duplicates
4. **Caching**: Stores hashes to speed up subsequent scans

### Deletion Strategy

When deleting duplicates, you can choose which file to keep:
- `newest`: Keep the most recently modified file
- `oldest`: Keep the oldest file
- `first`: Keep the first file encountered in the scan

## 💡 Tips

- Use `--dry-run` before actually deleting files
- For large directories, the first run may take time but subsequent runs will be faster due to caching
- Use `--size-only` for quick scans when you don't need perfect accuracy
- The cache file (`.dup_cache.json`) can be safely deleted to start fresh
- For photo/video files, use appropriate extensions to focus the search
- When deleting, choose the retention strategy that makes sense for your use case

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.
