CREATE TABLE FactVentas (
    Id INT IDENTITY PRIMARY KEY,

    IdFecha INT NOT NULL,
    IdCliente INT NOT NULL,
    IdUsuario INT NOT NULL,
    IdPaquete INT NOT NULL,
    IdDestino INT NOT NULL,

    TipoServicio VARCHAR(50) NOT NULL,

    Cantidad INT NOT NULL,
    PrecioUnitario DECIMAL(10,2) NOT NULL,
    Total DECIMAL(12,2) NOT NULL,

    -- Relaciones (opcional pero recomendado)
    FOREIGN KEY (IdFecha) REFERENCES DimFecha(IdFecha),
    FOREIGN KEY (IdCliente) REFERENCES DimCliente(IdCliente),
    FOREIGN KEY (IdUsuario) REFERENCES DimUsuario(IdUsuario),
    FOREIGN KEY (IdPaquete) REFERENCES DimPaquete(IdPaquete),
    FOREIGN KEY (IdDestino) REFERENCES DimDestino(IdDestino)
);

CREATE TABLE DimFecha (
    IdFecha INT PRIMARY KEY, -- formato: YYYYMMDD

    Fecha DATE NOT NULL,
    Anio INT NOT NULL,
    Mes INT NOT NULL,
    NombreMes VARCHAR(20) NOT NULL,
    Trimestre INT NOT NULL,
    Dia INT NOT NULL,
    DiaSemana VARCHAR(20) NOT NULL
);

CREATE TABLE DimCliente (
    IdCliente INT PRIMARY KEY,

    Nombre VARCHAR(100),
    Municipio VARCHAR(100),
    Departamento VARCHAR(100)
);


CREATE TABLE DimUsuario (
    IdUsuario INT PRIMARY KEY,

    Nombre VARCHAR(100),
    Correo VARCHAR(100),
    Rol VARCHAR(50)
);

CREATE TABLE DimPaquete (
    IdPaquete INT PRIMARY KEY,

    Nombre VARCHAR(100),
    Descripcion VARCHAR(250)
);

CREATE TABLE DimDestino (
    IdDestino INT PRIMARY KEY,

    Ciudad VARCHAR(100),
    Pais VARCHAR(100)
);