--Top Clientes
-- Pregunta
-- ¿Quiénes son los clientes más valiosos?
-- Objetivo
-- Programas de fidelización.

CREATE VIEW vw_TopClientes
AS
SELECT
    dc.NombreCliente,
    SUM(fv.Total) AS TotalComprado
FROM FactVenta fv
INNER JOIN DimCliente dc
    ON fv.IdDimCliente = dc.IdDimCliente
GROUP BY
    dc.NombreCliente;