import argparse
import requests
import json
import os
import logging
import sys
from datetime import datetime

# --- Configurări Globale ---
# Folosim numele containerului API, așa cum am stabilit
API_BASE_URL = "http://php_apache/"

# Definim calea către directorul de date, mapat în docker-compose.yml
# Scriptul se așteaptă să fie în /app, deci 'data' va fi în /app/data
DATA_DIR = 'data'
LOG_FILE = 'error.log'

# --- Configurarea Sistemului de Logging ---
# Configurăm logger-ul să scrie în fișierul mapat în docker-compose.yml
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler(sys.stdout) # Afișează logurile și în consolă
    ]
)

def get_exchange_rate(api_key, from_currency, to_currency, date_str):
    """
    Funcție pentru a prelua cursul de schimb de la API.
    """
    params = {
        'from': from_currency,
        'to': to_currency,
        'date': date_str
    }
    payload = {
        'key': api_key
    }
    try:
        logging.info(f"Se trimite cererea către: {API_BASE_URL} cu parametrii: {params}")
        response = requests.post(API_BASE_URL, params=params, data=payload, timeout=10)
        response.raise_for_status()  # Verifică dacă request-ul a avut erori HTTP (ex: 404, 500)
        
        data = response.json()
        if data.get("error"):
            logging.error(f"Eroare de la API: {data['error']}")
            return None
        
        return data.get("data")

    except requests.exceptions.RequestException as e:
        logging.error(f"Eroare de rețea sau HTTP: {e}")
        return None
    except json.JSONDecodeError:
        logging.error(f"Nu s-a putut decoda răspunsul JSON. Răspuns: {response.text}")
        return None

def save_data_to_json(data, from_currency, to_currency, date_str):
    """
    Funcție pentru a salva datele într-un fișier JSON.
    """
    try:
        # Creează directorul 'data' dacă nu există
        if not os.path.exists(DATA_DIR):
            os.makedirs(DATA_DIR)
            logging.info(f"Directorul '{DATA_DIR}' a fost creat.")
            
        filename = f"{from_currency.upper()}_{to_currency.upper()}_{date_str}.json"
        filepath = os.path.join(DATA_DIR, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        logging.info(f"Datele au fost salvate cu succes în: {filepath}")

    except OSError as e:
        logging.error(f"Eroare la salvarea fișierului: {e}")

def main():
    """Funcția principală a scriptului."""
    parser = argparse.ArgumentParser(description="Preluare curs valutar de la API.")
    parser.add_argument("from_currency", type=str, help="Moneda sursă (ex: USD).")
    parser.add_argument("to_currency", type=str, help="Moneda destinație (ex: EUR).")
    parser.add_argument("date", type=str, help="Data în format YYYY-MM-DD.")
    
    args = parser.parse_args()
    
    # Validăm formatul datei
    try:
        datetime.strptime(args.date, '%Y-%m-%d')
    except ValueError:
        logging.error("Format dată invalid. Folosiți YYYY-MM-DD.")
        sys.exit(1)

    api_key = os.getenv("API_KEY")
    if not api_key:
        logging.error("Variabila de mediu API_KEY nu este setată.")
        sys.exit(1)

    exchange_data = get_exchange_rate(api_key, args.from_currency, args.to_currency, args.date)
    
    if exchange_data:
        save_data_to_json(exchange_data, args.from_currency, args.to_currency, args.date)
    else:
        logging.warning("Procesul s-a încheiat fără a salva date.")
        sys.exit(1)

if __name__ == "__main__":
    main()