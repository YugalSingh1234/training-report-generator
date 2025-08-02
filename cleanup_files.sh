#!/bin/bash
# File Cleanup and Management Script
# Manages DOCX files and prevents storage issues

# Configuration
OUTPUT_DIR="/opt/word-generator/output"
UPLOAD_DIR="/opt/word-generator/static/uploads"
BACKUP_DIR="/opt/backups/files"
MAX_OUTPUT_FILES=50
MAX_UPLOAD_FILES=100
DAYS_TO_KEEP=30

echo "Starting file cleanup process..."

# Create backup directory if not exists
mkdir -p "$BACKUP_DIR"

# Function to cleanup old files
cleanup_old_files() {
    local dir=$1
    local days=$2
    local max_files=$3
    
    echo "Cleaning up $dir..."
    
    # Remove files older than specified days
    find "$dir" -name "*.docx" -mtime +$days -type f -delete
    find "$dir" -name "*.jpg" -mtime +$days -type f -delete
    find "$dir" -name "*.jpeg" -mtime +$days -type f -delete
    find "$dir" -name "*.png" -mtime +$days -type f -delete
    
    # Keep only the newest files if we exceed max count
    local file_count=$(find "$dir" -type f | wc -l)
    if [ $file_count -gt $max_files ]; then
        echo "Too many files ($file_count), keeping only newest $max_files"
        find "$dir" -type f -printf '%T@ %p\n' | sort -n | head -n -$max_files | cut -d' ' -f2- | xargs rm -f
    fi
}

# Backup important files before cleanup
echo "Creating backup of recent files..."
find "$OUTPUT_DIR" -name "*.docx" -mtime -7 -exec cp {} "$BACKUP_DIR/" \;

# Cleanup output directory
cleanup_old_files "$OUTPUT_DIR" $DAYS_TO_KEEP $MAX_OUTPUT_FILES

# Cleanup upload directory
cleanup_old_files "$UPLOAD_DIR" $DAYS_TO_KEEP $MAX_UPLOAD_FILES

# Check disk usage
echo "Disk usage after cleanup:"
df -h "$OUTPUT_DIR"
du -sh "$OUTPUT_DIR"
du -sh "$UPLOAD_DIR"

# Log cleanup results
echo "$(date): File cleanup completed" >> /var/log/word-generator-cleanup.log
echo "Output files: $(find $OUTPUT_DIR -type f | wc -l)" >> /var/log/word-generator-cleanup.log
echo "Upload files: $(find $UPLOAD_DIR -type f | wc -l)" >> /var/log/word-generator-cleanup.log

echo "File cleanup process completed!"
