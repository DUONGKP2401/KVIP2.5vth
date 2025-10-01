import threading
import base64
import os
import time
import re
import requests
import socket
import sys
from time import sleep
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
# Xóa bỏ: from concurrent.futures import ThreadPoolExecutor (Không cần nữa)
import json
from collections import Counter, defaultdict
from urllib.parse import urlparse, parse_qs
import random
import math

# Imports from get_device_id.py
import platform
import subprocess
import hashlib

# Check and install necessary libraries
try:
    from faker import Faker
    from requests import session
    from colorama import Fore, Style
    import pystyle
except ImportError:
    os.system("pip install faker requests colorama bs4 pystyle rich")
    os.system("pip3 install requests pysocks")
    print('__Vui Lòng Chạy Lại Tool__')
    sys.exit()

# =====================================================================================
# CONFIGURATION FOR VIP KEY
# =====================================================================================
# URL to the raw KEY-VIP.txt file on GitHub
VIP_KEY_URL = "https://raw.githubusercontent.com/DUONGKP2401/KEY-VIP.txt/main/KEY-VIP.txt"
VIP_CACHE_FILE = 'vip_cache.json'
# =====================================================================================

# Encrypt and decrypt data using base64
def encrypt_data(data):
    return base64.b64encode(data.encode()).decode()

def decrypt_data(encrypted_data):
    return base64.b64decode(encrypted_data.encode()).decode()

# Colors for display
xnhac = "\033[1;36m"
do = "\033[1;31m"
luc = "\033[1;32m"
vang = "\033[1;33m"
xduong = "\033[1;34m"
hong = "\033[1;35m"
trang = "\033[1;39m"
end = '\033[0m'

def banner():
    os.system("cls" if os.name == "nt" else "clear")
    banner_text = f"""
{luc}████████╗ ██████╗░░ ██╗░░██╗░
{luc}╚══██╔══╝ ██╔══██╗░ ██║██╔╝░░
{luc}░░░██║░░░ ██║░░██║░ █████╔╝░░
{luc}░░░██║░░░ ██║░░██║░ ██╔═██╗░░
{luc}░░░██║░░░ ██║░░██║░ ██║░╚██╗░
{luc}░░░╚═╝░░░ ╚█████╔╝░ ╚═╝░░╚═╝░
{trang}══════════════════════════

{vang}Admin: DUONG PHUNG
{vang}Nhóm Zalo: https://zalo.me/g/ddxsyp497
{vang}Tele: @tankeko12
{trang}══════════════════════════
"""
    for char in banner_text:
        sys.stdout.write(char)
        sys.stdout.flush()
        sleep(0.0001)

# =====================================================================================
# DEVICE ID AND IP ADDRESS FUNCTIONS
# =====================================================================================
def get_device_id():
    """Generates a stable device ID based on CPU information."""
    system = platform.system()
    try:
        if system == "Windows":
            cpu_info = subprocess.check_output('wmic cpu get ProcessorId', shell=True, text=True, stderr=subprocess.DEVNULL)
            cpu_info = ''.join(line.strip() for line in cpu_info.splitlines() if line.strip() and "ProcessorId" not in line)
        else:
            try:
                cpu_info = subprocess.check_output("cat /proc/cpuinfo", shell=True, text=True)
            except:
                cpu_info = platform.processor()
        if not cpu_info:
            cpu_info = platform.processor()
    except Exception:
        cpu_info = "Unknown"

    hash_hex = hashlib.sha256(cpu_info.encode()).hexdigest()
    only_digits = re.sub(r'\D', '', hash_hex)
    if len(only_digits) < 16:
        only_digits = (only_digits * 3)[:16]
    
    return f"DEVICE-{only_digits[:16]}"

def get_ip_address():
    """Gets the user's public IP address."""
    try:
        response = requests.get('https://api.ipify.org?format=json', timeout=5)
        ip_data = response.json()
        return ip_data.get('ip')
    except Exception as e:
        print(f"{do}Lỗi khi lấy địa chỉ IP: {e}{trang}")
        return None

def display_machine_info(ip_address, device_id):
    """Displays the banner, IP address, and Device ID."""
    banner()
    if ip_address:
        print(f"{trang}[{do}<>{trang}] {do}Địa chỉ IP: {vang}{ip_address}{trang}")
    else:
        print(f"{do}Không thể lấy địa chỉ IP của thiết bị.{trang}")
    
    if device_id:
        print(f"{trang}[{do}<>{trang}] {do}Mã Máy: {vang}{device_id}{trang}")
    else:
        print(f"{do}Không thể lấy Mã Máy của thiết bị.{trang}")

