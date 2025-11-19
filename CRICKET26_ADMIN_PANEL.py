# CRICKET26_ADMIN_PANEL.py
# 
# Admin Panel for Cricket 26 Utility - Version Management & Hash Generation
# Created by: XLR8 (Discord: xlr8_boi)
# 
# Features:
# - Visual JSON editor for version.json
# - Easy-to-use form for adding/editing updates
# - Hash/Checksum generator (MD5, SHA1, SHA256)
# - Game manifest generator
# - Direct GitHub integration
# - Backup and restore functionality

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import json
import hashlib
import requests
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List, Optional, Set
import os
import sv_ttk
import threading
import queue

# ==============================================================================
# --- CONSTANTS & CONFIGURATION ---
# ==============================================================================

class AdminConstants:
    APP_NAME = "Cricket 26 Admin Panel"
    APP_VERSION = "v1.0"
    VERSION_JSON_URL = "https://raw.githubusercontent.com/aman71711/CRICKET26_Utility/main/version.json"
    GITHUB_REPO = "aman71711/CRICKET26_Utility"
    
    # Theme colors (matching main utility)
    COLORS = {
        'primary': '#0d1117',
        'secondary': '#161b22',
        'accent': '#58a6ff',
        'success': '#3fb950',
        'warning': '#d29922',
        'error': '#f85149',
        'text': '#e6edf3',
        'text_secondary': '#8b949e',  # Muted text for hints/examples
        'border': '#30363d',
    }
    
    # Supported hash algorithms
    HASH_ALGORITHMS = ['MD5', 'SHA1', 'SHA256']
    
    # Default host configuration
    DEFAULT_HOST = {
        "id": "gdrive_primary",
        "name": "Google Drive",
        "links": {}
    }
    
    # Version.json structure template
    VERSION_JSON_TEMPLATE = {
        "latest_version": "",
        "versions": [],
        "hosts": [],
        "update_sizes": {},
        "host_preference_order": [],
        "manifest_links": {},
        "fallback_links": {}
    }

# ==============================================================================
# --- UTILITY FUNCTIONS ---
# ==============================================================================

def format_bytes(byte_count: int) -> str:
    """Format bytes into human-readable string."""
    if byte_count is None:
        return "N/A"
    power = 1024
    n = 0
    power_labels = {0: '', 1: 'KB', 2: 'MB', 3: 'GB', 4: 'TB'}
    while byte_count >= power and n < len(power_labels) - 1:
        byte_count /= power
        n += 1
    return f"{byte_count:.2f} {power_labels[n]}"

def calculate_file_hash(file_path: Path, algorithm: str = 'SHA256') -> Optional[str]:
    """Calculate hash of a file."""
    try:
        hash_obj = hashlib.new(algorithm.lower())
        with open(file_path, 'rb') as f:
            while chunk := f.read(8192):
                hash_obj.update(chunk)
        return hash_obj.hexdigest()
    except Exception as e:
        return None

# ==============================================================================
# --- VERSION MANAGER ---
# ==============================================================================

