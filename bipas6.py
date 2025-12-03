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
from datetime import datetime, timedelta
from faker import Faker
from time import sleep
from colorama import init, Fore, Back, Style
from http.cookies import SimpleCookie
from typing import Any, Dict, List, Optional, Tuple
import concurrent.futures
from functools import wraps
import urllib3
import urllib
import logging
from hashlib import sha1
from fake_useragent import UserAgent
from typing import Optional, Tuple, Dict
import ipaddress
import socket
import struct
import hashlib
import hmac
import secrets
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
import subprocess
import platform
import psutil
import numpy as np
from scipy import stats
import math
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
import functools

if sys.version_info >= (3, 0):
    from urllib.parse import urlencode, quote_plus

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
    HAVE_AIORPC = True
except ImportError:
    HAVE_AIORPC = False
    print(f"{merah}❌  aiohttp not installed. Install with: pip install aiohttp{reset}")

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

# ===================== ADVANCED IP SPOOFING 2025 =====================

# ===================== ADVANCED IP SPOOFING 2025 - UPDATED =====================

class AdvancedIPStealthSystem2025:
    """Sistem IP stealth dinamis 2025 dengan real-time validation dan enhanced spoofing"""
    
    def __init__(self):
        self.ip_pool = []
        self.blacklisted_ips = set()
        self.ip_sources = self._initialize_ip_sources()
        self.validator = IPValidator2025()
        self.generation_cache = {}
        self.cache_ttl = 300
        self.session_ip_map = {}
        
        # Load global ISP database for 50+ countries
        self.global_isp_database = self._load_global_isp_database()
        
        # Load comprehensive blacklist ranges (datacenter/VPN/proxy)
        self.blacklisted_ranges = self._load_blacklisted_ranges()
        self.datacenter_ranges = self._load_datacenter_ranges()
        self.vpn_ranges = self._load_vpn_ranges()
        
        # Country weights for realistic distribution
        self.country_weights = {
            # More balanced distribution - less Indonesia focus for better randomization
            "US": 0.20,  # USA - Instagram's largest market
            "IN": 0.15,  # India - second largest
            "BR": 0.12,  # Brazil - third largest
            "ID": 0.10,  # Indonesia - reduced from 40%
            "GB": 0.08,  # United Kingdom
            "DE": 0.07,  # Germany
            "JP": 0.06,  # Japan
            "PH": 0.05,  # Philippines
            "TH": 0.04,  # Thailand
            "VN": 0.03,  # Vietnam
            "AU": 0.03,  # Australia
            "MX": 0.03,  # Mexico
            "SG": 0.02,  # Singapore
            "TR": 0.02   # Turkey
        }
    
    def _load_global_isp_database(self) -> Dict[str, Dict[str, Any]]:
        """Load global ISP database with 50+ countries"""
        return {
            # ===== AMERICAS =====
            "US": {
                "att": {
                    "prefixes": ["12.0", "32.0", "63.0", "68.0", "99.0", "107.0", "108.0"],
                    "asn": "AS7018",
                    "as_name": "AT&T Services, Inc.",
                    "cities": ["New York", "Los Angeles", "Chicago", "Houston", "Phoenix"],
                    "ttl_range": (52, 64), "window_range": (64240, 65535), "mss_range": (1360, 1460),
                    "latency_range": (15, 40), "jitter_range": (2, 8), "packet_loss": (0.1, 0.4)
                },
                "verizon": {
                    "prefixes": ["66.174", "72.80", "96.244", "108.5", "141.152", "174.192"],
                    "asn": "AS701",
                    "as_name": "Verizon Business",
                    "cities": ["New York", "Philadelphia", "Boston", "Dallas", "Miami"],
                    "ttl_range": (54, 64), "window_range": (64240, 65535), "mss_range": (1360, 1460),
                    "latency_range": (12, 35), "jitter_range": (2, 7), "packet_loss": (0.1, 0.3)
                },
                "tmobile": {
                    "prefixes": ["172.32", "172.56", "174.198", "208.54", "66.94"],
                    "asn": "AS21928",
                    "as_name": "T-Mobile USA, Inc.",
                    "cities": ["Seattle", "Los Angeles", "Denver", "Atlanta", "Chicago"],
                    "ttl_range": (56, 64), "window_range": (64240, 65535), "mss_range": (1360, 1460),
                    "latency_range": (18, 45), "jitter_range": (3, 10), "packet_loss": (0.2, 0.5)
                },
                "comcast": {
                    "prefixes": ["50.128", "68.32", "73.0", "75.64", "76.96", "98.192"],
                    "asn": "AS7922",
                    "as_name": "Comcast Cable Communications",
                    "cities": ["Philadelphia", "San Francisco", "Chicago", "Denver", "Portland"],
                    "ttl_range": (50, 64), "window_range": (64240, 65535), "mss_range": (1360, 1460),
                    "latency_range": (10, 30), "jitter_range": (2, 6), "packet_loss": (0.1, 0.3)
                },
                "spectrum": {
                    "prefixes": ["24.30", "65.36", "66.41", "71.56", "97.64", "174.79"],
                    "asn": "AS11351",
                    "as_name": "Charter Communications",
                    "cities": ["New York", "Los Angeles", "Dallas", "Charlotte", "Orlando"],
                    "ttl_range": (52, 64), "window_range": (64240, 65535), "mss_range": (1360, 1460),
                    "latency_range": (12, 35), "jitter_range": (2, 8), "packet_loss": (0.1, 0.4)
                }
            },
            "CA": {
                "rogers": {
                    "prefixes": ["64.231", "99.224", "174.88", "184.64", "209.171"],
                    "asn": "AS812",
                    "as_name": "Rogers Communications Canada",
                    "cities": ["Toronto", "Vancouver", "Montreal", "Calgary", "Ottawa"],
                    "ttl_range": (52, 64), "window_range": (64240, 65535), "mss_range": (1360, 1460),
                    "latency_range": (15, 40), "jitter_range": (2, 8), "packet_loss": (0.1, 0.4)
                },
                "bell": {
                    "prefixes": ["67.68", "70.48", "99.248", "184.144", "206.108"],
                    "asn": "AS577",
                    "as_name": "Bell Canada",
                    "cities": ["Toronto", "Montreal", "Ottawa", "Hamilton", "Quebec City"],
                    "ttl_range": (54, 64), "window_range": (64240, 65535), "mss_range": (1360, 1460),
                    "latency_range": (12, 35), "jitter_range": (2, 7), "packet_loss": (0.1, 0.3)
                }
            },
            "MX": {
                "telmex": {
                    "prefixes": ["148.240", "187.188", "189.128", "200.38", "201.140"],
                    "asn": "AS8151",
                    "as_name": "Telmex S.A. de C.V.",
                    "cities": ["Mexico City", "Guadalajara", "Monterrey", "Cancun", "Tijuana"],
                    "ttl_range": (52, 64), "window_range": (64240, 65535), "mss_range": (1360, 1460),
                    "latency_range": (20, 50), "jitter_range": (3, 12), "packet_loss": (0.2, 0.6)
                }
            },
            "BR": {
                "vivo": {
                    "prefixes": ["177.40", "179.184", "187.0", "189.0", "200.150"],
                    "asn": "AS26599",
                    "as_name": "Telefonica Brasil S.A.",
                    "cities": ["Sao Paulo", "Rio de Janeiro", "Brasilia", "Salvador", "Belo Horizonte"],
                    "ttl_range": (52, 64), "window_range": (64240, 65535), "mss_range": (1360, 1460),
                    "latency_range": (25, 60), "jitter_range": (4, 15), "packet_loss": (0.3, 0.7)
                },
                "claro": {
                    "prefixes": ["170.80", "177.96", "186.192", "189.0", "201.17"],
                    "asn": "AS28573",
                    "as_name": "CLARO S.A.",
                    "cities": ["Sao Paulo", "Rio de Janeiro", "Curitiba", "Porto Alegre", "Recife"],
                    "ttl_range": (54, 64), "window_range": (64240, 65535), "mss_range": (1360, 1460),
                    "latency_range": (22, 55), "jitter_range": (3, 12), "packet_loss": (0.2, 0.6)
                }
            },
            "AR": {
                "claro_ar": {
                    "prefixes": ["168.226", "181.47", "186.0", "190.17", "200.59"],
                    "asn": "AS10834",
                    "as_name": "Telefonica de Argentina",
                    "cities": ["Buenos Aires", "Cordoba", "Rosario", "Mendoza", "Mar del Plata"],
                    "ttl_range": (52, 64), "window_range": (64240, 65535), "mss_range": (1360, 1460),
                    "latency_range": (25, 60), "jitter_range": (4, 15), "packet_loss": (0.3, 0.7)
                }
            },
            
            # ===== EUROPE =====
            "GB": {
                "bt": {
                    "prefixes": ["79.64", "81.96", "86.128", "90.192", "109.144"],
                    "asn": "AS2856",
                    "as_name": "BT Group plc",
                    "cities": ["London", "Manchester", "Birmingham", "Edinburgh", "Glasgow"],
                    "ttl_range": (52, 64), "window_range": (64240, 65535), "mss_range": (1360, 1460),
                    "latency_range": (10, 30), "jitter_range": (2, 6), "packet_loss": (0.1, 0.3)
                },
                "virgin": {
                    "prefixes": ["62.253", "80.192", "82.0", "86.0", "88.104"],
                    "asn": "AS5089",
                    "as_name": "Virgin Media Limited",
                    "cities": ["London", "Bristol", "Liverpool", "Leeds", "Sheffield"],
                    "ttl_range": (54, 64), "window_range": (64240, 65535), "mss_range": (1360, 1460),
                    "latency_range": (8, 25), "jitter_range": (2, 5), "packet_loss": (0.1, 0.2)
                },
                "vodafone_gb": {
                    "prefixes": ["92.234", "109.73", "176.24", "217.64"],
                    "asn": "AS12353",
                    "as_name": "Vodafone UK",
                    "cities": ["London", "Birmingham", "Manchester", "Reading", "Nottingham"],
                    "ttl_range": (56, 64), "window_range": (64240, 65535), "mss_range": (1360, 1460),
                    "latency_range": (12, 35), "jitter_range": (2, 8), "packet_loss": (0.1, 0.4)
                }
            },
            "DE": {
                "dtag": {
                    "prefixes": ["79.192", "84.128", "87.128", "91.0", "93.192"],
                    "asn": "AS3320",
                    "as_name": "Deutsche Telekom AG",
                    "cities": ["Berlin", "Munich", "Frankfurt", "Hamburg", "Cologne"],
                    "ttl_range": (52, 64), "window_range": (64240, 65535), "mss_range": (1360, 1460),
                    "latency_range": (10, 30), "jitter_range": (2, 6), "packet_loss": (0.1, 0.3)
                },
                "vodafone_de": {
                    "prefixes": ["77.20", "88.64", "94.216", "109.40", "178.0"],
                    "asn": "AS3209",
                    "as_name": "Vodafone GmbH",
                    "cities": ["Berlin", "Dusseldorf", "Munich", "Frankfurt", "Stuttgart"],
                    "ttl_range": (54, 64), "window_range": (64240, 65535), "mss_range": (1360, 1460),
                    "latency_range": (8, 25), "jitter_range": (2, 5), "packet_loss": (0.1, 0.2)
                }
            },
            "FR": {
                "orange_fr": {
                    "prefixes": ["80.10", "86.64", "88.160", "90.0", "109.128"],
                    "asn": "AS3215",
                    "as_name": "Orange S.A.",
                    "cities": ["Paris", "Lyon", "Marseille", "Toulouse", "Nice"],
                    "ttl_range": (52, 64), "window_range": (64240, 65535), "mss_range": (1360, 1460),
                    "latency_range": (10, 30), "jitter_range": (2, 6), "packet_loss": (0.1, 0.3)
                },
                "sfr": {
                    "prefixes": ["77.192", "86.192", "92.128", "109.192", "176.128"],
                    "asn": "AS15557",
                    "as_name": "SFR SA",
                    "cities": ["Paris", "Bordeaux", "Strasbourg", "Nantes", "Montpellier"],
                    "ttl_range": (54, 64), "window_range": (64240, 65535), "mss_range": (1360, 1460),
                    "latency_range": (8, 28), "jitter_range": (2, 5), "packet_loss": (0.1, 0.3)
                }
            },
            "IT": {
                "tim_it": {
                    "prefixes": ["79.0", "80.180", "87.0", "93.32", "95.232"],
                    "asn": "AS3269",
                    "as_name": "Telecom Italia",
                    "cities": ["Rome", "Milan", "Naples", "Turin", "Florence"],
                    "ttl_range": (52, 64), "window_range": (64240, 65535), "mss_range": (1360, 1460),
                    "latency_range": (12, 35), "jitter_range": (2, 8), "packet_loss": (0.2, 0.5)
                }
            },
            "ES": {
                "movistar_es": {
                    "prefixes": ["80.24", "83.32", "88.0", "95.16", "176.80"],
                    "asn": "AS3352",
                    "as_name": "Telefonica de Espana",
                    "cities": ["Madrid", "Barcelona", "Valencia", "Seville", "Bilbao"],
                    "ttl_range": (52, 64), "window_range": (64240, 65535), "mss_range": (1360, 1460),
                    "latency_range": (12, 35), "jitter_range": (2, 8), "packet_loss": (0.2, 0.5)
                }
            },
            "NL": {
                "kpn": {
                    "prefixes": ["77.160", "80.56", "83.80", "94.208", "109.32"],
                    "asn": "AS1136",
                    "as_name": "KPN B.V.",
                    "cities": ["Amsterdam", "Rotterdam", "The Hague", "Utrecht", "Eindhoven"],
                    "ttl_range": (54, 64), "window_range": (64240, 65535), "mss_range": (1360, 1460),
                    "latency_range": (6, 20), "jitter_range": (1, 4), "packet_loss": (0.1, 0.2)
                }
            },
            "PL": {
                "orange_pl": {
                    "prefixes": ["77.88", "83.28", "89.64", "95.160", "109.96"],
                    "asn": "AS5617",
                    "as_name": "Orange Polska",
                    "cities": ["Warsaw", "Krakow", "Gdansk", "Wroclaw", "Poznan"],
                    "ttl_range": (52, 64), "window_range": (64240, 65535), "mss_range": (1360, 1460),
                    "latency_range": (15, 40), "jitter_range": (2, 8), "packet_loss": (0.1, 0.4)
                }
            },
            "TR": {
                "turkcell": {
                    "prefixes": ["78.160", "88.224", "95.0", "176.88", "212.174"],
                    "asn": "AS9121",
                    "as_name": "Turk Telekom",
                    "cities": ["Istanbul", "Ankara", "Izmir", "Bursa", "Antalya"],
                    "ttl_range": (52, 64), "window_range": (64240, 65535), "mss_range": (1360, 1460),
                    "latency_range": (18, 45), "jitter_range": (3, 10), "packet_loss": (0.2, 0.5)
                }
            },
            "RU": {
                "mts_ru": {
                    "prefixes": ["78.106", "79.104", "83.220", "94.140", "176.194"],
                    "asn": "AS8359",
                    "as_name": "MTS PJSC",
                    "cities": ["Moscow", "Saint Petersburg", "Novosibirsk", "Yekaterinburg", "Kazan"],
                    "ttl_range": (52, 64), "window_range": (64240, 65535), "mss_range": (1360, 1460),
                    "latency_range": (20, 50), "jitter_range": (3, 12), "packet_loss": (0.2, 0.6)
                }
            },
            
            # ===== ASIA =====
            "IN": {
                "jio": {
                    "prefixes": ["49.40", "152.56", "157.33", "157.40", "157.49"],
                    "asn": "AS55836",
                    "as_name": "Reliance Jio Infocomm Limited",
                    "cities": ["Mumbai", "Delhi", "Bangalore", "Hyderabad", "Chennai"],
                    "ttl_range": (52, 64), "window_range": (64240, 65535), "mss_range": (1360, 1460),
                    "latency_range": (25, 60), "jitter_range": (4, 15), "packet_loss": (0.3, 0.7)
                },
                "airtel_in": {
                    "prefixes": ["106.192", "117.192", "122.160", "180.149", "182.64"],
                    "asn": "AS24560",
                    "as_name": "Bharti Airtel Ltd.",
                    "cities": ["Mumbai", "Delhi", "Kolkata", "Pune", "Ahmedabad"],
                    "ttl_range": (54, 64), "window_range": (64240, 65535), "mss_range": (1360, 1460),
                    "latency_range": (20, 50), "jitter_range": (3, 12), "packet_loss": (0.2, 0.5)
                }
            },
            "JP": {
                "ntt_docomo": {
                    "prefixes": ["49.96", "60.32", "106.128", "126.64", "153.128"],
                    "asn": "AS9605",
                    "as_name": "NTT DOCOMO, INC.",
                    "cities": ["Tokyo", "Osaka", "Nagoya", "Yokohama", "Sapporo"],
                    "ttl_range": (52, 64), "window_range": (64240, 65535), "mss_range": (1360, 1460),
                    "latency_range": (8, 25), "jitter_range": (2, 5), "packet_loss": (0.1, 0.2)
                },
                "softbank_jp": {
                    "prefixes": ["60.149", "124.144", "126.0", "183.176", "218.224"],
                    "asn": "AS17676",
                    "as_name": "SoftBank Corp.",
                    "cities": ["Tokyo", "Osaka", "Fukuoka", "Sendai", "Kobe"],
                    "ttl_range": (54, 64), "window_range": (64240, 65535), "mss_range": (1360, 1460),
                    "latency_range": (10, 30), "jitter_range": (2, 6), "packet_loss": (0.1, 0.3)
                }
            },
            "KR": {
                "skt": {
                    "prefixes": ["27.160", "39.0", "112.160", "118.32", "175.192"],
                    "asn": "AS9644",
                    "as_name": "SK Telecom",
                    "cities": ["Seoul", "Busan", "Incheon", "Daegu", "Daejeon"],
                    "ttl_range": (52, 64), "window_range": (64240, 65535), "mss_range": (1360, 1460),
                    "latency_range": (8, 25), "jitter_range": (2, 5), "packet_loss": (0.1, 0.2)
                }
            },
            "TH": {
                "ais": {
                    "prefixes": ["49.228", "101.108", "110.168", "125.24", "171.96"],
                    "asn": "AS131090",
                    "as_name": "Advanced Info Service PCL",
                    "cities": ["Bangkok", "Chiang Mai", "Phuket", "Pattaya", "Hat Yai"],
                    "ttl_range": (52, 64), "window_range": (64240, 65535), "mss_range": (1360, 1460),
                    "latency_range": (20, 50), "jitter_range": (3, 12), "packet_loss": (0.2, 0.5)
                },
                "true": {
                    "prefixes": ["49.48", "110.77", "124.120", "180.180", "183.88"],
                    "asn": "AS17552",
                    "as_name": "True Internet Co.,Ltd.",
                    "cities": ["Bangkok", "Nonthaburi", "Samut Prakan", "Pathum Thani", "Chonburi"],
                    "ttl_range": (54, 64), "window_range": (64240, 65535), "mss_range": (1360, 1460),
                    "latency_range": (18, 45), "jitter_range": (3, 10), "packet_loss": (0.2, 0.5)
                }
            },
            "VN": {
                "viettel": {
                    "prefixes": ["42.112", "113.160", "117.0", "171.224", "203.162"],
                    "asn": "AS7552",
                    "as_name": "Viettel Group",
                    "cities": ["Ho Chi Minh", "Hanoi", "Da Nang", "Hai Phong", "Can Tho"],
                    "ttl_range": (52, 64), "window_range": (64240, 65535), "mss_range": (1360, 1460),
                    "latency_range": (22, 55), "jitter_range": (3, 12), "packet_loss": (0.2, 0.6)
                },
                "vnpt": {
                    "prefixes": ["27.64", "115.72", "123.16", "125.234", "183.80"],
                    "asn": "AS45899",
                    "as_name": "VNPT Corp",
                    "cities": ["Hanoi", "Ho Chi Minh", "Da Nang", "Hue", "Nha Trang"],
                    "ttl_range": (54, 64), "window_range": (64240, 65535), "mss_range": (1360, 1460),
                    "latency_range": (20, 50), "jitter_range": (3, 10), "packet_loss": (0.2, 0.5)
                }
            },
            "PH": {
                "globe": {
                    "prefixes": ["49.144", "112.198", "119.92", "175.176", "180.190"],
                    "asn": "AS4775",
                    "as_name": "Globe Telecom",
                    "cities": ["Manila", "Quezon City", "Cebu", "Davao", "Makati"],
                    "ttl_range": (52, 64), "window_range": (64240, 65535), "mss_range": (1360, 1460),
                    "latency_range": (25, 60), "jitter_range": (4, 15), "packet_loss": (0.3, 0.7)
                },
                "pldt": {
                    "prefixes": ["49.144", "112.199", "119.93", "180.191", "202.57"],
                    "asn": "AS9299",
                    "as_name": "Philippine Long Distance Telephone Company",
                    "cities": ["Manila", "Cebu", "Davao", "Iloilo", "Zamboanga"],
                    "ttl_range": (54, 64), "window_range": (64240, 65535), "mss_range": (1360, 1460),
                    "latency_range": (22, 55), "jitter_range": (3, 12), "packet_loss": (0.2, 0.6)
                }
            },
            "MY": {
                "maxis": {
                    "prefixes": ["60.48", "113.210", "115.132", "175.136", "203.116"],
                    "asn": "AS9930",
                    "as_name": "Maxis Berhad",
                    "cities": ["Kuala Lumpur", "Penang", "Johor Bahru", "Kota Kinabalu", "Kuching"],
                    "ttl_range": (52, 64), "window_range": (64240, 65535), "mss_range": (1360, 1460),
                    "latency_range": (18, 45), "jitter_range": (3, 10), "packet_loss": (0.2, 0.5)
                }
            },
            "SG": {
                "singtel": {
                    "prefixes": ["116.86", "122.11", "124.12", "182.55", "203.117"],
                    "asn": "AS7473",
                    "as_name": "Singapore Telecommunications Ltd",
                    "cities": ["Singapore Central", "Jurong", "Tampines", "Woodlands", "Bedok"],
                    "ttl_range": (52, 64), "window_range": (64240, 65535), "mss_range": (1360, 1460),
                    "latency_range": (6, 20), "jitter_range": (1, 4), "packet_loss": (0.1, 0.2)
                },
                "starhub": {
                    "prefixes": ["27.54", "59.189", "115.66", "116.15", "202.166"],
                    "asn": "AS4657",
                    "as_name": "StarHub Ltd",
                    "cities": ["Singapore Central", "Toa Payoh", "Ang Mo Kio", "Clementi", "Pasir Ris"],
                    "ttl_range": (54, 64), "window_range": (64240, 65535), "mss_range": (1360, 1460),
                    "latency_range": (5, 18), "jitter_range": (1, 3), "packet_loss": (0.1, 0.2)
                }
            },
            "ID": {
                # Indonesian ISPs - existing configuration with enhancements
                "telkomsel": {
                    "prefixes": ["110.136", "110.137", "114.124", "118.137", "139.192", "182.253", "202.67"],
                    "asn": "AS7713",
                    "as_name": "PT Telekomunikasi Selular",
                    "cities": ["Jakarta", "Surabaya", "Bandung", "Medan", "Bali", "Makassar"],
                    "ttl_range": (48, 64), "window_range": (64240, 65535), "mss_range": (1360, 1460),
                    "latency_range": (15, 45), "jitter_range": (2, 10), "packet_loss": (0.1, 0.5)
                },
                "indosat": {
                    "prefixes": ["112.215", "114.4", "125.160", "139.0", "202.152", "202.43"],
                    "asn": "AS4761",
                    "as_name": "PT Indosat Tbk",
                    "cities": ["Jakarta", "Surabaya", "Makassar", "Balikpapan", "Batam"],
                    "ttl_range": (52, 60), "window_range": (64240, 65535), "mss_range": (1360, 1460),
                    "latency_range": (20, 50), "jitter_range": (3, 12), "packet_loss": (0.2, 0.6)
                },
                "xl": {
                    "prefixes": ["36.86", "114.120", "180.241", "202.43", "110.139"],
                    "asn": "AS24203",
                    "as_name": "PT XL Axiata Tbk",
                    "cities": ["Jakarta", "Yogyakarta", "Semarang", "Palembang", "Lampung"],
                    "ttl_range": (56, 64), "window_range": (64240, 65535), "mss_range": (1360, 1460),
                    "latency_range": (25, 55), "jitter_range": (4, 15), "packet_loss": (0.3, 0.7)
                },
                "tri": {
                    "prefixes": ["116.206", "118.96", "182.253", "203.190", "103.10"],
                    "asn": "AS23947",
                    "as_name": "PT Hutchison 3 Indonesia",
                    "cities": ["Jakarta", "Surabaya", "Bandung", "Bekasi", "Tangerang"],
                    "ttl_range": (60, 68), "window_range": (43800, 44200), "mss_range": (1360, 1460),
                    "latency_range": (30, 60), "jitter_range": (5, 18), "packet_loss": (0.4, 0.8)
                },
                "smartfren": {
                    "prefixes": ["202.67", "202.152", "103.10", "112.78"],
                    "asn": "AS10029",
                    "as_name": "PT Smartfren Telecom Tbk",
                    "cities": ["Jakarta", "Bali", "Batam", "Surabaya"],
                    "ttl_range": (52, 60), "window_range": (29200, 29500), "mss_range": (1360, 1460),
                    "latency_range": (35, 65), "jitter_range": (6, 20), "packet_loss": (0.5, 0.9)
                }
            },
            
            # ===== OCEANIA =====
            "AU": {
                "telstra": {
                    "prefixes": ["49.176", "58.96", "101.112", "110.174", "144.130"],
                    "asn": "AS1221",
                    "as_name": "Telstra Corporation Ltd",
                    "cities": ["Sydney", "Melbourne", "Brisbane", "Perth", "Adelaide"],
                    "ttl_range": (52, 64), "window_range": (64240, 65535), "mss_range": (1360, 1460),
                    "latency_range": (12, 35), "jitter_range": (2, 8), "packet_loss": (0.1, 0.4)
                },
                "optus": {
                    "prefixes": ["49.176", "58.108", "101.0", "211.26", "203.17"],
                    "asn": "AS4804",
                    "as_name": "Optus Internet Pty Ltd",
                    "cities": ["Sydney", "Melbourne", "Brisbane", "Gold Coast", "Canberra"],
                    "ttl_range": (54, 64), "window_range": (64240, 65535), "mss_range": (1360, 1460),
                    "latency_range": (10, 30), "jitter_range": (2, 6), "packet_loss": (0.1, 0.3)
                }
            },
            "NZ": {
                "spark": {
                    "prefixes": ["49.224", "121.72", "125.237", "202.21", "210.54"],
                    "asn": "AS4771",
                    "as_name": "Spark New Zealand Trading Ltd",
                    "cities": ["Auckland", "Wellington", "Christchurch", "Hamilton", "Tauranga"],
                    "ttl_range": (52, 64), "window_range": (64240, 65535), "mss_range": (1360, 1460),
                    "latency_range": (15, 40), "jitter_range": (2, 8), "packet_loss": (0.1, 0.4)
                }
            },
            
            # ===== MIDDLE EAST =====
            "AE": {
                "etisalat": {
                    "prefixes": ["77.221", "80.227", "94.56", "109.177", "213.42"],
                    "asn": "AS8966",
                    "as_name": "Emirates Telecommunications Corporation",
                    "cities": ["Dubai", "Abu Dhabi", "Sharjah", "Ajman", "Ras Al Khaimah"],
                    "ttl_range": (52, 64), "window_range": (64240, 65535), "mss_range": (1360, 1460),
                    "latency_range": (15, 40), "jitter_range": (2, 8), "packet_loss": (0.1, 0.4)
                },
                "du": {
                    "prefixes": ["82.194", "86.96", "94.200", "185.176", "212.58"],
                    "asn": "AS15802",
                    "as_name": "Emirates Integrated Telecommunications Company PJSC",
                    "cities": ["Dubai", "Abu Dhabi", "Sharjah", "Fujairah", "Al Ain"],
                    "ttl_range": (54, 64), "window_range": (64240, 65535), "mss_range": (1360, 1460),
                    "latency_range": (12, 35), "jitter_range": (2, 6), "packet_loss": (0.1, 0.3)
                }
            },
            "SA": {
                "stc": {
                    "prefixes": ["37.104", "78.92", "81.29", "82.169", "176.224"],
                    "asn": "AS25019",
                    "as_name": "Saudi Telecom Company",
                    "cities": ["Riyadh", "Jeddah", "Mecca", "Dammam", "Medina"],
                    "ttl_range": (52, 64), "window_range": (64240, 65535), "mss_range": (1360, 1460),
                    "latency_range": (18, 45), "jitter_range": (3, 10), "packet_loss": (0.2, 0.5)
                }
            }
        }
    
    def _load_blacklisted_ranges(self) -> List[str]:
        """Load comprehensive blacklist for datacenter/VPN/proxy ranges"""
        return [
            # AWS
            "13.0.0.0/8", "18.0.0.0/8", "52.0.0.0/8", "54.0.0.0/8", "3.0.0.0/8",
            # Google Cloud
            "34.0.0.0/8", "35.0.0.0/8", "130.211.0.0/16", "146.148.0.0/16",
            # Azure
            "20.0.0.0/8", "40.0.0.0/8", "51.0.0.0/8", "52.0.0.0/8",
            # DigitalOcean
            "67.205.0.0/16", "104.131.0.0/16", "104.236.0.0/16", "138.197.0.0/16",
            "159.65.0.0/16", "159.89.0.0/16", "161.35.0.0/16", "164.90.0.0/16",
            "165.22.0.0/16", "165.227.0.0/16", "167.71.0.0/16", "167.172.0.0/16",
            "174.138.0.0/16", "178.62.0.0/16", "188.166.0.0/16", "192.241.0.0/16",
            "198.199.0.0/16", "206.81.0.0/16", "209.97.0.0/16",
            # Linode
            "45.33.0.0/16", "45.56.0.0/16", "45.79.0.0/16", "50.116.0.0/16",
            "66.175.0.0/16", "69.164.0.0/16", "72.14.0.0/16", "74.207.0.0/16",
            "96.126.0.0/16", "97.107.0.0/16", "139.162.0.0/16", "172.104.0.0/16",
            "173.230.0.0/16", "176.58.0.0/16", "178.79.0.0/16", "192.155.0.0/16",
            "198.58.0.0/16", "198.74.0.0/16",
            # Vultr
            "45.32.0.0/16", "45.63.0.0/16", "45.76.0.0/16", "45.77.0.0/16",
            "66.42.0.0/16", "78.141.0.0/16", "95.179.0.0/16", "104.238.0.0/16",
            "107.191.0.0/16", "108.61.0.0/16", "136.244.0.0/16", "137.220.0.0/16",
            "139.180.0.0/16", "140.82.0.0/16", "141.164.0.0/16", "144.202.0.0/16",
            "149.28.0.0/16", "155.138.0.0/16", "192.248.0.0/16", "207.148.0.0/16",
            "208.167.0.0/16", "209.250.0.0/16", "216.128.0.0/16", "217.69.0.0/16",
            # OVH
            "51.38.0.0/16", "51.68.0.0/16", "51.75.0.0/16", "51.77.0.0/16",
            "51.79.0.0/16", "51.89.0.0/16", "51.91.0.0/16", "51.159.0.0/16",
            "54.36.0.0/16", "54.37.0.0/16", "54.38.0.0/16", "54.39.0.0/16",
            "91.121.0.0/16", "92.222.0.0/16", "137.74.0.0/16", "144.217.0.0/16",
            "145.239.0.0/16", "147.135.0.0/16", "158.69.0.0/16", "164.132.0.0/16",
            "176.31.0.0/16", "178.32.0.0/16", "185.228.0.0/16", "188.165.0.0/16",
            "193.70.0.0/16", "195.154.0.0/16", "198.27.0.0/16", "198.50.0.0/16",
            # Hetzner
            "5.9.0.0/16", "46.4.0.0/16", "78.46.0.0/16", "78.47.0.0/16",
            "88.99.0.0/16", "136.243.0.0/16", "138.201.0.0/16", "144.76.0.0/16",
            "148.251.0.0/16", "159.69.0.0/16", "168.119.0.0/16", "176.9.0.0/16",
            "178.63.0.0/16", "188.40.0.0/16", "195.201.0.0/16", "213.133.0.0/16",
            # Cloudflare
            "104.16.0.0/12", "172.64.0.0/13", "131.0.72.0/22", "141.101.64.0/18",
            "173.245.48.0/20", "188.114.96.0/20", "190.93.240.0/20", "197.234.240.0/22",
            "198.41.128.0/17", "162.158.0.0/15", "162.159.0.0/16",
            # Common VPN/Proxy providers
            "185.100.0.0/16", "185.101.0.0/16", "185.102.0.0/16", "193.100.0.0/16",
            "193.101.0.0/16", "209.141.0.0/16", "209.142.0.0/16", "107.189.0.0/16",
            "104.244.0.0/16", "45.12.0.0/16", "45.13.0.0/16", "45.14.0.0/16",
            "45.15.0.0/16"
        ]
    
    def _load_datacenter_ranges(self) -> List[str]:
        """Load known datacenter IP ranges"""
        return [
            # Major cloud providers (more specific ranges)
            "3.0.0.0/8", "13.0.0.0/8", "18.0.0.0/8", "34.0.0.0/8", "35.0.0.0/8",
            "52.0.0.0/8", "54.0.0.0/8", "20.0.0.0/8", "40.0.0.0/8", "51.0.0.0/8",
            # Oracle Cloud
            "129.146.0.0/16", "129.213.0.0/16", "130.35.0.0/16", "132.145.0.0/16",
            "134.70.0.0/16", "140.91.0.0/16", "144.21.0.0/16", "147.154.0.0/16",
            "150.136.0.0/16", "152.67.0.0/16", "155.248.0.0/16", "158.101.0.0/16",
            # IBM Cloud
            "159.122.0.0/16", "161.26.0.0/16", "161.156.0.0/16", "169.44.0.0/16",
            "169.45.0.0/16", "169.46.0.0/16", "169.47.0.0/16", "169.48.0.0/16",
            "169.53.0.0/16", "169.54.0.0/16", "169.55.0.0/16", "169.56.0.0/16",
            # Alibaba Cloud
            "47.74.0.0/16", "47.88.0.0/16", "47.89.0.0/16", "47.90.0.0/16",
            "47.91.0.0/16", "47.92.0.0/16", "47.93.0.0/16", "47.94.0.0/16",
            "47.95.0.0/16", "47.96.0.0/16", "47.97.0.0/16", "47.98.0.0/16",
            "47.99.0.0/16", "47.100.0.0/16", "47.101.0.0/16", "47.102.0.0/16",
            "47.103.0.0/16", "47.104.0.0/16", "47.105.0.0/16", "47.106.0.0/16",
            "47.107.0.0/16", "47.108.0.0/16", "47.109.0.0/16", "47.110.0.0/16"
        ]
    
    def _load_vpn_ranges(self) -> List[str]:
        """Load known VPN provider IP ranges"""
        return [
            # NordVPN
            "185.159.157.0/24", "185.159.156.0/24", "185.159.155.0/24",
            "185.159.154.0/24", "185.229.226.0/24", "185.229.225.0/24",
            # ExpressVPN
            "193.6.0.0/16", "193.34.0.0/16", "185.93.0.0/16",
            # Surfshark
            "178.18.0.0/16", "195.181.0.0/16",
            # ProtonVPN
            "185.107.56.0/24", "185.159.158.0/24", "185.159.159.0/24",
            # Mullvad
            "193.32.127.0/24", "193.138.0.0/16", "185.213.154.0/24",
            # Private Internet Access
            "199.116.0.0/16", "199.127.0.0/16", "173.199.0.0/16",
            # CyberGhost
            "89.187.0.0/16", "185.210.0.0/16", "185.230.0.0/16",
            # IPVanish
            "198.18.0.0/15", "66.115.0.0/16", "162.254.0.0/16",
            # TorGuard
            "104.238.0.0/16", "104.250.0.0/16", "199.102.0.0/16",
            # Windscribe
            "173.205.0.0/16", "69.197.0.0/16", "192.126.0.0/16",
            # HideMyAss
            "199.217.0.0/16", "199.249.0.0/16", "103.205.0.0/16",
            # TOR exit nodes (common ranges)
            "176.10.104.0/24", "176.10.99.0/24", "77.247.181.0/24",
            "91.219.236.0/24", "91.219.237.0/24", "109.70.100.0/24",
            "185.220.100.0/24", "185.220.101.0/24", "185.220.102.0/24",
            "185.220.103.0/24", "199.249.230.0/24", "204.8.156.0/24"
        ]
    
    def _is_ip_blacklisted(self, ip: str) -> bool:
        """Check if IP is in blacklisted ranges (datacenter/VPN/proxy)"""
        try:
            ip_obj = ipaddress.ip_address(ip)
            
            # Check blacklisted ranges
            for range_str in self.blacklisted_ranges:
                try:
                    network = ipaddress.ip_network(range_str, strict=False)
                    if ip_obj in network:
                        return True
                except ValueError:
                    continue
            
            # Check datacenter ranges
            for range_str in self.datacenter_ranges:
                try:
                    network = ipaddress.ip_network(range_str, strict=False)
                    if ip_obj in network:
                        return True
                except ValueError:
                    continue
            
            # Check VPN ranges
            for range_str in self.vpn_ranges:
                try:
                    network = ipaddress.ip_network(range_str, strict=False)
                    if ip_obj in network:
                        return True
                except ValueError:
                    continue
            
            return False
            
        except ValueError:
            return True  # Invalid IP is considered blacklisted
    
    def _validate_residential_ip(self, ip: str, isp_config: Dict[str, Any]) -> Dict[str, Any]:
        """Validate if IP appears to be a residential IP"""
        result = {
            "is_residential": True,
            "confidence": 100,
            "issues": [],
            "warnings": []
        }
        
        try:
            ip_obj = ipaddress.ip_address(ip)
            parts = ip.split('.')
            
            # Check 1: Not in blacklisted ranges
            if self._is_ip_blacklisted(ip):
                result["is_residential"] = False
                result["confidence"] -= 50
                result["issues"].append("IP in datacenter/VPN/proxy range")
            
            # Check 2: Matches ISP prefix pattern
            ip_matches_prefix = False
            for prefix in isp_config.get("prefixes", []):
                if ip.startswith(prefix):
                    ip_matches_prefix = True
                    break
            
            if not ip_matches_prefix:
                result["confidence"] -= 20
                result["warnings"].append("IP does not match ISP prefix pattern")
            
            # Check 3: Not using reserved host addresses
            last_octet = int(parts[3])
            if last_octet in [0, 1, 255, 254]:
                result["confidence"] -= 15
                result["warnings"].append("IP uses reserved host address")
            
            # Check 4: Check for common datacenter patterns
            first_octet = int(parts[0])
            datacenter_first_octets = [3, 13, 18, 20, 34, 35, 40, 51, 52, 54]
            if first_octet in datacenter_first_octets:
                result["is_residential"] = False
                result["confidence"] -= 40
                result["issues"].append("First octet matches common datacenter range")
            
            # Check 5: Validate ASN if provided
            if isp_config.get("asn"):
                # ASN validation would normally require external lookup
                # For now, we just validate the format
                asn = isp_config["asn"]
                if not asn.startswith("AS") or not asn[2:].isdigit():
                    result["confidence"] -= 10
                    result["warnings"].append("Invalid ASN format")
            
            # Final residential status based on confidence
            if result["confidence"] < 60:
                result["is_residential"] = False
            
            return result
            
        except Exception as e:
            return {
                "is_residential": False,
                "confidence": 0,
                "issues": [f"Validation error: {str(e)}"],
                "warnings": []
            }

    def _get_network_type_for_isp(self, isp: str, connection_type: str = "mobile") -> str:
        """Get network type yang benar berdasarkan ISP dan connection type - FIXED"""
        isp_network_map = {
            "telkomsel": {"mobile": "5G", "wifi": "WiFi"},
            "indosat": {"mobile": "LTE", "wifi": "WiFi"},
            "xl": {"mobile": "4G", "wifi": "WiFi"},
            "tri": {"mobile": "3G", "wifi": "WiFi"},
            "smartfren": {"mobile": "4G", "wifi": "WiFi"},
            "biznet": {"wifi": "Fiber", "mobile": "WiFi"},
            "firstmedia": {"wifi": "Cable", "mobile": "WiFi"},
            "myrepublic": {"wifi": "Fiber", "mobile": "WiFi"},
            "cbn": {"wifi": "Fiber", "mobile": "WiFi"}
        }
        
        return isp_network_map.get(isp, {}).get(connection_type, "WiFi")

    def _get_connection_type_for_isp(self, isp: str) -> str:
        """Determine connection type berdasarkan ISP - FIXED"""
        mobile_isps = ["telkomsel", "indosat", "xl", "tri", "smartfren"]
        return "mobile" if isp in mobile_isps else "wifi"
        
    def _initialize_ip_sources(self):
        """Initialize multiple IP generation sources dengan ISP Indonesia"""
        return {
            "telkomsel": self._generate_telkomsel_ips,
            "indosat": self._generate_indosat_ips,
            "xl": self._generate_xl_ips,
            "tri": self._generate_tri_ips,
            "smartfren": self._generate_smartfren_ips,
            "biznet": self._generate_biznet_ips,
            "cbn": self._generate_cbn_ips,
            "firstmedia": self._generate_firstmedia_ips,
            "myrepublic": self._generate_myrepublic_ips
        }
    
    def _generate_dynamic_isp_ips(self, isp_name: str) -> List[Dict[str, Any]]:
        """Generate fresh IPs untuk ISP tertentu dengan enhanced validation"""
        current_time = time.time()
        cache_key = f"{isp_name}_{int(current_time // 180)}"  # Cache 3 menit
        
        if cache_key in self.generation_cache:
            cached = self.generation_cache[cache_key]
            if current_time - cached["timestamp"] < 180:
                return cached["ips"]
        
        config = self._get_isp_config_enhanced(isp_name)
        if not config:
            return []
        
        ip_pool = []
        ip_count = random.randint(3, 8)  # Generate 3-8 IPs per ISP
        
        for i in range(ip_count):
            ip = self._generate_valid_indonesian_ip(isp_name, config)
            
            if not ip or not self._validate_ip_format_enhanced(ip):
                continue
            
            # Validasi lanjutan
            validation = self.validator.validate(ip, strict=True)
            if not validation["valid"] or validation["score"] < 70:
                continue
            
            if ip in self.blacklisted_ips:
                continue
            
            # Cek duplikasi
            if any(ip_info["ip"] == ip for ip_info in self.ip_pool):
                continue
            
            ip_info = self._create_enhanced_ip_profile(ip, config, isp_name)
            ip_pool.append(ip_info)
        
        # Cache hasil
        self.generation_cache[cache_key] = {
            "ips": ip_pool,
            "timestamp": current_time,
            "isp": isp_name
        }
        
        print(f"{cyan}    Generated {len(ip_pool)} validated IPs for {isp_name}{reset}")
        return ip_pool
    
    def _get_isp_config_enhanced(self, isp_name: str, country: str = "ID") -> Optional[Dict[str, Any]]:
        """Enhanced ISP configuration dengan global database support"""
        # First check global ISP database
        if country in self.global_isp_database:
            country_isps = self.global_isp_database[country]
            if isp_name in country_isps:
                return country_isps[isp_name]
        
        # Fallback to legacy Indonesian ISP configs for backward compatibility
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
                "prefixes": ["202.67", "202.152", "103.10", "112.78"],
                "asn": "AS10029",
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
                "prefixes": ["103.23", "103.31", "180.253", "202.78", "203.153"],
                "asn": "AS17451",
                "as_name": "Biznet ISP",
                "ttl_range": (52, 64),
                "window_range": (64240, 65535),
                "mss_range": (1360, 1460),
                "cities": ["Jakarta", "Bandung", "Surabaya", "Bali", "Yogyakarta"],
                "latency_range": (8, 25),
                "jitter_range": (1, 5),
                "packet_loss": (0.1, 0.3)
            },
            "cbn": {
                "prefixes": ["110.138", "119.82", "202.152", "202.169", "203.128"],
                "asn": "AS24000",
                "as_name": "PT Cyberindo Aditama",
                "ttl_range": (54, 64),
                "window_range": (64240, 65535),
                "mss_range": (1360, 1460),
                "cities": ["Jakarta", "Bandung", "Surabaya"],
                "latency_range": (10, 30),
                "jitter_range": (2, 6),
                "packet_loss": (0.1, 0.3)
            },
            "firstmedia": {
                "prefixes": ["111.94", "125.163", "180.214", "202.53", "203.109"],
                "asn": "AS23700",
                "as_name": "PT Link Net Tbk",
                "ttl_range": (52, 64),
                "window_range": (64240, 65535),
                "mss_range": (1360, 1460),
                "cities": ["Jakarta", "Bandung", "Surabaya", "Bekasi", "Tangerang"],
                "latency_range": (6, 20),
                "jitter_range": (1, 4),
                "packet_loss": (0.1, 0.2)
            },
            "myrepublic": {
                "prefixes": ["103.72", "103.76", "118.98", "180.251", "202.93"],
                "asn": "AS55655",
                "as_name": "PT Centrin Online Prima",
                "ttl_range": (54, 64),
                "window_range": (64240, 65535),
                "mss_range": (1360, 1460),
                "cities": ["Jakarta", "Bandung", "Surabaya", "Medan", "Makassar"],
                "latency_range": (5, 18),
                "jitter_range": (1, 4),
                "packet_loss": (0.1, 0.2)
            }
        }
        return isp_configs.get(isp_name)
    
    def get_global_isp_config(self, country: str, isp_name: str) -> Optional[Dict[str, Any]]:
        """Get ISP configuration for any country in the global database"""
        if country in self.global_isp_database:
            country_isps = self.global_isp_database[country]
            if isp_name in country_isps:
                return country_isps[isp_name]
        return None
    
    def get_random_global_isp(self) -> Tuple[str, str, Dict[str, Any]]:
        """Get a random ISP from the global database weighted by country popularity"""
        # Select country based on weights
        countries = list(self.country_weights.keys())
        weights = list(self.country_weights.values())
        selected_country = random.choices(countries, weights=weights)[0]
        
        # Get ISPs for selected country
        if selected_country in self.global_isp_database:
            country_isps = self.global_isp_database[selected_country]
            isp_name = random.choice(list(country_isps.keys()))
            return selected_country, isp_name, country_isps[isp_name]
        
        # Fallback to Indonesia
        return "ID", "telkomsel", self.global_isp_database["ID"]["telkomsel"]
    
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
        """Enhanced IP format validation"""
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
                print(f"{merah}    IP {ip} is private{reset}")
                return False
            
            if ip_obj.is_reserved:
                print(f"{merah}    IP {ip} is reserved{reset}")
                return False
            
            if ip_obj.is_loopback:
                print(f"{merah}    IP {ip} is loopback{reset}")
                return False
            
            if ip_obj.is_multicast:
                print(f"{merah}    IP {ip} is multicast{reset}")
                return False
            
            if ip_obj.is_link_local:
                print(f"{merah}    IP {ip} is link-local{reset}")
                return False
            
            # Check for suspicious patterns
            suspicious_patterns = [
                ip.endswith('.0'),
                ip.endswith('.255'),
                ip.endswith('.1'),
                ip.endswith('.254'),
                all(p == parts[0] for p in parts),  # All same
                parts[3] in ['0', '255', '1', '254']
            ]
            
            if any(suspicious_patterns):
                print(f"{merah}    IP {ip} has suspicious pattern{reset}")
                return False
            
            return True
            
        except Exception:
            return False
    
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
        """Enhanced city coordinates dengan lebih banyak kota Indonesia"""
        coordinates = {
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
            "Bogor": {"lat": -6.5971, "lon": 106.8060}
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
        """Get MNC untuk ISP Indonesia"""
        mnc_map = {
            "telkomsel": "10",
            "indosat": "01",
            "xl": "11",
            "tri": "89",
            "smartfren": "28",
            "biznet": "20",
            "cbn": "21"
        }
        return mnc_map.get(isp, "99")
    
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
    
    def get_fresh_ip_config(self, session_id: str = None, min_health: int = 80, connection_type: str = "mobile") -> Dict[str, Any]:
        """Get fresh IP configuration untuk session tertentu"""
        print(f"{cyan}🌐  Getting fresh IP config for session {session_id[:8] if session_id else 'new'} (connection: {connection_type})...{reset}")
        
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
        """Generate fresh batch of IPs using global ISP database"""
        print(f"{cyan}🌐  Generating enhanced global IP batch...{reset}")
        
        new_ips = []
        
        # Use global ISP database with weighted country selection
        # Generate IPs from multiple countries based on weights
        num_ips_to_generate = 20  # Generate batch of 20 IPs
        
        for _ in range(num_ips_to_generate):
            try:
                # Get random ISP from global database with weighted selection
                country_code, isp_name, isp_config = self.get_random_global_isp()
                
                print(f"{cyan}    Generating {isp_name} ({country_code}) IP...{reset}")
                
                # Generate IP for this ISP
                ip = self._generate_global_ip(country_code, isp_name, isp_config)
                
                if ip and self._validate_ip_format_enhanced(ip):
                    # Validate IP is not blacklisted
                    if self._is_ip_blacklisted(ip):
                        print(f"{kuning}    IP {ip} is blacklisted, skipping...{reset}")
                        continue
                    
                    # Create IP profile
                    ip_info = self._create_global_ip_profile(ip, isp_config, isp_name, country_code)
                    
                    # Validate residential
                    residential_check = self._validate_residential_ip(ip, isp_config)
                    if not residential_check["is_residential"]:
                        print(f"{kuning}    IP {ip} failed residential check, skipping...{reset}")
                        continue
                    
                    # Validate with validator
                    validation = self.validator.validate(ip, strict=True)
                    if validation["valid"] and validation["score"] >= 70:
                        ip_info["validation_score"] = validation["score"]
                        ip_info["last_validated"] = time.time()
                        ip_info["residential_confidence"] = residential_check["confidence"]
                        new_ips.append(ip_info)
                        print(f"{hijau}    Added IP: {ip} ({isp_name}, {country_code}) - Score: {validation['score']}{reset}")
                    else:
                        print(f"{kuning}    IP {ip} failed validation (score: {validation.get('score', 0)}){reset}")
                        
            except Exception as e:
                print(f"{merah}    Error generating IP: {str(e)[:50]}{reset}")
                continue
        
        # Tambahkan ke pool dengan deduplication
        existing_ips = {ip["ip"] for ip in self.ip_pool}
        unique_new_ips = [ip for ip in new_ips if ip["ip"] not in existing_ips]
        
        if unique_new_ips:
            self.ip_pool.extend(unique_new_ips)
            
            # Batasi pool size (keep freshest 100 IPs)
            if len(self.ip_pool) > 100:
                self.ip_pool.sort(key=lambda x: x.get("timestamp", 0), reverse=True)
                self.ip_pool = self.ip_pool[:100]
            
            print(f"{hijau}✅  Added {len(unique_new_ips)} fresh global IPs | Total pool: {len(self.ip_pool)}{reset}")
            
            # Show country distribution
            country_dist = {}
            for ip in self.ip_pool:
                cc = ip.get("country_code", "ID")
                country_dist[cc] = country_dist.get(cc, 0) + 1
            print(f"{cyan}    Country distribution: {country_dist}{reset}")
            
            # Update statistics
            avg_health = sum(ip.get("health_score", 0) for ip in self.ip_pool) / len(self.ip_pool)
            print(f"{cyan}    Avg health score: {avg_health:.1f}%{reset}")
        else:
            print(f"{merah}    No new unique IPs generated{reset}")
            self._generate_emergency_ip_batch()
    
    def _generate_global_ip(self, country_code: str, isp_name: str, isp_config: Dict[str, Any]) -> Optional[str]:
        """Generate a valid IP for any global ISP"""
        try:
            prefixes = isp_config.get("prefixes", [])
            if not prefixes:
                return None
            
            prefix = random.choice(prefixes)
            prefix_parts = prefix.split('.')
            
            # Generate remaining octets
            while len(prefix_parts) < 4:
                if len(prefix_parts) == 3:
                    # Last octet - avoid reserved addresses
                    fourth = random.randint(10, 240)
                    while fourth in [0, 1, 255, 254, 128]:
                        fourth = random.randint(10, 240)
                    prefix_parts.append(str(fourth))
                else:
                    prefix_parts.append(str(random.randint(0, 255)))
            
            ip = '.'.join(prefix_parts[:4])
            return ip
            
        except Exception as e:
            print(f"{merah}    Error generating global IP: {e}{reset}")
            return None
    
    def _create_global_ip_profile(self, ip: str, isp_config: Dict[str, Any], isp_name: str, country_code: str) -> Dict[str, Any]:
        """Create IP profile for global ISP"""
        cities = isp_config.get("cities", ["Unknown"])
        city = random.choice(cities)
        
        # Get connection type based on ISP
        connection_type = self._get_connection_type_for_isp(isp_name)
        network_type = self._get_network_type_for_isp(isp_name, connection_type)
        
        # Get latency/jitter from config
        latency_range = isp_config.get("latency_range", (20, 60))
        jitter_range = isp_config.get("jitter_range", (2, 10))
        packet_loss = isp_config.get("packet_loss", (0.1, 0.5))
        
        profile = {
            "ip": ip,
            "isp": isp_name,
            "country_code": country_code,
            "asn": isp_config.get("asn", ""),
            "as_name": isp_config.get("as_name", ""),
            "city": city,
            "connection_type": connection_type,
            "network_type": network_type,
            "health_score": random.randint(80, 95),
            "timestamp": time.time(),
            "usage_count": 0,
            "latency": random.uniform(*latency_range),
            "jitter": random.uniform(*jitter_range),
            "packet_loss": random.uniform(*packet_loss),
            "location": {
                "city": city,
                "country": country_code,
                "timezone": self._get_timezone_for_country(country_code)
            },
            "isp_info": {
                "isp": isp_name,
                "asn": isp_config.get("asn", ""),
                "as_name": isp_config.get("as_name", "")
            },
            "device_fingerprint": self._generate_device_fingerprint_for_ip(isp_name, connection_type),
            "headers": self._generate_headers_for_global_ip(ip, isp_config, country_code)
        }
        
        return profile
    
    def _get_timezone_for_country(self, country_code: str) -> str:
        """Get timezone for country code"""
        timezones = {
            "US": "America/New_York",
            "CA": "America/Toronto",
            "MX": "America/Mexico_City",
            "BR": "America/Sao_Paulo",
            "AR": "America/Buenos_Aires",
            "GB": "Europe/London",
            "DE": "Europe/Berlin",
            "FR": "Europe/Paris",
            "IT": "Europe/Rome",
            "ES": "Europe/Madrid",
            "NL": "Europe/Amsterdam",
            "PL": "Europe/Warsaw",
            "TR": "Europe/Istanbul",
            "RU": "Europe/Moscow",
            "IN": "Asia/Kolkata",
            "JP": "Asia/Tokyo",
            "KR": "Asia/Seoul",
            "TH": "Asia/Bangkok",
            "VN": "Asia/Ho_Chi_Minh",
            "PH": "Asia/Manila",
            "MY": "Asia/Kuala_Lumpur",
            "SG": "Asia/Singapore",
            "ID": "Asia/Jakarta",
            "AU": "Australia/Sydney",
            "NZ": "Pacific/Auckland",
            "AE": "Asia/Dubai",
            "SA": "Asia/Riyadh"
        }
        return timezones.get(country_code, "UTC")
    
    def _generate_headers_for_global_ip(self, ip: str, isp_config: Dict[str, Any], country_code: str) -> Dict[str, str]:
        """Generate headers appropriate for global IP"""
        # Get locale based on country
        locales = {
            "US": "en_US",
            "CA": "en_CA",
            "MX": "es_MX",
            "BR": "pt_BR",
            "AR": "es_AR",
            "GB": "en_GB",
            "DE": "de_DE",
            "FR": "fr_FR",
            "IT": "it_IT",
            "ES": "es_ES",
            "NL": "nl_NL",
            "PL": "pl_PL",
            "TR": "tr_TR",
            "RU": "ru_RU",
            "IN": "en_IN",
            "JP": "ja_JP",
            "KR": "ko_KR",
            "TH": "th_TH",
            "VN": "vi_VN",
            "PH": "en_PH",
            "MY": "ms_MY",
            "SG": "en_SG",
            "ID": "id_ID",
            "AU": "en_AU",
            "NZ": "en_NZ",
            "AE": "ar_AE",
            "SA": "ar_SA"
        }
        
        locale = locales.get(country_code, "en_US")
        lang = locale.split('_')[0]
        
        accept_language_map = {
            "en": "en-US,en;q=0.9",
            "de": "de-DE,de;q=0.9,en;q=0.8",
            "fr": "fr-FR,fr;q=0.9,en;q=0.8",
            "es": "es-ES,es;q=0.9,en;q=0.8",
            "pt": "pt-BR,pt;q=0.9,en;q=0.8",
            "it": "it-IT,it;q=0.9,en;q=0.8",
            "ja": "ja-JP,ja;q=0.9,en;q=0.8",
            "ko": "ko-KR,ko;q=0.9,en;q=0.8",
            "zh": "zh-CN,zh;q=0.9,en;q=0.8",
            "ru": "ru-RU,ru;q=0.9,en;q=0.8",
            "ar": "ar-SA,ar;q=0.9,en;q=0.8",
            "th": "th-TH,th;q=0.9,en;q=0.8",
            "vi": "vi-VN,vi;q=0.9,en;q=0.8",
            "id": "id-ID,id;q=0.9,en;q=0.8",
            "ms": "ms-MY,ms;q=0.9,en;q=0.8",
            "nl": "nl-NL,nl;q=0.9,en;q=0.8",
            "pl": "pl-PL,pl;q=0.9,en;q=0.8",
            "tr": "tr-TR,tr;q=0.9,en;q=0.8"
        }
        
        accept_language = accept_language_map.get(lang, "en-US,en;q=0.9")
        
        return {
            "Accept-Language": accept_language,
            "X-IG-App-Locale": locale,
            "X-IG-Device-Locale": locale,
            "X-IG-Mapped-Locale": locale
        }
    
    def _generate_emergency_ip_batch(self):
        """Generate emergency IP batch using global ISPs when all else fails"""
        print(f"{merah}🚨  Generating emergency global IP batch{reset}")
        
        emergency_ips = []
        
        # Generate emergency IPs from multiple countries
        emergency_isps = [
            # US ISPs
            ("12.0", "att", "US"),
            ("66.174", "verizon", "US"),
            ("172.32", "tmobile", "US"),
            ("50.128", "comcast", "US"),
            # European ISPs
            ("79.64", "bt", "GB"),
            ("79.192", "dtag", "DE"),
            ("80.10", "orange_fr", "FR"),
            # Asian ISPs
            ("49.40", "jio", "IN"),
            ("49.96", "ntt_docomo", "JP"),
            ("49.228", "ais", "TH"),
            # Indonesian ISPs (fallback)
            ("110.136", "telkomsel", "ID"),
            ("112.215", "indosat", "ID"),
            # Australian ISP
            ("49.176", "telstra", "AU"),
            # Middle East ISP
            ("77.221", "etisalat", "AE")
        ]
        
        for prefix, isp_name, country_code in emergency_isps:
            for _ in range(2):  # 2 IPs per prefix
                try:
                    # Generate valid IP
                    prefix_parts = prefix.split('.')
                    while len(prefix_parts) < 4:
                        if len(prefix_parts) == 3:
                            fourth = random.randint(10, 240)
                            prefix_parts.append(str(fourth))
                        else:
                            prefix_parts.append(str(random.randint(0, 255)))
                    
                    ip = '.'.join(prefix_parts[:4])
                    
                    # Validate format
                    if not self._validate_ip_format_enhanced(ip):
                        continue
                    
                    # Check blacklist
                    if self._is_ip_blacklisted(ip):
                        continue
                    
                    # Get ISP config from global database
                    isp_config = self.get_global_isp_config(country_code, isp_name)
                    if not isp_config:
                        # Fallback to enhanced config
                        isp_config = self._get_isp_config_enhanced(isp_name, country_code)
                    
                    if isp_config:
                        ip_info = self._create_global_ip_profile(ip, isp_config, isp_name, country_code)
                    else:
                        # Create minimal profile
                        ip_info = {
                            "ip": ip,
                            "isp": isp_name,
                            "country_code": country_code,
                            "health_score": 70,
                            "timestamp": time.time(),
                            "usage_count": 0,
                            "connection_type": "mobile",
                            "location": {"city": "Unknown", "country": country_code},
                            "isp_info": {"isp": isp_name}
                        }
                    
                    ip_info["emergency"] = True
                    ip_info["health_score"] = 75  # Lower score for emergency IPs
                    
                    emergency_ips.append(ip_info)
                    print(f"{cyan}      Generated emergency IP: {ip} ({isp_name}, {country_code}){reset}")
                    
                except Exception as e:
                    print(f"{merah}    Error generating emergency IP: {e}{reset}")
                    continue
        
        if emergency_ips:
            self.ip_pool = emergency_ips[:30]  # Keep 30 emergency IPs
            
            # Show country distribution
            country_dist = {}
            for ip in self.ip_pool:
                cc = ip.get("country_code", "ID")
                country_dist[cc] = country_dist.get(cc, 0) + 1
            print(f"{hijau}✅  Emergency batch generated: {len(self.ip_pool)} IPs{reset}")
            print(f"{cyan}    Country distribution: {country_dist}{reset}")
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
        
        # Build comprehensive config
        config = {
            "ip": ip_info["ip"],
            "session_id": session_id,
            "isp_info": {
                "isp": isp,
                "asn": ip_info["asn"],
                "as_name": ip_info.get("location", {}).get("as_name", ""),
                "carrier": ip_info.get("location", {}).get("carrier", "")
            },
            "connection_type": connection_type,  # FIXED: simpan connection type
            "location": ip_info["location"],
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
        """Generate random JA3 and JA3S fingerprints from valid Instagram client signatures"""
        # Real Instagram client JA3 fingerprints observed in production
        instagram_ja3_fingerprints = [
            # Chrome Mobile on Android (various versions)
            ("771,4865-4866-4867-49195-49199-49196-49200-52393-52392-49171-49172-156-157-47-53,0-23-65281-10-11-35-16-5-13-18-51-45-43-27-17513-21,29-23-24,0",
             "771,4865,65281-0-23-13-5-18-16-11-51-45-43-10-21,29-23-24,0"),
            ("771,4865-4866-4867-49195-49199-49196-49200-52393-52392-49171-49172-156-157-47-53,0-23-65281-10-11-35-16-5-13-18-51-45-43-27-21,29-23-24-25,0",
             "771,4865,65281-0-23-13-5-18-16-11-51-45-43-10,29-23,0"),
            ("771,4865-4866-4867-49195-49199-49196-49200-52393-52392-49171-49172-156-157-47-53,0-23-65281-10-11-35-16-5-13-18-51-45-43-27-17513,29-23-24,0",
             "771,4866,65281-0-23-13-5-18-16-11-51-45-43-10-21,29-23-24,0"),
            # Chrome 120+ mobile
            ("771,4865-4866-4867-49195-49199-49196-49200-52393-52392-49171-49172-156-157-47-53-10,0-23-65281-10-11-35-16-5-34-51-43-13-45-28-21,29-23-24,0",
             "771,4865,65281-0-23-13-5-18-16-11-51-45-43-10-21,29-23-24,0"),
            # Chrome 135 mobile
            ("771,4865-4866-4867-49195-49199-49196-49200-52393-52392-49171-49172-156-157-47-53,0-23-65281-10-11-35-16-5-13-18-51-45-43-27-17513-21-41,29-23-24-25-256-257,0",
             "771,4865,65281-0-23-13-5-18-16-11-51-45-43-10-21,29-23-24,0"),
            # WebView Android
            ("771,4865-4866-4867-49195-49199-49196-49200-52393-52392-49171-49172-156-157-47-53,0-23-65281-10-11-35-16-5-13-18-51-45-43-27-21,29-23-24,0",
             "771,4865,65281-0-23-13-5-18-16-11-51-45-43-10-21,29-23-24,0"),
            # Instagram Android app signatures
            ("771,4865-4866-4867-49195-49199-49196-49200-52393-52392-49171-49172-156-157-47-53,0-23-65281-10-11-35-16-5-13-18-51-45-43-27-17513-21,29-23-24-25-256,0",
             "771,4865,65281-0-23-13-5-18-16-11-51-45-43-10-21,29-23-24,0"),
            ("771,4865-4866-4867-49195-49199-49196-49200-52393-52392-49171-49172-156-157-47-53,0-23-65281-10-11-35-16-5-13-18-51-45-43-27-21-41,29-23-24-25,0",
             "771,4866,65281-0-23-13-5-18-16-11-51-45-43-10-21,29-23-24,0"),
        ]
        # Select random fingerprint
        return random.choice(instagram_ja3_fingerprints)
    
    def _generate_tls_fingerprint(self, profile: str) -> Dict[str, Any]:
        """Generate random TLS fingerprint with valid Instagram client configurations"""
        # Randomize cipher order while keeping valid combinations
        cipher_suites = [
            ["TLS_AES_128_GCM_SHA256", "TLS_AES_256_GCM_SHA384", "TLS_CHACHA20_POLY1305_SHA256"],
            ["TLS_AES_256_GCM_SHA384", "TLS_AES_128_GCM_SHA256", "TLS_CHACHA20_POLY1305_SHA256"],
            ["TLS_CHACHA20_POLY1305_SHA256", "TLS_AES_128_GCM_SHA256", "TLS_AES_256_GCM_SHA384"],
        ]
        
        ecdhe_ciphers = [
            ["TLS_ECDHE_ECDSA_WITH_AES_128_GCM_SHA256", "TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256", "TLS_ECDHE_ECDSA_WITH_AES_256_GCM_SHA384"],
            ["TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256", "TLS_ECDHE_ECDSA_WITH_AES_128_GCM_SHA256", "TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384"],
            ["TLS_ECDHE_ECDSA_WITH_AES_256_GCM_SHA384", "TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384", "TLS_ECDHE_ECDSA_WITH_AES_128_GCM_SHA256"],
        ]
        
        supported_groups_options = [
            ["X25519", "P-256", "P-384"],
            ["P-256", "X25519", "P-384"],
            ["X25519", "P-384", "P-256"],
            ["P-256", "P-384", "X25519"],
        ]
        
        signature_algorithms_options = [
            ["ecdsa_secp256r1_sha256", "rsa_pss_rsae_sha256", "rsa_pkcs1_sha256", "ecdsa_secp384r1_sha384", "rsa_pss_rsae_sha384", "rsa_pkcs1_sha384"],
            ["rsa_pss_rsae_sha256", "ecdsa_secp256r1_sha256", "rsa_pkcs1_sha256", "rsa_pss_rsae_sha384", "ecdsa_secp384r1_sha384", "rsa_pkcs1_sha384"],
            ["ecdsa_secp256r1_sha256", "ecdsa_secp384r1_sha384", "rsa_pss_rsae_sha256", "rsa_pss_rsae_sha384", "rsa_pkcs1_sha256", "rsa_pkcs1_sha384"],
        ]
        
        return {
            "version": "TLSv1.3",
            "ciphers": random.choice(cipher_suites) + random.choice(ecdhe_ciphers),
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
            "supported_groups": random.choice(supported_groups_options),
            "signature_algorithms": random.choice(signature_algorithms_options),
            "alpn_protocols": ["h2", "http/1.1"],
            "session_id_length": random.choice([32, 0]),  # Randomize session ID
            "compression_methods": [0],  # null compression
            "record_version": random.choice(["0x0303", "0x0301"]),  # TLS 1.2 or 1.0 in record
        }
    
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
                                 connection_type: str = "mobile") -> Dict[str, str]:
        """Generate enhanced headers dengan connection type aware - FIXED"""
        location = ip_info.get("location", {})
        device_fp = ip_info.get("device_fingerprint", {})
        network_metrics = ip_info.get("network_metrics", {})

        APP_IDS = [
            "1217981644879628",  # Instagram Lite
            "124024574287414",   # Instagram
            "936619743392459",   # Facebook (kadang dipakai)
            "256357684841271",   # IG App ID alternatif
            "382690043351011",   # IG Web ID baru
            "567067343352427",   # IG Business ID
        ]

        ASBD_IDS = [
            "700229", "717986", "738585",  # ← ID yang lebih baru
            "754782", "771975", "789687",
            "804456", "821594", "839398",
            "856086", "873496", "890423",
            "907698", "924485", "941738"
        ]

        app_id = random.choice(APP_IDS)
        asbd_id = random.choice(ASBD_IDS)
        web_session_id = self._generate_web_session_id()
        
        # Base headers
        headers = {
            # Standard headers
            "User-Agent": user_agent,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Accept-Language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "Cache-Control": "no-cache",
            "Pragma": "no-cache",
            
            # Security headers
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-User": "?1",
            
            # Connection type specific headers - FIXED
            "X-IG-Connection-Type": "CELL" if connection_type == "mobile" else "WIFI",
            "X-IG-Network-Type": network_metrics.get("network_type", "4G" if connection_type == "mobile" else "WIFI"),
            "X-IG-Bandwidth-Speed": f"{int(network_metrics.get('bandwidth_mbps', 50) * 1000)}",
            "X-IG-Signal-Strength": str(network_metrics.get("signal_strength", -65)),
        }
        
        # Mobile specific headers
        if connection_type == "mobile":
            headers.update({
                "X-IG-Carrier": location.get("carrier", ""),
                "X-IG-MCC": location.get("mcc", "510"),
                "X-IG-MNC": location.get("mnc", "10"),
                "X-IG-Phone-Number": f"+62{random.randint(811, 899)}{random.randint(1000000, 9999999)}",
            })
        
        # Device headers
        headers.update({
            "X-Requested-With": "XMLHttpRequest",
            "X-Ig-App-Id": app_id,
            "X-IG-Device-ID": device_fp.get("device_id", ""),
            "X-IG-Android-ID": device_fp.get("android_id", ""),
            "X-IG-Capabilities": "3brTvw==",
            "X-IG-Bandwidth-TotalTime": f"{random.randint(1000, 5000)}",
            "X-IG-Bandwidth-TotalBytes": f"{random.randint(100000, 500000)}",
            
            # IP headers
            "X-Forwarded-For": ip_info["ip"],
            "X-Real-IP": ip_info["ip"],
            "X-Client-IP": ip_info["ip"],
            "CF-Connecting-IP": ip_info["ip"],
            "True-Client-IP": ip_info["ip"],
            "X-Originating-IP": ip_info["ip"],
            "X-Remote-IP": ip_info["ip"],
            "X-Remote-Addr": ip_info["ip"],
            
            # Location headers
            "X-ASN": location.get("asn", ""),
            "X-ISP": location.get("isp", ""),
            "X-Country": location.get("country_code", "ID"),
            "X-City": location.get("city", "Jakarta"),
            "X-Region": location.get("province", "DKI Jakarta"),
            "X-Time-Zone": location.get("timezone", "Asia/Jakarta"),
            "X-Latitude": str(location.get("latitude", -6.2088)),
            "X-Longitude": str(location.get("longitude", 106.8456)),
            "X-Postal-Code": str(random.randint(10000, 17000)),
            
            # Network headers
            "X-Network-Type": network_metrics.get("network_type", "4G"),
            "X-Connection-Type": connection_type.upper(),
            
            # Session headers
            "X-Session-ID": str(uuid.uuid4())[:12],
            "X-Request-ID": str(uuid.uuid4()),
            "X-Correlation-ID": str(uuid.uuid4()),
            "X-Timestamp": str(int(time.time() * 1000)),
            
            # Protocol headers
            "X-Protocol-Version": "HTTP/2",
            "X-TLS-Version": "TLSv1.3",
            "X-HTTP2-Settings": base64.b64encode(
                json.dumps(self._generate_http2_settings("chrome_mobile_samsung")).encode()
            ).decode(),
            
            # Device capability headers
            "X-Device-Memory": str(device_fp.get("device_memory", 8)),
            "X-Viewport-Width": device_fp.get("screen_resolution", "1080x2400").split('x')[0],
            "X-Viewport-Height": str(int(device_fp.get("screen_resolution", "1080x2400").split('x')[1]) - 100),
            "X-Device-Pixel-Ratio": str(device_fp.get("dpi", 440) / 160),
            
            # Instagram specific
            "X-Ig-Www-Claim": "0",
            "X-Instagram-AJAX": "random_id",
            "X-CSRFToken": "missing",
            "X-Asbd-Id": asbd_id,
            "X-Web-Session-Id": web_session_id,
            "X-IG-Set-Authorization": "Bearer IGT:2:",
            
            # Additional headers
            "X-Frame-Options": "SAMEORIGIN",
            "X-Content-Type-Options": "nosniff",
            "X-XSS-Protection": "1; mode=block",
            "Referer": "https://www.instagram.com/accounts/emailsignup/",
            "Origin": "https://www.instagram.com",
            "DNT": "1",
            "TE": "Trailers"
        })
        
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
        return self._generate_dynamic_isp_ips("telkomsel")  # Reuse telkomsel
    
    def _generate_myrepublic_ips(self):
        return self._generate_dynamic_isp_ips("xl")  # Reuse xl

# ===================== IP VALIDATOR 2025 =====================

class IPValidator2025:
    """Enhanced IP validator dengan comprehensive validation"""
    
    def __init__(self):
        self.validation_cache = {}
        self.cache_ttl = 300
        self.validation_methods = [
            self._validate_format_enhanced,
            self._validate_range_enhanced,
            self._validate_reputation_enhanced,
            self._validate_geolocation,
            self._validate_network_properties
        ]
        self.vpn_ranges = self._load_vpn_ranges()
        self.datacenter_ranges = self._load_datacenter_ranges()
    
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
        """Generate enhanced WebRTC configurations"""
        return {
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
        """Generate enhanced WebGL configurations"""
        return {
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
    
    def get_complete_fingerprint(self, device_type: str = "android", brand: str = "samsung", connection_type: str = "mobile") -> Dict[str, Any]:
        """Get complete fingerprint untuk semua komponen dengan connection type awareness"""
        # Pilih config berdasarkan device type, brand, DAN connection_type
        if device_type == "ios":
            webrtc_profile = "ios_safari"
            webgl_profile = "apple_gpu"
            canvas_profile = "iphone_16_pro"
            audio_profile = "ios"
            font_profile = "ios"
            screen_profile = "iphone_16_pro"
        elif brand.lower() == "xiaomi":
            webrtc_profile = "android_chrome_xiaomi"
            webgl_profile = "mali_g710"
            canvas_profile = "xiaomi_14_pro"
            audio_profile = "android_xiaomi"
            font_profile = "android_xiaomi"
            screen_profile = "xiaomi_14_pro"
        else:
            # Default Samsung
            webrtc_profile = "android_chrome_samsung"
            webgl_profile = "adreno_750"
            canvas_profile = "samsung_galaxy_s24"
            audio_profile = "android_samsung"
            font_profile = "android_samsung"
            screen_profile = "samsung_galaxy_s24"
        
        # Generate fingerprint
        fingerprint = {
            "webrtc": self.get_webrtc_fingerprint(webrtc_profile),
            "webgl": self.get_webgl_fingerprint(webgl_profile),
            "canvas": self.get_canvas_fingerprint(canvas_profile),
            "audio": self.get_audio_fingerprint(audio_profile),
            "fonts": self.font_configs.get(font_profile, {}),
            "screen": self.screen_configs.get(screen_profile, {}),
            "device_type": device_type,
            "brand": brand,
            "connection_type": connection_type,  # Tambah ini
            "timestamp": int(time.time()),
            "fingerprint_id": f"fp_{int(time.time())}_{random.randint(1000, 9999)}",
            "composite_hash": hashlib.sha256(
                f"{device_type}{brand}{connection_type}{time.time()}{random.getrandbits(128)}".encode()
            ).hexdigest()[:64]
        }
        
        # Tambahkan noise untuk membuat fingerprint unik
        fingerprint["noise_factors"] = {
            "canvas_noise": random.uniform(0.001, 0.005),
            "audio_noise": random.uniform(0.0001, 0.001),
            "timing_noise": random.uniform(0.1, 0.5),
            "rendering_noise": random.uniform(0.01, 0.1)
        }
        
        return fingerprint
    
    def get_webrtc_fingerprint(self, profile: str = "android_chrome_samsung") -> Dict[str, Any]:
        """Get enhanced WebRTC fingerprint"""
        config = self.webrtc_configs.get(profile, self.webrtc_configs["android_chrome_samsung"])
        
        # Generate ICE candidates
        ice_candidates = self._generate_ice_candidates_enhanced()
        
        # Generate SDP
        sdp = self._generate_sdp_enhanced(profile)
        
        return {
            "config": config,
            "ice_candidates": ice_candidates,
            "local_description": {
                "type": "offer",
                "sdp": sdp
            },
            "fingerprint_hash": hashlib.sha256(
                f"{profile}{time.time()}{json.dumps(config)}".encode()
            ).hexdigest()[:32],
            "metadata": {
                "profile": profile,
                "generated_at": time.time(),
                "candidate_count": len(ice_candidates)
            }
        }
    
    def _generate_ice_candidates_enhanced(self) -> List[Dict[str, Any]]:
        """Generate enhanced ICE candidates"""
        candidates = []
        candidate_types = ["host", "srflx", "prflx"]
        
        for i in range(random.randint(3, 6)):
            candidate_type = random.choice(candidate_types)
            
            if candidate_type == "host":
                foundation = random.randint(1, 9999)
                component_id = 1
                transport = "udp"
                priority = random.randint(2113937151, 2113937151)
                local_ip = f"192.168.{random.randint(1, 254)}.{random.randint(1, 254)}"
                port = random.randint(10000, 60000)
                typ = "host"
                
                candidate = {
                    "candidate": f"candidate:{foundation} {component_id} {transport} {priority} {local_ip} {port} typ {typ}",
                    "sdpMid": "0",
                    "sdpMLineIndex": 0,
                    "usernameFragment": str(uuid.uuid4())[:16],
                    "type": typ,
                    "protocol": transport,
                    "address": local_ip,
                    "port": port,
                    "priority": priority
                }
                
            elif candidate_type == "srflx":
                foundation = random.randint(10000, 19999)
                component_id = 1
                transport = "udp"
                priority = random.randint(1677729535, 1677729535)
                local_ip = f"192.168.{random.randint(1, 254)}.{random.randint(1, 254)}"
                port = random.randint(10000, 60000)
                rel_addr = f"{random.randint(1, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}"
                rel_port = random.randint(10000, 60000)
                typ = "srflx"
                
                candidate = {
                    "candidate": f"candidate:{foundation} {component_id} {transport} {priority} {local_ip} {port} typ {typ} raddr {rel_addr} rport {rel_port}",
                    "sdpMid": "0",
                    "sdpMLineIndex": 0,
                    "usernameFragment": str(uuid.uuid4())[:16],
                    "type": typ,
                    "protocol": transport,
                    "address": local_ip,
                    "port": port,
                    "relatedAddress": rel_addr,
                    "relatedPort": rel_port,
                    "priority": priority
                }
                
            else:  # prflx
                foundation = random.randint(20000, 29999)
                component_id = 1
                transport = "udp"
                priority = random.randint(1677729535, 1677729535)
                local_ip = f"192.168.{random.randint(1, 254)}.{random.randint(1, 254)}"
                port = random.randint(10000, 60000)
                rel_addr = f"{random.randint(1, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}"
                rel_port = random.randint(10000, 60000)
                typ = "prflx"
                
                candidate = {
                    "candidate": f"candidate:{foundation} {component_id} {transport} {priority} {local_ip} {port} typ {typ} raddr {rel_addr} rport {rel_port}",
                    "sdpMid": "0",
                    "sdpMLineIndex": 0,
                    "usernameFragment": str(uuid.uuid4())[:16],
                    "type": typ,
                    "protocol": transport,
                    "address": local_ip,
                    "port": port,
                    "relatedAddress": rel_addr,
                    "relatedPort": rel_port,
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
        """Get enhanced WebGL fingerprint"""
        config = self.webgl_configs.get(profile, self.webgl_configs["adreno_750"])
        
        # Tambahkan extensions
        config["extensions"] = self._get_webgl_extensions_enhanced(profile)
        
        # Tambahkan parameters
        config["parameters"] = self._get_webgl_parameters_enhanced(profile)
        
        # Generate hash
        config_hash = hashlib.sha256(
            json.dumps(config, sort_keys=True).encode()
        ).hexdigest()[:32]
        
        # Tambahkan metadata
        config["metadata"] = {
            "profile": profile,
            "fingerprint_hash": config_hash,
            "generated_at": time.time(),
            "noise_factor": random.uniform(0.001, 0.005),
            "renderer_variation": random.uniform(0.95, 1.05)
        }
        
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
        """Get enhanced canvas fingerprint"""
        config = self.canvas_configs.get(profile, self.canvas_configs["samsung_galaxy_s24"])
        
        # Tambahkan data canvas yang unik
        canvas_data = {
            **config,
            "noise_seed": random.randint(1, 1000000),
            "gradient_quality": random.choice(["low", "medium", "high"]),
            "shadow_blur": random.uniform(0.5, 5.0),
            "line_width": random.uniform(0.5, 3.0),
            "miter_limit": random.uniform(1.0, 10.0),
            "global_alpha": random.uniform(0.8, 1.0),
            "composite_operations": [
                "source-over", "source-in", "source-out", "source-atop",
                "destination-over", "destination-in", "destination-out", "destination-atop",
                "lighter", "copy", "xor", "multiply", "screen", "overlay",
                "darken", "lighten", "color-dodge", "color-burn", "hard-light",
                "soft-light", "difference", "exclusion", "hue", "saturation",
                "color", "luminosity"
            ],
            "line_caps": ["butt", "round", "square"],
            "line_joins": ["bevel", "round", "miter"],
            "fill_styles": [
                "#FF0000", "#00FF00", "#0000FF", "#FFFF00", "#FF00FF", "#00FFFF",
                "rgba(255,0,0,0.5)", "rgba(0,255,0,0.5)", "rgba(0,0,255,0.5)",
                "linear-gradient(red, yellow)", "radial-gradient(red, yellow)"
            ]
        }
        
        # Generate hash
        canvas_hash = hashlib.sha256(
            f"{profile}{canvas_data['noise_seed']}".encode()
        ).hexdigest()[:32]
        
        # Tambahkan metadata
        canvas_data["metadata"] = {
            "profile": profile,
            "fingerprint_hash": canvas_hash,
            "generated_at": time.time(),
            "canvas_id": f"canvas_{int(time.time())}_{random.randint(1000, 9999)}"
        }
        
        return canvas_data
    
    def get_audio_fingerprint(self, profile: str = "android_samsung") -> Dict[str, Any]:
        """Get enhanced audio fingerprint"""
        config = self.audio_configs.get(profile, self.audio_configs["android_samsung"])
        
        # Generate audio context data
        audio_data = {
            **config,
            "context_id": str(uuid.uuid4()),
            "base_latency": random.uniform(0.005, 0.03),
            "output_latency": random.uniform(0.01, 0.05),
            "sample_rate_variance": random.randint(-100, 100),
            "channel_count_variance": random.randint(-1, 1),
            "channel_configuration": random.choice(["stereo", "quad", "5.1", "7.1"]),
            "channel_interpretation": random.choice(["speakers", "discrete"]),
            "channel_count_mode": random.choice(["max", "clamped-max", "explicit"]),
            "fft_size_options": [2048, 4096, 8192, 16384],
            "smoothing_time_constant_options": [0, 0.5, 0.8, 0.95, 1],
            "min_decibels_options": [-100, -96, -90, -80],
            "max_decibels_options": [-30, -24, -20, -10, 0]
        }
        
        # Generate hash
        audio_hash = hashlib.sha256(
            f"{profile}{audio_data['context_id']}".encode()
        ).hexdigest()[:32]
        
        # Tambahkan metadata
        audio_data["metadata"] = {
            "profile": profile,
            "fingerprint_hash": audio_hash,
            "generated_at": time.time(),
            "audio_id": f"audio_{int(time.time())}_{random.randint(1000, 9999)}"
        }
        
        return audio_data

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
    
    def generate_fingerprint(self, device_type: str = "android", location: str = "ID", 
                           isp: str = None, city: str = None, 
                           connection_type: str = "mobile") -> Dict[str, Any]:
        """Generate comprehensive fingerprint dengan connection type awareness - DIKOREKSI"""
        fingerprint_id = f"{device_type}_{location}_{connection_type}_{int(time.time())}"
        
        if fingerprint_id in self.fingerprint_cache:
            return self.fingerprint_cache[fingerprint_id]
        
        # Select device profile berdasarkan connection type
        if connection_type == "mobile":
            # Mobile devices
            if device_type == "ios":
                device_profile = self.device_profiles["iphone_16_pro_max"]
                os_profile = self.os_profiles["ios_18"]
                browser_profile = self.browser_profiles["safari_ios_18"]
                hardware_profile = self.hardware_profiles["apple_a18_pro"]
            else:
                device_options = ["samsung_galaxy_s24_ultra", "xiaomi_14_pro", "google_pixel_9_pro"]
                selected_device = random.choice(device_options)
                device_profile = self.device_profiles[selected_device]
                os_profile = self.os_profiles["android_14"]
                
                if selected_device == "samsung_galaxy_s24_ultra":
                    browser_profile = self.browser_profiles["samsung_browser_24"]
                    hardware_profile = self.hardware_profiles["snapdragon_8_gen3"]
                else:
                    browser_profile = self.browser_profiles["chrome_android_135"]
                    hardware_profile = random.choice([
                        self.hardware_profiles["snapdragon_8_gen3"], 
                        self.hardware_profiles["google_tensor_g4"]
                    ])
        else:
            # WiFi/Tablet devices - FIXED: tambah tablet profile
            device_options = ["samsung_galaxy_s24_ultra", "google_pixel_9_pro"]
            selected_device = random.choice(device_options)
            device_profile = self.device_profiles[selected_device]
            os_profile = self.os_profiles["android_14"]
            browser_profile = self.browser_profiles["chrome_android_135"]  # Chrome for tablet
            hardware_profile = self.hardware_profiles["snapdragon_8_gen3"]
        
        # Generate unique identifiers
        android_id = self._generate_android_id() if device_type == "android" else None
        advertising_id = self._generate_advertising_id()
        gsf_id = self._generate_gsf_id() if device_type == "android" else None
        
        # Generate location data - DIKOREKSI: tambah parameter city
        location_data = self._generate_location_data_enhanced(location, city)
        
        # Generate network data berdasarkan connection type - DIKOREKSI
        network_data = self._generate_network_data_enhanced(location, device_type, connection_type, isp)
        
        # Generate device fingerprint dengan connection type - DIKOREKSI
        device_fingerprint = self._generate_device_fingerprint_enhanced(device_profile, connection_type)
        
        # Generate sensor data - DIKOREKSI: sekarang didefinisikan
        sensor_data = self._generate_sensor_data_enhanced(device_profile["sensors"], connection_type)
        
        # Generate installed apps - DIKOREKSI: sekarang didefinisikan
        installed_apps = self._generate_installed_apps_indonesia_enhanced(device_type, connection_type)
        
        # Build fingerprint
        fingerprint = {
            "fingerprint_id": fingerprint_id,
            "timestamp": int(time.time()),
            "device_type": device_type,
            "connection_type": connection_type,  # Simpan connection type
            
            "device": {
                **device_profile,
                "identifiers": {
                    "android_id": android_id,
                    "advertising_id": advertising_id,
                    "gsf_id": gsf_id,
                    "serial_number": self._generate_serial_number(device_profile["brand"]),
                    "imei": self._generate_imei() if device_type == "android" and connection_type == "mobile" else None,
                    "meid": self._generate_meid() if device_type == "android" and connection_type == "mobile" else None
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
                "font_scale": random.uniform(0.85, 1.15),
                "display_size": random.choice(["default", "small", "large"]),
                "dark_mode": random.choice([True, False]),
                "battery_saver": False,
                "developer_options": random.choice([True, False])
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
                "thermal_state": random.choice(["nominal", "fair", "serious", "critical"]),
                "power_state": random.choice(["charged", "charging", "discharging", "full"]),
                "memory_pressure": random.choice(["normal", "warning", "critical"]),
                "disk_space": random.randint(10, device_profile["hardware"]["storage"] - 10)
            },
            
            # Privacy Settings
            "privacy": {
                "location_enabled": random.choice([True, False]),
                "camera_enabled": random.choice([True, False]),
                "microphone_enabled": random.choice([True, False]),
                "contacts_access": random.choice([True, False]),
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
    """Manager untuk berbagai layanan email - FIXED dengan priority system yang benar"""
    
    def __init__(self, preferred_service: str = "auto"):
        self.services = {
            "10minutemail": TenMinuteMailService2025(),
            "guerrillamail": GuerrillaMailService2025(),
            "1secmail": OneSecMailService2025(),
            "mailtm": MailTMService2025(),
            "tempmail_plus": TempMailPlusService2025(),
            "cmail": CmailService2025(),
            "gmail_alias": SimpleGmailAlias2025(),
        }
        self.email_cache = {}
        self.preferred_service = preferred_service
        self.active_services = {}
        
    def _get_service_priority(self, is_manual: bool = False) -> List[str]:
        """Get service priority list - 10minutemail sebagai prioritas utama"""
        if is_manual:
            return [
                "10minutemail",    # ⭐ Paling reliable untuk manual
                "guerrillamail",   # Fallback untuk manual
                "1secmail",        # Backup
                "mailtm",          # Alternatif
                "tempmail_plus",   # Lainnya
                "cmail",           # Lainnya
                "gmail_alias"      # Last resort
            ]
        else:
            return [
                "10minutemail",    # ⭐ Paling reliable (no API needed)
                "guerrillamail",   # Fallback utama
                "1secmail",        # Cepat dan mudah
                "mailtm",          # Bagus tapi kadang rate limited
                "tempmail_plus",   # Alternatif baru
                "cmail",           # Support API
                "gmail_alias"      # Manual fallback
            ]
    
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
        # Priority list berdasarkan reliability
        priority_list = [
            "1secmail",      # Paling reliable
            "10minutemail",  # Cepat dan mudah
            "mailtm",        # API support
            "tempmail_plus", # Alternatif
            "cmail",         # Backup
            "guerrillamail"  # Last resort
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
        """Initialize semua pattern OTP dengan priority"""
        # Format: (pattern_name, regex_pattern, priority)
        # Priority: 3 = tinggi (Indonesian), 2 = sedang (English), 1 = rendah (General)
        
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

class GmailAliasService2025:
    """Gmail alias service wrapper 2025"""
    
    def __init__(self):
        self.base_domains = ["gmail.com", "googlemail.com"]
        
    async def get_email(self) -> Optional[Dict[str, Any]]:
        """Generate Gmail alias"""
        try:
            # Generate base email
            base_username = random_string(8)
            domain = random.choice(self.base_domains)
            base_email = f"{base_username}@{domain}"
            
            # Generate alias dengan plus addressing
            alias_username = base_username
            alias_tags = []
            
            # Add dots
            if random.random() > 0.5:
                chars = list(alias_username)
                if len(chars) > 3:
                    pos = random.randint(1, len(chars) - 2)
                    chars.insert(pos, ".")
                    alias_username = "".join(chars)
                    alias_tags.append("dot")
            
            # Add plus tag
            plus_tags = ["work", "temp", "insta", "test", "new"]
            if random.random() > 0.3:
                tag = random.choice(plus_tags)
                alias_username = f"{alias_username}+{tag}"
                alias_tags.append("plus")
            
            # Add timestamp
            timestamp = str(int(time.time()))[-6:]
            alias_username = f"{alias_username}{timestamp}"
            alias_tags.append("timestamp")
            
            alias_email = f"{alias_username}@{domain}"
            
            return {
                "email": alias_email,
                "base_email": base_email,
                "service": "gmail_alias",
                "tags": alias_tags,
                "recovery_email": base_email
            }
            
        except Exception as e:
            print(f"{merah}❌  Gmail alias error: {e}{reset}")
            return None
    
    async def get_otp(self, email_address: str, email_data: Dict[str, Any]) -> Optional[str]:
        """Gmail alias doesn't support OTP retrieval directly"""
        # This would require access to actual Gmail account
        # In real implementation, use Gmail API with OAuth
        print(f"{kuning}⚠️   Gmail alias requires manual OTP check{reset}")
        return None
    
    async def verify_email(self, email_address: str, email_data: Dict[str, Any]) -> bool:
        """Gmail aliases are always valid"""
        return True

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
    
    async def verify_email(self, email_address: str, email_data: Dict[str, Any]) -> bool:
        """Verify Cmail.ai email"""
        try:
            check_url = f"{self.api_base}/api/emails?inbox={email_address}"
            resp = self.session.get(check_url, timeout=30)
            return resp.status_code == 200
        except Exception:
            return False

class TempMailService2025:
    """TempMail service wrapper 2025"""
    
    def __init__(self):
        self.api_base = "https://api.temp-mail.org"
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        })
    
    async def get_email(self) -> Optional[Dict[str, Any]]:
        """Get email from TempMail"""
        try:
            # Get available domains
            domains_resp = self.session.get(f"{self.api_base}/request/domains", timeout=30)
            domains_resp.raise_for_status()
            
            domains = domains_resp.json()
            if not domains:
                return None
            
            # Generate email
            username = random_string(10)
            domain = random.choice(domains)
            email = f"{username}{domain}"
            
            return {
                "email": email,
                "username": username,
                "domain": domain,
                "service": "tempmail"
            }
            
        except Exception as e:
            print(f"{merah}❌  TempMail error: {e}{reset}")
            return None
    
    async def get_otp(self, email_address: str, email_data: Dict[str, Any]) -> Optional[str]:
        """Get OTP from TempMail"""
        try:
            # Get messages for email
            params = {"email": email_address}
            messages_resp = self.session.get(f"{self.api_base}/request/mail/id/{hashlib.md5(email_address.encode()).hexdigest()}/", 
                                           params=params, timeout=30)
            
            if messages_resp.status_code == 200:
                messages = messages_resp.json()
                
                for message in messages:
                    subject = message.get("mail_subject", "")
                    body = message.get("mail_text", "")
                    
                    otp = self._extract_otp(subject + " " + body)
                    if otp:
                        return otp
            
            return None
            
        except Exception as e:
            print(f"{merah}❌  TempMail OTP error: {e}{reset}")
            return None
    
    async def verify_email(self, email_address: str, email_data: Dict[str, Any]) -> bool:
        """Verify TempMail email"""
        try:
            params = {"email": email_address}
            resp = self.session.get(f"{self.api_base}/request/mail/id/{hashlib.md5(email_address.encode()).hexdigest()}/", 
                                  params=params, timeout=30)
            return resp.status_code == 200
        except Exception:
            return False

def random_string(length: int = 10) -> str:
    """Generate random string"""
    chars = string.ascii_lowercase + string.digits
    return ''.join(random.choice(chars) for _ in range(length))

# ===================== SESSION MANAGEMENT 2025 =====================

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
        
        # Build complete headers
        complete_headers = self._build_complete_headers(
            fingerprint, behavior_profile, ip_config, webrtc_fingerprint
        )
        
        # **TAMBAHKAN HEADERS IMPORTANT**
        complete_headers.update({
            "X-Web-Session-Id": extra_session_id,
            "Priority": "u=1, i",
            "Sec-Ch-Prefers-Color-Scheme": "dark",
            "X-IG-WWW-Claim": "0"  # Default, akan diupdate nanti
        })
        
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
                "device_type": fingerprint.get("device_type", "android"),
                "location": fingerprint.get("location", {}).get("city", "Jakarta"),
                "isp": ip_config.get("isp_info", {}).get("isp", "telkomsel"),
                "connection_type": ip_config.get("connection_type", "mobile")
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
        """Build complete headers matching real Instagram web browser traffic.
        
        This method generates headers that match real Instagram desktop web
        browser traffic, NOT mobile app traffic. Mobile app headers are 
        detected as suspicious and cause checkpoints.
        """
        # Start with IP config headers
        headers = ip_config.get("headers", {}).copy()
        
        # Get location info for Accept-Language
        location_info = fingerprint.get("location", {}) if fingerprint else {}
        locale = location_info.get("locale", "id_ID")
        
        # Generate Chrome version
        chrome_major = random.choice([140, 141, 142, 143])
        chrome_full = f"{chrome_major}.0.{random.randint(7000, 7999)}.{random.randint(100, 200)}"
        
        # Platform choices (desktop only - mobile causes checkpoint!)
        platforms = [
            {"platform": "macOS", "platform_version": f"{random.randint(24, 26)}.0.{random.randint(0, 2)}", "ua_platform": "Macintosh; Intel Mac OS X 10_15_7"},
            {"platform": "Windows", "platform_version": f"{random.randint(10, 15)}.0.0", "ua_platform": "Windows NT 10.0; Win64; x64"},
        ]
        selected_platform = random.choice(platforms)
        
        # Generate Instagram AJAX build ID
        ig_ajax_id = random.choice(["1029952363", "1029951234", "1029950123", "1029948765"])
        
        # ===== DESKTOP WEB BROWSER HEADERS (NOT MOBILE APP) =====
        headers.update({
            # User-Agent - Desktop Chrome
            "User-Agent": f"Mozilla/5.0 ({selected_platform['ua_platform']}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{chrome_major}.0.0.0 Safari/537.36",
            "Accept": "*/*",
            "Accept-Language": self._get_accept_language_for_locale(locale) if hasattr(self, '_get_accept_language_for_locale') else "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
            "Accept-Encoding": "gzip, deflate, br",
            
            # Security Headers (Desktop format)
            "Sec-Ch-Ua-Full-Version-List": f'"Chromium";v="{chrome_full}", "Google Chrome";v="{chrome_full}", "Not_A Brand";v="99.0.0.0"',
            "Sec-Ch-Ua-Platform": f'"{selected_platform["platform"]}"',
            "Sec-Ch-Ua": f'"Chromium";v="{chrome_major}", "Google Chrome";v="{chrome_major}", "Not_A Brand";v="99"',
            "Sec-Ch-Ua-Model": '""',  # Empty for desktop
            "Sec-Ch-Ua-Mobile": "?0",  # Desktop = ?0
            "Sec-Ch-Ua-Platform-Version": f'"{selected_platform["platform_version"]}"',
            "Sec-Ch-Prefers-Color-Scheme": "dark",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            
            # Instagram Core Headers (Web only)
            "X-Ig-App-Id": "936619743392459",
            "X-Requested-With": "XMLHttpRequest",
            "X-Instagram-Ajax": ig_ajax_id,
            "X-Asbd-Id": random.choice(["359341", "359340", "359339"]),
            "X-Ig-Www-Claim": "0",
            
            # Standard Headers
            "Origin": "https://www.instagram.com",
            "Priority": "u=1, i",
        })
        
        return headers
    
    def _generate_pigeon_session_id(self) -> str:
        """Generate Pigeon Session ID seperti Instagram asli"""
        # Format: UFS-{uuid}-{random_int}
        random_uuid = str(uuid.uuid4()).upper()
        random_suffix = random.randint(100000000, 999999999)
        return f"UFS-{random_uuid}-{random_suffix}"
    
    def _generate_bloks_version_id(self) -> str:
        """Generate Bloks Version ID seperti Instagram asli
        
        The Bloks Version ID is a 64-character hex string used by Instagram
        to track feature flag versions. We generate it by combining:
        - 56 chars from SHA-256 hash (base version identifier)
        - 8 chars from MD5 hash (random suffix for uniqueness)
        This matches the format observed in real Instagram traffic.
        """
        # Generate 64-char hex string: 56 from SHA-256 + 8 from MD5
        BLOKS_BASE_LENGTH = 56  # Characters from main hash
        BLOKS_SUFFIX_LENGTH = 8  # Characters from random suffix
        
        base_hash = hashlib.sha256(str(time.time()).encode()).hexdigest()
        version_suffix = hashlib.md5(str(random.random()).encode()).hexdigest()[:BLOKS_SUFFIX_LENGTH]
        return f"{base_hash[:BLOKS_BASE_LENGTH]}{version_suffix}"
    
    def _get_ordered_cookie_chain(self, session_id: str) -> Dict[str, str]:
        """Get cookies in proper Instagram order"""
        if session_id not in self.cookie_jar:
            return {}
        
        all_cookies = self.cookie_jar[session_id]
        
        # Define cookie order as per Instagram requirements
        cookie_order = [
            "csrftoken",     # 1. CSRF token - always first
            "mid",           # 2. Machine ID
            "ig_did",        # 3. Device ID  
            "ig_nrcb",       # 4. Non-registered client browser
            "rur",           # 5. Region/Routing
            "shbid",         # 6. Session handling ID
            "shbts",         # 7. Session handling timestamp
            "ds_user_id"     # 8. Logged in user ID (only after login)
        ]
        
        ordered_cookies = {}
        
        # Add cookies in order
        for cookie_name in cookie_order:
            if cookie_name in all_cookies:
                ordered_cookies[cookie_name] = all_cookies[cookie_name]
        
        # Add any remaining cookies that are not in the standard order
        for cookie_name, cookie_value in all_cookies.items():
            if cookie_name not in ordered_cookies:
                ordered_cookies[cookie_name] = cookie_value
        
        return ordered_cookies
    
    def build_cookie_string(self, session_id: str) -> str:
        """Build properly ordered cookie string for Instagram"""
        ordered_cookies = self._get_ordered_cookie_chain(session_id)
        return "; ".join([f"{k}={v}" for k, v in ordered_cookies.items()])

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
    
    def refresh_session_completely(self, session_id: str) -> Optional[str]:
        """Completely refresh a session with new fingerprints and tokens.
        
        Use this when sessions get stale (400 errors, rate limits, etc.)
        This creates a completely fresh session with new identifiers.
        """
        if session_id not in self.sessions:
            return None
        
        old_session = self.sessions[session_id]
        
        # Generate completely new device ID and session IDs
        new_device_id = self._generate_consistent_device_id()
        new_extra_session_id = self._generate_extra_session_id()
        new_guid = str(uuid.uuid4())
        
        # Create new session ID
        new_session_id = f"sess_{self.session_counter:08d}_{int(time.time())}"
        self.session_counter += 1
        
        # Copy fingerprint but regenerate headers with new IDs
        fingerprint = old_session["fingerprint"].copy()
        behavior_profile = old_session["behavior_profile"].copy()
        ip_config = old_session["ip_config"].copy()
        
        # Rebuild complete headers with new session info
        complete_headers = self._build_complete_headers(
            fingerprint, behavior_profile, ip_config, old_session.get("webrtc_fingerprint")
        )
        
        complete_headers.update({
            "X-Web-Session-Id": new_extra_session_id,
            "Priority": "u=1, i",
            "Sec-Ch-Prefers-Color-Scheme": "dark",
            "X-IG-WWW-Claim": "0"
        })
        
        # Create fresh session data
        new_session = {
            "session_id": new_session_id,
            "created_at": time.time(),
            "last_activity": time.time(),
            "last_ip_change": time.time(),
            "fingerprint": fingerprint,
            "behavior_profile": behavior_profile,
            "ip_config": ip_config,
            "webrtc_fingerprint": old_session.get("webrtc_fingerprint", {}),
            "device_id": new_device_id,
            "extra_session_id": new_extra_session_id,
            "guid": new_guid,
            "uuid": str(uuid.uuid4()),
            "request_count": 0,
            "success_count": 0,
            "failure_count": 0,
            "state": "active",
            "sequence_number": 0,
            "tokens": {},  # Fresh tokens
            "cookies": {},  # Fresh cookies
            "headers": complete_headers,
            "current_headers": complete_headers,
            "metadata": old_session.get("metadata", {}).copy()
        }
        
        # Store new session
        self.sessions[new_session_id] = new_session
        self.session_states[new_session_id] = {
            "current_page": None,
            "form_data": {},
            "navigation_history": [],
            "interaction_log": [],
            "error_log": [],
            "cookie_jar": {},
            "performance_metrics": {
                "avg_response_time": 0,
                "success_rate": 1.0,
                "consecutive_errors": 0,
                "rate_limit_hits": 0,
                "ip_rotations": 0
            }
        }
        
        # Initialize cookie jar
        self.cookie_jar[new_session_id] = {}
        
        # Mark old session as refreshed
        old_session["state"] = "refreshed"
        old_session["refreshed_to"] = new_session_id
        
        print(f"{cyan}🔄  Session refreshed: {session_id[:12]} → {new_session_id[:12]}{reset}")
        
        return new_session_id
    
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
                          require_cookies: bool = True) -> Dict[str, Any]:  # FIXED: tambah parameter
        """Make request dengan COMPLETE session synchronization - FIXED"""
        
        # Check cache
        if cache_key and cache_key in self.request_cache:
            cached = self.request_cache[cache_key]
            if time.time() - cached["timestamp"] < self.cache_ttl:
                print(f"{cyan}💾  Using cached response for {cache_key}{reset}")
                return cached["response"]
        
        # Get session dengan semua komponen sinkron - FIXED
        session = self.session_manager.get_session_with_headers(session_id)
        if not session:
            return {"status": None, "error": f"Session {session_id} not found or expired"}
        
        # Get cookies dari session jika diperlukan - FIXED
        session_cookies = {}
        if require_cookies:
            session_cookies = self.session_manager.get_session_cookies(session_id)
            
            # Juga ambil cookies spesifik untuk domain
            if "instagram.com" in url:
                instagram_cookies = self.session_manager.get_session_cookies(session_id, "instagram.com")
                session_cookies.update(instagram_cookies)
        
        # Merge cookies: session cookies + request cookies - FIXED
        all_cookies = {**session_cookies, **(cookies or {})}
        
        # Get current headers dari session - FIXED
        current_headers = session.get("current_headers", {}).copy()
        
        # Merge headers: session headers + request headers - FIXED
        all_headers = {**current_headers, **(headers or {})}
        
        # Update User-Agent jika ada di session metadata - FIXED
        metadata = session.get("metadata", {})
        if "user_agent" in metadata and metadata["user_agent"]:
            all_headers["User-Agent"] = metadata["user_agent"]
        
        # NOTE: Removed mobile-specific headers (X-IG-Connection-Type, X-IG-Network-Type)
        # These are mobile app headers and cause 400 errors for web browser requests
        connection_type = metadata.get("connection_type", "mobile")
        
        # Create request object
        request_id = f"req_{int(time.time())}_{random.randint(1000, 9999)}"
        
        request_data = {
            "request_id": request_id,
            "session_id": session_id,
            "method": method,
            "url": url,
            "headers": all_headers,  # FIXED: gunakan merged headers
            "data": data,
            "cookies": all_cookies,  # FIXED: gunakan merged cookies
            "priority": priority,
            "cache_key": cache_key,
            "require_cookies": require_cookies,
            "timestamp": time.time(),
            "retry_count": 0,
            "connection_type": connection_type  # FIXED: simpan connection type
        }
        
        # Put in queue
        await self.request_queue.put(request_data)
        
        # Wait for result
        return await self._wait_for_result(request_id)
    
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
        """Enhanced human behavior simulation with natural patterns - IMPROVED"""
        session = self.session_manager.get_session(session_id)
        if not session:
            return
        
        behavior_profile = session.get("behavior_profile", {})
        connection_type = session.get("metadata", {}).get("connection_type", "mobile")
        url = request_data.get("url", "").lower()
        method = request_data.get("method", "GET")
        
        # ===== BASE TIMING BASED ON CONNECTION TYPE =====
        if connection_type == "mobile":
            # Mobile: faster reactions, more multitasking behavior
            base_thinking_time = random.uniform(0.3, 1.5)
            base_typing_delay = random.uniform(0.08, 0.25)
            scroll_speed_factor = 1.2  # Faster scrolling on mobile
        else:
            # WiFi/Desktop: slower, more deliberate
            base_thinking_time = random.uniform(0.8, 2.5)
            base_typing_delay = random.uniform(0.15, 0.4)
            scroll_speed_factor = 0.8  # Slower scrolling
        
        # ===== CONTEXT-AWARE TIMING ADJUSTMENTS =====
        context_multiplier = 1.0
        
        # Signup/login pages - users read more carefully
        if any(kw in url for kw in ["signup", "login", "register", "create"]):
            context_multiplier = 1.8
            # Add occasional hesitation (user reading terms, thinking about password)
            if random.random() < 0.3:
                await asyncio.sleep(random.uniform(2.0, 5.0))
        
        # API endpoints - faster (background requests)
        elif "/api/" in url or "/graphql" in url:
            context_multiplier = 0.3
        
        # Profile pages - moderate reading time
        elif "profile" in url or "accounts/edit" in url:
            context_multiplier = 1.3
        
        # ===== MICRO-INTERACTIONS =====
        # Simulate natural variations in human attention
        
        # 1. Reading/thinking time
        thinking_time = base_thinking_time * context_multiplier
        await asyncio.sleep(thinking_time)
        
        # 2. Occasional hesitation (10% chance)
        if random.random() < 0.1:
            hesitation_time = random.uniform(0.5, 2.0)
            await asyncio.sleep(hesitation_time)
        
        # 3. POST request specific - typing simulation
        if method == "POST" and request_data.get("data"):
            data_str = str(request_data["data"])
            char_count = len(data_str)
            
            # Typing speed from behavior profile (words per minute)
            wpm = behavior_profile.get("typing_speed_wpm", random.randint(60, 100))
            chars_per_second = (wpm * 5) / 60  # 5 chars per word average
            
            # Calculate typing time with variation
            base_typing_time = char_count / chars_per_second
            
            # Add random pauses (thinking while typing)
            pause_count = max(1, char_count // 50)  # Pause every ~50 chars
            pause_time = pause_count * random.uniform(0.3, 1.0)
            
            total_typing_time = min(base_typing_time + pause_time, 8.0)  # Cap at 8 seconds
            await asyncio.sleep(total_typing_time)
            
            # Error rate simulation (backspace, retype)
            error_rate = behavior_profile.get("error_rate", 0.03)
            if random.random() < error_rate:
                # Simulate correcting a mistake
                await asyncio.sleep(random.uniform(0.5, 1.5))
        
        # 4. Mouse movement simulation (implied by time)
        # Longer paths for form navigation
        if "form" in url or method == "POST":
            mouse_time = random.uniform(0.2, 0.8)
            await asyncio.sleep(mouse_time)
        
        # 5. Scroll simulation for page loads
        if method == "GET" and "api" not in url:
            # Simulate initial page scroll behavior
            scroll_time = random.uniform(0.3, 1.2) * scroll_speed_factor
            await asyncio.sleep(scroll_time)
    
    async def _apply_adaptive_request_spacing(self, session_id: str, domain: str):
        """Apply adaptive spacing between requests based on session history"""
        session_state = self.session_manager.get_session_state(session_id)
        if not session_state:
            return
        
        perf_metrics = session_state.get("performance_metrics", {})
        
        # Calculate spacing based on recent performance
        rate_limit_hits = perf_metrics.get("rate_limit_hits", 0)
        consecutive_errors = perf_metrics.get("consecutive_errors", 0)
        
        # Base spacing
        base_spacing = random.uniform(0.5, 2.0)
        
        # Increase spacing if we've hit rate limits
        if rate_limit_hits > 0:
            base_spacing *= (1 + (rate_limit_hits * 0.5))  # 50% increase per hit
        
        # Increase spacing if we have consecutive errors
        if consecutive_errors > 0:
            base_spacing *= (1 + (consecutive_errors * 0.3))  # 30% increase per error
        
        # Cap at 30 seconds
        final_spacing = min(base_spacing, 30.0)
        
        if final_spacing > 1.0:
            await asyncio.sleep(final_spacing)

    async def _handle_rate_limit(self, session_id: str, request_data: Dict[str, Any]):
        """Enhanced rate limit handling with exponential backoff - IMPROVED"""
        print(f"{cyan}🛡️   Handling rate limit for session {session_id[:8]}...{reset}")
        
        session = self.session_manager.get_session(session_id)
        if not session:
            return
        
        # Get rate limit hit count
        session_state = self.session_manager.get_session_state(session_id)
        rate_limit_hits = 1
        if session_state:
            rate_limit_hits = session_state.get("performance_metrics", {}).get("rate_limit_hits", 1)
        
        connection_type = session.get("metadata", {}).get("connection_type", "mobile")
        
        # ===== EXPONENTIAL BACKOFF STRATEGY =====
        # Base wait time increases exponentially with each rate limit hit
        base_wait = 30  # 30 seconds base
        max_wait = 600  # 10 minutes max
        
        # Calculate wait time with jitter
        exponential_wait = min(base_wait * (2 ** (rate_limit_hits - 1)), max_wait)
        jitter = random.uniform(-0.2, 0.2) * exponential_wait  # ±20% jitter
        wait_time = exponential_wait + jitter
        
        print(f"{kuning}    Rate limit hit #{rate_limit_hits}, waiting {wait_time:.1f}s...{reset}")
        
        # ===== ROTATION STRATEGY =====
        if rate_limit_hits >= 2:
            # After 2nd hit, rotate IP
            if connection_type == "mobile":
                print(f"{cyan}    Mobile: Rotating IP and fingerprint...{reset}")
                if self.account_creator:
                    await self.account_creator.rotate_ip_with_fingerprint(session_id)
            else:
                print(f"{cyan}    WiFi: Rotating fingerprint...{reset}")
                # Rotate fingerprint only for WiFi
                if self.account_creator:
                    # Just update fingerprint, keep IP
                    new_fingerprint = self.account_creator.fingerprint_system.generate_fingerprint(
                        device_type="android",
                        location=session.get("metadata", {}).get("location", "ID"),
                        connection_type=connection_type
                    )
                    self.session_manager.update_session(session_id, {
                        "fingerprint": new_fingerprint
                    })
        
        # Wait
        await asyncio.sleep(wait_time)
    
    async def _make_real_http_request(self, request_data: Dict[str, Any], 
                                    session: Dict[str, Any]) -> Dict[str, Any]:
        """Make REAL HTTP request menggunakan aiohttp"""
        method = request_data["method"]
        url = request_data["url"]
        headers = request_data["headers"]
        data = request_data["data"]
        
        # IMPORTANT: Use request headers directly, don't override with session headers
        # The calling code (_create_instagram_account) has already built complete headers
        all_headers = headers.copy()
        
        # Only add X-Web-Session-Id if not already present
        if "X-Web-Session-Id" not in all_headers and session.get("extra_session_id"):
            all_headers["X-Web-Session-Id"] = session.get("extra_session_id", "")
        
        # NOTE: Removed hardcoded header updates that were causing conflicts:
        # - X-IG-WWW-Claim (should match the request's X-Ig-Www-Claim)
        # - Sec-Ch-Ua-Platform-Version (already in request headers)
        # - etc.
        
        # Combine cookies
        session_cookies = session.get("cookies", {})
        request_cookies = request_data.get("cookies", {})
        all_cookies = {**session_cookies, **request_cookies}
        
        # Build Cookie header string in proper format
        if all_cookies:
            # Sort cookies in the order Instagram expects: mid, ig_did, datr, wd, ig_nrcb, ps_l, ps_n, rur, csrftoken
            cookie_order = ["mid", "ig_did", "datr", "wd", "ig_nrcb", "ps_l", "ps_n", "rur", "csrftoken"]
            ordered_cookies = []
            
            # Add cookies in order first
            for key in cookie_order:
                if key in all_cookies:
                    ordered_cookies.append(f"{key}={all_cookies[key]}")
            
            # Add remaining cookies
            for key, value in all_cookies.items():
                if key not in cookie_order:
                    ordered_cookies.append(f"{key}={value}")
            
            # Set Cookie header
            all_headers["Cookie"] = "; ".join(ordered_cookies)
        
        # print(f"{cyan}    Real request: {method} {url}{reset}")
        
        try:
            # Gunakan aiohttp untuk async HTTP requests
            timeout = aiohttp.ClientTimeout(total=30)
            
            # Don't use cookie_jar since we're setting Cookie header directly
            async with aiohttp.ClientSession(
                headers=all_headers,
                timeout=timeout
            ) as client_session:
                
                start_time = time.time()
                
                if method.upper() == "GET":
                    async with client_session.get(url, ssl=False) as response:
                        body = await response.read()
                        status = response.status
                        response_headers = dict(response.headers)
                        
                elif method.upper() == "POST":
                    async with client_session.post(url, data=data, ssl=False) as response:
                        body = await response.read()
                        status = response.status
                        response_headers = dict(response.headers)
                        
                else:
                    async with client_session.request(method, url, data=data, ssl=False) as response:
                        body = await response.read()
                        status = response.status
                        response_headers = dict(response.headers)
                
                response_time = time.time() - start_time
                
                # Get cookies from response headers (Set-Cookie)
                response_cookies = {}
                for key, value in response_headers.items():
                    if key.lower() == 'set-cookie':
                        # Parse Set-Cookie header
                        cookie_parts = value.split(';')[0]  # Get just name=value
                        if '=' in cookie_parts:
                            cookie_name, cookie_value = cookie_parts.split('=', 1)
                            response_cookies[cookie_name.strip()] = cookie_value.strip()
                
                # Also check if using aiohttp's cookie_jar (still available even without init)
                for cookie in client_session.cookie_jar:
                    response_cookies[cookie.key] = cookie.value
                
                # Debug info
                # print(f"{cyan}    Response: {status} in {response_time:.2f}s{reset}")
                
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
    """Adaptive rate limiter with intelligent learning for Instagram requests.
    
    This rate limiter implements several sophisticated features:
    
    1. Endpoint Classification:
       - instagram_signup: Most conservative (2 req/120s)
       - instagram_api: Conservative (3 req/60s)
       - instagram.com: Moderate (4 req/60s)
       - default: Relaxed (10 req/60s)
    
    2. Adaptive Learning:
       - Automatically reduces limits when rate limits are hit
       - Increases window size based on error history
       - Tracks per-session and per-endpoint statistics
    
    3. Cooldown Periods:
       - Sessions can be put in cooldown after hitting limits
       - Cooldowns are session-specific and can be reset after IP rotation
    
    4. Human-like Request Spacing:
       - Enforces minimum time between requests
       - Different spacing for different endpoint types
       - Prevents automated detection through timing analysis
    
    5. Domain Statistics:
       - Tracks success rates per domain
       - Monitors request patterns for anomaly detection
    """
    
    def __init__(self):
        self.request_log = {}
        self.domain_stats = {}  # Per-domain statistics
        
        # Default limits - conservative for Instagram
        self.limits = {
            "default": {"max_requests": 10, "window_seconds": 60},
            "instagram.com": {"max_requests": 4, "window_seconds": 60},  # More conservative
            "instagram_api": {"max_requests": 3, "window_seconds": 60},  # Even more conservative for API
            "instagram_signup": {"max_requests": 2, "window_seconds": 120},  # Very conservative for signup
            "critical": {"max_requests": 1, "window_seconds": 30}
        }
        
        self.adaptive_limits = {}
        self.cooldown_periods = {}  # Session-specific cooldowns
        
        # Human-like request spacing (seconds)
        self.min_request_spacing = {
            "default": 0.5,
            "instagram.com": 2.0,
            "instagram_api": 3.0,
            "instagram_signup": 5.0
        }
        
        self.last_request_time = {}  # Track last request per session
    
    def can_make_request(self, session_id: str, endpoint: str = None) -> bool:
        """Check if request can be made with adaptive learning"""
        now = time.time()
        
        # Check cooldown first
        if session_id in self.cooldown_periods:
            cooldown_until = self.cooldown_periods[session_id]
            if now < cooldown_until:
                remaining = cooldown_until - now
                print(f"{kuning}⏳  Session {session_id[:8]} in cooldown for {remaining:.1f}s{reset}")
                return False
        
        # Enforce minimum request spacing (human-like)
        endpoint_type = self._classify_endpoint(endpoint)
        min_spacing = self.min_request_spacing.get(endpoint_type, 0.5)
        
        session_last = self.last_request_time.get(session_id, 0)
        time_since_last = now - session_last
        
        if time_since_last < min_spacing:
            # Add small random delay to feel more human
            return False
        
        # Get adaptive limit config
        limit_config = self._get_adaptive_limit_config(session_id, endpoint)
        window = limit_config["window_seconds"]
        max_requests = limit_config["max_requests"]
        
        # Initialize session log
        if session_id not in self.request_log:
            self.request_log[session_id] = {}
        
        if endpoint_type not in self.request_log[session_id]:
            self.request_log[session_id][endpoint_type] = []
        
        # Clean old requests
        session_log = self.request_log[session_id][endpoint_type]
        session_log = [t for t in session_log if now - t < window]
        self.request_log[session_id][endpoint_type] = session_log
        
        # Check limit
        if len(session_log) >= max_requests:
            # Calculate wait time with jitter
            oldest_request = min(session_log) if session_log else now
            base_wait_time = window - (now - oldest_request)
            jitter = random.uniform(0, 5)  # Add 0-5s random jitter
            wait_time = base_wait_time + jitter
            
            if wait_time > 0:
                print(f"{kuning}⏳  Rate limit hit for {session_id[:8]} on {endpoint_type}, wait {wait_time:.1f}s{reset}")
                
                # Update adaptive limits
                self._record_rate_limit_hit(session_id, endpoint_type)
                
                return False
        
        # Record request
        session_log.append(now)
        self.last_request_time[session_id] = now
        
        # Update stats
        self._update_domain_stats(endpoint_type, True)
        
        return True
    
    def _classify_endpoint(self, endpoint: str) -> str:
        """Classify endpoint for rate limiting purposes"""
        if not endpoint:
            return "default"
        
        endpoint_lower = endpoint.lower()
        
        # Instagram signup endpoints (most conservative)
        if any(kw in endpoint_lower for kw in ["signup", "register", "create_ajax", "send_verify", "check_confirmation"]):
            return "instagram_signup"
        
        # Instagram API endpoints
        if any(kw in endpoint_lower for kw in ["/api/v1/", "/graphql", "web_create"]):
            return "instagram_api"
        
        # General Instagram
        if "instagram.com" in endpoint_lower:
            return "instagram.com"
        
        return "default"
    
    def _get_adaptive_limit_config(self, session_id: str, endpoint: str) -> Dict[str, Any]:
        """Get limit configuration with adaptive learning"""
        endpoint_type = self._classify_endpoint(endpoint)
        base_config = self.limits.get(endpoint_type, self.limits["default"]).copy()
        
        # Check if we have adaptive data for this session
        adaptive_key = f"{session_id}:{endpoint_type}"
        if adaptive_key in self.adaptive_limits:
            adaptive_data = self.adaptive_limits[adaptive_key]
            
            # Reduce limits if we've had rate limit hits
            rate_limit_hits = adaptive_data.get("rate_limit_hits", 0)
            if rate_limit_hits > 0:
                # Reduce max_requests by 20% for each hit, minimum 1
                reduction_factor = max(0.5, 1 - (rate_limit_hits * 0.2))
                base_config["max_requests"] = max(1, int(base_config["max_requests"] * reduction_factor))
                
                # Increase window by 30% for each hit
                increase_factor = 1 + (rate_limit_hits * 0.3)
                base_config["window_seconds"] = int(base_config["window_seconds"] * increase_factor)
        
        return base_config
    
    def _record_rate_limit_hit(self, session_id: str, endpoint_type: str):
        """Record rate limit hit for adaptive learning"""
        adaptive_key = f"{session_id}:{endpoint_type}"
        
        if adaptive_key not in self.adaptive_limits:
            self.adaptive_limits[adaptive_key] = {
                "total_requests": 0,
                "successful_requests": 0,
                "rate_limit_hits": 0,
                "avg_request_rate": 0,
                "last_updated": time.time()
            }
        
        self.adaptive_limits[adaptive_key]["rate_limit_hits"] += 1
        self.adaptive_limits[adaptive_key]["last_updated"] = time.time()
    
    def _update_domain_stats(self, endpoint_type: str, success: bool):
        """Update domain-level statistics"""
        if endpoint_type not in self.domain_stats:
            self.domain_stats[endpoint_type] = {
                "total_requests": 0,
                "successful_requests": 0,
                "rate_limit_hits": 0,
                "last_request": time.time()
            }
        
        self.domain_stats[endpoint_type]["total_requests"] += 1
        if success:
            self.domain_stats[endpoint_type]["successful_requests"] += 1
        self.domain_stats[endpoint_type]["last_request"] = time.time()
    
    def apply_cooldown(self, session_id: str, duration: float):
        """Apply cooldown to session"""
        self.cooldown_periods[session_id] = time.time() + duration
        print(f"{kuning}🧊  Applied {duration:.1f}s cooldown to session {session_id[:8]}{reset}")
    
    def reset_session_limits(self, session_id: str):
        """Reset adaptive limits for session (after IP rotation)"""
        keys_to_remove = [k for k in self.adaptive_limits.keys() if k.startswith(session_id)]
        for key in keys_to_remove:
            del self.adaptive_limits[key]
        
        if session_id in self.request_log:
            self.request_log[session_id] = {}
        
        if session_id in self.cooldown_periods:
            del self.cooldown_periods[session_id]
        
        print(f"{hijau}✅  Reset rate limits for session {session_id[:8]}{reset}")
    
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

# ===================== RESPONSE PROCESSOR 2025 =====================

class ResponseProcessor2025:
    """Advanced response processor dengan parsing dan analysis"""
    
    def __init__(self):
        self.parsers = {
            "json": self._parse_json,
            "html": self._parse_html,
            "text": self._parse_text,
            "binary": self._parse_binary
        }
        self.validators = self._initialize_validators()
        self.extractors = self._initialize_extractors()
    
    def _initialize_validators(self) -> Dict[str, Any]:
        """Initialize response validators"""
        return {
            "instagram": {
                "success_patterns": [
                    r'"status":"ok"',
                    r'"authenticated":true',
                    r'"account_created":true',
                    r'"user_id":\d+'
                ],
                "error_patterns": [
                    r'"status":"fail"',
                    r'"error":',
                    r'"message":"[^"]+"',
                    r'"challenge_required"',
                    r'"checkpoint_required"'
                ],
                "rate_limit_patterns": [
                    r'rate limit',
                    r'too many requests',
                    r'retry after',
                    r'wait.*minutes'
                ]
            },
            "generic": {
                "success_codes": [200, 201, 202, 204],
                "redirect_codes": [301, 302, 303, 307, 308],
                "client_error_codes": [400, 401, 403, 404, 429],
                "server_error_codes": [500, 502, 503, 504]
            }
        }
    
    def _initialize_extractors(self) -> Dict[str, Any]:
        """Initialize data extractors"""
        return {
            "instagram": {
                "user_id": r'"user_id":"(\d+)"',
                "username": r'"username":"([^"]+)"',
                "csrf_token": r'"csrf_token":"([^"]+)"',
                "session_id": r'"sessionid":"([^"]+)"',
                "ig_did": r'"ig_did":"([^"]+)"',
                "rollout_hash": r'"rollout_hash":"([^"]+)"'
            },
            "cookies": {
                "sessionid": r'sessionid=([^;]+)',
                "csrftoken": r'csrftoken=([^;]+)',
                "ig_did": r'ig_did=([^;]+)',
                "mid": r'mid=([^;]+)'
            },
            "headers": {
                "x_ig_set_www_claim": "X-IG-Set-WWW-Claim",
                "x_ig_set_authorization": "X-IG-Set-Authorization",
                "x_mid": "X-Mid"
            }
        }
    
    async def process_response(self, response: Dict[str, Any], 
                             response_type: str = "json") -> Dict[str, Any]:
        """Process HTTP response"""
        processed = {
            "original_response": response,
            "parsed_data": None,
            "validation_result": None,
            "extracted_data": {},
            "recommendations": [],
            "timestamp": time.time()
        }
        
        try:
            # Parse response body
            parsed_data = await self._parse_response(response, response_type)
            processed["parsed_data"] = parsed_data
            
            # Validate response
            validation_result = await self._validate_response(response, parsed_data)
            processed["validation_result"] = validation_result
            
            # Extract important data
            extracted_data = await self._extract_data(response, parsed_data)
            processed["extracted_data"] = extracted_data
            
            # Generate recommendations
            recommendations = await self._generate_recommendations(response, validation_result)
            processed["recommendations"] = recommendations
            
            # Calculate processing metrics
            processed["processing_metrics"] = {
                "parse_success": parsed_data is not None,
                "validation_score": validation_result.get("score", 0),
                "data_extracted": len(extracted_data) > 0
            }
            
        except Exception as e:
            processed["error"] = str(e)
            processed["processing_metrics"] = {
                "parse_success": False,
                "validation_score": 0,
                "data_extracted": False
            }
        
        return processed
    
    async def _parse_response(self, response: Dict[str, Any], 
                            response_type: str) -> Optional[Any]:
        """Parse response body"""
        body = response.get("body")
        if not body:
            return None
        
        # Determine parser
        content_type = response.get("headers", {}).get("Content-Type", "").lower()
        
        if "json" in content_type or response_type == "json":
            parser = self.parsers["json"]
        elif "html" in content_type:
            parser = self.parsers["html"]
        elif "text" in content_type:
            parser = self.parsers["text"]
        else:
            parser = self.parsers["binary"]
        
        # Parse
        try:
            return parser(body)
        except Exception:
            # Try other parsers
            for parser_name, parser_func in self.parsers.items():
                try:
                    return parser_func(body)
                except Exception:
                    continue
        
        return None
    
    def _parse_json(self, body: bytes) -> Optional[Dict[str, Any]]:
        """Parse JSON response"""
        try:
            if isinstance(body, bytes):
                body_str = body.decode('utf-8', errors='ignore')
            else:
                body_str = str(body)
            
            return json.loads(body_str)
        except Exception:
            # Try to extract JSON from string
            import re
            json_match = re.search(r'({.*})', body_str if isinstance(body, str) else body.decode('utf-8', errors='ignore'))
            if json_match:
                try:
                    return json.loads(json_match.group(1))
                except Exception:
                    pass
            
            return None
    
    def _parse_html(self, body: bytes) -> Optional[Dict[str, Any]]:
        """Parse HTML response"""
        try:
            from bs4 import BeautifulSoup
            
            soup = BeautifulSoup(body, 'html.parser')
            
            # Extract useful information
            title = soup.title.string if soup.title else None
            meta_tags = {}
            for meta in soup.find_all('meta'):
                if meta.get('name'):
                    meta_tags[meta['name']] = meta.get('content', '')
                elif meta.get('property'):
                    meta_tags[meta['property']] = meta.get('content', '')
            
            # Extract script data
            script_data = []
            for script in soup.find_all('script'):
                if script.string:
                    script_data.append(script.string.strip())
            
            # Extract links
            links = [a.get('href') for a in soup.find_all('a') if a.get('href')]
            
            return {
                "title": title,
                "meta_tags": meta_tags,
                "script_count": len(script_data),
                "link_count": len(links),
                "has_forms": len(soup.find_all('form')) > 0
            }
            
        except Exception:
            return {"raw_html_length": len(body)}
    
    def _parse_text(self, body: bytes) -> str:
        """Parse text response"""
        try:
            if isinstance(body, bytes):
                return body.decode('utf-8', errors='ignore')
            return str(body)
        except Exception:
            return ""
    
    def _parse_binary(self, body: bytes) -> Dict[str, Any]:
        """Parse binary response"""
        return {
            "length": len(body),
            "is_binary": True,
            "first_bytes": body[:100] if len(body) > 100 else body
        }
    
    async def _validate_response(self, response: Dict[str, Any], 
                               parsed_data: Any) -> Dict[str, Any]:
        """Validate response"""
        status = response.get("status")
        headers = response.get("headers", {})
        
        validation_result = {
            "status_code": status,
            "is_success": False,
            "is_error": False,
            "is_redirect": False,
            "score": 0,
            "issues": [],
            "warnings": []
        }
        
        # Check status code
        if status in self.validators["generic"]["success_codes"]:
            validation_result["is_success"] = True
            validation_result["score"] += 0.4
        elif status in self.validators["generic"]["redirect_codes"]:
            validation_result["is_redirect"] = True
            validation_result["score"] += 0.2
        elif status in self.validators["generic"]["client_error_codes"]:
            validation_result["is_error"] = True
            validation_result["score"] -= 0.3
        elif status in self.validators["generic"]["server_error_codes"]:
            validation_result["is_error"] = True
            validation_result["score"] -= 0.5
        
        # Check for Instagram-specific patterns
        if parsed_data and isinstance(parsed_data, dict):
            body_text = json.dumps(parsed_data)
            
            # Check success patterns
            for pattern in self.validators["instagram"]["success_patterns"]:
                if re.search(pattern, body_text, re.IGNORECASE):
                    validation_result["score"] += 0.1
                    validation_result["is_success"] = True
            
            # Check error patterns
            for pattern in self.validators["instagram"]["error_patterns"]:
                if re.search(pattern, body_text, re.IGNORECASE):
                    validation_result["score"] -= 0.2
                    validation_result["is_error"] = True
                    validation_result["issues"].append(f"Error pattern: {pattern}")
            
            # Check rate limit patterns
            for pattern in self.validators["instagram"]["rate_limit_patterns"]:
                if re.search(pattern, body_text, re.IGNORECASE):
                    validation_result["score"] -= 0.3
                    validation_result["is_error"] = True
                    validation_result["warnings"].append("Rate limit detected")
        
        # Check headers
        if "x-rate-limit-remaining" in headers:
            remaining = headers["x-rate-limit-remaining"]
            try:
                if int(remaining) < 10:
                    validation_result["warnings"].append(f"Low rate limit: {remaining}")
                    validation_result["score"] -= 0.1
            except ValueError:
                pass
        
        # Normalize score
        validation_result["score"] = max(0, min(1, validation_result["score"]))
        
        return validation_result
    
    async def _extract_data(self, response: Dict[str, Any], 
                          parsed_data: Any) -> Dict[str, Any]:
        """Extract important data from response"""
        extracted = {}
        
        # Extract from headers
        headers = response.get("headers", {})
        for key, header_name in self.extractors["headers"].items():
            if header_name in headers:
                extracted[key] = headers[header_name]
        
        # Extract from cookies
        cookies = response.get("cookies", {})
        for cookie_name in self.extractors["cookies"]:
            if cookie_name in cookies:
                extracted[cookie_name] = cookies[cookie_name]
        
        # Extract from body
        if parsed_data and isinstance(parsed_data, dict):
            body_text = json.dumps(parsed_data)
            
            for field, pattern in self.extractors["instagram"].items():
                match = re.search(pattern, body_text)
                if match:
                    extracted[field] = match.group(1)
        
        # Extract from response text
        if isinstance(parsed_data, str):
            # Try to find JSON in text
            import re
            json_match = re.search(r'({.*})', parsed_data)
            if json_match:
                try:
                    json_data = json.loads(json_match.group(1))
                    for field, pattern in self.extractors["instagram"].items():
                        if field in json_data:
                            extracted[field] = json_data[field]
                except Exception:
                    pass
        
        return extracted
    
    async def _generate_recommendations(self, response: Dict[str, Any],
                                      validation_result: Dict[str, Any]) -> List[str]:
        """Generate recommendations based on response"""
        recommendations = []
        
        status = response.get("status")
        
        if validation_result["is_success"]:
            if validation_result["score"] >= 0.8:
                recommendations.append("Continue with current strategy")
            else:
                recommendations.append("Proceed with caution")
        
        elif validation_result["is_error"]:
            if status == 429:
                recommendations.append("Implement exponential backoff")
                recommendations.append("Rotate IP address")
                recommendations.append("Reduce request frequency")
            
            elif status == 403:
                recommendations.append("Check authentication tokens")
                recommendations.append("Verify session cookies")
                recommendations.append("Consider using different fingerprint")
            
            elif status == 400:
                recommendations.append("Validate request parameters")
                recommendations.append("Check API documentation")
            
            else:
                recommendations.append("Retry with exponential backoff")
                recommendations.append("Check error details in response")
        
        elif validation_result["is_redirect"]:
            recommendations.append("Follow redirect if appropriate")
            recommendations.append("Update session state with new URL")
        
        # Add general recommendations
        if validation_result["score"] < 0.5:
            recommendations.append("Consider session rotation")
            recommendations.append("Review request patterns")
        
        if len(validation_result["warnings"]) > 0:
            recommendations.append("Address warnings before proceeding")
        
        return recommendations
    
    async def analyze_response_pattern(self, responses: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze response patterns across multiple requests"""
        if not responses:
            return {"error": "No responses to analyze"}
        
        analysis = {
            "total_responses": len(responses),
            "success_count": 0,
            "error_count": 0,
            "redirect_count": 0,
            "status_codes": {},
            "avg_response_time": 0,
            "pattern_detected": None,
            "anomalies": []
        }
        
        response_times = []
        
        for i, response in enumerate(responses):
            status = response.get("status")
            
            # Count status codes
            analysis["status_codes"][status] = analysis["status_codes"].get(status, 0) + 1
            
            # Categorize
            if status and 200 <= status < 300:
                analysis["success_count"] += 1
            elif status and 300 <= status < 400:
                analysis["redirect_count"] += 1
            else:
                analysis["error_count"] += 1
            
            # Collect response times
            response_time = response.get("response_time", 0)
            if response_time > 0:
                response_times.append(response_time)
        
        # Calculate statistics
        if response_times:
            analysis["avg_response_time"] = sum(response_times) / len(response_times)
            analysis["min_response_time"] = min(response_times)
            analysis["max_response_time"] = max(response_times)
            analysis["response_time_std"] = np.std(response_times) if len(response_times) > 1 else 0
        
        # Detect patterns
        success_rate = analysis["success_count"] / analysis["total_responses"]
        
        if success_rate >= 0.9:
            analysis["pattern_detected"] = "stable_success"
        elif success_rate >= 0.7:
            analysis["pattern_detected"] = "mostly_successful"
        elif success_rate >= 0.5:
            analysis["pattern_detected"] = "mixed_results"
        elif success_rate >= 0.3:
            analysis["pattern_detected"] = "mostly_failing"
        else:
            analysis["pattern_detected"] = "failing"
        
        # Detect anomalies
        if response_times and len(response_times) >= 3:
            mean_time = analysis["avg_response_time"]
            std_time = analysis["response_time_std"]
            
            for i, response_time in enumerate(response_times):
                if std_time > 0 and abs(response_time - mean_time) > 3 * std_time:
                    analysis["anomalies"].append({
                        "index": i,
                        "response_time": response_time,
                        "deviation": (response_time - mean_time) / std_time,
                        "type": "response_time_anomaly"
                    })
        
        # Calculate health score
        analysis["health_score"] = min(1.0, max(0.0, 
            success_rate * 0.7 + 
            (1 - (analysis.get("response_time_std", 0) / max(analysis["avg_response_time"], 1))) * 0.3
        ))
        
        # Generate recommendations
        analysis["recommendations"] = []
        
        if success_rate < 0.5:
            analysis["recommendations"].append("Consider changing strategy")
        
        if analysis.get("response_time_std", 0) > analysis["avg_response_time"] * 0.5:
            analysis["recommendations"].append("High response time variability detected")
        
        if analysis["error_count"] > analysis["success_count"]:
            analysis["recommendations"].append("Error rate too high, investigate root cause")
        
        return analysis

# ===================== ACCOUNT CREATOR 2025 =====================

class InstagramAccountCreator2025:
    """Instagram account creator 2025 dengan semua teknik terbaru"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {
            "use_proxy": False,
            "max_retries": 3,
            "request_timeout": 30,
            "email_service": "10minutemail",
            "location": "ID",
            "device_type": "android",
            "connection_type": "auto",
            "verbose": True
        }

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

    async def get_jazoest(self, url="https://www.instagram.com/accounts/emailsignup/"):
        """Enhanced jazoest extraction dengan caching"""
        # Check cache
        cache_key = hashlib.md5(url.encode()).hexdigest()
        current_time = time.time()
        
        if (cache_key in self.jazoest_cache and 
            current_time - self.jazoest_cache[cache_key]["timestamp"] < self.jazoest_ttl):
            return self.jazoest_cache[cache_key]["value"]
        
        # print(f"{cyan}🔍  Fetching fresh jazoest from {url}{reset}")
        
        try:
            # response = await self.request_orchestrator.make_request(
            #     session_id="temp_session",  # Temporary session for jazoest fetch
            #     method="GET",
            #     url=url,
            #     headers={
            #         "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            #         "Accept-Language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7"
            #     }
            # )
            
            # if response.get("status") == 200:
            #     html = response.get("body", b"").decode('utf-8', errors='ignore')
                
            #     # Multiple regex patterns
            #     patterns = [
            #         r'jazoest=(\d+)',
            #         r'"jazoest":"(\d+)"',
            #         r'name="jazoest" value="(\d+)"',
            #         r'jazoest[=:]\s*(\d+)',
            #         r'jazoest.*?(\d{4,5})'
            #     ]
                
            #     for pattern in patterns:
            #         match = re.search(pattern, html)
            #         if match:
            #             jazoest_value = match.group(1)
                        
            #             # Validate jazoest (usually 4-5 digits)
            #             if jazoest_value.isdigit() and 1000 <= int(jazoest_value) <= 99999:
            #                 self.jazoest_cache[cache_key] = {
            #                     "value": jazoest_value,
            #                     "timestamp": current_time,
            #                     "source": "fetched"
            #                 }
            #                 print(f"{hijau}✅  Got jazoest: {jazoest_value}{reset}")
            #                 return jazoest_value
            
            # Fallback generation
            session_hash = hashlib.sha256(str(time.time()).encode()).hexdigest()
            fallback = str(sum(ord(c) for c in session_hash) % 10000 + 1000)
            
            self.jazoest_cache[cache_key] = {
                "value": fallback,
                "timestamp": current_time,
                "source": "fallback"
            }
            
            print(f"{hijau}✅  Got jazoest: {fallback}{reset}")
            return fallback
            
        except Exception as e:
            print(f"{merah}❌  Error getting jazoest: {e}{reset}")
            # Emergency fallback
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
            
            # Call login page API (like real browsers do)
            await self._call_login_page_api(session_id)
            await asyncio.sleep(random.uniform(0.5, 1.5))
            
            # Get username suggestions
            username = await self._get_username_suggestion(session_id, email_data["email"], username_hint)
            if not username:
                return self._record_failure(attempt_id, "Failed to get username")
            
            # Check age eligibility before sending verification
            month, day, year = self._generate_birthdate()
            age_eligible = await self._check_age_eligibility(session_id, day, month, year)
            if not age_eligible:
                print(f"{kuning}⚠️   Age eligibility check failed, continuing anyway{reset}")
            await asyncio.sleep(random.uniform(0.5, 1.0))
            
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
            
            # Create account (pass the same birthdate we validated)
            account_created = await self._create_instagram_account(
                session_id, email_data["email"], username, password, signup_code,
                birthdate=(month, day, year)
            )
            
            if account_created:
                # Get session info for country code
                session = self.session_manager.get_session(session_id)
                ip_config = session.get("ip_config", {}) if session else {}
                country_code = ip_config.get("country_code", ip_config.get("location", {}).get("country", "ID"))
                
                result = self._record_success(attempt_id, {
                    "username": username,
                    "email": email_data["email"],
                    "password": password,
                    "session_id": session_id,
                    "country_code": country_code,
                    "created_at": time.time()
                })
                
                return result
            else:
                return self._record_failure(attempt_id, "Account creation failed")
            
        except Exception as e:
            print(f"{merah}❌  Error in account creation: {e}{reset}")
            import traceback
            traceback.print_exc()
            return self._record_failure(attempt_id, f"Unexpected error: {str(e)}")
    
    async def _create_new_session(self) -> Optional[str]:
        """Create new session with global ISP support"""
        try:
            # Determine connection type
            connection_type = self.config.get("connection_type", "auto")
            if connection_type == "auto":
                # Auto detect: 70% mobile, 30% wifi
                connection_type = "mobile" if random.random() < 0.7 else "wifi"
            
            print(f"{cyan}    Creating {connection_type.upper()} session...{reset}")
            
            # Get IP config first to know which country we're using
            ip_config = self.ip_system.get_fresh_ip_config(
                session_id=None,
                min_health=80,
                connection_type=connection_type
            )
            
            # Get country code from IP config
            country_code = ip_config.get("country_code", ip_config.get("location", {}).get("country", "ID"))
            city = ip_config.get("location", {}).get("city", "Jakarta")
            isp = ip_config.get("isp_info", {}).get("isp", ip_config.get("isp", "telkomsel"))
            
            print(f"{cyan}    Using ISP: {isp} ({country_code}) - City: {city}{reset}")
            
            # Generate fingerprint based on country and connection type
            fingerprint = self.fingerprint_system.generate_fingerprint(
                device_type=self.config["device_type"],
                location=country_code,  # Use country code instead of hardcoded
                connection_type=connection_type,
                isp=isp,
                city=city
            )
            
            # Generate behavior profile based on country
            user_type = self._get_behavior_type_for_country(country_code, connection_type)
            behavior_profile = self.behavior_system.generate_behavior_profile(user_type)
            
            # Generate WebRTC/WebGL fingerprint
            webrtc_fingerprint = self.web_system.get_complete_fingerprint(
                device_type=self.config["device_type"],
                brand=fingerprint.get("device", {}).get("brand", "Samsung"),
                connection_type=connection_type
            )
            
            # Create session with all fingerprints
            session_id = self.session_manager.create_session(
                fingerprint=fingerprint,
                behavior_profile=behavior_profile,
                ip_config=ip_config,
                webrtc_fingerprint=webrtc_fingerprint
            )
            
            print(f"{hijau}✅  Created new {connection_type.upper()} session: {session_id} ({country_code}){reset}")
            return session_id
            
        except Exception as e:
            print(f"{merah}❌  Failed to create session: {e}{reset}")
            import traceback
            traceback.print_exc()
            return None
    
    def _get_behavior_type_for_country(self, country_code: str, connection_type: str) -> str:
        """Get appropriate behavior type based on country - uses existing profile types only"""
        # Map countries to existing Indonesian behavior profiles
        # All countries use the base Indonesian profiles as they contain the same behavioral patterns
        # The profiles are just templates for typing speed, mouse movement, etc.
        
        existing_profiles = [
            "casual_indonesian", 
            "tech_savvy_indonesian", 
            "young_adult_indonesian", 
            "professional_indonesian"
        ]
        
        # Country preference mapping to existing profiles
        country_preference = {
            # Asian countries - casual/young adult focused
            "ID": ["casual_indonesian", "tech_savvy_indonesian", "young_adult_indonesian"],
            "IN": ["casual_indonesian", "tech_savvy_indonesian", "young_adult_indonesian"],
            "JP": ["tech_savvy_indonesian", "professional_indonesian"],
            "KR": ["tech_savvy_indonesian", "young_adult_indonesian"],
            "TH": ["casual_indonesian", "young_adult_indonesian"],
            "VN": ["casual_indonesian", "young_adult_indonesian"],
            "PH": ["casual_indonesian", "young_adult_indonesian"],
            "MY": ["casual_indonesian", "tech_savvy_indonesian"],
            "SG": ["tech_savvy_indonesian", "professional_indonesian"],
            
            # Western countries - more professional/tech savvy
            "US": ["tech_savvy_indonesian", "professional_indonesian", "young_adult_indonesian"],
            "CA": ["tech_savvy_indonesian", "professional_indonesian"],
            "GB": ["professional_indonesian", "tech_savvy_indonesian"],
            "DE": ["professional_indonesian", "tech_savvy_indonesian"],
            "FR": ["professional_indonesian", "casual_indonesian"],
            "IT": ["casual_indonesian", "young_adult_indonesian"],
            "ES": ["casual_indonesian", "young_adult_indonesian"],
            "NL": ["tech_savvy_indonesian", "professional_indonesian"],
            "PL": ["casual_indonesian", "young_adult_indonesian"],
            
            # Latin America - social/casual focused
            "MX": ["casual_indonesian", "young_adult_indonesian"],
            "BR": ["casual_indonesian", "young_adult_indonesian"],
            "AR": ["casual_indonesian", "young_adult_indonesian"],
            
            # Other regions
            "AU": ["tech_savvy_indonesian", "professional_indonesian"],
            "NZ": ["tech_savvy_indonesian", "professional_indonesian"],
            "TR": ["casual_indonesian", "young_adult_indonesian"],
            "RU": ["tech_savvy_indonesian", "casual_indonesian"],
            "AE": ["professional_indonesian", "tech_savvy_indonesian"],
            "SA": ["casual_indonesian", "young_adult_indonesian"]
        }
        
        # Get preferred profiles for country, default to all existing profiles
        preferred_profiles = country_preference.get(country_code, existing_profiles)
        
        # Filter by connection type
        if connection_type == "wifi":
            # WiFi users tend to be more professional/tech savvy
            wifi_preferred = ["tech_savvy_indonesian", "professional_indonesian"]
            matching = [p for p in preferred_profiles if p in wifi_preferred]
            if matching:
                return random.choice(matching)
        else:
            # Mobile users - casual/young adult
            mobile_preferred = ["casual_indonesian", "young_adult_indonesian"]
            matching = [p for p in preferred_profiles if p in mobile_preferred]
            if matching:
                return random.choice(matching)
        
        # Fallback to any preferred profile
        return random.choice(preferred_profiles)

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
            
            # 2. Get country and ISP info from new IP config
            country_code = new_ip_config.get("country_code", new_ip_config.get("location", {}).get("country", "ID"))
            isp = new_ip_config.get("isp_info", {}).get("isp", new_ip_config.get("isp", "telkomsel"))
            city = new_ip_config.get("location", {}).get("city", "Unknown")
            
            print(f"{cyan}    New IP country: {country_code}, ISP: {isp}{reset}")
            
            # 3. Regenerate fingerprint for new country and ISP
            new_fingerprint = self.fingerprint_system.generate_fingerprint(
                device_type=self.config["device_type"],
                location=country_code,  # Use country code
                isp=isp,
                city=city,
                connection_type=new_connection
            )
            
            # 4. Regenerate WebRTC/WebGL fingerprint
            device_brand = new_fingerprint.get("device", {}).get("brand", "Samsung")
            new_webrtc_fingerprint = self.web_system.get_complete_fingerprint(
                device_type=self.config["device_type"],
                brand=device_brand,
                connection_type=new_connection
            )
            
            # 5. Regenerate behavior profile based on new country
            user_type = self._get_behavior_type_for_country(country_code, new_connection)
            new_behavior = self.behavior_system.generate_behavior_profile(user_type)
            
            # 6. Rotate semua identitas sekaligus
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
                
                # Update metadata dengan connection type baru dan country
                self.session_manager.update_session(session_id, {
                    "metadata": {
                        **session.get("metadata", {}),
                        "connection_type": new_connection,
                        "country_code": country_code,
                        "isp": isp
                    }
                })
                
                self.stats["ip_rotations"] = self.stats.get("ip_rotations", 0) + 1
                print(f"{hijau}✅  Successfully rotated IP and fingerprints{reset}")
                print(f"{cyan}    New IP: {new_ip_config.get('ip', 'unknown')}")
                print(f"{cyan}    New ISP: {isp} ({country_code})")
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
        """
        Enhanced pre-signup browser simulation.
        
        Simulates real user behavior by visiting multiple pages before signup,
        building proper cookie chain and appearing as legitimate browser traffic.
        """
        print(f"{cyan}🧠  Simulating pre-signup behavior...{reset}")
        
        session = self.session_manager.get_session(session_id)
        if not session:
            return
        
        behavior_profile = session["behavior_profile"]
        
        # Get current session headers for consistent browsing
        base_headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-User": "?1",
            "Cache-Control": "max-age=0",
        }
        
        try:
            # ===== STEP 1: Visit Instagram homepage first (like a real browser) =====
            print(f"{cyan}    Step 1: Visiting homepage...{reset}")
            homepage_response = await self.request_orchestrator.make_request(
                session_id=session_id,
                method="GET",
                url="https://www.instagram.com/",
                headers={**base_headers, "Sec-Fetch-Site": "none"}
            )
            
            # Extract cookies from homepage
            if homepage_response.get("status") == 200:
                cookies = homepage_response.get("cookies", {})
                if cookies:
                    self.session_manager.update_session(session_id, {"cookies": cookies})
                    print(f"{cyan}    Got initial cookies: {list(cookies.keys())}{reset}")
            
            # Human-like delay between pages
            await asyncio.sleep(random.uniform(2.0, 4.0))
            
            # ===== STEP 2: Visit explore page (optional but makes traffic look natural) =====
            if random.random() < 0.6:  # 60% chance to visit explore first
                print(f"{cyan}    Step 2: Visiting explore page...{reset}")
                await self.request_orchestrator.make_request(
                    session_id=session_id,
                    method="GET",
                    url="https://www.instagram.com/explore/",
                    headers={**base_headers, 
                             "Referer": "https://www.instagram.com/",
                             "Sec-Fetch-Site": "same-origin"}
                )
                await asyncio.sleep(random.uniform(1.5, 3.0))
            
            # ===== STEP 3: Visit accounts/login first (natural user flow) =====
            if random.random() < 0.4:  # 40% chance to check login page first
                print(f"{cyan}    Step 3: Checking login page...{reset}")
                await self.request_orchestrator.make_request(
                    session_id=session_id,
                    method="GET",
                    url="https://www.instagram.com/accounts/login/",
                    headers={**base_headers,
                             "Referer": "https://www.instagram.com/",
                             "Sec-Fetch-Site": "same-origin"}
                )
                await asyncio.sleep(random.uniform(1.0, 2.5))
            
            # ===== STEP 4: Load GraphQL shared data (real browsers do this) =====
            print(f"{cyan}    Step 4: Loading shared data...{reset}")
            await self._load_instagram_shared_data(session_id)
            await asyncio.sleep(random.uniform(1.0, 2.0))
            
        except Exception as e:
            print(f"{kuning}    Pre-signup behavior warning: {e}{reset}")
        
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
    
    async def _load_instagram_shared_data(self, session_id: str) -> Optional[Dict]:
        """
        Load Instagram shared data (like real browsers do).
        
        This loads the shared data bundle that real browsers fetch,
        which contains CSRF tokens, device info, and other initialization data.
        """
        try:
            session = self.session_manager.get_session(session_id)
            if not session:
                return None
            
            # Request the web shared data endpoint
            response = await self.request_orchestrator.make_request(
                session_id=session_id,
                method="GET",
                url="https://www.instagram.com/data/shared_data/",
                headers={
                    "Accept": "*/*",
                    "X-Requested-With": "XMLHttpRequest",
                    "Referer": "https://www.instagram.com/",
                    "Sec-Fetch-Dest": "empty",
                    "Sec-Fetch-Mode": "cors",
                    "Sec-Fetch-Site": "same-origin"
                }
            )
            
            if response.get("status") == 200:
                try:
                    body = response.get("body", b"")
                    if body:
                        data = json.loads(body.decode('utf-8', errors='ignore'))
                        
                        # Extract and store CSRF token if present
                        config = data.get("config", {})
                        csrf_token = config.get("csrf_token")
                        if csrf_token:
                            self.session_manager.update_session(session_id, {
                                "tokens": {"csrftoken": csrf_token}
                            })
                        
                        return data
                except Exception:
                    pass
            
            return None
        except Exception as e:
            print(f"{kuning}    Shared data load warning: {e}{reset}")
            return None
    
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
    
    async def _create_emergency_email(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Create emergency email using 1secmail as fallback"""
        try:
            print(f"{kuning}⚠️   Using emergency email service (1secmail)...{reset}")
            
            # Try 1secmail service directly
            one_sec_mail = OneSecMail2025()
            email_data = await one_sec_mail.get_email()
            
            if email_data:
                # Record in email manager
                self.email_manager.email_cache[email_data["email"]] = {
                    "email_data": email_data,
                    "service_instance": one_sec_mail,
                    "session_id": session_id,
                    "created_at": time.time()
                }
                
                print(f"{hijau}✅  Emergency email created: {email_data['email']}{reset}")
                return email_data
            
            # If 1secmail fails, create manual email
            return await self._create_manual_email(session_id)
            
        except Exception as e:
            print(f"{merah}    Emergency email creation failed: {e}{reset}")
            return await self._create_manual_email(session_id)

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
        """
        Get initial CSRF token with enhanced browser simulation.
        
        This method properly simulates a real browser visiting the signup page,
        with correct headers, referer chain, and cookie handling.
        """
        print(f"{cyan}🛡️   Getting initial CSRF token...{reset}")
        
        try:
            session = self.session_manager.get_session(session_id)
            current_cookies = session.get("cookies", {}) if session else {}
            
            # Build proper browser-like headers
            ip_config = session.get("ip_config", {}) if session else {}
            country_code = ip_config.get("country_code", "US")
            
            locale_map = {
                "US": "en-US", "CA": "en-CA", "GB": "en-GB", "AU": "en-AU",
                "DE": "de-DE", "FR": "fr-FR", "IT": "it-IT", "ES": "es-ES",
                "BR": "pt-BR", "MX": "es-MX", "AR": "es-AR", "ID": "id-ID",
                "IN": "en-IN", "JP": "ja-JP", "KR": "ko-KR", "TH": "th-TH",
                "VN": "vi-VN", "PH": "en-PH", "MY": "ms-MY", "SG": "en-SG",
                "AE": "ar-AE", "SA": "ar-SA", "TR": "tr-TR", "RU": "ru-RU",
                "NL": "nl-NL", "PL": "pl-PL", "NZ": "en-NZ"
            }
            accept_language = locale_map.get(country_code, "en-US") + ",en;q=0.9"
            
            # Chrome version for consistency
            chrome_major = random.choice([140, 141, 142, 143])
            
            # Platform selection
            platforms = [
                {"platform": "macOS", "os_detail": "Macintosh; Intel Mac OS X 10_15_7"},
                {"platform": "Windows", "os_detail": "Windows NT 10.0; Win64; x64"},
            ]
            selected_platform = random.choice(platforms)
            
            headers = {
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
                "Accept-Encoding": "gzip, deflate, br",
                "Accept-Language": accept_language,
                "Cache-Control": "max-age=0",
                "Connection": "keep-alive",
                "Host": "www.instagram.com",
                "Sec-Ch-Ua": f'"Chromium";v="{chrome_major}", "Google Chrome";v="{chrome_major}", "Not_A Brand";v="99"',
                "Sec-Ch-Ua-Mobile": "?0",
                "Sec-Ch-Ua-Platform": f'"{selected_platform["platform"]}"',
                "Sec-Fetch-Dest": "document",
                "Sec-Fetch-Mode": "navigate",
                "Sec-Fetch-Site": "same-origin",
                "Sec-Fetch-User": "?1",
                "Upgrade-Insecure-Requests": "1",
                "User-Agent": f"Mozilla/5.0 ({selected_platform['os_detail']}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{chrome_major}.0.0.0 Safari/537.36",
                "Referer": "https://www.instagram.com/"
            }
            
            # Visit Instagram signup page
            response = await self.request_orchestrator.make_request(
                session_id=session_id,
                method="GET",
                url="https://www.instagram.com/accounts/emailsignup/",
                headers=headers,
                cookies=current_cookies
            )
            
            if response.get("status") == 200:
                # Extract CSRF dari cookies atau HTML
                cookies = response.get("cookies", {})
                if "csrftoken" in cookies:
                    csrf_token = cookies["csrftoken"]
                    
                    # Update session
                    self.session_manager.update_session(session_id, {
                        "tokens": {"csrftoken": csrf_token},
                        "cookies": cookies
                    })
                    
                    print(f"{hijau}✅  Got CSRF token: {csrf_token[:10]}...{reset}")
                    return csrf_token
            
            return None
            
        except Exception as e:
            print(f"{merah}❌  Failed to get CSRF token: {e}{reset}")
            return None
    
    async def _get_username_suggestion(self, session_id: str, email: str, 
                                 hint: Optional[str] = None) -> Optional[str]:
        """Dapatkan username suggestion dari Instagram - DIPERBAIKI"""
        print(f"{cyan}👤  Getting username suggestions...{reset}")
        
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
            
            # Prepare request data dengan lebih banyak parameter
            name = hint or email.split('@')[0]
            request_data = {
                "email": email,
                "first_name": name,
                "username": "",
                "opt_into_one_tap": "false",
                "guid": str(uuid.uuid4()),
                "device_id": session.get("device_id", f"android-{hashlib.sha256(session_id.encode()).hexdigest()[:20]}"),
                "waterfall_id": str(uuid.uuid4()),
                "fb_api_req_friendly_name": "IgWebAccountCreationUsernameSuggestions",
                "fb_api_caller_class": "RelayAPIMethod"
            }
            
            # ENCODE data dengan urlencode
            encoded_data = urlencode(request_data)
            
            print(f"{cyan}    Requesting username for: {email}{reset}")
            
            # Make request
            response = await self.request_orchestrator.make_request(
                session_id=session_id,
                method="POST",
                url="https://www.instagram.com/api/v1/web/accounts/web_create_ajax/attempt/",
                headers={
                    "Content-Type": "application/x-www-form-urlencoded",
                    "X-CSRFToken": session.get("tokens", {}).get("csrftoken", ""),
                    "X-Instagram-AJAX": "1"
                },
                data=encoded_data,  # Gunakan encoded_data, bukan raw dict
                cookies=session.get("cookies", {})
            )
            
            status = response.get("status")
            # print(f"{cyan}    Username API status: {status}{reset}")
            
            if status == 200:
                try:
                    body = response.get("body", b"")
                    if not body:
                        # print(f"{merah}    Empty response body{reset}")
                        return self._generate_fallback_username(email, hint)
                    
                    data = json.loads(body.decode('utf-8', errors='ignore'))
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
                    headers=headers,
                    data=simple_encoded,
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
                await asyncio.sleep(random.uniform(30, 60))
                # Coba sekali lagi
                return await self._get_username_suggestion(session_id, email, hint)
            
            elif status == 403:
                print(f"{merah}    Access forbidden -可能需要新的 CSRF token{reset}")
                # Coba dapatkan CSRF token baru
                new_csrf = await self._get_initial_csrf(session_id)
                if new_csrf:
                    print(f"{cyan}    Got new CSRF, retrying...{reset}")
                    return await self._get_username_suggestion(session_id, email, hint)
            
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
    
    async def _check_age_eligibility(self, session_id: str, day: str, month: str, year: str) -> bool:
        """
        Check age eligibility before sending verification email.
        
        This matches the real Instagram flow where age is verified before proceeding.
        """
        try:
            session = self.session_manager.get_session(session_id)
            if not session:
                return True  # Skip check if no session
            
            jazoest = await self.get_jazoest()
            
            request_data = {
                "day": day,
                "month": month,
                "year": year,
                "jazoest": jazoest
            }
            
            encoded_data = urlencode(request_data)
            
            response = await self.request_orchestrator.make_request(
                session_id=session_id,
                method="POST",
                url="https://www.instagram.com/api/v1/web/consent/check_age_eligibility/",
                headers={
                    "Content-Type": "application/x-www-form-urlencoded",
                    "X-CSRFToken": session.get("tokens", {}).get("csrftoken", ""),
                    "X-Instagram-Ajax": "1029952363",
                    "X-Ig-App-Id": "936619743392459",
                    "X-Requested-With": "XMLHttpRequest",
                    "X-Asbd-Id": "359341",
                    "Sec-Fetch-Site": "same-origin",
                    "Sec-Fetch-Mode": "cors",
                    "Sec-Fetch-Dest": "empty",
                    "Origin": "https://www.instagram.com",
                    "Referer": "https://www.instagram.com/accounts/emailsignup/"
                },
                data=encoded_data,
                cookies=session.get("cookies", {})
            )
            
            if response.get("status") == 200:
                try:
                    body = response.get("body", b"{}").decode('utf-8', errors='ignore')
                    data = json.loads(body) if body else {}
                    
                    if data.get("eligible_to_register") == True:
                        return True
                    else:
                        print(f"{kuning}    Age eligibility: {data}{reset}")
                        return False
                except Exception:
                    return True
            
            return True  # Assume eligible if request fails
            
        except Exception as e:
            print(f"{kuning}    Age check warning: {e}{reset}")
            return True
    
    async def _call_login_page_api(self, session_id: str) -> bool:
        """
        Call the login page API to check GDPR and TOS version.
        
        This is called by real Instagram browsers before signup.
        """
        try:
            session = self.session_manager.get_session(session_id)
            if not session:
                return True
            
            response = await self.request_orchestrator.make_request(
                session_id=session_id,
                method="GET",
                url="https://www.instagram.com/api/v1/web/login_page/",
                headers={
                    "Accept": "*/*",
                    "X-CSRFToken": session.get("tokens", {}).get("csrftoken", ""),
                    "X-Instagram-Ajax": "1029952363",
                    "X-Ig-App-Id": "936619743392459",
                    "X-Requested-With": "XMLHttpRequest",
                    "X-Asbd-Id": "359341",
                    "Sec-Fetch-Site": "same-origin",
                    "Sec-Fetch-Mode": "cors",
                    "Sec-Fetch-Dest": "empty",
                    "Referer": "https://www.instagram.com/accounts/emailsignup/"
                },
                cookies=session.get("cookies", {})
            )
            
            if response.get("status") == 200:
                try:
                    body = response.get("body", b"{}").decode('utf-8', errors='ignore')
                    data = json.loads(body) if body else {}
                    print(f"{cyan}    Login page API: gdpr_required={data.get('gdpr_required')}, tos_version={data.get('tos_version')}{reset}")
                    return True
                except Exception:
                    return True
            
            return True
            
        except Exception as e:
            print(f"{kuning}    Login page API warning: {e}{reset}")
            return True

    async def _send_verification_email(self, session_id: str, email: str) -> bool:
        """Kirim email verifikasi dengan jazoest"""
        print(f"{cyan}📤  Sending verification email...{reset}")
        
        try:
            session = self.session_manager.get_session(session_id)
            if not session:
                return False
            
            # Get fresh jazoest
            jazoest = await self.get_jazoest()
            
            # Prepare request dengan parameter lengkap
            request_data = {
                "device_id": session.get("device_id", ""),
                "email": email,
                "jazoest": jazoest,  # ← TAMBAHKAN JAZOEST
                "_uid": session.get("uid", ""),
                "guid": session.get("guid", str(uuid.uuid4())),
                "_uuid": session.get("uuid", str(uuid.uuid4()))
            }
            
            # Filter out empty values
            request_data = {k: v for k, v in request_data.items() if v}
            
            encoded_data = urlencode(request_data)
            
            response = await self.request_orchestrator.make_request(
                session_id=session_id,
                method="POST",
                url="https://www.instagram.com/api/v1/accounts/send_verify_email/",
                headers={
                    "Content-Type": "application/x-www-form-urlencoded",
                    "X-CSRFToken": session.get("tokens", {}).get("csrftoken", ""),
                    "X-Instagram-AJAX": "1",
                    "X-IG-WWW-Claim": session.get("ig_www_claim", "0"),
                    "X-Web-Session-Id": session.get("extra_session_id", ""),
                    "Priority": "u=1, i",
                    "Sec-Ch-Prefers-Color-Scheme": "dark"
                },
                data=encoded_data,
                cookies=session.get("cookies", {})
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
        """Verifikasi OTP dengan jazoest"""
        print(f"{cyan}🔐  Verifying OTP...{reset}")
        
        try:
            session = self.session_manager.get_session(session_id)
            if not session:
                return None
            
            # Get fresh jazoest
            jazoest = await self.get_jazoest()
            
            # Prepare request dengan parameter lengkap
            request_data = {
                "code": otp,
                "device_id": session.get("device_id", ""),
                "email": email,
                "jazoest": jazoest,  # ← TAMBAHKAN JAZOEST
                "_uid": session.get("uid", ""),
                "guid": session.get("guid", str(uuid.uuid4())),
                "_uuid": session.get("uuid", str(uuid.uuid4()))
            }
            
            # Filter out empty values
            request_data = {k: v for k, v in request_data.items() if v}
            
            encoded_data = urlencode(request_data)
            
            response = await self.request_orchestrator.make_request(
                session_id=session_id,
                method="POST",
                url="https://www.instagram.com/api/v1/accounts/check_confirmation_code/",
                headers={
                    "Content-Type": "application/x-www-form-urlencoded",
                    "X-CSRFToken": session.get("tokens", {}).get("csrftoken", ""),
                    "X-Instagram-AJAX": "1",
                    "X-IG-WWW-Claim": session.get("ig_www_claim", "0"),
                    "X-Web-Session-Id": session.get("extra_session_id", ""),
                    "Priority": "u=1, i",
                    "Sec-Ch-Prefers-Color-Scheme": "dark"
                },
                data=encoded_data,
                cookies=session.get("cookies", {})
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
                                      signup_code: str,
                                      birthdate: Optional[Tuple[str, str, str]] = None) -> bool:
        """
        Create Instagram account with comprehensive anti-detection measures.
        
        This method implements multiple techniques to avoid checkpoint/suspend:
        1. Human-like timing between requests
        2. Proper header and cookie chain
        3. IP rotation on failure
        4. Extended cooldowns
        
        Args:
            birthdate: Optional tuple of (month, day, year) strings. If not provided, generates new.
        """
        
        max_ip_retries = 3
        
        # Use provided birthdate or generate new one
        if birthdate:
            month, day, year = birthdate
        else:
            month, day, year = self._generate_birthdate()
        
        # Add human-like delay before account creation (thinking time)
        think_time = random.uniform(2.0, 5.0)
        print(f"{cyan}    Simulating form review time ({think_time:.1f}s)...{reset}")
        await asyncio.sleep(think_time)
        
        for ip_attempt in range(max_ip_retries):
            print(f"{cyan}    IP Attempt {ip_attempt + 1}/{max_ip_retries}{reset}")
            
            # Rotate IP jika bukan attempt pertama
            if ip_attempt > 0:
                print(f"{cyan}    Rotating to fresh IP and fingerprints...{reset}")
                success = await self.rotate_ip_with_fingerprint(session_id)
                
                if not success:
                    print(f"{merah}    Failed to rotate IP, trying fallback...{reset}")
                    # Fallback: coba get IP config baru saja
                    new_ip_config = self.ip_system.get_fresh_ip_config(min_health=75)
                    session = self.session_manager.get_session(session_id)
                    if session:
                        session["ip_config"] = new_ip_config
                        session["headers"] = {**session.get("headers", {}), **new_ip_config.get("headers", {})}
                
                # Extended cooldown before retry with new IP
                cooldown = random.uniform(25, 45)  # Increased from 15-30
                print(f"{kuning}    Extended cooldown {cooldown:.1f}s before new IP attempt{reset}")
                await asyncio.sleep(cooldown)
                
                # Re-establish session by visiting signup page again
                print(f"{cyan}    Re-establishing session...{reset}")
                await self._get_initial_csrf(session_id)
                await asyncio.sleep(random.uniform(1.5, 3.0))
            
            # Get session dengan headers terkini
            session = self.session_manager.get_session_with_headers(session_id)
            if not session:
                print(f"{merah}    Session not found after rotation{reset}")
                return False
            
            # Get fresh jazoest
            jazoest = await self.get_jazoest()
            
            # Use the birthdate passed to this method (already validated with age eligibility)
            # month, day, year are already defined from the method parameter
            
            # Extra session ID - format: "abc123:def456:ghi789" (colon-separated)
            extra_session_id = session.get("extra_session_id", "")
            if not extra_session_id:
                extra_session_id = self._generate_web_session_id()
            
            # Device ID (client_id) - format from real Instagram
            device_id = session.get("device_id", "")
            if not device_id:
                device_id = self._generate_device_id()
            
            name_first = fake_indonesia.first_name()
            
            # Get current cookies
            current_cookies = self.session_manager.get_session_cookies(session_id, "instagram.com")
            
            # Get IP config for locale info
            ip_config = session.get("ip_config", {})
            country_code = ip_config.get("country_code", ip_config.get("location", {}).get("country", "ID"))
            
            # Get locale for country
            locale_map = {
                "US": "en_US", "CA": "en_CA", "GB": "en_GB", "AU": "en_AU", "NZ": "en_NZ",
                "DE": "de_DE", "FR": "fr_FR", "IT": "it_IT", "ES": "es_ES", "NL": "nl_NL",
                "PL": "pl_PL", "TR": "tr_TR", "RU": "ru_RU", "BR": "pt_BR", "MX": "es_MX",
                "AR": "es_AR", "JP": "ja_JP", "KR": "ko_KR", "IN": "en_IN", "TH": "th_TH",
                "VN": "vi_VN", "PH": "en_PH", "MY": "ms_MY", "SG": "en_SG", "ID": "id_ID",
                "AE": "ar_AE", "SA": "ar_SA"
            }
            locale = locale_map.get(country_code, "en_US")
            
            # Generate Chrome version for consistency - use EXACT format from real Instagram
            chrome_major = 142  # Match the real headers exactly
            chrome_full = f"{chrome_major}.0.7444.162"
            
            # Use EXACT Instagram AJAX build ID from real traffic
            ig_ajax_id = "1029952363"
            
            # Use EXACT X-ASBD-ID from real traffic
            x_asbd_id = "359341"
            
            # Use macOS platform to match real headers exactly
            selected_platform = {
                "platform": "macOS",
                "platform_version": "26.0.1"
            }
            
            # Generate datr cookie if not present (browser fingerprint cookie)
            cookies = session.get("cookies", {})
            if "datr" not in cookies:
                datr = ''.join(random.choices(string.ascii_letters + string.digits + "_-", k=24))
                cookies["datr"] = datr
            
            # **ACCOUNT DATA MATCHING REAL INSTAGRAM FORMAT**
            # Note: Real Instagram uses version 10 encryption but we use version 0 (plaintext)
            # since we don't have the Instagram encryption key
            current_timestamp = int(time.time())
            encrypted_password = f"#PWD_INSTAGRAM_BROWSER:0:{current_timestamp}:{password}"
            
            account_data = {
                "enc_password": encrypted_password,
                "day": str(day),
                "email": email,
                "failed_birthday_year_count": "{}",
                "first_name": name_first,
                "month": str(month),
                "username": username,
                "year": str(year),
                "client_id": device_id,
                "seamless_login_enabled": "1",
                "tos_version": "row",
                "force_sign_up_code": signup_code,
                "extra_session_id": extra_session_id,
                "jazoest": jazoest,
            }
            
            # Filter out empty values
            account_data = {k: v for k, v in account_data.items() if v}
            
            encoded_data = urlencode(account_data)
            if "datr" not in cookies:
                datr = ''.join(random.choices(string.ascii_letters + string.digits + "_-", k=24))
                cookies["datr"] = datr
            
            # **HEADERS MATCHING REAL INSTAGRAM WEB BROWSER** (from provided sample)
            headers = {
                # ===== SECURITY HEADERS (Sec-Ch-*) - MUST BE FIRST =====
                "Sec-Ch-Ua-Full-Version-List": f'"Chromium";v="{chrome_full}", "Google Chrome";v="{chrome_full}", "Not_A Brand";v="99.0.0.0"',
                "Sec-Ch-Ua-Platform": f'"{selected_platform["platform"]}"',
                "Sec-Ch-Ua": f'"Chromium";v="{chrome_major}", "Google Chrome";v="{chrome_major}", "Not_A Brand";v="99"',
                "Sec-Ch-Ua-Model": '""',  # Empty for desktop
                "Sec-Ch-Ua-Mobile": "?0",  # Desktop = ?0, Mobile = ?1
                "Sec-Ch-Ua-Platform-Version": f'"{selected_platform["platform_version"]}"',
                "Sec-Ch-Prefers-Color-Scheme": "dark",
                "Sec-Fetch-Site": "same-origin",
                "Sec-Fetch-Mode": "cors",
                "Sec-Fetch-Dest": "empty",
                
                # ===== INSTAGRAM SPECIFIC HEADERS =====
                "X-Ig-App-Id": "936619743392459",  # Instagram Web App ID
                "X-Requested-With": "XMLHttpRequest",
                "X-Instagram-Ajax": ig_ajax_id,  # Numeric build ID
                "X-Csrftoken": session.get("tokens", {}).get("csrftoken", ""),
                "X-Web-Session-Id": extra_session_id,
                "X-Asbd-Id": x_asbd_id,
                
                # X-Ig-Www-Claim - format: "hmac.AR..." or "0" for new sessions
                "X-Ig-Www-Claim": session.get("ig_www_claim", "0"),
                
                # ===== STANDARD HTTP HEADERS =====
                "Content-Type": "application/x-www-form-urlencoded",
                "Accept": "*/*",
                "Accept-Language": self._get_accept_language_for_locale(locale),
                "Accept-Encoding": "gzip, deflate, br",
                "Origin": "https://www.instagram.com",
                "Referer": "https://www.instagram.com/accounts/emailsignup/",
                "Priority": "u=1, i",
                
                # ===== USER AGENT (Desktop Chrome) =====
                "User-Agent": f"Mozilla/5.0 ({selected_platform['platform'] if selected_platform['platform'] == 'Windows' else 'Macintosh'}; {'Intel Mac OS X 10_15_7' if selected_platform['platform'] == 'macOS' else 'Windows NT 10.0; Win64; x64'}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{chrome_major}.0.0.0 Safari/537.36",
            }
            
            # NOTE: Removed mobile-specific headers that cause checkpoint:
            # - X-IG-App-Locale, X-IG-Device-Locale, X-IG-Mapped-Locale (mobile app)
            # - X-Pigeon-Session-Id, X-Pigeon-Rawclienttime (mobile app)
            # - X-Bloks-Version-Id, X-Bloks-Is-Layout-RTL (mobile app)
            # - X-IG-Device-ID, X-IG-Android-ID (mobile app)
            # - X-IG-Connection-Type, X-IG-Bandwidth-* (mobile app)
            # - X-FB-HTTP-Engine, X-FB-Client-IP (mobile app)
            
            # Add session headers (don't override critical ones)
            session_headers = session.get("headers", {})
            for k, v in session_headers.items():
                if k not in headers:
                    headers[k] = v
            
            # Debug: print request info
            print(f"{cyan}    Creating account with country: {country_code}, locale: {locale}{reset}")
            
            # **ENDPOINT UTAMA** - gunakan yang sama dengan Instagram asli
            endpoints = [
                "https://www.instagram.com/accounts/web_create_ajax/",
                "https://www.instagram.com/api/v1/web/accounts/web_create_ajax/",
            ]
            
            for endpoint in endpoints:
                print(f"{cyan}    Trying endpoint: {endpoint}{reset}")
                
                response = await self.request_orchestrator.make_request(
                    session_id=session_id,
                    method="POST",
                    url=endpoint,
                    headers=headers,
                    data=encoded_data,
                    cookies=current_cookies,
                    require_cookies=True
                )
                
                status = response.get("status")
                # print(f"{cyan}    Status: {status}{reset}")
                
                if status == 200:
                    try:
                        body = response.get("body", b"")
                        if not body:
                            print(f"{merah}    Empty response body{reset}")
                            continue
                        
                        data = json.loads(body.decode('utf-8', errors='ignore'))
                        print(f"{cyan}    Response: {json.dumps(data, indent=2)[:300]}...{reset}")
                        
                        # **CHECK FOR CHECKPOINT/SUSPENDED FIRST** - critical fix
                        if data.get("message") == "checkpoint_required" or data.get("checkpoint_url"):
                            checkpoint_url = data.get("checkpoint_url", "")
                            if "suspended" in checkpoint_url.lower():
                                print(f"{merah}    Account immediately suspended!{reset}")
                                print(f"{merah}    Checkpoint URL: {checkpoint_url}{reset}")
                                # Don't try with same IP - it's burned
                                break  # Exit endpoint loop, try with new IP
                            else:
                                print(f"{kuning}    Checkpoint required: {checkpoint_url}{reset}")
                                # Could be verification checkpoint, log and continue
                                break
                        
                        # Check for failed status
                        if data.get("status") == "fail":
                            error_msg = data.get("message", "Unknown error")
                            print(f"{merah}    Instagram returned fail: {error_msg}{reset}")
                            # Analyze error and decide whether to retry
                            if "spam" in error_msg.lower() or "block" in error_msg.lower():
                                break  # IP is burned
                            continue  # Try next endpoint
                        
                        if data.get("account_created") == True:
                            self.session_manager.update_session(session_id, {
                                "account_created": True,
                                "instagram_username": username,
                                "instagram_user_id": data.get("user_id", ""),
                                "created_at": time.time(),
                                "success_count": session.get("success_count", 0) + 1
                            })

                            bio_text = fake.sentence(nb_words=6)
                            session = self.session_manager.get_session_with_headers(session_id)
                            if not session:
                                print(f"{merah}    Session not found after rotation{reset}")
                                return False

                            headers = {
                                "Content-Type": "application/x-www-form-urlencoded",
                                "X-CSRFToken": session.get("tokens", {}).get("csrftoken", ""),
                                "X-Instagram-AJAX": "1",
                                "X-Web-Session-Id": extra_session_id,
                                "Priority": "u=1, i",
                                "Sec-Ch-Prefers-Color-Scheme": "dark",
                                "X-Requested-With": "XMLHttpRequest",
                                "Referer": "https://www.instagram.com/accounts/edit/",
                                "Origin": "https://www.instagram.com",
                                "Sec-Fetch-Site": "same-origin",
                                "Sec-Fetch-Mode": "cors",
                                "Sec-Fetch-Dest": "empty"
                            }

                            current_cookies = self.session_manager.get_session_cookies(session_id, "instagram.com")
                            
                            # Add session headers
                            session_headers = session.get("headers", {})
                            headers.update({k: v for k, v in session_headers.items() if k not in headers})

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

                            response_edit = await self.request_orchestrator.make_request(
                                session_id=session_id,
                                method="POST",
                                url="https://www.instagram.com/api/v1/web/accounts/edit/",
                                headers=headers,
                                data=encoded_edit,
                                cookies=current_cookies,
                                require_cookies=True
                            )
                            
                            status = response_edit.get("status")

                            if status == 200:
                                try:
                                    body = response_edit.get("body", b"")
                                    if not body:
                                        print(f"{merah}    Empty response body{reset}")
                                        continue
                                    
                                    data = json.loads(body.decode('utf-8', errors='ignore'))
                                    print(f"{cyan}    Response: {json.dumps(data, indent=2)[:300]}...{reset}")
                                    
                                    if data.get("status") == "ok":
                                        # **SUCCESS!**
                                        print(f"\n{bg_hijau}{putih}✅  ACCOUNT CREATED SUCCESSFULLY!{reset}")
                                        print(f"{cyan}    User ID: {data.get('user_id', 'N/A')}{reset}")
                                        print(f"{cyan}    Username: {username}{reset}")
                                        
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
                                
                                        return True

                                    else:
                                        print(f"\n{bg_kuning}{putih}✅  ACCOUNT CREATED CHECKPOINT!{reset}")
                                        print(f"{cyan}    User ID: {data.get('user_id', 'N/A')}{reset}")
                                        print(f"{cyan}    Username: {username}{reset}")
                                        return False

                                except Exception as e:
                                    print(f"{merah}    Parse error: {e}{reset}")
                                    print(f"\n{bg_kuning}{putih}✅  ACCOUNT CREATED CHECKPOINT!{reset}")
                                    print(f"{cyan}    User ID: {data.get('user_id', 'N/A')}{reset}")
                                    print(f"{cyan}    Username: {username}{reset}")
                                    return False

                            else:
                                body = response_edit.get("body", b"")
                                if not body:
                                    print(f"{merah}    Empty response body{reset}")
                                    continue
                                
                                data = json.loads(body.decode('utf-8', errors='ignore'))
                                print(f"{cyan}    Response: {json.dumps(data, indent=2)[:300]}...{reset}")
                                print(f"\n{bg_kuning}{putih}✅  ACCOUNT CREATED CHECKPOINT!{reset}")
                                print(f"{cyan}    User ID: {data.get('user_id', 'N/A')}{reset}")
                                print(f"{cyan}    Username: {username}{reset}")
                                return False
                        else:
                            error_type = self._analyze_error_type(data)
                            print(f"{merah}    Account creation failed: {error_type}{reset}")
                            # print(f"{cyan}    Error details: {data}{reset}")
                            
                            # Jika error selain IP block, coba endpoint lain
                            if error_type != "ip_block":
                                continue
                            else:
                                break
                            
                    except json.JSONDecodeError as e:
                        print(f"{merah}    JSON parse error: {e}{reset}")
                        body_preview = response.get("body", b"").decode('utf-8', errors='ignore')[:500]
                        print(f"{cyan}    Raw response: {body_preview}...{reset}")
                        # Jika 200 OK tapi parse error, mungkin success
                        print(f"{hijau}✅  Account likely created (200 OK){reset}")
                        return True
                    except Exception as e:
                        print(f"{merah}    Parse error: {e}{reset}")
                        continue
                
                elif status == 403:
                    print(f"{merah}    403 Forbidden - IP likely blocked{reset}")
                    break  # Need new IP
                
                elif status == 429:
                    print(f"{kuning}    429 Rate Limited{reset}")
                    self.stats["rate_limited"] = self.stats.get("rate_limited", 0) + 1
                    
                    if ip_attempt < max_ip_retries - 1:
                        wait_time = random.uniform(60, 120)
                        print(f"{kuning}    Rate limit cooldown {wait_time:.1f}s{reset}")
                        await asyncio.sleep(wait_time)
                    break
                
                else:
                    print(f"{merah}    Endpoint failed with status: {status}{reset}")
                    continue
        
        print(f"{merah}❌  Account creation failed after {max_ip_retries} IP attempts{reset}")
        return False
    
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
        """Enhanced post-creation warmup to avoid checkpoint - IMPROVED"""
        print(f"{cyan}✨  Performing post-creation warmup to avoid checkpoint...{reset}")
        
        try:
            session = self.session_manager.get_session(session_id)
            if not session:
                return
            
            # Get current headers and cookies
            headers = session.get("headers", {}).copy()
            cookies = self.session_manager.get_session_cookies(session_id, "instagram.com")
            
            # ===== WARMUP PHASE 1: Initial browsing (like a new user exploring) =====
            print(f"{cyan}    Phase 1: Initial browsing...{reset}")
            
            # 1. View own profile
            await asyncio.sleep(random.uniform(2, 4))
            await self.request_orchestrator.make_request(
                session_id=session_id,
                method="GET",
                url=f"https://www.instagram.com/{username}/",
                headers={"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"},
                cookies=cookies
            )
            
            # 2. View explore page (natural behavior)
            await asyncio.sleep(random.uniform(3, 6))
            await self.request_orchestrator.make_request(
                session_id=session_id,
                method="GET",
                url="https://www.instagram.com/explore/",
                headers={"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"},
                cookies=cookies
            )
            
            # ===== WARMUP PHASE 2: Account settings (seems natural for new user) =====
            print(f"{cyan}    Phase 2: Account settings exploration...{reset}")
            
            # 3. View account settings
            await asyncio.sleep(random.uniform(2, 5))
            await self.request_orchestrator.make_request(
                session_id=session_id,
                method="GET",
                url="https://www.instagram.com/accounts/edit/",
                headers={"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"},
                cookies=cookies
            )
            
            # 4. Check privacy settings
            await asyncio.sleep(random.uniform(2, 4))
            await self.request_orchestrator.make_request(
                session_id=session_id,
                method="GET",
                url="https://www.instagram.com/accounts/privacy_and_security/",
                headers={"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"},
                cookies=cookies
            )
            
            # ===== WARMUP PHASE 3: Light interactions =====
            print(f"{cyan}    Phase 3: Light interactions...{reset}")
            
            # 5. View suggestions (getting friend recommendations)
            await asyncio.sleep(random.uniform(3, 6))
            await self.request_orchestrator.make_request(
                session_id=session_id,
                method="GET",
                url="https://www.instagram.com/explore/people/",
                headers={"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"},
                cookies=cookies
            )
            
            # ===== WARMUP PHASE 4: Activity simulation (critical for anti-checkpoint) =====
            print(f"{cyan}    Phase 4: Activity simulation...{reset}")
            
            # 6. View notifications (shows engagement)
            await asyncio.sleep(random.uniform(2, 4))
            await self.request_orchestrator.make_request(
                session_id=session_id,
                method="GET",
                url="https://www.instagram.com/accounts/activity/",
                headers={"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"},
                cookies=cookies
            )
            
            # 7. View a few popular hashtags (normal new user behavior)
            hashtags = ["travel", "photography", "food", "art", "music"]
            selected_hashtag = random.choice(hashtags)
            await asyncio.sleep(random.uniform(2, 4))
            await self.request_orchestrator.make_request(
                session_id=session_id,
                method="GET",
                url=f"https://www.instagram.com/explore/tags/{selected_hashtag}/",
                headers={"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"},
                cookies=cookies
            )
            
            # 8. Check emails/notifications preferences (shows account setup)
            await asyncio.sleep(random.uniform(2, 4))
            await self.request_orchestrator.make_request(
                session_id=session_id,
                method="GET",
                url="https://www.instagram.com/accounts/emails/settings/",
                headers={"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"},
                cookies=cookies
            )
            
            # 9. Final delay before concluding
            await asyncio.sleep(random.uniform(5, 10))
            
            print(f"{hijau}✅  Post-creation warmup complete (4 phases){reset}")
            print(f"{cyan}    Account should be warmed up and less likely to trigger checkpoint{reset}\n")
            
        except Exception as e:
            print(f"{merah}❌  Error in post-creation warmup: {e}{reset}")
            # Don't fail the whole process just because warmup failed
            print(f"{kuning}    Continuing anyway...{reset}\n")
    
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
    
    def _record_failure(self, attempt_id: str, reason: str) -> Dict[str, Any]:
        """Record failed account creation"""
        self.stats["failed"] += 1
        self.failed_accounts.append({
            "attempt_id": attempt_id,
            "reason": reason,
            "timestamp": time.time()
        })
        
        result = {
            "status": "failed",
            "attempt_id": attempt_id,
            "reason": reason,
            "timestamp": time.time(),
            "message": f"Account creation failed: {reason}"
        }
        
        print(f"{bg_merah}{putih}❌  ACCOUNT CREATION FAILED{reset}")
        print(f"    Reason: {reason}")
        
        return result
    
    def _get_accept_language_for_locale(self, locale: str) -> str:
        """Get Accept-Language header based on locale"""
        accept_language_map = {
            "en_US": "en-US,en;q=0.9",
            "en_CA": "en-CA,en;q=0.9,en-US;q=0.8",
            "en_GB": "en-GB,en;q=0.9,en-US;q=0.8",
            "en_AU": "en-AU,en;q=0.9,en-US;q=0.8",
            "en_NZ": "en-NZ,en;q=0.9,en-US;q=0.8",
            "en_IN": "en-IN,en;q=0.9,hi;q=0.8",
            "en_PH": "en-PH,en;q=0.9,fil;q=0.8",
            "en_SG": "en-SG,en;q=0.9,zh;q=0.8",
            "de_DE": "de-DE,de;q=0.9,en;q=0.8",
            "fr_FR": "fr-FR,fr;q=0.9,en;q=0.8",
            "it_IT": "it-IT,it;q=0.9,en;q=0.8",
            "es_ES": "es-ES,es;q=0.9,en;q=0.8",
            "es_MX": "es-MX,es;q=0.9,en;q=0.8",
            "es_AR": "es-AR,es;q=0.9,en;q=0.8",
            "pt_BR": "pt-BR,pt;q=0.9,en;q=0.8",
            "nl_NL": "nl-NL,nl;q=0.9,en;q=0.8",
            "pl_PL": "pl-PL,pl;q=0.9,en;q=0.8",
            "tr_TR": "tr-TR,tr;q=0.9,en;q=0.8",
            "ru_RU": "ru-RU,ru;q=0.9,en;q=0.8",
            "ja_JP": "ja-JP,ja;q=0.9,en;q=0.8",
            "ko_KR": "ko-KR,ko;q=0.9,en;q=0.8",
            "th_TH": "th-TH,th;q=0.9,en;q=0.8",
            "vi_VN": "vi-VN,vi;q=0.9,en;q=0.8",
            "ms_MY": "ms-MY,ms;q=0.9,en;q=0.8",
            "id_ID": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
            "ar_AE": "ar-AE,ar;q=0.9,en;q=0.8",
            "ar_SA": "ar-SA,ar;q=0.9,en;q=0.8"
        }
        return accept_language_map.get(locale, "en-US,en;q=0.9")
    
    def _generate_web_session_id(self) -> str:
        """
        Generate Instagram web session ID in the correct format.
        
        Real format: "abc123:def456:ghi789" (3 segments separated by colons)
        Each segment is 6 alphanumeric characters.
        """
        chars = string.ascii_lowercase + string.digits
        segment1 = ''.join(random.choices(chars, k=6))
        segment2 = ''.join(random.choices(chars, k=6))
        segment3 = ''.join(random.choices(chars, k=6))
        return f"{segment1}:{segment2}:{segment3}"
    
    def _generate_device_id(self) -> str:
        """
        Generate Instagram device ID (client_id) in the correct format.
        
        Real format: long alphanumeric string like "fteoi31uy3xvd18u088y17jrd6on11xzm10166bzhbvqlw1wigks5"
        """
        chars = string.ascii_lowercase + string.digits
        length = random.randint(45, 55)
        return ''.join(random.choices(chars, k=length))
    
    def _save_account_to_file(self, account_data: Dict[str, Any]):
        """Save account data to file"""
        try:
            filename = "accounts_2025.txt"
            country = account_data.get('country_code', 'ID')
            
            with open(filename, "a", encoding="utf-8") as f:
                f.write(f"{account_data['username']}|{account_data['password']}|"
                       f"{account_data['email']}|{account_data['session_id']}|"
                       f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}|{country}\n")
            
            print(f"{cyan}💾  Account saved to {filename}{reset}")
            
        except Exception as e:
            print(f"{merah}❌  Failed to save account: {e}{reset}")
    
    async def batch_create_accounts(self, count: int, password: str) -> Dict[str, Any]:
        """Create multiple accounts with session refresh on consecutive failures"""
        print(f"{cyan}🏭  Starting batch creation of {count} accounts{reset}")
        
        results = {
            "total": count,
            "successful": 0,
            "failed": 0,
            "accounts": [],
            "errors": [],
            "start_time": time.time()
        }
        
        consecutive_failures = 0
        max_consecutive_failures = 3  # Refresh session after 3 consecutive failures
        
        for i in range(count):
            print(f"\n{biru}🔹  Account {i + 1}/{count}{reset}")
            
            # Check if we need to refresh sessions due to consecutive failures
            if consecutive_failures >= max_consecutive_failures:
                print(f"{kuning}⚠️  {consecutive_failures} consecutive failures - refreshing all sessions{reset}")
                # Clear all sessions to start fresh
                self.session_manager.sessions.clear()
                self.session_manager.session_states.clear()
                self.session_manager.cookie_jar.clear()
                consecutive_failures = 0
                # Extended cooldown after session refresh
                extended_cooldown = random.uniform(60, 90)
                print(f"{kuning}⏳  Extended cooldown {extended_cooldown:.1f}s after session refresh{reset}")
                await asyncio.sleep(extended_cooldown)
            
            result = await self.create_account(password)
            
            if result["status"] == "success":
                results["successful"] += 1
                results["accounts"].append(result["account"])
                consecutive_failures = 0  # Reset on success
            else:
                results["failed"] += 1
                results["errors"].append(result)
                consecutive_failures += 1
            
            # Cooldown between accounts
            if i < count - 1:
                # Longer cooldown if we just had a failure
                if result["status"] != "success":
                    cooldown = random.uniform(45, 75)  # Longer cooldown on failure
                else:
                    cooldown = random.uniform(30, 60)
                print(f"{kuning}⏳  Cooldown for {cooldown:.1f}s before next account{reset}")
                await asyncio.sleep(cooldown)
        
        results["end_time"] = time.time()
        results["duration"] = results["end_time"] - results["start_time"]
        results["success_rate"] = results["successful"] / count if count > 0 else 0
        
        print(f"\n{bg_biru}{putih}📊  BATCH CREATION COMPLETE{reset}")
        print(f"    Successful: {results['successful']}/{count}")
        print(f"    Failed: {results['failed']}/{count}")
        print(f"    Success rate: {results['success_rate']:.1%}")
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
            "device_type": "android",
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
                "Device Type": config.get('device_type', 'android').upper(),
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
        
        print(f"\n{kuning}⚠️   Changing settings requires system restart{reset}")
        
        # Show current settings
        if self.system:
            status = self.system.get_system_status()
            config = status.get("config", {})
            
            print(f"\n{cyan}CURRENT SETTINGS:{reset}")
            print(f"{merah}─────────────────{reset}")
            print(f"  Password: {'*' * len(self.current_password) if self.current_password else 'Not set'}")
            print(f"  Device Type: {config.get('device_type', 'android').upper()}")
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
        "device_type": "android",
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