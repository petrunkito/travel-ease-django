-- Paquetes Más Vendidos
-- Pregunta
-- ¿Qué paquetes turísticos tienen más demanda?
-- Objetivo
-- Identificar productos estrella.

CREATE VIEW 
AS
SELECT top 20
    dp.NombrePaquete,
    SUM(fv.Cantidad) AS TotalReservas
FROM FactVenta fv
INNER JOIN DimPaquete dp
    ON fv.IdDimPaquete = dp.IdDimPaquete
GROUP BY
    dp.NombrePaquete order by TotalReservas desc;