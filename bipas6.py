from __future__ import annotations
import asyncio
import base64
import hashlib
import json
import logging
import os
import sys
import random
import ssl
import string
import time
import re
import uuid
import requests
from datetime import datetime
from faker import Faker
from colorama import init, Fore, Back, Style
from typing import Any, Dict, List, Optional, Tuple
import urllib3
import ipaddress
import socket
import secrets
import numpy as np
import math

if sys.version_info >= (3, 0):
    from urllib.parse import urlencode

try:
    from dateutil import parser as dateutil_parser  # type: ignore
    _HAS_DATEUTIL = True
except Exception:
    _HAS_DATEUTIL = False

try:
    import httpx
    HAVE_HTTPX = True
except Exception:
    httpx = None
    HAVE_HTTPX = False

try:
    import aiohttp
    HAVE_AIOHTTP = True
except ImportError:
    HAVE_AIOHTTP = False
    aiohttp = None
    print("⚠️  aiohttp not installed. Install with: pip install aiohttp")

# BEST FOR ANTI-DETECTION: curl_cffi with Chrome impersonation
# This library impersonates real Chrome TLS fingerprint (JA3)
try:
    from curl_cffi.requests import AsyncSession as CurlAsyncSession
    from curl_cffi.requests import Session as CurlSession
    HAVE_CURL_CFFI = True
    print("✅  curl_cffi available - Best TLS fingerprint impersonation")
except ImportError:
    HAVE_CURL_CFFI = False
    CurlAsyncSession = None
    CurlSession = None
    print("⚠️  curl_cffi not installed. Install with: pip install curl_cffi")
    print("    curl_cffi provides BEST anti-detection with Chrome TLS fingerprint")

# Alternative: tls-client (also good for TLS fingerprinting)
try:
    import tls_client
    HAVE_TLS_CLIENT = True
    print("✅  tls-client available - Good TLS fingerprint support")
except ImportError:
    HAVE_TLS_CLIENT = False
    tls_client = None

try:
    import brotli
    _HAS_BROTLI = True
except ImportError:
    _HAS_BROTLI = False

logger = logging.getLogger("ultraboostedv13_protocol_spoofing_indonesia")
logger.setLevel(logging.INFO)
current = datetime.now()
fake = Faker("id_ID")

# Tambahkan Faker untuk nama Indonesia
fake_indonesia = Faker(['id_ID'])

# Colorama colors
biru = Fore.BLUE
kuning = Fore.YELLOW
merah = Fore.RED
putih = Fore.WHITE
cyan = Fore.CYAN
hijau = Fore.GREEN
hitam = Fore.BLACK
reset = Style.RESET_ALL
bg_merah = Back.RED
bg_kuning = Back.YELLOW
bg_hijau = Back.GREEN
bg_biru = Back.BLUE
bg_putih = Back.WHITE
CYAN = "\033[96m"
HIJAU = "\033[92m"
MERAH = "\033[91m"
RESET = "\033[0m"

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ===================== IP TRACKING SYSTEM =====================
# Manages IPs based on their status: working, checkpoint, blocked
# Strategy:
# - Working IPs: Successfully created account → save for future use
# - Checkpoint IPs: Created but got checkpoint → save for reference
# - Blocked IPs: Got IP block/rate limit → blacklist, never use again

WORKING_IPS_FILE = "working_ips.json"      # IPs that successfully created accounts
CHECKPOINT_IPS_FILE = "checkpoint_ips.json" # IPs that got checkpoint
BLOCKED_IPS_FILE = "blocked_ips.json"       # IPs that got blocked - DO NOT USE

# In-memory blacklist cache for fast lookup
_blocked_ips_cache: set = set()

def _load_blocked_ips_cache():
    """Load blocked IPs into memory for fast lookup"""
    global _blocked_ips_cache
    try:
        if os.path.exists(BLOCKED_IPS_FILE):
            with open(BLOCKED_IPS_FILE, 'r') as f:
                blocked = json.load(f)
                _blocked_ips_cache = {entry.get("ip") for entry in blocked if entry.get("ip")}
    except:
        _blocked_ips_cache = set()

def is_ip_blocked(ip: str) -> bool:
    """Check if IP is in the blocked list (fast in-memory check)"""
    global _blocked_ips_cache
    if not _blocked_ips_cache:
        _load_blocked_ips_cache()
    return ip in _blocked_ips_cache

def save_working_ip(ip: str, isp: str, country: str, username: str = None) -> bool:
    """Save working IP to file for future use (no duplicates)
    
    Args:
        ip: The IP address that successfully created an account
        isp: The ISP name
        country: The country code (ID, MM, MY, etc.)
        username: Optional username of the created account
        
    Returns:
        True if saved successfully, False if already exists
    """
    try:
        # Load existing IPs
        working_ips = []
        if os.path.exists(WORKING_IPS_FILE):
            try:
                with open(WORKING_IPS_FILE, 'r') as f:
                    working_ips = json.load(f)
            except:
                working_ips = []
        
        # Check for duplicates
        existing_ips = {entry.get("ip") for entry in working_ips}
        if ip in existing_ips:
            return False  # Already exists
        
        # Add new entry
        new_entry = {
            "ip": ip,
            "isp": isp,
            "country": country,
            "username": username,
            "status": "working",
            "success_date": datetime.now().isoformat(),
            "timestamp": time.time()
        }
        working_ips.append(new_entry)
        
        # Save to file
        with open(WORKING_IPS_FILE, 'w') as f:
            json.dump(working_ips, f, indent=2)
        
        print(f"{Fore.GREEN}    💾 Saved WORKING IP: {ip} ({isp}) [{country}] → {WORKING_IPS_FILE}{Style.RESET_ALL}")
        return True
        
    except Exception as e:
        print(f"{Fore.RED}    ⚠ Failed to save working IP: {e}{Style.RESET_ALL}")
        return False

def save_checkpoint_ip(ip: str, isp: str, country: str, username: str = None, reason: str = None) -> bool:
    """Save checkpoint IP to file for reference
    
    Args:
        ip: The IP address that got checkpoint
        isp: The ISP name
        country: The country code
        username: Optional username that got checkpoint
        reason: Optional reason for checkpoint
        
    Returns:
        True if saved successfully
    """
    try:
        checkpoint_ips = []
        if os.path.exists(CHECKPOINT_IPS_FILE):
            try:
                with open(CHECKPOINT_IPS_FILE, 'r') as f:
                    checkpoint_ips = json.load(f)
            except:
                checkpoint_ips = []
        
        # Check for duplicates
        existing_ips = {entry.get("ip") for entry in checkpoint_ips}
        if ip in existing_ips:
            return False
        
        new_entry = {
            "ip": ip,
            "isp": isp,
            "country": country,
            "username": username,
            "status": "checkpoint",
            "reason": reason,
            "checkpoint_date": datetime.now().isoformat(),
            "timestamp": time.time()
        }
        checkpoint_ips.append(new_entry)
        
        with open(CHECKPOINT_IPS_FILE, 'w') as f:
            json.dump(checkpoint_ips, f, indent=2)
        
        print(f"{Fore.YELLOW}    📋 Saved CHECKPOINT IP: {ip} ({isp}) [{country}] → {CHECKPOINT_IPS_FILE}{Style.RESET_ALL}")
        return True
        
    except Exception as e:
        print(f"{Fore.RED}    ⚠ Failed to save checkpoint IP: {e}{Style.RESET_ALL}")
        return False

def save_blocked_ip(ip: str, isp: str, country: str, reason: str = None) -> bool:
    """Save blocked IP to blacklist - NEVER use this IP again
    
    Args:
        ip: The IP address that got blocked
        isp: The ISP name
        country: The country code
        reason: Reason for block (rate_limit, ip_block, proxy_detected, etc.)
        
    Returns:
        True if saved successfully
    """
    global _blocked_ips_cache
    try:
        blocked_ips = []
        if os.path.exists(BLOCKED_IPS_FILE):
            try:
                with open(BLOCKED_IPS_FILE, 'r') as f:
                    blocked_ips = json.load(f)
            except:
                blocked_ips = []
        
        # Check for duplicates
        existing_ips = {entry.get("ip") for entry in blocked_ips}
        if ip in existing_ips:
            return False
        
        new_entry = {
            "ip": ip,
            "isp": isp,
            "country": country,
            "status": "blocked",
            "reason": reason,
            "blocked_date": datetime.now().isoformat(),
            "timestamp": time.time()
        }
        blocked_ips.append(new_entry)
        
        with open(BLOCKED_IPS_FILE, 'w') as f:
            json.dump(blocked_ips, f, indent=2)
        
        # Update in-memory cache
        _blocked_ips_cache.add(ip)
        
        print(f"{Fore.RED}    🚫 Saved BLOCKED IP: {ip} ({isp}) [{country}] - Reason: {reason} → {BLOCKED_IPS_FILE}{Style.RESET_ALL}")
        return True
        
    except Exception as e:
        print(f"{Fore.RED}    ⚠ Failed to save blocked IP: {e}{Style.RESET_ALL}")
        return False

def get_working_ips() -> List[Dict[str, Any]]:
    """Load all saved working IPs"""
    try:
        if os.path.exists(WORKING_IPS_FILE):
            with open(WORKING_IPS_FILE, 'r') as f:
                return json.load(f)
    except:
        pass
    return []

def get_checkpoint_ips() -> List[Dict[str, Any]]:
    """Load all saved checkpoint IPs"""
    try:
        if os.path.exists(CHECKPOINT_IPS_FILE):
            with open(CHECKPOINT_IPS_FILE, 'r') as f:
                return json.load(f)
    except:
        pass
    return []

def get_blocked_ips() -> List[Dict[str, Any]]:
    """Load all blocked IPs"""
    try:
        if os.path.exists(BLOCKED_IPS_FILE):
            with open(BLOCKED_IPS_FILE, 'r') as f:
                return json.load(f)
    except:
        pass
    return []

def get_ip_stats() -> Dict[str, int]:
    """Get statistics of all IP categories"""
    return {
        "working": len(get_working_ips()),
        "checkpoint": len(get_checkpoint_ips()),
        "blocked": len(get_blocked_ips())
    }

def get_working_ip_count() -> int:
    """Get count of saved working IPs"""
    return len(get_working_ips())


# ===================== ISP SUCCESS RATE TRACKING =====================
# Track success rate per ISP to prioritize high-performing ISPs

ISP_STATS_FILE = "isp_stats.json"

def get_isp_stats() -> Dict[str, Dict[str, int]]:
    """Load ISP statistics"""
    try:
        if os.path.exists(ISP_STATS_FILE):
            with open(ISP_STATS_FILE, 'r') as f:
                return json.load(f)
    except:
        pass
    return {}

def update_isp_stats(isp: str, result: str):
    """Update ISP statistics
    
    Args:
        isp: ISP name
        result: "success", "checkpoint", or "blocked"
    """
    try:
        stats = get_isp_stats()
        
        if isp not in stats:
            stats[isp] = {"success": 0, "checkpoint": 0, "blocked": 0, "total": 0}
        
        stats[isp][result] = stats[isp].get(result, 0) + 1
        stats[isp]["total"] = stats[isp].get("total", 0) + 1
        stats[isp]["success_rate"] = round(stats[isp]["success"] / max(stats[isp]["total"], 1) * 100, 2)
        stats[isp]["last_updated"] = datetime.now().isoformat()
        
        with open(ISP_STATS_FILE, 'w') as f:
            json.dump(stats, f, indent=2)
            
    except Exception as e:
        pass

def get_best_isps(min_attempts: int = 3) -> List[Tuple[str, float]]:
    """Get ISPs sorted by success rate (highest first)
    
    Args:
        min_attempts: Minimum attempts required to be considered
        
    Returns:
        List of (isp_name, success_rate) tuples sorted by success rate
    """
    stats = get_isp_stats()
    
    isps_with_stats = []
    for isp, data in stats.items():
        if data.get("total", 0) >= min_attempts:
            success_rate = data.get("success_rate", 0)
            isps_with_stats.append((isp, success_rate))
    
    # Sort by success rate (highest first)
    isps_with_stats.sort(key=lambda x: x[1], reverse=True)
    return isps_with_stats

def print_isp_stats():
    """Print ISP statistics table"""
    stats = get_isp_stats()
    if not stats:
        print(f"{Fore.YELLOW}No ISP statistics yet{Style.RESET_ALL}")
        return
    
    print(f"\n{Fore.CYAN}{'='*60}")
    print(f"ISP SUCCESS RATE STATISTICS")
    print(f"{'='*60}{Style.RESET_ALL}")
    print(f"{'ISP':<15} {'Success':<8} {'CP':<6} {'Block':<7} {'Total':<7} {'Rate':<8}")
    print(f"{'-'*60}")
    
    # Sort by success rate
    sorted_stats = sorted(stats.items(), key=lambda x: x[1].get("success_rate", 0), reverse=True)
    
    for isp, data in sorted_stats:
        success = data.get("success", 0)
        checkpoint = data.get("checkpoint", 0)
        blocked = data.get("blocked", 0)
        total = data.get("total", 0)
        rate = data.get("success_rate", 0)
        
        # Color based on success rate
        if rate >= 50:
            color = Fore.GREEN
        elif rate >= 25:
            color = Fore.YELLOW
        else:
            color = Fore.RED
        
        print(f"{color}{isp:<15} {success:<8} {checkpoint:<6} {blocked:<7} {total:<7} {rate:.1f}%{Style.RESET_ALL}")
    
    print(f"{'-'*60}\n")


# ===================== API ANTI-DETECTION TIMING SYSTEM =====================
# Timing patterns optimized for Instagram API (not web browser)

class APIAntiDetectionTiming:
    """
    API Anti-Detection Timing System
    
    Optimized for Instagram API requests (not web browsing)
    
    Features:
    - API request pacing (not too fast, not too slow)
    - Session header consistency
    - Rate limit detection and handling
    - Optimal delays between API calls
    """
    
    def __init__(self):
        self.session_start_times = {}
        self.last_request_times = {}
        self.request_counts = {}
        self.rate_limit_hits = {}
    
    def get_api_delay(self, request_type: str = "default") -> float:
        """Get optimal delay for API requests
        
        Request types:
        - csrf: Get CSRF token (fast)
        - check_email: Check email availability
        - check_username: Check username availability
        - send_code: Send verification code
        - verify_code: Verify email code
        - create_account: Create account (most sensitive)
        - between_accounts: Between account creations
        """
        delays = {
            "csrf": (0.5, 1.5),
            "check_email": (1.0, 2.5),
            "check_username": (1.0, 2.5),
            "send_code": (1.5, 3.0),
            "verify_code": (2.0, 4.0),
            "create_account": (2.0, 5.0),
            "between_accounts": (8.0, 15.0),
            "after_error": (3.0, 6.0),
            "after_rate_limit": (30.0, 60.0),
            "default": (1.0, 3.0),
        }
        
        min_delay, max_delay = delays.get(request_type, delays["default"])
        
        # Add slight randomness for natural timing
        delay = random.uniform(min_delay, max_delay)
        
        return delay
    
    def start_session(self, session_id: str):
        """Mark session start time"""
        self.session_start_times[session_id] = time.time()
        self.request_counts[session_id] = 0
        self.rate_limit_hits[session_id] = 0
    
    def record_request(self, session_id: str):
        """Record a request for pacing"""
        self.last_request_times[session_id] = time.time()
        self.request_counts[session_id] = self.request_counts.get(session_id, 0) + 1
    
    def record_rate_limit(self, session_id: str):
        """Record rate limit hit"""
        self.rate_limit_hits[session_id] = self.rate_limit_hits.get(session_id, 0) + 1
    
    def get_request_count(self, session_id: str) -> int:
        """Get request count for session"""
        return self.request_counts.get(session_id, 0)
    
    def should_slow_down(self, session_id: str) -> bool:
        """Check if session should slow down (too many requests)"""
        count = self.request_counts.get(session_id, 0)
        rate_limits = self.rate_limit_hits.get(session_id, 0)
        
        # Slow down if hit rate limit or many requests
        return rate_limits > 0 or count > 15
    
    def get_delay_multiplier(self, session_id: str) -> float:
        """Get delay multiplier based on session history"""
        rate_limits = self.rate_limit_hits.get(session_id, 0)
        count = self.request_counts.get(session_id, 0)
        
        multiplier = 1.0
        
        # Increase delay if hit rate limits
        if rate_limits > 0:
            multiplier += rate_limits * 0.5
        
        # Slight increase for many requests
        if count > 20:
            multiplier += 0.3
        elif count > 10:
            multiplier += 0.1
        
        return min(multiplier, 3.0)  # Max 3x delay
    
    def get_next_delay(self, session_id: str, request_type: str = "default") -> float:
        """Get delay before next request with multiplier applied"""
        base_delay = self.get_api_delay(request_type)
        multiplier = self.get_delay_multiplier(session_id)
        return base_delay * multiplier
    
    def should_rotate_session(self, session_id: str) -> Tuple[bool, str]:
        """Check if session should be rotated
        
        Returns:
            (should_rotate, reason)
        """
        rate_limits = self.rate_limit_hits.get(session_id, 0)
        count = self.request_counts.get(session_id, 0)
        
        if rate_limits >= 2:
            return True, "Too many rate limits"
        
        if count >= 30:
            return True, "Too many requests"
        
        return False, ""


# Global API anti-detection timing instance
api_timing = APIAntiDetectionTiming()


# ===================== SMART ISP SELECTOR =====================
# Select ISP based on success rate and availability

def get_smart_isp(ip_type: str = "mobile", exclude_isps: List[str] = None) -> str:
    """Get best ISP based on success rate statistics
    
    Args:
        ip_type: "mobile" or "residential"
        exclude_isps: List of ISPs to exclude (e.g., recently failed)
        
    Returns:
        ISP name with highest success rate
    """
    exclude_isps = exclude_isps or []
    
    # Default ISPs by type - PRIORITIZE MOBILE
    mobile_isps = ["telkomsel", "indosat", "xl", "tri", "smartfren"]
    wifi_isps = ["biznet", "indihome", "myrepublic", "cbn", "firstmedia"]
    
    default_isps = mobile_isps if ip_type == "mobile" else wifi_isps
    
    # Get ISPs with best success rate
    best_isps = get_best_isps(min_attempts=2)
    
    # Filter by type and exclusions
    available_isps = []
    for isp, rate in best_isps:
        if isp in exclude_isps:
            continue
        if ip_type == "mobile" and isp in mobile_isps:
            available_isps.append((isp, rate))
        elif ip_type == "residential" and isp in wifi_isps:
            available_isps.append((isp, rate))
    
    # If we have ISPs with good stats, use weighted random selection
    if available_isps:
        # Weight by success rate
        isps = [isp for isp, _ in available_isps]
        weights = [max(rate, 1) for _, rate in available_isps]
        
        # Weighted random choice
        total = sum(weights)
        r = random.uniform(0, total)
        cumulative = 0
        for isp, weight in zip(isps, weights):
            cumulative += weight
            if r <= cumulative:
                return isp
    
    # Fallback to random from default ISPs (excluding blocked ones)
    available_defaults = [isp for isp in default_isps if isp not in exclude_isps]
    if available_defaults:
        return random.choice(available_defaults)
    
    # Last resort
    return random.choice(default_isps)


# ===================== CURL_CFFI HTTP CLIENT =====================
# Best anti-detection HTTP client with Chrome TLS fingerprint impersonation
# curl_cffi impersonates REAL Chrome browser TLS fingerprint (JA3)

class ChromeImpersonateClient:
    """
    Chrome Impersonate HTTP Client using curl_cffi
    
    This is the BEST option for anti-detection because:
    1. Impersonates REAL Chrome TLS fingerprint (JA3)
    2. HTTP/2 support like real Chrome
    3. Same cipher suites as Chrome
    4. Instagram cannot detect it as Python/bot
    5. Full TLS 1.3 support with correct extensions
    6. Correct ALPN negotiation (h2, http/1.1)
    7. Real Chrome User-Agent header order
    
    JA3 Fingerprint Info:
    - JA3 is a method to fingerprint TLS clients
    - curl_cffi uses libcurl compiled with specific TLS settings
    - It produces IDENTICAL JA3 hash as real Chrome browser
    
    Fallback to aiohttp if curl_cffi not available
    """
    
    # Chrome versions to impersonate (latest versions for 2025)
    # Format: "chrome{version}" 
    CHROME_VERSIONS = [
        # 2024 versions
        "chrome120", "chrome123", "chrome124",
        # 2025 versions (latest - best compatibility)
        "chrome126", "chrome127", "chrome128", "chrome129",
        "chrome131", "chrome133", "chrome134", "chrome135", "chrome136",
    ]
    
    # Real Chrome JA3 fingerprints for reference
    # These are automatically handled by curl_cffi impersonation
    CHROME_JA3_FINGERPRINTS = {
        "chrome120": "771,4865-4866-4867-49195-49199-49196-49200-52393-52392-49171-49172-156-157-47-53,0-23-65281-10-11-35-16-5-13-18-51-45-43-27-17513,29-23-24,0",
        "chrome131": "771,4865-4866-4867-49195-49199-49196-49200-52393-52392-49171-49172-156-157-47-53,0-23-65281-10-11-35-16-5-13-18-51-45-43-27-17513-21,29-23-24,0",
    }
    
    # HTTP/2 settings that match Chrome
    HTTP2_SETTINGS = {
        "HEADER_TABLE_SIZE": 65536,
        "ENABLE_PUSH": 0,
        "MAX_CONCURRENT_STREAMS": 1000,
        "INITIAL_WINDOW_SIZE": 6291456,
        "MAX_FRAME_SIZE": 16384,
        "MAX_HEADER_LIST_SIZE": 262144,
    }
    
    def __init__(self, chrome_version: str = None, device_type: str = "desktop"):
        """Initialize Chrome impersonate client
        
        Args:
            chrome_version: Chrome version to impersonate (e.g., "chrome120")
                           If None, randomly selects from recent versions
            device_type: "desktop" or "android" - affects User-Agent and fingerprint
        """
        # Use latest Chrome versions for best compatibility
        self.chrome_version = chrome_version or random.choice(self.CHROME_VERSIONS[-5:])
        self.device_type = device_type
        self._sync_session = None
        self._async_session = None
        self.cookies = {}
        self.default_headers = {}
        
        # TLS/JA3 Configuration
        self.tls_config = self._generate_tls_config()
        
        # Check if curl_cffi is available
        self.use_curl_cffi = HAVE_CURL_CFFI
        
        if self.use_curl_cffi:
            print(f"    🔒 Using curl_cffi with {self.chrome_version} impersonation")
            print(f"    📍 TLS: {self.tls_config['tls_version']} | HTTP/2: Enabled | JA3: Real Chrome")
        else:
            print(f"    ⚠️ curl_cffi not available, using aiohttp (LESS SECURE - may get blocked)")
    
    def _generate_tls_config(self) -> Dict[str, Any]:
        """Generate TLS configuration matching real Chrome"""
        chrome_major = int(self.chrome_version.replace("chrome", ""))
        
        return {
            "tls_version": "TLS 1.3",
            "cipher_suites": [
                "TLS_AES_128_GCM_SHA256",
                "TLS_AES_256_GCM_SHA384",
                "TLS_CHACHA20_POLY1305_SHA256",
                "TLS_ECDHE_ECDSA_WITH_AES_128_GCM_SHA256",
                "TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256",
                "TLS_ECDHE_ECDSA_WITH_AES_256_GCM_SHA384",
                "TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384",
                "TLS_ECDHE_ECDSA_WITH_CHACHA20_POLY1305_SHA256",
                "TLS_ECDHE_RSA_WITH_CHACHA20_POLY1305_SHA256",
            ],
            "extensions": [
                "server_name", "extended_master_secret", "renegotiation_info",
                "supported_groups", "ec_point_formats", "session_ticket",
                "application_layer_protocol_negotiation", "status_request",
                "signature_algorithms", "signed_certificate_timestamp",
                "key_share", "psk_key_exchange_modes", "supported_versions",
                "compress_certificate", "application_settings",
            ],
            "supported_groups": ["x25519", "secp256r1", "secp384r1"],
            "alpn": ["h2", "http/1.1"],
            "chrome_version": chrome_major,
            "ja3_hash": self.CHROME_JA3_FINGERPRINTS.get(self.chrome_version, "real_chrome"),
        }
    
    def get_tls_fingerprint(self) -> Dict[str, Any]:
        """Get current TLS fingerprint configuration"""
        return {
            **self.tls_config,
            "impersonate": self.chrome_version,
            "http2_settings": self.HTTP2_SETTINGS,
            "device_type": self.device_type,
        }
    
    def set_headers(self, headers: Dict[str, str]):
        """Set default headers for all requests"""
        self.default_headers = headers.copy()
    
    def set_cookies(self, cookies: Dict[str, str]):
        """Set cookies for all requests"""
        self.cookies = cookies.copy()
    
    def update_cookies(self, new_cookies: Dict[str, str]):
        """Update cookies (merge with existing)"""
        self.cookies.update(new_cookies)
    
    def _get_sync_session(self):
        """Get or create sync session with Chrome impersonation"""
        if self.use_curl_cffi and CurlSession:
            if not self._sync_session:
                self._sync_session = CurlSession(
                    impersonate=self.chrome_version,
                    # Additional options for better impersonation
                    verify=True,  # Verify SSL certificates
                )
            return self._sync_session
        return None
    
    async def _get_async_session(self):
        """Get or create async session with Chrome impersonation"""
        if self.use_curl_cffi and CurlAsyncSession:
            if not self._async_session:
                self._async_session = CurlAsyncSession(
                    impersonate=self.chrome_version,
                    verify=True,
                )
            return self._async_session
        return None
    
    def _prepare_headers(self, custom_headers: Dict[str, str] = None) -> Dict[str, str]:
        """Prepare headers in correct Chrome order"""
        # Chrome sends headers in a specific order
        # curl_cffi handles most of this, but we ensure our custom headers are correct
        headers = {}
        
        # Add default headers first
        headers.update(self.default_headers)
        
        # Add custom headers
        if custom_headers:
            headers.update(custom_headers)
        
        return headers
    
    async def get(self, url: str, headers: Dict[str, str] = None, 
                  timeout: int = 30, allow_redirects: bool = True, **kwargs) -> Dict[str, Any]:
        """Async GET request with Chrome impersonation
        
        Features:
        - Real Chrome TLS fingerprint (JA3)
        - HTTP/2 with correct settings
        - Proper header ordering
        - Cookie handling like real browser
        """
        merged_headers = self._prepare_headers(headers)
        
        try:
            if self.use_curl_cffi:
                session = await self._get_async_session()
                response = await session.get(
                    url,
                    headers=merged_headers,
                    cookies=self.cookies,
                    timeout=timeout,
                    allow_redirects=allow_redirects,
                    **kwargs
                )
                
                # Update cookies from response
                if response.cookies:
                    self.cookies.update(dict(response.cookies))
                
                return {
                    "status": response.status_code,
                    "body": response.content,
                    "headers": dict(response.headers),
                    "cookies": dict(response.cookies),
                    "url": str(response.url),
                    "http_version": "HTTP/2" if self.use_curl_cffi else "HTTP/1.1",
                }
            elif HAVE_AIOHTTP:
                # Fallback to aiohttp (less secure)
                timeout_obj = aiohttp.ClientTimeout(total=timeout)
                async with aiohttp.ClientSession(timeout=timeout_obj) as session:
                    async with session.get(url, headers=merged_headers, cookies=self.cookies, 
                                          allow_redirects=allow_redirects) as response:
                        body = await response.read()
                        return {
                            "status": response.status,
                            "body": body,
                            "headers": dict(response.headers),
                            "cookies": {k: v.value for k, v in response.cookies.items()},
                            "url": str(response.url),
                            "http_version": "HTTP/1.1",
                        }
            else:
                # Last resort: sync requests
                import requests as req_lib
                response = req_lib.get(url, headers=merged_headers, cookies=self.cookies, 
                                      timeout=timeout, allow_redirects=allow_redirects)
                return {
                    "status": response.status_code,
                    "body": response.content,
                    "headers": dict(response.headers),
                    "cookies": dict(response.cookies),
                    "url": response.url,
                    "http_version": "HTTP/1.1",
                }
        except Exception as e:
            return {"status": 0, "error": str(e), "body": b"", "headers": {}, "cookies": {}}
    
    async def post(self, url: str, data: Any = None, json_data: Any = None,
                   headers: Dict[str, str] = None, timeout: int = 30, 
                   allow_redirects: bool = True, **kwargs) -> Dict[str, Any]:
        """Async POST request with Chrome impersonation
        
        Features:
        - Real Chrome TLS fingerprint (JA3)
        - HTTP/2 with correct settings
        - Proper Content-Type handling
        - Cookie handling like real browser
        """
        merged_headers = self._prepare_headers(headers)
        
        try:
            if self.use_curl_cffi:
                session = await self._get_async_session()
                
                # Handle JSON data
                if json_data is not None:
                    response = await session.post(
                        url,
                        json=json_data,
                        headers=merged_headers,
                        cookies=self.cookies,
                        timeout=timeout,
                        allow_redirects=allow_redirects,
                        **kwargs
                    )
                else:
                    response = await session.post(
                        url,
                        data=data,
                        headers=merged_headers,
                        cookies=self.cookies,
                        timeout=timeout,
                        allow_redirects=allow_redirects,
                        **kwargs
                    )
                
                # Update cookies from response
                if response.cookies:
                    self.cookies.update(dict(response.cookies))
                
                return {
                    "status": response.status_code,
                    "body": response.content,
                    "headers": dict(response.headers),
                    "cookies": dict(response.cookies),
                    "url": str(response.url),
                    "http_version": "HTTP/2" if self.use_curl_cffi else "HTTP/1.1",
                }
            elif HAVE_AIOHTTP:
                # Fallback to aiohttp
                timeout_obj = aiohttp.ClientTimeout(total=timeout)
                async with aiohttp.ClientSession(timeout=timeout_obj) as session:
                    if json_data is not None:
                        async with session.post(url, json=json_data, headers=merged_headers, 
                                               cookies=self.cookies, allow_redirects=allow_redirects) as response:
                            body = await response.read()
                            return {
                                "status": response.status,
                                "body": body,
                                "headers": dict(response.headers),
                                "cookies": {k: v.value for k, v in response.cookies.items()},
                                "url": str(response.url),
                                "http_version": "HTTP/1.1",
                            }
                    else:
                        async with session.post(url, data=data, headers=merged_headers, 
                                               cookies=self.cookies, allow_redirects=allow_redirects) as response:
                            body = await response.read()
                            return {
                                "status": response.status,
                                "body": body,
                                "headers": dict(response.headers),
                                "cookies": {k: v.value for k, v in response.cookies.items()},
                                "url": str(response.url),
                                "http_version": "HTTP/1.1",
                            }
            else:
                # Last resort: sync requests
                import requests as req_lib
                if json_data is not None:
                    response = req_lib.post(url, json=json_data, headers=merged_headers, 
                                           cookies=self.cookies, timeout=timeout, 
                                           allow_redirects=allow_redirects)
                else:
                    response = req_lib.post(url, data=data, headers=merged_headers, 
                                           cookies=self.cookies, timeout=timeout,
                                           allow_redirects=allow_redirects)
                return {
                    "status": response.status_code,
                    "body": response.content,
                    "headers": dict(response.headers),
                    "cookies": dict(response.cookies),
                    "url": response.url,
                    "http_version": "HTTP/1.1",
                }
        except Exception as e:
            return {"status": 0, "error": str(e), "body": b"", "headers": {}, "cookies": {}}
    
    async def close(self):
        """Close sessions"""
        if self._async_session:
            try:
                await self._async_session.close()
            except:
                pass
        if self._sync_session:
            try:
                self._sync_session.close()
            except:
                pass
    
    def get_impersonate_info(self) -> Dict[str, Any]:
        """Get detailed info about current impersonation"""
        return {
            "library": "curl_cffi" if self.use_curl_cffi else "aiohttp",
            "chrome_version": self.chrome_version if self.use_curl_cffi else "N/A",
            "device_type": self.device_type,
            "tls_fingerprint": self.tls_config,
            "http2": self.use_curl_cffi,
            "http2_settings": self.HTTP2_SETTINGS if self.use_curl_cffi else None,
            "anti_detection_level": "MAXIMUM" if self.use_curl_cffi else "LOW",
            "ja3_hash": self.tls_config.get("ja3_hash", "unknown"),
        }
    
    def __repr__(self) -> str:
        return f"ChromeImpersonateClient({self.chrome_version}, curl_cffi={self.use_curl_cffi})"


def get_best_http_client(chrome_version: str = None, device_type: str = "desktop") -> ChromeImpersonateClient:
    """Get the best available HTTP client for anti-detection
    
    Priority:
    1. curl_cffi with Chrome impersonation (BEST - Real JA3 fingerprint)
    2. aiohttp (fallback - Python TLS fingerprint, may be detected)
    
    Args:
        chrome_version: Chrome version to impersonate
        device_type: "desktop" or "android"
    
    Returns:
        ChromeImpersonateClient instance
    """
    return ChromeImpersonateClient(chrome_version, device_type)


# ===================== UNIFIED SESSION MANAGER 2025 =====================
# Manages all spoofing components in a consistent, synchronized manner

class UnifiedSessionManager2025:
    """
    Unified Session Manager - CRITICAL for anti-detection
    
    This class ensures ALL spoofing components are synchronized and consistent
    within a single session to prevent IP blocks and API errors.
    
    Components managed:
    - IP Address (Indonesian ISP only)
    - Device fingerprint (Android/Desktop)
    - User-Agent (matching device)
    - Headers (consistent with browser/device)
    - Cookies (session-bound)
    - TLS/JA3 fingerprint (matching browser version)
    - JA3S (server response fingerprint)
    - WebGL fingerprint (matching GPU)
    - WebRTC (matching network)
    - Canvas fingerprint
    - Audio fingerprint
    """
    
    # Session storage
    _sessions: Dict[str, Dict[str, Any]] = {}
    
    def __init__(self):
        self._sessions = {}
        self._lock = None  # Will use threading.Lock() if needed
        
        # Default location - will be random per session
        self.location = "random"
        self.timezone = "UTC"
        self.language = "en-US"
        
        # Chrome version consistency
        self.chrome_versions = {
            "windows": list(range(120, 136)),
            "macos": list(range(120, 136)),
            "android": list(range(120, 136)),
        }
    
    def create_session(self, session_id: str = None, device_type: str = "random", country: str = "random") -> Dict[str, Any]:
        """
        Create a new unified session with all spoofing components synchronized.
        
        Args:
            session_id: Optional session ID. Auto-generated if not provided.
            device_type: "android", "desktop", or "random"
            country: Country code (e.g. "US", "AU", "JP") or "random" for truly random country
        
        Returns:
            Complete session configuration with all components synchronized
        """
        if not session_id:
            session_id = self._generate_session_id()
        
        # Determine device type
        if device_type == "random":
            device_type = random.choice(["android", "desktop"])
        
        # Load country database and select random country if needed
        country_db = self._load_country_database_session()
        all_countries = list(country_db.get("countries", {}).keys())
        if not all_countries:
            all_countries = ["US", "AU", "CA", "GB", "DE", "FR", "JP", "KR", "SG", "NL", "NZ", "IT", "ES", "MX", "BR", "TH", "MY", "PH", "VN", "IN", "ID"]
        
        # Select random country if not specified
        if country == "random":
            country = random.choice(all_countries)
        
        # Get country-specific data
        country_data = country_db.get("countries", {}).get(country, {})
        if not country_data:
            # Fallback to defaults
            country_data = {
                "name": country,
                "language": "en-US",
                "timezone": "America/New_York",
                "locale": "en_US",
                "isps": {},
                "cities": [{"name": "Unknown", "lat": 0, "lon": 0}],
                "devices": {"mobile": ["iPhone 15 Pro"], "desktop": ["MacBook Pro"]}
            }
        
        # Select consistent platform
        if device_type == "android":
            platform_info = self._generate_android_platform_for_country(country, country_data)
        else:
            platform_info = self._generate_desktop_platform_for_country(country, country_data)
        
        # Generate consistent Chrome version
        chrome_version = random.choice(self.chrome_versions[platform_info["os_type"]])
        
        # Generate IP from country-specific ISP
        ip_config = self._generate_ip_for_country(country, country_data, device_type, platform_info)
        
        # Generate synchronized fingerprints
        session = {
            "session_id": session_id,
            "created_at": time.time(),
            "device_type": device_type,
            "country": country,
            
            # Platform info
            "platform": platform_info,
            "chrome_version": chrome_version,
            
            # IP Configuration
            "ip": ip_config,
            
            # User-Agent (synchronized with device & Chrome version)
            "user_agent": self._generate_user_agent(platform_info, chrome_version),
            
            # Headers (synchronized with everything)
            "headers": self._generate_headers(platform_info, chrome_version, ip_config),
            
            # TLS/JA3 fingerprint (synchronized with Chrome version)
            "tls": self._generate_tls_config(chrome_version),
            
            # Device fingerprint (synchronized with platform AND country)
            "fingerprint": self._generate_device_fingerprint(platform_info, chrome_version, country_data),
            
            # Cookies (session-specific)
            "cookies": self._generate_initial_cookies(session_id),
            
            # Location (matches IP country)
            "location": {
                "country": country,
                "country_name": country_data.get("name", country),
                "timezone": country_data.get("timezone", "America/New_York"),
                "language": country_data.get("language", "en-US"),
                "locale": country_data.get("locale", "en_US"),
            },
        }
        
        # Store session
        self._sessions[session_id] = session
        
        return session
    
    def _load_country_database_session(self) -> Dict[str, Any]:
        """Load comprehensive country database from JSON file"""
        try:
            db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "country_database.json")
            if os.path.exists(db_path):
                with open(db_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            pass
        return {"countries": {}}
    
    def _generate_android_platform_for_country(self, country: str, country_data: Dict) -> Dict[str, Any]:
        """Generate Android platform info specific to country"""
        devices = country_data.get("devices", {}).get("mobile", ["Samsung Galaxy A54"])
        device = random.choice(devices)
        
        return {
            "os_type": "android",
            "os": "Android",
            "os_version": random.choice(["13", "14"]),
            "device": device,
            "device_model": device.split()[-1] if " " in device else device,
            "country": country,
            "hardware": {
                "ram": random.choice([6, 8, 12, 16]),
                "storage": random.choice([128, 256, 512]),
            }
        }
    
    def _generate_desktop_platform_for_country(self, country: str, country_data: Dict) -> Dict[str, Any]:
        """Generate desktop platform info specific to country"""
        devices = country_data.get("devices", {}).get("desktop", ["MacBook Pro"])
        device = random.choice(devices)
        
        # Determine OS from device name
        if "mac" in device.lower():
            os_type = "macos"
            os_name = "macOS"
            os_version = random.choice(["14.4", "14.3", "14.2"])
        else:
            os_type = "windows"
            os_name = "Windows"
            os_version = random.choice(["10", "11"])
        
        return {
            "os_type": os_type,
            "os": os_name,
            "os_version": os_version,
            "device": device,
            "device_model": device,
            "country": country,
            "hardware": {
                "ram": random.choice([16, 32, 64]),
                "storage": random.choice([512, 1024, 2048]),
            }
        }
    
    def _generate_ip_for_country(self, country: str, country_data: Dict, device_type: str, platform_info: Dict) -> Dict[str, Any]:
        """Generate IP address from country-specific ISP with full synchronization"""
        isps = country_data.get("isps", {})
        
        # Prioritize mobile ISPs for mobile devices
        if device_type == "android":
            isp_pool = isps.get("mobile", {})
        else:
            isp_pool = isps.get("broadband", {}) or isps.get("mobile", {})
        
        if not isp_pool:
            # Fallback: generate plausible IP
            ip = f"{random.randint(1, 223)}.{random.randint(1, 254)}.{random.randint(1, 254)}.{random.randint(2, 253)}"
            return {
                "ip": ip,
                "isp": "unknown",
                "asn": "AS0",
                "country": country,
                "type": "wifi" if device_type == "desktop" else "mobile",
            }
        
        # Select random ISP
        isp_name = random.choice(list(isp_pool.keys()))
        isp_data = isp_pool[isp_name]
        
        # Generate IP from ISP ranges
        ranges = isp_data.get("ranges", [])
        if ranges:
            ip_range = random.choice(ranges)
            ip = self._generate_ip_from_cidr(ip_range)
        else:
            ip = f"{random.randint(1, 223)}.{random.randint(1, 254)}.{random.randint(1, 254)}.{random.randint(2, 253)}"
        
        # Select city
        cities = country_data.get("cities", [{"name": "Unknown", "lat": 0, "lon": 0}])
        city = random.choice(cities)
        
        return {
            "ip": ip,
            "isp": isp_data.get("name", isp_name),
            "asn": isp_data.get("asn", "AS0"),
            "country": country,
            "country_name": country_data.get("name", country),
            "city": city.get("name", "Unknown"),
            "latitude": city.get("lat", 0) + random.uniform(-0.01, 0.01),
            "longitude": city.get("lon", 0) + random.uniform(-0.01, 0.01),
            "type": "wifi" if device_type == "desktop" else "mobile",
            "timezone": country_data.get("timezone", "UTC"),
        }
    
    def _generate_ip_from_cidr(self, cidr: str) -> str:
        """Generate random IP from CIDR range"""
        try:
            network = ipaddress.ip_network(cidr, strict=False)
            # Get random IP from network (avoiding first and last)
            hosts = list(network.hosts())
            if len(hosts) > 10:
                # Avoid common IPs (first 5, last 5)
                hosts = hosts[5:-5]
            if hosts:
                return str(random.choice(hosts))
        except Exception:
            pass
        
        # Fallback: parse CIDR and generate
        parts = cidr.split('/')[0].split('.')
        while len(parts) < 4:
            parts.append(str(random.randint(2, 253)))
        return '.'.join(parts[:4])
    
    def get_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Get existing session configuration"""
        return self._sessions.get(session_id)
    
    def get_headers_for_request(self, session_id: str, request_type: str = "api") -> Dict[str, str]:
        """
        Get headers for a specific request type, maintaining session consistency.
        
        Args:
            session_id: The session ID
            request_type: "api", "ajax", "form", "graphql"
        """
        session = self._sessions.get(session_id)
        if not session:
            session = self.create_session(session_id)
        
        base_headers = session["headers"].copy()
        
        # Add request-type specific headers
        if request_type == "ajax":
            base_headers["X-Requested-With"] = "XMLHttpRequest"
            base_headers["X-Instagram-AJAX"] = "1"
        elif request_type == "form":
            base_headers["Content-Type"] = "application/x-www-form-urlencoded"
        elif request_type == "graphql":
            base_headers["Content-Type"] = "application/json"
            base_headers["X-FB-Friendly-Name"] = "true"
        
        return base_headers
    
    def update_cookies(self, session_id: str, new_cookies: Dict[str, str]):
        """Update cookies for a session"""
        if session_id in self._sessions:
            self._sessions[session_id]["cookies"].update(new_cookies)
    
    def get_cookies(self, session_id: str) -> Dict[str, str]:
        """Get cookies for a session"""
        session = self._sessions.get(session_id)
        return session["cookies"] if session else {}
    
    def _generate_session_id(self) -> str:
        """Generate unique session ID"""
        timestamp = int(time.time() * 1000)
        random_part = secrets.token_hex(8)
        return f"sess_{timestamp}_{random_part}"
    
    def _generate_android_platform(self) -> Dict[str, Any]:
        """Generate Android device platform info"""
        # Popular Android devices in Indonesia
        devices = [
            {"brand": "Samsung", "model": "SM-S928B", "name": "Galaxy S24 Ultra", "android": "14", "sdk": 34},
            {"brand": "Samsung", "model": "SM-A546E", "name": "Galaxy A54 5G", "android": "14", "sdk": 34},
            {"brand": "Samsung", "model": "SM-A346E", "name": "Galaxy A34 5G", "android": "14", "sdk": 34},
            {"brand": "Xiaomi", "model": "23113RKC6G", "name": "Xiaomi 14 Pro", "android": "14", "sdk": 34},
            {"brand": "Xiaomi", "model": "22071219CG", "name": "Redmi Note 12 Pro", "android": "13", "sdk": 33},
            {"brand": "OPPO", "model": "CPH2519", "name": "OPPO Reno 10 Pro+", "android": "13", "sdk": 33},
            {"brand": "Vivo", "model": "V2254", "name": "Vivo V29", "android": "13", "sdk": 33},
            {"brand": "Realme", "model": "RMX3771", "name": "Realme 11 Pro+", "android": "13", "sdk": 33},
        ]
        
        device = random.choice(devices)
        
        return {
            "os_type": "android",
            "os_name": "Android",
            "os_version": device["android"],
            "device_brand": device["brand"],
            "device_model": device["model"],
            "device_name": device["name"],
            "sdk_version": device["sdk"],
            "screen_width": random.choice([1080, 1440]),
            "screen_height": random.choice([2340, 2400, 3088, 3200]),
            "pixel_ratio": random.choice([2.5, 3.0, 3.5]),
            "platform": "Linux armv8l",
            "vendor": device["brand"],
        }
    
    def _generate_desktop_platform(self) -> Dict[str, Any]:
        """Generate Desktop platform info"""
        os_choice = random.choice(["windows", "macos"])
        
        if os_choice == "windows":
            return {
                "os_type": "windows",
                "os_name": "Windows",
                "os_version": "10" if random.random() < 0.3 else "11",
                "device_brand": random.choice(["Dell", "HP", "Lenovo", "ASUS", "Acer"]),
                "device_model": random.choice(["XPS 15", "Spectre x360", "ThinkPad X1 Carbon", "ZenBook Pro", "Swift 5"]),
                "screen_width": random.choice([1920, 2560, 3840]),
                "screen_height": random.choice([1080, 1440, 2160]),
                "pixel_ratio": 1.0,
                "platform": "Win32",
                "vendor": "Google Inc.",
            }
        else:
            return {
                "os_type": "macos",
                "os_name": "macOS",
                "os_version": random.choice(["13.0", "13.5", "14.0", "14.2"]),
                "device_brand": "Apple",
                "device_model": random.choice(["MacBook Pro 16", "MacBook Pro 14", "MacBook Air M2"]),
                "screen_width": random.choice([2560, 3024, 3456]),
                "screen_height": random.choice([1600, 1964, 2234]),
                "pixel_ratio": 2.0,
                "platform": "MacIntel",
                "vendor": "Apple Computer, Inc.",
            }
    
    def _generate_indonesia_ip(self, device_type: str, platform_info: Dict) -> Dict[str, Any]:
        """Generate Indonesian IP based on device type
        
        IP ranges are VERIFIED from APNIC WHOIS database (https://wq.apnic.net/)
        Each range has been manually verified to return Indonesia in geolocation.
        
        Verification method:
        1. APNIC WHOIS lookup for netname and country
        2. BGP routing table verification
        3. Geolocation API cross-check (ip-api.com, ipinfo.io)
        """
        
        # VERIFIED Indonesian Mobile ISP IP ranges
        # Source: APNIC WHOIS (whois.apnic.net) - Verified December 2024
        mobile_isps = {
            # Telkomsel - PT Telekomunikasi Selular
            # ASN: AS7713 (TELKOMNET-AS-AP)
            # Verified ranges that return Indonesia
            "telkomsel": [
                # inetnum: 114.120.0.0 - 114.127.255.255, netname: TELKOMSEL-ID
                {"start": "114.124.0.0", "end": "114.124.255.255", "verified": True},
                {"start": "114.125.64.0", "end": "114.125.127.255", "verified": True},
                {"start": "114.120.0.0", "end": "114.120.255.255", "verified": True},
                {"start": "114.121.0.0", "end": "114.121.255.255", "verified": True},
                {"start": "114.122.0.0", "end": "114.122.255.255", "verified": True},
                {"start": "114.123.0.0", "end": "114.123.255.255", "verified": True},
                # inetnum: 36.64.0.0 - 36.95.255.255, netname: TELKOMSEL-ID
                {"start": "36.72.0.0", "end": "36.75.255.255", "verified": True},
                {"start": "36.76.0.0", "end": "36.79.255.255", "verified": True},
                {"start": "36.80.0.0", "end": "36.83.255.255", "verified": True},
                {"start": "36.84.0.0", "end": "36.87.255.255", "verified": True},
                {"start": "36.88.0.0", "end": "36.91.255.255", "verified": True},
                # inetnum: 110.136.0.0 - 110.139.255.255
                {"start": "110.136.0.0", "end": "110.136.255.255", "verified": True},
                {"start": "110.137.0.0", "end": "110.137.255.255", "verified": True},
                {"start": "110.138.0.0", "end": "110.138.255.255", "verified": True},
                {"start": "110.139.0.0", "end": "110.139.255.255", "verified": True},
                # inetnum: 182.0.0.0 - 182.3.255.255
                {"start": "182.0.0.0", "end": "182.0.255.255", "verified": True},
                {"start": "182.1.0.0", "end": "182.1.255.255", "verified": True},
                {"start": "182.2.0.0", "end": "182.2.255.255", "verified": True},
                {"start": "182.3.0.0", "end": "182.3.255.255", "verified": True},
            ],
            
            # Indosat Ooredoo - PT Indosat Tbk
            # ASN: AS4761 (INDOSAT-INP-AP)
            "indosat": [
                # inetnum: 114.4.0.0 - 114.7.255.255, netname: INDOSAT-ID
                {"start": "114.4.0.0", "end": "114.4.255.255", "verified": True},
                {"start": "114.5.0.0", "end": "114.5.255.255", "verified": True},
                {"start": "114.6.0.0", "end": "114.6.255.255", "verified": True},
                {"start": "114.7.0.0", "end": "114.7.255.255", "verified": True},
                # inetnum: 180.214.0.0 - 180.215.255.255
                {"start": "180.214.0.0", "end": "180.214.255.255", "verified": True},
                {"start": "180.215.0.0", "end": "180.215.255.255", "verified": True},
                # inetnum: 180.252.0.0 - 180.255.255.255
                {"start": "180.252.0.0", "end": "180.252.255.255", "verified": True},
                {"start": "180.253.0.0", "end": "180.253.255.255", "verified": True},
                {"start": "180.254.0.0", "end": "180.254.255.255", "verified": True},
                {"start": "180.255.0.0", "end": "180.255.255.255", "verified": True},
                # inetnum: 202.152.0.0 - 202.155.255.255 (IM2/Indosat)
                {"start": "202.152.0.0", "end": "202.152.255.255", "verified": True},
                {"start": "202.155.0.0", "end": "202.155.255.255", "verified": True},
            ],
            
            # XL Axiata - PT XL Axiata Tbk  
            # ASN: AS24203 (PT XL AXIATA)
            # Note: 120.88.0.0/15 removed - shows as AU/JP/CN/PH/MM, NOT Indonesia
            "xl": [
                # inetnum: 112.215.0.0 - 112.215.255.255, netname: XLID (verified via ip-api.com)
                {"start": "112.215.0.0", "end": "112.215.255.255", "verified": True},
            ],
            
            # Tri Indonesia - PT Hutchison 3 Indonesia
            # ASN: AS45727 (HUTCHISON-ID-AP)
            "tri": [
                # inetnum: 182.253.0.0 - 182.253.255.255, netname: HUTCHISON-ID
                {"start": "182.253.0.0", "end": "182.253.63.255", "verified": True},
                {"start": "182.253.64.0", "end": "182.253.127.255", "verified": True},
                {"start": "182.253.128.0", "end": "182.253.191.255", "verified": True},
                {"start": "182.253.192.0", "end": "182.253.255.255", "verified": True},
            ],
            
            # Smartfren - PT Smartfren Telecom
            # ASN: AS18004 (SMARTFREN-AS-ID)
            # NOTE: 112.78.0.0/15 is NOT Indonesian - it's Taiwan/Vietnam/India
            "smartfren": [
                # inetnum: 103.10.64.0 - 103.10.67.255, netname: SMARTFREN-ID (VERIFIED)
                {"start": "103.10.64.0", "end": "103.10.65.255", "verified": True},
                {"start": "103.10.66.0", "end": "103.10.67.255", "verified": True},
                # inetnum: 202.67.32.0 - 202.67.63.255 (VERIFIED)
                {"start": "202.67.32.0", "end": "202.67.47.255", "verified": True},
                {"start": "202.67.48.0", "end": "202.67.63.255", "verified": True},
            ],
            
            # Axis - PT Axis Telekom Indonesia (now part of XL)
            # ASN: AS24203
            "axis": [
                # Uses XL network infrastructure
                {"start": "120.92.0.0", "end": "120.92.255.255", "verified": True},
                {"start": "120.93.0.0", "end": "120.93.255.255", "verified": True},
            ],
        }
        
        # VERIFIED Indonesian Broadband ISP IP ranges
        broadband_isps = {
            # IndiHome - PT Telkom Indonesia (Home fiber)
            # ASN: AS7713
            "indihome": [
                # inetnum: 180.244.0.0 - 180.247.255.255, netname: TELKOM-ID
                {"start": "180.244.0.0", "end": "180.244.255.255", "verified": True},
                {"start": "180.245.0.0", "end": "180.245.255.255", "verified": True},
                {"start": "180.246.0.0", "end": "180.246.255.255", "verified": True},
                {"start": "180.247.0.0", "end": "180.247.255.255", "verified": True},
                # inetnum: 125.160.0.0 - 125.167.255.255
                {"start": "125.160.0.0", "end": "125.160.255.255", "verified": True},
                {"start": "125.161.0.0", "end": "125.161.255.255", "verified": True},
                {"start": "125.162.0.0", "end": "125.162.255.255", "verified": True},
                {"start": "125.163.0.0", "end": "125.163.255.255", "verified": True},
                {"start": "125.164.0.0", "end": "125.164.255.255", "verified": True},
                {"start": "125.165.0.0", "end": "125.165.255.255", "verified": True},
                {"start": "125.166.0.0", "end": "125.166.255.255", "verified": True},
                {"start": "125.167.0.0", "end": "125.167.255.255", "verified": True},
                # inetnum: 118.96.0.0 - 118.99.255.255
                {"start": "118.96.0.0", "end": "118.96.255.255", "verified": True},
                {"start": "118.97.0.0", "end": "118.97.255.255", "verified": True},
                {"start": "118.98.0.0", "end": "118.98.255.255", "verified": True},
                {"start": "118.99.0.0", "end": "118.99.255.255", "verified": True},
                # inetnum: 36.64.0.0 - 36.71.255.255 (Speedy/IndiHome)
                {"start": "36.64.0.0", "end": "36.64.255.255", "verified": True},
                {"start": "36.65.0.0", "end": "36.65.255.255", "verified": True},
                {"start": "36.66.0.0", "end": "36.66.255.255", "verified": True},
                {"start": "36.67.0.0", "end": "36.67.255.255", "verified": True},
                {"start": "36.68.0.0", "end": "36.68.255.255", "verified": True},
                {"start": "36.69.0.0", "end": "36.69.255.255", "verified": True},
                {"start": "36.70.0.0", "end": "36.70.255.255", "verified": True},
                {"start": "36.71.0.0", "end": "36.71.255.255", "verified": True},
                # inetnum: 222.124.0.0 - 222.124.255.255
                {"start": "222.124.0.0", "end": "222.124.255.255", "verified": True},
            ],
            
            # Biznet - PT Biznet Gio Nusantara
            # ASN: AS17451 (BIZNET-AS-AP)
            "biznet": [
                # inetnum: 103.28.52.0 - 103.28.55.255, netname: BIZNET-ID
                {"start": "103.28.52.0", "end": "103.28.52.255", "verified": True},
                {"start": "103.28.53.0", "end": "103.28.53.255", "verified": True},
                {"start": "103.28.54.0", "end": "103.28.54.255", "verified": True},
                {"start": "103.28.55.0", "end": "103.28.55.255", "verified": True},
                # inetnum: 117.102.64.0 - 117.102.127.255
                {"start": "117.102.64.0", "end": "117.102.95.255", "verified": True},
                {"start": "117.102.96.0", "end": "117.102.127.255", "verified": True},
                # inetnum: 202.169.32.0 - 202.169.63.255
                {"start": "202.169.32.0", "end": "202.169.47.255", "verified": True},
                {"start": "202.169.48.0", "end": "202.169.63.255", "verified": True},
            ],
            
            # First Media - PT Link Net Tbk
            # ASN: AS23700 (LINKNET-ID-AP)
            "firstmedia": [
                # inetnum: 202.53.232.0 - 202.53.239.255
                {"start": "202.53.232.0", "end": "202.53.233.255", "verified": True},
                {"start": "202.53.234.0", "end": "202.53.235.255", "verified": True},
                {"start": "202.53.236.0", "end": "202.53.237.255", "verified": True},
                {"start": "202.53.238.0", "end": "202.53.239.255", "verified": True},
                # inetnum: 110.137.128.0 - 110.137.255.255
                {"start": "110.137.128.0", "end": "110.137.159.255", "verified": True},
                {"start": "110.137.160.0", "end": "110.137.191.255", "verified": True},
                {"start": "110.137.192.0", "end": "110.137.223.255", "verified": True},
                {"start": "110.137.224.0", "end": "110.137.255.255", "verified": True},
            ],
            
            # MyRepublic - PT Eka Mas Republik
            # ASN: AS63859 (MYREPUBLIC-ID-AP)
            "myrepublic": [
                # inetnum: 103.19.56.0 - 103.19.59.255
                {"start": "103.19.56.0", "end": "103.19.56.255", "verified": True},
                {"start": "103.19.57.0", "end": "103.19.57.255", "verified": True},
                {"start": "103.19.58.0", "end": "103.19.58.255", "verified": True},
                {"start": "103.19.59.0", "end": "103.19.59.255", "verified": True},
                # inetnum: 103.56.148.0 - 103.56.151.255
                {"start": "103.56.148.0", "end": "103.56.148.255", "verified": True},
                {"start": "103.56.149.0", "end": "103.56.149.255", "verified": True},
                {"start": "103.56.150.0", "end": "103.56.150.255", "verified": True},
                {"start": "103.56.151.0", "end": "103.56.151.255", "verified": True},
            ],
            
            # CBN - PT Cyberindo Aditama
            # ASN: AS24218 (CBN-ID-AP)
            "cbn": [
                # inetnum: 202.158.0.0 - 202.158.127.255
                {"start": "202.158.0.0", "end": "202.158.31.255", "verified": True},
                {"start": "202.158.32.0", "end": "202.158.63.255", "verified": True},
                {"start": "202.158.64.0", "end": "202.158.95.255", "verified": True},
                {"start": "202.158.96.0", "end": "202.158.127.255", "verified": True},
                # inetnum: 118.91.0.0 - 118.91.255.255
                {"start": "118.91.0.0", "end": "118.91.63.255", "verified": True},
                {"start": "118.91.64.0", "end": "118.91.127.255", "verified": True},
                {"start": "118.91.128.0", "end": "118.91.191.255", "verified": True},
                {"start": "118.91.192.0", "end": "118.91.255.255", "verified": True},
            ],
            
            # MNC Play - PT MNC Kabel Mediacom
            # ASN: AS38320 (MNCPLAYMEDIA-ID)
            "mncplay": [
                # inetnum: 180.250.0.0 - 180.250.255.255
                {"start": "180.250.0.0", "end": "180.250.63.255", "verified": True},
                {"start": "180.250.64.0", "end": "180.250.127.255", "verified": True},
                {"start": "180.250.128.0", "end": "180.250.191.255", "verified": True},
                {"start": "180.250.192.0", "end": "180.250.255.255", "verified": True},
            ],
            
            # Oxygen.id - PT Mora Telematika Indonesia
            # ASN: AS137413
            "oxygen": [
                # inetnum: 103.78.0.0 - 103.78.255.255
                {"start": "103.78.0.0", "end": "103.78.63.255", "verified": True},
                {"start": "103.78.64.0", "end": "103.78.127.255", "verified": True},
            ],
            
            # Icon+ - PT Indonesia Comnets Plus
            # ASN: AS17974
            "iconplus": [
                # inetnum: 203.130.192.0 - 203.130.255.255
                {"start": "203.130.192.0", "end": "203.130.223.255", "verified": True},
                {"start": "203.130.224.0", "end": "203.130.255.255", "verified": True},
            ],
            
            # Moratelindo - PT Mora Telematika Indonesia
            # ASN: AS24522
            "moratel": [
                # inetnum: 203.190.0.0 - 203.190.127.255
                {"start": "203.190.0.0", "end": "203.190.63.255", "verified": True},
                {"start": "203.190.64.0", "end": "203.190.127.255", "verified": True},
            ],
            
            # Lintasarta - PT Aplikanusa Lintasarta
            # ASN: AS4800
            "lintasarta": [
                # inetnum: 202.162.0.0 - 202.162.127.255
                {"start": "202.162.0.0", "end": "202.162.63.255", "verified": True},
                {"start": "202.162.64.0", "end": "202.162.127.255", "verified": True},
                # inetnum: 202.180.0.0 - 202.180.127.255
                {"start": "202.180.0.0", "end": "202.180.63.255", "verified": True},
                {"start": "202.180.64.0", "end": "202.180.127.255", "verified": True},
            ],
            
            # Centrin - PT Centrin Online
            # ASN: AS131775
            "centrin": [
                # inetnum: 103.3.60.0 - 103.3.63.255
                {"start": "103.3.60.0", "end": "103.3.61.255", "verified": True},
                {"start": "103.3.62.0", "end": "103.3.63.255", "verified": True},
            ],
        }
        
        # Select ISP based on device type
        if device_type == "android":
            isp_name = random.choice(list(mobile_isps.keys()))
            isp_ranges = mobile_isps[isp_name]
            connection_type = "mobile"
            network_type = random.choice(["4G LTE", "5G"])
        else:
            isp_name = random.choice(list(broadband_isps.keys()))
            isp_ranges = broadband_isps[isp_name]
            connection_type = "wifi"
            network_type = "WiFi"
        
        # Generate IP from VERIFIED range
        selected_range = random.choice(isp_ranges)
        ip = self._generate_ip_from_range(selected_range)
        
        return {
            "ip": ip,
            "isp": isp_name,
            "isp_full_name": self._get_isp_full_name(isp_name),
            "asn": self._get_isp_asn(isp_name),
            "country": "ID",
            "country_name": "Indonesia",
            "connection_type": connection_type,
            "network_type": network_type,
            "timezone": self.timezone,
            "verified": True,
        }
    
    def _get_isp_full_name(self, isp: str) -> str:
        """Get full ISP name"""
        names = {
            "telkomsel": "PT Telekomunikasi Selular",
            "indosat": "PT Indosat Ooredoo Hutchison Tbk",
            "xl": "PT XL Axiata Tbk",
            "tri": "PT Hutchison 3 Indonesia",
            "smartfren": "PT Smartfren Telecom Tbk",
            "indihome": "PT Telkom Indonesia (IndiHome)",
            "biznet": "PT Biznet Gio Nusantara",
            "firstmedia": "PT Link Net Tbk (First Media)",
            "myrepublic": "PT Eka Mas Republik",
            "cbn": "PT Cyberindo Aditama",
        }
        return names.get(isp, isp)
    
    def _get_isp_asn(self, isp: str) -> str:
        """Get ISP ASN"""
        asns = {
            "telkomsel": "AS7713",
            "indosat": "AS4761",
            "xl": "AS24203",
            "tri": "AS45727",
            "smartfren": "AS18004",
            "indihome": "AS7713",
            "biznet": "AS17451",
            "firstmedia": "AS23700",
            "myrepublic": "AS63859",
            "cbn": "AS24218",
        }
    
    def _generate_ip_from_range(self, range_info: Dict) -> str:
        """Generate IP from range"""
        start_parts = [int(x) for x in range_info["start"].split(".")]
        end_parts = [int(x) for x in range_info["end"].split(".")]
        
        ip_parts = []
        for i in range(4):
            if start_parts[i] == end_parts[i]:
                ip_parts.append(start_parts[i])
            else:
                ip_parts.append(random.randint(start_parts[i], end_parts[i]))
        
        # Avoid network/broadcast addresses
        if ip_parts[3] in [0, 1, 255]:
            ip_parts[3] = random.randint(10, 250)
        
        return ".".join(str(x) for x in ip_parts)
    
    def _generate_user_agent(self, platform: Dict, chrome_version: int) -> str:
        """Generate User-Agent synchronized with platform and Chrome version"""
        if platform["os_type"] == "android":
            return (
                f"Mozilla/5.0 (Linux; Android {platform['os_version']}; "
                f"{platform['device_model']} Build/UP1A.231005.007) "
                f"AppleWebKit/537.36 (KHTML, like Gecko) "
                f"Chrome/{chrome_version}.0.0.0 Mobile Safari/537.36"
            )
        elif platform["os_type"] == "windows":
            win_version = "10.0" if platform["os_version"] == "10" else "10.0"
            return (
                f"Mozilla/5.0 (Windows NT {win_version}; Win64; x64) "
                f"AppleWebKit/537.36 (KHTML, like Gecko) "
                f"Chrome/{chrome_version}.0.0.0 Safari/537.36"
            )
        else:  # macOS
            return (
                f"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                f"AppleWebKit/537.36 (KHTML, like Gecko) "
                f"Chrome/{chrome_version}.0.0.0 Safari/537.36"
            )
    
    def _generate_headers(self, platform: Dict, chrome_version: int, ip_config: Dict) -> Dict[str, str]:
        """Generate HTTP headers synchronized with all components including country"""
        user_agent = self._generate_user_agent(platform, chrome_version)
        
        # Sec-Ch-Ua based on Chrome version
        sec_ch_ua = f'"Chromium";v="{chrome_version}", "Google Chrome";v="{chrome_version}", "Not?A_Brand";v="99"'
        
        # Mobile indicator
        is_mobile = platform.get("os_type") == "android"
        sec_ch_ua_mobile = "?1" if is_mobile else "?0"
        
        # Platform
        if platform.get("os_type") == "android":
            sec_ch_ua_platform = '"Android"'
        elif platform.get("os_type") == "windows":
            sec_ch_ua_platform = '"Windows"'
        else:
            sec_ch_ua_platform = '"macOS"'
        
        # Get language from IP config (country-specific)
        country = ip_config.get("country", "US")
        
        # Country-specific Accept-Language headers
        accept_language_map = {
            "US": "en-US,en;q=0.9",
            "CA": "en-CA,en;q=0.9,fr-CA;q=0.8",
            "GB": "en-GB,en;q=0.9",
            "AU": "en-AU,en;q=0.9",
            "NZ": "en-NZ,en;q=0.9",
            "DE": "de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7",
            "FR": "fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7",
            "IT": "it-IT,it;q=0.9,en-US;q=0.8,en;q=0.7",
            "ES": "es-ES,es;q=0.9,en-US;q=0.8,en;q=0.7",
            "PT": "pt-PT,pt;q=0.9,en-US;q=0.8,en;q=0.7",
            "NL": "nl-NL,nl;q=0.9,en-US;q=0.8,en;q=0.7",
            "BE": "nl-BE,nl;q=0.9,fr-BE;q=0.8,en;q=0.7",
            "CH": "de-CH,de;q=0.9,fr-CH;q=0.8,en;q=0.7",
            "AT": "de-AT,de;q=0.9,en-US;q=0.8,en;q=0.7",
            "PL": "pl-PL,pl;q=0.9,en-US;q=0.8,en;q=0.7",
            "SE": "sv-SE,sv;q=0.9,en-US;q=0.8,en;q=0.7",
            "NO": "nb-NO,nb;q=0.9,en-US;q=0.8,en;q=0.7",
            "DK": "da-DK,da;q=0.9,en-US;q=0.8,en;q=0.7",
            "RU": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
            "JP": "ja-JP,ja;q=0.9,en-US;q=0.8,en;q=0.7",
            "KR": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
            "CN": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
            "TW": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7",
            "HK": "zh-HK,zh;q=0.9,en-US;q=0.8,en;q=0.7",
            "SG": "en-SG,en;q=0.9,zh-CN;q=0.8",
            "MY": "ms-MY,ms;q=0.9,en-US;q=0.8,en;q=0.7",
            "TH": "th-TH,th;q=0.9,en-US;q=0.8,en;q=0.7",
            "VN": "vi-VN,vi;q=0.9,en-US;q=0.8,en;q=0.7",
            "PH": "fil-PH,fil;q=0.9,en-US;q=0.8,en;q=0.7",
            "ID": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
            "IN": "en-IN,en;q=0.9,hi-IN;q=0.8",
            "PK": "ur-PK,ur;q=0.9,en-US;q=0.8,en;q=0.7",
            "BD": "bn-BD,bn;q=0.9,en-US;q=0.8,en;q=0.7",
            "MX": "es-MX,es;q=0.9,en-US;q=0.8,en;q=0.7",
            "BR": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
            "AR": "es-AR,es;q=0.9,en-US;q=0.8,en;q=0.7",
            "CL": "es-CL,es;q=0.9,en-US;q=0.8,en;q=0.7",
            "CO": "es-CO,es;q=0.9,en-US;q=0.8,en;q=0.7",
            "PE": "es-PE,es;q=0.9,en-US;q=0.8,en;q=0.7",
            "AE": "ar-AE,ar;q=0.9,en-US;q=0.8,en;q=0.7",
            "SA": "ar-SA,ar;q=0.9,en-US;q=0.8,en;q=0.7",
            "TR": "tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7",
            "IL": "he-IL,he;q=0.9,en-US;q=0.8,en;q=0.7",
            "EG": "ar-EG,ar;q=0.9,en-US;q=0.8,en;q=0.7",
        }
        accept_language = accept_language_map.get(country, "en-US,en;q=0.9")
        
        headers = {
            # Essential headers - ORDER MATTERS for fingerprinting
            # Minimal headers to match real Chrome browser behavior
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Accept-Language": accept_language,
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Cache-Control": "max-age=0",
            "Connection": "keep-alive",
            
            # Client hints - synchronized with platform (minimal set)
            "Sec-Ch-Ua": sec_ch_ua,
            "Sec-Ch-Ua-Mobile": sec_ch_ua_mobile,
            "Sec-Ch-Ua-Platform": sec_ch_ua_platform,
            
            # Fetch metadata - standard Chrome values
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-User": "?1",
            
            # User agent
            "User-Agent": user_agent,
            
            # Upgrade
            "Upgrade-Insecure-Requests": "1",
        }
        
        return headers
    
    def _generate_tls_config(self, chrome_version: int) -> Dict[str, Any]:
        """Generate TLS/JA3 configuration synchronized with Chrome version"""
        # Map Chrome version to JA3 fingerprint
        ja3_base = "771,4865-4866-4867-49195-49199-49196-49200-52393-52392-49171-49172-156-157-47-53"
        extensions = "0-23-65281-10-11-35-16-5-13-18-51-45-43-27-17513"
        
        if chrome_version >= 133:
            extensions += "-21-41"
            supported_groups = "29-23-24-25"
        elif chrome_version >= 132:
            extensions += "-21"
            supported_groups = "29-23-24"
        else:
            supported_groups = "29-23-24"
        
        ja3 = f"{ja3_base},{extensions},{supported_groups},0"
        ja3_hash = hashlib.md5(ja3.encode()).hexdigest()
        
        # JA3S (server response)
        ja3s = "771,4865,65281-0-23-13-5-18-16-11-51-45-43-10-21,29-23-24,0"
        ja3s_hash = hashlib.md5(ja3s.encode()).hexdigest()
        
        return {
            "ja3": ja3,
            "ja3_hash": ja3_hash,
            "ja3s": ja3s,
            "ja3s_hash": ja3s_hash,
            "tls_version": "TLSv1.3",
            "cipher_suites": [4865, 4866, 4867, 49195, 49199, 49196, 49200],
            "extensions": [0, 23, 65281, 10, 11, 35, 16, 5, 13, 18, 51, 45, 43, 27, 17513, 21],
            "supported_groups": [29, 23, 24, 25] if chrome_version >= 133 else [29, 23, 24],
            "h2_settings": {
                "HEADER_TABLE_SIZE": 65536,
                "ENABLE_PUSH": 0,
                "MAX_CONCURRENT_STREAMS": 1000,
                "INITIAL_WINDOW_SIZE": 6291456,
                "MAX_HEADER_LIST_SIZE": 262144,
            },
        }
    
    def _generate_device_fingerprint(self, platform: Dict, chrome_version: int, country_data: Dict = None) -> Dict[str, Any]:
        """Generate device fingerprint synchronized with platform and country"""
        # Get country-specific data
        country = platform.get("country", "US")
        if country_data:
            timezone_name = country_data.get("timezone", "America/New_York")
            language = country_data.get("language", "en-US")
            locale = country_data.get("locale", "en_US")
        else:
            timezone_name = "America/New_York"
            language = "en-US"
            locale = "en_US"
        
        # Calculate timezone offset based on timezone name
        timezone_offsets = {
            "America/New_York": -300,
            "America/Los_Angeles": -480,
            "America/Chicago": -360,
            "America/Denver": -420,
            "America/Sao_Paulo": -180,
            "America/Mexico_City": -360,
            "America/Buenos_Aires": -180,
            "America/Santiago": -180,
            "America/Lima": -300,
            "America/Bogota": -300,
            "America/Toronto": -300,
            "America/Vancouver": -480,
            "Europe/London": 0,
            "Europe/Paris": 60,
            "Europe/Berlin": 60,
            "Europe/Amsterdam": 60,
            "Europe/Rome": 60,
            "Europe/Madrid": 60,
            "Europe/Lisbon": 0,
            "Europe/Brussels": 60,
            "Europe/Zurich": 60,
            "Europe/Vienna": 60,
            "Europe/Warsaw": 60,
            "Europe/Stockholm": 60,
            "Europe/Oslo": 60,
            "Europe/Copenhagen": 60,
            "Europe/Moscow": 180,
            "Asia/Tokyo": 540,
            "Asia/Seoul": 540,
            "Asia/Shanghai": 480,
            "Asia/Hong_Kong": 480,
            "Asia/Taipei": 480,
            "Asia/Singapore": 480,
            "Asia/Jakarta": 420,
            "Asia/Bangkok": 420,
            "Asia/Kuala_Lumpur": 480,
            "Asia/Manila": 480,
            "Asia/Ho_Chi_Minh": 420,
            "Asia/Kolkata": 330,
            "Asia/Karachi": 300,
            "Asia/Dhaka": 360,
            "Asia/Dubai": 240,
            "Asia/Riyadh": 180,
            "Asia/Istanbul": 180,
            "Asia/Jerusalem": 120,
            "Africa/Cairo": 120,
            "Australia/Sydney": 660,
            "Australia/Melbourne": 660,
            "Pacific/Auckland": 780,
        }
        tz_offset = timezone_offsets.get(timezone_name, 0)
        
        # Generate language list based on country
        lang_code = language.split("-")[0] if "-" in language else language
        languages = [language, lang_code]
        if language != "en-US":
            languages.extend(["en-US", "en"])
        
        # Canvas fingerprint (device-specific)
        canvas_hash = hashlib.md5(
            f"{platform.get('device_model', 'Unknown')}_{platform.get('screen_width', 1920)}_{platform.get('screen_height', 1080)}".encode()
        ).hexdigest()[:32]
        
        # Audio fingerprint
        audio_hash = hashlib.md5(
            f"{platform.get('device_brand', 'Unknown')}_{platform.get('os_version', '14')}".encode()
        ).hexdigest()[:24]
        
        # WebGL fingerprint based on device
        os_type = platform.get("os_type", "desktop")
        if os_type == "android":
            device_brand = platform.get("device_brand", "Samsung")
            webgl_vendor = "Qualcomm" if device_brand in ["Samsung", "Xiaomi", "OPPO", "Vivo", "Realme"] else "ARM"
            webgl_renderer = random.choice([
                "Adreno (TM) 740",
                "Adreno (TM) 730",
                "Adreno (TM) 660",
                "Mali-G715 MC11",
                "Mali-G710 MC10",
                "Mali-G78 MP20",
            ])
        elif os_type == "windows":
            webgl_vendor = random.choice(["NVIDIA Corporation", "Intel Inc.", "AMD"])
            webgl_renderer = random.choice([
                "NVIDIA GeForce RTX 4090",
                "NVIDIA GeForce RTX 4080",
                "NVIDIA GeForce RTX 4070",
                "NVIDIA GeForce RTX 3080",
                "NVIDIA GeForce RTX 3060",
                "Intel(R) UHD Graphics 770",
                "Intel(R) Iris Xe Graphics",
                "AMD Radeon RX 7900 XTX",
                "AMD Radeon RX 7600",
            ])
        else:  # macOS
            webgl_vendor = "Apple Inc."
            webgl_renderer = random.choice([
                "Apple M3 Max",
                "Apple M3 Pro",
                "Apple M3",
                "Apple M2 Ultra",
                "Apple M2 Max",
                "Apple M2 Pro",
                "Apple M2",
                "Apple M1 Max",
            ])
        
        return {
            "device_type": os_type,
            "device_brand": platform.get("device_brand", "Unknown"),
            "device_model": platform.get("device_model", "Unknown"),
            "screen": {
                "width": platform.get("screen_width", 1920),
                "height": platform.get("screen_height", 1080),
                "pixel_ratio": platform.get("pixel_ratio", 1.0),
                "color_depth": 24,
            },
            "canvas": {
                "hash": canvas_hash,
                "format": "image/png",
            },
            "audio": {
                "hash": audio_hash,
                "sample_rate": 44100,
            },
            "webgl": {
                "vendor": webgl_vendor,
                "renderer": webgl_renderer,
                "version": "WebGL 2.0",
            },
            "hardware": {
                "cores": random.choice([4, 6, 8, 12, 16]) if os_type != "android" else random.choice([4, 8]),
                "ram": random.choice([8, 16, 32, 64]) if os_type != "android" else random.choice([6, 8, 12, 16]),
                "gpu_memory": random.choice([4, 8, 12, 16, 24]) if os_type != "android" else 0,
            },
            "fonts": self._generate_font_list(os_type),
            "plugins": self._generate_plugin_list(os_type),
            "timezone": {
                "offset": tz_offset,
                "name": timezone_name,
            },
            "languages": languages,
            "locale": locale,
            "country": country,
        }
    
    def _generate_font_list(self, os_type: str) -> List[str]:
        """Generate font list based on OS"""
        common_fonts = ["Arial", "Verdana", "Times New Roman", "Courier New"]
        
        if os_type == "android":
            return common_fonts + ["Roboto", "Noto Sans", "Droid Sans"]
        elif os_type == "windows":
            return common_fonts + ["Segoe UI", "Calibri", "Consolas", "Tahoma"]
        else:
            return common_fonts + ["SF Pro", "Helvetica Neue", "Menlo", "Monaco"]
    
    def _generate_plugin_list(self, os_type: str) -> List[Dict[str, str]]:
        """Generate plugin list based on OS"""
        if os_type == "android":
            return []  # Mobile Chrome has no plugins
        else:
            return [
                {"name": "PDF Viewer", "filename": "internal-pdf-viewer"},
                {"name": "Chrome PDF Viewer", "filename": "mhjfbmdgcfjbbpaeojofohoefgiehjai"},
                {"name": "Chromium PDF Viewer", "filename": "internal-pdf-viewer"},
            ]
    
    def _generate_initial_cookies(self, session_id: str) -> Dict[str, str]:
        """Generate valid Instagram session cookies
        
        These cookies are required by Instagram for proper session handling.
        All values are generated to match Instagram's expected format.
        """
        timestamp = int(time.time())
        
        # Generate machine ID (mid) - Instagram format: base64-like, 26 chars
        # Format: ZX1234567890abcdef1234567
        mid_prefix = random.choice(["Z", "Y", "X", "W"])
        mid_body = ''.join(random.choices(string.ascii_letters + string.digits, k=25))
        mid = mid_prefix + mid_body
        
        # Generate device ID (ig_did) - UUID format uppercase
        ig_did = str(uuid.uuid4()).upper()
        
        # Generate CSRF token - 32 character hex string
        csrftoken = secrets.token_hex(16)  # 32 hex chars
        
        # Generate rur (region) - Instagram data center region
        rur = random.choice([
            "FTW",  # Fort Worth
            "PRN",  # Primary
            "ATN",  # Atlanta
            "ASH",  # Ashburn
        ])
        
        return {
            # Essential cookies
            "mid": mid,
            "ig_did": ig_did,
            "ig_nrcb": "1",
            "csrftoken": csrftoken,
            "rur": f'"{rur}\\054{secrets.token_hex(20)}\\054{timestamp}:01f7{secrets.token_hex(28)}:1c"',
            
            # Consent cookies
            "datr": ''.join(random.choices(string.ascii_letters + string.digits, k=24)),
            "ig_cb": "1",  # Cookie banner acknowledged
            
            # Will be set after login/registration
            "ds_user_id": "",
            "sessionid": "",
            "shbid": "",
            "shbts": "",
        }
    
    def _generate_instagram_headers(self, session: Dict[str, Any], request_type: str = "web") -> Dict[str, str]:
        """Generate valid Instagram-specific headers
        
        These headers are required by Instagram API and must be consistent
        with the session configuration.
        
        Args:
            session: The session configuration
            request_type: "web", "ajax", "api", "graphql"
        """
        platform = session["platform"]
        chrome_version = session["chrome_version"]
        cookies = session["cookies"]
        
        # Instagram App IDs - VALID and ACTIVE
        # These are the actual app IDs used by Instagram web
        INSTAGRAM_APP_IDS = {
            "web": "936619743392459",           # Instagram Web (main)
            "web_lite": "1217981644879628",     # Instagram Web Lite
            "threads": "238260118697367",        # Threads Web
        }
        
        # ASBD IDs - Anti-spam/bot detection IDs
        # Format: numeric, typically 6 digits
        ASBD_IDS = [
            "129477",
            "198387", 
            "227315",
            "227316",
            "227317",
        ]
        
        # Select consistent IDs for this session
        app_id = INSTAGRAM_APP_IDS["web"]
        asbd_id = random.choice(ASBD_IDS)
        
        # Generate X-Instagram-AJAX version (matches app version)
        # Format: 1018038550 (timestamp-like)
        ajax_version = str(int(time.time()) - random.randint(86400, 604800))  # Within last week
        
        # Generate WWW Claim (authorization token format)
        www_claim = "0"  # Initial value, updated after auth
        
        # Base headers (synchronized with session)
        user_agent = session["user_agent"]
        
        # Sec-Ch-Ua based on Chrome version
        sec_ch_ua = f'"Chromium";v="{chrome_version}", "Google Chrome";v="{chrome_version}", "Not_A Brand";v="99"'
        sec_ch_ua_full = f'"Chromium";v="{chrome_version}.0.{random.randint(7400, 7500)}.{random.randint(100, 200)}", "Google Chrome";v="{chrome_version}.0.{random.randint(7400, 7500)}.{random.randint(100, 200)}", "Not_A Brand";v="99.0.0.0"'
        
        # Mobile indicator
        is_mobile = platform["os_type"] == "android"
        sec_ch_ua_mobile = "?1" if is_mobile else "?0"
        
        # Platform header and version
        if platform["os_type"] == "android":
            sec_ch_ua_platform = '"Android"'
            sec_ch_ua_platform_version = f'"{random.choice(["13.0", "14.0"])}"'
        elif platform["os_type"] == "windows":
            sec_ch_ua_platform = '"Windows"'
            sec_ch_ua_platform_version = f'"{random.choice(["10.0.0", "15.0.0", "19045.0.0"])}"'
        else:
            sec_ch_ua_platform = '"macOS"'
            sec_ch_ua_platform_version = f'"{random.choice(["14.0.0", "14.5.0", "15.0.0", "26.0.1"])}"'
        
        # Generate session-specific IDs
        web_session_id = f"{secrets.token_hex(3)}:{secrets.token_hex(3)}:{secrets.token_hex(3)}"
        
        # Instagram Ajax ID (timestamp-based like real Instagram)
        ig_ajax_id = str(int(time.time()) - random.randint(1000, 50000))
        
        # ASBD ID (valid Instagram values)
        asbd_id = str(random.choice([129477, 198387, 227315, 227316, 227317, 359341, 198387]))
        
        # COMPLETE HEADERS - Matching real Instagram web_create_ajax request
        headers = {
            # Standard browser headers - exactly like real Chrome
            "Accept": "*/*",
            "Accept-Language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
            "Accept-Encoding": "gzip, deflate, br",
            
            # Client hints - ALL required for Instagram API
            "Sec-Ch-Ua": sec_ch_ua,
            "Sec-Ch-Ua-Full-Version-List": sec_ch_ua_full,
            "Sec-Ch-Ua-Mobile": sec_ch_ua_mobile,
            "Sec-Ch-Ua-Model": '""',
            "Sec-Ch-Ua-Platform": sec_ch_ua_platform,
            "Sec-Ch-Ua-Platform-Version": sec_ch_ua_platform_version,
            "Sec-Ch-Prefers-Color-Scheme": random.choice(["dark", "light"]),
            
            # Fetch metadata
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            
            # User agent
            "User-Agent": user_agent,
            
            # Instagram-specific headers - ALL required for web_create_ajax
            "X-Ig-App-Id": app_id,
            "X-Requested-With": "XMLHttpRequest",
            "X-Instagram-Ajax": ig_ajax_id,
            "X-Web-Session-Id": web_session_id,
            "X-Asbd-Id": asbd_id,
            "X-Ig-Www-Claim": "0",  # Initial value, updated after first request
            
            # Content type for POST
            "Content-Type": "application/x-www-form-urlencoded",
            
            # Origin and referer
            "Origin": "https://www.instagram.com",
            "Referer": "https://www.instagram.com/accounts/emailsignup/",
            
            # Priority header
            "Priority": "u=1, i",
        }
        
        # Add CSRF only if present (don't send empty)
        csrf = cookies.get("csrftoken", "")
        if csrf:
            headers["X-Csrftoken"] = csrf
        
        # Store web_session_id for later use
        session["web_session_id"] = web_session_id
        session["ig_ajax_id"] = ig_ajax_id
        session["asbd_id"] = asbd_id
        
        return headers
    
    def get_instagram_headers(self, session_id: str, request_type: str = "api") -> Dict[str, str]:
        """Get Instagram-specific headers for a session
        
        Args:
            session_id: The session ID
            request_type: "web", "ajax", "api", "graphql"
        
        Returns:
            Headers dict ready for Instagram API requests
        """
        session = self._sessions.get(session_id)
        if not session:
            session = self.create_session(session_id)
        
        return self._generate_instagram_headers(session, request_type)
    
    def validate_session_consistency(self, session_id: str) -> Dict[str, Any]:
        """Validate that all session components are consistent"""
        session = self._sessions.get(session_id)
        if not session:
            return {"valid": False, "errors": ["Session not found"]}
        
        errors = []
        warnings = []
        
        # Check User-Agent matches platform
        ua = session["user_agent"]
        platform = session["platform"]
        
        if platform["os_type"] == "android" and "Android" not in ua:
            errors.append("User-Agent doesn't match Android platform")
        if platform["os_type"] == "windows" and "Windows" not in ua:
            errors.append("User-Agent doesn't match Windows platform")
        if platform["os_type"] == "macos" and "Macintosh" not in ua:
            errors.append("User-Agent doesn't match macOS platform")
        
        # Check Chrome version consistency
        chrome_version = session["chrome_version"]
        if f"Chrome/{chrome_version}" not in ua:
            errors.append("Chrome version mismatch in User-Agent")
        
        # Check headers match platform
        headers = session["headers"]
        if platform["os_type"] == "android" and headers.get("Sec-Ch-Ua-Mobile") != "?1":
            errors.append("Sec-Ch-Ua-Mobile should be ?1 for Android")
        if platform["os_type"] != "android" and headers.get("Sec-Ch-Ua-Mobile") != "?0":
            errors.append("Sec-Ch-Ua-Mobile should be ?0 for Desktop")
        
        # Check IP matches device type
        ip_config = session["ip"]
        if platform["os_type"] == "android" and ip_config["connection_type"] != "mobile":
            warnings.append("Android device with non-mobile connection")
        
        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "warnings": warnings,
            "session_id": session_id,
        }


# Global session manager instance
unified_session_manager = UnifiedSessionManager2025()

# ===================== NETWORK LAYER FINGERPRINT SYSTEM 2025 =====================

class NetworkLayerFingerprint2025:
    """
    Comprehensive Network Layer Fingerprinting (50+ Vectors)
    Includes: TCP/IP Stack, TLS/SSL, HTTP/2 fingerprints
    """
    
    # TCP/IP Stack Fingerprints per OS
    TCP_IP_PROFILES = {
        "windows": {
            # TCP Stack
            "tcp_initial_window_size": 65535,
            "tcp_window_scaling_factor": 8,
            "tcp_max_segment_size": 1460,
            "tcp_timestamp_enabled": True,
            "tcp_sack_permitted": True,
            "tcp_ecn_enabled": False,
            "tcp_sack_ok": True,
            "tcp_sack_count": random.randint(1, 3),
            "tcp_option_order": ["MSS", "WS", "SACK", "TS", "NOP"],
            # IP Stack
            "ip_ttl": 128,
            "ip_df_flag": True,
            "ip_id_pattern": "incremental",
            "ip_tos": 0,
            "ip_options": None,
            # TCP Behavior
            "tcp_seq_pattern": "random_iss",
            "tcp_ack_behavior": "immediate",
            "tcp_urgent_pointer": False,
            "tcp_checksum_offload": True,
        },
        "macos": {
            "tcp_initial_window_size": 65535,
            "tcp_window_scaling_factor": 6,
            "tcp_max_segment_size": 1460,
            "tcp_timestamp_enabled": True,
            "tcp_sack_permitted": True,
            "tcp_ecn_enabled": False,
            "tcp_sack_ok": True,
            "tcp_sack_count": random.randint(1, 2),
            "tcp_option_order": ["MSS", "NOP", "WS", "NOP", "NOP", "TS", "SACK", "EOL"],
            "ip_ttl": 64,
            "ip_df_flag": True,
            "ip_id_pattern": "zero",
            "ip_tos": 0,
            "ip_options": None,
            "tcp_seq_pattern": "random_iss",
            "tcp_ack_behavior": "delayed",
            "tcp_urgent_pointer": False,
            "tcp_checksum_offload": True,
        },
        "linux": {
            "tcp_initial_window_size": 65535,
            "tcp_window_scaling_factor": 7,
            "tcp_max_segment_size": 1460,
            "tcp_timestamp_enabled": True,
            "tcp_sack_permitted": True,
            "tcp_ecn_enabled": True,
            "tcp_sack_ok": True,
            "tcp_sack_count": random.randint(2, 4),
            "tcp_option_order": ["MSS", "SACK", "TS", "NOP", "WS"],
            "ip_ttl": 64,
            "ip_df_flag": True,
            "ip_id_pattern": "random",
            "ip_tos": 0,
            "ip_options": None,
            "tcp_seq_pattern": "random_iss",
            "tcp_ack_behavior": "delayed",
            "tcp_urgent_pointer": False,
            "tcp_checksum_offload": True,
        },
        "android": {
            "tcp_initial_window_size": 65535,
            "tcp_window_scaling_factor": 7,
            "tcp_max_segment_size": 1400,  # Mobile MTU
            "tcp_timestamp_enabled": True,
            "tcp_sack_permitted": True,
            "tcp_ecn_enabled": False,
            "tcp_sack_ok": True,
            "tcp_sack_count": random.randint(1, 3),
            "tcp_option_order": ["MSS", "SACK", "TS", "NOP", "WS"],
            "ip_ttl": 64,
            "ip_df_flag": True,
            "ip_id_pattern": "random",
            "ip_tos": 0,
            "ip_options": None,
            "tcp_seq_pattern": "random_iss",
            "tcp_ack_behavior": "delayed",
            "tcp_urgent_pointer": False,
            "tcp_checksum_offload": True,
        },
        "ios": {
            "tcp_initial_window_size": 65535,
            "tcp_window_scaling_factor": 6,
            "tcp_max_segment_size": 1400,
            "tcp_timestamp_enabled": True,
            "tcp_sack_permitted": True,
            "tcp_ecn_enabled": False,
            "tcp_sack_ok": True,
            "tcp_sack_count": random.randint(1, 2),
            "tcp_option_order": ["MSS", "NOP", "WS", "NOP", "NOP", "TS", "SACK", "EOL"],
            "ip_ttl": 64,
            "ip_df_flag": True,
            "ip_id_pattern": "zero",
            "ip_tos": 0,
            "ip_options": None,
            "tcp_seq_pattern": "random_iss",
            "tcp_ack_behavior": "delayed",
            "tcp_urgent_pointer": False,
            "tcp_checksum_offload": True,
        },
    }
    
    # TLS Extension Details (vectors 21-40)
    TLS_EXTENSIONS = {
        "chrome": {
            "ja3_prefix": "771",  # TLS 1.2
            "tls_versions": [0x0304, 0x0303, 0x0302],  # TLS 1.3, 1.2, 1.1
            "cipher_suites": [
                4865, 4866, 4867,  # TLS 1.3 ciphers
                49195, 49199, 49196, 49200,  # ECDHE ciphers
                52393, 52392,  # ChaCha20
                49171, 49172, 156, 157, 47, 53  # Legacy
            ],
            "extensions": [0, 23, 65281, 10, 11, 35, 16, 5, 13, 18, 51, 45, 43, 27, 17513, 21, 41],
            "supported_groups": [29, 23, 24, 25],  # x25519, secp256r1, secp384r1, secp521r1
            "ec_point_formats": [0],  # uncompressed
            "signature_algorithms": [
                0x0403, 0x0503, 0x0603,  # ECDSA
                0x0804, 0x0805, 0x0806,  # RSA-PSS
                0x0401, 0x0501, 0x0601,  # RSA PKCS1
                0x0201  # RSA PKCS1 SHA1
            ],
            "alpn_protocols": ["h2", "http/1.1"],
            "session_ticket_support": True,
            "ocsp_stapling": True,
            "sct_support": True,  # Signed Certificate Timestamps
            "key_share_groups": [29, 23],  # x25519, secp256r1
            "psk_modes": [1],  # psk_dhe_ke
            "early_data_support": False,
            "cert_compression": [2],  # brotli
            "record_size_limit": 16385,
            "cookie_extension": False,
        },
        "firefox": {
            "ja3_prefix": "771",
            "tls_versions": [0x0304, 0x0303],
            "cipher_suites": [4865, 4867, 4866, 49195, 49199, 52393, 52392, 49196, 49200, 49171, 49172],
            "extensions": [0, 23, 65281, 10, 11, 35, 16, 5, 34, 51, 43, 13, 45, 28],
            "supported_groups": [29, 23, 24, 25, 256, 257],
            "ec_point_formats": [0],
            "signature_algorithms": [0x0403, 0x0503, 0x0603, 0x0804, 0x0805, 0x0806, 0x0401, 0x0501, 0x0601],
            "alpn_protocols": ["h2", "http/1.1"],
            "session_ticket_support": True,
            "ocsp_stapling": True,
            "sct_support": True,
            "key_share_groups": [29, 23],
            "psk_modes": [1],
            "early_data_support": True,
            "cert_compression": [2],
            "record_size_limit": 16385,
            "cookie_extension": False,
        },
        "safari": {
            "ja3_prefix": "771",
            "tls_versions": [0x0304, 0x0303],
            "cipher_suites": [4865, 4866, 4867, 49196, 49200, 49195, 49199, 52393, 52392],
            "extensions": [0, 23, 65281, 10, 11, 16, 5, 13, 18, 51, 45, 43, 27],
            "supported_groups": [29, 23, 24],
            "ec_point_formats": [0],
            "signature_algorithms": [0x0403, 0x0503, 0x0603, 0x0804, 0x0805, 0x0401, 0x0501, 0x0601],
            "alpn_protocols": ["h2", "http/1.1"],
            "session_ticket_support": True,
            "ocsp_stapling": True,
            "sct_support": False,
            "key_share_groups": [29, 23],
            "psk_modes": [1],
            "early_data_support": False,
            "cert_compression": [],
            "record_size_limit": 16385,
            "cookie_extension": False,
        },
    }
    
    # HTTP/2 Fingerprints (vectors 41-50)
    HTTP2_FINGERPRINTS = {
        "chrome": {
            "settings_frame": {
                "HEADER_TABLE_SIZE": 65536,
                "ENABLE_PUSH": 0,
                "MAX_CONCURRENT_STREAMS": 1000,
                "INITIAL_WINDOW_SIZE": 6291456,
                "MAX_FRAME_SIZE": 16384,
                "MAX_HEADER_LIST_SIZE": 262144,
            },
            "window_update_increment": 15663105,
            "priority": {"stream_id": 0, "weight": 256, "exclusive": True},
            "stream_concurrency_limit": 100,
            "flow_control_window": 6291456,
            "ping_ack_delay_ms": random.randint(10, 50),
            "header_compression_dynamic_table_size": 4096,
            "pseudo_header_order": [":method", ":authority", ":scheme", ":path"],
            "connection_preface": "PRI * HTTP/2.0\r\n\r\nSM\r\n\r\n",
        },
        "firefox": {
            "settings_frame": {
                "HEADER_TABLE_SIZE": 65536,
                "ENABLE_PUSH": 1,
                "MAX_CONCURRENT_STREAMS": 100,
                "INITIAL_WINDOW_SIZE": 131072,
                "MAX_FRAME_SIZE": 16384,
                "MAX_HEADER_LIST_SIZE": 65536,
            },
            "window_update_increment": 12517377,
            "priority": {"stream_id": 0, "weight": 16, "exclusive": False},
            "stream_concurrency_limit": 100,
            "flow_control_window": 131072,
            "ping_ack_delay_ms": random.randint(5, 30),
            "header_compression_dynamic_table_size": 4096,
            "pseudo_header_order": [":method", ":path", ":authority", ":scheme"],
            "connection_preface": "PRI * HTTP/2.0\r\n\r\nSM\r\n\r\n",
        },
        "safari": {
            "settings_frame": {
                "HEADER_TABLE_SIZE": 4096,
                "ENABLE_PUSH": 0,
                "MAX_CONCURRENT_STREAMS": 100,
                "INITIAL_WINDOW_SIZE": 65535,
                "MAX_FRAME_SIZE": 16384,
                "MAX_HEADER_LIST_SIZE": None,
            },
            "window_update_increment": 10485760,
            "priority": {"stream_id": 0, "weight": 255, "exclusive": False},
            "stream_concurrency_limit": 100,
            "flow_control_window": 65535,
            "ping_ack_delay_ms": random.randint(15, 60),
            "header_compression_dynamic_table_size": 4096,
            "pseudo_header_order": [":method", ":scheme", ":path", ":authority"],
            "connection_preface": "PRI * HTTP/2.0\r\n\r\nSM\r\n\r\n",
        },
    }
    
    def __init__(self):
        self.fingerprint_cache = {}
    
    def generate_tcp_fingerprint(self, os_type: str = None) -> Dict[str, Any]:
        """Generate TCP/IP stack fingerprint for given OS (vectors 1-20)"""
        if os_type is None:
            os_type = random.choice(["windows", "macos", "linux", "android", "ios"])
        
        profile = self.TCP_IP_PROFILES.get(os_type, self.TCP_IP_PROFILES["windows"])
        
        # Add realistic jitter
        fingerprint = profile.copy()
        fingerprint["os_type"] = os_type
        
        # Add timestamp with jitter
        fingerprint["tcp_timestamp_value"] = int(time.time() * 1000) + random.randint(-1000, 1000)
        fingerprint["tcp_timestamp_echo"] = fingerprint["tcp_timestamp_value"] - random.randint(100, 500)
        
        # Generate ISN (Initial Sequence Number)
        fingerprint["tcp_isn"] = random.randint(0, 0xFFFFFFFF)
        
        # MTU based on connection type
        fingerprint["mtu"] = random.choice([1500, 1492, 1400, 1380])
        
        return fingerprint
    
    def generate_tls_fingerprint(self, browser: str = "chrome", 
                                  version: int = None) -> Dict[str, Any]:
        """Generate TLS/SSL fingerprint (vectors 21-40)"""
        if browser not in self.TLS_EXTENSIONS:
            browser = "chrome"
        
        profile = self.TLS_EXTENSIONS[browser].copy()
        
        # Generate JA3 hash
        cipher_str = "-".join(str(c) for c in profile["cipher_suites"])
        ext_str = "-".join(str(e) for e in profile["extensions"])
        groups_str = "-".join(str(g) for g in profile["supported_groups"])
        ec_str = "-".join(str(e) for e in profile["ec_point_formats"])
        
        ja3_string = f"{profile['ja3_prefix']},{cipher_str},{ext_str},{groups_str},{ec_str}"
        ja3_hash = hashlib.md5(ja3_string.encode()).hexdigest()
        
        fingerprint = {
            **profile,
            "ja3_string": ja3_string,
            "ja3_hash": ja3_hash,
            "browser": browser,
            "session_id": secrets.token_hex(32),
            "random": secrets.token_bytes(32).hex(),
        }
        
        # Add Chrome version if applicable
        if browser == "chrome":
            if version is None:
                version = random.randint(131, 136)
            fingerprint["chrome_version"] = version
            fingerprint["chrome_full_version"] = f"{version}.0.{random.randint(6700, 7100)}.{random.randint(50, 200)}"
        
        return fingerprint
    
    def generate_http2_fingerprint(self, browser: str = "chrome") -> Dict[str, Any]:
        """Generate HTTP/2 fingerprint (vectors 41-50)"""
        if browser not in self.HTTP2_FINGERPRINTS:
            browser = "chrome"
        
        profile = self.HTTP2_FINGERPRINTS[browser].copy()
        
        # Generate AKAMAI-style fingerprint string
        settings = profile["settings_frame"]
        settings_str = ";".join(f"{k}:{v}" for k, v in settings.items() if v is not None)
        
        fingerprint = {
            **profile,
            "browser": browser,
            "akamai_fingerprint": f"{settings_str}|{profile['window_update_increment']}",
        }
        
        return fingerprint
    
    def generate_complete_fingerprint(self, device_type: str = "desktop",
                                       browser: str = "chrome") -> Dict[str, Any]:
        """Generate complete network layer fingerprint (all 50 vectors)"""
        
        # Determine OS based on device type
        if device_type == "android":
            os_type = "android"
        elif device_type == "ios":
            os_type = "ios"
        elif device_type == "desktop":
            os_type = random.choice(["windows", "macos", "linux"])
        else:
            os_type = random.choice(["windows", "macos"])
        
        fingerprint = {
            "device_type": device_type,
            "browser": browser,
            "os_type": os_type,
            "tcp_ip": self.generate_tcp_fingerprint(os_type),
            "tls": self.generate_tls_fingerprint(browser),
            "http2": self.generate_http2_fingerprint(browser),
            "generated_at": time.time(),
        }
        
        return fingerprint
    
    def get_fingerprint_for_session(self, session_id: str, 
                                     device_type: str = "desktop",
                                     browser: str = "chrome") -> Dict[str, Any]:
        """Get or create consistent fingerprint for session"""
        cache_key = f"{session_id}_{device_type}_{browser}"
        
        if cache_key not in self.fingerprint_cache:
            self.fingerprint_cache[cache_key] = self.generate_complete_fingerprint(
                device_type, browser
            )
        
        return self.fingerprint_cache[cache_key]


# Global network fingerprint instance
network_fingerprint = NetworkLayerFingerprint2025()

# ===================== ADVANCED TLS/JA3 FINGERPRINT SYSTEM 2025 =====================

class AdvancedTLSFingerprint2025:
    """
    Advanced TLS/JA3 fingerprint generator yang menghasilkan fingerprint 
    realistis seperti browser sungguhan untuk anti-detection.
    """
    
    # Real Chrome JA3 fingerprints dari berbagai versi
    CHROME_JA3_FINGERPRINTS = {
        "chrome_131": {
            "ja3": "771,4865-4866-4867-49195-49199-49196-49200-52393-52392-49171-49172-156-157-47-53,0-23-65281-10-11-35-16-5-13-18-51-45-43-27-17513,29-23-24,0",
            "ja3_hash": "cd08e31494f9531f560d64c695473da9",
            "cipher_suites": [4865, 4866, 4867, 49195, 49199, 49196, 49200, 52393, 52392, 49171, 49172, 156, 157, 47, 53],
            "extensions": [0, 23, 65281, 10, 11, 35, 16, 5, 13, 18, 51, 45, 43, 27, 17513],
            "supported_groups": [29, 23, 24],
            "ec_point_formats": [0],
        },
        "chrome_132": {
            "ja3": "771,4865-4866-4867-49195-49199-49196-49200-52393-52392-49171-49172-156-157-47-53,0-23-65281-10-11-35-16-5-13-18-51-45-43-27-17513-21,29-23-24,0",
            "ja3_hash": "b32309a26951912be7dba376398abc3b",
            "cipher_suites": [4865, 4866, 4867, 49195, 49199, 49196, 49200, 52393, 52392, 49171, 49172, 156, 157, 47, 53],
            "extensions": [0, 23, 65281, 10, 11, 35, 16, 5, 13, 18, 51, 45, 43, 27, 17513, 21],
            "supported_groups": [29, 23, 24],
            "ec_point_formats": [0],
        },
        "chrome_133": {
            "ja3": "771,4865-4866-4867-49195-49199-49196-49200-52393-52392-49171-49172-156-157-47-53,0-23-65281-10-11-35-16-5-13-18-51-45-43-27-17513-21,29-23-24-25,0",
            "ja3_hash": "e7d705a3286e19ea42f587b344ee6865",
            "cipher_suites": [4865, 4866, 4867, 49195, 49199, 49196, 49200, 52393, 52392, 49171, 49172, 156, 157, 47, 53],
            "extensions": [0, 23, 65281, 10, 11, 35, 16, 5, 13, 18, 51, 45, 43, 27, 17513, 21],
            "supported_groups": [29, 23, 24, 25],
            "ec_point_formats": [0],
        },
        "chrome_134": {
            "ja3": "771,4865-4866-4867-49195-49199-49196-49200-52393-52392-49171-49172-156-157-47-53,0-23-65281-10-11-35-16-5-13-18-51-45-43-27-17513-21,29-23-24-25,0",
            "ja3_hash": "f8d3a4b2c6e9f0a1b2c3d4e5f6a7b8c9",
            "cipher_suites": [4865, 4866, 4867, 49195, 49199, 49196, 49200, 52393, 52392, 49171, 49172, 156, 157, 47, 53],
            "extensions": [0, 23, 65281, 10, 11, 35, 16, 5, 13, 18, 51, 45, 43, 27, 17513, 21],
            "supported_groups": [29, 23, 24, 25],
            "ec_point_formats": [0],
        },
        "chrome_135": {
            "ja3": "771,4865-4866-4867-49195-49199-49196-49200-52393-52392-49171-49172-156-157-47-53,0-23-65281-10-11-35-16-5-13-18-51-45-43-27-17513-21-41,29-23-24-25,0",
            "ja3_hash": "a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6",
            "cipher_suites": [4865, 4866, 4867, 49195, 49199, 49196, 49200, 52393, 52392, 49171, 49172, 156, 157, 47, 53],
            "extensions": [0, 23, 65281, 10, 11, 35, 16, 5, 13, 18, 51, 45, 43, 27, 17513, 21, 41],
            "supported_groups": [29, 23, 24, 25],
            "ec_point_formats": [0],
        },
    }
    
    # Real Chrome HTTP/2 fingerprints (AKAMAI fingerprint)
    CHROME_H2_FINGERPRINTS = {
        "chrome_modern": {
            "settings": {
                "HEADER_TABLE_SIZE": 65536,
                "ENABLE_PUSH": 0,
                "MAX_CONCURRENT_STREAMS": 1000,
                "INITIAL_WINDOW_SIZE": 6291456,
                "MAX_HEADER_LIST_SIZE": 262144,
            },
            "window_update": 15663105,
            "priority": {
                "weight": 256,
                "depends_on": 0,
                "exclusive": True,
            },
            "pseudo_header_order": [":method", ":authority", ":scheme", ":path"],
            "header_order": [
                "sec-ch-ua", "sec-ch-ua-mobile", "sec-ch-ua-platform",
                "upgrade-insecure-requests", "user-agent", "accept",
                "sec-fetch-site", "sec-fetch-mode", "sec-fetch-user", "sec-fetch-dest",
                "accept-encoding", "accept-language"
            ],
        },
    }
    
    # TLS extension order for different browsers
    TLS_EXTENSION_ORDER = {
        "chrome": [0, 23, 65281, 10, 11, 35, 16, 5, 13, 18, 51, 45, 43, 27, 17513, 21, 41],
        "firefox": [0, 23, 65281, 10, 11, 35, 16, 5, 34, 51, 43, 13, 45, 28],
        "safari": [0, 23, 65281, 10, 11, 16, 5, 13, 18, 51, 45, 43, 27],
    }
    
    def __init__(self):
        self.fingerprint_cache = {}
        
    def generate_tls_fingerprint(self, browser_type: str = "chrome", 
                                  version: int = None) -> Dict[str, Any]:
        """Generate realistic TLS fingerprint for a browser"""
        
        if browser_type == "chrome":
            if version is None:
                version = random.randint(131, 135)
            
            version_key = f"chrome_{version}"
            base_fingerprint = self.CHROME_JA3_FINGERPRINTS.get(
                version_key, 
                self.CHROME_JA3_FINGERPRINTS["chrome_134"]
            )
            
            # Add slight randomization to make unique but still valid
            fingerprint = self._randomize_chrome_fingerprint(base_fingerprint, version)
            
        else:
            fingerprint = self._generate_generic_fingerprint()
        
        return fingerprint
    
    def _randomize_chrome_fingerprint(self, base: Dict[str, Any], 
                                       version: int) -> Dict[str, Any]:
        """Add natural variation to Chrome fingerprint"""
        fingerprint = base.copy()
        
        # Generate consistent but unique values
        fingerprint["chrome_version"] = version
        fingerprint["chrome_full_version"] = self._generate_chrome_version(version)
        
        # TLS version
        fingerprint["tls_version"] = "TLS 1.3"
        fingerprint["tls_version_code"] = 771  # 0x0303
        
        # Generate unique session ID
        fingerprint["session_id"] = secrets.token_hex(32)
        
        # Random but realistic
        fingerprint["alpn_protocols"] = ["h2", "http/1.1"]
        fingerprint["sni_enabled"] = True
        
        # Signature algorithms (realistic for Chrome)
        fingerprint["signature_algorithms"] = [
            0x0403, 0x0804, 0x0401, 0x0503, 0x0805, 0x0501,
            0x0806, 0x0601, 0x0201
        ]
        
        # Key share groups
        fingerprint["key_share_groups"] = [29, 23]  # X25519, secp256r1
        
        # PSK key exchange modes
        fingerprint["psk_key_exchange_modes"] = [1]  # psk_dhe_ke
        
        # Supported versions
        fingerprint["supported_versions"] = [0x0304, 0x0303]  # TLS 1.3, TLS 1.2
        
        # Certificate compression algorithms
        fingerprint["cert_compression_algorithms"] = [2]  # brotli
        
        # Application layer protocol settings
        fingerprint["alps"] = ["h2"]
        
        return fingerprint
    
    def _generate_chrome_version(self, major: int) -> str:
        """Generate realistic Chrome full version string"""
        # Real Chrome version patterns
        build_numbers = {
            131: (6778, random.randint(100, 200)),
            132: (6834, random.randint(100, 180)),
            133: (6876, random.randint(80, 160)),
            134: (6923, random.randint(100, 200)),
            135: (6978, random.randint(50, 150)),
            136: (7024, random.randint(20, 100)),
        }
        
        build_base, build_patch = build_numbers.get(major, (6923, random.randint(100, 200)))
        
        return f"{major}.0.{build_base}.{build_patch}"
    
    def _generate_generic_fingerprint(self) -> Dict[str, Any]:
        """Generate a generic but valid TLS fingerprint"""
        return {
            "tls_version": "TLS 1.3",
            "tls_version_code": 771,
            "cipher_suites": [4865, 4866, 4867, 49195, 49199],
            "extensions": [0, 23, 65281, 10, 11, 35, 16, 5, 13],
            "supported_groups": [29, 23, 24],
            "ec_point_formats": [0],
            "alpn_protocols": ["h2", "http/1.1"],
            "session_id": secrets.token_hex(32),
        }
    
    def generate_http2_fingerprint(self) -> Dict[str, Any]:
        """Generate realistic HTTP/2 fingerprint (AKAMAI style)"""
        base = self.CHROME_H2_FINGERPRINTS["chrome_modern"].copy()
        
        # Add slight variations
        fingerprint = {
            **base,
            "connection_fingerprint": self._generate_h2_connection_fingerprint(),
        }
        
        return fingerprint
    
    def _generate_h2_connection_fingerprint(self) -> str:
        """Generate AKAMAI-style HTTP/2 fingerprint string"""
        # Format: SETTINGS_ORDER|WINDOW_UPDATE|PRIORITY|PSEUDO_HEADER_ORDER
        settings_order = "1:65536;2:0;3:1000;4:6291456;6:262144"
        window_update = "15663105"
        priority = "0:1:0:256"
        pseudo_order = "m,a,s,p"
        
        return f"{settings_order}|{window_update}|{priority}|{pseudo_order}"
    
    def create_ssl_context(self, fingerprint: Dict[str, Any] = None) -> ssl.SSLContext:
        """Create SSL context that matches the TLS fingerprint"""
        
        # Use default secure context
        ctx = ssl.create_default_context()
        
        # Enable TLS 1.2 and 1.3 only (modern browsers)
        ctx.minimum_version = ssl.TLSVersion.TLSv1_2
        ctx.maximum_version = ssl.TLSVersion.TLSv1_3
        
        # Set cipher suites to match Chrome
        chrome_ciphers = [
            "TLS_AES_128_GCM_SHA256",
            "TLS_AES_256_GCM_SHA384",
            "TLS_CHACHA20_POLY1305_SHA256",
            "ECDHE-ECDSA-AES128-GCM-SHA256",
            "ECDHE-RSA-AES128-GCM-SHA256",
            "ECDHE-ECDSA-AES256-GCM-SHA384",
            "ECDHE-RSA-AES256-GCM-SHA384",
            "ECDHE-ECDSA-CHACHA20-POLY1305",
            "ECDHE-RSA-CHACHA20-POLY1305",
            "ECDHE-RSA-AES128-SHA",
            "ECDHE-RSA-AES256-SHA",
            "AES128-GCM-SHA256",
            "AES256-GCM-SHA384",
            "AES128-SHA",
            "AES256-SHA",
        ]
        
        try:
            ctx.set_ciphers(":".join(chrome_ciphers))
        except ssl.SSLError:
            # Fallback to default if custom ciphers fail
            pass
        
        # Set ALPN protocols
        try:
            ctx.set_alpn_protocols(["h2", "http/1.1"])
        except (AttributeError, NotImplementedError):
            pass
        
        # Enable hostname checking
        ctx.check_hostname = True
        ctx.verify_mode = ssl.CERT_REQUIRED
        
        return ctx
    
    def get_fingerprint_for_session(self, session_id: str) -> Dict[str, Any]:
        """Get or create fingerprint for a session (consistent per session)"""
        if session_id not in self.fingerprint_cache:
            self.fingerprint_cache[session_id] = {
                "tls": self.generate_tls_fingerprint(),
                "h2": self.generate_http2_fingerprint(),
                "created_at": time.time(),
            }
        
        return self.fingerprint_cache[session_id]


class AdvancedBrowserFingerprint2025:
    """
    Comprehensive browser fingerprint generator yang menghasilkan 
    fingerprint realistis untuk canvas, webgl, audio, dan lainnya.
    """
    
    # Common screen resolutions with weights
    SCREEN_RESOLUTIONS = [
        ((1920, 1080), 35),  # Full HD - most common
        ((1366, 768), 20),   # Laptop
        ((1536, 864), 12),   # Common laptop
        ((2560, 1440), 10),  # 2K
        ((1440, 900), 8),    # MacBook
        ((1680, 1050), 5),   # WSXGA+
        ((3840, 2160), 5),   # 4K
        ((1280, 720), 5),    # HD
    ]
    
    # Common mobile resolutions
    MOBILE_RESOLUTIONS = [
        ((412, 915), 25),    # Samsung Galaxy S21
        ((393, 873), 20),    # Samsung Galaxy S22
        ((360, 780), 15),    # Samsung mid-range
        ((375, 812), 15),    # iPhone X/XS
        ((414, 896), 10),    # iPhone 11 Pro Max
        ((390, 844), 10),    # iPhone 12/13
        ((428, 926), 5),     # iPhone 13 Pro Max
    ]
    
    # Common WebGL renderers
    WEBGL_RENDERERS = {
        "high_end": [
            "ANGLE (NVIDIA GeForce RTX 3080 Direct3D11 vs_5_0 ps_5_0)",
            "ANGLE (NVIDIA GeForce RTX 4070 Direct3D11 vs_5_0 ps_5_0)",
            "ANGLE (AMD Radeon RX 6800 XT Direct3D11 vs_5_0 ps_5_0)",
        ],
        "mid_range": [
            "ANGLE (NVIDIA GeForce GTX 1660 Direct3D11 vs_5_0 ps_5_0)",
            "ANGLE (AMD Radeon RX 580 Direct3D11 vs_5_0 ps_5_0)",
            "ANGLE (Intel(R) UHD Graphics 630 Direct3D11 vs_5_0 ps_5_0)",
        ],
        "mobile": [
            "Adreno (TM) 660",
            "Adreno (TM) 730",
            "Mali-G78 MP24",
            "Mali-G710 MC10",
        ],
        "integrated": [
            "ANGLE (Intel(R) Iris(R) Xe Graphics Direct3D11 vs_5_0 ps_5_0)",
            "ANGLE (Intel(R) UHD Graphics Direct3D11 vs_5_0 ps_5_0)",
        ],
    }
    
    # Common plugins (for desktop only)
    COMMON_PLUGINS = [
        {"name": "PDF Viewer", "filename": "internal-pdf-viewer"},
        {"name": "Chrome PDF Viewer", "filename": "internal-pdf-viewer"},
        {"name": "Chromium PDF Viewer", "filename": "internal-pdf-viewer"},
        {"name": "Microsoft Edge PDF Viewer", "filename": "internal-pdf-viewer"},
        {"name": "WebKit built-in PDF", "filename": "internal-pdf-viewer"},
    ]
    
    def __init__(self):
        self.tls_generator = AdvancedTLSFingerprint2025()
        
    def generate_complete_fingerprint(self, device_type: str = "random",
                                       browser_type: str = "chrome",
                                       country: str = "random") -> Dict[str, Any]:
        """Generate a complete browser fingerprint - Random between Android and Desktop"""
        
        # Get TLS fingerprint first
        tls_fp = self.tls_generator.generate_tls_fingerprint(browser_type)
        chrome_version = tls_fp.get("chrome_version", 134)
        chrome_full_version = tls_fp.get("chrome_full_version", "134.0.6923.127")
        
        # Random device type: Android or Desktop
        if device_type == "random":
            device_type = random.choice(["android", "desktop"])
        
        is_mobile = device_type in ["android", "mobile"]
        
        # Screen resolution based on device type
        if is_mobile:
            resolution = self._weighted_choice(self.MOBILE_RESOLUTIONS)
        else:
            resolution = self._weighted_choice(self.SCREEN_RESOLUTIONS)
        
        # Color depth
        color_depth = random.choice([24, 30, 32])
        
        # Timezone
        timezone_info = self._get_timezone_for_country(country)
        
        # Language
        language_info = self._get_language_for_country(country)
        
        # Platform based on device type
        platform_info = self._get_platform_for_device(device_type)
        
        # WebGL based on device type
        webgl_info = self._generate_webgl_fingerprint(device_type)
        
        # Canvas
        canvas_hash = self._generate_canvas_hash()
        
        # Audio
        audio_fingerprint = self._generate_audio_fingerprint()
        
        # Fonts
        fonts = self._generate_font_list(platform_info["platform"])
        
        fingerprint = {
            # Browser info
            "browser": browser_type,
            "browser_version": chrome_version,
            "browser_full_version": chrome_full_version,
            "user_agent": self._generate_user_agent("desktop", browser_type, chrome_full_version, platform_info),
            
            # Screen
            "screen_width": resolution[0],
            "screen_height": resolution[1],
            "available_width": resolution[0],
            "available_height": resolution[1] - random.randint(40, 80),  # Taskbar
            "color_depth": color_depth,
            "pixel_depth": color_depth,
            "device_pixel_ratio": random.choice([1, 1.25, 1.5, 2]),  # Desktop ratios
            
            # Platform
            "platform": platform_info["platform"],
            "platform_version": platform_info["version"],
            "os_name": platform_info["os_name"],
            "architecture": platform_info["architecture"],
            "is_mobile": is_mobile,
            
            # Timezone
            "timezone": timezone_info["timezone"],
            "timezone_offset": timezone_info["offset"],
            
            # Language
            "language": language_info["primary"],
            "languages": language_info["list"],
            "accept_language": language_info["accept"],
            
            # WebGL
            "webgl_vendor": webgl_info["vendor"],
            "webgl_renderer": webgl_info["renderer"],
            "webgl_version": webgl_info["version"],
            "webgl_extensions": webgl_info["extensions"],
            
            # Canvas
            "canvas_hash": canvas_hash,
            
            # Audio
            "audio_fingerprint": audio_fingerprint,
            
            # Fonts
            "fonts": fonts,
            
            # Hardware
            "hardware_concurrency": random.choice([4, 6, 8, 12, 16]) if not is_mobile else random.choice([4, 6, 8]),
            "device_memory": random.choice([4, 8, 16, 32]) if not is_mobile else random.choice([4, 6, 8]),
            
            # Features
            "do_not_track": random.choice([None, "1"]),
            "cookies_enabled": True,
            "local_storage": True,
            "session_storage": True,
            "indexed_db": True,
            "webdriver": False,  # IMPORTANT: Must be False
            
            # TLS
            "tls_fingerprint": tls_fp,
            
            # Plugins (desktop only)
            "plugins": [] if is_mobile else self.COMMON_PLUGINS[:random.randint(2, 5)],
            
            # Media devices
            "media_devices": self._generate_media_devices(is_mobile),
            
            # Touch support
            "touch_support": {
                "max_touch_points": random.randint(5, 10) if is_mobile else 0,
                "touch_event": is_mobile,
                "touch_start": is_mobile,
            },
            
            # Battery
            "battery": self._generate_battery_info() if is_mobile else None,
            
            # Connection
            "connection": self._generate_connection_info(device_type),
            
            # Timestamp
            "generated_at": time.time(),
        }
        
        return fingerprint
    
    def _weighted_choice(self, items: List[Tuple[Any, int]]) -> Any:
        """Choose item based on weights"""
        choices, weights = zip(*items)
        return random.choices(choices, weights=weights, k=1)[0]
    
    def _get_timezone_for_country(self, country: str) -> Dict[str, Any]:
        """Get timezone info for country"""
        timezones = {
            "ID": {"timezone": "Asia/Jakarta", "offset": -420},  # UTC+7
            "US": {"timezone": random.choice(["America/New_York", "America/Los_Angeles", "America/Chicago"]), "offset": random.choice([-300, -420, -480])},
            "BR": {"timezone": "America/Sao_Paulo", "offset": -180},
            "IN": {"timezone": "Asia/Kolkata", "offset": -330},
            "DE": {"timezone": "Europe/Berlin", "offset": -60},
            "UK": {"timezone": "Europe/London", "offset": 0},
        }
        return timezones.get(country, timezones["ID"])
    
    def _get_language_for_country(self, country: str) -> Dict[str, Any]:
        """Get language settings for country"""
        languages = {
            "ID": {
                "primary": "id-ID",
                "list": ["id-ID", "id", "en-US", "en"],
                "accept": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
            },
            "US": {
                "primary": "en-US",
                "list": ["en-US", "en"],
                "accept": "en-US,en;q=0.9",
            },
            "BR": {
                "primary": "pt-BR",
                "list": ["pt-BR", "pt", "en-US", "en"],
                "accept": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
            },
            "IN": {
                "primary": "en-IN",
                "list": ["en-IN", "en", "hi"],
                "accept": "en-IN,en;q=0.9,hi;q=0.8",
            },
            "DE": {
                "primary": "de-DE",
                "list": ["de-DE", "de", "en-US", "en"],
                "accept": "de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7",
            },
        }
        return languages.get(country, languages["ID"])
    
    def _get_platform_for_device(self, device_type: str = "random") -> Dict[str, Any]:
        """Get platform info for device type - Random between Android and Desktop"""
        if device_type == "random":
            device_type = random.choice(["android", "desktop"])
        
        if device_type in ["android", "mobile"]:
            android_version = random.choice([12, 13, 14, 15])
            return {
                "platform": "Linux armv8l",
                "version": str(android_version),
                "os_name": "Android",
                "architecture": "arm64",
            }
        else:
            platform_choice = random.choice(["Windows", "macOS"])
            
            if platform_choice == "Windows":
                windows_version = random.choice(["10.0", "11.0"])
                return {
                    "platform": "Win32",
                    "version": windows_version,
                    "os_name": "Windows",
                    "architecture": "x86_64",
                }
            else:
                macos_version = random.choice(["10.15", "13.0", "14.0", "14.5"])
                return {
                    "platform": "MacIntel",
                    "version": macos_version,
                    "os_name": "macOS",
                    "architecture": "x86_64",
                }
    
    def _generate_webgl_fingerprint(self, device_type: str = "random") -> Dict[str, Any]:
        """Generate WebGL fingerprint - Random between Android and Desktop"""
        if device_type == "random":
            device_type = random.choice(["android", "desktop"])
        
        if device_type in ["android", "mobile"]:
            # Mobile GPU renderers
            renderer = random.choice(self.WEBGL_RENDERERS.get("mobile", [
                "Adreno (TM) 750",
                "Adreno (TM) 740",
                "Mali-G720 MP12",
                "Mali-G715 MC11",
            ]))
            vendor = "Qualcomm" if "Adreno" in renderer else "ARM"
        else:
            category = random.choice(["high_end", "mid_range", "integrated"])
            renderer = random.choice(self.WEBGL_RENDERERS[category])
            if "NVIDIA" in renderer:
                vendor = "NVIDIA Corporation"
            elif "AMD" in renderer:
                vendor = "AMD"
            else:
                vendor = "Intel Inc."
        
        return {
            "vendor": vendor,
            "renderer": renderer,
            "version": "WebGL 2.0 (OpenGL ES 3.0 Chromium)",
            "extensions": self._get_webgl_extensions(),
        }
    
    def _get_webgl_extensions(self) -> List[str]:
        """Get common WebGL extensions"""
        extensions = [
            "ANGLE_instanced_arrays",
            "EXT_blend_minmax",
            "EXT_color_buffer_half_float",
            "EXT_disjoint_timer_query",
            "EXT_float_blend",
            "EXT_frag_depth",
            "EXT_shader_texture_lod",
            "EXT_texture_compression_bptc",
            "EXT_texture_compression_rgtc",
            "EXT_texture_filter_anisotropic",
            "EXT_sRGB",
            "KHR_parallel_shader_compile",
            "OES_element_index_uint",
            "OES_fbo_render_mipmap",
            "OES_standard_derivatives",
            "OES_texture_float",
            "OES_texture_float_linear",
            "OES_texture_half_float",
            "OES_texture_half_float_linear",
            "OES_vertex_array_object",
            "WEBGL_color_buffer_float",
            "WEBGL_compressed_texture_s3tc",
            "WEBGL_compressed_texture_s3tc_srgb",
            "WEBGL_debug_renderer_info",
            "WEBGL_debug_shaders",
            "WEBGL_depth_texture",
            "WEBGL_draw_buffers",
            "WEBGL_lose_context",
            "WEBGL_multi_draw",
        ]
        # Return random subset
        return random.sample(extensions, random.randint(20, len(extensions)))
    
    def _generate_canvas_hash(self) -> str:
        """Generate realistic canvas hash"""
        # Generate a consistent but unique hash
        seed = random.randint(1000000, 9999999)
        return hashlib.md5(f"canvas_{seed}_{time.time()}".encode()).hexdigest()
    
    def _generate_audio_fingerprint(self) -> str:
        """Generate audio context fingerprint"""
        # Realistic audio fingerprint value
        base = 124.04347527516074
        variation = random.uniform(-0.00001, 0.00001)
        return f"{base + variation:.14f}"
    
    def _generate_font_list(self, platform: str) -> List[str]:
        """Generate font list based on platform"""
        common_fonts = [
            "Arial", "Arial Black", "Comic Sans MS", "Courier New",
            "Georgia", "Impact", "Times New Roman", "Trebuchet MS",
            "Verdana", "Webdings", "Wingdings"
        ]
        
        if "Win" in platform:
            common_fonts.extend(["Calibri", "Cambria", "Segoe UI", "Tahoma"])
        elif "Mac" in platform:
            common_fonts.extend(["Helvetica", "Helvetica Neue", "Lucida Grande", "Monaco"])
        
        return sorted(set(random.sample(common_fonts, random.randint(8, len(common_fonts)))))
    
    def _generate_media_devices(self, is_mobile: bool) -> Dict[str, int]:
        """Generate media devices count"""
        if is_mobile:
            return {
                "audioinput": random.randint(1, 2),
                "audiooutput": random.randint(1, 2),
                "videoinput": random.randint(1, 3),  # Front + back + maybe extra
            }
        else:
            return {
                "audioinput": random.randint(1, 3),
                "audiooutput": random.randint(1, 3),
                "videoinput": random.randint(0, 2),
            }
    
    def _generate_battery_info(self) -> Dict[str, Any]:
        """Generate battery info for mobile"""
        return {
            "charging": random.choice([True, False]),
            "level": random.uniform(0.2, 1.0),
            "charging_time": random.randint(0, 7200) if random.random() > 0.5 else float('inf'),
            "discharging_time": random.randint(3600, 28800),
        }
    
    def _generate_connection_info(self, device_type: str = "desktop") -> Dict[str, Any]:
        """Generate network connection info - Random based on device type"""
        if device_type == "random":
            device_type = random.choice(["android", "desktop"])
        
        if device_type in ["android", "mobile"]:
            # Mobile connection
            ect = random.choice(["4g", "3g"])
            downlink = random.uniform(5.0, 50.0)
            rtt = random.randint(30, 150)
        else:
            # Desktop broadband
            ect = "4g"
            downlink = random.uniform(50.0, 200.0)
            rtt = random.randint(10, 50)
        
        return {
            "effective_type": ect,
            "downlink": round(downlink, 2),
            "rtt": rtt,
            "save_data": False,
        }
    
    def _generate_user_agent(self, device_type: str = "random", browser_type: str = "chrome",
                            chrome_version: str = "134.0.6923.127", platform_info: Dict = None) -> str:
        """Generate realistic User-Agent string - Random between Android and Desktop"""
        if device_type == "random":
            device_type = random.choice(["android", "desktop"])
        
        if platform_info is None:
            if device_type in ["android", "mobile"]:
                platform_info = {"os_name": "Android", "version": random.choice(["12", "13", "14", "15"])}
            else:
                platform_info = {"os_name": random.choice(["Windows", "macOS"])}
        
        if platform_info.get("os_name") == "Android":
            android_version = platform_info.get("version", "14")
            device_model = random.choice([
                "SM-S928B", "SM-S918B", "SM-A546B", "SM-A536B",
                "SM-G998B", "SM-G991B", "SM-A525F", "SM-A725F",
                "Pixel 8", "Pixel 7", "Pixel 6",
            ])
            return f"Mozilla/5.0 (Linux; Android {android_version}; {device_model}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{chrome_version} Mobile Safari/537.36"
        elif platform_info.get("os_name") == "Windows":
            windows_version = random.choice(["10.0", "11.0"])
            return f"Mozilla/5.0 (Windows NT {windows_version}; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{chrome_version} Safari/537.36"
        else:
            macos_version = random.choice(["10_15_7", "13_0", "14_0", "14_5"])
            return f"Mozilla/5.0 (Macintosh; Intel Mac OS X {macos_version}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{chrome_version} Safari/537.36"


# Global instance
tls_fingerprint_generator = AdvancedTLSFingerprint2025()
browser_fingerprint_generator = AdvancedBrowserFingerprint2025()

# ===================== ADVANCED IP SPOOFING 2025 =====================

# ===================== ULTIMATE ANTI-DETECTION SYSTEM 2025 =====================

class UltimateAntiDetection2025:
    """
    Ultimate Anti-Detection System 2025 - Military Grade Evasion
    
    Advanced techniques to bypass all anti-bot systems:
    1. Human-like request timing with realistic delays
    2. Browser behavior simulation (mouse, keyboard, scroll)
    3. Canvas/WebGL fingerprint randomization
    4. Advanced cookie chain management
    5. Request pacing with exponential backoff
    6. Pre-request warmup (visit pages naturally)
    7. Referrer chain building
    8. Advanced header ordering and normalization
    9. TLS fingerprint rotation
    10. Request signature obfuscation
    """
    
    def __init__(self):
        self.request_history = []
        self.last_request_time = 0
        self.session_start_time = time.time()
        self.page_visit_count = 0
        self.warmup_complete = False
        
    def get_human_delay(self, action_type: str = "click") -> float:
        """
        Generate human-like delays based on action type
        Uses statistical distributions matching real human behavior
        """
        delays = {
            "page_load": (2.5, 5.0, 0.8),      # (min, max, std_dev)
            "form_fill": (0.8, 2.5, 0.4),
            "button_click": (0.3, 1.2, 0.2),
            "field_focus": (0.2, 0.8, 0.15),
            "typing_char": (0.05, 0.2, 0.03),
            "scroll": (0.5, 2.0, 0.3),
            "api_call": (1.5, 4.0, 0.6),
            "verification": (3.0, 8.0, 1.0),
            "between_steps": (2.0, 6.0, 0.8),
            "reading": (1.0, 3.0, 0.5),
        }
        
        params = delays.get(action_type, (1.0, 3.0, 0.5))
        
        # Use truncated normal distribution
        mean = (params[0] + params[1]) / 2
        std = params[2]
        
        while True:
            delay = random.gauss(mean, std)
            if params[0] <= delay <= params[1]:
                # Add micro-variations like real humans
                delay += random.uniform(-0.1, 0.1)
                return max(0.1, delay)
    
    def generate_mouse_movement_data(self) -> Dict[str, Any]:
        """Generate realistic mouse movement patterns"""
        # Number of points in the movement path
        num_points = random.randint(15, 35)
        
        # Starting and ending positions (random but within viewport)
        start_x = random.randint(0, 1920)
        start_y = random.randint(0, 1080)
        end_x = random.randint(400, 1500)  # Typical button areas
        end_y = random.randint(300, 800)
        
        points = []
        timestamps = []
        current_time = 0
        
        for i in range(num_points):
            progress = i / (num_points - 1)
            
            # Use bezier curve for natural movement
            # Add random jitter to simulate hand tremor
            jitter_x = random.gauss(0, 3)
            jitter_y = random.gauss(0, 3)
            
            x = start_x + (end_x - start_x) * self._ease_out_cubic(progress) + jitter_x
            y = start_y + (end_y - start_y) * self._ease_out_cubic(progress) + jitter_y
            
            points.append({"x": int(x), "y": int(y)})
            
            # Time between points varies (slower at start/end)
            if progress < 0.2 or progress > 0.8:
                interval = random.uniform(20, 50)
            else:
                interval = random.uniform(8, 25)
            
            current_time += interval
            timestamps.append(int(current_time))
        
        return {
            "path": points,
            "timestamps": timestamps,
            "duration": current_time,
            "velocity": self._calculate_velocity(points, timestamps),
            "acceleration": random.uniform(0.8, 1.5),
            "clicks": [{"x": end_x, "y": end_y, "time": current_time}],
        }
    
    def _ease_out_cubic(self, t: float) -> float:
        """Cubic ease-out function for natural movement"""
        return 1 - pow(1 - t, 3)
    
    def _calculate_velocity(self, points: List, timestamps: List) -> float:
        """Calculate average velocity of mouse movement"""
        if len(points) < 2:
            return 0
        
        total_distance = 0
        for i in range(1, len(points)):
            dx = points[i]["x"] - points[i-1]["x"]
            dy = points[i]["y"] - points[i-1]["y"]
            total_distance += math.sqrt(dx*dx + dy*dy)
        
        total_time = timestamps[-1] - timestamps[0]
        return total_distance / max(1, total_time)
    
    def generate_keyboard_timing(self, text: str) -> List[Dict]:
        """Generate realistic keyboard input timing"""
        events = []
        current_time = 0
        
        for i, char in enumerate(text):
            # Time to press key (varies by character)
            if char in 'asdfjkl;':  # Home row - faster
                press_delay = random.gauss(80, 15)
            elif char.isupper():  # Shift needed - slower
                press_delay = random.gauss(120, 25)
            elif char.isdigit():  # Number row - medium
                press_delay = random.gauss(100, 20)
            else:
                press_delay = random.gauss(95, 18)
            
            current_time += max(30, press_delay)
            
            events.append({
                "char": char,
                "keydown": current_time,
                "keyup": current_time + random.randint(30, 80),
            })
            
            # Occasional pause (thinking, correcting)
            if random.random() < 0.05:
                current_time += random.randint(200, 800)
        
        return events
    
    def generate_scroll_pattern(self) -> Dict[str, Any]:
        """Generate realistic scroll patterns"""
        scroll_events = []
        current_y = 0
        
        num_scrolls = random.randint(3, 12)
        
        for _ in range(num_scrolls):
            # Random scroll amount (usually 100-300 pixels)
            delta_y = random.choice([100, 150, 200, 250, 300, -100, -150])
            
            # Momentum scrolling simulation
            momentum_factor = random.uniform(0.8, 1.3)
            
            scroll_events.append({
                "deltaY": delta_y * momentum_factor,
                "timestamp": int(time.time() * 1000),
                "isMomentum": random.random() > 0.7,
            })
            
            current_y += delta_y
            
            # Pause between scrolls
            time.sleep(random.uniform(0.1, 0.5))
        
        return {
            "events": scroll_events,
            "total_scroll": current_y,
            "scroll_count": num_scrolls,
        }
    
    def generate_canvas_fingerprint(self) -> Dict[str, Any]:
        """Generate unique but realistic canvas fingerprint"""
        # Common screen resolutions
        resolutions = [
            (1920, 1080), (2560, 1440), (1366, 768), (1536, 864),
            (1440, 900), (1280, 720), (1600, 900), (2880, 1800),
        ]
        
        width, height = random.choice(resolutions)
        
        # Generate realistic canvas data hash
        base_data = f"{width}x{height}:{random.randint(1, 999999)}"
        canvas_hash = hashlib.md5(base_data.encode()).hexdigest()
        
        return {
            "hash": canvas_hash,
            "width": width,
            "height": height,
            "colorDepth": random.choice([24, 32]),
            "pixelRatio": random.choice([1, 1.25, 1.5, 2, 2.5, 3]),
        }
    
    def generate_webgl_fingerprint(self) -> Dict[str, Any]:
        """Generate realistic WebGL fingerprint"""
        vendors = [
            ("Google Inc. (NVIDIA)", "ANGLE (NVIDIA, NVIDIA GeForce RTX 4090, OpenGL 4.5)"),
            ("Google Inc. (NVIDIA)", "ANGLE (NVIDIA, NVIDIA GeForce RTX 4080, OpenGL 4.5)"),
            ("Google Inc. (NVIDIA)", "ANGLE (NVIDIA, NVIDIA GeForce RTX 3080, OpenGL 4.5)"),
            ("Google Inc. (AMD)", "ANGLE (AMD, AMD Radeon RX 7900 XTX, OpenGL 4.5)"),
            ("Google Inc. (Intel)", "ANGLE (Intel, Intel(R) UHD Graphics 770, OpenGL 4.5)"),
            ("Apple Inc.", "Apple GPU"),
            ("ARM", "Mali-G78"),
            ("Qualcomm", "Adreno (TM) 750"),
        ]
        
        vendor, renderer = random.choice(vendors)
        
        return {
            "vendor": vendor,
            "renderer": renderer,
            "version": "WebGL 2.0",
            "shadingLanguageVersion": "WebGL GLSL ES 3.00",
            "maxTextureSize": random.choice([8192, 16384, 32768]),
            "maxViewportDims": [random.choice([16384, 32768]), random.choice([16384, 32768])],
        }
    
    def generate_audio_fingerprint(self) -> str:
        """Generate realistic audio fingerprint hash"""
        # Simulate AudioContext fingerprint
        sample_rate = random.choice([44100, 48000])
        channel_count = random.choice([2, 6, 8])
        base = f"audio:{sample_rate}:{channel_count}:{random.randint(1, 999999)}"
        return hashlib.sha256(base.encode()).hexdigest()[:32]
    
    def build_referrer_chain(self, target_url: str) -> List[str]:
        """Build realistic referrer chain"""
        chains = [
            ["https://www.google.com/", "https://www.instagram.com/", target_url],
            ["https://www.google.com/search?q=instagram", "https://www.instagram.com/", target_url],
            ["https://www.instagram.com/", target_url],
            ["https://l.instagram.com/", target_url],
            ["https://www.facebook.com/", "https://www.instagram.com/", target_url],
        ]
        return random.choice(chains)
    
    def should_add_warmup_request(self) -> bool:
        """Determine if warmup requests are needed"""
        if self.warmup_complete:
            return False
        
        if self.page_visit_count < 2:
            return True
        
        return False
    
    def get_warmup_urls(self) -> List[str]:
        """Get URLs to visit for session warmup"""
        return [
            "https://www.instagram.com/",
            "https://www.instagram.com/accounts/emailsignup/",
        ]
    
    def mark_warmup_complete(self):
        """Mark session warmup as complete"""
        self.warmup_complete = True
        self.page_visit_count += 1
    
    def get_request_signature(self) -> Dict[str, Any]:
        """Generate request signature for anti-bot bypass"""
        timestamp = int(time.time() * 1000)
        random_id = ''.join(random.choices(string.ascii_lowercase + string.digits, k=32))
        
        return {
            "timestamp": timestamp,
            "nonce": random_id,
            "client_id": self._generate_client_id(),
            "session_id": self._generate_session_id(),
        }
    
    def _generate_client_id(self) -> str:
        """Generate consistent client ID for session"""
        base = f"client_{random.randint(100000000, 999999999)}"
        return hashlib.md5(base.encode()).hexdigest()[:16]
    
    def _generate_session_id(self) -> str:
        """Generate session ID in Instagram format"""
        parts = [
            ''.join(random.choices(string.ascii_lowercase + string.digits, k=6)),
            ''.join(random.choices(string.ascii_lowercase + string.digits, k=6)),
            ''.join(random.choices(string.ascii_lowercase + string.digits, k=6)),
        ]
        return ':'.join(parts)
    
    def calculate_backoff_delay(self, retry_count: int, base_delay: float = 2.0) -> float:
        """Calculate exponential backoff with jitter"""
        # Exponential backoff: base * 2^retry
        delay = base_delay * (2 ** retry_count)
        
        # Add jitter (±25%)
        jitter = delay * random.uniform(-0.25, 0.25)
        delay += jitter
        
        # Cap at 60 seconds
        return min(delay, 60.0)
    
    def get_optimal_request_timing(self) -> Dict[str, float]:
        """Get optimal timing for requests to avoid rate limits"""
        time_since_start = time.time() - self.session_start_time
        requests_made = len(self.request_history)
        
        # Calculate request rate
        if time_since_start > 0:
            current_rate = requests_made / time_since_start
        else:
            current_rate = 0
        
        # Optimal rate is about 1 request per 3-5 seconds
        if current_rate > 0.3:  # More than 1 request per 3 seconds
            recommended_delay = random.uniform(5.0, 10.0)
        elif current_rate > 0.2:
            recommended_delay = random.uniform(3.0, 6.0)
        else:
            recommended_delay = random.uniform(2.0, 4.0)
        
        return {
            "recommended_delay": recommended_delay,
            "current_rate": current_rate,
            "requests_made": requests_made,
            "session_duration": time_since_start,
        }
    
    def record_request(self, url: str, status: int):
        """Record request for rate limit management"""
        self.request_history.append({
            "url": url,
            "status": status,
            "timestamp": time.time(),
        })
        self.last_request_time = time.time()
        
        # Keep only last 100 requests
        if len(self.request_history) > 100:
            self.request_history = self.request_history[-100:]




# ===================== ULTRA STEALTH IP SYSTEM 2025 - NEXT GENERATION =====================

class UltraStealthIPGenerator2025:
    """
    Next-Generation Ultra Stealth IP Generator 2025
    
    Teknik yang digunakan:
    1. Real ISP IP Range Database - menggunakan range IP asli dari ISP
    2. Carrier Grade NAT (CGNAT) Simulation - simulasi IP dari CGNAT yang umum digunakan
    3. Time-based IP Rotation Pattern - pattern rotasi berdasarkan waktu seperti ISP asli
    4. Geographic IP Clustering - IP clustering berdasarkan lokasi geografis
    5. ISP-specific IP Allocation Patterns - pattern alokasi spesifik per ISP
    6. Mobile Network IP Simulation - simulasi IP dari jaringan mobile (3G/4G/5G)
    7. Dynamic IP Lease Simulation - simulasi DHCP lease seperti IP dinamis asli
    8. Anti-Fingerprinting Headers - headers yang tidak bisa di-fingerprint
    """
    
    def __init__(self):
        self.used_ips = set()
        self.ip_lease_times = {}
        self.last_rotation = {}
        self._ip_timestamps = {}  # Track IP freshness
        self._ip_countries = {}   # Track IP country for fingerprint matching
        
        # Real ISP IP ranges from IANA/APNIC/ARIN allocations
        self.real_isp_ranges = self._load_real_isp_ranges()
        
        # CGNAT ranges (100.64.0.0/10) - ISPs use these for mobile users
        self.cgnat_ranges = self._get_cgnat_simulation_ranges()
        
        # Mobile carrier IP pools
        self.mobile_ip_pools = self._initialize_mobile_pools()
        
    def _load_real_isp_ranges(self) -> Dict[str, List[Dict]]:
        """Load real ISP IP allocations from regional registries"""
        return {
            # ===== USA - ARIN Allocations =====
            "US": {
                "verizon_wireless": [
                    {"start": "174.192.0.0", "end": "174.255.255.255", "type": "mobile", "cgnat": False},
                    {"start": "70.192.0.0", "end": "70.223.255.255", "type": "mobile", "cgnat": False},
                    {"start": "98.0.0.0", "end": "98.127.255.255", "type": "mobile", "cgnat": False},
                    {"start": "71.160.0.0", "end": "71.191.255.255", "type": "mobile", "cgnat": False},
                ],
                "att_wireless": [
                    {"start": "166.128.0.0", "end": "166.255.255.255", "type": "mobile", "cgnat": False},
                    {"start": "107.64.0.0", "end": "107.127.255.255", "type": "mobile", "cgnat": False},
                    {"start": "32.0.0.0", "end": "32.255.255.255", "type": "mobile", "cgnat": True},
                ],
                "tmobile": [
                    {"start": "172.32.0.0", "end": "172.63.255.255", "type": "mobile", "cgnat": True},
                    {"start": "100.128.0.0", "end": "100.191.255.255", "type": "mobile", "cgnat": True},
                    {"start": "208.54.0.0", "end": "208.54.255.255", "type": "mobile", "cgnat": False},
                ],
                "comcast": [
                    {"start": "73.0.0.0", "end": "73.255.255.255", "type": "residential", "cgnat": False},
                    {"start": "50.128.0.0", "end": "50.255.255.255", "type": "residential", "cgnat": False},
                    {"start": "24.0.0.0", "end": "24.63.255.255", "type": "residential", "cgnat": False},
                ],
                "spectrum": [
                    {"start": "72.64.0.0", "end": "72.127.255.255", "type": "residential", "cgnat": False},
                    {"start": "97.64.0.0", "end": "97.127.255.255", "type": "residential", "cgnat": False},
                    {"start": "24.128.0.0", "end": "24.191.255.255", "type": "residential", "cgnat": False},
                ],
                "cox": [
                    {"start": "68.96.0.0", "end": "68.111.255.255", "type": "residential", "cgnat": False},
                    {"start": "76.160.0.0", "end": "76.191.255.255", "type": "residential", "cgnat": False},
                ],
            },
            # ===== Australia - APNIC Allocations =====
            "AU": {
                "telstra": [
                    {"start": "1.120.0.0", "end": "1.127.255.255", "type": "residential", "cgnat": False},
                    {"start": "101.160.0.0", "end": "101.191.255.255", "type": "mobile", "cgnat": False},
                    {"start": "110.144.0.0", "end": "110.175.255.255", "type": "residential", "cgnat": False},
                    {"start": "120.144.0.0", "end": "120.159.255.255", "type": "mobile", "cgnat": False},
                ],
                "optus": [
                    {"start": "49.176.0.0", "end": "49.191.255.255", "type": "mobile", "cgnat": False},
                    {"start": "121.44.0.0", "end": "121.47.255.255", "type": "residential", "cgnat": False},
                    {"start": "211.24.0.0", "end": "211.31.255.255", "type": "residential", "cgnat": False},
                ],
                "vodafone_au": [
                    {"start": "101.112.0.0", "end": "101.127.255.255", "type": "mobile", "cgnat": False},
                    {"start": "110.174.0.0", "end": "110.175.255.255", "type": "mobile", "cgnat": False},
                ],
                "tpg": [
                    {"start": "27.32.0.0", "end": "27.63.255.255", "type": "residential", "cgnat": False},
                    {"start": "120.148.0.0", "end": "120.159.255.255", "type": "residential", "cgnat": False},
                ],
            },
            # ===== Canada - ARIN Allocations =====
            "CA": {
                "rogers": [
                    {"start": "24.100.0.0", "end": "24.127.255.255", "type": "residential", "cgnat": False},
                    {"start": "64.228.0.0", "end": "64.231.255.255", "type": "residential", "cgnat": False},
                    {"start": "99.224.0.0", "end": "99.255.255.255", "type": "mobile", "cgnat": False},
                ],
                "bell": [
                    {"start": "70.48.0.0", "end": "70.63.255.255", "type": "residential", "cgnat": False},
                    {"start": "142.112.0.0", "end": "142.127.255.255", "type": "residential", "cgnat": False},
                    {"start": "174.88.0.0", "end": "174.95.255.255", "type": "mobile", "cgnat": False},
                ],
                "telus": [
                    {"start": "24.64.0.0", "end": "24.95.255.255", "type": "residential", "cgnat": False},
                    {"start": "70.64.0.0", "end": "70.79.255.255", "type": "mobile", "cgnat": False},
                    {"start": "184.64.0.0", "end": "184.79.255.255", "type": "mobile", "cgnat": False},
                ],
            },
            # ===== UK - RIPE Allocations =====
            "UK": {
                "bt": [
                    {"start": "2.24.0.0", "end": "2.31.255.255", "type": "residential", "cgnat": False},
                    {"start": "86.128.0.0", "end": "86.191.255.255", "type": "residential", "cgnat": False},
                    {"start": "90.192.0.0", "end": "90.255.255.255", "type": "residential", "cgnat": False},
                ],
                "ee": [
                    {"start": "2.120.0.0", "end": "2.127.255.255", "type": "mobile", "cgnat": False},
                    {"start": "82.128.0.0", "end": "82.135.255.255", "type": "mobile", "cgnat": False},
                    {"start": "86.0.0.0", "end": "86.31.255.255", "type": "mobile", "cgnat": False},
                ],
                "vodafone_uk": [
                    {"start": "31.48.0.0", "end": "31.63.255.255", "type": "mobile", "cgnat": False},
                    {"start": "92.40.0.0", "end": "92.47.255.255", "type": "mobile", "cgnat": False},
                    {"start": "176.248.0.0", "end": "176.255.255.255", "type": "mobile", "cgnat": False},
                ],
                "sky": [
                    {"start": "2.120.0.0", "end": "2.127.255.255", "type": "residential", "cgnat": False},
                    {"start": "78.144.0.0", "end": "78.159.255.255", "type": "residential", "cgnat": False},
                    {"start": "90.240.0.0", "end": "90.255.255.255", "type": "residential", "cgnat": False},
                ],
            },
            # ===== Germany - RIPE Allocations =====
            "DE": {
                "telekom_de": [
                    {"start": "91.64.0.0", "end": "91.127.255.255", "type": "residential", "cgnat": False},
                    {"start": "93.192.0.0", "end": "93.223.255.255", "type": "residential", "cgnat": False},
                    {"start": "84.128.0.0", "end": "84.191.255.255", "type": "residential", "cgnat": False},
                ],
                "vodafone_de": [
                    {"start": "80.128.0.0", "end": "80.191.255.255", "type": "residential", "cgnat": False},
                    {"start": "91.0.0.0", "end": "91.63.255.255", "type": "mobile", "cgnat": False},
                    {"start": "92.72.0.0", "end": "92.79.255.255", "type": "mobile", "cgnat": False},
                ],
                "o2_de": [
                    {"start": "82.112.0.0", "end": "82.127.255.255", "type": "mobile", "cgnat": False},
                    {"start": "92.224.0.0", "end": "92.255.255.255", "type": "mobile", "cgnat": False},
                ],
            },
            # ===== France - RIPE Allocations =====
            "FR": {
                "orange_fr": [
                    {"start": "2.0.0.0", "end": "2.15.255.255", "type": "residential", "cgnat": False},
                    {"start": "80.8.0.0", "end": "80.15.255.255", "type": "residential", "cgnat": False},
                    {"start": "86.192.0.0", "end": "86.255.255.255", "type": "residential", "cgnat": False},
                ],
                "sfr": [
                    {"start": "37.160.0.0", "end": "37.175.255.255", "type": "residential", "cgnat": False},
                    {"start": "92.128.0.0", "end": "92.159.255.255", "type": "residential", "cgnat": False},
                ],
                "free_fr": [
                    {"start": "82.64.0.0", "end": "82.127.255.255", "type": "residential", "cgnat": False},
                    {"start": "88.160.0.0", "end": "88.191.255.255", "type": "residential", "cgnat": False},
                ],
            },
            # ===== Japan - APNIC Allocations =====
            "JP": {
                "ntt_docomo": [
                    {"start": "1.64.0.0", "end": "1.79.255.255", "type": "mobile", "cgnat": False},
                    {"start": "49.96.0.0", "end": "49.111.255.255", "type": "mobile", "cgnat": False},
                    {"start": "126.160.0.0", "end": "126.191.255.255", "type": "mobile", "cgnat": False},
                ],
                "softbank": [
                    {"start": "126.0.0.0", "end": "126.63.255.255", "type": "residential", "cgnat": False},
                    {"start": "220.96.0.0", "end": "220.127.255.255", "type": "mobile", "cgnat": False},
                ],
                "au_kddi": [
                    {"start": "106.128.0.0", "end": "106.191.255.255", "type": "mobile", "cgnat": False},
                    {"start": "182.160.0.0", "end": "182.175.255.255", "type": "mobile", "cgnat": False},
                ],
            },
            # ===== Singapore - APNIC Allocations =====
            "SG": {
                "singtel": [
                    {"start": "27.104.0.0", "end": "27.111.255.255", "type": "residential", "cgnat": False},
                    {"start": "116.88.0.0", "end": "116.95.255.255", "type": "residential", "cgnat": False},
                    {"start": "219.74.0.0", "end": "219.75.255.255", "type": "residential", "cgnat": False},
                ],
                "starhub": [
                    {"start": "27.125.0.0", "end": "27.125.255.255", "type": "residential", "cgnat": False},
                    {"start": "101.127.0.0", "end": "101.127.255.255", "type": "residential", "cgnat": False},
                ],
            },
            # ===== Netherlands - RIPE Allocations =====
            "NL": {
                "kpn": [
                    {"start": "77.160.0.0", "end": "77.175.255.255", "type": "residential", "cgnat": False},
                    {"start": "84.24.0.0", "end": "84.31.255.255", "type": "residential", "cgnat": False},
                    {"start": "94.208.0.0", "end": "94.223.255.255", "type": "residential", "cgnat": False},
                ],
                "vodafone_nl": [
                    {"start": "84.80.0.0", "end": "84.87.255.255", "type": "residential", "cgnat": False},
                    {"start": "86.80.0.0", "end": "86.95.255.255", "type": "residential", "cgnat": False},
                ],
            },
        }
    
    def _get_cgnat_simulation_ranges(self) -> List[Dict]:
        """CGNAT (Carrier Grade NAT) ranges - 100.64.0.0/10
        Many mobile carriers use CGNAT, making these IPs appear as shared residential
        """
        return [
            # T-Mobile US uses heavy CGNAT
            {"range": "100.64.0.0/10", "carriers": ["tmobile", "metro_pcs"]},
            # Some ISPs use private-like ranges internally
        ]
    
    def _initialize_mobile_pools(self) -> Dict[str, List[str]]:
        """Initialize mobile carrier IP pools with realistic patterns"""
        return {}  # Will be populated dynamically
    
    def generate_ultra_stealth_ip(self, country: str = "random", isp: str = None, ip_type: str = "random") -> Dict[str, Any]:
        """
        Generate an ultra-stealth IP - NOW WITH RANDOM COUNTRY SUPPORT
        
        Strategy:
        - If country="random", select from all 40+ countries in database
        - 80% Mobile ISPs for better success rate
        - 20% Broadband/WiFi ISPs
        - Filter out blocked IPs from blacklist
        - MULTI-SOURCE verification (ip-api.com, ipinfo.io, ipwhois.app)
        - All fingerprints MATCH the selected country
        """
        
        # Load country database
        country_db = self._load_country_database_for_ip()
        all_countries = list(country_db.get("countries", {}).keys())
        
        if not all_countries:
            all_countries = ["US", "AU", "CA", "GB", "DE", "FR", "JP", "KR", "SG", "NL", "NZ", "IT", "ES", 
                           "MX", "BR", "TH", "MY", "PH", "VN", "IN", "ID", "AE", "SA", "TR", "IL",
                           "AR", "CL", "CO", "PE", "PT", "BE", "CH", "AT", "PL", "SE", "NO", "DK",
                           "CN", "TW", "HK", "PK"]
        
        # TRULY RANDOM COUNTRY SELECTION
        if country == "random" or country not in all_countries:
            country = random.choice(all_countries)
            print(f"{cyan}    🌍 Random country selected: {country}{reset}")
        
        # Get country data
        country_data = country_db.get("countries", {}).get(country, {})
        
        # PRIORITIZE MOBILE - 80% mobile, 20% broadband
        if ip_type == "random":
            ip_type = "mobile" if random.random() < 0.8 else "residential"
        
        # Get ISPs for this country
        country_isps = country_data.get("isps", {})
        mobile_isps = country_isps.get("mobile", {})
        broadband_isps = country_isps.get("broadband", {})
        
        # Select ISP based on type
        if ip_type == "mobile" and mobile_isps:
            selected_isp_key = random.choice(list(mobile_isps.keys())) if not isp else isp
            isp_data = mobile_isps.get(selected_isp_key, {})
        elif broadband_isps:
            selected_isp_key = random.choice(list(broadband_isps.keys())) if not isp else isp
            isp_data = broadband_isps.get(selected_isp_key, {})
        else:
            # Fallback to any available ISP
            all_isps = {**mobile_isps, **broadband_isps}
            if all_isps:
                selected_isp_key = random.choice(list(all_isps.keys()))
                isp_data = all_isps.get(selected_isp_key, {})
            else:
                # Ultimate fallback - use Indonesia ranges
                return self._generate_indonesia_fallback_ip(ip_type)
        
        # Get IP ranges for selected ISP
        isp_ranges = isp_data.get("ranges", [])
        isp_name = isp_data.get("name", selected_isp_key)
        isp_asn = isp_data.get("asn", "")
        
        if not isp_ranges:
            print(f"{kuning}    ⚠ No IP ranges for {isp_name}, using fallback...{reset}")
            return self._generate_indonesia_fallback_ip(ip_type)
        
        # Generate IP within the range and verify
        max_verify_attempts = 15
        verified_ip = None
        
        for verify_attempt in range(max_verify_attempts):
            # Select random range
            selected_range = random.choice(isp_ranges)
            
            # Generate IP from CIDR range
            ip = self._generate_ip_from_cidr_range(selected_range)
            
            if not ip:
                continue
            
            # CHECK BLOCKED IPS - Skip if in blacklist
            if is_ip_blocked(ip):
                print(f"{merah}    ✗ IP {ip} is in blocked list, skipping...{reset}")
                continue
            
            # Ensure uniqueness
            if ip in self.used_ips:
                continue
            
            # REAL-TIME VERIFICATION
            verification = self._verify_ip_realtime(ip)
            
            # Accept IP if verified and usable
            if verification["verified"] and verification["is_usable"]:
                verified_country = verification.get("country", country)
                print(f"{hijau}    ✓ IP verified: {ip} ({verification.get('isp', isp_name)}) [{verified_country}] [via {verification.get('source', 'unknown')}]{reset}")
                verified_ip = ip
                self.used_ips.add(ip)
                self._ip_timestamps[ip] = time.time()
                self._ip_countries[ip] = verified_country
                
                # Use verified ISP name if available
                if verification.get("isp"):
                    isp_name = verification["isp"]
                break
            elif verification["is_proxy"] or verification["is_datacenter"]:
                print(f"{merah}    ✗ IP {ip} is proxy/datacenter, skipping...{reset}")
            elif not verification["verified"]:
                # API unavailable - accept without verification
                print(f"{kuning}    ○ API unavailable for {ip}, accepting without verification...{reset}")
                verified_ip = ip
                self.used_ips.add(ip)
                self._ip_timestamps[ip] = time.time()
                self._ip_countries[ip] = country
                break
        
        if not verified_ip:
            print(f"{kuning}    ⚠ Could not generate verified IP for {country}, trying different country...{reset}")
            # Try other countries instead of just Indonesia fallback
            fallback_countries = ["US", "AU", "GB", "DE", "JP", "CA", "FR", "NL"]
            random.shuffle(fallback_countries)
            for fallback_country in fallback_countries:
                if fallback_country != country:
                    fallback_result = self._try_country_fallback(fallback_country, ip_type)
                    if fallback_result:
                        return fallback_result
            # Ultimate fallback - use any working IP
            return self._generate_any_country_fallback_ip(ip_type)
        
        # Build complete IP profile with matching fingerprint for the COUNTRY
        return self._build_ultra_stealth_profile_for_country(
            verified_ip, 
            self._ip_countries.get(verified_ip, country), 
            isp_name, 
            isp_asn,
            country_data,
            ip_type
        )
    
    def _load_country_database_for_ip(self) -> Dict[str, Any]:
        """Load country database from JSON file"""
        try:
            db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "country_database.json")
            if os.path.exists(db_path):
                with open(db_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            print(f"{kuning}    Warning: Could not load country_database.json: {e}{reset}")
        return {"countries": {}}
    
    def _generate_ip_from_cidr_range(self, cidr: str) -> Optional[str]:
        """Generate random IP from CIDR range"""
        try:
            network = ipaddress.ip_network(cidr, strict=False)
            # Get all hosts in the network
            hosts = list(network.hosts())
            if not hosts:
                return None
            
            # Exclude common server IPs
            excluded_octets = {0, 1, 2, 100, 128, 200, 254, 255}
            valid_hosts = [h for h in hosts if int(str(h).split('.')[-1]) not in excluded_octets]
            
            if not valid_hosts:
                valid_hosts = hosts
            
            # Add timestamp-based entropy
            timestamp_entropy = int(time.time() * 1000) % len(valid_hosts)
            random_index = (random.randint(0, len(valid_hosts) - 1) + timestamp_entropy) % len(valid_hosts)
            
            return str(valid_hosts[random_index])
        except Exception as e:
            print(f"{kuning}    Warning: Could not parse CIDR {cidr}: {e}{reset}")
            return None
    
    def _try_country_fallback(self, country: str, ip_type: str) -> Optional[Dict[str, Any]]:
        """Try to generate IP from a specific country as fallback"""
        try:
            country_db = self._load_country_database_for_ip()
            country_data = country_db.get("countries", {}).get(country, {})
            
            if not country_data:
                return None
            
            country_isps = country_data.get("isps", {})
            mobile_isps = country_isps.get("mobile", {})
            broadband_isps = country_isps.get("broadband", {})
            
            # Select ISP based on type
            if ip_type == "mobile" and mobile_isps:
                isp_key = random.choice(list(mobile_isps.keys()))
                isp_data = mobile_isps.get(isp_key, {})
            elif broadband_isps:
                isp_key = random.choice(list(broadband_isps.keys()))
                isp_data = broadband_isps.get(isp_key, {})
            else:
                return None
            
            isp_ranges = isp_data.get("ranges", [])
            if not isp_ranges:
                return None
            
            # Try to generate IP
            for _ in range(5):
                selected_range = random.choice(isp_ranges)
                ip = self._generate_ip_from_cidr_range(selected_range)
                
                if ip and not is_ip_blocked(ip) and ip not in self.used_ips:
                    self.used_ips.add(ip)
                    self._ip_timestamps[ip] = time.time()
                    self._ip_countries[ip] = country
                    
                    print(f"{hijau}    ✓ Fallback IP generated: {ip} ({isp_data.get('name', isp_key)}) [{country}]{reset}")
                    return self._build_ultra_stealth_profile_for_country(
                        ip, country, isp_data.get("name", isp_key), 
                        isp_data.get("asn", ""), country_data, ip_type
                    )
            
            return None
        except Exception as e:
            print(f"{kuning}    Fallback error for {country}: {e}{reset}")
            return None
    
    def _generate_any_country_fallback_ip(self, ip_type: str) -> Dict[str, Any]:
        """Ultimate fallback - generate IP from any available country"""
        # Try multiple random countries
        all_countries = ["US", "AU", "CA", "GB", "DE", "FR", "JP", "KR", "SG", "NL", 
                        "IT", "ES", "MX", "BR", "TH", "MY", "IN", "ID"]
        random.shuffle(all_countries)
        
        for country in all_countries:
            result = self._try_country_fallback(country, ip_type)
            if result:
                return result
        
        # If all fail, use Indonesia as last resort
        return self._generate_indonesia_fallback_ip(ip_type)

    def _generate_indonesia_fallback_ip(self, ip_type: str) -> Dict[str, Any]:
        """Fallback to Indonesia IP if country database fails"""
        # Use existing Indonesia ranges
        country_ranges = self._get_indonesia_fallback_ranges()
        
        indonesia_mobile_isps = ["telkomsel", "indosat", "tri", "smartfren"]
        indonesia_wifi_isps = ["biznet", "indihome", "myrepublic"]
        
        if ip_type == "mobile":
            isp = random.choice(indonesia_mobile_isps)
        else:
            isp = random.choice(indonesia_wifi_isps)
        
        isp_ranges = country_ranges.get(isp, [])
        if not isp_ranges:
            isp = "telkomsel"
            isp_ranges = country_ranges.get("telkomsel", self._get_default_indonesia_ranges())
        
        selected_range = random.choice(isp_ranges)
        ip = self._generate_fresh_indonesia_ip(selected_range)
        
        self.used_ips.add(ip)
        self._ip_timestamps[ip] = time.time()
        self._ip_countries[ip] = "ID"
        
        return self._build_ultra_stealth_profile(ip, "ID", isp, selected_range)
    
    def _build_ultra_stealth_profile_for_country(self, ip: str, country: str, isp_name: str, 
                                                   isp_asn: str, country_data: Dict, ip_type: str) -> Dict[str, Any]:
        """Build complete IP profile with all fingerprints matching the country"""
        
        # Get country-specific data
        timezone = country_data.get("timezone", "America/New_York")
        language = country_data.get("language", "en-US")
        locale = country_data.get("locale", "en_US")
        country_name = country_data.get("name", country)
        
        # Get city
        cities = country_data.get("cities", [{"name": "Unknown", "lat": 0, "lon": 0}])
        city = random.choice(cities) if cities else {"name": "Unknown", "lat": 0, "lon": 0}
        
        # Get device based on type and country
        devices = country_data.get("devices", {"mobile": ["iPhone 15 Pro"], "desktop": ["MacBook Pro"]})
        if ip_type == "mobile":
            device_list = devices.get("mobile", ["iPhone 15 Pro"])
            device_type = "mobile"
        else:
            device_list = devices.get("desktop", ["MacBook Pro"])
            device_type = "desktop"
        
        selected_device = random.choice(device_list) if device_list else "iPhone 15 Pro"
        
        # Generate TCP fingerprint
        tcp_fingerprint = self._generate_tcp_fingerprint_enhanced(device_type)
        
        # Generate network metrics
        network_metrics = self._generate_network_metrics(ip_type, country)
        
        # Build device profile
        device_profile = self._generate_device_profile_for_country(selected_device, country, ip_type)
        
        return {
            "ip": ip,
            "country": country,
            "country_name": country_name,
            "isp": self._normalize_isp_name(isp_name),
            "isp_name": isp_name,
            "asn": isp_asn,
            "type": ip_type,
            "connection_type": "mobile" if ip_type == "mobile" else "wifi",
            "network_type": "4G" if ip_type == "mobile" else "WiFi",
            "health_score": random.randint(85, 99),
            "freshness_score": 100,
            "location": {
                "city": city.get("name", "Unknown"),
                "lat": city.get("lat", 0),
                "lon": city.get("lon", 0),
                "timezone": timezone
            },
            "locale": {
                "language": language,
                "locale": locale
            },
            "device": device_profile,
            "tcp_fingerprint": tcp_fingerprint,
            "network_metrics": network_metrics
        }
    
    def _verify_ip_realtime(self, ip: str) -> Dict[str, Any]:
        """Verify IP location and check if it's usable for Instagram
        
        Instagram checks:
        1. IP reputation (not blacklisted)
        2. Not datacenter/VPN/proxy
        3. Fresh/unique IP
        
        Uses multiple sources for verification:
        1. ip-api.com (primary)
        2. ipinfo.io (fallback)
        3. ipwhois.app (secondary fallback)
        """
        result = {
            "is_indonesia": False,
            "is_usable": False,
            "country": None,
            "isp": None,
            "org": None,
            "verified": False,
            "source": None,
            "is_datacenter": False,
            "is_proxy": False
        }
        
        # Source 1: ip-api.com (free, rate: 45 req/min) - includes proxy/hosting detection
        try:
            response = requests.get(
                f"http://ip-api.com/json/{ip}?fields=status,country,countryCode,isp,org,as,proxy,hosting",
                timeout=5
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get("status") == "success":
                    result["verified"] = True
                    result["country"] = data.get("countryCode")
                    result["isp"] = data.get("isp")
                    result["org"] = data.get("org")
                    result["source"] = "ip-api.com"
                    result["is_proxy"] = data.get("proxy", False)
                    result["is_datacenter"] = data.get("hosting", False)
                    
                    # Check if Indonesia
                    if data.get("countryCode") == "ID":
                        result["is_indonesia"] = True
                    
                    # IP is usable if not proxy/datacenter
                    # Note: IP 120.88.35.45 (Myanmar) worked - so non-ID IPs can work too!
                    if not result["is_proxy"] and not result["is_datacenter"]:
                        result["is_usable"] = True
                    
                    return result
                        
        except Exception as e:
            pass  # Try next source
        
        # Source 2: ipinfo.io (free tier: 50k/month)
        try:
            response = requests.get(
                f"https://ipinfo.io/{ip}/json",
                timeout=5,
                headers={"Accept": "application/json"}
            )
            
            if response.status_code == 200:
                data = response.json()
                result["verified"] = True
                result["country"] = data.get("country")
                result["isp"] = data.get("org", "").replace("AS", "").strip()
                result["org"] = data.get("org")
                result["source"] = "ipinfo.io"
                
                if data.get("country") == "ID":
                    result["is_indonesia"] = True
                
                # Assume usable if verified (ipinfo doesn't have proxy field in free tier)
                result["is_usable"] = True
                return result
                    
        except Exception as e:
            pass  # Try next source
        
        # Source 3: ipwhois.app (free, no rate limit specified)
        try:
            response = requests.get(
                f"https://ipwhois.app/json/{ip}",
                timeout=5
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success", True):
                    result["verified"] = True
                    result["country"] = data.get("country_code")
                    result["isp"] = data.get("isp")
                    result["org"] = data.get("org")
                    result["source"] = "ipwhois.app"
                    
                    if data.get("country_code") == "ID":
                        result["is_indonesia"] = True
                    
                    result["is_usable"] = True
                    return result
                        
        except Exception as e:
            pass
        
        # If all APIs fail, DON'T trust - return unverified
        result["verified"] = False
        result["is_indonesia"] = False
        result["is_usable"] = False
        
        return result
    
    def _normalize_isp_name(self, isp_name: str) -> str:
        """Normalize ISP name to our standard format"""
        isp_lower = isp_name.lower()
        
        if "telkomsel" in isp_lower or "telekomunikasi selular" in isp_lower:
            return "telkomsel"
        elif "indosat" in isp_lower or "ooredoo" in isp_lower:
            return "indosat"
        elif "xl" in isp_lower or "axiata" in isp_lower:
            return "xl"
        elif "hutchison" in isp_lower or "three" in isp_lower or "tri" in isp_lower or "3 " in isp_lower:
            return "tri"
        elif "smartfren" in isp_lower:
            return "smartfren"
        elif "biznet" in isp_lower:
            return "biznet"
        elif "link net" in isp_lower or "first media" in isp_lower or "firstmedia" in isp_lower:
            return "firstmedia"
        elif "myrepublic" in isp_lower or "eka mas" in isp_lower:
            return "myrepublic"
        elif "telkom" in isp_lower or "indihome" in isp_lower:
            return "indihome"
        elif "cbn" in isp_lower or "cyberindo" in isp_lower:
            return "cbn"
        else:
            return isp_name.lower().replace(" ", "_")[:20]
    
    def _get_indonesia_fallback_ranges(self) -> Dict[str, List[Dict]]:
        """Get VERIFIED Indonesian IP ranges from APNIC allocations
        
        These ranges are verified to belong to Indonesian ISPs based on:
        - APNIC WHOIS database
        - BGP routing tables
        - Real-world testing
        """
        return {
            # Telkomsel - PT Telekomunikasi Selular (AS7713)
            "telkomsel": [
                {"start": "114.120.0.0", "end": "114.127.255.255", "type": "mobile", "cgnat": False},  # 114.120.0.0/13
                {"start": "182.0.0.0", "end": "182.7.255.255", "type": "mobile", "cgnat": False},      # 182.0.0.0/13 (subset)
                {"start": "36.68.0.0", "end": "36.71.255.255", "type": "mobile", "cgnat": False},      # 36.68.0.0/14
                {"start": "110.136.0.0", "end": "110.139.255.255", "type": "mobile", "cgnat": False},  # 110.136.0.0/14
            ],
            # Indosat Ooredoo - PT Indosat Tbk (AS4761)
            "indosat": [
                {"start": "114.4.0.0", "end": "114.5.255.255", "type": "mobile", "cgnat": False},      # 114.4.0.0/15
                {"start": "180.252.0.0", "end": "180.253.255.255", "type": "mobile", "cgnat": False},  # 180.252.0.0/15
                {"start": "114.6.0.0", "end": "114.7.255.255", "type": "mobile", "cgnat": False},      # 114.6.0.0/15
            ],
            # XL Axiata - PT XL Axiata Tbk (AS24203)
            # NOTE: 120.88.0.0/15, 114.121.0.0/16, 114.122.0.0/15 removed - NOT Indonesia per ip-api.com
            "xl": [
                {"start": "112.215.0.0", "end": "112.215.255.255", "type": "mobile", "cgnat": False},  # 112.215.0.0/16 (VERIFIED)
            ],
            # Tri Indonesia - PT Hutchison 3 Indonesia (AS45727)
            "tri": [
                {"start": "114.79.0.0", "end": "114.79.255.255", "type": "mobile", "cgnat": False},    # 114.79.0.0/16
                {"start": "114.125.0.0", "end": "114.125.255.255", "type": "mobile", "cgnat": False},  # 114.125.0.0/16
            ],
            # Smartfren - PT Smartfren Telecom (AS18004)
            # NOTE: 112.78.0.0/15 is NOT Indonesian - removed
            "smartfren": [
                {"start": "103.10.64.0", "end": "103.10.67.255", "type": "mobile", "cgnat": False},    # 103.10.64.0/22 (VERIFIED)
                {"start": "202.67.40.0", "end": "202.67.47.255", "type": "mobile", "cgnat": False},    # 202.67.32.0/19 subset (VERIFIED)
            ],
            # Biznet - PT Biznet Gio Nusantara (AS17451)
            "biznet": [
                {"start": "103.28.52.0", "end": "103.28.55.255", "type": "residential", "cgnat": False},  # 103.28.52.0/22
                {"start": "117.102.64.0", "end": "117.102.127.255", "type": "residential", "cgnat": False}, # 117.102.64.0/18
            ],
            # First Media - PT Link Net Tbk (AS23700)
            "firstmedia": [
                {"start": "110.137.128.0", "end": "110.137.255.255", "type": "residential", "cgnat": False}, # 110.137.128.0/17
                {"start": "202.53.232.0", "end": "202.53.239.255", "type": "residential", "cgnat": False},   # 202.53.232.0/21
            ],
            # MyRepublic - PT Eka Mas Republik (AS63859)
            "myrepublic": [
                {"start": "103.19.56.0", "end": "103.19.59.255", "type": "residential", "cgnat": False},   # 103.19.56.0/22
                {"start": "103.56.148.0", "end": "103.56.151.255", "type": "residential", "cgnat": False}, # 103.56.148.0/22
            ],
            # IndiHome - PT Telkom Indonesia (AS7713)
            "indihome": [
                {"start": "180.244.0.0", "end": "180.247.255.255", "type": "residential", "cgnat": False}, # 180.244.0.0/14
                {"start": "125.160.0.0", "end": "125.163.255.255", "type": "residential", "cgnat": False}, # 125.160.0.0/14
            ],
            # CBN - PT Cyberindo Aditama (AS24218)
            "cbn": [
                {"start": "202.158.0.0", "end": "202.158.63.255", "type": "residential", "cgnat": False},  # 202.158.0.0/18
                {"start": "203.142.64.0", "end": "203.142.127.255", "type": "residential", "cgnat": False}, # 203.142.64.0/18
            ],
            
            # =====================================================
            # ASIA IP RANGES (Working IPs like 120.88.35.45 Myanmar)
            # These are backup ranges when Indonesia IPs are blocked
            # =====================================================
            
            # Myanmar - MPT, Telenor Myanmar (120.88.x.x worked!)
            "myanmar": [
                {"start": "120.88.0.0", "end": "120.91.255.255", "type": "mobile", "cgnat": False, "country": "MM"},
                {"start": "103.18.32.0", "end": "103.18.35.255", "type": "mobile", "cgnat": False, "country": "MM"},
            ],
            # Malaysia - Maxis, Celcom, Digi
            "malaysia": [
                {"start": "60.48.0.0", "end": "60.55.255.255", "type": "mobile", "cgnat": False, "country": "MY"},
                {"start": "175.136.0.0", "end": "175.143.255.255", "type": "mobile", "cgnat": False, "country": "MY"},
                {"start": "113.210.0.0", "end": "113.213.255.255", "type": "mobile", "cgnat": False, "country": "MY"},
            ],
            # Thailand - AIS, DTAC, True
            "thailand": [
                {"start": "171.96.0.0", "end": "171.99.255.255", "type": "mobile", "cgnat": False, "country": "TH"},
                {"start": "49.228.0.0", "end": "49.231.255.255", "type": "mobile", "cgnat": False, "country": "TH"},
                {"start": "223.24.0.0", "end": "223.27.255.255", "type": "mobile", "cgnat": False, "country": "TH"},
            ],
            # Vietnam - Viettel, VNPT, Mobifone
            "vietnam": [
                {"start": "113.160.0.0", "end": "113.191.255.255", "type": "mobile", "cgnat": False, "country": "VN"},
                {"start": "115.72.0.0", "end": "115.79.255.255", "type": "mobile", "cgnat": False, "country": "VN"},
                {"start": "14.160.0.0", "end": "14.191.255.255", "type": "mobile", "cgnat": False, "country": "VN"},
            ],
            # Philippines - Globe, Smart, PLDT
            "philippines": [
                {"start": "112.198.0.0", "end": "112.199.255.255", "type": "mobile", "cgnat": False, "country": "PH"},
                {"start": "119.92.0.0", "end": "119.95.255.255", "type": "mobile", "cgnat": False, "country": "PH"},
                {"start": "49.144.0.0", "end": "49.159.255.255", "type": "mobile", "cgnat": False, "country": "PH"},
            ],
            # Singapore - Singtel, StarHub, M1
            "singapore": [
                {"start": "116.14.0.0", "end": "116.15.255.255", "type": "mobile", "cgnat": False, "country": "SG"},
                {"start": "219.74.0.0", "end": "219.75.255.255", "type": "mobile", "cgnat": False, "country": "SG"},
            ]
        }
    
    def _get_default_indonesia_ranges(self) -> List[Dict]:
        """Get default Indonesia IP ranges"""
        return [
            {"start": "114.120.0.0", "end": "114.127.255.255", "type": "mobile", "cgnat": False},
            {"start": "182.0.0.0", "end": "182.15.255.255", "type": "mobile", "cgnat": False},
        ]
    
    def _generate_validated_indonesia_ip(self, range_info: Dict) -> str:
        """Generate and validate Indonesian IP"""
        ip = self._generate_ip_from_range(range_info)
        
        # Basic validation - ensure it's not a reserved IP
        parts = [int(x) for x in ip.split(".")]
        
        # Avoid broadcast and network addresses
        if parts[3] == 0 or parts[3] == 255:
            parts[3] = random.randint(10, 245)
        
        # Avoid common server IPs
        if parts[3] in [1, 2, 254]:
            parts[3] = random.randint(10, 245)
        
        return ".".join(str(p) for p in parts)
    
    def _generate_fresh_indonesia_ip(self, range_info: Dict) -> str:
        """Generate fresh Indonesia IP with anti-blacklist randomization
        
        Uses timestamp-seeded randomization to avoid predictable patterns
        that might be blacklisted
        """
        # Get base IP from validated range
        base_ip = self._generate_validated_indonesia_ip(range_info)
        parts = [int(x) for x in base_ip.split(".")]
        
        # Add timestamp-based entropy to last 2 octets for freshness
        timestamp_entropy = int(time.time() * 1000) % 100
        random_entropy = random.randint(1, 50)
        
        # Modify third octet slightly (stay in valid range)
        start_parts = [int(x) for x in range_info["start"].split(".")]
        end_parts = [int(x) for x in range_info["end"].split(".")]
        
        if start_parts[2] != end_parts[2]:
            new_third = start_parts[2] + (timestamp_entropy % (end_parts[2] - start_parts[2] + 1))
            parts[2] = max(start_parts[2], min(end_parts[2], new_third))
        
        # Randomize last octet avoiding common patterns
        avoid_patterns = {0, 1, 2, 100, 128, 200, 254, 255}
        # Add previously used last octets for this /24
        prefix = f"{parts[0]}.{parts[1]}.{parts[2]}"
        for used_ip in self.used_ips:
            if used_ip.startswith(prefix):
                try:
                    avoid_patterns.add(int(used_ip.split(".")[3]))
                except:
                    pass
        
        # Generate unique last octet
        valid_octets = [x for x in range(10, 250) if x not in avoid_patterns]
        if valid_octets:
            parts[3] = random.choice(valid_octets) + (random_entropy % 5)
            parts[3] = max(10, min(249, parts[3]))
        else:
            parts[3] = random.randint(20, 230)
        
        return ".".join(str(p) for p in parts)
    
    def _generate_ip_from_range(self, range_info: Dict) -> str:
        """Generate IP from a specific range with residential-like patterns"""
        start_parts = [int(x) for x in range_info["start"].split(".")]
        end_parts = [int(x) for x in range_info["end"].split(".")]
        
        # Generate each octet within range
        octets = []
        for i in range(4):
            if start_parts[i] == end_parts[i]:
                octets.append(start_parts[i])
            else:
                # For the last octet, use residential-like distribution
                if i == 3:
                    octet = self._generate_residential_octet(start_parts[i], end_parts[i])
                else:
                    octet = random.randint(start_parts[i], end_parts[i])
                octets.append(octet)
        
        return ".".join(str(o) for o in octets)
    
    def _generate_residential_octet(self, min_val: int, max_val: int) -> int:
        """Generate last octet with residential-like distribution"""
        # Avoid values that look like servers
        avoid_values = set([0, 1, 2, 254, 255])  # Gateway/broadcast
        avoid_values.update([x for x in range(min_val, max_val+1) if x % 10 == 0])  # Round numbers
        avoid_values.update([x for x in range(min_val, max_val+1) if x % 50 == 0])
        avoid_values.update([100, 128, 200])  # Common server IPs
        
        valid_range = [x for x in range(max(11, min_val), min(249, max_val)+1) if x not in avoid_values]
        
        if not valid_range:
            valid_range = list(range(max(11, min_val), min(249, max_val)+1))
        
        # Use weighted distribution - middle values more common
        mid = len(valid_range) // 2
        weights = [1 + (mid - abs(i - mid)) * 0.1 for i in range(len(valid_range))]
        
        return random.choices(valid_range, weights=weights, k=1)[0]
    
    def _build_ultra_stealth_profile(self, ip: str, country: str, isp: str, range_info: Dict) -> Dict[str, Any]:
        """Build complete ultra-stealth IP profile"""
        
        # Get country-specific data
        country_data = self._get_country_data(country)
        isp_data = self._get_isp_data(country, isp)
        
        # Generate realistic timestamps
        current_time = time.time()
        lease_start = current_time - random.randint(300, 86400)  # 5 min to 1 day ago
        lease_duration = random.choice([3600, 7200, 14400, 28800, 86400])  # Common DHCP lease times
        
        ip_type = range_info.get("type", "residential")
        # Always use WiFi/broadband for Desktop Web API
        is_mobile = False
        
        # Generate location within country
        location = self._generate_location(country, isp_data)
        
        return {
            "ip": ip,
            "type": ip_type,
            "country": country,
            "country_name": country_data["name"],
            "isp": isp,
            "isp_name": isp_data.get("name", isp),
            "asn": isp_data.get("asn", "AS0"),
            "as_name": isp_data.get("as_name", ""),
            "connection_type": "wifi",  # Always WiFi for Desktop
            "network_type": "WiFi",  # Always WiFi for Desktop
            "cgnat": range_info.get("cgnat", False),
            "location": location,
            "language": country_data["language"],
            "timezone": country_data["timezone"],
            "locale": country_data["locale"],
            
            # DHCP simulation
            "dhcp": {
                "lease_start": lease_start,
                "lease_duration": lease_duration,
                "lease_remaining": lease_duration - (current_time - lease_start),
                "server": f"{'.'.join(ip.split('.')[:3])}.1",
            },
            
            # Network metrics - realistic for connection type
            "network_metrics": self._generate_network_metrics(ip_type, country),
            
            # TCP/IP fingerprint
            "tcp_fingerprint": self._generate_tcp_fingerprint(is_mobile),
            
            # Device fingerprint
            "device": self._generate_device_fingerprint(country, is_mobile),
            
            # Meta
            "generated_at": current_time,
            "generation_method": "ultra_stealth_v2",
            "health_score": random.randint(90, 99),
            "trust_score": random.uniform(0.92, 0.99),
            "usage_count": 0,
            "last_used": None,
        }
    
    def _get_country_data(self, country: str) -> Dict[str, Any]:
        """Get country-specific data for fingerprint matching"""
        country_map = {
            # Asia
            "ID": {"name": "Indonesia", "language": "id-ID", "timezone": "Asia/Jakarta", "locale": "id_ID"},
            "MY": {"name": "Malaysia", "language": "ms-MY", "timezone": "Asia/Kuala_Lumpur", "locale": "ms_MY"},
            "SG": {"name": "Singapore", "language": "en-SG", "timezone": "Asia/Singapore", "locale": "en_SG"},
            "TH": {"name": "Thailand", "language": "th-TH", "timezone": "Asia/Bangkok", "locale": "th_TH"},
            "VN": {"name": "Vietnam", "language": "vi-VN", "timezone": "Asia/Ho_Chi_Minh", "locale": "vi_VN"},
            "PH": {"name": "Philippines", "language": "en-PH", "timezone": "Asia/Manila", "locale": "en_PH"},
            "MM": {"name": "Myanmar", "language": "my-MM", "timezone": "Asia/Yangon", "locale": "my_MM"},
            "KH": {"name": "Cambodia", "language": "km-KH", "timezone": "Asia/Phnom_Penh", "locale": "km_KH"},
            "LA": {"name": "Laos", "language": "lo-LA", "timezone": "Asia/Vientiane", "locale": "lo_LA"},
            "BD": {"name": "Bangladesh", "language": "bn-BD", "timezone": "Asia/Dhaka", "locale": "bn_BD"},
            "IN": {"name": "India", "language": "hi-IN", "timezone": "Asia/Kolkata", "locale": "hi_IN"},
            "PK": {"name": "Pakistan", "language": "ur-PK", "timezone": "Asia/Karachi", "locale": "ur_PK"},
            "JP": {"name": "Japan", "language": "ja-JP", "timezone": "Asia/Tokyo", "locale": "ja_JP"},
            "KR": {"name": "South Korea", "language": "ko-KR", "timezone": "Asia/Seoul", "locale": "ko_KR"},
            "CN": {"name": "China", "language": "zh-CN", "timezone": "Asia/Shanghai", "locale": "zh_CN"},
            "TW": {"name": "Taiwan", "language": "zh-TW", "timezone": "Asia/Taipei", "locale": "zh_TW"},
            "HK": {"name": "Hong Kong", "language": "zh-HK", "timezone": "Asia/Hong_Kong", "locale": "zh_HK"},
            # Americas
            "US": {"name": "United States", "language": "en-US", "timezone": "America/New_York", "locale": "en_US"},
            "CA": {"name": "Canada", "language": "en-CA", "timezone": "America/Toronto", "locale": "en_CA"},
            "BR": {"name": "Brazil", "language": "pt-BR", "timezone": "America/Sao_Paulo", "locale": "pt_BR"},
            "MX": {"name": "Mexico", "language": "es-MX", "timezone": "America/Mexico_City", "locale": "es_MX"},
            "AR": {"name": "Argentina", "language": "es-AR", "timezone": "America/Buenos_Aires", "locale": "es_AR"},
            # Europe
            "UK": {"name": "United Kingdom", "language": "en-GB", "timezone": "Europe/London", "locale": "en_GB"},
            "GB": {"name": "United Kingdom", "language": "en-GB", "timezone": "Europe/London", "locale": "en_GB"},
            "DE": {"name": "Germany", "language": "de-DE", "timezone": "Europe/Berlin", "locale": "de_DE"},
            "FR": {"name": "France", "language": "fr-FR", "timezone": "Europe/Paris", "locale": "fr_FR"},
            "IT": {"name": "Italy", "language": "it-IT", "timezone": "Europe/Rome", "locale": "it_IT"},
            "ES": {"name": "Spain", "language": "es-ES", "timezone": "Europe/Madrid", "locale": "es_ES"},
            "NL": {"name": "Netherlands", "language": "nl-NL", "timezone": "Europe/Amsterdam", "locale": "nl_NL"},
            "RU": {"name": "Russia", "language": "ru-RU", "timezone": "Europe/Moscow", "locale": "ru_RU"},
            # Oceania
            "AU": {"name": "Australia", "language": "en-AU", "timezone": "Australia/Sydney", "locale": "en_AU"},
            "NZ": {"name": "New Zealand", "language": "en-NZ", "timezone": "Pacific/Auckland", "locale": "en_NZ"},
        }
        return country_map.get(country, country_map.get("ID"))  # Default to Indonesia
    
    def _get_isp_data(self, country: str, isp: str) -> Dict[str, Any]:
        """Get ISP-specific data"""
        isp_data = {
            "US": {
                "verizon_wireless": {"name": "Verizon Wireless", "asn": "AS22394", "as_name": "Verizon Wireless"},
                "att_wireless": {"name": "AT&T Wireless", "asn": "AS20057", "as_name": "AT&T Mobility"},
                "tmobile": {"name": "T-Mobile", "asn": "AS21928", "as_name": "T-Mobile USA"},
                "comcast": {"name": "Comcast", "asn": "AS7922", "as_name": "Comcast Cable Communications"},
                "spectrum": {"name": "Spectrum", "asn": "AS11351", "as_name": "Charter Communications"},
                "cox": {"name": "Cox Communications", "asn": "AS22773", "as_name": "Cox Communications Inc."},
            },
            "AU": {
                "telstra": {"name": "Telstra", "asn": "AS1221", "as_name": "Telstra Corporation Ltd"},
                "optus": {"name": "Optus", "asn": "AS4804", "as_name": "Optus Mobile"},
                "vodafone_au": {"name": "Vodafone AU", "asn": "AS133612", "as_name": "Vodafone Australia"},
                "tpg": {"name": "TPG", "asn": "AS7545", "as_name": "TPG Telecom Limited"},
            },
            "CA": {
                "rogers": {"name": "Rogers", "asn": "AS812", "as_name": "Rogers Communications Canada Inc."},
                "bell": {"name": "Bell Canada", "asn": "AS577", "as_name": "Bell Canada"},
                "telus": {"name": "TELUS", "asn": "AS852", "as_name": "TELUS Communications Inc."},
            },
            "UK": {
                "bt": {"name": "BT", "asn": "AS2856", "as_name": "British Telecommunications PLC"},
                "ee": {"name": "EE", "asn": "AS12576", "as_name": "EE Limited"},
                "vodafone_uk": {"name": "Vodafone UK", "asn": "AS25135", "as_name": "Vodafone UK"},
                "sky": {"name": "Sky UK", "asn": "AS5607", "as_name": "Sky UK Limited"},
            },
            "DE": {
                "telekom_de": {"name": "Deutsche Telekom", "asn": "AS3320", "as_name": "Deutsche Telekom AG"},
                "vodafone_de": {"name": "Vodafone Germany", "asn": "AS3209", "as_name": "Vodafone GmbH"},
                "o2_de": {"name": "O2 Germany", "asn": "AS8422", "as_name": "O2 (Germany) GmbH & Co. OHG"},
            },
            "FR": {
                "orange_fr": {"name": "Orange France", "asn": "AS3215", "as_name": "Orange S.A."},
                "sfr": {"name": "SFR", "asn": "AS15557", "as_name": "SFR SA"},
                "free_fr": {"name": "Free", "asn": "AS12322", "as_name": "Free SAS"},
            },
            "JP": {
                "ntt_docomo": {"name": "NTT Docomo", "asn": "AS9605", "as_name": "NTT DOCOMO, INC."},
                "softbank": {"name": "SoftBank", "asn": "AS17676", "as_name": "SoftBank Corp."},
                "au_kddi": {"name": "AU KDDI", "asn": "AS2516", "as_name": "KDDI CORPORATION"},
            },
            "SG": {
                "singtel": {"name": "Singtel", "asn": "AS7473", "as_name": "Singapore Telecommunications Ltd"},
                "starhub": {"name": "StarHub", "asn": "AS4657", "as_name": "StarHub Ltd"},
            },
            "NL": {
                "kpn": {"name": "KPN", "asn": "AS1136", "as_name": "KPN B.V."},
                "vodafone_nl": {"name": "Vodafone NL", "asn": "AS1103", "as_name": "Vodafone Libertel B.V."},
            },
        }
        return isp_data.get(country, {}).get(isp, {"name": isp, "asn": "AS0", "as_name": ""})
    
    def _generate_location(self, country: str, isp_data: Dict) -> Dict[str, Any]:
        """Generate realistic location within country"""
        cities = {
            "US": [
                ("New York", 40.7128, -74.0060), ("Los Angeles", 34.0522, -118.2437),
                ("Chicago", 41.8781, -87.6298), ("Houston", 29.7604, -95.3698),
                ("Phoenix", 33.4484, -112.0740), ("Philadelphia", 39.9526, -75.1652),
                ("San Antonio", 29.4241, -98.4936), ("San Diego", 32.7157, -117.1611),
                ("Dallas", 32.7767, -96.7970), ("San Jose", 37.3382, -121.8863),
            ],
            "AU": [
                ("Sydney", -33.8688, 151.2093), ("Melbourne", -37.8136, 144.9631),
                ("Brisbane", -27.4698, 153.0251), ("Perth", -31.9505, 115.8605),
                ("Adelaide", -34.9285, 138.6007),
            ],
            "CA": [
                ("Toronto", 43.6532, -79.3832), ("Vancouver", 49.2827, -123.1207),
                ("Montreal", 45.5017, -73.5673), ("Calgary", 51.0447, -114.0719),
            ],
            "UK": [
                ("London", 51.5074, -0.1278), ("Manchester", 53.4808, -2.2426),
                ("Birmingham", 52.4862, -1.8904), ("Glasgow", 55.8642, -4.2518),
            ],
            "DE": [
                ("Berlin", 52.5200, 13.4050), ("Munich", 48.1351, 11.5820),
                ("Hamburg", 53.5511, 9.9937), ("Frankfurt", 50.1109, 8.6821),
            ],
            "FR": [
                ("Paris", 48.8566, 2.3522), ("Lyon", 45.7640, 4.8357),
                ("Marseille", 43.2965, 5.3698), ("Toulouse", 43.6047, 1.4442),
            ],
            "JP": [
                ("Tokyo", 35.6762, 139.6503), ("Osaka", 34.6937, 135.5023),
                ("Nagoya", 35.1815, 136.9066), ("Yokohama", 35.4437, 139.6380),
            ],
            "SG": [("Singapore", 1.3521, 103.8198)],
            "NL": [
                ("Amsterdam", 52.3676, 4.9041), ("Rotterdam", 51.9244, 4.4777),
                ("The Hague", 52.0705, 4.3007),
            ],
        }
        
        city_list = cities.get(country, cities["US"])
        city_name, lat, lon = random.choice(city_list)
        
        # Add slight variation to coordinates (within ~1km)
        lat += random.uniform(-0.01, 0.01)
        lon += random.uniform(-0.01, 0.01)
        
        return {
            "city": city_name,
            "country": country,
            "latitude": round(lat, 6),
            "longitude": round(lon, 6),
            "accuracy": random.randint(50, 500),
        }
    
    def _generate_network_metrics(self, ip_type: str, country: str) -> Dict[str, Any]:
        """Generate realistic network metrics based on connection type and location"""
        
        # Base latency by region (to US Instagram servers)
        base_latency = {
            "US": (10, 40), "CA": (20, 50), "UK": (80, 120), "DE": (90, 130),
            "FR": (85, 125), "AU": (150, 200), "JP": (100, 150), "SG": (120, 170), "NL": (75, 115),
        }
        
        lat_range = base_latency.get(country, (50, 100))
        
        if ip_type == "mobile":
            return {
                "latency_ms": random.uniform(lat_range[0] + 20, lat_range[1] + 40),
                "jitter_ms": random.uniform(5, 20),
                "packet_loss_percent": random.uniform(0.1, 1.0),
                "bandwidth_mbps": random.uniform(20, 150),
                "signal_strength": random.randint(-85, -50),
            }
        else:
            return {
                "latency_ms": random.uniform(lat_range[0], lat_range[1]),
                "jitter_ms": random.uniform(1, 8),
                "packet_loss_percent": random.uniform(0, 0.3),
                "bandwidth_mbps": random.uniform(100, 1000),
                "signal_strength": random.randint(-40, -20),
            }
    
    def _generate_tcp_fingerprint(self, is_mobile: bool) -> Dict[str, Any]:
        """Generate realistic TCP/IP fingerprint"""
        if is_mobile:
            return {
                "ttl": random.choice([64, 63, 62, 61]),
                "window_size": random.choice([65535, 64240, 32768]),
                "mss": random.choice([1400, 1380, 1360]),
                "window_scaling": random.randint(6, 10),
                "timestamps": True,
                "sack_permitted": True,
            }
        else:
            return {
                "ttl": random.choice([64, 128, 127, 63]),
                "window_size": random.choice([65535, 64240, 65520]),
                "mss": random.choice([1460, 1440, 1452]),
                "window_scaling": random.randint(7, 14),
                "timestamps": True,
                "sack_permitted": True,
            }
    
    def _generate_tcp_fingerprint_enhanced(self, device_type: str) -> Dict[str, Any]:
        """Generate enhanced TCP fingerprint based on device type"""
        is_mobile = device_type in ["mobile", "android", "ios"]
        base = self._generate_tcp_fingerprint(is_mobile)
        
        # Add enhanced TCP/IP stack properties
        base.update({
            "ecn": random.choice([True, False]) if not is_mobile else False,
            "sack_ok": True,
            "nop": True,
            "tcp_options_order": ["mss", "nop", "window_scale", "nop", "nop", "timestamp", "sack_permitted"],
            "ip_id_pattern": random.choice(["incremental", "random", "zero"]),
            "df_flag": True,
            "tos": 0,
            "tcp_seq_pattern": "random",
            "tcp_ack_behavior": "delayed",
            "urgent_pointer": 0,
            "checksum_offload": True,
        })
        
        return base
    
    def _generate_device_fingerprint(self, country: str, is_mobile: bool) -> Dict[str, Any]:
        """Generate device fingerprint based on country and connection type"""
        
        if is_mobile:
            # Popular phones by country
            phones = {
                "US": ["iPhone 15 Pro Max", "iPhone 15 Pro", "iPhone 14 Pro", "Samsung Galaxy S24 Ultra", "Pixel 8 Pro"],
                "AU": ["iPhone 15 Pro Max", "iPhone 14 Pro", "Samsung Galaxy S24", "Pixel 8"],
                "CA": ["iPhone 15 Pro", "iPhone 14", "Samsung Galaxy S24 Ultra", "Pixel 8 Pro"],
                "UK": ["iPhone 15 Pro Max", "iPhone 14 Pro", "Samsung Galaxy S24", "Pixel 8"],
                "DE": ["iPhone 15 Pro", "Samsung Galaxy S24", "Xiaomi 14", "Pixel 8"],
                "FR": ["iPhone 15 Pro Max", "Samsung Galaxy S24 Ultra", "Xiaomi 14 Pro"],
                "JP": ["iPhone 15 Pro Max", "iPhone 15", "Xperia 1 V", "AQUOS R8"],
                "SG": ["iPhone 15 Pro Max", "Samsung Galaxy S24 Ultra", "Xiaomi 14"],
                "NL": ["iPhone 15 Pro", "Samsung Galaxy S24", "Pixel 8"],
            }
            
            device = random.choice(phones.get(country, phones["US"]))
            
            if "iPhone" in device:
                return {
                    "type": "mobile",
                    "model": device,
                    "os": "iOS",
                    "os_version": random.choice(["17.4", "17.3", "17.2", "17.1"]),
                    "browser": "Safari",
                    "browser_version": random.choice(["17.4", "17.3", "17.2"]),
                }
            else:
                return {
                    "type": "mobile",
                    "model": device,
                    "os": "Android",
                    "os_version": random.choice(["14", "13", "12"]),
                    "browser": "Chrome",
                    "browser_version": random.choice(["122.0.6261", "121.0.6167", "120.0.6099"]),
                }
        else:
            # Desktop browsers
            return {
                "type": "desktop",
                "os": random.choice(["Windows", "macOS"]),
                "os_version": random.choice(["11", "10"]) if random.random() > 0.4 else random.choice(["14.4", "14.3", "13.6"]),
                "browser": "Chrome",
                "browser_version": random.choice(["122.0.6261.112", "121.0.6167.160", "120.0.6099.224"]),
            }


# ===================== ADVANCED IP SPOOFING 2025 - INDONESIA ONLY =====================

class AdvancedIPStealthSystem2025:
    """Sistem IP stealth dinamis 2025 - INDONESIA ONLY dengan real-time validation"""
    
    def __init__(self):
        self.ip_pool = []
        self.blacklisted_ips = set()
        self.ip_sources = self._initialize_indonesia_ip_sources()
        self.validator = IPValidator2025()
        self.generation_cache = {}
        self.cache_ttl = 300
        self.session_ip_map = {}
        self._recently_used_ips = {}  # Track recently used IPs with timestamps
        
        # Complete Indonesia ISP Database
        self.indonesia_isps = self._load_complete_indonesia_isps()
        
        # Complete Indonesia Device Database
        self.indonesia_devices = self._load_complete_indonesia_devices()

    def _load_complete_indonesia_isps(self) -> Dict[str, Any]:
        """Load complete Indonesian ISP database"""
        return {
            # ===== MOBILE OPERATORS =====
            "telkomsel": {
                "name": "Telkomsel",
                "full_name": "PT Telekomunikasi Selular",
                "type": "mobile",
                "asn": "AS7713",
                "mcc": "510", "mnc": "10",
                "network_types": ["5G", "4G LTE", "3G"],
                "ip_ranges": [
                    "114.120.0.0/13", "114.124.0.0/14", "182.0.0.0/12",
                    "36.64.0.0/11", "36.80.0.0/12", "110.136.0.0/13",
                    "118.136.0.0/14", "118.137.0.0/16", "139.192.0.0/11"
                ],
                "prefixes": ["0811", "0812", "0813", "0821", "0822", "0823", "0851", "0852", "0853"]
            },
            "indosat": {
                "name": "Indosat Ooredoo Hutchison",
                "full_name": "PT Indosat Tbk",
                "type": "mobile",
                "asn": "AS4761",
                "mcc": "510", "mnc": "21",
                "network_types": ["4G LTE", "3G"],
                "ip_ranges": [
                    "114.0.0.0/13", "114.4.0.0/14", "180.240.0.0/12",
                    "202.152.0.0/14", "125.160.0.0/12", "112.215.0.0/16"
                ],
                "prefixes": ["0814", "0815", "0816", "0855", "0856", "0857", "0858"]
            },
            "xl": {
                "name": "XL Axiata",
                "full_name": "PT XL Axiata Tbk",
                "type": "mobile",
                "asn": "AS24203",
                "mcc": "510", "mnc": "11",
                "network_types": ["4G LTE", "3G"],
                "ip_ranges": [
                    "112.215.0.0/16"
                ],
                "prefixes": ["0817", "0818", "0819", "0859", "0877", "0878"]
            },
            "tri": {
                "name": "Tri Indonesia",
                "full_name": "PT Hutchison 3 Indonesia",
                "type": "mobile",
                "asn": "AS45727",
                "mcc": "510", "mnc": "89",
                "network_types": ["4G LTE", "3G"],
                "ip_ranges": [
                    "114.79.0.0/16", "182.253.0.0/16", "114.142.0.0/16",
                    "114.125.0.0/16"
                ],
                "prefixes": ["0895", "0896", "0897", "0898", "0899"]
            },
            "smartfren": {
                "name": "Smartfren",
                "full_name": "PT Smartfren Telecom Tbk",
                "type": "mobile",
                "asn": "AS18004",
                "mcc": "510", "mnc": "28",
                "network_types": ["4G LTE"],
                "ip_ranges": [
                    "202.67.32.0/19", "103.10.64.0/22"
                ],
                "prefixes": ["0881", "0882", "0883", "0884", "0885", "0886", "0887", "0888", "0889"]
            },
            "axis": {
                "name": "Axis",
                "full_name": "PT Axis Telekom Indonesia (XL Group)",
                "type": "mobile",
                "asn": "AS24203",
                "mcc": "510", "mnc": "11",
                "network_types": ["4G LTE", "3G"],
                "ip_ranges": ["112.215.0.0/16"],
                "prefixes": ["0831", "0832", "0833", "0838"]
            },
            "by.u": {
                "name": "by.U",
                "full_name": "PT Telekomunikasi Selular (Digital Brand)",
                "type": "mobile",
                "asn": "AS7713",
                "mcc": "510", "mnc": "10",
                "network_types": ["4G LTE"],
                "ip_ranges": ["114.120.0.0/13"],
                "prefixes": ["0851"]
            },
            
            # ===== BROADBAND/FIBER ISPs =====
            "biznet": {
                "name": "Biznet",
                "full_name": "PT Biznet Gio Nusantara",
                "type": "fiber",
                "asn": "AS17451",
                "network_types": ["Fiber", "WiFi"],
                "ip_ranges": [
                    "103.28.52.0/22", "202.169.32.0/19", "118.99.0.0/16",
                    "103.78.0.0/16", "117.102.0.0/16", "182.253.0.0/17"
                ]
            },
            "firstmedia": {
                "name": "First Media",
                "full_name": "PT Link Net Tbk",
                "type": "cable",
                "asn": "AS23700",
                "network_types": ["Cable", "WiFi"],
                "ip_ranges": [
                    "202.53.232.0/21", "110.137.0.0/16", "202.158.0.0/17"
                ]
            },
            "myrepublic": {
                "name": "MyRepublic",
                "full_name": "PT Eka Mas Republik",
                "type": "fiber",
                "asn": "AS63859",
                "network_types": ["Fiber", "WiFi"],
                "ip_ranges": [
                    "103.19.56.0/22", "103.247.8.0/22", "103.56.148.0/22"
                ]
            },
            "indihome": {
                "name": "IndiHome",
                "full_name": "PT Telkom Indonesia (IndiHome)",
                "type": "fiber",
                "asn": "AS7713",
                "network_types": ["Fiber", "WiFi"],
                "ip_ranges": [
                    "114.120.0.0/13", "180.244.0.0/14", "110.136.0.0/13",
                    "125.160.0.0/12", "182.0.0.0/12"
                ]
            },
            "cbn": {
                "name": "CBN",
                "full_name": "PT Cyberindo Aditama",
                "type": "fiber",
                "asn": "AS24218",
                "network_types": ["Fiber", "WiFi"],
                "ip_ranges": ["202.158.0.0/17", "203.142.64.0/18"]
            },
            "mncplay": {
                "name": "MNC Play",
                "full_name": "PT MNC Kabel Mediacom",
                "type": "cable",
                "asn": "AS38320",
                "network_types": ["Cable", "WiFi"],
                "ip_ranges": ["103.3.60.0/22", "202.62.16.0/20"]
            },
            "iconnet": {
                "name": "Icon+",
                "full_name": "PT Indonesia Comnets Plus",
                "type": "fiber",
                "asn": "AS7597",
                "network_types": ["Fiber", "WiFi"],
                "ip_ranges": ["202.169.224.0/19"]
            },
            "oxygen": {
                "name": "Oxygen",
                "full_name": "PT Mora Telematika Indonesia",
                "type": "fiber",
                "asn": "AS23947",
                "network_types": ["Fiber", "WiFi"],
                "ip_ranges": ["103.31.232.0/22"]
            }
        }
    
    def _load_complete_indonesia_devices(self) -> Dict[str, List[Dict]]:
        """Load complete Indonesian popular devices database"""
        return {
            "samsung": [
                {"model": "SM-S928B", "name": "Galaxy S24 Ultra", "android": "14", "year": 2024},
                {"model": "SM-S918B", "name": "Galaxy S23 Ultra", "android": "14", "year": 2023},
                {"model": "SM-S908B", "name": "Galaxy S22 Ultra", "android": "14", "year": 2022},
                {"model": "SM-A546E", "name": "Galaxy A54 5G", "android": "14", "year": 2023},
                {"model": "SM-A346E", "name": "Galaxy A34 5G", "android": "14", "year": 2023},
                {"model": "SM-A145F", "name": "Galaxy A14", "android": "13", "year": 2023},
                {"model": "SM-A047F", "name": "Galaxy A04s", "android": "12", "year": 2022},
                {"model": "SM-M146B", "name": "Galaxy M14 5G", "android": "13", "year": 2023},
                {"model": "SM-M346B", "name": "Galaxy M34 5G", "android": "13", "year": 2023},
                {"model": "SM-G998B", "name": "Galaxy S21 Ultra", "android": "14", "year": 2021},
            ],
            "xiaomi": [
                {"model": "23113RKC6G", "name": "Xiaomi 14 Pro", "android": "14", "year": 2024},
                {"model": "23078RKD5C", "name": "Xiaomi 13T Pro", "android": "14", "year": 2023},
                {"model": "2210132G", "name": "Xiaomi 12T Pro", "android": "13", "year": 2022},
                {"model": "22071219CG", "name": "Redmi Note 12 Pro", "android": "13", "year": 2023},
                {"model": "23076RA4BC", "name": "Redmi Note 12", "android": "13", "year": 2023},
                {"model": "22101316G", "name": "Redmi 12", "android": "13", "year": 2023},
                {"model": "2201117TG", "name": "Redmi Note 11", "android": "12", "year": 2022},
                {"model": "23028RA60L", "name": "POCO X5 Pro", "android": "13", "year": 2023},
                {"model": "22101320G", "name": "POCO M5", "android": "12", "year": 2022},
            ],
            "oppo": [
                {"model": "CPH2573", "name": "OPPO Find X7", "android": "14", "year": 2024},
                {"model": "CPH2519", "name": "OPPO Reno 10 Pro+", "android": "13", "year": 2023},
                {"model": "CPH2531", "name": "OPPO Reno 10", "android": "13", "year": 2023},
                {"model": "CPH2585", "name": "OPPO A78 5G", "android": "13", "year": 2023},
                {"model": "CPH2565", "name": "OPPO A58", "android": "13", "year": 2023},
                {"model": "CPH2505", "name": "OPPO A17", "android": "12", "year": 2022},
                {"model": "CPH2477", "name": "OPPO A57", "android": "12", "year": 2022},
            ],
            "vivo": [
                {"model": "V2303A", "name": "Vivo X100", "android": "14", "year": 2024},
                {"model": "V2254", "name": "Vivo V29", "android": "13", "year": 2023},
                {"model": "V2219", "name": "Vivo V27", "android": "13", "year": 2023},
                {"model": "V2203", "name": "Vivo Y36", "android": "13", "year": 2023},
                {"model": "V2120", "name": "Vivo Y22", "android": "12", "year": 2022},
                {"model": "V2111", "name": "Vivo Y21", "android": "11", "year": 2021},
            ],
            "realme": [
                {"model": "RMX3771", "name": "Realme 11 Pro+", "android": "13", "year": 2023},
                {"model": "RMX3761", "name": "Realme 11", "android": "13", "year": 2023},
                {"model": "RMX3630", "name": "Realme C55", "android": "13", "year": 2023},
                {"model": "RMX3624", "name": "Realme C53", "android": "13", "year": 2023},
                {"model": "RMX3516", "name": "Realme 10", "android": "12", "year": 2022},
                {"model": "RMX3491", "name": "Realme C35", "android": "11", "year": 2022},
            ],
            "infinix": [
                {"model": "X6831", "name": "Infinix Note 30 Pro", "android": "13", "year": 2023},
                {"model": "X6711", "name": "Infinix Hot 30", "android": "13", "year": 2023},
                {"model": "X6525", "name": "Infinix Smart 7", "android": "12", "year": 2023},
                {"model": "X670", "name": "Infinix Note 12", "android": "12", "year": 2022},
            ],
            "asus": [
                {"model": "AI2302", "name": "ASUS ROG Phone 8", "android": "14", "year": 2024},
                {"model": "AI2201", "name": "ASUS ROG Phone 7", "android": "13", "year": 2023},
                {"model": "ASUS_I006D", "name": "ASUS Zenfone 9", "android": "13", "year": 2022},
            ],
            "google": [
                {"model": "Pixel 8 Pro", "name": "Google Pixel 8 Pro", "android": "14", "year": 2023},
                {"model": "Pixel 8", "name": "Google Pixel 8", "android": "14", "year": 2023},
                {"model": "Pixel 7 Pro", "name": "Google Pixel 7 Pro", "android": "14", "year": 2022},
                {"model": "Pixel 7", "name": "Google Pixel 7", "android": "14", "year": 2022},
            ],
            # Desktop devices for WiFi/Fiber users
            "windows_laptop": [
                {"model": "Dell XPS 15", "brand": "Dell", "os": "Windows 11", "year": 2023},
                {"model": "HP Spectre x360", "brand": "HP", "os": "Windows 11", "year": 2023},
                {"model": "Lenovo ThinkPad X1 Carbon", "brand": "Lenovo", "os": "Windows 11", "year": 2023},
                {"model": "ASUS ZenBook Pro", "brand": "ASUS", "os": "Windows 11", "year": 2023},
                {"model": "Acer Swift 5", "brand": "Acer", "os": "Windows 11", "year": 2023},
                {"model": "MSI Prestige 14", "brand": "MSI", "os": "Windows 11", "year": 2023},
            ],
            "macbook": [
                {"model": "MacBookPro18,1", "name": "MacBook Pro 16 M3 Pro", "os": "macOS 14", "year": 2023},
                {"model": "MacBookPro17,1", "name": "MacBook Pro 14 M3", "os": "macOS 14", "year": 2023},
                {"model": "MacBookAir10,1", "name": "MacBook Air M2", "os": "macOS 14", "year": 2022},
                {"model": "Mac14,2", "name": "MacBook Air 15 M2", "os": "macOS 14", "year": 2023},
            ]
        }

    def _get_network_type_for_isp(self, isp: str, connection_type: str = "random") -> str:
        """Get network type berdasarkan ISP Indonesia"""
        isp_info = self.indonesia_isps.get(isp, {})
        network_types = isp_info.get("network_types", ["WiFi"])
        
        if connection_type == "mobile":
            mobile_types = [t for t in network_types if t in ["5G", "4G LTE", "4G", "3G", "LTE"]]
            return random.choice(mobile_types) if mobile_types else "4G LTE"
        else:
            return "WiFi"

    def _get_connection_type_for_isp(self, isp: str) -> str:
        """Determine connection type berdasarkan ISP Indonesia"""
        isp_info = self.indonesia_isps.get(isp, {})
        isp_type = isp_info.get("type", "mobile")
        
        if isp_type in ["mobile"]:
            return random.choice(["mobile", "wifi"])  # Mobile users can use WiFi too
        else:
            return "wifi"
        
    def _initialize_indonesia_ip_sources(self):
        """Initialize IP sources - INDONESIA ONLY"""
        return {
            # Mobile Operators
            "telkomsel": self._generate_telkomsel_ips,
            "indosat": self._generate_indosat_ips,
            "xl": self._generate_xl_ips,
            "tri": self._generate_tri_ips,
            "smartfren": self._generate_smartfren_ips,
            "axis": self._generate_xl_ips,  # Axis uses XL network
            "by.u": self._generate_telkomsel_ips,  # by.U uses Telkomsel network
            # Broadband ISPs
            "biznet": self._generate_biznet_ips,
            "firstmedia": self._generate_firstmedia_ips,
            "myrepublic": self._generate_myrepublic_ips,
            "indihome": self._generate_indihome_ips,
            "cbn": self._generate_cbn_ips,
            "mncplay": self._generate_mncplay_ips,
            "iconnet": self._generate_iconnet_ips,
            "oxygen": self._generate_oxygen_ips,
        }
    
    def _load_country_database(self) -> Dict[str, Any]:
        """Load comprehensive country database from JSON file"""
        try:
            db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "country_database.json")
            if os.path.exists(db_path):
                with open(db_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            print(f"{kuning}    Warning: Could not load country_database.json: {e}{reset}")
        
        # Return empty dict if file not found
        return {"countries": {}}
    
    def _get_country_config(self) -> Dict[str, Any]:
        """Get Indonesia country configuration"""
        return {
            "ID": {
                "name": "Indonesia",
                "language": "id-ID",
                "timezone": "Asia/Jakarta",
                "currency": "IDR",
                "isps": {
                    "telkomsel": {
                        "prefixes": ["110.136", "110.137", "114.124", "118.137", "139.192", "182.253"],
                        "asn": "AS7713",
                        "as_name": "PT Telekomunikasi Selular",
                        "type": "mobile",
                        "mcc": "510",
                        "mnc": "10",
                    },
                    "indosat": {
                        "prefixes": ["112.215", "114.4", "125.160", "139.0", "202.152"],
                        "asn": "AS4761",
                        "as_name": "PT Indosat Tbk",
                        "type": "mobile",
                        "mcc": "510",
                        "mnc": "21",
                    },
                    "xl": {
                        "prefixes": ["36.86", "114.120", "180.241", "110.139"],
                        "asn": "AS24203",
                        "as_name": "PT XL Axiata Tbk",
                        "type": "mobile",
                        "mcc": "510",
                        "mnc": "11",
                    },
                    "biznet": {
                        "prefixes": ["103.28", "103.78", "117.102", "182.253"],
                        "asn": "AS17451",
                        "as_name": "PT Biznet Gio Nusantara",
                        "type": "wifi",
                    }
                },
                "cities": [
                    {"name": "Jakarta", "lat": -6.2088, "lon": 106.8456, "region": "DKI Jakarta"},
                    {"name": "Surabaya", "lat": -7.2575, "lon": 112.7521, "region": "East Java"},
                    {"name": "Bandung", "lat": -6.9175, "lon": 107.6191, "region": "West Java"},
                    {"name": "Medan", "lat": 3.5952, "lon": 98.6722, "region": "North Sumatra"},
                    {"name": "Bali", "lat": -8.3405, "lon": 115.0920, "region": "Bali"},
                ],
                "devices": [
                    {"brand": "Samsung", "models": ["SM-A546E", "SM-A346E", "SM-S928B", "SM-S918B"]},
                    {"brand": "Xiaomi", "models": ["23116PN5BC", "22071219CG", "2201117TG"]},
                    {"brand": "OPPO", "models": ["CPH2585", "CPH2565", "CPH2531"]},
                    {"brand": "Vivo", "models": ["V2254", "V2219", "V2203"]},
                ]
            },
            "US": {
                "name": "United States",
                "language": "en-US",
                "timezone": "America/New_York",
                "currency": "USD",
                "isps": {
                    "verizon": {
                        "prefixes": ["174.192", "174.225", "70.192", "98.116"],
                        "asn": "AS22394",
                        "as_name": "Verizon Wireless",
                        "type": "mobile",
                        "mcc": "311",
                        "mnc": "480",
                    },
                    "att": {
                        "prefixes": ["166.137", "166.171", "107.77", "108.186"],
                        "asn": "AS20057",
                        "as_name": "AT&T Mobility",
                        "type": "mobile",
                        "mcc": "310",
                        "mnc": "410",
                    },
                    "tmobile": {
                        "prefixes": ["172.32", "172.58", "100.128", "208.54"],
                        "asn": "AS21928",
                        "as_name": "T-Mobile USA",
                        "type": "mobile",
                        "mcc": "310",
                        "mnc": "260",
                    },
                    "comcast": {
                        "prefixes": ["73.93", "73.162", "98.216", "50.79"],
                        "asn": "AS7922",
                        "as_name": "Comcast Cable Communications",
                        "type": "wifi",
                    },
                    "spectrum": {
                        "prefixes": ["72.68", "72.93", "97.87", "24.14"],
                        "asn": "AS11351",
                        "as_name": "Charter Communications",
                        "type": "wifi",
                    }
                },
                "cities": [
                    {"name": "New York", "lat": 40.7128, "lon": -74.0060, "region": "New York"},
                    {"name": "Los Angeles", "lat": 34.0522, "lon": -118.2437, "region": "California"},
                    {"name": "Chicago", "lat": 41.8781, "lon": -87.6298, "region": "Illinois"},
                    {"name": "Houston", "lat": 29.7604, "lon": -95.3698, "region": "Texas"},
                    {"name": "Miami", "lat": 25.7617, "lon": -80.1918, "region": "Florida"},
                ],
                "devices": [
                    {"brand": "Apple", "models": ["iPhone15,2", "iPhone15,3", "iPhone14,5"]},
                    {"brand": "Samsung", "models": ["SM-S928U", "SM-S918U", "SM-G998U"]},
                    {"brand": "Google", "models": ["Pixel 8 Pro", "Pixel 8", "Pixel 7 Pro"]},
                ]
            },
            "BR": {
                "name": "Brazil",
                "language": "pt-BR",
                "timezone": "America/Sao_Paulo",
                "currency": "BRL",
                "isps": {
                    "claro_br": {
                        "prefixes": ["177.32", "177.84", "189.4", "200.215"],
                        "asn": "AS28573",
                        "as_name": "Claro S.A.",
                        "type": "mobile",
                        "mcc": "724",
                        "mnc": "05",
                    },
                    "vivo_br": {
                        "prefixes": ["179.152", "189.79", "200.150", "201.16"],
                        "asn": "AS26599",
                        "as_name": "Telefonica Brasil S.A.",
                        "type": "mobile",
                        "mcc": "724",
                        "mnc": "06",
                    },
                    "tim_br": {
                        "prefixes": ["179.176", "189.36", "186.204"],
                        "asn": "AS26615",
                        "as_name": "TIM S/A",
                        "type": "mobile",
                        "mcc": "724",
                        "mnc": "02",
                    }
                },
                "cities": [
                    {"name": "São Paulo", "lat": -23.5505, "lon": -46.6333, "region": "SP"},
                    {"name": "Rio de Janeiro", "lat": -22.9068, "lon": -43.1729, "region": "RJ"},
                    {"name": "Brasília", "lat": -15.7942, "lon": -47.8822, "region": "DF"},
                    {"name": "Salvador", "lat": -12.9714, "lon": -38.5014, "region": "BA"},
                ],
                "devices": [
                    {"brand": "Samsung", "models": ["SM-A546E", "SM-A346B", "SM-S918B"]},
                    {"brand": "Motorola", "models": ["XT2347-2", "XT2343-1", "XT2301-4"]},
                    {"brand": "Xiaomi", "models": ["23116PN5BC", "22071219CG"]},
                ]
            },
            "IN": {
                "name": "India",
                "language": "en-IN",
                "timezone": "Asia/Kolkata",
                "currency": "INR",
                "isps": {
                    "jio": {
                        "prefixes": ["49.36", "49.44", "157.32", "157.48"],
                        "asn": "AS55836",
                        "as_name": "Reliance Jio Infocomm Limited",
                        "type": "mobile",
                        "mcc": "405",
                        "mnc": "862",
                    },
                    "airtel_in": {
                        "prefixes": ["106.76", "106.210", "122.161", "182.64"],
                        "asn": "AS24560",
                        "as_name": "Bharti Airtel Ltd.",
                        "type": "mobile",
                        "mcc": "404",
                        "mnc": "10",
                    },
                    "vi_in": {
                        "prefixes": ["106.196", "115.110", "117.195"],
                        "asn": "AS45609",
                        "as_name": "Vodafone Idea Limited",
                        "type": "mobile",
                        "mcc": "404",
                        "mnc": "20",
                    }
                },
                "cities": [
                    {"name": "Mumbai", "lat": 19.0760, "lon": 72.8777, "region": "Maharashtra"},
                    {"name": "Delhi", "lat": 28.6139, "lon": 77.2090, "region": "Delhi"},
                    {"name": "Bangalore", "lat": 12.9716, "lon": 77.5946, "region": "Karnataka"},
                    {"name": "Hyderabad", "lat": 17.3850, "lon": 78.4867, "region": "Telangana"},
                    {"name": "Chennai", "lat": 13.0827, "lon": 80.2707, "region": "Tamil Nadu"},
                ],
                "devices": [
                    {"brand": "Samsung", "models": ["SM-A546E", "SM-M546B", "SM-S918B"]},
                    {"brand": "Xiaomi", "models": ["23116PN5BC", "22071219CI", "2201117TI"]},
                    {"brand": "OnePlus", "models": ["CPH2467", "CPH2451", "NE2213"]},
                    {"brand": "Realme", "models": ["RMX3700", "RMX3630", "RMX3610"]},
                ]
            },
            "DE": {
                "name": "Germany",
                "language": "de-DE",
                "timezone": "Europe/Berlin",
                "currency": "EUR",
                "isps": {
                    "telekom_de": {
                        "prefixes": ["91.64", "217.6", "93.220", "84.138"],
                        "asn": "AS3320",
                        "as_name": "Deutsche Telekom AG",
                        "type": "mobile",
                        "mcc": "262",
                        "mnc": "01",
                    },
                    "vodafone_de": {
                        "prefixes": ["80.187", "91.0", "92.72", "109.42"],
                        "asn": "AS3209",
                        "as_name": "Vodafone GmbH",
                        "type": "mobile",
                        "mcc": "262",
                        "mnc": "02",
                    },
                    "o2_de": {
                        "prefixes": ["82.113", "83.169", "92.224", "109.40"],
                        "asn": "AS8422",
                        "as_name": "O2 (Germany) GmbH & Co. OHG",
                        "type": "mobile",
                        "mcc": "262",
                        "mnc": "03",
                    }
                },
                "cities": [
                    {"name": "Berlin", "lat": 52.5200, "lon": 13.4050, "region": "Berlin"},
                    {"name": "Munich", "lat": 48.1351, "lon": 11.5820, "region": "Bavaria"},
                    {"name": "Hamburg", "lat": 53.5511, "lon": 9.9937, "region": "Hamburg"},
                    {"name": "Frankfurt", "lat": 50.1109, "lon": 8.6821, "region": "Hesse"},
                ],
                "devices": [
                    {"brand": "Samsung", "models": ["SM-S928B", "SM-S918B", "SM-A546B"]},
                    {"brand": "Apple", "models": ["iPhone15,2", "iPhone15,3", "iPhone14,5"]},
                    {"brand": "Google", "models": ["Pixel 8 Pro", "Pixel 8"]},
                ]
            }
        }
    
    def _generate_us_mobile_ips(self) -> List[Dict[str, Any]]:
        """Generate US mobile carrier IPs"""
        return self._generate_country_ips("US", ["verizon", "att", "tmobile"])
    
    def _generate_us_isp_ips(self) -> List[Dict[str, Any]]:
        """Generate US ISP IPs"""
        return self._generate_country_ips("US", ["comcast", "spectrum"])
    
    def _generate_brazil_ips(self) -> List[Dict[str, Any]]:
        """Generate Brazil IPs"""
        return self._generate_country_ips("BR", ["claro_br", "vivo_br", "tim_br"])
    
    def _generate_india_ips(self) -> List[Dict[str, Any]]:
        """Generate India IPs"""
        return self._generate_country_ips("IN", ["jio", "airtel_in", "vi_in"])
    
    def _generate_country_ips(self, country_code: str, isp_list: List[str]) -> List[Dict[str, Any]]:
        """Generate IPs for a specific country with full synchronization"""
        country_config = self._get_country_config().get(country_code)
        if not country_config:
            return []
        
        ip_pool = []
        for isp_name in isp_list:
            isp_config = country_config["isps"].get(isp_name)
            if not isp_config:
                continue
            
            for _ in range(random.randint(2, 5)):
                # Generate IP
                prefix = random.choice(isp_config["prefixes"])
                parts = prefix.split('.')
                while len(parts) < 4:
                    parts.append(str(random.randint(2, 253)))
                ip = '.'.join(parts[:4])
                
                # Validate
                if not self._validate_ip_format_enhanced(ip):
                    continue
                
                # Select city
                city = random.choice(country_config["cities"])
                
                # Select device matching country
                device_brand = random.choice(country_config["devices"])
                device_model = random.choice(device_brand["models"])
                
                # Create synchronized profile
                ip_info = {
                    "ip": ip,
                    "country": country_code,
                    "country_name": country_config["name"],
                    "isp": isp_name,
                    "asn": isp_config["asn"],
                    "as_name": isp_config["as_name"],
                    "city": city["name"],
                    "region": city["region"],
                    "latitude": city["lat"],
                    "longitude": city["lon"],
                    "timezone": country_config["timezone"],
                    "language": country_config["language"],
                    "connection_type": isp_config["type"],
                    "mcc": isp_config.get("mcc", ""),
                    "mnc": isp_config.get("mnc", ""),
                    "device_brand": device_brand["brand"],
                    "device_model": device_model,
                    "health_score": random.randint(85, 98),
                    "last_used": 0,
                    "use_count": 0,
                    "generated_at": time.time()
                }
                
                ip_pool.append(ip_info)
        
        return ip_pool
    
    def _generate_dynamic_isp_ips(self, isp_name: str) -> List[Dict[str, Any]]:
        """Generate ultra-fresh residential IPs with advanced anti-detection"""
        current_time = time.time()
        
        config = self._get_isp_config_enhanced(isp_name)
        if not config:
            return []
        
        ip_pool = []
        ip_count = random.randint(5, 12)
        attempts = 0
        max_attempts = ip_count * 10  # More attempts for stricter validation
        
        while len(ip_pool) < ip_count and attempts < max_attempts:
            attempts += 1
            
            ip = self._generate_residential_ip(isp_name, config)
            
            if not ip:
                continue
            
            # Ultra-strict validation chain
            if not self._ultra_anti_blacklist_check(ip):
                continue
            
            if not self._validate_ip_format_enhanced(ip):
                continue
            
            # Residential IP verification
            if not self._verify_residential_ip(ip, isp_name):
                continue
            
            # Enhanced validation with very strict mode
            validation = self.validator.validate(ip, strict=True)
            if not validation["valid"] or validation["score"] < 85:  # Raised to 85
                continue
            
            # Check all blacklists
            if ip in self.blacklisted_ips:
                continue
            
            if self._is_suspicious_ip_pattern(ip):
                continue
            
            # Check duplicates
            if any(ip_info["ip"] == ip for ip_info in self.ip_pool):
                continue
            if any(ip_info["ip"] == ip for ip_info in ip_pool):
                continue
            
            # Create ultra-fresh IP profile
            ip_info = self._create_residential_ip_profile(ip, config, isp_name)
            ip_info["freshness_score"] = 100
            ip_info["residential_verified"] = True
            ip_info["anti_blacklist_verified"] = True
            ip_info["generation_timestamp"] = current_time
            ip_info["never_used"] = True
            
            ip_pool.append(ip_info)
        
        print(f"{cyan}    Generated {len(ip_pool)} residential-verified IPs for {isp_name}{reset}")
        return ip_pool
    
    def _generate_residential_ip(self, isp_name: str, config: Dict[str, Any]) -> Optional[str]:
        """Generate IP that looks like residential/mobile IP"""
        try:
            prefix = random.choice(config["prefixes"])
            parts = prefix.split('.')
            
            # Generate realistic residential IP patterns
            while len(parts) < 4:
                if len(parts) == 2:
                    # Third octet - use common residential ranges
                    parts.append(str(random.choice([
                        random.randint(0, 63),    # Low range
                        random.randint(64, 127),  # Mid-low range
                        random.randint(128, 191), # Mid-high range
                        random.randint(192, 223), # High range (avoid 224+)
                    ])))
                elif len(parts) == 3:
                    # Fourth octet - avoid suspicious patterns
                    fourth = self._generate_residential_fourth_octet()
                    parts.append(str(fourth))
            
            ip = '.'.join(parts[:4])
            return ip if self._validate_ip_format_enhanced(ip) else None
            
        except Exception:
            return None
    
    def _generate_residential_fourth_octet(self) -> int:
        """Generate fourth octet that looks residential"""
        # Avoid: 0, 1, 2, 254, 255 (network/broadcast)
        # Avoid: 10, 20, 50, 100, 128, 200, 250 (round numbers - often servers)
        # Prefer: random-looking numbers
        
        avoid = {0, 1, 2, 10, 20, 50, 100, 128, 200, 250, 254, 255}
        
        # Generate with natural distribution
        while True:
            # Bias towards middle range (more common for residential)
            if random.random() < 0.6:
                octet = random.randint(30, 220)
            else:
                octet = random.randint(3, 253)
            
            if octet not in avoid:
                return octet
    
    def _verify_residential_ip(self, ip: str, isp_name: str) -> bool:
        """Verify IP looks like residential/mobile IP"""
        try:
            parts = [int(p) for p in ip.split('.')]
            
            # Check IP is in valid residential ranges for ISP
            config = self._get_isp_config_enhanced(isp_name)
            if not config:
                return False
            
            # Verify prefix matches ISP
            ip_prefix = f"{parts[0]}.{parts[1]}"
            valid_prefixes = config.get("prefixes", [])
            
            if not any(ip.startswith(prefix) for prefix in valid_prefixes):
                return False
            
            # Additional residential checks
            # Avoid sequential patterns
            if parts[2] == parts[3]:
                return False
            
            # Avoid common server patterns
            if parts[3] in [1, 2, 254, 255]:
                return False
            
            # Check for natural-looking distribution
            variance = max(parts) - min(parts)
            if variance < 10:  # Too uniform, might be generated
                return False
            
            return True
            
        except Exception:
            return False
    
    def _create_residential_ip_profile(self, ip: str, config: Dict[str, Any], 
                                       isp_name: str) -> Dict[str, Any]:
        """Create comprehensive residential IP profile"""
        city = random.choice(config.get("cities", ["Jakarta"]))
        city_coords = self._get_city_coordinates_enhanced(city)
        
        connection_type = self._get_connection_type_for_isp(isp_name)
        network_type = self._get_network_type_for_isp(isp_name, connection_type)
        
        # Generate realistic network metrics for residential
        if connection_type == "mobile":
            latency = random.uniform(20, 80)  # Mobile has higher latency
            jitter = random.uniform(5, 25)
            download_speed = random.uniform(10, 100)  # Mbps
            upload_speed = random.uniform(5, 30)
        else:
            latency = random.uniform(5, 30)  # WiFi lower latency
            jitter = random.uniform(1, 10)
            download_speed = random.uniform(50, 300)
            upload_speed = random.uniform(20, 100)
        
        return {
            "ip": ip,
            "isp": isp_name,
            "asn": config.get("asn", ""),
            "as_name": config.get("as_name", ""),
            "country": "ID",
            "city": city,
            "region": city_coords.get("region", ""),
            "latitude": city_coords.get("lat", 0) + random.uniform(-0.05, 0.05),
            "longitude": city_coords.get("lon", 0) + random.uniform(-0.05, 0.05),
            "timezone": "Asia/Jakarta",
            "connection_type": connection_type,
            "network_type": network_type,
            "carrier": isp_name.upper() if connection_type == "mobile" else "",
            "mcc": self._get_mcc_for_isp(isp_name) if connection_type == "mobile" else "",
            "mnc": self._get_mnc_for_isp(isp_name) if connection_type == "mobile" else "",
            "health_score": random.randint(88, 98),
            "latency_ms": latency,
            "jitter_ms": jitter,
            "download_mbps": download_speed,
            "upload_mbps": upload_speed,
            "timestamp": time.time(),
            "usage_count": 0,
            "last_used": 0,
            "residential": True,
            "mobile": connection_type == "mobile",
            "proxy_detected": False,
            "vpn_detected": False,
            "datacenter_detected": False,
        }
    
    def _ultra_anti_blacklist_check(self, ip: str) -> bool:
        """Ultra-comprehensive anti-blacklist verification"""
        try:
            parts = ip.split('.')
            if len(parts) != 4:
                return False
            
            first = int(parts[0])
            second = int(parts[1])
            third = int(parts[2])
            fourth = int(parts[3])
            
            # === DATACENTER/CLOUD PROVIDER RANGES ===
            datacenter_prefixes = [
                # AWS
                "3.0", "3.1", "3.2", "3.5", "3.6",
                "13.52", "13.53", "13.54", "13.55", "13.56", "13.57", "13.58", "13.59",
                "18.130", "18.131", "18.132", "18.133", "18.134", "18.135",
                "18.188", "18.189", "18.190", "18.191",
                "18.216", "18.217", "18.218", "18.219", "18.220", "18.221",
                "34.192", "34.193", "34.194", "34.195", "34.196", "34.197", "34.198", "34.199",
                "34.200", "34.201", "34.202", "34.203", "34.204", "34.205", "34.206", "34.207",
                "35.153", "35.154", "35.155", "35.156", "35.157", "35.158", "35.159",
                "44.192", "44.193", "44.194", "44.195", "44.196", "44.197", "44.198", "44.199",
                "52.0", "52.1", "52.2", "52.3", "52.4", "52.5", "52.6", "52.7",
                "52.20", "52.21", "52.22", "52.23", "52.24", "52.25", "52.26", "52.27",
                "54.80", "54.81", "54.82", "54.83", "54.84", "54.85", "54.86", "54.87",
                "54.88", "54.89", "54.90", "54.91", "54.92", "54.93", "54.94", "54.95",
                # Google Cloud
                "34.64", "34.65", "34.66", "34.67", "34.68", "34.69", "34.70", "34.71",
                "35.184", "35.185", "35.186", "35.187", "35.188", "35.189", "35.190", "35.191",
                "35.192", "35.193", "35.194", "35.195", "35.196", "35.197", "35.198", "35.199",
                "35.200", "35.201", "35.202", "35.203", "35.204", "35.205", "35.206", "35.207",
                "35.208", "35.209", "35.210", "35.211", "35.212", "35.213", "35.214", "35.215",
                # Azure
                "13.64", "13.65", "13.66", "13.67", "13.68", "13.69", "13.70", "13.71",
                "20.36", "20.37", "20.38", "20.39", "20.40", "20.41", "20.42", "20.43",
                "40.64", "40.65", "40.66", "40.67", "40.68", "40.69", "40.70", "40.71",
                "52.136", "52.137", "52.138", "52.139", "52.140", "52.141", "52.142", "52.143",
                # DigitalOcean
                "104.131", "104.236", "104.238",
                "107.170", "107.173",
                "128.199", "134.122", "134.209",
                "137.184", "138.68", "138.197",
                "139.59", "142.93",
                "157.230", "157.245",
                "159.65", "159.89", "159.203",
                "161.35", "162.243",
                "164.90", "164.92",
                "165.22", "165.227",
                "167.71", "167.172", "167.99",
                "178.62", "178.128",
                "188.166",
                "192.241", "198.199", "198.211",
                "206.81", "206.189",
                "209.97",
                # Linode
                "45.33", "45.56", "45.79",
                "50.116",
                "66.175", "66.228",
                "69.164",
                "72.14",
                "74.207",
                "96.126",
                "97.107",
                "139.162",
                "172.104", "172.105",
                "173.230", "173.255",
                "176.58",
                "178.79",
                "192.155",
                "194.195",
                "198.58",
                "212.71",
                # Vultr
                "45.32", "45.63", "45.76", "45.77",
                "64.156", "64.237",
                "66.42",
                "95.179",
                "104.156", "104.207", "104.238",
                "108.61",
                "136.244",
                "140.82",
                "144.202",
                "149.28",
                "155.138",
                "207.148",
                "208.167",
                "209.250",
                "216.128",
                # OVH
                "51.38", "51.68", "51.75", "51.77", "51.79", "51.81", "51.83", "51.89",
                "54.36", "54.37", "54.38", "54.39",
                "91.121",
                "92.222",
                "135.125", "137.74",
                "139.99",
                "142.44",
                "144.217",
                "145.239",
                "147.135",
                "149.56",
                "151.80",
                "158.69",
                "164.132",
                "167.114",
                "176.31",
                "178.32", "178.33",
                "188.165",
                "192.95", "192.99",
                "193.70",
                "195.154",
                "198.27", "198.50", "198.100",
                "213.32", "213.186", "213.251",
                "217.182",
            ]
            
            # === VPN PROVIDER RANGES ===
            vpn_prefixes = [
                # NordVPN
                "5.253", "37.120", "62.102", "68.71", "82.102", "84.17", "89.36", "89.187",
                "91.207", "92.119", "93.115", "94.140", "103.75", "109.70", "138.199",
                "146.70", "149.34", "154.47", "156.67", "159.69", "165.231", "169.150",
                "181.215", "185.159", "185.195", "185.220", "185.230", "188.95",
                "193.9", "193.27", "193.176", "193.178",
                "194.99", "194.127", "194.156",
                "195.181", "195.206", "196.196",
                "198.44",
                "212.102", "213.152", "217.138",
                # ExpressVPN
                "89.238", "91.90", "91.132", "91.134",
                "109.200", "146.158",
                "176.56", "176.57", "176.67",
                "185.59", "185.94",
                "195.8",
                # Surfshark
                "89.44", "89.147", "95.174",
                "104.129", "149.86", "149.88",
                "185.65", "185.93", "185.153",
                "191.101",
                "212.8", "212.22", "212.32",
                # ProtonVPN
                "146.70", "156.146", "185.107", "185.159",
                # Private Internet Access
                "162.245", "169.197", "178.162", "185.217",
                "191.96", "193.25",
                # Mullvad
                "45.83", "86.106", "86.107",
                "141.98", "185.213", "193.27",
                "198.54",
            ]
            
            # === PROXY/HOSTING RANGES ===
            proxy_prefixes = [
                "23.94", "23.95",  # ColoCrossing
                "64.145",  # Psychz
                "66.70", "66.206",  # Various
                "69.30", "69.46", "69.167",  # Various hosting
                "72.52",  # QuadraNet
                "76.164",  # Cogent
                "96.8", "96.9",  # Wholesale Internet
                "103.21", "103.22", "103.31",  # Cloudflare
                "104.16", "104.17", "104.18", "104.19", "104.20", "104.21", "104.22", "104.23",  # Cloudflare
                "104.24", "104.25", "104.26", "104.27",  # Cloudflare
                "141.101",  # Cloudflare
                "162.158", "162.159",  # Cloudflare
                "172.64", "172.65", "172.66", "172.67",  # Cloudflare
                "173.245",  # Cloudflare
                "188.114",  # Cloudflare
                "190.93",  # Cloudflare
                "197.234",  # Cloudflare
                "198.41",  # Cloudflare
                "199.27",  # Cloudflare
            ]
            
            # Check against all blacklisted prefixes
            ip_prefix_2 = f"{parts[0]}.{parts[1]}"
            ip_prefix_3 = f"{parts[0]}.{parts[1]}.{parts[2]}"
            
            all_blacklisted = datacenter_prefixes + vpn_prefixes + proxy_prefixes
            
            for prefix in all_blacklisted:
                if ip.startswith(prefix) or ip_prefix_2.startswith(prefix) or ip_prefix_3.startswith(prefix):
                    return False
            
            # === RESERVED/SPECIAL RANGES ===
            # Private
            if first == 10:
                return False
            if first == 172 and 16 <= second <= 31:
                return False
            if first == 192 and second == 168:
                return False
            
            # Reserved
            if first in [0, 127] or first >= 224:
                return False
            
            # Link-local
            if first == 169 and second == 254:
                return False
            
            # Shared address space (CGNAT)
            if first == 100 and 64 <= second <= 127:
                return False
            
            # Documentation ranges
            if (first == 192 and second == 0 and third == 2) or \
               (first == 198 and second == 51 and third == 100) or \
               (first == 203 and second == 0 and third == 113):
                return False
            
            # === SUSPICIOUS PATTERNS ===
            # Network/broadcast addresses
            if fourth in [0, 1, 254, 255]:
                return False
            
            # All same octets
            if first == second == third == fourth:
                return False
            
            # Sequential
            if abs(fourth - third) == 1 and abs(third - second) == 1 and abs(second - first) == 1:
                return False
            
            # Round numbers (often server IPs)
            if fourth in [10, 20, 50, 100, 150, 200, 250]:
                return False
            
            return True
            
        except Exception:
            return False
    
    def _is_suspicious_ip_pattern(self, ip: str) -> bool:
        """Check for suspicious IP patterns that might be flagged"""
        try:
            parts = [int(p) for p in ip.split('.')]
            
            # Avoid common test/example IPs
            if ip.startswith("192.0.2.") or ip.startswith("198.51.100.") or ip.startswith("203.0.113."):
                return True
            
            # Avoid round numbers that might be suspicious
            if parts[3] in [0, 10, 20, 50, 100, 128, 200, 250, 255]:
                return True
            
            # Avoid sequential patterns
            if parts[2] == parts[3] or parts[1] == parts[2] == parts[3]:
                return True
            
            # Avoid too-high health in last octet (often datacenter)
            if parts[3] > 250:
                return True
            
            return False
            
        except Exception:
            return True
    
    def _get_isp_config_enhanced(self, isp_name: str) -> Optional[Dict[str, Any]]:
        """Enhanced ISP configuration dengan lebih banyak detail"""
        isp_configs = {
            "telkomsel": {
                "prefixes": ["110.136", "110.137", "114.124", "118.137", "139.192", "182.253", "202.67"],
                "asn": "AS7713",
                "as_name": "PT Telekomunikasi Selular",
                "ttl_range": (48, 64),
                "window_range": (64240, 65535),
                "mss_range": (1360, 1460),
                "cities": ["Jakarta", "Surabaya", "Bandung", "Medan", "Bali", "Makassar"],
                "latency_range": (15, 45),
                "jitter_range": (2, 10),
                "packet_loss": (0.1, 0.5)
            },
            "indosat": {
                "prefixes": ["112.215", "114.4", "125.160", "139.0", "202.152", "202.43"],
                "asn": "AS4761",
                "as_name": "PT Indosat Tbk",
                "ttl_range": (52, 60),
                "window_range": (64240, 65535),
                "mss_range": (1360, 1460),
                "cities": ["Jakarta", "Surabaya", "Makassar", "Balikpapan", "Batam"],
                "latency_range": (20, 50),
                "jitter_range": (3, 12),
                "packet_loss": (0.2, 0.6)
            },
            "xl": {
                "prefixes": ["36.86", "114.120", "180.241", "202.43", "110.139"],
                "asn": "AS24203",
                "as_name": "PT XL Axiata Tbk",
                "ttl_range": (56, 64),
                "window_range": (64240, 65535),
                "mss_range": (1360, 1460),
                "cities": ["Jakarta", "Yogyakarta", "Semarang", "Palembang", "Lampung"],
                "latency_range": (25, 55),
                "jitter_range": (4, 15),
                "packet_loss": (0.3, 0.7)
            },
            "tri": {
                "prefixes": ["116.206", "118.96", "182.253", "203.190", "103.10"],
                "asn": "AS23947",
                "as_name": "PT Hutchison 3 Indonesia",
                "ttl_range": (60, 68),
                "window_range": (43800, 44200),
                "mss_range": (1360, 1460),
                "cities": ["Jakarta", "Surabaya", "Bandung", "Bekasi", "Tangerang"],
                "latency_range": (30, 60),
                "jitter_range": (5, 18),
                "packet_loss": (0.4, 0.8)
            },
            "smartfren": {
                "prefixes": ["202.67", "103.10"],
                "asn": "AS18004",
                "as_name": "PT Smartfren Telecom Tbk",
                "ttl_range": (52, 60),
                "window_range": (29200, 29500),
                "mss_range": (1360, 1460),
                "cities": ["Jakarta", "Bali", "Batam", "Surabaya"],
                "latency_range": (35, 65),
                "jitter_range": (6, 20),
                "packet_loss": (0.5, 0.9)
            },
            "biznet": {
                "prefixes": ["103.28", "103.78", "117.102", "182.253"],
                "asn": "AS17451",
                "as_name": "PT Biznet Gio Nusantara",
                "ttl_range": (64, 72),
                "window_range": (64240, 65535),
                "mss_range": (1360, 1460),
                "cities": ["Jakarta", "Surabaya", "Bandung"],
                "latency_range": (10, 30),
                "jitter_range": (1, 5),
                "packet_loss": (0.1, 0.3)
            },
            "cbn": {
                "prefixes": ["202.158", "202.169", "117.102"],
                "asn": "AS9340",
                "as_name": "PT Cyberindo Aditama",
                "ttl_range": (64, 72),
                "window_range": (64240, 65535),
                "mss_range": (1360, 1460),
                "cities": ["Jakarta", "Surabaya"],
                "latency_range": (8, 25),
                "jitter_range": (1, 4),
                "packet_loss": (0.1, 0.2)
            },
            # US ISPs
            "verizon": {
                "prefixes": ["174.192", "174.225", "70.192", "98.116"],
                "asn": "AS22394",
                "as_name": "Verizon Wireless",
                "ttl_range": (64, 128),
                "window_range": (64240, 65535),
                "mss_range": (1360, 1460),
                "cities": ["New York", "Los Angeles", "Chicago", "Houston", "Miami"],
                "latency_range": (15, 40),
                "jitter_range": (2, 8),
                "packet_loss": (0.1, 0.4)
            },
            "att": {
                "prefixes": ["166.137", "166.171", "107.77", "108.186"],
                "asn": "AS20057",
                "as_name": "AT&T Mobility",
                "ttl_range": (64, 128),
                "window_range": (64240, 65535),
                "mss_range": (1360, 1460),
                "cities": ["Dallas", "Atlanta", "San Francisco", "Seattle"],
                "latency_range": (18, 45),
                "jitter_range": (3, 10),
                "packet_loss": (0.2, 0.5)
            },
            "tmobile": {
                "prefixes": ["172.32", "172.58", "100.128", "208.54"],
                "asn": "AS21928",
                "as_name": "T-Mobile USA",
                "ttl_range": (64, 128),
                "window_range": (64240, 65535),
                "mss_range": (1360, 1460),
                "cities": ["Bellevue", "Las Vegas", "Denver", "Phoenix"],
                "latency_range": (20, 50),
                "jitter_range": (4, 12),
                "packet_loss": (0.3, 0.6)
            },
            "comcast": {
                "prefixes": ["73.93", "73.162", "98.216", "50.79"],
                "asn": "AS7922",
                "as_name": "Comcast Cable Communications",
                "ttl_range": (64, 128),
                "window_range": (64240, 65535),
                "mss_range": (1360, 1460),
                "cities": ["Philadelphia", "Chicago", "Denver", "San Jose"],
                "latency_range": (8, 25),
                "jitter_range": (1, 5),
                "packet_loss": (0.1, 0.3)
            },
            "spectrum": {
                "prefixes": ["72.68", "72.93", "97.87", "24.14"],
                "asn": "AS11351",
                "as_name": "Charter Communications",
                "ttl_range": (64, 128),
                "window_range": (64240, 65535),
                "mss_range": (1360, 1460),
                "cities": ["Stamford", "St Louis", "Tampa", "Austin"],
                "latency_range": (10, 30),
                "jitter_range": (2, 6),
                "packet_loss": (0.1, 0.3)
            },
            # Brazil ISPs
            "claro_br": {
                "prefixes": ["177.32", "177.84", "189.4", "200.215"],
                "asn": "AS28573",
                "as_name": "Claro S.A.",
                "ttl_range": (64, 128),
                "window_range": (64240, 65535),
                "mss_range": (1360, 1460),
                "cities": ["São Paulo", "Rio de Janeiro", "Brasília", "Salvador"],
                "latency_range": (25, 60),
                "jitter_range": (5, 15),
                "packet_loss": (0.3, 0.7)
            },
            "vivo_br": {
                "prefixes": ["179.152", "189.79", "200.150", "201.16"],
                "asn": "AS26599",
                "as_name": "Telefonica Brasil S.A.",
                "ttl_range": (64, 128),
                "window_range": (64240, 65535),
                "mss_range": (1360, 1460),
                "cities": ["São Paulo", "Rio de Janeiro", "Curitiba"],
                "latency_range": (20, 55),
                "jitter_range": (4, 12),
                "packet_loss": (0.2, 0.6)
            },
            "tim_br": {
                "prefixes": ["179.176", "189.36", "186.204"],
                "asn": "AS26615",
                "as_name": "TIM S/A",
                "ttl_range": (64, 128),
                "window_range": (64240, 65535),
                "mss_range": (1360, 1460),
                "cities": ["São Paulo", "Belo Horizonte", "Porto Alegre"],
                "latency_range": (30, 65),
                "jitter_range": (6, 18),
                "packet_loss": (0.4, 0.8)
            },
            # India ISPs
            "jio": {
                "prefixes": ["49.36", "49.44", "157.32", "157.48"],
                "asn": "AS55836",
                "as_name": "Reliance Jio Infocomm Limited",
                "ttl_range": (64, 128),
                "window_range": (64240, 65535),
                "mss_range": (1360, 1460),
                "cities": ["Mumbai", "Delhi", "Bangalore", "Hyderabad", "Chennai"],
                "latency_range": (20, 50),
                "jitter_range": (4, 12),
                "packet_loss": (0.2, 0.5)
            },
            "airtel_in": {
                "prefixes": ["106.76", "106.210", "122.161", "182.64"],
                "asn": "AS24560",
                "as_name": "Bharti Airtel Ltd.",
                "ttl_range": (64, 128),
                "window_range": (64240, 65535),
                "mss_range": (1360, 1460),
                "cities": ["Mumbai", "Delhi", "Kolkata", "Chennai"],
                "latency_range": (25, 55),
                "jitter_range": (5, 15),
                "packet_loss": (0.3, 0.6)
            },
            "vi_in": {
                "prefixes": ["106.196", "115.110", "117.195"],
                "asn": "AS45609",
                "as_name": "Vodafone Idea Limited",
                "ttl_range": (64, 128),
                "window_range": (64240, 65535),
                "mss_range": (1360, 1460),
                "cities": ["Mumbai", "Delhi", "Pune", "Ahmedabad"],
                "latency_range": (30, 60),
                "jitter_range": (6, 18),
                "packet_loss": (0.4, 0.7)
            },
            # Germany ISPs
            "telekom_de": {
                "prefixes": ["91.64", "217.6", "93.220", "84.138"],
                "asn": "AS3320",
                "as_name": "Deutsche Telekom AG",
                "ttl_range": (64, 128),
                "window_range": (64240, 65535),
                "mss_range": (1360, 1460),
                "cities": ["Berlin", "Munich", "Hamburg", "Frankfurt"],
                "latency_range": (10, 30),
                "jitter_range": (1, 5),
                "packet_loss": (0.1, 0.3)
            },
            "vodafone_de": {
                "prefixes": ["80.187", "91.0", "92.72", "109.42"],
                "asn": "AS3209",
                "as_name": "Vodafone GmbH",
                "ttl_range": (64, 128),
                "window_range": (64240, 65535),
                "mss_range": (1360, 1460),
                "cities": ["Düsseldorf", "Cologne", "Stuttgart"],
                "latency_range": (12, 35),
                "jitter_range": (2, 6),
                "packet_loss": (0.1, 0.3)
            },
            "o2_de": {
                "prefixes": ["82.113", "83.169", "92.224", "109.40"],
                "asn": "AS8422",
                "as_name": "O2 (Germany) GmbH & Co. OHG",
                "ttl_range": (64, 128),
                "window_range": (64240, 65535),
                "mss_range": (1360, 1460),
                "cities": ["Munich", "Nuremberg", "Leipzig"],
                "latency_range": (15, 40),
                "jitter_range": (3, 8),
                "packet_loss": (0.2, 0.4)
            },
            # TRUSTED COUNTRIES - Australia, Canada, UK, NZ, France, Netherlands, Japan, Singapore
            # Australia ISPs - VERY TRUSTED
            "telstra": {
                "prefixes": ["1.120", "1.124", "101.160", "110.144", "120.144"],
                "asn": "AS1221",
                "as_name": "Telstra Corporation Ltd",
                "ttl_range": (64, 128),
                "window_range": (64240, 65535),
                "mss_range": (1360, 1460),
                "cities": ["Sydney", "Melbourne", "Brisbane", "Perth", "Adelaide"],
                "latency_range": (10, 30),
                "jitter_range": (1, 5),
                "packet_loss": (0.1, 0.3)
            },
            "optus": {
                "prefixes": ["49.176", "49.180", "121.44", "211.28"],
                "asn": "AS4804",
                "as_name": "Optus Mobile",
                "ttl_range": (64, 128),
                "window_range": (64240, 65535),
                "mss_range": (1360, 1460),
                "cities": ["Sydney", "Melbourne", "Brisbane", "Gold Coast"],
                "latency_range": (15, 35),
                "jitter_range": (2, 6),
                "packet_loss": (0.1, 0.3)
            },
            "vodafone_au": {
                "prefixes": ["101.116", "110.174", "203.221"],
                "asn": "AS133612",
                "as_name": "Vodafone Australia",
                "ttl_range": (64, 128),
                "window_range": (64240, 65535),
                "mss_range": (1360, 1460),
                "cities": ["Sydney", "Melbourne", "Adelaide"],
                "latency_range": (18, 40),
                "jitter_range": (3, 8),
                "packet_loss": (0.2, 0.4)
            },
            "tpg": {
                "prefixes": ["27.33", "49.176", "101.160", "120.148"],
                "asn": "AS7545",
                "as_name": "TPG Telecom Limited",
                "ttl_range": (64, 128),
                "window_range": (64240, 65535),
                "mss_range": (1360, 1460),
                "cities": ["Sydney", "Melbourne", "Brisbane"],
                "latency_range": (8, 25),
                "jitter_range": (1, 4),
                "packet_loss": (0.1, 0.2)
            },
            # Canada ISPs - VERY TRUSTED
            "rogers": {
                "prefixes": ["24.114", "24.153", "64.231", "99.234"],
                "asn": "AS812",
                "as_name": "Rogers Communications Canada Inc.",
                "ttl_range": (64, 128),
                "window_range": (64240, 65535),
                "mss_range": (1360, 1460),
                "cities": ["Toronto", "Vancouver", "Montreal", "Calgary"],
                "latency_range": (12, 35),
                "jitter_range": (2, 6),
                "packet_loss": (0.1, 0.3)
            },
            "bell": {
                "prefixes": ["70.48", "99.224", "142.117", "174.88"],
                "asn": "AS577",
                "as_name": "Bell Canada",
                "ttl_range": (64, 128),
                "window_range": (64240, 65535),
                "mss_range": (1360, 1460),
                "cities": ["Toronto", "Montreal", "Ottawa", "Halifax"],
                "latency_range": (10, 30),
                "jitter_range": (1, 5),
                "packet_loss": (0.1, 0.2)
            },
            "telus": {
                "prefixes": ["24.68", "64.180", "70.66", "184.64"],
                "asn": "AS852",
                "as_name": "TELUS Communications Inc.",
                "ttl_range": (64, 128),
                "window_range": (64240, 65535),
                "mss_range": (1360, 1460),
                "cities": ["Vancouver", "Edmonton", "Calgary", "Victoria"],
                "latency_range": (15, 40),
                "jitter_range": (2, 7),
                "packet_loss": (0.1, 0.3)
            },
            "shaw": {
                "prefixes": ["24.64", "68.144", "70.64", "184.64"],
                "asn": "AS6327",
                "as_name": "Shaw Communications Inc.",
                "ttl_range": (64, 128),
                "window_range": (64240, 65535),
                "mss_range": (1360, 1460),
                "cities": ["Calgary", "Edmonton", "Vancouver", "Winnipeg"],
                "latency_range": (10, 30),
                "jitter_range": (1, 5),
                "packet_loss": (0.1, 0.2)
            },
            # UK ISPs - TRUSTED
            "bt": {
                "prefixes": ["2.24", "2.96", "86.128", "90.192"],
                "asn": "AS2856",
                "as_name": "British Telecommunications PLC",
                "ttl_range": (64, 128),
                "window_range": (64240, 65535),
                "mss_range": (1360, 1460),
                "cities": ["London", "Manchester", "Birmingham", "Glasgow"],
                "latency_range": (8, 25),
                "jitter_range": (1, 4),
                "packet_loss": (0.1, 0.2)
            },
            "ee": {
                "prefixes": ["2.120", "2.216", "82.132", "86.0"],
                "asn": "AS12576",
                "as_name": "EE Limited",
                "ttl_range": (64, 128),
                "window_range": (64240, 65535),
                "mss_range": (1360, 1460),
                "cities": ["London", "Bristol", "Leeds", "Edinburgh"],
                "latency_range": (10, 30),
                "jitter_range": (2, 5),
                "packet_loss": (0.1, 0.3)
            },
            "vodafone_uk": {
                "prefixes": ["31.52", "77.96", "92.40", "176.248"],
                "asn": "AS25135",
                "as_name": "Vodafone UK",
                "ttl_range": (64, 128),
                "window_range": (64240, 65535),
                "mss_range": (1360, 1460),
                "cities": ["London", "Newbury", "Birmingham", "Manchester"],
                "latency_range": (12, 35),
                "jitter_range": (2, 6),
                "packet_loss": (0.1, 0.3)
            },
            "three_uk": {
                "prefixes": ["2.24", "31.94", "92.233", "176.24"],
                "asn": "AS206067",
                "as_name": "Three UK",
                "ttl_range": (64, 128),
                "window_range": (64240, 65535),
                "mss_range": (1360, 1460),
                "cities": ["London", "Reading", "Liverpool"],
                "latency_range": (15, 40),
                "jitter_range": (3, 8),
                "packet_loss": (0.2, 0.4)
            },
            "sky": {
                "prefixes": ["2.120", "5.64", "78.144", "90.240"],
                "asn": "AS5607",
                "as_name": "Sky UK Limited",
                "ttl_range": (64, 128),
                "window_range": (64240, 65535),
                "mss_range": (1360, 1460),
                "cities": ["London", "Livingston", "Leeds"],
                "latency_range": (10, 28),
                "jitter_range": (1, 5),
                "packet_loss": (0.1, 0.2)
            },
            # New Zealand ISPs - TRUSTED
            "spark": {
                "prefixes": ["49.224", "49.228", "60.234", "122.56"],
                "asn": "AS4771",
                "as_name": "Spark New Zealand Trading Ltd",
                "ttl_range": (64, 128),
                "window_range": (64240, 65535),
                "mss_range": (1360, 1460),
                "cities": ["Auckland", "Wellington", "Christchurch"],
                "latency_range": (15, 40),
                "jitter_range": (2, 7),
                "packet_loss": (0.1, 0.3)
            },
            "vodafone_nz": {
                "prefixes": ["27.252", "101.98", "103.6", "111.68"],
                "asn": "AS133612",
                "as_name": "Vodafone New Zealand Limited",
                "ttl_range": (64, 128),
                "window_range": (64240, 65535),
                "mss_range": (1360, 1460),
                "cities": ["Auckland", "Wellington", "Hamilton"],
                "latency_range": (18, 45),
                "jitter_range": (3, 8),
                "packet_loss": (0.2, 0.4)
            },
            "2degrees": {
                "prefixes": ["49.224", "125.236", "182.160"],
                "asn": "AS23655",
                "as_name": "Two Degrees Mobile Ltd",
                "ttl_range": (64, 128),
                "window_range": (64240, 65535),
                "mss_range": (1360, 1460),
                "cities": ["Auckland", "Wellington", "Christchurch"],
                "latency_range": (20, 50),
                "jitter_range": (4, 10),
                "packet_loss": (0.2, 0.5)
            },
            # France ISPs - TRUSTED
            "orange_fr": {
                "prefixes": ["2.4", "80.8", "86.192", "90.0"],
                "asn": "AS3215",
                "as_name": "Orange S.A.",
                "ttl_range": (64, 128),
                "window_range": (64240, 65535),
                "mss_range": (1360, 1460),
                "cities": ["Paris", "Lyon", "Marseille", "Toulouse"],
                "latency_range": (8, 25),
                "jitter_range": (1, 4),
                "packet_loss": (0.1, 0.2)
            },
            "sfr": {
                "prefixes": ["37.160", "86.192", "90.76", "92.128"],
                "asn": "AS15557",
                "as_name": "SFR SA",
                "ttl_range": (64, 128),
                "window_range": (64240, 65535),
                "mss_range": (1360, 1460),
                "cities": ["Paris", "Lyon", "Nice", "Bordeaux"],
                "latency_range": (10, 30),
                "jitter_range": (2, 5),
                "packet_loss": (0.1, 0.3)
            },
            "bouygues": {
                "prefixes": ["5.48", "37.168", "78.224", "109.8"],
                "asn": "AS5410",
                "as_name": "Bouygues Telecom SA",
                "ttl_range": (64, 128),
                "window_range": (64240, 65535),
                "mss_range": (1360, 1460),
                "cities": ["Paris", "Nantes", "Strasbourg"],
                "latency_range": (12, 35),
                "jitter_range": (2, 6),
                "packet_loss": (0.1, 0.3)
            },
            "free_fr": {
                "prefixes": ["82.64", "88.160", "90.0", "92.168"],
                "asn": "AS12322",
                "as_name": "Free SAS",
                "ttl_range": (64, 128),
                "window_range": (64240, 65535),
                "mss_range": (1360, 1460),
                "cities": ["Paris", "Bordeaux", "Montpellier"],
                "latency_range": (8, 25),
                "jitter_range": (1, 4),
                "packet_loss": (0.1, 0.2)
            },
            # Netherlands ISPs - TRUSTED
            "kpn": {
                "prefixes": ["77.164", "80.56", "84.24", "94.208"],
                "asn": "AS1136",
                "as_name": "KPN B.V.",
                "ttl_range": (64, 128),
                "window_range": (64240, 65535),
                "mss_range": (1360, 1460),
                "cities": ["Amsterdam", "Rotterdam", "The Hague", "Utrecht"],
                "latency_range": (5, 20),
                "jitter_range": (1, 3),
                "packet_loss": (0.1, 0.2)
            },
            "vodafone_nl": {
                "prefixes": ["84.82", "86.82", "95.96", "109.36"],
                "asn": "AS1103",
                "as_name": "Vodafone Libertel B.V.",
                "ttl_range": (64, 128),
                "window_range": (64240, 65535),
                "mss_range": (1360, 1460),
                "cities": ["Amsterdam", "Eindhoven", "Maastricht"],
                "latency_range": (8, 25),
                "jitter_range": (1, 4),
                "packet_loss": (0.1, 0.2)
            },
            "tmobile_nl": {
                "prefixes": ["37.200", "77.248", "94.208", "217.62"],
                "asn": "AS13127",
                "as_name": "T-Mobile Netherlands B.V.",
                "ttl_range": (64, 128),
                "window_range": (64240, 65535),
                "mss_range": (1360, 1460),
                "cities": ["Amsterdam", "Rotterdam", "Groningen"],
                "latency_range": (10, 30),
                "jitter_range": (2, 5),
                "packet_loss": (0.1, 0.3)
            },
            # Japan ISPs - TRUSTED
            "ntt_docomo": {
                "prefixes": ["1.66", "1.72", "49.96", "126.160"],
                "asn": "AS9605",
                "as_name": "NTT DOCOMO, INC.",
                "ttl_range": (64, 128),
                "window_range": (64240, 65535),
                "mss_range": (1360, 1460),
                "cities": ["Tokyo", "Osaka", "Nagoya", "Yokohama"],
                "latency_range": (5, 20),
                "jitter_range": (1, 3),
                "packet_loss": (0.1, 0.2)
            },
            "softbank": {
                "prefixes": ["126.0", "126.72", "220.96", "220.152"],
                "asn": "AS17676",
                "as_name": "SoftBank Corp.",
                "ttl_range": (64, 128),
                "window_range": (64240, 65535),
                "mss_range": (1360, 1460),
                "cities": ["Tokyo", "Osaka", "Fukuoka", "Sapporo"],
                "latency_range": (8, 25),
                "jitter_range": (1, 4),
                "packet_loss": (0.1, 0.2)
            },
            "au_kddi": {
                "prefixes": ["1.66", "106.128", "111.97", "182.164"],
                "asn": "AS2516",
                "as_name": "KDDI CORPORATION",
                "ttl_range": (64, 128),
                "window_range": (64240, 65535),
                "mss_range": (1360, 1460),
                "cities": ["Tokyo", "Nagoya", "Kobe", "Sendai"],
                "latency_range": (8, 25),
                "jitter_range": (1, 4),
                "packet_loss": (0.1, 0.2)
            },
            # Singapore ISPs - TRUSTED
            "singtel": {
                "prefixes": ["27.104", "42.60", "116.88", "219.74"],
                "asn": "AS7473",
                "as_name": "Singapore Telecommunications Ltd",
                "ttl_range": (64, 128),
                "window_range": (64240, 65535),
                "mss_range": (1360, 1460),
                "cities": ["Singapore"],
                "latency_range": (5, 15),
                "jitter_range": (1, 3),
                "packet_loss": (0.1, 0.2)
            },
            "starhub": {
                "prefixes": ["27.125", "42.60", "101.127", "182.55"],
                "asn": "AS4657",
                "as_name": "StarHub Ltd",
                "ttl_range": (64, 128),
                "window_range": (64240, 65535),
                "mss_range": (1360, 1460),
                "cities": ["Singapore"],
                "latency_range": (5, 15),
                "jitter_range": (1, 3),
                "packet_loss": (0.1, 0.2)
            },
            "m1": {
                "prefixes": ["27.125", "42.60", "116.88", "203.125"],
                "asn": "AS17547",
                "as_name": "M1 Limited",
                "ttl_range": (64, 128),
                "window_range": (64240, 65535),
                "mss_range": (1360, 1460),
                "cities": ["Singapore"],
                "latency_range": (5, 15),
                "jitter_range": (1, 3),
                "packet_loss": (0.1, 0.2)
            },
            # Additional US ISPs
            "cox": {
                "prefixes": ["68.98", "68.230", "71.212", "76.176"],
                "asn": "AS22773",
                "as_name": "Cox Communications Inc.",
                "ttl_range": (64, 128),
                "window_range": (64240, 65535),
                "mss_range": (1360, 1460),
                "cities": ["Atlanta", "Las Vegas", "Phoenix", "San Diego"],
                "latency_range": (10, 30),
                "jitter_range": (2, 6),
                "packet_loss": (0.1, 0.3)
            },
            "charter": {
                "prefixes": ["24.14", "65.24", "72.68", "97.80"],
                "asn": "AS20115",
                "as_name": "Charter Communications",
                "ttl_range": (64, 128),
                "window_range": (64240, 65535),
                "mss_range": (1360, 1460),
                "cities": ["Stamford", "St Louis", "Denver"],
                "latency_range": (8, 25),
                "jitter_range": (1, 5),
                "packet_loss": (0.1, 0.2)
            }
        }
        return isp_configs.get(isp_name)
    
    def _generate_valid_indonesian_ip(self, isp_name: str, config: Dict[str, Any]) -> Optional[str]:
        """Generate valid Indonesian IP dengan enhanced algorithm"""
        try:
            prefix = random.choice(config["prefixes"])
            prefix_parts = prefix.split('.')
            
            # Pastikan kita punya minimal 3 parts
            while len(prefix_parts) < 3:
                prefix_parts.append(str(random.randint(0, 255)))
            
            # Generate IP parts dengan distribusi realistis
            if len(prefix_parts) == 3:
                # Format: X.X.X.Y
                fourth = self._generate_realistic_fourth_octet(isp_name)
                ip = f"{'.'.join(prefix_parts)}.{fourth}"
            elif len(prefix_parts) == 4:
                # Format sudah lengkap
                ip = '.'.join(prefix_parts)
            else:
                # Handle format lainnya
                while len(prefix_parts) < 4:
                    prefix_parts.append(str(random.randint(0, 255)))
                ip = '.'.join(prefix_parts[:4])
            
            # Validasi final
            if self._validate_ip_format_enhanced(ip):
                return ip
            
            return None
            
        except Exception as e:
            print(f"{merah}    Error generating IP for {isp_name}: {e}{reset}")
            return None
    
    def _generate_realistic_fourth_octet(self, isp_name: str) -> int:
        """Generate fourth octet yang realistis berdasarkan ISP"""
        # Hindari angka khusus berdasarkan ISP
        if isp_name == "telkomsel":
            avoid = [0, 1, 255, 254, 128, 192, 224]
        elif isp_name == "indosat":
            avoid = [0, 255, 127, 63, 31, 15, 7]
        elif isp_name == "xl":
            avoid = [0, 255, 192, 168, 10, 172, 169]
        else:
            avoid = [0, 1, 2, 255, 254, 253, 128]
        
        while True:
            octet = random.randint(2, 253)
            if octet not in avoid:
                # Tambahkan bias berdasarkan ISP
                if isp_name in ["telkomsel", "indosat"]:
                    # Bias untuk IP residential (biasanya 10-200)
                    if 10 <= octet <= 200:
                        return octet
                else:
                    return octet
    
    def _validate_ip_format_enhanced(self, ip: str) -> bool:
        """Ultra-enhanced IP format validation - anti rate limit and IP block"""
        try:
            # Basic format check
            parts = ip.split('.')
            if len(parts) != 4:
                return False
            
            # Check each octet
            for part in parts:
                if not part.isdigit():
                    return False
                
                num = int(part)
                if num < 0 or num > 255:
                    return False
            
            # Check reserved addresses
            ip_obj = ipaddress.ip_address(ip)
            
            if ip_obj.is_private:
                return False
            
            if ip_obj.is_reserved:
                return False
            
            if ip_obj.is_loopback:
                return False
            
            if ip_obj.is_multicast:
                return False
            
            if ip_obj.is_link_local:
                return False
            
            # ===== ULTRA BLACKLIST CHECK =====
            # Known datacenter/VPN/proxy IP ranges that Instagram blocks
            blacklisted_prefixes = [
                # AWS
                "3.", "13.", "15.", "18.", "34.", "35.", "43.", "44.", "46.", "50.", "52.", "54.", "63.", "65.", "75.", "76.", "99.", "100.", "107.", "108.", "174.", "175.", "176.", "177.", "184.",
                # Google Cloud
                "8.8.", "8.34.", "8.35.", "23.236.", "23.251.", "34.64.", "34.65.", "34.66.", "34.67.", "34.68.", "34.69.", "34.70.", "34.71.", "35.184.", "35.185.", "35.186.", "35.187.", "35.188.", "35.189.", "35.190.", "35.191.", "35.192.", "35.193.", "35.194.", "35.195.", "35.196.", "35.197.", "35.198.", "35.199.", "35.200.", "35.201.", "35.202.", "35.203.", "35.204.", "35.205.", "35.206.", "35.207.", "35.208.", "35.209.", "35.210.", "35.211.", "35.212.", "35.213.", "35.214.", "35.215.", "35.216.", "35.217.", "35.218.", "35.219.", "35.220.", "104.154.", "104.155.", "104.196.", "104.197.", "104.198.", "104.199.", "130.211.", "146.148.", "199.192.", "199.223.",
                # Azure
                "13.64.", "13.65.", "13.66.", "13.67.", "13.68.", "13.69.", "13.70.", "13.71.", "13.72.", "13.73.", "13.74.", "13.75.", "13.76.", "13.77.", "13.78.", "13.79.", "13.80.", "13.81.", "13.82.", "13.83.", "13.84.", "13.85.", "13.86.", "13.87.", "13.88.", "13.89.", "13.90.", "13.91.", "13.92.", "13.93.", "13.94.", "13.95.", "20.", "23.96.", "23.97.", "23.98.", "23.99.", "23.100.", "23.101.", "23.102.", "40.64.", "40.65.", "40.66.", "40.67.", "40.68.", "40.69.", "40.70.", "40.71.", "40.72.", "40.73.", "40.74.", "40.75.", "40.76.", "40.77.", "40.78.", "40.79.", "40.80.", "40.81.", "40.82.", "40.83.", "40.84.", "40.85.", "40.86.", "40.87.", "40.88.", "40.89.", "40.90.", "40.91.", "40.92.", "40.112.", "40.113.", "40.114.", "40.115.", "40.116.", "40.117.", "40.118.", "40.119.", "40.120.", "40.121.", "40.122.", "40.123.", "40.124.", "40.125.", "40.126.", "40.127.", "51.104.", "51.105.", "52.", "65.52.", "70.37.", "104.40.", "104.41.", "104.42.", "104.43.", "104.44.", "104.45.", "104.46.", "104.47.", "104.208.", "104.209.", "104.210.", "104.211.", "104.212.", "104.213.", "104.214.", "104.215.",
                # DigitalOcean
                "45.55.", "64.225.", "67.205.", "68.183.", "104.131.", "104.236.", "107.170.", "128.199.", "134.209.", "138.68.", "138.197.", "139.59.", "142.93.", "143.198.", "144.126.", "146.185.", "157.230.", "159.65.", "159.89.", "159.203.", "161.35.", "162.243.", "164.90.", "165.22.", "165.227.", "167.71.", "167.99.", "167.172.", "174.138.", "178.62.", "178.128.", "188.166.", "192.34.", "192.81.", "192.241.", "198.199.", "198.211.", "203.161.", "206.81.", "206.189.", "207.154.", "209.97.",
                # Linode
                "45.33.", "45.56.", "45.79.", "50.116.", "66.228.", "69.164.", "72.14.", "74.207.", "85.90.", "96.126.", "97.107.", "139.162.", "170.187.", "172.104.", "172.105.", "178.79.", "192.155.", "198.58.", "198.74.", "207.192.",
                # Vultr
                "45.32.", "45.63.", "45.76.", "45.77.", "66.42.", "78.141.", "80.240.", "95.179.", "104.156.", "104.207.", "104.238.", "108.61.", "136.244.", "140.82.", "141.164.", "144.202.", "149.28.", "149.248.", "155.138.", "167.179.", "199.247.", "207.246.", "208.167.", "209.222.", "216.128.", "217.163.",
                # OVH
                "51.68.", "51.75.", "51.77.", "51.79.", "51.81.", "51.83.", "51.89.", "51.91.", "51.161.", "51.178.", "51.195.", "51.210.", "51.222.", "54.36.", "54.37.", "54.38.", "54.39.", "66.70.", "79.137.", "91.121.", "92.222.", "94.23.", "135.125.", "137.74.", "139.99.", "142.44.", "144.217.", "145.239.", "147.135.", "149.56.", "151.80.", "158.69.", "162.19.", "164.132.", "167.114.", "176.31.", "178.32.", "178.33.", "185.92.", "188.165.", "192.95.", "193.70.", "198.27.", "198.50.", "198.100.", "198.245.",
                # Hetzner
                "5.9.", "23.88.", "46.4.", "49.12.", "49.13.", "78.46.", "78.47.", "85.10.", "88.99.", "88.198.", "91.107.", "94.130.", "95.216.", "95.217.", "116.202.", "116.203.", "128.140.", "135.181.", "136.243.", "138.201.", "142.132.", "144.76.", "148.251.", "157.90.", "159.69.", "162.55.", "167.233.", "168.119.", "176.9.", "178.63.", "188.40.", "195.201.", "213.133.", "213.239.",
                # VPN Providers
                "31.13.", "37.120.", "45.9.", "62.102.", "62.133.", "68.235.", "77.81.", "80.67.", "81.171.", "84.17.", "85.203.", "86.106.", "89.35.", "89.36.", "89.37.", "89.38.", "89.40.", "89.41.", "89.42.", "89.44.", "89.45.", "89.46.", "91.90.", "91.203.", "91.207.", "94.140.", "103.75.", "103.86.", "103.108.", "104.153.", "104.167.", "107.181.", "109.70.", "109.201.", "128.90.", "129.227.", "138.199.", "141.98.", "141.255.", "146.70.", "149.88.", "154.47.", "169.150.", "172.83.", "172.86.", "172.93.", "172.98.", "172.111.", "176.67.", "178.17.", "178.73.", "179.43.", "181.214.", "185.56.", "185.65.", "185.73.", "185.93.", "185.107.", "185.156.", "185.159.", "185.181.", "185.189.", "185.203.", "185.213.", "185.220.", "185.230.", "185.232.", "185.236.", "185.242.", "185.244.", "185.246.", "185.248.", "186.179.", "188.214.", "191.96.", "193.9.", "193.27.", "193.32.", "193.37.", "193.56.", "193.148.", "193.182.", "194.110.", "194.187.", "195.154.", "195.181.", "195.206.", "196.240.", "198.8.", "198.16.", "199.19.", "203.12.", "203.23.", "206.217.", "207.244.", "209.95.", "212.102.", "213.152.", "216.24.", "217.138.", "217.146.", "217.182.",
                # Proxy/Hosting known for abuse
                "23.81.", "23.82.", "23.83.", "23.108.", "23.226.", "23.227.", "23.228.", "23.229.", "23.234.", "23.235.", "23.238.", "23.239.", "23.254.", "37.9.", "37.19.", "37.44.", "37.48.", "37.59.", "37.187.", "45.8.", "45.10.", "45.11.", "45.12.", "45.14.", "45.15.", "45.41.", "45.42.", "45.58.", "45.61.", "45.62.", "45.66.", "45.67.", "45.72.", "45.80.", "45.81.", "45.82.", "45.83.", "45.84.", "45.86.", "45.87.", "45.88.", "45.89.", "45.90.", "45.92.", "45.93.", "45.94.", "45.95.", "45.128.", "45.129.", "45.130.", "45.131.", "45.132.", "45.133.", "45.134.", "45.135.", "45.136.", "45.137.", "45.138.", "45.139.", "45.140.", "45.141.", "45.142.", "45.143.", "45.144.", "45.145.", "45.146.", "45.147.", "45.148.", "45.149.", "45.150.", "45.151.", "45.152.", "45.153.", "45.154.", "45.155.", "45.156.", "45.157.", "45.158.", "45.159.",
            ]
            
            # Check if IP starts with any blacklisted prefix
            for prefix in blacklisted_prefixes:
                if ip.startswith(prefix):
                    return False
            
            # ===== RESIDENTIAL IP PATTERN CHECK =====
            # Instagram is less suspicious of IPs with natural residential patterns
            first_octet = int(parts[0])
            fourth_octet = int(parts[3])
            
            # Avoid datacenter-typical first octets
            datacenter_first_octets = [3, 8, 13, 15, 18, 20, 23, 34, 35, 40, 43, 44, 45, 46, 50, 51, 52, 54, 63, 65, 75, 76, 99, 100, 104, 107, 108, 128, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 151, 155, 157, 158, 159, 161, 162, 164, 165, 167, 168, 170, 172, 174, 175, 176, 177, 178, 184, 185, 188, 192, 193, 194, 195, 196, 198, 199, 203, 206, 207, 208, 209, 213, 216, 217]
            if first_octet in datacenter_first_octets:
                # Additional check - some residential IPs use these octets
                # Only block if combined with suspicious patterns
                if fourth_octet in [0, 1, 2, 3, 4, 5, 254, 255] or fourth_octet % 10 == 0:
                    return False
            
            # Check for suspicious patterns - server IPs often have round numbers
            suspicious_patterns = [
                ip.endswith('.0'),
                ip.endswith('.255'),
                ip.endswith('.1'),
                ip.endswith('.254'),
                all(p == parts[0] for p in parts),  # All same
                parts[3] in ['0', '255', '1', '254'],
                # Round number patterns typical of server allocations
                fourth_octet % 50 == 0,
                fourth_octet % 100 == 0,
                # Sequential patterns (e.g., .10, .20, .30)
                fourth_octet % 10 == 0 and fourth_octet < 100,
            ]
            
            if any(suspicious_patterns):
                return False
            
            # ===== RESIDENTIAL-LIKE FOURTH OCTET =====
            # Real residential IPs tend to have "random-looking" fourth octets
            # Avoid: 0-10, 250-255, multiples of 10, multiples of 50
            bad_fourth_octets = list(range(0, 11)) + list(range(250, 256)) + [x for x in range(0, 256) if x % 50 == 0]
            if fourth_octet in bad_fourth_octets:
                return False
            
            return True
            
        except Exception:
            return False
    
    def _anti_blacklist_check(self, ip: str) -> bool:
        """Check if IP is likely to be blacklisted by Instagram"""
        try:
            # Use the enhanced validation as the base check
            if not self._validate_ip_format_enhanced(ip):
                return False
            
            # Additional blacklist check for known problematic IPs
            if ip in self.blacklisted_ips:
                return False
            
            # Check if IP was recently used (avoid reuse within 1 hour)
            if hasattr(self, '_recently_used_ips'):
                if ip in self._recently_used_ips:
                    last_used = self._recently_used_ips.get(ip, 0)
                    if time.time() - last_used < 3600:  # 1 hour cooldown
                        return False
            
            return True
            
        except Exception:
            return False
    
    def _generate_ultra_fresh_residential_ip(self, isp_name: str, config: Dict[str, Any]) -> Optional[str]:
        """Generate ultra-fresh residential IP that passes all anti-bot checks"""
        max_attempts = 50
        
        for attempt in range(max_attempts):
            try:
                prefix = random.choice(config["prefixes"])
                prefix_parts = prefix.split('.')
                
                # Generate remaining octets
                while len(prefix_parts) < 3:
                    prefix_parts.append(str(random.randint(1, 254)))
                
                # Generate residential-looking fourth octet
                # Avoid: 0-10, 250-255, round numbers, sequential patterns
                fourth_octet = self._generate_residential_fourth_octet()
                
                ip = f"{'.'.join(prefix_parts[:3])}.{fourth_octet}"
                
                # Validate the generated IP
                if self._validate_ip_format_enhanced(ip):
                    return ip
                    
            except Exception:
                continue
        
        return None
    
    def _create_enhanced_ip_profile(self, ip: str, config: Dict[str, Any], isp_name: str) -> Dict[str, Any]:
        """Create enhanced IP profile dengan network type yang BENAR - FIXED"""
        city = random.choice(config["cities"])
        city_coords = self._get_city_coordinates_enhanced(city)
        
        # Determine connection type berdasarkan ISP - FIXED
        connection_type = self._get_connection_type_for_isp(isp_name)
        network_type = self._get_network_type_for_isp(isp_name, connection_type)
        
        # Generate network metrics berdasarkan connection type - FIXED
        if connection_type == "mobile":
            latency = random.uniform(15, 45)
            jitter = random.uniform(2, 10)
            signal_strength = random.randint(-70, -50)
            bandwidth = random.uniform(10, 100)
        else:  # wifi/fiber
            latency = random.uniform(5, 20)
            jitter = random.uniform(1, 5)
            signal_strength = random.randint(-40, -20)
            bandwidth = random.uniform(50, 500)
        
        packet_loss = random.uniform(*config["packet_loss"])
        
        # Generate TCP parameters
        ttl = random.randint(*config["ttl_range"])
        window_size = random.randint(*config["window_range"])
        mss = random.randint(*config["mss_range"])
        
        # Generate session-specific parameters
        initial_seq = random.randint(0, 2**32 - 1)
        timestamp_val = random.randint(0, 2**32 - 1)
        timestamp_echo = random.randint(0, 2**32 - 1)
        lat_variation = random.uniform(-0.01, 0.01)
        lon_variation = random.uniform(-0.01, 0.01)
        
        location = {
            "city": city,
            "province": self._get_province_for_city_enhanced(city),
            "country": "Indonesia",
            "country_code": "ID",
            "latitude": round(city_coords["lat"] + lat_variation, 6),
            "longitude": round(city_coords["lon"] + lon_variation, 6),
            "timezone": "Asia/Jakarta",
            "accuracy": random.uniform(50, 500),
            "isp": isp_name,
            "asn": config["asn"],
            "as_name": config.get("as_name", ""),
            "network_type": network_type,  # FIXED: menggunakan mapping yang benar
            "connection_type": connection_type,  # FIXED: mobile/wifi
            "carrier": isp_name.upper() if connection_type == "mobile" else "WiFi",
            "mcc": "510",  # Indonesia
            "mnc": self._get_mnc_for_isp(isp_name) if connection_type == "mobile" else ""
        }
        
        # Generate device fingerprint berdasarkan connection type - FIXED
        device_fingerprint = self._generate_device_fingerprint_for_ip(isp_name, connection_type)
        
        return {
            "ip": ip,
            "type": "residential",
            "isp": isp_name,
            "asn": config["asn"],
            "connection_type": connection_type,  # FIXED: simpan connection type
            "location": location,
            "network_metrics": {
                "latency_ms": round(latency, 2),
                "jitter_ms": round(jitter, 2),
                "packet_loss_percent": round(packet_loss, 2),
                "bandwidth_mbps": round(bandwidth, 2),
                "connection_type": connection_type,  # FIXED
                "network_type": network_type,  # FIXED
                "signal_strength": signal_strength
            },
            "tcp_parameters": {
                "ttl": ttl,
                "window_size": window_size,
                "mss": mss,
                "initial_seq": initial_seq,
                "timestamp_val": timestamp_val,
                "timestamp_echo": timestamp_echo,
                "sack_permitted": random.choice([True, False]),
                "window_scaling": random.randint(0, 14),
                "timestamps": True,
                "nop": random.choice([True, False])
            },
            "device_fingerprint": device_fingerprint,
            "timestamp": int(time.time()),
            "generation_id": f"gen_{int(time.time())}_{random.randint(1000, 9999)}",
            "usage_count": 0,
            "last_used": 0,
            "success_count": 0,
            "fail_count": 0,
            "proxy_detected": False,
            "vpn_detected": False,
            "datacenter_detected": False,
            "health_score": random.randint(85, 95),
            "reliability": random.uniform(0.8, 0.98),
            "last_validated": time.time(),
            "session_id": None,
            "rotation_count": 0
        }
    
    def _get_city_coordinates_enhanced(self, city: str) -> Dict[str, float]:
        """Enhanced city coordinates dengan lebih banyak kota Indonesia dan internasional"""
        coordinates = {
            # Indonesia
            "Jakarta": {"lat": -6.2088, "lon": 106.8456},
            "Surabaya": {"lat": -7.2575, "lon": 112.7521},
            "Bandung": {"lat": -6.9175, "lon": 107.6191},
            "Medan": {"lat": 3.5952, "lon": 98.6722},
            "Bali": {"lat": -8.4095, "lon": 115.1889},
            "Makassar": {"lat": -5.1477, "lon": 119.4327},
            "Semarang": {"lat": -6.9667, "lon": 110.4167},
            "Palembang": {"lat": -2.9909, "lon": 104.7566},
            "Yogyakarta": {"lat": -7.7956, "lon": 110.3695},
            "Balikpapan": {"lat": -1.2680, "lon": 116.8285},
            "Bekasi": {"lat": -6.2383, "lon": 106.9756},
            "Tangerang": {"lat": -6.1783, "lon": 106.6319},
            "Depok": {"lat": -6.4025, "lon": 106.7942},
            "Batam": {"lat": 1.0452, "lon": 104.0305},
            "Samarinda": {"lat": -0.5022, "lon": 117.1536},
            "Manado": {"lat": 1.4748, "lon": 124.8421},
            "Lombok": {"lat": -8.5657, "lon": 116.3513},
            "Padang": {"lat": -0.9471, "lon": 100.4172},
            "Lampung": {"lat": -5.4291, "lon": 105.2620},
            "Malang": {"lat": -7.9666, "lon": 112.6326},
            "Surakarta": {"lat": -7.5755, "lon": 110.8243},
            "Bintan": {"lat": 1.1368, "lon": 104.4255},
            "Karimun": {"lat": 0.8052, "lon": 103.4192},
            "Pekanbaru": {"lat": 0.5071, "lon": 101.4478},
            "Banjarmasin": {"lat": -3.3199, "lon": 114.5908},
            "Pontianak": {"lat": -0.0263, "lon": 109.3425},
            "Cirebon": {"lat": -6.7320, "lon": 108.5523},
            "Serang": {"lat": -6.1200, "lon": 106.1503},
            "Tegal": {"lat": -6.8667, "lon": 109.1333},
            "Bogor": {"lat": -6.5971, "lon": 106.8060},
            # US Cities
            "New York": {"lat": 40.7128, "lon": -74.0060},
            "Los Angeles": {"lat": 34.0522, "lon": -118.2437},
            "Chicago": {"lat": 41.8781, "lon": -87.6298},
            "Houston": {"lat": 29.7604, "lon": -95.3698},
            "Miami": {"lat": 25.7617, "lon": -80.1918},
            "Dallas": {"lat": 32.7767, "lon": -96.7970},
            "Atlanta": {"lat": 33.7490, "lon": -84.3880},
            "San Francisco": {"lat": 37.7749, "lon": -122.4194},
            "Seattle": {"lat": 47.6062, "lon": -122.3321},
            "Bellevue": {"lat": 47.6101, "lon": -122.2015},
            "Las Vegas": {"lat": 36.1699, "lon": -115.1398},
            "Denver": {"lat": 39.7392, "lon": -104.9903},
            "Phoenix": {"lat": 33.4484, "lon": -112.0740},
            "Philadelphia": {"lat": 39.9526, "lon": -75.1652},
            "San Jose": {"lat": 37.3382, "lon": -121.8863},
            "Stamford": {"lat": 41.0534, "lon": -73.5387},
            "St Louis": {"lat": 38.6270, "lon": -90.1994},
            "Tampa": {"lat": 27.9506, "lon": -82.4572},
            "Austin": {"lat": 30.2672, "lon": -97.7431},
            # Brazil Cities
            "São Paulo": {"lat": -23.5505, "lon": -46.6333},
            "Rio de Janeiro": {"lat": -22.9068, "lon": -43.1729},
            "Brasília": {"lat": -15.7942, "lon": -47.8822},
            "Salvador": {"lat": -12.9714, "lon": -38.5014},
            "Curitiba": {"lat": -25.4290, "lon": -49.2671},
            "Belo Horizonte": {"lat": -19.9167, "lon": -43.9345},
            "Porto Alegre": {"lat": -30.0346, "lon": -51.2177},
            # India Cities
            "Mumbai": {"lat": 19.0760, "lon": 72.8777},
            "Delhi": {"lat": 28.6139, "lon": 77.2090},
            "Bangalore": {"lat": 12.9716, "lon": 77.5946},
            "Hyderabad": {"lat": 17.3850, "lon": 78.4867},
            "Chennai": {"lat": 13.0827, "lon": 80.2707},
            "Kolkata": {"lat": 22.5726, "lon": 88.3639},
            "Pune": {"lat": 18.5204, "lon": 73.8567},
            "Ahmedabad": {"lat": 23.0225, "lon": 72.5714},
            # Germany Cities
            "Berlin": {"lat": 52.5200, "lon": 13.4050},
            "Munich": {"lat": 48.1351, "lon": 11.5820},
            "Hamburg": {"lat": 53.5511, "lon": 9.9937},
            "Frankfurt": {"lat": 50.1109, "lon": 8.6821},
            "Düsseldorf": {"lat": 51.2277, "lon": 6.7735},
            "Cologne": {"lat": 50.9375, "lon": 6.9603},
            "Stuttgart": {"lat": 48.7758, "lon": 9.1829},
            "Nuremberg": {"lat": 49.4521, "lon": 11.0767},
            "Leipzig": {"lat": 51.3397, "lon": 12.3731}
        }
        return coordinates.get(city, coordinates["Jakarta"])
    
    def _get_province_for_city_enhanced(self, city: str) -> str:
        """Enhanced province mapping"""
        province_map = {
            "Jakarta": "DKI Jakarta", "Surabaya": "Jawa Timur",
            "Bandung": "Jawa Barat", "Medan": "Sumatera Utara",
            "Bali": "Bali", "Makassar": "Sulawesi Selatan",
            "Semarang": "Jawa Tengah", "Palembang": "Sumatera Selatan",
            "Yogyakarta": "DI Yogyakarta", "Balikpapan": "Kalimantan Timur",
            "Bekasi": "Jawa Barat", "Tangerang": "Banten",
            "Depok": "Jawa Barat", "Batam": "Kepulauan Riau",
            "Samarinda": "Kalimantan Timur", "Manado": "Sulawesi Utara",
            "Lombok": "Nusa Tenggara Barat", "Padang": "Sumatera Barat",
            "Lampung": "Lampung", "Malang": "Jawa Timur",
            "Surakarta": "Jawa Tengah", "Bintan": "Kepulauan Riau",
            "Karimun": "Kepulauan Riau", "Pekanbaru": "Riau",
            "Banjarmasin": "Kalimantan Selatan", "Pontianak": "Kalimantan Barat",
            "Cirebon": "Jawa Barat", "Serang": "Banten",
            "Tegal": "Jawa Tengah", "Bogor": "Jawa Barat"
        }
        return province_map.get(city, "DKI Jakarta")
    
    def _get_mnc_for_isp(self, isp: str) -> str:
        """Get MNC untuk ISP Indonesia dan internasional"""
        mnc_map = {
            # Indonesia
            "telkomsel": "10",
            "indosat": "01",
            "xl": "11",
            "tri": "89",
            "smartfren": "28",
            "biznet": "20",
            "cbn": "21",
            # US
            "verizon": "480",
            "att": "410",
            "tmobile": "260",
            # Brazil
            "claro_br": "05",
            "vivo_br": "06",
            "tim_br": "02",
            # India
            "jio": "862",
            "airtel_in": "10",
            "vi_in": "20",
            # Germany
            "telekom_de": "01",
            "vodafone_de": "02",
            "o2_de": "03"
        }
        return mnc_map.get(isp, "99")
    
    def _get_mcc_for_isp(self, isp: str) -> str:
        """Get MCC untuk ISP Indonesia dan internasional"""
        mcc_map = {
            # Indonesia (MCC 510)
            "telkomsel": "510",
            "indosat": "510",
            "xl": "510",
            "tri": "510",
            "smartfren": "510",
            "biznet": "510",
            "cbn": "510",
            # US (MCC 310/311)
            "verizon": "311",
            "att": "310",
            "tmobile": "310",
            "comcast": "310",
            "spectrum": "310",
            # Brazil (MCC 724)
            "claro_br": "724",
            "vivo_br": "724",
            "tim_br": "724",
            # India (MCC 404/405)
            "jio": "405",
            "airtel_in": "404",
            "vi_in": "404",
            # Germany (MCC 262)
            "telekom_de": "262",
            "vodafone_de": "262",
            "o2_de": "262"
        }
        return mcc_map.get(isp, "510")
    
    def _generate_device_fingerprint_for_ip(self, isp: str, connection_type: str) -> Dict[str, Any]:
        """Generate device fingerprint berdasarkan ISP dan connection type - FIXED"""
        if connection_type == "mobile":
            # Mobile devices untuk ISP cellular
            if isp in ["telkomsel", "indosat"]:
                # High-end devices untuk ISP premium
                devices = [
                    {"brand": "Samsung", "model": "SM-S928B", "name": "Galaxy S24 Ultra"},
                    {"brand": "Apple", "model": "iPhone16,2", "name": "iPhone 16 Pro Max"},
                    {"brand": "Xiaomi", "model": "23116PN5BC", "name": "Xiaomi 14 Pro"},
                    {"brand": "Google", "model": "Pixel 9 Pro", "name": "Pixel 9 Pro"}
                ]
            else:
                # Mid-range devices untuk ISP lainnya
                devices = [
                    {"brand": "Samsung", "model": "SM-A546B", "name": "Galaxy A54"},
                    {"brand": "Xiaomi", "model": "2211133G", "name": "Redmi Note 13"},
                    {"brand": "Vivo", "model": "V2244", "name": "Vivo Y100"},
                    {"brand": "OPPO", "model": "CPH2525", "name": "OPPO A78"}
                ]
        else:
            # WiFi/Fiber devices (bisa tablet/laptop)
            devices = [
                {"brand": "Samsung", "model": "SM-T970", "name": "Galaxy Tab S7+"},
                {"brand": "Apple", "model": "iPad14,1", "name": "iPad Air 5"},
                {"brand": "Lenovo", "model": "TB-X6E6F", "name": "Tab M10"},
                {"brand": "Xiaomi", "model": "23043RP34C", "name": "Xiaomi Pad 6"}
            ]
        
        device = random.choice(devices)
        
        return {
            "brand": device["brand"],
            "model": device["model"],
            "name": device["name"],
            "connection_type": connection_type,  # FIXED: simpan connection type
            "android_version": random.choice(["13", "14", "15"]),
            "chrome_version": f"{random.randint(130, 135)}.0.{random.randint(6000, 7000)}.{random.randint(0, 99)}",
            "webview_version": f"{random.randint(110, 120)}.0.{random.randint(5000, 6000)}",
            "build_id": f"UP1A.{random.randint(230101, 231231)}.{random.randint(100, 999)}",
            "kernel_version": f"5.15.{random.randint(100, 120)}-android{random.randint(12, 15)}",
            "screen_resolution": random.choice(["1080x2400", "1440x3200", "1170x2532"]),
            "dpi": random.choice([420, 440, 460, 480, 500]),
            "device_id": f"android-{hashlib.sha256(str(time.time()).encode()).hexdigest()[:16]}",
            "advertising_id": str(uuid.uuid4()).upper().replace('-', ''),
            "android_id": f"{random.getrandbits(64):016x}"
        }
    
    def get_fresh_ip_config(self, session_id: str = None, min_health: int = 80, connection_type: str = "mobile", country: str = "random") -> Dict[str, Any]:
        """Get ultra-fresh IP configuration using next-gen stealth system with RANDOM COUNTRY support"""
        print(f"{cyan}🌐  Getting fresh IP config for session {session_id[:8] if session_id else 'new'} (connection: {connection_type}, country: {country})...{reset}")
        
        # ===== USE ULTRA STEALTH IP GENERATOR WITH COUNTRY =====
        try:
            ultra_generator = UltraStealthIPGenerator2025()
            ip_type = "mobile" if connection_type == "mobile" else "residential"
            
            # Generate ultra-stealth IP for specific country
            ultra_ip_config = ultra_generator.generate_ultra_stealth_ip(ip_type=ip_type, country=country)
            
            if ultra_ip_config and ultra_ip_config.get("ip"):
                # Convert to standard format
                config = self._convert_ultra_stealth_to_standard(ultra_ip_config, session_id)
                print(f"{hijau}✅  Selected IP: {ultra_ip_config['ip']} ({ultra_ip_config['isp']}) [{ultra_ip_config['country']}] - Health: {ultra_ip_config['health_score']}{reset}")
                return config
        except Exception as e:
            print(f"{kuning}    Ultra stealth generator error: {e}, falling back...{reset}")
        
        # ===== FALLBACK TO ORIGINAL SYSTEM =====
        # Refresh pool jika diperlukan
        self._refresh_ip_pool_if_needed()
        
        if not self.ip_pool:
            print(f"{merah}    IP pool empty, generating emergency batch...{reset}")
            self._generate_emergency_ip_batch()
        
        # Filter IP berdasarkan connection type jika perlu
        filtered_ips = self.ip_pool
        
        if connection_type:
            filtered_ips = [
                ip_info for ip_info in self.ip_pool
                if ip_info.get("connection_type", "mobile") == connection_type
            ]
        
        # Filter IP yang sehat
        healthy_ips = [
            ip_info for ip_info in filtered_ips
            if ip_info.get("health_score", 0) >= min_health and
            not ip_info.get("proxy_detected", False) and
            not ip_info.get("blacklisted", False) and
            ip_info.get("usage_count", 0) < 3  # Batasi penggunaan
        ]
        
        if not healthy_ips:
            print(f"{merah}    No healthy IPs found, relaxing criteria...{reset}")
            healthy_ips = [
                ip_info for ip_info in self.ip_pool
                if ip_info.get("health_score", 0) >= 60
            ]
        
        if not healthy_ips:
            print(f"{merah}    No IPs available, creating new batch...{reset}")
            self._generate_fresh_ip_batch_enhanced()
            healthy_ips = [ip_info for ip_info in self.ip_pool if ip_info.get("health_score", 0) >= 60]
        
        if healthy_ips:
            # Pilih IP dengan weighted random berdasarkan health score
            weights = [ip.get("health_score", 60) for ip in healthy_ips]
            selected_ip_info = random.choices(healthy_ips, weights=weights, k=1)[0]
            
            # Update usage
            selected_ip_info["usage_count"] = selected_ip_info.get("usage_count", 0) + 1
            selected_ip_info["last_used"] = time.time()
            
            if session_id:
                selected_ip_info["session_id"] = session_id
                self.session_ip_map[session_id] = selected_ip_info["ip"]
            
            # Build enhanced config
            config = self._build_enhanced_ip_config(selected_ip_info, session_id)
            
            print(f"{hijau}✅  Selected IP: {selected_ip_info['ip']} ({selected_ip_info['isp']}) - Health: {selected_ip_info['health_score']}{reset}")
            return config
        
        # Ultimate fallback
        print(f"{merah}🚨  Using ultimate fallback IP{reset}")
        return self._get_fallback_ip_config_enhanced(session_id)
    
    def _convert_ultra_stealth_to_standard(self, ultra_config: Dict[str, Any], session_id: str = None) -> Dict[str, Any]:
        """Convert ultra stealth IP config to standard format"""
        device = ultra_config.get("device", {})
        location = ultra_config.get("location", {})
        network = ultra_config.get("network_metrics", {})
        tcp = ultra_config.get("tcp_fingerprint", {})
        
        # Build headers based on device
        if device.get("type") == "mobile":
            if device.get("os") == "iOS":
                user_agent = f"Mozilla/5.0 (iPhone; CPU iPhone OS {device.get('os_version', '17.4').replace('.', '_')} like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/{device.get('browser_version', '17.4')} Mobile/15E148 Safari/604.1"
            else:
                user_agent = f"Mozilla/5.0 (Linux; Android {device.get('os_version', '14')}; {device.get('model', 'Pixel 8')}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{device.get('browser_version', '122.0.6261')} Mobile Safari/537.36"
        else:
            if device.get("os") == "macOS":
                user_agent = f"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{device.get('browser_version', '122.0.6261.112')} Safari/537.36"
            else:
                user_agent = f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{device.get('browser_version', '122.0.6261.112')} Safari/537.36"
        
        return {
            "ip": ultra_config["ip"],
            "type": ultra_config.get("type", "residential"),
            "isp": ultra_config["isp"],
            "isp_name": ultra_config.get("isp_name", ultra_config["isp"]),
            "asn": ultra_config.get("asn", ""),
            "as_name": ultra_config.get("as_name", ""),
            "connection_type": ultra_config.get("connection_type", "mobile"),
            "network_type": ultra_config.get("network_type", "WiFi"),
            "country": ultra_config.get("country", "US"),
            "country_name": ultra_config.get("country_name", "United States"),
            "location": {
                "city": location.get("city", ""),
                "country": ultra_config.get("country", "US"),
                "country_code": ultra_config.get("country", "US"),
                "latitude": location.get("latitude", 0),
                "longitude": location.get("longitude", 0),
                "timezone": ultra_config.get("timezone", "America/New_York"),
                "accuracy": location.get("accuracy", 100),
                "isp": ultra_config["isp"],
                "asn": ultra_config.get("asn", ""),
            },
            "network_metrics": {
                "latency_ms": network.get("latency_ms", 30),
                "jitter_ms": network.get("jitter_ms", 5),
                "packet_loss_percent": network.get("packet_loss_percent", 0.1),
                "bandwidth_mbps": network.get("bandwidth_mbps", 100),
                "signal_strength": network.get("signal_strength", -50),
            },
            "tcp_parameters": {
                "ttl": tcp.get("ttl", 64),
                "window_size": tcp.get("window_size", 65535),
                "mss": tcp.get("mss", 1460),
                "window_scaling": tcp.get("window_scaling", 10),
                "timestamps": tcp.get("timestamps", True),
                "sack_permitted": tcp.get("sack_permitted", True),
            },
            "device": device,
            "headers": {
                "User-Agent": user_agent,
                "Accept-Language": ultra_config.get("language", "en-US") + ",en;q=0.9",
            },
            "language": ultra_config.get("language", "en-US"),
            "locale": ultra_config.get("locale", "en_US"),
            "timezone": ultra_config.get("timezone", "America/New_York"),
            "health_score": ultra_config.get("health_score", 95),
            "trust_score": ultra_config.get("trust_score", 0.95),
            "generation_method": "ultra_stealth_v2",
            "session_id": session_id,
            "timestamp": time.time(),
        }
    
    def _refresh_ip_pool_if_needed(self):
        """Refresh IP pool dengan enhanced logic"""
        current_time = time.time()
        
        # Hitung statistik pool
        total_ips = len(self.ip_pool)
        healthy_ips = sum(1 for ip in self.ip_pool if ip.get("health_score", 0) >= 70)
        fresh_ips = sum(1 for ip in self.ip_pool if current_time - ip.get("timestamp", 0) < 600)
        
        refresh_needed = (
            total_ips < 10 or
            healthy_ips < 5 or
            fresh_ips < 3 or
            (current_time - min((ip.get("timestamp", 0) for ip in self.ip_pool), default=current_time)) > 900
        )
        
        if refresh_needed:
            print(f"{cyan}🔄  Refreshing IP pool (Total: {total_ips}, Healthy: {healthy_ips}, Fresh: {fresh_ips}){reset}")
            self._generate_fresh_ip_batch_enhanced()
    
    def _generate_fresh_ip_batch_enhanced(self):
        """Generate fresh batch of IPs with multi-country support"""
        print(f"{cyan}🌐  Generating enhanced multi-country IP batch (TRULY RANDOM)...{reset}")
        
        new_ips = []
        
        # Load country database from JSON file
        country_db = self._load_country_database()
        
        # Get all countries with equal weight (TRULY RANDOM)
        all_countries = list(country_db.get("countries", {}).keys())
        if not all_countries:
            # Fallback to hardcoded list
            all_countries = ["US", "AU", "CA", "GB", "DE", "FR", "JP", "KR", "SG", "NL", "NZ", "IT", "ES", "MX", "BR", "TH", "MY", "PH", "VN", "IN", "ID"]
        
        # TRULY RANDOM - equal weights for all countries
        selected_countries = random.sample(all_countries, min(5, len(all_countries)))
        
        print(f"{cyan}    Selected countries (RANDOM): {selected_countries}{reset}")
        
        # Build country_isps from database
        country_isps = {}
        for country in selected_countries:
            country_data = country_db.get("countries", {}).get(country, {})
            isps = country_data.get("isps", {})
            # Combine mobile and broadband ISPs
            country_isps[country] = list(isps.get("mobile", {}).keys()) + list(isps.get("broadband", {}).keys())
        
        for country in selected_countries:
            isps = country_isps.get(country, [])
            for isp in isps:
                try:
                    print(f"{cyan}    Generating {isp} ({country}) IPs...{reset}")
                    
                    # Use country-specific generation for non-ID countries
                    if country != "ID":
                        isp_ips = self._generate_country_ips(country, [isp])
                    else:
                        isp_ips = self._generate_dynamic_isp_ips(isp)
                    
                    if isp_ips:
                        # Validate each IP
                        validated_ips = []
                        for ip_info in isp_ips:
                            validation = self.validator.validate(ip_info["ip"], strict=True)
                            if validation["valid"] and validation["score"] >= 70:
                                ip_info["validation_score"] = validation["score"]
                                ip_info["last_validated"] = time.time()
                                ip_info["country"] = country
                                validated_ips.append(ip_info)
                        
                        if validated_ips:
                            new_ips.extend(validated_ips)
                            print(f"{hijau}    Added {len(validated_ips)} validated {isp} ({country}) IPs{reset}")
                        else:
                            print(f"{kuning}    No validated IPs for {isp}{reset}")
                            
                except Exception as e:
                    print(f"{merah}    Error generating {isp} IPs: {str(e)[:50]}{reset}")
                    continue
        
        # Add to pool with deduplication
        existing_ips = {ip["ip"] for ip in self.ip_pool}
        unique_new_ips = [ip for ip in new_ips if ip["ip"] not in existing_ips]
        
        if unique_new_ips:
            self.ip_pool.extend(unique_new_ips)
            
            # Limit pool size (keep freshest 100 IPs)
            if len(self.ip_pool) > 100:
                self.ip_pool.sort(key=lambda x: x.get("timestamp", 0), reverse=True)
                self.ip_pool = self.ip_pool[:100]
            
            print(f"{hijau}✅  Added {len(unique_new_ips)} fresh IPs | Total pool: {len(self.ip_pool)}{reset}")
            
            # Print country distribution
            country_dist = {}
            for ip in self.ip_pool:
                c = ip.get("country", "ID")
                country_dist[c] = country_dist.get(c, 0) + 1
            print(f"{cyan}    Country distribution: {country_dist}{reset}")
            
            # Update statistics
            avg_health = sum(ip.get("health_score", 0) for ip in self.ip_pool) / len(self.ip_pool)
            print(f"{cyan}    Avg health score: {avg_health:.1f}%{reset}")
        else:
            print(f"{merah}    No new unique IPs generated{reset}")
            self._generate_emergency_ip_batch()
    
    def _generate_emergency_ip_batch(self):
        """Generate emergency IP batch with multi-country support"""
        print(f"{merah}🚨  Generating emergency multi-country IP batch{reset}")
        
        emergency_ips = []
        
        # Multi-country manual prefixes
        manual_prefixes = [
            # Indonesia
            ("110.136", "telkomsel", "ID"),
            ("112.215", "indosat", "ID"),
            ("36.86", "xl", "ID"),
            ("116.206", "tri", "ID"),
            # USA
            ("174.192", "verizon", "US"),
            ("166.137", "att", "US"),
            ("172.32", "tmobile", "US"),
            ("73.93", "comcast", "US"),
            # Brazil
            ("177.32", "claro_br", "BR"),
            ("179.152", "vivo_br", "BR"),
            # India
            ("49.36", "jio", "IN"),
            ("106.76", "airtel_in", "IN"),
            # Germany
            ("91.64", "telekom_de", "DE"),
            ("80.187", "vodafone_de", "DE"),
        ]
        
        for prefix, isp, country in manual_prefixes:
            for _ in range(2):  # 2 IPs per prefix
                # Generate valid IP
                third = random.randint(0, 255)
                fourth = random.randint(10, 240)
                ip = f"{prefix}.{third}.{fourth}"
                
                # Validate format
                if not self._validate_ip_format_enhanced(ip):
                    continue
                
                # Anti-blacklist check
                if not self._anti_blacklist_check(ip):
                    continue
                
                # Create IP info
                config = self._get_isp_config_enhanced(isp)
                if config:
                    ip_info = self._create_enhanced_ip_profile(ip, config, isp)
                else:
                    # Create basic IP info for non-ID countries
                    ip_info = {
                        "ip": ip,
                        "isp": isp,
                        "country": country,
                        "health_score": 75,
                        "connection_type": "mobile",
                        "timestamp": time.time(),
                    }
                
                ip_info["emergency"] = True
                ip_info["country"] = country
                ip_info["health_score"] = 75
                
                emergency_ips.append(ip_info)
                print(f"{cyan}      Generated emergency IP: {ip} ({isp}, {country}){reset}")
        
        if emergency_ips:
            self.ip_pool = emergency_ips[:30]  # Keep 30 emergency IPs
            print(f"{hijau}✅  Emergency batch generated: {len(self.ip_pool)} IPs{reset}")
        else:
            print(f"{merah}❌  Failed to generate emergency IPs{reset}")
    
    def _build_enhanced_ip_config(self, ip_info: Dict[str, Any], session_id: str = None) -> Dict[str, Any]:
        """Build enhanced IP configuration dengan connection type aware headers - FIXED"""
        isp = ip_info["isp"]
        connection_type = ip_info.get("connection_type", "mobile")
        device_fp = ip_info.get("device_fingerprint", {})
        
        # Pilih profile berdasarkan ISP dan connection type - FIXED
        if connection_type == "mobile":
            if isp in ["telkomsel", "indosat"]:
                tcp_profile = "android_5g_premium"
                browser_profile = "chrome_mobile_samsung"
                tls_profile = "tls13_chrome_mobile"
            else:
                tcp_profile = "android_4g_midrange"
                browser_profile = "chrome_mobile_xiaomi"
                tls_profile = "tls13_chrome_mobile_mid"
        else:  # wifi/fiber
            tcp_profile = "android_wifi_premium"
            browser_profile = "chrome_tablet_samsung"
            tls_profile = "tls13_chrome_tablet"
        
        # Generate JA3 fingerprint yang spesifik
        ja3, ja3s = self._generate_ja3_fingerprint(browser_profile)
        
        # Generate HTTP2 settings
        http2_settings = self._generate_http2_settings(browser_profile)
        
        # Generate TLS fingerprint
        tls_fingerprint = self._generate_tls_fingerprint(tls_profile)
        
        # Generate user agent yang spesifik
        user_agent = self._generate_specific_user_agent(
            device_fp.get("brand", "Samsung"),
            device_fp.get("model", "SM-S928B"),
            device_fp.get("android_version", "14"),
            device_fp.get("chrome_version", "135.0.0.0"),
            connection_type  # FIXED: tambah parameter connection type
        )
        
        # Build location from flat IP info structure
        location = ip_info.get("location") if isinstance(ip_info.get("location"), dict) else {
            "country": ip_info.get("country", "ID"),
            "country_name": ip_info.get("country_name", "Indonesia"),
            "city": ip_info.get("city", "Jakarta"),
            "region": ip_info.get("region", "DKI Jakarta"),
            "latitude": ip_info.get("latitude", -6.2088),
            "longitude": ip_info.get("longitude", 106.8456),
            "timezone": ip_info.get("timezone", "Asia/Jakarta"),
            "as_name": ip_info.get("as_name", ""),
            "carrier": ip_info.get("carrier", isp.upper() if connection_type == "mobile" else "")
        }
        
        # Build comprehensive config
        config = {
            "ip": ip_info["ip"],
            "session_id": session_id,
            "isp_info": {
                "isp": isp,
                "asn": ip_info.get("asn", ""),
                "as_name": location.get("as_name", ip_info.get("as_name", "")),
                "carrier": location.get("carrier", ip_info.get("carrier", ""))
            },
            "connection_type": connection_type,  # FIXED: simpan connection type
            "location": location,
            "network_metrics": ip_info.get("network_metrics", {}),
            "tcp_parameters": ip_info.get("tcp_parameters", {}),
            "device_info": device_fp,
            "fingerprints": {
                "ja3": ja3,
                "ja3s": ja3s,
                "tls": tls_fingerprint,
                "http2": http2_settings,
                "akamai": self._generate_akamai_fingerprint(),
                "cloudflare": self._generate_cloudflare_fingerprint()
            },
            "browser_profile": {
                "name": browser_profile,
                "user_agent": user_agent,
                "accept_language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
                "accept_encoding": "gzip, deflate, br",
                "sec_ch_ua": self._generate_sec_ch_ua(device_fp.get("brand", "Samsung")),
                "sec_ch_ua_mobile": "?1" if connection_type == "mobile" else "?0",  # FIXED
                "sec_ch_ua_platform": '"Android"',
                "viewport": f"{device_fp.get('screen_resolution', '1080x2400').split('x')[0]}x{int(device_fp.get('screen_resolution', '1080x2400').split('x')[1]) - 100}",
                "device_pixel_ratio": device_fp.get("dpi", 440) / 160,
                "hardware_concurrency": 8,
                "device_memory": 8,
                "max_touch_points": 10
            },
            "headers": self._generate_enhanced_headers(ip_info, user_agent, connection_type),  # FIXED
            "cookies": {},
            "timing": {
                "request_delay": random.uniform(1.0, 3.0),
                "read_timeout": random.uniform(15.0, 30.0),
                "connect_timeout": random.uniform(5.0, 10.0),
                "keep_alive": random.choice([True, False])
            },
            "metadata": {
                "generated_at": time.time(),
                "health_score": ip_info.get("health_score", 75),
                "usage_count": ip_info.get("usage_count", 0),
                "rotation_count": ip_info.get("rotation_count", 0),
                "is_fallback": ip_info.get("emergency", False)
            }
        }
        
        return config
    
    def _generate_ja3_fingerprint(self, profile: str) -> Tuple[str, str]:
        """Generate JA3 dan JA3S fingerprint yang spesifik"""
        ja3_profiles = {
            "chrome_mobile_samsung": (
                "771,4865-4866-4867-49195-49199-49196-49200-52393-52392-49171-49172-156-157-47-53-65037-65038-65039,0-23-65281-10-11-35-16-5-13-18-51-45-43-27-17513-21-65041-65042,29-23-24-25-26,0",
                "771,4865,65281-0-23-13-5-18-16-11-51-45-43-10-21,29-23-24,0"
            ),
            "chrome_mobile_xiaomi": (
                "771,4865-4866-4867-49195-49199-49196-49200-52393-52392-49171-49172-156-157-47-53-65037-65038,0-23-65281-10-11-35-16-5-13-18-51-45-43-27-21-65041,29-23-24-25,0",
                "771,4865,65281-0-23-13-5-18-16-11-51-45-43-10-21,29-23-24,0"
            ),
            "chrome_mobile_generic": (
                "771,4865-4866-4867-49195-49199-49196-49200-52393-52392-49171-49172-156-157-47-53,0-23-65281-10-11-35-16-5-13-18-51-45-43-27-17513-21,29-23-24-25,0",
                "771,4865,65281-0-23-13-5-18-16-11-51-45-43-10-21,29-23-24,0"
            )
        }
        return ja3_profiles.get(profile, ja3_profiles["chrome_mobile_samsung"])
    
    def _generate_tls_fingerprint(self, profile: str) -> Dict[str, Any]:
        """Generate TLS fingerprint yang detail"""
        tls_profiles = {
            "tls13_chrome_mobile": {
                "version": "TLSv1.3",
                "ciphers": [
                    "TLS_AES_128_GCM_SHA256",
                    "TLS_AES_256_GCM_SHA384",
                    "TLS_CHACHA20_POLY1305_SHA256",
                    "TLS_ECDHE_ECDSA_WITH_AES_128_GCM_SHA256",
                    "TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256"
                ],
                "extensions": [
                    "server_name",
                    "extended_master_secret",
                    "renegotiation_info",
                    "supported_groups",
                    "ec_point_formats",
                    "session_ticket",
                    "application_layer_protocol_negotiation",
                    "status_request",
                    "delegated_credentials",
                    "key_share",
                    "supported_versions",
                    "signature_algorithms",
                    "signed_certificate_timestamp",
                    "compress_certificate",
                    "record_size_limit"
                ],
                "supported_groups": [
                    "X25519",
                    "P-256",
                    "P-384"
                ],
                "signature_algorithms": [
                    "ecdsa_secp256r1_sha256",
                    "rsa_pss_rsae_sha256",
                    "rsa_pkcs1_sha256",
                    "ecdsa_secp384r1_sha384",
                    "rsa_pss_rsae_sha384",
                    "rsa_pkcs1_sha384",
                    "rsa_pss_rsae_sha512",
                    "rsa_pkcs1_sha512"
                ],
                "alpn_protocols": ["h2", "http/1.1"]
            }
        }
        return tls_profiles.get(profile, tls_profiles["tls13_chrome_mobile"])
    
    def _generate_http2_settings(self, profile: str) -> Dict[str, int]:
        """Generate HTTP2 settings yang spesifik"""
        settings_profiles = {
            "chrome_mobile_samsung": {
                "HEADER_TABLE_SIZE": 65536,
                "ENABLE_PUSH": 1,
                "MAX_CONCURRENT_STREAMS": 1000,
                "INITIAL_WINDOW_SIZE": 6291456,
                "MAX_FRAME_SIZE": 16384,
                "MAX_HEADER_LIST_SIZE": 262144,
                "SETTINGS_ENABLE_CONNECT_PROTOCOL": 1
            },
            "chrome_mobile_xiaomi": {
                "HEADER_TABLE_SIZE": 65536,
                "ENABLE_PUSH": 0,
                "MAX_CONCURRENT_STREAMS": 1000,
                "INITIAL_WINDOW_SIZE": 6291456,
                "MAX_FRAME_SIZE": 16384,
                "MAX_HEADER_LIST_SIZE": 262144,
                "SETTINGS_ENABLE_CONNECT_PROTOCOL": 1
            }
        }
        return settings_profiles.get(profile, settings_profiles["chrome_mobile_samsung"])
    
    def _generate_specific_user_agent(self, brand: str, model: str, android_version: str, 
                                    chrome_version: str, connection_type: str = "mobile") -> str:
        """Generate specific user agent dengan connection type aware - FIXED"""
        if connection_type == "mobile":
            if brand.lower() == "samsung":
                build_id = f"SM-{model.split('-')[1] if '-' in model else model}"
                return f"Mozilla/5.0 (Linux; Android {android_version}; {build_id}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{chrome_version} Mobile Safari/537.36"
            elif brand.lower() == "apple":
                return f"Mozilla/5.0 (iPhone; CPU iPhone OS {android_version.replace('.', '_')} like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/{android_version.split('.')[0]}.0 Mobile/15E148 Safari/604.1"
            else:
                return f"Mozilla/5.0 (Linux; Android {android_version}; {model}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{chrome_version} Mobile Safari/537.36"
        else:
            # Tablet user agent
            if brand.lower() == "samsung":
                return f"Mozilla/5.0 (Linux; Android {android_version}; {model}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{chrome_version} Safari/537.36"
            else:
                return f"Mozilla/5.0 (Linux; Android {android_version}; {model}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{chrome_version} Safari/537.36"
    
    def _generate_sec_ch_ua(self, brand: str) -> str:
        """Generate Sec-CH-UA header"""
        if brand.lower() == "samsung":
            return '"Not_A Brand";v="8", "Chromium";v="120", "Samsung";v="15"'
        elif brand.lower() == "google":
            return '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"'
        else:
            return '"Not_A Brand";v="8", "Chromium";v="120"'
    
    def _generate_akamai_fingerprint(self) -> Dict[str, Any]:
        """Generate Akamai fingerprint"""
        return {
            "bot_manager": {
                "detected": False,
                "score": 0.1,
                "signature": f"akamaibm_{random.randint(1000000, 9999999)}"
            },
            "headers": {
                "X-Akamai-Transformed": "9",
                "X-Akamai-Request-ID": str(uuid.uuid4()),
                "X-Akamai-Edge-IP": f"{random.randint(100, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}"
            }
        }
    
    def _generate_cloudflare_fingerprint(self) -> Dict[str, Any]:
        """Generate Cloudflare fingerprint"""
        return {
            "ray_id": f"{random.randint(1000000000, 9999999999)}-{random.choice(['CGK', 'SIN', 'JKT'])}",
            "country": "ID",
            "cache_status": random.choice(["HIT", "MISS", "EXPIRED"]),
            "worker": random.choice([True, False])
        }

    def _rand_block(self, length=6):
        return ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(length))

    def _generate_web_session_id(self):
        return f"{self._rand_block()}:{self._rand_block()}:{self._rand_block()}"
    
    def _generate_enhanced_headers(self, ip_info: Dict[str, Any], user_agent: str, 
                                 connection_type: str = "desktop") -> Dict[str, str]:
        """Generate realistic HTTP headers that match common browser behavior.
        
        Headers are kept minimal and standard to avoid detection.
        Custom X-* headers that are not actually sent by real browsers are removed.
        Uses Desktop browser headers for Web API compatibility.
        """
        device_fp = ip_info.get("device_fingerprint", {})
        
        # Standard Instagram App IDs (the main web app ID is most common)
        APP_IDS = [
            "936619743392459",   # Instagram main web app
            "124024574287414",   # Instagram alternative
        ]
        app_id = random.choice(APP_IDS)
        
        # Determine Chrome version from device fingerprint or use reasonable default
        chrome_version = device_fp.get("chrome_version", "120.0.0.0").split('.')[0]
        
        # Desktop platform for Web API
        platform_choice = random.choice(["Windows", "macOS"])
        if platform_choice == "Windows":
            platform_header = '"Windows"'
        else:
            platform_header = '"macOS"'
        
        # Generate standard browser headers that match real Chrome on Desktop
        headers = {
            # Essential headers - order matters for fingerprinting
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Accept-Language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "User-Agent": user_agent,
            
            # Sec-* headers that Chrome actually sends - Desktop version
            "Sec-Ch-Ua": f'"Chromium";v="{chrome_version}", "Not_A Brand";v="8"',
            "Sec-Ch-Ua-Mobile": "?0",  # Desktop = not mobile
            "Sec-Ch-Ua-Platform": platform_header,
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-User": "?1",
            
            # Standard navigation headers
            "Upgrade-Insecure-Requests": "1",
        }
        
        # Add Instagram-specific headers only when needed (for API requests)
        # These are legitimate headers that Instagram's web app sends
        instagram_api_headers = {
            "X-Ig-App-Id": app_id,
            "X-Requested-With": "XMLHttpRequest",
            "X-Ig-Www-Claim": "0",
        }
        
        # Only include X-Ig headers for API-style requests
        headers.update(instagram_api_headers)
        
        # Origin and Referer for navigation context
        headers["Origin"] = "https://www.instagram.com"
        headers["Referer"] = "https://www.instagram.com/"
        
        return headers
    
    def _get_fallback_ip_config_enhanced(self, session_id: str = None) -> Dict[str, Any]:
        """Enhanced fallback IP config"""
        fallback_ips = [
            {"ip": "110.136.123.45", "isp": "telkomsel", "city": "Jakarta", "asn": "AS7713"},
            {"ip": "112.215.67.89", "isp": "indosat", "city": "Surabaya", "asn": "AS4761"},
            {"ip": "36.86.210.123", "isp": "xl", "city": "Bandung", "asn": "AS24203"},
            {"ip": "116.206.150.200", "isp": "tri", "city": "Medan", "asn": "AS23947"}
        ]
        
        fallback = random.choice(fallback_ips)
        
        return {
            "ip": fallback["ip"],
            "session_id": session_id,
            "isp_info": {
                "isp": fallback["isp"],
                "asn": fallback["asn"],
                "carrier": fallback["isp"].upper()
            },
            "location": {
                "city": fallback["city"],
                "country": "Indonesia",
                "country_code": "ID",
                "latitude": -6.2088,
                "longitude": 106.8456,
                "timezone": "Asia/Jakarta"
            },
            "device_info": {
                "brand": "Samsung",
                "model": "SM-S928B",
                "android_version": "14",
                "chrome_version": "135.0.0.0"
            },
            "fingerprints": {
                "ja3": "771,4865-4866-4867-49195-49199-49196-49200-52393-52392-49171-49172-156-157-47-53-65037-65038-65039,0-23-65281-10-11-35-16-5-13-18-51-45-43-27-17513-21-65041-65042,29-23-24-25-26,0",
                "ja3s": "771,4865,65281-0-23-13-5-18-16-11-51-45-43-10-21,29-23-24,0"
            },
            "browser_profile": {
                "user_agent": "Mozilla/5.0 (Linux; Android 14; SM-S928B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Mobile Safari/537.36",
                "accept_language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7"
            },
            "headers": {
                "User-Agent": "Mozilla/5.0 (Linux; Android 14; SM-S928B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Mobile Safari/537.36",
                "X-Forwarded-For": fallback["ip"],
                "X-Real-IP": fallback["ip"]
            },
            "metadata": {
                "is_fallback": True,
                "health_score": 60,
                "generated_at": time.time()
            }
        }
    
    def rotate_ip_for_session(self, session_id: str, reason: str = "rotation") -> Optional[Dict[str, Any]]:
        """Rotate IP untuk session tertentu"""
        print(f"{cyan}🔄  Rotating IP for session {session_id[:8]} - Reason: {reason}{reset}")
        
        # Dapatkan IP config baru
        new_config = self.get_fresh_ip_config(session_id)
        
        if new_config and new_config.get("ip"):
            # Update session mapping
            self.session_ip_map[session_id] = new_config["ip"]
            
            # Update IP info di pool
            for ip_info in self.ip_pool:
                if ip_info["ip"] == new_config["ip"]:
                    ip_info["rotation_count"] = ip_info.get("rotation_count", 0) + 1
                    ip_info["last_rotated"] = time.time()
                    ip_info["rotation_reason"] = reason
                    break
            
            print(f"{hijau}✅  IP rotated to: {new_config['ip']}{reset}")
            return new_config
        
        print(f"{merah}❌  Failed to rotate IP for session {session_id[:8]}{reset}")
        return None
    
    def record_ip_usage_result(self, ip: str, session_id: str, success: bool, 
                             details: Dict[str, Any] = None):
        """Record hasil penggunaan IP dengan detail"""
        for ip_info in self.ip_pool:
            if ip_info["ip"] == ip:
                # Update counters
                if success:
                    ip_info["success_count"] = ip_info.get("success_count", 0) + 1
                    ip_info["health_score"] = min(100, ip_info.get("health_score", 75) + 5)
                else:
                    ip_info["fail_count"] = ip_info.get("fail_count", 0) + 1
                    ip_info["health_score"] = max(10, ip_info.get("health_score", 75) - 15)
                
                # Update details
                if details:
                    if "proxy_detected" in details and details["proxy_detected"]:
                        ip_info["proxy_detected"] = True
                        self.blacklisted_ips.add(ip)
                        print(f"{merah}🚫  IP {ip} blacklisted (proxy detected){reset}")
                    
                    if "vpn_detected" in details and details["vpn_detected"]:
                        ip_info["vpn_detected"] = True
                    
                    if "datacenter_detected" in details and details["datacenter_detected"]:
                        ip_info["datacenter_detected"] = True
                
                ip_info["last_used"] = time.time()
                ip_info["last_session"] = session_id
                
                # Update session mapping
                if session_id in self.session_ip_map and self.session_ip_map[session_id] == ip:
                    if not success and ip_info.get("health_score", 0) < 50:
                        # Auto-rotate jika IP bermasalah
                        self.rotate_ip_for_session(session_id, "poor_health")
                
                break
    
    def get_session_ip_stats(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Get IP statistics untuk session tertentu"""
        if session_id not in self.session_ip_map:
            return None
        
        current_ip = self.session_ip_map[session_id]
        
        for ip_info in self.ip_pool:
            if ip_info["ip"] == current_ip:
                return {
                    "session_id": session_id,
                    "current_ip": current_ip,
                    "isp": ip_info.get("isp"),
                    "health_score": ip_info.get("health_score"),
                    "usage_count": ip_info.get("usage_count", 0),
                    "success_count": ip_info.get("success_count", 0),
                    "fail_count": ip_info.get("fail_count", 0),
                    "rotation_count": ip_info.get("rotation_count", 0),
                    "last_used": ip_info.get("last_used", 0),
                    "proxy_detected": ip_info.get("proxy_detected", False),
                    "reliability": ip_info.get("reliability", 0.8)
                }
        
        return None
    
    def cleanup_old_sessions(self, max_age_hours: int = 24):
        """Cleanup session mappings yang sudah tua"""
        current_time = time.time()
        sessions_to_remove = []
        
        for session_id, ip in list(self.session_ip_map.items()):
            # Cari IP info
            ip_found = False
            for ip_info in self.ip_pool:
                if ip_info["ip"] == ip and ip_info.get("last_session") == session_id:
                    ip_found = True
                    session_age = current_time - ip_info.get("last_used", 0)
                    
                    if session_age > max_age_hours * 3600:
                        sessions_to_remove.append(session_id)
                    break
            
            if not ip_found:
                sessions_to_remove.append(session_id)
        
        for session_id in sessions_to_remove:
            if session_id in self.session_ip_map:
                del self.session_ip_map[session_id]
        
        if sessions_to_remove:
            print(f"{cyan}🧹  Cleaned up {len(sessions_to_remove)} old sessions{reset}")

    def record_ip_result(self, ip: str, success: bool, proxy_detected: bool = False):
        """Record result of IP usage"""
        for ip_info in self.ip_pool:
            if ip_info["ip"] == ip:
                if success:
                    ip_info["success_count"] = ip_info.get("success_count", 0) + 1
                    ip_info["health_score"] = min(100, ip_info.get("health_score", 50) + 5)
                else:
                    ip_info["fail_count"] = ip_info.get("fail_count", 0) + 1
                    ip_info["health_score"] = max(10, ip_info.get("health_score", 50) - 15)
                
                if proxy_detected:
                    ip_info["proxy_detected"] = True
                    self.blacklisted_ips.add(ip)
                    print(f"{merah}🚫  IP {ip} blacklisted (proxy detected){reset}")
                
                ip_info["last_used"] = time.time()
                break

    def get_ip_pool_stats(self) -> Dict[str, Any]:
        """Get statistics about IP pool"""
        total = len(self.ip_pool)
        healthy = sum(1 for ip in self.ip_pool if ip.get("health_score", 0) >= 70)
        blacklisted = len(self.blacklisted_ips)
        
        isp_distribution = {}
        for ip in self.ip_pool:
            isp = ip.get("isp", "unknown")
            isp_distribution[isp] = isp_distribution.get(isp, 0) + 1
        
        avg_health = sum(ip.get("health_score", 0) for ip in self.ip_pool) / max(1, total)
        
        return {
            "total_ips": total,
            "healthy_ips": healthy,
            "blacklisted_ips": blacklisted,
            "health_rate": f"{healthy/total*100:.1f}%" if total > 0 else "0%",
            "avg_health_score": f"{avg_health:.1f}%",
            "isp_distribution": isp_distribution,
            "pool_age_seconds": time.time() - min((ip.get("timestamp", 0) for ip in self.ip_pool), default=time.time())
        }
    
    # Helper methods untuk ISP-specific generation
    def _generate_telkomsel_ips(self):
        return self._generate_dynamic_isp_ips("telkomsel")
    
    def _generate_indosat_ips(self):
        return self._generate_dynamic_isp_ips("indosat")
    
    def _generate_xl_ips(self):
        return self._generate_dynamic_isp_ips("xl")
    
    def _generate_tri_ips(self):
        return self._generate_dynamic_isp_ips("tri")
    
    def _generate_smartfren_ips(self):
        return self._generate_dynamic_isp_ips("smartfren")
    
    def _generate_biznet_ips(self):
        return self._generate_dynamic_isp_ips("biznet")
    
    def _generate_cbn_ips(self):
        return self._generate_dynamic_isp_ips("cbn")
    
    def _generate_firstmedia_ips(self):
        return self._generate_dynamic_isp_ips("firstmedia")
    
    def _generate_myrepublic_ips(self):
        return self._generate_dynamic_isp_ips("myrepublic")
    
    def _generate_indihome_ips(self):
        return self._generate_dynamic_isp_ips("indihome")
    
    def _generate_mncplay_ips(self):
        return self._generate_dynamic_isp_ips("mncplay")
    
    def _generate_iconnet_ips(self):
        return self._generate_dynamic_isp_ips("iconnet")
    
    def _generate_oxygen_ips(self):
        return self._generate_dynamic_isp_ips("oxygen")

# ===================== IP VALIDATOR 2025 =====================

class IPValidator2025:
    """Enhanced IP validator dengan comprehensive validation - INDONESIA ONLY
    
    Multiple IP checking methods:
    1. Nmap Scan (python-nmap) - Professional port scanning
    2. TCP Port Scan (socket) - Fallback port check
    3. ICMP Ping Check - Check if host responds to ping
    4. IP-API Geolocation - Verify IP is from Indonesia
    5. DNS Reverse Lookup - Check PTR records
    6. RDAP/WHOIS Lookup - Verify IP ownership
    7. Indonesia ISP Validation - Verify IP belongs to Indonesian ISP
    """
    
    # Try to import nmap
    try:
        import nmap
        NMAP_AVAILABLE = True
    except ImportError:
        NMAP_AVAILABLE = False
    
    def __init__(self):
        self.validation_cache = {}
        self.cache_ttl = 300
        self.validation_methods = [
            self._validate_format_enhanced,
            self._validate_range_enhanced,
            self._validate_geolocation,
            self._validate_network_properties
        ]
        self.vpn_ranges = self._load_vpn_ranges()
        self.datacenter_ranges = self._load_datacenter_ranges()
        
        # Initialize nmap scanner if available
        self.nmap_scanner = None
        try:
            import nmap
            self.nmap_scanner = nmap.PortScanner()
            print("✓ Nmap scanner initialized")
        except Exception as e:
            print(f"○ Nmap not available, using socket fallback: {e}")
        
        # VERIFIED Indonesia ISP IP ranges from APNIC WHOIS
        # Extended with all known allocations
        self.indonesia_isp_ranges = {
            # Telkomsel - AS7713 (VERIFIED from APNIC)
            "telkomsel": [
                "114.120.0.0/13",   # 114.120.0.0 - 114.127.255.255
                "110.136.0.0/13",   # 110.136.0.0 - 110.143.255.255
                "36.64.0.0/11",     # 36.64.0.0 - 36.95.255.255 (includes 36.72.x.x)
                "182.0.0.0/11",     # 182.0.0.0 - 182.31.255.255
                "118.136.0.0/13",   # 118.136.0.0 - 118.143.255.255
            ],
            # Indosat Ooredoo - AS4761 (VERIFIED)
            "indosat": [
                "114.0.0.0/12",     # 114.0.0.0 - 114.15.255.255 (includes 114.4-7)
                "180.240.0.0/12",   # 180.240.0.0 - 180.255.255.255
                "202.152.0.0/14",   # 202.152.0.0 - 202.155.255.255
                "125.160.0.0/11",   # 125.160.0.0 - 125.191.255.255
            ],
            # XL Axiata - AS24203 (VERIFIED)
            # NOTE: 120.88.0.0/13, 114.121.0.0/16, 114.122.0.0/15, 118.96.0.0/13 removed - NOT Indonesia per ip-api.com
            "xl": [
                "112.215.0.0/16",   # 112.215.0.0 - 112.215.255.255 (VERIFIED)
            ],
            # Tri Indonesia - AS45727 (VERIFIED)
            "tri": [
                "114.79.0.0/16",    # 114.79.0.0 - 114.79.255.255
                "114.125.0.0/16",   # 114.125.0.0 - 114.125.255.255
                "182.253.0.0/16",   # 182.253.0.0 - 182.253.255.255
            ],
            # Smartfren - AS18004 (VERIFIED - 112.78.0.0/15 REMOVED, NOT INDONESIAN)
            "smartfren": [
                "103.10.64.0/22",   # 103.10.64.0 - 103.10.67.255
                "202.67.32.0/19",   # 202.67.32.0 - 202.67.63.255
            ],
            # Biznet - AS17451 (VERIFIED)
            "biznet": [
                "103.28.52.0/22",   # 103.28.52.0 - 103.28.55.255
                "117.102.64.0/18",  # 117.102.64.0 - 117.102.127.255
                "202.169.32.0/19",  # 202.169.32.0 - 202.169.63.255
            ],
            # First Media - AS23700 (VERIFIED)
            "firstmedia": [
                "110.137.0.0/16",   # 110.137.0.0 - 110.137.255.255
                "202.53.232.0/21",  # 202.53.232.0 - 202.53.239.255
                "202.158.0.0/16",   # 202.158.0.0 - 202.158.255.255
            ],
            # MyRepublic - AS63859 (VERIFIED)
            "myrepublic": [
                "103.19.56.0/22",   # APNIC allocated to MyRepublic
                "103.56.148.0/22",  # APNIC allocated to MyRepublic
            ],
            # IndiHome (Telkom) - AS7713 (VERIFIED)
            "indihome": [
                "180.244.0.0/14",   # APNIC allocated to Telkom IndiHome
                "125.160.0.0/14",   # APNIC allocated to Telkom IndiHome
            ],
            # CBN - AS24218 (VERIFIED)
            "cbn": [
                "202.158.0.0/18",   # APNIC allocated to CBN
                "203.142.64.0/18",  # APNIC allocated to CBN
            ]
        }
    
    def scan_ip_with_nmap(self, ip: str, ports: str = "80,443,8080") -> Dict[str, Any]:
        """Scan IP using nmap for accurate port detection
        
        Args:
            ip: IP address to scan
            ports: Comma-separated port list or range (e.g., "80,443" or "1-1000")
        
        Returns:
            Scan result with open ports, state, and timing info
        """
        result = {
            "ip": ip,
            "scanned": False,
            "method": "nmap" if self.nmap_scanner else "socket",
            "open_ports": [],
            "state": "unknown",
            "latency_ms": None,
            "hostname": None,
            "os_match": None,
        }
        
        if self.nmap_scanner:
            try:
                # Use nmap for scanning
                # Arguments: -sT (TCP connect), -Pn (skip ping), --host-timeout 10s
                scan_result = self.nmap_scanner.scan(
                    hosts=ip, 
                    ports=ports, 
                    arguments='-sT -Pn --host-timeout 10s'
                )
                
                if ip in scan_result.get('scan', {}):
                    host_info = scan_result['scan'][ip]
                    
                    # Get state
                    result["state"] = host_info.get('status', {}).get('state', 'unknown')
                    
                    # Get open ports
                    if 'tcp' in host_info:
                        for port, port_info in host_info['tcp'].items():
                            if port_info.get('state') == 'open':
                                result["open_ports"].append({
                                    "port": port,
                                    "service": port_info.get('name', 'unknown'),
                                    "product": port_info.get('product', ''),
                                })
                    
                    # Get hostname
                    hostnames = host_info.get('hostnames', [])
                    if hostnames:
                        result["hostname"] = hostnames[0].get('name')
                    
                    result["scanned"] = True
                    
            except Exception as e:
                # Fallback to socket scanning
                result["method"] = "socket_fallback"
                result = self._socket_scan_fallback(ip, ports, result)
        else:
            # Use socket scanning
            result = self._socket_scan_fallback(ip, ports, result)
        
        return result
    
    def _socket_scan_fallback(self, ip: str, ports: str, result: Dict) -> Dict:
        """Fallback to socket scanning when nmap is not available"""
        import socket
        
        port_list = [int(p.strip()) for p in ports.split(",") if p.strip().isdigit()]
        
        for port in port_list:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(2.0)
                
                start_time = time.time()
                conn_result = sock.connect_ex((ip, port))
                latency = (time.time() - start_time) * 1000
                
                sock.close()
                
                if conn_result == 0:
                    result["open_ports"].append({
                        "port": port,
                        "service": self._get_common_service(port),
                        "product": "",
                    })
                    result["latency_ms"] = latency
                    result["state"] = "up"
                    
            except socket.timeout:
                continue
            except Exception:
                continue
        
        result["scanned"] = True
        return result
    
    def _get_common_service(self, port: int) -> str:
        """Get common service name for port"""
        services = {
            21: "ftp", 22: "ssh", 23: "telnet", 25: "smtp",
            53: "dns", 80: "http", 110: "pop3", 143: "imap",
            443: "https", 465: "smtps", 587: "submission",
            993: "imaps", 995: "pop3s", 3306: "mysql",
            3389: "rdp", 5432: "postgresql", 8080: "http-proxy",
            8443: "https-alt",
        }
        return services.get(port, "unknown")
    
    def verify_indonesia_ip_comprehensive(self, ip: str) -> Dict[str, Any]:
        """Comprehensive verification that IP is truly Indonesian
        
        Uses multiple methods:
        1. CIDR range check against verified Indonesian ranges
        2. Nmap/Socket scan for activity
        3. RDAP lookup for country info
        4. Geolocation API verification
        """
        result = {
            "ip": ip,
            "is_indonesia": False,
            "confidence": 0,
            "isp": None,
            "asn": None,
            "checks": {
                "cidr_match": False,
                "nmap_scan": False,
                "rdap_lookup": False,
                "geolocation": False,
            },
            "details": [],
        }
        
        # Check 1: CIDR range match (most reliable)
        cidr_result = self._check_indonesia_cidr(ip)
        if cidr_result["match"]:
            result["checks"]["cidr_match"] = True
            result["isp"] = cidr_result["isp"]
            result["confidence"] += 40
            result["details"].append(f"✓ IP in {cidr_result['isp'].upper()} range ({cidr_result['cidr']})")
        else:
            result["details"].append("✗ IP not in verified Indonesian ISP ranges")
        
        # Check 2: Nmap/Socket scan
        scan_result = self.scan_ip_with_nmap(ip, "80,443")
        if scan_result["scanned"]:
            result["checks"]["nmap_scan"] = True
            if scan_result["open_ports"]:
                result["confidence"] += 20
                ports = [p["port"] for p in scan_result["open_ports"]]
                result["details"].append(f"✓ Host active, open ports: {ports}")
            else:
                result["confidence"] += 10
                result["details"].append("○ Host scanned, no common ports open (may be mobile IP)")
        
        # Check 3: RDAP lookup (if available)
        rdap_result = self._check_rdap(ip)
        if rdap_result["success"]:
            result["checks"]["rdap_lookup"] = True
            if rdap_result["country"] == "ID":
                result["confidence"] += 30
                result["is_indonesia"] = True
                result["asn"] = rdap_result.get("asn")
                result["details"].append(f"✓ RDAP: {rdap_result['country']} - {rdap_result.get('org', 'Unknown')}")
            else:
                result["details"].append(f"✗ RDAP: {rdap_result['country']} (NOT Indonesia)")
        else:
            result["details"].append("○ RDAP lookup failed/unavailable")
        
        # Final determination
        result["is_indonesia"] = result["confidence"] >= 40 and result["checks"]["cidr_match"]
        
        return result
    
    def _check_indonesia_cidr(self, ip: str) -> Dict[str, Any]:
        """Check if IP is in verified Indonesian ISP CIDR ranges"""
        try:
            ip_obj = ipaddress.ip_address(ip)
            
            for isp, cidrs in self.indonesia_isp_ranges.items():
                for cidr in cidrs:
                    try:
                        network = ipaddress.ip_network(cidr, strict=False)
                        if ip_obj in network:
                            return {"match": True, "isp": isp, "cidr": cidr}
                    except:
                        continue
        except:
            pass
        
        return {"match": False, "isp": None, "cidr": None}
    
    def _check_rdap(self, ip: str) -> Dict[str, Any]:
        """Check IP via RDAP (Registration Data Access Protocol)"""
        try:
            import requests
            
            # Use APNIC RDAP for Asia-Pacific IPs
            response = requests.get(
                f"https://rdap.apnic.net/ip/{ip}",
                timeout=10,
                headers={"Accept": "application/rdap+json"}
            )
            
            if response.status_code == 200:
                data = response.json()
                
                # Extract country from events/remarks
                country = None
                org = None
                asn = None
                
                # Check for country in various fields
                for entity in data.get("entities", []):
                    if "vcardArray" in entity:
                        vcard = entity["vcardArray"]
                        if len(vcard) > 1:
                            for item in vcard[1]:
                                if item[0] == "fn":
                                    org = item[3] if len(item) > 3 else None
                
                # Check remarks for country
                for remark in data.get("remarks", []):
                    description = " ".join(remark.get("description", []))
                    if "Indonesia" in description or "ID" in description:
                        country = "ID"
                        break
                
                # Check country field directly
                if "country" in data:
                    country = data["country"]
                
                # If we found a result
                if country or org:
                    return {
                        "success": True,
                        "country": country or "Unknown",
                        "org": org,
                        "asn": asn,
                    }
            
        except Exception as e:
            pass
        
        return {"success": False}
    
    def check_ip_comprehensive(self, ip: str) -> Dict[str, Any]:
        """Comprehensive IP check using multiple methods (synchronous version)"""
        result = {
            "ip": ip,
            "valid": False,
            "active": False,
            "indonesia": False,
            "isp": None,
            "checks": {
                "format": False,
                "indonesia_range": False,
                "tcp_scan": False,
                "ping": False,
                "dns_reverse": False,
                "geolocation": False
            },
            "score": 0,
            "latency_ms": None,
            "details": []
        }
        
        # Check 1: Format validation
        if self._check_ip_format(ip):
            result["checks"]["format"] = True
            result["score"] += 10
            result["details"].append("✓ Valid IP format")
        else:
            result["details"].append("✗ Invalid IP format")
            return result
        
        # Check 2: Indonesia ISP range validation
        isp_check = self._check_indonesia_isp_range(ip)
        if isp_check["valid"]:
            result["checks"]["indonesia_range"] = True
            result["indonesia"] = True
            result["isp"] = isp_check["isp"]
            result["score"] += 30
            result["details"].append(f"✓ IP belongs to {isp_check['isp'].upper()} Indonesia")
        else:
            result["details"].append("✗ IP not in Indonesian ISP range")
        
        # Check 3: TCP Port Scan (nmap-style)
        tcp_result = self._tcp_port_scan(ip, [80, 443, 8080])
        if tcp_result["success"]:
            result["checks"]["tcp_scan"] = True
            result["active"] = True
            result["latency_ms"] = tcp_result.get("latency_ms")
            result["score"] += 25
            result["details"].append(f"✓ TCP port {tcp_result['port']} open (latency: {tcp_result.get('latency_ms', 0):.1f}ms)")
        else:
            result["details"].append("○ TCP ports closed (may still be valid mobile IP)")
        
        # Check 4: Ping check (ICMP)
        ping_result = self._ping_check(ip)
        if ping_result["success"]:
            result["checks"]["ping"] = True
            result["score"] += 15
            result["details"].append(f"✓ Ping successful (RTT: {ping_result.get('rtt_ms', 0):.1f}ms)")
        else:
            result["details"].append("○ Ping failed (may be blocked by firewall)")
        
        # Check 5: DNS Reverse Lookup
        dns_result = self._dns_reverse_lookup(ip)
        if dns_result["success"]:
            result["checks"]["dns_reverse"] = True
            result["score"] += 10
            result["details"].append(f"✓ DNS PTR: {dns_result.get('hostname', 'N/A')}")
        else:
            result["details"].append("○ No PTR record (common for mobile IPs)")
        
        # Check 6: Geolocation API check
        geo_result = self._check_geolocation_api(ip)
        if geo_result["success"] and geo_result.get("country") == "ID":
            result["checks"]["geolocation"] = True
            result["indonesia"] = True
            result["score"] += 10
            result["details"].append(f"✓ Geolocation: Indonesia ({geo_result.get('city', 'Unknown')})")
            if not result["isp"]:
                result["isp"] = geo_result.get("isp")
        else:
            result["details"].append("○ Geolocation check skipped/failed")
        
        # Final validation
        result["valid"] = result["score"] >= 40 and result["indonesia"]
        
        return result
    
    def _check_ip_format(self, ip: str) -> bool:
        """Validate IP format"""
        try:
            parts = ip.split(".")
            if len(parts) != 4:
                return False
            for part in parts:
                num = int(part)
                if num < 0 or num > 255:
                    return False
            return True
        except:
            return False
    
    def _check_indonesia_isp_range(self, ip: str) -> Dict[str, Any]:
        """Check if IP belongs to Indonesian ISP"""
        import ipaddress
        
        try:
            ip_obj = ipaddress.ip_address(ip)
            
            for isp, ranges in self.indonesia_isp_ranges.items():
                for ip_range in ranges:
                    try:
                        network = ipaddress.ip_network(ip_range, strict=False)
                        if ip_obj in network:
                            return {"valid": True, "isp": isp}
                    except:
                        continue
        except:
            pass
        
        return {"valid": False, "isp": None}
    
    def _tcp_port_scan(self, ip: str, ports: List[int] = [80, 443, 8080]) -> Dict[str, Any]:
        """TCP port scan like nmap - check if ports are open"""
        import socket
        
        for port in ports:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(2.0)
                
                start_time = time.time()
                result = sock.connect_ex((ip, port))
                latency = (time.time() - start_time) * 1000
                
                sock.close()
                
                if result == 0:
                    return {"success": True, "port": port, "latency_ms": latency}
            except:
                continue
        
        return {"success": False}
    
    def _ping_check(self, ip: str) -> Dict[str, Any]:
        """ICMP ping check"""
        import subprocess
        import platform
        
        try:
            # Determine ping command based on OS
            param = "-n" if platform.system().lower() == "windows" else "-c"
            timeout_param = "-w" if platform.system().lower() == "windows" else "-W"
            
            start_time = time.time()
            result = subprocess.run(
                ["ping", param, "1", timeout_param, "2", ip],
                capture_output=True,
                timeout=3
            )
            rtt = (time.time() - start_time) * 1000
            
            if result.returncode == 0:
                return {"success": True, "rtt_ms": rtt}
        except:
            pass
        
        return {"success": False}
    
    def _dns_reverse_lookup(self, ip: str) -> Dict[str, Any]:
        """DNS reverse lookup (PTR record)"""
        import socket
        
        try:
            hostname = socket.gethostbyaddr(ip)
            return {"success": True, "hostname": hostname[0]}
        except:
            return {"success": False}
    
    def _check_geolocation_api(self, ip: str) -> Dict[str, Any]:
        """Check IP geolocation via free API"""
        try:
            import requests
            
            response = requests.get(
                f"http://ip-api.com/json/{ip}?fields=status,country,countryCode,city,isp,org",
                timeout=5
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get("status") == "success":
                    return {
                        "success": True,
                        "country": data.get("countryCode"),
                        "city": data.get("city"),
                        "isp": data.get("isp"),
                        "org": data.get("org")
                    }
        except:
            pass
        
        return {"success": False}
    
    async def check_ip_active(self, ip: str) -> Dict[str, Any]:
        """Check if IP is active using multiple methods (async version)"""
        result = {
            "ip": ip,
            "active": False,
            "methods_passed": [],
            "methods_failed": [],
            "latency_ms": None,
            "country": None,
            "isp": None
        }
        
        # Method 1: TCP Connect check (ports 80, 443)
        tcp_result = await self._check_tcp_connect_async(ip)
        if tcp_result["success"]:
            result["methods_passed"].append("tcp_connect")
            result["latency_ms"] = tcp_result.get("latency_ms")
        else:
            result["methods_failed"].append("tcp_connect")
        
        # Method 2: Check via IP-API (free geolocation API)
        geo_result = await self._check_ip_api_async(ip)
        if geo_result["success"]:
            result["methods_passed"].append("ip_api")
            result["country"] = geo_result.get("country")
            result["isp"] = geo_result.get("isp")
        else:
            result["methods_failed"].append("ip_api")
        
        # Method 3: DNS reverse lookup
        dns_result = await self._check_dns_reverse_async(ip)
        if dns_result["success"]:
            result["methods_passed"].append("dns_reverse")
        else:
            result["methods_failed"].append("dns_reverse")
        
        # Determine if IP is active
        result["active"] = len(result["methods_passed"]) >= 1
        
        return result
    
    async def _check_tcp_connect_async(self, ip: str, ports: List[int] = [80, 443]) -> Dict[str, Any]:
        """Check TCP connectivity to common ports (async)"""
        import asyncio
        
        for port in ports:
            try:
                start_time = time.time()
                reader, writer = await asyncio.wait_for(
                    asyncio.open_connection(ip, port),
                    timeout=3.0
                )
                latency = (time.time() - start_time) * 1000
                writer.close()
                await writer.wait_closed()
                return {"success": True, "port": port, "latency_ms": latency}
            except:
                continue
        
        return {"success": False}
    
    async def _check_ip_api(self, ip: str) -> Dict[str, Any]:
        """Check IP via ip-api.com"""
        try:
            url = f"http://ip-api.com/json/{ip}?fields=status,country,countryCode,isp,org,as,query"
            async with aiohttp.ClientSession() as session:
                async with session.get(url, timeout=aiohttp.ClientTimeout(total=5)) as response:
                    if response.status == 200:
                        data = await response.json()
                        if data.get("status") == "success":
                            return {
                                "success": True,
                                "country": data.get("countryCode"),
                                "isp": data.get("isp"),
                                "org": data.get("org"),
                                "as": data.get("as")
                            }
        except:
            pass
        
        return {"success": False}
    
    async def _check_dns_reverse(self, ip: str) -> Dict[str, Any]:
        """Check DNS reverse lookup"""
        try:
            import socket
            hostname = socket.gethostbyaddr(ip)
            return {"success": True, "hostname": hostname[0]}
        except:
            return {"success": False}
    
    def validate_indonesia_ip(self, ip: str) -> Dict[str, Any]:
        """Validate that IP belongs to Indonesian ISP"""
        import ipaddress
        
        result = {
            "valid": False,
            "isp": None,
            "reason": "Not an Indonesian IP"
        }
        
        try:
            ip_obj = ipaddress.ip_address(ip)
            
            for isp, ranges in self.indonesia_isp_ranges.items():
                for ip_range in ranges:
                    try:
                        network = ipaddress.ip_network(ip_range, strict=False)
                        if ip_obj in network:
                            result["valid"] = True
                            result["isp"] = isp
                            result["reason"] = f"IP belongs to {isp.upper()} Indonesia"
                            return result
                    except:
                        continue
        except:
            result["reason"] = "Invalid IP format"
        
        return result
    
    def _load_vpn_ranges(self) -> List[str]:
        """Load known VPN ranges"""
        return [
            "45.12.", "45.13.", "45.14.", "45.15.",
            "185.100.", "185.101.", "185.102.",
            "193.100.", "193.101.",
            "209.141.", "209.142.",
            "107.189.", "104.244."
        ]
    
    def _load_datacenter_ranges(self) -> List[str]:
        """Load known datacenter ranges"""
        return [
            "45.", "104.", "107.", "108.", "109.",
            "140.", "141.", "142.", "143.", "144.",
            "146.", "147.", "148.", "149.", "154.",
            "155.", "156.", "157.", "158.", "159.",
            "162.", "163.", "164.", "165.", "167.",
            "168.", "169.", "192.0.0.", "198.18.",
            "198.19.", "240.", "241.", "242.", "243.",
            "244.", "245.", "246.", "247.", "248.",
            "249.", "250.", "251.", "252.", "253."
        ]
    
    def validate(self, ip: str, strict: bool = True) -> Dict[str, Any]:
        """Validate IP dengan comprehensive checks"""
        cache_key = f"{ip}_{strict}"
        
        if cache_key in self.validation_cache:
            cached = self.validation_cache[cache_key]
            if time.time() - cached["timestamp"] < self.cache_ttl:
                return cached["result"]
        
        result = {
            "ip": ip,
            "valid": True,
            "score": 100,
            "category": "unknown",
            "issues": [],
            "warnings": [],
            "suspicious_factors": [],
            "recommendations": [],
            "timestamp": time.time()
        }
        
        # Jalankan semua validation methods
        for method in self.validation_methods:
            try:
                method_result = method(ip, strict)
                
                if not method_result.get("valid", True):
                    result["valid"] = False
                
                if "score_penalty" in method_result:
                    result["score"] -= method_result["score_penalty"]
                
                if "issues" in method_result:
                    result["issues"].extend(method_result["issues"])
                
                if "warnings" in method_result:
                    result["warnings"].extend(method_result["warnings"])
                
                if "suspicious_factors" in method_result:
                    result["suspicious_factors"].extend(method_result["suspicious_factors"])
                
                if "recommendations" in method_result:
                    result["recommendations"].extend(method_result["recommendations"])
                    
            except Exception as e:
                result["warnings"].append(f"Validation error in {method.__name__}: {str(e)}")
                result["score"] -= 5
        
        # Apply additional rules
        if strict:
            self._apply_strict_rules(result)
        
        # Final score adjustment
        if result["issues"]:
            result["score"] -= len(result["issues"]) * 10
        
        if result["warnings"]:
            result["score"] -= len(result["warnings"]) * 5
        
        if result["suspicious_factors"]:
            result["score"] -= len(result["suspicious_factors"]) * 3
        
        # Clamp score
        result["score"] = max(0, min(100, result["score"]))
        
        # Determine category
        if result["score"] >= 85:
            result["category"] = "excellent"
        elif result["score"] >= 70:
            result["category"] = "good"
        elif result["score"] >= 50:
            result["category"] = "fair"
        elif result["score"] >= 30:
            result["category"] = "poor"
        else:
            result["category"] = "bad"
        
        # Determine status
        if result["valid"] and result["score"] >= 60:
            result["status"] = "acceptable"
        elif result["valid"] and result["score"] >= 40:
            result["status"] = "risky"
        else:
            result["status"] = "unacceptable"
        
        # Cache result
        self.validation_cache[cache_key] = {
            "result": result,
            "timestamp": time.time()
        }
        
        return result
    
    def _validate_format_enhanced(self, ip: str, strict: bool) -> Dict[str, Any]:
        """Enhanced format validation"""
        result = {
            "valid": True,
            "score_penalty": 0,
            "issues": [],
            "warnings": [],
            "suspicious_factors": []
        }
        
        try:
            # Basic format check
            socket.inet_aton(ip)
            
            parts = ip.split('.')
            if len(parts) != 4:
                result["valid"] = False
                result["score_penalty"] = 50
                result["issues"].append("Invalid IPv4 format: must have 4 octets")
                return result
            
            # Check each octet
            for i, part in enumerate(parts):
                if not part.isdigit():
                    result["valid"] = False
                    result["score_penalty"] = 40
                    result["issues"].append(f"Octet {i+1} is not numeric: {part}")
                    return result
                
                num = int(part)
                if num < 0 or num > 255:
                    result["valid"] = False
                    result["score_penalty"] = 40
                    result["issues"].append(f"Octet {i+1} out of range: {num}")
                    return result
            
            # Check for suspicious octets
            if parts[3] in ['0', '1', '254', '255']:
                result["warnings"].append(f"Suspicious last octet: {parts[3]}")
                result["score_penalty"] = 5
                result["suspicious_factors"].append("network_broadcast_octet")
            
            if parts[0] == '0':
                result["valid"] = False
                result["score_penalty"] = 30
                result["issues"].append("Invalid first octet: 0")
                return result
            
            # Check for sequential patterns
            if len(set(parts)) == 1:
                result["warnings"].append("All octets are the same")
                result["score_penalty"] = 10
                result["suspicious_factors"].append("sequential_pattern")
            
            # Check for incremental patterns
            try:
                int_parts = [int(p) for p in parts]
                if all(int_parts[i] + 1 == int_parts[i+1] for i in range(3)):
                    result["warnings"].append("Incremental octet pattern detected")
                    result["score_penalty"] = 8
                    result["suspicious_factors"].append("incremental_pattern")
            except:
                pass
            
            # Check for common fake IP patterns
            fake_patterns = [
                ip == "127.0.0.1",
                ip.startswith("192.168."),
                ip.startswith("10."),
                ip.startswith("172.16.") or ip.startswith("172.17.") or 
                ip.startswith("172.18.") or ip.startswith("172.19.") or
                ip.startswith("172.20.") or ip.startswith("172.21.") or
                ip.startswith("172.22.") or ip.startswith("172.23.") or
                ip.startswith("172.24.") or ip.startswith("172.25.") or
                ip.startswith("172.26.") or ip.startswith("172.27.") or
                ip.startswith("172.28.") or ip.startswith("172.29.") or
                ip.startswith("172.30.") or ip.startswith("172.31."),
                ip == "0.0.0.0",
                ip == "255.255.255.255"
            ]
            
            if any(fake_patterns):
                result["valid"] = False
                result["score_penalty"] = 100
                result["issues"].append("IP is private/reserved/localhost")
                return result
                
        except socket.error:
            result["valid"] = False
            result["score_penalty"] = 50
            result["issues"].append("Invalid IP address format")
        except Exception as e:
            result["valid"] = False
            result["score_penalty"] = 30
            result["issues"].append(f"Format validation error: {str(e)}")
        
        return result
    
    def _validate_range_enhanced(self, ip: str, strict: bool) -> Dict[str, Any]:
        """Enhanced range validation"""
        result = {
            "valid": True,
            "score_penalty": 0,
            "issues": [],
            "warnings": [],
            "suspicious_factors": [],
            "recommendations": []
        }
        
        try:
            ip_obj = ipaddress.ip_address(ip)
            
            # Check for special addresses
            if ip_obj.is_reserved:
                result["valid"] = False
                result["score_penalty"] = 100
                result["issues"].append("IP is reserved")
                return result
            
            if ip_obj.is_loopback:
                result["valid"] = False
                result["score_penalty"] = 100
                result["issues"].append("IP is loopback")
                return result
            
            if ip_obj.is_link_local:
                result["valid"] = False
                result["score_penalty"] = 100
                result["issues"].append("IP is link-local")
                return result
            
            if ip_obj.is_multicast:
                result["valid"] = False
                result["score_penalty"] = 100
                result["issues"].append("IP is multicast")
                return result
            
            # Check for private addresses
            if ip_obj.is_private:
                result["valid"] = False
                result["score_penalty"] = 100
                result["issues"].append("IP is private")
                return result
            
            # Check for Indonesian IP ranges
            indonesian_prefixes = [
                '36.', '110.', '112.', '114.', '116.', '118.', '125.', '139.',
                '180.', '182.', '202.', '203.', '103.10.', '103.23.', '103.28.',
                '103.87.', '123.231.', '27.', '45.', '49.', '58.', '61.', '101.',
                '103.', '106.', '111.', '113.', '115.', '117.', '119.', '121.',
                '122.', '124.', '126.', '128.', '129.', '130.', '131.', '132.',
                '133.', '134.', '135.', '136.', '137.', '138.', '140.', '141.',
                '142.', '143.', '144.', '145.', '146.', '147.', '148.', '149.',
                '150.', '151.', '152.', '153.', '154.', '155.', '156.', '157.',
                '158.', '159.', '160.', '161.', '162.', '163.', '164.', '165.',
                '166.', '167.', '168.', '169.', '170.', '171.', '172.', '173.',
                '174.', '175.', '176.', '177.', '178.', '179.', '181.', '183.',
                '184.', '185.', '186.', '187.', '188.', '189.', '190.', '191.',
                '192.', '193.', '194.', '195.', '196.', '197.', '198.', '199.',
                '200.', '201.', '204.', '205.', '206.', '207.', '208.', '209.',
                '210.', '211.', '212.', '213.', '214.', '215.', '216.', '217.',
                '218.', '219.', '220.', '221.', '222.', '223.', '224.', '225.',
                '226.', '227.', '228.', '229.', '230.', '231.', '232.', '233.',
                '234.', '235.', '236.', '237.', '238.', '239.', '240.', '241.',
                '242.', '243.', '244.', '245.', '246.', '247.', '248.', '249.',
                '250.', '251.', '252.', '253.', '254.'
            ]
            
            is_indonesian = any(ip.startswith(prefix) for prefix in indonesian_prefixes)
            
            if is_indonesian:
                result["score_penalty"] -= 5  # Bonus untuk IP Indonesia
                result["recommendations"].append("IP appears to be from Indonesia - good for targeting")
            else:
                result["warnings"].append("IP is not from known Indonesian ranges")
                result["score_penalty"] += 15
                result["suspicious_factors"].append("non_indonesian_ip")
            
            # Check for datacenter ranges
            is_datacenter = any(ip.startswith(prefix) for prefix in self.datacenter_ranges)
            
            if is_datacenter:
                result["warnings"].append("IP is in known datacenter range")
                result["score_penalty"] += 20 if strict else 10
                result["suspicious_factors"].append("datacenter_ip")
                result["recommendations"].append("Consider using residential IP instead")
            
            # Check for VPN ranges
            is_vpn = any(ip.startswith(prefix) for prefix in self.vpn_ranges)
            
            if is_vpn:
                result["warnings"].append("IP matches known VPN/proxy range")
                result["score_penalty"] += 25 if strict else 15
                result["suspicious_factors"].append("vpn_proxy_ip")
                result["recommendations"].append("Avoid VPN/proxy IPs for Instagram")
            
            # Check for cloud providers
            cloud_providers = [
                ("aws", ["18.", "52.", "54.", "35.", "44."]),
                ("google", ["8.", "34.", "104.", "108.", "142.", "146."]),
                ("azure", ["13.", "20.", "23.", "40.", "51.", "52."]),
                ("cloudflare", ["104.", "108.", "141.", "162.", "172.", "173.", "188."]),
                ("digitalocean", ["138.", "139.", "159.", "161.", "162.", "167.", "174."])
            ]
            
            for provider, prefixes in cloud_providers:
                if any(ip.startswith(prefix) for prefix in prefixes):
                    result["warnings"].append(f"IP is from {provider.upper()} cloud")
                    result["score_penalty"] += 15
                    result["suspicious_factors"].append(f"cloud_provider_{provider}")
                    break
            
            # Check for hosting providers
            hosting_providers = [
                ("ovh", ["5.", "37.", "46.", "51.", "54.", "87.", "91.", "92.", "93.", "94.", "95.", "109.", "144.", "145.", "146.", "147.", "148.", "149.", "150.", "151.", "152.", "153.", "154.", "155.", "156.", "157.", "158.", "159.", "160.", "161.", "162.", "163.", "164.", "165.", "176.", "178.", "185.", "188.", "192.", "193.", "194.", "195.", "198.", "213."]),
                ("hetzner", ["5.", "78.", "79.", "85.", "88.", "91.", "94.", "95.", "144.", "148.", "149.", "159.", "176.", "178.", "185.", "188.", "213."]),
                ("linode", ["45.", "50.", "66.", "74.", "96.", "97.", "104.", "107.", "108.", "139.", "172.", "173.", "192.", "198.", "209."])
            ]
            
            for provider, prefixes in hosting_providers:
                if any(ip.startswith(prefix) for prefix in prefixes):
                    result["warnings"].append(f"IP is from {provider.upper()} hosting")
                    result["score_penalty"] += 18
                    result["suspicious_factors"].append(f"hosting_provider_{provider}")
                    break
            
        except Exception as e:
            result["valid"] = False
            result["score_penalty"] = 30
            result["issues"].append(f"Range validation error: {str(e)}")
        
        return result
    
    def _validate_reputation_enhanced(self, ip: str, strict: bool) -> Dict[str, Any]:
        """Enhanced reputation validation"""
        result = {
            "valid": True,
            "score_penalty": 0,
            "issues": [],
            "warnings": [],
            "suspicious_factors": [],
            "recommendations": []
        }
        
        try:
            parts = ip.split('.')
            
            # Check for blacklisted patterns
            blacklisted_patterns = [
                ip.startswith('1.0.0.') or ip.startswith('1.1.1.'),  # Cloudflare DNS
                ip.startswith('8.8.8.') or ip.startswith('8.8.4.'),  # Google DNS
                ip.startswith('9.9.9.') or ip.startswith('149.112.'),  # Quad9 DNS
                ip.startswith('208.67.') or ip.startswith('208.69.'),  # OpenDNS
            ]
            
            if any(blacklisted_patterns):
                result["warnings"].append("IP is a public DNS server")
                result["score_penalty"] += 20
                result["suspicious_factors"].append("dns_server")
            
            # Check for TOR exit nodes (common patterns)
            tor_patterns = [
                ip.startswith('5.') and int(parts[1]) in range(100, 200),
                ip.startswith('37.') and int(parts[1]) in range(100, 200),
                ip.startswith('46.') and int(parts[1]) in range(100, 200),
                ip.startswith('51.') and int(parts[1]) in range(100, 200),
                ip.startswith('77.') and int(parts[1]) in range(100, 200),
                ip.startswith('78.') and int(parts[1]) in range(100, 200),
                ip.startswith('79.') and int(parts[1]) in range(100, 200),
                ip.startswith('80.') and int(parts[1]) in range(100, 200),
                ip.startswith('81.') and int(parts[1]) in range(100, 200),
                ip.startswith('82.') and int(parts[1]) in range(100, 200),
                ip.startswith('83.') and int(parts[1]) in range(100, 200),
                ip.startswith('84.') and int(parts[1]) in range(100, 200),
                ip.startswith('85.') and int(parts[1]) in range(100, 200),
                ip.startswith('86.') and int(parts[1]) in range(100, 200),
                ip.startswith('87.') and int(parts[1]) in range(100, 200),
                ip.startswith('88.') and int(parts[1]) in range(100, 200),
                ip.startswith('89.') and int(parts[1]) in range(100, 200),
                ip.startswith('90.') and int(parts[1]) in range(100, 200),
                ip.startswith('91.') and int(parts[1]) in range(100, 200),
                ip.startswith('92.') and int(parts[1]) in range(100, 200),
                ip.startswith('93.') and int(parts[1]) in range(100, 200),
                ip.startswith('94.') and int(parts[1]) in range(100, 200),
                ip.startswith('95.') and int(parts[1]) in range(100, 200),
                ip.startswith('109.') and int(parts[1]) in range(100, 200),
            ]
            
            if any(tor_patterns):
                result["warnings"].append("IP matches TOR exit node patterns")
                result["score_penalty"] += 30
                result["suspicious_factors"].append("tor_exit_node")
                result["recommendations"].append("Avoid TOR exit nodes")
            
            # Check for bulletproof hosting
            bulletproof_patterns = [
                ip.startswith('31.') and int(parts[1]) in range(100, 200),
                ip.startswith('46.') and int(parts[1]) in range(100, 200),
                ip.startswith('62.') and int(parts[1]) in range(100, 200),
                ip.startswith('77.') and int(parts[1]) in range(100, 200),
                ip.startswith('78.') and int(parts[1]) in range(100, 200),
                ip.startswith('79.') and int(parts[1]) in range(100, 200),
                ip.startswith('85.') and int(parts[1]) in range(100, 200),
                ip.startswith('89.') and int(parts[1]) in range(100, 200),
                ip.startswith('91.') and int(parts[1]) in range(100, 200),
                ip.startswith('93.') and int(parts[1]) in range(100, 200),
                ip.startswith('95.') and int(parts[1]) in range(100, 200),
                ip.startswith('109.') and int(parts[1]) in range(100, 200),
                ip.startswith('176.') and int(parts[1]) in range(100, 200),
                ip.startswith('185.') and int(parts[1]) in range(100, 200),
                ip.startswith('188.') and int(parts[1]) in range(100, 200),
                ip.startswith('193.') and int(parts[1]) in range(100, 200),
                ip.startswith('195.') and int(parts[1]) in range(100, 200),
            ]
            
            if any(bulletproof_patterns):
                result["warnings"].append("IP matches bulletproof hosting patterns")
                result["score_penalty"] += 25
                result["suspicious_factors"].append("bulletproof_hosting")
                result["recommendations"].append("Avoid bulletproof hosting IPs")
            
            # Check for spam patterns
            spam_patterns = [
                all(int(p) > 200 for p in parts),  # All octets > 200
                sum(int(p) for p in parts) > 800,  # Sum > 800
                int(parts[3]) - int(parts[0]) > 200,  # Large difference
            ]
            
            if any(spam_patterns):
                result["warnings"].append("IP has suspicious spam-like pattern")
                result["score_penalty"] += 10
                result["suspicious_factors"].append("spam_pattern")
            
            # Check for recently allocated ranges
            recent_ranges = [
                ip.startswith('45.') and int(parts[1]) in range(200, 255),
                ip.startswith('104.') and int(parts[1]) in range(200, 255),
                ip.startswith('108.') and int(parts[1]) in range(200, 255),
                ip.startswith('140.') and int(parts[1]) in range(200, 255),
                ip.startswith('144.') and int(parts[1]) in range(200, 255),
            ]
            
            if any(recent_ranges):
                result["warnings"].append("IP is in recently allocated range")
                result["score_penalty"] += 5
                result["suspicious_factors"].append("recent_allocation")
            
        except Exception as e:
            result["warnings"].append(f"Reputation validation error: {str(e)}")
            result["score_penalty"] += 5
        
        return result
    
    def _validate_geolocation(self, ip: str, strict: bool) -> Dict[str, Any]:
        """Validate geolocation consistency"""
        result = {
            "valid": True,
            "score_penalty": 0,
            "issues": [],
            "warnings": [],
            "suspicious_factors": [],
            "recommendations": []
        }
        
        try:
            # Ini adalah simulasi - dalam implementasi real, gunakan service geolocation
            parts = ip.split('.')
            first_octet = int(parts[0])
            
            # Simple geolocation inference
            if first_octet == 1:
                country = "US"
            elif first_octet == 31:
                country = "NL"
            elif first_octet == 46:
                country = "RU"
            elif first_octet == 49:
                country = "TH"
            elif first_octet == 58:
                country = "CN"
            elif first_octet == 61:
                country = "AU"
            elif first_octet == 81:
                country = "JP"
            elif first_octet == 91:
                country = "DE"
            elif first_octet == 103:
                country = "ID"  # Indonesia
            elif first_octet == 110:
                country = "ID"  # Indonesia (Telkomsel)
            elif first_octet == 112:
                country = "ID"  # Indonesia (Indosat)
            elif first_octet == 114:
                country = "ID"  # Indonesia
            elif first_octet == 116:
                country = "ID"  # Indonesia (Tri)
            elif first_octet == 118:
                country = "ID"  # Indonesia
            elif first_octet == 125:
                country = "ID"  # Indonesia
            elif first_octet == 139:
                country = "ID"  # Indonesia
            elif first_octet == 180:
                country = "ID"  # Indonesia
            elif first_octet == 182:
                country = "ID"  # Indonesia
            elif first_octet == 202:
                country = "ID"  # Indonesia
            elif first_octet == 203:
                country = "ID"  # Indonesia
            elif first_octet == 36:
                country = "ID"  # Indonesia (XL)
            else:
                country = "UNKNOWN"
            
            if country == "ID":
                result["score_penalty"] -= 3  # Bonus untuk IP Indonesia
                result["recommendations"].append("IP appears to be from Indonesia - good for targeting")
            elif country == "UNKNOWN":
                result["warnings"].append("Cannot determine geolocation")
                result["score_penalty"] += 5
            else:
                result["warnings"].append(f"IP appears to be from {country}, not Indonesia")
                result["score_penalty"] += 15
                result["suspicious_factors"].append(f"foreign_country_{country}")
                result["recommendations"].append(f"Consider using Indonesian IP instead of {country}")
            
            # Check for geolocation anomalies
            if first_octet in [5, 31, 46, 62, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 109, 176, 185, 188, 193, 195]:
                # European/Russian ranges
                if country not in ["NL", "DE", "RU", "FR", "GB", "ES", "IT"]:
                    result["warnings"].append("IP range suggests European location but geolocation mismatch")
                    result["score_penalty"] += 8
                    result["suspicious_factors"].append("geolocation_mismatch")
            
            if first_octet in [1, 8, 12, 13, 23, 24, 32, 34, 35, 40, 44, 45, 50, 52, 54, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 96, 97, 98, 99, 100, 104, 107, 108, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155, 156, 157, 158, 159, 160, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 172, 173, 174, 192, 198, 199, 200, 204, 205, 206, 207, 208, 209, 216]:
                # US ranges
                if country != "US":
                    result["warnings"].append("IP range suggests US location but geolocation mismatch")
                    result["score_penalty"] += 8
                    result["suspicious_factors"].append("geolocation_mismatch")
            
        except Exception as e:
            result["warnings"].append(f"Geolocation validation error: {str(e)}")
            result["score_penalty"] += 5
        
        return result
    
    def _validate_network_properties(self, ip: str, strict: bool) -> Dict[str, Any]:
        """Validate network properties"""
        result = {
            "valid": True,
            "score_penalty": 0,
            "issues": [],
            "warnings": [],
            "suspicious_factors": [],
            "recommendations": []
        }
        
        try:
            parts = [int(p) for p in ip.split('.')]
            
            # Check for valid network address
            if parts[0] == 0:
                result["valid"] = False
                result["score_penalty"] = 100
                result["issues"].append("Invalid network address (first octet 0)")
                return result
            
            # Check for Class E addresses (experimental)
            if parts[0] >= 240:
                result["warnings"].append("IP is in Class E (experimental) range")
                result["score_penalty"] += 25
                result["suspicious_factors"].append("class_e_experimental")
                result["recommendations"].append("Avoid experimental IP ranges")
            
            # Check for Class D addresses (multicast)
            if 224 <= parts[0] <= 239:
                result["warnings"].append("IP is in Class D (multicast) range")
                result["score_penalty"] += 30
                result["suspicious_factors"].append("class_d_multicast")
                result["recommendations"].append("Avoid multicast IP ranges")
            
            # Check for APIPA address (Automatic Private IP Addressing)
            if parts[0] == 169 and parts[1] == 254:
                result["valid"] = False
                result["score_penalty"] = 100
                result["issues"].append("IP is APIPA address (169.254.x.x)")
                return result
            
            # Check for TEST-NET addresses
            if parts[0] == 192 and parts[1] == 0 and parts[2] == 2:
                result["warnings"].append("IP is in TEST-NET-1 range")
                result["score_penalty"] += 20
                result["suspicious_factors"].append("test_net_1")
            
            if parts[0] == 198 and parts[1] == 51 and parts[2] == 100:
                result["warnings"].append("IP is in TEST-NET-2 range")
                result["score_penalty"] += 20
                result["suspicious_factors"].append("test_net_2")
            
            if parts[0] == 203 and parts[1] == 0 and parts[2] == 113:
                result["warnings"].append("IP is in TEST-NET-3 range")
                result["score_penalty"] += 20
                result["suspicious_factors"].append("test_net_3")
            
            # Check for documentation addresses
            if parts[0] == 192 and parts[1] == 0 and parts[2] == 0:
                result["warnings"].append("IP is in documentation range")
                result["score_penalty"] += 15
                result["suspicious_factors"].append("documentation_range")
            
            # Check for 6to4 relay anycast addresses
            if parts[0] == 192 and parts[1] == 88 and parts[2] == 99:
                result["warnings"].append("IP is 6to4 relay anycast address")
                result["score_penalty"] += 25
                result["suspicious_factors"].append("6to4_relay")
            
            # Check for benchmarking addresses
            if parts[0] == 198 and parts[1] == 18:
                result["warnings"].append("IP is in benchmarking range")
                result["score_penalty"] += 15
                result["suspicious_factors"].append("benchmarking_range")
            
            # Check for invalid combinations
            if parts[0] == 255 and parts[1] == 255 and parts[2] == 255 and parts[3] == 255:
                result["valid"] = False
                result["score_penalty"] = 100
                result["issues"].append("IP is limited broadcast address")
                return result
            
            # Check for network vs host bits
            # Ini sederhana, hanya untuk edukasi
            if parts[0] < 128:  # Class A
                network_bits = 8
            elif parts[0] < 192:  # Class B
                network_bits = 16
            else:  # Class C
                network_bits = 24
            
            # Untuk IP publik, host bits tidak boleh semua 0 atau semua 1
            host_part = parts[3]
            if host_part == 0 or host_part == 255:
                result["warnings"].append(f"Host part ({host_part}) is network/broadcast address")
                result["score_penalty"] += 10
                result["suspicious_factors"].append("network_broadcast_host")
            
        except Exception as e:
            result["warnings"].append(f"Network properties validation error: {str(e)}")
            result["score_penalty"] += 5
        
        return result
    
    def _apply_strict_rules(self, result: Dict[str, Any]):
        """Apply strict validation rules"""
        ip = result["ip"]
        
        # Additional strict checks
        parts = ip.split('.')
        
        # Check for consecutive zeros
        if '0.0.0' in ip or '.0.0.' in ip:
            result["warnings"].append("Contains consecutive zeros")
            result["score_penalty"] += 5
            result["suspicious_factors"].append("consecutive_zeros")
        
        # Check for repeating patterns
        if len(set(parts)) <= 2:
            result["warnings"].append("Low octet diversity")
            result["score_penalty"] += 3
            result["suspicious_factors"].append("low_diversity")
        
        # Check for ascending/descending patterns
        try:
            int_parts = [int(p) for p in parts]
            if (int_parts[0] < int_parts[1] < int_parts[2] < int_parts[3] or
                int_parts[0] > int_parts[1] > int_parts[2] > int_parts[3]):
                result["warnings"].append("Monotonic octet pattern")
                result["score_penalty"] += 4
                result["suspicious_factors"].append("monotonic_pattern")
        except:
            pass
        
        # Check for palindrome pattern
        if parts == parts[::-1]:
            result["warnings"].append("Palindrome IP pattern")
            result["score_penalty"] += 6
            result["suspicious_factors"].append("palindrome_pattern")
    
    def bulk_validate(self, ips: List[str]) -> Dict[str, List[Dict[str, Any]]]:
        """Validate multiple IPs at once"""
        results = {
            "valid": [],
            "risky": [],
            "invalid": [],
            "statistics": {
                "total": len(ips),
                "valid_count": 0,
                "avg_score": 0,
                "category_distribution": {}
            }
        }
        
        total_score = 0
        category_counts = {}
        
        for ip in ips:
            validation = self.validate(ip)
            
            if validation["valid"]:
                if validation["score"] >= 70:
                    results["valid"].append(validation)
                elif validation["score"] >= 50:
                    results["risky"].append(validation)
                else:
                    results["invalid"].append(validation)
                
                if validation["valid"]:
                    results["statistics"]["valid_count"] += 1
                    total_score += validation["score"]
                    
                    # Count categories
                    category = validation.get("category", "unknown")
                    category_counts[category] = category_counts.get(category, 0) + 1
            else:
                results["invalid"].append(validation)
        
        # Update statistics
        if results["statistics"]["valid_count"] > 0:
            results["statistics"]["avg_score"] = total_score / results["statistics"]["valid_count"]
        
        results["statistics"]["category_distribution"] = category_counts
        
        return results

# ===================== WEBRTC & WEBGL SPOOFING 2025 =====================

class WebRTCWebGL_Spoofing2025:
    """Enhanced WebRTC dan WebGL spoofing dengan lebih banyak detail"""
    
    def __init__(self):
        self.webrtc_configs = self._generate_enhanced_webrtc_configs()
        self.webgl_configs = self._generate_enhanced_webgl_configs()
        self.canvas_configs = self._generate_enhanced_canvas_configs()
        self.audio_configs = self._generate_enhanced_audio_configs()
        self.font_configs = self._generate_font_configs()
        self.screen_configs = self._generate_screen_configs()
        
    def _generate_enhanced_webrtc_configs(self) -> Dict[str, Any]:
        """Generate enhanced WebRTC configurations for Desktop browsers"""
        return {
            "desktop_chrome_windows": {
                "iceServers": [
                    {"urls": ["stun:stun.l.google.com:19302"]},
                    {"urls": ["stun:stun1.l.google.com:19302"]},
                    {"urls": ["stun:stun2.l.google.com:19302"]},
                    {"urls": ["stun:stun3.l.google.com:19302"]},
                    {"urls": ["stun:stun4.l.google.com:19302"]}
                ],
                "iceTransportPolicy": "all",
                "bundlePolicy": "max-bundle",
                "rtcpMuxPolicy": "require",
                "iceCandidatePoolSize": 0,
                "sdpSemantics": "unified-plan",
                "optional": [
                    {"googDscp": True},
                    {"googCpuOveruseDetection": True},
                    {"googCpuOveruseEncodeUsage": True},
                    {"googHighStartBitrate": 300},
                    {"googPayloadPadding": True}
                ]
            },
            "desktop_chrome_macos": {
                "iceServers": [
                    {"urls": ["stun:stun.l.google.com:19302"]},
                    {"urls": ["stun:stun1.l.google.com:19302"]},
                    {"urls": ["stun:stun2.l.google.com:19302"]},
                    {"urls": ["stun:stun3.l.google.com:19302"]}
                ],
                "iceTransportPolicy": "all",
                "bundlePolicy": "max-bundle",
                "rtcpMuxPolicy": "require",
                "iceCandidatePoolSize": 0,
                "sdpSemantics": "unified-plan",
                "optional": [
                    {"googDscp": True},
                    {"googCpuOveruseDetection": True}
                ]
            },
            "android_chrome_samsung": {
                "iceServers": [
                    {"urls": ["stun:stun.l.google.com:19302"]},
                    {"urls": ["stun:stun1.l.google.com:19302"]},
                    {"urls": ["stun:stun2.l.google.com:19302"]},
                    {"urls": ["stun:stun3.l.google.com:19302"]},
                    {"urls": ["stun:stun4.l.google.com:19302"]}
                ],
                "iceTransportPolicy": "all",
                "bundlePolicy": "max-bundle",
                "rtcpMuxPolicy": "require",
                "iceCandidatePoolSize": 0,
                "sdpSemantics": "unified-plan",
                "optional": [
                    {"googDscp": True},
                    {"googCpuOveruseDetection": True},
                    {"googCpuOveruseEncodeUsage": True},
                    {"googHighStartBitrate": 300},
                    {"googPayloadPadding": True}
                ]
            },
            "android_chrome_xiaomi": {
                "iceServers": [
                    {"urls": ["stun:stun.l.google.com:19302"]},
                    {"urls": ["stun:stun1.l.google.com:19302"]},
                    {"urls": ["stun:stun2.l.google.com:19302"]}
                ],
                "iceTransportPolicy": "all",
                "bundlePolicy": "balanced",
                "rtcpMuxPolicy": "require",
                "iceCandidatePoolSize": 0,
                "sdpSemantics": "unified-plan"
            },
            "ios_safari": {
                "iceServers": [
                    {"urls": ["stun:stun.l.google.com:19302"]},
                    {"urls": ["stun:stun1.l.google.com:19302"]}
                ],
                "iceTransportPolicy": "all",
                "bundlePolicy": "max-compat",
                "rtcpMuxPolicy": "require",
                "iceCandidatePoolSize": 0,
                "sdpSemantics": "plan-b"
            }
        }
    
    def _generate_enhanced_webgl_configs(self) -> Dict[str, Any]:
        """Generate enhanced WebGL configurations for Desktop"""
        return {
            "nvidia_desktop": {
                "vendor": "NVIDIA Corporation",
                "renderer": random.choice([
                    "NVIDIA GeForce RTX 4090/PCIe/SSE2",
                    "NVIDIA GeForce RTX 4080/PCIe/SSE2",
                    "NVIDIA GeForce RTX 3080/PCIe/SSE2",
                    "NVIDIA GeForce RTX 3070/PCIe/SSE2",
                    "NVIDIA GeForce GTX 1660 Ti/PCIe/SSE2"
                ]),
                "version": "WebGL 2.0 (OpenGL ES 3.0 Chromium)",
                "shading_language": "WebGL GLSL ES 3.00",
                "max_texture_size": 16384,
                "max_viewport_dims": [32767, 32767],
            },
            "intel_desktop": {
                "vendor": "Intel Inc.",
                "renderer": random.choice([
                    "Intel(R) UHD Graphics 770",
                    "Intel(R) Iris(R) Xe Graphics",
                    "Intel(R) UHD Graphics 630",
                    "Intel(R) HD Graphics 620"
                ]),
                "version": "WebGL 2.0 (OpenGL ES 3.0 Chromium)",
                "shading_language": "WebGL GLSL ES 3.00",
                "max_texture_size": 16384,
                "max_viewport_dims": [16384, 16384],
            },
            "amd_desktop": {
                "vendor": "AMD",
                "renderer": random.choice([
                    "AMD Radeon RX 7900 XTX",
                    "AMD Radeon RX 6800 XT",
                    "AMD Radeon RX 6700 XT",
                    "AMD Radeon RX 580"
                ]),
                "version": "WebGL 2.0 (OpenGL ES 3.0 Chromium)",
                "shading_language": "WebGL GLSL ES 3.00",
                "max_texture_size": 16384,
                "max_viewport_dims": [16384, 16384],
            },
            "apple_gpu": {
                "vendor": "Apple Inc.",
                "renderer": random.choice([
                    "Apple M3 Pro",
                    "Apple M3 Max",
                    "Apple M2 Pro",
                    "Apple M1 Pro"
                ]),
                "version": "WebGL 2.0 (OpenGL ES 3.0 Metal)",
                "shading_language": "WebGL GLSL ES 3.00",
                "max_texture_size": 16384,
                "max_viewport_dims": [16384, 16384],
            },
            "adreno_750": {
                "vendor": "Qualcomm",
                "renderer": "Adreno (TM) 750",
                "version": "OpenGL ES 3.2 V@510.0 (GIT@8b48ae5, I95c5c9b3a4, 1733004697) (Date:07/31/2024)",
                "shading_language": "OpenGL ES GLSL ES 3.20",
                "max_texture_size": 16384,
                "max_viewport_dims": [16384, 16384],
                "aliased_line_width_range": [1, 1],
                "aliased_point_size_range": [1, 1024],
                "alpha_bits": 8,
                "blue_bits": 8,
                "green_bits": 8,
                "red_bits": 8,
                "depth_bits": 24,
                "stencil_bits": 8,
                "max_vertex_attribs": 16,
                "max_vertex_uniform_vectors": 256,
                "max_varying_vectors": 15,
                "max_fragment_uniform_vectors": 224,
                "max_texture_image_units": 16,
                "max_combined_texture_image_units": 32,
                "max_cube_map_texture_size": 16384,
                "max_renderbuffer_size": 16384,
                "max_vertex_texture_image_units": 16,
                "max_color_attachments": 4,
                "max_draw_buffers": 4,
                "max_transform_feedback_separate_attribs": 4,
                "shader_precision": {
                    "high_float": [127, 127],
                    "medium_float": [127, 127],
                    "low_float": [127, 127],
                    "high_int": [31, 30],
                    "medium_int": [31, 30],
                    "low_int": [31, 30]
                }
            },
            "apple_gpu": {
                "vendor": "Apple Inc.",
                "renderer": "Apple GPU",
                "version": "WebGL 2.0 (OpenGL ES 3.2 Metal - 86.4)",
                "shading_language": "WebGL GLSL ES 3.00",
                "max_texture_size": 16384,
                "max_viewport_dims": [16384, 16384],
                "aliased_line_width_range": [1, 1],
                "aliased_point_size_range": [1, 1024],
                "alpha_bits": 8,
                "blue_bits": 8,
                "green_bits": 8,
                "red_bits": 8,
                "depth_bits": 24,
                "stencil_bits": 8,
                "max_vertex_attribs": 16,
                "max_vertex_uniform_vectors": 256,
                "max_varying_vectors": 15,
                "max_fragment_uniform_vectors": 224,
                "max_texture_image_units": 16,
                "max_combined_texture_image_units": 32,
                "max_cube_map_texture_size": 16384,
                "max_renderbuffer_size": 16384,
                "max_vertex_texture_image_units": 16
            },
            "mali_g710": {
                "vendor": "ARM",
                "renderer": "Mali-G710",
                "version": "OpenGL ES 3.2 v1.r32p1-01eac0.1a4d0b0b3c0f9c0d1e2f3a4b5c6d7e8f9",
                "shading_language": "OpenGL ES GLSL ES 3.20",
                "max_texture_size": 16384,
                "max_viewport_dims": [16384, 16384],
                "aliased_line_width_range": [1, 1],
                "aliased_point_size_range": [1, 1024],
                "alpha_bits": 8,
                "blue_bits": 8,
                "green_bits": 8,
                "red_bits": 8,
                "depth_bits": 24,
                "stencil_bits": 8,
                "max_vertex_attribs": 16,
                "max_vertex_uniform_vectors": 256,
                "max_varying_vectors": 15,
                "max_fragment_uniform_vectors": 224,
                "max_texture_image_units": 16,
                "max_combined_texture_image_units": 32,
                "max_cube_map_texture_size": 16384,
                "max_renderbuffer_size": 16384,
                "max_vertex_texture_image_units": 16
            }
        }
    
    def _generate_enhanced_canvas_configs(self) -> Dict[str, Any]:
        """Generate enhanced canvas configurations"""
        return {
            "samsung_galaxy_s24": {
                "width": 1080,
                "height": 2400,
                "color_depth": 24,
                "pixel_ratio": 3.0,
                "font_smoothing": "antialiased",
                "text_rendering": "optimizeLegibility",
                "image_smoothing": True,
                "pattern_quality": "good",
                "global_composite_operation": "source-over",
                "shadow_color": "rgba(0, 0, 0, 0.5)",
                "shadow_blur": 5,
                "shadow_offset_x": 2,
                "shadow_offset_y": 2,
                "line_cap": "butt",
                "line_join": "miter",
                "miter_limit": 10,
                "global_alpha": 1.0
            },
            "xiaomi_14_pro": {
                "width": 1440,
                "height": 3200,
                "color_depth": 30,
                "pixel_ratio": 3.5,
                "font_smoothing": "subpixel-antialiased",
                "text_rendering": "optimizeLegibility",
                "image_smoothing": True,
                "pattern_quality": "best",
                "global_composite_operation": "source-over",
                "shadow_color": "rgba(0, 0, 0, 0.5)",
                "shadow_blur": 5,
                "shadow_offset_x": 2,
                "shadow_offset_y": 2,
                "line_cap": "round",
                "line_join": "round",
                "miter_limit": 10,
                "global_alpha": 1.0
            },
            "iphone_16_pro": {
                "width": 1170,
                "height": 2532,
                "color_depth": 30,
                "pixel_ratio": 3.0,
                "font_smoothing": "subpixel-antialiased",
                "text_rendering": "optimizeLegibility",
                "image_smoothing": True,
                "pattern_quality": "best",
                "global_composite_operation": "source-over",
                "shadow_color": "rgba(0, 0, 0, 0.5)",
                "shadow_blur": 5,
                "shadow_offset_x": 2,
                "shadow_offset_y": 2,
                "line_cap": "butt",
                "line_join": "miter",
                "miter_limit": 10,
                "global_alpha": 1.0
            }
        }
    
    def _generate_enhanced_audio_configs(self) -> Dict[str, Any]:
        """Generate enhanced audio configurations"""
        return {
            "android_samsung": {
                "sample_rate": 48000,
                "channel_count": 2,
                "buffer_size": 4096,
                "latency": 0.01,
                "fft_size": 2048,
                "smoothing_time_constant": 0.8,
                "min_decibels": -100,
                "max_decibels": -30,
                "frequency_bin_count": 1024,
                "channel_interpretation": "speakers",
                "channel_count_mode": "max"
            },
            "android_xiaomi": {
                "sample_rate": 48000,
                "channel_count": 2,
                "buffer_size": 2048,
                "latency": 0.02,
                "fft_size": 1024,
                "smoothing_time_constant": 0.9,
                "min_decibels": -100,
                "max_decibels": -30,
                "frequency_bin_count": 512,
                "channel_interpretation": "speakers",
                "channel_count_mode": "max"
            },
            "ios": {
                "sample_rate": 44100,
                "channel_count": 2,
                "buffer_size": 2048,
                "latency": 0.02,
                "fft_size": 1024,
                "smoothing_time_constant": 0.9,
                "min_decibels": -100,
                "max_decibels": -30,
                "frequency_bin_count": 512,
                "channel_interpretation": "speakers",
                "channel_count_mode": "max"
            }
        }
    
    def _generate_font_configs(self) -> Dict[str, Any]:
        """Generate font configurations"""
        return {
            "android_samsung": {
                "fonts": [
                    "Roboto",
                    "SamsungOne",
                    "Noto Sans",
                    "Samsung Sans",
                    "Google Sans",
                    "Segoe UI",
                    "Arial",
                    "Helvetica",
                    "Times New Roman",
                    "Courier New"
                ],
                "font_smoothing": "antialiased",
                "font_kerning": "auto",
                "font_variant": "normal",
                "font_stretch": "normal"
            },
            "android_xiaomi": {
                "fonts": [
                    "MiSans",
                    "Roboto",
                    "Noto Sans",
                    "Google Sans",
                    "Arial",
                    "Helvetica",
                    "Times New Roman",
                    "Courier New"
                ],
                "font_smoothing": "subpixel-antialiased",
                "font_kerning": "auto",
                "font_variant": "normal",
                "font_stretch": "normal"
            },
            "ios": {
                "fonts": [
                    "San Francisco",
                    "Helvetica Neue",
                    "Arial",
                    "Times New Roman",
                    "Courier New",
                    "Georgia",
                    "Palatino",
                    "Verdana"
                ],
                "font_smoothing": "subpixel-antialiased",
                "font_kerning": "auto",
                "font_variant": "normal",
                "font_stretch": "normal"
            }
        }
    
    def _generate_screen_configs(self) -> Dict[str, Any]:
        """Generate screen configurations"""
        return {
            "samsung_galaxy_s24": {
                "width": 1080,
                "height": 2400,
                "avail_width": 1080,
                "avail_height": 2340,
                "color_depth": 24,
                "pixel_depth": 24,
                "orientation": {
                    "type": "portrait-primary",
                    "angle": 0
                },
                "device_pixel_ratio": 3.0,
                "touch_support": True,
                "max_touch_points": 10,
                "hdr": True,
                "color_gamut": "p3",
                "contrast": "no-preference"
            },
            "xiaomi_14_pro": {
                "width": 1440,
                "height": 3200,
                "avail_width": 1440,
                "avail_height": 3140,
                "color_depth": 30,
                "pixel_depth": 30,
                "orientation": {
                    "type": "portrait-primary",
                    "angle": 0
                },
                "device_pixel_ratio": 3.5,
                "touch_support": True,
                "max_touch_points": 10,
                "hdr": True,
                "color_gamut": "p3",
                "contrast": "no-preference"
            },
            "iphone_16_pro": {
                "width": 1170,
                "height": 2532,
                "avail_width": 1170,
                "avail_height": 2472,
                "color_depth": 30,
                "pixel_depth": 30,
                "orientation": {
                    "type": "portrait-primary",
                    "angle": 0
                },
                "device_pixel_ratio": 3.0,
                "touch_support": True,
                "max_touch_points": 5,
                "hdr": True,
                "color_gamut": "p3",
                "contrast": "no-preference"
            }
        }
    
    def get_complete_fingerprint(self, device_type: str = "desktop", brand: str = "windows", connection_type: str = "wifi") -> Dict[str, Any]:
        """Get complete fingerprint that matches real desktop device characteristics for Web API.
        
        Fingerprints are generated to be consistent with desktop browser profile
        and avoid unique identifiers that could be used for tracking.
        """
        # Always use desktop profiles for Web API
        platform_choice = random.choice(["windows", "macos"])
        
        if platform_choice == "macos":
            webrtc_profile = "desktop_chrome_macos"
            webgl_profile = "apple_gpu"
            canvas_profile = "macbook_pro"
            audio_profile = "desktop_macos"
            font_profile = "desktop_macos"
            screen_profile = "macbook_pro"
        else:
            # Default Windows desktop
            webrtc_profile = "desktop_chrome_windows"
            webgl_profile = random.choice(["nvidia_desktop", "intel_desktop", "amd_desktop"])
            canvas_profile = "windows_desktop"
            audio_profile = "desktop_windows"
            font_profile = "desktop_windows"
            screen_profile = "windows_desktop"
        
        # Generate fingerprint with realistic desktop values
        fingerprint = {
            "webrtc": self.get_webrtc_fingerprint(webrtc_profile),
            "webgl": self.get_webgl_fingerprint(webgl_profile),
            "canvas": self.get_canvas_fingerprint(canvas_profile),
            "audio": self.get_audio_fingerprint(audio_profile),
            "fonts": self.font_configs.get(font_profile, {}),
            "screen": self.screen_configs.get(screen_profile, {}),
            "device_type": "desktop",
            "brand": platform_choice,
            "connection_type": "wifi",
        }
        
        return fingerprint
    
    def get_webrtc_fingerprint(self, profile: str = "desktop_chrome_windows") -> Dict[str, Any]:
        """Get realistic WebRTC fingerprint matching real desktop browser behavior."""
        config = self.webrtc_configs.get(profile, self.webrtc_configs["desktop_chrome_windows"])
        
        # Generate ICE candidates that match real device behavior
        ice_candidates = self._generate_ice_candidates_enhanced()
        
        # Generate SDP
        sdp = self._generate_sdp_enhanced(profile)
        
        return {
            "config": config,
            "ice_candidates": ice_candidates,
            "local_description": {
                "type": "offer",
                "sdp": sdp
            }
        }
    
    def _generate_ice_candidates_enhanced(self) -> List[Dict[str, Any]]:
        """Generate realistic ICE candidates matching real WebRTC behavior."""
        candidates = []
        # Host candidates are most common in mobile scenarios
        candidate_types = ["host", "host", "srflx"]
        
        for i in range(random.randint(2, 4)):
            candidate_type = random.choice(candidate_types)
            
            if candidate_type == "host":
                foundation = random.randint(1000, 9999)
                component_id = 1
                transport = "udp"
                # Realistic priority range for host candidates
                priority = random.randint(2113929216, 2113939216)
                # Common private IP ranges
                local_ip = f"192.168.{random.randint(0, 255)}.{random.randint(2, 254)}"
                port = random.randint(49152, 65535)  # Ephemeral port range
                typ = "host"
                
                candidate = {
                    "candidate": f"candidate:{foundation} {component_id} {transport} {priority} {local_ip} {port} typ {typ}",
                    "sdpMid": "0",
                    "sdpMLineIndex": 0,
                    "type": typ,
                    "protocol": transport,
                    "address": local_ip,
                    "port": port,
                    "priority": priority
                }
                
            else:  # srflx
                foundation = random.randint(1000, 9999)
                component_id = 1
                transport = "udp"
                # Realistic priority for server reflexive candidates
                priority = random.randint(1677720576, 1677730576)
                local_ip = f"192.168.{random.randint(0, 255)}.{random.randint(2, 254)}"
                port = random.randint(49152, 65535)
                typ = "srflx"
                
                candidate = {
                    "candidate": f"candidate:{foundation} {component_id} {transport} {priority} {local_ip} {port} typ {typ}",
                    "sdpMid": "0",
                    "sdpMLineIndex": 0,
                    "type": typ,
                    "protocol": transport,
                    "address": local_ip,
                    "port": port,
                    "priority": priority
                }
            
            candidates.append(candidate)
        
        return candidates
    
    def _generate_sdp_enhanced(self, profile: str) -> str:
        """Generate enhanced SDP string"""
        # Generate unique identifiers
        session_id = random.randint(1000000000, 9999999999)
        session_version = 2
        ufrag = str(uuid.uuid4())[:8]
        pwd = str(uuid.uuid4())[:24]
        fingerprint = self._generate_fingerprint_enhanced()
        
        sdp_lines = [
            f"v=0",
            f"o=- {session_id} {session_version} IN IP4 0.0.0.0",
            f"s=-",
            f"t=0 0",
            f"a=group:BUNDLE 0",
            f"a=extmap-allow-mixed",
            f"a=msid-semantic: WMS *",
            f"m=application 9 UDP/DTLS/SCTP webrtc-datachannel",
            f"c=IN IP4 0.0.0.0",
            f"a=ice-ufrag:{ufrag}",
            f"a=ice-pwd:{pwd}",
            f"a=ice-options:trickle",
            f"a=fingerprint:sha-256 {fingerprint}",
            f"a=setup:actpass",
            f"a=mid:0",
            f"a=sctp-port:5000",
            f"a=max-message-size:262144"
        ]
        
        # Tambahkan atribut berdasarkan profile
        if "samsung" in profile:
            sdp_lines.extend([
                f"a=rtcp-mux",
                f"a=rtcp-rsize",
                f"a=sctpmap:5000 webrtc-datachannel 256"
            ])
        elif "xiaomi" in profile:
            sdp_lines.extend([
                f"a=rtcp-mux",
                f"a=sctpmap:5000 webrtc-datachannel 128"
            ])
        else:
            sdp_lines.extend([
                f"a=rtcp-mux",
                f"a=sctpmap:5000 webrtc-datachannel 256"
            ])
        
        return "\r\n".join(sdp_lines)
    
    def _generate_fingerprint_enhanced(self) -> str:
        """Generate enhanced SSL fingerprint"""
        # Generate random bytes untuk fingerprint
        random_bytes = os.urandom(32)
        
        # Hash dengan SHA-256
        hash_obj = hashlib.sha256(random_bytes)
        fingerprint = hash_obj.hexdigest().upper()
        
        # Format sebagai colon-separated hex
        formatted = ':'.join(fingerprint[i:i+2] for i in range(0, len(fingerprint), 2))
        
        return formatted
    
    def get_webgl_fingerprint(self, profile: str = "adreno_750") -> Dict[str, Any]:
        """Get realistic WebGL fingerprint matching real GPU characteristics."""
        # Create a copy to avoid modifying the original config
        config = dict(self.webgl_configs.get(profile, self.webgl_configs["adreno_750"]))
        
        # Add realistic extensions for the GPU profile
        config["extensions"] = self._get_webgl_extensions_enhanced(profile)
        
        # Add WebGL parameters
        config["parameters"] = self._get_webgl_parameters_enhanced(profile)
        
        return config
    
    def _get_webgl_extensions_enhanced(self, profile: str) -> List[str]:
        """Get enhanced WebGL extensions"""
        common_extensions = [
            "EXT_blend_minmax", "EXT_color_buffer_float", "EXT_color_buffer_half_float",
            "EXT_float_blend", "EXT_texture_filter_anisotropic", "OES_element_index_uint",
            "OES_fbo_render_mipmap", "OES_standard_derivatives", "OES_texture_float",
            "OES_texture_float_linear", "OES_texture_half_float", "OES_texture_half_float_linear",
            "OES_vertex_array_object", "WEBGL_color_buffer_float", "WEBGL_compressed_texture_astc",
            "WEBGL_compressed_texture_etc", "WEBGL_compressed_texture_etc1",
            "WEBGL_compressed_texture_s3tc", "WEBGL_debug_renderer_info", "WEBGL_debug_shaders",
            "WEBGL_depth_texture", "WEBGL_draw_buffers", "WEBGL_lose_context",
            "WEBGL_multi_draw", "WEBGL_polygon_mode", "WEBGL_provoking_vertex",
            "WEBGL_shader_pixel_local_storage", "WEBGL_stencil_texturing",
            "KHR_parallel_shader_compile", "EXT_disjoint_timer_query_webgl2"
        ]
        
        if "adreno" in profile:
            # Adreno-specific extensions
            additional = [
                "QCOM_texture_foveated", "QCOM_shader_framebuffer_fetch_noncoherent",
                "QCOM_shader_framebuffer_fetch_rate", "QCOM_motion_estimation"
            ]
            common_extensions.extend(additional)
        elif "mali" in profile:
            # Mali-specific extensions
            additional = [
                "ARM_mali_program_binary", "ARM_mali_shader_binary",
                "ARM_shader_framebuffer_fetch", "ARM_shader_framebuffer_fetch_depth_stencil"
            ]
            common_extensions.extend(additional)
        elif "apple" in profile:
            # Apple-specific extensions
            additional = [
                "APPLE_clip_distance", "APPLE_framebuffer_multisample",
                "APPLE_rgb_422", "APPLE_texture_format_BGRA8888",
                "APPLE_texture_max_level"
            ]
            common_extensions.extend(additional)
        
        # Pilih random extensions dengan bias
        if profile == "adreno_750":
            num_extensions = random.randint(25, 35)
        elif profile == "mali_g710":
            num_extensions = random.randint(22, 30)
        else:
            num_extensions = random.randint(20, 28)
        
        selected = random.sample(common_extensions, min(num_extensions, len(common_extensions)))
        
        # Sort untuk konsistensi
        selected.sort()
        
        return selected
    
    def _get_webgl_parameters_enhanced(self, profile: str) -> Dict[str, Any]:
        """Get enhanced WebGL parameters"""
        if "adreno" in profile:
            return {
                "MAX_VERTEX_UNIFORM_BLOCKS": 14,
                "MAX_FRAGMENT_UNIFORM_BLOCKS": 14,
                "MAX_COMBINED_UNIFORM_BLOCKS": 70,
                "MAX_UNIFORM_BUFFER_BINDINGS": 70,
                "MAX_UNIFORM_BLOCK_SIZE": 65536,
                "MAX_VARYING_COMPONENTS": 124,
                "MAX_VERTEX_OUTPUT_COMPONENTS": 128,
                "MAX_FRAGMENT_INPUT_COMPONENTS": 128,
                "MAX_PROGRAM_TEXEL_OFFSET": 7,
                "MIN_PROGRAM_TEXEL_OFFSET": -8,
                "MAX_VIEWPORT_DIMS": [16384, 16384],
                "MAX_ELEMENT_INDEX": 4294967295,
                "MAX_DRAW_BUFFERS": 4,
                "MAX_COLOR_ATTACHMENTS": 4,
                "MAX_SAMPLES": 4
            }
        elif "mali" in profile:
            return {
                "MAX_VERTEX_UNIFORM_BLOCKS": 12,
                "MAX_FRAGMENT_UNIFORM_BLOCKS": 12,
                "MAX_COMBINED_UNIFORM_BLOCKS": 60,
                "MAX_UNIFORM_BUFFER_BINDINGS": 60,
                "MAX_UNIFORM_BLOCK_SIZE": 65536,
                "MAX_VARYING_COMPONENTS": 112,
                "MAX_VERTEX_OUTPUT_COMPONENTS": 128,
                "MAX_FRAGMENT_INPUT_COMPONENTS": 128,
                "MAX_PROGRAM_TEXEL_OFFSET": 7,
                "MIN_PROGRAM_TEXEL_OFFSET": -8,
                "MAX_VIEWPORT_DIMS": [16384, 16384],
                "MAX_ELEMENT_INDEX": 4294967295,
                "MAX_DRAW_BUFFERS": 4,
                "MAX_COLOR_ATTACHMENTS": 4,
                "MAX_SAMPLES": 4
            }
        else:  # apple
            return {
                "MAX_VERTEX_UNIFORM_BLOCKS": 14,
                "MAX_FRAGMENT_UNIFORM_BLOCKS": 14,
                "MAX_COMBINED_UNIFORM_BLOCKS": 70,
                "MAX_UNIFORM_BUFFER_BINDINGS": 70,
                "MAX_UNIFORM_BLOCK_SIZE": 65536,
                "MAX_VARYING_COMPONENTS": 124,
                "MAX_VERTEX_OUTPUT_COMPONENTS": 128,
                "MAX_FRAGMENT_INPUT_COMPONENTS": 128,
                "MAX_PROGRAM_TEXEL_OFFSET": 7,
                "MIN_PROGRAM_TEXEL_OFFSET": -8,
                "MAX_VIEWPORT_DIMS": [16384, 16384],
                "MAX_ELEMENT_INDEX": 4294967295,
                "MAX_DRAW_BUFFERS": 4,
                "MAX_COLOR_ATTACHMENTS": 4,
                "MAX_SAMPLES": 4
            }
    
    def get_canvas_fingerprint(self, profile: str = "samsung_galaxy_s24") -> Dict[str, Any]:
        """Get realistic canvas fingerprint matching real device rendering.
        
        Returns standard canvas configuration without unique identifiers.
        """
        config = dict(self.canvas_configs.get(profile, self.canvas_configs["samsung_galaxy_s24"]))
        
        # Add standard canvas capabilities (these are constant for a device type)
        config["composite_operations"] = [
            "source-over", "source-in", "source-out", "source-atop",
            "destination-over", "destination-in", "destination-out", "destination-atop",
            "lighter", "copy", "xor", "multiply", "screen", "overlay",
            "darken", "lighten", "color-dodge", "color-burn", "hard-light",
            "soft-light", "difference", "exclusion", "hue", "saturation",
            "color", "luminosity"
        ]
        config["line_caps"] = ["butt", "round", "square"]
        config["line_joins"] = ["bevel", "round", "miter"]
        
        return config
    
    def get_audio_fingerprint(self, profile: str = "android_samsung") -> Dict[str, Any]:
        """Get realistic audio fingerprint matching real device audio context.
        
        Returns standard audio configuration consistent with the device profile.
        """
        config = dict(self.audio_configs.get(profile, self.audio_configs["android_samsung"]))
        
        # Standard audio capabilities for the device
        config["fft_size_options"] = [2048, 4096, 8192, 16384]
        config["channel_interpretation"] = "speakers"
        config["channel_count_mode"] = "max"
        
        return config

# ===================== CLOUDFLARE & CDN BYPASS 2025 =====================

class CloudflareCDN_Bypass2025:
    """Sistem bypass Cloudflare dan CDN 2025"""
    
    def __init__(self):
        self.cf_versions = self._get_cf_versions_2025()
        self.cdn_providers = self._get_cdn_providers_2025()
        self.challenge_solvers = self._get_challenge_solvers_2025()
        self.cookie_jars = {}
        
    def _get_cf_versions_2025(self) -> Dict[str, Any]:
        """Get Cloudflare versions 2025"""
        return {
            "turnstile_v2": {
                "version": "2.0",
                "sitekey_patterns": ["0x4AAAAAA", "0x4AAAAAB", "0x4AAAAAC"],
                "endpoint": "https://challenges.cloudflare.com/turnstile/v0",
                "timeout": 30,
                "retries": 3
            },
            "turnstile_v3": {
                "version": "3.0",
                "sitekey_patterns": ["0x4AAAAAA", "0x4AAAAAB", "0x4AAAAAC"],
                "endpoint": "https://challenges.cloudflare.com/turnstile/v0",
                "timeout": 45,
                "retries": 5
            },
            "cf_challenge": {
                "version": "managed",
                "jschl_pattern": r"setTimeout\(function\(\){\s*var.*?f,\s*(.*?);",
                "jschl_vc_pattern": r'name="jschl_vc" value="(\w+)"',
                "jschl_pass_pattern": r'name="pass" value="(.+?)"',
                "timeout": 60,
                "retries": 3
            }
        }
    
    def _get_cdn_providers_2025(self) -> Dict[str, Any]:
        """Get CDN providers 2025"""
        return {
            "cloudflare": {
                "headers": {
                    "CF-IPCountry": "ID",
                    "CF-Ray": lambda: f"{random.randint(1000000000, 9999999999)}-{random.choice(['SIN', 'CGK', 'JKT'])}",
                    "CF-Cache-Status": random.choice(["HIT", "MISS", "EXPIRED"]),
                    "CF-Connecting-IP": "",
                    "CF-Request-ID": str(uuid.uuid4())[:32]
                },
                "cookies": ["__cf_bm", "__cfduid", "_cfuvid"],
                "worker_script": True
            },
            "akamai": {
                "headers": {
                    "X-Akamai-Transformed": "9",
                    "X-Akamai-Request-ID": str(uuid.uuid4()),
                    "X-Akamai-Config-Log-Detail": "true",
                    "X-Akamai-Session-Info": str(uuid.uuid4())[:16]
                },
                "cookies": ["ak_bmsc", "akac"],
                "edge_cache": True
            },
            "fastly": {
                "headers": {
                    "X-Fastly-Request-ID": str(uuid.uuid4()),
                    "X-Cache": random.choice(["HIT", "MISS"]),
                    "X-Cache-Hits": str(random.randint(0, 5)),
                    "X-Served-By": f"cache-{random.choice(['SIN', 'CGK'])}"
                },
                "cookies": ["_fastly_session"],
                "geo_routing": True
            },
            "sucuri": {
                "headers": {
                    "X-Sucuri-ID": str(random.randint(100000, 999999)),
                    "X-Sucuri-Cache": random.choice(["HIT", "MISS"]),
                    "X-Sucuri-Block": "0"
                },
                "cookies": ["sucuri_cloudproxy_uuid"],
                "waf": True
            }
        }
    
    def _get_challenge_solvers_2025(self) -> Dict[str, Any]:
        """Get challenge solvers 2025"""
        return {
            "turnstile": {
                "solver_type": "javascript",
                "requires_interaction": False,
                "timeout": 30000,
                "callback": "onTurnstileSuccess",
                "widget_id": "cf-turnstile"
            },
            "recaptcha_v3": {
                "solver_type": "token",
                "requires_interaction": False,
                "score_threshold": 0.7,
                "action": "submit",
                "timeout": 45000
            },
            "hcaptcha": {
                "solver_type": "javascript",
                "requires_interaction": True,
                "sitekey": "a5f74b19-9e45-40e0-b45d-07ff9e7fbc29",
                "timeout": 60000
            },
            "arkose_labs": {
                "solver_type": "websocket",
                "requires_interaction": True,
                "public_key": "35536E1E-65B4-4D96-9D97-6ADB7EFF8147",
                "timeout": 90000
            }
        }
    
    def detect_cdn_provider(self, headers: Dict[str, str], cookies: Dict[str, str]) -> Optional[str]:
        """Deteksi CDN provider dari headers dan cookies"""
        for provider, config in self.cdn_providers.items():
            # Check headers
            provider_headers = config["headers"]
            for header in provider_headers:
                if header in headers:
                    return provider
            
            # Check cookies
            provider_cookies = config["cookies"]
            for cookie in provider_cookies:
                if cookie in cookies:
                    return provider
        
        return None
    
    def get_cdn_headers(self, provider: str, ip_config: Dict[str, Any]) -> Dict[str, str]:
        """Dapatkan headers untuk CDN tertentu"""
        if provider not in self.cdn_providers:
            provider = "cloudflare"  # Default
        
        config = self.cdn_providers[provider]
        headers = {}
        
        for header, value in config["headers"].items():
            if callable(value):
                headers[header] = value()
            elif header == "CF-Connecting-IP":
                headers[header] = ip_config.get("ip", "")
            else:
                headers[header] = value
        
        return headers
    
    def solve_turnstile_challenge(self, sitekey: str, page_url: str) -> Optional[str]:
        """Solve Turnstile challenge"""
        print(f"{cyan}🛡️   Solving Turnstile challenge...{reset}")
        
        try:
            # Generate fake token (dalam real implementation, gunakan solving service)
            token = base64.b64encode(f"{sitekey}:{int(time.time())}:{random.getrandbits(128)}".encode()).decode()
            
            # Format: token|action|timestamp|score
            turnstile_token = f"{token}|submit|{int(time.time())}|0.9"
            
            print(f"{hijau}✅  Generated Turnstile token{reset}")
            return turnstile_token
        
        except Exception as e:
            print(f"{merah}❌  Turnstile solving failed: {e}{reset}")
            return None
    
    def solve_jschl_challenge(self, html_content: str, page_url: str) -> Optional[Dict[str, str]]:
        """Solve jschl challenge"""
        print(f"{cyan}🛡️   Solving jschl challenge...{reset}")
        
        try:
            # Extract challenge parameters
            jschl_vc_match = re.search(self.cf_versions["cf_challenge"]["jschl_vc_pattern"], html_content)
            jschl_pass_match = re.search(self.cf_versions["cf_challenge"]["jschl_pass_pattern"], html_content)
            
            if not jschl_vc_match or not jschl_pass_match:
                return None
            
            jschl_vc = jschl_vc_match.group(1)
            jschl_pass = jschl_pass_match.group(1)
            
            # Extract and calculate jschl_answer
            jschl_match = re.search(self.cf_versions["cf_challenge"]["jschl_pattern"], html_content, re.DOTALL)
            if not jschl_match:
                return None
            
            jschl_code = jschl_match.group(1)
            
            # Simple calculation (dalam real implementation perlu eval JavaScript)
            jschl_answer = len(page_url) + random.randint(10, 100)
            
            # Add delay seperti browser asli
            time.sleep(4)
            
            return {
                "jschl_vc": jschl_vc,
                "jschl_answer": str(jschl_answer),
                "pass": jschl_pass
            }
        
        except Exception as e:
            print(f"{merah}❌  jschl solving failed: {e}{reset}")
            return None
    
    def bypass_cloudflare(self, url: str, headers: Dict[str, str], cookies: Dict[str, str]) -> Dict[str, Any]:
        """Bypass Cloudflare protection"""
        print(f"{cyan}🛡️   Bypassing Cloudflare...{reset}")
        
        result = {
            "success": False,
            "cookies": {},
            "headers": {},
            "challenge_solved": False,
            "provider": "unknown"
        }
        
        try:
            # Deteksi provider
            provider = self.detect_cdn_provider(headers, cookies)
            result["provider"] = provider or "unknown"
            
            # Get CDN headers
            ip_config = {"ip": headers.get("X-Real-IP", headers.get("X-Forwarded-For", "127.0.0.1"))}
            cdn_headers = self.get_cdn_headers(provider or "cloudflare", ip_config)
            
            # Simulasi request pertama
            initial_response = self._simulate_initial_request(url, {**headers, **cdn_headers})
            
            if initial_response.get("status") == 200:
                # Tidak ada challenge
                result["success"] = True
                result["headers"] = {**headers, **cdn_headers}
                print(f"{hijau}✅  Cloudflare bypassed (no challenge){reset}")
            
            elif initial_response.get("status") == 403:
                # Challenge detected
                html = initial_response.get("body", "").decode('utf-8', errors='ignore')
                
                # Cek jenis challenge
                if "turnstile" in html.lower():
                    # Turnstile challenge
                    sitekey_match = re.search(r'data-sitekey=["\']([^"\']+)["\']', html)
                    if sitekey_match:
                        sitekey = sitekey_match.group(1)
                        token = self.solve_turnstile_challenge(sitekey, url)
                        
                        if token:
                            # Submit token
                            challenge_response = self._submit_turnstile_token(url, token, {**headers, **cdn_headers})
                            
                            if challenge_response.get("status") == 200:
                                result["success"] = True
                                result["challenge_solved"] = True
                                result["headers"] = {**headers, **cdn_headers}
                                result["cookies"] = challenge_response.get("cookies", {})
                                print(f"{hijau}✅  Turnstile challenge solved{reset}")
                
                elif "jschl_vc" in html:
                    # jschl challenge
                    challenge_data = self.solve_jschl_challenge(html, url)
                    
                    if challenge_data:
                        # Submit challenge
                        challenge_url = f"{url}?jschl_vc={challenge_data['jschl_vc']}&jschl_answer={challenge_data['jschl_answer']}&pass={challenge_data['pass']}"
                        challenge_response = self._submit_jschl_challenge(challenge_url, {**headers, **cdn_headers})
                        
                        if challenge_response.get("status") == 200:
                            result["success"] = True
                            result["challenge_solved"] = True
                            result["headers"] = {**headers, **cdn_headers}
                            result["cookies"] = challenge_response.get("cookies", {})
                            print(f"{hijau}✅  jschl challenge solved{reset}")
            
            return result
        
        except Exception as e:
            print(f"{merah}❌  Cloudflare bypass failed: {e}{reset}")
            result["error"] = str(e)
            return result
    
    def _simulate_initial_request(self, url: str, headers: Dict[str, str]) -> Dict[str, Any]:
        """Simulate initial request"""
        # Ini adalah simulasi - dalam real implementation gunakan requests/httpx
        time.sleep(random.uniform(1.0, 3.0))
        
        # Random response simulation
        responses = [
            {"status": 200, "body": b"OK", "cookies": {}},
            {"status": 403, "body": b"Challenge Page", "cookies": {}},
            {"status": 429, "body": b"Rate Limited", "cookies": {}}
        ]
        
        return random.choice(responses)
    
    def _submit_turnstile_token(self, url: str, token: str, headers: Dict[str, str]) -> Dict[str, Any]:
        """Submit Turnstile token"""
        time.sleep(random.uniform(2.0, 5.0))
        
        # Simulasi success
        return {
            "status": 200,
            "body": b"Success",
            "cookies": {
                "cf_clearance": str(uuid.uuid4()),
                "__cf_bm": base64.b64encode(os.urandom(32)).decode()
            }
        }
    
    def _submit_jschl_challenge(self, url: str, headers: Dict[str, str]) -> Dict[str, Any]:
        """Submit jschl challenge"""
        time.sleep(5.0)  # Waktu delay seperti browser
        
        # Simulasi success
        return {
            "status": 200,
            "body": b"Success",
            "cookies": {
                "cf_clearance": str(uuid.uuid4()),
                "__cf_bm": base64.b64encode(os.urandom(32)).decode()
            }
        }
    
    def maintain_session_cookies(self, domain: str, cookies: Dict[str, str]):
        """Maintain session cookies untuk domain tertentu"""
        if domain not in self.cookie_jars:
            self.cookie_jars[domain] = {}
        
        self.cookie_jars[domain].update(cookies)
        
        # Cleanup expired cookies (simulasi)
        for cookie_name in list(self.cookie_jars[domain].keys()):
            if random.random() < 0.1:  # 10% chance cookie expired
                del self.cookie_jars[domain][cookie_name]
    
    def get_cookies_for_domain(self, domain: str) -> Dict[str, str]:
        """Dapatkan cookies untuk domain"""
        return self.cookie_jars.get(domain, {})

# ===================== ADVANCED FINGERPRINTING 2025 =====================

class AdvancedFingerprinting2025:
    """Sistem fingerprinting tingkat lanjut 2025 dengan anti-detection"""
    
    def __init__(self):
        self.device_profiles = self._generate_device_profiles_2025()
        self.browser_profiles = self._generate_browser_profiles_2025()
        self.os_profiles = self._generate_os_profiles_2025()
        self.hardware_profiles = self._generate_hardware_profiles_2025()
        self.fingerprint_cache = {}
        self.consistency_validator = ConsistencyValidator2025()
        
    def _generate_device_profiles_2025(self) -> Dict[str, Any]:
        """Generate device profiles 2025 - TIDAK PERLU DIUBAH"""
        return {
            "samsung_galaxy_s24_ultra": {
                "brand": "Samsung",
                "model": "SM-S928B",
                "market_name": "Galaxy S24 Ultra",
                "year": 2024,
                "android_version": "14",
                "oneui_version": "6.1",
                "screen": {
                    "width": 1440,
                    "height": 3088,
                    "dpi": 500,
                    "refresh_rate": 120,
                    "technology": "Dynamic AMOLED 2X"
                },
                "hardware": {
                    "chipset": "Snapdragon 8 Gen 3 for Galaxy",
                    "ram": 12,
                    "storage": 512,
                    "battery": 5000,
                    "gpu": "Adreno 750"
                },
                "sensors": ["accelerometer", "gyro", "proximity", "compass", "barometer", "ultrasonic"],
                "features": ["5G", "WiFi 7", "Bluetooth 5.3", "NFC", "UWB", "IP68"]
            },
            "iphone_16_pro_max": {
                "brand": "Apple",
                "model": "iPhone16,2",
                "market_name": "iPhone 16 Pro Max",
                "year": 2024,
                "ios_version": "18",
                "screen": {
                    "width": 1290,
                    "height": 2796,
                    "dpi": 460,
                    "refresh_rate": 120,
                    "technology": "Super Retina XDR"
                },
                "hardware": {
                    "chipset": "A18 Pro",
                    "ram": 8,
                    "storage": 512,
                    "battery": 4676,
                    "gpu": "Apple GPU (6-core)"
                },
                "sensors": ["Face ID", "LiDAR", "accelerometer", "gyro", "proximity", "compass", "barometer"],
                "features": ["5G", "WiFi 7", "Bluetooth 5.4", "NFC", "UWB", "IP68"]
            },
            "xiaomi_14_pro": {
                "brand": "Xiaomi",
                "model": "23116PN5BC",
                "market_name": "Xiaomi 14 Pro",
                "year": 2023,
                "android_version": "14",
                "miui_version": "15",
                "screen": {
                    "width": 1440,
                    "height": 3200,
                    "dpi": 522,
                    "refresh_rate": 120,
                    "technology": "CrystalRes AMOLED"
                },
                "hardware": {
                    "chipset": "Snapdragon 8 Gen 3",
                    "ram": 16,
                    "storage": 1024,
                    "battery": 4880,
                    "gpu": "Adreno 750"
                },
                "sensors": ["accelerometer", "gyro", "proximity", "compass", "color spectrum", "laser autofocus"],
                "features": ["5G", "WiFi 7", "Bluetooth 5.4", "NFC", "IR blaster", "IP68"]
            },
            "google_pixel_9_pro": {
                "brand": "Google",
                "model": "Pixel 9 Pro",
                "market_name": "Pixel 9 Pro",
                "year": 2024,
                "android_version": "15",
                "screen": {
                    "width": 1344,
                    "height": 2992,
                    "dpi": 489,
                    "refresh_rate": 120,
                    "technology": "LTPO OLED"
                },
                "hardware": {
                    "chipset": "Google Tensor G4",
                    "ram": 16,
                    "storage": 512,
                    "battery": 5050,
                    "gpu": "ARM Mali-G715"
                },
                "sensors": ["accelerometer", "gyro", "proximity", "compass", "barometer", "thermometer"],
                "features": ["5G", "WiFi 7", "Bluetooth 5.4", "NFC", "UWB", "IP68"]
            }
        }
    
    def _generate_browser_profiles_2025(self) -> Dict[str, Any]:
        """Generate browser profiles 2025"""
        return {
            "chrome_android_135": {
                "name": "Chrome",
                "version": "135.0.0.0",
                "engine": "Blink",
                "engine_version": "135.0.0.0",
                "app_version": "5.0 (Linux; Android 14; SM-S928B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Mobile Safari/537.36",
                "vendor": "Google Inc.",
                "language": "id-ID",
                "languages": ["id-ID", "id", "en-US", "en"],
                "platform": "Linux aarch64",
                "user_agent": "Mozilla/5.0 (Linux; Android 14; SM-S928B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Mobile Safari/537.36",
                "features": {
                    "webgl": "WebGL 2.0",
                    "webrtc": True,
                    "webassembly": True,
                    "service_workers": True,
                    "push_api": True,
                    "web_bluetooth": False,
                    "web_usb": False,
                    "web_nfc": False
                }
            },
            "safari_ios_18": {
                "name": "Safari",
                "version": "18.0",
                "engine": "WebKit",
                "engine_version": "605.1.15",
                "app_version": "5.0 (iPhone; CPU iPhone OS 18_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.0 Mobile/15E148 Safari/604.1",
                "vendor": "Apple Computer, Inc.",
                "language": "id-ID",
                "languages": ["id-ID", "id", "en-US", "en"],
                "platform": "iPhone",
                "user_agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 18_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.0 Mobile/15E148 Safari/604.1",
                "features": {
                    "webgl": "WebGL 2.0",
                    "webrtc": True,
                    "webassembly": True,
                    "service_workers": True,
                    "push_api": True,
                    "web_bluetooth": False,
                    "web_usb": False,
                    "web_nfc": False
                }
            },
            "samsung_browser_24": {
                "name": "Samsung Browser",
                "version": "24.0",
                "engine": "Blink",
                "engine_version": "135.0.0.0",
                "app_version": "5.0 (Linux; Android 14; SM-S928B) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/24.0 Chrome/135.0.0.0 Mobile Safari/537.36",
                "vendor": "Samsung",
                "language": "id-ID",
                "languages": ["id-ID", "id", "en-US", "en"],
                "platform": "Linux aarch64",
                "user_agent": "Mozilla/5.0 (Linux; Android 14; SM-S928B) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/24.0 Chrome/135.0.0.0 Mobile Safari/537.36",
                "features": {
                    "webgl": "WebGL 2.0",
                    "webrtc": True,
                    "webassembly": True,
                    "service_workers": True,
                    "push_api": True,
                    "web_bluetooth": True,
                    "web_usb": False,
                    "web_nfc": True
                }
            }
        }
    
    def _generate_os_profiles_2025(self) -> Dict[str, Any]:
        """Generate OS profiles 2025"""
        return {
            "android_14": {
                "name": "Android",
                "version": "14",
                "api_level": 34,
                "security_patch": "2024-12-05",
                "build_id": "UP1A.231005.007",
                "incremental": "11311212",
                "codename": "Upside Down Cake",
                "kernel_version": "5.15.110-android14-9-00001-gb5c7c1d5c2b6",
                "abi": "arm64-v8a",
                "features": ["5G", "WiFi 7", "Bluetooth 5.3", "NFC", "UWB", "Spatial Audio"]
            },
            "ios_18": {
                "name": "iOS",
                "version": "18.0",
                "build": "22A334",
                "device_support": "iPhone12,1-iPhone16,6",
                "kernel_version": "Darwin Kernel Version 23.0.0: Wed Aug 28 20:52:21 PDT 2024; root:xnu-10002.41.9~2/RELEASE_ARM64_T8110",
                "abi": "arm64e",
                "features": ["5G", "WiFi 7", "Bluetooth 5.4", "NFC", "UWB", "Spatial Audio"]
            }
        }
    
    def _generate_hardware_profiles_2025(self) -> Dict[str, Any]:
        """Generate hardware profiles 2025"""
        return {
            "snapdragon_8_gen3": {
                "manufacturer": "Qualcomm",
                "model": "SM8650-AB",
                "cores": 8,
                "architecture": "Kryo",
                "process": "4nm",
                "gpu": "Adreno 750",
                "gpu_version": "OpenGL ES 3.2",
                "neural_engine": "Hexagon",
                "ai_performance": "60 TOPS",
                "clock_speed": {
                    "prime": 3.3,
                    "performance": 3.2,
                    "efficiency": 2.3
                }
            },
            "apple_a18_pro": {
                "manufacturer": "Apple",
                "model": "APL1W10",
                "cores": 6,
                "architecture": "Avalanche/Blizzard",
                "process": "3nm",
                "gpu": "Apple GPU (6-core)",
                "gpu_version": "Metal 3",
                "neural_engine": "16-core",
                "ai_performance": "35 TOPS",
                "clock_speed": {
                    "performance": 3.7,
                    "efficiency": 2.1
                }
            },
            "google_tensor_g4": {
                "manufacturer": "Google",
                "model": "GS201",
                "cores": 9,
                "architecture": "Cortex",
                "process": "4nm",
                "gpu": "ARM Mali-G715",
                "gpu_version": "OpenGL ES 3.2",
                "neural_engine": "Edge TPU",
                "ai_performance": "40 TOPS",
                "clock_speed": {
                    "prime": 3.1,
                    "performance": 2.6,
                    "efficiency": 1.9
                }
            }
        }
    
    def generate_fingerprint(self, device_type: str = "random", location: str = "ID", 
                           isp: str = None, city: str = None, 
                           connection_type: str = "random") -> Dict[str, Any]:
        """Generate comprehensive fingerprint - Random between Android and Desktop, Indonesia only"""
        
        # Random device type
        if device_type == "random":
            device_type = random.choice(["android", "desktop"])
        
        # Random connection type based on device
        if connection_type == "random":
            connection_type = "mobile" if device_type == "android" else "wifi"
        
        fingerprint_id = f"{device_type}_{location}_{connection_type}_{int(time.time())}"
        
        if fingerprint_id in self.fingerprint_cache:
            return self.fingerprint_cache[fingerprint_id]
        
        # Device profile based on type
        if device_type == "android":
            # Android device profiles
            android_device = random.choice([
                {"brand": "Samsung", "model": "SM-S928B", "market_name": "Galaxy S24 Ultra"},
                {"brand": "Samsung", "model": "SM-S918B", "market_name": "Galaxy S23 Ultra"},
                {"brand": "Samsung", "model": "SM-A546B", "market_name": "Galaxy A54"},
                {"brand": "Xiaomi", "model": "23113RKC6G", "market_name": "Xiaomi 14 Pro"},
                {"brand": "OPPO", "model": "CPH2573", "market_name": "OPPO Find X7"},
                {"brand": "Vivo", "model": "V2303A", "market_name": "Vivo X100"},
            ])
            device_profile = {
                **android_device,
                "screen": {"width": random.choice([1080, 1440]), "height": random.choice([2340, 3088]), "dpi": random.choice([420, 560])},
                "sensors": ["accelerometer", "gyro", "proximity", "compass", "barometer"],
                "hardware": {
                    "ram": random.choice([8, 12, 16]),
                    "storage": random.choice([128, 256, 512])
                }
            }
            os_profile = {
                "name": "Android",
                "version": random.choice(["13", "14", "15"]),
                "build": f"TP1A.{random.randint(220000, 240000)}.{random.randint(1, 50)}"
            }
            browser_profile = self._get_android_chrome_profile()
            hardware_profile = random.choice([
                self.hardware_profiles.get("snapdragon_8_gen3", {"cores": 8, "memory": 12}),
                self.hardware_profiles.get("google_tensor_g4", {"cores": 9, "memory": 12}),
            ])
        else:
            # Desktop profiles (Windows/macOS)
            platform_choice = random.choice(["windows", "macos"])
            
            if platform_choice == "macos":
                device_profile = {
                    "brand": "Apple",
                    "model": random.choice(["MacBookPro18,1", "MacBookPro17,1", "MacBookAir10,1"]),
                    "market_name": random.choice(["MacBook Pro 16", "MacBook Pro 14", "MacBook Air M2"]),
                    "screen": {"width": 2560, "height": 1600, "dpi": 227},
                    "sensors": ["accelerometer", "gyro", "ambient_light"],
                    "hardware": {
                        "ram": random.choice([16, 32, 64]),
                        "storage": random.choice([512, 1024, 2048])
                    }
                }
                os_profile = {
                    "name": "macOS",
                    "version": random.choice(["14.0", "13.0", "12.0"]),
                    "build": random.choice(["23A344", "22A380", "21G72"])
                }
                browser_profile = self._get_desktop_chrome_profile("macos")
                hardware_profile = {
                    "processor": random.choice(["Apple M3 Pro", "Apple M2 Pro", "Apple M1 Max"]),
                    "cores": random.choice([10, 12, 14]),
                    "memory": random.choice([16, 32, 64])
                }
            else:
                device_profile = {
                    "brand": random.choice(["Dell", "HP", "Lenovo", "ASUS"]),
                    "model": random.choice(["XPS 15", "Spectre x360", "ThinkPad X1", "ZenBook Pro"]),
                    "market_name": random.choice(["Dell XPS 15 9530", "HP Spectre x360", "Lenovo ThinkPad X1 Carbon"]),
                    "screen": {"width": 1920, "height": 1080, "dpi": 141},
                    "sensors": [],
                    "hardware": {
                        "ram": random.choice([16, 32, 64]),
                        "storage": random.choice([512, 1024, 2048])
                    }
                }
                os_profile = {
                    "name": "Windows",
                    "version": random.choice(["10.0", "11.0"]),
                    "build": random.choice(["19045", "22631", "22000"])
                }
                browser_profile = self._get_desktop_chrome_profile("windows")
                hardware_profile = {
                    "processor": random.choice(["Intel Core i7-13700H", "Intel Core i9-13900H", "AMD Ryzen 9 7945HX"]),
                    "cores": random.choice([8, 12, 16]),
                    "memory": random.choice([16, 32, 64])
                }
        
        # Generate unique identifiers
        advertising_id = self._generate_advertising_id()
        
        # Generate location data - Indonesia only
        location_data = self._generate_location_data_enhanced("ID", city)
        
        # Generate network data based on device type
        network_data = self._generate_network_data_enhanced("ID", device_type, connection_type, isp)
        
        # Generate device fingerprint
        device_fingerprint = self._generate_device_fingerprint_enhanced(device_profile, connection_type)
        
        # Generate sensor data - Desktop has limited sensors
        sensor_data = {}
        
        # Desktop doesn't have installed apps like mobile
        installed_apps = []
        
        # Build fingerprint for Desktop
        fingerprint = {
            "fingerprint_id": fingerprint_id,
            "timestamp": int(time.time()),
            "device_type": "desktop",
            "connection_type": "wifi",
            
            "device": {
                **device_profile,
                "identifiers": {
                    "advertising_id": advertising_id,
                    "serial_number": None,
                    "imei": None,
                    "meid": None
                },
                "fingerprint": device_fingerprint
            },
            
            "os": {
                **os_profile,
                "timezone": location_data["timezone"],
                "locale": f"{location_data['language']}_{location}",
                "language": location_data["language"],
                "languages": [location_data["language"], "en-US", "en"],
                "keyboard_layout": "qwerty",
                "font_scale": 1.0,
                "display_size": "default",
                "dark_mode": random.choice([True, False]),
                "battery_saver": False,
                "developer_options": False
            },
            
            "browser": {
                **browser_profile,
                "user_agent": browser_profile["user_agent"],
                "accept_language": f"{location_data['language']},{location_data['language'].split('-')[0]};q=0.9,en-US;q=0.8,en;q=0.7",
                "timezone_offset": self._calculate_timezone_offset(location_data["timezone"]),
                "screen": device_profile["screen"],
                "viewport": {
                    "width": device_profile["screen"]["width"],
                    "height": device_profile["screen"]["height"] - 100,  # Subtract status/address bar
                    "device_pixel_ratio": device_profile["screen"]["dpi"] / 160
                },
                "hardware_concurrency": hardware_profile["cores"],
                "device_memory": device_profile["hardware"]["ram"],
                "max_touch_points": 10 if connection_type == "mobile" else 5  # DIKOREKSI
            },
            
            # Hardware Info
            "hardware": {
                **hardware_profile,
                "ram": device_profile["hardware"]["ram"],
                "storage": device_profile["hardware"]["storage"],
                "battery": {
                    "level": random.randint(20, 100),
                    "charging": random.choice([True, False]),
                    "charging_time": random.randint(0, 3600) if not random.choice([True, False]) else -1,
                    "discharging_time": random.randint(3600, 7200),
                    "health": random.choice(["good", "fair", "poor"]),
                    "technology": "Li-ion",
                    "temperature": random.randint(25, 40),
                    "voltage": random.randint(3700, 4200)
                }
            },
            
            # Network Info - DIKOREKSI: gunakan network_data yang sudah dihasilkan
            "network": {
                **network_data,
                "signal_strength": random.randint(-70, -50) if connection_type == "mobile" else random.randint(-40, -20),
                "network_type": "5G" if connection_type == "mobile" else "WiFi",
                "carrier": network_data.get("carrier", "Unknown"),
                "sim_country": location,
                "roaming": False,
                "metered": True if connection_type == "mobile" else False,
                "vpn_active": False,
                "proxy_active": False
            },
            
            # Location Info
            "location": location_data,
            
            # Sensor Data - DIKOREKSI: sekarang didefinisikan
            "sensors": sensor_data,
            
            # Installed Apps - DIKOREKSI: sekarang didefinisikan
            "installed_apps": installed_apps,
            
            # System State
            "system": {
                "uptime": random.randint(3600, 86400),  # 1-24 hours
                "boot_time": int(time.time()) - random.randint(3600, 86400),
                "thermal_state": "nominal",
                "power_state": "charged",
                "memory_pressure": "normal",
                "disk_space": random.randint(50, 500)  # Desktop has more storage
            },
            
            # Privacy Settings
            "privacy": {
                "location_enabled": random.choice([True, False]),
                "camera_enabled": random.choice([True, False]),
                "microphone_enabled": random.choice([True, False]),
                "contacts_access": False,  # Desktop doesn't have contacts
                "photos_access": random.choice([True, False]),
                "notifications_enabled": random.choice([True, False]),
                "ad_tracking": random.choice([True, False]),
                "analytics": random.choice([True, False])
            }
        }
        
        # Validate consistency
        fingerprint["consistency_check"] = self.consistency_validator.validate(fingerprint)
        
        # Cache fingerprint
        self.fingerprint_cache[fingerprint_id] = fingerprint
        
        return fingerprint
    
    def _get_android_chrome_profile(self) -> Dict[str, Any]:
        """Generate Android Chrome browser profile"""
        chrome_version = random.choice([131, 132, 133, 134, 135, 136])
        chrome_full = f"{chrome_version}.0.{random.randint(6778, 6998)}.{random.randint(0, 250)}"
        android_version = random.choice(["13", "14", "15"])
        device_model = random.choice([
            "SM-S928B", "SM-S918B", "SM-A546B", 
            "Pixel 8", "Pixel 7 Pro",
            "23113RKC6G", "V2303A"
        ])
        
        user_agent = f"Mozilla/5.0 (Linux; Android {android_version}; {device_model}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{chrome_full} Mobile Safari/537.36"
        
        return {
            "name": "Chrome Mobile",
            "version": chrome_full,
            "app_version": f"5.0 (Linux; Android {android_version}; {device_model})",
            "user_agent": user_agent,
            "platform": '"Android"',
            "vendor": "Google Inc.",
            "product": "Gecko",
            "product_sub": "20030107",
            "language": "id-ID",
            "languages": ["id-ID", "id", "en-US", "en"],
            "online": True,
            "java_enabled": False,
            "cookies_enabled": True,
            "do_not_track": None,
            "pdf_viewer_enabled": False,
            "webdriver": False,
            "device_memory": random.choice([4, 6, 8, 12]),
            "hardware_concurrency": random.choice([4, 8]),
            "max_touch_points": random.choice([5, 10]),
            "webgl": True,
            "webrtc": True,
        }
    
    def _get_desktop_chrome_profile(self, platform: str) -> Dict[str, Any]:
        """Generate desktop Chrome browser profile for Web API"""
        chrome_version = random.choice([131, 132, 133, 134, 135, 136])
        chrome_full = f"{chrome_version}.0.{random.randint(6778, 6998)}.{random.randint(0, 250)}"
        
        if platform == "macos":
            macos_version = random.choice(["10_15_7", "13_0", "14_0", "14_5"])
            user_agent = f"Mozilla/5.0 (Macintosh; Intel Mac OS X {macos_version}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{chrome_full} Safari/537.36"
            platform_header = '"macOS"'
        else:
            windows_version = random.choice(["10.0", "11.0"])
            user_agent = f"Mozilla/5.0 (Windows NT {windows_version}; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{chrome_full} Safari/537.36"
            platform_header = '"Windows"'
        
        return {
            "name": "Google Chrome",
            "version": chrome_full,
            "app_version": f"5.0 ({platform.title()})",
            "user_agent": user_agent,
            "platform": platform_header,
            "vendor": "Google Inc.",
            "product": "Gecko",
            "product_sub": "20030107",
            "language": "id-ID",
            "languages": ["id-ID", "id", "en-US", "en"],
            "online": True,
            "java_enabled": False,
            "cookies_enabled": True,
            "do_not_track": None,
            "pdf_viewer_enabled": True,
            "webdriver": False,
            "device_memory": random.choice([8, 16, 32]),
            "hardware_concurrency": random.choice([4, 8, 12, 16]),
            "max_touch_points": 0,  # Desktop has no touch
            "webgl": True,
            "webrtc": True,
        }
    
    def _generate_android_id(self) -> str:
        """Generate Android ID"""
        return f"{random.getrandbits(64):016x}"
    
    def _generate_advertising_id(self) -> str:
        """Generate Advertising ID"""
        return str(uuid.uuid4()).replace('-', '').upper()
    
    def _generate_gsf_id(self) -> str:
        """Generate GSF ID (Google Services Framework)"""
        return str(uuid.uuid4())
    
    def _generate_serial_number(self, brand: str) -> str:
        """Generate serial number"""
        year = random.randint(2023, 2024)
        week = random.randint(1, 52)
        factory = random.choice(["CH", "VN", "IN", "ID", "MY"])
        sequence = random.randint(100000, 999999)
        
        return f"{factory}{year % 10}{week:02d}{factory[0]}{sequence}"
    
    def _generate_imei(self) -> str:
        """Generate IMEI"""
        # Format: 8-digit TAC + 6-digit SNR + 1 check digit
        tac = random.randint(35000000, 35999999)  # TAC range
        snr = random.randint(100000, 999999)  # Serial number
        imei_without_check = f"{tac}{snr}"
        
        # Calculate check digit (Luhn algorithm)
        total = 0
        for i, digit in enumerate(imei_without_check):
            n = int(digit)
            if i % 2 == 0:  # Even position (0-indexed)
                total += n
            else:
                total += sum(int(d) for d in str(n * 2))
        
        check_digit = (10 - (total % 10)) % 10
        
        return f"{imei_without_check}{check_digit}"
    
    def _generate_meid(self) -> str:
        """Generate MEID"""
        # Format: 8-digit manufacturer code + 6-digit serial + 1 check digit
        manufacturer = random.choice(["A10000", "A10001", "A10002"])
        serial = random.randint(100000, 999999)
        return f"{manufacturer}{serial:06d}"
    
    def _generate_location_data_enhanced(self, country_code: str, city: str = None) -> Dict[str, Any]:
        """Generate enhanced location data dengan parameter city - BARU"""
        indonesian_cities = [
            {"city": "Jakarta", "province": "DKI Jakarta", "lat": -6.2088, "lon": 106.8456},
            {"city": "Surabaya", "province": "Jawa Timur", "lat": -7.2575, "lon": 112.7521},
            {"city": "Bandung", "province": "Jawa Barat", "lat": -6.9175, "lon": 107.6191},
            {"city": "Medan", "province": "Sumatera Utara", "lat": 3.5952, "lon": 98.6722},
            {"city": "Bekasi", "province": "Jawa Barat", "lat": -6.2383, "lon": 106.9756},
            {"city": "Makassar", "province": "Sulawesi Selatan", "lat": -5.1477, "lon": 119.4327},
            {"city": "Semarang", "province": "Jawa Tengah", "lat": -6.9667, "lon": 110.4167},
            {"city": "Palembang", "province": "Sumatera Selatan", "lat": -2.9909, "lon": 104.7566},
            {"city": "Tangerang", "province": "Banten", "lat": -6.1783, "lon": 106.6319},
            {"city": "Bali", "province": "Bali", "lat": -8.4095, "lon": 115.1889}
        ]
        
        # Jika city tidak diberikan, pilih random
        if city:
            # Cari kota yang diminta
            selected_city = next((c for c in indonesian_cities if c["city"].lower() == city.lower()), None)
            if not selected_city:
                selected_city = random.choice(indonesian_cities)
        else:
            selected_city = random.choice(indonesian_cities)
        
        # Tambahkan variasi kecil pada koordinat
        lat_variation = random.uniform(-0.01, 0.01)  # FIXED: didefinisikan
        lon_variation = random.uniform(-0.01, 0.01)  # FIXED: didefinisikan
        
        return {
            "country": "Indonesia",
            "country_code": country_code,
            "city": selected_city["city"],
            "province": selected_city["province"],
            "latitude": round(selected_city["lat"] + lat_variation, 6),
            "longitude": round(selected_city["lon"] + lon_variation, 6),
            "accuracy": random.uniform(10, 100),  # meters
            "altitude": random.uniform(0, 100),
            "speed": random.uniform(0, 5),
            "heading": random.uniform(0, 360),
            "timezone": "Asia/Jakarta",
            "language": "id-ID",
            "locale": "id_ID",
            "currency": "IDR",
            "region_code": "ID"
        }
    
    def _generate_network_data_enhanced(self, country_code: str, device_type: str, 
                                      connection_type: str, isp: str = None) -> Dict[str, Any]:
        """Generate enhanced network data dengan semua parameter - BARU"""
        indonesian_carriers = [
            {"name": "Telkomsel", "mcc": "510", "mnc": "10", "type": "mobile"},
            {"name": "Indosat", "mcc": "510", "mnc": "01", "type": "mobile"},
            {"name": "XL Axiata", "mcc": "510", "mnc": "11", "type": "mobile"},
            {"name": "3 (Tri)", "mcc": "510", "mnc": "89", "type": "mobile"},
            {"name": "Smartfren", "mcc": "510", "mnc": "28", "type": "mobile"}
        ]
        
        indonesian_isps = [
            {"name": "Biznet", "type": "wifi"},
            {"name": "First Media", "type": "wifi"},
            {"name": "IndiHome", "type": "wifi"},
            {"name": "MyRepublic", "type": "wifi"},
            {"name": "CBN", "type": "wifi"}
        ]
        
        # Pilih berdasarkan connection_type
        if connection_type == "mobile":
            # Pilih carrier mobile
            if isp:
                # Cari carrier berdasarkan nama ISP
                carrier = next((c for c in indonesian_carriers if c["name"].lower() == isp.lower()), None)
                if not carrier:
                    carrier = random.choice(indonesian_carriers)
            else:
                carrier = random.choice(indonesian_carriers)
            
            return {
                "carrier": carrier["name"],
                "mcc": carrier["mcc"],
                "mnc": carrier["mnc"],
                "operator": carrier["name"],
                "sim_operator": f"{carrier['mcc']}{carrier['mnc']}",
                "network_operator": f"{carrier['mcc']}{carrier['mnc']}",
                "sim_country": country_code,
                "network_country": country_code,
                "sim_state": "ready",
                "network_type": random.choice(["5G", "LTE", "HSPA+"]),
                "data_state": "connected",
                "data_activity": random.choice(["in", "out", "inout", "none"]),
                "roaming": False
            }
        else:
            # WiFi connection
            if isp:
                # Cari ISP berdasarkan nama
                isp_info = next((i for i in indonesian_isps if i["name"].lower() == isp.lower()), None)
                if not isp_info:
                    isp_info = random.choice(indonesian_isps)
            else:
                isp_info = random.choice(indonesian_isps)
            
            return {
                "carrier": isp_info["name"],
                "mcc": "510",
                "mnc": "99",  # Generic untuk WiFi
                "operator": isp_info["name"],
                "sim_operator": f"51099",
                "network_operator": f"51099",
                "sim_country": country_code,
                "network_country": country_code,
                "sim_state": "absent",  # Tidak ada SIM untuk WiFi
                "network_type": "WiFi",
                "data_state": "connected",
                "data_activity": random.choice(["in", "out", "inout", "none"]),
                "roaming": False
            }
    
    def _generate_sensor_data_enhanced(self, sensors: List[str], connection_type: str) -> Dict[str, Any]:
        """Generate enhanced sensor data dengan connection type awareness - BARU"""
        sensor_data = {}
        
        for sensor in sensors:
            if sensor == "accelerometer":
                sensor_data[sensor] = {
                    "x": random.uniform(-9.8, 9.8),
                    "y": random.uniform(-9.8, 9.8),
                    "z": random.uniform(-9.8, 9.8),
                    "accuracy": random.choice([0, 1, 2, 3])
                }
            elif sensor == "gyro":
                sensor_data[sensor] = {
                    "x": random.uniform(-10, 10),
                    "y": random.uniform(-10, 10),
                    "z": random.uniform(-10, 10),
                    "accuracy": random.choice([0, 1, 2, 3])
                }
            elif sensor == "proximity":
                sensor_data[sensor] = {
                    "distance": random.uniform(0, 5) if connection_type == "mobile" else 0.0,  # Mobile lebih mungkin ada proximity
                    "accuracy": random.choice([0, 1, 2, 3])
                }
            elif sensor == "compass":
                sensor_data[sensor] = {
                    "heading": random.uniform(0, 360),
                    "accuracy": random.choice([0, 1, 2, 3])
                }
            elif sensor == "barometer":
                sensor_data[sensor] = {
                    "pressure": random.uniform(950, 1050),
                    "accuracy": random.choice([0, 1, 2, 3])
                }
            elif sensor == "light":
                sensor_data[sensor] = {
                    "illuminance": random.uniform(0, 10000),
                    "accuracy": random.choice([0, 1, 2, 3])
                }
            elif sensor == "Face ID":
                sensor_data[sensor] = {
                    "available": True,
                    "enrolled": random.choice([True, False]),
                    "accuracy": 3
                }
            elif sensor == "LiDAR":
                sensor_data[sensor] = {
                    "available": True,
                    "scanning": False,
                    "accuracy": 3
                }
            else:
                # Sensor umum lainnya
                sensor_data[sensor] = {
                    "available": True,
                    "value": random.uniform(0, 100),
                    "accuracy": random.choice([0, 1, 2, 3])
                }
        
        return sensor_data
    
    def _generate_installed_apps_indonesia_enhanced(self, device_type: str, connection_type: str) -> List[str]:
        """Generate installed apps untuk Indonesia dengan connection type awareness - BARU"""
        common_apps = [
            "com.instagram.android",  # Instagram
            "com.whatsapp",  # WhatsApp
            "com.facebook.katana",  # Facebook
            "com.twitter.android",  # Twitter/X
            "com.google.android.youtube",  # YouTube
            "com.tokopedia.tkpd",  # Tokopedia
            "com.shopee.id",  # Shopee
            "id.co.bri.brimo",  # BRImo
            "com.bca",  # BCA Mobile
            "com.gojek.app",  # Gojek
            "com.grab.android",  # Grab
            "com.traveloka.android",  # Traveloka
            "com.zhiliaoapp.musically",  # TikTok
            "com.truecaller",  # Truecaller
            "com.spotify.music",  # Spotify
            "com.google.android.gm",  # Gmail
            "com.google.chrome",  # Chrome
            "com.android.chrome",  # Chrome (system)
            "com.google.android.apps.maps",  # Google Maps
            "com.google.android.apps.photos",  # Google Photos
            "com.google.android.apps.docs",  # Google Docs
            "com.microsoft.office.word",  # Word
            "com.microsoft.office.excel",  # Excel
            "com.adobe.reader",  # Adobe Reader
            "com.netflix.mediaclient",  # Netflix
            "com.disney.disneyplus",  # Disney+",
        ]
        
        # Tambahkan apps berdasarkan device_type
        if device_type == "ios":
            # iOS apps
            common_apps = [app.replace('.android', '').replace('com.', '') for app in common_apps]
            common_apps.extend([
                "com.apple.Pages",
                "com.apple.Numbers",
                "com.apple.Keynote",
                "com.apple.mobilegarageband"
            ])
        
        # Tambahkan apps berdasarkan connection_type
        if connection_type == "mobile":
            common_apps.extend([
                "com.telkomsel.tcash",  # TCash
                "com.dana",  # DANA
                "com.ovo.android",  # OVO
                "id.co.jago",  # Jago
                "com.linkaja.android"  # LinkAja
            ])
        else:
            # WiFi/Tablet apps
            common_apps.extend([
                "com.microsoft.skydrive",  # OneDrive
                "com.dropbox.android",  # Dropbox
                "com.evernote",  # Evernote
                "com.skype.raider",  # Skype
                "com.zoom.videomeetings"  # Zoom
            ])
        
        # Random selection
        num_apps = random.randint(25, 40) if connection_type == "mobile" else random.randint(20, 30)
        return random.sample(common_apps, min(num_apps, len(common_apps)))

    def _generate_device_fingerprint_enhanced(self, device_profile: Dict[str, Any], 
                                           connection_type: str) -> Dict[str, Any]:
        """Generate enhanced device fingerprint dengan connection type awareness - BARU"""
        if connection_type == "mobile":
            # Mobile devices
            if device_profile["brand"].lower() == "samsung":
                device = {
                    "brand": "Samsung",
                    "model": device_profile["model"],
                    "name": device_profile["market_name"],
                    "connection_type": "mobile",
                    "android_version": device_profile.get("android_version", "14"),
                    "chrome_version": f"{random.randint(130, 135)}.0.{random.randint(6000, 7000)}.{random.randint(0, 99)}",
                    "webview_version": f"{random.randint(110, 120)}.0.{random.randint(5000, 6000)}",
                    "build_id": f"UP1A.{random.randint(230101, 231231)}.{random.randint(100, 999)}",
                    "kernel_version": f"5.15.{random.randint(100, 120)}-android{random.randint(12, 15)}",
                    "screen_resolution": f"{device_profile['screen']['width']}x{device_profile['screen']['height']}",
                    "dpi": device_profile["screen"]["dpi"],
                    "device_id": f"android-{hashlib.sha256(str(time.time()).encode()).hexdigest()[:16]}",
                    "advertising_id": str(uuid.uuid4()).upper().replace('-', ''),
                    "android_id": f"{random.getrandbits(64):016x}"
                }
            else:
                device = {
                    "brand": device_profile["brand"],
                    "model": device_profile["model"],
                    "name": device_profile["market_name"],
                    "connection_type": "mobile",
                    "android_version": device_profile.get("android_version", "14"),
                    "chrome_version": f"{random.randint(130, 135)}.0.{random.randint(6000, 7000)}.{random.randint(0, 99)}",
                    "webview_version": f"{random.randint(110, 120)}.0.{random.randint(5000, 6000)}",
                    "build_id": f"RP1A.{random.randint(230101, 231231)}.{random.randint(100, 999)}",
                    "kernel_version": f"5.15.{random.randint(100, 120)}-android{random.randint(12, 15)}",
                    "screen_resolution": f"{device_profile['screen']['width']}x{device_profile['screen']['height']}",
                    "dpi": device_profile["screen"]["dpi"],
                    "device_id": f"android-{hashlib.sha256(str(time.time()).encode()).hexdigest()[:16]}",
                    "advertising_id": str(uuid.uuid4()).upper().replace('-', ''),
                    "android_id": f"{random.getrandbits(64):016x}"
                }
        else:
            # WiFi/Tablet devices
            device = {
                "brand": device_profile["brand"],
                "model": device_profile["model"],
                "name": f"{device_profile['market_name']} (Tablet)",
                "connection_type": "wifi",
                "android_version": device_profile.get("android_version", "14"),
                "chrome_version": f"{random.randint(130, 135)}.0.{random.randint(6000, 7000)}.{random.randint(0, 99)}",
                "webview_version": f"{random.randint(110, 120)}.0.{random.randint(5000, 6000)}",
                "build_id": f"TP1A.{random.randint(230101, 231231)}.{random.randint(100, 999)}",
                "kernel_version": f"5.15.{random.randint(100, 120)}-android{random.randint(12, 15)}",
                "screen_resolution": f"{device_profile['screen']['width']}x{device_profile['screen']['height']}",
                "dpi": device_profile["screen"]["dpi"],
                "device_id": f"tablet-{hashlib.sha256(str(time.time()).encode()).hexdigest()[:16]}",
                "advertising_id": str(uuid.uuid4()).upper().replace('-', ''),
                "android_id": f"{random.getrandbits(64):016x}" if device_profile["brand"].lower() != "apple" else None
            }
        
        return device
    
    def _calculate_timezone_offset(self, timezone: str) -> int:
        """Calculate timezone offset"""
        if timezone == "Asia/Jakarta":
            return 420  # UTC+7 in minutes
        elif timezone == "Asia/Makassar":
            return 480  # UTC+8
        elif timezone == "Asia/Jayapura":
            return 540  # UTC+9
        else:
            return 420
    
    def validate_fingerprint(self, fingerprint: Dict[str, Any]) -> Dict[str, Any]:
        """Validate fingerprint consistency"""
        return self.consistency_validator.validate(fingerprint)

class ConsistencyValidator2025:
    """Validator untuk konsistensi fingerprint 2025"""
    
    def __init__(self):
        self.validation_rules = self._load_validation_rules_2025()
        
    def _load_validation_rules_2025(self) -> Dict[str, Any]:
        """Load validation rules 2025"""
        return {
            "device_consistency": {
                "rules": [
                    ("device.brand", "device.model", "device.market_name"),
                    ("device.android_version", "os.version"),
                    ("device.screen.width", "browser.screen.width"),
                    ("device.screen.height", "browser.screen.height"),
                    ("device.hardware.ram", "browser.device_memory")
                ],
                "threshold": 0.9
            },
            "location_consistency": {
                "rules": [
                    ("location.country_code", "network.sim_country"),
                    ("location.timezone", "os.timezone"),
                    ("location.language", "os.language"),
                    ("location.locale", "os.locale")
                ],
                "threshold": 1.0
            },
            "network_consistency": {
                "rules": [
                    ("network.carrier", "network.operator"),
                    ("network.mcc", "network.sim_operator[:3]"),
                    ("network.mnc", "network.sim_operator[3:]"),
                    ("network.sim_country", "network.network_country")
                ],
                "threshold": 0.9
            },
            "browser_consistency": {
                "rules": [
                    ("browser.user_agent", "device.device_type"),
                    ("browser.platform", "os.name"),
                    ("browser.hardware_concurrency", "hardware.cores"),
                    ("browser.viewport.width", "device.screen.width")
                ],
                "threshold": 0.8
            }
        }
    
    def validate(self, fingerprint: Dict[str, Any]) -> Dict[str, Any]:
        """Validate fingerprint consistency"""
        results = {
            "overall_score": 0.0,
            "category_scores": {},
            "issues": [],
            "passed": False
        }
        
        category_scores = []
        
        for category, config in self.validation_rules.items():
            category_score = self._validate_category(fingerprint, category, config)
            results["category_scores"][category] = category_score
            category_scores.append(category_score)
            
            if category_score < config["threshold"]:
                results["issues"].append(f"{category}: Score {category_score:.2f} < {config['threshold']}")
        
        # Calculate overall score
        if category_scores:
            results["overall_score"] = sum(category_scores) / len(category_scores)
            results["passed"] = results["overall_score"] >= 0.85
        
        return results
    
    def _validate_category(self, fingerprint: Dict[str, Any], category: str, config: Dict[str, Any]) -> float:
        """Validate specific category"""
        passed_rules = 0
        total_rules = len(config["rules"])
        
        for rule in config["rules"]:
            if self._check_rule(fingerprint, rule):
                passed_rules += 1
        
        return passed_rules / total_rules if total_rules > 0 else 1.0
    
    def _check_rule(self, fingerprint: Dict[str, Any], rule: tuple) -> bool:
        """Check single rule"""
        try:
            values = []
            for key in rule:
                value = self._get_nested_value(fingerprint, key)
                if value is None:
                    return False
                values.append(value)
            
            # Check consistency
            if len(set(str(v) for v in values)) <= 2:
                return True
            
            # Allow some variation for numeric values
            if all(isinstance(v, (int, float)) for v in values):
                avg = sum(values) / len(values)
                variation = max(abs(v - avg) / avg if avg != 0 else abs(v) for v in values)
                return variation < 0.1  # Allow 10% variation
            
            return False
            
        except Exception:
            return False
    
    def _get_nested_value(self, obj: Dict[str, Any], key: str) -> Any:
        """Get nested value"""
        keys = key.split('.')
        current = obj
        
        for k in keys:
            # Handle array indexing
            if '[' in k and ']' in k:
                base_key = k.split('[')[0]
                index = int(k.split('[')[1].split(']')[0])
                
                if base_key in current and isinstance(current[base_key], (list, tuple)):
                    current = current[base_key][index] if index < len(current[base_key]) else None
                else:
                    return None
            
            # Handle slicing
            elif '[:' in k or '[:' in k:
                base_key = k.split('[')[0]
                slice_parts = k.split('[')[1].split(']')[0].split(':')
                
                if base_key in current and isinstance(current[base_key], (str, list, tuple)):
                    if len(slice_parts) == 1:
                        end = int(slice_parts[0])
                        current = current[base_key][:end]
                    elif len(slice_parts) == 2:
                        start = int(slice_parts[0]) if slice_parts[0] else 0
                        end = int(slice_parts[1]) if slice_parts[1] else len(current[base_key])
                        current = current[base_key][start:end]
                    else:
                        return None
                else:
                    return None
            
            # Handle regular key
            else:
                if isinstance(current, dict) and k in current:
                    current = current[k]
                else:
                    return None
        
        return current

# ===================== BEHAVIORAL ANALYSIS & MIMICRY 2025 =====================

class BehavioralMimicry2025:
    """Sistem behavioral mimicry 2025 untuk meniru perilaku manusia"""
    
    def __init__(self):
        self.behavior_profiles = self._generate_behavior_profiles_2025()
        self.interaction_patterns = self._generate_interaction_patterns_2025()
        self.timing_profiles = self._generate_timing_profiles_2025()
        self.session_history = {}
        
    def _generate_behavior_profiles_2025(self) -> Dict[str, Any]:
        """Generate behavior profiles 2025"""
        return {
            "casual_indonesian": {
                "typing_speed_wpm": (60, 90),
                "typing_accuracy": (0.85, 0.95),
                "mouse_speed_px_s": (500, 1500),
                "mouse_acceleration": (1.2, 2.0),
                "scroll_speed_px_s": (800, 2000),
                "scroll_pattern": "smooth",
                "attention_span_s": (30, 120),
                "error_rate": (0.02, 0.05),
                "hesitation_time_s": (0.1, 0.5),
                "multi_tasking": False,
                "device_usage": "mobile_primary"
            },
            "tech_savvy_indonesian": {
                "typing_speed_wpm": (80, 120),
                "typing_accuracy": (0.90, 0.98),
                "mouse_speed_px_s": (800, 2000),
                "mouse_acceleration": (1.5, 2.5),
                "scroll_speed_px_s": (1200, 3000),
                "scroll_pattern": "bursty",
                "attention_span_s": (15, 60),
                "error_rate": (0.01, 0.03),
                "hesitation_time_s": (0.05, 0.3),
                "multi_tasking": True,
                "device_usage": "multi_device"
            },
            "young_adult_indonesian": {
                "typing_speed_wpm": (70, 110),
                "typing_accuracy": (0.88, 0.96),
                "mouse_speed_px_s": (600, 1800),
                "mouse_acceleration": (1.3, 2.2),
                "scroll_speed_px_s": (1000, 2500),
                "scroll_pattern": "fast_scroll",
                "attention_span_s": (20, 90),
                "error_rate": (0.015, 0.04),
                "hesitation_time_s": (0.08, 0.4),
                "multi_tasking": True,
                "device_usage": "mobile_only"
            },
            "professional_indonesian": {
                "typing_speed_wpm": (65, 100),
                "typing_accuracy": (0.92, 0.99),
                "mouse_speed_px_s": (700, 1600),
                "mouse_acceleration": (1.4, 2.3),
                "scroll_speed_px_s": (900, 2200),
                "scroll_pattern": "methodical",
                "attention_span_s": (45, 150),
                "error_rate": (0.01, 0.025),
                "hesitation_time_s": (0.15, 0.6),
                "multi_tasking": False,
                "device_usage": "desktop_primary"
            }
        }
    
    def _generate_interaction_patterns_2025(self) -> Dict[str, Any]:
        """Generate interaction patterns 2025"""
        return {
            "instagram_exploration": {
                "actions": [
                    {"type": "scroll", "duration": (5, 15), "distance": (500, 1500)},
                    {"type": "pause", "duration": (1, 3)},
                    {"type": "like", "duration": (0.5, 1.5)},
                    {"type": "scroll", "duration": (3, 8), "distance": (300, 800)},
                    {"type": "pause", "duration": (2, 5)},
                    {"type": "view_story", "duration": (8, 15)},
                    {"type": "scroll", "duration": (7, 12), "distance": (700, 1200)},
                    {"type": "pause", "duration": (1, 4)},
                    {"type": "comment", "duration": (3, 10)}
                ],
                "repeat_pattern": (3, 8)
            },
            "signup_process": {
                "actions": [
                    {"type": "field_focus", "duration": (0.5, 1.5)},
                    {"type": "typing", "duration": (2, 5)},
                    {"type": "field_switch", "duration": (0.3, 1.0)},
                    {"type": "typing", "duration": (1, 3)},
                    {"type": "field_switch", "duration": (0.2, 0.8)},
                    {"type": "typing", "duration": (3, 7)},
                    {"type": "review", "duration": (2, 4)},
                    {"type": "submit", "duration": (0.5, 1.0)}
                ],
                "repeat_pattern": 1
            },
            "profile_editing": {
                "actions": [
                    {"type": "upload_photo", "duration": (5, 15)},
                    {"type": "crop", "duration": (3, 8)},
                    {"type": "edit_bio", "duration": (10, 30)},
                    {"type": "save", "duration": (1, 3)},
                    {"type": "preview", "duration": (3, 7)},
                    {"type": "final_save", "duration": (0.5, 1.5)}
                ],
                "repeat_pattern": 1
            }
        }
    
    def _generate_timing_profiles_2025(self) -> Dict[str, Any]:
        """Generate timing profiles 2025"""
        return {
            "human_react": {
                "distribution": "gamma",
                "shape": 2.0,
                "scale": 0.3,
                "min_ms": 100,
                "max_ms": 1000
            },
            "reading_time": {
                "distribution": "lognormal",
                "mean": 1.5,
                "sigma": 0.5,
                "min_s": 0.5,
                "max_s": 10.0
            },
            "typing_delay": {
                "distribution": "normal",
                "mean": 0.2,
                "std": 0.05,
                "min_s": 0.1,
                "max_s": 0.5
            },
            "hesitation": {
                "distribution": "exponential",
                "lambda": 0.5,
                "min_s": 0.05,
                "max_s": 2.0
            }
        }
    
    def generate_behavior_profile(self, user_type: str = None) -> Dict[str, Any]:
        """Generate behavior profile"""
        if not user_type:
            user_type = random.choice(list(self.behavior_profiles.keys()))
        
        base_profile = self.behavior_profiles[user_type]
        
        # Generate specific values within ranges
        profile = {
            "user_type": user_type,
            "typing_speed_wpm": random.uniform(*base_profile["typing_speed_wpm"]),
            "typing_accuracy": random.uniform(*base_profile["typing_accuracy"]),
            "mouse_speed_px_s": random.uniform(*base_profile["mouse_speed_px_s"]),
            "mouse_acceleration": random.uniform(*base_profile["mouse_acceleration"]),
            "scroll_speed_px_s": random.uniform(*base_profile["scroll_speed_px_s"]),
            "scroll_pattern": base_profile["scroll_pattern"],
            "attention_span_s": random.uniform(*base_profile["attention_span_s"]),
            "error_rate": random.uniform(*base_profile["error_rate"]),
            "hesitation_time_s": random.uniform(*base_profile["hesitation_time_s"]),
            "multi_tasking": base_profile["multi_tasking"],
            "device_usage": base_profile["device_usage"],
            "session_id": str(uuid.uuid4())[:12],
            "generated_at": int(time.time())
        }
        
        # Generate interaction style
        profile["interaction_style"] = self._generate_interaction_style(profile)
        
        # Generate timing model
        profile["timing_model"] = self._generate_timing_model(profile)
        
        return profile
    
    def _generate_interaction_style(self, profile: Dict[str, Any]) -> Dict[str, Any]:
        """Generate interaction style"""
        return {
            "click_precision": random.uniform(0.85, 0.98),
            "double_click_rate": random.uniform(0.01, 0.05),
            "right_click_rate": random.uniform(0.02, 0.08),
            "drag_drop_frequency": random.uniform(0.1, 0.3),
            "tab_switching_frequency": random.uniform(0.2, 0.6) if profile["multi_tasking"] else random.uniform(0.05, 0.2),
            "copy_paste_frequency": random.uniform(0.1, 0.4),
            "undo_redo_frequency": random.uniform(0.05, 0.15),
            "zoom_frequency": random.uniform(0.02, 0.1),
            "refresh_frequency": random.uniform(0.01, 0.05),
            "bookmark_frequency": random.uniform(0.005, 0.02)
        }
    
    def _generate_timing_model(self, profile: Dict[str, Any]) -> Dict[str, Any]:
        """Generate timing model"""
        return {
            "reaction_time_ms": self._generate_reaction_time(profile),
            "reading_time_s": self._generate_reading_time(profile),
            "typing_delay_s": self._generate_typing_delay(profile),
            "hesitation_time_s": self._generate_hesitation_time(profile),
            "between_actions_s": self._generate_between_actions_time(profile),
            "session_duration_s": random.uniform(300, 3600),
            "idle_periods": random.randint(1, 5)
        }
    
    def _generate_reaction_time(self, profile: Dict[str, Any]) -> float:
        """Generate reaction time"""
        config = self.timing_profiles["human_react"]
        
        if config["distribution"] == "gamma":
            value = random.gammavariate(config["shape"], config["scale"])
        elif config["distribution"] == "normal":
            value = random.normalvariate(config["mean"], config["std"])
        elif config["distribution"] == "lognormal":
            value = random.lognormvariate(config["mean"], config["sigma"])
        else:  # exponential
            value = random.expovariate(config["lambda"])
        
        # Adjust based on profile
        if profile["user_type"] == "tech_savvy_indonesian":
            value *= 0.8  # Faster reaction
        elif profile["user_type"] == "professional_indonesian":
            value *= 0.9
        
        # Clamp to range
        return max(config["min_ms"], min(value * 1000, config["max_ms"]))
    
    def _generate_reading_time(self, profile: Dict[str, Any]) -> float:
        """Generate reading time"""
        config = self.timing_profiles["reading_time"]
        
        if config["distribution"] == "gamma":
            value = random.gammavariate(config["shape"], config["scale"])
        elif config["distribution"] == "normal":
            value = random.normalvariate(config["mean"], config["std"])
        elif config["distribution"] == "lognormal":
            value = random.lognormvariate(config["mean"], config["sigma"])
        else:  # exponential
            value = random.expovariate(config["lambda"])
        
        # Adjust based on profile
        if profile["user_type"] == "casual_indonesian":
            value *= 1.2  # Slower reading
        elif profile["user_type"] == "tech_savvy_indonesian":
            value *= 0.7  # Faster reading
        
        # Clamp to range
        return max(config["min_s"], min(value, config["max_s"]))
    
    def _generate_typing_delay(self, profile: Dict[str, Any]) -> float:
        """Generate typing delay"""
        config = self.timing_profiles["typing_delay"]
        
        value = random.normalvariate(config["mean"], config["std"])
        
        # Adjust based on typing speed
        typing_speed = profile["typing_speed_wpm"]
        if typing_speed > 100:
            value *= 0.7  # Faster typing
        elif typing_speed < 70:
            value *= 1.3  # Slower typing
        
        # Clamp to range
        return max(config["min_s"], min(value, config["max_s"]))
    
    def _generate_hesitation_time(self, profile: Dict[str, Any]) -> float:
        """Generate hesitation time"""
        config = self.timing_profiles["hesitation"]
        
        value = random.expovariate(config["lambda"])
        
        # Adjust based on profile
        if profile["user_type"] == "casual_indonesian":
            value *= 1.5  # More hesitation
        elif profile["user_type"] == "tech_savvy_indonesian":
            value *= 0.6  # Less hesitation
        
        # Clamp to range
        return max(config["min_s"], min(value, config["max_s"]))
    
    def _generate_between_actions_time(self, profile: Dict[str, Any]) -> float:
        """Generate time between actions"""
        # Use gamma distribution untuk human-like timing
        value = random.gammavariate(1.5, 0.3)
        
        # Adjust based on profile
        if profile["user_type"] == "casual_indonesian":
            value *= 1.3
        elif profile["user_type"] == "tech_savvy_indonesian":
            value *= 0.8
        
        return max(0.1, min(value, 2.0))
    
    def simulate_interaction(self, behavior_profile: Dict[str, Any], 
                           interaction_type: str = "instagram_exploration") -> List[Dict[str, Any]]:
        """Simulate human interaction"""
        if interaction_type not in self.interaction_patterns:
            interaction_type = "instagram_exploration"
        
        pattern = self.interaction_patterns[interaction_type]
        actions = []
        
        # Determine number of repetitions
        if isinstance(pattern["repeat_pattern"], tuple):
            repetitions = random.randint(*pattern["repeat_pattern"])
        else:
            repetitions = pattern["repeat_pattern"]
        
        timing_model = behavior_profile["timing_model"]
        
        for rep in range(repetitions):
            for action_template in pattern["actions"]:
                action = self._simulate_single_action(action_template, behavior_profile, timing_model)
                actions.append(action)
                
                # Add between-actions delay
                if random.random() > 0.3:  # 70% chance
                    delay_action = {
                        "type": "delay",
                        "duration": timing_model["between_actions_s"],
                        "timestamp": time.time() + sum(a.get("duration", 0) for a in actions)
                    }
                    actions.append(delay_action)
        
        return actions
    
    def _simulate_single_action(self, action_template: Dict[str, Any], 
                              behavior_profile: Dict[str, Any], 
                              timing_model: Dict[str, Any]) -> Dict[str, Any]:
        """Simulate single action"""
        action_type = action_template["type"]
        
        # Base action
        action = {
            "type": action_type,
            "timestamp": time.time(),
            "behavior_profile": behavior_profile["user_type"]
        }
        
        # Add type-specific details
        if action_type == "scroll":
            duration = random.uniform(*action_template["duration"])
            distance = random.uniform(*action_template["distance"])
            
            action.update({
                "duration": duration,
                "distance": distance,
                "speed": distance / duration,
                "direction": random.choice(["up", "down"]),
                "smoothness": random.uniform(0.7, 0.95)
            })
            
        elif action_type == "typing":
            duration = random.uniform(*action_template["duration"])
            
            action.update({
                "duration": duration,
                "typing_speed_wpm": behavior_profile["typing_speed_wpm"],
                "accuracy": behavior_profile["typing_accuracy"],
                "backspaces": int(duration * behavior_profile["error_rate"] * 10),
                "typing_delay": timing_model["typing_delay_s"]
            })
            
        elif action_type == "like":
            duration = random.uniform(*action_template["duration"])
            
            action.update({
                "duration": duration,
                "reaction_time": timing_model["reaction_time_ms"],
                "double_tap": random.random() < 0.3,  # 30% double tap
                "hold_time": random.uniform(0.1, 0.5)
            })
            
        elif action_type == "pause":
            duration = random.uniform(*action_template["duration"])
            
            action.update({
                "duration": duration,
                "reason": random.choice(["reading", "thinking", "distracted", "checking"]),
                "hesitation": random.random() < 0.4  # 40% chance hesitation
            })
            
        else:
            # Generic action
            if "duration" in action_template:
                duration = random.uniform(*action_template["duration"])
                action["duration"] = duration
        
        # Add human variations
        action["human_variation"] = random.uniform(0.8, 1.2)
        
        return action
    
    def record_session(self, session_id: str, behavior_profile: Dict[str, Any], 
                      interactions: List[Dict[str, Any]]):
        """Record session history"""
        self.session_history[session_id] = {
            "behavior_profile": behavior_profile,
            "interactions": interactions,
            "start_time": time.time(),
            "end_time": time.time() + sum(i.get("duration", 0) for i in interactions),
            "total_actions": len(interactions),
            "session_hash": hashlib.sha256(f"{session_id}{time.time()}".encode()).hexdigest()[:16]
        }
    
    def get_session_summary(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Get session summary"""
        if session_id not in self.session_history:
            return None
        
        session = self.session_history[session_id]
        
        # Calculate statistics
        interactions = session["interactions"]
        total_duration = session["end_time"] - session["start_time"]
        
        action_types = {}
        for interaction in interactions:
            action_type = interaction["type"]
            action_types[action_type] = action_types.get(action_type, 0) + 1
        
        return {
            "session_id": session_id,
            "behavior_profile": session["behavior_profile"]["user_type"],
            "start_time": session["start_time"],
            "end_time": session["end_time"],
            "total_duration": total_duration,
            "total_actions": session["total_actions"],
            "actions_per_minute": (session["total_actions"] / total_duration * 60) if total_duration > 0 else 0,
            "action_types": action_types,
            "session_hash": session["session_hash"],
            "human_likeness_score": self._calculate_human_likeness(session)
        }
    
    def _calculate_human_likeness(self, session: Dict[str, Any]) -> float:
        """Calculate human likeness score"""
        interactions = session["interactions"]
        
        if not interactions:
            return 0.0
        
        scores = []
        
        # Check timing variations
        durations = [i.get("duration", 0) for i in interactions if "duration" in i]
        if durations:
            # Human timing has variation
            mean_duration = sum(durations) / len(durations)
            variance = sum((d - mean_duration) ** 2 for d in durations) / len(durations)
            std_dev = variance ** 0.5
            
            # Ideal human variance (not too perfect, not too random)
            if 0.1 < std_dev / mean_duration < 0.5:
                scores.append(1.0)
            elif 0.05 < std_dev / mean_duration < 0.7:
                scores.append(0.7)
            else:
                scores.append(0.3)
        
        # Check action patterns
        action_sequence = [i["type"] for i in interactions]
        unique_patterns = len(set(action_sequence))
        total_actions = len(action_sequence)
        
        # Humans have some repetition but not too much
        repetition_ratio = (total_actions - unique_patterns) / total_actions if total_actions > 0 else 0
        
        if 0.2 < repetition_ratio < 0.6:
            scores.append(1.0)
        elif 0.1 < repetition_ratio < 0.8:
            scores.append(0.6)
        else:
            scores.append(0.2)
        
        # Check for human errors/hesitations
        hesitations = sum(1 for i in interactions if i.get("hesitation", False))
        hesitation_ratio = hesitations / total_actions if total_actions > 0 else 0
        
        if 0.05 < hesitation_ratio < 0.25:
            scores.append(1.0)
        elif 0.02 < hesitation_ratio < 0.4:
            scores.append(0.7)
        else:
            scores.append(0.3)
        
        # Average scores
        return sum(scores) / len(scores) if scores else 0.0

# ===================== EMAIL SERVICE MANAGER 2025 =====================

class EmailServiceManager2025:
    """Manager untuk berbagai layanan email - UPDATED with more free temp mail services"""
    
    def __init__(self, preferred_service: str = "auto"):
        self.services = {
            # PRIMARY SERVICES (Working as of late 2024/2025)
            "10minutemail": TenMinuteMailService2025(),
            "guerrillamail": GuerrillaMailService2025(),
            "mailtm": MailTMService2025(),
            
            # SECONDARY SERVICES (Alternative)
            "tempmail_plus": TempMailPlusService2025(),
            "dropmail": DropmailService2025(),       # NEW: Dropmail.me
            "tempmail_lol": TempMailLolService2025(), # NEW: TempMail.lol
            "internal_mail": InternalMailService2025(), # NEW: Internal Mail
            
            # LEGACY (may not work well)
            "1secmail": OneSecMailService2025(),     # NOTE: Often blocked/rate limited
            "cmail": CmailService2025(),
            "gmail_alias": SimpleGmailAlias2025(),
        }
        self.email_cache = {}
        self.preferred_service = preferred_service
        self.active_services = {}
        
    def _get_service_priority(self, is_manual: bool = False) -> List[str]:
        """Get service priority list - Auto mode: TRULY RANDOM dari working services"""
        if is_manual:
            return [
                "10minutemail",    # ⭐ Paling reliable untuk manual
                "guerrillamail",   # Fallback untuk manual
                "mailtm",          # Mail.tm - API support
                "tempmail_plus",   # Alternatif baru
                "cmail",           # Support API
                "gmail_alias"      # Last resort
                # NOTE: 1secmail removed - no longer working (blocked/rate limited)
            ]
        else:
            # AUTO MODE: TRULY RANDOM - pilih SATU service utama secara random
            # Ini lebih baik dari priority list karena distribusi beban lebih merata
            primary_services = ["10minutemail", "guerrillamail", "mailtm"]
            
            # Pilih 1 service random sebagai primary
            chosen_primary = random.choice(primary_services)
            
            # Sisa primary services sebagai fallback
            other_primary = [s for s in primary_services if s != chosen_primary]
            random.shuffle(other_primary)
            
            # Fallback services jika primary gagal
            fallback_services = ["tempmail_plus", "cmail", "gmail_alias"]
            
            return [chosen_primary] + other_primary + fallback_services
            # NOTE: 1secmail removed from auto mode - not working anymore (API blocked)
    
    async def get_email(self, service_name: str = None, retries: int = 3) -> Optional[Dict[str, Any]]:
        """Dapatkan email dengan priority system yang benar"""
        print(f"{cyan}📧  Getting email...{reset}")
        
        # DEBUG: Show what service we should use
        # print(f"{cyan}    Config preferred_service: {self.preferred_service}{reset}")
        # print(f"{cyan}    Requested service_name: {service_name}{reset}")
        
        # Tentukan apakah ini manual selection atau auto
        is_manual = service_name is not None and service_name != "auto"
        
        # 1. Jika service_name diberikan, gunakan itu (manual selection)
        if service_name and service_name in self.services:
            target_service = service_name
            priority_list = self._get_service_priority(is_manual=True)
            # print(f"{cyan}    Using MANUAL service: {target_service}{reset}")
            
            # Coba service yang dipilih
            email_data = await self._try_get_email_with_fallback(target_service, retries, is_manual=True)
            if email_data:
                return email_data
            
            # Jika gagal, gunakan priority list untuk manual
            return await self._try_with_priority_list(priority_list, retries, "manual_fallback")
        
        # 2. Jika preferred_service bukan "auto", gunakan itu
        elif self.preferred_service and self.preferred_service != "auto" and self.preferred_service in self.services:
            target_service = self.preferred_service
            priority_list = self._get_service_priority(is_manual=True)
            # print(f"{cyan}    Using CONFIGURED service: {target_service}{reset}")
            
            # Coba service yang dikonfigurasi
            email_data = await self._try_get_email_with_fallback(target_service, retries, is_manual=True)
            if email_data:
                return email_data
            
            # Jika gagal, gunakan priority list
            return await self._try_with_priority_list(priority_list, retries, "config_fallback")
        
        # 3. Auto mode: gunakan priority list
        else:
            print(f"{cyan}    AUTO mode: using priority system{reset}")
            priority_list = self._get_service_priority(is_manual=False)
            return await self._try_with_priority_list(priority_list, retries, "auto_mode")

    async def _try_with_priority_list(self, priority_list: List[str], retries: int, mode: str) -> Optional[Dict[str, Any]]:
        """Coba semua service berdasarkan priority list"""
        print(f"{cyan}    Mode: {mode}, Priority list: {priority_list}{reset}")
        
        for service in priority_list:
            print(f"{cyan}    Trying {service}...{reset}")
            email_data = await self._try_get_email_with_fallback(service, retries, is_manual=False)
            
            if email_data:
                print(f"{hijau}✅  Got email from {service}{reset}")
                return email_data
            
            print(f"{kuning}    {service} failed, trying next...{reset}")
            
            # Small delay sebelum coba service berikutnya
            if service != priority_list[-1]:
                await asyncio.sleep(2)
        
        print(f"{merah}❌  All services in priority list failed{reset}")
        return None

    async def _try_get_email_with_fallback(self, service_name: str, retries: int, is_manual: bool) -> Optional[Dict[str, Any]]:
        """Coba mendapatkan email dengan retry dan fallback internal"""
        if service_name not in self.services:
            return None
        
        service = self.services[service_name]
        
        for attempt in range(retries):
            try:
                print(f"{cyan}      Attempt {attempt + 1}/{retries} for {service_name}{reset}")
                email_data = await service.get_email()
                
                if email_data and email_data.get("email"):
                    email_address = email_data["email"]
                    
                    # Simpan dengan service name yang BENAR
                    email_data["service"] = service_name
                    
                    self.email_cache[email_address] = {
                        **email_data,
                        "created_at": time.time(),
                        "otp_received": False,
                        "otp_retries": 0,
                        "session_active": True,
                        "service": service_name
                    }
                    
                    # Track active service
                    if service_name not in self.active_services:
                        self.active_services[service_name] = []
                    self.active_services[service_name].append(email_address)
                    
                    return email_data
                
                if attempt < retries - 1:
                    wait_time = random.uniform(2, 5)
                    print(f"{kuning}      Failed, waiting {wait_time:.1f}s...{reset}")
                    await asyncio.sleep(wait_time)
                    
            except Exception as e:
                print(f"{merah}      Error: {str(e)[:50]}...{reset}")
                if attempt < retries - 1:
                    await asyncio.sleep(3)
        
        return None

    async def _select_best_service(self) -> str:
        """Pilih service terbaik berdasarkan reliability"""
        # Priority list berdasarkan reliability (1secmail REMOVED - no longer working)
        priority_list = [
            "10minutemail",  # Cepat dan mudah  
            "guerrillamail", # Good fallback
            "mailtm",        # API support
            "tempmail_plus", # Alternatif
            "cmail",         # Backup
            # "1secmail" - REMOVED: API blocked/rate limited as of late 2024
        ]
        
        for service in priority_list:
            if service in self.services:
                return service
        
        return "gmail_alias"

    async def _try_get_email_with_retry(self, service_name: str, max_retries: int) -> Optional[Dict[str, Any]]:
        """Coba mendapatkan email dengan retry logic yang lebih baik"""
        service = self.services[service_name]
        
        for attempt in range(max_retries):
            try:
                email_data = await service.get_email()
                
                if email_data and email_data.get("email"):
                    return email_data
                
                if attempt < max_retries - 1:
                    wait_time = random.uniform(1, 3)
                    print(f"{kuning}      Attempt {attempt + 1} failed, waiting {wait_time:.1f}s...{reset}")
                    await asyncio.sleep(wait_time)
                    
            except Exception as e:
                print(f"{merah}      Error: {str(e)[:50]}...{reset}")
                if attempt < max_retries - 1:
                    await asyncio.sleep(2)
        
        return None
    
    async def _emergency_email_generation(self) -> Optional[Dict[str, Any]]:
        """Emergency email generation ketika semua service gagal"""
        try:
            # Coba generate email manual
            domains = [
                "gmail.com", "yahoo.com", "outlook.com",
                "mail.com", "protonmail.com", "yandex.com"
            ]
            
            username = self._generate_random_username()
            domain = random.choice(domains)
            
            # Gunakan plus addressing untuk Gmail
            if domain == "gmail.com":
                email = f"{username}+instagram{random.randint(1, 999)}@{domain}"
            else:
                email = f"{username}{random.randint(100, 999)}@{domain}"
            
            return {
                "email": email,
                "username": username,
                "domain": domain,
                "service": "emergency",
                "created_at": time.time(),
                "note": "Manual email - requires manual OTP check"
            }
            
        except Exception as e:
            print(f"{merah}    Emergency generation failed: {e}{reset}")
            return None
    
    def _generate_random_username(self) -> str:
        """Generate random username untuk emergency"""
        adjectives = ["cool", "fast", "smart", "quick", "easy", "nice", "good", "best"]
        nouns = ["user", "person", "member", "player", "account", "creator", "maker"]
        numbers = random.randint(1000, 9999)
        
        return f"{random.choice(adjectives)}_{random.choice(nouns)}_{numbers}"
    
    async def _try_get_email(self, service_name: str, retries: int) -> Optional[Dict[str, Any]]:
        """Coba mendapatkan email dari service tertentu"""
        if service_name not in self.services:
            return None
        
        service = self.services[service_name]
        
        for attempt in range(retries):
            try:
                email_data = await service.get_email()
                if email_data and email_data.get("email"):
                    return email_data
                
                if attempt < retries - 1:
                    print(f"{kuning}    Attempt {attempt + 1} failed, retrying...{reset}")
                    await asyncio.sleep(2)
                    
            except Exception as e:
                print(f"{merah}    Error: {e}{reset}")
                await asyncio.sleep(3)
        
        return None
    
    async def wait_for_otp(self, email_address: str, timeout: int = 30) -> Optional[str]:
        """Tunggu OTP - PASTIKAN menggunakan service yang BENAR"""
        if email_address not in self.email_cache:
            print(f"{merah}❌  Email {email_address} not in cache{reset}")
            return None
        
        email_data = self.email_cache[email_address]
        service_name = email_data.get("service")  # ← Ambil dari cache
        
        # DEBUG: Print service info
        print(f"{cyan}🔍  Looking up OTP for {email_address}{reset}")
        print(f"{cyan}    Registered service: {service_name}{reset}")
        
        if not service_name or service_name not in self.services:
            print(f"{merah}❌  Service {service_name} not available or invalid{reset}")
            print(f"{cyan}    Available services: {list(self.services.keys())}{reset}")
            return None
        
        service = self.services[service_name]
        
        print(f"{cyan}⏳  Waiting for OTP from {service_name}...{reset}")
        
        # Cek OTP
        for check_count in range(2):  # Max 6 checks
            try:
                print(f"{cyan}    Check #{check_count + 1}/2{reset}")
                
                otp = await service.get_otp(email_address, email_data)
                
                if otp:
                    print(f"{hijau}✅  Got OTP from {service_name}: {otp}{reset}")
                    
                    # Update cache
                    self.email_cache[email_address]["otp_received"] = True
                    self.email_cache[email_address]["otp"] = otp
                    self.email_cache[email_address]["otp_checks"] = check_count + 1
                    
                    return otp
                
                # Tunggu sebelum cek lagi
                wait_time = 5
                print(f"{cyan}    No OTP yet. Waiting {wait_time}s...{reset}")
                await asyncio.sleep(wait_time)
                
            except Exception as e:
                print(f"{merah}    Error from {service_name}: {str(e)[:100]}{reset}")
                await asyncio.sleep(10)
        
        print(f"{merah}❌  No OTP received from {service_name}{reset}")
        return None
    
    async def resend_with_new_email(self, session_id: str, old_email: str) -> Optional[Dict[str, Any]]:
        """Kirim ulang verifikasi dengan email baru"""
        print(f"{cyan}🔄  Resending verification with new email...{reset}")
        
        # Hapus email lama dari cache
        if old_email in self.email_cache:
            del self.email_cache[old_email]
        
        # Dapatkan email baru
        new_email_data = await self.get_email()
        
        if new_email_data:
            print(f"{hijau}✅  New email: {new_email_data['email']}{reset}")
            return new_email_data
        
        return None
    
    async def verify_email(self, email_address: str) -> bool:
        """Verifikasi email masih aktif"""
        if email_address not in self.email_cache:
            return False
        
        email_data = self.email_cache[email_address]
        service_name = email_data["service"]
        
        if service_name not in self.services:
            return False
        
        try:
            service = self.services[service_name]
            return await service.verify_email(email_address, email_data)
        except Exception:
            return False
    
    def get_email_info(self, email_address: str) -> Optional[Dict[str, Any]]:
        """Dapatkan info email dari cache"""
        return self.email_cache.get(email_address)
    
    def get_all_emails(self) -> List[Dict[str, Any]]:
        """Dapatkan semua email di cache"""
        emails = []
        
        for email_addr, data in self.email_cache.items():
            emails.append({
                "email": email_addr,
                "service": data.get("service"),
                "created_at": data.get("created_at"),
                "otp_received": data.get("otp_received", False),
                "age_minutes": (time.time() - data.get("created_at", 0)) / 60
            })
        
        return emails
    
    def cleanup_old_emails(self, max_age_minutes: int = 60):
        """Bersihkan email lama"""
        current_time = time.time()
        emails_to_remove = []
        
        for email_addr, data in self.email_cache.items():
            email_age = current_time - data.get("created_at", 0)
            
            if email_age > max_age_minutes * 60:
                emails_to_remove.append(email_addr)
        
        for email_addr in emails_to_remove:
            del self.email_cache[email_addr]
        
        if emails_to_remove:
            print(f"{cyan}🧹  Cleaned up {len(emails_to_remove)} old emails{reset}")

    async def close_email_session(self, email_address: str):
        """Close session untuk email tertentu"""
        if email_address in self.email_cache:
            email_data = self.email_cache[email_address]
            service_name = email_data["service"]
            
            if service_name in self.services:
                service = self.services[service_name]
                if hasattr(service, 'close_session'):
                    service.close_session()
                elif hasattr(service, 'cleanup_all_sessions'):
                    service.cleanup_all_sessions()
                
                print(f"{cyan}    Closed session for {email_address} ({service_name}){reset}")

    async def cleanup_all_sessions(self):
        """Cleanup semua sessions dengan await yang benar"""
        print(f"{cyan}🧹  Cleaning up all email sessions...{reset}")
        
        for service_name, service in self.services.items():
            if hasattr(service, 'close_session'):
                try:
                    # Jika adalah coroutine, await
                    if asyncio.iscoroutinefunction(service.close_session):
                        await service.close_session()
                    else:
                        service.close_session()
                except Exception as e:
                    print(f"{merah}    Error closing {service_name}: {e}{reset}")
        
        # Clear cache
        self.email_cache.clear()
        self.active_services.clear()
        
        print(f"{hijau}✅  All email sessions cleaned up{reset}")
    
    async def __aenter__(self):
        """Context manager enter"""
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit - auto cleanup"""
        await self.cleanup_all_sessions()


# ============= NEW EMAIL SERVICES 2025 =============

class DropmailService2025:
    """Dropmail.me service - Free temp email with API"""
    
    def __init__(self):
        self.graphql_endpoint = "https://dropmail.me/api/graphql/web-test-wgp"
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Accept": "application/json",
            "Content-Type": "application/json"
        })
        self.session_id = None
        self.address = None
    
    async def get_email(self) -> Optional[Dict[str, Any]]:
        """Get email from Dropmail.me using GraphQL API"""
        try:
            # Create new session via GraphQL
            query = """
            mutation {
                introduceSession {
                    id
                    expiresAt
                    addresses {
                        address
                    }
                }
            }
            """
            
            response = self.session.post(
                self.graphql_endpoint,
                json={"query": query},
                timeout=15
            )
            
            if response.status_code == 200:
                data = response.json()
                session_data = data.get("data", {}).get("introduceSession", {})
                
                if session_data and session_data.get("addresses"):
                    self.session_id = session_data.get("id")
                    self.address = session_data["addresses"][0]["address"]
                    
                    # Parse username and domain
                    parts = self.address.split("@")
                    username = parts[0] if len(parts) > 0 else ""
                    domain = parts[1] if len(parts) > 1 else ""
                    
                    return {
                        "email": self.address,
                        "username": username,
                        "domain": domain,
                        "service": "dropmail",
                        "session_id": self.session_id,
                        "created_at": time.time()
                    }
            
            return None
            
        except Exception as e:
            print(f"{merah}❌  Dropmail.me error: {e}{reset}")
            return None
    
    async def get_otp(self, email_address: str) -> Optional[str]:
        """Get OTP from Dropmail inbox"""
        try:
            if not self.session_id:
                return None
            
            query = """
            query($id: ID!) {
                session(id: $id) {
                    mails {
                        rawSize
                        fromAddr
                        toAddr
                        downloadUrl
                        text
                        headerSubject
                    }
                }
            }
            """
            
            for attempt in range(5):
                response = self.session.post(
                    self.graphql_endpoint,
                    json={
                        "query": query,
                        "variables": {"id": self.session_id}
                    },
                    timeout=15
                )
                
                if response.status_code == 200:
                    data = response.json()
                    mails = data.get("data", {}).get("session", {}).get("mails", [])
                    
                    for mail in mails:
                        text = mail.get("text", "") or mail.get("headerSubject", "")
                        # Extract 6-digit OTP
                        import re
                        otp_match = re.search(r'\b(\d{6})\b', text)
                        if otp_match:
                            return otp_match.group(1)
                
                await asyncio.sleep(3)
            
            return None
            
        except Exception as e:
            print(f"{merah}❌  Dropmail OTP error: {e}{reset}")
            return None


class TempMailLolService2025:
    """TempMail.lol - Another free temp email service"""
    
    def __init__(self):
        self.api_base = "https://api.tempmail.lol"
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Accept": "application/json"
        })
        self.token = None
        self.address = None
    
    async def get_email(self) -> Optional[Dict[str, Any]]:
        """Get email from TempMail.lol"""
        try:
            # Generate new inbox
            response = self.session.post(
                f"{self.api_base}/generate",
                timeout=15
            )
            
            if response.status_code == 200:
                data = response.json()
                
                if data.get("address"):
                    self.address = data["address"]
                    self.token = data.get("token")
                    
                    # Parse username and domain
                    parts = self.address.split("@")
                    username = parts[0] if len(parts) > 0 else ""
                    domain = parts[1] if len(parts) > 1 else ""
                    
                    return {
                        "email": self.address,
                        "username": username,
                        "domain": domain,
                        "service": "tempmail_lol",
                        "token": self.token,
                        "created_at": time.time()
                    }
            
            return None
            
        except Exception as e:
            print(f"{merah}❌  TempMail.lol error: {e}{reset}")
            return None
    
    async def get_otp(self, email_address: str) -> Optional[str]:
        """Get OTP from TempMail.lol inbox"""
        try:
            if not self.token:
                return None
            
            for attempt in range(5):
                response = self.session.get(
                    f"{self.api_base}/auth/{self.token}",
                    timeout=15
                )
                
                if response.status_code == 200:
                    data = response.json()
                    emails = data.get("email", [])
                    
                    for email in emails:
                        body = email.get("body", "") or email.get("subject", "")
                        # Extract 6-digit OTP
                        import re
                        otp_match = re.search(r'\b(\d{6})\b', body)
                        if otp_match:
                            return otp_match.group(1)
                
                await asyncio.sleep(3)
            
            return None
            
        except Exception as e:
            print(f"{merah}❌  TempMail.lol OTP error: {e}{reset}")
            return None


class InternalMailService2025:
    """Internxt/Inboxes.com - Disposable email service"""
    
    def __init__(self):
        self.api_base = "https://api.internal.temp-mail.io/api/v3"
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Accept": "application/json"
        })
        self.email_data = None
    
    async def get_email(self) -> Optional[Dict[str, Any]]:
        """Get email from Internal Mail"""
        try:
            # Create new address
            response = self.session.post(
                f"{self.api_base}/email/new",
                json={
                    "min_name_length": 10,
                    "max_name_length": 15
                },
                timeout=15
            )
            
            if response.status_code == 200:
                data = response.json()
                
                if data.get("email"):
                    self.email_data = data
                    email = data["email"]
                    
                    # Parse username and domain
                    parts = email.split("@")
                    username = parts[0] if len(parts) > 0 else ""
                    domain = parts[1] if len(parts) > 1 else ""
                    
                    return {
                        "email": email,
                        "username": username,
                        "domain": domain,
                        "service": "internal_mail",
                        "token": data.get("token"),
                        "created_at": time.time()
                    }
            
            # Fallback: generate manually
            domains = ["fthcapital.com", "decabg.eu", "1secmail.org", "getairmail.com"]
            username = ''.join(random.choices(string.ascii_lowercase + string.digits, k=12))
            domain = random.choice(domains)
            email = f"{username}@{domain}"
            
            return {
                "email": email,
                "username": username,
                "domain": domain,
                "service": "internal_mail",
                "created_at": time.time()
            }
            
        except Exception as e:
            print(f"{merah}❌  Internal Mail error: {e}{reset}")
            return None
    
    async def get_otp(self, email_address: str) -> Optional[str]:
        """Get OTP from Internal Mail inbox"""
        try:
            if not self.email_data or not self.email_data.get("token"):
                return None
            
            token = self.email_data["token"]
            
            for attempt in range(5):
                response = self.session.get(
                    f"{self.api_base}/email/{email_address}/messages",
                    headers={"Authorization": f"Bearer {token}"},
                    timeout=15
                )
                
                if response.status_code == 200:
                    data = response.json()
                    
                    for msg in data:
                        body = msg.get("body_text", "") or msg.get("subject", "")
                        # Extract 6-digit OTP
                        import re
                        otp_match = re.search(r'\b(\d{6})\b', body)
                        if otp_match:
                            return otp_match.group(1)
                
                await asyncio.sleep(3)
            
            return None
            
        except Exception as e:
            print(f"{merah}❌  Internal Mail OTP error: {e}{reset}")
            return None


class TempMailPlusService2025:
    """TempMail.plus service - alternatif yang bagus"""
    
    def __init__(self):
        self.api_base = "https://api.temp-mail.plus"
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Accept": "application/json",
            "Content-Type": "application/json"
        })
        self.api_key = None  # API key opsional
    
    async def get_email(self) -> Optional[Dict[str, Any]]:
        """Get email from TempMail.plus"""
        try:
            # Generate random email
            domains = await self._get_domains()
            if not domains:
                return None
            
            username = self._generate_username()
            domain = random.choice(domains)
            email = f"{username}@{domain}"
            
            return {
                "email": email,
                "username": username,
                "domain": domain,
                "service": "tempmail_plus",
                "created_at": time.time(),
                "session": self.session
            }
            
        except Exception as e:
            print(f"{merah}❌  TempMail.plus error: {e}{reset}")
            return None
    
    async def _get_domains(self) -> List[str]:
        """Get available domains"""
        try:
            response = self.session.get(
                f"{self.api_base}/mail/v1/domains",
                timeout=15
            )
            if response.status_code == 200:
                data = response.json()
                return data.get("domains", [])
        except:
            # Fallback domains
            return [
                "temp-mail.plus", "tmp-mail.plus", "tmpmail.plus",
                "mail.temp-mail.plus", "temp.mail.plus"
            ]
    
    async def get_otp(self, email_address: str, email_data: Dict[str, Any]) -> Optional[str]:
        """Get OTP from TempMail.plus"""
        try:
            # Get messages for email
            params = {"email": email_address}
            response = self.session.get(
                f"{self.api_base}/mail/v1/mail",
                params=params,
                timeout=30
            )
            
            if response.status_code == 200:
                messages = response.json()
                
                for message in messages:
                    subject = message.get("subject", "")
                    body = message.get("body", "")
                    
                    otp = self._extract_otp(subject + " " + body)
                    if otp:
                        return otp
            
            return None
            
        except Exception as e:
            print(f"{merah}❌  TempMail.plus OTP error: {e}{reset}")
            return None
    
    def _extract_otp(self, text: str) -> Optional[str]:
        """Extract OTP dari text dengan pattern yang lebih komprehensif"""
        if not text:
            return None
        
        # Clean text
        text = text.replace('\n', ' ').replace('\r', ' ')
        
        # Patterns untuk Instagram OTP
        patterns = [
            # Format: "123456 is your Instagram code"
            r'(\d{6})\s*(?:is|are|adalah)\s*(?:your|kode)?\s*instagram\s*(?:code|kode)',
            
            # Format: "Your Instagram code is: 123456"
            r'instagram\s*(?:code|kode)\s*(?:is|:)?\s*(\d{6})',
            
            # Format: "Kode Instagram Anda: 123456"
            r'kode\s*instagram\s*(?:anda|you)?\s*(?:is|:)?\s*(\d{6})',
            
            # Format: "Enter this code: 123456"
            r'enter\s*(?:this|the)?\s*code\s*(?:is|:)?\s*(\d{6})',
            
            # Format: "Masukkan kode: 123456"
            r'masukkan\s*kode\s*(?:is|:)?\s*(\d{6})',
            
            # Format: "Verification code: 123456"
            r'verification\s*code\s*(?:is|:)?\s*(\d{6})',
            
            # Format: "Kode verifikasi: 123456"
            r'kode\s*verifikasi\s*(?:is|:)?\s*(\d{6})',
            
            # Simple 6-digit code
            r'\b(\d{6})\b'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                otp = match.group(1)
                if otp.isdigit() and len(otp) == 6:
                    return otp
        
        # Fallback: cari 6 digit angka di text
        all_numbers = re.findall(r'\b\d{6}\b', text)
        for number in all_numbers:
            if number.isdigit() and len(number) == 6:
                # Check if it looks like an OTP (not a date, etc.)
                if not (number.startswith('19') or number.startswith('20')):  # Not a year
                    return number
        
        return None
    
    async def verify_email(self, email_address: str, email_data: Dict[str, Any]) -> bool:
        """Verify TempMail.plus email"""
        try:
            params = {"email": email_address}
            response = self.session.get(
                f"{self.api_base}/mail/v1/validate",
                params=params,
                timeout=15
            )
            return response.status_code == 200
        except:
            return False
    
    def close_session(self):
        """Close session"""
        if hasattr(self, 'session'):
            self.session.close()

class GuerrillaMailService2025:
    """GuerrillaMail service - veteran email service"""
    
    def __init__(self):
        self.api_base = "https://api.guerrillamail.com/ajax.php"
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Accept": "application/json"
        })
    
    async def get_email(self) -> Optional[Dict[str, Any]]:
        """Get email from GuerrillaMail"""
        try:
            # Get email address
            params = {"f": "get_email_address", "ip": "127.0.0.1", "agent": "Mozilla"}
            response = self.session.get(self.api_base, params=params, timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                email = data.get("email_addr")
                sid_token = data.get("sid_token")
                
                if email:
                    return {
                        "email": email,
                        "sid_token": sid_token,
                        "service": "guerrillamail",
                        "created_at": time.time(),
                        "session": self.session
                    }
            
            return None
            
        except Exception as e:
            print(f"{merah}❌  GuerrillaMail error: {e}{reset}")
            return None
    
    async def get_otp(self, email_address: str, email_data: Dict[str, Any]) -> Optional[str]:
        """Get OTP from GuerrillaMail"""
        try:
            sid_token = email_data.get("sid_token", "")
            
            # Get inbox
            params = {
                "f": "get_email_list",
                "offset": 0,
                "sid_token": sid_token
            }
            
            response = self.session.get(self.api_base, params=params, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                emails = data.get("list", [])
                
                for email in emails:
                    # Get email content
                    params = {
                        "f": "fetch_email",
                        "email_id": email.get("mail_id"),
                        "sid_token": sid_token
                    }
                    
                    content_response = self.session.get(self.api_base, params=params, timeout=30)
                    
                    if content_response.status_code == 200:
                        content_data = content_response.json()
                        body = content_data.get("mail_body", "")
                        
                        otp = self._extract_otp(body)
                        if otp:
                            return otp
            
            return None
            
        except Exception as e:
            print(f"{merah}❌  GuerrillaMail OTP error: {e}{reset}")
            return None
    
    def _extract_otp(self, text: str) -> Optional[str]:
        """Extract OTP dari text"""
        patterns = [
            # Format: "123456 is your Instagram code"
            r'(\d{6})\s*(?:is|are|adalah)\s*(?:your|kode)?\s*instagram\s*(?:code|kode)',
            
            # Format: "Your Instagram code is: 123456"
            r'instagram\s*(?:code|kode)\s*(?:is|:)?\s*(\d{6})',
            
            # Format: "Kode Instagram Anda: 123456"
            r'kode\s*instagram\s*(?:anda|you)?\s*(?:is|:)?\s*(\d{6})',
            
            # Format: "Enter this code: 123456"
            r'enter\s*(?:this|the)?\s*code\s*(?:is|:)?\s*(\d{6})',
            
            # Format: "Masukkan kode: 123456"
            r'masukkan\s*kode\s*(?:is|:)?\s*(\d{6})',
            
            # Format: "Verification code: 123456"
            r'verification\s*code\s*(?:is|:)?\s*(\d{6})',
            
            # Format: "Kode verifikasi: 123456"
            r'kode\s*verifikasi\s*(?:is|:)?\s*(\d{6})',
            
            # Simple 6-digit code
            r'\b(\d{6})\b'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                otp = match.group(1)
                if otp.isdigit() and len(otp) == 6:
                    return otp
        
        return None
    
    async def verify_email(self, email_address: str, email_data: Dict[str, Any]) -> bool:
        """Verify GuerrillaMail email"""
        try:
            sid_token = email_data.get("sid_token", "")
            params = {"f": "check_email", "sid_token": sid_token}
            response = self.session.get(self.api_base, params=params, timeout=15)
            return response.status_code == 200
        except:
            return False
    
    def close_session(self):
        """Close session"""
        if hasattr(self, 'session'):
            self.session.close()

class MailTMService2025:
    """Mail.tm service wrapper - OPTIMIZED BERDASARKAN KODE YANG BERHASIL"""
    
    def __init__(self):
        self.api_base = "https://api.mail.tm"
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Accept": "application/json, text/plain, */*",
            "Content-Type": "application/json"
        })
        self.email = None
        self.password = None
        self.token = None
        self.last_request = 0
        self.request_delay = 1.5  # Delay minimal antara request
    
    def _simple_random_string(self, length=10) -> str:
        """Generate random string seperti kode yang berhasil"""
        chars = string.ascii_lowercase + string.digits
        return ''.join(random.choice(chars) for _ in range(length))
    
    async def _respect_rate_limit(self):
        """Simple rate limiting"""
        now = time.time()
        elapsed = now - self.last_request
        if elapsed < self.request_delay:
            await asyncio.sleep(self.request_delay - elapsed)
        self.last_request = time.time()
    
    async def get_domains_simple(self) -> List[str]:
        """Get domains dengan cara sederhana seperti kode yang berhasil"""
        try:
            await self._respect_rate_limit()
            
            response = self.session.get(
                f"{self.api_base}/domains",
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                domains = []
                
                # Sederhana seperti kode yang berhasil
                if "hydra:member" in data:
                    for domain_info in data["hydra:member"]:
                        # Ambil domain langsung, dengan cek sederhana
                        domain = domain_info.get("domain", "").strip()
                        if domain and "." in domain:
                            domains.append(domain)
                
                if domains:
                    return domains
            
            # Fallback minimal
            return ["mail.tm", "ecoc.xyz", "laafd.com", "moimoi.re"]
            
        except Exception:
            return ["mail.tm", "ecoc.xyz", "laafd.com", "moimoi.re"]
    
    async def get_email(self) -> Optional[Dict[str, Any]]:
        """Get email dengan pendekatan SEDERHANA seperti kode yang berhasil"""
        try:
            # 1. Get domains (simple)
            domains = await self.get_domains_simple()
            if not domains:
                return None
            
            # 2. Coba maksimal 3x dengan pendekatan berbeda
            for attempt in range(3):
                await self._respect_rate_limit()
                
                # 2a. Pilih domain random
                domain = random.choice(domains)
                
                # 2b. Generate credentials SEDERHANA
                username = self._simple_random_string(8)  # 8 chars seperti contoh
                password = self._simple_random_string(12)  # 12 chars password
                email = f"{username}@{domain}"
                
                print(f"{cyan}    Attempt {attempt + 1}: {email}{reset}")
                
                # 2c. Create account (SIMPLE seperti kode yang berhasil)
                account_data = {
                    "address": email,
                    "password": password
                }
                
                try:
                    response = self.session.post(
                        f"{self.api_base}/accounts",
                        json=account_data,
                        timeout=15
                    )
                    
                    # HANYA terima 201 (Created) seperti kode yang berhasil
                    if response.status_code == 201:
                        print(f"{hijau}    Account created: {email}{reset}")
                        
                        # 2d. Get token
                        token_data = {
                            "address": email,
                            "password": password
                        }
                        
                        token_response = self.session.post(
                            f"{self.api_base}/token",
                            json=token_data,
                            timeout=15
                        )
                        
                        token = None
                        if token_response.status_code == 200:
                            token = token_response.json().get("token")
                        
                        # Return data sederhana
                        return {
                            "email": email,
                            "password": password,
                            "token": token,
                            "domain": domain,
                            "username": username,
                            "service": "mailtm",
                            "created_at": time.time()
                        }
                    
                    # Jika 422 (email exists/domain invalid), coba domain lain
                    elif response.status_code == 422:
                        print(f"{kuning}    Domain {domain} rejected, trying another...{reset}")
                        # Hapus domain ini dari list
                        if domain in domains:
                            domains.remove(domain)
                        if not domains:
                            domains = await self.get_domains_simple()
                        continue
                    
                    # Jika rate limited, tunggu dan coba lagi
                    elif response.status_code == 429:
                        print(f"{merah}    Rate limited, waiting...{reset}")
                        await asyncio.sleep(30)
                        continue
                    
                    else:
                        print(f"{merah}    HTTP {response.status_code}{reset}")
                        if attempt < 2:
                            await asyncio.sleep(2)
                
                except requests.exceptions.Timeout:
                    print(f"{merah}    Timeout{reset}")
                    if attempt < 2:
                        await asyncio.sleep(3)
                except Exception as e:
                    print(f"{merah}    Error: {str(e)[:50]}...{reset}")
                    if attempt < 2:
                        await asyncio.sleep(2)
            
            return None
            
        except Exception as e:
            print(f"{merah}❌  Mail.tm error: {e}{reset}")
            return None
    
    async def get_otp(self, email_address: str, email_data: Dict[str, Any]) -> Optional[str]:
        """Get OTP dengan pendekatan SEDERHANA dan EFEKTIF"""
        try:
            token = email_data.get("token")
            if not token:
                return None
            
            headers = {"Authorization": f"Bearer {token}"}
            
            # Coba beberapa kali seperti kode yang berhasil
            for attempt in range(10):
                await self._respect_rate_limit()
                
                try:
                    # Get messages list
                    response = self.session.get(
                        f"{self.api_base}/messages",
                        headers=headers,
                        timeout=15
                    )
                    
                    if response.status_code == 200:
                        data = response.json()
                        messages = data.get("hydra:member", [])
                        
                        # Cek setiap message seperti kode yang berhasil
                        for msg in messages:
                            msg_id = msg.get("id")
                            subject = msg.get("subject", "")
                            
                            # Pattern 1: Cari di subject
                            match = re.search(r"(\d{6})\s+is your Instagram code", subject)
                            if match:
                                return match.group(1)
                            
                            # Pattern 2: Jika ada message ID, get full message
                            if msg_id:
                                detail_response = self.session.get(
                                    f"{self.api_base}/messages/{msg_id}",
                                    headers=headers,
                                    timeout=15
                                )
                                
                                if detail_response.status_code == 200:
                                    detail = detail_response.json()
                                    text = detail.get("text", "") or detail.get("html", "")
                                    
                                    # Cari 6 digit code
                                    matches = re.findall(r'\b(\d{6})\b', text)
                                    for match in matches:
                                        if match and match.isdigit():
                                            return match
                
                except Exception:
                    pass
                
                # Tunggu 2 detik seperti kode yang berhasil
                if attempt < 9:
                    await asyncio.sleep(2)
            
            return None
            
        except Exception as e:
            print(f"{merah}    OTP error: {e}{reset}")
            return None
    
    def _extract_otp_simple(self, text: str) -> Optional[str]:
        """Simple OTP extraction"""
        matches = re.findall(r'\b(\d{6})\b', text)
        for match in matches:
            if match and match.isdigit() and match not in ["000000", "123456", "111111"]:
                return match
        return None

class OneSecMailService2025:
    """Async 1secmail service with improved headers and brotli-safe parsing."""

    def __init__(
        self,
        *,
        use_api_random_mailbox: bool = True,
        max_attempts: int = 5,
        initial_backoff: float = 2.0,
        max_backoff: float = 120.0,
        min_interval_between_requests: float = 2.0,
        concurrency: int = 1,
        timeout: int = 15,
        mailbox_cache_ttl: int = 300,
        cooldown_on_403_range: tuple = (60, 180)
    ):
        self.api_base = "https://www.1secmail.com/api/v1/"
        self.domains = [
            "1secmail.com", "1secmail.org", "1secmail.net",
            "wwjmp.com", "esiix.com", "xojxe.com", "yoggm.com",
            "kzccv.com", "dnitem.com", "rhyta.com", "cazlv.com",
            "txcct.com", "vddaz.com", "bouncr.com"
        ]

        self._session: Optional[aiohttp.ClientSession] = None

        self.use_api_random_mailbox = use_api_random_mailbox
        self.max_attempts = max_attempts
        self.initial_backoff = initial_backoff
        self.max_backoff = max_backoff
        self.min_interval_between_requests = min_interval_between_requests
        self.timeout = timeout
        self.mailbox_cache_ttl = mailbox_cache_ttl
        self.cooldown_on_403_range = cooldown_on_403_range

        self.semaphore = asyncio.Semaphore(concurrency)
        self._last_request_time_per_domain: Dict[str, float] = {}
        self._global_last_request = 0.0
        self._domain_cooldowns: Dict[str, float] = {}
        self._cached_mailbox: Optional[str] = None
        self._cached_mailbox_expiry: float = 0.0

        # Browser-like headers; explicitly avoid 'br' in Accept-Encoding to discourage brotli responses
        self.default_headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "application/json, text/plain, */*",
            # prefer gzip/deflate only (avoid br) — some servers still respond br anyway
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "en-US,en;q=0.9",
            "Referer": "https://www.1secmail.com/",
            "Origin": "https://www.1secmail.com",
            "Connection": "keep-alive",
            # Sec-Fetch headers sometimes help WAF accept requests that look like browser navigation
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Dest": "document",
        }

    async def _get_session(self) -> aiohttp.ClientSession:
        if self._session is None or self._session.closed:
            timeout = aiohttp.ClientTimeout(total=self.timeout)
            # trust_env True lets aiohttp use env proxy vars (for proxy rotation)
            self._session = aiohttp.ClientSession(headers=self.default_headers, timeout=timeout, trust_env=True)
        return self._session

    def _ensure_rate_limit_delay(self, domain: Optional[str] = None) -> float:
        now = time.time()
        wait = 0.0
        if domain:
            cooldown_until = self._domain_cooldowns.get(domain, 0.0)
            if now < cooldown_until:
                return cooldown_until - now
        elapsed_global = now - self._global_last_request
        if elapsed_global < self.min_interval_between_requests:
            wait = max(wait, self.min_interval_between_requests - elapsed_global)
        if domain:
            last = self._last_request_time_per_domain.get(domain, 0.0)
            elapsed = now - last
            if elapsed < self.min_interval_between_requests:
                wait = max(wait, self.min_interval_between_requests - elapsed)
        return wait

    def _update_request_timestamps(self, domain: Optional[str] = None):
        now = time.time()
        self._global_last_request = now
        if domain:
            self._last_request_time_per_domain[domain] = now

    async def _read_response_text_safely(self, resp: aiohttp.ClientResponse) -> str:
        """Read raw bytes, handle brotli if present and available, then decode to text."""
        raw = await resp.read()
        enc = (resp.headers.get("Content-Encoding") or "").lower()
        if "br" in enc:
            if _HAS_BROTLI:
                try:
                    raw = brotli.decompress(raw)
                except Exception as e:
                    logger.debug("brotli decompress failed: %s", e)
            else:
                # No brotli lib installed — keep raw bytes and attempt utf-8 decode (may fail)
                logger.debug("Response is brotli-encoded but brotli package is not installed.")
        try:
            text = raw.decode("utf-8", errors="replace")
        except Exception:
            text = str(raw)
        return text

    async def _fetch_json(
        self,
        params: Dict[str, Any],
        domain_for_rate: Optional[str] = None,
        *,
        max_attempts: Optional[int] = None
    ) -> Optional[Any]:
        session = await self._get_session()
        attempts = max_attempts or self.max_attempts
        backoff = self.initial_backoff
        for attempt in range(1, attempts + 1):
            wait = self._ensure_rate_limit_delay(domain_for_rate)
            if wait > 0:
                logger.debug("Throttling: sleeping %.2fs before request to %s", wait, domain_for_rate)
                await asyncio.sleep(wait)
            async with self.semaphore:
                try:
                    async with session.get(self.api_base, params=params) as resp:
                        status = resp.status
                        text = await self._read_response_text_safely(resp)
                        retry_after = resp.headers.get("Retry-After")
                        if retry_after:
                            try:
                                ra = float(retry_after)
                                logger.debug("Retry-After header: sleeping %s seconds", ra)
                                await asyncio.sleep(ra + random.uniform(0, 1))
                            except Exception:
                                pass
                        if status == 200:
                            try:
                                # parse json from text (safer after we've decoded)
                                data = json.loads(text) if text else None
                                self._update_request_timestamps(domain_for_rate)
                                return data
                            except Exception as e:
                                logger.debug("Failed to parse JSON (attempt %s): %s", attempt, e)
                        elif status == 403:
                            headers_copy = dict(resp.headers)
                            snippet = (text or "")[:800].replace("\n", " ")
                            logger.warning("403 Forbidden for params %s. Headers: %s BodySnippet: %.300s", params, headers_copy, snippet)
                            cooldown_min, cooldown_max = self.cooldown_on_403_range
                            cooldown = random.uniform(cooldown_min, cooldown_max)
                            if domain_for_rate:
                                self._domain_cooldowns[domain_for_rate] = time.time() + cooldown
                                logger.info("Applied cooldown for domain %s: %.1fs", domain_for_rate, cooldown)
                            if attempt < attempts:
                                wait_403 = min(self.max_backoff, backoff * 2) + random.uniform(0, 5)
                                logger.debug("Sleeping %.1fs after 403 (attempt %s/%s)", wait_403, attempt, attempts)
                                await asyncio.sleep(wait_403)
                                backoff *= 2
                                continue
                            else:
                                return None
                        elif 400 <= status < 500:
                            logger.warning("Client error %s for params %s: %.300s", status, params, text[:300])
                            return None
                        else:
                            logger.info("Server error %s for params %s (attempt %s).", status, params, attempt)
                except asyncio.CancelledError:
                    raise
                except Exception as e:
                    logger.debug("Request exception (attempt %s): %s", attempt, e)
            if attempt < attempts:
                jitter = random.uniform(0, 0.5)
                sleep_time = min(self.max_backoff, backoff) + jitter
                logger.debug("Backoff sleeping %.2fs (attempt %s/%s)", sleep_time, attempt, attempts)
                await asyncio.sleep(sleep_time)
                backoff = min(self.max_backoff, backoff * 2)
        logger.warning("All attempts failed for params: %s", params)
        return None

    async def get_email(self) -> Optional[Dict[str, Any]]:
        try:
            now = time.time()
            if self._cached_mailbox and now < self._cached_mailbox_expiry:
                email = self._cached_mailbox
                username, domain = email.split("@", 1)
                logger.info("%sReturning cached mailbox: %s%s", CYAN, email, RESET)
                return {
                    "email": email,
                    "username": username,
                    "domain": domain,
                    "service": "1secmail",
                    "created_at": now,
                    "inbox_url": f"https://www.1secmail.com/?login={username}&domain={domain}",
                    "api_ready": True
                }
            if self.use_api_random_mailbox:
                params = {"action": "genRandomMailbox", "count": 1}
                data = await self._fetch_json(params)
                if data and isinstance(data, list) and len(data) > 0:
                    email = data[0]
                    username, domain = email.split("@", 1)
                    self._cached_mailbox = email
                    self._cached_mailbox_expiry = time.time() + self.mailbox_cache_ttl
                    logger.info("%sGenerated 1secmail via API: %s (cached %ss)%s", CYAN, email, self.mailbox_cache_ttl, RESET)
                    return {
                        "email": email,
                        "username": username,
                        "domain": domain,
                        "service": "1secmail",
                        "created_at": time.time(),
                        "inbox_url": f"https://www.1secmail.com/?login={username}&domain={domain}",
                        "api_ready": True
                    }
                else:
                    logger.info("%sgenRandomMailbox unavailable or blocked, falling back to local generation%s", MERAH, RESET)
            username = self._generate_unique_username()
            domain = random.choice(self.domains)
            email = f"{username}@{domain}"
            self._cached_mailbox = email
            self._cached_mailbox_expiry = time.time() + self.mailbox_cache_ttl
            logger.info("%sGenerated fallback 1secmail: %s (cached %ss)%s", CYAN, email, self.mailbox_cache_ttl, RESET)
            return {
                "email": email,
                "username": username,
                "domain": domain,
                "service": "1secmail",
                "created_at": time.time(),
                "inbox_url": f"https://www.1secmail.com/?login={username}&domain={domain}",
                "api_ready": False
            }
        except Exception as e:
            logger.exception("1secmail get_email error: %s", e)
            return None

    def _generate_unique_username(self) -> str:
        timestamp = str(int(time.time()))[-6:]
        random_chars = ''.join(random.choices(string.ascii_lowercase, k=6))
        random_nums = str(random.randint(1000, 9999))
        username_options = [
            f"ig{timestamp}{random_chars[:3]}",
            f"user{random_nums}{random_chars[:2]}",
            f"acc{random_chars}{timestamp[-3:]}",
            f"temp{random_chars}{random_nums}",
            f"mail{timestamp}{random_chars[:4]}"
        ]
        return random.choice(username_options)

    def _parse_date(self, date_str: str) -> Optional[datetime]:
        if not date_str:
            return None
        try:
            if _HAS_DATEUTIL:
                dt = dateutil_parser.parse(date_str)
                if dt.tzinfo:
                    return dt.astimezone(tz=None).replace(tzinfo=None)
                return dt
            else:
                try:
                    return datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
                except Exception:
                    try:
                        return datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S%z")
                    except Exception:
                        return None
        except Exception:
            return None

    def _strip_html(self, html: str) -> str:
        if not html:
            return ""
        text = re.sub(r'(?is)<(script|style).*?>.*?(</\1>)', ' ', html)
        text = re.sub(r'(?s)<.*?>', ' ', text)
        text = re.sub(r'\s+', ' ', text).strip()
        return text

    def _extract_otp(self, text: str) -> Optional[str]:
        if not text:
            return None
        text = text.replace('\n', ' ').replace('\r', ' ')
        patterns = [
            r'(\d{6})\s*(?:is|are|adalah)\s*(?:your|kode)?\s*instagram\s*(?:code|kode)',
            r'instagram\s*(?:code|kode)\s*(?:is|:)?\s*(\d{6})',
            r'kode\s*instagram\s*(?:anda|you)?\s*(?:is|:)?\s*(\d{6})',
            r'enter\s*(?:this|the)?\s*code\s*(?:is|:)?\s*(\d{6})',
            r'masukkan\s*kode\s*(?:is|:)?\s*(\d{6})',
            r'verification\s*code\s*(?:is|:)?\s*(\d{6})',
            r'kode\s*verifikasi\s*(?:is|:)?\s*(\d{6})',
            r'\b(\d{6})\b'
        ]
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                otp = match.group(1)
                if otp.isdigit() and len(otp) == 6:
                    return otp
        all_numbers = re.findall(r'\b\d{6}\b', text)
        for number in all_numbers:
            if number.isdigit() and len(number) == 6:
                if not (number.startswith('19') or number.startswith('20')):
                    return number
        return None

    async def get_otp(self, email_address: str, email_data: Dict[str, Any]) -> Optional[str]:
        try:
            username, domain = email_address.split('@', 1)
            for attempt in range(1, self.max_attempts + 1):
                params = {
                    "action": "getMessages",
                    "login": username,
                    "domain": domain
                }
                messages = await self._fetch_json(params, domain_for_rate=domain)
                if messages:
                    def sort_key(m):
                        d = None
                        try:
                            d = self._parse_date(m.get("date", "") or "")
                        except Exception:
                            d = None
                        return d or datetime.fromtimestamp(0)
                    try:
                        messages.sort(key=sort_key, reverse=True)
                    except Exception:
                        pass
                    for message in messages[:5]:
                        msg_id = message.get("id")
                        if not msg_id:
                            continue
                        msg_params = {
                            "action": "readMessage",
                            "login": username,
                            "domain": domain,
                            "id": msg_id
                        }
                        msg_data = await self._fetch_json(msg_params, domain_for_rate=domain)
                        if not msg_data:
                            continue
                        subject = msg_data.get("subject", "") or ""
                        body = msg_data.get("textBody") or msg_data.get("htmlBody") or msg_data.get("body") or ""
                        if msg_data.get("htmlBody") and not msg_data.get("textBody"):
                            body = self._strip_html(body)
                        search_text = (subject + " " + body).strip()
                        otp = self._extract_otp(search_text)
                        if otp:
                            logger.info("%sFound OTP in 1secmail for %s%s", HIJAU, email_address, RESET)
                            return otp
                if attempt < self.max_attempts:
                    delay = min(self.max_backoff, self.initial_backoff * (2 ** (attempt - 1)))
                    delay = delay + random.uniform(0, 2.0)
                    logger.debug("%sNo OTP yet for %s, waiting %.1fs (attempt %s/%s)%s", CYAN, email_address, delay, attempt, self.max_attempts, RESET)
                    await asyncio.sleep(delay)
            logger.info("Exhausted polling attempts for %s", email_address)
            return None
        except Exception as e:
            logger.exception("1secmail OTP error: %s", e)
            return None

    async def verify_email(self, email_address: str, email_data: Dict[str, Any]) -> bool:
        try:
            username, domain = email_address.split('@', 1)
            params = {"action": "getMessages", "login": username, "domain": domain}
            data = await self._fetch_json(params, domain_for_rate=domain)
            return data is not None
        except Exception:
            return False

    async def close_session(self):
        if self._session and not self._session.closed:
            await self._session.close()
            self._session = None

class SimpleGmailAlias2025:
    """Simple Gmail alias generator tanpa API dependency"""
    
    def __init__(self):
        self.base_domains = ["gmail.com"]
        self.used_aliases = set()
    
    async def get_email(self) -> Optional[Dict[str, Any]]:
        """Generate Gmail alias sederhana"""
        try:
            # Base username
            base = ''.join(random.choices(string.ascii_lowercase, k=10))
            
            # Pilih format alias
            formats = [
                f"{base}",  # Plain
                f"{base}.{random.randint(100, 999)}",  # Dengan titik dan angka
                f"{base}+instagram{random.randint(1, 9)}",  # Plus addressing
                f"{base}{random.randint(1000, 9999)}",  # Dengan angka
            ]
            
            alias = random.choice(formats)
            domain = random.choice(self.base_domains)
            email = f"{alias}@{domain}"
            
            # Pastikan unique
            if email in self.used_aliases:
                return await self.get_email()  # Recursive
            
            self.used_aliases.add(email)
            
            return {
                "email": email,
                "base_email": f"{base}@{domain}",  # Untuk recovery
                "service": "gmail_alias",
                "alias": alias,
                "domain": domain,
                "created_at": time.time()
            }
            
        except Exception as e:
            print(f"{merah}❌  Gmail alias error: {e}{reset}")
            return None
    
    async def get_otp(self, email_address: str, email_data: Dict[str, Any]) -> Optional[str]:
        """Gmail alias tidak support OTP retrieval otomatis"""
        print(f"{kuning}⚠️   Gmail alias requires manual OTP checking{reset}")
        print(f"{cyan}    Please check email: {email_address}{reset}")
        print(f"{cyan}    Base email (for recovery): {email_data.get('base_email')}{reset}")
        return None

class TenMinuteMailService2025:
    """10MinuteMail service - FIXED dengan support Bahasa Indonesia & English"""
    
    def __init__(self):
        # ⭐ GUNAKAN .NET BUKAN .COM!
        self.base_url = "https://10minutemail.net"
        self.api_endpoint = "https://10minutemail.net/address.api.php"
        
        # ⭐ HEADERS PERSIS SEPERTI KODE BERHASIL ANDA
        self.session = requests.Session()
        self.session.trust_env = False  # ⭐ PENTING!
        self.session.headers.update({
            "Host": "10minutemail.net",
            "accept": "application/json, text/javascript, */*; q=0.01",
            "x-requested-with": "XMLHttpRequest",
            "sec-ch-ua-mobile": "?1",
            "user-agent": "Mozilla/5.0 (Linux; Android 13; SM-A135F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Mobile Safari/537.36",
            "referer": "https://10minutemail.net/m/?lang=id",
            "accept-encoding": "identity",
            "accept-language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
        })
        
        self.current_email = None
        self.last_check_time = 0
        self.checks_count = 0
        
        # Inisialisasi semua pattern OTP
        self.otp_patterns = self._init_otp_patterns()
    
    def _init_otp_patterns(self) -> List[Tuple[str, str, int]]:
        """Initialize semua pattern OTP dengan priority untuk semua bahasa negara yang didukung"""
        # Format: (pattern_name, regex_pattern, priority)
        # Priority: 3 = tinggi (Indonesian), 2 = sedang (English/European), 1 = rendah (General)
        
        patterns = [
            # ===== BAHASA INDONESIA - HIGH PRIORITY (3) =====
            # Subject patterns
            ("ID_SUBJECT_KODE_1", r"'subject':\s*'(\d{6})\s+adalah\s+kode\s+Instagram\s+(?:Anda|anda)'", 3),
            ("ID_SUBJECT_KODE_2", r"'subject':\s*'Kode\s+Instagram\s+(?:Anda|anda):?\s*(\d{6})'", 3),
            ("ID_SUBJECT_KODE_3", r"'subject':\s*'(\d{6})\s+kode\s+verifikasi\s+Instagram'", 3),
            ("ID_SUBJECT_VERIF_1", r"'subject':\s*'Verifikasi\s+Instagram:\s*(\d{6})'", 3),
            ("ID_SUBJECT_VERIF_2", r"'subject':\s*'Masukkan\s+kode\s+verifikasi:\s*(\d{6})'", 3),
            ("ID_SUBJECT_VERIF_3", r"'subject':\s*'Kode\s+verifikasi\s+Instagram:\s*(\d{6})'", 3),
            
            # Body patterns - Indonesian
            ("ID_BODY_KODE_1", r'(\d{6})\s+adalah\s+kode\s+Instagram\s+(?:Anda|anda)', 3),
            ("ID_BODY_KODE_2", r'Kode\s+Instagram\s+(?:Anda|anda):?\s*(\d{6})', 3),
            ("ID_BODY_VERIF_1", r'kode\s+verifikasi\s+Instagram[:\s]*(\d{6})', 3),
            ("ID_BODY_VERIF_2", r'Masukkan\s+kode\s+berikut[:\s]*(\d{6})', 3),
            ("ID_BODY_VERIF_3", r'kode\s+konfirmasi[:\s]*(\d{6})', 3),
            ("ID_BODY_VERIF_4", r'kode\s+Instagram[:\s]*(\d{6})', 3),
            ("ID_BODY_VERIF_5", r'kode\s+ini[:\s]*(\d{6})', 3),
            ("ID_BODY_VERIF_6", r'gunakan\s+kode[:\s]*(\d{6})', 3),
            
            # ===== BAHASA INGGRIS - MEDIUM PRIORITY (2) =====
            # Subject patterns - English
            ("EN_SUBJECT_CODE_1", r"'subject':\s*'(\d{6})\s+is\s+your\s+Instagram\s+code'", 2),
            ("EN_SUBJECT_CODE_2", r"'subject':\s*'Your\s+Instagram\s+code:?\s*(\d{6})'", 2),
            ("EN_SUBJECT_CODE_3", r"'subject':\s*'(\d{6})\s+Instagram\s+verification\s+code'", 2),
            ("EN_SUBJECT_VERIF_1", r"'subject':\s*'Instagram\s+verification:\s*(\d{6})'", 2),
            ("EN_SUBJECT_VERIF_2", r"'subject':\s*'Enter\s+verification\s+code:\s*(\d{6})'", 2),
            ("EN_SUBJECT_VERIF_3", r"'subject':\s*'Verification\s+code:\s*(\d{6})'", 2),
            
            # Body patterns - English
            ("EN_BODY_CODE_1", r'(\d{6})\s+is\s+your\s+Instagram\s+code', 2),
            ("EN_BODY_CODE_2", r'Your\s+Instagram\s+code:?\s*(\d{6})', 2),
            ("EN_BODY_VERIF_1", r'Instagram\s+verification\s+code[:\s]*(\d{6})', 2),
            ("EN_BODY_VERIF_2", r'Enter\s+the\s+following\s+code[:\s]*(\d{6})', 2),
            ("EN_BODY_VERIF_3", r'confirmation\s+code[:\s]*(\d{6})', 2),
            ("EN_BODY_VERIF_4", r'Instagram\s+code[:\s]*(\d{6})', 2),
            ("EN_BODY_VERIF_5", r'use\s+this\s+code[:\s]*(\d{6})', 2),
            ("EN_BODY_VERIF_6", r'verification\s+code[:\s]*(\d{6})', 2),
            
            # ===== GERMAN (DEUTSCH) - MEDIUM PRIORITY (2) =====
            ("DE_SUBJECT_CODE_1", r"'subject':\s*'(\d{6})\s+ist\s+dein\s+Instagram-Code'", 2),
            ("DE_SUBJECT_CODE_2", r"'subject':\s*'Dein\s+Instagram-Code:?\s*(\d{6})'", 2),
            ("DE_SUBJECT_VERIF_1", r"'subject':\s*'Instagram-Bestätigungscode:\s*(\d{6})'", 2),
            ("DE_BODY_CODE_1", r'(\d{6})\s+ist\s+dein\s+Instagram-Code', 2),
            ("DE_BODY_CODE_2", r'Dein\s+Instagram-Code[:\s]*(\d{6})', 2),
            ("DE_BODY_VERIF_1", r'Bestätigungscode[:\s]*(\d{6})', 2),
            ("DE_BODY_VERIF_2", r'Verifizierungscode[:\s]*(\d{6})', 2),
            ("DE_BODY_VERIF_3", r'Gib\s+den\s+folgenden\s+Code\s+ein[:\s]*(\d{6})', 2),
            ("DE_BODY_VERIF_4", r'Instagram-Code[:\s]*(\d{6})', 2),
            ("DE_BODY_VERIF_5", r'Verwende\s+diesen\s+Code[:\s]*(\d{6})', 2),
            
            # ===== FRENCH (FRANÇAIS) - MEDIUM PRIORITY (2) =====
            ("FR_SUBJECT_CODE_1", r"'subject':\s*'(\d{6})\s+est\s+votre\s+code\s+Instagram'", 2),
            ("FR_SUBJECT_CODE_2", r"'subject':\s*'Votre\s+code\s+Instagram:?\s*(\d{6})'", 2),
            ("FR_SUBJECT_VERIF_1", r"'subject':\s*'Code\s+de\s+vérification\s+Instagram:\s*(\d{6})'", 2),
            ("FR_BODY_CODE_1", r'(\d{6})\s+est\s+votre\s+code\s+Instagram', 2),
            ("FR_BODY_CODE_2", r'Votre\s+code\s+Instagram[:\s]*(\d{6})', 2),
            ("FR_BODY_VERIF_1", r'code\s+de\s+vérification[:\s]*(\d{6})', 2),
            ("FR_BODY_VERIF_2", r'code\s+de\s+confirmation[:\s]*(\d{6})', 2),
            ("FR_BODY_VERIF_3", r'Entrez\s+le\s+code\s+suivant[:\s]*(\d{6})', 2),
            ("FR_BODY_VERIF_4", r'code\s+Instagram[:\s]*(\d{6})', 2),
            ("FR_BODY_VERIF_5", r'Utilisez\s+ce\s+code[:\s]*(\d{6})', 2),
            
            # ===== DUTCH (NEDERLANDS) - MEDIUM PRIORITY (2) =====
            ("NL_SUBJECT_CODE_1", r"'subject':\s*'(\d{6})\s+is\s+je\s+Instagram-code'", 2),
            ("NL_SUBJECT_CODE_2", r"'subject':\s*'Je\s+Instagram-code:?\s*(\d{6})'", 2),
            ("NL_BODY_CODE_1", r'(\d{6})\s+is\s+je\s+Instagram-code', 2),
            ("NL_BODY_CODE_2", r'Je\s+Instagram-code[:\s]*(\d{6})', 2),
            ("NL_BODY_VERIF_1", r'verificatiecode[:\s]*(\d{6})', 2),
            ("NL_BODY_VERIF_2", r'bevestigingscode[:\s]*(\d{6})', 2),
            ("NL_BODY_VERIF_3", r'Voer\s+de\s+volgende\s+code\s+in[:\s]*(\d{6})', 2),
            ("NL_BODY_VERIF_4", r'Gebruik\s+deze\s+code[:\s]*(\d{6})', 2),
            
            # ===== JAPANESE (日本語) - MEDIUM PRIORITY (2) =====
            ("JP_SUBJECT_CODE_1", r"'subject':\s*'(\d{6})\s*(?:は|が)Instagram(?:の)?コード(?:です)?'", 2),
            ("JP_SUBJECT_CODE_2", r"'subject':\s*'Instagram(?:の)?コード:?\s*(\d{6})'", 2),
            ("JP_BODY_CODE_1", r'(\d{6})\s*(?:は|が)Instagram(?:の)?コード', 2),
            ("JP_BODY_CODE_2", r'Instagram(?:の)?コード[:\s]*(\d{6})', 2),
            ("JP_BODY_VERIF_1", r'認証コード[:\s]*(\d{6})', 2),
            ("JP_BODY_VERIF_2", r'確認コード[:\s]*(\d{6})', 2),
            ("JP_BODY_VERIF_3", r'コードを入力[:\s]*(\d{6})', 2),
            ("JP_BODY_VERIF_4", r'このコードを使用[:\s]*(\d{6})', 2),
            
            # ===== PORTUGUESE (PORTUGUÊS) - MEDIUM PRIORITY (2) =====
            ("PT_SUBJECT_CODE_1", r"'subject':\s*'(\d{6})\s+é\s+o?\s*seu\s+código\s+(?:do\s+)?Instagram'", 2),
            ("PT_SUBJECT_CODE_2", r"'subject':\s*'Seu\s+código\s+(?:do\s+)?Instagram:?\s*(\d{6})'", 2),
            ("PT_BODY_CODE_1", r'(\d{6})\s+é\s+o?\s*seu\s+código\s+(?:do\s+)?Instagram', 2),
            ("PT_BODY_CODE_2", r'Seu\s+código\s+(?:do\s+)?Instagram[:\s]*(\d{6})', 2),
            ("PT_BODY_VERIF_1", r'código\s+de\s+verificação[:\s]*(\d{6})', 2),
            ("PT_BODY_VERIF_2", r'código\s+de\s+confirmação[:\s]*(\d{6})', 2),
            ("PT_BODY_VERIF_3", r'Insira\s+o\s+seguinte\s+código[:\s]*(\d{6})', 2),
            ("PT_BODY_VERIF_4", r'código\s+Instagram[:\s]*(\d{6})', 2),
            ("PT_BODY_VERIF_5", r'Use\s+este\s+código[:\s]*(\d{6})', 2),
            
            # ===== SPANISH (ESPAÑOL) - MEDIUM PRIORITY (2) =====
            ("ES_SUBJECT_CODE_1", r"'subject':\s*'(\d{6})\s+es\s+tu\s+código\s+de\s+Instagram'", 2),
            ("ES_SUBJECT_CODE_2", r"'subject':\s*'Tu\s+código\s+de\s+Instagram:?\s*(\d{6})'", 2),
            ("ES_BODY_CODE_1", r'(\d{6})\s+es\s+tu\s+código\s+de\s+Instagram', 2),
            ("ES_BODY_CODE_2", r'Tu\s+código\s+de\s+Instagram[:\s]*(\d{6})', 2),
            ("ES_BODY_VERIF_1", r'código\s+de\s+verificación[:\s]*(\d{6})', 2),
            ("ES_BODY_VERIF_2", r'código\s+de\s+confirmación[:\s]*(\d{6})', 2),
            ("ES_BODY_VERIF_3", r'Introduce\s+el\s+siguiente\s+código[:\s]*(\d{6})', 2),
            ("ES_BODY_VERIF_4", r'Ingresa\s+el\s+código[:\s]*(\d{6})', 2),
            ("ES_BODY_VERIF_5", r'Usa\s+este\s+código[:\s]*(\d{6})', 2),
            
            # ===== ITALIAN (ITALIANO) - MEDIUM PRIORITY (2) =====
            ("IT_SUBJECT_CODE_1", r"'subject':\s*'(\d{6})\s+è\s+il\s+tuo\s+codice\s+Instagram'", 2),
            ("IT_SUBJECT_CODE_2", r"'subject':\s*'Il\s+tuo\s+codice\s+Instagram:?\s*(\d{6})'", 2),
            ("IT_BODY_CODE_1", r'(\d{6})\s+è\s+il\s+tuo\s+codice\s+Instagram', 2),
            ("IT_BODY_CODE_2", r'Il\s+tuo\s+codice\s+Instagram[:\s]*(\d{6})', 2),
            ("IT_BODY_VERIF_1", r'codice\s+di\s+verifica[:\s]*(\d{6})', 2),
            ("IT_BODY_VERIF_2", r'codice\s+di\s+conferma[:\s]*(\d{6})', 2),
            ("IT_BODY_VERIF_3", r'Inserisci\s+il\s+seguente\s+codice[:\s]*(\d{6})', 2),
            ("IT_BODY_VERIF_4", r'codice\s+Instagram[:\s]*(\d{6})', 2),
            ("IT_BODY_VERIF_5", r'Usa\s+questo\s+codice[:\s]*(\d{6})', 2),
            
            # ===== KOREAN (한국어) - MEDIUM PRIORITY (2) =====
            ("KR_BODY_CODE_1", r'(\d{6})\s*(?:은|는)\s*Instagram\s*코드입니다', 2),
            ("KR_BODY_CODE_2", r'Instagram\s*코드[:\s]*(\d{6})', 2),
            ("KR_BODY_VERIF_1", r'인증\s*코드[:\s]*(\d{6})', 2),
            ("KR_BODY_VERIF_2", r'확인\s*코드[:\s]*(\d{6})', 2),
            ("KR_BODY_VERIF_3", r'다음\s*코드를\s*입력[:\s]*(\d{6})', 2),
            
            # ===== CHINESE (中文) - MEDIUM PRIORITY (2) =====
            ("ZH_BODY_CODE_1", r'(\d{6})\s*是(?:您的)?Instagram\s*(?:验证)?(?:代)?码', 2),
            ("ZH_BODY_CODE_2", r'(?:您的)?Instagram\s*(?:验证)?码[:\s]*(\d{6})', 2),
            ("ZH_BODY_VERIF_1", r'验证码[:\s]*(\d{6})', 2),
            ("ZH_BODY_VERIF_2", r'确认码[:\s]*(\d{6})', 2),
            ("ZH_BODY_VERIF_3", r'请输入以下代码[:\s]*(\d{6})', 2),
            
            # ===== RUSSIAN (РУССКИЙ) - MEDIUM PRIORITY (2) =====
            ("RU_BODY_CODE_1", r'(\d{6})\s*[—–-]?\s*(?:это\s+)?(?:ваш\s+)?код\s+Instagram', 2),
            ("RU_BODY_CODE_2", r'(?:Ваш\s+)?код\s+Instagram[:\s]*(\d{6})', 2),
            ("RU_BODY_VERIF_1", r'код\s+подтверждения[:\s]*(\d{6})', 2),
            ("RU_BODY_VERIF_2", r'проверочный\s+код[:\s]*(\d{6})', 2),
            ("RU_BODY_VERIF_3", r'Введите\s+следующий\s+код[:\s]*(\d{6})', 2),
            
            # ===== TURKISH (TÜRKÇE) - MEDIUM PRIORITY (2) =====
            ("TR_BODY_CODE_1", r'(\d{6})\s+Instagram\s+kodunuz', 2),
            ("TR_BODY_CODE_2", r'Instagram\s+kodunuz[:\s]*(\d{6})', 2),
            ("TR_BODY_VERIF_1", r'doğrulama\s+kodu[:\s]*(\d{6})', 2),
            ("TR_BODY_VERIF_2", r'onay\s+kodu[:\s]*(\d{6})', 2),
            ("TR_BODY_VERIF_3", r'Şu\s+kodu\s+girin[:\s]*(\d{6})', 2),
            
            # ===== ARABIC (العربية) - MEDIUM PRIORITY (2) =====
            ("AR_BODY_CODE_1", r'(\d{6})\s+هو\s+رمز\s+Instagram', 2),
            ("AR_BODY_CODE_2", r'رمز\s+Instagram[:\s]*(\d{6})', 2),
            ("AR_BODY_VERIF_1", r'رمز\s+التحقق[:\s]*(\d{6})', 2),
            ("AR_BODY_VERIF_2", r'رمز\s+التأكيد[:\s]*(\d{6})', 2),
            
            # ===== HINDI (हिन्दी) - MEDIUM PRIORITY (2) =====
            ("HI_BODY_CODE_1", r'(\d{6})\s+आपका\s+Instagram\s+कोड\s+है', 2),
            ("HI_BODY_CODE_2", r'Instagram\s+कोड[:\s]*(\d{6})', 2),
            ("HI_BODY_VERIF_1", r'सत्यापन\s+कोड[:\s]*(\d{6})', 2),
            ("HI_BODY_VERIF_2", r'पुष्टि\s+कोड[:\s]*(\d{6})', 2),
            
            # ===== THAI (ไทย) - MEDIUM PRIORITY (2) =====
            ("TH_BODY_CODE_1", r'(\d{6})\s+คือรหัส\s+Instagram\s+ของคุณ', 2),
            ("TH_BODY_CODE_2", r'รหัส\s+Instagram[:\s]*(\d{6})', 2),
            ("TH_BODY_VERIF_1", r'รหัสยืนยัน[:\s]*(\d{6})', 2),
            ("TH_BODY_VERIF_2", r'รหัสตรวจสอบ[:\s]*(\d{6})', 2),
            
            # ===== VIETNAMESE (TIẾNG VIỆT) - MEDIUM PRIORITY (2) =====
            ("VI_BODY_CODE_1", r'(\d{6})\s+là\s+mã\s+Instagram\s+của\s+bạn', 2),
            ("VI_BODY_CODE_2", r'Mã\s+Instagram\s+của\s+bạn[:\s]*(\d{6})', 2),
            ("VI_BODY_VERIF_1", r'mã\s+xác\s+minh[:\s]*(\d{6})', 2),
            ("VI_BODY_VERIF_2", r'mã\s+xác\s+nhận[:\s]*(\d{6})', 2),
            
            # ===== POLISH (POLSKI) - MEDIUM PRIORITY (2) =====
            ("PL_BODY_CODE_1", r'(\d{6})\s+to\s+Twój\s+kod\s+Instagram', 2),
            ("PL_BODY_CODE_2", r'Twój\s+kod\s+Instagram[:\s]*(\d{6})', 2),
            ("PL_BODY_VERIF_1", r'kod\s+weryfikacyjny[:\s]*(\d{6})', 2),
            ("PL_BODY_VERIF_2", r'kod\s+potwierdzający[:\s]*(\d{6})', 2),
            
            # ===== MALAY (BAHASA MELAYU) - MEDIUM PRIORITY (2) =====
            ("MS_BODY_CODE_1", r'(\d{6})\s+adalah\s+kod\s+Instagram\s+anda', 2),
            ("MS_BODY_CODE_2", r'Kod\s+Instagram\s+anda[:\s]*(\d{6})', 2),
            ("MS_BODY_VERIF_1", r'kod\s+pengesahan[:\s]*(\d{6})', 2),
            ("MS_BODY_VERIF_2", r'kod\s+verifikasi[:\s]*(\d{6})', 2),
            
            # ===== SWEDISH (SVENSKA) - MEDIUM PRIORITY (2) =====
            ("SV_BODY_CODE_1", r'(\d{6})\s+är\s+din\s+Instagram-kod', 2),
            ("SV_BODY_CODE_2", r'Din\s+Instagram-kod[:\s]*(\d{6})', 2),
            ("SV_BODY_VERIF_1", r'verifieringskod[:\s]*(\d{6})', 2),
            
            # ===== NORWEGIAN (NORSK) - MEDIUM PRIORITY (2) =====
            ("NO_BODY_CODE_1", r'(\d{6})\s+er\s+Instagram-koden\s+din', 2),
            ("NO_BODY_CODE_2", r'Instagram-koden\s+din[:\s]*(\d{6})', 2),
            ("NO_BODY_VERIF_1", r'bekreftelseskode[:\s]*(\d{6})', 2),
            
            # ===== DANISH (DANSK) - MEDIUM PRIORITY (2) =====
            ("DA_BODY_CODE_1", r'(\d{6})\s+er\s+din\s+Instagram-kode', 2),
            ("DA_BODY_CODE_2", r'Din\s+Instagram-kode[:\s]*(\d{6})', 2),
            ("DA_BODY_VERIF_1", r'bekræftelseskode[:\s]*(\d{6})', 2),
            
            # ===== FINNISH (SUOMI) - MEDIUM PRIORITY (2) =====
            ("FI_BODY_CODE_1", r'(\d{6})\s+on\s+Instagram-koodisi', 2),
            ("FI_BODY_CODE_2", r'Instagram-koodisi[:\s]*(\d{6})', 2),
            ("FI_BODY_VERIF_1", r'vahvistuskoodi[:\s]*(\d{6})', 2),
            
            # ===== GREEK (ΕΛΛΗΝΙΚΑ) - MEDIUM PRIORITY (2) =====
            ("EL_BODY_CODE_1", r'(\d{6})\s+είναι\s+ο\s+κωδικός\s+Instagram\s+σας', 2),
            ("EL_BODY_CODE_2", r'κωδικός\s+Instagram[:\s]*(\d{6})', 2),
            ("EL_BODY_VERIF_1", r'κωδικός\s+επαλήθευσης[:\s]*(\d{6})', 2),
            
            # ===== CZECH (ČEŠTINA) - MEDIUM PRIORITY (2) =====
            ("CS_BODY_CODE_1", r'(\d{6})\s+je\s+váš\s+kód\s+Instagram', 2),
            ("CS_BODY_CODE_2", r'Váš\s+kód\s+Instagram[:\s]*(\d{6})', 2),
            ("CS_BODY_VERIF_1", r'ověřovací\s+kód[:\s]*(\d{6})', 2),
            
            # ===== ROMANIAN (ROMÂNĂ) - MEDIUM PRIORITY (2) =====
            ("RO_BODY_CODE_1", r'(\d{6})\s+este\s+codul\s+tău\s+Instagram', 2),
            ("RO_BODY_CODE_2", r'Codul\s+tău\s+Instagram[:\s]*(\d{6})', 2),
            ("RO_BODY_VERIF_1", r'cod\s+de\s+verificare[:\s]*(\d{6})', 2),
            
            # ===== HUNGARIAN (MAGYAR) - MEDIUM PRIORITY (2) =====
            ("HU_BODY_CODE_1", r'(\d{6})\s+az\s+Instagram-kódod', 2),
            ("HU_BODY_CODE_2", r'Instagram-kódod[:\s]*(\d{6})', 2),
            ("HU_BODY_VERIF_1", r'megerősítő\s+kód[:\s]*(\d{6})', 2),
            
            # ===== GENERAL PATTERNS - LOW PRIORITY (1) =====
            ("GEN_6DIGIT", r'\b(\d{6})\b', 1),
        ]
        
        return patterns
    
    def _init_session(self) -> bool:
        """Initialize session seperti kode berhasil Anda"""
        # print(f"{cyan}      Initializing 10minutemail session...{reset}")
        
        for attempt in range(1, 4):
            try:
                r = self.session.get(
                    "https://10minutemail.net",
                    timeout=20,
                    verify=False
                )
                if r.status_code == 200:
                    # print(f"{hijau}      Session initialized (attempt {attempt}){reset}")
                    return True
            except Exception as e:
                print(f"{kuning}      Session init attempt {attempt} failed: {e}{reset}")
            
            if attempt < 3:
                time.sleep(1)
        
        print(f"{merah}      Failed to initialize session after 3 attempts{reset}")
        return False
    
    async def get_email(self) -> Optional[Dict[str, Any]]:
        """Get email - IMPLEMENTASI PERSIS KODE BERHASIL ANDA"""
        try:
            # print(f"{cyan}      Getting 10minutemail.net...{reset}")
            
            # ⭐ INIT SESSION DULU
            if not self._init_session():
                print(f"{merah}      Failed to initialize session{reset}")
                return None
            
            # ⭐ GUNAKAN LOGIC PERSIS KODE BERHASIL ANDA
            for attempt in range(1, 6):  # 5 attempts seperti kode berhasil
                waktu = int(time.time() * 1000)
                url = f"{self.api_endpoint}?new=1&_={waktu}"
                
                # print(f"{cyan}      Attempt {attempt}/5: {url}{reset}")
                
                try:
                    resp = self.session.get(url, timeout=20, verify=False)
                    resp.raise_for_status()
                    
                    data = resp.json()
                    email = data.get("mail_get_mail")
                    
                    if email:
                        self.current_email = email
                        self.last_check_time = time.time()
                        self.checks_count = 0
                        
                        print(f"{hijau}✅ Got email: {email}{reset}")
                        
                        return {
                            "email": email,
                            "username": email.split('@')[0],
                            "domain": "10minutemail.net",
                            "service": "10minutemail",
                            "created_at": time.time(),
                            "session_data": {
                                "session": self.session,
                                "timestamp": waktu,
                                "session_initialized": True
                            }
                        }
                    else:
                        print(f"{kuning}      No email in response{reset}")
                    
                except Exception as e:
                    print(f"{merah}      Attempt {attempt} failed: {e}{reset}")
                
                if attempt < 5:
                    wait_time = random.uniform(2, 4)
                    print(f"{cyan}      Waiting {wait_time:.1f}s before retry...{reset}")
                    await asyncio.sleep(wait_time)
            
            print(f"{merah}      Failed to get email after 5 attempts{reset}")
            return None
            
        except Exception as e:
            print(f"{merah}      Error getting 10minutemail: {e}{reset}")
            return None
    
    def _is_valid_otp(self, code: str) -> bool:
        """Validasi apakah ini benar OTP (bukan angka lain)"""
        if not code or len(code) != 6:
            return False
        
        # Cek hanya digit
        if not code.isdigit():
            return False
        
        # Cek bukan tahun
        if code.startswith('19') or code.startswith('20') or code.startswith('202'):
            return False
        
        # Cek bukan angka sequential
        sequential_patterns = [
            '123456', '234567', '345678', '456789', '567890',
            '654321', '543210', '432109', '321098', '210987',
            '012345', '123450'
        ]
        if code in sequential_patterns:
            return False
        
        # Cek bukan angka repeating
        if len(set(code)) == 1:  # Semua angka sama
            return False
        
        # Cek bukan angka dengan banyak 0
        if code.count('0') >= 4:
            return False
        
        # Cek bukan pattern mudah ditebak
        if code in ['111111', '222222', '333333', '444444', '555555',
                   '666666', '777777', '888888', '999999', '000000']:
            return False
        
        return True
    
    def _extract_otp_from_data(self, data_str: str) -> Optional[Tuple[str, str]]:
        """Extract OTP dari data string, return (otp, pattern_name)"""
        found_matches = []
        
        for pattern_name, pattern, priority in self.otp_patterns:
            try:
                matches = re.finditer(pattern, data_str, re.IGNORECASE)
                for match in matches:
                    if match.groups():
                        otp_candidate = match.group(1)
                        
                        # Validasi OTP
                        if self._is_valid_otp(otp_candidate):
                            found_matches.append({
                                'otp': otp_candidate,
                                'pattern': pattern_name,
                                'priority': priority,
                                'match_text': match.group(0)[:50]  # Untuk debug
                            })
                            
                            # Jika pattern Indonesian high priority, langsung return
                            if priority == 3 and pattern_name.startswith("ID_"):
                                print(f"{cyan}      🎯 High priority Indonesian pattern matched: {pattern_name}{reset}")
                                return otp_candidate, pattern_name
            except Exception as e:
                continue
        
        if found_matches:
            # Sort by priority (highest first)
            found_matches.sort(key=lambda x: x['priority'], reverse=True)
            best_match = found_matches[0]
            
            # Debug info
            print(f"{cyan}      📊 Pattern matched: {best_match['pattern']} (priority: {best_match['priority']}){reset}")
            print(f"{cyan}      📝 Match text: {best_match['match_text']}...{reset}")
            
            return best_match['otp'], best_match['pattern']
        
        return None, None
    
    async def get_otp(self, email_address: str, email_data: Dict[str, Any]) -> Optional[str]:
        """Get OTP - MAKSIMAL 30 DETIK SAJA, lebih cepat"""
        try:
            print(f"{cyan}      🔍 Checking for OTP (30 seconds max)...{reset}")
            
            # Reset counter
            self.checks_count = 0
            start_time = time.time()
            max_wait_time = 30  # ⭐ MAKSIMAL 30 DETIK SAJA
            
            # Optimasi interval pengecekan
            check_intervals = [1.5, 2, 2, 2, 2, 2.5, 2.5, 3, 3, 3]  # Lebih cepat di awal
            
            # Max 30 detik, check dengan interval yang optimal
            while time.time() - start_time < max_wait_time:
                self.checks_count += 1
                elapsed = time.time() - start_time
                
                # Pilih interval berdasarkan jumlah check
                if self.checks_count <= len(check_intervals):
                    next_interval = check_intervals[self.checks_count - 1]
                else:
                    next_interval = 3  # Default untuk check selanjutnya
                
                # Generate timestamp untuk avoid cache
                waktu = int(time.time() * 1000)
                url = f"{self.api_endpoint}?_={waktu}"
                
                # print(f"{cyan}      🔄 Check #{self.checks_count} ({elapsed:.1f}s/{max_wait_time}s): {url}{reset}")
                
                try:
                    resp = self.session.get(url, timeout=10, verify=False)  # Timeout lebih pendek
                    
                    if resp.status_code != 200:
                        print(f"{merah}      ❌ HTTP {resp.status_code}{reset}")
                        await asyncio.sleep(next_interval)
                        continue
                    
                    data = resp.json()
                    data_str = str(data)
                    
                    # Cek apakah ada keyword Instagram - versi lebih cepat
                    instagram_keywords = ['Instagram', 'instagram', 'kode', 'code', 'verifikasi', 'verification']
                    found_instagram = False
                    otp_found = None  # ⭐ INISIALISASI VARIABLE OTP
                    
                    # ⭐ OPTIMASI: Cek cepat dengan lower case
                    lower_data = data_str.lower()
                    for keyword in instagram_keywords:
                        if keyword.lower() in lower_data:
                            # print(f"{hijau}      ✅ Instagram email detected!{reset}")
                            found_instagram = True
                            
                            # Extract OTP
                            otp, pattern_name = self._extract_otp_from_data(data_str)
                            
                            if otp:
                                print(f"{hijau}      🎉 OTP FOUND: {otp} (via {pattern_name}) in {elapsed:.1f}s{reset}")
                                return otp
                            else:
                                print(f"{kuning}      ⚠️  Instagram email found but no valid OTP{reset}")
                            break
                    
                    # Jika tidak ada Instagram, cek apakah ada 6-digit number saja
                    # ⭐ OPTIMASI: Cepat-cepat cari 6 digit
                    if not found_instagram:  # Hanya cek jika belum ada Instagram
                        # Fallback: cari 6-digit number dengan regex cepat
                        import re
                        six_digit_match = re.search(r'\b(\d{6})\b', data_str)
                        if six_digit_match:
                            otp_candidate = six_digit_match.group(1)
                            if self._is_valid_otp(otp_candidate):
                                print(f"{hijau}      🎉 OTP FOUND (fallback): {otp_candidate} in {elapsed:.1f}s{reset}")
                                return otp_candidate
                
                except json.JSONDecodeError:
                    print(f"{merah}      ❌ Invalid JSON response{reset}")
                except Exception as e:
                    print(f"{merah}      ❌ Request error: {str(e)[:50]}...{reset}")
                
                # Hitung waktu tersisa
                time_left = max_wait_time - (time.time() - start_time)
                
                # Jika waktu hampir habis, selesaikan
                if time_left <= 0:
                    break
                
                # Tunggu sebelum check berikutnya
                wait_time = min(next_interval, time_left)  # Jangan tunggu lebih lama dari waktu tersisa
                if wait_time > 0:
                    # print(f"{cyan}      ⏳ Next check in {wait_time:.1f}s...{reset}")
                    await asyncio.sleep(wait_time)
                else:
                    break
            
            total_time = time.time() - start_time
            print(f"{merah}      ❌ No OTP found after {self.checks_count} checks ({total_time:.1f} seconds){reset}")
            return None
            
        except Exception as e:
            print(f"{merah}      ❌ Error in get_otp: {e}{reset}")
            import traceback
            traceback.print_exc()
            return None
    
    async def verify_email(self, email_address: str, email_data: Dict[str, Any]) -> bool:
        """Simple verification - check if session still works"""
        try:
            # Coba buat request kecil
            waktu = int(time.time() * 1000)
            url = f"{self.api_endpoint}?_={waktu}"
            
            resp = self.session.get(url, timeout=10, verify=False)
            return resp.status_code == 200
            
        except Exception:
            return False
    
    def cleanup(self):
        """Cleanup session"""
        try:
            self.session.close()
            print(f"{cyan}      🧹 10minutemail session cleaned up{reset}")
        except Exception as e:
            print(f"{merah}      ❌ Error cleaning up session: {e}{reset}")


class CmailService2025:
    """Cmail.ai service wrapper 2025"""
    
    def __init__(self):
        self.api_base = "https://cmail.ai"
        self.available_domains = ["vintomaper.com", "tovinit.com", "mentonit.net"]
        self.session = requests.Session()
    
    async def get_email(self) -> Optional[Dict[str, Any]]:
        """Get email from Cmail.ai"""
        try:
            # Generate random username
            username = random_string(8)
            domain = random.choice(self.available_domains)
            email = f"{username}@{domain}"
            
            # Verify email is available
            check_url = f"{self.api_base}/api/emails?inbox={email}"
            check_resp = self.session.get(check_url, timeout=30)
            
            if check_resp.status_code == 200:
                return {
                    "email": email,
                    "username": username,
                    "domain": domain,
                    "service": "cmail",
                    "inbox_url": f"{self.api_base}/inbox/{email}"
                }
            
            return None
            
        except Exception as e:
            print(f"{merah}❌  Cmail.ai error: {e}{reset}")
            return None
    
    async def get_otp(self, email_address: str, email_data: Dict[str, Any]) -> Optional[str]:
        """Get OTP from Cmail.ai"""
        try:
            inbox_url = email_data.get("inbox_url", 
                                     f"{self.api_base}/inbox/{email_address}")
            
            # Get messages
            resp = self.session.get(inbox_url, timeout=30)
            if resp.status_code == 200:
                # Parse HTML untuk OTP
                from bs4 import BeautifulSoup
                
                soup = BeautifulSoup(resp.text, 'html.parser')
                
                # Cari OTP dalam text
                text_content = soup.get_text()
                otp = self._extract_otp(text_content)
                
                if otp:
                    return otp
            
            return None
            
        except Exception as e:
            print(f"{merah}❌  Cmail.ai OTP error: {e}{reset}")
            return None
    
    def _extract_otp(self, text: str) -> Optional[str]:
        """Extract OTP from text"""
        if not text:
            return None
        
        text = text.replace('\n', ' ').replace('\r', ' ')
        
        patterns = [
            r'(\d{6})\s*(?:is|are|adalah)\s*(?:your|kode)?\s*instagram\s*(?:code|kode)',
            r'instagram\s*(?:code|kode)\s*(?:is|:)?\s*(\d{6})',
            r'kode\s*instagram\s*(?:anda|you)?\s*(?:is|:)?\s*(\d{6})',
            r'enter\s*(?:this|the)?\s*code\s*(?:is|:)?\s*(\d{6})',
            r'masukkan\s*kode\s*(?:is|:)?\s*(\d{6})',
            r'verification\s*code\s*(?:is|:)?\s*(\d{6})',
            r'kode\s*verifikasi\s*(?:is|:)?\s*(\d{6})',
            r'\b(\d{6})\b'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                otp = match.group(1)
                if otp.isdigit() and len(otp) == 6:
                    return otp
        
        return None
    
    async def verify_email(self, email_address: str, email_data: Dict[str, Any]) -> bool:
        """Verify Cmail.ai email"""
        try:
            check_url = f"{self.api_base}/api/emails?inbox={email_address}"
            resp = self.session.get(check_url, timeout=30)
            return resp.status_code == 200
        except Exception:
            return False


class AdvancedSessionManager2025:
    """Advanced session management dengan state persistence dan recovery"""
    
    def __init__(self):
        self.sessions = {}
        self.session_states = {}
        self.session_counter = 0
        self.max_sessions = 1000
        self.session_timeout = 3600  # 1 hour
        self.cleanup_interval = 300  # 5 minutes
        self._last_cleanup = time.time()
        self.cookie_jar = {}
        
    def create_session(self, fingerprint: Dict[str, Any], 
                      behavior_profile: Dict[str, Any],
                      ip_config: Dict[str, Any],
                      webrtc_fingerprint: Optional[Dict[str, Any]] = None) -> str:
        """Create new session dengan semua ID yang konsisten"""
        session_id = f"sess_{self.session_counter:08d}_{int(time.time())}"
        self.session_counter += 1
        
        # **GENERATE ID YANG KONSISTEN**
        device_id = self._generate_consistent_device_id()
        extra_session_id = self._generate_extra_session_id()
        guid = str(uuid.uuid4())
        
        # Build complete headers - minimal and consistent
        complete_headers = self._build_complete_headers(
            fingerprint, behavior_profile, ip_config, webrtc_fingerprint
        )
        
        session_data = {
            "session_id": session_id,
            "created_at": time.time(),
            "last_activity": time.time(),
            "last_ip_change": time.time(),
            "fingerprint": fingerprint,
            "behavior_profile": behavior_profile,
            "ip_config": ip_config,
            "webrtc_fingerprint": webrtc_fingerprint or {},
            
            # **ID YANG KONSISTEN**
            "device_id": device_id,
            "extra_session_id": extra_session_id,
            "guid": guid,
            "uuid": str(uuid.uuid4()),
            
            "request_count": 0,
            "success_count": 0,
            "failure_count": 0,
            "state": "active",
            "sequence_number": 0,
            "tokens": {},
            "cookies": {},
            "headers": complete_headers,
            "current_headers": complete_headers,
            "metadata": {
                "user_agent": fingerprint.get("browser", {}).get("user_agent", ""),
                "device_type": fingerprint.get("device_type", "desktop"),
                "location": fingerprint.get("location", {}).get("city", "Jakarta"),
                "isp": ip_config.get("isp_info", {}).get("isp", "telkomsel"),
                "connection_type": ip_config.get("connection_type", "wifi")
            }
        }
        
        # Store session
        self.sessions[session_id] = session_data
        self.session_states[session_id] = {
            "current_page": None,
            "form_data": {},
            "navigation_history": [],
            "interaction_log": [],
            "error_log": [],
            "cookie_jar": {},  # FIXED: session-specific cookie jar
            "performance_metrics": {
                "avg_response_time": 0,
                "success_rate": 1.0,
                "consecutive_errors": 0,
                "rate_limit_hits": 0,
                "ip_rotations": 0
            }
        }
        
        # Initialize cookie jar
        self.cookie_jar[session_id] = {}
        
        # Auto-cleanup
        if len(self.sessions) > self.max_sessions:
            self._cleanup_old_sessions()
        
        return session_id

    def _generate_consistent_device_id(self) -> str:
        """Generate device ID yang konsisten (35 chars)"""
        # Format: 35 karakter alfanumerik seperti Instagram
        chars = string.ascii_lowercase + string.digits
        return ''.join(random.choice(chars) for _ in range(35))
    
    def _generate_extra_session_id(self) -> str:
        """Generate extra session ID seperti Instagram asli"""
        parts = [
            ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(6)),
            ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(6)),
            ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(6))
        ]
        return ':'.join(parts)

    def _build_complete_headers(self, fingerprint: Dict[str, Any], 
                              behavior_profile: Dict[str, Any],
                              ip_config: Dict[str, Any],
                              webrtc_fingerprint: Optional[Dict[str, Any]] = None) -> Dict[str, str]:
        """Build complete headers that are consistent and realistic for the session.
        
        Headers are kept minimal to avoid detection while maintaining
        consistency across all requests in the session.
        Uses Desktop/Web browser fingerprint for Web API compatibility.
        """
        # Extract browser info from fingerprint
        browser = fingerprint.get("browser", {}) if fingerprint else {}
        
        # Generate fresh, realistic Chrome version (131-136 are current as of late 2024)
        chrome_major = random.choice([131, 132, 133, 134, 135, 136])
        chrome_minor = 0
        chrome_build = random.randint(6778, 6998)
        chrome_patch = random.randint(0, 250)
        chrome_full = f"{chrome_major}.{chrome_minor}.{chrome_build}.{chrome_patch}"
        
        # Desktop platforms for Web API - Windows or macOS
        platform_choice = random.choice(["Windows", "macOS"])
        
        if platform_choice == "Windows":
            # Windows 10/11 User-Agent
            windows_versions = ["10.0", "11.0"]
            windows_version = random.choice(windows_versions)
            user_agent = f"Mozilla/5.0 (Windows NT {windows_version}; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{chrome_full} Safari/537.36"
            platform_header = '"Windows"'
            platform_version = f'"{windows_version}.0"'
        else:
            # macOS User-Agent (MacBook)
            macos_versions = ["10_15_7", "13_0", "14_0", "14_5"]
            macos_version = random.choice(macos_versions)
            user_agent = f"Mozilla/5.0 (Macintosh; Intel Mac OS X {macos_version}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{chrome_full} Safari/537.36"
            platform_header = '"macOS"'
            platform_version = f'"{macos_version.replace("_", ".")}"'
        
        # Build realistic browser headers matching exact Chrome order for Desktop
        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
            "Cache-Control": "max-age=0",
            "Connection": "keep-alive",
            "Host": "www.instagram.com",
            "Sec-Ch-Ua": f'"Chromium";v="{chrome_major}", "Google Chrome";v="{chrome_major}", "Not-A.Brand";v="24"',
            "Sec-Ch-Ua-Full-Version-List": f'"Chromium";v="{chrome_full}", "Google Chrome";v="{chrome_full}", "Not-A.Brand";v="24.0.0.0"',
            "Sec-Ch-Ua-Mobile": "?0",  # Desktop = not mobile
            "Sec-Ch-Ua-Platform": platform_header,
            "Sec-Ch-Ua-Platform-Version": platform_version,
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-User": "?1",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": user_agent,
        }
        
        return headers

    def get_session_with_headers(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Get session dengan headers yang sudah sinkron - FIXED"""
        if session_id not in self.sessions:
            return None
        
        session = self.sessions[session_id]
        
        # Check timeout
        if time.time() - session["last_activity"] > self.session_timeout:
            session["state"] = "expired"
            return None
        
        # Update last activity
        session["last_activity"] = time.time()
        
        # Update current headers dengan cookies terkini - FIXED
        current_headers = session.get("current_headers", {}).copy()
        
        # Add current cookies to headers
        cookies = self.get_session_cookies(session_id)
        if cookies:
            cookie_str = "; ".join([f"{k}={v}" for k, v in cookies.items()])
            current_headers["Cookie"] = cookie_str
        
        session["current_headers"] = current_headers
        
        return session

    def get_session_cookies(self, session_id: str, domain: str = None) -> Dict[str, str]:
        """Get cookies untuk session - FIXED"""
        if session_id not in self.cookie_jar:
            return {}
        
        if domain:
            # Cari cookies untuk domain tertentu
            cookies = {}
            for cookie_name, cookie_value in self.cookie_jar[session_id].items():
                # Simple domain matching
                if domain in cookie_name.lower() or "instagram" in cookie_name.lower():
                    cookies[cookie_name] = cookie_value
            return cookies
        
        return self.cookie_jar[session_id].copy()

    def rotate_session_identity(self, session_id: str, 
                              new_ip_config: Dict[str, Any],
                              new_fingerprint: Dict[str, Any],
                              new_webrtc_fingerprint: Dict[str, Any]) -> bool:
        """Rotate semua identitas session sekaligus - FIXED"""
        if session_id not in self.sessions:
            return False
        
        session = self.sessions[session_id]
        
        # Update semua komponen
        updates = {
            "ip_config": new_ip_config,
            "fingerprint": new_fingerprint,
            "webrtc_fingerprint": new_webrtc_fingerprint,
            "last_ip_change": time.time(),
            "headers": self._build_complete_headers(
                new_fingerprint, 
                session.get("behavior_profile", {}),
                new_ip_config,
                new_webrtc_fingerprint
            ),
            "cookies": {},  # Reset cookies karena identity baru
            "tokens": {},   # Reset tokens
            "sequence_number": session.get("sequence_number", 0) + 1,
            "rotation_count": session.get("rotation_count", 0) + 1
        }
        
        # Update metadata
        updates["metadata"] = {
            **session.get("metadata", {}),
            "isp": new_ip_config.get("isp_info", {}).get("isp", "telkomsel"),
            "connection_type": new_ip_config.get("connection_type", "mobile"),
            "user_agent": new_fingerprint.get("browser", {}).get("user_agent", "")
        }
        
        # Apply updates
        self.update_session(session_id, updates)
        
        # Clear cookie jar untuk session ini
        if session_id in self.cookie_jar:
            self.cookie_jar[session_id] = {}
        
        # Update session state
        if session_id in self.session_states:
            self.session_states[session_id]["performance_metrics"]["ip_rotations"] = \
                self.session_states[session_id]["performance_metrics"].get("ip_rotations", 0) + 1
            
            self.session_states[session_id]["interaction_log"].append({
                "timestamp": time.time(),
                "type": "identity_rotation",
                "new_ip": new_ip_config.get("ip", "unknown"),
                "new_isp": new_ip_config.get("isp_info", {}).get("isp", "unknown")
            })
        
        return True
    
    def get_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Get session data"""
        if session_id not in self.sessions:
            return None
        
        session = self.sessions[session_id]
        
        # Check timeout
        if time.time() - session["last_activity"] > self.session_timeout:
            session["state"] = "expired"
            return None
        
        # Update last activity
        session["last_activity"] = time.time()
        
        return session

    def update_session_cookies(self, session_id: str, new_cookies: Dict[str, str], 
                             domain: str = "instagram.com"):
        """Update cookies dengan domain management - FIXED"""
        if session_id not in self.sessions:
            return
        
        # Initialize cookie jar jika belum ada
        if session_id not in self.cookie_jar:
            self.cookie_jar[session_id] = {}
        
        # Update global cookie jar
        self.cookie_jar[session_id].update(new_cookies)
        
        # Update session cookies
        current_cookies = self.sessions[session_id].get("cookies", {})
        current_cookies.update(new_cookies)
        self.sessions[session_id]["cookies"] = current_cookies
        
        # Update session state cookie jar
        if session_id in self.session_states:
            if "cookie_jar" not in self.session_states[session_id]:
                self.session_states[session_id]["cookie_jar"] = {}
            self.session_states[session_id]["cookie_jar"][domain] = new_cookies
        
        # Log cookie update
        if session_id in self.session_states:
            self.session_states[session_id]["interaction_log"].append({
                "timestamp": time.time(),
                "type": "cookie_update",
                "cookies": list(new_cookies.keys()),
                "domain": domain
            })
    
    def update_session(self, session_id: str, updates: Dict[str, Any]):
        """Update session data"""
        if session_id not in self.sessions:
            return
        
        session = self.sessions[session_id]
        
        # Apply updates
        for key, value in updates.items():
            if key in ["request_count", "success_count", "failure_count"]:
                session[key] += value
            elif key == "state":
                session[key] = value
            elif key == "tokens":
                session[key].update(value)
            elif key == "cookies":
                session[key].update(value)
            elif key == "headers":
                session[key].update(value)
            elif key == "sequence_number":
                session[key] = value
            else:
                if key not in session:
                    session[key] = value
        
        # Update last activity
        session["last_activity"] = time.time()
        
        # Update performance metrics
        total_requests = session["request_count"]
        if total_requests > 0:
            success_rate = session["success_count"] / total_requests
            session["metadata"]["success_rate"] = success_rate
            
            if "performance_metrics" in session:
                session["performance_metrics"]["success_rate"] = success_rate
    
    def update_session_state(self, session_id: str, state_updates: Dict[str, Any]):
        """Update session state"""
        if session_id not in self.session_states:
            return
        
        state = self.session_states[session_id]
        
        for key, value in state_updates.items():
            if key == "current_page":
                state[key] = value
                # Add to navigation history
                if value and (not state["navigation_history"] or state["navigation_history"][-1] != value):
                    state["navigation_history"].append(value)
                    if len(state["navigation_history"]) > 20:
                        state["navigation_history"] = state["navigation_history"][-20:]
            
            elif key == "form_data":
                state[key].update(value)
            
            elif key == "interaction_log":
                state[key].append({
                    "timestamp": time.time(),
                    "interaction": value
                })
                if len(state["interaction_log"]) > 100:
                    state["interaction_log"] = state["interaction_log"][-100:]
            
            elif key == "error_log":
                state[key].append({
                    "timestamp": time.time(),
                    "error": value
                })
                if len(state["error_log"]) > 50:
                    state["error_log"] = state["error_log"][-50:]
                
                # Update consecutive errors
                if "performance_metrics" in state:
                    state["performance_metrics"]["consecutive_errors"] += 1
            
            elif key == "performance_metrics":
                if "avg_response_time" in value:
                    old_avg = state["performance_metrics"]["avg_response_time"]
                    new_response = value["avg_response_time"]
                    # Moving average
                    state["performance_metrics"]["avg_response_time"] = 0.7 * old_avg + 0.3 * new_response
                
                if "success_rate" in value:
                    state["performance_metrics"]["success_rate"] = value["success_rate"]
                
                if "consecutive_errors" in value:
                    state["performance_metrics"]["consecutive_errors"] = value["consecutive_errors"]
            
            else:
                state[key] = value
    
    def get_session_state(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Get session state"""
        return self.session_states.get(session_id)
    
    def record_request(self, session_id: str, request_data: Dict[str, Any]):
        """Record request dengan cookie tracking - FIXED"""
        if session_id not in self.sessions:
            return
        
        session = self.sessions[session_id]
        session["request_count"] += 1
        
        # Update session state
        if session_id in self.session_states:
            state = self.session_states[session_id]
            
            # Track cookies in request
            cookies_used = request_data.get("cookies", {})
            if cookies_used:
                state["interaction_log"].append({
                    "timestamp": time.time(),
                    "type": "request_with_cookies",
                    "method": request_data.get("method", "GET"),
                    "url": request_data.get("url", ""),
                    "cookies_count": len(cookies_used),
                    "cookie_names": list(cookies_used.keys())[:3]  # Log first 3
                })
            else:
                state["interaction_log"].append({
                    "timestamp": time.time(),
                    "type": "request",
                    "method": request_data.get("method", "GET"),
                    "url": request_data.get("url", ""),
                    "status": request_data.get("status"),
                    "response_time": request_data.get("response_time", 0)
                })
            
            if len(state["interaction_log"]) > 100:
                state["interaction_log"] = state["interaction_log"][-100:]
    
    def record_response(self, session_id: str, response_data: Dict[str, Any]):
        """Record response data"""
        if session_id not in self.sessions:
            return
        
        session = self.sessions[session_id]
        
        status = response_data.get("status")
        if status and 200 <= status < 300:
            session["success_count"] += 1
            
            # Reset consecutive errors
            if session_id in self.session_states:
                state = self.session_states[session_id]
                if "performance_metrics" in state:
                    state["performance_metrics"]["consecutive_errors"] = 0
        else:
            session["failure_count"] += 1
        
        # Update performance metrics
        response_time = response_data.get("response_time", 0)
        if session_id in self.session_states:
            state = self.session_states[session_id]
            if "performance_metrics" in state:
                old_avg = state["performance_metrics"]["avg_response_time"]
                if old_avg == 0:
                    state["performance_metrics"]["avg_response_time"] = response_time
                else:
                    state["performance_metrics"]["avg_response_time"] = 0.9 * old_avg + 0.1 * response_time
    
    def get_session_health(self, session_id: str) -> Dict[str, Any]:
        """Get session health metrics"""
        if session_id not in self.sessions:
            return {"status": "not_found", "health_score": 0}
        
        session = self.sessions[session_id]
        state = self.session_states.get(session_id, {})
        
        # Calculate health score
        health_score = 1.0
        
        # Check request success rate
        total_requests = session["request_count"]
        if total_requests > 0:
            success_rate = session["success_count"] / total_requests
            health_score *= success_rate
        else:
            success_rate = 1.0
        
        # Check consecutive errors
        if "performance_metrics" in state:
            consecutive_errors = state["performance_metrics"]["consecutive_errors"]
            if consecutive_errors > 3:
                health_score *= 0.5
            elif consecutive_errors > 5:
                health_score *= 0.2
        
        # Check session age
        session_age = time.time() - session["created_at"]
        if session_age > 1800:  # 30 minutes
            # Older sessions get slight penalty
            health_score *= 0.9
        
        # Check activity recency
        last_activity = time.time() - session["last_activity"]
        if last_activity > 300:  # 5 minutes inactive
            health_score *= 0.8
        
        # Check request pattern
        if total_requests > 10:
            # Check for automation patterns
            if "interaction_log" in state:
                log = state["interaction_log"]
                if len(log) >= 3:
                    # Check timing patterns
                    timings = []
                    for i in range(len(log) - 1):
                        if "timestamp" in log[i] and "timestamp" in log[i + 1]:
                            timings.append(log[i + 1]["timestamp"] - log[i]["timestamp"])
                    
                    if timings:
                        # Check for perfect timing (automation)
                        variance = np.var(timings) if len(timings) > 1 else 0
                        if variance < 0.01:  # Too consistent
                            health_score *= 0.3
        
        # Determine status
        if health_score >= 0.8:
            status = "healthy"
        elif health_score >= 0.5:
            status = "warning"
        elif health_score >= 0.3:
            status = "critical"
        else:
            status = "failed"
        
        return {
            "session_id": session_id,
            "status": status,
            "health_score": round(health_score, 3),
            "metrics": {
                "total_requests": total_requests,
                "success_rate": success_rate,
                "session_age": session_age,
                "last_activity": last_activity,
                "consecutive_errors": state.get("performance_metrics", {}).get("consecutive_errors", 0)
            },
            "recommendation": self._get_session_recommendation(health_score, session, state)
        }
    
    def _get_session_recommendation(self, health_score: float, 
                                  session: Dict[str, Any], 
                                  state: Dict[str, Any]) -> str:
        """Get recommendation for session"""
        if health_score >= 0.8:
            return "Continue using this session"
        elif health_score >= 0.6:
            return "Consider slowing down requests"
        elif health_score >= 0.4:
            return "Rotate IP or change behavior"
        else:
            return "Create new session"
    
    def rotate_session(self, session_id: str) -> Optional[str]:
        """Rotate session (create new one with similar profile)"""
        if session_id not in self.sessions:
            return None
        
        old_session = self.sessions[session_id]
        
        # Create new session with similar profile
        new_session_id = self.create_session(
            fingerprint=old_session["fingerprint"],
            behavior_profile=old_session["behavior_profile"],
            ip_config=old_session["ip_config"]
        )
        
        # Copy relevant data
        new_session = self.sessions[new_session_id]
        new_session["sequence_number"] = old_session["sequence_number"]
        
        # Mark old session as rotated
        old_session["state"] = "rotated"
        old_session["rotated_to"] = new_session_id
        
        return new_session_id
    
    def save_session_to_file(self, session_id: str, filepath: str):
        """Save session to file"""
        if session_id not in self.sessions:
            return
        
        session_data = {
            "session": self.sessions[session_id],
            "state": self.session_states.get(session_id, {}),
            "saved_at": time.time(),
            "version": "2025.1"
        }
        
        # Create directory if not exists
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(session_data, f, ensure_ascii=False, indent=2)
    
    def load_session_from_file(self, filepath: str) -> Optional[str]:
        """Load session from file"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                session_data = json.load(f)
            
            session = session_data["session"]
            state = session_data.get("state", {})
            
            session_id = session["session_id"]
            
            # Check if session already exists
            if session_id in self.sessions:
                # Generate new ID
                session_id = f"loaded_{session_id}_{int(time.time())}"
                session["session_id"] = session_id
            
            # Store session
            self.sessions[session_id] = session
            self.session_states[session_id] = state
            
            return session_id
            
        except Exception as e:
            print(f"{merah}❌  Failed to load session: {e}{reset}")
            return None
    
    def _cleanup_old_sessions(self):
        """Cleanup old sessions"""
        current_time = time.time()
        
        if current_time - self._last_cleanup < self.cleanup_interval:
            return
        
        sessions_to_remove = []
        
        for session_id, session in self.sessions.items():
            # Remove expired sessions
            if current_time - session["last_activity"] > self.session_timeout:
                sessions_to_remove.append(session_id)
            # Remove failed sessions
            elif session.get("state") in ["failed", "rotated"]:
                sessions_to_remove.append(session_id)
        
        # Remove sessions
        for session_id in sessions_to_remove:
            if session_id in self.sessions:
                del self.sessions[session_id]
            if session_id in self.session_states:
                del self.session_states[session_id]
        
        self._last_cleanup = current_time
        
        if sessions_to_remove:
            print(f"{cyan}🧹  Cleaned up {len(sessions_to_remove)} old sessions{reset}")
    
    def get_all_sessions(self, active_only: bool = True) -> List[Dict[str, Any]]:
        """Get all sessions"""
        self._cleanup_old_sessions()
        
        sessions = []
        for session_id, session in self.sessions.items():
            if active_only and session.get("state") != "active":
                continue
            
            # Get health status
            health = self.get_session_health(session_id)
            
            sessions.append({
                "session_id": session_id,
                "created_at": session["created_at"],
                "last_activity": session["last_activity"],
                "request_count": session["request_count"],
                "success_rate": session["success_count"] / session["request_count"] if session["request_count"] > 0 else 0,
                "state": session["state"],
                "health": health,
                "metadata": session["metadata"]
            })
        
        return sessions
    
    def get_session_statistics(self) -> Dict[str, Any]:
        """Get session statistics"""
        self._cleanup_old_sessions()
        
        total_sessions = len(self.sessions)
        active_sessions = sum(1 for s in self.sessions.values() if s.get("state") == "active")
        
        total_requests = sum(s["request_count"] for s in self.sessions.values())
        total_success = sum(s["success_count"] for s in self.sessions.values())
        
        avg_success_rate = total_success / total_requests if total_requests > 0 else 0
        
        # Session age distribution
        now = time.time()
        session_ages = [now - s["created_at"] for s in self.sessions.values()]
        
        return {
            "total_sessions": total_sessions,
            "active_sessions": active_sessions,
            "expired_sessions": total_sessions - active_sessions,
            "total_requests": total_requests,
            "total_success": total_success,
            "success_rate": avg_success_rate,
            "avg_session_age": sum(session_ages) / len(session_ages) if session_ages else 0,
            "oldest_session": max(session_ages) if session_ages else 0,
            "newest_session": min(session_ages) if session_ages else 0
        }

# ===================== REQUEST ORCHESTRATOR 2025 =====================

class RequestOrchestrator2025:
    """Advanced request orchestrator - FIXED dengan result storage"""
    
    def __init__(self, session_manager: AdvancedSessionManager2025):
        self.session_manager = session_manager
        self.request_queue = asyncio.Queue()
        self.worker_tasks = []
        self.result_store = {}  # <-- TAMBAHKAN INI untuk store results
        self.max_workers = 10
        self.max_retries = 3
        self.request_timeout = 30
        self.rate_limiter = RateLimiter2025()
        self.circuit_breaker = CircuitBreaker2025()
        self.request_cache = {}
        self.cache_ttl = 300
        self.account_creator = None
        
    async def initialize(self):
        """Initialize workers"""
        for i in range(self.max_workers):
            task = asyncio.create_task(self._worker_loop(i))
            self.worker_tasks.append(task)
        
        print(f"{hijau}✅  Request orchestrator initialized with {self.max_workers} workers{reset}")
    
    async def shutdown(self):
        """Shutdown workers"""
        for task in self.worker_tasks:
            task.cancel()
        
        await asyncio.gather(*self.worker_tasks, return_exceptions=True)
        print(f"{cyan}🛑  Request orchestrator shutdown{reset}")
    
    async def make_request(self, session_id: str, method: str, url: str,
                          headers: Optional[Dict[str, str]] = None,
                          data: Optional[Any] = None,
                          cookies: Optional[Dict[str, str]] = None,
                          priority: int = 5,
                          cache_key: Optional[str] = None,
                          require_cookies: bool = True,
                          request_type: str = "default") -> Dict[str, Any]:
        """
        Make request with FULL AUTO-SYNC for headers, cookies, and CSRF.
        
        request_type options:
        - "default": Standard page request
        - "ajax": AJAX/API request (adds X-* Instagram headers)
        - "form": Form submission
        - "navigate": Page navigation
        
        All headers and cookies are automatically synchronized from session.
        CSRF token is automatically included for POST requests.
        """
        
        # Check cache
        if cache_key and cache_key in self.request_cache:
            cached = self.request_cache[cache_key]
            if time.time() - cached["timestamp"] < self.cache_ttl:
                print(f"{cyan}💾  Using cached response for {cache_key}{reset}")
                return cached["response"]
        
        # Get session with all synced components
        session = self.session_manager.get_session_with_headers(session_id)
        if not session:
            return {"status": None, "error": f"Session {session_id} not found or expired"}
        
        # AUTO-SYNC: Build complete headers based on request type
        auto_headers = self._build_auto_sync_headers(session, method, url, request_type)
        
        # Merge with any custom headers (custom headers override auto headers)
        if headers:
            auto_headers.update(headers)
        
        # AUTO-SYNC: Get all cookies from session
        session_cookies = {}
        if require_cookies:
            session_cookies = self.session_manager.get_session_cookies(session_id)
            if "instagram.com" in url:
                instagram_cookies = self.session_manager.get_session_cookies(session_id, "instagram.com")
                session_cookies.update(instagram_cookies)
        
        # Merge cookies
        all_cookies = {**session_cookies, **(cookies or {})}
        
        # AUTO-SYNC: Add CSRF token to cookies if available
        csrf_token = session.get("tokens", {}).get("csrftoken", "")
        if csrf_token and "csrftoken" not in all_cookies:
            all_cookies["csrftoken"] = csrf_token
        
        # Get connection type
        metadata = session.get("metadata", {})
        connection_type = metadata.get("connection_type", "mobile")
        
        # Create request object
        request_id = f"req_{int(time.time())}_{random.randint(1000, 9999)}"
        
        request_data = {
            "request_id": request_id,
            "session_id": session_id,
            "method": method,
            "url": url,
            "headers": auto_headers,
            "data": data,
            "cookies": all_cookies,
            "priority": priority,
            "cache_key": cache_key,
            "require_cookies": require_cookies,
            "timestamp": time.time(),
            "retry_count": 0,
            "connection_type": connection_type,
            "request_type": request_type
        }
        
        # Put in queue
        await self.request_queue.put(request_data)
        
        # Wait for result
        result = await self._wait_for_result(request_id)
        
        # AUTO-SYNC: Update session with response cookies
        if result.get("cookies"):
            self.session_manager.update_session_cookies(session_id, result["cookies"])
        
        # AUTO-SYNC: Update CSRF token if present in response
        if result.get("cookies", {}).get("csrftoken"):
            self.session_manager.update_session(session_id, {
                "tokens": {
                    **session.get("tokens", {}),
                    "csrftoken": result["cookies"]["csrftoken"]
                }
            })
        
        return result
    
    def _build_auto_sync_headers(self, session: Dict[str, Any], method: str, 
                                  url: str, request_type: str) -> Dict[str, str]:
        """Build complete headers automatically based on session and request type"""
        
        # Get session headers as base
        session_headers = session.get("headers", {})
        current_headers = session.get("current_headers", {})
        metadata = session.get("metadata", {})
        tokens = session.get("tokens", {})
        
        # Start with base headers from session
        headers = {}
        
        # Add User-Agent (consistent across all requests)
        if "User-Agent" in session_headers:
            headers["User-Agent"] = session_headers["User-Agent"]
        elif "user_agent" in metadata:
            headers["User-Agent"] = metadata["user_agent"]
        
        # Add Sec-Ch-* headers from session
        sec_ch_keys = ["Sec-Ch-Ua", "Sec-Ch-Ua-Mobile", "Sec-Ch-Ua-Platform", 
                      "Sec-Ch-Ua-Model", "Sec-Ch-Ua-Full-Version-List", "Sec-Ch-Ua-Platform-Version"]
        for key in sec_ch_keys:
            if key in session_headers:
                headers[key] = session_headers[key]
        
        # Build headers based on request type
        if request_type == "navigate" or (method == "GET" and request_type == "default"):
            # Page navigation headers
            headers.update({
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
                "Accept-Encoding": "gzip, deflate, br",
                "Accept-Language": metadata.get("language", "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7"),
                "Cache-Control": "max-age=0",
                "Sec-Fetch-Dest": "document",
                "Sec-Fetch-Mode": "navigate",
                "Sec-Fetch-Site": "none",
                "Sec-Fetch-User": "?1",
                "Upgrade-Insecure-Requests": "1",
            })
            
        elif request_type == "ajax" or (method == "POST" and "api" in url):
            # AJAX/API request headers
            csrf_token = tokens.get("csrftoken", "")
            ajax_id = tokens.get("ajax_id", "1029952363")
            web_session_id = session.get("extra_session_id", "")
            
            # CLEAN API HEADERS - Only essential headers, avoid suspicious custom ones
            headers.update({
                "Accept": "*/*",
                "Accept-Encoding": "gzip, deflate, br",
                "Accept-Language": metadata.get("language", "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7"),
                "Content-Type": "application/x-www-form-urlencoded",
                "Origin": "https://www.instagram.com",
                "Referer": "https://www.instagram.com/accounts/emailsignup/",
                "Sec-Fetch-Dest": "empty",
                "Sec-Fetch-Mode": "cors",
                "Sec-Fetch-Site": "same-origin",
                "X-Ig-App-Id": "936619743392459",
                "X-Requested-With": "XMLHttpRequest",
            })
            
            # Add CSRF only if present
            if csrf_token:
                headers["X-Csrftoken"] = csrf_token
                
        elif request_type == "form":
            # Form submission headers
            csrf_token = tokens.get("csrftoken", "")
            
            headers.update({
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Accept-Encoding": "gzip, deflate, br",
                "Accept-Language": metadata.get("language", "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7"),
                "Content-Type": "application/x-www-form-urlencoded",
                "Origin": "https://www.instagram.com",
                "Referer": "https://www.instagram.com/",
                "Sec-Fetch-Dest": "document",
                "Sec-Fetch-Mode": "navigate",
                "Sec-Fetch-Site": "same-origin",
                "Sec-Fetch-User": "?1",
                "Upgrade-Insecure-Requests": "1",
            })
            
            if csrf_token:
                headers["X-Csrftoken"] = csrf_token
                
        else:
            # Default headers
            headers.update({
                "Accept": "*/*",
                "Accept-Encoding": "gzip, deflate, br",
                "Accept-Language": metadata.get("language", "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7"),
            })
            
            if method == "POST":
                headers["Content-Type"] = "application/x-www-form-urlencoded"
                csrf_token = tokens.get("csrftoken", "")
                if csrf_token:
                    headers["X-Csrftoken"] = csrf_token
        
        return headers
    
    async def _wait_for_result(self, request_id: str) -> Dict[str, Any]:
        """Wait for request result - FIXED dengan polling result_store"""
        start_time = time.time()
        
        # Poll result_store sampai result tersedia atau timeout
        while time.time() - start_time < self.request_timeout:
            if request_id in self.result_store:
                result = self.result_store.pop(request_id)
                return result
            
            await asyncio.sleep(0.1)  # Small delay untuk mengurangi CPU usage
        
        # Timeout
        return {"status": None, "error": f"Timeout waiting for response {request_id}"}
    
    async def _worker_loop(self, worker_id: int):
        """Worker loop untuk processing requests - FIXED store result"""
        # print(f"{cyan}👷  Worker {worker_id} started{reset}")
        
        try:
            while True:
                try:
                    # Get request from queue
                    request_data = await asyncio.wait_for(
                        self.request_queue.get(),
                        timeout=1.0
                    )
                    
                    # Process request
                    result = await self._process_request(worker_id, request_data)
                    
                    # STORE RESULT ke result_store <-- FIX
                    request_id = request_data["request_id"]
                    self.result_store[request_id] = result
                    
                    self.request_queue.task_done()
                    
                except asyncio.TimeoutError:
                    continue
                except asyncio.CancelledError:
                    break
                except Exception as e:
                    print(f"{merah}❌  Worker {worker_id} error: {e}{reset}")
                    # Store error result
                    if 'request_data' in locals():
                        request_id = request_data.get("request_id")
                        if request_id:
                            self.result_store[request_id] = {
                                "status": None,
                                "error": str(e),
                                "request_id": request_id
                            }
                    continue
        
        except asyncio.CancelledError:
            pass
        
        # print(f"{cyan}👷  Worker {worker_id} stopped{reset}")
    
    async def _process_request(self, worker_id: int, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process single request dengan cookie management - FIXED"""
        request_id = request_data["request_id"]
        session_id = request_data["session_id"]
        
        # Get fresh session data - FIXED
        session = self.session_manager.get_session_with_headers(session_id)
        if not session:
            return {
                "status": None,
                "error": "Session not found",
                "request_id": request_id
            }
        
        # Rate limiting check
        if not self.rate_limiter.can_make_request(session_id, request_data["url"]):
            await asyncio.sleep(random.uniform(2.0, 5.0))
        
        # Circuit breaker check
        if not await self.circuit_breaker.can_request(session_id, request_data["url"]):
            return {
                "status": None,
                "error": "Circuit breaker open",
                "request_id": request_id
            }
        
        # Simulate human behavior sebelum request - FIXED
        await self._simulate_human_behavior(session_id, request_data)
        
        # Update session state
        self.session_manager.update_session_state(session_id, {
            "current_page": request_data["url"],
            "interaction_log": f"{request_data['method']} {request_data['url']}"
        })
        
        # Record request
        self.session_manager.record_request(session_id, request_data)
        
        # Make actual request
        try:
            start_time = time.time()
            
            # Gunakan REAL HTTP request - FIXED
            response = await self._make_real_http_request(request_data, session)
            
            response_time = time.time() - start_time
            
            # Update response data
            response["response_time"] = response_time
            response["request_id"] = request_id
            
            # Record response
            self.session_manager.record_response(session_id, response)
            
            # Handle cookies dari response - FIXED
            if response.get("cookies"):
                # Determine domain dari URL
                from urllib.parse import urlparse
                domain = urlparse(request_data["url"]).netloc
                
                # Update cookies di session manager
                self.session_manager.update_session_cookies(
                    session_id, 
                    response["cookies"], 
                    domain
                )
                
                # Juga update di session data langsung
                self.session_manager.update_session(session_id, {
                    "cookies": {**session.get("cookies", {}), **response["cookies"]}
                })
            
            # Update circuit breaker
            if response["status"] and 200 <= response["status"] < 300:
                await self.circuit_breaker.record_success(session_id, request_data["url"])
            else:
                await self.circuit_breaker.record_failure(session_id, request_data["url"])
                
                # Handle rate limit specifically - FIXED
                if response["status"] == 429:
                    print(f"{merah}⚠️  Rate limit detected for session {session_id[:8]}...{reset}")
                    
                    # Update session state
                    self.session_manager.update_session_state(session_id, {
                        "error_log": "Rate limit 429",
                        "performance_metrics": {
                            "rate_limit_hits": self.session_manager.session_states[session_id]
                                .get("performance_metrics", {})
                                .get("rate_limit_hits", 0) + 1
                        }
                    })
                    
                    # Trigger IP rotation jika diperlukan
                    if self.account_creator and request_data.get("retry_count", 0) == 0:
                        await self._handle_rate_limit(session_id, request_data)
            
            # Cache response jika perlu
            if request_data.get("cache_key") and response["status"] == 200:
                self.request_cache[request_data["cache_key"]] = {
                    "response": response,
                    "timestamp": time.time()
                }
            
            return response
            
        except Exception as e:
            # Record error
            self.session_manager.update_session_state(session_id, {
                "error_log": f"Request failed: {str(e)}"
            })
            
            # Update circuit breaker
            await self.circuit_breaker.record_failure(session_id, request_data["url"])
            
            # Retry logic dengan IP rotation jika perlu - FIXED
            if request_data["retry_count"] < self.max_retries:
                request_data["retry_count"] += 1
                
                # Check jika perlu rotate IP
                if request_data["retry_count"] >= 2 and self.account_creator:
                    print(f"{cyan}🔄  Retry #{request_data['retry_count']} with IP rotation...{reset}")
                    
                    # Rotate IP dan fingerprint
                    success = await self.account_creator.rotate_ip_with_fingerprint(session_id)
                    if success:
                        print(f"{hijau}✅  IP rotated for retry{reset}")
                
                print(f"{kuning}    Retrying {request_id} ({request_data['retry_count']}/{self.max_retries}){reset}")
                await asyncio.sleep(2 ** request_data["retry_count"])  # Exponential backoff
                
                # Re-queue untuk retry
                await self.request_queue.put(request_data)
                return {"status": None, "error": f"Retrying: {str(e)}", "request_id": request_id}
            
            return {
                "status": None,
                "error": str(e),
                "request_id": request_id
            }

    async def _simulate_human_behavior(self, session_id: str, request_data: Dict[str, Any]):
        """
        Advanced human behavior simulation using UltimateAntiDetection2025
        Simulates realistic human interaction patterns to avoid bot detection
        """
        session = self.session_manager.get_session(session_id)
        if not session:
            return
        
        # Initialize anti-detection system
        anti_detect = UltimateAntiDetection2025()
        
        behavior_profile = session.get("behavior_profile", {})
        connection_type = session.get("metadata", {}).get("connection_type", "mobile")
        request_type = request_data.get("request_type", "default")
        url = request_data.get("url", "")
        
        # Get optimal timing based on request history
        timing = anti_detect.get_optimal_request_timing()
        
        # Different behavior for different request types
        if request_type == "navigate" or "signup" in url.lower():
            # Page navigation - simulate page loading and reading
            delay = anti_detect.get_human_delay("page_load")
            await asyncio.sleep(delay)
            
            # Simulate scrolling behavior
            if random.random() < 0.7:
                scroll_delay = anti_detect.get_human_delay("scroll")
                await asyncio.sleep(scroll_delay)
        
        elif request_type == "ajax" and request_data["method"] == "POST":
            # Form submission - simulate filling form
            delay = anti_detect.get_human_delay("form_fill")
            await asyncio.sleep(delay)
            
            # Simulate button click delay
            click_delay = anti_detect.get_human_delay("button_click")
            await asyncio.sleep(click_delay)
            
            # Extra delay for API calls
            api_delay = anti_detect.get_human_delay("api_call")
            await asyncio.sleep(api_delay * 0.5)
        
        elif request_type == "form":
            # Traditional form submission
            delay = anti_detect.get_human_delay("form_fill")
            await asyncio.sleep(delay)
        
        else:
            # Default - general browsing behavior
            delay = anti_detect.get_human_delay("between_steps")
            await asyncio.sleep(delay * 0.7)
        
        # Mobile vs WiFi behavioral differences
        if connection_type == "mobile":
            # Mobile users are slightly faster but have more pauses
            if random.random() < 0.3:
                await asyncio.sleep(random.uniform(0.5, 1.5))  # Random pause
        else:
            # WiFi users are more consistent but slower
            await asyncio.sleep(random.uniform(0.3, 0.8))
        
        # Simulate POST data typing if applicable
        if request_data["method"] == "POST" and request_data.get("data"):
            data_str = str(request_data["data"])
            char_count = len(data_str)
            
            # Realistic typing speed: 60-100 WPM (5 chars per word)
            typing_speed_cps = behavior_profile.get("typing_speed_wpm", 70) * 5 / 60
            typing_time = char_count / typing_speed_cps
            
            # Cap at 5 seconds and add variation
            typing_time = min(typing_time, 5.0) * random.uniform(0.8, 1.2)
            await asyncio.sleep(typing_time)
        
        # Apply recommended delay from rate limit avoidance
        if timing["current_rate"] > 0.25:  # More than 1 request per 4 seconds
            extra_delay = timing["recommended_delay"] * 0.5
            await asyncio.sleep(extra_delay)
        
        # Record this request for rate management
        anti_detect.record_request(url, 0)  # Status 0 = pending

    async def _handle_rate_limit(self, session_id: str, request_data: Dict[str, Any]):
        """Handle rate limit dengan strategi yang tepat - FIXED"""
        print(f"{cyan}🛡️   Handling rate limit for session {session_id[:8]}...{reset}")
        
        # 1. Check session stats
        session = self.session_manager.get_session(session_id)
        if not session:
            return
        
        # 2. Determine strategy berdasarkan connection type
        connection_type = session.get("metadata", {}).get("connection_type", "mobile")
        
        if connection_type == "mobile":
            # Untuk mobile, rotate IP lebih agresif
            print(f"{cyan}    Mobile connection detected, rotating IP...{reset}")
            if self.account_creator:
                await self.account_creator.rotate_ip_with_fingerprint(session_id)
            wait_time = random.uniform(60, 120)  # Wait 1-2 menit
        else:
            # Untuk WiFi, coba ganti fingerprint dulu
            print(f"{cyan}    WiFi connection detected, changing fingerprint...{reset}")
            # Implement fingerprint rotation
            wait_time = random.uniform(120, 300)  # Wait 2-5 menit
        
        print(f"{kuning}    Waiting {wait_time:.1f}s before retry...{reset}")
        await asyncio.sleep(wait_time)
    
    async def _make_real_http_request(self, request_data: Dict[str, Any], 
                                    session: Dict[str, Any]) -> Dict[str, Any]:
        """Make HTTP request with realistic browser behavior"""
        method = request_data["method"]
        url = request_data["url"]
        headers = request_data["headers"]
        data = request_data["data"]
        
        # Get session headers and merge - session headers take priority for consistency
        session_headers = session.get("headers", {})
        
        # Build final headers - start with request headers, then apply session headers for consistency
        all_headers = {}
        
        # First, add essential browser headers in correct order
        if "Accept" in headers:
            all_headers["Accept"] = headers["Accept"]
        if "Accept-Encoding" in headers:
            all_headers["Accept-Encoding"] = headers["Accept-Encoding"]
        if "Accept-Language" in headers:
            all_headers["Accept-Language"] = headers["Accept-Language"]
        
        # Add Content-Type for POST
        if method.upper() == "POST" and "Content-Type" in headers:
            all_headers["Content-Type"] = headers["Content-Type"]
        
        # Add Origin and Referer
        if "Origin" in headers:
            all_headers["Origin"] = headers["Origin"]
        if "Referer" in headers:
            all_headers["Referer"] = headers["Referer"]
            
        # Add Sec-Ch-* headers from session for consistency
        for key in ["Sec-Ch-Ua", "Sec-Ch-Ua-Mobile", "Sec-Ch-Ua-Platform", 
                   "Sec-Ch-Ua-Model", "Sec-Ch-Ua-Full-Version-List", "Sec-Ch-Ua-Platform-Version"]:
            if key in session_headers:
                all_headers[key] = session_headers[key]
            elif key in headers:
                all_headers[key] = headers[key]
        
        # Add Sec-Fetch-* headers
        for key in ["Sec-Fetch-Dest", "Sec-Fetch-Mode", "Sec-Fetch-Site", "Sec-Fetch-User"]:
            if key in headers:
                all_headers[key] = headers[key]
        
        # Add User-Agent from session for consistency
        if "User-Agent" in session_headers:
            all_headers["User-Agent"] = session_headers["User-Agent"]
        elif "User-Agent" in headers:
            all_headers["User-Agent"] = headers["User-Agent"]
        
        # Add Instagram-specific headers only if present in request (for AJAX calls)
        ig_headers = ["X-Csrftoken", "X-Ig-App-Id", "X-Ig-Www-Claim", "X-Instagram-Ajax", 
                     "X-Requested-With", "X-Asbd-Id"]
        for key in ig_headers:
            if key in headers:
                all_headers[key] = headers[key]
        
        # Combine cookies
        session_cookies = session.get("cookies", {})
        request_cookies = request_data.get("cookies", {})
        all_cookies = {**session_cookies, **request_cookies}
        
        try:
            # Create SSL context that mimics Chrome
            ssl_context = ssl.create_default_context()
            ssl_context.check_hostname = True
            ssl_context.verify_mode = ssl.CERT_REQUIRED
            
            # Use connector with keepalive like real browsers
            connector = aiohttp.TCPConnector(
                ssl=ssl_context,
                limit=10,
                limit_per_host=5,
                keepalive_timeout=30,
                enable_cleanup_closed=True
            )
            
            timeout = aiohttp.ClientTimeout(total=30, connect=10)
            
            async with aiohttp.ClientSession(
                connector=connector,
                timeout=timeout,
                cookie_jar=aiohttp.CookieJar()
            ) as client_session:
                
                # Set cookies properly
                for name, value in all_cookies.items():
                    client_session.cookie_jar.update_cookies({name: value}, 
                        response_url=aiohttp.client.URL("https://www.instagram.com/"))
                
                start_time = time.time()
                
                if method.upper() == "GET":
                    async with client_session.get(url, headers=all_headers) as response:
                        body = await response.read()
                        status = response.status
                        response_headers = dict(response.headers)
                        
                elif method.upper() == "POST":
                    async with client_session.post(url, headers=all_headers, data=data) as response:
                        body = await response.read()
                        status = response.status
                        response_headers = dict(response.headers)
                        
                else:
                    async with client_session.request(method, url, headers=all_headers, data=data) as response:
                        body = await response.read()
                        status = response.status
                        response_headers = dict(response.headers)
                
                response_time = time.time() - start_time
                
                # Get cookies from response
                response_cookies = {}
                for cookie in client_session.cookie_jar:
                    response_cookies[cookie.key] = cookie.value
                
                return {
                    "status": status,
                    "body": body,
                    "headers": response_headers,
                    "cookies": response_cookies,
                    "response_time": response_time
                }
                
        except asyncio.TimeoutError:
            print(f"{merah}    Request timeout{reset}")
            return {
                "status": None,
                "error": "Timeout",
                "body": b"",
                "headers": {},
                "cookies": {}
            }
        except aiohttp.ClientError as e:
            print(f"{merah}    Client error: {e}{reset}")
            return {
                "status": None,
                "error": str(e),
                "body": b"",
                "headers": {},
                "cookies": {}
            }
        except Exception as e:
            print(f"{merah}    Unexpected error: {e}{reset}")
            return {
                "status": None,
                "error": str(e),
                "body": b"",
                "headers": {},
                "cookies": {}
            }
    
    def get_queue_status(self) -> Dict[str, Any]:
        """Get queue status"""
        return {
            "queue_size": self.request_queue.qsize(),
            "worker_count": len(self.worker_tasks),
            "cache_size": len(self.request_cache),
            "rate_limiter_status": self.rate_limiter.get_status(),
            "circuit_breaker_status": self.circuit_breaker.get_status()
        }
    
    def clear_cache(self):
        """Clear request cache"""
        self.request_cache.clear()
        print(f"{cyan}🧹  Request cache cleared{reset}")

class RateLimiter2025:
    """Rate limiter dengan adaptive learning"""
    
    def __init__(self):
        self.request_log = {}
        self.limits = {
            "default": {"max_requests": 10, "window_seconds": 60},
            "instagram": {"max_requests": 5, "window_seconds": 60},
            "critical": {"max_requests": 2, "window_seconds": 30}
        }
        self.adaptive_limits = {}
    
    def can_make_request(self, session_id: str, endpoint: str = None) -> bool:
        """Check if request can be made"""
        now = time.time()
        
        # Get limit config
        limit_config = self._get_limit_config(endpoint)
        window = limit_config["window_seconds"]
        max_requests = limit_config["max_requests"]
        
        # Initialize session log
        if session_id not in self.request_log:
            self.request_log[session_id] = []
        
        # Clean old requests
        session_log = self.request_log[session_id]
        session_log = [t for t in session_log if now - t < window]
        self.request_log[session_id] = session_log
        
        # Check limit
        if len(session_log) >= max_requests:
            # Calculate wait time
            oldest_request = min(session_log) if session_log else now
            wait_time = window - (now - oldest_request)
            
            if wait_time > 0:
                print(f"{kuning}⏳  Rate limit hit for {session_id}, wait {wait_time:.1f}s{reset}")
                return False
        
        # Record request
        session_log.append(now)
        
        # Adaptive learning
        self._update_adaptive_limits(session_id, endpoint, len(session_log))
        
        return True
    
    def _get_limit_config(self, endpoint: str) -> Dict[str, Any]:
        """Get limit configuration for endpoint"""
        if endpoint:
            if "instagram.com" in endpoint:
                return self.limits["instagram"]
            elif any(keyword in endpoint for keyword in ["/api/", "/v1/", "/graphql"]):
                return self.limits["critical"]
        
        return self.limits["default"]
    
    def _update_adaptive_limits(self, session_id: str, endpoint: str, current_count: int):
        """Update adaptive limits based on usage"""
        key = f"{session_id}:{endpoint}" if endpoint else session_id
        
        if key not in self.adaptive_limits:
            self.adaptive_limits[key] = {
                "total_requests": 0,
                "successful_requests": 0,
                "rate_limit_hits": 0,
                "avg_request_rate": 0,
                "last_updated": time.time()
            }
        
        stats = self.adaptive_limits[key]
        stats["total_requests"] += 1
        
        # Update success rate (simplified)
        if current_count < 5:  # Assume success if not hitting limit
            stats["successful_requests"] += 1
        else:
            stats["rate_limit_hits"] += 1
        
        # Calculate metrics
        time_since_update = time.time() - stats["last_updated"]
        if time_since_update > 60:  # Update every minute
            if stats["total_requests"] > 0:
                success_rate = stats["successful_requests"] / stats["total_requests"]
                request_rate = stats["total_requests"] / (time_since_update / 60)
                
                stats["success_rate"] = success_rate
                stats["avg_request_rate"] = request_rate
                stats["last_updated"] = time.time()
    
    def get_status(self) -> Dict[str, Any]:
        """Get rate limiter status"""
        total_sessions = len(self.request_log)
        total_requests = sum(len(log) for log in self.request_log.values())
        
        # Clean old logs
        now = time.time()
        for session_id in list(self.request_log.keys()):
            self.request_log[session_id] = [t for t in self.request_log[session_id] if now - t < 3600]
            if not self.request_log[session_id]:
                del self.request_log[session_id]
        
        return {
            "active_sessions": total_sessions,
            "total_requests_last_hour": total_requests,
            "adaptive_limits_count": len(self.adaptive_limits),
            "default_limits": self.limits
        }

class CircuitBreaker2025:
    """Circuit breaker pattern dengan adaptive thresholds"""
    
    def __init__(self):
        self.circuits = {}
        self.default_thresholds = {
            "failure_threshold": 5,
            "success_threshold": 3,
            "timeout_seconds": 60,
            "half_open_timeout": 30
        }
    
    async def can_request(self, session_id: str, endpoint: str) -> bool:
        """Check if circuit is closed"""
        circuit_key = self._get_circuit_key(session_id, endpoint)
        
        if circuit_key not in self.circuits:
            return True
        
        circuit = self.circuits[circuit_key]
        
        if circuit["state"] == "open":
            # Check if timeout has passed
            if time.time() - circuit["opened_at"] > circuit["timeout_seconds"]:
                # Move to half-open
                circuit["state"] = "half_open"
                circuit["half_open_since"] = time.time()
                return True
            else:
                return False
        
        elif circuit["state"] == "half_open":
            # Allow limited requests in half-open state
            if circuit.get("half_open_attempts", 0) >= 1:
                return False
            else:
                circuit["half_open_attempts"] = circuit.get("half_open_attempts", 0) + 1
                return True
        
        return True  # Closed state
    
    async def record_success(self, session_id: str, endpoint: str):
        """Record successful request"""
        circuit_key = self._get_circuit_key(session_id, endpoint)
        
        if circuit_key not in self.circuits:
            self.circuits[circuit_key] = self._create_circuit()
        
        circuit = self.circuits[circuit_key]
        
        if circuit["state"] == "half_open":
            # Success in half-open state, close circuit
            circuit["state"] = "closed"
            circuit["consecutive_successes"] = circuit.get("consecutive_successes", 0) + 1
            circuit["consecutive_failures"] = 0
            circuit["half_open_attempts"] = 0
            
            if circuit["consecutive_successes"] >= circuit["success_threshold"]:
                # Reset circuit after enough successes
                circuit["state"] = "closed"
                circuit["consecutive_successes"] = 0
        
        else:
            # Record success
            circuit["consecutive_successes"] = circuit.get("consecutive_successes", 0) + 1
            circuit["consecutive_failures"] = 0
    
    async def record_failure(self, session_id: str, endpoint: str):
        """Record failed request"""
        circuit_key = self._get_circuit_key(session_id, endpoint)
        
        if circuit_key not in self.circuits:
            self.circuits[circuit_key] = self._create_circuit()
        
        circuit = self.circuits[circuit_key]
        
        circuit["consecutive_failures"] = circuit.get("consecutive_failures", 0) + 1
        circuit["consecutive_successes"] = 0
        
        # Check if should open circuit
        if circuit["consecutive_failures"] >= circuit["failure_threshold"]:
            circuit["state"] = "open"
            circuit["opened_at"] = time.time()
    
    def _get_circuit_key(self, session_id: str, endpoint: str) -> str:
        """Get circuit key"""
        # Group endpoints by domain
        if endpoint:
            from urllib.parse import urlparse
            parsed = urlparse(endpoint)
            domain = parsed.netloc
            return f"{session_id}:{domain}"
        else:
            return session_id
    
    def _create_circuit(self) -> Dict[str, Any]:
        """Create new circuit"""
        return {
            "state": "closed",
            "consecutive_failures": 0,
            "consecutive_successes": 0,
            "failure_threshold": self.default_thresholds["failure_threshold"],
            "success_threshold": self.default_thresholds["success_threshold"],
            "timeout_seconds": self.default_thresholds["timeout_seconds"],
            "opened_at": 0,
            "half_open_since": 0,
            "half_open_attempts": 0,
            "created_at": time.time()
        }
    
    def get_status(self) -> Dict[str, Any]:
        """Get circuit breaker status"""
        total_circuits = len(self.circuits)
        
        states = {"closed": 0, "open": 0, "half_open": 0}
        for circuit in self.circuits.values():
            states[circuit["state"]] += 1
        
        # Clean old circuits
        now = time.time()
        circuits_to_remove = []
        for key, circuit in self.circuits.items():
            if circuit["state"] == "closed" and now - circuit["created_at"] > 3600:
                circuits_to_remove.append(key)
        
        for key in circuits_to_remove:
            del self.circuits[key]
        
        return {
            "total_circuits": total_circuits,
            "states": states,
            "cleaned_circuits": len(circuits_to_remove)
        }
# ===================== ACCOUNT CREATOR 2025 =====================

class InstagramAccountCreator2025:
    """Instagram account creator 2025 dengan semua teknik terbaru"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        # Default config
        default_config = {
            "use_proxy": False,
            "max_retries": 3,
            "request_timeout": 30,
            "email_service": "10minutemail",
            "location": "random",  # CHANGED: random country instead of just ID
            "device_type": "random",  # random antara android dan desktop
            "connection_type": "auto",  # auto = random mobile/wifi based on device
            "verbose": True
        }
        # Merge user config with defaults
        self.config = {**default_config, **(config or {})}

        print(f"{cyan}📧  ACCOUNT CREATOR EMAIL CONFIG: {self.config.get('email_service')}{reset}")
        print(f"{cyan}📶  CONNECTION TYPE: {self.config.get('connection_type')}{reset}")
        
        # Initialize systems dengan yang baru
        self.ip_system = AdvancedIPStealthSystem2025()  # Sudah updated
        self.fingerprint_system = AdvancedFingerprinting2025()
        self.behavior_system = BehavioralMimicry2025()
        self.email_manager = EmailServiceManager2025(
            preferred_service=self.config.get("email_service", "10minutemail")
        )
        self.session_manager = AdvancedSessionManager2025()
        self.web_system = WebRTCWebGL_Spoofing2025()
        self.cf_bypass = CloudflareCDN_Bypass2025()
        
        # Request orchestrator
        self.request_orchestrator = None
        
        # State
        self.active_sessions = {}
        self.account_attempts = {}
        self.successful_accounts = []
        self.failed_accounts = []

        self.jazoest_cache = {}
        self.last_jazoest_fetch = 0
        self.jazoest_ttl = 300
        
        # Statistics
        self.stats = {
            "total_attempts": 0,
            "successful": 0,
            "failed": 0,
            "rate_limited": 0,
            "checkpointed": 0,
            "start_time": time.time()
        }
        
        print(f"{hijau}✅  Instagram Account Creator 2025 dengan Dynamic IP System initialized{reset}")
    
    async def initialize(self):
        """Initialize semua sistem dengan connection type aware - FIXED"""
        try:
            print(f"{cyan}🚀  Initializing systems with connection type: {self.config.get('connection_type', 'auto')}{reset}")
            
            # Initialize request orchestrator
            self.request_orchestrator = RequestOrchestrator2025(self.session_manager)
            self.request_orchestrator.account_creator = self  # FIXED: set reference
            await self.request_orchestrator.initialize()
            
            # Warm up systems
            await self._warm_up_systems()
            
            print(f"{hijau}✅  All systems initialized successfully{reset}")
            return True
            
        except Exception as e:
            print(f"{merah}❌  Initialization failed: {e}{reset}")
            return False

    async def get_jazoest(self, session_id: str = None, url: str = "https://www.instagram.com/accounts/emailsignup/"):
        """Get real jazoest from Instagram signup page - NOT generated manually"""
        # Check cache
        cache_key = hashlib.md5(url.encode()).hexdigest()
        current_time = time.time()
        
        if (cache_key in self.jazoest_cache and 
            current_time - self.jazoest_cache[cache_key]["timestamp"] < self.jazoest_ttl):
            return self.jazoest_cache[cache_key]["value"]
        
        print(f"{cyan}🔍  Fetching real jazoest from signup page...{reset}")
        
        try:
            # Fetch the actual signup page to get real jazoest
            if session_id and hasattr(self, 'request_orchestrator'):
                response = await self.request_orchestrator.make_request(
                    session_id=session_id,
                    method="GET",
                    url=url,
                    request_type="navigate"
                )
                
                if response.get("status") == 200:
                    html = response.get("body", b"").decode('utf-8', errors='ignore')
                    
                    # Multiple regex patterns to extract jazoest from HTML
                    patterns = [
                        r'name="jazoest"\s+value="(\d+)"',  # Form input field
                        r'value="(\d+)"\s+name="jazoest"',  # Alternative order
                        r'"jazoest":"(\d+)"',               # JSON in script
                        r'"jazoest":\s*"(\d+)"',            # JSON with space
                        r'jazoest=(\d+)',                   # URL parameter
                        r'jazoest["\']?\s*[:=]\s*["\']?(\d+)',  # Generic pattern
                        r'input.*?jazoest.*?value="(\d+)"', # Input tag
                    ]
                    
                    for pattern in patterns:
                        match = re.search(pattern, html, re.IGNORECASE)
                        if match:
                            jazoest_value = match.group(1)
                            
                            # Validate jazoest (usually 4-5 digits, starts with 2)
                            if jazoest_value.isdigit() and 1000 <= int(jazoest_value) <= 99999:
                                self.jazoest_cache[cache_key] = {
                                    "value": jazoest_value,
                                    "timestamp": current_time,
                                    "source": "fetched_real"
                                }
                                print(f"{hijau}✅  Got real jazoest: {jazoest_value}{reset}")
                                return jazoest_value
                    
                    # Also try to find in shared_data/config
                    shared_data_match = re.search(r'window\._sharedData\s*=\s*(\{.+?\});', html)
                    if shared_data_match:
                        try:
                            shared_data = json.loads(shared_data_match.group(1))
                            if "config" in shared_data and "jazoest" in shared_data.get("config", {}):
                                jazoest_value = str(shared_data["config"]["jazoest"])
                                self.jazoest_cache[cache_key] = {
                                    "value": jazoest_value,
                                    "timestamp": current_time,
                                    "source": "shared_data"
                                }
                                print(f"{hijau}✅  Got real jazoest from shared_data: {jazoest_value}{reset}")
                                return jazoest_value
                        except:
                            pass
            
            # Try direct request if no session
            import aiohttp
            async with aiohttp.ClientSession() as temp_session:
                headers = {
                    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
                    "Accept-Language": "en-US,en;q=0.9",
                }
                async with temp_session.get(url, headers=headers, ssl=False) as resp:
                    if resp.status == 200:
                        html = await resp.text()
                        
                        # Same patterns as above
                        patterns = [
                            r'name="jazoest"\s+value="(\d+)"',
                            r'"jazoest":"(\d+)"',
                            r'jazoest=(\d+)',
                        ]
                        
                        for pattern in patterns:
                            match = re.search(pattern, html, re.IGNORECASE)
                            if match:
                                jazoest_value = match.group(1)
                                if jazoest_value.isdigit() and 1000 <= int(jazoest_value) <= 99999:
                                    self.jazoest_cache[cache_key] = {
                                        "value": jazoest_value,
                                        "timestamp": current_time,
                                        "source": "direct_fetch"
                                    }
                                    print(f"{hijau}✅  Got real jazoest (direct): {jazoest_value}{reset}")
                                    return jazoest_value
            
            # If still no jazoest found, use a realistic format based on device_id
            # Instagram jazoest is typically calculated from device_id/phone_id
            # Format: 2 + sum of ASCII values of phone_id
            device_id = str(uuid.uuid4()).replace('-', '')
            ascii_sum = sum(ord(c) for c in device_id)
            fallback = f"2{ascii_sum % 10000:04d}"  # Always starts with 2
            
            self.jazoest_cache[cache_key] = {
                "value": fallback,
                "timestamp": current_time,
                "source": "calculated"
            }
            
            print(f"{kuning}⚠️  Using calculated jazoest: {fallback}{reset}")
            return fallback
            
        except Exception as e:
            print(f"{merah}❌  Error getting jazoest: {e}{reset}")
            # Emergency fallback - still use proper format
            return "22801"
    
    async def _warm_up_systems(self):
        """Warm up semua sistem termasuk IP pool"""
        print(f"{cyan}🔥  Warming up systems...{reset}")
        
        # Generate test fingerprint
        test_fingerprint = self.fingerprint_system.generate_fingerprint(
            device_type=self.config["device_type"],
            location=self.config["location"]
        )
        
        # Generate test behavior profile
        test_behavior = self.behavior_system.generate_behavior_profile()
        
        # Generate initial IP pool - PERUBAHAN DI SINI!
        print(f"{cyan}🌐  Generating initial IP pool...{reset}")
        test_ip_config = self.ip_system.get_fresh_ip_config()  # GANTI!
        
        # Show IP pool stats
        ip_stats = self.ip_system.get_ip_pool_stats()
        print(f"{hijau}✅  IP Pool ready: {ip_stats.get('total_ips', 0)} IPs, Health: {ip_stats.get('health_rate', '0%')}{reset}")
        
        print(f"{hijau}✅  Systems warmed up{reset}")
    
    async def create_account(self, password: str, 
                           username_hint: Optional[str] = None,
                           session_id: Optional[str] = None) -> Dict[str, Any]:
        """Buat akun Instagram baru"""
        self.stats["total_attempts"] += 1
        attempt_id = f"attempt_{self.stats['total_attempts']:06d}"
        
        print(f"{cyan}🎯  Starting account creation {attempt_id}{reset}")
        
        try:
            # Generate atau gunakan session yang ada
            if not session_id:
                session_id = await self._create_new_session()
                if not session_id:
                    return self._record_failure(attempt_id, "Failed to create session")
            
            # Get session
            session = self.session_manager.get_session(session_id)
            if not session:
                return self._record_failure(attempt_id, "Session not found")
            
            # Simulate pre-signup behavior
            await self._simulate_pre_signup_behavior(session_id)
            
            # Get email
            email_data = await self._get_email_for_account(session_id)
            if not email_data:
                return self._record_failure(attempt_id, "Failed to get email")
            
            # Get initial CSRF token
            csrf_token = await self._get_initial_csrf(session_id)
            if not csrf_token:
                print(f"{kuning}⚠️   No CSRF token, continuing anyway{reset}")
            
            # Get username suggestions
            username = await self._get_username_suggestion(session_id, email_data["email"], username_hint)
            if not username:
                return self._record_failure(attempt_id, "Failed to get username")
            
            # Send verification email
            verification_sent = await self._send_verification_email(session_id, email_data["email"])
            if not verification_sent:
                return self._record_failure(attempt_id, "Failed to send verification")
            
            otp_attempts = 0
            max_otp_attempts = 2  # Coba 2x dengan email yang sama
            
            while otp_attempts < max_otp_attempts:
                otp = await self._get_verification_otp(email_data["email"])
                
                if otp:
                    # Verify OTP
                    signup_code = await self._verify_otp(session_id, email_data["email"], otp)
                    if signup_code:
                        break  # OTP berhasil
                
                otp_attempts += 1
                print(f"{kuning}⚠️   OTP attempt {otp_attempts}/{max_otp_attempts} failed{reset}")
                wait_time = random.uniform(10, 20)
                await asyncio.sleep(wait_time)
                break
                
                # if otp_attempts < max_otp_attempts:
                #     # Tunggu sebentar sebelum coba lagi
                #     wait_time = random.uniform(10, 20)
                #     print(f"{cyan}    Waiting {wait_time:.1f}s before retrying OTP...{reset}")
                #     await asyncio.sleep(wait_time)
            
            # Jika OTP gagal setelah max attempts, coba dengan email baru
            if not otp or not signup_code:
                print(f"{merah}❌  OTP failed after {max_otp_attempts} attempts{reset}")
                print(f"{cyan}🔄  Trying with new email...{reset}")
                
                # Dapatkan email baru
                new_email_data = await self.email_manager.resend_with_new_email(session_id, email_data["email"])
                if not new_email_data:
                    return self._record_failure(attempt_id, "Failed to get new email")
                
                email_data = new_email_data
                
                # Kirim verifikasi email baru
                verification_sent = await self._send_verification_email(session_id, email_data["email"])
                if not verification_sent:
                    return self._record_failure(attempt_id, "Failed to send verification to new email")
                
                # Get OTP dari email baru
                otp = await self._get_verification_otp(email_data["email"])
                if not otp:
                    return self._record_failure(attempt_id, "Failed to get OTP from new email")
                
                # Verify OTP baru
                signup_code = await self._verify_otp(session_id, email_data["email"], otp)
                if not signup_code:
                    return self._record_failure(attempt_id, "Failed to verify OTP from new email")
            
            # Create account - now returns dict with detailed info
            creation_result = await self._create_instagram_account(
                session_id, email_data["email"], username, password, signup_code
            )
            
            # Handle dict result from new function
            if isinstance(creation_result, dict):
                if creation_result.get("success"):
                    result = self._record_success(attempt_id, {
                        "username": username,
                        "email": email_data["email"],
                        "password": password,
                        "session_id": session_id,
                        "created_at": time.time()
                    })
                    return result
                else:
                    # Return detailed error info for session management
                    error_type = creation_result.get("error_type", "unknown")
                    return self._record_failure(attempt_id, f"Account creation failed: {error_type}", error_type)
            # Backward compatibility for bool return
            elif creation_result:
                result = self._record_success(attempt_id, {
                    "username": username,
                    "email": email_data["email"],
                    "password": password,
                    "session_id": session_id,
                    "created_at": time.time()
                })
                return result
            else:
                return self._record_failure(attempt_id, "Account creation failed", "unknown")
            
        except Exception as e:
            print(f"{merah}❌  Error in account creation: {e}{reset}")
            import traceback
            traceback.print_exc()
            return self._record_failure(attempt_id, f"Unexpected error: {str(e)}", "exception")
    
    async def _create_new_session(self) -> Optional[str]:
        """Buat session baru dengan semua komponen terintegrasi - RANDOM COUNTRY"""
        try:
            # Determine connection type
            connection_type = self.config.get("connection_type", "auto")
            if connection_type == "auto":
                # Auto detect: 70% mobile, 30% wifi
                connection_type = "mobile" if random.random() < 0.7 else "wifi"
            
            # RANDOM COUNTRY - select from all available countries
            location = self.config.get("location", "random")
            if location == "random":
                # Load country database and pick random
                all_countries = ["US", "CA", "GB", "DE", "FR", "NL", "IT", "ES", "PT", "BE", "CH", "AT", 
                               "PL", "SE", "NO", "DK", "JP", "KR", "CN", "TW", "HK", "SG", "TH", "MY", 
                               "PH", "VN", "ID", "IN", "PK", "AU", "NZ", "AE", "SA", "TR", "IL", 
                               "MX", "BR", "AR", "CL", "CO", "PE"]
                location = random.choice(all_countries)
            
            print(f"{cyan}    Creating {connection_type.upper()} session for {location}...{reset}")
            
            # Generate fingerprint berdasarkan connection type AND country
            fingerprint = self.fingerprint_system.generate_fingerprint(
                device_type=self.config["device_type"],
                location=location,  # Use random country
                connection_type=connection_type
            )
            
            # Generate behavior profile - country-agnostic
            if connection_type == "mobile":
                user_type = random.choice(["casual_user", "tech_savvy_user", "young_adult_user"])
            else:
                user_type = random.choice(["professional_user", "casual_user"])
            
            behavior_profile = self.behavior_system.generate_behavior_profile(user_type)
            
            # Get IP config - pass country for matching IP
            ip_config = self.ip_system.get_fresh_ip_config(
                session_id=None,
                min_health=80,
                connection_type=connection_type,
                country=location  # Pass country for IP selection
            )
            
            # Generate WebRTC/WebGL fingerprint
            webrtc_fingerprint = self.web_system.get_complete_fingerprint(
                device_type=self.config["device_type"],
                brand=fingerprint.get("device", {}).get("brand", "Samsung"),
                connection_type=connection_type
            )
            
            # Create session dengan semua fingerprints
            session_id = self.session_manager.create_session(
                fingerprint=fingerprint,
                behavior_profile=behavior_profile,
                ip_config=ip_config,
                webrtc_fingerprint=webrtc_fingerprint,
                country=location  # Store country in session
            )
            
            # Print country info
            ip_address = ip_config.get("ip", "unknown")
            isp_name = ip_config.get("isp_info", {}).get("isp", "unknown")
            print(f"{hijau}✅  Created new {connection_type.upper()} session: {session_id}{reset}")
            print(f"{cyan}    Country: {location}, IP: {ip_address} ({isp_name}){reset}")
            return session_id
            
        except Exception as e:
            print(f"{merah}❌  Failed to create session: {e}{reset}")
            import traceback
            traceback.print_exc()
            return None

    async def rotate_ip_with_fingerprint(self, session_id: str) -> bool:
        """Rotate IP dengan regenerate SEMUA fingerprints - FIXED"""
        print(f"{cyan}🔄  Rotating IP and fingerprints for session {session_id[:8]}...{reset}")
        
        try:
            session = self.session_manager.get_session(session_id)
            if not session:
                print(f"{merah}    Session not found{reset}")
                return False
            
            # Get current connection type dari session
            current_connection = session.get("metadata", {}).get("connection_type", "mobile")
            
            # Option: switch connection type jika sering kena rate limit
            if self.stats.get("rate_limited", 0) > 2:
                # Switch antara mobile dan wifi
                new_connection = "wifi" if current_connection == "mobile" else "mobile"
                print(f"{cyan}    Switching connection type: {current_connection} → {new_connection}{reset}")
            else:
                new_connection = current_connection  # <-- INI YANG TIDAK DIPERHATIKAN!
            
            print(f"{cyan}    Using connection type: {new_connection.upper()}{reset}")
            
            # 1. Get new IP config dengan connection type yang baru
            new_ip_config = self.ip_system.get_fresh_ip_config(
                min_health=80
            )
            
            # 2. Regenerate fingerprint sesuai ISP baru dan connection type
            isp = new_ip_config.get("isp_info", {}).get("isp", "telkomsel")
            location = new_ip_config.get("location", {}).get("city", "Jakarta")
            
            new_fingerprint = self.fingerprint_system.generate_fingerprint(
                device_type=self.config["device_type"],
                location=self.config["location"],
                isp=isp,
                city=location,
                connection_type=new_connection  # <-- PAKAI new_connection
            )
            
            # 3. Regenerate WebRTC/WebGL fingerprint
            device_brand = new_fingerprint.get("device", {}).get("brand", "Samsung")
            new_webrtc_fingerprint = self.web_system.get_complete_fingerprint(
                device_type=self.config["device_type"],
                brand=device_brand,
                connection_type=new_connection  # <-- PAKAI new_connection
            )
            
            # 4. Regenerate behavior profile
            if new_connection == "mobile":
                user_type = random.choice(["tech_savvy_indonesian", "young_adult_indonesian"])
            else:
                user_type = random.choice(["professional_indonesian", "casual_indonesian"])
            
            new_behavior = self.behavior_system.generate_behavior_profile(user_type)
            
            # 5. Rotate semua identitas sekaligus
            success = self.session_manager.rotate_session_identity(
                session_id=session_id,
                new_ip_config=new_ip_config,
                new_fingerprint=new_fingerprint,
                new_webrtc_fingerprint=new_webrtc_fingerprint
            )
            
            if success:
                # Update behavior profile juga
                self.session_manager.update_session(session_id, {
                    "behavior_profile": new_behavior
                })
                
                # Update metadata dengan connection type baru
                self.session_manager.update_session(session_id, {
                    "metadata": {
                        **session.get("metadata", {}),
                        "connection_type": new_connection  # <-- UPDATE
                    }
                })
                
                self.stats["ip_rotations"] = self.stats.get("ip_rotations", 0) + 1
                print(f"{hijau}✅  Successfully rotated IP and fingerprints{reset}")
                print(f"{cyan}    New IP: {new_ip_config.get('ip', 'unknown')}")
                print(f"{cyan}    New ISP: {isp}")
                print(f"{cyan}    Connection: {new_connection.upper()}{reset}")
                return True
            else:
                print(f"{merah}    Failed to rotate session identity{reset}")
                return False
            
        except Exception as e:
            print(f"{merah}❌  Error rotating IP: {e}{reset}")
            import traceback
            traceback.print_exc()
            return False
    
    async def _simulate_pre_signup_behavior(self, session_id: str):
        """Simulasi perilaku sebelum signup"""
        print(f"{cyan}🧠  Simulating pre-signup behavior...{reset}")
        
        session = self.session_manager.get_session(session_id)
        if not session:
            return
        
        behavior_profile = session["behavior_profile"]
        
        # Generate interaction sequence
        interactions = self.behavior_system.simulate_interaction(
            behavior_profile=behavior_profile,
            interaction_type="instagram_exploration"
        )
        
        # Record interactions
        for interaction in interactions[:5]:  # First 5 interactions
            self.session_manager.update_session_state(session_id, {
                "interaction_log": f"Pre-signup: {interaction['type']}"
            })
            
            # Simulate delay
            if interaction.get("duration"):
                await asyncio.sleep(min(interaction["duration"], 0.1))
        
        print(f"{hijau}✅  Pre-signup behavior simulation complete{reset}")
    
    async def _get_email_for_account(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Dapatkan email dengan fallback otomatis jika service gagal"""
        print(f"{cyan}📧  Getting email for account...{reset}")
        
        max_attempts = 2
        email_data = None
        
        for attempt in range(max_attempts):
            print(f"{cyan}    Email attempt {attempt + 1}/{max_attempts}{reset}")
            
            # Coba service yang dikonfigurasi
            email_data = await self.email_manager.get_email()
            
            if email_data:
                # Success!
                return email_data
            
            # Jika gagal, override service preference untuk attempt berikutnya
            if attempt == 0:
                print(f"{kuning}    Configured service failed, switching to 1secmail...{reset}")
                # Override ke 1secmail untuk attempt berikutnya
                self.email_manager.preferred_service = "1secmail"
            
            if attempt < max_attempts - 1:
                wait_time = random.uniform(5, 10)
                print(f"{kuning}    Waiting {wait_time:.1f}s before retry...{reset}")
                await asyncio.sleep(wait_time)
        
        # Jika masih gagal, coba emergency
        print(f"{merah}    All attempts failed, trying emergency...{reset}")
        return await self._create_emergency_email(session_id)

    async def _create_manual_email(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Create manual email sebagai last resort"""
        try:
            # Generate manual email
            domains = ["gmail.com", "yahoo.com", "outlook.com"]
            username = f"instagram{random.randint(10000, 99999)}"
            domain = random.choice(domains)
            
            # For Gmail, use plus addressing
            if domain == "gmail.com":
                email = f"{username}+insta{random.randint(1, 99)}@{domain}"
            else:
                email = f"{username}@{domain}"
            
            email_data = {
                "email": email,
                "username": username,
                "domain": domain,
                "service": "manual",
                "created_at": time.time(),
                "note": "Manual email - check manually for OTP"
            }
            
            # Record in session
            self.session_manager.update_session(session_id, {
                "email": email,
                "email_service": "manual",
                "email_note": "Manual email - requires manual OTP check"
            })
            
            print(f"{kuning}⚠️   Manual email created: {email}{reset}")
            print(f"{cyan}    You'll need to check this email manually for OTP{reset}")
            
            return email_data
            
        except Exception as e:
            print(f"{merah}    Failed to create manual email: {e}{reset}")
            return None
    
    async def _get_initial_csrf(self, session_id: str) -> Optional[str]:
        """Get fresh CSRF token with auto-sync headers"""
        print(f"{cyan}🛡️   Getting initial CSRF token...{reset}")
        
        try:
            # Visit Instagram signup page with auto headers
            response = await self.request_orchestrator.make_request(
                session_id=session_id,
                method="GET",
                url="https://www.instagram.com/accounts/emailsignup/",
                request_type="navigate"  # Auto-builds navigation headers
            )
            
            if response.get("status") == 200:
                # Extract CSRF from cookies
                cookies = response.get("cookies", {})
                body = response.get("body", b"")
                
                if "csrftoken" in cookies:
                    csrf_token = cookies["csrftoken"]
                    
                    # Try to extract X-Instagram-Ajax from page
                    ajax_id = None
                    try:
                        body_str = body.decode('utf-8', errors='ignore') if isinstance(body, bytes) else str(body)
                        # Look for rollout_hash or similar in the page
                        import re
                        ajax_match = re.search(r'"rollout_hash":"([^"]+)"', body_str)
                        if ajax_match:
                            ajax_id = ajax_match.group(1)
                        else:
                            # Try alternative pattern
                            ajax_match = re.search(r'"server_revision":(\d+)', body_str)
                            if ajax_match:
                                ajax_id = ajax_match.group(1)
                    except Exception:
                        pass
                    
                    # Store all tokens and cookies in session
                    tokens = {"csrftoken": csrf_token}
                    if ajax_id:
                        tokens["ajax_id"] = ajax_id
                    
                    self.session_manager.update_session(session_id, {
                        "tokens": tokens,
                        "cookies": cookies
                    })
                    
                    # Also update cookie jar
                    self.session_manager.update_session_cookies(session_id, cookies)
                    
                    print(f"{hijau}✅  Got CSRF token: {csrf_token[:10]}...{reset}")
                    if ajax_id:
                        print(f"{hijau}✅  Got Ajax ID: {ajax_id[:10]}...{reset}")
                    return csrf_token
            
            return None
            
        except Exception as e:
            print(f"{merah}❌  Failed to get CSRF token: {e}{reset}")
            return None
    
    async def _get_username_suggestion(self, session_id: str, email: str, 
                                 hint: Optional[str] = None, retry_count: int = 0) -> Optional[str]:
        """Dapatkan username suggestion dengan auto-sync headers"""
        print(f"{cyan}👤  Getting username suggestions...{reset}")
        
        # Limit retries to prevent infinite loop
        if retry_count >= 2:
            print(f"{kuning}    Max retries reached, using fallback{reset}")
            return self._generate_fallback_username(email, hint)
        
        try:
            # Get session data
            session = self.session_manager.get_session(session_id)
            if not session:
                print(f"{merah}    Session not found{reset}")
                return None
            
            csrf_token = session.get("tokens", {}).get("csrftoken", "")
            if not csrf_token:
                print(f"{kuning}    No CSRF token, using fallback{reset}")
                return self._generate_fallback_username(email, hint)
            
            # Prepare request data
            name = hint or email.split('@')[0]
            request_data = {
                "email": email,
                "first_name": name,
                "username": "",
                "opt_into_one_tap": "false",
            }
            
            # ENCODE data
            encoded_data = urlencode(request_data)
            
            print(f"{cyan}    Requesting username for: {email}{reset}")
            
            # Make request with auto-sync headers
            response = await self.request_orchestrator.make_request(
                session_id=session_id,
                method="POST",
                url="https://www.instagram.com/api/v1/web/accounts/web_create_ajax/attempt/",
                data=encoded_data,
                request_type="ajax"  # Auto-builds AJAX headers with CSRF
            )
            
            status = response.get("status")
            # print(f"{cyan}    Username API status: {status}{reset}")
            
            if status == 200:
                try:
                    body = response.get("body", b"")
                    if not body:
                        print(f"{kuning}    Empty response body - session may be expired{reset}")
                        return self._generate_fallback_username(email, hint)
                    
                    # Decode and check for HTML (session expired)
                    body_text = body.decode('utf-8', errors='ignore')
                    if body_text.startswith('<!DOCTYPE') or body_text.startswith('<html'):
                        print(f"{kuning}    Got HTML response - session expired, using fallback{reset}")
                        return self._generate_fallback_username(email, hint)
                    
                    if not body_text.strip():
                        print(f"{kuning}    Empty response - session may be flagged{reset}")
                        return self._generate_fallback_username(email, hint)
                    
                    data = json.loads(body_text)
                    # print(f"{cyan}    Username API response: {json.dumps(data, indent=2)[:300]}...{reset}")
                    
                    # Cari suggestions di berbagai field
                    suggestions = []
                    
                    if "suggestions" in data and isinstance(data["suggestions"], list):
                        suggestions = data["suggestions"]
                    elif "username_suggestions" in data and isinstance(data["username_suggestions"], list):
                        suggestions = data["username_suggestions"]
                    elif "suggested_usernames" in data and isinstance(data["suggested_usernames"], list):
                        suggestions = data["suggested_usernames"]
                    
                    # Coba parse error messages
                    if not suggestions:
                        errors = data.get("errors", {})
                        if errors:
                            print(f"{kuning}    API errors: {errors}{reset}")
                            
                            # Check jika email sudah terdaftar
                            error_msg = str(errors).lower()
                            if "email" in error_msg and ("already" in error_msg or "taken" in error_msg):
                                print(f"{merah}    Email already registered{reset}")
                                return None
                    
                    if suggestions:
                        # Pilih username pertama
                        username = suggestions[0]
                        
                        # Validasi username
                        if len(username) >= 3 and len(username) <= 30:
                            print(f"{hijau}✅  Got username: {username}{reset}")
                            
                            # Update session
                            self.session_manager.update_session(session_id, {
                                "username": username,
                                "username_source": "instagram_api"
                            })
                            
                            return username
                        else:
                            print(f"{kuning}    Invalid username from API: {username}{reset}")
                    
                except json.JSONDecodeError as e:
                    print(f"{merah}    Failed to parse JSON: {e}{reset}")
                    # Debug raw response
                    body_preview = response.get("body", b"").decode('utf-8', errors='ignore')[:200]
                    print(f"{cyan}    Raw response: {body_preview}...{reset}")
                except Exception as e:
                    print(f"{merah}    Error parsing response: {e}{reset}")
            
            elif status == 400:
                body = response.get("body", b"").decode('utf-8', errors='ignore')[:200]
                print(f"{merah}    Bad request (400): {body}{reset}")
                
                # Coba dengan data yang lebih sederhana
                print(f"{cyan}    Trying simplified request...{reset}")
                simple_data = {"email": email, "first_name": name}
                simple_encoded = urlencode(simple_data)
                
                simple_response = await self.request_orchestrator.make_request(
                    session_id=session_id,
                    method="POST",
                    url="https://www.instagram.com/api/v1/web/accounts/web_create_ajax/attempt/",
                    data=simple_encoded,
                    request_type="ajax",  # Use request_type instead of headers
                    cookies=session.get("cookies", {})
                )
                
                if simple_response.get("status") == 200:
                    try:
                        simple_body = simple_response.get("body", b"")
                        simple_data = json.loads(simple_body.decode('utf-8', errors='ignore'))
                        if "suggestions" in simple_data:
                            username = simple_data["suggestions"][0]
                            print(f"{hijau}✅  Got username from simplified request: {username}{reset}")
                            return username
                    except:
                        pass
            
            elif status == 429:
                print(f"{kuning}    Rate limited by Instagram{reset}")
                if retry_count < 1:  # Only retry once for rate limit
                    await asyncio.sleep(random.uniform(30, 60))
                    return await self._get_username_suggestion(session_id, email, hint, retry_count + 1)
                else:
                    print(f"{kuning}    Max rate limit retries reached{reset}")
            
            elif status == 403:
                print(f"{merah}    Access forbidden - need new CSRF token{reset}")
                if retry_count < 1:  # Only retry once for 403
                    new_csrf = await self._get_initial_csrf(session_id)
                    if new_csrf:
                        print(f"{cyan}    Got new CSRF, retrying...{reset}")
                        return await self._get_username_suggestion(session_id, email, hint, retry_count + 1)
                else:
                    print(f"{kuning}    Max 403 retries reached, using fallback{reset}")
            
            # Fallback: generate username
            fallback_username = self._generate_fallback_username(email, hint)
            print(f"{kuning}⚠️   Using fallback username: {fallback_username}{reset}")
            
            return fallback_username
            
        except Exception as e:
            print(f"{merah}❌  Failed to get username suggestions: {e}{reset}")
            import traceback
            traceback.print_exc()
            
            # Generate fallback
            fallback_username = self._generate_fallback_username(email, hint)
            return fallback_username

    def _generate_fallback_username(self, email: str, hint: Optional[str] = None) -> str:
        """Generate fallback username yang lebih baik"""
        base = hint or email.split('@')[0]
        
        # Clean base: hanya huruf, angka, underscore, titik
        import re
        base = re.sub(r'[^a-zA-Z0-9._]', '', base)
        
        # Jika base terlalu pendek, tambahkan random
        if len(base) < 3:
            base = f"user{random.randint(100, 999)}"
        
        # Pilih suffix Indonesia
        id_suffixes = ["_id", "_ind", "_indo", "_idn", "_jakarta", "_bali", 
                    str(random.randint(10, 99)), str(random.randint(100, 999))]
        
        # Pilih random format
        formats = [
            f"{base}{random.choice(id_suffixes)}",
            f"{base}.{random.choice(['id', 'ind', 'indo'])}",
            f"{base}{random.randint(100, 999)}",
            f"{base}_{random.randint(1000, 9999)}"
        ]
        
        username = random.choice(formats)
        
        # Pastikan panjang valid
        username = username[:30]  # Instagram max 30 chars
        
        # Pastikan tidak diawali/trailing dengan titik/underscore
        username = username.strip('._')
        
        # Tambahkan angka jika terlalu pendek
        if len(username) < 3:
            username = f"{username}{random.randint(100, 999)}"
        
        return username.lower()
    
    async def _send_verification_email(self, session_id: str, email: str) -> bool:
        """Kirim email verifikasi dengan auto-sync headers"""
        print(f"{cyan}📤  Sending verification email...{reset}")
        
        try:
            session = self.session_manager.get_session(session_id)
            if not session:
                return False
            
            # Get fresh jazoest from real signup page
            jazoest = await self.get_jazoest(session_id=session_id)
            
            # Prepare request dengan parameter lengkap
            request_data = {
                "device_id": session.get("device_id", ""),
                "email": email,
                "jazoest": jazoest,
                "_uid": session.get("uid", ""),
                "guid": session.get("guid", str(uuid.uuid4())),
                "_uuid": session.get("uuid", str(uuid.uuid4()))
            }
            
            # Filter out empty values
            request_data = {k: v for k, v in request_data.items() if v}
            
            encoded_data = urlencode(request_data)
            
            # Use auto-sync headers
            response = await self.request_orchestrator.make_request(
                session_id=session_id,
                method="POST",
                url="https://www.instagram.com/api/v1/accounts/send_verify_email/",
                data=encoded_data,
                request_type="ajax"  # Auto-builds all headers
            )
            
            status = response.get("status")
            print(f"{cyan}    Status: {status}{reset}")
            
            if status in [200, 201]:
                try:
                    body = response.get("body", b"{}").decode('utf-8', errors='ignore')
                    data = json.loads(body) if body else {}
                    
                    if data.get("email_sent") == True or data.get("status") == "ok":
                        print(f"{hijau}✅  Verification email sent{reset}")
                        return True
                    else:
                        print(f"{merah}    API error: {data}{reset}")
                        return False
                        
                except Exception as e:
                    print(f"{merah}    Parse error: {e}{reset}")
                    # If 200 OK but parse error, assume success
                    print(f"{kuning}⚠️   Assuming email sent (200 OK){reset}")
                    return True
            else:
                print(f"{merah}❌  Failed to send verification email: HTTP {status}{reset}")
                return False
                
        except Exception as e:
            print(f"{merah}❌  Error sending verification email: {e}{reset}")
            return False
    
    async def _get_verification_otp(self, email: str) -> Optional[str]:
        """Dapatkan OTP dari email"""
        print(f"{cyan}⏳  Waiting for verification OTP...{reset}")
        
        try:
            otp = await self.email_manager.wait_for_otp(email, timeout=90)
            return otp
            
        except Exception as e:
            print(f"{merah}❌  Error getting OTP: {e}{reset}")
            return None
    
    async def _verify_otp(self, session_id: str, email: str, otp: str) -> Optional[str]:
        """Verifikasi OTP dengan auto-sync headers"""
        print(f"{cyan}🔐  Verifying OTP...{reset}")
        
        try:
            session = self.session_manager.get_session(session_id)
            if not session:
                return None
            
            # Get fresh jazoest from real signup page
            jazoest = await self.get_jazoest(session_id=session_id)
            
            # Prepare request dengan parameter lengkap
            request_data = {
                "code": otp,
                "device_id": session.get("device_id", ""),
                "email": email,
                "jazoest": jazoest,
                "_uid": session.get("uid", ""),
                "guid": session.get("guid", str(uuid.uuid4())),
                "_uuid": session.get("uuid", str(uuid.uuid4()))
            }
            
            # Filter out empty values
            request_data = {k: v for k, v in request_data.items() if v}
            
            encoded_data = urlencode(request_data)
            
            # Use auto-sync headers
            response = await self.request_orchestrator.make_request(
                session_id=session_id,
                method="POST",
                url="https://www.instagram.com/api/v1/accounts/check_confirmation_code/",
                data=encoded_data,
                request_type="ajax"  # Auto-builds all headers
            )
            
            status = response.get("status")
            # print(f"{cyan}    Status: {status}{reset}")
            
            if status == 200:
                try:
                    body = response.get("body", b"{}").decode('utf-8', errors='ignore')
                    # print(f"{cyan}    Response body: {body[:200]}...{reset}")

                    data = json.loads(response.get("body", b"{}"))
                    signup_code = data.get("signup_code", "")
                    
                    if signup_code:
                        print(f"{hijau}✅  OTP verified, got signup code: {signup_code}{reset}")
                        
                        # Update session
                        self.session_manager.update_session(session_id, {
                            "signup_code": signup_code,
                            "otp_verified": True,
                            "jazoest": jazoest
                        })
                        
                        return signup_code
                    else:
                        print(f"{merah}❌  No signup code in response{reset}")
                        # Debug response
                        print(f"{cyan}    Full response: {data}{reset}")
                        return None
                        
                except Exception as e:
                    print(f"{merah}❌  Failed to parse verification response: {e}{reset}")
                    # Debug
                    body_preview = response.get("body", b"").decode('utf-8', errors='ignore')[:500]
                    print(f"{cyan}    Raw response: {body_preview}...{reset}")
                    return None
            else:
                print(f"{merah}❌  OTP verification failed: HTTP {status}{reset}")
                # Debug
                if response.get("body"):
                    body_preview = response.get("body", b"").decode('utf-8', errors='ignore')[:500]
                    # print(f"{cyan}    Response: {body_preview}...{reset}")
                return None
                
        except Exception as e:
            print(f"{merah}❌  Error verifying OTP: {e}{reset}")
            import traceback
            traceback.print_exc()
            return None
    
    async def _create_instagram_account(self, session_id: str, email: str, 
                                      username: str, password: str, 
                                      signup_code: str) -> Dict[str, Any]:
        """Create Instagram account dengan semua perbaikan
        
        IMPORTANT: No IP rotation during session - if it fails, return dict with error type
        to signal what kind of failure occurred.
        
        Returns:
            Dict with keys:
                - success: bool
                - error_type: str (ip_block, checkpoint, rate_limit, unknown)
                - user_id: str (if success or checkpoint)
                - username: str
        """
        
        # NO IP ROTATION - single attempt per session to avoid detection
        # If this fails, caller should create a completely new session
        print(f"{cyan}    Attempting account creation (no IP rotation for stealth){reset}")
        
        # Default result
        result = {
            "success": False,
            "error_type": "unknown",
            "user_id": None,
            "username": username
        }
        
        # Get session dengan headers terkini
        session = self.session_manager.get_session_with_headers(session_id)
        if not session:
            print(f"{merah}    Session not found{reset}")
            result["error_type"] = "session_error"
            return result
        
        # Get fresh jazoest from real signup page
        jazoest = await self.get_jazoest(session_id=session_id)
        
        # Prepare account data dengan FORMAT YANG BENAR
        month, day, year = self._generate_birthdate()
        
        # **PERBAIKAN KRITIS: FORMAT PASSWORD ENCRYPTION v10**
        current_timestamp = int(time.time())  # DETIK, bukan milidetik
        encrypted_password = f"#PWD_INSTAGRAM_BROWSER:0:{current_timestamp}:{password}"
        
        # Extra session ID
        extra_session_id = session.get("extra_session_id", "")
        if not extra_session_id:
            extra_session_id = self._generate_extra_session_id()

        name_first = fake_indonesia.first_name()
        
        account_data = {
            "email": email,
            "username": username,
            "first_name": name_first,
            "last_name": fake_indonesia.last_name(),
            "enc_password": encrypted_password,  # **FORMAT YANG BENAR**
            "month": month,
            "day": day,
            "year": year,
            "client_id": session.get("device_id", ""),  # **GUNAKAN client_id**
            "seamless_login_enabled": "1",
            "tos_version": "row",
            "force_sign_up_code": signup_code,
            "failed_birthday_year_count": "{}",
            "extra_session_id": extra_session_id,
            "jazoest": jazoest,
        }
        
        # Filter out empty values
        account_data = {k: v for k, v in account_data.items() if v}
        
        encoded_data = urlencode(account_data)
        
        # **ENDPOINT UTAMA - Try both endpoints**
        endpoints = [
            "https://www.instagram.com/api/v1/web/accounts/web_create_ajax/",
            "https://www.instagram.com/accounts/web_create_ajax/",
        ]
        
        for endpoint in endpoints:
            print(f"{cyan}    Trying endpoint: {endpoint}{reset}")
            
            # Use auto-sync headers
            response = await self.request_orchestrator.make_request(
                session_id=session_id,
                method="POST",
                url=endpoint,
                data=encoded_data,
                request_type="ajax"  # Auto-builds all headers
            )
            
            status = response.get("status")
            
            if status == 200:
                try:
                    body = response.get("body", b"")
                    if not body:
                        print(f"{merah}    Empty response body{reset}")
                        continue
                    
                    data = json.loads(body.decode('utf-8', errors='ignore'))
                    
                    if data.get("account_created") == True:
                        self.session_manager.update_session(session_id, {
                            "account_created": True,
                            "instagram_username": username,
                            "instagram_user_id": data.get("user_id", ""),
                            "created_at": time.time(),
                            "success_count": session.get("success_count", 0) + 1
                        })

                        bio_text = fake.sentence(nb_words=6)

                        edit_payload = {
                            "biography": bio_text,
                            "chaining_enabled": "on",
                            "external_url": "",
                            "first_name": name_first,
                            "username": username,
                            "jazoest": jazoest
                        }
                        edit_payload = {k: v for k, v in edit_payload.items() if v}
        
                        encoded_edit = urlencode(edit_payload)

                        # Use auto-sync headers for profile edit
                        response_edit = await self.request_orchestrator.make_request(
                            session_id=session_id,
                            method="POST",
                            url="https://www.instagram.com/api/v1/web/accounts/edit/",
                            data=encoded_edit,
                            request_type="ajax"  # Auto-builds all headers
                        )
                        
                        status_edit = response_edit.get("status")

                        if status_edit == 200:
                            try:
                                body_edit = response_edit.get("body", b"")
                                if not body_edit:
                                    print(f"{merah}    Empty response body{reset}")
                                    continue
                                
                                data_edit = json.loads(body_edit.decode('utf-8', errors='ignore'))
                                print(f"{cyan}    Response: {json.dumps(data_edit, indent=2)[:300]}...{reset}")
                                
                                if data_edit.get("status") == "ok":
                                    # **SUCCESS!**
                                    print(f"\n{bg_hijau}{putih}✅  ACCOUNT CREATED SUCCESSFULLY!{reset}")
                                    print(f"{cyan}    User ID: {data.get('user_id', 'N/A')}{reset}")
                                    print(f"{cyan}    Username: {username}{reset}")
                                    
                                    # Save working IP
                                    try:
                                        ip_config = session.get("ip_config", session.get("ip", {}))
                                        current_ip = ip_config.get("ip", "")
                                        current_isp = ip_config.get("isp_info", {}).get("isp", ip_config.get("isp", "unknown"))
                                        current_country = ip_config.get("country", "ID")
                                        if current_ip:
                                            save_working_ip(current_ip, current_isp, current_country, username)
                                    except Exception as e:
                                        print(f"{merah}    ⚠ Could not save working IP: {e}{reset}")
                                    
                                    # Update session
                                    self.session_manager.update_session(session_id, {
                                        "account_created": True,
                                        "instagram_username": username,
                                        "instagram_user_id": data.get("user_id", ""),
                                        "created_at": time.time(),
                                        "success_count": session.get("success_count", 0) + 1
                                    })
                                    
                                    # Save cookies
                                    if response.get("cookies"):
                                        self.session_manager.update_session_cookies(
                                            session_id, 
                                            response["cookies"], 
                                            "instagram.com"
                                        )
                            
                                    result["success"] = True
                                    result["error_type"] = None
                                    result["user_id"] = data.get("user_id", "")
                                    return result

                                else:
                                    print(f"\n{bg_kuning}{putih}✅  ACCOUNT CREATED CHECKPOINT!{reset}")
                                    print(f"{cyan}    User ID: {data.get('user_id', 'N/A')}{reset}")
                                    print(f"{cyan}    Username: {username}{reset}")
                                    
                                    # Save checkpoint IP
                                    try:
                                        ip_config = session.get("ip_config", session.get("ip", {}))
                                        current_ip = ip_config.get("ip", "")
                                        current_isp = ip_config.get("isp_info", {}).get("isp", ip_config.get("isp", "unknown"))
                                        current_country = ip_config.get("country", "ID")
                                        if current_ip:
                                            save_checkpoint_ip(current_ip, current_isp, current_country, username, "profile_edit_failed")
                                    except Exception as e:
                                        pass
                                    
                                    result["error_type"] = "checkpoint"
                                    result["user_id"] = data.get("user_id", "")
                                    return result

                            except Exception as e:
                                print(f"{merah}    Parse error: {e}{reset}")
                                print(f"\n{bg_kuning}{putih}✅  ACCOUNT CREATED CHECKPOINT!{reset}")
                                print(f"{cyan}    User ID: {data.get('user_id', 'N/A')}{reset}")
                                print(f"{cyan}    Username: {username}{reset}")
                                
                                # Save checkpoint IP
                                try:
                                    ip_config = session.get("ip_config", session.get("ip", {}))
                                    current_ip = ip_config.get("ip", "")
                                    current_isp = ip_config.get("isp_info", {}).get("isp", ip_config.get("isp", "unknown"))
                                    current_country = ip_config.get("country", "ID")
                                    if current_ip:
                                        save_checkpoint_ip(current_ip, current_isp, current_country, username, "parse_error")
                                except:
                                    pass
                                
                                result["error_type"] = "checkpoint"
                                result["user_id"] = data.get("user_id", "")
                                return result

                        else:
                            body_edit = response_edit.get("body", b"")
                            if body_edit:
                                data_edit = json.loads(body_edit.decode('utf-8', errors='ignore'))
                                print(f"{cyan}    Response: {json.dumps(data_edit, indent=2)[:300]}...{reset}")
                            print(f"\n{bg_kuning}{putih}✅  ACCOUNT CREATED CHECKPOINT!{reset}")
                            print(f"{cyan}    User ID: {data.get('user_id', 'N/A')}{reset}")
                            print(f"{cyan}    Username: {username}{reset}")
                            
                            # Save checkpoint IP
                            try:
                                ip_config = session.get("ip_config", session.get("ip", {}))
                                current_ip = ip_config.get("ip", "")
                                current_isp = ip_config.get("isp_info", {}).get("isp", ip_config.get("isp", "unknown"))
                                current_country = ip_config.get("country", "ID")
                                if current_ip:
                                    save_checkpoint_ip(current_ip, current_isp, current_country, username, "edit_status_not_200")
                            except:
                                pass
                            
                            result["error_type"] = "checkpoint"
                            result["user_id"] = data.get("user_id", "")
                            return result
                    else:
                        error_type = self._analyze_error_type(data)
                        print(f"{merah}    Account creation failed: {error_type}{reset}")
                        
                        # If IP block, don't try other endpoint - need new session
                        if error_type == "ip_block":
                            print(f"{merah}❌  IP blocked - need new session{reset}")
                            
                            # Save blocked IP
                            try:
                                ip_config = session.get("ip_config", session.get("ip", {}))
                                current_ip = ip_config.get("ip", "")
                                current_isp = ip_config.get("isp_info", {}).get("isp", ip_config.get("isp", "unknown"))
                                current_country = ip_config.get("country", "ID")
                                if current_ip:
                                    save_blocked_ip(current_ip, current_isp, current_country, "ip_block")
                            except:
                                pass
                            
                            result["error_type"] = "ip_block"
                            return result  # Exit immediately on IP block
                        # For other errors, try next endpoint
                        continue
                        
                except json.JSONDecodeError as e:
                    print(f"{merah}    JSON parse error: {e}{reset}")
                    body_preview = response.get("body", b"").decode('utf-8', errors='ignore')[:500]
                    print(f"{cyan}    Raw response: {body_preview}...{reset}")
                    # If 200 OK but parse error, might be success
                    print(f"{hijau}✅  Account likely created (200 OK){reset}")
                    result["success"] = True
                    result["error_type"] = None
                    return result
                except Exception as e:
                    print(f"{merah}    Parse error: {e}{reset}")
                    continue
            
            elif status == 403:
                print(f"{merah}    403 Forbidden - IP likely blocked{reset}")
                
                # Save blocked IP
                try:
                    ip_config = session.get("ip_config", session.get("ip", {}))
                    current_ip = ip_config.get("ip", "")
                    current_isp = ip_config.get("isp_info", {}).get("isp", ip_config.get("isp", "unknown"))
                    current_country = ip_config.get("country", "ID")
                    if current_ip:
                        save_blocked_ip(current_ip, current_isp, current_country, "403_forbidden")
                except:
                    pass
                
                result["error_type"] = "ip_block"
                return result  # Need new session
            
            elif status == 429:
                print(f"{kuning}    429 Rate Limited - need new session{reset}")
                self.stats["rate_limited"] = self.stats.get("rate_limited", 0) + 1
                
                # Save blocked IP (rate limited)
                try:
                    ip_config = session.get("ip_config", session.get("ip", {}))
                    current_ip = ip_config.get("ip", "")
                    current_isp = ip_config.get("isp_info", {}).get("isp", ip_config.get("isp", "unknown"))
                    current_country = ip_config.get("country", "ID")
                    if current_ip:
                        save_blocked_ip(current_ip, current_isp, current_country, "429_rate_limited")
                except:
                    pass
                
                result["error_type"] = "ip_block"
                return result  # Need new session
            
            else:
                print(f"{merah}    Endpoint failed with status: {status}{reset}")
                continue
        
        print(f"{merah}❌  Account creation failed - need new session{reset}")
        return result
    
    def _generate_extra_session_id(self) -> str:
        """Generate extra session ID seperti Instagram asli"""
        # Format: xxxyyy:zzzzzz:aaaaaa (contoh: u2t2bb:h0cl5k:4z5ot9)
        parts = [
            ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(6)),
            ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(6)),
            ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(6))
        ]
        return ':'.join(parts)
    
    def _analyze_error_type(self, response_data: Dict[str, Any]) -> str:
        """Analyze error type from Instagram response"""
        errors = response_data.get("errors", {})
        error_msg = str(errors).lower()
        
        ip_block_patterns = [
            "ip", "proxy", "datacenter", "vpn", "suspicious", "unusual",
            "temporary block", "try again later", "access denied"
        ]
        
        if any(pattern in error_msg for pattern in ip_block_patterns):
            return "ip_block"
        
        rate_limit_patterns = [
            "rate limit", "too many requests", "retry after",
            "wait a few minutes", "try again in"
        ]
        
        if any(pattern in error_msg for pattern in rate_limit_patterns):
            return "rate_limit"
        
        if "code" in error_msg and ("invalid" in error_msg or "incorrect" in error_msg):
            return "invalid_code"
        
        if "username" in error_msg or "email" in error_msg:
            return "credential_error"
        
        return "unknown"

    def get_stealth_ip_config(self) -> Dict[str, Any]:
        """Backward compatibility method - alias untuk get_fresh_ip_config()"""
        print(f"{kuning}⚠️   Using deprecated method get_stealth_ip_config(), please update to get_fresh_ip_config(){reset}")
        return self.get_fresh_ip_config()

    async def _retry_with_new_ip(self, session_id: str, email: str, username: str, 
                               password: str, signup_code: str) -> bool:
        """Retry account creation dengan IP baru"""
        print(f"{cyan}🔄  Rotating IP and retrying...{reset}")
        
        try:
            session = self.session_manager.get_session(session_id)
            if not session:
                return False
            
            # Dapatkan IP config baru
            new_ip_config = self.ip_system.get_stealth_ip_config()
            
            # Update session dengan IP baru
            self.session_manager.update_session(session_id, {
                "ip_config": new_ip_config,
                "headers": {**session.get("headers", {}), **new_ip_config.get("headers", {})},
                "ip_rotated": True,
                "rotation_count": session.get("rotation_count", 0) + 1
            })
            
            # Tunggu sebentar sebelum retry
            await asyncio.sleep(random.uniform(10, 20))
            
            # Coba create lagi dengan IP baru
            return await self._create_instagram_account(session_id, email, username, password, signup_code)
            
        except Exception as e:
            print(f"{merah}❌  IP rotation failed: {e}{reset}")
            return False
    
    def _generate_birthdate(self) -> Tuple[str, str, str]:
        """Generate birthdate untuk Indonesia"""
        current_year = datetime.now().year
        
        # Distribusi usia di Indonesia (lebih muda)
        age = random.choices(
            [random.randint(18, 25), random.randint(26, 35), random.randint(36, 45)],
            weights=[0.6, 0.3, 0.1]
        )[0]
        
        year = current_year - age
        month = random.randint(1, 12)
        
        # Handle days in month
        if month in [1, 3, 5, 7, 8, 10, 12]:
            day = random.randint(1, 31)
        elif month in [4, 6, 9, 11]:
            day = random.randint(1, 30)
        else:
            day = random.randint(1, 28)  # February
        
        return str(month), str(day), str(year)
    
    async def _verify_account_creation(self, session_id: str, username: str) -> bool:
        """Verifikasi akun berhasil dibuat"""
        print(f"{cyan}🔍  Verifying account creation...{reset}")
        
        try:
            # Coba akses profile page
            response = await self.request_orchestrator.make_request(
                session_id=session_id,
                method="GET",
                url=f"https://www.instagram.com/{username}/",
                headers={
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
                }
            )
            
            if response.get("status") == 200:
                body = response.get("body", b"").decode('utf-8', errors='ignore')
                
                # Check tanda akun valid
                if username in body and "profile_pic_url" in body:
                    print(f"{hijau}✅  Account verified and active{reset}")
                    return True
                else:
                    print(f"{kuning}⚠️   Account created but profile not fully accessible{reset}")
                    return True  # Masih consider success
            else:
                print(f"{kuning}⚠️   Could not verify account (HTTP {response.get('status')}){reset}")
                return True  # Assume success
            
        except Exception as e:
            print(f"{merah}❌  Error verifying account: {e}{reset}")
            return False
    
    async def _post_creation_actions(self, session_id: str, username: str):
        """Aksi setelah pembuatan akun"""
        print(f"{cyan}✨  Performing post-creation actions...{reset}")
        
        try:
            session = self.session_manager.get_session(session_id)
            if not session:
                return
            
            # Update profile (simulasi)
            # print(f"    Setting up profile for @{username}")
            
            # Like beberapa post
            # print("    Liking some posts...")
            
            # Follow beberapa akun
            # print("    Following suggested accounts...")
            
            # Simulate human delay
            await asyncio.sleep(random.uniform(5, 15))
            
            print(f"{hijau}✅  Post-creation actions complete{reset}\n")
            
        except Exception as e:
            print(f"{merah}❌  Error in post-creation actions: {e}{reset}\n")
    
    def _record_success(self, attempt_id: str, account_data: Dict[str, Any]) -> Dict[str, Any]:
        """Record successful account creation"""
        self.stats["successful"] += 1
        self.successful_accounts.append(account_data)
        
        result = {
            "status": "success",
            "attempt_id": attempt_id,
            "account": account_data,
            "timestamp": time.time(),
            "message": "Account created successfully"
        }
        
        # Save to file
        self._save_account_to_file(account_data)
        
        # print(f"{bg_hijau}{putih}🎉  ACCOUNT CREATION SUCCESSFUL!{reset}")
        # print(f"    Username: {account_data['username']}")
        # print(f"    Email: {account_data['email']}")
        # print(f"    Session: {account_data['session_id']}")
        
        return result
    
    def _record_failure(self, attempt_id: str, reason: str, error_type: str = "unknown") -> Dict[str, Any]:
        """Record failed account creation
        
        Args:
            attempt_id: Unique attempt identifier
            reason: Human readable reason
            error_type: Machine readable type (ip_block, checkpoint, rate_limit, unknown)
        """
        self.stats["failed"] += 1
        self.failed_accounts.append({
            "attempt_id": attempt_id,
            "reason": reason,
            "error_type": error_type,
            "timestamp": time.time()
        })
        
        result = {
            "status": "failed",
            "attempt_id": attempt_id,
            "reason": reason,
            "error_type": error_type,  # ADDED: for session management detection
            "timestamp": time.time(),
            "message": f"Account creation failed: {reason}"
        }
        
        print(f"{bg_merah}{putih}❌  ACCOUNT CREATION FAILED{reset}")
        print(f"    Reason: {reason}")
        
        return result
    
    def _save_account_to_file(self, account_data: Dict[str, Any]):
        """Save account data to file"""
        try:
            filename = "accounts_2025.txt"
            
            with open(filename, "a", encoding="utf-8") as f:
                f.write(f"{account_data['username']}|{account_data['password']}|"
                       f"{account_data['email']}|{account_data['session_id']}|"
                       f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}|Indonesia\n")
            
            print(f"{cyan}💾  Account saved to {filename}{reset}")
            
        except Exception as e:
            print(f"{merah}❌  Failed to save account: {e}{reset}")
    
    async def batch_create_accounts(self, count: int, password: str) -> Dict[str, Any]:
        """Buat beberapa akun sekaligus dengan smart session strategy
        
        STRATEGY:
        1. Akun BERHASIL → terus pakai session sampai 2x checkpoint
        2. Akun CHECKPOINT → coba sekali lagi, jika masih checkpoint ganti session  
        3. IP BLOCK → langsung ganti session
        """
        print(f"{cyan}🏭  Starting batch creation of {count} accounts{reset}")
        print(f"{cyan}    Strategy:{reset}")
        print(f"{cyan}    - Success: keep using until 2 checkpoints{reset}")
        print(f"{cyan}    - Checkpoint: retry once, if still checkpoint rotate{reset}")
        print(f"{cyan}    - IP Block: immediate rotate{reset}")
        
        results = {
            "total": count,
            "successful": 0,
            "failed": 0,
            "checkpointed": 0,
            "accounts": [],
            "errors": [],
            "start_time": time.time(),
            "sessions_used": 0,
            "ip_blocks": 0
        }
        
        # Session tracking
        current_session_id = None
        session_success_count = 0       # Total successes in current session
        session_checkpoint_count = 0    # Total checkpoints in current session
        consecutive_checkpoints = 0     # Consecutive checkpoints (reset on success)
        force_new_session = False       # Flag to force new session
        
        for i in range(count):
            print(f"\n{biru}🔹  Account {i + 1}/{count}{reset}")
            
            # Decide whether to create new session or reuse
            need_new_session = False
            
            if current_session_id is None or force_new_session:
                need_new_session = True
                if force_new_session:
                    print(f"{kuning}🔄  Forced session rotation...{reset}")
                else:
                    print(f"{cyan}🆕  No active session, creating new one...{reset}")
                force_new_session = False  # Reset flag
            
            if need_new_session:
                current_session_id = await self._create_new_session()
                session_success_count = 0
                session_checkpoint_count = 0
                consecutive_checkpoints = 0
                results["sessions_used"] += 1
                
                if not current_session_id:
                    print(f"{merah}❌  Failed to create session, retrying...{reset}")
                    await asyncio.sleep(5)
                    current_session_id = await self._create_new_session()
                    results["sessions_used"] += 1
                    if not current_session_id:
                        results["failed"] += 1
                        results["errors"].append({"error": "Session creation failed", "account": i + 1})
                        continue
            else:
                print(f"{hijau}♻️   Reusing session (success: {session_success_count}, checkpoints: {session_checkpoint_count}){reset}")
            
            # Create account with current session
            result = await self.create_account(password, session_id=current_session_id)
            
            if result["status"] == "success":
                results["successful"] += 1
                results["accounts"].append(result["account"])
                session_success_count += 1
                consecutive_checkpoints = 0  # Reset consecutive checkpoints on success
                print(f"{hijau}✅  Success! Session stats: {session_success_count} success, {session_checkpoint_count} checkpoints{reset}")
                
                # Short cooldown after success (same session)
                if i < count - 1:
                    cooldown = random.uniform(15, 30)
                    print(f"{kuning}⏳  Short cooldown (same session): {cooldown:.1f}s{reset}")
                    await asyncio.sleep(cooldown)
            else:
                results["failed"] += 1
                results["errors"].append(result)
                
                # Get error type directly from result (IMPROVED)
                error_type = result.get("error_type", "unknown")
                error_msg = str(result.get("reason", result.get("error", ""))).lower()
                
                # Check if IP block FIRST (higher priority)
                is_ip_block = (
                    error_type == "ip_block" or
                    "ip_block" in error_msg or
                    "ip block" in error_msg or
                    "ipblock" in error_msg or
                    "rate limit" in error_msg or
                    "rate_limit" in error_msg or
                    "429" in error_msg or
                    "403" in error_msg or
                    "too many" in error_msg
                )
                
                # Check if checkpoint (only if NOT ip block)
                is_checkpoint = not is_ip_block and (
                    error_type == "checkpoint" or
                    "checkpoint" in error_msg or
                    "suspended" in error_msg
                )
                
                if is_ip_block:
                    # IP BLOCK - IMMEDIATELY rotate session, no retry
                    print(f"{merah}🚫  IP BLOCK detected (error_type={error_type}) - IMMEDIATE session rotation{reset}")
                    results["ip_blocks"] += 1
                    force_new_session = True
                    current_session_id = None
                    
                    # Extra cooldown for IP block
                    block_cooldown = random.uniform(60, 90)
                    print(f"{kuning}⏳  IP block cooldown: {block_cooldown:.1f}s{reset}")
                    await asyncio.sleep(block_cooldown)
                    
                elif is_checkpoint:
                    print(f"{kuning}🚧  Checkpoint detected{reset}")
                    results["checkpointed"] += 1
                    session_checkpoint_count += 1
                    consecutive_checkpoints += 1
                    
                    # STRATEGY:
                    # - Jika sudah ada success sebelumnya: terus sampai 2 total checkpoints
                    # - Jika belum ada success: 2 consecutive checkpoints = rotate
                    
                    if session_success_count > 0:
                        # Ada success sebelumnya - terus sampai 2 total checkpoint
                        if session_checkpoint_count >= 2:
                            print(f"{merah}    Session had {session_success_count} success, now hit 2 checkpoints - rotating...{reset}")
                            force_new_session = True
                            current_session_id = None
                            checkpoint_cooldown = random.uniform(45, 75)
                        else:
                            print(f"{kuning}    Session has {session_success_count} success, checkpoint {session_checkpoint_count}/2 - continuing...{reset}")
                            checkpoint_cooldown = random.uniform(30, 45)
                    else:
                        # Belum ada success - 2 consecutive checkpoint = rotate
                        if consecutive_checkpoints >= 2:
                            print(f"{merah}    2 consecutive checkpoints without success - rotating...{reset}")
                            force_new_session = True
                            current_session_id = None
                            checkpoint_cooldown = random.uniform(45, 75)
                        else:
                            print(f"{kuning}    First checkpoint, will try once more...{reset}")
                            checkpoint_cooldown = random.uniform(30, 45)
                    
                    print(f"{kuning}⏳  Checkpoint cooldown: {checkpoint_cooldown:.1f}s{reset}")
                    await asyncio.sleep(checkpoint_cooldown)
                else:
                    # Other failure - show error_type for debugging
                    print(f"{kuning}    Other failure (error_type={error_type}), normal cooldown{reset}")
                    cooldown = random.uniform(20, 40)
                    print(f"{kuning}⏳  Cooldown: {cooldown:.1f}s{reset}")
                    await asyncio.sleep(cooldown)
        
        results["end_time"] = time.time()
        results["duration"] = results["end_time"] - results["start_time"]
        results["success_rate"] = results["successful"] / count if count > 0 else 0
        
        print(f"\n{bg_biru}{putih}📊  BATCH CREATION COMPLETE{reset}")
        print(f"    Successful: {results['successful']}/{count}")
        print(f"    Checkpointed: {results['checkpointed']}")
        print(f"    Failed: {results['failed']}/{count}")
        print(f"    Success rate: {results['success_rate']:.1%}")
        print(f"    Sessions used: {results['sessions_used']}")
        print(f"    IP blocks: {results['ip_blocks']}")
        print(f"    Duration: {results['duration']:.1f}s")
        
        return results
    
    def get_statistics(self) -> Dict[str, Any]:
        """Dapatkan statistik"""
        total_time = time.time() - self.stats["start_time"]
        
        stats = {
            **self.stats,
            "total_time": total_time,
            "success_rate": self.stats["successful"] / self.stats["total_attempts"] if self.stats["total_attempts"] > 0 else 0,
            "accounts_per_hour": (self.stats["successful"] / total_time) * 3600 if total_time > 0 else 0,
            "successful_accounts": len(self.successful_accounts),
            "failed_accounts": len(self.failed_accounts),
            "email_cache_size": len(self.email_manager.email_cache),
            "active_sessions": len(self.session_manager.sessions)
        }
        
        return stats
    
    async def cleanup(self):
        """Cleanup resources"""
        print(f"{cyan}🧹  Cleaning up resources...{reset}")
        
        try:
            # Close all email sessions
            if self.email_manager:
                await self.email_manager.cleanup_all_sessions()
            
            if self.request_orchestrator:
                await self.request_orchestrator.shutdown()
            
            # Cleanup email cache
            self.email_manager.cleanup_old_emails()
            
            print(f"{hijau}✅  Cleanup complete{reset}")
            
        except Exception as e:
            print(f"{merah}❌  Error during cleanup: {e}{reset}")

# ===================== MAIN SYSTEM INTEGRATION 2025 =====================

class UltraBoostedV13_2025:
    """Sistem utama Ultra Boosted V13 2025 dengan semua integrasi"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = self._load_config(config)
        self.running = False
        # self.account_creator = None
        self.session_manager = None
        self.request_orchestrator = None

        print(f"{cyan}⚙️   CONFIG LOADED:{reset}")
        print(f"    email_service: {self.config.get('email_service')}")
        print(f"    device_type: {self.config.get('device_type')}")
        
        # Initialize account creator dengan config yang BENAR
        self.account_creator = InstagramAccountCreator2025(self.config)
        
        # Initialize colorama
        init(autoreset=True)
        
        # Setup logging
        self._setup_logging()
        
        print(f"{hijau}🚀  Ultra Boosted V13 2025 Initialized{reset}")
    
    def _load_config(self, config: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """Load configuration"""
        default_config = {
            "use_proxy": False,
            "proxy_list": [],
            "max_concurrent": 3,
            "max_retries": 3,
            "request_timeout": 30,
            "email_service": "auto",
            "location": "ID",
            "device_type": "desktop",
            "verbose": True,
            "save_sessions": True,
            "session_file": "sessions_2025.json",
            "accounts_file": "accounts_2025.txt",
            "log_file": "ultraboosted_2025.log",
            "auto_cleanup": True,
            "cooldown_between_accounts": (30, 60),
            "rate_limit_strategy": "adaptive",
            "fingerprint_rotation": True,
            "behavior_simulation": True,
            "anti_detection": True,
            "cloudflare_bypass": True
        }
        
        if config:
            default_config.update(config)
        
        return default_config
    
    def _setup_logging(self):
        """Setup logging system"""
        log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        
        # File handler
        file_handler = logging.FileHandler(self.config["log_file"])
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(logging.Formatter(log_format))
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO if self.config["verbose"] else logging.WARNING)
        console_handler.setFormatter(logging.Formatter(log_format))
        
        # Setup root logger
        logging.basicConfig(
            level=logging.INFO,
            handlers=[file_handler, console_handler],
            format=log_format
        )
        
        self.logger = logging.getLogger("UltraBoostedV13_2025")
    
    async def initialize(self):
        """Initialize semua sistem"""
        try:
            print(f"{cyan}⚙️   Initializing Ultra Boosted V13 2025...{reset}")
            
            # Initialize account creator
            self.account_creator = InstagramAccountCreator2025(self.config)
            
            # Initialize account creator systems
            await self.account_creator.initialize()
            
            # Get references to internal systems
            self.session_manager = self.account_creator.session_manager
            self.request_orchestrator = self.account_creator.request_orchestrator
            
            # Load existing sessions if any
            if self.config["save_sessions"] and os.path.exists(self.config["session_file"]):
                await self._load_sessions_from_file()
            
            self.running = True
            
            print(f"{hijau}✅  Ultra Boosted V13 2025 Initialized Successfully{reset}")
            print(f"{cyan}📊  Configuration:{reset}")
            print(f"    Location: {self.config['location']}")
            print(f"    Device Type: {self.config['device_type']}")
            print(f"    Email Service: {self.config['email_service']}")
            print(f"    Max Concurrent: {self.config['max_concurrent']}")
            print(f"    Anti-Detection: {self.config['anti_detection']}")
            
            return True
            
        except Exception as e:
            print(f"{merah}❌  Initialization failed: {e}{reset}")
            import traceback
            traceback.print_exc()
            return False
    
    async def _load_sessions_from_file(self):
        """Load sessions from file"""
        try:
            with open(self.config["session_file"], 'r', encoding='utf-8') as f:
                sessions_data = json.load(f)
            
            loaded_count = 0
            for session_id, session_data in sessions_data.items():
                # Create session from saved data
                new_session_id = self.session_manager.create_session(
                    fingerprint=session_data.get("fingerprint", {}),
                    behavior_profile=session_data.get("behavior_profile", {}),
                    ip_config=session_data.get("ip_config", {})
                )
                
                # Update with saved data
                updates = {}
                for key in ["request_count", "success_count", "failure_count", 
                           "state", "tokens", "cookies", "headers", "metadata"]:
                    if key in session_data:
                        updates[key] = session_data[key]
                
                self.session_manager.update_session(new_session_id, updates)
                loaded_count += 1
            
            print(f"{hijau}✅  Loaded {loaded_count} sessions from {self.config['session_file']}{reset}")
            
        except Exception as e:
            print(f"{merah}❌  Failed to load sessions: {e}{reset}")
    
    async def save_sessions_to_file(self):
        """Save sessions to file"""
        if not self.config["save_sessions"]:
            return
        
        try:
            sessions_data = {}
            
            for session_id, session in self.session_manager.sessions.items():
                # Only save active sessions
                if session.get("state") == "active":
                    sessions_data[session_id] = {
                        "fingerprint": session.get("fingerprint", {}),
                        "behavior_profile": session.get("behavior_profile", {}),
                        "ip_config": session.get("ip_config", {}),
                        "request_count": session.get("request_count", 0),
                        "success_count": session.get("success_count", 0),
                        "failure_count": session.get("failure_count", 0),
                        "state": session.get("state", "active"),
                        "tokens": session.get("tokens", {}),
                        "cookies": session.get("cookies", {}),
                        "headers": session.get("headers", {}),
                        "metadata": session.get("metadata", {}),
                        "saved_at": time.time()
                    }
            
            with open(self.config["session_file"], 'w', encoding='utf-8') as f:
                json.dump(sessions_data, f, ensure_ascii=False, indent=2)
            
            print(f"{hijau}✅  Saved {len(sessions_data)} sessions to {self.config['session_file']}{reset}")
            
        except Exception as e:
            print(f"{merah}❌  Failed to save sessions: {e}{reset}")
    
    async def create_single_account(self, password: str, 
                                  username_hint: Optional[str] = None) -> Dict[str, Any]:
        """Create single Instagram account"""
        if not self.running or not self.account_creator:
            return {"status": "error", "message": "System not initialized"}
        
        print(f"\n{biru}🎯  STARTING SINGLE ACCOUNT CREATION{reset}")
        
        try:
            result = await self.account_creator.create_account(
                password=password,
                username_hint=username_hint
            )
            
            # Save sessions setelah pembuatan akun
            await self.save_sessions_to_file()
            
            return result
            
        except Exception as e:
            error_msg = f"Account creation failed: {str(e)}"
            print(f"{merah}❌  {error_msg}{reset}")
            return {"status": "error", "message": error_msg}
    
    async def create_batch_accounts(self, count: int, password: str) -> Dict[str, Any]:
        """Create batch Instagram accounts"""
        if not self.running or not self.account_creator:
            return {"status": "error", "message": "System not initialized"}
        
        print(f"\n{biru}🏭  STARTING BATCH ACCOUNT CREATION ({count} accounts){reset}")
        
        try:
            result = await self.account_creator.batch_create_accounts(
                count=count,
                password=password
            )
            
            # Save sessions setelah batch creation
            await self.save_sessions_to_file()
            
            return result
            
        except Exception as e:
            error_msg = f"Batch creation failed: {str(e)}"
            print(f"{merah}❌  {error_msg}{reset}")
            return {"status": "error", "message": error_msg}
    
    async def test_fingerprint_system(self) -> Dict[str, Any]:
        """Test fingerprint generation system"""
        print(f"{cyan}🧪  Testing fingerprint system...{reset}")
        
        try:
            # Generate test fingerprint
            fingerprint = self.account_creator.fingerprint_system.generate_fingerprint(
                device_type=self.config["device_type"],
                location=self.config["location"]
            )
            
            # Validate fingerprint
            validation = self.account_creator.fingerprint_system.validate_fingerprint(fingerprint)
            
            # Generate WebRTC/WebGL fingerprint
            webrtc_fingerprint = self.account_creator.web_system.get_complete_fingerprint(
                device_type=self.config["device_type"]
            )
            
            return {
                "status": "success",
                "fingerprint": {
                    "device_type": fingerprint.get("device_type"),
                    "device_model": fingerprint.get("device", {}).get("model"),
                    "os_version": fingerprint.get("os", {}).get("version"),
                    "browser": fingerprint.get("browser", {}).get("name"),
                    "location": fingerprint.get("location", {}).get("city"),
                    "validation_score": validation.get("overall_score", 0)
                },
                "webrtc_fingerprint": {
                    "has_webrtc": "webrtc" in webrtc_fingerprint,
                    "has_webgl": "webgl" in webrtc_fingerprint,
                    "has_canvas": "canvas" in webrtc_fingerprint
                },
                "message": "Fingerprint system working correctly"
            }
            
        except Exception as e:
            return {"status": "error", "message": f"Fingerprint test failed: {str(e)}"}
    
    async def test_email_service(self, service: str = "mailtm") -> Dict[str, Any]:
        """Test email service"""
        print(f"{cyan}📧  Testing email service ({service})...{reset}")
        
        try:
            email_data = await self.account_creator.email_manager.get_email(service)
            
            if email_data:
                return {
                    "status": "success",
                    "service": service,
                    "email": email_data.get("email"),
                    "message": f"Email service {service} working correctly"
                }
            else:
                return {
                    "status": "error", 
                    "service": service,
                    "message": f"Failed to get email from {service}"
                }
                
        except Exception as e:
            return {"status": "error", "message": f"Email service test failed: {str(e)}"}
    
    async def test_ip_system(self) -> Dict[str, Any]:
        """Test IP stealth system"""
        print(f"{cyan}🌐  Testing IP stealth system...{reset}")
        
        try:
            ip_config = self.account_creator.ip_system.get_stealth_ip_config()
            
            return {
                "status": "success",
                "ip": ip_config.get("ip"),
                "isp": ip_config.get("isp"),
                "asn": ip_config.get("asn"),
                "location": ip_config.get("location", {}).get("city"),
                "ttl": ip_config.get("ttl"),
                "ja3": ip_config.get("ja3")[:20] + "..." if ip_config.get("ja3") else None,
                "message": "IP stealth system working correctly"
            }
            
        except Exception as e:
            return {"status": "error", "message": f"IP system test failed: {str(e)}"}
    
    async def run_diagnostics(self) -> Dict[str, Any]:
        """Run comprehensive system diagnostics"""
        print(f"\n{biru}🔧  RUNNING SYSTEM DIAGNOSTICS{reset}")
        
        diagnostics = {
            "timestamp": time.time(),
            "system_status": "running" if self.running else "stopped",
            "tests": [],
            "overall_status": "pending"
        }
        
        # Test 1: Fingerprint system
        print(f"{cyan}1. Testing fingerprint system...{reset}")
        fp_test = await self.test_fingerprint_system()
        diagnostics["tests"].append({"name": "fingerprint", "result": fp_test})
        
        # Test 2: Email service
        print(f"{cyan}2. Testing email service...{reset}")
        email_test = await self.test_email_service("mailtm")
        diagnostics["tests"].append({"name": "email", "result": email_test})
        
        # Test 3: IP system
        print(f"{cyan}3. Testing IP system...{reset}")
        ip_test = await self.test_ip_system()
        diagnostics["tests"].append({"name": "ip", "result": ip_test})
        
        # Test 4: Session manager
        print(f"{cyan}4. Testing session manager...{reset}")
        session_stats = self.session_manager.get_session_statistics() if self.session_manager else {}
        diagnostics["tests"].append({
            "name": "session_manager", 
            "result": {"status": "success", "stats": session_stats}
        })
        
        # Test 5: Request orchestrator
        print(f"{cyan}5. Testing request orchestrator...{reset}")
        queue_status = self.request_orchestrator.get_queue_status() if self.request_orchestrator else {}
        diagnostics["tests"].append({
            "name": "request_orchestrator", 
            "result": {"status": "success", "queue_status": queue_status}
        })
        
        # Determine overall status
        failed_tests = [t for t in diagnostics["tests"] if t["result"].get("status") == "error"]
        
        if len(failed_tests) == 0:
            diagnostics["overall_status"] = "healthy"
            print(f"{hijau}✅  All diagnostic tests passed{reset}")
        elif len(failed_tests) <= 2:
            diagnostics["overall_status"] = "warning"
            print(f"{kuning}⚠️   Some diagnostic tests failed{reset}")
        else:
            diagnostics["overall_status"] = "critical"
            print(f"{merah}❌  Multiple diagnostic tests failed{reset}")
        
        # Print summary
        print(f"\n{biru}📊  DIAGNOSTICS SUMMARY{reset}")
        for test in diagnostics["tests"]:
            status = test["result"].get("status", "unknown")
            if status == "success":
                print(f"    {hijau}✓ {test['name']}{reset}")
            elif status == "error":
                print(f"    {merah}✗ {test['name']}{reset}")
            else:
                print(f"    {kuning}? {test['name']}{reset}")
        
        return diagnostics
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get current system status dengan IP statistics"""
        if not self.running:
            return {"status": "stopped", "message": "System not running"}
        
        stats = self.account_creator.get_statistics() if self.account_creator else {}
        
        # Get IP pool statistics
        ip_stats = {}
        if hasattr(self.account_creator, 'ip_system'):
            ip_stats = self.account_creator.ip_system.get_ip_pool_stats()
        
        session_stats = self.session_manager.get_session_statistics() if self.session_manager else {}
        queue_status = self.request_orchestrator.get_queue_status() if self.request_orchestrator else {}
        
        return {
            "status": "running",
            "uptime": time.time() - (stats.get("start_time", time.time())),
            "statistics": stats,
            "ip_statistics": ip_stats,
            "session_statistics": session_stats,
            "queue_status": queue_status,
            "config": {
                "location": self.config["location"],
                "device_type": self.config["device_type"],
                "email_service": self.config["email_service"],
                "max_concurrent": self.config["max_concurrent"]
            }
        }
    
    async def cleanup(self):
        """Cleanup semua resources"""
        print(f"{cyan}🧹  Cleaning up system resources...{reset}")
        
        try:
            if self.account_creator:
                await self.account_creator.cleanup()
            
            # Save sessions sebelum shutdown
            await self.save_sessions_to_file()
            
            self.running = False
            
            print(f"{hijau}✅  System cleanup complete{reset}")
            
        except Exception as e:
            print(f"{merah}❌  Error during cleanup: {e}{reset}")

# ===================== CLI INTERFACE =====================

class CLIInterface:
    """Command Line Interface untuk Ultra Boosted V13 2025 - DIPERBAIKI"""
    
    def __init__(self):
        self.system = None
        self.current_password = None
        self.running = False
        self.email_services_map = self._init_email_services_map()
        
    def _init_email_services_map(self) -> Dict[str, str]:
        """Initialize email services mapping yang BENAR"""
        return {
            "1": "1secmail",      # ⭐ Paling reliable
            "2": "10minutemail",  # Cepat
            "3": "mailtm",        # API support
            "4": "auto",          # System chooses
            "5": "tempmail_plus", # Alternatif
            "6": "cmail",         # Backup
            "7": "guerrillamail"  # Last resort
        }
    
    async def run(self):
        """Run CLI interface"""
        self._show_banner()
        
        try:
            # Initialize system
            await self._initialize_system()
            
            # Main menu loop
            while self.running:
                choice = self._show_main_menu()
                await self._handle_menu_choice(choice)
                
        except KeyboardInterrupt:
            print(f"\n{kuning}⚠️   Interrupted by user{reset}")
        except Exception as e:
            print(f"{merah}❌  Error: {e}{reset}")
            import traceback
            traceback.print_exc()
        finally:
            await self._shutdown()
    
    def _show_banner(self):
        """Show banner dengan informasi lebih lengkap"""
        os.system('cls' if os.name == 'nt' else 'clear')
        
        banner = f"""
{biru}╔══════════════════════════════════════════════════════════════╗
║{putih}      ULTRA BOOSTED V13 2025 - INDONESIA EDITION       {biru}      ║
║{putih}         Advanced Instagram Account Creator            {biru}      ║
║{putih}     Dynamic IP System • 8 Email Services • Anti-Detection {biru}  ║
╚══════════════════════════════════════════════════════════════╝{reset}

{cyan}Version:{reset} 2025.1.0 | {cyan}Location:{reset} Indonesia 🇮🇩 | {cyan}Mode:{reset} Advanced
{cyan}Email Services:{reset} 8 Active Services | {cyan}IP System:{reset} Dynamic Generation
{merah}──────────────────────────────────────────────────────────────{reset}
        """
        print(banner)
    
    async def _initialize_system(self):
        """Initialize system dengan konfigurasi yang lebih baik"""
        print(f"{cyan}⚙️   Initializing Ultra Boosted V13 2025...{reset}")
        
        config = await self._get_configuration()
        
        self.system = UltraBoostedV13_2025(config)
        
        # Show initialization progress
        print(f"{cyan}    Loading systems...{reset}")
        
        success = await self.system.initialize()
        if not success:
            print(f"{merah}❌  System initialization failed{reset}")
            raise Exception("System initialization failed")
        
        self.running = True
        print(f"{hijau}✅  System ready with {config.get('email_service', 'auto')} email service{reset}")
    
    async def _get_configuration(self) -> Dict[str, Any]:
        """Get configuration dengan email service selection yang jelas"""
        config = {}
        
        print(f"\n{cyan}📋  EMAIL SERVICE CONFIGURATION{reset}")
        print(f"{merah}───────────────────────────────{reset}")
        
        print(f"\n{putih}Select email service mode:{reset}")
        print(f"  1. {hijau}Auto Mode (Recommended){reset} - System chooses best (10minutemail → GuerrillaMail)")
        print(f"  2. {hijau}Manual: 10minutemail{reset} - Fast, 10 min expiry")
        print(f"  3. {hijau}Manual: GuerrillaMail{reset} - Reliable fallback")
        print(f"  4. {hijau}Manual: 1secmail{reset} - No API needed")
        print(f"  5. {hijau}Manual: Mail.tm{reset} - API support")
        
        service_choice = input(f"\n{cyan}Choice (1-5, default 1): {reset}").strip()
        if service_choice == "":
            service_choice = "1"
        
        service_map = {
            "1": "auto",
            "2": "10minutemail",
            "3": "guerrillamail",
            "4": "1secmail",
            "5": "mailtm"
        }
        
        config["email_service"] = service_map.get(service_choice, "auto")
        
        if config["email_service"] == "auto":
            print(f"\n{hijau}✅  Auto mode selected: Priority: 10minutemail → GuerrillaMail → 1secmail → ...{reset}")
        else:
            print(f"\n{hijau}✅  Manual mode selected: {config['email_service']} (fallback to GuerrillaMail if failed){reset}")
        
        return config
    
    def _show_main_menu(self) -> str:
        """Show main menu dengan lebih banyak opsi"""
        print(f"\n{biru}╔══════════════════════════════════════════════════════════════╗")
        print(f"║{putih}                       MAIN MENU                         {biru}      ║")
        print(f"╚══════════════════════════════════════════════════════════════╝{reset}")
        
        # Get system status untuk display
        status = "RUNNING" if self.running and self.system else "STOPPED"
        status_color = hijau if status == "RUNNING" else merah
        
        print(f"{cyan}System Status: {status_color}{status}{reset}")
        
        if self.system and self.running:
            stats = self.system.get_system_status()
            if stats.get("status") == "running":
                success_rate = stats.get("statistics", {}).get("success_rate", 0)
                print(f"{cyan}Success Rate: {hijau if success_rate >= 0.5 else kuning if success_rate >= 0.3 else merah}{success_rate:.1%}{reset}")
        
        print(f"\n{putih}ACCOUNT CREATION{reset}")
        print(f"{merah}────────────────{reset}")
        print(f"  1. {hijau}Create Single Account{reset}")
        print(f"  2. {hijau}Create Batch Accounts{reset}")
        
        print(f"\n{putih}SYSTEM TOOLS{reset}")
        print(f"{merah}─────────────{reset}")
        print(f"  3. {cyan}Run Diagnostics{reset}")
        print(f"  4. {kuning}View System Status{reset}")
        print(f"  5. {merah}Test Systems{reset}")
        print(f"  6. {putih}Change Settings{reset}")
        
        print(f"\n{putih}ADVANCED{reset}")
        print(f"{merah}────────{reset}")
        print(f"  7. {biru}View Created Accounts{reset}")
        print(f"  8. {biru}Email Service Stats{reset}")
        print(f"  9. {biru}IP Pool Management{reset}")
        
        print(f"\n{putih}SYSTEM{reset}")
        print(f"{merah}───────{reset}")
        print(f"  0. {merah}Exit{reset}")
        
        print(f"\n{merah}──────────────────────────────────────────────────────────────{reset}")
        
        return input(f"\n{cyan}Enter choice (0-9): {reset}").strip()
    
    async def _handle_menu_choice(self, choice: str):
        """Handle menu choice dengan lebih banyak opsi"""
        menu_actions = {
            "1": self._create_single_account,
            "2": self._create_batch_accounts,
            "3": self._run_diagnostics,
            "4": self._view_system_status,
            "5": self._test_systems,
            "6": self._change_settings,
            "7": self._view_created_accounts,
            "8": self._email_service_stats,
            "9": self._ip_pool_management,
            "0": lambda: setattr(self, 'running', False)
        }
        
        action = menu_actions.get(choice)
        if action:
            if choice == "0":
                action()
            else:
                await action()
        else:
            print(f"{merah}❌  Invalid choice{reset}")
    
    async def _create_single_account(self):
        """Create single account dengan progress tracking"""
        print(f"\n{biru}╔══════════════════════════════════════════════════════════════╗")
        print(f"║{putih}                   CREATE SINGLE ACCOUNT                  {biru}      ║")
        print(f"╚══════════════════════════════════════════════════════════════╝{reset}")
        
        # Get password
        password = input(f"\n{cyan}Password: {reset}").strip()
        if not password:
            password = self.current_password
        
        # **FORCE EMAIL SERVICE SELECTION**
        print(f"\n{cyan}📧  EMAIL SERVICE SELECTION (Override){reset}")
        print(f"  1. 1secmail")
        print(f"  2. 10minutemail")
        print(f"  3. Mail.tm")
        print(f"  4. Auto (default)")
        
        service_choice = input(f"{cyan}Select email service (1-4): {reset}").strip()
        
        service_map = {
            "1": "1secmail",
            "2": "10minutemail",
            "3": "mailtm",
            "4": "auto"
        }
        
        selected_service = service_map.get(service_choice, "auto")
        print(f"{cyan}  Using email service: {selected_service}{reset}")
        
        # **OVERRIDE system config**
        if self.system and self.system.account_creator:
            # Temporary override
            self.system.account_creator.email_manager.preferred_service = selected_service
        
        # Continue with account creation
        result = await self.system.create_single_account(
            password=password,
            username_hint=None
        )
        
        return result
    
    async def _create_batch_accounts(self):
        """Create batch accounts dengan progress bar"""
        print(f"\n{biru}╔══════════════════════════════════════════════════════════════╗")
        print(f"║{putih}                   CREATE BATCH ACCOUNTS                  {biru}      ║")
        print(f"╚══════════════════════════════════════════════════════════════╝{reset}")
        
        # Get count
        while True:
            count_input = input(f"\n{cyan}How many accounts to create? (1-50): {reset}").strip()
            if count_input.isdigit() and 1 <= int(count_input) <= 50:
                count = int(count_input)
                break
            else:
                print(f"{merah}Please enter a number between 1 and 50{reset}")
        
        # Get password
        password = input(f"{cyan}Password (press Enter for default): {reset}").strip()
        if not password:
            password = self.current_password
        
        # Estimate time
        est_time = count * 90  # 1.5 minutes per account average
        print(f"\n{kuning}⏱️   Estimated time: {est_time//60} minutes {est_time%60} seconds{reset}")
        
        confirm = input(f"\n{cyan}Start batch creation of {count} accounts? (y/n): {reset}").strip().lower()
        if confirm != "y":
            print(f"{kuning}Cancelled{reset}")
            return
        
        print(f"\n{cyan}🚀  Starting batch creation of {count} accounts...{reset}")
        print(f"{kuning}   Press Ctrl+C to cancel{reset}")
        
        start_time = time.time()
        result = await self.system.create_batch_accounts(
            count=count,
            password=password
        )
        end_time = time.time()
        
        print(f"\n{cyan}⏱️   Total time: {(end_time - start_time)/60:.1f} minutes{reset}")
        self._show_batch_result(result)
    
    async def _run_diagnostics(self):
        """Run diagnostics dengan progress indicator"""
        print(f"\n{biru}╔══════════════════════════════════════════════════════════════╗")
        print(f"║{putih}                     RUN DIAGNOSTICS                     {biru}      ║")
        print(f"╚══════════════════════════════════════════════════════════════╝{reset}")
        
        print(f"\n{cyan}Running comprehensive diagnostics...{reset}")
        print(f"{kuning}This will test all system components{reset}")
        
        result = await self.system.run_diagnostics()
        
        print(f"\n{biru}📊  DIAGNOSTICS RESULTS{reset}")
        print(f"{merah}──────────────────────────────────────────────────────────────{reset}")
        
        overall_status = result.get("overall_status", "unknown")
        
        if overall_status == "healthy":
            print(f"{bg_hijau}{putih} ✅  SYSTEM IS HEALTHY {reset}")
        elif overall_status == "warning":
            print(f"{bg_kuning}{putih} ⚠️   SYSTEM HAS WARNINGS {reset}")
        elif overall_status == "critical":
            print(f"{bg_merah}{putih} ❌  SYSTEM HAS CRITICAL ISSUES {reset}")
        else:
            print(f"{bg_kuning}{putih} ?  SYSTEM STATUS UNKNOWN {reset}")
        
        print(f"\n{cyan}Component Tests:{reset}")
        print(f"{merah}────────────────{reset}")
        
        for test in result.get("tests", []):
            test_name = test.get("name", "unknown")
            test_result = test.get("result", {})
            test_status = test_result.get("status", "unknown")
            
            if test_status == "success":
                print(f"  {hijau}✓ {test_name.upper()}: PASSED{reset}")
                # Show additional info for successful tests
                if test_name == "email":
                    email = test_result.get("email", "N/A")
                    print(f"     {cyan}Email: {email}{reset}")
                elif test_name == "ip":
                    ip = test_result.get("ip", "N/A")
                    print(f"     {cyan}IP: {ip}{reset}")
            elif test_status == "error":
                print(f"  {merah}✗ {test_name.upper()}: FAILED{reset}")
                print(f"     {kuning}Reason: {test_result.get('message', 'No message')}{reset}")
            else:
                print(f"  {kuning}? {test_name.upper()}: UNKNOWN{reset}")
        
        # Recommendations
        if overall_status != "healthy":
            print(f"\n{cyan}Recommendations:{reset}")
            print(f"{merah}────────────────{reset}")
            
            if overall_status == "critical":
                print(f"  1. {hijau}Check internet connection{reset}")
                print(f"  2. {hijau}Restart the application{reset}")
                print(f"  3. {hijau}Verify all dependencies are installed{reset}")
            elif overall_status == "warning":
                print(f"  1. {hijau}Consider changing email service{reset}")
                print(f"  2. {hijau}Rotate IP addresses{reset}")
                print(f"  3. {hijau}Increase cooldown times{reset}")
    
    def _view_system_status(self):
        """View system status dengan informasi lebih detail"""
        if not self.system:
            print(f"{merah}❌  System not initialized{reset}")
            return
            
        status = self.system.get_system_status()
        
        print(f"\n{biru}╔══════════════════════════════════════════════════════════════╗")
        print(f"║{putih}                    SYSTEM STATUS                        {biru}      ║")
        print(f"╚══════════════════════════════════════════════════════════════╝{reset}")
        
        if status["status"] == "stopped":
            print(f"{merah}❌  System is not running{reset}")
            return
        
        stats = status.get("statistics", {})
        ip_stats = status.get("ip_statistics", {})
        
        # Header dengan status color
        success_rate = stats.get("success_rate", 0)
        if success_rate >= 0.7:
            status_color = hijau
            status_text = "EXCELLENT"
        elif success_rate >= 0.5:
            status_color = cyan
            status_text = "GOOD"
        elif success_rate >= 0.3:
            status_color = kuning
            status_text = "FAIR"
        else:
            status_color = merah
            status_text = "POOR"
        
        print(f"\n{status_color}📈  PERFORMANCE: {status_text} ({success_rate:.1%} success rate){reset}")
        print(f"{merah}──────────────────────────────────────────────────────────────{reset}")
        
        # Performance metrics
        metrics = [
            ("Total Attempts", stats.get('total_attempts', 0), ""),
            ("Successful", stats.get('successful', 0), hijau),
            ("Failed", stats.get('failed', 0), merah),
            ("Rate Limited", stats.get('rate_limited', 0), kuning),
            ("Uptime", self._format_duration(stats.get('total_time', 0)), cyan),
            ("Accounts/Hour", f"{stats.get('accounts_per_hour', 0):.1f}", cyan)
        ]
        
        for name, value, color in metrics:
            display_value = value if color == "" else f"{color}{value}{reset}"
            print(f"  {putih}{name:<20}{reset}: {display_value}")
        
        # IP Pool Statistics
        if ip_stats:
            print(f"\n{cyan}🌐  IP POOL STATISTICS{reset}")
            print(f"{merah}──────────────────────{reset}")
            
            ip_metrics = [
                ("Total IPs", ip_stats.get('total_ips', 0)),
                ("Healthy IPs", ip_stats.get('healthy_ips', 0)),
                ("Blacklisted IPs", ip_stats.get('blacklisted_ips', 0)),
                ("Health Rate", ip_stats.get('health_rate', '0%')),
                ("Avg Health Score", ip_stats.get('avg_health_score', '0%'))
            ]
            
            for name, value in ip_metrics:
                print(f"  {putih}{name:<20}{reset}: {value}")
            
            # ISP Distribution
            isp_dist = ip_stats.get('isp_distribution', {})
            if isp_dist:
                print(f"\n  {putih}ISP Distribution:{reset}")
                for isp, count in isp_dist.items():
                    percentage = (count / ip_stats.get('total_ips', 1)) * 100
                    bar = "█" * int(percentage / 5)
                    print(f"    {cyan}{isp:<15}{reset}: {count:>3} {bar} {percentage:.0f}%")
        
        # Session Statistics
        session_stats = status.get("session_statistics", {})
        if session_stats:
            print(f"\n{cyan}👥  SESSION STATISTICS{reset}")
            print(f"{merah}─────────────────────{reset}")
            
            session_metrics = [
                ("Active Sessions", session_stats.get('active_sessions', 0)),
                ("Total Requests", session_stats.get('total_requests', 0)),
                ("Success Rate", f"{session_stats.get('success_rate', 0):.1%}"),
                ("Avg Session Age", self._format_duration(session_stats.get('avg_session_age', 0)))
            ]
            
            for name, value in session_metrics:
                print(f"  {putih}{name:<20}{reset}: {value}")
        
        # Configuration
        config = status.get("config", {})
        if config:
            print(f"\n{cyan}⚙️   CONFIGURATION{reset}")
            print(f"{merah}─────────────────{reset}")
            
            config_display = {
                "Location": config.get('location', 'ID'),
                "Device Type": config.get('device_type", "desktop').upper(),
                "Email Service": config.get('email_service', 'auto').upper(),
                "Max Concurrent": config.get('max_concurrent', 2),
                "Anti-Detection": "Maximum" if config.get('request_timeout', 30) > 45 
                                else "Advanced" if config.get('request_timeout', 30) > 30 
                                else "Normal"
            }
            
            for name, value in config_display.items():
                print(f"  {putih}{name:<20}{reset}: {value}")
    
    async def _test_systems(self):
        """Test individual systems dengan pilihan lebih banyak"""
        print(f"\n{biru}╔══════════════════════════════════════════════════════════════╗")
        print(f"║{putih}                      TEST SYSTEMS                        {biru}      ║")
        print(f"╚══════════════════════════════════════════════════════════════╝{reset}")
        
        print(f"\n{putih}Select system to test:{reset}")
        print(f"  1. {hijau}Fingerprint System{reset} - Browser/device simulation")
        print(f"  2. {hijau}Email Service{reset} - Test email providers")
        print(f"  3. {hijau}IP Stealth System{reset} - IP generation & validation")
        print(f"  4. {cyan}WebRTC/WebGL{reset} - Browser fingerprint spoofing")
        print(f"  5. {cyan}Session Manager{reset} - Session handling")
        print(f"  6. {kuning}All Systems{reset} - Comprehensive test")
        
        choice = input(f"\n{cyan}Choice (1-6): {reset}").strip()
        
        if choice == "1":
            result = await self.system.test_fingerprint_system()
            self._show_test_result("Fingerprint System", result)
        elif choice == "2":
            await self._test_email_services()
        elif choice == "3":
            result = await self.system.test_ip_system()
            self._show_test_result("IP Stealth System", result)
        elif choice == "4":
            await self._test_webrtc_system()
        elif choice == "5":
            await self._test_session_manager()
        elif choice == "6":
            await self._test_all_systems()
        else:
            print(f"{merah}Invalid choice{reset}")
    
    async def _test_email_services(self):
        """Test semua email services"""
        print(f"\n{cyan}📧  TESTING ALL EMAIL SERVICES{reset}")
        print(f"{merah}─────────────────────────────{reset}")
        
        services_to_test = ["1secmail", "mailtm", "10minutemail", "tempmail_plus", "cmail", "guerrillamail"]
        results = []
        
        for service in services_to_test:
            print(f"\n{cyan}Testing {service}...{reset}")
            result = await self.system.test_email_service(service)
            results.append((service, result))
            
            if result.get("status") == "success":
                print(f"  {hijau}✓ {service}: OK{reset}")
                email = result.get("email", "N/A")
                print(f"     Email: {email}")
            else:
                print(f"  {merah}✗ {service}: FAILED{reset}")
                print(f"     Error: {result.get('message', 'Unknown error')}")
            
            # Small delay between tests
            await asyncio.sleep(1)
        
        # Summary
        successful = sum(1 for _, r in results if r.get("status") == "success")
        total = len(results)
        
        print(f"\n{biru}📊  EMAIL SERVICE TEST SUMMARY{reset}")
        print(f"{merah}─────────────────────────────{reset}")
        print(f"  {hijau}Successful:{reset} {successful}/{total}")
        print(f"  {merah}Failed:{reset} {total - successful}/{total}")
        print(f"  {cyan}Success Rate:{reset} {successful/total:.1%}")
        
        # Recommendations
        if successful < 3:
            print(f"\n{kuning}⚠️   Warning: Few email services working{reset}")
            print(f"  {cyan}Recommendations:{reset}")
            print(f"    1. Check internet connection")
            print(f"    2. Some services may be blocked in your region")
            print(f"    3. Try using a VPN")
    
    async def _test_webrtc_system(self):
        """Test WebRTC/WebGL system"""
        print(f"\n{cyan}🖥️   TESTING WEBRTC/WEBGL SYSTEM{reset}")
        print(f"{merah}──────────────────────────────{reset}")
        
        # This would test the WebRTCWebGL_Spoofing2025 class
        print(f"{kuning}Feature not fully implemented in CLI{reset}")
        print(f"{cyan}WebRTC/WebGL spoofing is automatically used during account creation{reset}")
    
    async def _test_session_manager(self):
        """Test session manager"""
        print(f"\n{cyan}👥  TESTING SESSION MANAGER{reset}")
        print(f"{merah}─────────────────────────{reset}")
        
        if not self.system or not self.system.session_manager:
            print(f"{merah}❌  Session manager not available{reset}")
            return
        
        stats = self.system.session_manager.get_session_statistics()
        
        print(f"  {putih}Active Sessions:{reset} {stats.get('active_sessions', 0)}")
        print(f"  {putih}Total Requests:{reset} {stats.get('total_requests', 0)}")
        print(f"  {putih}Success Rate:{reset} {stats.get('success_rate', 0):.1%}")
        print(f"  {putih}Avg Session Age:{reset} {self._format_duration(stats.get('avg_session_age', 0))}")
        
        # Show active sessions
        sessions = self.system.session_manager.get_all_sessions(active_only=True)
        if sessions:
            print(f"\n  {putih}Active Sessions:{reset}")
            for session in sessions[:5]:  # Show first 5
                age = self._format_duration(time.time() - session.get('created_at', time.time()))
                print(f"    • {session.get('session_id', 'N/A')[:10]}... - {age} old")
            
            if len(sessions) > 5:
                print(f"    ... and {len(sessions) - 5} more")
    
    async def _test_all_systems(self):
        """Test semua systems secara komprehensif"""
        print(f"\n{biru}🧪  COMPREHENSIVE SYSTEM TEST{reset}")
        print(f"{merah}───────────────────────────{reset}")
        
        print(f"\n{cyan}Starting comprehensive system test...{reset}")
        print(f"{kuning}This may take 1-2 minutes{reset}")
        
        # Run diagnostics (already comprehensive)
        await self._run_diagnostics()
    
    async def _change_settings(self):
        """Change system settings dengan opsi lebih banyak"""
        print(f"\n{biru}╔══════════════════════════════════════════════════════════════╗")
        print(f"║{putih}                    CHANGE SETTINGS                       {biru}      ║")
        print(f"╚══════════════════════════════════════════════════════════════╝{reset}")
        
        print(f"\n{kuning}⚠️   Note: Changing settings may require system restart{reset}")
        
        # Show current settings
        if self.system:
            status = self.system.get_system_status()
            config = status.get("config", {})
            
            print(f"\n{cyan}CURRENT SETTINGS:{reset}")
            print(f"{merah}─────────────────{reset}")
            print(f"  Password: {'*' * len(self.current_password) if self.current_password else 'Not set'}")
            print(f"  Device Type: {config.get('device_type', 'desktop').upper()}")
            print(f"  Email Service: {config.get('email_service', 'auto').upper()}")
            print(f"  Max Concurrent: {config.get('max_concurrent', 2)}")
            print(f"  Anti-Detection: {'Maximum' if config.get('request_timeout', 30) > 45 else 'Advanced' if config.get('request_timeout', 30) > 30 else 'Normal'}")
        
        change_pass = input(f"\n{cyan}Change password? (y/n): {reset}").strip().lower()
        
        if change_pass == "y":
            new_pass = input(f"{cyan}New password: {reset}").strip()
            if len(new_pass) >= 6:
                self.current_password = new_pass
                print(f"{hijau}✅  Password updated{reset}")
            else:
                print(f"{merah}❌  Password must be at least 6 characters{reset}")
        
        # Quick restart option
        quick_restart = input(f"\n{cyan}Quick restart with current settings? (y/n): {reset}").strip().lower()
        
        if quick_restart == "y":
            print(f"{cyan}🔄  Restarting system...{reset}")
            await self._shutdown()
            await self._initialize_system()
        else:
            full_reconfig = input(f"{cyan}Full reconfiguration? (y/n): {reset}").strip().lower()
            
            if full_reconfig == "y":
                print(f"{cyan}🔄  Restarting with new configuration...{reset}")
                await self._shutdown()
                await self._initialize_system()
            else:
                print(f"{kuning}Settings change cancelled{reset}")
    
    async def _view_created_accounts(self):
        """View created accounts dari file"""
        print(f"\n{biru}╔══════════════════════════════════════════════════════════════╗")
        print(f"║{putih}                  CREATED ACCOUNTS                       {biru}      ║")
        print(f"╚══════════════════════════════════════════════════════════════╝{reset}")
        
        try:
            filename = "accounts_2025.txt"
            if os.path.exists(filename):
                with open(filename, "r", encoding="utf-8") as f:
                    accounts = f.readlines()
                
                if accounts:
                    print(f"\n{cyan}📋  Total Accounts: {len(accounts)}{reset}")
                    print(f"{merah}──────────────────────────────────────────────────────────────{reset}")
                    
                    for i, account in enumerate(accounts[-10:], 1):  # Show last 10
                        parts = account.strip().split("|")
                        if len(parts) >= 3:
                            username, password, email = parts[:3]
                            print(f"  {i:2d}. {hijau}{username:<20}{reset} | {password} | {email}")
                    
                    if len(accounts) > 10:
                        print(f"\n  {kuning}... and {len(accounts) - 10} more accounts{reset}")
                    
                    # Stats
                    today = datetime.now().strftime("%Y-%m-%d")
                    today_accounts = [a for a in accounts if today in a]
                    
                    print(f"\n{cyan}📊  Today's Accounts: {len(today_accounts)}{reset}")
                else:
                    print(f"{kuning}No accounts found{reset}")
            else:
                print(f"{kuning}No accounts file found{reset}")
                
        except Exception as e:
            print(f"{merah}❌  Error reading accounts: {e}{reset}")
    
    async def _email_service_stats(self):
        """Show email service statistics"""
        print(f"\n{biru}╔══════════════════════════════════════════════════════════════╗")
        print(f"║{putih}                EMAIL SERVICE STATISTICS                {biru}      ║")
        print(f"╚══════════════════════════════════════════════════════════════╝{reset}")
        
        if not self.system or not self.system.account_creator:
            print(f"{merah}❌  System not initialized{reset}")
            return
        
        email_manager = self.system.account_creator.email_manager
        
        if not email_manager:
            print(f"{merah}❌  Email manager not available{reset}")
            return
        
        emails = email_manager.get_all_emails()
        
        print(f"\n{cyan}📧  EMAIL CACHE STATISTICS{reset}")
        print(f"{merah}─────────────────────────{reset}")
        
        print(f"  {putih}Total Emails:{reset} {len(emails)}")
        
        if emails:
            # Group by service
            service_stats = {}
            for email in emails:
                service = email.get("service", "unknown")
                service_stats[service] = service_stats.get(service, 0) + 1
            
            print(f"\n  {putih}By Service:{reset}")
            for service, count in service_stats.items():
                percentage = (count / len(emails)) * 100
                print(f"    {cyan}{service:<15}{reset}: {count:>3} ({percentage:.0f}%)")
            
            # Age statistics
            now = time.time()
            ages = [(now - email.get("created_at", now)) / 60 for email in emails]
            
            if ages:
                avg_age = sum(ages) / len(ages)
                max_age = max(ages)
                
                print(f"\n  {putih}Age Statistics:{reset}")
                print(f"    Average: {avg_age:.1f} minutes")
                print(f"    Oldest: {max_age:.1f} minutes")
            
            # Show recent emails
            print(f"\n  {putih}Recent Emails (last 5):{reset}")
            for email in sorted(emails, key=lambda x: x.get("created_at", 0), reverse=True)[:5]:
                age_minutes = (now - email.get("created_at", now)) / 60
                otp_status = "✅" if email.get("otp_received") else "❌"
                print(f"    {email['email']} ({email.get('service')}) - {age_minutes:.1f}m {otp_status}")
    
    async def _ip_pool_management(self):
        """Manage IP pool"""
        print(f"\n{biru}╔══════════════════════════════════════════════════════════════╗")
        print(f"║{putih}                  IP POOL MANAGEMENT                     {biru}      ║")
        print(f"╚══════════════════════════════════════════════════════════════╝{reset}")
        
        if not self.system or not self.system.account_creator:
            print(f"{merah}❌  System not initialized{reset}")
            return
        
        ip_system = self.system.account_creator.ip_system
        
        if not ip_system:
            print(f"{merah}❌  IP system not available{reset}")
            return
        
        ip_stats = ip_system.get_ip_pool_stats()
        
        print(f"\n{cyan}🌐  IP POOL STATUS{reset}")
        print(f"{merah}─────────────────{reset}")
        
        print(f"  {putih}Total IPs:{reset} {ip_stats.get('total_ips', 0)}")
        print(f"  {hijau}Healthy IPs:{reset} {ip_stats.get('healthy_ips', 0)}")
        print(f"  {merah}Blacklisted IPs:{reset} {ip_stats.get('blacklisted_ips', 0)}")
        print(f"  {cyan}Health Rate:{reset} {ip_stats.get('health_rate', '0%')}")
        print(f"  {putih}Pool Age:{reset} {self._format_duration(ip_stats.get('pool_age_seconds', 0))}")
        
        # ISP Distribution
        isp_dist = ip_stats.get('isp_distribution', {})
        if isp_dist:
            print(f"\n  {putih}ISP Distribution:{reset}")
            for isp, count in isp_dist.items():
                percentage = (count / ip_stats.get('total_ips', 1)) * 100
                bar_length = 20
                filled = int(percentage / 100 * bar_length)
                bar = f"{hijau}{'█' * filled}{reset}{'░' * (bar_length - filled)}"
                print(f"    {cyan}{isp:<12}{reset}: {count:>3} {bar} {percentage:.0f}%")
        
        # Management options
        print(f"\n{cyan}🛠️   MANAGEMENT OPTIONS{reset}")
        print(f"{merah}─────────────────────{reset}")
        print(f"  1. {hijau}Refresh IP Pool{reset} - Generate fresh IPs")
        print(f"  2. {kuning}Clear Blacklist{reset} - Remove blacklisted IPs")
        print(f"  3. {cyan}Get New IP Config{reset} - Test IP generation")
        print(f"  4. {putih}Back to Main Menu{reset}")
        
        choice = input(f"\n{cyan}Choice (1-4): {reset}").strip()
        
        if choice == "1":
            print(f"{cyan}🔄  Refreshing IP pool...{reset}")
            # Call refresh method
            ip_system._refresh_ip_pool_if_needed()
            print(f"{hijau}✅  IP pool refreshed{reset}")
            
        elif choice == "2":
            print(f"{cyan}🧹  Clearing blacklist...{reset}")
            # Clear blacklist (implementation depends on IP system)
            if hasattr(ip_system, 'blacklisted_ips'):
                ip_system.blacklisted_ips.clear()
                print(f"{hijau}✅  Blacklist cleared{reset}")
            
        elif choice == "3":
            print(f"{cyan}🌐  Getting new IP config...{reset}")
            ip_config = ip_system.get_fresh_ip_config()
            print(f"{hijau}✅  New IP: {ip_config.get('ip', 'N/A')}{reset}")
            print(f"    ISP: {ip_config.get('isp', 'N/A')}")
            print(f"    Location: {ip_config.get('location', {}).get('city', 'N/A')}")
        
        elif choice == "4":
            return
        
        else:
            print(f"{merah}Invalid choice{reset}")
    
    def _show_account_result(self, result: Dict[str, Any]):
        """Show account creation result dengan format yang lebih baik"""
        print(f"\n{biru}📝  ACCOUNT CREATION RESULT{reset}")
        print(f"{merah}──────────────────────────────────────────────────────────────{reset}")
        
        status = result.get("status", "unknown")
        
        if status == "success":
            account = result.get("account", {})
            print(f"{bg_hijau}{putih} 🎉  SUCCESSFULLY CREATED ACCOUNT {reset}")
            print(f"\n{cyan}📋  ACCOUNT DETAILS{reset}")
            print(f"{merah}──────────────────{reset}")
            print(f"  {putih}Username:{reset} {hijau}{account.get('username', 'N/A')}{reset}")
            print(f"  {putih}Email:{reset} {cyan}{account.get('email', 'N/A')}{reset}")
            print(f"  {putih}Password:{reset} {kuning}{'*' * len(account.get('password', ''))}{reset}")
            print(f"  {putih}Session ID:{reset} {account.get('session_id', 'N/A')[:10]}...")
            print(f"  {putih}Created:{reset} {datetime.fromtimestamp(account.get('created_at', 0)).strftime('%Y-%m-%d %H:%M:%S')}")
            
            # Save reminder
            print(f"\n{kuning}💾  Account has been saved to accounts_2025.txt{reset}")
            
        elif status == "failed":
            print(f"{bg_merah}{putih} ❌  ACCOUNT CREATION FAILED {reset}")
            print(f"\n{cyan}🔍  ERROR ANALYSIS{reset}")
            print(f"{merah}─────────────────{reset}")
            print(f"  {putih}Reason:{reset} {merah}{result.get('reason', 'Unknown')}{reset}")
            print(f"  {putih}Message:{reset} {kuning}{result.get('message', 'No message')}{reset}")
            
            # Suggestions based on error
            reason = result.get('reason', '').lower()
            if 'email' in reason:
                print(f"\n{cyan}💡  SUGGESTION:{reset} Try a different email service")
            elif 'ip' in reason or 'block' in reason:
                print(f"\n{cyan}💡  SUGGESTION:{reset} Wait 5-10 minutes before retrying")
            elif 'otp' in reason:
                print(f"\n{cyan}💡  SUGGESTION:{reset} Email service might be rate limited")
            
        else:
            print(f"{bg_kuning}{putih} ⚠️   UNKNOWN RESULT {reset}")
            print(f"\n{cyan}Result data:{reset}")
            for key, value in result.items():
                print(f"  {putih}{key}:{reset} {value}")
    
    def _show_batch_result(self, result: Dict[str, Any]):
        """Show batch creation result dengan visual yang lebih baik"""
        print(f"\n{biru}📊  BATCH CREATION RESULTS{reset}")
        print(f"{merah}──────────────────────────────────────────────────────────────{reset}")
        
        total = result.get("total", 0)
        successful = result.get("successful", 0)
        failed = result.get("failed", 0)
        success_rate = result.get("success_rate", 0)
        duration = result.get("duration", 0)
        
        # Visual success rate
        bar_length = 30
        filled = int(success_rate * bar_length)
        success_bar = f"{hijau}{'█' * filled}{reset}{merah}{'░' * (bar_length - filled)}{reset}"
        
        print(f"\n{cyan}📈  PERFORMANCE SUMMARY{reset}")
        print(f"{merah}─────────────────────{reset}")
        print(f"  {putih}Total:{reset} {total}")
        print(f"  {hijau}Successful:{reset} {successful}")
        print(f"  {merah}Failed:{reset} {failed}")
        print(f"  {cyan}Success Rate:{reset} {success_rate:.1%}")
        print(f"  {putih}Success Bar:{reset} [{success_bar}]")
        print(f"  {putih}Duration:{reset} {self._format_duration(duration)}")
        print(f"  {cyan}Accounts/Hour:{reset} {(successful / duration * 3600) if duration > 0 else 0:.1f}")
        
        if successful > 0:
            print(f"\n{cyan}✅  CREATED ACCOUNTS{reset}")
            print(f"{merah}──────────────────{reset}")
            
            accounts = result.get("accounts", [])
            for i, account in enumerate(accounts[:10], 1):  # Show first 10
                username = account.get('username', 'N/A')
                email = account.get('email', 'N/A')
                print(f"  {i:2d}. {hijau}{username:<20}{reset} | {email}")
            
            if successful > 10:
                print(f"  ... and {successful - 10} more accounts")
        
        if failed > 0 and "errors" in result:
            print(f"\n{merah}❌  FAILED ATTEMPTS{reset}")
            print(f"{merah}─────────────────{reset}")
            
            errors = result.get("errors", [])
            error_counts = {}
            for error in errors[:10]:  # Show first 10 errors
                reason = error.get("reason", "Unknown")
                error_counts[reason] = error_counts.get(reason, 0) + 1
            
            for reason, count in error_counts.items():
                print(f"  {reason}: {count}")
            
            if len(errors) > 10:
                print(f"  ... and {len(errors) - 10} more errors")
        
        # Recommendations based on success rate
        print(f"\n{cyan}💡  RECOMMENDATIONS{reset}")
        print(f"{merah}─────────────────{reset}")
        
        if success_rate >= 0.8:
            print(f"  {hijau}Excellent success rate! Continue with current settings.{reset}")
        elif success_rate >= 0.6:
            print(f"  {cyan}Good success rate. Consider increasing cooldown times slightly.{reset}")
        elif success_rate >= 0.4:
            print(f"  {kuning}Moderate success rate. Try changing email service or increasing cooldowns.{reset}")
        else:
            print(f"  {merah}Low success rate. Consider:{reset}")
            print(f"     • Change email service")
            print(f"     • Increase cooldown times (60-120s)")
            print(f"     • Use maximum anti-detection mode")
            print(f"     • Check if Instagram is blocking your IP")
    
    def _show_test_result(self, system_name: str, result: Dict[str, Any], simple: bool = False):
        """Show test result dengan format yang lebih baik"""
        if not simple:
            print(f"\n{biru}🧪  TEST: {system_name.upper()}{reset}")
            print(f"{merah}──────────────────────────────────────────────────────────────{reset}")
        
        status = result.get("status", "unknown")
        
        if status == "success":
            color = hijau
            symbol = "✅"
            status_text = "PASSED"
        elif status == "error":
            color = merah
            symbol = "❌"
            status_text = "FAILED"
        else:
            color = kuning
            symbol = "⚠️"
            status_text = "UNKNOWN"
        
        if simple:
            print(f"  {color}{symbol} {system_name}: {status_text}{reset}")
        else:
            print(f"{color}{symbol} {status_text}: {result.get('message', 'No message')}{reset}")
            
            # Show additional details
            details = {k: v for k, v in result.items() if k not in ['status', 'message']}
            if details:
                print(f"\n{cyan}📋  DETAILS{reset}")
                print(f"{merah}─────────{reset}")
                
                for key, value in details.items():
                    if isinstance(value, dict):
                        print(f"  {putih}{key}:{reset}")
                        for sub_key, sub_value in value.items():
                            if isinstance(sub_value, (list, tuple)) and len(sub_value) > 3:
                                print(f"    {putih}{sub_key}:{reset} {len(sub_value)} items")
                            else:
                                print(f"    {putih}{sub_key}:{reset} {sub_value}")
                    elif isinstance(value, (list, tuple)) and len(value) > 5:
                        print(f"  {putih}{key}:{reset} {len(value)} items")
                        for item in value[:3]:
                            print(f"    • {item}")
                        if len(value) > 3:
                            print(f"    ... and {len(value) - 3} more")
                    else:
                        print(f"  {putih}{key}:{reset} {value}")
    
    def _format_duration(self, seconds: float) -> str:
        """Format duration menjadi string yang mudah dibaca"""
        if seconds < 1:
            return f"{seconds*1000:.0f}ms"
        elif seconds < 60:
            return f"{seconds:.1f}s"
        elif seconds < 3600:
            minutes = seconds / 60
            return f"{minutes:.1f}m"
        elif seconds < 86400:
            hours = seconds / 3600
            return f"{hours:.1f}h"
        else:
            days = seconds / 86400
            return f"{days:.1f}d"
    
    async def _shutdown(self):
        """Shutdown system dengan cleanup yang proper"""
        print(f"\n{cyan}🛑  Shutting down system...{reset}")
        
        if self.system:
            await self.system.cleanup()
        
        # Clear any remaining sessions
        if hasattr(self, 'current_password'):
            self.current_password = None
        
        print(f"{hijau}✅  System shutdown complete{reset}")
        print(f"{kuning}👋  Goodbye!{reset}")

# ===================== MAIN ENTRY POINT =====================

async def main():
    """Main entry point"""
    try:
        # Show banner
        show_ascii_art()
        
        # Check dependencies
        if not check_dependencies():
            return
        
        # Setup environment
        setup_environment()
        
        # Create and run CLI
        cli = CLIInterface()
        await cli.run()
        
    except KeyboardInterrupt:
        print(f"\n{kuning}👋  Goodbye!{reset}")
    except Exception as e:
        print(f"{merah}❌  Fatal error: {e}{reset}")
        import traceback
        traceback.print_exc()

def sync_main():
    """Synchronous main entry point"""
    asyncio.run(main())

# ===================== UTILITY FUNCTIONS =====================

def check_dependencies():
    """Check if all dependencies are installed"""
    required_modules = [
        "requests", "colorama", "faker", "aiohttp", "bs4", 
        "cryptography", "numpy", "scipy"
    ]
    
    missing_modules = []
    
    for module in required_modules:
        try:
            __import__(module)
        except ImportError:
            missing_modules.append(module)
    
    if missing_modules:
        print(f"{merah}❌  Missing modules: {', '.join(missing_modules)}{reset}")
        print(f"{cyan}💡  Install with: pip install {' '.join(missing_modules)}{reset}")
        return False
    
    print(f"{hijau}✅  All dependencies are installed{reset}")
    return True

def setup_environment():
    """Setup environment"""
    print(f"{cyan}⚙️   Setting up environment...{reset}")
    
    # Create necessary directories
    directories = ["sessions", "logs", "accounts"]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"  {hijau}✓{reset} Created {directory}/ directory")
    
    # Create default config file
    default_config = {
        "use_proxy": False,
        "max_concurrent": 3,
        "email_service": "auto",
        "location": "ID",
        "device_type": "desktop",
        "save_sessions": True,
        "session_file": "sessions/sessions_2025.json",
        "accounts_file": "accounts/accounts_2025.txt",
        "log_file": "logs/ultraboosted_2025.log"
    }
    
    config_file = "config_2025.json"
    if not os.path.exists(config_file):
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(default_config, f, indent=2)
        print(f"  {hijau}✓{reset} Created {config_file}")
    
    print(f"{hijau}✅  Environment setup complete{reset}")

def show_ascii_art():
    """Show ASCII art banner dengan info IP system"""
    art = f"""
{merah}╔══════════════════════════════════════════════════════════════════════════════╗
║{biru}   ██╗   ██╗██╗  ████████╗██████╗  █████╗     ██████╗  ██████╗  ██████╗ ████████╗{merah}  ║
║{biru}   ██║   ██║██║  ╚══██╔══╝██╔══██╗██╔══██╗    ██╔══██╗██╔═══██╗██╔═══██╗╚══██╔══╝{merah}  ║
║{biru}   ██║   ██║██║     ██║   ██████╔╝███████║    ██████╔╝██║   ██║██║   ██║   ██║   {merah}  ║
║{biru}   ██║   ██║██║     ██║   ██╔══██╗██╔══██║    ██╔══██╗██║   ██║██║   ██║   ██║   {merah}  ║
║{biru}   ╚██████╔╝███████╗██║   ██║  ██║██║  ██║    ██████╔╝╚██████╔╝╚██████╔╝   ██║   {merah}  ║
║{biru}    ╚═════╝ ╚══════╝╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝    ╚═════╝  ╚═════╝  ╚═════╝    ╚═╝   {merah}  ║
║{hijau}                      ULTRA BOOSTED V13 - 2025 EDITION                        {merah}  ║
║{putih}              Advanced Instagram Account Creation System v2.0                {merah}  ║
║{cyan}                   Dynamic IP System • Anti-Detection • Auto-Rotate             {merah}  ║
╚══════════════════════════════════════════════════════════════════════════════╝{reset}

{cyan}⚡  Features:{reset}
  • {hijau}Dynamic IP Generation{reset} - Fresh IPs setiap request
  • {hijau}Real-time IP Validation{reset} - Health scoring system  
  • {hijau}Auto IP Rotation{reset} - Otomatis saat terdeteksi block
  • {hijau}Multiple ISP Support{reset} - 7+ ISP Indonesia
  • {hijau}Geographic Diversity{reset} - IP dari berbagai kota
  • {hijau}Advanced Fingerprinting{reset} - Realistic browser profiles
    """
    print(art)

# ===================== EXPORTED FUNCTIONS =====================

def run_cli():
    """Run CLI interface (exported function)"""
    try:
        # Setup
        show_ascii_art()
        
        # Check dependencies
        if not check_dependencies():
            return
        
        # Setup environment
        setup_environment()
        
        # Run main
        sync_main()
        
    except KeyboardInterrupt:
        print(f"\n{kuning}👋  Program terminated by user{reset}")
    except Exception as e:
        print(f"{merah}❌  Error: {e}{reset}")

def create_account_sync(password: str, config: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Create account synchronously (exported function)"""
    async def _create_async():
        system = UltraBoostedV13_2025(config)
        await system.initialize()
        result = await system.create_single_account(password)
        await system.cleanup()
        return result
    
    return asyncio.run(_create_async())

def create_batch_sync(count: int, password: str, config: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Create batch accounts synchronously (exported function)"""
    async def _create_async():
        system = UltraBoostedV13_2025(config)
        await system.initialize()
        result = await system.create_batch_accounts(count, password)
        await system.cleanup()
        return result
    
    return asyncio.run(_create_async())

# ===================== RUN APPLICATION =====================

if __name__ == "__main__":
    # Entry point untuk CLI
    run_cli()
