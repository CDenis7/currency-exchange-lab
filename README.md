# Laborator 02: Crearea unui script Python pentru interacțiunea cu o API

Acest proiect conține un script Python pentru a interacționa cu o API pentru cursul de schimb valutar local, a preluat data pentru o anumită dată și a le salva într-un fișier JSON.

# Descriere Generală

Proiectul este format din două componente principale:

Un server API local (serviciu web): Rulează într-un container Docker și oferă date despre cursurile de schimb valutar.

Un script Python (client): Trimite cereri către serverul API pentru a obține date specifice și le salvează local.

# Partea 1: Serviciul API (Serverul)

Pentru început, am configurat și am pornit serverul API local, care se află în folderul lab02prep.

Pașii de Configurare și Rulare pe care i-am urmat

Am navigat în directorul serverului:

Folosind un terminal, am intrat în folderul lab02prep.

Am creat fișierul de configurare:

Pentru ca serverul să aibă o cheie API, am copiat fișierul sample.env pentru a crea fișierul .env si am pornit Serverul. Am folosit comenzile:

<img width="974" height="462" alt="image" src="https://github.com/user-attachments/assets/6ecac922-7940-41f2-ae5f-6c221e6ba156" />

După pornire, serverul a devenit activ la adresa http://localhost:8080. Am lăsat acest terminal deschis pe toată durata lucrului.

# Partea 2: Scriptul de Automatizare (Clientul Python)

Cu serverul rulând, am trecut la configurarea și rularea scriptului Python din folderul automation/lab02.

Pașii de Configurare și Rulare pe care i-am urmat

 Am deschis un NOU Terminal:

 Am lăsat terminalul cu serverul activ și am deschis o a doua fereastră de terminal.

 Am navigat în directorul scriptului:
 
 În noul terminal, am intrat în folderul automation/lab02.
 
 Am instalat Dependențele:
    
Pentru a rula scriptul, este necesară biblioteca requests din Python. Aceasta poate fi instalată folosind managerul de pachete pip și fișierul requirements.txt furnizat.

    py -m pip install -r requirements.txt
    
<img width="974" height="412" alt="image" src="https://github.com/user-attachments/assets/940a590a-d769-4d7f-8a8e-5f6f37c25d7c" />

 Am setat Cheia API si am rulat Scriptul::
 
<img width="974" height="94" alt="image" src="https://github.com/user-attachments/assets/d7a4c76d-2ce9-471a-9ed8-e4a31e06ea17" />

În final, am executat scriptul cu diverse seturi de date pentru a-l testa.

Sintaxa folosită:

python currency_exchange_rate.py <MONEDA_SURSA> <MONEDA_DESTINATIE> <AAAA-LL-ZZ>

<img width="974" height="144" alt="image" src="https://github.com/user-attachments/assets/2476cf59-0708-4484-985a-2df7e06fae09" />

<img width="974" height="479" alt="image" src="https://github.com/user-attachments/assets/f0c2e486-94ac-42f3-9dbb-cd262c47fdb4" />

# Structura și logica scriptului

Scriptul este conceput pentru a fi robust și a gestiona erorile corespunzător. Logica principală este structurată astfel:

Configurare Inițială:

Importă bibliotecile necesare (os, sys, requests, json, logging, etc.).

Definește constante globale, cum ar fi URL-ul API-ului, numele directorului pentru date și numele fișierului de log.

Configurează sistemul de logging pentru a scrie erorile în fișierul error.log.

Funcția Principală (main):

Validarea precondițiilor: Verifică dacă variabila de mediu API_KEY este setată și dacă numărul de argumente din linia de comandă este corect (trebuie să fie exact trei). Dacă nu, scriptul se oprește cu un mesaj de eroare.

Construirea Cererii: Preia argumentele din linia de comandă și construiește URL-ul și corpul (payload) cererii POST.

Comunicarea cu API-ul: Folosește un bloc try...except pentru a trimite cererea către server. Acest bloc prinde erori de rețea (ex: serverul nu este pornit).

Procesarea Răspunsului:

Verifică dacă răspunsul de la server este unul de succes (cod 200 OK).

Transformă răspunsul din format text JSON într-un obiect Python.

Verifică dacă răspunsul conține o cheie de eroare specifică API-ului (ex: "monedă invalidă").

Salvarea Datelor:

Dacă răspunsul este valid și nu conține erori, scriptul se asigură că directorul data există (îl creează dacă este necesar).

Construiește un nume de fișier dinamic, pe baza argumentelor (ex: USD_EUR_2025-01-15.json).

Scrie datele primite în acest fișier, în format JSON.

Afișează un mesaj de succes în consolă.

Gestionarea Erorilor: Orice eroare apărută în oricare dintre pașii de mai sus (validare, cerere, procesare, salvare) este prinsă, înregistrată în error.log și un mesaj de eroare este afișat în consolă.

# Concluzie

Acest laborator a demonstrat cu succes capacitatea de a crea și utiliza un client Python pentru a interacționa cu un API web. Au fost atinse obiectivele cheie, incluzând trimiterea de cereri HTTP parametrizate, procesarea răspunsurilor JSON, gestionarea robustă a erorilor și salvarea datelor într-un format structurat. Proiectul a consolidat cunoștințele practice despre arhitectura client-server și automatizarea proceselor de extragere a datelor.

# Surse:

Python: https://docs.python.org/3/

Biblioteca requests: https://requests.readthedocs.io/en/latest/

Docker Compose: https://docs.docker.com/compose/
