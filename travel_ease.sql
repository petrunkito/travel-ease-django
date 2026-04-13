--la tabla Usuario hace referencia a la tabla al usuario que provee django


-- CREATE TABLE Usuario (
--     Id INT IDENTITY PRIMARY KEY,
--     Nombre VARCHAR(100) NOT NULL,
--     Correo VARCHAR(100) NOT NULL UNIQUE,
--     Contrasena varchar(255),
--     FechaRegistro DATETIME DEFAULT GETDATE(),
--     Activo BIT DEFAULT 1
-- );

-- CREATE TABLE Rol (
--     Id INT IDENTITY PRIMARY KEY,
--     Nombre VARCHAR(20) NOT NULL,
--     Codigo VARCHAR(20) NOT NULL UNIQUE
-- );

-- INSERT INTO Roles (Nombre, Codigo) VALUES
-- ('Asistente', 'ASISTENTE'),
-- ('Admin', 'ADMIN');

-- CREATE TABLE UsuarioRol (
--     Id INT IDENTITY PRIMARY KEY,
--     IdUsuario INT NOT NULL, 
--     IdRol INT NOT NULL,
--     FOREIGN KEY (IdUsuario) REFERENCES Usuario(Id),
--     FOREIGN KEY (IdRol) REFERENCES Roles(Id),
--     UNIQUE (IdUsuario, IdRol)
);

CREATE TABLE Departamento (
    Id INT IDENTITY PRIMARY KEY,
    Nombre NVARCHAR(100) NOT NULL,
    Codigo VARCHAR(20) NOT NULL UNIQUE
);

INSERT INTO Departamento (Nombre, Codigo) VALUES
('Managua', 'MAN'),
('León', 'LEO'),
('Chinandega', 'CHI'),
('Masaya', 'MAS'),
('Granada', 'GRA'),
('Carazo', 'CAR'),
('Rivas', 'RIV'),
('Nueva Segovia', 'NSE'),
('Madriz', 'MAD'),
('Estelí', 'EST'),
('Jinotega', 'JIN'),
('Matagalpa', 'MAT'),
('Boaco', 'BOA'),
('Chontales', 'CHO'),
('Río San Juan', 'RSJ'),
('Región Autónoma de la Costa Caribe Norte', 'RACCN'),
('Región Autónoma de la Costa Caribe Sur', 'RACCS');

CREATE TABLE Municipio (
    Id INT IDENTITY PRIMARY KEY,
    IdDepartamento INT,
    Nombre NVARCHAR(100),
    Codigo VARCHAR(20) NOT NULL UNIQUE,
    FOREIGN KEY (IdDepartamento) REFERENCES Departamento(id)
);

INSERT INTO Municipio (IdDepartamento, Nombre, Codigo) VALUES
(1, 'Managua', 'MAN-01'),
(1, 'Tipitapa', 'MAN-02'),
(1, 'Ciudad Sandino', 'MAN-03'),
(1, 'San Rafael del Sur', 'MAN-04'),
(1, 'Ticuantepe', 'MAN-05'),
(1, 'El Crucero', 'MAN-06'),
(1, 'Mateare', 'MAN-07'),
(1, 'San Francisco Libre', 'MAN-08'),
(1, 'Villa El Carmen', 'MAN-09');
INSERT INTO Municipio (IdDepartamento, Nombre, Codigo) VALUES
(2, 'León', 'LEO-01'),
(2, 'La Paz Centro', 'LEO-02'),
(2, 'Nagarote', 'LEO-03'),
(2, 'Telica', 'LEO-04'),
(2, 'Quezalguaque', 'LEO-05'),
(2, 'El Sauce', 'LEO-06'),
(2, 'Achuapa', 'LEO-07'),
(2, 'Santa Rosa del Peñón', 'LEO-08');
INSERT INTO Municipio (IdDepartamento, Nombre, Codigo) VALUES
(3, 'Chinandega', 'CHI-01'),
(3, 'El Viejo', 'CHI-02'),
(3, 'Corinto', 'CHI-03'),
(3, 'Chichigalpa', 'CHI-04'),
(3, 'Posoltega', 'CHI-05'),
(3, 'Puerto Morazán', 'CHI-06'),
(3, 'Somotillo', 'CHI-07'),
(3, 'Villanueva', 'CHI-08'),
(3, 'Cinco Pinos', 'CHI-09'),
(3, 'San Pedro del Norte', 'CHI-10'),
(3, 'San Francisco del Norte', 'CHI-11'),
(3, 'El Realejo', 'CHI-12'),
(3, 'Santo Tomás del Norte', 'CHI-13');
INSERT INTO Municipio (IdDepartamento, Nombre, Codigo) VALUES
(4, 'Masaya', 'MAS-01'),
(4, 'Nindirí', 'MAS-02'),
(4, 'Tisma', 'MAS-03'),
(4, 'Masatepe', 'MAS-04'),
(4, 'Nandasmo', 'MAS-05'),
(4, 'Catarina', 'MAS-06'),
(4, 'San Juan de Oriente', 'MAS-07'),
(4, 'Niquinohomo', 'MAS-08'),
(4, 'La Concepción', 'MAS-09');
INSERT INTO Municipio (IdDepartamento, Nombre, Codigo) VALUES
(5, 'Granada', 'GRA-01'),
(5, 'Diriomo', 'GRA-02'),
(5, 'Diriá', 'GRA-03'),
(5, 'Nandaime', 'GRA-04');
INSERT INTO Municipio (IdDepartamento, Nombre, Codigo) VALUES
(6, 'Jinotepe', 'CAR-01'),
(6, 'Dolores', 'CAR-02'),
(6, 'Diriamba', 'CAR-03'),
(6, 'San Marcos', 'CAR-04'),
(6, 'Santa Teresa', 'CAR-05'),
(6, 'La Paz de Carazo', 'CAR-06'),
(6, 'El Rosario', 'CAR-07'),
(6, 'La Conquista', 'CAR-08');
INSERT INTO Municipio (IdDepartamento, Nombre, Codigo) VALUES
(7, 'Rivas', 'RIV-01'),
(7, 'San Jorge', 'RIV-02'),
(7, 'San Juan del Sur', 'RIV-03'),
(7, 'Cárdenas', 'RIV-04'),
(7, 'Potosí', 'RIV-05'),
(7, 'Belén', 'RIV-06'),
(7, 'Buenos Aires', 'RIV-07'),
(7, 'Tola', 'RIV-08'),
(7, 'Moyogalpa', 'RIV-09'),
(7, 'Altagracia', 'RIV-10');




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
    FOREIGN KEY (IdUsuarioRegistro) REFERENCES auth_user(id)--el auth_user(id) es el auth_user de django indicando quien creo este registro
);

