--Ingresos por Destino
-- Pregunta
-- ¿Qué destinos generan más dinero?
-- Objetivo
-- Saber dónde enfocar campañas de marketing.

CREATE VIEW vw_IngresosPorDestino
AS
SELECT top 10
    dd.Pais,
    dd.Ciudad,
    SUM(fv.Total) AS Ingresos
FROM FactVenta fv
INNER JOIN DimDestino dd
    ON fv.IdDimDestino = dd.IdDimDestino
GROUP BY
    dd.Pais,
    dd.Ciudad order by ingresos desc;