### **Enhanced Visual Design & Modular Architecture (`v1.0` - Cricket 26 Edition)**
# CRICKET26_UTILITY_v1.0 ("Phoenix Enhanced - Cricket 26")
# 
# Created by: XLR8 (Discord: xlr8_boi)
# Contributor: ADITYA (Discord: adityaberchha)
# 
# GitHub Repository: https://github.com/aman71711/CRICKET26_Utility
#
# v1.0 (Cricket 26 Initial Release):
#         - FEATURE: Updated for Cricket 26 game support
#         - FEATURE: Google Drive download support via gdown
#         - FEATURE: Optional fallback link system for reliability
#         - FEATURE: Sequential update installation (V1 → V2 → V3)
#         - FEATURE: Improved version.json structure for admin panel
#         - REMOVED: Pixeldrain and Akirabox support
#         - IMPROVEMENT: Enhanced error handling for sequential updates
#         - IMPROVEMENT: Better admin panel integration


import multiprocessing
import re
import tkinter as tk
import tempfile
from tkinter import ttk, filedialog, messagebox, Menu
import os
import sys
import subprocess
import shutil
import threading
import queue
import hashlib
import requests
import json
import winreg
import webbrowser
import ctypes
import socket
import platform
import time
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, Any, List, Tuple, Callable
from collections import deque
from enum import Enum, auto
from functools import wraps
from concurrent.futures import ThreadPoolExecutor, Future, as_completed, wait, FIRST_COMPLETED

# --- Dependency Checks ---
try:
    import psutil
    import sv_ttk
    import cpuinfo
    import winreg
    import webbrowser
    import ctypes
    import socket
    import platform
    import time
    import json
    import wmi
    import pythoncom
    # NEW: Import gdown for Google Drive support
    import gdown
    # Don't import tkfontawesome - we'll use Unicode symbols instead
except ImportError as e:
    root = tk.Tk()
    root.withdraw()
    missing_lib = str(e).split("'")[1] if "'" in str(e) else "unknown"
    if missing_lib == "gdown":
        messagebox.showerror("Missing Dependencies", f"Google Drive support requires 'gdown' library.\nPlease install it by running:\n\npip install gdown\n\nMissing: {e}")
    else:
        messagebox.showerror("Missing Dependencies", f"Some required libraries are missing.\nPlease install them by running:\n\npip install psutil sv-ttk py-cpuinfo WMI pywin32 gdown\n\nMissing: {e}")
    sys.exit(1)

# ==============================================================================
# --- CONSTANTS, ENUMS, AND THEME DATA ---
# ==============================================================================
class Constants:
    SCRIPT_VERSION = "v1.0"
    APP_NAME = "Cricket 26 Auto Updater"
    APP_VERSION = "v1.0"
    AUTHOR = "XLR8"
    CREATOR_DISCORD = "xlr8_boi"
    API_URL = "https://raw.githubusercontent.com/aman71711/CRICKET26_Utility/main/version.json"
    LOG_FILENAME = "cricket26_updater.log"
    DISCORD_LINK = "https://discord.gg/5gWWv3ar"
    LOG_SYMBOLS = {"INFO": "✅", "WARNING": "⚠️", "ERROR": "❌", "CRITICAL": "🛑", "SETTING": "⚙️", "DIAG": "🩺" }
    CACHE_DIR = Path(tempfile.gettempdir()) / "cricket26_updater_cache"
    VERIFICATION_LOGS_DIR = CACHE_DIR / "Verification_Logs"
    GAME_EXECUTABLE = "cricket26.exe"
    DOWNLOAD_TIMEOUT_SECONDS = 15
    DOWNLOAD_THREADS = 6  # Number of concurrent download threads for smart system
    DOWNLOAD_CONCURRENT_CHUNKS = 8  # Increased from 4 to 8 for better speed
    DOWNLOAD_CHUNK_SIZE = 10 * 1024 * 1024  # 10MB chunks for optimal performance
    DOWNLOAD_BUFFER_SIZE = 128 * 1024  # 128KB buffer for file writing
    DIAG_PROCESS_TIMEOUT_SECONDS = 60
    DXDIAG_TIMEOUT_SECONDS = 180
    WMI_TIMEOUT_SECONDS = 20
    
    # UI Performance Optimization Constants
    QUEUE_PROCESS_INTERVAL_ACTIVE = 30  # ms during active operations (was 50)
    QUEUE_PROCESS_INTERVAL_IDLE = 100  # ms during idle (was 100)
    MAX_QUEUE_MESSAGES_PER_CYCLE = 20  # Limit messages per cycle to prevent UI freeze
    MAX_LOG_BUFFER_SIZE = 10000  # Maximum log entries to keep in memory
    CLEANUP_INTERVAL_CYCLES = 300  # Cleanup every N cycles (300 * 30ms = 9s)
    
    # --- Modern Unicode Icons (No FontAwesome dependency needed) ---
    ICON_SHIELD = '🛡️'              # shield (protection/security)
    ICON_SUN = '☀️'                 # sun (light theme)
    ICON_MOON = '🌙'                # moon (dark theme)
    ICON_CLOUD_DOWNLOAD = '🔄'      # sync/updater (better than cloud for updates)
    ICON_CHECK_CIRCLE = '✅'        # check circle (verification success)
    ICON_TOOLS = '🔧'               # tools (maintenance/settings)
    ICON_STETHOSCOPE = '🩺'         # stethoscope (diagnostics)
    ICON_FILE_ALT = '📄'            # file (documents/logs)
    ICON_SEARCH = '🔍'              # search (check for updates)
    ICON_CHECK = '✓'                # check (confirmation)
    ICON_DOWNLOAD = '⬇️'            # download (download action)
    ICON_PAUSE = '⏸️'               # pause (pause download)
    ICON_PLAY = '▶️'                # play (resume download)
    ICON_TIMES = '❌'               # times (cancel/close)
    ICON_SHIELD_CHECK = '🛡️✓'      # shield-check (verified protection)
    ICON_SAVE = '💾'                # save (backup saves)
    ICON_UPLOAD = '⬆️'              # upload (restore backup)
    ICON_COPY = '📋'                # copy (copy to clipboard)
    ICON_GAMEPAD = '🎮'             # gamepad (launch game)
    ICON_DATABASE = '🗄️'           # database (data management)
    ICON_HISTORY = '📚'             # history (version history)
    ICON_ARCHIVE = '📦'             # archive (compressed files)
    ICON_FOLDER = '📁'              # folder (directory selection)
    ICON_FOLDER_OPEN = '📂'         # folder-open (opened directory)
    ICON_TRASH = '🗑️'              # trash (clear cache)
    ICON_BROOM = '🧹'               # broom (cleanup/clear cache)
    ICON_ERASER = '🧽'              # eraser (clear/delete)
    ICON_RETRY = '🔄'               # retry (retry failed download)
    ICON_FILE_EXPORT = '📤'         # file-export (export logs)
    ICON_REFRESH = '🔄'             # refresh (reload/update)
    ICON_WARNING = '⚠️'             # warning (alerts)
    ICON_QUESTION = '❓'            # question (help/info)
    ICON_COG = '⚙️'                 # cog (settings)
    ICON_MAGIC = '✨'               # magic (auto-features)
    ICON_ROCKET = '🚀'              # rocket (launch/start)
    ICON_STAR = '⭐'                # star (featured/important)
    ICON_SHORTCUT = '🔗'            # shortcut creation
    ICON_HEART = '❤️'               # heart (favorites)
    ICON_SYNC = '🔄'                # sync (synchronization)
    ICON_BOLT = '⚡'                # bolt (fast/performance)
    ICON_CHART_LINE = '📈'          # chart-line (statistics)
    ICON_USER_SHIELD = '👤🛡️'       # user-shield (admin privileges)
    ICON_GDRIVE = '📂'              # Google Drive icon

# ==============================================================================
# --- CREDITS & ACKNOWLEDGMENTS ---
# ==============================================================================

# --- CREDITS & ACKNOWLEDGMENTS ---
# (Refactored: Removed Begula from credits)
class Credits:
    """Cricket 26 Auto Updater - Development Team"""
    # --- Development Team ---
    TEAM = {
        'XLR8': {
            'username': 'xlr8_boi',
            'role': 'Creator'
        },
        'ADITYA': {
            'username': 'adityaberchha',
            'role': 'Contributor'
        }
    }
    # --- Project Information ---
    PROJECT_INFO = {
        'repository': 'https://github.com/aman71711/CRICKET26_Utility',
        'discord_server': 'https://discord.gg/5gWWv3ar',
        'version': Constants.SCRIPT_VERSION
    }
    @classmethod
    def get_credits_text(cls) -> str:
        """Generate a formatted credits text for display."""
        credits_text = f"""
{Constants.APP_NAME} {Constants.SCRIPT_VERSION}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

👑 XLR8 (@xlr8_boi) - Creator
⭐ ADITYA (@adityaberchha) - Contributor

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Thank you for using Cricket 26 Auto Updater!
        """.strip()
        return credits_text
    @classmethod
    def get_team_info(cls) -> Dict[str, Any]:
        """Get structured team information for programmatic use."""
        return {
            'team': cls.TEAM,
            'project': cls.PROJECT_INFO
        }

# ==============================================================================
# --- MODERN THEMING SYSTEM ---
# ==============================================================================
class ModernThemeManager:
    """Advanced theming system for world-class UI/UX design."""
    
    # --- Color Palettes (Modern Design System) ---
    THEMES = {
        'dark': {
            'name': 'Dark Professional',
            'colors': {
                'primary': '#0a0a0a',           # Deeper black for modern look
                'secondary': '#141414',         # Rich dark gray
                'tertiary': '#1e1e1e',          # Elevated surface
                'accent': '#2196F3',            # Material Blue - more vibrant
                'accent_hover': '#1976D2',      # Darker blue on hover
                'success': '#4CAF50',           # Material Green - vibrant
                'warning': '#FF9800',           # Material Orange
                'error': '#F44336',             # Material Red
                'info': '#00BCD4',              # Cyan - bright and modern
                'cyan': '#00E5FF',              # Electric cyan for highlights
                'purple': '#9C27B0',            # Material Purple for variety
                'text_primary': '#FFFFFF',      # Pure white
                'text_secondary': '#B0BEC5',    # Cool gray
                'text_muted': '#78909C',        # Muted blue-gray
                'border': '#263238',            # Dark blue-gray border
                'highlight': '#37474F',         # Blue-gray highlight
                'surface': '#1a1a1a',           # Surface gray
                'card': '#212121',              # Elevated card
                'cache_button': '#F44336',      # Material red for destructive action
                'cache_button_hover': '#D32F2F', # Darker red
                'gradient_start': '#0a0a0a',    # Deep black
                'gradient_end': '#1e1e1e',      # Elevated surface
            },
            'fonts': {
                'title': ('Segoe UI', 20, 'bold'),
                'subtitle': ('Segoe UI', 14, 'normal'),
                'body': ('Segoe UI', 10, 'normal'),
                'button': ('Segoe UI', 10, 'bold'),
                'mono': ('Consolas', 9, 'normal'),
            }
        }
    }
    
    # --- Modern Layout Configuration ---
    LAYOUT_CONFIG = {
        'padding': {
            'main_frame': 20,
            'section_frame': 16,
            'button_frame': 12,
            'widget_spacing': 8,
            'card_padding': 16,
        },
        'geometry': {
            'min_width': 1100,
            'min_height': 800,
            'default_width': 1200,
            'default_height': 900,
        },
        'spacing': {
            'section_gap': 20,
            'widget_gap': 12,
            'button_gap': 8,
            'card_gap': 16,
        },
        'borders': {
            'radius': 8,
            'width': 1,
        },
        'animations': {
            'hover_duration': 200,
            'transition_duration': 300,
        }
    }
    
    # --- Button Configurations ---
    BUTTON_STYLES = {
        'primary': {
            'icon': Constants.ICON_CHECK,
            'style': 'Modern.Primary.TButton',
            'height': 36,
            'padding': (16, 8),
        },
        'secondary': {
            'icon': Constants.ICON_TOOLS,
            'style': 'Modern.Secondary.TButton',
            'height': 32,
            'padding': (12, 6),
        },
        'success': {
            'icon': Constants.ICON_CHECK_CIRCLE,
            'style': 'Modern.Success.TButton',
            'height': 32,
            'padding': (12, 6),
        },
        'warning': {
            'icon': Constants.ICON_WARNING,
            'style': 'Modern.Warning.TButton',
            'height': 32,
            'padding': (12, 6),
        },
        'danger': {
            'icon': Constants.ICON_TIMES,
            'style': 'Modern.Danger.TButton',
            'height': 32,
            'padding': (12, 6),
        },
        'cache_clear': {
            'icon': Constants.ICON_BROOM,
            'style': 'Modern.CacheClear.TButton',
            'text': 'Clear Download Cache',
            'tooltip': 'Remove all downloaded update files to free up disk space',
            'height': 36,
            'padding': (16, 8),
        }
    }
    
    @classmethod
    def get_theme(cls, theme_name: str) -> Dict[str, Any]:
        """Get a complete theme configuration."""
        return cls.THEMES.get(theme_name, cls.THEMES['dark'])
    
    @classmethod
    def get_cyan_color(cls, theme_name: str) -> str:
        """Get the cyan color - always dark theme since light mode removed."""
        return cls.THEMES['dark']['colors']['cyan']
    
    @classmethod
    def get_button_config(cls, button_type: str) -> Dict[str, Any]:
        """Get button configuration for a specific type."""
        return cls.BUTTON_STYLES.get(button_type, cls.BUTTON_STYLES['secondary'])
    
    @classmethod
    def apply_modern_styles(cls, root_widget, theme_name: str):
        """Apply modern TTK styles based on the theme with error handling."""
        try:
            theme = cls.get_theme(theme_name)
            colors = theme['colors']
            fonts = theme['fonts']
            
            style = ttk.Style()
            
            # Apply base theme first
            try:
                sv_ttk.set_theme(theme_name)
            except Exception as e:
                logger.log(f"Failed to apply sv_ttk theme: {e}", "WARNING")
                # Continue with custom styling
            
            # Configure essential modern button styles only
            try:
                style.configure('Modern.Primary.TButton',
                               font=fonts['button'],  # Use consistent button font (bold)
                               foreground='white',
                               background=colors['accent'],
                               focuscolor='none',
                               borderwidth=0,
                               relief='flat')
                
                style.map('Modern.Primary.TButton',
                         background=[('active', colors['accent_hover']),
                                   ('pressed', colors['accent_hover']),
                                   ('disabled', '#2a2a2a')],  # Proper gray for disabled background
                         foreground=[('active', 'white'),
                                   ('pressed', 'white'),
                                   ('disabled', '#666666')])  # Proper gray for disabled text
                
                style.configure('Modern.Secondary.TButton',
                               font=fonts['button'],  # Use consistent button font (bold)
                               foreground=colors['text_primary'],
                               background=colors['tertiary'],
                               focuscolor='none',
                               borderwidth=0,
                               relief='flat')
                
                style.map('Modern.Secondary.TButton',
                         foreground=[('active', colors['text_primary']),
                                   ('pressed', colors['text_primary']),
                                   ('disabled', '#666666')],  # Proper gray for disabled text
                         background=[('active', colors['accent_hover']),
                                   ('pressed', colors['accent_hover']),
                                   ('disabled', '#2a2a2a')])
                
                style.configure('Modern.CacheClear.TButton',
                               font=fonts['button'],
                               foreground='white',
                               background=colors['cache_button'],
                               focuscolor='none',
                               borderwidth=0,
                               relief='flat')
                
                style.map('Modern.CacheClear.TButton',
                         background=[('active', colors['cache_button_hover']),
                                   ('pressed', colors['cache_button_hover']),
                                   ('disabled', '#2a2a2a')],  # Proper gray for disabled
                         foreground=[('active', 'white'),
                                   ('pressed', 'white'),
                                   ('disabled', '#666666')])  # Proper gray for disabled text
                
                style.configure('Modern.Danger.TButton',
                               font=fonts['button'],
                               foreground='white',
                               background=colors['error'],
                               focuscolor='none',
                               borderwidth=0,
                               relief='flat')
                
                style.map('Modern.Danger.TButton',
                         background=[('active', '#D32F2F'),
                                   ('pressed', '#D32F2F'),
                                   ('disabled', '#2a2a2a')],
                         foreground=[('active', 'white'),
                                   ('pressed', 'white'),
                                   ('disabled', '#666666')])
                
                style.configure('Modern.Utility.TButton',
                               font=fonts['button'],  # Use consistent button font (bold)
                               foreground=colors['text_primary'],
                               background=colors['tertiary'],
                               focuscolor='none',
                               borderwidth=0,
                               relief='flat')
                
                style.map('Modern.Utility.TButton',
                         foreground=[('active', colors['text_primary']),
                                   ('pressed', colors['text_primary']),
                                   ('disabled', '#666666')],  # Proper gray for disabled text
                         background=[('active', colors['accent_hover']),
                                   ('pressed', colors['accent_hover']),
                                   ('disabled', '#2a2a2a')])  # Proper gray for disabled background
                
                style.configure('Modern.Small.TButton',
                               font=fonts['button'],  # Use consistent button font (bold)
                               foreground=colors['text_primary'],
                               background=colors['tertiary'],
                               focuscolor='none',
                               borderwidth=0,
                               relief='flat')
                
                style.map('Modern.Small.TButton',
                         foreground=[('active', colors['text_primary']),
                                   ('pressed', colors['text_primary']),
                                   ('disabled', '#666666')],  # Proper gray for disabled text
                         background=[('active', colors['accent_hover']),
                                   ('pressed', colors['accent_hover']),
                                   ('disabled', '#2a2a2a')])  # Proper gray for disabled background
                
                # Red danger button for cache clearing
                style.configure('Modern.Danger.TButton',
                               font=fonts['button'],  # Use consistent button font (bold)
                               foreground='white',
                               background='#e74c3c',  # Red background
                               focuscolor='none',
                               borderwidth=0,
                               relief='flat')
                
                style.map('Modern.Danger.TButton',
                         background=[('active', '#c0392b'),  # Darker red on hover
                                   ('pressed', '#c0392b'),
                                   ('disabled', '#2a2a2a')],  # Proper gray for disabled
                         foreground=[('active', 'white'),
                                   ('pressed', 'white'),
                                   ('disabled', '#666666')])  # Proper gray for disabled text
                
                # Success button styling
                style.configure('Modern.Success.TButton',
                               font=fonts['button'],  # Use consistent button font (bold)
                               foreground='white',
                               background='#27ae60',  # Green background
                               focuscolor='none',
                               borderwidth=0,
                               relief='flat')
                
                style.map('Modern.Success.TButton',
                         background=[('active', '#229954'),  # Darker green on hover
                                   ('pressed', '#229954'),
                                   ('disabled', '#2a2a2a')],  # Proper gray for disabled
                         foreground=[('active', 'white'),
                                   ('pressed', 'white'),
                                   ('disabled', '#666666')])  # Proper gray for disabled text
                
                # Warning button styling
                style.configure('Modern.Warning.TButton',
                               font=fonts['button'],  # Use consistent button font (bold)
                               foreground='white',
                               background='#f39c12',  # Orange background
                               focuscolor='none',
                               borderwidth=0,
                               relief='flat')
                
                style.map('Modern.Warning.TButton',
                         background=[('active', '#e67e22'),  # Darker orange on hover
                                   ('pressed', '#e67e22'),
                                   ('disabled', '#2a2a2a')],  # Proper gray for disabled
                         foreground=[('active', 'white'),
                                   ('pressed', 'white'),
                                   ('disabled', '#666666')])  # Proper gray for disabled text
                
                # Essential label styles with enhanced typography
                style.configure('Modern.Title.TLabel', 
                               font=fonts['title'],
                               foreground=colors['text_primary'])
                
                style.configure('Modern.Subtitle.TLabel', 
                               font=fonts['subtitle'],
                               foreground=colors['text_secondary'])
                
                # Status and feedback styles with color coding
                style.configure('Modern.Success.TLabel',
                               font=fonts['body'],
                               foreground='#27ae60')  # Green for success
                
                style.configure('Modern.Warning.TLabel',
                               font=fonts['body'],
                               foreground='#f39c12')  # Orange for warnings
                
                style.configure('Modern.Error.TLabel',
                               font=fonts['body'],
                               foreground='#e74c3c')  # Red for errors
                
                style.configure('Modern.Info.TLabel',
                               font=fonts['body'],
                               foreground='#3498db')  # Blue for info
                
                style.configure('Modern.Muted.TLabel',
                               font=('Segoe UI', 8),
                               foreground=colors['text_muted'])
                
                # Enhanced progress styles
                style.configure('Modern.Progress.TLabel',
                               font=fonts['body'],
                               foreground='#3498db')  # Blue for progress
                
                logger.log("Modern theme styles applied successfully", "INFO")
                
            except Exception as e:
                logger.log(f"Failed to configure custom styles: {e}", "WARNING")
                # Fall back to basic styling
                
        except Exception as e:
            logger.log(f"Critical error in theme application: {e}", "ERROR")
            # Application will continue with default TTK styles

# Alias for backwards compatibility
ThemeManager = ModernThemeManager

class AppState(Enum):
    STARTING = auto(); IDLE = auto(); UPDATING = auto(); VERIFYING = auto()
    DIAGNOSTICS = auto(); MANUAL_INSTALLING = auto(); BUSY = auto()

class Q_MSG:
    STATUS = 'status'; OVERALL_STATUS = 'overall_status'; PROGRESS = 'progress'
    PROGRESS_MODE = 'progress_mode'
    COMPLETE = 'complete'; CANCELLED = 'cancelled'; CHECKSUM_CONFIRM = 'checksum_mismatch_confirm'
    DOWNLOAD_FAILED = 'download_failed_persistently'; VERIFY_STATS = 'verify_stats_update'
    DOWNLOAD_RETRY_WAIT = 'download_retry_wait'; DOWNLOAD_SPEED = 'download_speed'  # NEW: Speed/ETA display
    DOWNLOAD_ERROR_RETRY = 'download_error_retry'  # NEW: Error recovery
    VERIFY_COMPLETE = 'verify_complete'; VERIFY_CANCELLED = 'verify_cancelled'
    VERIFY_ISSUES_BATCH = 'verify_issues_batch'
    MANUAL_INSTALL_CONFIRM = 'manual_install_confirm'
    MANUAL_INSTALL_COMPLETE = 'manual_install_complete'
    ERROR = 'error'

# ==============================================================================
# --- HELPER FUNCTIONS & DECORATORS ---
# ==============================================================================
def is_admin() -> bool:
    """Checks if the script is running with administrative privileges."""
    try: return ctypes.windll.shell32.IsUserAnAdmin() != 0
    except Exception: return False

def format_bytes(byte_count: int) -> str:
    """Formats a byte count into a human-readable string (KB, MB, GB)."""
    if byte_count is None: return "N/A"
    power = 1024; n = 0; power_labels = {0: '', 1: 'K', 2: 'M', 3: 'G', 4: 'T'}
    while byte_count >= power and n < len(power_labels) -1: byte_count /= power; n += 1
    return f"{byte_count:.2f} {power_labels[n]}B"

class Logger:
    """Enhanced file logger with rotation and size management."""
    MAX_LOG_SIZE = 10 * 1024 * 1024  # 10MB max log size
    MAX_BACKUP_FILES = 5  # Keep up to 5 backup log files
    
    def __init__(self, filename: str):
        self.log_file = Path(filename)
        self.log_lock = threading.Lock()  # Thread-safe logging
        self.ensure_log_file_exists()
    
    def ensure_log_file_exists(self):
        try:
            if not self.log_file.parent.exists(): 
                self.log_file.parent.mkdir(parents=True, exist_ok=True)
            if not self.log_file.exists(): 
                self.log_file.write_text(f"{Constants.APP_NAME} Log File\n{'='*40}\n\n", encoding='utf-8')
        except (IOError, PermissionError) as e: 
            print(f"CRITICAL: Could not create log file '{self.log_file}': {e}")
    
    def _rotate_log_if_needed(self):
        """Rotate log file if it exceeds maximum size."""
        try:
            if self.log_file.exists() and self.log_file.stat().st_size > self.MAX_LOG_SIZE:
                # Archive current log and create new one
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                archive_name = self.log_file.with_name(f"{self.log_file.stem}_{timestamp}{self.log_file.suffix}")
                self.log_file.rename(archive_name)
                
                # Clean up old backup files, keep only MAX_BACKUP_FILES
                backup_files = sorted(self.log_file.parent.glob(f"{self.log_file.stem}_*{self.log_file.suffix}"))
                while len(backup_files) > self.MAX_BACKUP_FILES:
                    oldest_backup = backup_files.pop(0)
                    oldest_backup.unlink(missing_ok=True)
                
                self.ensure_log_file_exists()
        except Exception as e:
            print(f"Warning: Log rotation failed: {e}")
    
    def log(self, message: str, level: str = "INFO"):
        with self.log_lock:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_entry = f"[{timestamp}] [{level.upper()}] {message}\n"
            try:
                self._rotate_log_if_needed()  # Check if rotation is needed
                with self.log_file.open("a", encoding='utf-8') as f: 
                    f.write(log_entry)
            except (IOError, PermissionError) as e:
                print(f"Failed to write to log file: {e}")
                self.ensure_log_file_exists()
    
    def archive(self) -> str:
        with self.log_lock:
            self.ensure_log_file_exists()
            timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
            archive_name = self.log_file.with_name(f"{self.log_file.stem}_manual_archive_{timestamp}{self.log_file.suffix}")
            if self.log_file.exists():
                self.log_file.rename(archive_name)
                self.log("Log file manually archived.", "INFO")
                return str(archive_name)
            raise FileNotFoundError("Log file does not exist.")

logger = Logger(Constants.LOG_FILENAME)

