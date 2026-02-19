-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 14-02-2026 a las 17:43:27
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `appcoches`
--
CREATE DATABASE IF NOT EXISTS `appcoches` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE `appcoches`;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `coches`
--

DROP TABLE IF EXISTS `coches`;
CREATE TABLE IF NOT EXISTS `coches` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `marca` varchar(50) NOT NULL,
  `modelo` varchar(50) NOT NULL,
  `año` int(11) NOT NULL,
  `precio` decimal(10,2) NOT NULL,
  `descripcion` text DEFAULT NULL,
  `imagen` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `coches`
--

INSERT INTO `coches` (`id`, `marca`, `modelo`, `año`, `precio`, `descripcion`, `imagen`) VALUES
(1, 'Audi', 'S5 Coupé', 2012, 26000.00, 'Audi S5 Coupé 3.0 TFSI 333 CV quattro S tronic 7 vel., elegante y deportivo, con 112 000 km, combina potencia y lujo en cada detalle.', 'coche_1770234356.jpg'),
(8, 'BMW', '335i Coupé', 2007, 17000.00, 'BMW 335i Coupé 2007, potente y elegante, con 135 000 km, perfecto equilibrio entre deportividad y confort.', 'coche_1770234577.jpg'),
(9, 'BMW', 'M5 E60', 2006, 30000.00, 'BMW M5 E60 2006 con solo 42.200 km, motor V10 atmosférico de 507 CV en estado impecable.\nPrestaciones de superdeportivo con el confort y elegancia de una berlina de lujo.', 'coche_1770407403.jpg'),
(10, 'Volvo', 'XC60 B4', 2023, 40000.00, 'Volvo XC60 B4 2023 con solo 200 km, motor 2.0 mild-hybrid de 197 CV con cambio automático y tracción eficiente.', 'coche_1770407631.jpg'),
(11, 'Volkswagen', 'Scirocco R', 2009, 13500.00, 'Volkswagen Scirocco R 2009 con 110 000 km, coupé deportivo potente y equilibrado.\nMotor 2.0 TSI, tracción delantera y aceleración ágil con hasta 250 km/h de velocidad punta.', 'coche_1770407845.jpg'),
(12, 'Volkswagen', 'Golf R32', 2008, 15000.00, 'Volkswagen R32 2008 con 136 000 km, deportivo clásico con motor VR6 3.2 L de 250 CV y 236 lb·ft, tracción integral 4MOTION y transmisión 6 velocidades (manual o DSG).', 'coche_1770408065.jpg'),
(13, 'Audi', 'S8 D3', 2006, 23000.00, 'Audi S8 D3 2006 con 99 000 km, berlina de lujo deportiva con motor V10 5.2 L atmosférico de 450 CV y 540 Nm, tracción quattro y cambio automático Tiptronic para aceleración contundente y refinada.', 'coche_1770408144.jpg'),
(14, 'Seat', 'Arona', 2024, 26000.00, 'SEAT Arona 2024 con solo ~3.000 km, SUV urbano con motor gasolina TSI eficiente (115–150 CV según versión) y conectividad y asistentes de conducción modernos.', 'coche_1770408332.jpg'),
(15, 'Opel', 'Corsa', 2021, 10500.00, 'Opel Corsa 2021 gasolina con 30 000 km, motor 1.2 Turbo (~100 CV) ágil y económico con etiqueta medioambiental eficiente.', 'coche_1770408378.jpg'),
(16, 'Mercedes-Benz', 'CLS 400 4MATIC', 2016, 27600.00, 'Mercedes‑Benz CLS 400 4MATIC 2016 con 66 000 km, potente berlina de lujo con motor V6 3.0 Turbo de 333 CV y tracción integral para una conducción estable y dinámica.', 'coche_1770408758.jpg'),
(17, 'BMW', 'X6', 2014, 26000.00, 'BMW X6 M50d 2014 con 145 000 km, SUV potente con motor diésel 3.0 Turbo de 381 CV y tracción total xDrive para un rendimiento sólido y conducción versátil.', 'coche_1770408975.jpg'),
(18, 'Seat', 'Ibiza', 2018, 12100.00, 'Seat Ibiza 2018 con 45 000 km, utilitario ágil con motor gasolina eficiente ideal para ciudad y viajes cortos.\nConfort práctico, bajo consumo y tecnología moderna para uso diario.', 'coche_1770409105.jpg');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuarios`
--

DROP TABLE IF EXISTS `usuarios`;
CREATE TABLE IF NOT EXISTS `usuarios` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password` varchar(255) NOT NULL,
  `rol` enum('admin','usuario') DEFAULT 'usuario',
  `fecha_registro` timestamp NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `usuarios`
--

INSERT INTO `usuarios` (`id`, `nombre`, `email`, `password`, `rol`, `fecha_registro`) VALUES
(1, 'Admin Principal', 'admin@ejemplo.com', '240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9', 'admin', '2026-01-30 22:07:48'),
(6, 'Carlos Sierra', 'carlosss30112005@gmail.com', '6d6312327480f0f70d9d3313899958d8e11b82be50735ebd70160bdb9f6668ea', 'usuario', '2026-02-02 09:10:20');
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;