# =====================================================================================
# XÓA BỎ HOÀN TOÀN CÁC HÀM XỬ LÝ KEY FREE
# =====================================================================================
# luu_thong_tin_ip, tai_thong_tin_ip, kiem_tra_ip, 
# generate_key_and_url, get_shortened_link_phu, process_free_key đã được xóa.

# =====================================================================================
# VIP KEY HANDLING FUNCTIONS
# =====================================================================================

def save_vip_key_info(device_id, key, expiration_date_str):
    """Saves VIP key information to a local cache file."""
    data = {'device_id': device_id, 'key': key, 'expiration_date': expiration_date_str}
    encrypted_data = encrypt_data(json.dumps(data))
    with open(VIP_CACHE_FILE, 'w') as file:
        file.write(encrypted_data)
    print(f"{luc}Đã lưu thông tin Key VIP cho lần đăng nhập sau.{trang}")

def load_vip_key_info():
    """Loads VIP key information from the local cache file."""
    try:
        with open(VIP_CACHE_FILE, 'r') as file:
            encrypted_data = file.read()
        return json.loads(decrypt_data(encrypted_data))
    except (FileNotFoundError, json.JSONDecodeError, TypeError):
        return None

def display_remaining_time(expiry_date_str):
    """Calculates and displays the remaining time for a VIP key."""
    try:
        expiry_date = datetime.strptime(expiry_date_str, '%d/%m/%Y').replace(hour=23, minute=59, second=59)
        now = datetime.now()
        
        if expiry_date > now:
            delta = expiry_date - now
            days = delta.days
            hours, remainder = divmod(delta.seconds, 3600)
            minutes, _ = divmod(remainder, 60)
            print(f"{xnhac}Key VIP của bạn còn lại: {luc}{days} ngày, {hours} giờ, {minutes} phút.{trang}")
        else:
            print(f"{do}Key VIP của bạn đã hết hạn.{trang}")
    except ValueError:
        print(f"{vang}Không thể xác định ngày hết hạn của key.{trang}")

def check_vip_key(machine_id, user_key):
    """
    Checks the VIP key from the URL on GitHub.
    Returns:
        (status, expiration_date_str): Tuple containing status and expiry date string.
    """
    print(f"{vang}Đang kiểm tra Key VIP...{trang}")
    try:
        response = requests.get(VIP_KEY_URL, timeout=10)
        if response.status_code != 200:
            print(f"{do}Lỗi: Không thể tải danh sách key (Status code: {response.status_code}).{trang}")
            return 'error', None

        key_list = response.text.strip().split('\n')
        for line in key_list:
            parts = line.strip().split('|')
            if len(parts) >= 4:
                key_ma_may, key_value, _, key_ngay_het_han = parts
                
                if key_ma_may == machine_id and key_value == user_key:
                    try:
                        expiry_date = datetime.strptime(key_ngay_het_han, '%d/%m/%Y')
                        if expiry_date.date() >= datetime.now().date():
                            return 'valid', key_ngay_het_han
                        else:
                            return 'expired', None
                    except ValueError:
                        continue
        return 'not_found', None
    except requests.exceptions.RequestException as e:
        print(f"{do}Lỗi kết nối đến server key: {e}{trang}")
        return 'error', None

# =====================================================================================
# MAIN AUTHENTICATION FLOW
# =====================================================================================
def main_authentication():
    ip_address = get_ip_address()
    device_id = get_device_id()
    display_machine_info(ip_address, device_id)

    if not ip_address or not device_id:
        print(f"{do}Không thể lấy thông tin thiết bị cần thiết. Vui lòng kiểm tra kết nối mạng.{trang}")
        return False

    # 1. Ưu tiên kiểm tra Key VIP đã lưu trong file cache
    cached_vip_info = load_vip_key_info()
    if cached_vip_info and cached_vip_info.get('device_id') == device_id:
        try:
            expiry_date = datetime.strptime(cached_vip_info['expiration_date'], '%d/%m/%Y')
            if expiry_date.date() >= datetime.now().date():
                print(f"{luc}Đã tìm thấy Key VIP hợp lệ, tự động đăng nhập...{trang}")
                display_remaining_time(cached_vip_info['expiration_date'])
                sleep(3)
                return True
            else:
                print(f"{vang}Key VIP đã lưu đã hết hạn. Vui lòng nhập key mới.{trang}")
        except (ValueError, KeyError):
            print(f"{do}Lỗi file lưu key. Vui lòng nhập lại key.{trang}")

    # 2. Nếu không có key VIP hợp lệ đã lưu, yêu cầu người dùng nhập key
    while True:
        try:
            print(f"{trang}═══════════════════════════════════")
            vip_key_input = input(f'{trang}[{do}<>{trang}] {vang}Vui lòng nhập Key VIP của bạn: {luc}')
            
            if not vip_key_input:
                print(f"{vang}Key không được để trống. Vui lòng nhập lại.{trang}")
                continue

            status, expiry_date_str = check_vip_key(device_id, vip_key_input)
            
            if status == 'valid':
                print(f"{luc}Xác thực Key VIP thành công!{trang}")
                save_vip_key_info(device_id, vip_key_input, expiry_date_str)
                display_remaining_time(expiry_date_str)
                sleep(3)
                return True
            elif status == 'expired':
                print(f"{do}Key VIP của bạn đã hết hạn. Vui lòng liên hệ admin.{trang}")
            elif status == 'not_found':
                print(f"{do}Key VIP không hợp lệ hoặc không tồn tại cho mã máy này.{trang}")
            else: # status == 'error'
                print(f"{do}Đã xảy ra lỗi trong quá trình xác thực. Vui lòng thử lại.{trang}")
            
            sleep(2)

        except KeyboardInterrupt:
            print(f"\n{trang}[{do}<>{trang}] {do}Cảm ơn bạn đã dùng Tool !!!{trang}")
            sys.exit()