class VersionManager:
    """Handles loading, editing, and saving version.json with utility-compatible structure."""
    
    def __init__(self):
        # Initialize with correct structure
        self.data: Dict[str, Any] = {
            "latest_version": "",
            "versions": [],
            "hosts": [{
                "id": "gdrive_primary",
                "name": "Google Drive",
                "links": {}
            }],
            "update_sizes": {},
            "host_preference_order": ["gdrive_primary"],
            "manifest_links": {},
            "fallback_links": {}
        }
        self.backup_data: Dict[str, Any] = {}
        self.file_path: Optional[Path] = None
    
    def load_from_url(self) -> bool:
        """Load version.json from GitHub."""
        try:
            response = requests.get(AdminConstants.VERSION_JSON_URL, timeout=10)
            response.raise_for_status()
            loaded_data = response.json()
            
            # Ensure structure is correct
            self.data = self._ensure_correct_structure(loaded_data)
            self.backup_data = self.data.copy()
            return True
        except Exception as e:
            return False
    
    def load_from_file(self, file_path: Path) -> bool:
        """Load version.json from local file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                loaded_data = json.load(f)
            
            # Ensure structure is correct
            self.data = self._ensure_correct_structure(loaded_data)
            self.backup_data = self.data.copy()
            self.file_path = file_path
            return True
        except Exception as e:
            return False
    
    def _ensure_correct_structure(self, data: Dict) -> Dict:
        """Ensure data has the correct structure for the utility."""
        corrected = {
            "latest_version": data.get("latest_version", ""),
            "versions": data.get("versions", []),
            "hosts": data.get("hosts", [{
                "id": "gdrive_primary",
                "name": "Google Drive",
                "links": {}
            }]),
            "update_sizes": data.get("update_sizes", {}),
            "host_preference_order": data.get("host_preference_order", ["gdrive_primary"]),
            "manifest_links": data.get("manifest_links", {}),
            "fallback_links": data.get("fallback_links", {})
        }
        return corrected
    
    def save_to_file(self, file_path: Optional[Path] = None) -> bool:
        """Save version.json to file."""
        try:
            target_path = file_path or self.file_path
            if not target_path:
                return False
            
            # Create backup
            if target_path.exists():
                backup_path = target_path.with_suffix('.json.backup')
                backup_path.write_text(target_path.read_text(encoding='utf-8'), encoding='utf-8')
            
            # Save with proper formatting
            with open(target_path, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, indent=2, ensure_ascii=False)
            
            self.file_path = target_path
            self.backup_data = self.data.copy()
            return True
        except Exception as e:
            return False
    
    def add_update(self, from_version: str, to_version: str, gdrive_link: str, 
                   update_size: str, manifest_link: str = "", 
                   fallback_url: str = "", fallback_message: str = "") -> bool:
        """Add a new update path (from_version -> to_version)."""
        try:
            # Create update key (format: "1.0_1.1")
            update_key = f"{from_version}_{to_version}"
            
            # Add to hosts[0].links
            if not self.data['hosts']:
                self.data['hosts'] = [{
                    "id": "gdrive_primary",
                    "name": "Google Drive",
                    "links": {}
                }]
            
            self.data['hosts'][0]['links'][update_key] = gdrive_link
            
            # Add update size
            self.data['update_sizes'][update_key] = update_size
            
            # Add manifest link if provided
            if manifest_link:
                self.data['manifest_links'][to_version] = manifest_link
            
            # Add fallback info if provided
            if fallback_url or fallback_message:
                if 'fallback_links' not in self.data:
                    self.data['fallback_links'] = {}
                self.data['fallback_links'][update_key] = {
                    "url": fallback_url,
                    "message": fallback_message if fallback_message else "Primary download unavailable. Using fallback server."
                }
            
            # Rebuild versions array
            self.rebuild_versions_array()
            
            return True
        except Exception as e:
            return False
    
    def update_existing(self, from_version: str, to_version: str, old_to_version: str,
                       gdrive_link: str, update_size: str, manifest_link: str = "",
                       fallback_url: str = "", fallback_message: str = "") -> bool:
        """Update an existing update path."""
        try:
            # Remove old entry
            old_key = f"{from_version}_{old_to_version}"
            new_key = f"{from_version}_{to_version}"
            
            # Remove old links
            if self.data['hosts'] and old_key in self.data['hosts'][0]['links']:
                del self.data['hosts'][0]['links'][old_key]
            if old_key in self.data['update_sizes']:
                del self.data['update_sizes'][old_key]
            if old_to_version in self.data['manifest_links']:
                del self.data['manifest_links'][old_to_version]
            if 'fallback_links' in self.data and old_key in self.data['fallback_links']:
                del self.data['fallback_links'][old_key]
            
            # Add new entry
            return self.add_update(from_version, to_version, gdrive_link, update_size, 
                                 manifest_link, fallback_url, fallback_message)
        except Exception as e:
            return False
    
    def delete_update(self, from_version: str, to_version: str) -> bool:
        """Delete an update path."""
        try:
            update_key = f"{from_version}_{to_version}"
            
            # Remove from hosts[0].links
            if self.data['hosts'] and update_key in self.data['hosts'][0]['links']:
                del self.data['hosts'][0]['links'][update_key]
            
            # Remove from update_sizes
            if update_key in self.data['update_sizes']:
                del self.data['update_sizes'][update_key]
            
            # Remove from manifest_links
            if to_version in self.data['manifest_links']:
                del self.data['manifest_links'][to_version]
            
            # Remove from fallback_links
            if 'fallback_links' in self.data and update_key in self.data['fallback_links']:
                del self.data['fallback_links'][update_key]
            
            # Rebuild versions array
            self.rebuild_versions_array()
            
            return True
        except Exception as e:
            return False
    
    def get_update(self, from_version: str, to_version: str) -> Optional[Dict[str, Any]]:
        """Get a specific update path."""
        update_key = f"{from_version}_{to_version}"
        
        if self.data['hosts'] and update_key in self.data['hosts'][0]['links']:
            result = {
                'from_version': from_version,
                'to_version': to_version,
                'gdrive_link': self.data['hosts'][0]['links'][update_key],
                'update_size': self.data['update_sizes'].get(update_key, '0 MB'),
                'manifest_link': self.data['manifest_links'].get(to_version, ''),
                'fallback_url': '',
                'fallback_message': ''
            }
            
            # Get fallback info if exists
            if 'fallback_links' in self.data and update_key in self.data['fallback_links']:
                fallback = self.data['fallback_links'][update_key]
                result['fallback_url'] = fallback.get('url', '')
                result['fallback_message'] = fallback.get('message', '')
            
            return result
        return None
    
    def get_all_updates(self) -> List[Dict[str, Any]]:
        """Get all update paths."""
        updates = []
        if not self.data['hosts']:
            return updates
        
        for update_key, gdrive_link in self.data['hosts'][0]['links'].items():
            if '_' in update_key:
                from_ver, to_ver = update_key.split('_', 1)
                updates.append({
                    'from_version': from_ver,
                    'to_version': to_ver,
                    'update_key': update_key,
                    'gdrive_link': gdrive_link,
                    'update_size': self.data['update_sizes'].get(update_key, '0 MB'),
                    'manifest_link': self.data['manifest_links'].get(to_ver, '')
                })
        
        return updates
    
    def set_latest_version(self, version: str) -> bool:
        """Set the latest version."""
        try:
            self.data['latest_version'] = version
            self.rebuild_versions_array()
            return True
        except Exception as e:
            return False
    
    def restore_backup(self):
        """Restore from backup."""
        self.data = self.backup_data.copy()
    
    def rebuild_versions_array(self):
        """Rebuild the versions array from all update paths with intelligent version sorting."""
        if not self.data['hosts'] or not self.data['hosts'][0]['links']:
            self.data['versions'] = []
            return
        
        # Extract all unique versions from update keys
        all_versions = set()
        for update_key in self.data['hosts'][0]['links'].keys():
            if '_' in update_key:
                from_ver, to_ver = update_key.split('_', 1)
                all_versions.add(from_ver)
                all_versions.add(to_ver)
        
        # Sort versions intelligently (handles 1.0, 1.1, 1.2, 1.3, 1.3.5, etc.)
        def version_key(v):
            """Convert version string to sortable tuple of integers."""
            try:
                # Split by '.' and convert each part to integer
                # Example: "1.3.5" -> (1, 3, 5), "1.3" -> (1, 3, 0)
                parts = v.split('.')
                # Pad with zeros to ensure consistent comparison (max 4 parts)
                int_parts = [int(p) if p.isdigit() else 0 for p in parts]
                # Pad to 4 parts for consistent sorting
                while len(int_parts) < 4:
                    int_parts.append(0)
                return tuple(int_parts[:4])
            except:
                # Fallback for non-standard versions
                return (0, 0, 0, 0)
        
        sorted_versions = sorted(all_versions, key=version_key)
        self.data['versions'] = sorted_versions
        
        # Note: Do NOT auto-set latest_version here - let user control it via checkbox

# ==============================================================================
# --- MANIFEST GENERATOR ---
# ==============================================================================

class ManifestGenerator:
    """Generate game file manifest for verification."""
    
    @staticmethod
    def generate_manifest(game_dir: Path, progress_callback=None) -> Dict[str, str]:
        """Generate manifest of all game files with SHA256 hashes."""
        manifest = {}
        total_files = sum(1 for _ in game_dir.rglob('*') if _.is_file())
        processed = 0
        
        for file_path in game_dir.rglob('*'):
            if file_path.is_file():
                try:
                    relative_path = file_path.relative_to(game_dir)
                    file_hash = calculate_file_hash(file_path, 'SHA256')
                    
                    if file_hash:
                        manifest[str(relative_path).replace('\\', '/')] = file_hash
                    
                    processed += 1
                    if progress_callback:
                        progress_callback(processed, total_files, str(relative_path))
                
                except Exception as e:
                    continue
        
        return manifest
    
    @staticmethod
    def save_manifest(manifest: Dict[str, str], output_path: Path) -> bool:
        """Save manifest to JSON file."""
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(manifest, f, indent=2, ensure_ascii=False)
            return True
        except Exception:
            return False

# ==============================================================================
# --- ADMIN PANEL GUI ---
# ==============================================================================

class AdminPanelGUI(tk.Tk):
    """Main admin panel GUI."""
    
    def __init__(self):
        super().__init__()
        
        self.title(f"{AdminConstants.APP_NAME} - {AdminConstants.APP_VERSION}")
        self.geometry("1400x900")
        self.minsize(1200, 800)
        
        # Initialize managers
        self.version_manager = VersionManager()
        self.manifest_generator = ManifestGenerator()
        
        # Apply theme
        sv_ttk.set_theme("dark")
        self.configure(bg=AdminConstants.COLORS['primary'])
        
        # Create UI
        self.create_menu()
        self.create_widgets()
        
        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        self.status_bar = ttk.Label(self, textvariable=self.status_var, relief=tk.SUNKEN)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Center window
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - (self.winfo_width() // 2)
        y = (self.winfo_screenheight() // 2) - (self.winfo_height() // 2)
        self.geometry(f"+{x}+{y}")
        
        # Auto-load from GitHub on startup
        self.after(100, self.auto_load_from_github)
    
    def create_menu(self):
        """Create menu bar."""
        menubar = tk.Menu(self)
        self.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Load from GitHub", command=self.load_from_github)
        file_menu.add_command(label="Load from File...", command=self.load_from_file)
        file_menu.add_separator()
        file_menu.add_command(label="Save", command=self.save_file)
        file_menu.add_command(label="Save As...", command=self.save_file_as)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.quit)
        
        # Edit menu
        edit_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Edit", menu=edit_menu)
        edit_menu.add_command(label="Restore Backup", command=self.restore_backup)
        edit_menu.add_command(label="Format JSON", command=self.format_json_view)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)
    
    def create_widgets(self):
        """Create main widgets."""
        # Main container
        main_container = ttk.Frame(self, padding=10)
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(main_container)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Create tabs
        self.create_version_editor_tab()
        self.create_advanced_hash_tools_tab()
        self.create_json_viewer_tab()
    
    def create_version_editor_tab(self):
        """Create version editor tab."""
        tab = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(tab, text="📝 Version Editor")
        
        # Split into left (list) and right (editor)
        paned = ttk.PanedWindow(tab, orient=tk.HORIZONTAL)
        paned.pack(fill=tk.BOTH, expand=True)
        
        # ===== LEFT PANEL - Update List =====
        left_frame = ttk.Frame(paned)
        paned.add(left_frame, weight=1)
        
        # Header with latest version display
        header_left_frame = ttk.Frame(left_frame)
        header_left_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(header_left_frame, text="Existing Updates", font=('Segoe UI', 12, 'bold')).pack(side=tk.LEFT)
        
        # Latest version label
        self.latest_version_label = ttk.Label(header_left_frame, text="Latest: N/A | Versions: 0 | Updates: 0", 
                                               font=('Segoe UI', 9, 'bold'), 
                                               foreground=AdminConstants.COLORS['success'])
        self.latest_version_label.pack(side=tk.RIGHT)
        
        # Listbox with scrollbar
        list_frame = ttk.Frame(left_frame)
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.updates_listbox = tk.Listbox(list_frame, 
                                          yscrollcommand=scrollbar.set, 
                                          bg=AdminConstants.COLORS['secondary'],
                                          fg=AdminConstants.COLORS['text'],
                                          selectbackground=AdminConstants.COLORS['accent'],
                                          selectforeground='#ffffff',
                                          font=('Segoe UI', 10),
                                          relief=tk.FLAT,
                                          borderwidth=2,
                                          highlightthickness=1,
                                          highlightbackground=AdminConstants.COLORS['border'])
        self.updates_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.updates_listbox.yview)
        
        self.updates_listbox.bind('<<ListboxSelect>>', self.on_update_selected)
        
        # Buttons below list
        btn_frame = ttk.Frame(left_frame)
        btn_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Button(btn_frame, text="➕ New Update", command=self.new_update).pack(fill=tk.X, pady=2)
        ttk.Button(btn_frame, text="🗑️ Delete", command=self.delete_update).pack(fill=tk.X, pady=2)
        ttk.Button(btn_frame, text="⭐ Set as Latest", command=self.set_as_latest_version).pack(fill=tk.X, pady=2)
        ttk.Button(btn_frame, text="🔄 Refresh", command=self.refresh_updates_list).pack(fill=tk.X, pady=2)
        
        # Separator
        ttk.Separator(btn_frame, orient='horizontal').pack(fill=tk.X, pady=8)
        
        # GitHub Upload Button (Prominent)
        self.github_upload_btn = ttk.Button(btn_frame, text="🚀 Upload to GitHub", 
                                           command=self.upload_to_github, 
                                           style='Accent.TButton')
        self.github_upload_btn.pack(fill=tk.X, pady=2)
        
        # ===== RIGHT PANEL - Editor =====
        right_frame = ttk.Frame(paned)
        paned.add(right_frame, weight=3)
        
        # Header with Save button
        header_frame = ttk.Frame(right_frame)
        header_frame.pack(fill=tk.X, pady=(0, 15))
        
        ttk.Label(header_frame, text="Update Details", font=('Segoe UI', 14, 'bold')).pack(side=tk.LEFT)
        
        # Info label for mandatory fields
        info_label = ttk.Label(header_frame, text="* = Required Fields", 
                              foreground=AdminConstants.COLORS['error'], 
                              font=('Segoe UI', 9, 'italic'))
        info_label.pack(side=tk.LEFT, padx=(15, 0))
        
        ttk.Button(header_frame, text="💾 Save Update", command=self.save_current_update, 
                  style='Accent.TButton').pack(side=tk.RIGHT, ipadx=10, ipady=5)
        
        # Scrollable editor
        editor_canvas = tk.Canvas(right_frame, bg=AdminConstants.COLORS['primary'], highlightthickness=0)
        editor_scrollbar = ttk.Scrollbar(right_frame, orient=tk.VERTICAL, command=editor_canvas.yview)
        self.editor_frame = ttk.Frame(editor_canvas)
        
        self.editor_frame.bind('<Configure>', lambda e: editor_canvas.configure(scrollregion=editor_canvas.bbox('all')))
        editor_canvas.create_window((0, 0), window=self.editor_frame, anchor=tk.NW, width=700)
        editor_canvas.configure(yscrollcommand=editor_scrollbar.set)
        
        editor_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        editor_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Create input fields
        self.create_editor_fields()
    
    def create_editor_fields(self):
        """Create editor input fields for update PATH (from → to)."""
        # Basic info - UPDATE PATH
        basic_frame = ttk.LabelFrame(self.editor_frame, text="📋 Update Path Information", padding=20)
        basic_frame.pack(fill=tk.X, pady=(0, 10), padx=15)
        basic_frame.columnconfigure(0, weight=1)
        
        # From Version (MANDATORY)
        from_version_label = ttk.Frame(basic_frame)
        from_version_label.grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        ttk.Label(from_version_label, text="*", foreground=AdminConstants.COLORS['error'], 
                 font=('Segoe UI', 11, 'bold')).pack(side=tk.LEFT, padx=(0, 2))
        ttk.Label(from_version_label, text="From Version", 
                 font=('Segoe UI', 10, 'bold')).pack(side=tk.LEFT)
        
        from_version_input_frame = ttk.Frame(basic_frame)
        from_version_input_frame.grid(row=1, column=0, sticky=tk.EW, pady=(0, 15))
        from_version_input_frame.columnconfigure(0, weight=1)
        
        self.from_version_entry = ttk.Entry(from_version_input_frame, font=('Segoe UI', 11))
        self.from_version_entry.grid(row=0, column=0, sticky=tk.EW, padx=(0, 10))
        ttk.Label(from_version_input_frame, text="Starting version (e.g., 1.0, 2.5)", 
                 foreground=AdminConstants.COLORS['text_secondary'], 
                 font=('Segoe UI', 9)).grid(row=0, column=1, sticky=tk.W)
        
        # To Version (MANDATORY)
        to_version_label = ttk.Frame(basic_frame)
        to_version_label.grid(row=2, column=0, sticky=tk.W, pady=(0, 5))
        ttk.Label(to_version_label, text="*", foreground=AdminConstants.COLORS['error'], 
                 font=('Segoe UI', 11, 'bold')).pack(side=tk.LEFT, padx=(0, 2))
        ttk.Label(to_version_label, text="To Version", 
                 font=('Segoe UI', 10, 'bold')).pack(side=tk.LEFT)
        
        to_version_input_frame = ttk.Frame(basic_frame)
        to_version_input_frame.grid(row=3, column=0, sticky=tk.EW, pady=(0, 15))
        to_version_input_frame.columnconfigure(0, weight=1)
        
        self.to_version_entry = ttk.Entry(to_version_input_frame, font=('Segoe UI', 11))
        self.to_version_entry.grid(row=0, column=0, sticky=tk.EW, padx=(0, 10))
        ttk.Label(to_version_input_frame, text="Target version (e.g., 1.1, 3.0)", 
                 foreground=AdminConstants.COLORS['text_secondary'], 
                 font=('Segoe UI', 9)).grid(row=0, column=1, sticky=tk.W)
        
        # Update Size (MANDATORY)
        size_label = ttk.Frame(basic_frame)
        size_label.grid(row=4, column=0, sticky=tk.W, pady=(0, 5))
        ttk.Label(size_label, text="*", foreground=AdminConstants.COLORS['error'], 
                 font=('Segoe UI', 11, 'bold')).pack(side=tk.LEFT, padx=(0, 2))
        ttk.Label(size_label, text="Update Size", 
                 font=('Segoe UI', 10, 'bold')).pack(side=tk.LEFT)
        
        size_input_frame = ttk.Frame(basic_frame)
        size_input_frame.grid(row=5, column=0, sticky=tk.EW, pady=(0, 5))
        size_input_frame.columnconfigure(0, weight=1)
        
        self.update_size_entry = ttk.Entry(size_input_frame, font=('Segoe UI', 11))
        self.update_size_entry.grid(row=0, column=0, sticky=tk.EW, padx=(0, 10))
        ttk.Label(size_input_frame, text="Examples: 500 MB, 1.2 GB, 50 KB", 
                 foreground=AdminConstants.COLORS['text_secondary'], 
                 font=('Segoe UI', 9)).grid(row=0, column=1, sticky=tk.W)
        
        # Set as Latest Version Checkbox
        latest_checkbox_frame = ttk.Frame(basic_frame)
        latest_checkbox_frame.grid(row=6, column=0, sticky=tk.W, pady=(10, 0))
        
        self.set_as_latest_var = tk.BooleanVar(value=True)  # Default: enabled
        self.set_as_latest_checkbox = ttk.Checkbutton(
            latest_checkbox_frame,
            text="✓ Set as Latest Version",
            variable=self.set_as_latest_var,
            style='Switch.TCheckbutton'
        )
        self.set_as_latest_checkbox.pack(side=tk.LEFT)
        
        ttk.Label(latest_checkbox_frame, text="(Enable to make 'To Version' the new latest)", 
                 foreground=AdminConstants.COLORS['text_secondary'], 
                 font=('Segoe UI', 9, 'italic')).pack(side=tk.LEFT, padx=(10, 0))
        
        # Google Drive Link (MANDATORY)
        gdrive_frame = ttk.LabelFrame(self.editor_frame, text="📥 Download Source", padding=20)
        gdrive_frame.pack(fill=tk.X, pady=(0, 10), padx=15)
        gdrive_frame.columnconfigure(0, weight=1)
        
        # Google Drive Link label with mandatory marker
        gdrive_label = ttk.Frame(gdrive_frame)
        gdrive_label.grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        ttk.Label(gdrive_label, text="*", foreground=AdminConstants.COLORS['error'], 
                 font=('Segoe UI', 11, 'bold')).pack(side=tk.LEFT, padx=(0, 2))
        ttk.Label(gdrive_label, text="Google Drive File ID or URL", 
                 font=('Segoe UI', 10, 'bold')).pack(side=tk.LEFT)
        
        self.gdrive_link_entry = ttk.Entry(gdrive_frame, font=('Segoe UI', 10))
        self.gdrive_link_entry.grid(row=1, column=0, sticky=tk.EW, pady=(0, 5))
        
        ttk.Label(gdrive_frame, text="Example: 1abc123XYZ  or  https://drive.google.com/file/d/1abc123XYZ/view", 
                 foreground=AdminConstants.COLORS['text_secondary'], 
                 font=('Segoe UI', 9)).grid(row=2, column=0, sticky=tk.W)
        
        # Manifest File Upload & Link (OPTIONAL)
        manifest_frame = ttk.LabelFrame(self.editor_frame, text="📄 Manifest Configuration (Optional)", padding=20)
        manifest_frame.pack(fill=tk.X, pady=(0, 10), padx=15)
        manifest_frame.columnconfigure(0, weight=1)
        
        # Upload manifest file
        ttk.Label(manifest_frame, text="Manifest File", 
                 font=('Segoe UI', 10, 'bold')).grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        
        upload_container = ttk.Frame(manifest_frame)
        upload_container.grid(row=1, column=0, sticky=tk.W, pady=(0, 10))
        
        ttk.Button(upload_container, text="📁 Browse File", 
                  command=self.browse_manifest_file).pack(side=tk.LEFT, padx=(0, 10))
        self.manifest_file_label = ttk.Label(upload_container, text="No file selected", 
                                            foreground=AdminConstants.COLORS['text_secondary'],
                                            font=('Segoe UI', 9))
        self.manifest_file_label.pack(side=tk.LEFT)
        
        # Upload button
        ttk.Button(manifest_frame, text="🚀 Upload Manifest to GitHub", 
                  command=self.upload_manifest_to_github).grid(row=2, column=0, sticky=tk.W, pady=(0, 10))
        
        # Auto-generated manifest URL
        ttk.Label(manifest_frame, text="Generated Manifest URL", 
                 font=('Segoe UI', 10, 'bold')).grid(row=3, column=0, sticky=tk.W, pady=(0, 5))
        
        self.manifest_link_entry = ttk.Entry(manifest_frame, font=('Segoe UI', 9),
                                            foreground=AdminConstants.COLORS['success'])
        self.manifest_link_entry.grid(row=4, column=0, sticky=tk.EW, pady=(0, 5))
        
        ttk.Label(manifest_frame, text="ℹ️ Upload manifest JSON → Auto-saves to /manifests/ folder → URL generated automatically", 
                 foreground=AdminConstants.COLORS['text_secondary'], 
                 font=('Segoe UI', 9)).grid(row=5, column=0, sticky=tk.W)
        
        # Store selected manifest file path
        self.selected_manifest_path = None
        
        # Fallback Download (OPTIONAL)
        fallback_frame = ttk.LabelFrame(self.editor_frame, text="🔄 Fallback Download (Optional)", padding=20)
        fallback_frame.pack(fill=tk.X, pady=(0, 10), padx=15)
        fallback_frame.columnconfigure(0, weight=1)
        
        ttk.Label(fallback_frame, text="Fallback Download URL", 
                 font=('Segoe UI', 10, 'bold')).grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        
        self.fallback_url_entry = ttk.Entry(fallback_frame, font=('Segoe UI', 10))
        self.fallback_url_entry.grid(row=1, column=0, sticky=tk.EW, pady=(0, 5))
        
        ttk.Label(fallback_frame, text="⚠️ Must be DIRECT download URL (e.g., Pixeldrain API, GitHub releases)", 
                 foreground=AdminConstants.COLORS['warning'], 
                 font=('Segoe UI', 9)).grid(row=2, column=0, sticky=tk.W, pady=(0, 10))
        
        ttk.Label(fallback_frame, text="Fallback Message", 
                 font=('Segoe UI', 10, 'bold')).grid(row=3, column=0, sticky=tk.W, pady=(0, 5))
        
        self.fallback_message_text = tk.Text(fallback_frame, height=2,
                                            bg=AdminConstants.COLORS['secondary'],
                                            fg=AdminConstants.COLORS['text'],
                                            font=('Segoe UI', 10),
                                            wrap=tk.WORD,
                                            relief=tk.SOLID,
                                            borderwidth=1,
                                            padx=10, pady=8)
        self.fallback_message_text.grid(row=4, column=0, sticky=tk.EW, pady=(0, 5))
        
        ttk.Label(fallback_frame, text="ℹ️ Used automatically when GDrive fails (quota exceeded, network issues)", 
                 foreground=AdminConstants.COLORS['text_secondary'], 
                 font=('Segoe UI', 9)).grid(row=5, column=0, sticky=tk.W)
    
    def create_advanced_hash_tools_tab(self):
        """Create advanced hash tools tab (integrated from Hashgenerator v5.0)."""
        tab = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(tab, text="🔧 Advanced Hash Tools")
        
        # Configure custom styles for this tab
        style = ttk.Style()
        style.configure('Treeview', rowheight=25, background=AdminConstants.COLORS['secondary'], 
                       foreground=AdminConstants.COLORS['text'], fieldbackground=AdminConstants.COLORS['secondary'])
        style.configure('TLabelframe.Label', font=('Segoe UI', 10, 'bold'))
        
        # Main container
        main_frame = ttk.Frame(tab)
        main_frame.pack(fill=tk.BOTH, expand=True)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        # State variables
        self.adv_game_root: Optional[Path] = None
        self.adv_update_queue = queue.Queue()
        self.adv_is_processing = False
        self.adv_last_generated_manifest: Optional[Dict[str, str]] = None
        self.adv_last_generation_errors: Optional[List[str]] = None
        self.adv_single_file_path = tk.StringVar(value="")
        self.adv_single_file_hash = tk.StringVar(value="")
        self.adv_var_root_path = tk.StringVar(value="No root folder selected.")
        self.adv_var_status = tk.StringVar(value="Ready. Select a folder or use conversion tools.")
        
        # --- Top bar with folder selection and conversion tools ---
        top_bar_frame = ttk.Frame(main_frame)
        top_bar_frame.grid(row=0, column=0, sticky='ew', pady=(0, 10))
        top_bar_frame.columnconfigure(1, weight=1)
        
        # Folder selection
        frame_step1 = ttk.LabelFrame(top_bar_frame, text="Select Root Folder", padding=10)
        frame_step1.grid(row=0, column=0, sticky='ns')
        self.adv_btn_select_root = ttk.Button(frame_step1, text="📁 Select Root...", command=self.adv_select_game_root)
        self.adv_btn_select_root.pack()
        
        # Conversion Tools
        frame_convert = ttk.LabelFrame(top_bar_frame, text="Conversion Tools", padding=10)
        frame_convert.grid(row=0, column=1, sticky='ew', padx=(10, 0))
        frame_convert.columnconfigure((0, 1, 2), weight=1)
        
        self.adv_btn_md5_convert = ttk.Button(frame_convert, text="Convert from MD5", command=self.adv_start_md5_conversion)
        self.adv_btn_md5_convert.grid(row=0, column=0, sticky='ew', padx=(0, 5))
        
        self.adv_btn_sfv_convert = ttk.Button(frame_convert, text="Convert from SFV", command=self.adv_start_sfv_conversion)
        self.adv_btn_sfv_convert.grid(row=0, column=1, sticky='ew', padx=(0, 5))
        
        self.adv_btn_fast_convert = ttk.Button(frame_convert, text="Fast Convert (JSON Lookup)", command=self.adv_start_fast_conversion)
        self.adv_btn_fast_convert.grid(row=0, column=2, sticky='ew')
        
        # Root path display
        ttk.Label(main_frame, textvariable=self.adv_var_root_path, foreground=AdminConstants.COLORS['accent']).grid(row=1, column=0, sticky='ew', pady=(0, 10))
        
        # --- Paned window with explorer and staging ---
        paned_window = ttk.PanedWindow(main_frame, orient='horizontal')
        paned_window.grid(row=2, column=0, sticky='nsew', pady=(0, 10))
        
        # Left: File Explorer
        frame_explorer = ttk.LabelFrame(paned_window, text="Available Items", padding=10)
        paned_window.add(frame_explorer, weight=1)
        frame_explorer.columnconfigure(0, weight=1)
        frame_explorer.rowconfigure(0, weight=1)
        
        self.adv_tree_explorer = ttk.Treeview(frame_explorer, selectmode='extended')
        self.adv_tree_explorer.grid(row=0, column=0, sticky='nsew')
        
        self.adv_btn_add_to_stage = ttk.Button(frame_explorer, text="Add to Manifest →", command=self.adv_add_to_staging)
        self.adv_btn_add_to_stage.grid(row=1, column=0, sticky='e', pady=(10, 0))
        
        # Right: Staged items
        frame_staging = ttk.LabelFrame(paned_window, text="Items to Include in Manifest", padding=10)
        paned_window.add(frame_staging, weight=1)
        frame_staging.columnconfigure(0, weight=1)
        frame_staging.rowconfigure(0, weight=1)
        
        self.adv_list_staged = tk.Listbox(frame_staging, selectmode='extended',
                                         bg=AdminConstants.COLORS['secondary'],
                                         fg=AdminConstants.COLORS['text'],
                                         selectbackground=AdminConstants.COLORS['accent'])
        self.adv_list_staged.grid(row=0, column=0, sticky='nsew')
        
        self.adv_btn_remove_from_stage = ttk.Button(frame_staging, text="← Remove from Manifest", command=self.adv_remove_from_staging)
        self.adv_btn_remove_from_stage.grid(row=1, column=0, sticky='w', pady=(10, 0))
        
        # --- Generate manifest section ---
        frame_generate = ttk.LabelFrame(main_frame, text="Generate Manifest / Save Result", padding=10)
        frame_generate.grid(row=3, column=0, sticky='ew', pady=(10, 0))
        frame_generate.columnconfigure(0, weight=1)
        
        btn_container = ttk.Frame(frame_generate)
        btn_container.grid(row=0, column=0, sticky='ew', pady=(0, 10))
        btn_container.columnconfigure(0, weight=1)
        
        self.adv_btn_generate = ttk.Button(btn_container, text="⚡ Generate Manifest (from staged items)", 
                                          command=self.adv_start_generation_thread, style='Accent.TButton')
        self.adv_btn_generate.grid(row=0, column=0, sticky='ew', padx=(0, 5))
        
        self.adv_btn_save_last = ttk.Button(btn_container, text="💾 Save Last Result...", command=self.adv_save_last_manifest)
        self.adv_btn_save_last.grid(row=0, column=1, sticky='w')
        
        self.adv_progress_bar = ttk.Progressbar(frame_generate, orient='horizontal', mode='determinate')
        self.adv_progress_bar.grid(row=1, column=0, sticky='ew')
        
        # --- Single File Hash Calculator ---
        frame_single_hash = ttk.LabelFrame(main_frame, text="Single File Hash Calculator", padding=10)
        frame_single_hash.grid(row=4, column=0, sticky='ew', pady=(10, 0))
        frame_single_hash.columnconfigure(0, weight=1)
        
        # File selection
        sf_file_frame = ttk.Frame(frame_single_hash)
        sf_file_frame.grid(row=0, column=0, sticky='ew', pady=(0, 5))
        sf_file_frame.columnconfigure(0, weight=1)
        
        self.adv_sf_path_entry = ttk.Entry(sf_file_frame, textvariable=self.adv_single_file_path, state='readonly')
        self.adv_sf_path_entry.grid(row=0, column=0, sticky='ew')
        
        self.adv_sf_select_btn = ttk.Button(sf_file_frame, text="📁 Select File...", command=self.adv_select_single_file)
        self.adv_sf_select_btn.grid(row=0, column=1, padx=(10, 0))
        
        # Hash display
        sf_hash_frame = ttk.Frame(frame_single_hash)
        sf_hash_frame.grid(row=1, column=0, sticky='ew', pady=(0, 5))
        sf_hash_frame.columnconfigure(0, weight=1)
        
        self.adv_sf_hash_entry = ttk.Entry(sf_hash_frame, textvariable=self.adv_single_file_hash, state='readonly',
                                          font=('Consolas', 10))
        self.adv_sf_hash_entry.grid(row=0, column=0, sticky='ew')
        
        self.adv_sf_copy_btn = ttk.Button(sf_hash_frame, text="📋 Copy", command=self.adv_copy_hash_to_clipboard)
        self.adv_sf_copy_btn.grid(row=0, column=1, padx=(10, 0))
        
        # Action buttons
        sf_action_frame = ttk.Frame(frame_single_hash)
        sf_action_frame.grid(row=2, column=0, sticky='ew')
        sf_action_frame.columnconfigure(1, weight=1)
        
        self.adv_sf_calc_btn = ttk.Button(sf_action_frame, text="🔐 Calculate SHA-256 Hash", 
                                         command=self.adv_start_single_file_hash, style='Accent.TButton')
        self.adv_sf_calc_btn.grid(row=0, column=0, sticky='w')
        
        self.adv_sf_save_btn = ttk.Button(sf_action_frame, text="💾 Save to .sha256 file...", 
                                         command=self.adv_save_hash_to_file)
        self.adv_sf_save_btn.grid(row=0, column=1, sticky='w', padx=(10, 0))
        
        self.adv_sf_progress_bar = ttk.Progressbar(sf_action_frame, orient='horizontal', mode='determinate')
        self.adv_sf_progress_bar.grid(row=0, column=2, sticky='ew', padx=(10, 0))
        sf_action_frame.columnconfigure(2, weight=1)
        
        # Status bar for this tab
        status_frame = ttk.Frame(main_frame)
        status_frame.grid(row=5, column=0, sticky='ew', pady=(10, 0))
        ttk.Label(status_frame, textvariable=self.adv_var_status, relief='sunken', anchor='w', padding="5").pack(fill='x')
        
        # Update UI state
        self.adv_update_ui_state()
        
        # Start queue processing
        self.after(100, self.adv_process_queue)
    
    def create_json_viewer_tab(self):
        """Create JSON viewer tab."""
        tab = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(tab, text="📄 JSON Viewer")
        
        # Title
        title_frame = ttk.Frame(tab)
        title_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(title_frame, text="version.json - Complete View", 
                 font=('Segoe UI', 16, 'bold')).pack(side=tk.LEFT)
        ttk.Button(title_frame, text="🔄 Refresh", command=self.refresh_json_view).pack(side=tk.RIGHT)
        
        # JSON display
        self.json_text = scrolledtext.ScrolledText(tab, 
                                                   bg=AdminConstants.COLORS['secondary'],
                                                   fg=AdminConstants.COLORS['text'],
                                                   font=('Consolas', 10),
                                                   wrap=tk.NONE)
        self.json_text.pack(fill=tk.BOTH, expand=True)
        
        # Configure syntax highlighting
        self.json_text.tag_config('key', foreground='#79c0ff')
        self.json_text.tag_config('string', foreground='#a5d6ff')
        self.json_text.tag_config('number', foreground='#3fb950')
        self.json_text.tag_config('boolean', foreground='#d29922')
    
    # ==============================================================================
    # --- EVENT HANDLERS - Version Editor ---
    # ==============================================================================
    
    def auto_load_from_github(self):
        """Auto-load version.json from GitHub on startup (silent)."""
        self.status_var.set("Loading from GitHub...")
        self.update_idletasks()
        
        if self.version_manager.load_from_url():
            self.refresh_updates_list()
            # Switch to JSON viewer tab and refresh
            self.notebook.select(2)  # JSON Viewer is tab index 2
            self.update_idletasks()
            self.refresh_json_view()
            # Switch back to Version Editor tab
            self.notebook.select(0)
            self.status_var.set("✅ Loaded from GitHub - Ready to edit")
        else:
            self.status_var.set("⚠️ Failed to load from GitHub - Using empty data")
    
    def load_from_github(self):
        """Load version.json from GitHub."""
        self.status_var.set("Loading from GitHub...")
        self.update_idletasks()
        
        if self.version_manager.load_from_url():
            self.refresh_updates_list()
            # Switch to JSON viewer tab to ensure widget is created
            self.notebook.select(2)  # JSON Viewer is tab index 2
            self.update_idletasks()
            self.refresh_json_view()
            self.status_var.set("✅ Loaded from GitHub successfully")
            messagebox.showinfo("Success", "version.json loaded from GitHub successfully!")
        else:
            self.status_var.set("❌ Failed to load from GitHub")
            messagebox.showerror("Error", "Failed to load version.json from GitHub.\nCheck your internet connection.")
    
    def load_from_file(self):
        """Load version.json from file."""
        file_path = filedialog.askopenfilename(
            title="Select version.json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if file_path:
            if self.version_manager.load_from_file(Path(file_path)):
                self.refresh_updates_list()
                # Switch to JSON viewer tab to ensure widget is created
                self.notebook.select(2)  # JSON Viewer is tab index 2
                self.update_idletasks()
                self.refresh_json_view()
                self.status_var.set(f"✅ Loaded: {Path(file_path).name}")
                messagebox.showinfo("Success", f"Loaded successfully!\n{file_path}")
            else:
                self.status_var.set("❌ Failed to load file")
                messagebox.showerror("Error", "Failed to load the file.\nPlease check the file format.")
    
    def save_file(self):
        """Save to current file."""
        if self.version_manager.file_path:
            if self.version_manager.save_to_file():
                self.status_var.set(f"✅ Saved: {self.version_manager.file_path.name}")
                messagebox.showinfo("Success", "Saved successfully!")
            else:
                self.status_var.set("❌ Failed to save")
                messagebox.showerror("Error", "Failed to save the file.")
        else:
            self.save_file_as()
    
    def save_file_as(self):
        """Save to new file."""
        file_path = filedialog.asksaveasfilename(
            title="Save version.json",
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if file_path:
            if self.version_manager.save_to_file(Path(file_path)):
                self.status_var.set(f"✅ Saved: {Path(file_path).name}")
                messagebox.showinfo("Success", f"Saved successfully!\n{file_path}")
            else:
                self.status_var.set("❌ Failed to save")
                messagebox.showerror("Error", "Failed to save the file.")
    
    def restore_backup(self):
        """Restore from backup."""
        if messagebox.askyesno("Restore Backup", "This will discard all unsaved changes.\nContinue?"):
            self.version_manager.restore_backup()
            self.refresh_updates_list()
            self.refresh_json_view()
            self.clear_editor()
            self.status_var.set("✅ Restored from backup")
    
    def refresh_updates_list(self):
        """Refresh the updates listbox."""
        self.updates_listbox.delete(0, tk.END)
        
        updates = self.version_manager.get_all_updates()
        
        if isinstance(updates, list):
            # Display update paths in order (oldest to newest)
            for update in updates:
                from_ver = update.get('from_version', '?')
                to_ver = update.get('to_version', '?')
                size = update.get('update_size', '? MB')
                
                # Format: "v1.0 → v1.1 (500 MB)"
                display_text = f"v{from_ver} → v{to_ver} ({size})"
                self.updates_listbox.insert(tk.END, display_text)
        
        # Update latest version label with version count
        latest_version = self.version_manager.data.get('latest_version', 'N/A')
        versions_list = self.version_manager.data.get('versions', [])
        version_count = len(versions_list)
        
        self.latest_version_label.config(
            text=f"Latest: v{latest_version} | Total Versions: {version_count} | Updates: {len(updates) if isinstance(updates, list) else 0}"
        )
    
    def on_update_selected(self, event):
        """Handle update path selection from list."""
        selection = self.updates_listbox.curselection()
        if not selection:
            return
        
        # Get selected update path
        selected_text = self.updates_listbox.get(selection[0])
        # Format: "v1.0 → v1.1 (500 MB)"
        update_key = selected_text.split(' (')[0]  # "v1.0 → v1.1"
        from_ver, to_ver = update_key.replace('v', '').split(' → ')
        
        # Load update data
        update_data = self.version_manager.get_update(from_ver.strip(), to_ver.strip())
        if update_data:
            self.populate_editor(from_ver.strip(), to_ver.strip(), update_data)
    
    def populate_editor(self, from_version: str, to_version: str, update_data: Dict[str, Any]):
        """Populate editor fields with update path data."""
        self.current_update_key = f"{from_version}_{to_version}"
        
        # Fill update path fields
        self.from_version_entry.delete(0, tk.END)
        self.from_version_entry.insert(0, from_version)
        
        self.to_version_entry.delete(0, tk.END)
        self.to_version_entry.insert(0, to_version)
        
        self.update_size_entry.delete(0, tk.END)
        self.update_size_entry.insert(0, update_data.get('update_size', ''))
        
        self.gdrive_link_entry.delete(0, tk.END)
        self.gdrive_link_entry.insert(0, update_data.get('gdrive_link', ''))
        
        self.manifest_link_entry.delete(0, tk.END)
        self.manifest_link_entry.insert(0, update_data.get('manifest_link', ''))
        
        self.fallback_url_entry.delete(0, tk.END)
        self.fallback_url_entry.insert(0, update_data.get('fallback_url', ''))
        
        self.fallback_message_text.delete('1.0', tk.END)
        self.fallback_message_text.insert('1.0', update_data.get('fallback_message', ''))
        
        # Set checkbox based on whether this update's 'to_version' is the current latest
        current_latest = self.version_manager.data.get('latest_version', '')
        is_latest = (to_version == current_latest)
        self.set_as_latest_var.set(is_latest)
    
    def clear_editor(self):
        """Clear all editor fields."""
        self.current_update_key = None
        self.from_version_entry.delete(0, tk.END)
        self.to_version_entry.delete(0, tk.END)
        self.update_size_entry.delete(0, tk.END)
        self.gdrive_link_entry.delete(0, tk.END)
        self.manifest_link_entry.delete(0, tk.END)
        self.fallback_url_entry.delete(0, tk.END)
        self.fallback_message_text.delete('1.0', tk.END)
        self.set_as_latest_var.set(True)  # Default: enabled for new updates
    
    def new_update(self):
        """Create new update path."""
        self.clear_editor()
        self.current_update_key = None
        # Focus on from version field for easy editing
        self.from_version_entry.focus_set()
        self.status_var.set("Creating new update path - Enter FROM version to begin")
    
    def delete_update(self):
        """Delete selected update path."""
        selection = self.updates_listbox.curselection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select an update to delete.")
            return
        
        selected_text = self.updates_listbox.get(selection[0])
        # Format: "v1.0 → v1.1 (500 MB)"
        update_key = selected_text.split(' (')[0]  # "v1.0 → v1.1"
        from_ver, to_ver = update_key.replace('v', '').split(' → ')
        
        if messagebox.askyesno("Confirm Delete", f"Delete update path {update_key}?"):
            if self.version_manager.delete_update(from_ver.strip(), to_ver.strip()):
                self.refresh_updates_list()
                self.refresh_json_view()
                self.clear_editor()
                self.status_var.set(f"✅ Deleted: {update_key}")
            else:
                messagebox.showerror("Error", "Failed to delete update.")
    
    def save_current_update(self):
        """Save current update path being edited."""
        # Validate MANDATORY fields
        from_version = self.from_version_entry.get().strip()
        if not from_version:
            messagebox.showwarning("Missing Required Field", 
                                  "⚠️ From Version is required!\n\nPlease enter the starting version (e.g., 1.0)")
            self.from_version_entry.focus_set()
            return
        
        to_version = self.to_version_entry.get().strip()
        if not to_version:
            messagebox.showwarning("Missing Required Field", 
                                  "⚠️ To Version is required!\n\nPlease enter the target version (e.g., 1.1)")
            self.to_version_entry.focus_set()
            return
        
        update_size = self.update_size_entry.get().strip()
        if not update_size:
            messagebox.showwarning("Missing Required Field", 
                                  "⚠️ Update Size is required!\n\nPlease enter the file size (e.g., 500 MB, 1.2 GB)")
            self.update_size_entry.focus_set()
            return
        
        gdrive_link = self.gdrive_link_entry.get().strip()
        if not gdrive_link:
            messagebox.showwarning("Missing Required Field", 
                                  "⚠️ Google Drive Link is required!\n\nPlease enter the GDrive file ID or link.")
            self.gdrive_link_entry.focus_set()
            return
        
        # Optional manifest link and fallback
        manifest_link = self.manifest_link_entry.get().strip()
        fallback_url = self.fallback_url_entry.get().strip()
        fallback_message = self.fallback_message_text.get('1.0', tk.END).strip()
        
        # Check if should set as latest version
        set_as_latest = self.set_as_latest_var.get()
        
        # Save or update
        if hasattr(self, 'current_update_key') and self.current_update_key:
            # Update existing
            old_from, old_to = self.current_update_key.split('_')
            if self.version_manager.update_existing(from_version, to_version, old_to,
                                                   gdrive_link, update_size, manifest_link,
                                                   fallback_url, fallback_message):
                # Update latest_version if checkbox is enabled
                if set_as_latest:
                    self.version_manager.data['latest_version'] = to_version
                
                self.refresh_updates_list()
                self.refresh_json_view()
                latest_msg = f" (Set as Latest: v{to_version})" if set_as_latest else ""
                self.status_var.set(f"✅ Updated: v{from_version} → v{to_version}{latest_msg}")
                messagebox.showinfo("Success", f"✅ Updated v{from_version} → v{to_version} successfully!{latest_msg}")
            else:
                messagebox.showerror("Error", "Failed to update.")
        else:
            # Add new
            if self.version_manager.add_update(from_version, to_version, gdrive_link, 
                                              update_size, manifest_link,
                                              fallback_url, fallback_message):
                # Update latest_version if checkbox is enabled (default for new updates)
                if set_as_latest:
                    self.version_manager.data['latest_version'] = to_version
                
                self.refresh_updates_list()
                self.refresh_json_view()
                latest_msg = f" (Set as Latest: v{to_version})" if set_as_latest else ""
                self.status_var.set(f"✅ Added: v{from_version} → v{to_version}{latest_msg}")
                messagebox.showinfo("Success", f"✅ Added v{from_version} → v{to_version} successfully!{latest_msg}")
                self.clear_editor()
            else:
                messagebox.showerror("Error", "Failed to add update.")
    
    def set_as_latest_version(self):
        """Set selected version as latest version."""
        selection = self.updates_listbox.curselection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select an update path.")
            return
        
        selected_text = self.updates_listbox.get(selection[0])
        # Format: "v1.0 → v1.1 (500 MB)"
        update_key = selected_text.split(' (')[0]  # "v1.0 → v1.1"
        _, to_ver = update_key.replace('v', '').split(' → ')
        
        if messagebox.askyesno("Set as Latest", f"Set v{to_ver.strip()} as the latest version?"):
            if self.version_manager.set_latest_version(to_ver.strip()):
                self.refresh_updates_list()
                self.refresh_json_view()
                self.status_var.set(f"✅ Set v{to_ver.strip()} as latest version")
                messagebox.showinfo("Success", f"v{to_ver.strip()} is now the latest version!")
            else:
                messagebox.showerror("Error", "Failed to set latest version.")
    
    def upload_to_github(self):
        """Upload version.json to GitHub."""
        # Confirm upload
        if not messagebox.askyesno("Upload to GitHub", 
                                   "This will commit and push version.json to GitHub.\n\nContinue?"):
            return
        
        self.status_var.set("🚀 Uploading to GitHub...")
        self.update_idletasks()
        
        try:
            import subprocess
            import os
            
            # Save to file first
            if not self.version_manager.save_to_file(Path("version.json")):
                messagebox.showerror("Error", "Failed to save version.json file!")
                return
            
            # Get current directory
            cwd = os.getcwd()
            
            # Git commands
            commands = [
                ['git', 'add', 'version.json'],
                ['git', 'commit', '-m', 'Updated version.json via Admin Panel'],
                ['git', 'push', 'origin', 'main']
            ]
            
            for cmd in commands:
                result = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
                if result.returncode != 0 and 'nothing to commit' not in result.stdout:
                    # Ignore "nothing to commit" as it's not an error
                    if 'nothing to commit' not in result.stderr:
                        error_msg = result.stderr or result.stdout
                        messagebox.showerror("Git Error", f"Failed to execute: {' '.join(cmd)}\n\n{error_msg}")
                        self.status_var.set("❌ Upload failed")
                        return
            
            self.status_var.set("✅ Successfully uploaded to GitHub!")
            messagebox.showinfo("Success", "version.json has been uploaded to GitHub successfully!\n\nChanges are now live.")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to upload to GitHub:\n{str(e)}")
            self.status_var.set("❌ Upload failed")
    
    def browse_manifest_file(self):
        """Browse and select manifest JSON file."""
        file_path = filedialog.askopenfilename(
            title="Select Manifest JSON File",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if file_path:
            self.selected_manifest_path = file_path
            filename = Path(file_path).name
            self.manifest_file_label.config(text=filename, foreground=AdminConstants.COLORS['success'])
            self.status_var.set(f"Selected manifest: {filename}")
    
    def upload_manifest_to_github(self):
        """Upload manifest file to GitHub /manifests/ folder."""
        if not self.selected_manifest_path:
            messagebox.showwarning("No File Selected", "Please browse and select a manifest JSON file first!")
            return
        
        # Get version for filename
        version = self.version_entry.get().strip()
        if not version:
            messagebox.showwarning("Version Required", "Please enter a version number first!")
            return
        
        try:
            import subprocess
            import os
            import shutil
            
            # Create manifests folder if doesn't exist
            manifests_folder = Path("manifests")
            manifests_folder.mkdir(exist_ok=True)
            
            # Copy manifest file to manifests folder
            manifest_filename = f"manifest_v{version}.json"
            dest_path = manifests_folder / manifest_filename
            shutil.copy2(self.selected_manifest_path, dest_path)
            
            self.status_var.set(f"📤 Uploading {manifest_filename} to GitHub...")
            self.update_idletasks()
            
            # Git commands
            cwd = os.getcwd()
            commands = [
                ['git', 'add', f'manifests/{manifest_filename}'],
                ['git', 'commit', '-m', f'Add manifest for v{version}'],
                ['git', 'push', 'origin', 'main']
            ]
            
            for cmd in commands:
                result = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
                if result.returncode != 0 and 'nothing to commit' not in result.stdout:
                    if 'nothing to commit' not in result.stderr:
                        error_msg = result.stderr or result.stdout
                        messagebox.showerror("Git Error", f"Failed: {' '.join(cmd)}\n\n{error_msg}")
                        self.status_var.set("❌ Manifest upload failed")
                        return
            
            # Generate GitHub raw URL
            repo_url = f"https://raw.githubusercontent.com/{AdminConstants.GITHUB_REPO}/main/manifests/{manifest_filename}"
            
            # Update the manifest link entry
            self.manifest_link_entry.delete(0, tk.END)
            self.manifest_link_entry.insert(0, repo_url)
            
            self.status_var.set(f"✅ Manifest uploaded successfully!")
            messagebox.showinfo("Success", 
                              f"Manifest uploaded to GitHub!\n\n"
                              f"File: manifests/{manifest_filename}\n"
                              f"URL: {repo_url}\n\n"
                              f"The URL has been auto-filled in the Manifest URL field.")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to upload manifest:\n{str(e)}")
            self.status_var.set("❌ Manifest upload failed")
    
    # ==============================================================================
    # --- EVENT HANDLERS - JSON Viewer ---
    # ==============================================================================
    
    def refresh_json_view(self):
        """Refresh JSON viewer with current data."""
        if not hasattr(self, 'json_text'):
            return
            
        self.json_text.delete('1.0', tk.END)
        
        if self.version_manager.data:
            json_str = json.dumps(self.version_manager.data, indent=2, ensure_ascii=False)
            self.json_text.insert('1.0', json_str)
            self.apply_json_syntax_highlighting()
        else:
            self.json_text.insert('1.0', '{\n  "No data loaded"\n}')
    
    def format_json_view(self):
        """Format JSON view."""
        self.refresh_json_view()
    
    def apply_json_syntax_highlighting(self):
        """Apply basic syntax highlighting to JSON."""
        # This is a simplified version - full highlighting would be more complex
        content = self.json_text.get('1.0', tk.END)
        
        # Clear existing tags
        for tag in ['key', 'string', 'number', 'boolean']:
            self.json_text.tag_remove(tag, '1.0', tk.END)
        
        # Apply highlighting (basic pattern matching)
        import re
        
        # Highlight keys (strings before colons)
        for match in re.finditer(r'"([^"]+)"(?=\s*:)', content):
            start_idx = f"1.0+{match.start()}c"
            end_idx = f"1.0+{match.end()}c"
            self.json_text.tag_add('key', start_idx, end_idx)
    
    # ==============================================================================
    # --- MISC ---
    # ==============================================================================
    
    def show_about(self):
        """Show about dialog."""
        messagebox.showinfo(
            "About",
            f"{AdminConstants.APP_NAME}\n"
            f"Version: {AdminConstants.APP_VERSION}\n\n"
            f"Admin panel for managing Cricket 26 version.json\n\n"
            f"Created by: XLR8 (xlr8_boi)\n"
            f"Repository: {AdminConstants.GITHUB_REPO}"
        )
    
    # ==============================================================================
    # --- ADVANCED HASH TOOLS - Helper Functions ---
    # ==============================================================================
    
    def adv_calculate_sha256(self, file_path: Path) -> Optional[str]:
        """Calculate SHA-256 hash for a file."""
        sha256 = hashlib.sha256()
        try:
            with open(file_path, "rb") as f:
                while chunk := f.read(8192):
                    sha256.update(chunk)
            return sha256.hexdigest()
        except (IOError, OSError) as e:
            return None
    
    def adv_robust_parse_md5_file(self, md5_filepath: str) -> List[str]:
        """Parse MD5 file to extract file paths."""
        paths = []
        with open(md5_filepath, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith(';') or line.startswith('#'):
                    continue
                parts = line.split()
                if len(parts) >= 2:
                    paths.append(' '.join(parts[1:]))
        return paths
    
    def adv_robust_parse_sfv_file(self, sfv_filepath: str) -> List[str]:
        """Parse SFV file to extract file paths."""
        paths = []
        with open(sfv_filepath, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith(';') or line.startswith('#'):
                    continue
                parts = line.split()
                if len(parts) >= 2:
                    # SFV format: filename CRC32
                    # Take everything except last part (CRC32)
                    paths.append(' '.join(parts[:-1]))
        return paths
    
    def adv_update_ui_state(self):
        """Update UI state for advanced tools."""
        is_idle = not self.adv_is_processing
        
        # Folder and conversion controls
        self.adv_btn_select_root.config(state='normal' if is_idle else 'disabled')
        self.adv_btn_md5_convert.config(state='normal' if self.adv_game_root and is_idle else 'disabled')
        self.adv_btn_sfv_convert.config(state='normal' if self.adv_game_root and is_idle else 'disabled')
        self.adv_btn_fast_convert.config(state='normal' if is_idle else 'disabled')
        
        # Staging controls
        has_selection = len(self.adv_tree_explorer.selection()) > 0 if hasattr(self, 'adv_tree_explorer') else False
        has_staged = self.adv_list_staged.size() > 0 if hasattr(self, 'adv_list_staged') else False
        
        self.adv_btn_add_to_stage.config(state='normal' if has_selection and is_idle else 'disabled')
        self.adv_btn_remove_from_stage.config(state='normal' if has_staged and is_idle else 'disabled')
        self.adv_btn_generate.config(state='normal' if has_staged and is_idle else 'disabled')
        self.adv_btn_save_last.config(state='normal' if self.adv_last_generated_manifest and is_idle else 'disabled')
        
        # Single file hasher controls
        self.adv_sf_select_btn.config(state='normal' if is_idle else 'disabled')
        self.adv_sf_calc_btn.config(state='normal' if self.adv_single_file_path.get() and is_idle else 'disabled')
        self.adv_sf_copy_btn.config(state='normal' if self.adv_single_file_hash.get() and is_idle else 'disabled')
        self.adv_sf_save_btn.config(state='normal' if self.adv_single_file_hash.get() and is_idle else 'disabled')
    
    # ==============================================================================
    # --- ADVANCED HASH TOOLS - Event Handlers ---
    # ==============================================================================
    
    def adv_select_game_root(self):
        """Select game root folder."""
        path = filedialog.askdirectory(title="Select the Main Game Folder")
        if not path:
            return
        
        self.adv_game_root = Path(path).resolve()
        self.adv_var_root_path.set(f"Root: {self.adv_game_root}")
        self.adv_list_staged.delete(0, tk.END)
        self.adv_populate_explorer()
        self.adv_var_status.set("Game root set. Select items or use conversion tools.")
        self.adv_update_ui_state()
    
    def adv_populate_explorer(self):
        """Populate file explorer tree."""
        self.adv_tree_explorer.delete(*self.adv_tree_explorer.get_children())
        
        if not self.adv_game_root or not self.adv_game_root.exists():
            return
        
        for item in sorted(self.adv_game_root.iterdir()):
            self.adv_tree_explorer.insert('', tk.END, text=item.name, values=(str(item),))
    
    def adv_add_to_staging(self):
        """Add selected items to staging list."""
        selections = self.adv_tree_explorer.selection()
        for item_id in selections:
            item_name = self.adv_tree_explorer.item(item_id)['text']
            if item_name not in self.adv_list_staged.get(0, tk.END):
                self.adv_list_staged.insert(tk.END, item_name)
        self.adv_update_ui_state()
    
    def adv_remove_from_staging(self):
        """Remove selected items from staging list."""
        selections = self.adv_list_staged.curselection()
        for index in reversed(selections):
            self.adv_list_staged.delete(index)
        self.adv_update_ui_state()
    
    def adv_select_single_file(self):
        """Select single file for hashing."""
        filepath = filedialog.askopenfilename(title="Select file to hash", filetypes=[("All files", "*.*")])
        if not filepath:
            return
        
        self.adv_single_file_path.set(filepath)
        self.adv_single_file_hash.set("")
        self.adv_sf_progress_bar['value'] = 0
        self.adv_update_ui_state()
        self.adv_var_status.set(f"File selected: {Path(filepath).name}")
    
    def adv_copy_hash_to_clipboard(self):
        """Copy hash to clipboard."""
        hash_val = self.adv_single_file_hash.get()
        if not hash_val:
            return
        
        self.clipboard_clear()
        self.clipboard_append(hash_val)
        self.adv_var_status.set("Hash copied to clipboard!")
        messagebox.showinfo("Copied", "Hash copied to clipboard!")
    
    def adv_save_hash_to_file(self):
        """Save hash to .sha256 file."""
        hash_val = self.adv_single_file_hash.get()
        source_path = Path(self.adv_single_file_path.get())
        
        if not (hash_val and source_path.exists()):
            return
        
        output_filename = filedialog.asksaveasfilename(
            title="Save SHA-256 Hash As",
            initialfile=f"{source_path.name}.sha256",
            defaultextension=".sha256",
            filetypes=[("SHA-256 files", "*.sha256"), ("Text files", "*.txt")]
        )
        
        if not output_filename:
            return
        
        try:
            with open(output_filename, 'w', encoding='utf-8') as f:
                f.write(f"{hash_val}  {source_path.name}\n")
            self.adv_var_status.set(f"Hash saved: {Path(output_filename).name}")
            messagebox.showinfo("Success", f"Hash saved successfully!\n{output_filename}")
        except (IOError, OSError) as e:
            messagebox.showerror("Error", f"Failed to save hash:\n{e}")
    
    # ==============================================================================
    # --- ADVANCED HASH TOOLS - Worker Thread Starters ---
    # ==============================================================================
    
    def adv_start_generation_thread(self):
        """Start manifest generation."""
        staged_paths = [self.adv_game_root / item_name for item_name in self.adv_list_staged.get(0, tk.END)]
        if not staged_paths:
            messagebox.showwarning("No Items", "No items staged for manifest generation.")
            return
        
        self.adv_start_processing("Generating manifest...", self.adv_generate_manifest_worker, (staged_paths, self.adv_game_root))
    
    def adv_start_md5_conversion(self):
        """Start MD5 to SHA256 conversion."""
        if not self.adv_game_root:
            messagebox.showwarning("No Root", "Please select game root folder first.")
            return
        
        md5_filepath = filedialog.askopenfilename(
            title="Select MD5 Checksum File",
            filetypes=[("MD5 files", "*.md5"), ("All files", "*.*")]
        )
        
        if not md5_filepath:
            return
        
        self.adv_start_processing("Converting MD5 to SHA256...", self.adv_md5_convert_worker, (md5_filepath, self.adv_game_root))
    
    def adv_start_sfv_conversion(self):
        """Start SFV to SHA256 conversion."""
        if not self.adv_game_root:
            messagebox.showwarning("No Root", "Please select game root folder first.")
            return
        
        sfv_filepath = filedialog.askopenfilename(
            title="Select SFV Checksum File",
            filetypes=[("SFV files", "*.sfv"), ("All files", "*.*")]
        )
        
        if not sfv_filepath:
            return
        
        self.adv_start_processing("Converting SFV to SHA256...", self.adv_sfv_convert_worker, (sfv_filepath, self.adv_game_root))
    
    def adv_start_fast_conversion(self):
        """Start fast JSON lookup conversion."""
        master_json_path = filedialog.askopenfilename(
            title="Select MASTER SHA-256 manifest.json",
            filetypes=[("JSON files", "*.json")]
        )
        
        if not master_json_path:
            return
        
        md5_filepath = filedialog.askopenfilename(
            title="Select TARGET MD5 File to convert",
            filetypes=[("MD5 files", "*.md5"), ("All files", "*.*")]
        )
        
        if not md5_filepath:
            return
        
        self.adv_start_processing("Fast converting via JSON lookup...", self.adv_fast_convert_worker, (master_json_path, md5_filepath))
    
    def adv_start_single_file_hash(self):
        """Start single file hash calculation."""
        filepath = self.adv_single_file_path.get()
        if not filepath:
            return
        
        self.adv_is_processing = True
        self.adv_sf_progress_bar['value'] = 0
        self.adv_single_file_hash.set("")
        self.adv_var_status.set(f"Hashing: {Path(filepath).name}...")
        self.adv_update_ui_state()
        
        thread = threading.Thread(target=self.adv_calculate_single_file_hash_worker, args=(Path(filepath),), daemon=True)
        thread.start()
    
    def adv_start_processing(self, start_message: str, worker_func, args):
        """Start background processing."""
        self.adv_is_processing = True
        self.adv_last_generated_manifest = None
        self.adv_last_generation_errors = None
        self.adv_progress_bar['value'] = 0
        self.adv_var_status.set(start_message)
        self.adv_update_ui_state()
        
        thread = threading.Thread(target=worker_func, args=args, daemon=True)
        thread.start()
    
    # ==============================================================================
    # --- ADVANCED HASH TOOLS - Worker Functions ---
    # ==============================================================================
    
    def adv_generate_manifest_worker(self, paths_to_process: List[Path], game_root: Path):
        """Worker: Generate manifest from selected paths."""
        try:
            total_files = sum(1 for p in paths_to_process for _ in p.rglob('*') if _.is_file())
            manifest = {}
            errors = []
            processed = 0
            
            for base_path in paths_to_process:
                if base_path.is_file():
                    file_list = [base_path]
                else:
                    file_list = [f for f in base_path.rglob('*') if f.is_file()]
                
                for file_path in file_list:
                    try:
                        relative_path = file_path.relative_to(game_root)
                        file_hash = self.adv_calculate_sha256(file_path)
                        
                        if file_hash:
                            manifest[str(relative_path).replace('\\', '/')] = file_hash
                        else:
                            errors.append(f"Failed to hash: {relative_path}")
                        
                        processed += 1
                        progress = int((processed / total_files) * 100) if total_files > 0 else 0
                        self.adv_update_queue.put(('progress', progress))
                        self.adv_update_queue.put(('status', f"Processing: {relative_path.name} ({processed}/{total_files})"))
                    
                    except Exception as e:
                        errors.append(f"Error processing {file_path.name}: {e}")
            
            self.adv_update_queue.put(('complete', (manifest, errors)))
        
        except Exception as e:
            self.adv_update_queue.put(('error', f"Generation failed: {e}"))
    
    def adv_md5_convert_worker(self, md5_filepath: str, game_root: Path):
        """Worker: Convert MD5 manifest to SHA256."""
        try:
            file_paths = self.adv_robust_parse_md5_file(md5_filepath)
            total_files = len(file_paths)
            manifest = {}
            errors = []
            
            for idx, rel_path in enumerate(file_paths, 1):
                full_path = game_root / rel_path
                
                if full_path.exists() and full_path.is_file():
                    file_hash = self.adv_calculate_sha256(full_path)
                    if file_hash:
                        manifest[rel_path.replace('\\', '/')] = file_hash
                    else:
                        errors.append(f"Failed to hash: {rel_path}")
                else:
                    errors.append(f"File not found: {rel_path}")
                
                progress = int((idx / total_files) * 100)
                self.adv_update_queue.put(('progress', progress))
                self.adv_update_queue.put(('status', f"Converting: {Path(rel_path).name} ({idx}/{total_files})"))
            
            self.adv_update_queue.put(('complete', (manifest, errors)))
        
        except Exception as e:
            self.adv_update_queue.put(('error', f"MD5 conversion failed: {e}"))
    
    def adv_sfv_convert_worker(self, sfv_filepath: str, game_root: Path):
        """Worker: Convert SFV manifest to SHA256."""
        try:
            file_paths = self.adv_robust_parse_sfv_file(sfv_filepath)
            total_files = len(file_paths)
            manifest = {}
            errors = []
            
            for idx, rel_path in enumerate(file_paths, 1):
                full_path = game_root / rel_path
                
                if full_path.exists() and full_path.is_file():
                    file_hash = self.adv_calculate_sha256(full_path)
                    if file_hash:
                        manifest[rel_path.replace('\\', '/')] = file_hash
                    else:
                        errors.append(f"Failed to hash: {rel_path}")
                else:
                    errors.append(f"File not found: {rel_path}")
                
                progress = int((idx / total_files) * 100)
                self.adv_update_queue.put(('progress', progress))
                self.adv_update_queue.put(('status', f"Converting: {Path(rel_path).name} ({idx}/{total_files})"))
            
            self.adv_update_queue.put(('complete', (manifest, errors)))
        
        except Exception as e:
            self.adv_update_queue.put(('error', f"SFV conversion failed: {e}"))
    
    def adv_fast_convert_worker(self, master_json_path: str, md5_filepath: str):
        """Worker: Fast convert using JSON lookup."""
        try:
            with open(master_json_path, 'r', encoding='utf-8') as f:
                master_manifest = json.load(f)
            
            file_paths = self.adv_robust_parse_md5_file(md5_filepath)
            total_files = len(file_paths)
            manifest = {}
            errors = []
            
            for idx, rel_path in enumerate(file_paths, 1):
                normalized_path = rel_path.replace('\\', '/')
                
                if normalized_path in master_manifest:
                    manifest[normalized_path] = master_manifest[normalized_path]
                else:
                    errors.append(f"Not found in master: {rel_path}")
                
                progress = int((idx / total_files) * 100)
                self.adv_update_queue.put(('progress', progress))
                self.adv_update_queue.put(('status', f"Looking up: {Path(rel_path).name} ({idx}/{total_files})"))
            
            self.adv_update_queue.put(('complete', (manifest, errors)))
        
        except Exception as e:
            self.adv_update_queue.put(('error', f"Fast conversion failed: {e}"))
    
    def adv_calculate_single_file_hash_worker(self, file_path: Path):
        """Worker: Calculate single file hash."""
        sha256 = hashlib.sha256()
        
        try:
            file_size = file_path.stat().st_size
            processed = 0
            
            with open(file_path, 'rb') as f:
                while chunk := f.read(8192):
                    sha256.update(chunk)
                    processed += len(chunk)
                    progress = int((processed / file_size) * 100) if file_size > 0 else 100
                    self.adv_update_queue.put(('sf_progress', progress))
            
            hash_result = sha256.hexdigest()
            self.adv_update_queue.put(('sf_complete', hash_result))
        
        except (IOError, OSError) as e:
            self.adv_update_queue.put(('sf_error', f"Hashing failed: {e}"))
    
    def adv_process_queue(self):
        """Process queue updates."""
        try:
            while True:
                msg_type, data = self.adv_update_queue.get_nowait()
                
                if msg_type == 'progress':
                    self.adv_progress_bar['value'] = data
                elif msg_type == 'status':
                    self.adv_var_status.set(data)
                elif msg_type == 'complete':
                    self.adv_on_generation_complete(data[0], data[1])
                elif msg_type == 'error':
                    self.adv_on_generation_error(data)
                elif msg_type == 'sf_progress':
                    self.adv_sf_progress_bar['value'] = data
                elif msg_type == 'sf_complete':
                    self.adv_on_single_file_hash_complete(data)
                elif msg_type == 'sf_error':
                    self.adv_on_single_file_hash_error(data)
        
        except queue.Empty:
            pass
        
        self.after(100, self.adv_process_queue)
    
    def adv_on_generation_complete(self, manifest: Dict[str, str], errors: List[str]):
        """Handle manifest generation completion."""
        self.adv_is_processing = False
        self.adv_last_generated_manifest = manifest
        self.adv_last_generation_errors = errors
        self.adv_progress_bar['value'] = 100
        
        error_summary = f"\n{len(errors)} errors occurred." if errors else ""
        self.adv_var_status.set(f"✅ Complete! Generated {len(manifest)} hashes.{error_summary}")
        self.adv_update_ui_state()
        
        messagebox.showinfo("Complete", f"Manifest generated!\n\nFiles: {len(manifest)}\nErrors: {len(errors)}")
    
    def adv_on_generation_error(self, error_message: str):
        """Handle generation error."""
        self.adv_is_processing = False
        self.adv_var_status.set(f"❌ Error: {error_message}")
        self.adv_update_ui_state()
        messagebox.showerror("Error", error_message)
    
    def adv_on_single_file_hash_complete(self, hash_result: str):
        """Handle single file hash completion."""
        self.adv_is_processing = False
        self.adv_single_file_hash.set(hash_result)
        self.adv_sf_progress_bar['value'] = 100
        self.adv_var_status.set("✅ Hash calculated successfully!")
        self.adv_update_ui_state()
    
    def adv_on_single_file_hash_error(self, error_message: str):
        """Handle single file hash error."""
        self.adv_is_processing = False
        self.adv_sf_progress_bar['value'] = 0
        self.adv_var_status.set(f"❌ {error_message}")
        self.adv_update_ui_state()
        messagebox.showerror("Error", error_message)
    
    def adv_save_last_manifest(self):
        """Save last generated manifest."""
        if not self.adv_last_generated_manifest:
            messagebox.showwarning("No Manifest", "No manifest to save. Generate one first.")
            return
        
        output_filename = filedialog.asksaveasfilename(
            title="Save Manifest As",
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if not output_filename:
            return
        
        try:
            with open(output_filename, 'w', encoding='utf-8') as f:
                json.dump(self.adv_last_generated_manifest, f, indent=2, ensure_ascii=False)
            
            self.adv_var_status.set(f"✅ Manifest saved: {Path(output_filename).name}")
            messagebox.showinfo("Success", f"Manifest saved!\n{output_filename}")
        
        except (IOError, OSError) as e:
            messagebox.showerror("Error", f"Failed to save manifest:\n{e}")

# ==============================================================================
# --- MAIN ---
# ==============================================================================

if __name__ == "__main__":
    app = AdminPanelGUI()
    app.mainloop()