def require_admin(relaunch_arg: str = "") -> Callable:
    """
    Decorator for controller methods that require admin rights.
    If not admin, it prompts the user to relaunch the application with elevation.
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(controller: 'AppController', *args, **kwargs):
            logger.log(f"Checking admin rights for {func.__name__}. Current admin status: {controller.is_admin}", "SETTING")
            
            if controller.is_admin:
                logger.log(f"Admin rights confirmed. Executing {func.__name__}.", "SETTING")
                return func(controller, *args, **kwargs)
            else:
                logger.log(f"Admin rights required for {func.__name__}. Prompting user for elevation.", "SETTING")
                msg = "This action requires Admin rights. The application will now restart with elevated permissions to complete the operation.\n\nWould you like to continue?"
                if messagebox.askyesno("Admin Rights Required", msg):
                    # Set a visual indicator that we're relaunching
                    if hasattr(controller.view, 'diag_run_button'):
                        controller.view.diag_run_button.config(text="🔄 Relaunching as Admin...", state='disabled')
                    logger.log(f"User approved admin elevation. Relaunching with arg: {relaunch_arg}", "SETTING")
                    controller._relaunch_as_admin(relaunch_arg)
                    # Close current application to avoid confusion
                    controller.view.after(2000, controller.on_closing)  # Close after 2 seconds
                else:
                    logger.log("User cancelled admin elevation request.", "SETTING")
                    # Reset state if user cancels
                    controller.set_state(AppState.IDLE)
        return wrapper
    return decorator

# ==============================================================================
# --- CORE LOGIC COMPONENTS (WORKER CLASSES) ---
# ==============================================================================
class APIHandler:
    """Enhanced API handler with robust error handling and recovery."""
    
    @staticmethod
    def load_update_data() -> Tuple[Optional[Dict[str, Any]], str]:
        """
        Loads update data with enhanced error handling and multiple fallback strategies.
        Returns a tuple of (data, source), where source is 'API', 'CACHE', or 'NONE'.
        """
        api_url = Constants.API_URL
        headers = {'Accept': 'application/vnd.github.v3.raw'}
        cache_path = Constants.CACHE_DIR / "version.json"
        
        # Ensure cache directory exists
        try:
            Constants.CACHE_DIR.mkdir(exist_ok=True, parents=True)
        except Exception as e:
            logger.log(f"Failed to create cache directory: {e}", "WARNING")
        
        # Try primary API with enhanced error handling
        for attempt in range(3):  # 3 attempts with different strategies
            try:
                logger.log(f"Fetching version data from GitHub API (attempt {attempt + 1}/3)...", "INFO")
                
                timeout_values = [(5, 10), (10, 20), (15, 30)][attempt]  # Progressive timeout
                
                response = requests.get(
                    api_url, 
                    headers=headers, 
                    timeout=timeout_values,
                    allow_redirects=True,
                    verify=True  # Ensure SSL verification
                )
                response.raise_for_status()
                
                # Validate response content
                if not response.content:
                    raise ValueError("Empty response from API")
                
                data = response.json()
                
                # Validate essential fields for both old and new schema
                if not isinstance(data, dict):
                    raise ValueError("Invalid API response format - not a dict")
                
                # Check for new schema (v2.0) with sequential updates
                schema_version = data.get('metadata', {}).get('schema_version', '1.0')
                
                if schema_version == '2.0':
                    # New Cricket 26 schema validation
                    logger.log("Detected new schema version 2.0 (Cricket 26 sequential updates)", "INFO")
                    
                    # Check for required top-level sections
                    required_sections = ['metadata', 'game_info', 'updates']
                    missing_sections = [s for s in required_sections if s not in data]
                    if missing_sections:
                        raise ValueError(f"Invalid v2.0 schema - missing sections: {missing_sections}")
                    
                    # Check metadata fields
                    metadata = data.get('metadata', {})
                    if 'game_name' not in metadata:
                        raise ValueError("Invalid v2.0 schema - metadata missing game_name")
                    
                    # Check game_info fields
                    game_info = data.get('game_info', {})
                    if 'latest_version' not in game_info:
                        raise ValueError("Invalid v2.0 schema - game_info missing latest_version")
                    
                    # Validate updates structure
                    for idx, update in enumerate(data.get('updates', [])):
                        required_update_fields = ['from_version', 'to_version', 'downloads']
                        missing = [f for f in required_update_fields if f not in update]
                        if missing:
                            raise ValueError(f"Update {idx} missing fields: {missing}")
                        
                        # Validate downloads structure
                        downloads = update.get('downloads', {})
                        if 'primary' not in downloads:
                            raise ValueError(f"Update {idx} missing primary download source")
                        
                        # Validate primary download has required fields
                        primary = downloads['primary']
                        if 'type' not in primary:
                            raise ValueError(f"Update {idx} primary download missing type")
                    
                    logger.log(f"Schema v2.0 validation passed: {len(data['updates'])} sequential updates", "INFO")
                    
                    # Normalize v2.0 schema by flattening for backward compatibility
                    data['latest_version'] = data['game_info']['latest_version']
                    data['game_name'] = data['metadata']['game_name']
                    data['versions'] = data['game_info'].get('all_versions', [])
                
                elif 'latest_version' not in data:
                    # Old schema requires at least latest_version
                    raise ValueError("Invalid API response format - missing latest_version")
                
                logger.log(f"Successfully loaded from GitHub API: v{data.get('latest_version')}", "INFO")
                
                # Cache the successful response
                try:
                    with open(cache_path, 'w', encoding='utf-8') as f:
                        json.dump(data, f, indent=2)
                    logger.log("API response cached successfully", "INFO")
                except Exception as cache_error:
                    logger.log(f"Failed to cache API response: {cache_error}", "WARNING")
                
                return data, "API"
                
            except requests.exceptions.SSLError as e:
                logger.log(f"SSL error on attempt {attempt + 1}: {e}", "ERROR")
                if attempt == 2:  # Last attempt
                    logger.log("All SSL attempts failed, falling back to cache", "WARNING")
                    
            except requests.exceptions.Timeout as e:
                logger.log(f"Timeout on attempt {attempt + 1}: {e}", "WARNING")
                if attempt < 2:
                    time.sleep(2 ** attempt)  # Exponential backoff
                    
            except requests.exceptions.ConnectionError as e:
                logger.log(f"Connection error on attempt {attempt + 1}: {e}", "WARNING")
                if attempt < 2:
                    time.sleep(2 ** attempt)
                    
            except requests.exceptions.HTTPError as e:
                status_code = getattr(e.response, 'status_code', 'unknown')
                logger.log(f"HTTP error {status_code} on attempt {attempt + 1}: {e}", "ERROR")
                if status_code in [429, 503]:  # Rate limit or service unavailable
                    if attempt < 2:
                        time.sleep(5 * (attempt + 1))
                else:
                    break  # Don't retry for client errors (4xx)
                    
            except (ValueError, json.JSONDecodeError) as e:
                logger.log(f"Invalid API response on attempt {attempt + 1}: {e}", "ERROR")
                break  # Don't retry for data format errors
                
            except Exception as e:
                logger.log(f"Unexpected error on attempt {attempt + 1}: {e}", "ERROR")
                if attempt < 2:
                    time.sleep(1)
        
        # Fallback to cache
        if cache_path.exists():
            try:
                logger.log("API failed, attempting to load from cache...", "INFO")
                
                # Check cache age
                cache_age = time.time() - cache_path.stat().st_mtime
                cache_hours = cache_age / 3600
                
                if cache_hours > 24:  # Cache older than 24 hours
                    logger.log(f"Cache is {cache_hours:.1f} hours old, but using due to API failure", "WARNING")
                
                data = json.loads(cache_path.read_text(encoding="utf-8"))
                
                # Validate cached data - check for v2.0 schema first
                if not isinstance(data, dict):
                    raise ValueError("Invalid cached data format - not a dict")
                
                # Normalize v2.0 schema if present
                schema_version = data.get('metadata', {}).get('schema_version', '1.0')
                if schema_version == '2.0':
                    # Flatten v2.0 structure for backward compatibility
                    if 'game_info' in data and 'latest_version' in data['game_info']:
                        data['latest_version'] = data['game_info']['latest_version']
                    if 'metadata' in data and 'game_name' in data['metadata']:
                        data['game_name'] = data['metadata']['game_name']
                    if 'game_info' in data and 'all_versions' in data['game_info']:
                        data['versions'] = data['game_info']['all_versions']
                
                # Now validate required field exists
                if 'latest_version' not in data:
                    raise ValueError("Invalid cached data format - missing latest_version")
                
                logger.log(f"Successfully loaded from cache: v{data.get('latest_version')}", "INFO")
                return data, "CACHE"
                
            except (json.JSONDecodeError, IOError, ValueError) as e:
                logger.log(f"Cache fallback failed: {e}", "ERROR")
                # Try to remove corrupted cache
                try:
                    cache_path.unlink(missing_ok=True)
                    logger.log("Removed corrupted cache file", "INFO")
                except:
                    pass
        
        logger.log("All data sources failed - API and cache both unavailable", "CRITICAL")
        return None, "NONE"

# ==============================================================================
# --- TESTING AND VALIDATION FUNCTIONS ---
# ==============================================================================
def run_basic_functionality_tests():
    """Run basic tests to ensure core functionality is working."""
    test_results = []
    
    try:
        # Test 1: Logger functionality
        test_logger = Logger("test_log.txt")
        test_logger.log("Test message", "INFO")
        test_results.append(("Logger Test", "PASS", "Basic logging works"))
    except Exception as e:
        test_results.append(("Logger Test", "FAIL", str(e)))
    
    try:
        # Test 2: Constants validation
        assert hasattr(Constants, 'APP_NAME')
        assert hasattr(Constants, 'SCRIPT_VERSION')
        assert hasattr(Constants, 'CACHE_DIR')
        test_results.append(("Constants Test", "PASS", "All required constants defined"))
    except Exception as e:
        test_results.append(("Constants Test", "FAIL", str(e)))
    
    try:
        # Test 3: Theme manager functionality
        theme = ModernThemeManager.get_theme('dark')
        assert 'colors' in theme
        assert 'fonts' in theme
        test_results.append(("Theme Manager Test", "PASS", "Theme system works"))
    except Exception as e:
        test_results.append(("Theme Manager Test", "FAIL", str(e)))
    
    try:
        # Test 4: Credits validation (ensure no Begula references)
        credits_text = Credits.get_credits_text()
        if 'begula' in credits_text.lower() or 'beluga' in credits_text.lower():
            test_results.append(("Credits Test", "FAIL", "Begula still referenced in credits"))
        else:
            test_results.append(("Credits Test", "PASS", "Begula successfully removed"))
    except Exception as e:
        test_results.append(("Credits Test", "FAIL", str(e)))
    
    try:
        # Test 5: Path safety validation
        test_path = Path("test/../../dangerous")
        safe_game_dir = Path("C:/test_game")
        resolved_test = test_path.resolve()
        resolved_game = safe_game_dir.resolve()
        
        # This should detect path traversal
        is_safe = str(resolved_test).startswith(str(resolved_game))
        if not is_safe:
            test_results.append(("Path Safety Test", "PASS", "Path traversal detection works"))
        else:
            test_results.append(("Path Safety Test", "FAIL", "Path traversal not detected"))
    except Exception as e:
        test_results.append(("Path Safety Test", "FAIL", str(e)))
    
    # Print test results
    logger.log("=== FUNCTIONALITY TEST RESULTS ===", "INFO")
    for test_name, result, details in test_results:
        status_icon = "✅" if result == "PASS" else "❌"
        logger.log(f"{status_icon} {test_name}: {result} - {details}", "INFO")
    
    return test_results

# ==============================================================================
# --- GOOGLE DRIVE DOWNLOAD SUPPORT ---
# ==============================================================================

def download_from_gdrive(file_id: str, output_path: Path, 
                        progress_queue: queue.Queue,
                        cancel_event: threading.Event) -> bool:
    """
    Download file from Google Drive using gdown library.
    
    Args:
        file_id: Google Drive file ID or full URL
        output_path: Where to save the downloaded file
        progress_queue: Queue for progress messages
        cancel_event: Event to check for cancellation
    
    Returns:
        True if download successful, False otherwise
    """
    try:
        # Extract file ID from URL if needed
        if 'drive.google.com' in file_id:
            import re
            match = re.search(r'/d/([a-zA-Z0-9_-]+)', file_id)
            if match:
                file_id = match.group(1)
            else:
                match = re.search(r'id=([a-zA-Z0-9_-]+)', file_id)
                if match:
                    file_id = match.group(1)
        
        # Construct download URL
        url = f"https://drive.google.com/uc?id={file_id}"
        
        # Send status update
        progress_queue.put({
            'type': Q_MSG.STATUS,
            'message': f'{Constants.ICON_GDRIVE} Downloading from Google Drive...'
        })
        
        logger.log(f"Starting Google Drive download: {file_id}", "INFO")
        
        # Check if user cancelled before starting download
        if cancel_event.is_set():
            logger.log("Google Drive download cancelled before start", "WARNING")
            return False
        
        # Download with gdown
        result = gdown.download(
            url, 
            str(output_path), 
            quiet=False,
            fuzzy=True  # Handle shared link variations
        )
        
        # Check for cancellation after download
        if cancel_event.is_set():
            logger.log("Google Drive download cancelled - cleaning up", "WARNING")
            if output_path.exists():
                output_path.unlink()  # Delete partial file
            return False
        
        # Check if download succeeded
        if result and output_path.exists() and output_path.stat().st_size > 0:
            logger.log(f"Google Drive download complete: {output_path.name}", "INFO")
            progress_queue.put({
                'type': Q_MSG.STATUS,
                'message': '✅ Google Drive download complete'
            })
            return True
        else:
            raise RuntimeError("Download failed - file is empty or doesn't exist")
            
    except Exception as e:
        logger.log(f"Google Drive download failed: {e}", "ERROR")
        progress_queue.put({
            'type': Q_MSG.STATUS,
            'message': f'❌ Google Drive download failed: {str(e)[:50]}'
        })
        
        # Clean up partial files
        if output_path.exists():
            try:
                output_path.unlink()
            except:
                pass
        
        return False

# ==============================================================================
# --- MULTI-THREADED CONCURRENT DOWNLOADER ---
# ==============================================================================

class ConcurrentDownloader:
    """Manages multi-threaded, pausable, and resumable file downloads with intelligent host failover."""
    def __init__(self, progress_queue: queue.Queue, cancel_event: threading.Event, pause_event: threading.Event):
        self.progress_queue = progress_queue
        self.cancel_event = cancel_event
        self.pause_event = pause_event
        self.speed_buffer = deque(maxlen=10)
        self.total_downloaded = 0
        self.download_lock = threading.Lock()
        self.host_performance = {}  # Track host performance for smart ordering
        self.current_primary_host = None
        self.current_backup_host = None
        self.retry_count = 0
        self.max_retries = 4  # Maximum retry attempts per host
        
        # NEW: Enhanced tracking for speed/ETA and error recovery
        self.download_start_time = None
        self.last_speed_calculation = 0
        self.error_history = []  # Track recent errors for smart recovery
        self.consecutive_failures = 0
        self.last_successful_host = None
        self.download_session_stats = {
            'total_bytes': 0,
            'bytes_downloaded': 0,
            'average_speed': 0,
            'peak_speed': 0,
            'time_elapsed': 0,
            'eta_seconds': 0
        }

    def _format_eta(self, seconds: float) -> str:
        if not (0 <= seconds <= 3600 * 24 * 7): return "--:--"
        if seconds < 60: return f"{int(seconds)}s"
        if seconds < 3600: return f"{int(seconds // 60)}m {int(seconds % 60)}s"
        return f"{int(seconds // 3600)}h {int((seconds % 3600) // 60)}m"
    
    def _record_error(self, error_type: str, host_id: str, details: str = ""):
        """Record download errors for smart recovery analysis."""
        error_record = {
            'timestamp': time.time(),
            'type': error_type,
            'host_id': host_id,
            'details': details
        }
        self.error_history.append(error_record)
        
        # Keep only recent errors (last 5 minutes)
        cutoff_time = time.time() - 300  # 5 minutes
        self.error_history = [e for e in self.error_history if e['timestamp'] > cutoff_time]
        
        # Track consecutive failures
        if error_type in ['SSL', 'Connection', 'Timeout']:
            self.consecutive_failures += 1
        
        logger.log(f"Error recorded: {error_type} on {host_id} - {details}", "WARNING")
    
    def _analyze_error_patterns(self) -> Dict[str, Any]:
        """Analyze recent error patterns to suggest recovery strategies."""
        if not self.error_history:
            return {'strategy': 'normal', 'suggestion': 'Continue normal operation'}
        
        recent_errors = [e for e in self.error_history if e['timestamp'] > time.time() - 60]  # Last minute
        
        # Count error types
        error_counts = {}
        host_errors = {}
        for error in recent_errors:
            error_counts[error['type']] = error_counts.get(error['type'], 0) + 1
            host_errors[error['host_id']] = host_errors.get(error['host_id'], 0) + 1
        
        # Determine recovery strategy
        if error_counts.get('SSL', 0) >= 3:
            return {
                'strategy': 'dns_fix',
                'suggestion': 'Multiple SSL errors detected. Consider DNS configuration.',
                'action': 'offer_dns_fix'
            }
        elif error_counts.get('Connection', 0) >= 3:
            return {
                'strategy': 'network_check',
                'suggestion': 'Network connectivity issues detected.',
                'action': 'check_connectivity'
            }
        elif self.consecutive_failures >= 5:
            return {
                'strategy': 'cooldown',
                'suggestion': 'Multiple consecutive failures. Recommend brief pause.',
                'action': 'suggest_pause'
            }
        else:
            return {'strategy': 'normal', 'suggestion': 'Continue with current approach'}
    
    def _update_session_stats(self, bytes_downloaded: int, total_bytes: int):
        """Update download session statistics for detailed reporting."""
        current_time = time.time()
        
        if self.download_start_time is None:
            self.download_start_time = current_time
        
        self.download_session_stats['bytes_downloaded'] = bytes_downloaded
        self.download_session_stats['total_bytes'] = total_bytes
        self.download_session_stats['time_elapsed'] = current_time - self.download_start_time
        
        # Calculate speeds
        if self.download_session_stats['time_elapsed'] > 0:
            self.download_session_stats['average_speed'] = bytes_downloaded / self.download_session_stats['time_elapsed']
        
        # Calculate ETA
        if len(self.speed_buffer) > 0:
            current_speed = sum(self.speed_buffer) / len(self.speed_buffer)
            remaining_bytes = total_bytes - bytes_downloaded
            if current_speed > 0:
                self.download_session_stats['eta_seconds'] = remaining_bytes / current_speed
            
            # Track peak speed
            if current_speed > self.download_session_stats['peak_speed']:
                self.download_session_stats['peak_speed'] = current_speed

    def _download_chunk(self, url: str, start_byte: int, end_byte: int, output_path: Path, progress_path: Path, chunk_index: int) -> bool:
        headers = {'Range': f'bytes={start_byte}-{end_byte}'}
        
        for attempt in range(self.max_retries):
            self.pause_event.wait()
            if self.cancel_event.is_set(): return False
            
            # Aggressive timeout strategy: start fast, escalate moderately
            timeout = 6 if attempt == 0 else (8 if attempt == 1 else (10 if attempt == 2 else 12))
            
            try:
                with requests.get(url, headers=headers, stream=True, timeout=timeout) as r:
                    r.raise_for_status()
                    with open(output_path, "r+b") as f:
                        f.seek(start_byte)
                        chunk_size_downloaded = 0
                        for chunk in r.iter_content(chunk_size=8192):
                            self.pause_event.wait()
                            if self.cancel_event.is_set(): return False
                            f.write(chunk)
                            chunk_size_downloaded += len(chunk)
                            
                            # Update total downloaded in real-time for smooth progress
                            with self.download_lock: 
                                self.total_downloaded += len(chunk)
                
                # Immediately flush progress to disk for resume reliability
                with progress_path.open("a", encoding='utf-8') as pf:
                    pf.write(f"{chunk_index}\n")
                return True
                
            except (requests.exceptions.HTTPError, requests.exceptions.SSLError, requests.exceptions.ConnectionError) as e:
                # Critical errors - fail immediately to trigger host switch
                if isinstance(e, requests.exceptions.HTTPError):
                    if e.response.status_code in [404, 403, 410]:  # File not found errors
                        logger.log(f"Chunk {chunk_index}: File not accessible on this host (HTTP {e.response.status_code}). Switching host immediately.", "ERROR")
                        self._record_error("HTTP", getattr(self, 'current_primary_host', 'unknown'), f"Status {e.response.status_code}")
                        return False
                    error_msg = f"HTTP {e.response.status_code}"
                    self._record_error("HTTP", getattr(self, 'current_primary_host', 'unknown'), error_msg)
                elif isinstance(e, requests.exceptions.SSLError):
                    error_msg = "SSL/TLS Error"
                    self._record_error("SSL", getattr(self, 'current_primary_host', 'unknown'), str(e))
                    # Immediate UI feedback for SSL/TLS errors to prevent appearance of being stuck
                    self.progress_queue.put({'type': Q_MSG.STATUS, 'message': f"⚠️ SSL/TLS error on chunk {chunk_index}, switching host..."})
                else:
                    error_msg = "Connection Refused"
                    self._record_error("Connection", getattr(self, 'current_primary_host', 'unknown'), str(e))
                    
                logger.log(f"Chunk {chunk_index}: Critical failure ({error_msg}). Will switch host after retries.", "ERROR")
                
                # For critical errors, only retry once quickly before switching host
                if attempt == 0:
                    time.sleep(0.3)  # Very short wait for immediate retry
                    continue
                else:
                    # Check for error patterns and suggest recovery
                    error_analysis = self._analyze_error_patterns()
                    if error_analysis['strategy'] != 'normal':
                        self.progress_queue.put({
                            'type': Q_MSG.DOWNLOAD_ERROR_RETRY,
                            'analysis': error_analysis,
                            'chunk_index': chunk_index
                        })
                    
                    # Immediate status update before returning failure
                    if isinstance(e, requests.exceptions.SSLError):
                        self.progress_queue.put({'type': Q_MSG.STATUS, 'message': f"❌ SSL/TLS errors, switching to backup host..."})
                    return False  # Switch host after 1 retry for critical errors
                
            except (requests.exceptions.Timeout, requests.exceptions.ReadTimeout) as e:
                # Timeout errors - more forgiving, allow more retries
                self._record_error("Timeout", getattr(self, 'current_primary_host', 'unknown'), f"Timeout after {timeout}s")
                logger.log(f"Chunk {chunk_index}: Timeout on attempt {attempt+1}/{self.max_retries} ({timeout}s): {type(e).__name__}", "WARNING")
                if self.cancel_event.is_set(): return False
                if attempt < self.max_retries - 1:
                    # Escalating wait times: 0.3s, 0.7s, 1.2s
                    wait_time = 0.3 + (attempt * 0.4)
                    time.sleep(wait_time)
                    
            except requests.RequestException as e:
                # Other network errors - moderate retry strategy
                logger.log(f"Chunk {chunk_index}: Network error on attempt {attempt+1}/{self.max_retries}: {type(e).__name__}", "WARNING")
                if self.cancel_event.is_set(): return False
                if attempt < self.max_retries - 1:
                    # Faster retry for network errors: 0.5s, 1.0s, 1.5s
                    wait_time = 0.5 + (attempt * 0.5)
                    time.sleep(wait_time)
                    
        logger.log(f"Chunk {chunk_index}: Failed after {self.max_retries} attempts. Switching to backup host.", "ERROR")
        return False

    def _test_host_parallel(self, link_info: Dict[str, str], results: List, index: int) -> None:
        """Test a single host in parallel and store results."""
        link = link_info['link']
        host_id = link_info['host_id']
        start_time = time.time()
        
        try:
            # Quick connection test with tight timeout
            response = requests.head(link, timeout=4, allow_redirects=True)
            response.raise_for_status()
            response_time = time.time() - start_time
            size = int(response.headers.get('content-length', 0))
            
            if size > 0:
                # Store performance metrics
                self.host_performance[host_id] = {
                    'response_time': response_time,
                    'size': size,
                    'success': True,
                    'last_test': time.time()
                }
                results[index] = {
                    'host_info': link_info,
                    'size': size,
                    'response_time': response_time,
                    'success': True
                }
                logger.log(f"✅ Host '{host_id}' responded in {response_time:.2f}s - {format_bytes(size)}", "INFO")
            else:
                results[index] = {'success': False, 'host_info': link_info, 'error': 'No content-length'}
                logger.log(f"❌ Host '{host_id}' returned no file size", "WARNING")
                
        except requests.RequestException as e:
            response_time = time.time() - start_time
            results[index] = {
                'success': False, 
                'host_info': link_info, 
                'error': str(e),
                'response_time': response_time
            }
            logger.log(f"❌ Host '{host_id}' failed in {response_time:.2f}s: {type(e).__name__}", "WARNING")

    def _get_remote_file_info(self, links: List[Dict[str, str]]) -> Tuple[int, Dict[str, str], Dict[str, str]]:
        """Smart host testing - optimized for single vs multi-host scenarios."""
        if not links:
            return 0, {}, {}
        
        # INTELLIGENT MODE DETECTION - Single host vs Multi-host behavior
        is_single_host_mode = len(links) == 1
        
        if is_single_host_mode:
            # SINGLE HOST MODE - Direct connection, no racing messages
            single_host = links[0]
            logger.log(f"📡 SINGLE HOST MODE: Connecting to {single_host['host_id']}...", "INFO")
            self.progress_queue.put({'type': Q_MSG.STATUS, 'message': f"📡 Connecting to {single_host['host_id']}..."})
            
            # Test the single host directly
            results = [None]
            self._test_host_parallel(single_host, results, 0)
            
            if results[0] and results[0].get('success'):
                host_result = results[0]
                host_info = host_result['host_info']
                
                logger.log(f"✅ Connected to {host_info['host_id']} ({host_result['response_time']:.2f}s)", "INFO")
                self.progress_queue.put({'type': Q_MSG.STATUS, 'message': f"✅ Connected to {host_info['host_id']}"})
                
                self.current_primary_host = host_info['host_id']
                self.current_backup_host = host_info['host_id']  # Same host as backup
                
                return host_result['size'], host_info, host_info
            else:
                logger.log(f"❌ Failed to connect to {single_host['host_id']}", "ERROR")
                self.progress_queue.put({'type': Q_MSG.STATUS, 'message': f"❌ Failed to connect to {single_host['host_id']}"})
                return 0, {}, {}
        else:
            # MULTI-HOST SMART MODE - Parallel racing for best performance
            logger.log(f"🚀 SMART PARALLEL TESTING: Racing {len(links)} hosts to find the fastest...", "INFO")
            self.progress_queue.put({'type': Q_MSG.STATUS, 'message': f"🏁 Racing {len(links)} hosts for fastest response..."})
            
            # Prepare parallel testing
            results = [None] * len(links)
            threads = []
            
            # Start all host tests simultaneously
            for i, link_info in enumerate(links):
                thread = threading.Thread(
                    target=self._test_host_parallel,
                    args=(link_info, results, i),
                    daemon=True
                )
                threads.append(thread)
                thread.start()
            
            # Show progress while waiting
            start_time = time.time()
            successful_hosts = []
            
            # Wait for all tests to complete with timeout
            for i, thread in enumerate(threads):
                thread.join(timeout=5)  # 5 second timeout per host
                
                # Update progress
                completed = i + 1
                self.progress_queue.put({
                    'type': Q_MSG.STATUS, 
                    'message': f"🔍 Testing progress: {completed}/{len(links)} hosts checked..."
                })
                
                # Check if we have a successful result
                if results[i] and results[i].get('success'):
                    successful_hosts.append(results[i])
            
            # Filter and sort successful hosts by response time
            successful_hosts = [r for r in results if r and r.get('success')]
            
            if not successful_hosts:
                logger.log("🚫 PARALLEL TEST FAILED: No hosts responded successfully!", "ERROR")
                self.progress_queue.put({'type': Q_MSG.STATUS, 'message': "❌ All hosts failed - check connection"})
                return 0, {}, {}
            
            # Sort by response time (fastest first)
            successful_hosts.sort(key=lambda x: x['response_time'])
            primary_host = successful_hosts[0]
            backup_host = successful_hosts[1] if len(successful_hosts) > 1 else successful_hosts[0]
            
            total_time = time.time() - start_time
            primary_info = primary_host['host_info']
            backup_info = backup_host['host_info']
            
            logger.log(f"🎯 WINNER: '{primary_info['host_id']}' ({primary_host['response_time']:.2f}s) | Backup: '{backup_info['host_id']}' ({backup_host['response_time']:.2f}s)", "INFO")
            logger.log(f"📊 Parallel test completed in {total_time:.2f}s - {len(successful_hosts)}/{len(links)} hosts available", "INFO")
            
            self.current_primary_host = primary_info['host_id']
            self.current_backup_host = backup_info['host_id']
            
            self.progress_queue.put({
                'type': Q_MSG.STATUS, 
                'message': f"🏆 Primary: {primary_info['host_id']} | Backup: {backup_info['host_id']}"
            })
            
            return primary_host['size'], primary_info, backup_info

    def download_file(self, links: List[Dict[str, str]], destination_folder: Path, output_filename: str) -> Optional[Tuple[Path, str]]:
        output_path = destination_folder / output_filename
        progress_path = output_path.with_suffix(output_path.suffix + '.progress')
        host_info_path = output_path.with_suffix(output_path.suffix + '.hostinfo')
        
        # INTELLIGENT MODE DETECTION for appropriate messaging
        is_single_host_mode = len(links) == 1
        selected_host_name = links[0]['host_id'] if is_single_host_mode else "multiple hosts"
        
        if is_single_host_mode:
            logger.log(f"� SINGLE HOST DOWNLOAD: Starting '{output_filename}' from {selected_host_name}", "INFO")
            self.progress_queue.put({'type': Q_MSG.STATUS, 'message': f"📱 Starting download from {selected_host_name}..."})
            self.progress_queue.put({'type': Q_MSG.OVERALL_STATUS, 'message': f"📡 Downloading {output_filename} from {selected_host_name}"})
        else:
            logger.log(f"🚀 SMART DOWNLOAD: Starting '{output_filename}' with {len(links)} available hosts", "INFO")
            self.progress_queue.put({'type': Q_MSG.STATUS, 'message': f"🔍 Initializing smart download for {output_filename}..."})
            self.progress_queue.put({'type': Q_MSG.OVERALL_STATUS, 'message': f"🧠 Smart host selection for {output_filename}"})

        # Smart host testing - optimized for single vs multi-host scenarios
        total_size, primary_host_info, backup_host_info = self._get_remote_file_info(links)
        if total_size == 0:
            if is_single_host_mode:
                raise ConnectionError(f"DOWNLOAD FAILED: Could not connect to {selected_host_name} for {output_filename}.")
            else:
                raise ConnectionError(f"SMART DOWNLOAD FAILED: No hosts responded for {output_filename} out of {len(links)} available hosts.")

        # Create optimized download order with intelligent fallback and progress-aware prioritization
        download_sequence = []
        
        # Check for existing progress to prioritize accordingly
        existing_progress_info = None
        if progress_path.exists() and output_path.exists() and host_info_path.exists():
            try:
                # Load previous download state
                previous_host_info = {}
                with host_info_path.open("r", encoding='utf-8') as hf:
                    for line in hf:
                        if line.strip():
                            key, value = line.strip().split('=', 1)
                            previous_host_info[key] = value
                
                previous_host_id = previous_host_info.get('host_id', 'unknown')
                previous_file_size = int(previous_host_info.get('file_size', '0'))
                current_size = output_path.stat().st_size if output_path.exists() else 0
                completion_percentage = (current_size / total_size * 100) if total_size > 0 and previous_file_size == total_size else 0
                
                if completion_percentage > 60:  # 60% threshold for smart resume
                    existing_progress_info = {
                        'host_id': previous_host_id,
                        'completion': completion_percentage,
                        'file_size_match': previous_file_size == total_size
                    }
                    logger.log(f"🔍 FOUND EXISTING PROGRESS: {completion_percentage:.1f}% from host '{previous_host_id}'", "INFO")
                    
            except Exception as e:
                logger.log(f"⚠️ Could not read existing progress: {e}", "WARNING")
        
        # Build download sequence with intelligent progress-aware prioritization
        if existing_progress_info and existing_progress_info['file_size_match']:
            # Smart host prioritization based on progress
            previous_host_id = existing_progress_info['host_id']
            completion = existing_progress_info['completion']
            
            # Find the host with existing progress
            existing_host = next((h for h in links if h['host_id'] == previous_host_id), None)
            
            if existing_host and completion > 60:
                # >60% downloaded - LOCK to this host as primary priority
                logger.log(f"🔒 HOST LOCK: '{previous_host_id}' has {completion:.1f}% progress - using as primary host", "INFO")
                download_sequence = [existing_host]
                
                # Add other hosts as backups only (will only be used if primary fails)
                for link_info in links:
                    if link_info['host_id'] != previous_host_id:
                        download_sequence.append(link_info)
                        
            elif existing_host and completion > 0:
                # Some progress but <60% - prefer this host but don't lock to it
                logger.log(f"🚀 PROGRESS PRIORITY: Using '{previous_host_id}' first ({completion:.1f}% already downloaded)", "INFO")
                download_sequence = [existing_host]
                
                # Add fastest host as second priority if different
                if primary_host_info['host_id'] != previous_host_id:
                    download_sequence.append(primary_host_info)
                if backup_host_info and backup_host_info['host_id'] != previous_host_id and backup_host_info != primary_host_info:
                    download_sequence.append(backup_host_info)
                    
                # Add remaining hosts
                for link_info in links:
                    if link_info not in download_sequence:
                        download_sequence.append(link_info)
            else:
                logger.log(f"⚠️ Host '{previous_host_id}' with progress not available, using speed priority", "WARNING")
                # Fall back to speed-based priority
                download_sequence = [primary_host_info]
                if backup_host_info and backup_host_info != primary_host_info:
                    download_sequence.append(backup_host_info)
                
                # Add remaining hosts as tertiary backups
                for link_info in links:
                    if link_info not in download_sequence:
                        download_sequence.append(link_info)
        else:
            # No significant progress or file size mismatch - use speed-based priority
            download_sequence = [primary_host_info]
            if backup_host_info and backup_host_info != primary_host_info:
                download_sequence.append(backup_host_info)
            
            # Add remaining hosts as tertiary backups
            for link_info in links:
                if link_info not in download_sequence:
                    download_sequence.append(link_info)

        logger.log(f"📋 OPTIMIZED DOWNLOAD SEQUENCE: {[h['host_id'] for h in download_sequence[:3]]}{'...' if len(download_sequence) > 3 else ''}", "INFO")

        # Smart resume logic with ENHANCED same-host resume and intelligent host switching
        completed_chunks = set()
        current_host_id = primary_host_info['host_id']
        
        if progress_path.exists() and output_path.exists() and host_info_path.exists():
            logger.log("🔍 Checking resume compatibility...", "INFO")
            try:
                # Load previous download state
                previous_host_info = {}
                try:
                    with host_info_path.open("r", encoding='utf-8') as hf:
                        for line in hf:
                            if line.strip():
                                key, value = line.strip().split('=', 1)
                                previous_host_info[key] = value
                except Exception:
                    previous_host_info = {}
                
                previous_host_id = previous_host_info.get('host_id', 'unknown')
                previous_file_size = int(previous_host_info.get('file_size', '0'))
                current_size = output_path.stat().st_size if output_path.exists() else 0
                completion_percentage = (current_size / total_size * 100) if total_size > 0 else 0
                
                # ENHANCED RESUME LOGIC - Your requirements implemented:
                # 1. Resume from any size if same host
                # 2. Only switch hosts if >60% progress and current host fails  
                # 3. Always use fastest host but delete partial files when switching
                
                if previous_host_id == current_host_id and previous_file_size == total_size:
                    # SAME HOST RESUME - Resume from any size (no minimum threshold)
                    if current_size > 0 and current_size <= total_size:
                        try:
                            with progress_path.open("r", encoding='utf-8') as pf:
                                completed_chunks = {int(line) for line in pf if line.strip()}
                            logger.log(f"✅ SAME HOST RESUME: Continuing from {previous_host_id} with {completion_percentage:.1f}% progress", "INFO")
                            self.progress_queue.put({'type': Q_MSG.STATUS, 'message': f"⚡ Resuming from {current_host_id} ({completion_percentage:.1f}% done)..."})
                        except (ValueError, IOError):
                            logger.log("⚠️ Progress file corrupted, restarting from beginning", "WARNING")
                            self._cleanup_partial_files(output_path, progress_path, host_info_path)
                    else:
                        logger.log(f"⚠️ Invalid file size {current_size}, restarting", "WARNING")
                        self._cleanup_partial_files(output_path, progress_path, host_info_path)
                        
                elif previous_host_id != current_host_id:
                    # DIFFERENT HOST - Smart decision based on progress and host availability
                    
                    if completion_percentage > 60:
                        # >60% downloaded - Try to continue with original host if available (HOST LOCK)
                        original_host = next((h for h in download_sequence if h['host_id'] == previous_host_id), None)
                        
                        if original_host:
                            logger.log(f"� HOST LOCK ACTIVATED: {completion_percentage:.1f}% from '{previous_host_id}' - prioritizing original host", "INFO")
                            # Move original host to front to prioritize it
                            if download_sequence[0]['host_id'] != previous_host_id:
                                download_sequence.remove(original_host)
                                download_sequence.insert(0, original_host)
                            current_host_id = previous_host_id
                            
                            try:
                                with progress_path.open("r", encoding='utf-8') as pf:
                                    completed_chunks = {int(line) for line in pf if line.strip()}
                                self.progress_queue.put({'type': Q_MSG.STATUS, 'message': f"� Host locked: Resuming from {previous_host_id} ({completion_percentage:.1f}%)..."})
                            except (ValueError, IOError):
                                logger.log("⚠️ Progress file corrupted but preserving host priority", "WARNING")
                                self._cleanup_partial_files(output_path, progress_path, host_info_path)
                        else:
                            # Original host not available - delete partial file and use fastest host
                            logger.log(f"⚠️ HOST SWITCH REQUIRED: Original host '{previous_host_id}' unavailable, deleting partial file", "WARNING")
                            self.progress_queue.put({'type': Q_MSG.STATUS, 'message': f"🔄 Host switched: Deleting partial file and using fastest host..."})
                            self._cleanup_partial_files(output_path, progress_path, host_info_path)
                    else:
                        # <60% downloaded - Always use fastest host, delete partial file
                        logger.log(f"🚀 OPTIMAL HOST SWITCH: {completion_percentage:.1f}% from '{previous_host_id}' → '{current_host_id}' (faster)", "INFO")
                        self.progress_queue.put({'type': Q_MSG.STATUS, 'message': f"🚀 Switching to faster host {current_host_id}, deleting partial file..."})
                        self._cleanup_partial_files(output_path, progress_path, host_info_path)
                        
                elif previous_file_size != total_size:
                    # File size changed - Always restart
                    logger.log(f"🔄 SIZE CHANGE: File size changed from {previous_file_size} to {total_size}, restarting", "WARNING")
                    self.progress_queue.put({'type': Q_MSG.STATUS, 'message': f"🔄 File size changed, restarting download..."})
                    self._cleanup_partial_files(output_path, progress_path, host_info_path)
                    
            except (ValueError, IOError, OSError) as e:
                logger.log(f"⚠️ Resume state corrupted, restarting fresh: {e}", "WARNING")
                self._cleanup_partial_files(output_path, progress_path, host_info_path)

        # Initialize fresh download if needed
        if not output_path.exists():
            logger.log(f"🆕 FRESH DOWNLOAD: Preparing {output_filename} ({format_bytes(total_size)})", "INFO")
            with open(output_path, "wb") as f: 
                f.truncate(total_size)
            completed_chunks.clear()
            
            # Create host tracking file
            self._create_host_info_file(host_info_path, current_host_id, total_size)

        # Prepare chunk structure
        chunk_size = Constants.DOWNLOAD_CHUNK_SIZE
        num_chunks = max(1, (total_size + chunk_size - 1) // chunk_size)
        all_chunks = [{'index': i, 'start': i * chunk_size, 'end': min((i + 1) * chunk_size - 1, total_size - 1)} for i in range(num_chunks)]

        # INTELLIGENT MULTI-HOST DOWNLOAD with smart failover
        for attempt, host_info in enumerate(download_sequence):
            if self.cancel_event.is_set(): 
                break
                
            host_id = host_info['host_id']
            link = host_info['link']
            
            logger.log(f"📡 DOWNLOAD ATTEMPT {attempt + 1}/{len(download_sequence)}: Using host '{host_id}'", "INFO")
            
            if attempt > 0:
                # Switching hosts due to failure - implement smart host preservation logic
                self.progress_queue.put({
                    'type': Q_MSG.STATUS, 
                    'message': f"🔄 Switching to host {host_id} (attempt {attempt + 1})..."
                })
                
                # SMART HOST SWITCHING LOGIC:
                # 1. Resume from any size if continuing with same host
                # 2. If >60% downloaded from previous host, try to stick with that host unless it fails
                # 3. Only delete partial files when actually switching to different host
                should_clean = False
                
                if existing_progress_info:
                    previous_host_id = existing_progress_info['host_id']
                    completion_percentage = existing_progress_info['completion']
                    current_host_id = host_id
                    
                    if previous_host_id == current_host_id:
                        # Same host - ALWAYS try to resume from any size
                        logger.log(f"🔄 SAME HOST RESUME: Continuing with '{host_id}' from {completion_percentage:.1f}%", "INFO")
                        should_clean = False
                        
                        # Verify we can still resume
                        try:
                            with progress_path.open("r", encoding='utf-8') as pf:
                                completed_chunks = {int(line) for line in pf if line.strip()}
                            if len(completed_chunks) > 0:
                                logger.log(f"✅ SAME HOST RESUME: {len(completed_chunks)} chunks already downloaded", "INFO")
                            else:
                                logger.log("⚠️ No valid chunks found, will restart with same host", "WARNING")
                                should_clean = True
                        except Exception as e:
                            logger.log(f"⚠️ Could not verify resume state: {e}", "WARNING")
                            should_clean = True
                    else:
                        # Different host - check if we should preserve >60% progress
                        if completion_percentage > 60:
                            # >60% downloaded - try to stick with previous host first
                            previous_host_available = next((h for h in download_sequence if h['host_id'] == previous_host_id), None)
                            if previous_host_available and previous_host_id != current_host_id:
                                logger.log(f"🔒 HOST LOCK: {completion_percentage:.1f}% done with '{previous_host_id}', trying to continue with it instead of switching to '{current_host_id}'", "INFO")
                                # Skip this host and try to continue with the previous one
                                continue
                            else:
                                # Previous host not available anymore, switch and delete
                                logger.log(f"🗑️ FORCED SWITCH: Previous host '{previous_host_id}' unavailable, deleting {completion_percentage:.1f}% progress and switching to '{current_host_id}'", "WARNING")
                                should_clean = True
                        else:
                            # <60% downloaded - normal switch, delete partial file
                            logger.log(f"🧹 CLEAN SWITCH: Only {completion_percentage:.1f}% done, switching from '{previous_host_id}' to '{current_host_id}'", "INFO")
                            should_clean = True
                else:
                    # No existing progress info - start fresh
                    should_clean = True
                
                if should_clean:
                    # Delete partial files when switching hosts
                    logger.log(f"🧹 CLEANING: Removing partial files before switching to host '{host_id}'", "INFO")
                    self._cleanup_partial_files(output_path, progress_path, host_info_path)
                    completed_chunks.clear()
                    
                    # Verify new host has correct file size
                    if not self._verify_host_file_size(link, total_size, host_id):
                        continue
                    
                    # Recreate files for new host
                    with open(output_path, "wb") as f: 
                        f.truncate(total_size)
                    self._create_host_info_file(host_info_path, host_id, total_size)
                else:
                    # Just update the host info file for resume (same host)
                    self._create_host_info_file(host_info_path, host_id, total_size)
                
                # Brief pause before retry (escalating)
                retry_delay = min(0.5 + (attempt * 0.3), 2.0)  # 0.5s, 0.8s, 1.1s, max 2s
                time.sleep(retry_delay)

            try:
                # Execute download with current host
                success = self._execute_download_with_host(
                    link, host_id, output_path, progress_path, 
                    all_chunks, completed_chunks, total_size, output_filename
                )
                
                if success:
                    logger.log(f"✅ DOWNLOAD SUCCESS: '{output_filename}' completed via host '{host_id}'", "INFO")
                    return output_path, host_id
                else:
                    # Download failed, try next host
                    logger.log(f"❌ HOST FAILED: '{host_id}' failed download, trying next host...", "WARNING")
                    continue
                    
            except Exception as e:
                logger.log(f"💥 HOST EXCEPTION: '{host_id}' encountered error: {e}", "ERROR")
                continue

        # All hosts failed - ensure UI can recover
        logger.log(f"🚫 COMPLETE FAILURE: All {len(download_sequence)} hosts failed for '{output_filename}'", "ERROR")
        
        # Send immediate status update to prevent UI lock
        self.progress_queue.put({'type': Q_MSG.STATUS, 'message': f"❌ All {len(download_sequence)} hosts failed for {output_filename}"})
        
        # Force progress update to show failure state
        self.progress_queue.put({'type': Q_MSG.PROGRESS, 'value': 0})
        
        return None

    def _cleanup_partial_files(self, output_path: Path, progress_path: Path, host_info_path: Path):
        """Clean up partial download files."""
        for path in [output_path, progress_path, host_info_path]:
            if path.exists():
                path.unlink(missing_ok=True)

    def _create_host_info_file(self, host_info_path: Path, host_id: str, total_size: int):
        """Create host tracking file."""
        with host_info_path.open("w", encoding='utf-8') as hf:
            hf.write(f"host_id={host_id}\n")
            hf.write(f"file_size={total_size}\n")
            hf.write(f"start_time={time.time()}\n")

    def _verify_host_file_size(self, link: str, expected_size: int, host_id: str) -> bool:
        """Verify host has correct file size when switching."""
        try:
            response = requests.head(link, timeout=4, allow_redirects=True)
            response.raise_for_status()
            actual_size = int(response.headers.get('content-length', 0))
            
            size_tolerance = min(expected_size * 0.01, 1024 * 1024)  # 1% or 1MB tolerance
            size_diff = abs(actual_size - expected_size)
            
            if size_diff > size_tolerance:
                logger.log(f"❌ Host '{host_id}' has wrong file size: {format_bytes(actual_size)} vs expected {format_bytes(expected_size)}", "ERROR")
                return False
            elif size_diff > 0:
                logger.log(f"⚠️ Host '{host_id}' has slight size difference: {format_bytes(size_diff)}", "WARNING")
            
            return True
            
        except requests.RequestException as e:
            logger.log(f"❌ Cannot verify size for host '{host_id}': {e}", "ERROR")
            return False

    def _execute_download_with_host(self, link: str, host_id: str, output_path: Path, 
                                  progress_path: Path, all_chunks: List, completed_chunks: set, 
                                  total_size: int, output_filename: str) -> bool:
        """Execute the actual download with detailed progress tracking."""
        chunks_to_download = [c for c in all_chunks if c['index'] not in completed_chunks]
        if not chunks_to_download:
            return True  # Already complete

        # Enhanced UI feedback
        self.progress_queue.put({
            'type': Q_MSG.STATUS, 
            'message': f"⬇️ Downloading from {host_id} | {len(chunks_to_download)} chunks remaining"
        })
        self.progress_queue.put({
            'type': Q_MSG.OVERALL_STATUS, 
            'message': f"📥 Active download: {output_filename} from {host_id}"
        })

        # Initialize download tracking
        initial_downloaded_size = sum((c['end'] - c['start'] + 1) for c in all_chunks if c['index'] in completed_chunks)
        with self.download_lock: 
            self.total_downloaded = initial_downloaded_size
        self.speed_buffer.clear()
        last_update_time, last_update_size = time.time(), self.total_downloaded

        # Show initial progress
        initial_progress = (self.total_downloaded / total_size) * 100 if total_size > 0 else 0
        initial_progress = min(initial_progress, 100.0)
        
        if initial_progress > 0:
            self.progress_queue.put({
                'type': Q_MSG.STATUS, 
                'message': f"⬇️ Resuming | {initial_progress:.1f}% | {host_id}"
            })
            self.progress_queue.put({'type': Q_MSG.PROGRESS, 'value': initial_progress})
        else:
            self.progress_queue.put({
                'type': Q_MSG.STATUS, 
                'message': f"⬇️ Starting fresh | 0% | {host_id}"
            })
            self.progress_queue.put({'type': Q_MSG.PROGRESS, 'value': 0})

        # Multi-threaded download with REAL-TIME progress tracking
        failed_chunks = []
        chunk_futures = {}
        
        with ThreadPoolExecutor(max_workers=Constants.DOWNLOAD_THREADS) as executor:
            # Submit all chunks
            for chunk in chunks_to_download:
                if self.cancel_event.is_set(): 
                    break
                future = executor.submit(
                    self._download_chunk, link, chunk['start'], chunk['end'], 
                    output_path, progress_path, chunk['index']
                )
                chunk_futures[future] = chunk

            # REAL-TIME progress monitoring with continuous updates
            completed_count = 0
            total_chunks = len(chunks_to_download)
            
            # Start continuous progress monitoring thread
            def real_time_progress_monitor():
                """Monitor progress in real-time with frequent updates."""
                last_update = time.time()
                last_size = self.total_downloaded
                
                while chunk_futures and not self.cancel_event.is_set():
                    self.pause_event.wait()  # Respect pause state
                    
                    current_time = time.time()
                    current_size = self.total_downloaded
                    time_diff = current_time - last_update
                    
                    # Update UI every 200ms for smooth progress
                    if time_diff >= 0.2:
                        with self.download_lock:
                            progress = (current_size / total_size) * 100 if total_size > 0 else 0
                            progress = min(progress, 100.0)
                            
                            # Calculate real-time speed
                            size_diff = current_size - last_size
                            instant_speed = size_diff / time_diff if time_diff > 0 else 0
                            
                            # Update speed buffer for smoothing
                            if instant_speed > 0:
                                self.speed_buffer.append(instant_speed)
                            
                            avg_speed = sum(self.speed_buffer) / len(self.speed_buffer) if self.speed_buffer else 0
                            remaining_bytes = total_size - current_size
                            eta = remaining_bytes / avg_speed if avg_speed > 0 else 0
                            
                            # Update session statistics
                            self._update_session_stats(current_size, total_size)
                            
                            # Enhanced status with more details
                            if not self.pause_event.is_set():
                                status_msg = f"⏸️ PAUSED | {progress:.1f}% | {format_bytes(avg_speed)}/s | Host: {host_id}"
                            else:
                                chunks_remaining = len(chunk_futures)
                                # Enhanced display with peak speed and session stats
                                peak_speed_str = f"Peak: {format_bytes(self.download_session_stats['peak_speed'])}/s" if self.download_session_stats['peak_speed'] > 0 else ""
                                status_msg = f"⬇️ {host_id} | {progress:.1f}% | {format_bytes(avg_speed)}/s | ETA: {self._format_eta(eta)} | {chunks_remaining} chunks"
                            
                            # Send enhanced real-time updates
                            self.progress_queue.put({'type': Q_MSG.STATUS, 'message': status_msg})
                            self.progress_queue.put({'type': Q_MSG.PROGRESS, 'value': progress})
                            
                            # Send detailed speed/ETA information for UI enhancement
                            self.progress_queue.put({
                                'type': Q_MSG.DOWNLOAD_SPEED,
                                'current_speed': avg_speed,
                                'peak_speed': self.download_session_stats['peak_speed'],
                                'average_speed': self.download_session_stats['average_speed'],
                                'eta_seconds': eta,
                                'eta_formatted': self._format_eta(eta),
                                'time_elapsed': self.download_session_stats['time_elapsed'],
                                'bytes_remaining': remaining_bytes,
                                'progress_percent': progress
                            })
                            
                            last_update = current_time
                            last_size = current_size
                    
                    time.sleep(0.1)  # Check every 100ms for responsiveness
            
            # Start real-time monitoring
            monitor_thread = threading.Thread(target=real_time_progress_monitor, daemon=True)
            monitor_thread.start()
            
            # Process completed chunks as they finish
            for future in as_completed(chunk_futures):
                if self.cancel_event.is_set(): 
                    break
                    
                chunk = chunk_futures.pop(future)  # Remove from active futures
                try:
                    success = future.result()
                    if success:
                        completed_count += 1
                        completed_chunks.add(chunk['index'])
                        
                        # Immediate progress update when chunk completes
                        with self.download_lock:
                            progress = (self.total_downloaded / total_size) * 100 if total_size > 0 else 0
                            progress = min(progress, 100.0)
                        
                        # Quick update for chunk completion
                        chunks_remaining = len(chunk_futures)
                        if chunks_remaining > 0:
                            self.progress_queue.put({
                                'type': Q_MSG.STATUS, 
                                'message': f"⬇️ {host_id} | {progress:.1f}% | Chunk {completed_count}/{total_chunks} | {chunks_remaining} remaining"
                            })
                        
                    else:
                        # Chunk failed
                        failed_chunks.append(chunk)
                        logger.log(f"⚠️ Chunk {chunk['index']} failed from host '{host_id}'", "WARNING")
                        
                except Exception as e:
                    failed_chunks.append(chunk)
                    logger.log(f"💥 Chunk {chunk['index']} exception from host '{host_id}': {e}", "ERROR")

        # Check download success
        if self.cancel_event.is_set():
            return False
            
        if failed_chunks:
            failure_rate = len(failed_chunks) / total_chunks * 100
            logger.log(f"⚠️ Host '{host_id}' had {len(failed_chunks)}/{total_chunks} failed chunks ({failure_rate:.1f}%)", "WARNING")
            
            # Critical failure detection - if too many SSL/TLS errors, fail immediately
            ssl_errors = sum(1 for chunk in failed_chunks if any("SSL/TLS Error" in str(e) for e in [chunk.get('error', '')]))
            critical_failure_rate = ssl_errors / total_chunks * 100 if total_chunks > 0 else 0
            
            # If failure rate is too high, abandon this host
            if failure_rate > 20:  # More than 20% failed
                if critical_failure_rate > 10:  # SSL/TLS errors are critical
                    logger.log(f"❌ Host '{host_id}' has critical SSL/TLS failure rate ({critical_failure_rate:.1f}%), abandoning immediately", "ERROR")
                    self.progress_queue.put({'type': Q_MSG.STATUS, 'message': f"❌ Critical SSL/TLS errors from {host_id}, switching..."})
                    return False
                else:
                    logger.log(f"❌ Host '{host_id}' failure rate too high ({failure_rate:.1f}%), switching host", "ERROR")
                    self.progress_queue.put({'type': Q_MSG.STATUS, 'message': f"❌ Host {host_id} failed, switching..."})
                    return False
            else:
                # Retry failed chunks once, but not SSL/TLS errors
                retryable_chunks = [chunk for chunk in failed_chunks if not any("SSL/TLS Error" in str(e) for e in [chunk.get('error', '')])]
                if retryable_chunks:
                    logger.log(f"🔄 Retrying {len(retryable_chunks)} non-critical failed chunks from host '{host_id}'", "INFO")
                    self.progress_queue.put({'type': Q_MSG.STATUS, 'message': f"🔄 Retrying {len(retryable_chunks)} chunks from {host_id}..."})
                    
                    for chunk in retryable_chunks[:5]:  # Limit retries to avoid infinite loops
                        if self.cancel_event.is_set():
                            break
                        success = self._download_chunk(link, chunk['start'], chunk['end'], output_path, progress_path, chunk['index'])
                        if success:
                            completed_chunks.add(chunk['index'])
                        else:
                            logger.log(f"❌ Final retry failed for chunk {chunk['index']} from host '{host_id}'", "ERROR")
                            self.progress_queue.put({'type': Q_MSG.STATUS, 'message': f"❌ Final retry failed for chunk {chunk['index']}"})
                            return False
                
                # If SSL/TLS errors remain, fail
                if ssl_errors > 0:
                    logger.log(f"❌ {ssl_errors} SSL/TLS errors cannot be retried, host '{host_id}' failed", "ERROR")
                    self.progress_queue.put({'type': Q_MSG.STATUS, 'message': f"❌ SSL/TLS errors on {host_id}, cannot continue"})
                    return False

        # Final verification
        final_chunks_to_download = [c for c in all_chunks if c['index'] not in completed_chunks]
        if final_chunks_to_download:
            logger.log(f"❌ Download incomplete: {len(final_chunks_to_download)} chunks still missing from host '{host_id}'", "ERROR")
            return False

        # Success!
        self.progress_queue.put({'type': Q_MSG.STATUS, 'message': f"✅ Download complete from {host_id}"})
        self.progress_queue.put({'type': Q_MSG.PROGRESS, 'value': 100})
        return True

class Extractor:
    @staticmethod
    def find_7zip_executable() -> Optional[str]:
        base_path = getattr(sys, '_MEIPASS', Path(__file__).resolve().parent); bundled_exe_path = Path(base_path) / "7z.exe"
        if bundled_exe_path.exists(): return str(bundled_exe_path)
        logger.log("Bundled 7-Zip not found. Searching system...", "WARNING")
        registry_paths = [ (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\7-Zip"), (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node\7-Zip") ]
        for hive, key_path in registry_paths:
            try:
                with winreg.OpenKey(hive, key_path) as key:
                    path, _ = winreg.QueryValueEx(key, "Path"); exe = Path(path) / "7z.exe"
                    if exe.exists(): logger.log(f"Found 7-Zip in registry: {exe}", "INFO"); return str(exe)
            except FileNotFoundError: continue
        exe = shutil.which("7z");
        if exe: logger.log(f"Found 7-Zip in system PATH: {exe}", "INFO"); return str(exe)
        logger.log("7-Zip executable could not be found anywhere.", "CRITICAL"); return None

    def extract_archive(self, archive_path: Path, dest_dir: Path, progress_queue: queue.Queue, cancel_event: threading.Event) -> None:
        seven_zip_exe = self.find_7zip_executable()
        if not seven_zip_exe:
            raise FileNotFoundError("7-Zip executable not found. Please place 7z.exe in the application folder.")
        command = [seven_zip_exe, 'x', str(archive_path), f'-o{dest_dir}', '-y']
        logger.log(f"Executing asynchronous extraction: {' '.join(command)}", "INFO")
        progress_queue.put({'type': Q_MSG.PROGRESS_MODE, 'mode': 'indeterminate'})
        proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, creationflags=subprocess.CREATE_NO_WINDOW)
        while proc.poll() is None:
            if cancel_event.is_set():
                proc.terminate()
                try:
                    proc.wait(timeout=3.0)  # Give it 3 seconds to terminate gracefully
                except subprocess.TimeoutExpired:
                    proc.kill()  # Force kill if it doesn't terminate
                    logger.log("Extraction process force killed", "WARNING")
                logger.log("Extraction cancelled by user.", "INFO")
                raise InterruptedError("Extraction cancelled.")
            time.sleep(0.2)
        progress_queue.put({'type': Q_MSG.PROGRESS_MODE, 'mode': 'determinate'})
        stdout, stderr = proc.communicate()
        if proc.returncode != 0:
            error_details = stderr or stdout or "Unknown 7-Zip error."
            logger.log(f"Extraction failed for '{archive_path.name}': {error_details}", "ERROR")
            raise RuntimeError(f"Extraction failed: {error_details}")
        logger.log(f"Successfully extracted '{archive_path.name}'.", "INFO")

    def install_files(self, source_dir: Path, game_dir: Path, progress_queue: queue.Queue, cancel_event: threading.Event) -> None:
        logger.log(f"Preparing to install files from '{source_dir}' to '{game_dir}'.", "INFO")
        progress_queue.put({'type': Q_MSG.STATUS, 'message': "Analyzing patch files..."})
        files_to_copy = []
        total_size = 0
        source_root = next((Path(root) for root, _, files in os.walk(source_dir) if Constants.GAME_EXECUTABLE in files), source_dir)
        logger.log(f"Determined effective source root for copy: {source_root}", "INFO")

        # Security: Resolve absolute paths to prevent path traversal
        game_dir_resolved = game_dir.resolve()
        source_root_resolved = source_root.resolve()

        for root, _, files in os.walk(source_root):
            if cancel_event.is_set(): 
                raise InterruptedError("Installation cancelled during analysis.")
            for file in files:
                src_path = Path(root) / file
                try:
                    rel_path = src_path.relative_to(source_root)
                    dest_path = game_dir / rel_path
                    
                    # Security: Validate destination path to prevent path traversal
                    dest_path_resolved = dest_path.resolve()
                    if not str(dest_path_resolved).startswith(str(game_dir_resolved)):
                        logger.log(f"SECURITY: Skipping file with suspicious path: {rel_path}", "WARNING")
                        continue
                    
                    # Additional security: Check for dangerous file extensions
                    if dest_path.suffix.lower() in ['.exe', '.bat', '.cmd', '.scr', '.com', '.pif'] and dest_path.name != Constants.GAME_EXECUTABLE:
                        logger.log(f"SECURITY: Skipping potentially dangerous file: {dest_path.name}", "WARNING")
                        continue
                    
                    file_size = src_path.stat().st_size
                    files_to_copy.append({'src': src_path, 'dest': dest_path, 'size': file_size})
                    total_size += file_size
                    
                except (ValueError, FileNotFoundError) as e:
                    logger.log(f"File analysis error for {src_path}: {e}. Skipping.", "WARNING")

        logger.log(f"Analysis complete. Found {len(files_to_copy)} files to install, totaling {format_bytes(total_size)}.", "INFO")
        copied_size = 0
        last_update_time = time.time()

        for i, file_info in enumerate(files_to_copy):
            if cancel_event.is_set(): 
                raise InterruptedError("Installation cancelled by user.")
            
            try:
                # Ensure parent directory exists
                file_info['dest'].parent.mkdir(parents=True, exist_ok=True)
                
                # Copy with verification
                shutil.copy2(file_info['src'], file_info['dest'])
                copied_size += file_info['size']
                
                # Update progress
                current_time = time.time()
                if current_time - last_update_time > 0.05:
                    progress = (copied_size / total_size) * 100 if total_size > 0 else 100
                    progress_queue.put({'type': Q_MSG.PROGRESS, 'value': progress})
                    progress_queue.put({'type': Q_MSG.STATUS, 'message': f"Copying: {file_info['dest'].name}"})
                    last_update_time = current_time
                    
            except (IOError, OSError) as e:
                logger.log(f"Failed to copy {file_info['src']} to {file_info['dest']}: {e}", "ERROR")
                raise RuntimeError(f"Installation failed: Could not copy {file_info['dest'].name}")
        
        logger.log("All files installed successfully.", "INFO")

class GameManager:
    """Manages game-specific operations like version checking, launching, and save backups."""
    def __init__(self, game_dir: str): self.game_dir = Path(game_dir) if game_dir else None
    def check_version(self) -> Optional[str]:
        if not self.game_dir: return None
        version_file = self.game_dir / "version.txt"
        if not version_file.exists(): logger.log(f"version.txt not found in {self.game_dir}", "WARNING"); return "NOT_FOUND"
        try:
            content = version_file.read_text().strip(); parts = content.split('.')
            if len(parts) >= 3: version = parts[2].split()[0]; logger.log(f"Detected game version: v{version}", "INFO"); return version
            else: logger.log(f"Invalid version format in version.txt: {content}", "WARNING"); return "INVALID_FORMAT"
        except IOError as e: logger.log(f"Error reading version.txt: {e}", "ERROR"); return "READ_ERROR"
    def launch_game(self) -> Optional[str]:
        if not self.game_dir: return "Game directory not set."
        exe_path = self.game_dir / Constants.GAME_EXECUTABLE
        if not exe_path.exists(): return f"{Constants.GAME_EXECUTABLE} not found in the selected directory."
        try: subprocess.Popen([str(exe_path)], cwd=str(self.game_dir)); logger.log("Game launched successfully.", "INFO"); return None
        except OSError as e: logger.log(f"Failed to launch game: {e}", "ERROR"); return f"Failed to launch game: {e}"
    def backup_saved_games(self) -> str:
        saved_games_path = Path.home() / "Saved Games" / "Cricket 24"
        if not saved_games_path.exists(): msg = f"Saved games folder not found at: {saved_games_path}"; logger.log(msg, "WARNING"); raise FileNotFoundError(msg)
        backup_dir = saved_games_path.parent / "Cricket 26 Backups"; backup_dir.mkdir(exist_ok=True)
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        backup_zip_path = backup_dir / f"Cricket26_Save_{timestamp}.zip"
        shutil.make_archive(str(backup_zip_path.with_suffix('')), 'zip', str(saved_games_path))
        logger.log(f"Backup created successfully: {backup_zip_path}", "INFO"); return f"Backup complete: {backup_zip_path}"
    def restore_backup(self, backup_zip_path_str: str) -> str:
        backup_zip_path = Path(backup_zip_path_str)
        saved_games_path = Path.home() / "Saved Games" / "Cricket 26"
        saved_games_parent = saved_games_path.parent
        with tempfile.TemporaryDirectory(prefix="c26-restore-", dir=saved_games_parent) as temp_restore_dir:
            logger.log(f"Unpacking backup '{backup_zip_path.name}' to a temporary location...", "INFO")
            try:
                shutil.unpack_archive(backup_zip_path, temp_restore_dir)
                logger.log("Unpacking successful.", "INFO")
            except Exception as e:
                logger.log(f"CRITICAL: Failed to unpack the backup archive '{backup_zip_path.name}'. Details: {e}", "ERROR")
                raise RuntimeError(f"Could not restore backup. The archive file might be corrupted.\nDetails: {e}")
            unpacked_source_dir = Path(temp_restore_dir) / "Cricket 26"
            if not unpacked_source_dir.exists():
                logger.log("CRITICAL: Backup archive has an unexpected structure. Expected a 'Cricket 26' folder inside.", "ERROR")
                raise ValueError("Backup archive has an unexpected structure. Cannot proceed with restore.")
            original_data_temp_name = None
            if saved_games_path.exists():
                original_data_temp_name = saved_games_path.with_name(f"Cricket 26_pre-restore_{int(time.time())}")
                logger.log(f"Temporarily renaming current save data to '{original_data_temp_name.name}'...", "INFO")
                saved_games_path.rename(original_data_temp_name)
            try:
                logger.log("Moving new data into place...", "INFO")
                unpacked_source_dir.rename(saved_games_path)
            except Exception as e:
                logger.log(f"CRITICAL: Failed to move new data into place: {e}. Attempting rollback.", "CRITICAL")
                if original_data_temp_name and original_data_temp_name.exists():
                    logger.log("Attempting to roll back by restoring original save data...", "INFO")
                    original_data_temp_name.rename(saved_games_path)
                    logger.log("Rollback successful. Your original save data is safe.", "INFO")
                    raise RuntimeError(f"A critical error occurred while finalizing the restore.\n\nYour original save data has been automatically restored.\nPlease check the log for details about the failure: {e}")
                else:
                    logger.log("CRITICAL: Rollback failed. Original data backup could not be found.", "CRITICAL")
                    raise RuntimeError("A critical error occurred and the automatic rollback FAILED. Please check your 'Saved Games' folder for a '_pre-restore_' backup.")

            if original_data_temp_name and original_data_temp_name.exists():
                logger.log("Restore complete. Cleaning up old save data...", "INFO")
                shutil.rmtree(original_data_temp_name)
        logger.log(f"Successfully restored backup from: {backup_zip_path.name}", "INFO")
        return f"Successfully restored backup:\n{backup_zip_path.name}"

class UpdateWorkflow:
    """Encapsulates the entire multi-step update process."""
    def __init__(self, game_dir: str, cache_dir: Path, updates: List, data: Dict, queue: queue.Queue, cancel: threading.Event, pause: threading.Event, verify: bool, decision_queue: queue.Queue):
        self.game_dir, self.cache_dir = Path(game_dir), cache_dir; self.updates, self.data = updates, data
        self.progress_queue, self.cancel_event, self.pause_event, self.verify_checksums = queue, cancel, pause, verify
        self.decision_queue = decision_queue
        self.downloader = ConcurrentDownloader(self.progress_queue, self.cancel_event, self.pause_event)
        self.extractor = Extractor()

    def run(self):
        logger.log("Update workflow started.", "INFO")
        # Immediately update UI to show workflow has started
        self.progress_queue.put({'type': Q_MSG.OVERALL_STATUS, 'message': "Initializing update..."})
        self.progress_queue.put({'type': Q_MSG.STATUS, 'message': "Starting update process..."})
        downloaded_files = []
        
        # Check if using sequential update system
        schema_version = self.data.get('metadata', {}).get('schema_version', '1.0')
        supports_sequential = self.data.get('metadata', {}).get('supports_sequential_updates', False)
        is_sequential = schema_version == '2.0' or supports_sequential
        
        try:
            if self.cancel_event.is_set(): raise InterruptedError("Cancelled before start")
            self._check_disk_space()
            if self.cancel_event.is_set(): raise InterruptedError("Cancelled during disk check")
            downloaded_files = self._run_download_phase()
            if self.cancel_event.is_set() or not downloaded_files: raise InterruptedError("Cancelled during download")
            
            # Only run install phase if NOT using sequential (sequential installs as it goes)
            if not is_sequential:
                self._run_install_phase(downloaded_files)
                if self.cancel_event.is_set(): raise InterruptedError("Cancelled before completion")
                self._cleanup_successful_update_files(downloaded_files)
            
            self.progress_queue.put({'type': Q_MSG.COMPLETE, 'final_version': self.data.get('latest_version', 'N/A')})
        except InterruptedError as e:
            logger.log(f"Update workflow cancelled: {e}", "INFO")
            if not is_sequential:
                self._cleanup_failed_update_files(downloaded_files)
        except Exception as e:
            if not self.cancel_event.is_set():
                logger.log(f"Update workflow stopped due to a runtime error: {e}", "CRITICAL")
                self.progress_queue.put({'type': Q_MSG.DOWNLOAD_FAILED, 'reason': str(e)})
        finally:
            if self.cancel_event.is_set(): self.progress_queue.put({'type': Q_MSG.CANCELLED})
            logger.log("Update workflow finished.", "INFO")

    def _check_disk_space(self):
        self.progress_queue.put({'type': Q_MSG.OVERALL_STATUS, 'message': "Checking disk space..."})
        total_download_size = sum(u.get('size_bytes', 0) for u in self.updates)
        max_install_size = max((u.get('size_bytes', 0) for u in self.updates), default=0) * 2.5
        cache_drive = Path(self.cache_dir.anchor); game_drive = Path(self.game_dir.anchor)
        cache_free = shutil.disk_usage(cache_drive).free
        if cache_free < total_download_size: raise RuntimeError(f"Not enough space on {cache_drive} for downloads. Required: {format_bytes(total_download_size)}, Available: {format_bytes(cache_free)}")
        if game_drive == cache_drive:
             if cache_free < (total_download_size + max_install_size): raise RuntimeError(f"Not enough space on {game_drive} for download & install. Required: ~{format_bytes(total_download_size + max_install_size)}, Available: {format_bytes(cache_free)}")
        else:
            game_free = shutil.disk_usage(game_drive).free
            if game_free < max_install_size: raise RuntimeError(f"Not enough space on game drive {game_drive} for installation. Required: ~{format_bytes(max_install_size)}, Available: {format_bytes(game_free)}")
        logger.log("Disk space check passed.", "INFO")

    def _download_update_with_fallback(self, update_info: Dict) -> Optional[Path]:
        """
        Download update with fallback support for Cricket 26 v2.0 schema.
        Tries primary source first, then fallbacks in order.
        """
        downloads = update_info.get('downloads', {})
        
        # Try primary first
        primary = downloads.get('primary')
        if primary:
            self.progress_queue.put({
                'type': Q_MSG.STATUS,
                'message': f'📥 Trying primary: {primary.get("name", primary.get("type", "Unknown"))}'
            })
            
            result = self._download_from_source(primary, update_info)
            if result:
                return result
        
        # Primary failed - try fallbacks
        fallbacks = downloads.get('fallback', [])
        
        for i, fallback in enumerate(fallbacks, 1):
            self.progress_queue.put({
                'type': Q_MSG.STATUS,
                'message': f'🔄 Trying fallback {i}/{len(fallbacks)}: {fallback.get("name", fallback.get("type", "Unknown"))}'
            })
            
            result = self._download_from_source(fallback, update_info)
            if result:
                return result
        
        # All sources failed
        return None

    def _download_from_source(self, source: Dict, update_info: Dict) -> Optional[Path]:
        """
        Download from a single source (gdrive or direct).
        """
        source_type = source.get('type', 'unknown')
        
        try:
            archive_name = f"C26_Update_{update_info.get('from_version', '?')}_to_{update_info.get('to_version', '?')}.zip"
            output_path = self.cache_dir / archive_name
            
            if source_type == 'gdrive':
                # Google Drive download
                file_id = source.get('file_id')
                if not file_id:
                    # Try to extract from URL
                    url = source.get('url', '')
                    import re
                    match = re.search(r'/d/([a-zA-Z0-9_-]+)', url)
                    if match:
                        file_id = match.group(1)
                    else:
                        logger.log(f"No file_id found in source: {source}", "ERROR")
                        return None
                
                success = download_from_gdrive(
                    file_id,
                    output_path,
                    self.progress_queue,
                    self.cancel_event
                )
                
                if success and output_path.exists():
                    return output_path
                
            elif source_type == 'direct':
                # Direct HTTP download (use existing download system)
                url = source.get('url')
                if not url:
                    logger.log(f"No URL found in source: {source}", "ERROR")
                    return None
                
                # Create link format for existing downloader
                links = [{'link': url, 'host_id': source.get('name', 'direct')}]
                result = self.downloader.download_file(
                    links,
                    self.cache_dir,
                    archive_name
                )
                
                if result:
                    return result[0]  # Return the path
            
            else:
                logger.log(f"Unknown source type: {source_type}", "ERROR")
                
        except Exception as e:
            logger.log(f"Download from {source.get('name', 'unknown')} failed: {e}", "ERROR")
        
        return None

    def _run_download_phase_sequential(self) -> List[Dict[str, Any]]:
        """
        Download and INSTALL updates SEQUENTIALLY for Cricket 26 (install-as-you-go).
        Each update is installed immediately after download so partial progress is preserved.
        If update 7/12 fails, updates 1-6 remain installed.
        """
        num_updates = len(self.updates)
        completed_updates = []
        
        logger.log(f"Starting sequential download-and-install for {num_updates} updates", "INFO")
        
        with tempfile.TemporaryDirectory(prefix="c26-extract-") as temp_extract_dir_str:
            extract_dir = Path(temp_extract_dir_str)
            
            for i, update_info in enumerate(self.updates, 1):
                if self.cancel_event.is_set():
                    raise InterruptedError("Sequential update cancelled by user")
                
                # Show which update we're on
                from_ver = update_info.get('from_version', '?')
                to_ver = update_info.get('to_version', '?')
                
                self.progress_queue.put({
                    'type': Q_MSG.OVERALL_STATUS,
                    'message': f'📦 Sequential Update {i}/{num_updates}: v{from_ver} → v{to_ver}'
                })
                
                # Download with fallback support
                try:
                    self.progress_queue.put({
                        'type': Q_MSG.STATUS,
                        'message': f'⬇️ Downloading update {i}/{num_updates}...'
                    })
                    
                    downloaded_file = self._download_update_with_fallback(update_info)
                    
                    if not downloaded_file:
                        # Download failed even with fallbacks
                        raise RuntimeError(
                            f"Failed to download update {i}/{num_updates}. "
                            f"All sources failed for v{from_ver} → v{to_ver}. "
                            f"Game is at v{self.updates[i-2].get('to_version', 'unknown') if i > 1 else 'base'} "
                            f"(Installed: {len(completed_updates)}/{num_updates} updates)."
                        )
                    
                    # Download successful - verify if needed
                    if self.verify_checksums:
                        expected_checksum = update_info.get('downloads', {}).get('primary', {}).get('checksum')
                        if expected_checksum:
                            self.progress_queue.put({
                                'type': Q_MSG.STATUS,
                                'message': f'🔐 Verifying update {i}/{num_updates}...'
                            })
                            
                            if not self._verify_checksum(downloaded_file, expected_checksum):
                                logger.log(f"Checksum mismatch for update {i}", "ERROR")
                                # Clean up and fail
                                downloaded_file.unlink(missing_ok=True)
                                raise RuntimeError(f"Security verification failed for update {i}/{num_updates}")
                    
                    self.progress_queue.put({
                        'type': Q_MSG.STATUS,
                        'message': f'✅ Update {i}/{num_updates} downloaded successfully!'
                    })
                    
                    # INSTALL IMMEDIATELY (install-as-you-go)
                    self.progress_queue.put({
                        'type': Q_MSG.OVERALL_STATUS,
                        'message': f'📦 Installing Update {i}/{num_updates}...'
                    })
                    
                    # Extract
                    self.progress_queue.put({
                        'type': Q_MSG.STATUS,
                        'message': f'📂 Extracting update {i}/{num_updates}...'
                    })
                    self.extractor.extract_archive(downloaded_file, extract_dir, self.progress_queue, self.cancel_event)
                    
                    # Install
                    self.progress_queue.put({
                        'type': Q_MSG.STATUS,
                        'message': f'💾 Installing update {i}/{num_updates} to game directory...'
                    })
                    self.progress_queue.put({'type': Q_MSG.PROGRESS, 'value': 0})
                    self.extractor.install_files(extract_dir, self.game_dir, self.progress_queue, self.cancel_event)
                    
                    # Clean up extracted files for next update
                    for item in extract_dir.iterdir():
                        if item.is_dir():
                            import shutil
                            shutil.rmtree(item, ignore_errors=True)
                        else:
                            item.unlink(missing_ok=True)
                    
                    # Delete downloaded archive to save space
                    downloaded_file.unlink(missing_ok=True)
                    
                    # Mark as completed and installed
                    completed_updates.append({
                        'info': update_info,
                        'installed': True
                    })
                    
                    self.progress_queue.put({
                        'type': Q_MSG.STATUS,
                        'message': f'✅ Update {i}/{num_updates} installed successfully! Game now at v{to_ver}'
                    })
                    
                except Exception as e:
                    # Update failed - but previous updates are already installed!
                    logger.log(f"Sequential update {i}/{num_updates} failed: {e}", "ERROR")
                    
                    current_version = self.updates[i-2].get('to_version', 'unknown') if i > 1 else 'base'
                    
                    self.progress_queue.put({
                        'type': Q_MSG.DOWNLOAD_FAILED,
                        'reason': f'Update {i}/{num_updates} failed: {str(e)}\n\n'
                                  f'✅ Good News: Updates 1-{len(completed_updates)} are already installed!\n'
                                  f'📌 Current Game Version: v{current_version}\n'
                                  f'❌ Failed at: v{from_ver} → v{to_ver}\n\n'
                                  f'Your game is playable at v{current_version}. '
                                  f'You can retry the update later to complete remaining updates.'
                    })
                    
                    raise
        
        # All updates downloaded AND installed successfully!
        self.progress_queue.put({
            'type': Q_MSG.OVERALL_STATUS,
            'message': f'🎉 All {num_updates} updates installed successfully!'
        })
        
        return completed_updates

    def _run_download_phase(self) -> List[Dict[str, Any]]:
        """
        Main download phase - detects schema version and uses appropriate method.
        """
        # Check if using new v2.0 schema with sequential updates
        schema_version = self.data.get('metadata', {}).get('schema_version', '1.0')
        supports_sequential = self.data.get('metadata', {}).get('supports_sequential_updates', False)
        
        if schema_version == '2.0' or supports_sequential:
            logger.log("Using sequential update system (v2.0 schema)", "INFO")
            return self._run_download_phase_sequential()
        else:
            logger.log("Using legacy parallel download system", "INFO")
            return self._run_download_phase_legacy()
    
    def _run_download_phase_legacy(self) -> List[Dict[str, Any]]:
        """Legacy download phase for old schema (original Cricket 24 method)."""
        downloaded_files_map = []
        num_updates = len(self.updates)
        
        # INTELLIGENT MODE DETECTION for contextual messaging
        is_single_host_mode = all(len(update.get('links', [])) == 1 for update in self.updates)
        total_unique_hosts = len(set(link['host_id'] for update in self.updates for link in update.get('links', [])))
        
        if is_single_host_mode and total_unique_hosts == 1:
            # Pure single host mode - simplified messaging
            single_host_name = self.updates[0].get('links', [{}])[0].get('host_id', 'selected host')
            self.progress_queue.put({'type': Q_MSG.OVERALL_STATUS, 'message': f"📱 DOWNLOAD: Starting {num_updates} patch(es) from {single_host_name}"})
            self.progress_queue.put({'type': Q_MSG.STATUS, 'message': f"📡 Connecting to {single_host_name} for {num_updates} update file(s)..."})
        else:
            # Multi-host smart mode - advanced messaging
            self.progress_queue.put({'type': Q_MSG.OVERALL_STATUS, 'message': f"🚀 SMART DOWNLOAD: Starting {num_updates} patch(es) with intelligent host selection..."})
            self.progress_queue.put({'type': Q_MSG.STATUS, 'message': f"🧠 Initializing multi-host download system for {num_updates} update file(s)..."})
        
        for i, update_info in enumerate(self.updates):
            if self.cancel_event.is_set(): raise InterruptedError("Download phase cancelled.")
            
            # Enhanced patch info with contextual messaging
            patch_name = f"v{update_info.get('from', '?')} → v{update_info.get('to', '?')}"
            available_hosts = len(update_info.get('links', []))
            patch_is_single_host = available_hosts == 1
            
            if patch_is_single_host:
                # Single host for this patch
                host_name = update_info.get('links', [{}])[0].get('host_id', 'host')
                self.progress_queue.put({'type': Q_MSG.OVERALL_STATUS, 'message': f"📥 PATCH {i+1}/{num_updates}: {patch_name} from {host_name}"})
                self.progress_queue.put({'type': Q_MSG.STATUS, 'message': f"📡 Downloading patch {patch_name} from {host_name}..."})
            else:
                # Multi-host for this patch
                self.progress_queue.put({'type': Q_MSG.OVERALL_STATUS, 'message': f"📥 SMART PATCH {i+1}/{num_updates}: {patch_name} | {available_hosts} hosts available"})
                self.progress_queue.put({'type': Q_MSG.STATUS, 'message': f"🧠 Smart system: Testing {available_hosts} hosts for patch {patch_name}..."})
            
            archive_name = f"C26_Update_{update_info['from']}_to_{update_info['to']}.zip"
            
            try:
                download_result = self.downloader.download_file(update_info.get('links', []), self.cache_dir, archive_name)
                if not download_result:
                    if self.cancel_event.is_set(): 
                        raise InterruptedError("Download cancelled during file transfer.")
                    else: 
                        # Create contextual error message based on available hosts
                        if available_hosts == 1:
                            # Single host failure
                            single_host_name = update_info.get('links', [{}])[0].get('host_id', 'selected host')
                            raise RuntimeError(f"DOWNLOAD FAILED: {single_host_name} was unable to provide the update file for v{update_info.get('to', 'N/A')}. This could be due to network issues or server problems.")
                        else:
                            # Multi-host failure  
                            raise RuntimeError(f"SMART DOWNLOAD FAILED: All {available_hosts} hosts failed for update v{update_info.get('to', 'N/A')}.")
                
                dl_file_path, host_id = download_result
                
                # Show success with host info
                self.progress_queue.put({'type': Q_MSG.STATUS, 'message': f"✅ Patch {i+1}/{num_updates} downloaded successfully from {host_id}"})
                
            except Exception as e:
                # Enhanced error reporting with contextual host information
                error_msg = str(e)
                if "SMART DOWNLOAD FAILED" in error_msg or "hosts failed" in error_msg:
                    raise RuntimeError(f"Smart multi-host download system failed for patch {patch_name}: {error_msg}")
                elif "DOWNLOAD FAILED" in error_msg:
                    raise RuntimeError(f"Single host download failed for patch {patch_name}: {error_msg}")
                else:
                    raise RuntimeError(f"Download error for patch {patch_name}: {error_msg}")
            
            if self.verify_checksums:
                self.progress_queue.put({'type': Q_MSG.OVERALL_STATUS, 'message': f"🔍 SECURITY CHECK: Verifying Patch {i+1}/{num_updates}..."})
                self.progress_queue.put({'type': Q_MSG.STATUS, 'message': f"🔐 Checking file integrity for {patch_name} from {host_id}..."})
                
                expected_checksum = self._get_checksum_for_host(host_id, update_info['key'])
                
                if expected_checksum:
                    if not self._verify_checksum(dl_file_path, expected_checksum):
                        self.progress_queue.put({'type': Q_MSG.CHECKSUM_CONFIRM, 'update_info': update_info})
                        if not self.decision_queue.get():
                            if dl_file_path.exists(): dl_file_path.unlink(missing_ok=True)
                            raise RuntimeError(f"Update aborted by user due to checksum mismatch for v{update_info.get('to', 'N/A')}.")
                        logger.log(f"User continued despite checksum mismatch for v{update_info.get('to', 'N/A')}.", "WARNING")
                    else:
                        self.progress_queue.put({'type': Q_MSG.STATUS, 'message': f"🔐 Security check passed for {patch_name}"})
                else:
                    logger.log(f"No checksum found for host '{host_id}' for patch to v{update_info['to']}. Skipping verification.", "WARNING")
                    self.progress_queue.put({'type': Q_MSG.STATUS, 'message': f"⚠️ No checksum available for {patch_name} from {host_id}"})

            downloaded_files_map.append({'info': update_info, 'path': dl_file_path})
            
        # Final success status with contextual messaging
        if num_updates == 1 and available_hosts == 1:
            single_host_name = downloaded_files_map[0]['info']['links'][0]['host_id']
            self.progress_queue.put({'type': Q_MSG.STATUS, 'message': f"✅ Update downloaded successfully from {single_host_name}"})
        else:
            self.progress_queue.put({'type': Q_MSG.STATUS, 'message': f"✅ All {num_updates} patch(es) downloaded successfully with smart system"})
        return downloaded_files_map

    def _run_install_phase(self, files_to_install: List[Dict[str, Any]]):
        with tempfile.TemporaryDirectory(prefix="c26-extract-") as temp_extract_dir_str:
            extract_dir = Path(temp_extract_dir_str)
            for i, downloaded_file in enumerate(files_to_install):
                if self.cancel_event.is_set(): raise InterruptedError("Installation phase cancelled.")
                
                self.progress_queue.put({'type': Q_MSG.OVERALL_STATUS, 'message': f"Extracting Patch {i+1}/{len(files_to_install)}..."})
                self.extractor.extract_archive(downloaded_file['path'], extract_dir, self.progress_queue, self.cancel_event)

                self.progress_queue.put({'type': Q_MSG.OVERALL_STATUS, 'message': f"Installing Patch {i+1}/{len(files_to_install)}..."})
                self.progress_queue.put({'type': Q_MSG.PROGRESS, 'value': 0})
                self.extractor.install_files(extract_dir, self.game_dir, self.progress_queue, self.cancel_event)

                for item in extract_dir.iterdir():
                    if item.is_dir(): shutil.rmtree(item)
                    else: item.unlink()

    def _cleanup_successful_update_files(self, downloaded_files: List[Dict[str, Any]]):
        logger.log("Update successful. Cleaning up used patch files.", "INFO")
        self.progress_queue.put({'type': Q_MSG.OVERALL_STATUS, 'message': "Cleaning up temporary files..."})
        for file_data in downloaded_files:
            archive_path = file_data['path']
            try:
                archive_path.unlink(missing_ok=True)
            except OSError as e:
                logger.log(f"Could not delete file {archive_path.name} during cleanup: {e}", "WARNING")

    def _cleanup_failed_update_files(self, downloaded_files: List[Dict[str, Any]]):
        logger.log("Cleaning up files from failed/cancelled update.", "INFO")
        for file_data in downloaded_files:
            archive_path = file_data['path']
            try:
                archive_path.with_suffix(archive_path.suffix + '.progress').unlink(missing_ok=True)
                archive_path.unlink(missing_ok=True)
                logger.log(f"Deleted incomplete download: {archive_path.name}", "INFO")
            except OSError as e:
                logger.log(f"Could not delete file {archive_path.name} during cleanup: {e}", "WARNING")

    def _get_checksum_for_host(self, host_id: str, update_key: str) -> Optional[str]:
        for host in self.data.get('hosts', []):
            if host.get('id') == host_id:
                host_checksums = host.get('checksums')
                if isinstance(host_checksums, dict):
                    checksum = host_checksums.get(update_key)
                    if checksum:
                        logger.log(f"Found specific checksum for host '{host_id}' and patch '{update_key}'.", "INFO")
                        return checksum
                    else:
                        logger.log(f"Host '{host_id}' has a checksums object, but no entry for '{update_key}'.", "WARNING")
                        return None
        
        logger.log(f"No checksums object defined for host '{host_id}'. Verification for this file will be skipped.", "WARNING")
        return None

    def _verify_checksum(self, file_path: Path, expected_hash: str) -> bool:
        self.progress_queue.put({'type': Q_MSG.STATUS, 'message': f"Verifying integrity of {file_path.name}..."})
        logger.log(f"Verifying checksum for {file_path.name}", "INFO"); sha256 = hashlib.sha256()
        try:
            with open(file_path, "rb") as f:
                for chunk in iter(lambda: f.read(4 * 1024 * 1024), b""):
                    if self.cancel_event.is_set(): return False
                    self.pause_event.wait()
                    sha256.update(chunk)
            is_valid = sha256.hexdigest().lower() == expected_hash.lower()
            logger.log(f"Checksum for {file_path.name} {'OK' if is_valid else 'MISMATCH'}.", "INFO" if is_valid else "ERROR")
            return is_valid
        except IOError as e:
            logger.log(f"Could not read file for checksum: {e}", "ERROR")
            return False

class GameVerifier:
    """Handles the logic for verifying game files against a manifest."""
    def __init__(self, game_dir: Path, manifest: Dict, queue: queue.Queue, cancel: threading.Event, pause: threading.Event):
        self.game_dir, self.manifest_data = game_dir, manifest
        self.progress_queue, self.cancel_event, self.pause_event = queue, cancel, pause
        self.issue_buffer: List[Tuple[str, str]] = []
        self.BUFFER_FLUSH_SIZE = 100
        self.BUFFER_FLUSH_INTERVAL_S = 0.5
        self.last_flush_time = 0

    def _flush_issue_buffer(self, force: bool = False):
        if self.issue_buffer and (force or len(self.issue_buffer) >= self.BUFFER_FLUSH_SIZE or time.time() - self.last_flush_time > self.BUFFER_FLUSH_INTERVAL_S):
            self.progress_queue.put({'type': Q_MSG.VERIFY_ISSUES_BATCH, 'batch': list(self.issue_buffer)})
            self.issue_buffer.clear()
            self.last_flush_time = time.time()

    def _calculate_sha256(self, file_path: Path) -> Optional[str]:
        sha256 = hashlib.sha256()
        try:
            with open(file_path, "rb") as f:
                while chunk := f.read(4 * 1024 * 1024):
                    if self.cancel_event.is_set(): return None
                    self.pause_event.wait(); sha256.update(chunk)
            return sha256.hexdigest()
        except (IOError, PermissionError):
            logger.log(f"Permission denied or IO error reading {file_path} for hashing.", "ERROR")
            return None

    def run(self):
        logger.log("Starting game file verification (in-memory)...", "INFO")
        self.progress_queue.put({'type': Q_MSG.OVERALL_STATUS, 'message': 'Verifying Game Files'})
        normalized_manifest = {key.replace('\\', '/'): value for key, value in self.manifest_data.items()}
        try:
            local_files = {p.relative_to(self.game_dir).as_posix() for p in self.game_dir.rglob('*') if p.is_file()}
        except PermissionError:
            self.progress_queue.put({'type': Q_MSG.ERROR, 'message': "Permission denied when scanning game files. Please check folder permissions."})
            return
        manifest_files = set(normalized_manifest.keys())
        missing_files, corrupted_files, good_files, extra_files, unreadable_files = [], [], [], sorted(list(local_files - manifest_files)), []
        self.last_flush_time = time.time()
        for rel_path in sorted(list(manifest_files - local_files)):
            if self.cancel_event.is_set(): break
            missing_files.append(rel_path)
            self.issue_buffer.append(('missing', rel_path))
            self._flush_issue_buffer()
        if not self.cancel_event.is_set():
            files_to_check = sorted(list(manifest_files.intersection(local_files)))
            last_update_time = time.time()
            for i, rel_path in enumerate(files_to_check):
                if self.cancel_event.is_set(): break
                self.pause_event.wait()
                current_time = time.time()
                if current_time - last_update_time > 0.1:
                    self.progress_queue.put({'type': Q_MSG.VERIFY_STATS, 'data': {'processed': i, 'total': len(files_to_check), 'missing': len(missing_files), 'corrupted': len(corrupted_files), 'current_file': Path(rel_path).name}})
                    last_update_time = current_time
                full_path = self.game_dir / rel_path.replace('/', os.sep); expected_hash = normalized_manifest.get(rel_path)
                if not expected_hash: continue
                calculated_hash = self._calculate_sha256(full_path)
                if calculated_hash is None:
                    if self.cancel_event.is_set(): break
                    unreadable_files.append(rel_path)
                    continue
                if calculated_hash.lower() == expected_hash.lower():
                    good_files.append(rel_path)
                else:
                    corrupted_files.append(rel_path)
                    self.issue_buffer.append(('corrupted', rel_path))
                    logger.log(f"Verification failed for {rel_path}. Hash mismatch.", "WARNING")
                self._flush_issue_buffer()
        self._flush_issue_buffer(force=True)
        if self.cancel_event.is_set():
            self.progress_queue.put({'type': Q_MSG.VERIFY_CANCELLED})
            return
        final_data = {'processed': len(files_to_check), 'total': len(files_to_check), 'missing': len(missing_files), 'corrupted': len(corrupted_files), 'current_file': "Finalizing report..."}
        self.progress_queue.put({'type': Q_MSG.VERIFY_STATS, 'data': final_data})
        results = {"missing": missing_files, "corrupted": corrupted_files, "extra": extra_files, "good": good_files, "unreadable": unreadable_files}
        self.progress_queue.put({'type': Q_MSG.VERIFY_COMPLETE, 'results': results}); logger.log("Game file verification finished.", "INFO")

class DiagnosticsManager:
    """Collects and reports system, game, and crash log information."""
    def __init__(self, game_dir: Optional[Path]):
        self.game_dir = game_dir
        self.is_admin = is_admin()

    def _format_driver_version(self, gpu_name: str, driver_version: str) -> str:
        if not driver_version or driver_version == "N/A":
            return "N/A"
        if "nvidia" in gpu_name.lower():
            try:
                numerals = driver_version.replace('.', '')
                if len(numerals) >= 5:
                    last_five = numerals[-5:]
                    return f"{last_five[:3]}.{last_five[3:]}"
            except (IndexError, ValueError) as e:
                logger.log(f"Could not parse NVIDIA driver version '{driver_version}': {e}", "WARNING")
                return driver_version
        return driver_version

    def _get_simplified_directx_version(self) -> str:
        try:
            win_version = platform.version(); major_version = int(win_version.split('.')[0])
            if major_version >= 10: return "12"
            if major_version == 6:
                minor_version = int(win_version.split('.')[1])
                if minor_version >= 2: return "11.1"
                if minor_version == 1: return "11"
                if minor_version == 0: return "10"
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\DirectX") as key: version_str, _ = winreg.QueryValueEx(key, "Version"); return "9.0c" if version_str.startswith("4.09") else version_str
        except Exception as e: logger.log(f"Could not determine DirectX version: {e}", "WARNING"); return "Unknown"

    def _get_wmi_data(self) -> Dict[str, str]:
        wmi_report = {}
        try:
            import pythoncom
            pythoncom.CoInitializeEx(0)
            import wmi
            wmi_obj = wmi.WMI()

            ram_info = psutil.virtual_memory()
            wmi_report["RAM"] = f"{format_bytes(ram_info.total)} (Available: {format_bytes(ram_info.available)})"

            gpu_controllers = wmi_obj.Win32_VideoController()
            if not gpu_controllers:
                wmi_report["GPU"] = "N/A"
            else:
                gpu_details = []
                sorted_gpus = sorted(gpu_controllers, key=lambda g: 0 if any(m in (g.Name or "").lower() for m in ['nvidia', 'amd', 'radeon']) else 1)
                for gpu in sorted_gpus:
                    gpu_name = gpu.Name or "Unknown GPU"
                    driver_ver = self._format_driver_version(gpu_name, gpu.DriverVersion)
                    gpu_details.append(f"{gpu_name} (Driver: {driver_ver})")
                wmi_report["GPU"] = "\n".join(gpu_details)
        except Exception as e:
            logger.log(f"WMI data collection failed: {e}", "ERROR")
            wmi_report['wmi_error'] = f"Could not collect WMI data: {e}"
            wmi_report["GPU"] = "Error collecting data"
            wmi_report["RAM"] = "Error collecting data"
        finally:
            if 'pythoncom' in sys.modules:
                pythoncom.CoUninitialize()
        return wmi_report

    def _get_system_info(self) -> Dict[str, str]:
        """Get system information with enhanced error handling and performance optimization."""
        report_part = {
            "OS": "N/A", "CPU": "N/A", "DirectX Version": "N/A",
            "Disk Space": "N/A", "Game Version": "Directory Not Selected"
        }
        
        try:
            # OS information with timeout protection
            try:
                report_part["OS"] = f"{platform.system()} {platform.release()} ({platform.version()})"
            except Exception as e:
                logger.log(f"Failed to get OS info: {e}", "WARNING")
                report_part["OS"] = "Unknown OS"
            
            # CPU information with fallback
            try:
                cpu_info = cpuinfo.get_cpu_info()
                report_part["CPU"] = cpu_info.get('brand_raw', cpu_info.get('brand', 'Unknown CPU'))
            except Exception as e:
                logger.log(f"Failed to get CPU info: {e}", "WARNING")
                report_part["CPU"] = "Unknown CPU"
            
            # DirectX version with error handling
            try:
                report_part["DirectX Version"] = self._get_simplified_directx_version()
            except Exception as e:
                logger.log(f"Failed to get DirectX version: {e}", "WARNING")
                report_part["DirectX Version"] = "Unknown"
            
            # Disk space with multiple drive fallback
            try:
                disk = shutil.disk_usage("C:\\")
                report_part['Disk Space'] = f"C: Total: {format_bytes(disk.total)}, Free: {format_bytes(disk.free)}"
            except (FileNotFoundError, OSError) as e:
                logger.log(f"Failed to get disk space: {e}", "WARNING")
                report_part['Disk Space'] = "C: drive not accessible"

            # Game version with improved error handling
            if self.game_dir and self.game_dir.exists():
                try:
                    version = GameManager(str(self.game_dir)).check_version()
                    report_part["Game Version"] = version or "Unknown"
                except Exception as e:
                    logger.log(f"Failed to get game version: {e}", "WARNING")
                    report_part["Game Version"] = "Version check failed"
            else:
                report_part["Game Version"] = "Directory not selected or invalid"
                
        except Exception as e:
            logger.log(f"Critical error in system info gathering: {e}", "ERROR")
            # Return minimal safe report
            report_part = {k: "Error" for k in report_part.keys()}

        return report_part

    def generate_report(self, full_scan: bool = False) -> Dict[str, Any]:
        logger.log(f"Starting diagnostics report generation (Full Scan: {full_scan}, Admin: {self.is_admin}).", "DIAG")
        report = {'system': self._get_system_info()}
        wmi_data = self._get_wmi_data()
        report['system'].update(wmi_data)

        if full_scan:
            logger.log(f"Full scan requested. Admin status: {self.is_admin}", "DIAG")
            if not self.is_admin:
                report['crashes'] = "🔒 ADMINISTRATOR RIGHTS REQUIRED\n\nTo scan Windows Event Logs for Cricket 26 crashes, this application needs Administrator privileges.\n\n📋 HOW TO ENABLE CRASH LOG SCANNING:\n1. Close this application\n2. Right-click on the Cricket 26 Updater executable\n3. Select 'Run as Administrator'\n4. Click 'Run Full System Scan' again\n\n💡 WHY ADMIN RIGHTS ARE NEEDED:\nWindows Event Logs contain sensitive system information and require elevated privileges to access crash data from Application Error events."
                logger.log("Crash log scan skipped: Not running as Admin.", "WARNING")
            else:
                logger.log("Starting Cricket 26 crash detection with admin privileges.", "DIAG")
                # Enhanced Cricket 26 specific crash detection with multiple search strategies
                cricket_crashes = []
                
                try:
                    # Strategy 1: Search all Application Error events and filter for cricket26.exe
                    command = ['wevtutil', 'qe', 'Application', 
                             '/q:*[System[Provider[@Name=\'Application Error\']]]', 
                             '/c:50', '/rd:true', '/f:text']
                    
                    logger.log(f"Executing crash detection command: {' '.join(command)}", "DIAG")
                    proc = subprocess.run(command, capture_output=True, text=True, 
                                        creationflags=subprocess.CREATE_NO_WINDOW, 
                                        encoding='utf-8', errors='ignore', 
                                        timeout=Constants.DIAG_PROCESS_TIMEOUT_SECONDS)
                    
                    if proc.returncode == 0 and proc.stdout.strip():
                        # Parse events and filter for Cricket 26 crashes
                        events = proc.stdout.strip().split('Event[')
                        
                        for i, event in enumerate(events[1:], 1):  # Skip first empty split
                            try:
                                import re
                                
                                # Look for cricket26.exe in the event text (case insensitive)
                                if 'cricket26.exe' not in event.lower():
                                    continue
                                
                                # Extract crash information with improved regex patterns
                                timestamp_match = re.search(r'Date: ([^\r\n]+)', event)
                                app_name_match = re.search(r'Faulting application name: ([^,\r\n]+)', event)
                                app_version_match = re.search(r'version: ([^,\r\n]+)', event)
                                fault_module_match = re.search(r'Faulting module name: ([^,\r\n]+)', event)
                                exception_code_match = re.search(r'Exception code: (0x[0-9a-fA-F]+)', event)
                                app_path_match = re.search(r'Faulting application path: ([^\r\n]+)', event)
                                report_id_match = re.search(r'Report Id: ([^\r\n]+)', event)
                                
                                if timestamp_match and app_name_match:
                                    # Parse timestamp (ISO format to readable)
                                    timestamp_raw = timestamp_match.group(1).strip()
                                    try:
                                        # Convert from ISO format to readable format
                                        if 'T' in timestamp_raw and 'Z' in timestamp_raw:
                                            timestamp_dt = datetime.fromisoformat(timestamp_raw.replace('Z', '+00:00'))
                                            timestamp = timestamp_dt.strftime('%Y-%m-%d %H:%M:%S')
                                        else:
                                            timestamp = timestamp_raw
                                    except:
                                        timestamp = timestamp_raw
                                    
                                    app_name = app_name_match.group(1).strip()
                                    app_version = app_version_match.group(1).strip() if app_version_match else "Unknown"
                                    fault_module = fault_module_match.group(1).strip() if fault_module_match else "Unknown"
                                    exception_code = exception_code_match.group(1) if exception_code_match else "Unknown"
                                    app_path = app_path_match.group(1).strip() if app_path_match else "Unknown"
                                    report_id = report_id_match.group(1).strip() if report_id_match else "Unknown"
                                    
                                    # Determine crash type based on exception code
                                    crash_type_details = {
                                        '0xc0000005': ('Access Violation', 'Critical memory access error - likely a bug in the game code or corrupted memory'),
                                        '0xc0000409': ('Stack Buffer Overflow', 'Security-related crash - stack corruption detected'),
                                        '0xc000041d': ('Fast Fail Exception', 'Security check failure - corrupted data structures'),
                                        '0x80000003': ('Breakpoint Exception', 'Debug breakpoint - possibly corrupted executable'),
                                        '0xc0000002': ('File Not Found', 'Missing required game files or libraries'),
                                        '0x80131623': ('.NET Exception', 'Managed code error - likely a framework issue')
                                    }
                                    
                                    crash_type, crash_description = crash_type_details.get(
                                        exception_code.lower(), 
                                        ('Application Error', 'General application crash - check game files and drivers')
                                    )
                                    
                                    # Create simplified crash entry
                                    crash_entry = f"""🔥 CRICKET 26 CRASH #{len(cricket_crashes) + 1}