# =====================================================================================
# CHẠY CHƯƠNG TRÌNH
# =====================================================================================
if __name__ == "__main__":
    if main_authentication():
        #
        # ĐẶT CÁC CHỨC NĂNG CHÍNH CỦA TOOL CỦA BẠN VÀO ĐÂY
        #
        print("\n\033[1;32mĐăng nhập thành công! Bắt đầu chạy chức năng chính của tool...")
        time.sleep(5)
        print("\033[1;33mTool đã chạy xong. Cảm ơn bạn đã sử dụng!")
        # Ví dụ: main_tool_function()
    else:
        print("\n\033[1;31mXác thực thất bại. Thoát chương trình.")
        sys.exit()

# SECTION 1: UI & UTILITIES
# ==============================================================================
try:
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich.style import Style
    from rich.text import Text
except ImportError:
    print("Thư viện 'rich' chưa được cài đặt. Vui lòng cài đặt: pip install rich")
    sys.exit(1)

console = Console()
STYLE_SUCCESS, STYLE_ERROR, STYLE_WARNING, STYLE_INFO, STYLE_HEADER, STYLE_VALUE = \
    Style(color="green"), Style(color="red"), Style(color="yellow"), Style(color="cyan"), \
    Style(color="magenta", bold=True), Style(color="blue", bold=True)

def clear_console(): os.system("cls" if os.name == "nt" else "clear")
def show_header():
    # === NÂNG CẤP: Cập nhật phiên bản lên V2.9 ===
    header = Text("Tool Xworld Vua thoát hiểm V2.5S - admin: DUONG PHUNG nhóm zalo: https://zalo.me/g/ddxsyp497  telegram: @tankeko12 -Lưu ý : Hãy quản lí vốn thật tốt; không tham lam, biết điểm dừng. Chúc bạn dùng tool vui vẻ!!", style=STYLE_HEADER, justify="center")
    console.print(Panel(header, border_style="magenta", expand=False)); console.print()

# ==============================================================================
# SECTION 2: CONFIGURATION
# ==============================================================================
CONFIG_FILE = "config.json"
def load_or_create_config():
    if os.path.exists(CONFIG_FILE):
        if console.input(f"🔎 Đã tìm thấy file config. Dùng lại? ([bold green]Y[/bold green]/n): ").strip().lower() in ["y", "yes", ""]:
            try:
                with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                    config = json.load(f)
                    if all(k in config for k in ["stop_profit", "stop_loss", "max_lose_streak", "play_rounds", "pause_rounds"]):
                        return config
            except (json.JSONDecodeError, KeyError):
                console.print("⚠️ File config bị lỗi hoặc không hợp lệ. Vui lòng tạo mới.", style=STYLE_WARNING)

    console.print("⚠️ Không tìm thấy config hoặc config cũ. Vui lòng tạo mới.", style=STYLE_WARNING)
    config = {
        "url_game": console.input(f"[{STYLE_INFO}]Nhập Link Game:[/] ").strip(),
        "bet_type": console.input(f"[{STYLE_INFO}]Nhập Loại Tiền cược (BUILD/USDT/WORLD):[/] ").strip().upper(),
        "base_bet": float(console.input(f"[{STYLE_INFO}]Nhập Số Tiền Cược cơ bản:[/] ").strip()),
        "multiplier": float(console.input(f"[{STYLE_INFO}]Nhập Cấp số nhân sau khi thua:[/] ").strip()),
        "max_lose_streak": int(console.input(f"[{STYLE_WARNING}]Nhập Giới hạn chuỗi thua để DỪNG/RESET (ví dụ: 5):[/] ").strip()),
        "stop_profit": float(console.input(f"[{STYLE_SUCCESS}]Nhập Số LÃI mục tiêu để DỪNG (ví dụ: 50):[/] ").strip()),
        "stop_loss": float(console.input(f"[{STYLE_ERROR}]Nhập Mức LỖ tối đa để DỪNG (ví dụ: 100):[/] ").strip())
    }

    while True:
        try:
            config["play_rounds"] = int(console.input(f"[{STYLE_INFO}]Nhập số ván muốn chơi trước khi tạm nghỉ (nhập 0 để chơi liên tục):[/] ").strip())
            config["pause_rounds"] = int(console.input(f"[{STYLE_INFO}]Nhập số ván muốn nghỉ sau mỗi phiên:[/] ").strip())
            if config["play_rounds"] > 0 and config["pause_rounds"] <= 0:
                console.print("🔥 Nếu đã cài số ván chơi, số ván nghỉ phải lớn hơn 0. Vui lòng nhập lại.", style=STYLE_WARNING)
                continue
            if config["play_rounds"] < 0 or config["pause_rounds"] < 0:
                 console.print("🔥 Vui lòng nhập số dương.", style=STYLE_WARNING)
                 continue
            break
        except ValueError:
            console.print("🔥 Vui lòng nhập một số hợp lệ.", style=STYLE_ERROR)

    with open(CONFIG_FILE, "w", encoding="utf-8") as f: json.dump(config, f, indent=4)
    console.print(f"✅ Đã lưu config vào file [bold cyan]{CONFIG_FILE}[/bold cyan]", style=STYLE_SUCCESS)
    return config

