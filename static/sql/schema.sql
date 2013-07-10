/*

plen: {0, 6, 8, 10, 12} // value of the shortest permitted password
psets: {1, 2, 3, 4} // number of symbol sets that must be used
pdict: {1, 0}  // are passwords checked whether they match a dictionary
phist: {0, 1, 2, 3}  // history check of passwords resp. none, minimum (1 past password, exact match), strict (2 past passwords, string distance of 2), extreme (4 past passwords, string distance of 5)
prenew: {0, 1, 2, 3} // when the system asks users to renew passwords: never, annually, quarterly, monthly
pattempts: {1, 0} // is there a limit on wrong password attempts
precovery: {1, 0} // are forgotten passwords restored automatically(1), or is there human support(0)

 */
CREATE TABLE `users` (
  `username` varchar(15) NOT NULL,
  `Id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(70) NOT NULL,
  `email` varchar(45) NOT NULL,
  PRIMARY KEY (`Id`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8;

CREATE TABLE `pw_policy` (
  `idpolicy` int(11) NOT NULL AUTO_INCREMENT,
  `plen` int(11) NOT NULL,
  `psets` int(11) NOT NULL,
  `pdict` tinyint(4) NOT NULL,
  `phist` int(11) NOT NULL,
  `prenew` int(11) NOT NULL,
  `pattempts` tinyint(4) NOT NULL,
  `precovery` tinyint(4) NOT NULL,
  `userid` int(11) NOT NULL,
  `date` datetime NOT NULL,
  PRIMARY KEY (`idpolicy`),
  KEY `userid_idx` (`userid`),
  CONSTRAINT `userid` FOREIGN KEY (`userid`) REFERENCES `users` (`Id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=57 DEFAULT CHARSET=utf8;

CREATE TABLE `pwrecovery` (
  `Id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(20) NOT NULL,
  `date` datetime NOT NULL,
  `rid` text NOT NULL,
  `isrecovered` int(11) NOT NULL,
  PRIMARY KEY (`Id`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8;

CREATE TABLE `scores` (
  `idscores` int(11) NOT NULL AUTO_INCREMENT,
  `userid` int(11) NOT NULL,
  `score_type` int(11) NOT NULL,
  `score_value` decimal(5,2) NOT NULL,
  `date` datetime NOT NULL,
  `rank` int(11) NOT NULL,
  PRIMARY KEY (`idscores`),
  KEY `userid_idx` (`userid`),
  CONSTRAINT `` FOREIGN KEY (`userid`) REFERENCES `users` (`Id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8;