# 🏭 PLASTIKA a.s. – Digital Shopfloor & IoT Analytics Stack

Kompletní referenční projekt uchazeče o pozici **Data Analyst** v **PLASTIKA a.s.** (Kroměříž).  
Projekt integruje **InfluxDB**, **Grafanu**, **Python (Pandas)** a **ERP QI (SQL)** pro řešení skutečných výzev popsaných ve **Výroční zprávě 2024**.

---

## 🎯 Hlavní business use-case projektu: Řešení KPI 02 (Náklady na nejakost - NNJ)
Ve Výroční zprávě 2024 PLASTIKA a.s. uvádí:
> *"Cílová hodnota Nákladů na nejakost (NNJ) pro rok 2024 stanovená na 2,89 % nebyla splněna (skutečnost 4,98 %). Důvodem byl nárůst zmetkovitosti lisovaných a lakovaných dílů u nově nabíhajících projektů."*

Tento projekt ukazuje, jak Data Analyst pomocí propojení **telemetrie ze vstřikovacích lisů v InfluxDB** a **zakázkových norem z ERP systému QI** dokáže:
1. **Identifikovat anomálie v reálném čase v Grafaně** (přehřátí taveniny, propady vstřikovacích tlaků, vady na lince lakovny).
2. **Kvantifikovat finanční ztráty** z nejakosti na jednotlivých zakázkách (Škoda Auto, Continental, TIFS, VW).
3. **Provádět Root-Cause analýzu** s doporučeními pro ředitele výroby a kvality.

---

## 🚀 Rychlé spuštění projektu (Quick Start)

### 1. Spuštění kontejnerů (Docker Compose)
```bash
docker compose up -d
```

### 🔐 Přihlašovací údaje k webovým rozhraním:

| Služba | URL | Uživatel | Heslo | Detaily |
| :--- | :--- | :--- | :--- | :--- |
| **Grafana** | [http://localhost:3000](http://localhost:3000) | `admin` | `admin` | Dashboards ➔ **Výroba Plastika** |
| **InfluxDB v2** | [http://localhost:8086](http://localhost:8086) | `admin` | `adminpassword123` | Org: `plastika`, Bucket: `production_metrics` |

*(API Token pro InfluxDB klienta: `plastika-super-secret-auth-token-12345`)*

---

### 2. Spuštění generátoru výrobních dat (Live stream)
```bash
.venv\Scripts\activate
python data_generator.py
```
*(Nebo jednoduše dvakrát klikněte na soubor **`start_demo.bat`**, který vše spustí a vygeneruje čerstvá data k aktuálnímu dni).*

### 3. Spuštění manažerského analytického vyhodnocení (Python + SQL + InfluxDB)
```bash
python analytics_demo.py
```

---

## 🏭 Simulované výrobní linky a zakázky

| Provoz / ID | Stroj | Zákazník | Projekt | Díl / Forma | Materiál |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **002 - Vstřikovna** (`LIS-201`) | Engel Victory 120t (2K lis) | **Škoda Auto** | SpaceBEV / Kodiaq | Rámeček přístrojové desky (`FORMA-SKODA-BEV-01`) | PC-ABS / TPE |
| **002 - Vstřikovna** (`LIS-208`) | Engel Duo 500t | **Continental** | ECU Sensor Housing | Konektorové pouzdro 24-PIN (`FORMA-CONTI-ECU-24`) | PA66-GF30 |
| **002 - Vstřikovna** (`LIS-305`) | KraussMaffei CX 650t | **TI Fluid Systems (TIFS)** | Fuel & Thermal Line | Palivový a chladicí adaptér (`FORMA-TIFS-FUEL-08`) | POM-C / PA12 |
| **008 - Lakovna** (`LAK-FLAT-01`) | Linka FLAT BED | **VW Koncern** | VW Emblem & Trim | Dekorační lakovaný nápis (`FORMA-VW-EMBLEM-02`) | ABS lakovaný |

---

## 🧠 Analytické koncepty pro pohovor (Interview Master Points)

1. **Modelování v InfluxDB (Tags vs. Fields):**
   - **Tags (indexované):** `provoz`, `machine_id`, `customer`, `project`, `mold_id`, `material`, `defect_type`, `status`.
   - **Fields (numerická data):** `melt_temperature`, `hydraulic_pressure`, `cycle_time`, `power_consumption_kw`, `is_scrap`, `scrap_cost_czk`.
2. **Informační ekosystém Plastiky:**
   - Znalost systémů **ERP QI**, **WMS DCIx** s funkcí **RTG** (retrográdní výdej materiálu dle signálů ze strojů) a aplikace **S-Karta** pro technologické parametry forem.
3. **Představení ROI a finančního dopadu:**
   - Snížení NNJ ze **4,98 %** na cílových **2,89 %** představuje pro Plastiku úsporu **přes 20 mil. Kč ročně**.