# ==============================================================================
# SECTION 3: PREDICTION LOGIC (V2.9 - DIVERSIFIED COLLECTIVE STRATEGY)
# ==============================================================================
def choose_safe_room(recent_100, lose_streak=0, last_win_room=None, user_id=None, issue_id=None):
    try:
        full_history = [int(r["killed_room_id"]) for r in recent_100 if "killed_room_id" in r] if isinstance(recent_100, list) else []
        if len(full_history) < 20: return random.randint(1, 8), 0

        # LỚP 1: LỌC CỨNG - CÁC QUY TẮC BẤT BIẾN
        candidate_rooms = set(range(1, 9))
        last_killed = full_history[0]

        candidate_rooms.discard(last_killed)
        if last_win_room:
            candidate_rooms.discard(last_win_room)

        hot_counts_15 = Counter(full_history[:15])
        for room, count in hot_counts_15.items():
            if count >= 3:
                candidate_rooms.discard(room)

        if not candidate_rooms:
            fallback_pool = list(range(1, 9))
            if last_killed in fallback_pool: fallback_pool.remove(last_killed)
            return random.choice(fallback_pool) if fallback_pool else random.randint(1, 8), 5.0

        # LỚP 2: HỘI ĐỒNG CHUYÊN GIA - PHÂN TÍCH ĐA CHIỀU (KHÔNG DÙNG TRỌNG SỐ)
        def _get_contrarian_danger(history, candidates):
            gaps = {r: history.index(r) if r in history else len(history) for r in candidates}
            if not gaps: return set()
            max_gap = max(gaps.values())
            return {room for room, gap in gaps.items() if gap == max_gap}

        def _get_pattern_danger(history, candidates):
            if len(history) < 2: return set()
            transitions = defaultdict(Counter)
            for i in range(len(history) - 1): transitions[history[i+1]][history[i]] += 1
            if history[0] in transitions and transitions[history[0]]:
                most_likely = transitions[history[0]].most_common(1)[0][0]
                if most_likely in candidates: return {most_likely}
            return set()

        def _get_parity_danger(history, candidates):
            if len(history) < 4: return set()
            parities = [h % 2 for h in history[:4]]
            if len(set(parities)) == 1:
                return {r for r in candidates if r % 2 == parities[0]}
            return set()

        def _get_trend_danger(history, candidates):
            return {room for room, count in hot_counts_15.items() if count >= 2 and room in candidates}

        def _get_neighbor_danger(history, candidates):
            last = history[0]
            neighbors = {(last % 8) + 1, (last - 2 + 8) % 8 + 1}
            return {r for r in candidates if r in neighbors}

        # === NÂNG CẤP V2.9: Thêm chuyên gia phân tích phòng đối xứng (1-5, 2-6,...) ===
        def _get_opposite_danger(history, candidates):
            """Chuyên gia cảnh báo về phòng đối diện với phòng vừa bị tiêu diệt."""
            if not history: return set()
            last = history[0]
            opposites = {1: 5, 5: 1, 2: 6, 6: 2, 3: 7, 7: 3, 4: 8, 8: 4}
            opposite_room = opposites.get(last)
            if opposite_room and opposite_room in candidates:
                return {opposite_room}
            return set()

        # Thêm chuyên gia mới vào hội đồng
        all_specialists = [_get_contrarian_danger, _get_pattern_danger, _get_parity_danger,
                           _get_trend_danger, _get_neighbor_danger, _get_opposite_danger]

        danger_votes = Counter()
        for specialist in all_specialists:
            dangerous_rooms = specialist(full_history, candidate_rooms)
            for room in dangerous_rooms:
                danger_votes[room] += 1

        # LỚP 3: LỰA CHỌN PHÂN TÁN - ĐẢM BẢO MỖI USER CHỌN 1 PHÒNG KHÁC NHAU
        rooms_by_vote = defaultdict(list)
        for r in candidate_rooms:
            rooms_by_vote[danger_votes.get(r, 0)].append(r)

        if not rooms_by_vote:
             return random.choice(list(candidate_rooms)) if candidate_rooms else random.randint(1,8), 5.0

        min_danger_score = min(rooms_by_vote.keys())
        safest_pool = rooms_by_vote[min_danger_score]
        
        # Sắp xếp pool an toàn để đảm bảo thứ tự nhất quán cho mọi người dùng
        safest_pool.sort()

        # === CỐT LÕI BẢO VỆ: Sử dụng UserID và IssueID để phân tán cược, tránh bị game soi ===
        # Logic này đảm bảo rằng với cùng một ván, những người dùng khác nhau sẽ chọn các phòng khác nhau
        # trong nhóm những phòng an toàn nhất, khiến hành vi trông tự nhiên và không thể bị theo dõi.
        if not user_id or not issue_id or not safest_pool:
            return random.choice(safest_pool) if safest_pool else random.randint(1,8), min_danger_score

        try:
            # Công thức giúp mỗi user có một lựa chọn khác nhau nhưng có thể đoán trước được
            choice_index = (int(user_id) + int(issue_id)) % len(safest_pool)
            final_choice = safest_pool[choice_index]
            return final_choice, min_danger_score
        except (ValueError, TypeError):
             return random.choice(safest_pool), min_danger_score

    except Exception:
        return random.randint(1, 8), 0

