-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: May 23, 2024 at 08:56 PM
-- Server version: 10.4.28-MariaDB
-- PHP Version: 8.2.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `precise_extract`
--

-- --------------------------------------------------------

--
-- Table structure for table `abc`
--

CREATE TABLE `abc` (
  `Date` date DEFAULT NULL,
  `Instrument_Id` varchar(100) DEFAULT NULL,
  `Amount` int(100) DEFAULT NULL,
  `Type` varchar(100) DEFAULT NULL,
  `Balance` int(100) DEFAULT NULL,
  `Remarks` varchar(200) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `abc`
--

INSERT INTO `abc` (`Date`, `Instrument_Id`, `Amount`, `Type`, `Balance`, `Remarks`) VALUES
('2022-12-15', '', 8100, 'DR', 2094, '05216015000619'),
('2022-12-12', '', 9100, 'CR', 10194, 'UPI/234678412099/P2V/nay.kothari123- 1@okhdfcbank/N'),
('2022-12-12', '', 500, 'DR', 1094, 'ATMWDR234613017371BDBG BLOCKBKC BANDRA'),
('2022-11-12', '', 5000, 'CR', 6094, 'UPI/234543148645/P2V/shahshailsh0707@okhdfc bank/S'),
('2022-03-12', '', 16, 'CR', 1094, '05212011023472:IntPd:01-09-2022 to 30-11-2022'),
('2022-01-16', '', 8100, 'DR', 1078, '05216015000619'),
('2022-11-15', '', 8100, 'CR', 9178, 'UPI/231916286245/P2V/nay.kothari123- 1@okhdfebank/N'),
('2022-10-15', '', 8100, 'DR', 1078, '05216015000619'),
('2022-10-13', '', 8100, 'CR', 9178, 'NEFT_IN:KKBKH22286926474/0045/NAYNESH CHANDRAKANTKOTHARI'),
('2022-09-15', '', 8100, 'DR', 1078, '05216015000619'),
('2022-04-09', '', 8100, 'CR', 9178, 'NEFT_IN:KKBKH22247867272/0040/NAYNESH CHANDRAKANTKOTHARI'),
('2022-04-09', '', 22, 'CR', 1078, '05212011023472:Int.Pd:01-06-2022 to 31-08-2022'),
('2022-08-15', '', 8100, 'DR', 1056, '05216015000619'),
('2022-04-08', '', 8100, 'CR', 9156, 'NEFT_IN:KKBKH22216911633/0045/NAYNESH CHANDRAKANTKOTHARI'),
('2022-07-15', '', 8100, 'DR', 1056, '05216015000619'),
('2022-03-07', '', 8100, 'CR', 9156, 'NEFT_IN:KKBKH22184750332/0046/NAYNESH CHANDRAKANTKOTHARI'),
('2022-06-16', '', 8100, 'DR', 1056, '05216015000619'),
('2022-06-15', '', 8100, 'CR', 9156, 'NEFT_IN:KKBKH22166650673/0020/NAYNESH CHANDRAKANTKOTHARI'),
('2022-09-06', '', 17, 'CR', 1056, '05212011023472:Int.Pd:01-03-2022 to 31-05-2022'),
('2022-07-06', '', 177, 'DR', 1039, 'ATMANN.CHRGFORCARD-4066YEAR'),
('2022-05-15', '', 8100, 'DR', 1216, 'ENDED2021-2022 05216015000619'),
('2022-08-05', '', 8100, 'CR', 9316, 'NEFT_IN:KKBKH22128814627/0022/NAYNESH CHANDRAKANTKOTHARI'),
('2022-04-15', '', 8100, 'DR', 1216, '05216015000619'),
('2022-09-04', '', 8100, 'CR', 9316, 'NEFT_IN:KKBKH22099836149/0020/NAYNESH CHANDRAKANTKOTHARI'),
('2022-03-16', '', 8100, 'DR', 1216, '05216015000619'),
('2022-03-15', '', 8100, 'CR', 9316, 'NEFT_IN:KKBKH22074643475/0017/NAYNESH CHANDRAKANTKOTHARI'),
('2022-04-03', '', 39, 'CR', 1216, '05212011023472:Int.Pd:01-12-2021to 28-02-2022'),
('2022-02-15', '', 8100, 'DR', 1177, '05216015000619'),
('2022-04-02', '', 8100, 'CR', 9277, 'NEFT_IN:KKBKH22035645820/0046/NAYNESH CHANDRAKANTKOTHARI'),
('2022-01-15', '', 8100, 'DR', 1177, '05216015000619'),
('2022-02-01', '', 8100, 'CR', 9277, 'NEFT_IN:KKBKH22002653845/0028/NAYNESH CHANDRAKANTKOTHARI');

-- --------------------------------------------------------

--
-- Table structure for table `hello`
--

CREATE TABLE `hello` (
  `Date` date DEFAULT NULL,
  `Instrument_Id` varchar(100) DEFAULT NULL,
  `Amount` int(100) DEFAULT NULL,
  `Type` varchar(100) DEFAULT NULL,
  `Balance` int(100) DEFAULT NULL,
  `Remarks` varchar(200) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `hello`
--

INSERT INTO `hello` (`Date`, `Instrument_Id`, `Amount`, `Type`, `Balance`, `Remarks`) VALUES
('2023-12-19', '', 900, 'CR', 2005, 'UPI/335384736212/P2V/may.kothari123'),
('2023-12-15', '', 8100, 'DR', 1105, '7@okhdfebank/N 05216015000619'),
('2023-12-13', '', 500, 'DR', 9205, 'UPI/334772111605/P2V/nay.kothari123- 7@okhdfebank/N'),
('2023-03-12', '', 34, 'CR', 9705, '05212011023472:IntPd:01-09-2023to 30-11-2023'),
('2023-02-12', '', 8100, 'CR', 9671, 'NEFTNAYNESH CHANDRAKANTKOTHARI'),
('2023-11-15', '', 8100, 'DR', 1571, '05216015000619'),
('2023-01-11', '', 8100, 'CR', 9671, 'UPI/330532351625/P2V/nay.kothari123 2/@okaxis/NAYNE'),
('2023-10-19', '', 2, 'DR', 1571, 'SMS CHRG FOR:01-07-2023to30-09-2023'),
('2023-10-15', '', 8100, 'DR', 1573, '05216015000619'),
('2023-04-10', '', 8100, 'CR', 9673, 'NEFT NAYNESH CHANDRAKANT KOTHARI'),
('2023-09-15', '', 8100, 'DR', 1573, '05216015000619'),
('2023-02-09', '', 8100, 'CR', 9673, 'UPI/324518307119/P2V/nay.kothari123-'),
('2023-02-09', '', 38, 'CR', 1573, '2@okaxis/NAYNE 05212011023472:Int.Pd:01-06-2023 to 31-08-2023'),
('2023-08-15', '', 8100, 'DR', 1535, '05216015000619'),
('2023-01-08', '', 4100, 'CR', 9635, 'UPI/321397061720/P2V/may.kothari123- 6@okhdfcbank/N'),
('2023-01-08', '', 4000, 'CR', 5535, 'UPI/321396908515/P2V/may.kothari123'),
('0000-00-00', '', 0, '', 0, '6@okhdfebank/N'),
('2023-07-16', '', 3, 'DR', 1534, 'SMS CHRG FOR:01-04-2023t030-06-2023'),
('2023-07-15', '', 8100, 'DR', 1537, '05216015000619'),
('2023-06-30', '', 350, 'DR', 9637, 'UPI/318120953740/P2V/nay.kothari123 1@okaxis/NAYNE'),
('2023-06-22', '', 8100, 'CR', 9987, 'UPI/317323150060/P2V/nay.kothari123- 6@okhdfcbank/N'),
('2023-06-15', '', 8100, 'DR', 1887, '05216015000619'),
('2023-12-06', '', 177, 'DR', 9987, 'ATMANN.CHRGFORCARD-4066YEAR ENDED2022-2023'),
('2023-07-06', '', 8100, 'CR', 10164, 'UPI/315860503472/P2V/nay.kothari123- 6@okhdfcbank/N'),
('2023-04-06', '', 27, 'CR', 2064, '05212011023472:Int.Pd:01-03-2023 to 31-05-2023'),
('2023-05-15', '', 8100, 'DR', 2037, '05216015000619'),
('2023-07-05', '', 8100, 'CR', 10137, 'NEFT_IN:KKBKH23127838042/0031/NAYNESH CHANDRAKANTKOTHARI'),
('2023-04-15', '', 8100, 'DR', 2037, '05216015000619'),
('2023-12-04', '', 1, 'DR', 10137, 'SMS CHRG FOR:01-01-2023t031-03-2023'),
('2023-10-04', '', 8100, 'CR', 10139, 'NEFTNAYNESHCHANDRAKANTKOTHARI'),
('2023-03-16', '', 2, 'DR', 2039, 'SMS CHRG FOR:01-10-2022t031-12-2022'),
('2023-03-15', '', 8100, 'DR', 2041, '05216015000619'),
('2023-07-03', '', 7100, 'CR', 10141, 'NEFT_IN:KKBKH23066650160/0038/NAYNESH CHANDRAKANTKOTHARI'),
('2023-03-03', '', 26, 'CR', 3041, '05212011023472:Int.Pd:01-12-2022 to 28-02-2023'),
('2023-02-15', '', 8100, 'DR', 3015, '05216015000619'),
('2023-02-14', '', 2, 'DR', 11115, 'SMS CHRG FOR:01-07-2022t030-09-2022'),
('2023-03-02', '', 2100, 'CR', 11117, 'UPI/303404053616/P2V/nay.kothari123- 6@okhdfebank/N'),
('2023-01-31', '', 7000, 'CR', 9017, 'UPI/303130744891/P2V/vimalsagarjain@okhdfcba nk/SHE'),
('2023-01-15', '', 8100, 'DR', 2017, '05216015000619'),
('2023-01-14', '', 8200, 'CR', 10117, 'UPI/30148188316/P2V/nay.kothari23 6@okhdfcbank/N'),
('2023-08-01', '', 177, 'DR', 1917, 'QAB Charges from 01-10-2022 to 31-12-2022');

-- --------------------------------------------------------

--
-- Table structure for table `test`
--

CREATE TABLE `test` (
  `gender(male,female)` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL CHECK (json_valid(`gender(male,female)`)),
  `id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `test`
--

INSERT INTO `test` (`gender(male,female)`, `id`) VALUES
('{\"male\":2,\"female\":3}', 1),
('{\"male\":4,\"female\":5}', 2);

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

CREATE TABLE `user` (
  `userid` varchar(39) NOT NULL,
  `email` varchar(120) NOT NULL,
  `password` varchar(120) NOT NULL,
  `tables` varchar(200) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `user`
--

INSERT INTO `user` (`userid`, `email`, `password`, `tables`) VALUES
('', '', '', 'results'),
('17594164095492891793121081320226362432', 'meethalayman@gmail.com', '$2b$12$hma5/EjG46Pi72H2AZirlefziVx7B6U/CNC74ddhiki6U7fEeWPG2', NULL),
('177657590118603622714646109125795726077', 'doshi.maitri.mk@gmail.com', '$2b$12$QaQ7VYRRU5KaHJ7le/H4C.VXQxb.Om7D0rXKSZyBKt0xFniQEip4W', NULL),
('311440532879583556277770460729714008441', 'rpl.kothari123@gmail.com', '$2b$12$OfguF2HNyRZuQ5So.wlykOF8IWlDDLofRJ0dMk0HCqxx8fnUJsjIa', NULL),
('80908932720233265373125914068709548619', 'tirth.n.kothari@gmail.com', '$2b$12$KMxMYFsLbbDVTSO/pBbTZ.g1w7KYT0SXKELWpt2IjKAT0VfTSathi', NULL);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`userid`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