CREATE TABLE Vuelo (
    Id INT IDENTITY PRIMARY KEY,
    Aerolinea VARCHAR(100) NOT NULL,
    Origen VARCHAR(100) NOT NULL,
    Destino VARCHAR(100) NOT NULL,
    FechaSalida DATETIME NOT NULL,
    FechaLlegada DATETIME NOT NULL,
    Activo BIT DEFAULT 1

);

CREATE TABLE Hotel (
    Id INT IDENTITY PRIMARY KEY,
    Nombre VARCHAR(100) NOT NULL,
    Ciudad VARCHAR(100) NOT NULL,
    Estrellas INT,
    Categoria VARCHAR(50),
    Activo BIT DEFAULT 1

);

CREATE TABLE TipoTransporte (
    Id INT IDENTITY PRIMARY KEY,
    Nombre VARCHAR(50),
    Codigo VARCHAR(20) NOT NULL UNIQUE,
    Activo BIT DEFAULT 1
);

CREATE TABLE Transporte (
    Id INT IDENTITY PRIMARY KEY,
    IdTipoTransporte INT NOT NULL,
    Origen VARCHAR(100) NOT NULL,
    Destino VARCHAR(100) NOT NULL,
    Activo BIT DEFAULT 1,
    FOREIGN KEY (IdTipoTransporte) REFERENCES TipoTransporte(Id),
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
    FOREIGN KEY (IdUsuario) REFERENCES auth_user(Id)--el auth_user(id) es el auth_user de django indicando quien creo este registro
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
    Nombre VARCHAR(50),
    Codigo VARCHAR(20) NOT NULL UNIQUE
);

INSERT INTO EstadoReserva (Nombre, Codigo) VALUES
('Pendiente', 'PEND'),
('Pagado', 'PAG'),
('Cancelado', 'CANC');

CREATE TABLE Reserva (
    Id INT IDENTITY PRIMARY KEY,
    IdCliente INT,
    IdUsuarioVendedor INT,
    Fecha DATETIME DEFAULT GETDATE(),
    Total DECIMAL(10,2),
    Activo BIT DEFAULT 1,
    FOREIGN KEY (IdCliente) REFERENCES Cliente(Id),
    FOREIGN KEY (IdUsuarioVendedor) REFERENCES auth_user(Id)--el auth_user(id) es el auth_user de django indicando quien creo este registro
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

CREATE TABLE TipoPago (
    Id INT IDENTITY PRIMARY KEY,
    Nombre VARCHAR(50),
    Codigo VARCHAR(20) NOT NULL UNIQUE
);

INSERT INTO TipoPago (Nombre, Codigo) VALUES
('EFECTIVO', 'EFEC');


CREATE TABLE Pago (
    Id INT IDENTITY PRIMARY KEY,
    IdReserva INT,
    IdTipoPago INT,
    Monto DECIMAL(10,2),
    Estado VARCHAR(50),
    FechaPago DATETIME DEFAULT GETDATE(),
    FOREIGN KEY (IdReserva) REFERENCES Reserva(Id),
    FOREIGN KEY (IdTipoPago) REFERENCES TipoPago(Id)
);

CREATE TABLE Factura (
    Id INT IDENTITY PRIMARY KEY,
    IdReserva INT,
    NumeroFactura VARCHAR(50),
    FechaEmision DATETIME,
    Total DECIMAL(10,2),
    FOREIGN KEY (IdReserva) REFERENCES Reserva(Id)
);



