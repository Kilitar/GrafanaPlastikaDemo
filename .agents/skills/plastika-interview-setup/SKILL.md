---
name: plastika-interview-setup
description: Instrukce pro inicializaci a spuštění referenčního IoT & Analytics projektu PLASTIKA a.s. na novém notebooku.
---

# 🏭 Plastika a.s. – Setup a spuštění na novém notebooku

Tento skill slouží k automatické přípravě a spuštění prostředí pro pohovor na pozici **Data Analyst v PLASTIKA a.s.**.

## 📌 Informace o projektu
- **GitHub repozitář:** `https://github.com/Kilitar/GrafanaPlastikaDemo.git`
- **Technologický stack:** Docker (InfluxDB 2.7, Grafana 11), Python 3.10+ (InfluxDB Client, Pandas), SQLite mock ERP QI.
- **Doména:** Výroba vstřikováním plastů (Engel, KraussMaffei) a lakovna (FlatBed), sledování KPI 02 - Náklady na nejakost (NNJ).

---

## 🛠️ Postup spuštění pro agenta

Pokud uživatel požádá o přípravu nebo spuštění na novém stroji:

1. **Naklonování repozitáře (pokud ještě není naklonován):**
   ```powershell
   git clone https://github.com/Kilitar/GrafanaPlastikaDemo.git .
   ```

2. **Vytvoření virtuálního prostředí a instalace knihoven:**
   ```powershell
   python -m venv .venv
   .venv\Scripts\pip install -r requirements.txt
   ```

3. **Spuštění Docker kontejnerů:**
   ```powershell
   docker compose up -d
   ```

4. **Vygenerování čerstvých historických dat a spuštění živého streamu:**
   ```powershell
   .venv\Scripts\python -u data_generator.py
   ```

5. **Přístupy pro uživatele:**
   - **Grafana:** `http://localhost:3000` (login: `admin` / `admin`)
   - **InfluxDB:** `http://localhost:8086` (login: `admin` / `adminpassword123`)

---

## 📊 Prezentace pokročilé analytiky:
Kromě Grafany agent na požádání spustí manažerský vyhodnocovací skript:
```powershell
.venv\Scripts\python analytics_demo.py
```
Tento skript demonstruje schopnost analytika spojit časové řady z IoT s relačními databázemi (ERP QI) a vyčíslit finanční dopady.