📅 Date/Time: {timestamp}
🎮 Application: {app_name} (Version {app_version})
📁 Game Path: {app_path}
⚠️ Error Type: {crash_type}
💻 Exception Code: {exception_code}
🔧 Faulting Module: {fault_module}
📋 Report ID: {report_id}"""
                                    
                                    cricket_crashes.append(crash_entry)
                                    
                            except Exception as e:
                                logger.log(f"Error parsing crash event {i}: {e}", "ERROR")
                                continue
                                
                except (subprocess.TimeoutExpired, Exception) as e:
                    logger.log(f"Error searching for Cricket 26 crashes: {e}", "ERROR")
                
                # Format final output
                if cricket_crashes:
                    crashes_to_show = cricket_crashes[:3]  # Show only first 3 most recent crashes
                    report['crashes'] = f"🔥 FOUND {len(cricket_crashes)} CRICKET 26 CRASH(ES):\n\n" + "\n\n" + "="*80 + "\n\n".join(crashes_to_show)
                    
                    if len(cricket_crashes) > 3:
                        report['crashes'] += f"\n\n📊 SUMMARY: Showing 3 most recent crashes out of {len(cricket_crashes)} total found."
                    
                    report['crashes'] += f"\n\n�️ CRASH ANALYSIS COMPLETE\nAll crashes have been identified and analyzed. Use the troubleshooting tips above to resolve these issues."
                    
                    logger.log(f"Found {len(cricket_crashes)} Cricket 26 specific crashes.", "DIAG")
                else:
                    report['crashes'] = f"✅ NO CRICKET 26 CRASHES FOUND\n\n🔍 SEARCH RESULTS:\n• Searched 50 most recent Application Error events\n• Checked for cricket26.exe specifically\n• No Cricket 26 crashes detected in Windows Event Logs\n\n📋 POSSIBLE REASONS:\n• Cricket 26 is running stable without crashes\n• Event logs may have been cleared by Windows\n• Crashes might be logged under a different name\n• Game might be freezing instead of crashing\n\n💡 MANUAL CHECK:\n• Open Windows Event Viewer manually\n• Navigate to Windows Logs > Application\n• Filter by 'Application Error' source\n• Look for cricket26.exe entries"
                    logger.log("No Cricket 26 specific crashes found in Windows Event Logs.", "DIAG")
        else:
            report['crashes'] = "📋 CRASH LOG SCANNING NOT PERFORMED\n\nThis is a quick system scan that only checks basic system information.\n\n🔄 TO SCAN FOR CRASH LOGS:\n1. Click 'Run Full System Scan' button above\n2. Grant Administrator privileges if prompted\n3. Wait for the full scan to complete\n\n� FULL SCAN OVERVIEW:\n• Recent Cricket 24 crashes detected\n• Basic crash information and timing\n• System compatibility check"

        logger.log("Diagnostics report generation complete.", "INFO")
        return report

# ==============================================================================
# --- APPLICATION CONTROLLER (The Brain) ---
# ==============================================================================
class BackgroundTaskManager:
    """Enhanced thread pool manager with memory leak prevention."""
    def __init__(self, controller: 'AppController'):
        self.controller = controller
        self.executor = ThreadPoolExecutor(max_workers=5, thread_name_prefix='AppWorker')
        self.active_futures: set = set()  # Track active futures for cleanup
        self._cleanup_lock = threading.Lock()

    def submit(self, task_func: Callable, on_done: Optional[Callable] = None, on_error: Optional[Callable] = None, *, is_utility_task: bool = False, args: tuple = (), kwargs: dict = {}) -> Future:
        future = self.executor.submit(task_func, *args, **kwargs)
        
        # Track the future for cleanup
        with self._cleanup_lock:
            self.active_futures.add(future)

        def _callback(f: Future):
            try:
                # Remove future from tracking set
                with self._cleanup_lock:
                    self.active_futures.discard(f)
                
                if f.cancelled():
                    logger.log(f"Task '{task_func.__name__}' was cancelled.", "INFO")
                    return

                try:
                    result = f.result()
                    if on_done:
                        self.controller.view.after(0, on_done, result)
                except Exception as e:
                    log_msg = f"Error in background task '{task_func.__name__}': {e}"
                    if isinstance(e, (requests.ConnectionError, requests.Timeout)):
                        logger.log(log_msg, "ERROR")
                        message = "Network Error: Could not connect. Please check your internet connection."
                    elif isinstance(e, (IOError, PermissionError, OSError)):
                        logger.log(log_msg, "ERROR")
                        message = "File Error: Could not access a required file. Please check permissions and disk space."
                    else:
                        logger.log(log_msg, "CRITICAL")
                        message = f"An unexpected error occurred: {e}"

                    if on_error:
                        self.controller.view.after(0, on_error, message)
                    else:
                        self.controller.view.after(0, self.controller._handle_generic_error, message)
                finally:
                    if is_utility_task:
                        self.controller.view.after(10, self.controller.set_state, AppState.IDLE)
            
            except Exception as cleanup_error:
                logger.log(f"Error in future cleanup: {cleanup_error}", "ERROR")

        future.add_done_callback(_callback)
        return future

    def cleanup_completed_futures(self):
        """Clean up completed futures to prevent memory leaks."""
        with self._cleanup_lock:
            completed_futures = {f for f in self.active_futures if f.done()}
            for future in completed_futures:
                self.active_futures.discard(future)
                # Clear any remaining references
                try:
                    future.result(timeout=0)  # This will raise if there was an exception
                except:
                    pass  # Ignore exceptions during cleanup
            
            if completed_futures:
                logger.log(f"Cleaned up {len(completed_futures)} completed futures", "INFO")

    def shutdown(self):
        """Quick shutdown without blocking."""
        logger.log("Shutting down BackgroundTaskManager...", "INFO")
        
        # Cancel all pending futures
        with self._cleanup_lock:
            for future in self.active_futures:
                if not future.done():
                    future.cancel()
            self.active_futures.clear()
        
        # Quick executor shutdown without waiting
        try:
            self.executor.shutdown(wait=False)  # Don't wait for completion
            logger.log("BackgroundTaskManager shutdown initiated", "INFO")
        except Exception as e:
            logger.log(f"Error during executor shutdown: {e}", "ERROR")
        else:
            logger.log("BackgroundTaskManager shutdown complete", "INFO")

def manage_state(state: AppState) -> Callable:
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(controller: 'AppController', *args, **kwargs):
            if controller.state != AppState.IDLE and controller.state != AppState.STARTING:
                logger.log(f"Attempted to start task '{func.__name__}' while in a busy state '{controller.state.name}'. Aborting.", "WARNING")
                return

            try:
                controller.set_state(state)
                return func(controller, *args, **kwargs)
            except Exception as e:
                logger.log(f"Immediate critical error in '{func.__name__}' before task submission: {e}", "CRITICAL")
                controller.set_state(AppState.IDLE)
                messagebox.showerror("Critical Error", f"Could not start operation: {e}")
        return wrapper
    return decorator

class AppController:
    """Orchestrates the application logic, connecting the GUI and worker classes."""
    def __init__(self, view: 'AppGUI'):
        self.view = view
        self.state = AppState.IDLE
        self._state_lock = threading.RLock()  # Thread-safe state management
        self.game_dir = view.game_dir_var
        self.verify_checksum_enabled = view.verify_checksum_var
        self.download_source_var = view.download_source_var
        self.current_version = ""
        self.updates_to_install = []
        self.last_verify_results = {}
        self.last_diag_report = {}
        self.diag_info_fetched = False
        self._last_diag_scan_time = 0
        self.dir_change_tasks: List[Future] = []
        self.progress_queue = queue.Queue()
        self.decision_queue = queue.Queue()
        self.updater_cancel_event = threading.Event()
        self.downloader_pause_event = threading.Event(); self.downloader_pause_event.set()
        self.verifier_cancel_event = threading.Event()
        self.verifier_pause_event = threading.Event(); self.verifier_pause_event.set()
        self.verifier_scan_started = False
        self.is_in_retry_wait = False
        self.update_data = None
        self.is_admin = is_admin()
        self.task_manager = BackgroundTaskManager(self)
        
        # NEW: Enhanced error recovery and download management
        self._last_download_failure = None  # Track last failure for retry functionality
        self.download_stats = {}  # Track current download statistics
        self.queue_handlers = {
            Q_MSG.STATUS: self._handle_status, Q_MSG.OVERALL_STATUS: self._handle_overall_status,
            Q_MSG.PROGRESS: self._handle_progress, Q_MSG.PROGRESS_MODE: self._handle_progress_mode,
            Q_MSG.CANCELLED: self._handle_cancelled, Q_MSG.COMPLETE: self._handle_update_complete,
            Q_MSG.CHECKSUM_CONFIRM: self._handle_checksum_confirm,
            Q_MSG.DOWNLOAD_FAILED: self._handle_download_failure, Q_MSG.DOWNLOAD_RETRY_WAIT: self._handle_download_retry_wait,
            Q_MSG.DOWNLOAD_SPEED: self._handle_download_speed, Q_MSG.DOWNLOAD_ERROR_RETRY: self._handle_download_error_retry,  # NEW handlers
            Q_MSG.VERIFY_STATS: self._handle_verify_stats, Q_MSG.VERIFY_COMPLETE: self._handle_verify_complete,
            Q_MSG.VERIFY_CANCELLED: self._handle_verify_cancelled, Q_MSG.VERIFY_ISSUES_BATCH: self._handle_verify_issues_batch,
            Q_MSG.MANUAL_INSTALL_CONFIRM: self._handle_manual_install_confirm,
            Q_MSG.MANUAL_INSTALL_COMPLETE: self._handle_manual_install_complete,
            Q_MSG.ERROR: lambda msg: messagebox.showerror("Error", msg.get('message', 'An unknown error occurred.')),
        }

    def start(self, startup_actions: List[Tuple[Callable, Tuple]]):
        self.set_state(AppState.STARTING)
        self.process_queue()
        self.view.refresh_logs()
        logger.log(f"Application started. Admin: {'Yes' if self.is_admin else 'No'}", "SETTING")
        try:
            Constants.CACHE_DIR.mkdir(exist_ok=True)
            Constants.VERIFICATION_LOGS_DIR.mkdir(exist_ok=True)
        except PermissionError as e:
            logger.log(f"FATAL: No permission to create cache directory at {Constants.CACHE_DIR}. {e}", "CRITICAL")
            messagebox.showerror("Fatal Startup Error", f"Could not create or access the cache directory.\n\nPlease check your permissions for the folder:\n{Constants.CACHE_DIR}")
            self.view.after(100, self.on_closing)
            return

        self.task_manager.submit(
            APIHandler.load_update_data,
            on_done=self._on_initial_data_loaded,
            on_error=self._on_initial_data_load_error
        )
        
        self.startup_actions = startup_actions

    def process_queue(self):
        try:
            # Process all pending messages with improved batching for real-time responsiveness
            messages_processed = 0
            max_messages_per_cycle = Constants.MAX_QUEUE_MESSAGES_PER_CYCLE  # Use constant (was hardcoded 10)
            
            while not self.progress_queue.empty() and messages_processed < max_messages_per_cycle:
                try:
                    msg = self.progress_queue.get_nowait()
                    handler = self.queue_handlers.get(msg.get('type'))
                    if handler:
                        try:
                            handler(msg)
                        except Exception as e:
                            logger.log(f"Error in queue handler for {msg.get('type')}: {e}", "CRITICAL")
                    messages_processed += 1
                except queue.Empty:
                    break
                except Exception as e:
                    logger.log(f"Critical error in process_queue loop: {e}", "CRITICAL")
                    
            # Optimized periodic cleanup
            if not hasattr(self, '_cleanup_counter'):
                self._cleanup_counter = 0
            self._cleanup_counter += 1
            if self._cleanup_counter >= Constants.CLEANUP_INTERVAL_CYCLES:
                self._cleanup_counter = 0
                try:
                    self.task_manager.cleanup_completed_futures()
                except Exception as e:
                    logger.log(f"Error during periodic cleanup: {e}", "ERROR")
        except Exception as e:
            logger.log(f"process_queue outer exception: {e}", "CRITICAL")
        finally:
            # Dynamic scheduling for optimal real-time responsiveness
            if self.state in [AppState.UPDATING, AppState.VERIFYING, AppState.MANUAL_INSTALLING]:
                interval = Constants.QUEUE_PROCESS_INTERVAL_ACTIVE  # 30ms during active operations
            else:
                interval = Constants.QUEUE_PROCESS_INTERVAL_IDLE  # 100ms during idle
            
            if hasattr(self, 'view') and self.view.winfo_exists():
                self.view.after(interval, self.process_queue)

    def set_state(self, new_state: AppState):
        """Thread-safe state management with logging."""
        with self._state_lock:
            if self.state == new_state: 
                return
            old_state = self.state
            self.state = new_state
            logger.log(f"State transition: {old_state.name} -> {new_state.name}", "SETTING")
            # Schedule UI update on main thread
            self.view.after_idle(lambda: self.view.update_ui_for_state(new_state))

    def on_closing(self):
        busy_states = [AppState.UPDATING, AppState.VERIFYING, AppState.MANUAL_INSTALLING, AppState.BUSY, AppState.DIAGNOSTICS]
        if self.state in busy_states:
            if not messagebox.askyesno("Confirm Exit", "An operation is currently in progress.\n\nAre you sure you want to exit? This may leave files in an incomplete state.", icon='warning'):
                return
        
        logger.log("Application shutdown initiated", "INFO")
        
        # Set all cancellation events to allow threads to exit
        self.downloader_pause_event.set()
        self.updater_cancel_event.set()
        self.verifier_cancel_event.set()
        
        # Cancel any pending directory change tasks
        for task in self.dir_change_tasks:
            if not task.done():
                task.cancel()
        
        # Quick cleanup of task manager without blocking
        try:
            self.task_manager.shutdown()
        except Exception as e:
            logger.log(f"Error during task manager shutdown: {e}", "WARNING")
        
        # Immediate GUI destruction
        logger.log("Application shutdown complete", "INFO")
        self.view.destroy()

    def select_game_dir(self):
        if self.state != AppState.IDLE: return
        new_directory = filedialog.askdirectory(title="Select Cricket 26 Game Directory")
        if new_directory and new_directory != self.game_dir.get():
            self.game_dir.set(new_directory)

    def process_directory_change(self):
        dir_path = self.game_dir.get()
        if dir_path:
            self.view.show_dashboard_view("Updater")
            self.view.show_dashboard_view("Verifier")
            self.handle_dir_tasks()
        else:
            self.view.show_welcome_view("Updater")
            self.view.show_welcome_view("Verifier")

    def handle_dir_tasks(self):
        for task in self.dir_change_tasks:
            if not task.done():
                task.cancel()
        self.dir_change_tasks.clear()
        logger.log(f"Game directory changed to: {self.game_dir.get()}. Pending init tasks cancelled.", "INFO")

        self.view.refresh_logs()

        task1 = self.task_manager.submit(self.refresh_version_and_updates)
        task2 = self.task_manager.submit(self.run_initial_diagnostics)
        self.dir_change_tasks.extend([task1, task2])


    def refresh_version_and_updates(self):
        dir_path = self.game_dir.get()
        manager = GameManager(dir_path)
        version = manager.check_version()
        self.view.update_dashboard_action_button.config(text=f"{Constants.ICON_SEARCH} Check for Updates", command=self.check_updates, style="Accent.TButton", state='normal')
        self.view.update_plan_text.config(state='normal')
        self.view.update_plan_text.delete(1.0, tk.END)
        if version in ["NOT_FOUND", "INVALID_FORMAT", "READ_ERROR"]:
            self.current_version = ""
            self.view.dashboard_game_version_label.config(text=f"v?.?.?")
            self.view.dashboard_status_label.config(text="Could not detect version. Please check the directory.", style="Warning.TLabel")
            self.view.update_plan_text.insert(tk.END, "Please select a valid Cricket 26 directory.")
        else:
            self.current_version = version
            self.view.dashboard_game_version_label.config(text=f"v{self.current_version}")
            self.view.dashboard_status_label.config(text="Ready to check for updates.", style="Info.TLabel")
            self.view.update_plan_text.insert(tk.END, "Click 'Check for Updates' to see the required patches.")

        self.updates_to_install.clear()
        self.view.update_plan_text.config(state='disabled')
        if self.state != AppState.STARTING: self.set_state(AppState.IDLE)
        self.view.host_selector.config(state="disabled")

    def _get_ordered_links_for_update(self, update_key: str) -> List[Dict[str, str]]:
        user_selection = self.download_source_var.get()
        all_hosts_by_name = {host['name']: host for host in self.update_data.get('hosts', [])}

        if user_selection != "Automatic":
            if user_selection in all_hosts_by_name:
                host = all_hosts_by_name[user_selection]
                link = host['links'].get(update_key)
                return [{'link': link, 'host_id': host['id']}] if link else []
            return []

        ordered_links = []
        preference_order = self.update_data.get('host_preference_order', [])
        all_hosts_by_id = {host['id']: host for host in self.update_data.get('hosts', [])}
        for host_id in preference_order:
            if host_id in all_hosts_by_id:
                host = all_hosts_by_id[host_id]
                link = host['links'].get(update_key)
                if link:
                    ordered_links.append({'link': link, 'host_id': host_id})
        return ordered_links

    def check_updates(self):
        logger.log("User clicked 'Check for Updates'.", "INFO")
        if not self.update_data: messagebox.showerror("API Error", "Could not load update data."); return
        if not self.game_dir.get(): messagebox.showerror("Error", "Please select the game directory first."); return
        if not self.current_version: messagebox.showerror("Error", "Could not detect game version."); return
        try:
            latest = self.update_data.get('latest_version')
            self.view.dashboard_latest_version_label.config(text=f"v{latest}")
            if self.current_version == latest:
                self.view.dashboard_status_label.config(text="You are on the latest version!", style="Success.TLabel")
                self.view.update_dashboard_action_button.config(text=f"{Constants.ICON_CHECK} All Set!", state='disabled', style='TButton')
                self.updates_to_install.clear()
                self.view.host_selector.config(state="disabled")
                return

            versions = self.update_data.get('versions', [])
            current_idx = versions.index(self.current_version)
            update_keys = [f"{versions[i]}_{versions[i+1]}" for i in range(current_idx, len(versions)-1)]

            update_sizes = self.update_data.get('update_sizes', {});
            self.updates_to_install = []

            for i, key in enumerate(update_keys, start=current_idx):
                ordered_links = self._get_ordered_links_for_update(key)
                if not ordered_links:
                    logger.log(f"No download links found for update key {key} on any host.", "ERROR")
                    continue

                size_str = update_sizes.get(key, "0 B")
                size_bytes = 0
                try:
                    num_part_str = size_str.split()[0]
                    num_part = float(num_part_str)
                    if "MB" in size_str.upper(): size_bytes = int(num_part * 1024 * 1024)
                    elif "GB" in size_str.upper(): size_bytes = int(num_part * 1024 * 1024 * 1024)
                    elif "KB" in size_str.upper(): size_bytes = int(num_part * 1024)
                    else: size_bytes = int(num_part)
                except (ValueError, IndexError):
                    size_bytes = 0

                self.updates_to_install.append({
                    'from': versions[i],
                    'to': versions[i+1],
                    'links': ordered_links,
                    'size': size_str,
                    'size_bytes': size_bytes,
                    'key': key
                })

            self.view.update_plan_text.config(state='normal'); self.view.update_plan_text.delete(1.0, tk.END)

            if self.updates_to_install:
                self.view.update_plan_text.tag_configure("bold", font=("Segoe UI", 10))
                self.view.update_plan_text.insert(tk.END, "The following patches will be installed:\n\n", "cyan")
                total_size_bytes = 0
                for update in self.updates_to_install:
                    self.view.update_plan_text.insert(tk.END, f"• Patch from v{update['from']} to v{update['to']} (Size: {update['size']})\n", "cyan")
                    total_size_bytes += update['size_bytes']
                self.view.update_plan_text.insert(tk.END, f"\nTotal Download Size: ", "cyan")
                self.view.update_plan_text.insert(tk.END, f"~{format_bytes(total_size_bytes)}", "cyan")

                self.view.dashboard_status_label.config(text=f"{len(self.updates_to_install)} update(s) found. Ready to install.", style="Success.TLabel")
                logger.log(f"Found {len(self.updates_to_install)} updates.", "INFO")
                self.view.update_dashboard_action_button.config(text=f"{Constants.ICON_DOWNLOAD} Start Update", command=self.start_update, style="Accent.TButton", state='normal')
                self.view.host_selector.config(state="readonly")
            else:
                self.view.update_plan_text.insert(tk.END, "You are up to date!")
                self.view.dashboard_status_label.config(text="You are on the latest version!", style="Success.TLabel")
                self.view.update_dashboard_action_button.config(text=f"{Constants.ICON_CHECK} All Set!", state='disabled', style='TButton')
                self.view.host_selector.config(state="disabled")

        except ValueError:
            messagebox.showerror("Version Error", f"Your version (v{self.current_version}) is not in the update path. Consider manual install.")
            logger.log(f"Unrecognized version v{self.current_version} in path.", "ERROR")
            self.view.dashboard_status_label.config(text="Your version is not on the official update path.", style="Error.TLabel")
            self.updates_to_install.clear()
        except (KeyError, IndexError) as e:
            messagebox.showerror("Update Check Failed", f"Update data is malformed or incomplete.\nDetails: Missing key {e}\nCheck logs for details.")
            logger.log(f"Failed during update check due to malformed data: {e}", "CRITICAL")
        except Exception as e:
            messagebox.showerror("Update Check Failed", f"An unexpected error occurred: {e}\nCheck logs for details.")
            logger.log(f"Failed during update check: {e}", "CRITICAL")

        self.view.update_plan_text.config(state='disabled')
        self.set_state(AppState.IDLE)
        self.view.refresh_logs()

    def is_game_running(self) -> bool:
        return any(f'{Constants.GAME_EXECUTABLE}' in p.info['name'].lower() for p in psutil.process_iter(['name']))

    def _cleanup_all_partial_downloads(self, preserve_significant_progress: bool = False):
        """Comprehensive cleanup of all partial download state to prevent UI issues on restart."""
        try:
            if preserve_significant_progress:
                logger.log("Cleaning up partial downloads while preserving significant progress...", "INFO")
            else:
                logger.log("Cleaning up all partial download state before starting new update...", "INFO")
            
            # Clear the cache directory of partial downloads and progress files
            if Constants.CACHE_DIR.exists():
                for file_path in Constants.CACHE_DIR.iterdir():
                    try:
                        if file_path.is_file():
                            should_remove = False
                            
                            # Remove non-download files unconditionally
                            if file_path.name.endswith(('.tmp', '.progress.bak', '.hostinfo.bak')):
                                should_remove = True
                            
                            # Handle progress files and main downloads more carefully
                            elif file_path.name.endswith(('.progress', '.hostinfo', '.zip')):
                                if preserve_significant_progress:
                                    if file_path.name.endswith('.zip'):
                                        # Smart host-aware progress preservation for ZIP files
                                        try:
                                            file_size = file_path.stat().st_size
                                            progress_file = file_path.with_suffix('.progress')
                                            hostinfo_file = file_path.with_suffix('.hostinfo')
                                            
                                            if progress_file.exists() and hostinfo_file.exists():
                                                # Read host info and progress data
                                                try:
                                                    with hostinfo_file.open("r", encoding='utf-8') as hf:
                                                        host_info = {}
                                                        for line in hf:
                                                            if line.strip():
                                                                key, value = line.strip().split('=', 1)
                                                                host_info[key] = value
                                                    
                                                    expected_size = int(host_info.get('file_size', '0'))
                                                    current_host_id = host_info.get('host_id', '')
                                                    
                                                    if expected_size > 0:
                                                        completion_percentage = (file_size / expected_size * 100)
                                                        
                                                        # SMART HOST LOGIC: Only preserve if >60% AND continuing with same host
                                                        # OR if >60% and we want to prioritize this host due to significant progress
                                                        if completion_percentage > 60:
                                                            logger.log(f"Smart preserve: {file_path.name} ({completion_percentage:.1f}% from host {current_host_id})", "INFO")
                                                            logger.log(f"Host lock: Will prioritize host {current_host_id} due to >60% progress", "SETTING")
                                                            continue  # Skip removal - preserve this significant progress
                                                        elif completion_percentage > 0:
                                                            # Allow resume from any size with same host, but remove if switching hosts
                                                            logger.log(f"Preserving same-host progress: {file_path.name} ({completion_percentage:.1f}%)", "INFO")
                                                            continue  # Keep for same-host resume
                                                        else:
                                                            should_remove = True  # No meaningful progress
                                                    else:
                                                        should_remove = True  # No valid size info
                                                except (OSError, ValueError, KeyError) as e:
                                                    logger.log(f"Could not read progress info for {file_path.name}: {e}", "WARNING")
                                                    should_remove = True  # Error reading, remove to be safe
                                            else:
                                                # No progress/hostinfo files, preserve larger files for potential resume
                                                if file_size > 10 * 1024 * 1024:  # >10MB might be worth preserving
                                                    logger.log(f"Preserving untracked file: {file_path.name} ({format_bytes(file_size)})", "INFO")
                                                    continue
                                                else:
                                                    should_remove = True  # Small file, not worth preserving
                                                    
                                        except (OSError, ValueError):
                                            should_remove = True  # Error checking, remove to be safe
                                    elif file_path.name.endswith(('.progress', '.hostinfo')):
                                        # For progress/hostinfo files, check if corresponding zip exists and should be preserved
                                        zip_file = file_path.with_suffix('').with_suffix('.zip')  # Remove .progress/.hostinfo and add .zip
                                        if zip_file.exists():
                                            try:
                                                zip_size = zip_file.stat().st_size
                                                if zip_size > 10 * 1024 * 1024:  # If zip is >10MB, preserve tracking files too
                                                    logger.log(f"Preserving tracking file for large download: {file_path.name}", "INFO")
                                                    continue  # Keep tracking file with its zip
                                                else:
                                                    should_remove = True  # Small zip, remove tracking
                                            except (OSError, ValueError):
                                                should_remove = True  # Error checking zip, remove tracking
                                        else:
                                            should_remove = True  # No corresponding zip file
                                    else:
                                        should_remove = True  # Not a zip file and not preserving
                                else:
                                    should_remove = True  # Not preserving or not a download file
                            
                            if should_remove:
                                file_path.unlink(missing_ok=True)
                                logger.log(f"Removed partial file: {file_path.name}", "INFO")
                                
                    except (OSError, PermissionError) as e:
                        logger.log(f"Could not remove {file_path.name}: {e}", "WARNING")
            
            # Reset download state variables
            if hasattr(self, 'downloader_pause_event'):
                self.downloader_pause_event.set()  # Ensure not paused
            if hasattr(self, 'updater_cancel_event'):
                self.updater_cancel_event.clear()  # Clear cancel flag
                
            # Clear any lingering progress queue messages
            try:
                while True:
                    self.progress_queue.get_nowait()
            except queue.Empty:
                pass  # Queue is now empty
                
            logger.log("Partial download cleanup completed.", "INFO")
            
        except Exception as e:
            logger.log(f"Error during partial download cleanup: {e}", "WARNING")
            # Don't fail the update start due to cleanup issues

    @manage_state(AppState.UPDATING)
    def start_update(self):
        logger.log("User clicked 'Start Update'.", "INFO")
        
        # --- SMART CLEANUP: Preserve significant progress while cleaning up problematic state ---
        self._cleanup_all_partial_downloads(preserve_significant_progress=True)
        
        # --- UI RESET: Always reset updater UI state before starting a new update ---
        self.view.updater_status_label.config(text="Status: Initializing smart download system...")
        self.view.updater_overall_label.config(text="Overall: Preparing intelligent multi-host download...")
        self.view.updater_bar.config(value=0, mode='determinate')
        if hasattr(self.view, 'updater_cancel_button'):
            self.view.updater_cancel_button.config(state='normal', text=f"{Constants.ICON_TIMES} Cancel")
        if hasattr(self.view, 'updater_pause_button'):
            self.view.updater_pause_button.config(text=f"{Constants.ICON_PAUSE} Pause", state='normal')

        if self.is_game_running(): messagebox.showwarning("Game Running", f"Please close {Constants.GAME_EXECUTABLE} before updating."); self.set_state(AppState.IDLE); return
        if not self.updates_to_install: messagebox.showerror("Error", "No updates selected."); self.set_state(AppState.IDLE); return
        latest = self.update_data.get('latest_version', 'the latest version')
        total_patches = len(self.updates_to_install)
        total_hosts = len(self.update_data.get('hosts', []))
        
        # Check if user selected a specific host or automatic mode
        selected_source = self.download_source_var.get()
        is_single_host = selected_source != "Automatic"
        
        if is_single_host:
            # Single host mode - simpler messaging
            prompt = f"� UPDATE: v{self.current_version} → v{latest}\n\n{total_patches} patch(es) will be downloaded from {selected_source}\n\n⚡ Features:\n• Resume support on interruptions\n• Progress tracking\n• Automatic retries\n\nProceed with update?"
            dialog_title = "Confirm Update"
        else:
            # Multi-host smart mode - advanced messaging
            prompt = f"�🚀 SMART UPDATE: v{self.current_version} → v{latest}\n\n📦 {total_patches} patch(es) will be downloaded using our intelligent multi-host system\n🌐 {total_hosts} download sources available for maximum speed and reliability\n\n⚡ Features:\n• Automatic fastest host selection\n• Instant failover to backup hosts\n• Smart resume on interruptions\n• Enhanced progress tracking\n\nProceed with smart update?"
            dialog_title = "Confirm Smart Update"
            
        if not messagebox.askyesno(dialog_title, prompt): self.set_state(AppState.IDLE); return
        if self.is_game_running(): messagebox.showwarning("Game Running", f"It looks like {Constants.GAME_EXECUTABLE} was started. Please close it before updating."); self.set_state(AppState.IDLE); return

        logger.log(f"UPDATE MODE: {'Single Host (' + selected_source + ')' if is_single_host else 'Smart Multi-Host'} | Checksum verification: {'enabled' if self.verify_checksum_enabled.get() else 'disabled'}", "SETTING")
        for update in self.updates_to_install:
            update['links'] = self._get_ordered_links_for_update(update['key'])

        self.view.show_progress_view("Updater")
        
        # Set appropriate UI messaging based on mode
        if is_single_host:
            # Single host mode - simple messaging
            self.view.updater_status_label.config(text=f"Status: Connecting to {selected_source}...")
            self.view.updater_overall_label.config(text=f"Overall: Preparing download from {selected_source}...")
            status_msg = f"📦 UPDATE: Starting download from {selected_source}"
            overall_msg = f"📡 Connecting to {selected_source} for {total_patches} patch(es)..."
        else:
            # Multi-host smart mode - advanced messaging  
            self.view.updater_status_label.config(text="Status: 🧠 Smart download system initializing...")
            self.view.updater_overall_label.config(text="Overall: 🚀 Preparing intelligent multi-host download...")
            status_msg = f"🚀 SMART UPDATE: Initializing for {total_patches} patch(es)..."
            overall_msg = f"🧠 Smart system: Testing {total_hosts} hosts for optimal speed..."
        self.view.updater_bar.config(value=0, mode='determinate')
        
        # Force immediate UI refresh to ensure changes are visible
        self.view.update_idletasks()
        self.view.update()  # Force an immediate UI update
        
        # Send appropriate status messages to queue based on mode
        self.progress_queue.put({'type': Q_MSG.STATUS, 'message': status_msg})
        self.progress_queue.put({'type': Q_MSG.OVERALL_STATUS, 'message': overall_msg})
        
        # Process the queue immediately to show these updates
        self.process_queue()
        
        self.updater_cancel_event.clear()
        self.downloader_pause_event.set()
        self.view.updater_pause_button.config(text=f"{Constants.ICON_PAUSE} Pause", command=self.pause_resume_download)
        self.view.updater_cancel_button.config(command=self.cancel_update)

        workflow = UpdateWorkflow(self.game_dir.get(), Constants.CACHE_DIR, self.updates_to_install, self.update_data, self.progress_queue, self.updater_cancel_event, self.downloader_pause_event, self.verify_checksum_enabled.get(), self.decision_queue)
        
        # Enhanced heartbeat with appropriate messaging based on mode
        def update_heartbeat():
            counter = 0
            while self.state == AppState.UPDATING and not self.updater_cancel_event.is_set():
                counter += 1
                if counter % 5 == 0:  # Every 5 seconds - keep user informed
                    if is_single_host:
                        self.progress_queue.put({
                            'type': Q_MSG.STATUS, 
                            'message': f"📡 Downloading from {selected_source} | Runtime: {counter}s"
                        })
                    else:
                        self.progress_queue.put({
                            'type': Q_MSG.STATUS, 
                            'message': f"🧠 Smart system operational | Runtime: {counter}s | Multi-host active"
                        })
                time.sleep(1)
        
        # Start enhanced heartbeat in background
        threading.Thread(target=update_heartbeat, daemon=True).start()
        
        self.task_manager.submit(workflow.run)
        
        # Initial queue processing for immediate response
        # Single immediate queue processing (removed redundant calls)
        self.view.after(1, self.process_queue)

    def cancel_update(self):
        if self.state == AppState.UPDATING:
            # Determine messaging based on current mode
            selected_source = self.download_source_var.get()
            is_single_host = selected_source != "Automatic"
            
            if is_single_host:
                dialog_message = f"Cancel download from {selected_source}?\n\nThe download will stop and partial files will be cleaned up."
                dialog_title = "Cancel Download"
                log_message = f"User initiated download cancellation from {selected_source}."
                status_message = "Status: 🛑 Cancelling download..."
            else:
                dialog_message = "Cancel the intelligent multi-host download?\n\nThe smart system will safely stop all active downloads and clean up partial files."
                dialog_title = "Cancel Smart Update"
                log_message = "User initiated smart update cancellation."
                status_message = "Status: 🛑 Cancelling smart download..."
            
            if messagebox.askyesno(dialog_title, dialog_message):
                logger.log(log_message, "INFO")
                self.downloader_pause_event.set()
                self.updater_cancel_event.set()
                self.view.updater_status_label.config(text=status_message)
                
                # Disable cancel button to prevent multiple clicks
                if hasattr(self.view, 'updater_cancel_button'):
                    if is_single_host:
                        self.view.updater_cancel_button.config(state='disabled', text=f"{Constants.ICON_TIMES} Cancelling...")
                    else:
                        self.view.updater_cancel_button.config(state='disabled', text=f"{Constants.ICON_TIMES} Stopping smart system...")
                
                # Start a timeout timer to force reset if cancellation takes too long
                def force_reset_after_timeout():
                    time.sleep(5)  # Wait 5 seconds for graceful cancellation
                    if self.state == AppState.UPDATING:
                        logger.log("Force resetting update after cancellation timeout.", "WARNING")
                        self.set_state(AppState.IDLE)
                        self.view.show_dashboard_view("Updater")
                        self.view.updater_status_label.config(text="Status: Download stopped")
                        if hasattr(self.view, 'updater_cancel_button'):
                            self.view.updater_cancel_button.config(state='normal', text=f"{Constants.ICON_TIMES} Cancel")
                
                # Start timeout thread as daemon so it doesn't block app shutdown
                threading.Thread(target=force_reset_after_timeout, daemon=True).start()
                logger.log("Update cancellation initiated with timeout protection.", "SETTING")

    def pause_resume_download(self):
        if self.state != AppState.UPDATING: return
        
        # Determine messaging based on current mode
        selected_source = self.download_source_var.get()
        is_single_host = selected_source != "Automatic"
        
        # Enhanced pause/resume with better state management
        try:
            if self.downloader_pause_event.is_set():
                # Pausing download - Enhanced robustness
                self.downloader_pause_event.clear()
                
                # Immediately update UI to prevent double-clicks
                self.view.updater_pause_button.config(text=f"{Constants.ICON_PLAY} Resume", state='disabled')
                
                # Contextual messaging
                if is_single_host:
                    self.progress_queue.put({'type': Q_MSG.STATUS, 'message': f"⏸️ Pausing download from {selected_source}..."})
                    logger.log(f"Download from {selected_source} paused by user.", "INFO")
                else:
                    self.progress_queue.put({'type': Q_MSG.STATUS, 'message': "⏸️ Pausing smart download system..."})
                    logger.log("Smart download paused by user.", "INFO")
                
                # Short delay to ensure pause takes effect, then re-enable button
                def enable_button_after_pause():
                    time.sleep(0.5)  # Allow pause to take effect
                    if self.state == AppState.UPDATING:  # Only if still updating
                        self.view.updater_pause_button.config(state='normal')
                        # Final pause confirmation
                        if is_single_host:
                            self.progress_queue.put({'type': Q_MSG.STATUS, 'message': f"⏸️ Download paused | {selected_source}"})
                        else:
                            self.progress_queue.put({'type': Q_MSG.STATUS, 'message': "⏸️ Smart download paused | Click Resume to continue"})
                
                threading.Thread(target=enable_button_after_pause, daemon=True).start()
                
            else:
                # Resuming download - Enhanced robustness
                self.downloader_pause_event.set()
                
                # Immediately update UI
                self.view.updater_pause_button.config(text=f"{Constants.ICON_PAUSE} Pause")
                
                # Contextual messaging
                if is_single_host:
                    self.progress_queue.put({'type': Q_MSG.STATUS, 'message': f"▶️ Resuming download from {selected_source}..."})
                    logger.log(f"Download from {selected_source} resumed by user.", "INFO")
                else:
                    self.progress_queue.put({'type': Q_MSG.STATUS, 'message': "▶️ Resuming smart download system..."})
                    logger.log("Smart download resumed by user.", "INFO")
                
                # Brief delay for resume confirmation
                def confirm_resume():
                    time.sleep(0.3)
                    if self.state == AppState.UPDATING and self.downloader_pause_event.is_set():
                        if is_single_host:
                            self.progress_queue.put({'type': Q_MSG.STATUS, 'message': f"▶️ Download resumed | {selected_source}"})
                        else:
                            self.progress_queue.put({'type': Q_MSG.STATUS, 'message': "▶️ Smart download resumed | Continuing..."})
                
                threading.Thread(target=confirm_resume, daemon=True).start()
                
        except Exception as e:
            logger.log(f"Error in pause/resume operation: {e}", "ERROR")
            # Ensure button state is consistent even if error occurs
            if hasattr(self.view, 'updater_pause_button'):
                self.view.updater_pause_button.config(state='normal')

    @manage_state(AppState.BUSY)
    def launch_game(self, *args):
        error = GameManager(self.game_dir.get()).launch_game()
        if error: 
            messagebox.showerror("Launch Error", error)
        else:
            # Start monitoring for game exit to auto-restore IDLE state
            self._start_game_exit_monitor()

    @manage_state(AppState.BUSY)
    def backup_saved_games(self):
        self.task_manager.submit(
            GameManager(self.game_dir.get()).backup_saved_games,
            on_done=self._on_utility_complete,
            on_error=lambda msg: self._on_utility_error("Backup Failed", msg),
            is_utility_task=True
        )

    @manage_state(AppState.BUSY)
    def restore_backup(self):
        backup_dir = Path.home() / "Saved Games" / "Cricket 26 Backups"
        if not backup_dir.exists() or not any(backup_dir.glob('*.zip')): messagebox.showinfo("No Backups", f"No backups found in:\n{backup_dir}"); self.set_state(AppState.IDLE); return
        backup_to_restore = filedialog.askopenfilename(title="Select Backup to Restore", initialdir=backup_dir, filetypes=[("Backup Files", "*.zip")])
        if not backup_to_restore: self.set_state(AppState.IDLE); return
        if not messagebox.askyesno("Confirm Restore", "This will permanently delete your CURRENT save data and replace it with the backup.\n\nThis is your final confirmation. Are you sure?", icon='warning'): self.set_state(AppState.IDLE); return

        self.task_manager.submit(
            GameManager(self.game_dir.get()).restore_backup,
            on_done=self._on_utility_complete,
            on_error=lambda msg: self._on_utility_error("Restore Failed", msg),
            is_utility_task=True,
            kwargs={'backup_zip_path_str': backup_to_restore}
        )

    def _start_game_exit_monitor(self):
        """Start monitoring for game exit to automatically restore IDLE state."""
        def monitor_game_exit():
            # Wait a bit for game to fully start
            time.sleep(3)
            while True:
                if not self.is_game_running():
                    # Game has exited, restore IDLE state
                    logger.log("Game exited, restoring IDLE state.", "INFO")
                    self.set_state(AppState.IDLE)
                    break
                time.sleep(2)  # Check every 2 seconds
        
        # Start monitoring in background thread
        threading.Thread(target=monitor_game_exit, daemon=True).start()

    def manual_install(self):
        logger.log("User clicked 'Manual Install'.", "INFO");
        if self.state != AppState.IDLE: return
        if not self.game_dir.get(): messagebox.showerror("Error", "Please select the game directory first."); return
        zip_path_str = filedialog.askopenfilename(title="Select Update Archive", filetypes=[("Archives", "*.zip *.rar *.7z")]);
        if not zip_path_str: return

        self.set_state(AppState.MANUAL_INSTALLING)
        self.view.show_progress_view("Updater")
        self.view.updater_pause_button.config(state='disabled')
        self.view.updater_cancel_button.config(command=lambda: self.progress_queue.put({'type': Q_MSG.CANCELLED}))

        def _hasher_task(zip_path: Path):
            self.progress_queue.put({'type': Q_MSG.OVERALL_STATUS, 'message': f"Verifying file: {zip_path.name}..."});
            sha256 = hashlib.sha256()
            with open(zip_path, "rb") as f:
                while chunk := f.read(4 * 1024 * 1024): sha256.update(chunk)
            calculated_hash = sha256.hexdigest().lower()
            checksums_data = (self.update_data or {}).get('checksums', {})
            matched_key = next((k for k, v in checksums_data.items() if isinstance(v, str) and v.lower() == calculated_hash), None)
            return {'path': str(zip_path), 'matched': matched_key}

        self.task_manager.submit(
            _hasher_task,
            on_done=lambda data: self.progress_queue.put({'type': Q_MSG.MANUAL_INSTALL_CONFIRM, 'data': data}),
            on_error=self._on_manual_install_error,
            kwargs={'zip_path': Path(zip_path_str)}
        )

    def _manual_install_installer(self, zip_path: Path):
        self.set_state(AppState.MANUAL_INSTALLING)
        self.progress_queue.put({'type': Q_MSG.OVERALL_STATUS, 'message': f"Installing {zip_path.name}"});
        self.progress_queue.put({'type': Q_MSG.STATUS, 'message': f"Extracting..."});

        def _installer_task():
            with tempfile.TemporaryDirectory() as extract_dir:
                Extractor().extract_archive(zip_path, Path(extract_dir), self.progress_queue, self.updater_cancel_event)
                Extractor().install_files(Path(extract_dir), Path(self.game_dir.get()), self.progress_queue, self.updater_cancel_event)
            return None

        def _on_done(result):
            self.progress_queue.put({'type': Q_MSG.MANUAL_INSTALL_COMPLETE})

        def _on_error(message):
            self._on_manual_install_error(message)

        self.task_manager.submit(_installer_task, on_done=_on_done, on_error=_on_error)


    def _open_folder(self, path: Path, not_found_msg: str):
        if not path or not path.exists():
            try: path.mkdir(parents=True, exist_ok=True)
            except OSError as e:
                logger.log(f"Could not create folder {path}: {e}", "ERROR")
                messagebox.showerror("Error", f"Could not create folder:\n{path}")
                return
        webbrowser.open(os.path.realpath(path)); logger.log(f"Opened folder: {path}", "INFO")

    def open_game_dir(self): self._open_folder(Path(self.game_dir.get()) if self.game_dir.get() else None, "Game directory is not selected.")
    def open_save_dir(self): self._open_folder(Path.home() / "Saved Games" / "Cricket 26", "Save game folder not found.")
    def open_backups_dir(self): self._open_folder(Path.home() / "Saved Games" / "Cricket 26 Backups", "Backups folder not found.")

    @manage_state(AppState.BUSY)
    def create_cricket26_shortcuts(self):
        """Create Cricket 26 shortcuts for Windows Start Menu."""
        if not self.game_dir.get():
            messagebox.showerror("Error", "Please select the Cricket 26 game directory first.")
            self.set_state(AppState.IDLE)
            return
            
        game_exe = Path(self.game_dir.get()) / Constants.GAME_EXECUTABLE
        if not game_exe.exists():
            messagebox.showerror("Error", f"{Constants.GAME_EXECUTABLE} not found in the selected directory.\nPlease select a valid Cricket 26 directory.")
            self.set_state(AppState.IDLE)
            return

        def _create_shortcuts_task():
            try:
                game_dir = Path(self.game_dir.get())
                game_exe_path = str(game_exe)
                game_dir_path = str(game_dir)
                
                results = []
                
                # Create Start Menu shortcut for current user
                powershell_cmd = f"""
                $startMenu = [Environment]::GetFolderPath('StartMenu')
                $gamesFolder = Join-Path $startMenu 'Programs\\Games'
                if (!(Test-Path $gamesFolder)) {{ New-Item -ItemType Directory -Path $gamesFolder -Force }}
                $s = (New-Object -ComObject WScript.Shell).CreateShortcut((Join-Path $gamesFolder 'Cricket 26.lnk'))
                $s.TargetPath = '{game_exe_path}'
                $s.WorkingDirectory = '{game_dir_path}'
                $s.Description = 'Cricket 26 Game'
                $s.IconLocation = '{game_exe_path},0'
                $s.Save()
                Write-Host 'Start Menu shortcut created'
                """
                
                proc = subprocess.run(['powershell', '-NoProfile', '-ExecutionPolicy', 'Bypass', '-Command', powershell_cmd], 
                                    capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW)
                if proc.returncode == 0:
                    results.append("✓ Start Menu shortcut created")
                else:
                    results.append("⚠ Start Menu shortcut creation failed")
                
                # Refresh Start Menu cache
                try:
                    subprocess.run(['powershell', '-Command', 
                                  "Get-Process -Name StartMenuExperienceHost -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue; Start-Sleep 1"], 
                                  capture_output=True, creationflags=subprocess.CREATE_NO_WINDOW, timeout=10)
                    results.append("✓ Start Menu cache refreshed")
                except:
                    results.append("⚠ Start Menu cache refresh skipped")
                
                logger.log("Cricket 26 shortcuts creation completed", "INFO")
                
                success_message = "Cricket 26 shortcuts created successfully!\n\n" + "\n".join(results)
                success_message += "\n\nCricket 26 should now be:\n"
                success_message += "• Searchable in Start Menu (type 'Cricket' or 'Cricket 26')\n"
                success_message += "• Pinnable to Start Menu and Taskbar\n\n"
                success_message += "Note: Shortcut created for current user only."
                
                return success_message
                
            except Exception as e:
                logger.log(f"Error creating Cricket 26 shortcuts: {e}", "ERROR")
                raise RuntimeError(f"Failed to create shortcuts: {e}")

        self.task_manager.submit(
            _create_shortcuts_task,
            on_done=self._on_utility_complete,
            on_error=lambda msg: self._on_utility_error("Shortcut Creation Failed", msg),
            is_utility_task=True
        )

    def update_cache_size_label(self):
        def _task():
            if not Constants.CACHE_DIR.exists(): return "0 B"
            total_size = sum(f.stat().st_size for f in Constants.CACHE_DIR.glob('**/*') if f.is_file()); return format_bytes(total_size)

        self.task_manager.submit(_task, on_done=lambda s: self.view.cache_size_label.config(text=f"Size: {s}"))

    @manage_state(AppState.BUSY)
    def clear_download_cache(self):
        cache_dir = Constants.CACHE_DIR
        if not cache_dir.exists() or not any(cache_dir.iterdir()):
            messagebox.showinfo("Cache Empty", "The download cache is already empty.")
            self.set_state(AppState.IDLE)
            return

        total_size = sum(f.stat().st_size for f in cache_dir.glob('**/*') if f.is_file())
        if not messagebox.askyesno("Confirm Clear Cache", f"This will delete all cached update files, freeing up {format_bytes(total_size)}.\n\nAre you sure?", icon='warning'):
            self.set_state(AppState.IDLE)
            return

        def _clear_cache_worker(cd: Path):
            for item in cd.iterdir():
                if item.is_dir(): shutil.rmtree(item)
                else: item.unlink()
            return "The download cache has been cleared successfully."

        def _on_clear_cache_done(message: str):
            self._on_utility_complete(message)
            self.update_cache_size_label()

        self.task_manager.submit(
            _clear_cache_worker,
            on_done=_on_clear_cache_done,
            on_error=lambda msg: self._on_utility_error("Clear Cache Failed", msg),
            is_utility_task=True,
            kwargs={'cd': cache_dir}
        )

    @manage_state(AppState.BUSY)
    def clear_all_downloads(self):
        """Clear all cached downloads from the updater."""
        cache_dir = Constants.CACHE_DIR
        if not cache_dir.exists() or not any(cache_dir.iterdir()):
            messagebox.showinfo("No Downloads", "There are no cached downloads to clear.")
            self.set_state(AppState.IDLE)
            return

        total_size = sum(f.stat().st_size for f in cache_dir.glob('**/*') if f.is_file())
        if not messagebox.askyesno("Clear All Downloads", f"This will permanently delete all downloaded update files ({format_bytes(total_size)}).\n\nContinue?", icon='warning'):
            self.set_state(AppState.IDLE)
            return

        def _clear_worker(cd: Path):
            for item in cd.iterdir():
                if item.is_dir(): shutil.rmtree(item)
                else: item.unlink()
            return "All downloads cleared successfully."

        def _on_done(msg: str):
            self._on_utility_complete(msg)
            self.update_cache_size_label()

        self.task_manager.submit(
            _clear_worker,
            on_done=_on_done,
            on_error=lambda msg: self._on_utility_error("Clear Failed", msg),
            is_utility_task=True,
            kwargs={'cd': cache_dir}
        )

    def _relaunch_as_admin(self, extra_arg: str = ""):
        logger.log(f"Attempting to relaunch with admin privileges. Extra arg: {extra_arg}", "SETTING")
        try:
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, f'"{sys.argv[0]}" {extra_arg}', None, 1)
            self.view.after(500, self.on_closing)
        except Exception as e:
            logger.log(f"Failed to relaunch as admin: {e}", "ERROR")
            messagebox.showerror("Elevation Failed", f"Could not restart with Admin rights:\n{e}")

    def _get_active_interface(self) -> Optional[str]:
        try:
            interfaces = psutil.net_if_addrs()
            stats = psutil.net_if_stats()
            
            active_adapters = []
            for intf, addrs in interfaces.items():
                if stats[intf].isup and "Loopback" not in intf:
                    if any(addr.family == socket.AF_INET for addr in addrs):
                        active_adapters.append(intf)
            
            if not active_adapters: return None
            if len(active_adapters) == 1: return active_adapters[0]

            return self.view.ask_user_to_select_interface(active_adapters)

        except Exception as e:
            logger.log(f"Could not get network interface: {e}", "ERROR")
            return None


    @require_admin(relaunch_arg='--set-dns-from-failure')
    def set_dns_from_failure(self): self._run_dns_command(set_dns=True, from_failure_flow=True)

    @require_admin(relaunch_arg='--set-dns')
    def set_dns(self): self._run_dns_command(set_dns=True)

    @require_admin(relaunch_arg='--reset-dns')
    def reset_dns(self): self._run_dns_command(set_dns=False)

    @manage_state(AppState.BUSY)
    def reset_proxy(self):
        """Reset Windows HTTP proxy settings."""
        def _task():
            command = ['netsh', 'winhttp', 'reset', 'proxy']
            subprocess.run(command, check=True, capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW)
            logger.log(f"Proxy reset successful: {' '.join(command)}", "INFO")
            return "Windows HTTP proxy settings have been reset successfully."

        def _on_done(msg: str):
            messagebox.showinfo("Success", msg)
            self.set_state(AppState.IDLE)

        self.task_manager.submit(_task, on_done=_on_done, on_error=lambda msg: self._on_utility_error("Proxy Reset Failed", msg), is_utility_task=True)

    def _run_dns_command(self, set_dns: bool, from_failure_flow: bool = False):
        def _task():
            interface = self._get_active_interface()
            if not interface: 
                raise ValueError("No active network adapter found or selected.")
            
            # Backup current DNS settings before making changes
            backup_success = self._backup_current_dns(interface)
            if not backup_success and set_dns:
                logger.log("Warning: Could not backup current DNS settings", "WARNING")
            
            command = ['netsh', 'interface', 'ipv4', 'set', 'dnsserver', f'name="{interface}"']
            if set_dns: 
                command.extend(['static', '1.1.1.1', 'primary'])
            else: 
                command.append('dhcp')
            
            subprocess.run(command, check=True, capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW)
            logger.log(f"DNS command successful: {' '.join(command)}", "INFO")

        def _on_done(result):
            if from_failure_flow: 
                self.progress_queue.put({'type': Q_MSG.DOWNLOAD_FAILED})
            else: 
                messagebox.showinfo("Success", "DNS settings updated successfully!")

        self.set_state(AppState.BUSY)
        self.task_manager.submit(_task, on_done=_on_done, on_error=lambda msg: self._on_utility_error("DNS Change Failed", msg), is_utility_task=True)

    def _backup_current_dns(self, interface: str) -> bool:
        """Backup current DNS settings for the given interface."""
        try:
            # Get current DNS configuration
            result = subprocess.run(
                ['netsh', 'interface', 'ipv4', 'show', 'dns', f'name="{interface}"'], 
                capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW
            )
            
            if result.returncode == 0:
                # Save backup to a file
                backup_file = Constants.CACHE_DIR / f"dns_backup_{interface.replace(' ', '_')}.txt"
                Constants.CACHE_DIR.mkdir(exist_ok=True)
                
                backup_data = {
                    'interface': interface,
                    'timestamp': datetime.now().isoformat(),
                    'dns_config': result.stdout
                }
                
                with backup_file.open('w', encoding='utf-8') as f:
                    json.dump(backup_data, f, indent=2)
                
                logger.log(f"DNS backup created: {backup_file}", "INFO")
                return True
            else:
                logger.log(f"Failed to query DNS settings: {result.stderr}", "ERROR")
                return False
                
        except Exception as e:
            logger.log(f"DNS backup failed: {e}", "ERROR")
            return False

    def restore_dns_backup(self, interface: str = None) -> bool:
        """Restore DNS settings from backup."""
        try:
            if not interface:
                interface = self._get_active_interface()
            if not interface:
                return False
                
            backup_file = Constants.CACHE_DIR / f"dns_backup_{interface.replace(' ', '_')}.txt"
            
            if not backup_file.exists():
                logger.log("No DNS backup found for interface", "WARNING")
                return False
                
            with backup_file.open('r', encoding='utf-8') as f:
                backup_data = json.load(f)
            
            # For now, just reset to DHCP as a safe fallback
            # More sophisticated restoration could parse the backup data
            command = ['netsh', 'interface', 'ipv4', 'set', 'dnsserver', f'name="{interface}"', 'dhcp']
            result = subprocess.run(command, check=True, capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW)
            
            logger.log(f"DNS restored from backup for interface {interface}", "INFO")
            return True
            
        except Exception as e:
            logger.log(f"DNS restore failed: {e}", "ERROR")
            return False

    @manage_state(AppState.VERIFYING)
    def start_verification(self):
        logger.log("User clicked 'Verify Game Files'.", "INFO")
        if self.is_game_running(): messagebox.showwarning("Game Running", "Please close Cricket 26 before verifying."); self.set_state(AppState.IDLE); return
        if not self.game_dir.get() or not Path(self.game_dir.get()).exists(): messagebox.showerror("Error", "Please select a valid game directory first."); self.set_state(AppState.IDLE); return
        if not self.current_version: messagebox.showerror("Error", "Could not detect game version. Re-select directory."); self.set_state(AppState.IDLE); return

        self.view.show_progress_view("Verifier")
        self.verifier_scan_started = False
        self.view.verifier_bar.config(mode='indeterminate'); self.view.verifier_bar.start()
        self.view.verifier_overall_label.config(text="Status: Downloading verification data...")
        
        # Reset all verification states and UI elements
        self.last_verify_results.clear()
        self.verifier_cancel_event.clear()
        self.verifier_pause_event.set()
        
        # Reset button states and text
        self.view.verifier_pause_button.config(text=f"{Constants.ICON_PAUSE} Pause", command=self.pause_verification, state='normal')
        self.view.verifier_cancel_button.config(text=f"{Constants.ICON_TIMES} Cancel", command=self.cancel_verification, state='normal')
        self.view.verifier_status_label.config(text="Status: Downloading verification data...")
        
        # Reset missing/corrupted counters in progress view
        if hasattr(self.view, 'verifier_missing_label'):
            self.view.verifier_missing_label.config(text=f"{Constants.ICON_WARNING} Missing: 0")
        if hasattr(self.view, 'verifier_corrupted_label'):
            self.view.verifier_corrupted_label.config(text=f"{Constants.ICON_TIMES} Corrupted: 0")
        
        report_text = self.view.verify_report_text
        report_text.config(state='normal'); report_text.delete(1.0, tk.END)
        report_text.insert(tk.END, "Status: Downloading verification data...\n\n", ("Default", "StatusLine"))
        report_text.insert(tk.END, "--- Issues Found ---\n", "Header")
        report_text.config(state='disabled')

        self.task_manager.submit(self._load_manifest_worker, on_done=self._on_manifest_loaded, on_error=self._on_verify_error)

    def _load_manifest_worker(self) -> Dict:
        # Check for cancellation before starting
        if self.verifier_cancel_event.is_set():
            raise InterruptedError("Verification cancelled during initialization.")
            
        manifest_api_url = self.update_data.get('manifest_links', {}).get(self.current_version)
        if not manifest_api_url: raise ValueError(f"A verification manifest for v{self.current_version} is not available.")
        
        # Check for cancellation before download
        if self.verifier_cancel_event.is_set():
            raise InterruptedError("Verification cancelled before downloading manifest.")
            
        try:
            response = requests.get(manifest_api_url, headers={'Accept': 'application/vnd.github.v3.raw'}, timeout=15); response.raise_for_status()
            
            # Check for cancellation after download
            if self.verifier_cancel_event.is_set():
                raise InterruptedError("Verification cancelled after downloading manifest.")
                
            logger.log("Manifest downloaded successfully.", "INFO"); return response.json()
        except json.JSONDecodeError as e: logger.log(f"Failed to parse manifest JSON: {e}", "CRITICAL"); raise ValueError("Downloaded manifest file is corrupted or not valid JSON.")
        except requests.RequestException as e: logger.log(f"Failed to download manifest: {e}", "ERROR"); raise ConnectionError("Could not download the verification manifest.")

    def _on_manifest_loaded(self, manifest_data: Dict):
        logger.log("Manifest loaded, starting verifier worker.", "INFO")
        self.view.verifier_bar.stop(); self.view.verifier_bar.config(mode='determinate')
        report_text = self.view.verify_report_text; report_text.config(state='normal')
        status_range = report_text.tag_ranges("StatusLine")
        if status_range: report_text.delete(status_range[0], status_range[1])
        report_text.config(state='disabled')

        verifier = GameVerifier(Path(self.game_dir.get()), manifest_data, self.progress_queue, self.verifier_cancel_event, self.verifier_pause_event)
        self.task_manager.submit(verifier.run)

    def pause_verification(self):
        if self.verifier_pause_event.is_set(): self.verifier_pause_event.clear(); self.view.verifier_pause_button.config(text=f"{Constants.ICON_PLAY} Resume"); self.view.verifier_status_label.config(text="Status: Paused.")
        else: self.verifier_pause_event.set(); self.view.verifier_pause_button.config(text=f"{Constants.ICON_PAUSE} Pause");
        logger.log(f"Verification {'paused' if not self.verifier_pause_event.is_set() else 'resumed'}.", "SETTING")

    def cancel_verification(self):
        """Cancel verification with immediate feedback and timeout protection."""
        logger.log("User requested verification cancellation.", "INFO")
        self.verifier_cancel_event.set()
        self.verifier_pause_event.set()
        
        # Provide immediate UI feedback
        self.view.verifier_cancel_button.config(state='disabled', text=f"{Constants.ICON_TIMES} Cancelling...")
        self.view.verifier_pause_button.config(state='disabled')
        self.view.verifier_status_label.config(text="Status: Cancelling verification...")
        
        # Start a timeout timer to force reset if cancellation takes too long
        def force_reset_after_timeout():
            time.sleep(3)  # Wait 3 seconds for graceful cancellation
            if self.state == AppState.VERIFYING:
                logger.log("Force resetting verification after timeout.", "WARNING")
                self.set_state(AppState.IDLE)
                self.view.show_dashboard_view("Verifier")
                self._reset_verifier_ui("Verification cancelled (timeout).")
        
        threading.Thread(target=force_reset_after_timeout, daemon=True).start()
        logger.log("Verification cancellation initiated.", "SETTING")

    def generate_full_report_text(self, r: dict) -> str:
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        summary_lines = [
            f"Full Game Verification Report - {ts}", "=" * 60,
            f"SUMMARY: {len(r.get('good', []))} Good, {len(r.get('missing', []))} Missing, {len(r.get('corrupted', []))} Corrupted, {len(r.get('unreadable', []))} Unreadable, {len(r.get('extra', []))} Extra files.",
            "\n--- CORRUPTED FILES (Hash mismatch) ---", '\n'.join(p.replace('/', os.sep) for p in r.get('corrupted', [])) or "None.",
            "\n--- MISSING FILES (Expected but not found) ---", '\n'.join(p.replace('/', os.sep) for p in r.get('missing', [])) or "None.",
            "\n--- UNREADABLE FILES (Check Permissions) ---", '\n'.join(p.replace('/', os.sep) for p in r.get('unreadable', [])) or "None.",
            "\n--- EXTRA FILES (Not in manifest) ---", '\n'.join(p.replace('/', os.sep) for p in r.get('extra', [])) or "None.",
            "\n--- GOOD FILES (Verified OK) ---", '\n'.join(p.replace('/', os.sep) for p in r.get('good', [])) or "None."
        ]
        return "\n".join(summary_lines)

    @manage_state(AppState.BUSY)
    def save_report(self, mode: str):
        if not self.last_verify_results: 
            messagebox.showwarning("No Data", "No verification results to save.")
            self.set_state(AppState.IDLE)
            return
            
        title = f"Save {mode.title()} Report" if mode == 'full' else "Save Problem List"
        initial_file = f"Cricket26_{mode.title()}_Report_{self.current_version}.txt"
        file_path_str = filedialog.asksaveasfilename(
            title=title, 
            defaultextension=".txt", 
            filetypes=[("Text Files", "*.txt")], 
            initialfile=initial_file
        )
        if not file_path_str: 
            self.set_state(AppState.IDLE)
            return

        def _task():
            r = self.last_verify_results
            if mode == 'full':
                report_str = self.generate_full_report_text(r)
            else:
                # Simple problem report - only file paths for Discord forwarding
                corrupted_files = r.get('corrupted', [])
                missing_files = r.get('missing', [])
                unreadable_files = r.get('unreadable', [])
                
                # Combine all problem files and convert paths to Windows format
                all_problem_files = corrupted_files + missing_files + unreadable_files
                problem_paths = [p.replace('/', os.sep) for p in all_problem_files]
                
                # Only file paths, no headers or descriptions
                report_str = '\n'.join(problem_paths)
            
            Path(file_path_str).write_text(report_str, encoding='utf-8')
            logger.log(f"Saved '{mode}' verification report to {file_path_str}", "INFO")
            return f"Report saved to:\n{file_path_str}"

        self.task_manager.submit(_task, on_done=self._on_utility_complete, on_error=lambda msg: self._on_utility_error("Save Report Failed", msg), is_utility_task=True)

    def copy_problem_files_list(self):
        """Copy only the file paths of problematic files to clipboard - no headers or descriptions."""
        if not self.last_verify_results: 
            return
            
        corrupted_files = self.last_verify_results.get('corrupted', [])
        missing_files = self.last_verify_results.get('missing', [])
        unreadable_files = self.last_verify_results.get('unreadable', [])
        
        # Combine all problem files
        all_problem_files = corrupted_files + missing_files + unreadable_files
        
        if not all_problem_files: 
            messagebox.showinfo("No Files", "No problematic files found to copy.")
            return
            
        # Convert to Windows paths and copy only the file paths - nothing else
        problem_paths = [p.replace('/', os.sep) for p in all_problem_files]
        clipboard_text = "\n".join(problem_paths)
        
        self.view.clipboard_clear()
        self.view.clipboard_append(clipboard_text)
        
        messagebox.showinfo("Copied to Clipboard", f"{len(all_problem_files)} problem file paths copied to clipboard.")
        logger.log("Copied clean problem files list to clipboard.", "INFO")

    @manage_state(AppState.BUSY)
    def export_diagnostics_results(self):
        """Export comprehensive diagnostics results including all scan data."""
        if not self.last_diag_report and not self.last_verify_results:
            messagebox.showwarning("No Data", "No diagnostics or verification results available to export.")
            self.set_state(AppState.IDLE)
            return
            
        file_path = filedialog.asksaveasfilename(
            title="Export Diagnostics Results",
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt"), ("JSON Files", "*.json"), ("All Files", "*.*")],
            initialfile=f"Cricket26_Diagnostics_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        )
        
        if not file_path:
            self.set_state(AppState.IDLE)
            return
        
        def _task():
            results = {
                'export_timestamp': datetime.now().isoformat(),
                'game_directory': self.game_dir.get(),
                'diagnostics_data': self.last_diag_report if self.last_diag_report else {},
                'verification_data': self.last_verify_results if self.last_verify_results else {},
                'system_info': {
                    'platform': platform.platform(),
                    'python_version': platform.python_version(),
                    'app_version': Constants.APP_VERSION
                }
            }
            
            if file_path.lower().endswith('.json'):
                # Export as JSON for programmatic access
                import json
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(results, f, indent=2, ensure_ascii=False)
            else:
                # Export as formatted text for human reading
                export_text = f"""CRICKET 26 DIAGNOSTICS EXPORT
