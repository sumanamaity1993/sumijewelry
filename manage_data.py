#!/usr/bin/env python
"""
Data Management Script for Sumi Jewelry Store

This script helps manage database and media files for the separate
database management approach used with free hosting platforms.
"""

import os
import shutil
import zipfile
from datetime import datetime
from pathlib import Path

def create_backup():
    """Create a backup of current local database and media files"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = f"backup_{timestamp}"
    
    print(f"Creating backup: {backup_dir}")
    
    # Create backup directory
    os.makedirs(backup_dir, exist_ok=True)
    
    # Backup database
    if os.path.exists("db.sqlite3"):
        shutil.copy2("db.sqlite3", f"{backup_dir}/db.sqlite3")
        print("✓ Database backed up")
    else:
        print("⚠ No database file found")
    
    # Backup media files
    if os.path.exists("media"):
        shutil.copytree("media", f"{backup_dir}/media")
        print("✓ Media files backed up")
    else:
        print("⚠ No media directory found")
    
    # Create zip file
    zip_filename = f"{backup_dir}.zip"
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(backup_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, backup_dir)
                zipf.write(file_path, arcname)
    
    # Clean up backup directory
    shutil.rmtree(backup_dir)
    
    print(f"✓ Backup created: {zip_filename}")
    return zip_filename

def restore_from_backup(backup_file):
    """Restore database and media from backup file"""
    if not os.path.exists(backup_file):
        print(f"❌ Backup file not found: {backup_file}")
        return
    
    print(f"Restoring from backup: {backup_file}")
    
    # Extract backup
    with zipfile.ZipFile(backup_file, 'r') as zipf:
        zipf.extractall("temp_restore")
    
    # Restore database
    if os.path.exists("temp_restore/db.sqlite3"):
        shutil.copy2("temp_restore/db.sqlite3", "db.sqlite3")
        print("✓ Database restored")
    
    # Restore media files
    if os.path.exists("temp_restore/media"):
        if os.path.exists("media"):
            shutil.rmtree("media")
        shutil.copytree("temp_restore/media", "media")
        print("✓ Media files restored")
    
    # Clean up
    shutil.rmtree("temp_restore")
    print("✓ Restore completed")

def list_backups():
    """List all available backup files"""
    backup_files = [f for f in os.listdir('.') if f.startswith('backup_') and f.endswith('.zip')]
    
    if not backup_files:
        print("No backup files found")
        return
    
    print("Available backups:")
    for backup in sorted(backup_files, reverse=True):
        size = os.path.getsize(backup) / (1024 * 1024)  # Size in MB
        print(f"  {backup} ({size:.1f} MB)")

def show_status():
    """Show current status of database and media files"""
    print("Current Status:")
    
    # Database status
    if os.path.exists("db.sqlite3"):
        size = os.path.getsize("db.sqlite3") / (1024 * 1024)  # Size in MB
        print(f"  Database: ✓ Present ({size:.1f} MB)")
    else:
        print("  Database: ❌ Not found")
    
    # Media status
    if os.path.exists("media"):
        media_count = sum([len(files) for r, d, files in os.walk("media")])
        print(f"  Media files: ✓ Present ({media_count} files)")
    else:
        print("  Media files: ❌ Not found")

def main():
    """Main function with menu"""
    print("Sumi Jewelry Store - Data Management")
    print("=" * 40)
    
    while True:
        print("\nOptions:")
        print("1. Create backup")
        print("2. Restore from backup")
        print("3. List backups")
        print("4. Show status")
        print("5. Exit")
        
        choice = input("\nEnter your choice (1-5): ").strip()
        
        if choice == "1":
            create_backup()
        elif choice == "2":
            list_backups()
            backup_file = input("Enter backup filename to restore: ").strip()
            if backup_file:
                restore_from_backup(backup_file)
        elif choice == "3":
            list_backups()
        elif choice == "4":
            show_status()
        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main() 