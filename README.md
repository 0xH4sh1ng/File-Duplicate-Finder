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