Generated: {results['export_timestamp']}
Game Directory: {results['game_directory']}
App Version: {Constants.APP_VERSION}

{'='*60}
SYSTEM INFORMATION
{'='*60}
Platform: {results['system_info']['platform']}
Python Version: {results['system_info']['python_version']}

"""
                
                if results['diagnostics_data']:
                    export_text += f"""{'='*60}
DIAGNOSTICS REPORT
{'='*60}
{results['diagnostics_data'].get('summary', 'No summary available')}

Performance Metrics:
{results['diagnostics_data'].get('performance', 'No performance data')}

Game Crashes (Last 5):
{results['diagnostics_data'].get('crashes', 'No crash data')}

"""
                
                if results['verification_data']:
                    verify_data = results['verification_data']
                    total_files = verify_data.get('total_files', 0)
                    corrupted = verify_data.get('corrupted', [])
                    missing = verify_data.get('missing', [])
                    unreadable = verify_data.get('unreadable', [])
                    
                    export_text += f"""{'='*60}
FILE VERIFICATION RESULTS
{'='*60}
Total Files Scanned: {total_files}
Corrupted Files: {len(corrupted)}
Missing Files: {len(missing)}
Unreadable Files: {len(unreadable)}

"""
                    
                    if corrupted:
                        export_text += "CORRUPTED FILES:\n"
                        for file_path in corrupted:
                            export_text += f"  • {file_path}\n"
                        export_text += "\n"
                    
                    if missing:
                        export_text += "MISSING FILES:\n"
                        for file_path in missing:
                            export_text += f"  • {file_path}\n"
                        export_text += "\n"
                    
                    if unreadable:
                        export_text += "UNREADABLE FILES:\n"
                        for file_path in unreadable:
                            export_text += f"  • {file_path}\n"
                        export_text += "\n"
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(export_text)
            
            return f"Diagnostics results exported to:\n{file_path}"
        
        self.task_manager.submit(_task, on_done=self._on_utility_complete, on_error=lambda msg: self._on_utility_error("Export Failed", msg), is_utility_task=True)

    def prime_diagnostics_cache(self):
        logger.log("Priming diagnostics cache in background...", "DIAG")
        diag_manager = DiagnosticsManager(Path(self.game_dir.get()) if self.game_dir.get() else None)
        self.task_manager.submit(
            diag_manager.generate_report,
            on_done=self._on_diag_initial_complete,
            on_error=self._on_diagnostics_error
        )

    @manage_state(AppState.BUSY)
    def run_initial_diagnostics(self):
        if time.time() - self._last_diag_scan_time < 300:
            logger.log("Skipping redundant diagnostics scan due to cache.", "DIAG")
            self.set_state(AppState.IDLE)
            return
        diag_manager = DiagnosticsManager(Path(self.game_dir.get()) if self.game_dir.get() else None)
        self.task_manager.submit(
            diag_manager.generate_report,
            on_done=self._on_diag_partial_complete,
            on_error=lambda msg: self._on_diagnostics_error("Initial Diagnostics Failed", msg),
            is_utility_task=True
        )

    @require_admin(relaunch_arg='--run-diagnostics')
    @manage_state(AppState.DIAGNOSTICS)
    def run_full_diagnostics(self, from_admin_relaunch: bool = False):
        logger.log("User clicked 'Run Full Scan'. Admin status: {}".format("Yes" if self.is_admin else "No"), "DIAG")
        
        # Show immediate visual feedback
        if hasattr(self.view, 'diag_run_button'):
            self.view.diag_run_button.config(text="🔄 Running Full Scan...", state='disabled')
        
        # Clear any existing crash log data to ensure fresh scan
        if hasattr(self, 'last_diag_report') and 'crashes' in self.last_diag_report:
            del self.last_diag_report['crashes']
        
        diag_manager = DiagnosticsManager(Path(self.game_dir.get()) if self.game_dir.get() else None)
        self.task_manager.submit(
            diag_manager.generate_report,
            on_done=self._on_diag_full_complete,
            on_error=lambda msg: self._on_diagnostics_error("Full Diagnostics Failed", msg),
            kwargs={'full_scan':True}
        )

    @manage_state(AppState.BUSY)
    def generate_dxdiag_report(self):
        save_path = filedialog.asksaveasfilename(title="Save DxDiag Report", defaultextension=".txt", filetypes=[("Text Files", "*.txt")], initialfile=f"DxDiag_{platform.node()}_{datetime.now().strftime('%Y%m%d')}.txt")
        if not save_path: self.set_state(AppState.IDLE); return

        def _task():
            command = ['dxdiag', '/t', save_path]; logger.log(f"Executing DxDiag command: {command}", "DIAG")
            try:
                subprocess.run(command, check=True, creationflags=subprocess.CREATE_NO_WINDOW, timeout=Constants.DXDIAG_TIMEOUT_SECONDS)
                return f"DxDiag report saved to:\n{save_path}"
            except subprocess.TimeoutExpired:
                raise RuntimeError(f"DxDiag report generation timed out after {Constants.DXDIAG_TIMEOUT_SECONDS} seconds.")

        self.task_manager.submit(_task, on_done=self._on_utility_complete, on_error=lambda msg: self._on_utility_error("DxDiag Failed", msg), is_utility_task=True)

    @manage_state(AppState.BUSY)
    def save_diagnostics_report(self):
        if not self.last_diag_report: messagebox.showwarning("No Data", "No diagnostics report to save."); self.set_state(AppState.IDLE); return
        file_path = filedialog.asksaveasfilename(title="Save Scan Report", defaultextension=".txt", filetypes=[("Text Files", "*.txt")], initialfile=f"Cricket26_Scan_Report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")
        if not file_path: self.set_state(AppState.IDLE); return

        def _task():
            report_str = f"Cricket 26 Diagnostics Scan Report - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n" + "="*60 + "\n\n--- System Information ---\n"
            for key, value in self.last_diag_report.get('system', {}).items():
                report_str += f"{key+':':<35} {value}\n"
            report_str += "\n--- Game Crash Logs (Last 5) ---\n" + self.last_diag_report.get('crashes', "N/A")
            Path(file_path).write_text(report_str, encoding='utf-8')
            return f"Scan report saved to:\n{file_path}"

        self.task_manager.submit(_task, on_done=self._on_utility_complete, on_error=lambda msg: self._on_utility_error("Save Report Failed", msg), is_utility_task=True)

    @manage_state(AppState.BUSY)
    def save_logs(self):
        file_path = filedialog.asksaveasfilename(title="Export Current Log", defaultextension=".log", filetypes=[("Log Files", "*.log"), ("Text Files", "*.txt")], initialfile=Constants.LOG_FILENAME)
        if not file_path: self.set_state(AppState.IDLE); return
        def _task():
            shutil.copy(logger.log_file, file_path)
            return 'Logs exported successfully.'
        self.task_manager.submit(_task, on_done=self._on_utility_complete, on_error=lambda msg: self._on_utility_error("Export Log Failed", msg), is_utility_task=True)

    @manage_state(AppState.BUSY)
    def archive_logs(self):
        def _task():
            archive_path = logger.archive()
            self.view.reset_log_position()
            return f"Log archived as:\n{archive_path}"
        self.task_manager.submit(_task, on_done=self._on_utility_complete, on_error=lambda msg: self._on_utility_error("Archive Log Failed", msg), is_utility_task=True)

    def _on_initial_data_loaded(self, result: Tuple[Dict, str]):
        data, source = result
        self.update_data = data
        self.view.dashboard_latest_version_label.config(text=f"v{data.get('latest_version', '???')}")
        if source == 'CACHE':
            self.view.dashboard_latest_version_label.config(style='Warning.TLabel')
        logger.log(f"Initial data loaded successfully from {source}.", "INFO")
        host_names = ["Automatic"] + [host['name'] for host in self.update_data.get('hosts', [])]
        self.view.host_selector['values'] = host_names
        self.view.download_source_var.set("Automatic")
        self.update_cache_size_label()

        self.prime_diagnostics_cache()

        if self.startup_actions:
            logger.log("Initial data loaded, processing startup actions.", "INFO")
            for func, args in self.startup_actions:
                try: func(*args)
                except Exception as e: logger.log(f"Error running startup action {func.__name__}: {e}", "ERROR")
        
        self.set_state(AppState.IDLE)


    def _on_initial_data_load_error(self, message: str):
        logger.log(f"FATAL: Could not load initial data. Error: {message}", "CRITICAL")
        self.view.show_api_error()
        self.set_state(AppState.IDLE)

    def _handle_generic_error(self, message: str):
        messagebox.showerror("Error", f"{message}\n\nCheck logs for more details.")
        self.set_state(AppState.IDLE)
        if self.view.progress_frame.winfo_viewable():
             self.view.show_dashboard_view("Updater")
        if self.view.verifier_progress_frame.winfo_viewable():
            self.view.show_dashboard_view("Verifier")
            self._reset_verifier_ui("Operation failed.")
    def _on_utility_complete(self, message: str):
        messagebox.showinfo("Success", message)
        self.view.refresh_logs()

    def _on_utility_error(self, title: str, message: str):
        messagebox.showerror(title, message)
        self.view.refresh_logs()

    def _on_manual_install_error(self, message: str):
        self.view.show_dashboard_view("Updater")
        self.set_state(AppState.IDLE)
        messagebox.showerror("Manual Install Failed", message)

    def _on_diagnostics_error(self, title: str, message: str):
        # Reset the button state
        if hasattr(self.view, 'diag_run_button'):
            self.view.diag_run_button.config(text=f"{Constants.ICON_SHIELD} Run Full Scan", state='normal')
        
        self.set_state(AppState.IDLE)
        logger.log(f"Diagnostics error occurred: {title} - {message}", "ERROR")
        messagebox.showerror(title, message)

    def _on_verify_error(self, message: str):
        self.set_state(AppState.IDLE)
        self.view.show_dashboard_view("Verifier")
        
        # Check if this was a cancellation
        if "cancelled" in message.lower() or isinstance(getattr(self, '_last_verify_exception', None), InterruptedError):
            self._reset_verifier_ui("Verification cancelled.")
            # Don't show error popup for user cancellations
        else:
            self._reset_verifier_ui("Verification failed.")
            # Show single error popup
            messagebox.showerror("Verification Failed", message)

    def _handle_cancelled(self, msg: dict):
        current_state = self.state
        if current_state in [AppState.UPDATING, AppState.MANUAL_INSTALLING]:
            self.view.show_dashboard_view("Updater")
            
            # Comprehensive UI reset to prevent leftover state
            self.view.updater_status_label.config(text="Status: Update cancelled")
            self.view.updater_overall_label.config(text="Overall: Ready to begin")
            self.view.updater_bar.config(value=0, mode='determinate')
            
            # Reset button states properly
            if hasattr(self.view, 'updater_cancel_button'):
                self.view.updater_cancel_button.config(state='normal', text=f"{Constants.ICON_TIMES} Cancel")
            if hasattr(self.view, 'updater_pause_button'):
                self.view.updater_pause_button.config(text=f"{Constants.ICON_PAUSE} Pause", state='disabled')
            
            # Smart cleanup of partial state after cancellation - preserve progress if significant
            self.view.after(500, lambda: self._cleanup_all_partial_downloads(preserve_significant_progress=True))  # Delayed cleanup to allow threads to finish
                
        elif current_state == AppState.VERIFYING:
            self.view.show_dashboard_view("Verifier")
            self._reset_verifier_ui("Verification cancelled.")
        
        self.downloader_pause_event.set()
        self.set_state(AppState.IDLE)
        logger.log("Operation cancelled and UI reset completed.", "INFO")

    def _reset_verifier_ui(self, message: str):
        # Reset progress bar
        self.view.verifier_bar.stop()
        self.view.verifier_bar.config(value=0, mode='determinate')
        
        # Reset status labels
        self.view.verifier_status_label.config(text="Status: Ready")
        self.view.verifier_overall_label.config(text="Overall: Ready to begin")
        
        # Reset button states and text
        self.view.verifier_pause_button.config(text=f"{Constants.ICON_PAUSE} Pause", state='disabled')
        self.view.verifier_cancel_button.config(text=f"{Constants.ICON_TIMES} Cancel", state='disabled')
        
        # Reset missing/corrupted counters
        if hasattr(self.view, 'verifier_missing_label'):
            self.view.verifier_missing_label.config(text=f"{Constants.ICON_WARNING} Missing: 0")
        if hasattr(self.view, 'verifier_corrupted_label'):
            self.view.verifier_corrupted_label.config(text=f"{Constants.ICON_TIMES} Corrupted: 0")
        
        report_text = self.view.verify_report_text
        report_text.config(state='normal'); report_text.delete(1.0, tk.END)
        report_text.insert(tk.END, f"--- {message} ---\n"); report_text.config(state='disabled')

    def _handle_status(self, msg: dict):
        """Handle status updates with safety checks to prevent UI crashes."""
        try:
            if not hasattr(self, 'view') or not self.view.winfo_exists():
                return
            
            if self.state in [AppState.UPDATING, AppState.MANUAL_INSTALLING]:
                if hasattr(self.view, 'updater_status_label') and self.view.updater_status_label.winfo_exists():
                    self.view.updater_status_label.config(text=f"Status: {msg.get('message', '')}")
            elif self.state == AppState.VERIFYING:
                if hasattr(self.view, 'verifier_status_label') and self.view.verifier_status_label.winfo_exists():
                    self.view.verifier_status_label.config(text=f"Status: {msg.get('message', '')}")
        except (tk.TclError, AttributeError, Exception) as e:
            logger.log(f"Status update failed: {e}", "WARNING")

    def _handle_overall_status(self, msg: dict):
        """Handle overall status updates with safety checks."""
        try:
            if not hasattr(self, 'view') or not self.view.winfo_exists():
                return
            
            if self.state in [AppState.UPDATING, AppState.MANUAL_INSTALLING]:
                if hasattr(self.view, 'updater_overall_label') and self.view.updater_overall_label.winfo_exists():
                    self.view.updater_overall_label.config(text=f"{msg.get('message', '')}")
            elif self.state == AppState.VERIFYING:
                if hasattr(self.view, 'verifier_overall_label') and self.view.verifier_overall_label.winfo_exists():
                    self.view.verifier_overall_label.config(text=f"{msg.get('message', '')}")
        except (tk.TclError, AttributeError, Exception) as e:
            logger.log(f"Overall status update failed: {e}", "WARNING")

    def _handle_progress(self, msg: dict):
        """Handle progress updates with comprehensive safety checks."""
        try:
            if not hasattr(self, 'view') or not self.view.winfo_exists():
                return
            
            progress_bar = None
            if self.state in [AppState.UPDATING, AppState.MANUAL_INSTALLING]:
                if hasattr(self.view, 'updater_bar') and self.view.updater_bar.winfo_exists():
                    progress_bar = self.view.updater_bar
            elif self.state == AppState.VERIFYING:
                if hasattr(self.view, 'verifier_bar') and self.view.verifier_bar.winfo_exists():
                    progress_bar = self.view.verifier_bar
                
            if progress_bar:
                # Ensure consistent progress bar state
                current_mode = progress_bar.cget('mode')
                if current_mode == 'indeterminate':
                    progress_bar.stop()
                    progress_bar.config(mode='determinate')
                
                # Validate and clamp progress value
                progress_value = msg.get('value', 0)
                if isinstance(progress_value, (int, float)):
                    progress_value = max(0, min(100, progress_value))  # Clamp between 0-100
                    progress_bar.config(value=progress_value)
                else:
                    logger.log(f"Invalid progress value received: {progress_value}", "WARNING")
        except (tk.TclError, AttributeError, Exception) as e:
            logger.log(f"Progress update failed: {e}", "WARNING")

    def _handle_progress_mode(self, msg: dict):
        progress_bar = None
        if self.state in [AppState.UPDATING, AppState.MANUAL_INSTALLING]: 
            progress_bar = self.view.updater_bar
        elif self.state == AppState.VERIFYING: 
            progress_bar = self.view.verifier_bar
            
        if progress_bar:
            new_mode = msg.get('mode', 'determinate')
            current_mode = progress_bar.cget('mode')
            
            if new_mode == 'indeterminate' and current_mode != 'indeterminate': 
                progress_bar.config(mode='indeterminate')
                progress_bar.start()
            elif new_mode == 'determinate' and current_mode == 'indeterminate': 
                progress_bar.stop()
                progress_bar.config(mode='determinate', value=0)  # Reset to 0 when switching

    def _handle_download_retry_wait(self, msg: dict):
        self.is_in_retry_wait = True
        self.view.updater_bar.config(mode='indeterminate'); self.view.updater_bar.start()
        duration = msg.get('duration', 10)
        host_id = msg.get('host_id', 'current host')
        retry_count = msg.get('retry_count', 1)
        self.view.updater_status_label.config(text=f"Status: Host {host_id} issue. Retry {retry_count}/4 in {duration}s...")

    def _handle_download_speed(self, msg: dict):
        """Handle enhanced download speed and ETA information."""
        # Update speed display if we have enhanced UI elements (could be added to GUI later)
        current_speed = msg.get('current_speed', 0)
        eta_formatted = msg.get('eta_formatted', '--:--')
        progress_percent = msg.get('progress_percent', 0)
        peak_speed = msg.get('peak_speed', 0)
        
        # For now, store this info for potential UI enhancement
        if not hasattr(self, 'download_stats'):
            self.download_stats = {}
        
        self.download_stats.update({
            'current_speed': current_speed,
            'peak_speed': peak_speed,
            'eta': eta_formatted,
            'progress': progress_percent
        })
        
        # Could enhance status bar with this info
        if hasattr(self.view, 'updater_speed_label'):  # Future UI enhancement
            speed_text = f"Speed: {format_bytes(current_speed)}/s | Peak: {format_bytes(peak_speed)}/s | ETA: {eta_formatted}"
            self.view.updater_speed_label.config(text=speed_text)

    def _handle_download_error_retry(self, msg: dict):
        """Handle smart download error recovery suggestions."""
        analysis = msg.get('analysis', {})
        chunk_index = msg.get('chunk_index', 0)
        strategy = analysis.get('strategy', 'normal')
        
        # Log the error analysis
        logger.log(f"Download error analysis for chunk {chunk_index}: {analysis.get('suggestion', 'No specific suggestion')}", "INFO")
        
        # Handle different recovery strategies
        if strategy == 'dns_fix':
            # Offer DNS fix for SSL errors
            self.view.after(100, lambda: self._offer_dns_recovery(analysis))
        elif strategy == 'cooldown':
            # Suggest brief pause for consecutive failures
            self.view.after(100, lambda: self._offer_cooldown_recovery(analysis))
        elif strategy == 'network_check':
            # Suggest network troubleshooting
            self.view.after(100, lambda: self._offer_network_recovery(analysis))
    
    def _offer_dns_recovery(self, analysis: dict):
        """Offer DNS configuration fix for SSL-related issues."""
        if messagebox.askyesno(
            "SSL Error Recovery", 
            f"🔧 SMART ERROR RECOVERY\n\n{analysis.get('suggestion', '')}\n\nMultiple SSL/TLS errors detected. This often indicates DNS or network configuration issues.\n\nWould you like to try setting public DNS (Cloudflare) to resolve this?\n\n(Requires Admin rights)", 
            icon='warning'
        ):
            logger.log("User accepted DNS recovery suggestion", "INFO")
            self.set_dns_from_failure()
        else:
            logger.log("User declined DNS recovery suggestion", "INFO")
    
    def _offer_cooldown_recovery(self, analysis: dict):
        """Offer brief pause for consecutive failure recovery."""
        if messagebox.askyesno(
            "Smart Recovery", 
            f"🧠 SMART ERROR RECOVERY\n\n{analysis.get('suggestion', '')}\n\nMultiple consecutive failures detected. Would you like to pause for 30 seconds to allow the connection to stabilize?\n\nThis often helps resolve temporary network issues.", 
            icon='info'
        ):
            logger.log("User accepted cooldown recovery suggestion", "INFO")
            self.view.updater_status_label.config(text="Status: ⏳ Smart recovery pause (30s)...")
            # Implement a 30-second pause
            threading.Thread(target=lambda: [time.sleep(30), 
                            self.view.updater_status_label.config(text="Status: ▶️ Resuming after recovery pause...")], 
                            daemon=True).start()
        else:
            logger.log("User declined cooldown recovery suggestion", "INFO")
    
    def _offer_network_recovery(self, analysis: dict):
        """Offer network connectivity troubleshooting."""
        messagebox.showinfo(
            "Network Recovery", 
            f"🌐 SMART ERROR RECOVERY\n\n{analysis.get('suggestion', '')}\n\nTroubleshooting suggestions:\n• Check your internet connection\n• Temporarily disable VPN if active\n• Check firewall/antivirus settings\n• Try switching to mobile hotspot\n\nThe download will continue automatically with backup hosts."
        )
        logger.log("Network recovery information displayed to user", "INFO")
    
    def _add_retry_button(self):
        """Add a retry button to the updater dashboard."""
        if hasattr(self.view, 'update_dashboard_action_button') and hasattr(self, '_last_download_failure'):
            # Change the main action button to retry
            self.view.update_dashboard_action_button.config(
                text=f"{Constants.ICON_RETRY} Retry Last Download",
                command=self._retry_last_download,
                style="Accent.TButton",
                state='normal'
            )
            
            # Update status to show retry is available
            self.view.dashboard_status_label.config(
                text="Download failed. Click 'Retry Last Download' to try again.",
                style="Warning.TLabel"
            )
    
    def _show_download_retry_dialog(self, error_msg: str, is_single_host: bool):
        """Show an enhanced retry dialog with multiple options."""
        # Custom dialog for retry options
        result = messagebox.askyesnocancel(
            "Download Failed - Retry Options",
            f"{error_msg}\n\nRetry now?",
            icon='warning'
        )
        
        if result is True:  # Yes - Retry
            logger.log("User chose to retry download immediately", "INFO")
            self._retry_last_download()
        elif result is False:  # No - Don't retry, but offer DNS fix
            if not is_single_host and "SSL" in error_msg:
                if messagebox.askyesno("Network Fix", "Would you like to try setting public DNS (Cloudflare) to fix connectivity issues?\n\n(Requires Admin rights)", icon='question'):
                    self.set_dns_from_failure()
        # None/Cancel - Do nothing, user can retry manually later
    
    def _retry_last_download(self):
        """Retry the last failed download with the same settings."""
        if not hasattr(self, '_last_download_failure') or not self._last_download_failure:
            messagebox.showwarning("No Previous Download", "No previous download to retry.")
            return
        
        failure_info = self._last_download_failure
        failure_age = time.time() - failure_info['timestamp']
        
        # Check if failure is too old (more than 10 minutes)
        if failure_age > 600:  # 10 minutes
            messagebox.showwarning("Retry Expired", "The failed download is too old to retry. Please start a new download.")
            return
        
        # Restore the previous updates list
        if failure_info['updates']:
            self.updates_to_install = failure_info['updates']
            logger.log(f"Retrying download of {len(self.updates_to_install)} updates", "INFO")
            
            # Clear failure info since we're retrying
            self._last_download_failure = None
            
            # Remove retry button and restore normal state
            self._restore_normal_download_button()
            
            # Start the download again
            self.start_update()
        else:
            messagebox.showerror("Retry Error", "Cannot retry: No update information available.")
    
    def _restore_normal_download_button(self):
        """Restore the normal download button state."""
        if hasattr(self.view, 'update_dashboard_action_button'):
            self.view.update_dashboard_action_button.config(
                text=f"{Constants.ICON_DOWNLOAD} Start Update",
                command=self.start_update,
                style="Accent.TButton"
            )

    def _handle_update_complete(self, msg: dict):
        self.view.show_dashboard_view("Updater")
        self.set_state(AppState.IDLE)
        self.updates_to_install.clear()
        self.refresh_version_and_updates()
        self.downloader_pause_event.set()
        if messagebox.askquestion("Update Complete", f"Game updated to v{msg.get('final_version', 'N/A')}!\n\nLaunch game now?", icon='info') == 'yes': self.launch_game()

    def _handle_checksum_confirm(self, msg: dict):
        update_info = msg.get('update_info', {})
        proceed = messagebox.askyesno("Checksum Mismatch", f"WARNING: The downloaded file for the update to v{update_info.get('to', 'N/A')} is corrupt or has been modified.\n\nAre you sure you want to continue?", icon='warning')
        self.decision_queue.put(proceed)

    def _handle_download_failure(self, msg: Optional[dict] = None):
        # Store failure information for potential retry
        self._last_download_failure = {
            'timestamp': time.time(),
            'reason': msg.get('reason') if msg else None,
            'updates': self.updates_to_install.copy() if self.updates_to_install else []
        }
        
        self.view.show_dashboard_view("Updater")
        self.set_state(AppState.IDLE)
        
        # Determine the download mode from the current selection
        selected_source = self.download_source_var.get()
        is_single_host = selected_source != "Automatic"
        
        # Re-enable buttons regardless of failure type to prevent UI lock
        if hasattr(self.view, 'updater_cancel_button'):
            self.view.updater_cancel_button.config(state='normal', text=f"{Constants.ICON_TIMES} Cancel")
        if hasattr(self.view, 'updater_pause_button'):
            self.view.updater_pause_button.config(state='normal', text=f"{Constants.ICON_PAUSE} Pause")
        
        # Add retry button to dashboard
        self._add_retry_button()
        
        reason = msg.get('reason') if msg else None
        
        if reason:
            # Enhanced error messages with retry option
            if is_single_host:
                if "hosts failed" in reason.lower() or "SSL/TLS Error" in reason:
                    error_msg = f"🔄 DOWNLOAD FAILED - RETRY AVAILABLE\n\nDownload Failed from {selected_source}\n\n{reason}\n\nThis could be due to:\n• Network connectivity issues\n• Server temporarily unavailable\n• SSL/TLS connection problems\n• Firewall/antivirus blocking downloads\n\n❓ Would you like to:\n• Retry the same download\n• Try a different host\n• Check connection settings"
                    status_msg = f"Download from {selected_source} failed. Retry available."
                    
                    # Show retry dialog
                    self._show_download_retry_dialog(error_msg, is_single_host)
                else:
                    error_msg = f"Download Error: {reason}\n\nPlease check the logs for technical details."
                    status_msg = f"Download from {selected_source} failed. Check logs."
                    messagebox.showerror("Download Failed", error_msg)
            else:
                if "hosts failed" in reason.lower():
                    error_msg = f"🔄 SMART DOWNLOAD FAILED - RETRY AVAILABLE\n\nAll available hosts were unable to provide the update file.\n\n{reason}\n\nThis could be due to:\n• Network connectivity issues\n• Temporary server problems\n• Firewall/antivirus blocking downloads\n\n❓ Would you like to:\n• Retry the smart download\n• Try manual DNS fix\n• Check network settings"
                    status_msg = "Smart download failed. Retry available."
                    
                    # Show retry dialog
                    self._show_download_retry_dialog(error_msg, is_single_host)
                else:
                    error_msg = f"Download Error: {reason}\n\nPlease check the logs for technical details."
                    status_msg = "Smart download failed. Check logs."
            
            messagebox.showerror("Download Failed", error_msg)
            self.view.dashboard_status_label.config(text=status_msg, style="Error.TLabel")
            return
            
        # Default failure handling - offer DNS fix for multi-host, manual install for single host
        if is_single_host:
            if messagebox.askyesno("Download Failed", f"Download from {selected_source} failed. This may be a connectivity issue with this specific host.\n\nWould you like to try a different download source automatically?", icon='warning'):
                # Switch to automatic mode for retry
                self.download_source_var.set("Automatic")
                self.view.host_selector.set("Automatic")
                messagebox.showinfo("Source Changed", "Download source changed to 'Automatic' for the next attempt. You can now try the update again.")
                self.view.dashboard_status_label.config(text="Source changed to Automatic. Ready to retry.", style="Info.TLabel")
            elif messagebox.askyesno("Manual Installation", "You can also download the update files yourself and install them using the manual installer.\n\nWould you like to open the manual installer now?", icon='question'):
                try:
                    tab_names = [self.view.notebook.tab(i, "text") for i in self.view.notebook.tabs()]
                    util_tab_index = tab_names.index("Utilities")
                    self.view.notebook.select(util_tab_index)
                    self.manual_install()
                except (ValueError, tk.TclError):
                    messagebox.showerror("Error", "Could not switch to Utilities tab automatically. Please click it yourself."); logger.log("Could not find Utilities tab to switch to.", "ERROR")
            else:
                self.view.dashboard_status_label.config(text=f"Download from {selected_source} failed. No action taken.", style="Error.TLabel")
        else:
            if messagebox.askyesno("Download Failed", "The smart download system tried multiple hosts but all failed. This may be a network issue.\n\nWould you like to try an automatic fix by setting a public DNS (Cloudflare)?\n\n(This may require Admin rights.)", icon='warning'):
                self.set_dns_from_failure()
            elif messagebox.askyesno("Manual Installation", "Okay. You can also download the update files yourself and install them using the manual installer.\n\nWould you like to open the manual installer now?", icon='question'):
                try:
                    tab_names = [self.view.notebook.tab(i, "text") for i in self.view.notebook.tabs()]
                    util_tab_index = tab_names.index("Utilities")
                    self.view.notebook.select(util_tab_index)
                    self.manual_install()
                except (ValueError, tk.TclError):
                    messagebox.showerror("Error", "Could not switch to Utilities tab automatically. Please click it yourself."); logger.log("Could not find Utilities tab to switch to.", "ERROR")
            else:
                self.view.dashboard_status_label.config(text="Smart download failed. No action taken.", style="Error.TLabel")

    def _handle_verify_stats(self, msg: dict):
        if not self.verifier_scan_started:
            self.view.verifier_bar.stop(); self.view.verifier_bar.config(mode='determinate')
            self.verifier_scan_started = True
        data = msg.get('data', {})
        stats_label, missing_label, corrupted_label, file_label = self.view.verify_stats_label, self.view.verify_missing_label, self.view.verify_corrupted_label, self.view.verifier_status_label
        
        if 'status' in data: 
            file_label.config(text=f"Status: {data['status']}")
        else:
            progress_val = (data.get('total', 0) > 0 and (data.get('processed', 0) / data['total'] * 100)) or 0
            self.view.verifier_bar['value'] = progress_val
            # Update with colored icons and numbers
            stats_label.config(text=f"📊 Progress: {data.get('processed',0)}/{data.get('total',0)}")
            missing_label.config(text=f"⚠️ Missing: {data.get('missing',0)}")
            corrupted_label.config(text=f"❌ Corrupted: {data.get('corrupted',0)}")
            file_label.config(text=f"Now Scanning: {data.get('current_file','N/A')}")

    def _handle_verify_complete(self, msg: dict):
        self.last_verify_results = msg.get('results', {})
        self.view.show_dashboard_view("Verifier"); self.set_state(AppState.IDLE)
        r = self.last_verify_results
        num_missing, num_corrupted, num_unreadable, num_extra = len(r.get('missing', [])), len(r.get('corrupted', [])), len(r.get('unreadable', [])), len(r.get('extra', []))
        num_problems = num_missing + num_corrupted + num_unreadable
        
        # Enable report buttons after verification completes
        self.view.save_full_report_button.config(state='normal')
        self.view.save_problem_report_button.config(state='normal' if num_problems > 0 else 'disabled')
        self.view.copy_problem_files_button.config(state='normal' if num_problems > 0 else 'disabled')
        
        report_text = self.view.verify_report_text; report_text.config(state='normal')
        
        # Add final summary with colors
        summary_header = f"\n{'='*50}\n📊 VERIFICATION SUMMARY\n{'='*50}\n"
        report_text.insert(tk.END, summary_header, "info")
        
        if num_missing > 0:
            report_text.insert(tk.END, f"⚠️ Missing Files: {num_missing}\n", "warning")
        if num_corrupted > 0:
            report_text.insert(tk.END, f"❌ Corrupted Files: {num_corrupted}\n", "error")
        if num_unreadable > 0:
            report_text.insert(tk.END, f"🔒 Unreadable Files: {num_unreadable}\n", "error")
        if num_extra > 0:
            report_text.insert(tk.END, f"📁 Extra Files: {num_extra}\n", "info")
        
        if num_problems == 0:
            report_text.insert(tk.END, "✅ All files verified successfully!\n", "success")
        else:
            report_text.insert(tk.END, f"⚠️ Total Problems Found: {num_problems}\n", "warning")
        
        report_text.insert(tk.END, "\nVerification Complete.\n", "info")
        report_text.config(state='disabled'); report_text.see(tk.END)
        
        if num_problems > 0: 
            messagebox.showinfo("Verification Complete", f"Verification complete. Found {num_problems} problem file(s).\n\n({num_missing} missing, {num_corrupted} corrupted, {num_unreadable} unreadable)\n\nSee the report for details.")
        else: 
            messagebox.showinfo("Verification Complete", "Verification complete. No problems found!")

    def _handle_verify_cancelled(self, msg: dict):
        self.view.show_dashboard_view("Verifier"); self.set_state(AppState.IDLE); self._reset_verifier_ui("Verification cancelled by user.")
        # Keep buttons disabled after cancellation
        self.view.save_full_report_button.config(state='disabled')
        self.view.save_problem_report_button.config(state='disabled')
        self.view.copy_problem_files_button.config(state='disabled')

    def _handle_verify_issues_batch(self, msg: dict):
        batch = msg.get('batch', [])
        if not batch: return
        report_text = self.view.verify_report_text; report_text.config(state='normal')
        
        for issue_type, path in batch:
            if issue_type == 'missing':
                report_text.insert(tk.END, f"⚠️ MISSING:   {path.replace('/', os.sep)}\n", "warning")
            elif issue_type == 'corrupted':
                report_text.insert(tk.END, f"❌ CORRUPTED: {path.replace('/', os.sep)}\n", "error")
        
        report_text.config(state='disabled'); report_text.see(tk.END)

    def _populate_diag_ui_from_cache(self):
        if not self.last_diag_report: logger.log("Tried to populate diagnostics UI, but no data cached.", "WARNING"); return
        for key, value in self.last_diag_report.get('system', {}).items():
            if key in self.view.diag_labels: self.view.diag_labels[key].config(text=str(value))
        self.view.crash_log_text.config(state='normal'); self.view.crash_log_text.delete(1.0, tk.END); self.view.crash_log_text.insert(tk.END, self.last_diag_report.get('crashes', 'Error retrieving data.')); self.view.crash_log_text.config(state='disabled')
        logger.log("Populated diagnostics UI from cached data.", "INFO")

    def _on_diag_initial_complete(self, report: dict):
        self.last_diag_report = report
        self.diag_info_fetched = True
        self._populate_diag_ui_from_cache()

    def _on_diag_partial_complete(self, report: dict):
        self.last_diag_report = report
        self._last_diag_scan_time = time.time()
        self._populate_diag_ui_from_cache()
        if 'error' in self.last_diag_report.get('system', {}):
            messagebox.showerror("Diagnostics Error", self.last_diag_report['system']['error'])

    def _on_diag_full_complete(self, report: dict):
        self.last_diag_report = report
        self._last_diag_scan_time = time.time()
        self._populate_diag_ui_from_cache()
        
        # Reset the button state
        if hasattr(self.view, 'diag_run_button'):
            self.view.diag_run_button.config(text=f"{Constants.ICON_SHIELD} Run Full Scan", state='normal')
        
        if 'error' in self.last_diag_report.get('system', {}):
            messagebox.showerror("Diagnostics Error", self.last_diag_report['system']['error'])
        
        self.set_state(AppState.IDLE)
        logger.log("Full diagnostics scan completed successfully.", "INFO")
        messagebox.showinfo("Scan Complete", "Full diagnostics scan has finished.")
        
        # Refresh logs to show the latest information
        self.view.refresh_logs()

    def _handle_manual_install_confirm(self, msg: dict):
        data = msg.get('data', {}); proceed = False; matched_version = data.get('matched')
        if matched_version: proceed = messagebox.askyesno("Checksum Match", f"File appears to be an official update for v{matched_version.replace('_', ' -> v')}\n\nDo you want to install it?")
        else: proceed = messagebox.askyesno("Unknown Checksum", "This file does not match any known update checksum.\nInstalling it could be risky.\n\nAre you sure?", icon='warning')

        if proceed: self._manual_install_installer(Path(data.get('path','')))
        else: self.progress_queue.put({'type': Q_MSG.CANCELLED})

    def _handle_manual_install_complete(self, msg: dict):
        self.view.show_dashboard_view("Updater")
        messagebox.showinfo("Success", "Manual installation completed successfully!")
        self.refresh_version_and_updates()
        self.set_state(AppState.IDLE)


# ==============================================================================
# --- GUI VIEW (The Body) --- [UI Overhaul Version]
# ==============================================================================
class AppGUI(tk.Tk):
    """Manages the entire Tkinter GUI, its creation, and state updates."""
    def __init__(self):
        super().__init__()
        self.controller: Optional[AppController] = None
        self.game_dir_var = tk.StringVar(value="")
        self.verify_checksum_var = tk.BooleanVar(value=True)
        self.download_source_var = tk.StringVar(value="Automatic")
        self.dark_mode = True
        self.log_file_last_pos = 0
        self.log_content_has_changed = False
        self.is_admin = is_admin()
        
        # Modern window configuration
        admin_text = f" {Constants.ICON_USER_SHIELD}" if self.is_admin else ""
        self.title(f"{Constants.APP_NAME} {Constants.SCRIPT_VERSION}{admin_text} - by {Constants.AUTHOR}")
        
        # Apply modern layout configuration
        layout = ModernThemeManager.LAYOUT_CONFIG
        self.geometry(f"{layout['geometry']['default_width']}x{layout['geometry']['default_height']}")
        self.minsize(layout['geometry']['min_width'], layout['geometry']['min_height'])
        
        # Modern window styling
        self.configure(bg='#0f0f0f')
        
        # Set icon if available
        try:
            self.iconify()  # Modern minimize behavior
        except:
            pass

    def set_controller(self, controller: AppController):
        self.controller = controller
        self.protocol("WM_DELETE_WINDOW", self.controller.on_closing)
        self.create_menu()
        self.create_widgets()
        self._define_widget_groups()
        self.set_theme()
        self.game_dir_var.trace_add("write", self._on_game_dir_changed)

    def show_api_error(self):
        """Displays a fatal error screen if initial data cannot be loaded."""
        for widget in self.winfo_children(): widget.destroy()
        error_frame = ttk.Frame(self, padding=40); error_frame.pack(fill=tk.BOTH, expand=True)
        ttk.Label(error_frame, text=Constants.ICON_WARNING, font=("TkFontAwesome", 48), style="Error.TLabel").pack(pady=10)
        ttk.Label(error_frame, text="Fatal Error", font=("Segoe UI", 24), style="Error.TLabel").pack(pady=10)
        ttk.Label(error_frame, text="Could not fetch update info from server or cache.\nPlease check your internet connection.\nApplication cannot continue.", justify=tk.CENTER, wraplength=400).pack(pady=10)
        ttk.Button(error_frame, text="Exit", command=self.destroy, style="Modern.Primary.TButton").pack(pady=20, ipadx=20, ipady=8)
        self.config(cursor="")

    def create_menu(self):
        menubar = Menu(self); self.config(menu=menubar)
        file_menu = Menu(menubar, tearoff=0)
        file_menu.add_command(label="Exit", command=self.controller.on_closing)
        menubar.add_cascade(label="File", menu=file_menu)
        
        help_menu = Menu(menubar, tearoff=0)
        help_menu.add_command(label="Get Help on Discord", command=lambda: webbrowser.open(Constants.DISCORD_LINK))
        help_menu.add_command(label="About", command=self.show_about_dialog)
        menubar.add_cascade(label="Help", menu=help_menu)

    def show_about_dialog(self):
        messagebox.showinfo("About", f"{Constants.APP_NAME}\nVersion: {Constants.SCRIPT_VERSION}\nAuthor: {Constants.AUTHOR}")

    def _on_tab_changed(self, event):
        if not self.controller: return
        try:
            selected_tab_text = self.notebook.tab(self.notebook.select(), "text")
        except tk.TclError:
            return

        if "Diagnostics" in selected_tab_text:
            if self.controller.diag_info_fetched: self.controller._populate_diag_ui_from_cache()
            else: self.controller.run_initial_diagnostics()
        elif "Logs" in selected_tab_text:
            if self.log_content_has_changed:
                self.log_text.see(tk.END)
                self.log_content_has_changed = False

    def _on_game_dir_changed(self, *args):
        if not self.controller: return
        self.controller.process_directory_change()

    def create_widgets(self):
        layout = ModernThemeManager.LAYOUT_CONFIG
        theme = ModernThemeManager.get_theme('dark')
        
        # Modern main frame with enhanced styling
        main_frame = ttk.Frame(self, padding=layout['padding']['main_frame'])
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Enhanced header with modern design
        header_frame = ttk.Frame(main_frame)
        header_frame.pack(fill=tk.X, pady=(0, layout['spacing']['section_gap']))
        
        # Modern title with enhanced typography
        title_label = ttk.Label(header_frame, text=Constants.APP_NAME, 
                               style="Modern.Title.TLabel")
        title_label.pack(side=tk.LEFT)
        
        # Modern notebook with enhanced styling
        self.notebook = ttk.Notebook(main_frame, style='TNotebook')
        self.notebook.pack(fill=tk.BOTH, expand=True, pady=layout['spacing']['widget_gap'])

        # Add tabs with modern icons and enhanced spacing
        self.notebook.add(self.create_updater_tab(), text=f" {Constants.ICON_CLOUD_DOWNLOAD}  Updater ")
        self.notebook.add(self.create_verifier_tab(), text=f" {Constants.ICON_CHECK_CIRCLE}  Verifier ")
        self.notebook.add(self.create_utility_tab(), text=f" {Constants.ICON_TOOLS}  Utilities ")
        self.notebook.add(self.create_diagnostics_tab(), text=f" {Constants.ICON_STETHOSCOPE}  Diagnostics ")
        self.notebook.add(self.create_logs_tab(), text=f" {Constants.ICON_FILE_ALT}  Logs ")
        self.notebook.add(self.create_credits_tab(), text=f" {Constants.ICON_STAR}  Credits ")
        self.notebook.bind("<<NotebookTabChanged>>", self._on_tab_changed)

    def create_updater_tab(self):
        layout = ThemeManager.LAYOUT_CONFIG
        self.updater_tab = ttk.Frame(self.notebook, padding=layout['padding']['section_frame'])
        self.updater_tab.rowconfigure(0, weight=1); self.updater_tab.columnconfigure(0, weight=1)

        self.updater_welcome_frame = self._create_welcome_view(self.updater_tab, "Updater")
        self.updater_welcome_frame.grid(row=0, column=0, sticky='nsew')

        self.updater_dashboard_frame = self._create_updater_dashboard_view(self.updater_tab)
        self.updater_dashboard_frame.grid_forget()

        return self.updater_tab

    def _create_updater_dashboard_view(self, parent):
        dashboard_frame = ttk.Frame(parent, padding=10); dashboard_frame.columnconfigure(0, weight=1)

        # Enhanced info frame with better visual hierarchy
        info_frame = ttk.LabelFrame(dashboard_frame, text="📊 Update Status Dashboard"); 
        info_frame.grid(row=0, column=0, sticky='ew', pady=(0, 15), ipady=15, padx=5); 
        info_frame.columnconfigure(1, weight=1)
        
        # Directory section with modern styling
        ttk.Label(info_frame, text="Game Directory:", style="Modern.Subtitle.TLabel").grid(row=0, column=0, sticky='e', padx=(15, 10), pady=8)
        dir_subframe = ttk.Frame(info_frame); dir_subframe.grid(row=0, column=1, sticky='ew', padx=(0,15)); dir_subframe.columnconfigure(0, weight=1)
        self.dashboard_dir_entry = ttk.Entry(dir_subframe, textvariable=self.game_dir_var, state='readonly', font=('Segoe UI', 9)); 
        self.dashboard_dir_entry.grid(row=0, column=0, sticky='ew')
        ttk.Button(dir_subframe, text="📁 Change...", command=self.controller.select_game_dir, style="Modern.Small.TButton").grid(row=0, column=1, padx=(8,0))
        
        # Version info with color coding
        ttk.Label(info_frame, text="Current Version:", style="Modern.Subtitle.TLabel").grid(row=1, column=0, sticky='e', padx=(15, 10), pady=8)
        self.dashboard_game_version_label = ttk.Label(info_frame, text="v?.?.?", font=('Segoe UI', 10), foreground='#3498db'); 
        self.dashboard_game_version_label.grid(row=1, column=1, sticky='w', padx=(0, 15))
        
        ttk.Label(info_frame, text="Latest Version:", style="Modern.Subtitle.TLabel").grid(row=2, column=0, sticky='e', padx=(15, 10), pady=8)
        self.dashboard_latest_version_label = ttk.Label(info_frame, text="v?.?.?", font=('Segoe UI', 10), foreground='#27ae60'); 
        self.dashboard_latest_version_label.grid(row=2, column=1, sticky='w', padx=(0, 15))

        # Enhanced action and progress section
        self.action_progress_frame = ttk.Frame(dashboard_frame); 
        self.action_progress_frame.grid(row=1, column=0, sticky='ew', pady=(0, 15)); 
        self.action_progress_frame.columnconfigure(0, weight=1)

        # Enhanced idle frame with better status display
        self.idle_frame = ttk.Frame(self.action_progress_frame); 
        self.idle_frame.grid(row=0, column=0, sticky='ew'); 
        self.idle_frame.columnconfigure(0, weight=1)
        
        # Status label with enhanced styling and color feedback
        self.dashboard_status_label = ttk.Label(
            self.idle_frame, 
            text="🔄 Initializing application...", 
            font=('Segoe UI', 11, 'normal'),
            foreground='#3498db',
            anchor='center'
        )
        self.dashboard_status_label.grid(row=0, column=0, pady=(0, 20))
        
        # Enhanced action button with better positioning
        action_button_frame = ttk.Frame(self.idle_frame); 
        action_button_frame.grid(row=1, column=0)
        self.update_dashboard_action_button = ttk.Button(
            action_button_frame, 
            text="⏳ Please wait...", 
            state='disabled', 
            style="Modern.Primary.TButton"
        )
        self.update_dashboard_action_button.pack(pady=8, ipadx=25, ipady=10)

        self.progress_frame = self._create_progress_view(self.action_progress_frame, "Updater")

        self.details_frame = ttk.LabelFrame(dashboard_frame, text="📋 Update Plan & Options")
        self.details_frame.grid(row=2, column=0, sticky='nsew', ipady=5, padx=5, pady=(15,0))
        self.details_frame.rowconfigure(0, weight=1)
        self.details_frame.columnconfigure(0, weight=1)
        
        # Get theme color
        cyan_color = ModernThemeManager.get_cyan_color('dark')
        
        plan_scroll = ttk.Scrollbar(self.details_frame, orient=tk.VERTICAL)
        self.update_plan_text = tk.Text(self.details_frame, wrap=tk.WORD, yscrollcommand=plan_scroll.set, font=("Segoe UI", 10), relief='flat', height=5, bd=0, highlightthickness=0)
        plan_scroll.config(command=self.update_plan_text.yview)
        self.update_plan_text.grid(row=0, column=0, sticky='nsew', padx=(10,0), pady=10)
        plan_scroll.grid(row=0, column=1, sticky='ns', padx=(0,10), pady=10)
        self.update_plan_text.config(state='disabled')
        
        # Configure text tags for colored styling
        self.update_plan_text.tag_configure("cyan", foreground=cyan_color)
        self.update_plan_text.tag_configure("normal", foreground='#ffffff')
        
        # Options section (always visible, no message)
        options_subframe = ttk.Frame(self.details_frame)
        options_subframe.grid(row=2, column=0, columnspan=2, sticky='ew', padx=10, pady=(10,10))
        options_subframe.columnconfigure(1, weight=1)
        
        ttk.Label(options_subframe, text="Download Source:", foreground=cyan_color, font=("Segoe UI", 9, 'bold')).grid(row=0, column=0, sticky='w', padx=(0,10), pady=5)
        self.host_selector = ttk.Combobox(options_subframe, textvariable=self.download_source_var, state="disabled", values=["Automatic"])
        self.host_selector.grid(row=0, column=1, sticky='ew', padx=(0,10), pady=5)
        self.host_selector.bind("<<ComboboxSelected>>", lambda e: self.details_frame.focus_set())
        
        self.checksum_checkbox = ttk.Checkbutton(options_subframe, text="Verify Checksums", variable=self.verify_checksum_var, style="Switch.TCheckbutton")
        self.checksum_checkbox.grid(row=0, column=2, sticky='w', padx=(10,0), pady=5)
        
        # Clear Downloads button
        clear_downloads_btn = ttk.Button(options_subframe, text=f"{Constants.ICON_TRASH} Clear All Downloads", 
                                        command=self.controller.clear_all_downloads,
                                        style="Modern.Danger.TButton")
        clear_downloads_btn.grid(row=0, column=3, sticky='w', padx=(15,0), pady=5)

        return dashboard_frame

    def create_verifier_tab(self):
        layout = ThemeManager.LAYOUT_CONFIG
        self.verifier_tab = ttk.Frame(self.notebook, padding=layout['padding']['section_frame'])
        self.verifier_tab.rowconfigure(0, weight=1); self.verifier_tab.columnconfigure(0, weight=1)

        self.verifier_welcome_frame = self._create_welcome_view(self.verifier_tab, "Verifier")
        self.verifier_welcome_frame.grid(row=0, column=0, sticky='nsew')

        self.verifier_dashboard_frame = self._create_verifier_dashboard_view(self.verifier_tab)
        self.verifier_dashboard_frame.grid_forget()

        return self.verifier_tab

    def _create_verifier_dashboard_view(self, parent):
        dashboard_frame = ttk.Frame(parent, padding=10)
        dashboard_frame.rowconfigure(1, weight=1); dashboard_frame.columnconfigure(0, weight=1)

        self.verifier_action_progress_frame = ttk.Frame(dashboard_frame); self.verifier_action_progress_frame.grid(row=0, column=0, sticky='ew', pady=(0, 15)); self.verifier_action_progress_frame.columnconfigure(0, weight=1)
        self.verifier_idle_frame = ttk.Frame(self.verifier_action_progress_frame); self.verifier_idle_frame.grid(row=0, column=0, sticky='ew'); self.verifier_idle_frame.columnconfigure(0, weight=1)
        self.verify_button = ttk.Button(self.verifier_idle_frame, text=f" {Constants.ICON_SHIELD_CHECK}  Verify All Game Files", command=self.controller.start_verification, style="Accent.TButton")
        self.verify_button.pack(pady=(0, 12), ipady=6)

        self.verifier_progress_frame = self._create_progress_view(self.verifier_action_progress_frame, "Verifier")

        report_frame = ttk.LabelFrame(dashboard_frame, text="Verification Report"); report_frame.grid(row=1, column=0, sticky='nsew', ipady=5, padx=5); report_frame.rowconfigure(0, weight=1); report_frame.columnconfigure(0, weight=1)
        scroll = ttk.Scrollbar(report_frame, orient=tk.VERTICAL); self.verify_report_text = tk.Text(report_frame, wrap=tk.WORD, height=8, relief='flat', font=("Consolas", 9), yscrollcommand=scroll.set, bd=0, highlightthickness=0)
        scroll.config(command=self.verify_report_text.yview); self.verify_report_text.grid(row=0, column=0, sticky='nsew', padx=(10,0), pady=10); scroll.grid(row=0, column=1, sticky='ns', padx=(0,10), pady=10)
        
        # Configure text tags for colored output
        self.verify_report_text.tag_config("error", foreground="#e74c3c")      # Red for corrupted files
        self.verify_report_text.tag_config("warning", foreground="#f39c12")    # Orange for missing files
        self.verify_report_text.tag_config("success", foreground="#27ae60")    # Green for success
        self.verify_report_text.tag_config("info", foreground="#3498db")       # Blue for info
        
        self.verify_report_text.insert(tk.END, "A summary of any issues found will appear here after verification."); self.verify_report_text.config(state='disabled')
        report_actions = ttk.Frame(report_frame); report_actions.grid(row=1, column=0, columnspan=2, sticky='ew', padx=10, pady=(8,12))
        self.save_full_report_button = ttk.Button(report_actions, text=f" {Constants.ICON_SAVE}  Save Full Report", state='disabled', command=lambda: self.controller.save_report('full'), style="Modern.Secondary.TButton")
        self.save_full_report_button.pack(side=tk.LEFT, padx=(0,12), ipady=6)
        self.save_problem_report_button = ttk.Button(report_actions, text=f" {Constants.ICON_FILE_EXPORT}  Save Problem List", state='disabled', command=lambda: self.controller.save_report('problems'), style="Modern.Secondary.TButton")
        self.save_problem_report_button.pack(side=tk.LEFT, padx=(0,12), ipady=6)
        self.copy_problem_files_button = ttk.Button(report_actions, text=f" {Constants.ICON_COPY}  Copy Problem List", state='disabled', command=self.controller.copy_problem_files_list, style="Modern.Secondary.TButton")
        self.copy_problem_files_button.pack(side=tk.LEFT, ipady=6)
        return dashboard_frame

    def _create_welcome_view(self, parent, tab_name):
        welcome_frame = ttk.Frame(parent, padding=20)
        welcome_frame.columnconfigure(0, weight=1); welcome_frame.rowconfigure(1, weight=1); welcome_frame.rowconfigure(4, weight=1)

        if tab_name == "Updater":
            icon, title, subtitle = Constants.ICON_CLOUD_DOWNLOAD, "Ready to Begin?", "To get started, please select your Cricket 26 game directory."
        else:
            icon, title, subtitle = Constants.ICON_CHECK_CIRCLE, "Game File Verifier", "To verify your game files, please select the Cricket 26 directory."
        
        ttk.Label(welcome_frame, text=icon, font=("TkFontAwesome", 48), style="Accent.TLabel").grid(row=1, column=0, sticky='s', pady=12)
        ttk.Label(welcome_frame, text=title, font=("Segoe UI", 24)).grid(row=2, column=0, pady=8)
        ttk.Label(welcome_frame, text=subtitle, style="Subtitle.TLabel", wraplength=400, justify='center').grid(row=3, column=0, pady=(0, 20))
        
        select_button = ttk.Button(welcome_frame, text=f" {Constants.ICON_FOLDER_OPEN}  Select Game Directory", 
                                 style="Accent.TButton", command=self.controller.select_game_dir)
        select_button.grid(row=4, column=0, sticky='n', ipady=8, ipadx=16)
        
        return welcome_frame

    def _create_progress_view(self, parent, tab_name):
        progress_frame = ttk.LabelFrame(parent, text="In Progress"); progress_frame.columnconfigure(0, weight=1)

        overall_label = ttk.Label(progress_frame, text="Overall: Starting...", font=("Segoe UI", 12), anchor='center')
        overall_label.grid(row=0, column=0, pady=(10, 5), sticky='ew', padx=10)

        progress_bar = ttk.Progressbar(progress_frame, mode='determinate', length=400)
        progress_bar.grid(row=1, column=0, sticky='ew', pady=5, padx=10, ipady=4)

        status_label = ttk.Label(progress_frame, text="Status: Initializing...", font=("Segoe UI", 10), anchor='center')
        status_label.grid(row=2, column=0, pady=(0, 10), sticky='ew', padx=10)

        button_row = 3
        if tab_name == "Updater":
            self.updater_overall_label = overall_label
            self.updater_bar = progress_bar
            self.updater_status_label = status_label
        elif tab_name == "Verifier":
            self.verifier_overall_label = overall_label
            self.verifier_bar = progress_bar
            self.verifier_status_label = status_label
            stats_frame = ttk.Frame(progress_frame); stats_frame.grid(row=3, column=0, sticky='ew', padx=10, pady=(0,10)); stats_frame.columnconfigure((0,1,2), weight=1)
            self.verify_stats_label = ttk.Label(stats_frame, text="📊 Progress: -/-", style="Modern.Info.TLabel", foreground='#27ae60'); self.verify_stats_label.grid(row=0, column=0, sticky='w')
            self.verify_missing_label = ttk.Label(stats_frame, text="⚠️ Missing: -", style="Modern.Warning.TLabel", foreground='#f39c12'); self.verify_missing_label.grid(row=0, column=1, sticky='w')
            self.verify_corrupted_label = ttk.Label(stats_frame, text="❌ Corrupted: -", style="Modern.Error.TLabel", foreground='#e74c3c'); self.verify_corrupted_label.grid(row=0, column=2, sticky='w')
            button_row = 4

        progress_buttons_frame = ttk.Frame(progress_frame)
        progress_buttons_frame.grid(row=button_row, column=0, pady=12)

        pause_button = ttk.Button(progress_buttons_frame, text=f" {Constants.ICON_PAUSE}  Pause")
        pause_button.pack(side=tk.LEFT, padx=8, ipady=4)
        cancel_button = ttk.Button(progress_buttons_frame, text=f" {Constants.ICON_TIMES}  Cancel", style="Error.TButton")
        cancel_button.pack(side=tk.LEFT, padx=8, ipady=4)

        if tab_name == "Updater":
            self.updater_pause_button = pause_button
            self.updater_cancel_button = cancel_button
        elif tab_name == "Verifier":
            self.verifier_pause_button = pause_button
            self.verifier_cancel_button = cancel_button
            # Configure verifier cancel button functionality
            self.verifier_cancel_button.config(command=self.controller.cancel_verification)

        progress_frame.grid_forget()
        return progress_frame

    def create_utility_tab(self):
        """Create a well-organized utility tab with balanced 2-column layout."""
        layout = ModernThemeManager.LAYOUT_CONFIG
        
        # Main container
        tab = ttk.Frame(self.notebook, padding=10)
        tab.columnconfigure((0, 1), weight=1)
        tab.rowconfigure((0, 1, 2, 3), weight=1)
        
        # Enhanced button creation helper
        def create_utility_button(parent, text, icon, command, style_type="secondary", row=0, column=0, columnspan=1):
            """Create a standard utility button."""
            button_config = ModernThemeManager.get_button_config(style_type)
            
            button = ttk.Button(
                parent, 
                text=f"{icon}  {text}", 
                command=command, 
                style=button_config['style']
            )
            button.grid(row=row, column=column, columnspan=columnspan, sticky='ew', padx=6, pady=4, ipady=6)
            return button

        # === GAME MANAGEMENT SECTION ===
        game_section = ttk.LabelFrame(tab, text="🎮 Game Management", padding=10)
        game_section.grid(row=0, column=0, columnspan=2, sticky='ew', pady=(0, 8))
        game_section.columnconfigure((0, 1), weight=1)
        
        self.launch_game_button = create_utility_button(
            game_section, "Launch Cricket 26", Constants.ICON_GAMEPAD, 
            self.controller.launch_game, "primary", 0, 0
        )
        
        self.backup_saves_button = create_utility_button(
            game_section, "Backup Saves", Constants.ICON_DATABASE, 
            self.controller.backup_saved_games, "success", 0, 1
        )
        
        self.restore_backup_button = create_utility_button(
            game_section, "Restore Backup", Constants.ICON_HISTORY, 
            self.controller.restore_backup, "secondary", 1, 0
        )
        
        self.manual_install_button = create_utility_button(
            game_section, "Manual Install", Constants.ICON_ARCHIVE, 
            self.controller.manual_install, "secondary", 1, 1
        )

        # === FOLDER SHORTCUTS SECTION ===
        folder_section = ttk.LabelFrame(tab, text="📁 Quick Access", padding=10)
        folder_section.grid(row=1, column=0, sticky='nsew', padx=(0, 4), pady=(0, 8))
        folder_section.columnconfigure(0, weight=1)
        
        self.open_save_dir_button = create_utility_button(
            folder_section, "Save Location", Constants.ICON_FOLDER_OPEN, 
            self.controller.open_save_dir, "secondary", 0, 0
        )
        
        self.open_backups_dir_button = create_utility_button(
            folder_section, "Backups Folder", Constants.ICON_FOLDER, 
            self.controller.open_backups_dir, "secondary", 1, 0
        )
        
        self.create_shortcuts_button = create_utility_button(
            folder_section, "Create Shortcuts", Constants.ICON_SHORTCUT, 
            self.controller.create_cricket26_shortcuts, "secondary", 2, 0
        )

        # === NETWORK TOOLS SECTION ===
        network_section = ttk.LabelFrame(tab, text="🌐 Network Tools", padding=10)
        network_section.grid(row=1, column=1, sticky='nsew', padx=(4, 0), pady=(0, 8))
        network_section.columnconfigure(0, weight=1)
        
        self.dns_set_button = create_utility_button(
            network_section, "Set Cloudflare DNS", Constants.ICON_SHIELD_CHECK, 
            self.controller.set_dns, "secondary", 0, 0
        )
        
        self.dns_reset_button = create_utility_button(
            network_section, "Reset DNS", Constants.ICON_REFRESH, 
            self.controller.reset_dns, "secondary", 1, 0
        )
        
        self.proxy_reset_button = create_utility_button(
            network_section, "Reset Proxy", Constants.ICON_NETWORK, 
            self.controller.reset_proxy, "secondary", 2, 0
        )

        # === CACHE MANAGEMENT SECTION ===
        cache_section = ttk.LabelFrame(tab, text="🗑️ Cache Management", padding=10)
        cache_section.grid(row=2, column=0, columnspan=2, sticky='ew', pady=(0, 8))
        cache_section.columnconfigure(0, weight=1)
        
        # Red clear cache button with danger styling
        self.clear_cache_button = ttk.Button(
            cache_section, 
            text=f"{Constants.ICON_TRASH}  Clear Download Cache", 
            command=self.controller.clear_download_cache,
            style="Modern.Danger.TButton"
        )
        self.clear_cache_button.pack(pady=6, ipady=8, fill='x', padx=30)

        # === CACHE INFO SECTION ===
        cache_info_section = ttk.LabelFrame(tab, text="💾 Cache Information", padding=10)
        cache_info_section.grid(row=3, column=0, columnspan=2, sticky='ew')
        cache_info_section.columnconfigure(1, weight=1)
        
        ttk.Label(cache_info_section, text="Location:", font=("Segoe UI", 9, "bold")).grid(row=0, column=0, sticky='w', padx=(0, 10), pady=4)
        ttk.Label(cache_info_section, text=str(Constants.CACHE_DIR), foreground="#B0BEC5", font=("Segoe UI", 9)).grid(row=0, column=1, sticky='w', pady=4)
        
        ttk.Label(cache_info_section, text="Size:", font=("Segoe UI", 9, "bold")).grid(row=1, column=0, sticky='w', padx=(0, 10), pady=4)
        self.cache_size_label = ttk.Label(cache_info_section, text="Calculating...", foreground="#B0BEC5", font=("Segoe UI", 9))
        self.cache_size_label.grid(row=1, column=1, sticky='w', pady=4)
        
        return tab

    def create_diagnostics_tab(self):
        """Create enhanced diagnostics tab with better visual organization."""
        layout = ThemeManager.LAYOUT_CONFIG
        tab = ttk.Frame(self.notebook, padding=layout['padding']['section_frame'])
        tab.columnconfigure(0, weight=1)
        tab.rowconfigure(1, weight=1)

        # Enhanced header with description
        header_frame = ttk.Frame(tab)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        ttk.Label(header_frame, text="🩺 System Diagnostics", style="Modern.Title.TLabel").pack(anchor='w')
        ttk.Label(header_frame, text="Analyze your system and game installation for potential issues", 
                 style="Modern.Muted.TLabel").pack(anchor='w', pady=(5, 0))

        # Enhanced controls frame with better spacing
        controls_frame = ttk.LabelFrame(tab, text="Diagnostic Tools", padding=15)
        controls_frame.pack(fill=tk.X, pady=(0, 20))
        controls_frame.columnconfigure((0, 1, 2), weight=1)

        self.diag_run_button = ttk.Button(
            controls_frame, 
            text=f" {Constants.ICON_USER_SHIELD}  Run Full System Scan", 
            command=self.controller.run_full_diagnostics, 
            style="Modern.Primary.TButton"
        )
        self.diag_run_button.grid(row=0, column=0, sticky='ew', padx=(0, 10), ipady=10)
        
        self.dxdiag_button = ttk.Button(
            controls_frame, 
            text=f" {Constants.ICON_FILE_ALT}  Generate DxDiag Report", 
            command=self.controller.generate_dxdiag_report, 
            style="Modern.Secondary.TButton"
        )
        self.dxdiag_button.grid(row=0, column=1, sticky='ew', padx=5, ipady=10)
        
        self.diag_save_button = ttk.Button(
            controls_frame, 
            text=f" {Constants.ICON_SAVE}  Export Results", 
            command=self.controller.save_diagnostics_report, 
            state='disabled', 
            style="Modern.Secondary.TButton"
        )
        self.diag_save_button.grid(row=0, column=2, sticky='ew', padx=(10, 0), ipady=10)

        # --- Main Paned Window ---
        main_pane = ttk.PanedWindow(tab, orient=tk.HORIZONTAL)
        main_pane.pack(fill=tk.BOTH, expand=True)

        # --- System Information Frame ---
        sys_info_frame = ttk.LabelFrame(main_pane, text="System Information", padding=10)
        sys_info_frame.columnconfigure(1, weight=1)
        main_pane.add(sys_info_frame, weight=1)
        
        self.diag_labels = {}
        labels_to_create = {
            "Game Version": "Game Version", "OS": "Operating System", "CPU": "Processor",
            "RAM": "Memory (RAM)", "GPU": "Graphics Card(s)", "DirectX Version": "DirectX Version",
            "Disk Space": "Disk Space"
        }
        for i, (key, label_text) in enumerate(labels_to_create.items()):
            ttk.Label(sys_info_frame, text=f"{label_text}:", font=("Segoe UI", 10)).grid(row=i, column=0, sticky='nw', pady=4, padx=5)
            self.diag_labels[key] = ttk.Label(sys_info_frame, text="Loading...", wraplength=320, justify=tk.LEFT)
            self.diag_labels[key].grid(row=i, column=1, sticky='new', padx=5, pady=4)

        # --- Crash Logs Frame ---
        crash_frame = ttk.LabelFrame(main_pane, text="Game Crash Logs", padding=10)
        main_pane.add(crash_frame, weight=2)
        crash_frame.rowconfigure(0, weight=1)
        crash_frame.columnconfigure(0, weight=1)
        
        scroll = ttk.Scrollbar(crash_frame, orient=tk.VERTICAL)
        self.crash_log_text = tk.Text(crash_frame, wrap=tk.WORD, state='disabled', font=("Consolas", 9), relief='flat', yscrollcommand=scroll.set, bd=0, highlightthickness=0, padx=5, pady=5)
        scroll.config(command=self.crash_log_text.yview)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.crash_log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        initial_msg = "🔄 System information is loading...\n\n📋 CRASH LOG ANALYSIS:\nTo scan for Cricket 26 crash logs from Windows Event Logs, click 'Run Full System Scan' above.\n\n⚠️ Note: Crash log scanning requires Administrator privileges to access Windows Event Logs.\n\nIf you're not running as Administrator, you'll need to:\n1. Right-click the application\n2. Select 'Run as Administrator'\n3. Then click 'Run Full System Scan'"
        self.crash_log_text.config(state='normal')
        self.crash_log_text.delete('1.0', tk.END)
        self.crash_log_text.insert(tk.END, initial_msg)
        self.crash_log_text.config(state='disabled')
        
        return tab

    def create_logs_tab(self):
        """Create enhanced logs tab with better visual organization."""
        layout = ThemeManager.LAYOUT_CONFIG
        tab = ttk.Frame(self.notebook, padding=layout['padding']['section_frame'])
        tab.rowconfigure(1, weight=1)
        tab.columnconfigure(0, weight=1)

        # Enhanced header with description
        header_frame = ttk.Frame(tab)
        header_frame.grid(row=0, column=0, sticky='ew', pady=(0, 15))
        
        ttk.Label(header_frame, text="📄 Application Logs", style="Modern.Title.TLabel").pack(anchor='w')
        ttk.Label(header_frame, text="View and manage application logs for troubleshooting", 
                 style="Modern.Muted.TLabel").pack(anchor='w', pady=(5, 0))

        # Enhanced log frame with better styling
        log_frame = ttk.LabelFrame(tab, text="Log Output", padding=10)
        log_frame.grid(row=1, column=0, sticky='nsew', pady=(0, 15))
        log_frame.rowconfigure(0, weight=1)
        log_frame.columnconfigure(0, weight=1)

        scroll = ttk.Scrollbar(log_frame, orient=tk.VERTICAL)
        self.log_text = tk.Text(
            log_frame, 
            wrap=tk.WORD, 
            state='disabled', 
            font=("Consolas", 9), 
            relief='flat', 
            padx=10, 
            pady=10, 
            yscrollcommand=scroll.set, 
            bd=0, 
            highlightthickness=0,
            background='#1e1e1e',
            foreground='#ffffff'
        )
        
        # Configure text tags for colored log entries
        self.log_text.tag_config("error", foreground="#e74c3c")     # Red for errors/critical
        self.log_text.tag_config("warning", foreground="#f39c12")   # Orange for warnings  
        self.log_text.tag_config("info", foreground="#3498db")      # Blue for info/settings/diag
        self.log_text.tag_config("success", foreground="#27ae60")   # Green for success operations
        
        scroll.config(command=self.log_text.yview)
        scroll.pack(side=tk.RIGHT, fill=tk.Y, padx=(5, 0))
        self.log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Enhanced controls frame - moved to bottom for better organization
        controls = ttk.LabelFrame(tab, text="Log Management", padding=10)
        controls.grid(row=2, column=0, sticky='ew')
        
        # Create a horizontal layout for buttons
        button_frame = ttk.Frame(controls)
        button_frame.pack(expand=True, fill='x')
        
        self.log_refresh_btn = ttk.Button(
            button_frame, 
            text=f" {Constants.ICON_REFRESH}  Refresh", 
            command=self.refresh_logs, 
            style="Modern.Secondary.TButton"
        )
        self.log_refresh_btn.pack(side=tk.LEFT, padx=(0, 10), ipady=6, ipadx=12)
        
        self.log_archive_btn = ttk.Button(
            button_frame, 
            text=f" {Constants.ICON_ARCHIVE}  Archive", 
            command=self.controller.archive_logs, 
            style="Modern.Secondary.TButton"
        )
        self.log_archive_btn.pack(side=tk.LEFT, padx=(0, 10), ipady=6, ipadx=12)
        
        self.log_save_btn = ttk.Button(
            button_frame, 
            text=f" {Constants.ICON_SAVE}  Export", 
            command=self.controller.save_logs, 
            style="Modern.Secondary.TButton"
        )
        self.log_save_btn.pack(side=tk.LEFT, ipady=6, ipadx=12)
        
        return tab

    def create_credits_tab(self):
        """Create enhanced credits tab with team information and acknowledgments."""
        layout = ThemeManager.LAYOUT_CONFIG
        tab = ttk.Frame(self.notebook, padding=layout['padding']['section_frame'])
        tab.rowconfigure(1, weight=1)
        tab.columnconfigure(0, weight=1)

        # Enhanced header with modern styling
        header_frame = ttk.Frame(tab)
        header_frame.grid(row=0, column=0, sticky='ew', pady=(0, 20))
        
        ttk.Label(header_frame, text=f"{Constants.ICON_STAR} Development Team & Credits", 
                 style="Modern.Title.TLabel").pack(anchor='w')
        ttk.Label(header_frame, text="Meet the talented team behind Cricket 26 Auto Updater", 
                 style="Modern.Muted.TLabel").pack(anchor='w', pady=(5, 0))

        # Main credits frame with scrolling capability
        credits_frame = ttk.LabelFrame(tab, text="Credits & Acknowledgments", padding=15)
        credits_frame.grid(row=1, column=0, sticky='nsew', pady=(0, 15))
        credits_frame.rowconfigure(0, weight=1)
        credits_frame.columnconfigure(0, weight=1)

        # Create scrollable text widget for credits
        scroll = ttk.Scrollbar(credits_frame, orient=tk.VERTICAL)
        self.credits_text = tk.Text(
            credits_frame, 
            wrap=tk.WORD, 
            state='disabled', 
            font=("Segoe UI", 10), 
            relief='flat', 
            padx=20, 
            pady=20, 
            yscrollcommand=scroll.set, 
            bd=0, 
            highlightthickness=0,
            background='#1e1e1e',
            foreground='#ffffff',
            height=20
        )
        
        scroll.config(command=self.credits_text.yview)
        scroll.pack(side=tk.RIGHT, fill=tk.Y, padx=(5, 0))
        self.credits_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Populate credits content
        self._populate_credits_content()

        # Action buttons frame
        action_frame = ttk.LabelFrame(tab, text="Actions", padding=10)
        action_frame.grid(row=2, column=0, sticky='ew')
        
        button_frame = ttk.Frame(action_frame)
        button_frame.pack(expand=True, fill='x')
        
        # GitHub repository button
        github_btn = ttk.Button(
            button_frame, 
            text=f" {Constants.ICON_DATABASE}  Visit GitHub Repository", 
            command=lambda: webbrowser.open(Credits.PROJECT_INFO['repository']), 
            style="Modern.Secondary.TButton"
        )
        github_btn.pack(side=tk.LEFT, padx=(0, 10), ipady=6, ipadx=12)
        
        # Discord community button
        discord_btn = ttk.Button(
            button_frame, 
            text=f" {Constants.ICON_HEART}  Join Discord Community", 
            command=lambda: webbrowser.open(Constants.DISCORD_LINK), 
            style="Modern.Secondary.TButton"
        )
        discord_btn.pack(side=tk.LEFT, padx=(0, 10), ipady=6, ipadx=12)
        
        return tab

    def _populate_credits_content(self):
        """Populate the credits text widget with formatted team information."""
        self.credits_text.config(state='normal')
        self.credits_text.delete(1.0, tk.END)
        
        # Get credits text from the Credits class
        credits_content = Credits.get_credits_text()
        
        # Configure text tags for styling
        self.credits_text.tag_config("title", font=("Segoe UI", 16, "bold"), foreground="#ffffff")
        self.credits_text.tag_config("creator", font=("Segoe UI", 12, "bold"), foreground="#ffd700")  # Gold for creator
        self.credits_text.tag_config("developer", font=("Segoe UI", 11, "bold"), foreground="#87ceeb")  # Sky blue for developer
        self.credits_text.tag_config("contributor", font=("Segoe UI", 10, "bold"), foreground="#98fb98")  # Light green for contributor
        self.credits_text.tag_config("section", font=("Segoe UI", 11, "bold"), foreground="#dcdcdc")
        self.credits_text.tag_config("link", font=("Segoe UI", 10), foreground="#5dade2", underline=True)
        self.credits_text.tag_config("normal", font=("Segoe UI", 10), foreground="#ffffff")
        
        # Configure username tags (non-clickable)
        self.credits_text.tag_config("discord_xlr8", font=("Segoe UI", 11, "bold"), foreground="#ffd700")
        self.credits_text.tag_config("discord_aditya", font=("Segoe UI", 10, "bold"), foreground="#87ceeb")
        self.credits_text.tag_config("discord_begula", font=("Segoe UI", 10, "bold"), foreground="#98fb98")
        
        # Insert the credits content
        self.credits_text.insert(tk.END, credits_content, "normal")
        
        # Apply specific styling to different sections and highlight usernames
        content = self.credits_text.get(1.0, tk.END)
        lines = content.split('\n')
        
        start_line = 1.0
        for i, line in enumerate(lines):
            line_start = f"{i+1}.0"
            line_end = f"{i+1}.end"
            
            if "Cricket 26 Auto Updater" in line and "v" in line:
                self.credits_text.tag_add("title", line_start, line_end)
            elif line.strip().startswith("👑"):
                self.credits_text.tag_add("creator", line_start, line_end)
                # Highlight XLR8 full name
                match = re.search(r'XLR8 \(@xlr8_boi\)', line)
                if match:
                    start_pos = f"{i+1}.{match.start()}"
                    end_pos = f"{i+1}.{match.end()}"
                    self.credits_text.tag_add("discord_xlr8", start_pos, end_pos)
            elif line.strip().startswith("⭐"):
                self.credits_text.tag_add("developer", line_start, line_end)
                # Highlight ADITYA full name
                match = re.search(r'ADITYA \(@adityaberchha\)', line)
                if match:
                    start_pos = f"{i+1}.{match.start()}"
                    end_pos = f"{i+1}.{match.end()}"
                    self.credits_text.tag_add("discord_aditya", start_pos, end_pos)
            elif line.strip().startswith("🤝"):
                self.credits_text.tag_add("contributor", line_start, line_end)
                # Highlight Begula full name
                match = re.search(r'Begula \(@belugaaaaaaaaaaaaa\)', line)
                if match:
                    start_pos = f"{i+1}.{match.start()}"
                    end_pos = f"{i+1}.{match.end()}"
                    self.credits_text.tag_add("discord_begula", start_pos, end_pos)
            elif line.strip().startswith("🔗"):
                self.credits_text.tag_add("link", line_start, line_end)
            elif line.strip().startswith("━"):
                self.credits_text.tag_add("section", line_start, line_end)
        
        self.credits_text.config(state='disabled')

    def _define_widget_groups(self):
        self.utility_buttons = [ self.dns_set_button, self.dns_reset_button, self.launch_game_button, self.backup_saves_button, self.restore_backup_button, self.manual_install_button, self.clear_cache_button, self.open_save_dir_button, self.open_backups_dir_button, self.create_shortcuts_button ]
        self.verifier_report_buttons = [ self.save_full_report_button, self.save_problem_report_button, self.copy_problem_files_button ]
        self.log_buttons = [ self.log_refresh_btn, self.log_archive_btn, self.log_save_btn ]
        self.diag_buttons = [self.diag_run_button, self.dxdiag_button, self.diag_save_button]
        self.updater_option_widgets = [self.checksum_checkbox, self.host_selector]

    def update_status_with_color(self, message: str, status_type: str = "info"):
        """Update status message with appropriate color coding."""
        if hasattr(self, 'dashboard_status_label'):
            # Color mapping for different status types
            colors = {
                'info': '#3498db',      # Blue for information
                'success': '#27ae60',   # Green for success
                'warning': '#f39c12',   # Orange for warnings
                'error': '#e74c3c',     # Red for errors
                'progress': '#9b59b6'   # Purple for progress
            }
            
            # Status icons for different types
            icons = {
                'info': '🔄',
                'success': '✅',
                'warning': '⚠️',
                'error': '❌',
                'progress': '⏳'
            }
            
            color = colors.get(status_type, colors['info'])
            icon = icons.get(status_type, icons['info'])
            
            # Update the label with colored text and icon
            self.dashboard_status_label.config(
                text=f"{icon} {message}",
                foreground=color
            )

    def set_theme(self):
        """Apply modern theming using the enhanced ModernThemeManager system."""
        theme_name = 'dark'
        theme = ModernThemeManager.get_theme(theme_name)
        colors = theme['colors']
        
        # Apply modern styles
        ModernThemeManager.apply_modern_styles(self, theme_name)
        
        # Configure verification report text colors with enhanced visual feedback
        self.verify_report_text.tag_config("Default", foreground=colors['text_primary'], font=theme['fonts']['mono'])
        self.verify_report_text.tag_config("Header", 
                                         foreground=colors['accent'], 
                                         font=('Segoe UI', 11))
        self.verify_report_text.tag_config("Missing", 
                                         foreground='#f39c12',  # Bright orange/yellow for missing files
                                         font=('Segoe UI', 10, 'normal'))
        self.verify_report_text.tag_config("Corrupted", 
                                         foreground='#e74c3c',  # Bright red for corrupted files
                                         font=('Segoe UI', 10))
        self.verify_report_text.tag_config("Success", 
                                         foreground='#27ae60',  # Bright green for success
                                         font=('Segoe UI', 10, 'normal'))
        self.verify_report_text.tag_config("Progress", 
                                         foreground='#3498db',  # Blue for progress updates
                                         font=('Segoe UI', 10, 'normal'))
        self.verify_report_text.tag_config("Warning", 
                                         foreground='#f39c12',  # Orange for warnings
                                         font=('Segoe UI', 10, 'normal'))
        self.verify_report_text.tag_config("Info", 
                                         foreground=colors['info'], 
                                         font=('Segoe UI', 10, 'normal'))

        # Configure log text colors with modern hierarchy
        self.log_text.tag_config("INFO", foreground=colors['success'])
        self.log_text.tag_config("WARNING", foreground=colors['warning'])
        self.log_text.tag_config("ERROR", 
                                foreground=colors['error'], 
                                font=theme['fonts']['mono'])
        self.log_text.tag_config("CRITICAL", 
                                foreground='white', 
                                background=colors['error'], 
                                font=theme['fonts']['mono'])
        self.log_text.tag_config("SETTING", foreground=colors['info'])
        self.log_text.tag_config("DIAG", foreground='#9C27B0')
        
        # Update window background
        self.configure(bg=colors['primary'])

    def show_welcome_view(self, tab_name: str):
        if tab_name == "Updater": self.updater_dashboard_frame.grid_forget(); self.updater_welcome_frame.grid(row=0, column=0, sticky='nsew')
        elif tab_name == "Verifier": self.verifier_dashboard_frame.grid_forget(); self.verifier_welcome_frame.grid(row=0, column=0, sticky='nsew')
        self.update_idletasks()

    def show_dashboard_view(self, tab_name: str):
        if tab_name == "Updater": self.updater_welcome_frame.grid_forget(); self.updater_dashboard_frame.grid(row=0, column=0, sticky='nsew'); self.progress_frame.grid_forget(); self.idle_frame.grid(row=0, column=0, sticky='ew'); self.details_frame.grid(row=2, column=0, sticky='nsew', ipady=5, padx=5, pady=(15,0))
        elif tab_name == "Verifier": self.verifier_welcome_frame.grid_forget(); self.verifier_dashboard_frame.grid(row=0, column=0, sticky='nsew'); self.verifier_progress_frame.grid_forget(); self.verifier_idle_frame.grid(row=0, column=0, sticky='ew')
        self.update_idletasks()

    def show_progress_view(self, tab_name: str):
        if tab_name == "Updater": self.idle_frame.grid_forget(); self.details_frame.grid_forget(); self.progress_frame.grid(row=0, column=0, sticky='ew')
        elif tab_name == "Verifier": self.verifier_idle_frame.grid_forget(); self.verifier_progress_frame.grid(row=0, column=0, sticky='ew')
        self.update_idletasks()

    def update_ui_for_state(self, new_state: AppState):
        is_idle = new_state == AppState.IDLE
        
        conflicting_actions = self.utility_buttons + self.diag_buttons + self.updater_option_widgets
        for widget in conflicting_actions:
            widget.config(state='normal' if is_idle else 'disabled')

        # Verify button should be disabled during verification process
        can_verify = self.controller and self.controller.game_dir.get() != "" and new_state != AppState.VERIFYING
        self.verify_button.config(state='normal' if is_idle and can_verify else 'disabled')
        
        # Verifier report buttons should only be enabled when idle AND verification results exist
        can_use_reports = is_idle and self.controller and self.controller.last_verify_results
        for btn in self.verifier_report_buttons:
            btn.config(state='normal' if can_use_reports else 'disabled')

        can_check = self.controller and self.controller.game_dir.get() != "" and self.controller.update_data is not None
        if is_idle:
            if self.controller.updates_to_install:
                self.update_dashboard_action_button.config(text=f"{Constants.ICON_DOWNLOAD} Start Update", command=self.controller.start_update, state='normal')
                self.host_selector.config(state="readonly")
            else:
                self.update_dashboard_action_button.config(text=f"{Constants.ICON_SEARCH} Check for Updates", command=self.controller.check_updates, state='normal' if can_check else 'disabled')
                self.host_selector.config(state="disabled")
        else:
             self.update_dashboard_action_button.config(state='disabled')

        self.diag_save_button.config(state='normal' if is_idle and self.controller.last_diag_report else 'disabled')

    def reset_log_position(self): self.log_file_last_pos = 0; self.log_text.delete(1.0, tk.END); self.refresh_logs()

    def refresh_logs(self):
        self.log_text.config(state='normal')
        
        # Try to get Windows Event Logs first (Application and System logs)
        try:
            event_logs = []
            
            # Get recent application errors from Windows Event Viewer
            try:
                app_command = ['wevtutil', 'qe', 'Application', '/c:20', '/rd:true', '/f:text']
                proc = subprocess.run(app_command, capture_output=True, text=True, 
                                    creationflags=subprocess.CREATE_NO_WINDOW, 
                                    encoding='utf-8', errors='ignore', timeout=10)
                
                if proc.returncode == 0 and proc.stdout.strip():
                    app_events = proc.stdout.strip().split('Event[')
                    for i, event in enumerate(app_events[1:6]):  # Show only first 5 events
                        try:
                            import re
                            timestamp_match = re.search(r'TimeCreated SystemTime="([^"]+)"', event)
                            level_match = re.search(r'Level>(\d+)<', event)
                            source_match = re.search(r'Provider Name="([^"]+)"', event)
                            event_id_match = re.search(r'EventID>(\d+)<', event)
                            
                            if timestamp_match:
                                timestamp = timestamp_match.group(1)[:19].replace('T', ' ')
                                level = "Error" if level_match and level_match.group(1) == "2" else "Warning" if level_match and level_match.group(1) == "3" else "Info"
                                source = source_match.group(1) if source_match else "Unknown"
                                event_id = event_id_match.group(1) if event_id_match else "Unknown"
                                
                                log_entry = f"🖥️ {timestamp} | {level} | {source} | Event ID: {event_id}"
                                tag = "error" if level == "Error" else "warning" if level == "Warning" else "info"
                                self.log_text.insert(tk.END, f"{log_entry}\n", tag)
                        except:
                            continue
            except:
                pass
            
            # Get system events
            try:
                sys_command = ['wevtutil', 'qe', 'System', '/c:10', '/rd:true', '/f:text']
                proc = subprocess.run(sys_command, capture_output=True, text=True, 
                                    creationflags=subprocess.CREATE_NO_WINDOW, 
                                    encoding='utf-8', errors='ignore', timeout=10)
                
                if proc.returncode == 0 and proc.stdout.strip():
                    sys_events = proc.stdout.strip().split('Event[')
                    for i, event in enumerate(sys_events[1:4]):  # Show only first 3 system events
                        try:
                            import re
                            timestamp_match = re.search(r'TimeCreated SystemTime="([^"]+)"', event)
                            level_match = re.search(r'Level>(\d+)<', event)
                            source_match = re.search(r'Provider Name="([^"]+)"', event)
                            
                            if timestamp_match:
                                timestamp = timestamp_match.group(1)[:19].replace('T', ' ')
                                level = "Error" if level_match and level_match.group(1) == "2" else "Warning" if level_match and level_match.group(1) == "3" else "Info"
                                source = source_match.group(1) if source_match else "Unknown"
                                
                                log_entry = f"⚙️ {timestamp} | {level} | {source} (System)"
                                tag = "error" if level == "Error" else "warning" if level == "Warning" else "info"
                                self.log_text.insert(tk.END, f"{log_entry}\n", tag)
                        except:
                            continue
            except:
                pass
                
            # Add separator
            self.log_text.insert(tk.END, "\n" + "="*60 + "\n", "info")
            self.log_text.insert(tk.END, "📄 APPLICATION LOGS:\n", "info")
            self.log_text.insert(tk.END, "="*60 + "\n\n", "info")
            
        except Exception as e:
            self.log_text.insert(tk.END, f"❌ Could not read Windows Event Logs: {e}\n\n", "error")
        
        # Then show application logs
        log_levels = {
            "[CRITICAL]": "error", 
            "[ERROR]": "error", 
            "[WARNING]": "warning", 
            "[SETTING]": "info", 
            "[DIAG]": "info",
            "[INFO]": "success"  # Green for general info operations
        }
        try:
            if logger.log_file.exists():
                current_size = logger.log_file.stat().st_size
                if current_size < self.log_file_last_pos: 
                    self.log_file_last_pos = 0
                
                new_content = False
                with logger.log_file.open('r', encoding='utf-8') as f:
                    f.seek(self.log_file_last_pos)
                    lines_added = 0
                    
                    for line in f:
                        new_content = True
                        line_stripped = line.strip()
                        
                        # Limit log buffer size to prevent memory bloat
                        if lines_added > 0 and lines_added % 100 == 0:
                            current_lines = int(self.log_text.index('end-1c').split('.')[0])
                            if current_lines > Constants.MAX_LOG_BUFFER_SIZE:
                                # Delete oldest 20% of lines
                                delete_count = int(Constants.MAX_LOG_BUFFER_SIZE * 0.2)
                                self.log_text.delete('1.0', f'{delete_count}.0')
                        
                        # Determine the tag based on log level
                        tag = "success"  # default to green for general operations
                        for marker, level_tag in log_levels.items():
                            if marker in line_stripped:
                                tag = level_tag
                                break
                        
                        # Get symbol for the log level
                        level_markers = {
                            "[CRITICAL]": "CRITICAL", "[ERROR]": "ERROR", 
                            "[WARNING]": "WARNING", "[SETTING]": "SETTING", 
                            "[DIAG]": "DIAG", "[INFO]": "INFO"
                        }
                        level = next((lvl for tag_marker, lvl in level_markers.items() if tag_marker in line_stripped), "INFO")
                        symbol = Constants.LOG_SYMBOLS.get(level, 'ℹ️')
                        
                        # Insert with appropriate color tag
                        self.log_text.insert(tk.END, f"{symbol} {line_stripped}\n", tag)
                        lines_added += 1
                    
                    self.log_file_last_pos = f.tell()
                
                if new_content:
                    self.log_content_has_changed = True
                    # Safety check for notebook existence
                    if hasattr(self, 'notebook') and self.notebook.winfo_exists():
                        try:
                            if "Logs" in self.notebook.tab(self.notebook.select(), "text"):
                                self.log_text.see(tk.END)
                                self.log_content_has_changed = False
                        except (tk.TclError, Exception):
                            pass  # Tab not selected or notebook destroyed
            else:
                self.log_text.insert(tk.END, "📄 No application log file found.\n", "warning")
                self.log_file_last_pos = 0
        except Exception as e:
            self.log_text.insert(tk.END, f"❌ Could not read application log file: {e}\n", "error")
        finally:
            self.log_text.config(state='disabled')

    def ask_user_to_select_interface(self, adapters: List[str]) -> Optional[str]:
        dialog = tk.Toplevel(self)
        dialog.title("Select Network Adapter")
        
        ttk.Label(dialog, text="Multiple active network adapters found.\nPlease select the one connected to the internet:").pack(padx=20, pady=10)
        
        selected_adapter = tk.StringVar()
        
        for adapter in adapters:
            ttk.Radiobutton(dialog, text=adapter, variable=selected_adapter, value=adapter).pack(anchor='w', padx=20)
            
        selected_adapter.set(adapters[0])
        
        result = None
        def on_ok():
            nonlocal result
            result = selected_adapter.get()
            dialog.destroy()
            
        ok_button = ttk.Button(dialog, text="OK", command=on_ok, style="Modern.Primary.TButton")
        ok_button.pack(pady=10)
        
        dialog.transient(self)
        dialog.grab_set()
        self.wait_window(dialog)
        
        return result

# ==============================================================================
# --- MAIN EXECUTION BLOCK ---
# ==============================================================================
if __name__ == "__main__":
    if sys.platform != "win32":
        root = tk.Tk(); root.withdraw()
        messagebox.showerror("Unsupported OS", "This application uses Windows-specific features and is not compatible with this operating system.")
        sys.exit(1)

    # This is required for pyinstaller
    multiprocessing.freeze_support()

    # Check for WMI dependency separately as it is part of pywin32
    try:
        import wmi
        import pythoncom
    except ImportError:
        root = tk.Tk(); root.withdraw()
        messagebox.showerror("Missing Dependency", "The 'pywin32' library is required for system diagnostics.\n\nPlease install it by running:\npip install pywin32")
        sys.exit(1)

    try:
        view = AppGUI()
        controller = AppController(view)
        view.set_controller(controller)

        startup_actions = []
        if len(sys.argv) > 1 and controller.is_admin:
            action = sys.argv[1]
            logger.log(f"Application launched with argument: {action}", "INFO")
            if action == '--run-diagnostics':
                def relaunch_diagnostics():
                    try:
                        tab_names = [view.notebook.tab(i, "text") for i in view.notebook.tabs()]
                        # Find index of Diagnostics tab regardless of icon
                        diag_tab_index = next(i for i, name in enumerate(tab_names) if "Diagnostics" in name)
                        view.notebook.select(diag_tab_index)
                    except (ValueError, StopIteration, tk.TclError): 
                        logger.log("Could not auto-switch to Diagnostics tab on relaunch.", "WARNING")
                    controller.run_full_diagnostics(from_admin_relaunch=True)
                startup_actions.append((relaunch_diagnostics, ()))
            elif action == '--set-dns': startup_actions.append((controller.set_dns, ()))
            elif action == '--reset-dns': startup_actions.append((controller.reset_dns, ()))
            elif action == '--set-dns-from-failure': startup_actions.append((controller.set_dns_from_failure, ()))

        controller.start(startup_actions)
        view.mainloop()

    except Exception as e:
        logger.log(f"A critical unhandled exception occurred in __main__: {e}", "CRITICAL")
        try:
            root = tk.Tk(); root.withdraw()
            messagebox.showerror("Fatal Error", f"A fatal error occurred: {e}\n\nPlease check the log file for details.")
        except Exception as final_e:
            print(f"FATAL ERROR: {e}\nCould not display messagebox: {final_e}")
