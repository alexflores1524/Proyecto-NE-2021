
/* TABLA Prestamos*/
CREATE TABLE `gespres_flask`.`prestamos`(
    `idPrestamo` INT NOT NULL AUTO_INCREMENT,
    `idCliente` INT NOT NULL,
    `cantidad` DOUBLE NOT NULL,
    `numero_plazos` INT NOT NULL,
    `fecha_prestamo` TIMESTAMP NOT NULL,
    `abono` DOUBLE NOT NULL,
    `restante` DOUBLE NOT NULL,
    `status` BOOLEAN NOT NULL DEFAULT TRUE,
    `is_active` BOOLEAN NOT NULL DEFAULT TRUE,
    `create_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `update_at` TIMESTAMP ON UPDATE CURRENT_TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY(`idPrestamo`)
) ENGINE = INNODB;

/* TABLA Clientes*/
CREATE TABLE `gespres_flask`.`clientes`(
    `idCliente` INT NOT NULL AUTO_INCREMENT,
    `nombre` VARCHAR(50) NOT NULL,
    `apellido` VARCHAR(50) NOT NULL,
    `fecha_nacimiento` TIMESTAMP NOT NULL,
    `telefono` BIGINT NOT NULL,
    `email` VARCHAR(50) NOT NULL,
    `is_active` BOOLEAN NOT NULL DEFAULT TRUE,
    `create_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `update_at` TIMESTAMP ON UPDATE CURRENT_TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY(`idCliente`)
) ENGINE = INNODB;

/* TABLA USUARIOS*/
CREATE TABLE `gespres_flask`.`usuarios`(
    `idUser` INT NOT NULL AUTO_INCREMENT,
    `usuario` VARCHAR(50) NOT NULL,
    `password` VARCHAR(50) NOT NULL,
    `is_active` BOOLEAN NOT NULL DEFAULT TRUE,
    `create_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `update_at` TIMESTAMP ON UPDATE CURRENT_TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY(`idUser`)
) ENGINE = INNODB;

/* TABLA Plazos*/
CREATE TABLE `gespres_flask`.`plazos`(
    `idPlazo` INT NOT NULL AUTO_INCREMENT,
    `idPrestamo` INT NOT NULL,
    `subtotal` DOUBLE NOT NULL,
    `fecha_pago` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `is_active` BOOLEAN NOT NULL DEFAULT TRUE,
    `create_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `update_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY(`idPlazo`)
) ENGINE = INNODB;

/* TABLA Cobros*/
CREATE TABLE `gespres_flask`.`cobros`(
    `idCobro` INT NOT NULL AUTO_INCREMENT,
    `idPrestamo` INT NOT NULL,
    `idPlazo` INT NOT NULL,
    `cantidad` DOUBLE NOT NULL,
    `fecha_cobro` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `is_active` BOOLEAN NOT NULL DEFAULT TRUE,
    `create_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `update_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY(`idCobro`)
) ENGINE = INNODB;

/* 
Ejemplo INSERT
INSERT INTO `usuarios` (`idUser`, `usuario`, `password`, `is_active`, `create_at`, `update_at`) VALUES (NULL, 'juan@git.com', '12345', '1', current_timestamp(), current_timestamp());

INSERT INTO `clientes` (`idCliente`, `nombre`, `apellido`, `fecha_nacimiento`, `telefono`, `email`, `is_active`, `create_at`, `update_at`) VALUES (NULL, 'Raul', 'Ramirez', '1984-04-07', '3300112244', 'hugo@git.com', '1', current_timestamp(), current_timestamp());

SELECT 
	clientes.nombre,
    clientes.apellido,
    prestamos.abono,
    prestamos.restante
FROM prestamos
INNER JOIN clientes on clientes.idCliente = prestamos.idCliente
WHERE prestamos.idPrestamo = 1

*/
