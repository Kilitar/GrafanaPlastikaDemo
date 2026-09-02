@echo off
chcp 65001 > nul
echo ========================================================
echo   PLASTIKA a.s. - Start prostredi pro pohovor
echo ========================================================
echo.

echo [1/3] Spoustim Docker kontejnery (InfluxDB + Grafana)...
docker compose up -d

echo.
echo [2/3] Generuji cerstva vyrobni data az do aktualni minuty...
call .venv\Scripts\python -c "import data_generator, influxdb_client; c=influxdb_client.InfluxDBClient(url=data_generator.INFLUX_URL, token=data_generator.INFLUX_TOKEN, org=data_generator.INFLUX_ORG); data_generator.seed_historical_data(c, hours=8)"

echo.
echo [3/3] Oteviram Grafanu v prohlizeci...
start http://localhost:3000

echo.
echo ========================================================
echo   HOTOVO! Dashboard je pripraven na: http://localhost:3000
echo   (Prihlaseni: admin / admin)
echo.
echo   Spoustim zivy proud telemetrie na pozadi...
echo   (Toto okno muzete nechat bezet nebo minimalizovat)
echo ========================================================
echo.

call .venv\Scripts\python -u data_generator.py
