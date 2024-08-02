-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jul 29, 2024 at 05:08 AM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.1.25

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `odc_keys_witel_jember`
--

-- --------------------------------------------------------

--
-- Table structure for table `borrowed_keys`
--

CREATE TABLE `borrowed_keys` (
  `id` int(11) NOT NULL,
  `key_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `time_borrowed` timestamp NOT NULL DEFAULT current_timestamp(),
  `keys_returned` timestamp NULL DEFAULT NULL,
  `is_return` tinyint(1) DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `odc_info`
--

CREATE TABLE `odc_info` (
  `odc_id` int(11) NOT NULL,
  `odc_name` varchar(255) NOT NULL,
  `is_key_available` tinyint(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `odc_info`
--

INSERT INTO `odc_info` (`odc_id`, `odc_name`, `is_key_available`) VALUES
(1, 'ODC-Alpha-123', 1),
(2, 'ODC-Beta-123', 1),
(3, 'ODC-Gamma-123', 0);

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `user_id` bigint(20) DEFAULT NULL,
  `username` varchar(255) NOT NULL,
  `is_registered` tinyint(1) DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`user_id`, `username`, `is_registered`) VALUES
(5721823426, 'khuluqilkarims', 1);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `borrowed_keys`
--
ALTER TABLE `borrowed_keys`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD UNIQUE KEY `user_id` (`user_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `borrowed_keys`
--
ALTER TABLE `borrowed_keys`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
