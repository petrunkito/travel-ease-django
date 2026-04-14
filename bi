¿Qué destinos generan mayores ingresos y cuál es el comportamiento de ventas 
según el tipo de servicio (vuelo, hotel, transporte), el tiempo y el vendedor?

¿Dónde gana más dinero la empresa?
¿Qué tipo de servicio aporta más?
¿Qué vendedores rinden mejor?
¿Cómo cambian las ventas en el tiempo?

FactVentas
-----------
Id (PK)
IdFecha
IdCliente -- el cliente
IdUsuario -- el vendedor
IdPaquete
IdDestino
TipoServicio
Cantidad
PrecioUnitario
Total


DimFecha
-----------
IdFecha (PK)
Fecha
Año
Mes
NombreMes
Trimestre
Dia
DiaSemana


DimCliente
-----------
IdCliente (PK)
Nombre
Municipio
Departamento


DimUsuario
-----------
IdUsuario (PK)
Nombre
Correo
Rol


DimPaquete
-----------
IdPaquete (PK)
Nombre
Descripcion


DimDestino
-----------
IdDestino (PK)
Ciudad
Pais


                DimFecha
                   |
DimCliente — FactVentas — DimUsuario
                   |
               DimPaquete
                   |
               DimDestino
                   |
               DimServicio