# ==============================================================================
# SECTION 4: API & DATA HANDLING
# ==============================================================================
def make_api_request(session, method, url, max_retries=3, **kwargs):
    base_delay = 1
    for attempt in range(max_retries):
        time.sleep(random.uniform(0.3, 0.8))
        try:
            response = session.request(method, url, timeout=10, **kwargs)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException:
            if attempt == max_retries - 1: return None
            time.sleep((base_delay * 2 ** attempt) + random.uniform(0.5, 1.5))
    return None

def get_wallet_balance(session, url, bet_type):
    resp = make_api_request(session, "GET", url)
    if not resp or resp.get("code") not in [0, 200]: return None
    wallet = resp.get("data", {}).get("cwallet")
    if wallet is None: return None
    key_map = {"USDT": "ctoken_kusdt", "WORLD": "ctoken_kther", "BUILD": "ctoken_contribute"}
    balance_str = wallet.get(key_map.get(bet_type))
    return float(balance_str) if balance_str is not None else None

def display_summary(session_state, round_data, config, room_names_map):
    BET_TYPE, MAX_LOSE_STREAK = config["bet_type"], config["max_lose_streak"]
    win_rate = (session_state['wins'] / (session_state['wins'] + session_state['losses']) * 100) if (session_state['wins'] + session_state['losses']) > 0 else 0
    
    summary_table = Table(title=f"[bold]Tóm Tắt Vòng {session_state['round']}[/]", show_header=True, header_style="bold magenta")
    summary_table.add_column("Chỉ số", width=15); summary_table.add_column("Giá trị")
    summary_table.add_row("Ván đấu", f"#{round_data.get('issue_id', 'N/A')}")
    summary_table.add_row("Hành động", round_data.get('action', Text("---")))
    if round_data.get('result'):
        killed_room_id = round_data['result'].get('killed_room_id', 'N/A')
        killed_room_name = room_names_map.get(str(killed_room_id), '?')
        summary_table.add_row("Phòng Sát Thủ", f"{killed_room_id} ({killed_room_name})")
    
    if round_data.get('final_balance') is not None:
        summary_table.add_row("Số dư Hiện tại", f"{round_data.get('final_balance', 0):.4f} {BET_TYPE}")

    summary_table.add_row("Kết quả", round_data.get('outcome', Text("---")))
    summary_table.add_row("Tiền cược", f"{round_data.get('bet_amount', 0):.4f} {BET_TYPE}")
    profit_text = Text(f"{round_data.get('round_profit', 0):+.4f}", style=STYLE_SUCCESS if round_data.get('round_profit', 0) >= 0 else STYLE_ERROR)
    summary_table.add_row("Lời/Lỗ Vòng", profit_text)
    total_profit_text = Text(f"{session_state.get('cumulative_profit', 0):+.4f}", style=STYLE_SUCCESS if session_state.get('cumulative_profit', 0) >= 0 else STYLE_ERROR)
    summary_table.add_row("Tổng Lời/Lỗ", total_profit_text)
    summary_table.add_row("Thắng/Thua", f"{session_state['wins']}/{session_state['losses']} ({win_rate:.2f}%)")
    summary_table.add_row("Chuỗi thắng", f"{session_state['win_streak']} (Max: {session_state['max_win_streak']})")
    summary_table.add_row("Chuỗi thua", f"[red]{session_state['lose_streak']}[/red]/{MAX_LOSE_STREAK}")
    console.print(summary_table); console.print("-" * 60)

