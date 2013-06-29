
--
-- Database: `sprks`
--

-- --------------------------------------------------------

--
-- Table structure for table `password_recovery`
--

CREATE TABLE IF NOT EXISTS `password_recovery` (
  `user_id` int(11) NOT NULL AUTO_INCREMENT,
  `date` datetime NOT NULL,
  `token` text NOT NULL,
  `isrecovered` int(11) NOT NULL,
  PRIMARY KEY (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

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
  `pautorecover` tinyint(4) NOT NULL,
  `userid` int(11) NOT NULL,
  `date` datetime NOT NULL,
  PRIMARY KEY (`idpolicy`),
  KEY `userid_idx` (`userid`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=2 ;

-- --------------------------------------------------------

--
-- Table structure for table `scores`
--

CREATE TABLE IF NOT EXISTS `scores` (
  `idscores` int(11) NOT NULL AUTO_INCREMENT,
  `userid` int(11) NOT NULL,
  `score_type` int(11) NOT NULL,
  `score_value` decimal(5,2) NOT NULL,
  `date` datetime NOT NULL,
  `rank` int(11) NOT NULL,
  PRIMARY KEY (`idscores`),
  KEY `userid_idx` (`userid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

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
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=2 ;

--
-- Constraints for table `pw_policy`
--
ALTER TABLE `pw_policy`
  ADD CONSTRAINT `userid` FOREIGN KEY (`userid`) REFERENCES `users` (`user_id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `scores`
--
ALTER TABLE `scores`
  ADD CONSTRAINT `` FOREIGN KEY (`userid`) REFERENCES `users` (`user_id`) ON DELETE CASCADE ON UPDATE CASCADE;
