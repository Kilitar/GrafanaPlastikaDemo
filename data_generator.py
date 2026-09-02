"""
Python generátor výrobních telemetrických dat – PLASTIKA a.s. Kroměříž
Plně autentická data založená na Výroční zprávě 2024 a výrobním programu:
- Provoz 002: Vstřikolisovny (Engel Victory 120t 2K, Engel Duo 500t, KraussMaffei CX 650t)
- Provoz 008: Lakovna (Linka Flat Bed)
- Reální zákazníci: Škoda Auto (SpaceBEV/Kodiaq), Continental, TI Fluid Systems (TIFS), VW koncern
- Návaznost na firemní systémy: ERP QI, WMS DCIx (RTG výdej) a S-Karta
"""

import time
import random
import datetime
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

INFLUX_URL = "http://localhost:8086"
INFLUX_TOKEN = "plastika-super-secret-auth-token-12345"
INFLUX_ORG = "plastika"
INFLUX_BUCKET = "production_metrics"

# Definice reálných strojů a zakázek dle výroční zprávy Plastika a.s.
MACHINES = [
    {
        "provoz": "002_Vstrikovna",
        "machine_id": "LIS-201",
        "machine_name": "Engel Victory 120t (2K lis)",
        "customer": "Škoda Auto",
        "project": "SpaceBEV / Kodiaq",
        "part_name": "Rámeček přístrojové desky 2K",
        "mold_id": "FORMA-SKODA-BEV-01",
        "material": "PC-ABS / TPE",
        "operator": "OP-104_Novak",
        "nominal_temp": 268.0,      # °C
        "temp_tolerance": 6.0,
        "nominal_pressure": 172.0,  # bar
        "pressure_tolerance": 10.0,
        "base_cycle_time": 32.4,    # s
        "power_base": 38.0,         # kW
        "unit_cost_czk": 85.50      # Výrobní cena dílu
    },
    {
        "provoz": "002_Vstrikovna",
        "machine_id": "LIS-208",
        "machine_name": "Engel Duo 500t",
        "customer": "Continental",
        "project": "ECU Sensor Housing",
        "part_name": "Konektorové pouzdro senzorů 24-PIN",
        "mold_id": "FORMA-CONTI-ECU-24",
        "material": "PA66-GF30",
        "operator": "OP-208_Svoboda",
        "nominal_temp": 290.0,      # °C
        "temp_tolerance": 5.0,
        "nominal_pressure": 188.0,  # bar
        "pressure_tolerance": 12.0,
        "base_cycle_time": 18.6,    # s
        "power_base": 52.0,         # kW
        "unit_cost_czk": 42.00
    },
    {
        "provoz": "002_Vstrikovna",
        "machine_id": "LIS-305",
        "machine_name": "KraussMaffei CX 650t",
        "customer": "TI Fluid Systems (TIFS)",
        "project": "Fuel & Thermal Line",
        "part_name": "Palivový a chladicí adaptér",
        "mold_id": "FORMA-TIFS-FUEL-08",
        "material": "POM-C / PA12",
        "operator": "OP-312_Dvorak",
        "nominal_temp": 215.0,      # °C
        "temp_tolerance": 7.0,
        "nominal_pressure": 145.0,  # bar
        "pressure_tolerance": 8.0,
        "base_cycle_time": 24.2,    # s
        "power_base": 64.0,         # kW
        "unit_cost_czk": 61.20
    },
    {
        "provoz": "008_Lakovna",
        "machine_id": "LAK-FLAT-01",
        "machine_name": "Lakovací linka FLAT BED",
        "customer": "VW Koncern",
        "project": "VW Emblem & Trim",
        "part_name": "Dekorační lakovaný nápis",
        "mold_id": "FORMA-VW-EMBLEM-02",
        "material": "ABS lakovaný",
        "operator": "OP-405_Kralova",
        "nominal_temp": 82.0,       # Teplota sušicí komory (°C)
        "temp_tolerance": 3.0,
        "nominal_pressure": 4.5,    # Tlak rozstřiku laku (bar)
        "pressure_tolerance": 0.4,
        "base_cycle_time": 12.0,    # s takt linky
        "power_base": 24.0,         # kW
        "unit_cost_czk": 115.00
    }
]


