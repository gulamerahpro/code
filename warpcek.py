import requests
import json
import logging
import http.client
from urllib3.exceptions import InsecureRequestWarning

# Nonaktifkan warning SSL
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# Konfigurasi logging
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

def generate_random_string(length=10):
    """Generate random string untuk install_id dan fcm_token"""
    import string
    import random
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

def check_warp_key(key):
    """Fungsi untuk memeriksa status WARP key"""
    url = "https://api.cloudflareclient.com/v0a745/reg"
    
    # Konfigurasi headers dan payload
    headers = {
        "Content-Type": "application/json; charset=UTF-8",
        "User-Agent": "okhttp/3.12.1",
        "Accept": "application/json",
        "Accept-Language": "en-US",
    }
    
    payload = {
        "key": key,
        "install_id": generate_random_string(22),
        "fcm_token": generate_random_string(22),
        "referrer": key,
        "warp_enabled": False,
        "tos": "20210928",
        "type": "Android",
        "locale": "en_US"
    }
    
    # Konfigurasi session requests
    session = requests.Session()
    session.headers.update(headers)
    
    try:
        # Kirim request dengan konfigurasi tambahan
        response = session.post(
            url, 
            json=payload, 
            verify=False,  # Nonaktifkan verifikasi SSL
            timeout=10     # Tambahkan timeout
        )
        
        # Log detail response
        logger.info(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            try:
                data = response.json()
                
                # Debug: Print seluruh response
                logger.info(f"Full Response: {json.dumps(data, indent=2)}")
                
                # Cek referral count
                referral_count = data.get("account", {}).get("referral_count", 0)
                
                if referral_count < 5:
                    logger.info(f"Key {key}: Valid (Referral Count: {referral_count})")
                    return "Valid"
                else:
                    logger.info(f"Key {key}: Full (Referral Count: {referral_count})")
                    return "Full"
            
            except json.JSONDecodeError:
                logger.error("Gagal mendekode JSON")
                return "Error: Invalid JSON"
        
        elif response.status_code == 403:
            logger.warning(f"Key {key}: Diblokir atau tidak valid")
            return "Blocked"
        
        else:
            logger.warning(f"Kode status tidak dikenal: {response.status_code}")
            return f"Unknown Status: {response.status_code}"
    
    except requests.exceptions.RequestException as e:
        logger.error(f"Request Error: {e}")
        return f"Request Error: {e}"
    
    except Exception as e:
        logger.error(f"Unexpected Error: {e}")
        return f"Unexpected Error: {e}"

def main():
    """Fungsi utama untuk memproses daftar keys"""
    input_file = "keys.txt"
    output_file = "warp_keys_status.txt"
    
    try:
        with open(input_file, "r") as infile, open(output_file, "w") as outfile:
            keys = [line.strip() for line in infile if line.strip()]
            
            logger.info(f"Total keys yang akan dicek: {len(keys)}")
            
            for key in keys:
                status = check_warp_key(key)
                print(f"Key: {key} - Status: {status}")
                outfile.write(f"{key} - {status}\n")
        
        logger.info(f"Hasil telah disimpan di {output_file}")
    
    except FileNotFoundError:
        logger.error(f"File {input_file} tidak ditemukan.")
    
    except Exception as e:
        logger.error(f"Terjadi kesalahan: {e}")
    
    

if __name__ == "__main__":
    main()