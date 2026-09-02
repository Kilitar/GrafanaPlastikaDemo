"""
Ukázky dotazů v jazyce FLUX pro InfluxDB (Modul 3 & 5)
Dotazování výrobních dat z InfluxDB a konverze do pandas DataFrame.
"""

from influxdb_client import InfluxDBClient
import pandas as pd

INFLUX_URL = "http://localhost:8086"
INFLUX_TOKEN = "plastika-super-secret-auth-token-12345"
INFLUX_ORG = "plastika"
INFLUX_BUCKET = "production_metrics"


def get_influx_client():
    return InfluxDBClient(url=INFLUX_URL, token=INFLUX_TOKEN, org=INFLUX_ORG)


def query_average_metrics_last_hour():
    """
    1. FLUX DOTAZ: Průměrné hodnoty teplot a tlaků za poslední hodinu podle strojů.
    """
    flux_query = f'''
    from(bucket: "{INFLUX_BUCKET}")
      |> range(start: -1h)
      |> filter(fn: (r) => r._measurement == "injection_molding")
      |> filter(fn: (r) => r._field == "melt_temperature" or r._field == "hydraulic_pressure")
      |> mean()
    '''
    with get_influx_client() as client:
        query_api = client.query_api()
        tables = query_api.query(flux_query)
        
        print("\n📊 --- PRŮMĚRNÉ METRIKY ZA POSLEDNÍ HODINU ---")
        for table in tables:
            for record in table.records:
                machine = record.values.get("machine_id")
                field = record.get_field()
                val = record.get_value()
                unit = "°C" if "temp" in field else "bar"
                print(f"Stroj: {machine:<8} | Metrika: {field:<20} | Hodnota: {val:6.2f} {unit}")


def query_anomalies_and_scrap():
    """
    2. FLUX DOTAZ: Detekce anomálií a zmetkových cyklů (kde is_scrap == 1).
    """
    flux_query = f'''
    from(bucket: "{INFLUX_BUCKET}")
      |> range(start: -6h)
      |> filter(fn: (r) => r._measurement == "injection_molding")
      |> filter(fn: (r) => r._field == "is_scrap" and r._value == 1)
      |> count()
    '''
    with get_influx_client() as client:
        query_api = client.query_api()
        tables = query_api.query(flux_query)
        
        print("\n⚠️ --- POČET ZMETKOVÝCH CYKLŮ ZA POSLEDNÍCH 6 HODIN ---")
        for table in tables:
            for record in table.records:
                machine = record.values.get("machine_id")
                scrap_count = record.get_value()
                print(f"Stroj: {machine:<8} | Detekováno neshodných kusů (zmetků): {scrap_count}")


def query_to_dataframe(start_range: str = "-2h") -> pd.DataFrame:
    """
    3. PANDAS INTEGRACE: Načtení dat přímo do Pandas DataFrame pro analytiku.
    """
    flux_query = f'''
    from(bucket: "{INFLUX_BUCKET}")
      |> range(start: {start_range})
      |> filter(fn: (r) => r._measurement == "injection_molding")
      |> pivot(rowKey: ["_time", "machine_id"], columnKey: ["_field"], valueColumn: "_value")
      |> keep(columns: ["_time", "machine_id", "machine_name", "material", "melt_temperature", "hydraulic_pressure", "cycle_time", "power_consumption_kw", "is_scrap"])
    '''
    with get_influx_client() as client:
        query_api = client.query_api()
        df = query_api.query_data_frame(flux_query)
        return df


if __name__ == "__main__":
    query_average_metrics_last_hour()
    query_anomalies_and_scrap()
    
    print("\n🐼 --- NAČTENÍ DAT DO PANDAS DATAFRAME ---")
    df = query_to_dataframe(start_range="-1h")
    if isinstance(df, list):
        df = pd.concat(df)
    print(f"Rozměry DataFrame: {df.shape}")
    print(df[['_time', 'machine_id', 'melt_temperature', 'hydraulic_pressure', 'cycle_time', 'is_scrap']].head(10))
