"""
CRICKET 26 MANIFEST GENERATOR
Generates SHA256 manifest files for game directory verification
"""

import hashlib
import json
import os
from pathlib import Path
from datetime import datetime


def calculate_sha256(file_path):
    """Calculate SHA256 hash of a file"""
    sha256 = hashlib.sha256()
    try:
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b''):
                sha256.update(chunk)
        return sha256.hexdigest()
    except Exception as e:
        print(f"❌ Error reading {file_path}: {e}")
        return None


def should_exclude_file(rel_path):
    """Check if file should be excluded from manifest"""
    exclude_extensions = [
        '.log', '.tmp', '.cache', '.bak',
        '.sav', '.dat', '.ini', '.cfg'
    ]
    
    exclude_folders = [
        'Logs/', 'Temp/', 'Cache/', 'Saves/',
        'Screenshots/', 'Replays/'
    ]
    
    # Check extension
    if any(rel_path.lower().endswith(ext) for ext in exclude_extensions):
        return True
    
    # Check folder
    if any(folder.lower() in rel_path.lower() for folder in exclude_folders):
        return True
    
    return False


def generate_manifest(game_dir, version, output_dir="."):
    """Generate manifest file for game directory"""
    print(f"\n🔍 Scanning Cricket 26 directory: {game_dir}")
    print(f"📦 Version: {version}")
    print(f"⏳ This may take a few minutes...\n")
    
    game_path = Path(game_dir)
    
    if not game_path.exists():
        print(f"❌ Error: Directory not found: {game_dir}")
        return False
    
    # Check for cricket26.exe
    exe_path = game_path / "cricket26.exe"
    if not exe_path.exists():
        print(f"⚠️ Warning: cricket26.exe not found in {game_dir}")
        response = input("Continue anyway? (y/n): ")
        if response.lower() != 'y':
            return False
    
    manifest = {}
    file_count = 0
    excluded_count = 0
    
    # Scan all files
    for file_path in game_path.rglob('*'):
        if file_path.is_file():
            # Calculate relative path
            rel_path = str(file_path.relative_to(game_path)).replace('\\', '/')
            
            # Check if should exclude
            if should_exclude_file(rel_path):
                excluded_count += 1
                continue
            
            # Calculate SHA256
            file_hash = calculate_sha256(file_path)
            
            if file_hash:
                manifest[rel_path] = file_hash
                file_count += 1
                
                # Progress indicator
                if file_count % 100 == 0:
                    print(f"📊 Processed {file_count} files...")
    
    # Add metadata
    manifest_with_metadata = {
        "_comment": f"Cricket 26 v{version} - File Manifest",
        "_description": f"SHA256 checksums for all game files in version {version}",
        "_generated": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "_file_count": file_count,
        "_excluded_count": excluded_count,
        "_game_directory": str(game_dir),
        **manifest
    }
    
    # Save manifest
    output_file = Path(output_dir) / f"{version}_manifest.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(manifest_with_metadata, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Manifest generated successfully!")
    print(f"📄 File: {output_file}")
    print(f"📊 Files included: {file_count}")
    print(f"⏭️ Files excluded: {excluded_count}")
    print(f"💾 File size: {output_file.stat().st_size / 1024:.2f} KB")
    
    return True


def interactive_mode():
    """Interactive manifest generation"""
    print("\n" + "="*60)
    print("🎮 CRICKET 26 MANIFEST GENERATOR")
    print("="*60)
    
    # Get game directory
    print("\n📂 Enter Cricket 26 installation directory:")
    print("   Example: C:/Games/Cricket 26")
    game_dir = input("Directory: ").strip().strip('"')
    
    if not game_dir:
        print("❌ Error: Directory cannot be empty")
        return
    
    # Get version
    print("\n🏷️ Enter version number:")
    print("   Example: 1.0.4")
    version = input("Version: ").strip()
    
    if not version:
        print("❌ Error: Version cannot be empty")
        return
    
    # Confirm
    print(f"\n📋 Summary:")
    print(f"   Directory: {game_dir}")
    print(f"   Version: {version}")
    print(f"   Output: {version}_manifest.json")
    
    confirm = input("\nProceed? (y/n): ").strip().lower()
    
    if confirm == 'y':
        generate_manifest(game_dir, version)
    else:
        print("❌ Cancelled")


def quick_generate(game_dir, version):
    """Quick generation without prompts"""
    return generate_manifest(game_dir, version)


if __name__ == "__main__":
    # Run interactive mode
    interactive_mode()
    
    # OR use quick mode:
    # quick_generate("C:/Games/Cricket 26", "1.0.4")
