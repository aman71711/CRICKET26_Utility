"""
CRICKET 26 VERSION.JSON ADMIN PANEL
Simple Python script to manage version.json updates easily
Author: Cricket 26 Utility Team
"""

import json
import os
from datetime import datetime
from pathlib import Path

class Cricket26AdminPanel:
    def __init__(self, version_json_path="version.json"):
        self.version_json_path = Path(version_json_path)
        self.data = self.load_version_json()
    
    def load_version_json(self):
        """Load the version.json file"""
        if not self.version_json_path.exists():
            print(f"❌ Error: {self.version_json_path} not found!")
            return None
        
        with open(self.version_json_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def save_version_json(self):
        """Save changes to version.json with backup"""
        # Create backup
        backup_path = self.version_json_path.with_suffix('.json.backup')
        if self.version_json_path.exists():
            import shutil
            shutil.copy2(self.version_json_path, backup_path)
            print(f"✅ Backup created: {backup_path}")
        
        # Update timestamp
        self.data['metadata']['last_updated'] = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
        
        # Save with pretty formatting
        with open(self.version_json_path, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Saved: {self.version_json_path}")
    
    def add_new_update(self, from_ver, to_ver, gdrive_url, gdrive_file_id, 
                       checksum, size_mb, description, changelog_list):
        """Add a new update to the updates array"""
        
        # Calculate next update_id
        next_id = len(self.data['updates']) + 1
        
        new_update = {
            "update_id": next_id,
            "from_version": from_ver,
            "to_version": to_ver,
            "release_date": datetime.now().strftime("%Y-%m-%d"),
            "size_mb": size_mb,
            "mandatory": True,
            "description": description,
            "changelog": changelog_list,
            "downloads": {
                "primary": {
                    "type": "gdrive",
                    "name": "Google Drive Official Mirror",
                    "url": gdrive_url,
                    "file_id": gdrive_file_id,
                    "checksum": checksum
                },
                "fallback": []
            }
        }
        
        # Add to updates array
        self.data['updates'].append(new_update)
        
        # Update game_info
        if to_ver not in self.data['game_info']['all_versions']:
            self.data['game_info']['all_versions'].append(to_ver)
        self.data['game_info']['latest_version'] = to_ver
        
        print(f"✅ Added update: {from_ver} → {to_ver}")
        return new_update
    
    def add_fallback_link(self, update_id, link_type, name, url, checksum, file_id=None):
        """Add a fallback link to an existing update"""
        
        # Find update by ID
        update = next((u for u in self.data['updates'] if u['update_id'] == update_id), None)
        
        if not update:
            print(f"❌ Error: Update ID {update_id} not found!")
            return False
        
        fallback = {
            "type": link_type,
            "name": name,
            "url": url,
            "checksum": checksum
        }
        
        if file_id and link_type == "gdrive":
            fallback["file_id"] = file_id
        
        update['downloads']['fallback'].append(fallback)
        print(f"✅ Added fallback '{name}' to update {update_id}")
        return True
    
    def add_verification_manifest(self, version, github_api_url):
        """Add verification manifest URL for a version"""
        self.data['verification_manifests'][version] = github_api_url
        print(f"✅ Added manifest for version {version}")
    
    def update_latest_version(self, version):
        """Update the latest version number"""
        self.data['game_info']['latest_version'] = version
        print(f"✅ Latest version updated to {version}")
    
    def view_updates(self):
        """Display all updates in a readable format"""
        print("\n" + "="*60)
        print("CRICKET 26 - ALL UPDATES")
        print("="*60)
        
        for update in self.data['updates']:
            print(f"\n[{update['update_id']}] {update['from_version']} → {update['to_version']}")
            print(f"   📅 Release: {update['release_date']}")
            print(f"   💾 Size: {update['size_mb']} MB")
            print(f"   📝 {update['description']}")
            print(f"   🔗 Primary: {update['downloads']['primary']['name']}")
            print(f"   🔄 Fallbacks: {len(update['downloads']['fallback'])}")
        
        print("\n" + "="*60)
        print(f"Latest Version: {self.data['game_info']['latest_version']}")
        print("="*60 + "\n")
    
    def interactive_mode(self):
        """Interactive command-line interface"""
        print("\n🎮 CRICKET 26 ADMIN PANEL")
        print("="*60)
        
        while True:
            print("\nOptions:")
            print("1. View all updates")
            print("2. Add new update")
            print("3. Add fallback link to update")
            print("4. Add verification manifest")
            print("5. Update latest version")
            print("6. Save and exit")
            print("7. Exit without saving")
            
            choice = input("\nEnter choice (1-7): ").strip()
            
            if choice == "1":
                self.view_updates()
            
            elif choice == "2":
                print("\n--- ADD NEW UPDATE ---")
                from_ver = input("From version (e.g., 1.0.3): ").strip()
                to_ver = input("To version (e.g., 1.0.4): ").strip()
                gdrive_url = input("Google Drive URL: ").strip()
                gdrive_file_id = input("Google Drive File ID: ").strip()
                checksum = input("SHA256 checksum: ").strip()
                size_mb = int(input("Size in MB: ").strip())
                description = input("Description: ").strip()
                
                print("\nChangelog (enter one item per line, empty line to finish):")
                changelog = []
                while True:
                    item = input("- ").strip()
                    if not item:
                        break
                    changelog.append(item)
                
                self.add_new_update(from_ver, to_ver, gdrive_url, gdrive_file_id,
                                   checksum, size_mb, description, changelog)
            
            elif choice == "3":
                self.view_updates()
                update_id = int(input("\nUpdate ID to add fallback to: ").strip())
                link_type = input("Type (gdrive/direct): ").strip()
                name = input("Name (e.g., 'CDN Mirror EU'): ").strip()
                url = input("URL: ").strip()
                checksum = input("SHA256 checksum: ").strip()
                file_id = None
                if link_type == "gdrive":
                    file_id = input("Google Drive File ID: ").strip()
                
                self.add_fallback_link(update_id, link_type, name, url, checksum, file_id)
            
            elif choice == "4":
                version = input("Version (e.g., 1.0.4): ").strip()
                github_url = input("GitHub API URL: ").strip()
                self.add_verification_manifest(version, github_url)
            
            elif choice == "5":
                version = input("New latest version (e.g., 1.0.4): ").strip()
                self.update_latest_version(version)
            
            elif choice == "6":
                self.save_version_json()
                print("👋 Goodbye!")
                break
            
            elif choice == "7":
                print("👋 Exiting without saving...")
                break
            
            else:
                print("❌ Invalid choice!")


# QUICK ADD EXAMPLE - Uncomment and modify to quickly add updates
def quick_add_example():
    """Example: Quick way to add an update programmatically"""
    admin = Cricket26AdminPanel("version.json")
    
    # Add new update
    admin.add_new_update(
        from_ver="1.0.3",
        to_ver="1.0.4",
        gdrive_url="https://drive.google.com/file/d/YOUR_FILE_ID/view?usp=sharing",
        gdrive_file_id="YOUR_FILE_ID",
        checksum="your_sha256_checksum_here",
        size_mb=420,
        description="Bug fixes and new features",
        changelog_list=[
            "Fixed critical bug in multiplayer",
            "Added new batting animations",
            "Performance improvements",
            "UI enhancements"
        ]
    )
    
    # Add fallback links
    admin.add_fallback_link(
        update_id=4,  # The update we just added
        link_type="direct",
        name="CDN Mirror (Global)",
        url="https://cdn.example.com/cricket26/patches/1.0.3_to_1.0.4.zip",
        checksum="your_sha256_checksum_here"
    )
    
    # Add verification manifest
    admin.add_verification_manifest(
        version="1.0.4",
        github_api_url="https://api.github.com/repos/aman71711/CRICKET26_Utility/contents/manifests/1.0.4_manifest.json"
    )
    
    # Save
    admin.save_version_json()
    print("✅ Update 1.0.4 added successfully!")


if __name__ == "__main__":
    # Run interactive mode by default
    admin = Cricket26AdminPanel("version.json")
    
    if admin.data:
        admin.interactive_mode()
    
    # OR uncomment below to use quick_add_example() instead
    # quick_add_example()
