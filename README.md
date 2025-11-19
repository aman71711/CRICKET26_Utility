# 🏏 Cricket 26 Auto Updater

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Discord](https://img.shields.io/badge/Discord-Join%20Server-7289da.svg)](https://discord.gg/5gWWv3ar)

Professional auto-updater for Cricket 26 with **Google Drive support**, **sequential updates**, and **intelligent fallback system**.

## ✨ Features

- ✅ **Sequential Updates** - V1→V2→V3 in correct order, auto-installs as downloaded
- ✅ **Google Drive Downloads** - Primary source with gdown integration
- ✅ **Smart Fallback** - Auto-tries backup sources if primary fails
- ✅ **SHA256 Verification** - File integrity checks before installation
- ✅ **File Verifier** - Scan game directory against official manifests
- ✅ **Resume/Pause** - Pause downloads and resume anytime
- ✅ **Modern UI** - Clean interface with real-time progress
- ✅ **Admin Panel** - Easy version.json management via Python script

---

## 📥 Quick Start

1. **Download** `CRICKET26_UTILITY_FULL.py`
2. **Install dependencies**: `pip install -r requirements.txt`
3. **Run**: `python CRICKET26_UTILITY_FULL.py`
4. Select Cricket 26 directory → Check for updates → Install

---

## 🛠️ Admin Panel Usage

Manage version.json easily:

```powershell
python admin_panel.py
```

**Add new update:**
```python
from admin_panel import Cricket26AdminPanel

admin = Cricket26AdminPanel("version.json")
admin.add_new_update(
    from_ver="1.0.3",
    to_ver="1.0.4",
    gdrive_url="https://drive.google.com/file/d/FILE_ID/view",
    gdrive_file_id="FILE_ID",
    checksum="sha256_hash",
    size_mb=420,
    description="Bug fixes",
    changelog_list=["Fix 1", "Fix 2"]
)
admin.save_version_json()
```

See [ADMIN_PANEL_GUIDE.md](docs/ADMIN_PANEL_GUIDE.md) for details.

---

## 📂 Repository Structure

```
├── CRICKET26_UTILITY_FULL.py    # Main updater
├── version.json                  # Update configuration
├── admin_panel.py                # Admin tool
├── requirements.txt              # Dependencies
├── README.md                     # Documentation
├── LICENSE                       # MIT License
│
├── docs/
│   └── ADMIN_PANEL_GUIDE.md     # Admin panel guide
│
└── manifests/                    # Verification manifests
    ├── generate_manifest.py     # Generator script
    └── *.json                   # Version manifests
```

---

## 🔧 version.json Structure

```json
{
  "metadata": {
    "schema_version": "2.0",
    "supports_sequential_updates": true
  },
  "game_info": {
    "latest_version": "1.0.3"
  },
  "updates": [
    {
      "from_version": "1.0.0",
      "to_version": "1.0.1",
      "size_mb": 250,
      "changelog": ["Fix 1", "Fix 2"],
      "downloads": {
        "primary": {
          "type": "gdrive",
          "url": "https://drive.google.com/file/d/FILE_ID/view",
          "file_id": "FILE_ID",
          "checksum": "sha256_hash"
        },
        "fallback": [...]
      }
    }
  ],
  "verification_manifests": {
    "1.0.0": "https://api.github.com/repos/USER/REPO/contents/manifests/1.0.0_manifest.json"
  }
}
```

**Edit via admin panel for safety!**

---

## 📊 Requirements

- Windows 7/8/10/11 (64-bit)
- Python 3.8+
- Internet connection

---

## 💬 Support

- **Discord**: [Join Server](https://discord.gg/5gWWv3ar)
- **Issues**: [Report Bug](https://github.com/aman71711/CRICKET26_Utility/issues)

---

**Made with ❤️ for the Cricket 26 community**
