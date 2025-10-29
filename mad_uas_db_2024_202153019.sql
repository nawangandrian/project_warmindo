-- phpMyAdmin SQL Dump
-- version 4.7.4
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jan 13, 2025 at 04:09 PM
-- Server version: 10.1.29-MariaDB
-- PHP Version: 7.2.0

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `mad_uas_db_2024_202153019`
--

-- --------------------------------------------------------

--
-- Table structure for table `detail_transaksi`
--

CREATE TABLE `detail_transaksi` (
  `ID_Detail` int(11) NOT NULL,
  `ID_Transaksi` varchar(15) DEFAULT NULL,
  `ID_Menu` int(11) DEFAULT NULL,
  `Jumlah` int(11) NOT NULL,
  `Subtotal` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `detail_transaksi`
--

INSERT INTO `detail_transaksi` (`ID_Detail`, `ID_Transaksi`, `ID_Menu`, `Jumlah`, `Subtotal`) VALUES
(25, 'TR130125001', 15, 1, 6000),
(26, 'TR130125002', 17, 1, 6000),
(27, 'TR130125002', 13, 1, 6000),
(28, 'TR130125003', 15, 1, 6000),
(29, 'TR130125004', 12, 1, 5000),
(30, 'TR130125004', 15, 2, 12000),
(31, 'TR130125005', 15, 2, 12000),
(32, 'TR130125006', 10, 3, 18000),
(33, 'TR130125006', 16, 1, 5000),
(34, 'TR130125007', 15, 1, 6000),
(35, 'TR130125007', 16, 1, 5000),
(36, 'TR130125007', 12, 1, 5000),
(37, 'TR130125008', 11, 2, 12000),
(38, 'TR130125009', 13, 1, 6000),
(39, 'TR130125009', 14, 1, 5000),
(40, 'TR130125010', 13, 3, 18000),
(41, 'TR130125011', 17, 1, 6000),
(42, 'TR130125011', 16, 1, 5000),
(43, 'TR130125011', 15, 1, 6000),
(44, 'TR130125011', 12, 1, 5000),
(45, 'TR130125011', 10, 1, 6000),
(46, 'TR130125012', 17, 1, 6000),
(47, 'TR130125012', 16, 1, 5000),
(48, 'TR130125012', 13, 1, 6000),
(49, 'TR130125012', 11, 1, 6000),
(50, 'TR130125012', 14, 1, 5000),
(51, 'TR130125012', 12, 1, 5000),
(52, 'TR130125012', 10, 1, 6000),
(53, 'TR130125013', 17, 1, 6000),
(54, 'TR130125013', 16, 1, 5000),
(55, 'TR130125013', 15, 1, 6000),
(56, 'TR130125013', 14, 1, 5000),
(57, 'TR130125013', 13, 1, 6000),
(58, 'TR130125013', 12, 1, 5000),
(59, 'TR130125013', 11, 1, 6000),
(60, 'TR130125013', 10, 1, 6000);

-- --------------------------------------------------------

--
-- Table structure for table `kasir`
--

CREATE TABLE `kasir` (
  `ID_Kasir` int(11) NOT NULL,
  `Nama_Kasir` varchar(255) NOT NULL,
  `No_Telepon_Kasir` varchar(15) NOT NULL,
  `Alamat_Kasir` varchar(255) NOT NULL,
  `ID_User` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `kasir`
--

INSERT INTO `kasir` (`ID_Kasir`, `Nama_Kasir`, `No_Telepon_Kasir`, `Alamat_Kasir`, `ID_User`) VALUES
(1, 'Aksar Frida', '085678651211', 'Dawe', 2),
(3, 'Caca Andika', '087533457658', 'Bae', 5),
(5, 'Nawang Andrian', '086563572398', 'Gebog', 3),
(7, 'Dimas Arya', '086421234213', 'Kaliwungu', 4),
(8, 'Bagus Cahyo', '086532452376', 'Jekulo', 0);

-- --------------------------------------------------------

--
-- Table structure for table `menu`
--

CREATE TABLE `menu` (
  `ID_Menu` int(11) NOT NULL,
  `Nama_Menu` varchar(255) NOT NULL,
  `Jenis_Menu` enum('Mie Goreng','Mie Kuah') NOT NULL,
  `Harga` int(11) NOT NULL,
  `Stok` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `menu`
--

INSERT INTO `menu` (`ID_Menu`, `Nama_Menu`, `Jenis_Menu`, `Harga`, `Stok`) VALUES
(10, 'Indomie Goreng Ayam Bawang', 'Mie Goreng', 6000, 26),
(11, 'Indomie Goreng Pedas', 'Mie Goreng', 6000, 30),
(12, 'Indomie Soto Mie', 'Mie Kuah', 5000, 27),
(13, 'Indomie Mi Goreng Rendang', 'Mie Goreng', 6000, 36),
(14, 'Indomie Kuah Ayam Bawang', 'Mie Kuah', 5000, 27),
(15, 'Indomie Goreng Special', 'Mie Goreng', 6000, 34),
(16, 'Indomie Mie Kuah Kari Ayam', 'Mie Kuah', 5000, 21),
(17, 'Indomie Goreng Sambal Matah', 'Mie Goreng', 6000, 34);

-- --------------------------------------------------------

--
-- Table structure for table `pelanggan`
--

CREATE TABLE `pelanggan` (
  `ID_Pelanggan` int(11) NOT NULL,
  `Nama_Pelanggan` varchar(255) NOT NULL,
  `No_Telepon_Pelanggan` varchar(15) NOT NULL,
  `Alamat_Pelanggan` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `pelanggan`
--

INSERT INTO `pelanggan` (`ID_Pelanggan`, `Nama_Pelanggan`, `No_Telepon_Pelanggan`, `Alamat_Pelanggan`) VALUES
(2, 'Wijaya', '087545671287', 'Bae'),
(3, 'Alan', '085623234576', 'Gebog');

-- --------------------------------------------------------

--
-- Table structure for table `transaksi`
--

CREATE TABLE `transaksi` (
  `ID_Transaksi` varchar(15) NOT NULL,
  `Tanggal_Transaksi` datetime NOT NULL,
  `Jumlah_Beli` int(11) NOT NULL,
  `Diskon_Transaksi` decimal(10,2) NOT NULL,
  `Pajak_Transaksi` decimal(10,2) NOT NULL,
  `Total_Harga` int(11) NOT NULL,
  `Metode_Pembayaran` enum('Tunai','Kartu Kredit','Transfer') NOT NULL,
  `Jenis_Pesanan` enum('Take Away','Dine In') NOT NULL,
  `ID_Pelanggan` int(11) DEFAULT NULL,
  `ID_Kasir` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `transaksi`
--

INSERT INTO `transaksi` (`ID_Transaksi`, `Tanggal_Transaksi`, `Jumlah_Beli`, `Diskon_Transaksi`, `Pajak_Transaksi`, `Total_Harga`, `Metode_Pembayaran`, `Jenis_Pesanan`, `ID_Pelanggan`, `ID_Kasir`) VALUES
('TR130125001', '2025-01-13 19:22:21', 1, '300.00', '120.00', 5820, 'Tunai', 'Dine In', 2, 5),
('TR130125002', '2025-01-13 20:07:17', 2, '360.00', '120.00', 11760, 'Transfer', 'Take Away', 2, 5),
('TR130125003', '2025-01-13 20:07:57', 1, '300.00', '120.00', 5820, 'Kartu Kredit', 'Dine In', 3, 5),
('TR130125004', '2025-01-13 20:08:45', 3, '850.00', '340.00', 16490, 'Transfer', 'Take Away', 3, 7),
('TR130125005', '2025-01-13 20:18:15', 2, '1200.00', '600.00', 11400, 'Kartu Kredit', 'Take Away', 3, 7),
('TR130125006', '2025-01-13 20:18:56', 4, '1610.00', '920.00', 22310, 'Transfer', 'Dine In', 2, 7),
('TR130125007', '2025-01-13 20:19:47', 3, '1600.00', '800.00', 15200, 'Transfer', 'Take Away', 3, 7),
('TR130125008', '2025-01-13 20:21:24', 2, '360.00', '0.00', 11640, 'Tunai', 'Take Away', 2, 7),
('TR130125009', '2025-01-13 20:22:06', 2, '110.00', '330.00', 11220, 'Kartu Kredit', 'Dine In', 3, 5),
('TR130125010', '2025-01-13 20:22:30', 3, '900.00', '180.00', 17280, 'Kartu Kredit', 'Take Away', 3, 5),
('TR130125011', '2025-01-13 20:24:52', 5, '3360.00', '1120.00', 25760, 'Kartu Kredit', 'Dine In', 2, 5),
('TR130125012', '2025-01-13 20:30:44', 7, '4680.00', '3900.00', 38220, 'Tunai', 'Dine In', 3, 5),
('TR130125013', '2025-01-13 20:43:05', 8, '450.00', '2250.00', 46800, 'Kartu Kredit', 'Take Away', 2, 5);

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

CREATE TABLE `user` (
  `id_user` int(11) NOT NULL,
  `username` varchar(50) NOT NULL,
  `password` varchar(50) NOT NULL,
  `hak_akses` enum('Admin','Kasir') NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `user`
--

INSERT INTO `user` (`id_user`, `username`, `password`, `hak_akses`) VALUES
(1, 'admin', '123', 'Admin'),
(3, 'Alan', '123', 'Kasir'),
(4, 'Dimas', '123', 'Kasir');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `detail_transaksi`
--
ALTER TABLE `detail_transaksi`
  ADD PRIMARY KEY (`ID_Detail`),
  ADD KEY `ID_Menu` (`ID_Menu`),
  ADD KEY `detail_transaksi_ibfk_1` (`ID_Transaksi`);

--
-- Indexes for table `kasir`
--
ALTER TABLE `kasir`
  ADD PRIMARY KEY (`ID_Kasir`);

--
-- Indexes for table `menu`
--
ALTER TABLE `menu`
  ADD PRIMARY KEY (`ID_Menu`);

--
-- Indexes for table `pelanggan`
--
ALTER TABLE `pelanggan`
  ADD PRIMARY KEY (`ID_Pelanggan`);

--
-- Indexes for table `transaksi`
--
ALTER TABLE `transaksi`
  ADD PRIMARY KEY (`ID_Transaksi`),
  ADD KEY `ID_Pelanggan` (`ID_Pelanggan`),
  ADD KEY `ID_Kasir` (`ID_Kasir`);

--
-- Indexes for table `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`id_user`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `detail_transaksi`
--
ALTER TABLE `detail_transaksi`
  MODIFY `ID_Detail` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=61;

--
-- AUTO_INCREMENT for table `kasir`
--
ALTER TABLE `kasir`
  MODIFY `ID_Kasir` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT for table `menu`
--
ALTER TABLE `menu`
  MODIFY `ID_Menu` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=18;

--
-- AUTO_INCREMENT for table `pelanggan`
--
ALTER TABLE `pelanggan`
  MODIFY `ID_Pelanggan` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `user`
--
ALTER TABLE `user`
  MODIFY `id_user` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `detail_transaksi`
--
ALTER TABLE `detail_transaksi`
  ADD CONSTRAINT `detail_transaksi_ibfk_1` FOREIGN KEY (`ID_Transaksi`) REFERENCES `transaksi` (`ID_Transaksi`),
  ADD CONSTRAINT `detail_transaksi_ibfk_2` FOREIGN KEY (`ID_Menu`) REFERENCES `menu` (`ID_Menu`);

--
-- Constraints for table `transaksi`
--
ALTER TABLE `transaksi`
  ADD CONSTRAINT `transaksi_ibfk_1` FOREIGN KEY (`ID_Pelanggan`) REFERENCES `pelanggan` (`ID_Pelanggan`),
  ADD CONSTRAINT `transaksi_ibfk_2` FOREIGN KEY (`ID_Kasir`) REFERENCES `kasir` (`ID_Kasir`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