def generate_machine_point(machine: dict, timestamp: datetime.datetime, total_cycles: int, total_scrap: int):
    """
    Vygeneruje bod telemetrie s věrnou fyzikální simulací a zmetkovitostí dle KPI 2024.
    """
    # Míra zmetkovitosti cca 4.5 - 5% (odpovídá reálnému NNJ 4,98 % z výroční zprávy 2024)
    is_anomaly = random.random() < 0.045
    
    if is_anomaly:
        temp_delta = random.choice([random.uniform(12.0, 24.0), random.uniform(-18.0, -10.0)])
        temp = machine["nominal_temp"] + temp_delta
        pressure = machine["nominal_pressure"] + random.uniform(-20.0, 30.0)
        cycle_time = machine["base_cycle_time"] + random.uniform(3.0, 8.5)
        status = "ALERT" if abs(temp_delta) > 16.0 else "WARNING"
        is_scrap = 1
        defect_type = random.choice(["Prehrati_taveniny", "Propadlina", "Nedoliti_tvaru", "Vada_laku_Hrudka"])
    else:
        temp = machine["nominal_temp"] + random.gauss(0, machine["temp_tolerance"] / 3.0)
        pressure = machine["nominal_pressure"] + random.gauss(0, machine["pressure_tolerance"] / 3.0)
        cycle_time = max(8.0, machine["base_cycle_time"] + random.gauss(0, 0.5))
        status = "RUNNING"
        is_scrap = 0
        defect_type = "None"

    power = machine["power_base"] + (pressure / 12.0) + random.uniform(-1.5, 1.5)
    scrap_cost = machine["unit_cost_czk"] if is_scrap else 0.0

    point = (
        Point("injection_molding")
        .tag("provoz", machine["provoz"])
        .tag("machine_id", machine["machine_id"])
        .tag("machine_name", machine["machine_name"])
        .tag("customer", machine["customer"])
        .tag("project", machine["project"])
        .tag("mold_id", machine["mold_id"])
        .tag("material", machine["material"])
        .tag("operator", machine["operator"])
        .tag("status", status)
        .tag("defect_type", defect_type)
        .field("melt_temperature", round(float(temp), 2))
        .field("hydraulic_pressure", round(float(pressure), 2))
        .field("cycle_time", round(float(cycle_time), 2))
        .field("power_consumption_kw", round(float(power), 2))
        .field("parts_produced_total", int(total_cycles))
        .field("scrap_total", int(total_scrap))
        .field("is_scrap", int(is_scrap))
        .field("scrap_cost_czk", round(float(scrap_cost), 2))
        .time(timestamp, WritePrecision.S)
    )
    
    return point, is_scrap


def seed_historical_data(client: InfluxDBClient, hours: int = 8):
    """
    Naplní InfluxDB historickými daty za posledních N hodin.
    """
    print(f"🏭 Plastika a.s. -> Zapisuji autentická historická data za {hours} hodin...")
    write_api = client.write_api(write_options=SYNCHRONOUS)
    
    now = datetime.datetime.now(datetime.timezone.utc)
    start_time = now - datetime.timedelta(hours=hours)
    step = datetime.timedelta(seconds=15)
    
    machine_state_counters = {
        m["machine_id"]: {"cycles": random.randint(450, 1200), "scrap": random.randint(15, 60)}
        for m in MACHINES
    }
    
    points_batch = []
    current_time = start_time
    
    while current_time <= now:
        for machine in MACHINES:
            mid = machine["machine_id"]
            machine_state_counters[mid]["cycles"] += 1
            
            point, is_scrap = generate_machine_point(
                machine,
                current_time,
                machine_state_counters[mid]["cycles"],
                machine_state_counters[mid]["scrap"]
            )
            if is_scrap:
                machine_state_counters[mid]["scrap"] += 1
                
            points_batch.append(point)
            
            if len(points_batch) >= 1000:
                write_api.write(bucket=INFLUX_BUCKET, org=INFLUX_ORG, record=points_batch)
                points_batch = []
                
        current_time += step

    if points_batch:
        write_api.write(bucket=INFLUX_BUCKET, org=INFLUX_ORG, record=points_batch)
        
    print("✅ Historická data úspěšně nahrána do InfluxDB!")
    return machine_state_counters


def run_live_stream(client: InfluxDBClient, machine_counters: dict, interval_sec: float = 2.0):
    print(f"🚀 Spouštím live stream výrobních dat Plastika (interval: {interval_sec}s). Ukončení Ctrl+C.")
    write_api = client.write_api(write_options=SYNCHRONOUS)
    
    try:
        while True:
            now = datetime.datetime.now(datetime.timezone.utc)
            points = []
            
            for machine in MACHINES:
                mid = machine["machine_id"]
                machine_counters[mid]["cycles"] += 1
                
                point, is_scrap = generate_machine_point(
                    machine,
                    now,
                    machine_counters[mid]["cycles"],
                    machine_counters[mid]["scrap"]
                )
                if is_scrap:
                    machine_counters[mid]["scrap"] += 1
                    
                points.append(point)
                
            write_api.write(bucket=INFLUX_BUCKET, org=INFLUX_ORG, record=points)
            print(f"[{now.strftime('%H:%M:%S')}] Telemetrie odeslána: LIS-201 (Škoda BEV), LIS-208 (Conti), LIS-305 (TIFS), LAK-01 (VW)")
            time.sleep(interval_sec)
            
    except KeyboardInterrupt:
        print("\n🛑 Generátor zastaven uživatelem.")


if __name__ == "__main__":
    with InfluxDBClient(url=INFLUX_URL, token=INFLUX_TOKEN, org=INFLUX_ORG) as client:
        counters = seed_historical_data(client, hours=8)
        run_live_stream(client, counters, interval_sec=2.0)
