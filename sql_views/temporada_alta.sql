-- Temporada Alta
-- Pregunta
-- ¿Cuáles son los meses con mayores ingresos?
-- Objetivo
-- Planificar promociones.

CREATE VIEW vw_TemporadaAlta
AS
SELECT
    dt.MesNombre,
    SUM(fv.Total) AS TotalVentas
FROM FactVenta fv
INNER JOIN DimTiempo dt
    ON fv.IdDimTiempo = dt.IdDimTiempo
GROUP BY
    dt.MesNombre,
    dt.MesNumero;