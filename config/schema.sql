-- phpMyAdmin SQL Dump
-- version 4.0.4
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Jul 09, 2013 at 11:29 AM
-- Server version: 5.6.12
-- PHP Version: 5.4.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `sprks`
--
CREATE DATABASE IF NOT EXISTS `sprks` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `sprks`;

-- --------------------------------------------------------

--
-- Table structure for table `journal`
--

CREATE TABLE IF NOT EXISTS `journal` (
  `user_id` int(11) NOT NULL,
  `date` date NOT NULL,
  `incident_id` int(11) NOT NULL,
  `cost` int(11) NOT NULL,
  `commited` tinyint(1) NOT NULL,
  KEY `user_id_idx` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `password_recovery`
--

CREATE TABLE IF NOT EXISTS `password_recovery` (
  `user_id` int(11) NOT NULL,
  `datetime` datetime NOT NULL,
  `token` char(56) NOT NULL,
  `invalid` int(11) NOT NULL,
  PRIMARY KEY (`token`),
  KEY `user_id_idx` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `pw_policy`
--

CREATE TABLE IF NOT EXISTS `pw_policy` (
  `idpolicy` int(11) NOT NULL AUTO_INCREMENT,
  `plen` int(11) NOT NULL,
  `psets` int(11) NOT NULL,
  `pdict` tinyint(4) NOT NULL,
  `phist` int(11) NOT NULL,
  `prenew` int(11) NOT NULL,
  `pattempts` tinyint(4) NOT NULL,
  `precovery` tinyint(4) NOT NULL,
  `userid` int(11) NOT NULL,
  `date` date NOT NULL,
  PRIMARY KEY (`idpolicy`),
  KEY `userid_idx` (`userid`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=16 ;

-- --------------------------------------------------------

--
-- Table structure for table `scores`
--

CREATE TABLE IF NOT EXISTS `scores` (
  `idscores` int(11) NOT NULL AUTO_INCREMENT,
  `userid` int(11) NOT NULL,
  `score_type` int(11) NOT NULL,
  `score_value` decimal(5,2) NOT NULL,
  `date` date NOT NULL,
  `rank` int(11) NOT NULL,
  PRIMARY KEY (`idscores`),
  KEY `userid_idx` (`userid`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=3 ;

-- --------------------------------------------------------

--
-- Table structure for table `sessions`
--

CREATE TABLE IF NOT EXISTS `sessions` (
  `session_id` char(128) NOT NULL,
  `atime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `data` text,
  UNIQUE KEY `session_id` (`session_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE IF NOT EXISTS `users` (
  `username` varchar(15) NOT NULL,
  `user_id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(70) NOT NULL,
  `email` varchar(45) NOT NULL,
  PRIMARY KEY (`user_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=11 ;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `journal`
--
ALTER TABLE `journal`
  ADD CONSTRAINT `journal_user_id` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `password_recovery`
--
ALTER TABLE `password_recovery`
  ADD CONSTRAINT `password_recovery_user_id` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `pw_policy`
--
ALTER TABLE `pw_policy`
  ADD CONSTRAINT `pw_policy_userid` FOREIGN KEY (`userid`) REFERENCES `users` (`user_id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `scores`
--
ALTER TABLE `scores`
  ADD CONSTRAINT `scores_user_id` FOREIGN KEY (`userid`) REFERENCES `users` (`user_id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Biometrics policy table
--
CREATE  TABLE `sprks`.`biometrics` (
  `id` INT NOT NULL AUTO_INCREMENT ,
  `bdata` TINYINT(1) NOT NULL ,
  PRIMARY KEY (`id`) );


--
-- Passfaces policy table
--


CREATE TABLE `sprks`.`passfaces` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `pdata` int(1) NOT NULL,
  PRIMARY KEY (`id`)
)



--
-- Policies table
--
CREATE  TABLE `sprks`.`policies` (
  `id` INT NOT NULL AUTO_INCREMENT ,
  `user_id` INT NOT NULL ,
  `location` VARCHAR(45) NOT NULL ,
  `employee` VARCHAR(45) NOT NULL ,
  `device` VARCHAR(45) NOT NULL ,
  `policy_id` INT NOT NULL ,
  `date` DATE NOT NULL ,
  PRIMARY KEY (`id`) );


/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
