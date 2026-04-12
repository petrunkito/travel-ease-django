CREATE TABLE Usuario (
    Id INT IDENTITY PRIMARY KEY,
    Nombre VARCHAR(100) NOT NULL,
    Correo VARCHAR(100) NOT NULL UNIQUE,
    Contrasena varchar(255),
    FechaRegistro DATETIME DEFAULT GETDATE(),
    Activo BIT DEFAULT 1
);

CREATE TABLE Rol (
    Id INT IDENTITY PRIMARY KEY,
    Nombre VARCHAR(20) NOT NULL,
    Codigo VARCHAR(20) NOT NULL UNIQUE
);

INSERT INTO Roles (Nombre, Codigo) VALUES
('Asistente', 'ASISTENTE'),
('Admin', 'ADMIN');

CREATE TABLE UsuarioRol (
    Id INT IDENTITY PRIMARY KEY,
    IdUsuario INT NOT NULL, 
    IdRol INT NOT NULL,
    FOREIGN KEY (IdUsuario) REFERENCES Usuario(Id),
    FOREIGN KEY (IdRol) REFERENCES Roles(Id),
    UNIQUE (IdUsuario, IdRol)
);

CREATE TABLE Departamento (
    Id INT IDENTITY PRIMARY KEY,
    Nombre NVARCHAR(100) NOT NULL
);

CREATE TABLE Municipio (
    Id INT IDENTITY PRIMARY KEY,
    IdDepartamento INT,
    Nombre NVARCHAR(100),
    FOREIGN KEY (idDepartamento) REFERENCES Departamento(id)
);

CREATE TABLE Cliente (
    Id INT IDENTITY PRIMARY KEY,
    IdMunicipio INT NOT NULL,
    IdUsuarioRegistro INT NOT NULL,
    Nombre VARCHAR(100),
    Cedula VARCHAR(20),
    Direccion VARCHAR(250),
    Numero VARCHAR(20),
    FechaRegistro DATETIME DEFAULT GETDATE(),
    Activo BIT DEFAULT 1,
    FOREIGN KEY (IdMunicipio) REFERENCES Municipio(Id),
    FOREIGN KEY (IdUsuarioRegistro) REFERENCES Usuario(Id)
);

CREATE TABLE Vuelo (
    Id INT IDENTITY PRIMARY KEY,
    Aerolinea VARCHAR(100) NOT NULL,
    Origen VARCHAR(100) NOT NULL,
    Destino VARCHAR(100) NOT NULL,
    FechaSalida DATETIME NOT NULL,
    FechaLlegada DATETIME NOT NULL
);

CREATE TABLE Hotel (
    Id INT IDENTITY PRIMARY KEY,
    Nombre VARCHAR(100) NOT NULL,
    Ciudad VARCHAR(100) NOT NULL,
    Estrellas INT,
    Categoria VARCHAR(50)
);

CREATE TABLE TipoTransporte (
    Id INT IDENTITY PRIMARY KEY,
    Nombre VARCHAR(50)
);

CREATE TABLE Transporte (
    Id INT IDENTITY PRIMARY KEY,
    IdTipoTransporte INT NOT NULL,
    Origen VARCHAR(100) NOT NULL,
    Destino VARCHAR(100) NOT NULL,
    FOREIGN KEY (IdTipoTransporte) REFERENCES TipoTransporte(Id)
);

CREATE TABLE HistorialPrecio (
    Id INT IDENTITY PRIMARY KEY,
    TipoServicio VARCHAR(50), -- Vuelo, Hotel, Transporte
    IdServicio INT,
    Precio DECIMAL(10,2),
    FechaInicio DATETIME,
    FechaFin DATETIME
);

CREATE TABLE PaqueteTuristico (
    Id INT IDENTITY PRIMARY KEY,
    IdUsuario INT,
    Nombre VARCHAR(100),
    Descripcion VARCHAR(250),
    FechaCreacion DATETIME DEFAULT GETDATE(),
    Activo BIT DEFAULT 1,
    FOREIGN KEY (IdUsuario) REFERENCES Usuario(Id)
);


CREATE TABLE DetallePaquete (
    Id INT IDENTITY PRIMARY KEY,
    IdPaquete INT,
    TipoServicio VARCHAR(50), -- Vuelo, Hotel, Transporte
    IdServicio INT,
    Cantidad INT,
    PrecioUnitario DECIMAL(10,2),
    Total DECIMAL(10,2),
    FOREIGN KEY (IdPaquete) REFERENCES PaqueteTuristico(Id)
);

CREATE TABLE EstadoReserva (
    Id INT IDENTITY PRIMARY KEY,
    Nombre VARCHAR(50)
);

CREATE TABLE Reserva (
    Id INT IDENTITY PRIMARY KEY,
    IdCliente INT,
    IdUsuarioVendedor INT,
    Fecha DATETIME DEFAULT GETDATE(),
    Total DECIMAL(10,2),
    Activo BIT DEFAULT 1,
    FOREIGN KEY (IdCliente) REFERENCES Cliente(Id),
    FOREIGN KEY (IdUsuarioVendedor) REFERENCES Usuario(Id)
);

CREATE TABLE DetalleReserva (
    Id INT IDENTITY PRIMARY KEY,
    IdReserva INT ,
    IdPaquete INT,
    TipoServicio VARCHAR(50),
    IdServicio INT,
    Cantidad INT,
    PrecioUnitario DECIMAL(10,2),
    Total DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (IdReserva) REFERENCES Reserva(Id),
    FOREIGN KEY (IdPaquete) REFERENCES PaqueteTuristico(Id)
);

CREATE TABLE HistorialEstadoReserva (
    Id INT IDENTITY PRIMARY KEY,
    IdReserva INT NOT NULL,
    IdEstado INT NOT NULL,
    Fecha DATETIME DEFAULT GETDATE(),
    FOREIGN KEY (IdReserva) REFERENCES Reserva(Id),
    FOREIGN KEY (IdEstado) REFERENCES EstadoReserva(Id)
);

CREATE TABLE Pago (
    Id INT IDENTITY PRIMARY KEY,
    IdReserva INT,
    Monto DECIMAL(10,2),
    Estado VARCHAR(50),
    FechaPago DATETIME DEFAULT GETDATE(),
    FOREIGN KEY (IdReserva) REFERENCES Reserva(Id)
);

CREATE TABLE Factura (
    Id INT IDENTITY PRIMARY KEY,
    IdReserva INT,
    NumeroFactura VARCHAR(50),
    FechaEmision DATETIME,
    Total DECIMAL(10,2),
    FOREIGN KEY (IdReserva) REFERENCES Reserva(Id)
);



