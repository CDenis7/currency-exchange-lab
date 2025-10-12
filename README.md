# Laborator 03 - Configurarea Planificatorului de Sarcini (Cron)

## Obiectiv
Învățarea configurării planificatorului de sarcini (cron) pentru automatizarea execuției scripturilor.

## Descrierea Proiectului

Acest laborator extinde funcționalitatea laboratorului 02 prin adăugarea automatizării cu ajutorul cron. Sistemul preia automat cursurile de schimb valutar la intervale programate, fără intervenție manuală.

## Structura Proiectului

<img width="451" height="453" alt="image" src="https://github.com/user-attachments/assets/e142e3e3-598f-42cd-bea4-ee796527ce0e" />

## Descrierea Fișierelor

### `currency_exchange_rate.py`
Script Python care comunică cu API-ul PHP pentru a prelua cursurile de schimb valutar pentru o dată specificată. Acceptă trei argumente:
- Moneda sursă (ex: MDL)
- Moneda destinație (ex: EUR, USD)
- Data în format YYYY-MM-DD

### `cronjob`
Fișier care definește două sarcini cron:
- **Sarcina zilnică (6:00 AM)**: Preia cursul MDL la EUR pentru ziua precedentă
- **Sarcina săptămânală (Vineri 5:00 PM)**: Preia cursul MDL la USD pentru vinerea precedentă

Conținut:

<img width="1440" height="172" alt="image" src="https://github.com/user-attachments/assets/73f65a10-8c8d-4f1d-89d1-3f3afd188832" />

### `Dockerfile`
Construiește o imagine de container bazată pe Python 3.11 cu:
- Daemon-ul cron instalat
- Dependențe Python din requirements.txt
- Sarcini cron configurate
- Script de pornire (entrypoint)

<img width="710" height="844" alt="image" src="https://github.com/user-attachments/assets/82e0e4b4-455e-4744-a5ad-7c4d74584594" />

### `entrypoint.sh`
Script de inițializare care:
- Exportă variabilele de mediu pentru cron (`env > /etc/environment`)
- Creează fișierul de log pentru cron
- Pornește monitorizarea logurilor în background
- Lansează daemon-ul cron în foreground (`cron -f`)

<img width="612" height="620" alt="image" src="https://github.com/user-attachments/assets/15d4cf6f-d150-4d00-8785-6e02afa9b900" />

### `docker-compose.yml`
Orchestrează două servicii:
- **web**: Server PHP Apache cu API-ul
- **cron**: Container Python cu sarcinile programate

<img width="459" height="786" alt="image" src="https://github.com/user-attachments/assets/d33f0416-69b5-4f1e-b4da-b1a2657844e0" />

### `.env`
Conține cheia API necesară pentru autentificare:

<img width="343" height="77" alt="image" src="https://github.com/user-attachments/assets/0981e63f-8d0e-4920-895a-597d922f5b66" />

## Cerințe Preliminare

- Docker instalat (versiunea 20.10 sau mai recentă)
- Docker Compose instalat (versiunea 1.29 sau mai recentă)
- Git (pentru controlul versiunilor)

## Instalare și Configurare

### 1. Pregătirea Fișierelor

Cream directorul lab3 si copiam fișierele din lab02

### 2. Crearea Fișierelor Noi

Cream următoarele fișiere în directorul `lab03`:

#### `cronjob`

<img width="1440" height="172" alt="image" src="https://github.com/user-attachments/assets/73f65a10-8c8d-4f1d-89d1-3f3afd188832" />

**Important**: 
- Fișierul trebuie să aibă line endings de tip Unix (LF, nu CRLF)
- Trebuie să existe un newline la sfârșitul fișierului
- Nu lăsați linii goale între intrări

#### `entrypoint.sh`

<img width="612" height="620" alt="image" src="https://github.com/user-attachments/assets/15d4cf6f-d150-4d00-8785-6e02afa9b900" />

#### `Dockerfile`

<img width="710" height="844" alt="image" src="https://github.com/user-attachments/assets/82e0e4b4-455e-4744-a5ad-7c4d74584594" />

#### `docker-compose.yml`

<img width="459" height="786" alt="image" src="https://github.com/user-attachments/assets/d33f0416-69b5-4f1e-b4da-b1a2657844e0" />

### 3. Construirea și Pornirea Containerelor

# Construim imaginile Docker
docker-compose build

<img width="1708" height="560" alt="image" src="https://github.com/user-attachments/assets/83f5404c-e764-4543-99ee-a2773d0614ca" />

# Pornim toate serviciile
docker-compose up -d

