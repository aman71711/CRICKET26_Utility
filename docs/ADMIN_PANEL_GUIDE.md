# 🎮 CRICKET 26 ADMIN PANEL GUIDE

## Quick Start

### Method 1: Interactive Mode (Easiest)
```bash
python admin_panel.py
```

Then follow the menu:
1. View all updates
2. Add new update
3. Add fallback link
4. Save changes

### Method 2: Quick Add (Fastest for bulk updates)

1. Open `admin_panel.py`
2. Scroll to `quick_add_example()` function
3. Modify the example with your update details
4. Uncomment the last line: `# quick_add_example()`
5. Run: `python admin_panel.py`

---

## version.json Structure Explained

```json
{
  "metadata": {
    "game_name": "Cricket 26",
    "schema_version": "2.0",           // Don't change
    "supports_sequential_updates": true, // Don't change
    "latest_version": "1.0.3"          // Auto-updated by admin panel
  },

  "game_info": {
    "latest_version": "1.0.3",         // Current latest version
    "all_versions": ["1.0.0", "1.0.1", "1.0.2", "1.0.3"],
    "base_version": "1.0.0"
  },

  "updates": [
    {
      "update_id": 1,                  // Sequential number (1, 2, 3...)
      "from_version": "1.0.0",         // Starting version
      "to_version": "1.0.1",           // Ending version
      "release_date": "2025-01-15",    // YYYY-MM-DD format
      "size_mb": 250,                  // Size in megabytes
      "mandatory": true,               // true/false
      "description": "Brief description",
      "changelog": [
        "Change 1",
        "Change 2"
      ],
      "downloads": {
        "primary": {
          "type": "gdrive",            // "gdrive" or "direct"
          "name": "Display Name",
          "url": "Full URL",
          "file_id": "Google Drive ID", // Required for gdrive
          "checksum": "SHA256 hash"
        },
        "fallback": [
          // Same structure as primary, array of backup sources
        ]
      }
    }
  ],

  "verification_manifests": {
    "1.0.0": "GitHub API URL",         // One entry per version
    "1.0.1": "GitHub API URL"
  }
}
```

---

## Common Tasks

### Adding a New Update (1.0.3 → 1.0.4)

**Interactive Mode:**
```bash
python admin_panel.py
# Choose option 2
# Fill in the prompts
```

**Quick Add Mode:**
```python
admin = Cricket26AdminPanel("version.json")

admin.add_new_update(
    from_ver="1.0.3",
    to_ver="1.0.4",
    gdrive_url="https://drive.google.com/file/d/YOUR_FILE_ID/view",
    gdrive_file_id="YOUR_FILE_ID",
    checksum="sha256_hash_here",
    size_mb=420,
    description="Bug fixes and new content",
    changelog_list=[
        "Fixed crash in career mode",
        "Added new stadiums",
        "Performance improvements"
    ]
)

admin.save_version_json()
```

### Adding a Fallback Link

```python
admin.add_fallback_link(
    update_id=4,              # Which update to add fallback to
    link_type="direct",       # "gdrive" or "direct"
    name="CDN Mirror (US)",
    url="https://cdn.example.com/patch.zip",
    checksum="sha256_hash_here"
)
```

### Adding Verification Manifest

```python
admin.add_verification_manifest(
    version="1.0.4",
    github_api_url="https://api.github.com/repos/USER/REPO/contents/manifests/1.0.4_manifest.json"
)
```

---

## How to Get SHA256 Checksum

### Windows PowerShell:
```powershell
Get-FileHash "C:\path\to\patch.zip" -Algorithm SHA256
```

### Linux/Mac:
```bash
sha256sum /path/to/patch.zip
```

### Python:
```python
import hashlib

def get_checksum(file_path):
    sha256 = hashlib.sha256()
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b''):
            sha256.update(chunk)
    return sha256.hexdigest()

print(get_checksum("patch.zip"))
```

---

## Google Drive Setup

### Getting File ID from URL:
```
URL: https://drive.google.com/file/d/1ABC123XYZ456/view?usp=sharing
File ID: 1ABC123XYZ456
         ↑ This part
```

### Making File Publicly Accessible:
1. Right-click file in Google Drive
2. Click "Share"
3. Change to "Anyone with the link"
4. Set to "Viewer" permission
5. Copy link

---

## Download Source Types

### Google Drive (Recommended)
```json
{
  "type": "gdrive",
  "name": "Google Drive Official",
  "url": "https://drive.google.com/file/d/FILE_ID/view",
  "file_id": "FILE_ID",
  "checksum": "sha256_hash"
}
```

### Direct HTTP/HTTPS
```json
{
  "type": "direct",
  "name": "CDN Mirror",
  "url": "https://cdn.example.com/patch.zip",
  "checksum": "sha256_hash"
}
```

---

## Best Practices

### ✅ DO:
- Always backup before editing (admin panel does this automatically)
- Use sequential version numbers (1.0.0 → 1.0.1 → 1.0.2)
- Test download links before adding
- Generate SHA256 checksums for all files
- Add at least one fallback source
- Use descriptive names for download sources
- Keep changelog clear and user-friendly

### ❌ DON'T:
- Skip versions (1.0.0 → 1.0.2) ❌
- Use same checksum for different files
- Add broken/expired links
- Forget to update latest_version
- Edit version.json manually without backup
- Remove old updates (breaks sequential installation)

---

## Troubleshooting

### "Backup created" but changes not saved?
- Check file permissions
- Make sure version.json isn't read-only

### Invalid JSON error?
- Restore from `.json.backup` file
- Validate JSON at https://jsonlint.com/

### Updates not showing in utility?
- Check `metadata.schema_version` is "2.0"
- Verify `supports_sequential_updates` is true
- Ensure `game_info.latest_version` matches newest update

---

## Example: Complete Update Addition

```python
from admin_panel import Cricket26AdminPanel

# Initialize
admin = Cricket26AdminPanel("version.json")

# Add main update
admin.add_new_update(
    from_ver="1.0.3",
    to_ver="1.0.4",
    gdrive_url="https://drive.google.com/file/d/1ABC123/view",
    gdrive_file_id="1ABC123",
    checksum="e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
    size_mb=380,
    description="Winter Update - New features and fixes",
    changelog_list=[
        "Added 5 new international stadiums",
        "New weather system with dynamic conditions",
        "Fixed multiplayer lobby issues",
        "Improved ball physics",
        "UI/UX enhancements",
        "Performance optimizations"
    ]
)

# Add fallback 1
admin.add_fallback_link(
    update_id=4,
    link_type="direct",
    name="CDN Mirror (US)",
    url="https://cdn.example.com/cricket26/1.0.3_to_1.0.4.zip",
    checksum="e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
)

# Add fallback 2
admin.add_fallback_link(
    update_id=4,
    link_type="gdrive",
    name="Google Drive Backup",
    url="https://drive.google.com/file/d/1XYZ789/view",
    checksum="e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
    file_id="1XYZ789"
)

# Add verification manifest
admin.add_verification_manifest(
    version="1.0.4",
    github_api_url="https://api.github.com/repos/aman71711/CRICKET26_Utility/contents/manifests/1.0.4_manifest.json"
)

# Save all changes
admin.save_version_json()

print("✅ Update 1.0.4 added successfully with 2 fallback sources!")
```

---

## Contact & Support

- **Discord**: https://discord.gg/5gWWv3ar
- **GitHub**: https://github.com/aman71711/CRICKET26_Utility

---

*Last updated: 2025-02-15*
