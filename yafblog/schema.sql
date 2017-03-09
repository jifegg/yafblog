DROP TABLE IF EXISTS `article`;
CREATE TABLE `article` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `title` VARCHAR(100) NOT NULL COMMENT '����',
  `content` TEXT NOT NULL COMMENT '����',
  `content_html` TEXT COMMENT 'markdown',
  `toc_html` TEXT,
  `category` INT(11) NOT NULL COMMENT '����',
  `tags` VARCHAR(100) DEFAULT NULL COMMENT '��ǩ',
  `archive` CHAR(6) NOT NULL COMMENT '�浵',
  `addtime` INT(11) NOT NULL COMMENT '���ʱ��',
  PRIMARY KEY (`id`),
  UNIQUE KEY `title` (`title`)
) ENGINE=MYISAM DEFAULT CHARSET=utf8;


DROP TABLE IF EXISTS `category`;
CREATE TABLE `category` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(100) DEFAULT NULL COMMENT '����',
  `num` MEDIUMINT(9) DEFAULT '0' COMMENT '����',
  `addtime` INT(11) DEFAULT '0' COMMENT '���ʱ��',
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=MYISAM DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `tag`;
CREATE TABLE `tag` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(100) DEFAULT NULL,
  `num` MEDIUMINT(9) DEFAULT '0',
  `addtime` INT(11) DEFAULT '0',
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=MYISAM DEFAULT CHARSET=utf8;


DROP TABLE IF EXISTS `archive`;
CREATE TABLE `archive` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `month` CHAR(6) NOT NULL,
  `num` MEDIUMINT(9) DEFAULT '0',
  `addtime` INT(11) DEFAULT '0',
  PRIMARY KEY (`id`),
  UNIQUE KEY `month` (`month`)
) ENGINE=MYISAM  DEFAULT CHARSET=utf8;


DROP TABLE IF EXISTS `admin`;
CREATE TABLE `admin` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `username` VARCHAR(50) DEFAULT NULL,
  `password` CHAR(32) DEFAULT NULL,
  `addtime` INT(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MYISAM  DEFAULT CHARSET=utf8;
INSERT INTO `admin` (`id`, `username`, `password`, `addtime`) values('1','admin','21232f297a57a5a743894a0e4a801fc3',NULL);