<img width="1703" height="180" alt="image" src="https://github.com/user-attachments/assets/2d1121fb-af38-48e1-9d3f-684cf73b8755" />

# Verificam statusul containerelor
docker-compose ps

<img width="1708" height="199" alt="image" src="https://github.com/user-attachments/assets/aa54d670-76b8-43e0-bb7a-55b22d9534e0" />

## Verificarea Funcționării

### 1. Verificam Sarcinile Cron Instalate

<img width="1699" height="154" alt="image" src="https://github.com/user-attachments/assets/ee58302e-68f7-4183-95e9-50f6340a3d77" />

Vedem cele două sarcini cron configurate.

### 2. Monitorizam Logurile Cron

# Vizualizam logurile în timp real

docker-compose logs -f cron

<img width="1023" height="170" alt="image" src="https://github.com/user-attachments/assets/1a8c7859-e42c-4b13-91fa-208b174158b7" />

Scriptul nu va arata nimic pentru ca nu e ora indicata in cron.

### 3. Testam Scriptul Manual

# Executam scriptul manual pentru a verifica funcționarea

docker exec cron_container python currency_exchange_rate.py MDL EUR 2025-10-11

<img width="1693" height="163" alt="image" src="https://github.com/user-attachments/assets/860a0c56-35ee-4e44-9e16-478d7e158eb8" />

## Explicația Programării Cron

### Formatul Cron
```
* * * * * comanda_de_executat
│ │ │ │ │
│ │ │ │ └─── Ziua săptămânii (0-7, 0 și 7 = Duminică)
│ │ │ └───── Luna (1-12)
│ │ └─────── Ziua lunii (1-31)
│ └───────── Ora (0-23)
└─────────── Minutul (0-59)
```

### Sarcina Zilnică (6:00 AM)
```cron
0 6 * * * cd /app && /usr/local/bin/python currency_exchange_rate.py MDL EUR $(date -d "yesterday" +\%Y-\%m-\%d) >> /var/log/cron.log 2>&1
```

**Explicație:**
- `0 6 * * *` - Se execută în fiecare zi la ora 6:00 AM
- `$(date -d "yesterday" +\%Y-\%m-\%d)` - Calculează data de ieri
- `>> /var/log/cron.log 2>&1` - Redirectează output-ul și erorile către log

### Sarcina Săptămânală (Vineri 5:00 PM)
```cron
0 17 * * 5 cd /app && /usr/local/bin/python currency_exchange_rate.py MDL USD $(date -d "last friday" +\%Y-\%m-\%d) >> /var/log/cron.log 2>&1
```

**Explicație:**
- `0 17 * * 5` - Se execută în fiecare Vineri la ora 17:00 (5:00 PM)
- `$(date -d "last friday" +\%Y-\%m-\%d)` - Calculează data Vinerii precedente
- Ziua 5 în cron reprezintă Vineri (0=Duminică, 1=Luni, ..., 5=Vineri)

## Testarea cu Execuție Frecventă

Pentru a testa fără a aștepta până la ora programată, putem modifica temporar fișierul `cronjob` să ruleze în fiecare minut:

<img width="1425" height="114" alt="image" src="https://github.com/user-attachments/assets/a7b78617-148d-403e-8a3d-696fb1a3a7c3" />

Apoi reconstruiți și reporniți:

<img width="1694" height="868" alt="image" src="https://github.com/user-attachments/assets/ee9a9194-f159-4be9-b474-148580056687" />

# Monitorizam logurile
docker-compose logs -f cron

<img width="1699" height="585" alt="image" src="https://github.com/user-attachments/assets/fe8f25ad-9f19-4e6d-88d1-fd5491546e9d" />

<img width="356" height="91" alt="image" src="https://github.com/user-attachments/assets/3659c717-e7d2-4d3e-8c35-4c00ea23ed17" />

Nu uitam să revenim la programul original după testare

## Concluzie

In acest laborator, am explorat automatizarea execuției scripturilor într-un mediu containerizat folosind cron. Am învățat să creăm un Dockerfile care include atât cron, cât și Python, folosind scripturi entrypoint pentru a inițializa corect serviciul. De asemenea, am acoperit configurarea sarcinilor programate, gestionarea variabilelor de mediu în cron și tehnicile esențiale de monitorizare și depanare. La final, am orchestrat întreaga configurație multi-container cu docker-compose.

## Surse:

- [Cron Format Documentation](https://crontab.guru/) - Validator și explicator pentru sintaxa cron
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Python Requests Library](https://requests.readthedocs.io/)
- [Cron Best Practices](https://sanctum.geek.nz/arabesque/cron-best-practices/)

