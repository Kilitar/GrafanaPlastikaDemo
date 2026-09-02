# Vzorový projekt: Průmyslový monitoring vstřikovacích lisů (Plastika a.s.)

## 🎯 Cíl projektu
Příprava praktického referenčního projektu pro pohovor na pozici **Data Analyst** v **Plastika a.s.**
Cílem je demonstrovat schopnost rychle adoptovat firemní technologický stack (**Grafana** + **InfluxDB**), propojit jej se silnými stránkami (**Python**, **SQL**, datová analytika) a představit reálný průmyslový use-case (vstřikovací lisy).

---

## 🛠 Technologický stack
- **Time-series databáze:** InfluxDB (v2 / v3 – organizace, buckety, Flux / SQL / InfluxQL)
- **Vizualizace a alerting:** Grafana (Dashboards, real-time metriky, alert thresholds)
- **Generování a orchestrace dat:** Python (`influxdb-client`, `pandas`, `numpy`)
- **Kontejnerizace:** Docker & Docker Compose (jednoduché lokální spuštění na jedno kliknutí)
- **Analytická nadstavba:** Python / Jupyter / Pandas (analýza cyklů, anomálií, korelace s výrobními zakázkami v relační SQL databázi)

---

## 📦 Moduly projektu

### Modul 1: Lokální prostředí jedním klikem (Docker)
- Konfigurace `docker-compose.yml` pro spuštění InfluxDB a Grafany.
- Přednastavené healthchecky, persistentní volumes pro zachování dat a dashboardů.
- Automatické propojení Grafany s InfluxDB datasource (provisioning).

### Modul 2: Python generátor výrobních dat (Plastika Use-Case)
- Realistická simulace 3 vstřikovacích lisů (např. *Lis 1 - Engel*, *Lis 2 - Arburg*, *Lis 3 - KraussMaffei*).
- **Měřené metriky (Fields):**
  - Teplota taveniny (°C)
  - Vstřikovací tlak (bar)
  - Doba cyklu (s)
  - Počet vyrobených kusů / cyklů
  - Procentuální zmetkovitost / indikátor anomálie
- **Metadata (Tags):**
  - `machine_id`, `mold_id` (forma), `operator_id`, `material_type` (např. PP, ABS, PA66)
- Simulace občasných anomálií (přehřátí taveniny, pokles tlaku, zasekávání cyklu).

### Modul 3: Práce s InfluxDB & dotazovací jazyk (Flux / InfluxQL)
- Návrh schématu pro časové řady:
  - **Bucket:** `production_metrics`
  - **Measurement:** `injection_molding`
  - **Tags vs. Fields** (optimalizace indexace a výkonu).
- Receptář praktických dotazů (agregace po minutách/hodinách, detekce mezních stavů, derivace rychlosti cyklů).

### Modul 4: Výroba profesionálního Grafana Dashboardu
- Komplexní výrobní dashboard:
  - **Real-time Time Series grafy:** Vývoj teploty taveniny a vstřikovacího tlaku s barevnými zónami.
  - **Stat / Gauge panely:** Aktuální stav lisu (RUNNING, IDLE, ERROR), aktuální teplota vs. limitní tolerance.
  - **Výrobní KPI:** Celkový počet kusů za směnu, OEE odhad (Overall Equipment Effectiveness), průměrný čas cyklu.
  - **Alerting:** Nastavení vizuálních a notifikačních pravidel při překročení kritické teploty/tlaku.

### Modul 5: Analytický pohled (Python + InfluxDB + SQL)
- Propojení InfluxDB s `pandas.DataFrame` přes Python klienta.
- Analýza technologických oken (korelace parametrů procesu s kvalitou výrobků).
- Spojení časových řad s relačními daty (SQL tabulka zakázek, šarží materiálu a plánu údržby).
- Export zjištění a manažerský report.

---

## 🚀 Další kroky realizace
1. [x] Uložení kontextu a plánu projektu ([PROJECT_PLAN.md](file:///d:/Antigravity%20Projects/Grafana/PROJECT_PLAN.md)).
2. [ ] Vytvoření `docker-compose.yml` (InfluxDB + Grafana s automatickým provisioningem).
3. [ ] Vytvoření Python generátoru dat `data_generator.py`.
4. [ ] Nastavení dashboardu v Grafaně.
5. [ ] Vytvoření analytického skriptu / notebooku pro business pohled.
