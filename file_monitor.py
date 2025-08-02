#!/usr/bin/env python3
"""
File System Monitoring for Word Generator
Monitor DOCX file sizes, counts, and disk usage
"""
import os
import psutil
import json
from datetime import datetime
from pathlib import Path

class FileMonitor:
    def __init__(self, base_dir="/opt/word-generator"):
        self.base_dir = Path(base_dir)
        self.output_dir = self.base_dir / "output"
        self.upload_dir = self.base_dir / "static" / "uploads"
        
    def get_directory_stats(self, directory):
        """Get statistics for a directory."""
        directory = Path(directory)
        if not directory.exists():
            return {"error": f"Directory {directory} does not exist"}
            
        stats = {
            "path": str(directory),
            "total_files": 0,
            "total_size_mb": 0,
            "docx_files": 0,
            "docx_size_mb": 0,
            "image_files": 0,
            "image_size_mb": 0,
            "largest_file": {"name": "", "size_mb": 0},
            "oldest_file": {"name": "", "date": ""},
            "newest_file": {"name": "", "date": ""}
        }
        
        try:
            files = list(directory.rglob("*"))
            files = [f for f in files if f.is_file()]
            
            if not files:
                return stats
                
            stats["total_files"] = len(files)
            
            # Analyze each file
            largest_size = 0
            oldest_time = float('inf')
            newest_time = 0
            
            for file_path in files:
                try:
                    file_stat = file_path.stat()
                    size_mb = file_stat.st_size / (1024 * 1024)
                    stats["total_size_mb"] += size_mb
                    
                    # Check file type
                    if file_path.suffix.lower() == '.docx':
                        stats["docx_files"] += 1
                        stats["docx_size_mb"] += size_mb
                    elif file_path.suffix.lower() in ['.jpg', '.jpeg', '.png', '.gif']:
                        stats["image_files"] += 1
                        stats["image_size_mb"] += size_mb
                    
                    # Track largest file
                    if size_mb > largest_size:
                        largest_size = size_mb
                        stats["largest_file"] = {
                            "name": file_path.name,
                            "size_mb": round(size_mb, 2)
                        }
                    
                    # Track oldest/newest files
                    mtime = file_stat.st_mtime
                    if mtime < oldest_time:
                        oldest_time = mtime
                        stats["oldest_file"] = {
                            "name": file_path.name,
                            "date": datetime.fromtimestamp(mtime).strftime("%Y-%m-%d %H:%M")
                        }
                    
                    if mtime > newest_time:
                        newest_time = mtime
                        stats["newest_file"] = {
                            "name": file_path.name,
                            "date": datetime.fromtimestamp(mtime).strftime("%Y-%m-%d %H:%M")
                        }
                        
                except (OSError, PermissionError):
                    continue
            
            # Round sizes
            stats["total_size_mb"] = round(stats["total_size_mb"], 2)
            stats["docx_size_mb"] = round(stats["docx_size_mb"], 2)
            stats["image_size_mb"] = round(stats["image_size_mb"], 2)
            
        except Exception as e:
            stats["error"] = str(e)
            
        return stats
    
    def get_disk_usage(self):
        """Get disk usage statistics."""
        try:
            usage = psutil.disk_usage(str(self.base_dir))
            return {
                "total_gb": round(usage.total / (1024**3), 2),
                "used_gb": round(usage.used / (1024**3), 2),
                "free_gb": round(usage.free / (1024**3), 2),
                "used_percent": round((usage.used / usage.total) * 100, 1)
            }
        except Exception as e:
            return {"error": str(e)}
    
    def check_file_limits(self):
        """Check if file counts or sizes exceed limits."""
        warnings = []
        
        # Check output directory
        output_stats = self.get_directory_stats(self.output_dir)
        if output_stats.get("total_files", 0) > 50:
            warnings.append(f"Output directory has {output_stats['total_files']} files (limit: 50)")
        
        if output_stats.get("total_size_mb", 0) > 500:
            warnings.append(f"Output directory size: {output_stats['total_size_mb']}MB (warning: >500MB)")
        
        # Check upload directory
        upload_stats = self.get_directory_stats(self.upload_dir)
        if upload_stats.get("total_files", 0) > 100:
            warnings.append(f"Upload directory has {upload_stats['total_files']} files (limit: 100)")
        
        if upload_stats.get("total_size_mb", 0) > 1000:
            warnings.append(f"Upload directory size: {upload_stats['total_size_mb']}MB (warning: >1GB)")
        
        # Check disk usage
        disk_usage = self.get_disk_usage()
        if disk_usage.get("used_percent", 0) > 85:
            warnings.append(f"Disk usage: {disk_usage['used_percent']}% (warning: >85%)")
        
        return warnings
    
    def generate_report(self):
        """Generate a comprehensive file monitoring report."""
        report = {
            "timestamp": datetime.now().isoformat(),
            "output_directory": self.get_directory_stats(self.output_dir),
            "upload_directory": self.get_directory_stats(self.upload_dir),
            "disk_usage": self.get_disk_usage(),
            "warnings": self.check_file_limits()
        }
        
        return report
    
    def save_report(self, filename=None):
        """Save monitoring report to file."""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"/var/log/file_monitor_{timestamp}.json"
        
        report = self.generate_report()
        
        try:
            with open(filename, 'w') as f:
                json.dump(report, f, indent=2)
            return filename
        except Exception as e:
            print(f"Error saving report: {e}")
            return None

def main():
    """Main function for command line usage."""
    monitor = FileMonitor()
    report = monitor.generate_report()
    
    print("="*50)
    print("FILE SYSTEM MONITORING REPORT")
    print("="*50)
    print(f"Generated: {report['timestamp']}")
    print()
    
    # Output directory stats
    output = report['output_directory']
    print("OUTPUT DIRECTORY:")
    print(f"  Files: {output.get('total_files', 0)} ({output.get('docx_files', 0)} DOCX)")
    print(f"  Size: {output.get('total_size_mb', 0)}MB")
    if output.get('largest_file', {}).get('name'):
        print(f"  Largest: {output['largest_file']['name']} ({output['largest_file']['size_mb']}MB)")
    print()
    
    # Upload directory stats
    upload = report['upload_directory']
    print("UPLOAD DIRECTORY:")
    print(f"  Files: {upload.get('total_files', 0)} ({upload.get('image_files', 0)} images)")
    print(f"  Size: {upload.get('total_size_mb', 0)}MB")
    if upload.get('largest_file', {}).get('name'):
        print(f"  Largest: {upload['largest_file']['name']} ({upload['largest_file']['size_mb']}MB)")
    print()
    
    # Disk usage
    disk = report['disk_usage']
    print("DISK USAGE:")
    print(f"  Used: {disk.get('used_gb', 0)}GB / {disk.get('total_gb', 0)}GB ({disk.get('used_percent', 0)}%)")
    print(f"  Free: {disk.get('free_gb', 0)}GB")
    print()
    
    # Warnings
    if report['warnings']:
        print("⚠️  WARNINGS:")
        for warning in report['warnings']:
            print(f"  - {warning}")
    else:
        print("✅ No warnings - all file limits within normal ranges")
    
    print("="*50)

if __name__ == "__main__":
    main()
