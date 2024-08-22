-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: May 23, 2024 at 10:42 AM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.0.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `erp`
--

-- --------------------------------------------------------

--
-- Table structure for table `signup`
--

CREATE TABLE `signup` (
  `fname` varchar(200) NOT NULL,
  `email` varchar(200) NOT NULL,
  `uname` varchar(200) NOT NULL,
  `pass` varchar(200) NOT NULL,
  `uimg` blob NOT NULL,
  `mobile` varchar(200) NOT NULL,
  `des` varchar(200) NOT NULL,
  `exp` varchar(200) NOT NULL,
  `salary` varchar(200) NOT NULL,
  `gender` varchar(200) NOT NULL,
  `totalpro` varchar(200) NOT NULL,
  `profile` varchar(200) NOT NULL,
  `status` varchar(200) NOT NULL DEFAULT 'Inactive'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `signup`
--

INSERT INTO `signup` (`fname`, `email`, `uname`, `pass`, `uimg`, `mobile`, `des`, `exp`, `salary`, `gender`, `totalpro`, `profile`, `status`) VALUES
('Rashi gothefode', 'rashi@gmail.com', 'rashi', 'rashi', 0x672e6a7067, '', '', '', '', '', '', 'Employee', 'Inactive'),
('Ravi Thakare', 'ravi@gmail.com', 'ravi', 'ravi', 0x64656d6f206c6f67696e2e6a7067, '7894561319', 'Backend Developer', '5', '200000', 'Male', '3', 'Employee', 'Inactive'),
('Shubham Thakare', 'shubham@gmail.com', 'shubham', 'shubham', 0x726168756c2e6a7067, '', '', '', '', '', '', 'Interns', 'Inactive'),
('vishal kambe', 'vishal@gmail.com', 'vishal', 'vishal', 0x70726f66696c652e6a706567, '', 'Full-Stack Developer', '', '', 'Male', '', 'Employee', 'Inactive');

-- --------------------------------------------------------

--
-- Table structure for table `task`
--

CREATE TABLE `task` (
  `tprofile` varchar(200) NOT NULL,
  `tsend` varchar(200) NOT NULL,
  `tname` varchar(200) NOT NULL,
  `tdes` varchar(200) NOT NULL,
  `tldate` date NOT NULL,
  `tltime` time(6) NOT NULL,
  `ttdate` date NOT NULL DEFAULT current_timestamp(),
  `tstatus` varchar(200) NOT NULL,
  `tid` int(200) NOT NULL,
  `tsug` varchar(255) NOT NULL,
  `tupload` varchar(255) NOT NULL,
  `ename` varchar(200) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `task`
--

INSERT INTO `task` (`tprofile`, `tsend`, `tname`, `tdes`, `tldate`, `tltime`, `ttdate`, `tstatus`, `tid`, `tsug`, `tupload`, `ename`) VALUES
('Employee', 'Employee', 'Personal Work', 'personal work', '2024-05-30', '20:00:00.000000', '2024-05-24', 'Submit', 13, '', '', 'prashik');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `signup`
--
ALTER TABLE `signup`
  ADD PRIMARY KEY (`uname`);

--
-- Indexes for table `task`
--
ALTER TABLE `task`
  ADD PRIMARY KEY (`tid`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `task`
--
ALTER TABLE `task`
  MODIFY `tid` int(200) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
