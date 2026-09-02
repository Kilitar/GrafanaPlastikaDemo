# 📋 Instrukce pro nasazení a spuštění projektu na novém notebooku

Tento dokument slouží jako **přesný průvodce pro uživatele i pro AI agenta (Antigravity / Gemini)** na novém notebooku, aby byl celý stack PLASTIKA a.s. připraven na prezentaci během několika minut.

---

## 💻 1. Co musí být na notebooku předem nainstalováno (Prerekvizity)

Pokud notebook ještě tyto nástroje nemá, stačí je stáhnout a nainstalovat:

1. **Git pro Windows:** [https://git-scm.com/download/win](https://git-scm.com/download/win)
2. **Python 3.10+ (nebo 3.11/3.12):** [https://www.python.org/downloads/](https://www.python.org/downloads/) *(Při instalaci nezapomeňte zaškrtnout: ☑️ "Add python.exe to PATH")*
3. **Docker Desktop:** [https://www.docker.com/products/docker-desktop/](https://www.docker.com/products/docker-desktop/) *(Ujistěte se, že je Docker spuštěný a svítí zelená ikona "Engine running")*

---

## 🤖 2. Instrukce pro AI Agenta na novém notebooku

Pokud otevřete Antigravity / Gemini na notebooku v prázdné složce, předejte agentovi tento prompt:

```markdown
Pracujeme na referenčním projektu pro pohovor na pozici Data Analyst v PLASTIKA a.s.
Repozitář projektu: https://github.com/Kilitar/GrafanaPlastikaDemo.git

Proveď tyto kroky:
1. Naklonuj repozitář: git clone https://github.com/Kilitar/GrafanaPlastikaDemo.git .
2. Vytvoř virtuální prostředí Pythonu: python -m venv .venv
3. Nainstaluj závislosti: .venv\Scripts\pip install -r requirements.txt
4. Spusť Docker kontejnery: docker compose up -d
5. Spusť start_demo.bat nebo vygeneruj čerstvá data k aktuálnímu datu pohovoru přes data_generator.py.
```

---

## 🚀 3. Ruční postup krok za krokem (Pokud to budete spouštět sám bez agenta)

Otevřete terminál (PowerShell nebo CMD) ve složce, kde chcete mít projekt:

### Krok 1: Klonování repozitáře
```powershell
git clone https://github.com/Kilitar/GrafanaPlastikaDemo.git
cd GrafanaPlastikaDemo
```

### Krok 2: Příprava Python prostředí a instalace knihoven
```powershell
python -m venv .venv
.venv\Scripts\pip install -r requirements.txt
```

### Krok 3: Spuštění celé demonstrace (1-Click)
Jednoduše dvakrát klikněte na soubor **`start_demo.bat`** (nebo v terminálu zadejte):
```powershell
.\start_demo.bat
```

Tento skript automaticky:
1. Spustí Docker kontejnery s InfluxDB a Grafanou.
2. Zkontroluje dostupnost InfluxDB a **vygeneruje čerstvá telemetrická data za posledních 8 hodin přesně k aktuální minutě spuštění** (takže v grafech nebudou žádné prázdné mezery).
3. Otevře webový prohlížeč na adrese [http://localhost:3000](http://localhost:3000).
4. Ponechá běžet živý generátor dat (nové body každé 2 vteřiny).

---

## 🔑 4. Rychlý přehled přihlašovacích údajů

| Služba | URL | Uživatel | Heslo |
| :--- | :--- | :--- | :--- |
| **Grafana** | [http://localhost:3000](http://localhost:3000) | `admin` | `admin` |
| **InfluxDB v2** | [http://localhost:8086](http://localhost:8086) | `admin` | `adminpassword123` |

---

## 🎤 5. Co na pohovoru ukázat a spustit (Prezentační scénář)

1. **Živý Shopfloor Dashboard v Grafaně:**
   * Otevřete [http://localhost:3000](http://localhost:3000) ➔ Dashboard **PLASTIKA a.s. – Digital Shopfloor & Quality Monitoring**.
   * **Stav linek:** Horní stavové semafory pro 4 klíčové stroje (Škoda, Continental, TIFS, VW).
   * **Procesní parametry:** Grafy teplot taveniny a hydraulických tlaků podle technologické S-Karty.
   * **Kvalita a NNJ:** Zmetkovitost v kusech vs. limit NNJ 2,89 %.
   * **Finanční metriky (2+2 layout):** Finanční NNJ % ze zakázky a hodinová intenzita škod v Kč/h.

2. **Manažerský report pro ředitele výroby a kvality:**
   * V terminálu spusťte:
     ```powershell
     .venv\Scripts\python analytics_demo.py
     ```
   * Tento skript v reálném čase propojí časové řady z InfluxDB se zakázkami v ERP QI (SQLite mock) a vytiskne:
     * Vyhodnocení celkového KPI 02 (NNJ) firmy.
     * Analýzu nejztrátovějších zakázek (Root-Cause analýza: přehřátí u Škoda BEV, podstříknutí u TIFS).
     * Finanční dopad a doporučená nápravná opatření pro technology.