# ==============================================================================
# SECTION 5: MAIN LOGIC
# ==============================================================================
def main():
        
    clear_console(); show_header(); config = load_or_create_config()
    try:
        params = parse_qs(urlparse(config["url_game"]).query)
        user_id, secret_key = params.get("userId", [None])[0], params.get("secretKey", [None])[0]
        if not user_id or not secret_key: raise ValueError("Invalid Link")
    except (ValueError, IndexError, TypeError):
        console.print("[red]LỖI: Link game không hợp lệ.[/red]"); return

    BET_TYPE, BASE_BET, MULTIPLIER, STOP_PROFIT, STOP_LOSS, MAX_LOSE_STREAK, PLAY_ROUNDS, PAUSE_ROUNDS = \
        config["bet_type"], config["base_bet"], config["multiplier"], \
        config["stop_profit"], config["stop_loss"], config["max_lose_streak"], \
        config["play_rounds"], config["pause_rounds"]
    
    ROOM_NAMES = {"1":"Nhà Kho", "2":"Phòng Họp", "3":"PhGĐ", "4":"PhTròChuyện", "5":"PhGiámSát", "6":"VănPhòng", "7":"PhTàiVụ", "8":"PhNhânSự"}

    API_BASE = "https://api.escapemaster.net/escape_game"
    URL_USER_INFO = "https://user.3games.io/user/regist?is_cwallet=1"
    URL_BET = f"{API_BASE}/bet"
    URL_RECENT_10 = f"{API_BASE}/recent_10_issues?asset={BET_TYPE}"
    URL_RECENT_100 = f"{API_BASE}/recent_issues?limit=100&asset={BET_TYPE}"
    
    title = "[bold cyan]Cấu Hình Hoạt Động[/]"
    play_pause_text = f"Chơi {PLAY_ROUNDS} ván, nghỉ {PAUSE_ROUNDS} ván" if PLAY_ROUNDS > 0 else "Chơi liên tục"
    text = (f"Loại Tiền Cược : {BET_TYPE}\nCược Cơ Bản    : {BASE_BET}\nCấp số nhân    : x{MULTIPLIER}\n"
            f"Chế độ chơi     : {play_pause_text}\n"
            f"[yellow]Giới hạn thua   : {MAX_LOSE_STREAK} ván[/yellow]\n"
            f"[green]Mục tiêu Lãi   : +{STOP_PROFIT}[/green]\n[red]Ngưỡng Cắt Lỗ  : -{STOP_LOSS}[/red]")
    console.print(Panel(Text(text, style="white"), title=title, border_style="cyan", expand=False))

    api_session = requests.Session()
    USER_AGENTS = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/116.0",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    ]
    api_session.headers.update({"user-id": user_id, "user-secret-key": secret_key, "user-agent": random.choice(USER_AGENTS)})
    
    console.print("🔄 [italic]Đang quét số dư ban đầu làm mốc...[/italic]")
    initial_balance = get_wallet_balance(api_session, URL_USER_INFO, BET_TYPE)
    if initial_balance is None:
        console.print("❌ [red]Không thể lấy số dư ban đầu. Vui lòng kiểm tra lại Link Game và kết nối.[/red]"); return
    console.print(f"✅ [green]Số dư ban đầu được ghi nhận: [bold]{initial_balance:.4f} {BET_TYPE}[/bold][/green]\n")
    
    session_state = { "round": 0, "wins": 0, "losses": 0, "cumulative_profit": 0.0, "lose_streak": 0, "win_streak": 0, "max_win_streak": 0, "last_known_issue_id": None, "last_bet_on": None, "balance_before_bet": initial_balance, "initial_balance": initial_balance, "rounds_played_this_session": 0, "rounds_to_skip": 0, "last_win_room": None }

    while True:
        try:
            resp10 = make_api_request(api_session, "GET", URL_RECENT_10)
            if not resp10 or not resp10.get("data"):
                console.print("[yellow]Không thể lấy lịch sử 10 ván, đang chờ...[/yellow]", end="\r"); time.sleep(5); continue
            
            latest_result = resp10["data"][0]
            latest_issue_id = str(latest_result.get("issue_id"))

            if latest_issue_id != session_state["last_known_issue_id"]:
                session_state["round"] += 1
                console.print(f"\n--- Vòng {session_state['round']}: Xử lý kết quả ván #{latest_issue_id} ---", style="bold yellow")
                
                round_data = {"issue_id": latest_issue_id, "bet_amount": 0, "round_profit": 0, "result": latest_result, "action": Text("---"), "outcome": Text("Không cược", style="dim")}
                last_bet = session_state.get("last_bet_on")
                
                if last_bet and str(last_bet["issue_id"]) == latest_issue_id:
                    if PLAY_ROUNDS > 0: session_state["rounds_played_this_session"] += 1
                    killed_room_id = latest_result.get("killed_room_id")
                    bet_room, bet_amount, balance_before = last_bet['room'], last_bet['amount'], session_state['balance_before_bet']

                    console.print("[cyan]... Đang đồng bộ số dư từ máy chủ ...[/cyan]", end="\r"); time.sleep(random.uniform(8, 12))
                    final_balance = get_wallet_balance(api_session, URL_USER_INFO, BET_TYPE)
                    console.print(" " * 60, end="\r")
                    
                    is_win = (killed_room_id is not None and int(killed_room_id) != int(bet_room))
                    
                    if is_win:
                        round_data["outcome"] = Text("THẮNG", style=STYLE_SUCCESS)
                        session_state.update({"wins": session_state["wins"]+1, "lose_streak": 0, "win_streak": session_state["win_streak"]+1, "last_win_room": bet_room})
                        session_state["max_win_streak"] = max(session_state["max_win_streak"], session_state["win_streak"])
                        round_profit = (final_balance - balance_before) if final_balance is not None and balance_before is not None else bet_amount * 0.95
                    else:
                        round_data["outcome"] = Text("THUA", style=STYLE_ERROR)
                        session_state.update({"losses": session_state["losses"]+1, "lose_streak": session_state["lose_streak"]+1, "win_streak": 0})
                        round_profit = -bet_amount
                    
                    session_state["cumulative_profit"] = (final_balance - session_state["initial_balance"]) if final_balance is not None else session_state["cumulative_profit"] + round_profit
                    
                    bet_room_name = ROOM_NAMES.get(str(bet_room), '?')
                    action_text = Text(f"Đã cược Phòng {bet_room} ({bet_room_name})", style=STYLE_INFO)
                    round_data.update({ "bet_amount": bet_amount, "action": action_text, "round_profit": round_profit, "final_balance": final_balance })
                
                if session_state["round"] > 1 or (session_state["round"] == 1 and last_bet): display_summary(session_state, round_data, config, ROOM_NAMES)
                
                if 0 < MAX_LOSE_STREAK <= session_state['lose_streak']:
                    console.print(Panel(f"BẠN ĐÃ THUA LIÊN TIẾP {session_state['lose_streak']} VÁN!", title="[bold yellow]ĐẠT GIỚI HẠN CHUỖI THUA[/bold yellow]", border_style="yellow"))
                    choice = console.input("Bạn muốn [bold green]Chơi tiếp[/bold green] (reset tiền cược) hay [bold red]Nghỉ[/bold red]? (mặc định là Chơi tiếp) [C/N]: ").strip().lower()
                    if choice in ['n', 'nghi']: console.print("[yellow]Bot đã dừng theo yêu cầu của người dùng.[/yellow]"); return
                    else: session_state['lose_streak'] = 0; console.print("[green]Đã reset tiền cược về mức ban đầu. Tiếp tục chơi...[/green]\n")

                if session_state['cumulative_profit'] >= STOP_PROFIT: console.print(Panel(f"✅ ĐÃ ĐẠT MỤC TIÊU LỢI NHUẬN! (Tổng lãi: {session_state['cumulative_profit']:.4f} {BET_TYPE})", title="[bold green]DỪNG TOOL[/bold green]", border_style="green")); return
                if session_state['cumulative_profit'] <= -STOP_LOSS: console.print(Panel(f"❌ ĐÃ CHẠM NGƯỠNG CẮT LỖ! (Tổng lỗ: {session_state['cumulative_profit']:.4f} {BET_TYPE})", title="[bold red]DỪNG TOOL[/bold red]", border_style="red")); return

                session_state["last_known_issue_id"] = latest_issue_id
                next_round_id = int(latest_issue_id) + 1

                if PLAY_ROUNDS > 0 and session_state["rounds_played_this_session"] >= PLAY_ROUNDS:
                    console.print(Panel(f"Đã hoàn thành {session_state['rounds_played_this_session']} ván. Bắt đầu nghỉ {PAUSE_ROUNDS} ván.", title="[bold cyan]TẠM NGHỈ[/bold cyan]", border_style="cyan"))
                    session_state["rounds_to_skip"] = PAUSE_ROUNDS; session_state["rounds_played_this_session"] = 0

                if session_state["rounds_to_skip"] > 0:
                    console.print(f"😴 [yellow]Đang trong thời gian nghỉ, bỏ qua cược. Còn lại [bold]{session_state['rounds_to_skip']}[/bold] ván nghỉ...[/yellow]")
                    session_state["rounds_to_skip"] -= 1; session_state["last_bet_on"] = None; time.sleep(5); continue
                
                current_balance = get_wallet_balance(api_session, URL_USER_INFO, BET_TYPE)
                if current_balance is None:
                    console.print(f"⚠️ Không thể xác minh số dư, tạm bỏ qua ván #{next_round_id} để đảm bảo an toàn.", style=STYLE_WARNING); session_state["last_bet_on"] = None; time.sleep(10); continue
                
                if session_state.get("last_bet_on") and str(session_state["last_bet_on"]["issue_id"]) == str(next_round_id):
                    console.print(f"🛡️ [yellow]Đã có cược cho ván #{next_round_id}. Bỏ qua để tránh cược trùng.[/yellow]"); time.sleep(5); continue

                session_state['balance_before_bet'] = current_balance
                console.print(f"💰 Số dư hiện tại: [bold green]{current_balance:.4f} {BET_TYPE}[/bold green] | Chuẩn bị cho ván: [bold]#{next_round_id}[/bold]")
                
                resp100 = make_api_request(api_session, "GET", URL_RECENT_100)
                recent_100_hist = resp100.get("data") if resp100 and resp100.get("data") else []
                
                time.sleep(random.uniform(1.0, 2.5))
                console.print(f"🤖 [italic]BOT V2.5S đang phân tích ván #{next_round_id}...[/italic]")
                
                predicted_room, danger_score = choose_safe_room(recent_100_hist, session_state['lose_streak'], session_state['last_win_room'], user_id, next_round_id)
                
                HESITATION_THRESHOLD = 3.0
                if danger_score >= HESITATION_THRESHOLD and random.random() < 0.33:
                    console.print(f"🤔 [yellow]Tín hiệu không rõ ràng (độ rủi ro: {danger_score:.1f}). Tạm nghỉ 1 ván để quan sát.[/yellow]"); session_state["last_bet_on"] = None; continue

                base_bet_amount = round(BASE_BET * (MULTIPLIER ** session_state["lose_streak"]), 4)
                bet_amount = round(base_bet_amount * random.uniform(0.995, 1.015), 4)
                
                if bet_amount > current_balance:
                    console.print(f"⚠️ Không đủ số dư ({current_balance:.4f}). Cần {bet_amount:.4f}. Bỏ qua ván.", style=STYLE_WARNING); session_state["last_bet_on"] = None
                else:
                    predicted_room_name = ROOM_NAMES.get(str(predicted_room), "?")
                    console.print(f"✅ Cược [bold blue]{bet_amount:.4f} {BET_TYPE}[/bold blue] vào phòng [bold blue]{predicted_room} ({predicted_room_name})[/bold blue] cho ván [bold]#{next_round_id}[/bold]...")
                    
                    bet_payload = { "asset_type": BET_TYPE, "user_id": int(user_id), "room_id": predicted_room, "bet_amount": bet_amount }
                    bet_response = make_api_request(api_session, "POST", URL_BET, json=bet_payload)

                    if bet_response and bet_response.get("code") == 0:
                        session_state["last_bet_on"] = {"issue_id": next_round_id, "room": predicted_room, "amount": bet_amount}
                        console.print("✅ Đặt cược thành công!", style="green")
                    else:
                        console.print(f"❌ Đặt cược thất bại! Phản hồi: {bet_response}", style="red"); session_state["last_bet_on"] = None
            else:
                console.print(f"[yellow]... Chờ kết quả ván #{int(latest_issue_id) + 1} ...[/yellow]", end="\r")
                time.sleep(3)
        except Exception as e:
            console.print(f"\n[red]Gặp lỗi trong vòng lặp chính: {e}. Đang thử lại sau 10 giây...[/red]"); time.sleep(10)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n\nBot đã dừng bởi người dùng.", style="bold yellow")
    except Exception as e:
        console.print(f"\nĐã xảy ra lỗi không mong muốn:", style=STYLE_ERROR)
        console.print_exception(show_locals=False)