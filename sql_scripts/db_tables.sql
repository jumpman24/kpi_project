CREATE TABLE `country` (
    `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
    `name` VARCHAR(255) NOT NULL,
    `code` CHAR(2) NOT NULL,
    PRIMARY KEY (`id`),
    UNIQUE (`code`)
);

CREATE TABLE `city` (
    `country_id` INT UNSIGNED NOT NULL,
    `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
    `name` VARCHAR(255) NOT NULL,
    PRIMARY KEY (`id`),
    CONSTRAINT `FK_country_city` FOREIGN KEY (`country_id`) REFERENCES `country`(`id`)
);

CREATE TABLE `national_rank` (
    `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
    `name` VARCHAR(255) NOT NULL,
    `abbreviate` VARCHAR(20) NOT NULL,
    PRIMARY KEY (`id`)
);

CREATE TABLE `rank` (
    `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
    `name` VARCHAR(255) NOT NULL,
    `abbreviate` CHAR(3) NOT NULL,
    PRIMARY KEY (`id`)
);

CREATE TABLE `player` (
    `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
    `PIN` CHAR(8),
    `last_name` VARCHAR(255) NOT NULL,
    `first_name` VARCHAR(255) NOT NULL,
    `rating` DECIMAL(7, 3) UNSIGNED DEFAULT 100,
    `city_id` INT UNSIGNED,
    `rank_id` INT UNSIGNED,
    `national_rank_id` INT UNSIGNED,
    `is_active` TINYINT(1) DEFAULT 1,
    PRIMARY KEY (`id`),
    UNIQUE (`PIN`),
    CONSTRAINT `FK_city_player` FOREIGN KEY (`city_id`) REFERENCES `city`(`id`),
    CONSTRAINT `FK_rank_player` FOREIGN KEY (`rank_id`) REFERENCES `rank`(`id`),
    CONSTRAINT `FK_national_rank_player` FOREIGN KEY (`national_rank_id`) REFERENCES `national_rank`(`id`)
);

CREATE TABLE `tournament` (
    `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
    `PIN` CHAR(8),
    `name` VARCHAR(255) NOT NULL,
    `city_id` INT UNSIGNED,
    `date_start` DATE NOT NULL,
    `date_end` DATE NOT NULL,
    `is_ranked` TINYINT(1),
    PRIMARY KEY (`id`),
    CONSTRAINT `FK_city_tournament` FOREIGN KEY (`city_id`) REFERENCES `city`(`id`)
);

CREATE TABLE `participant` (
    `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
    `player_id` INT UNSIGNED NOT NULL,
    `tournament_id` INT UNSIGNED NOT NULL,
    `rank_id` INT UNSIGNED,
    `place` INT UNSIGNED,
    `rating_start` DECIMAL(8, 4),
    `rating_end` DECIMAL(8, 4),
    PRIMARY KEY (`id`),
    CONSTRAINT `FK_player_participant` FOREIGN KEY (`player_id`) REFERENCES `player`(`id`),
    CONSTRAINT `FK_tournament_participant` FOREIGN KEY (`tournament_id`) REFERENCES `tournament`(`id`),
    CONSTRAINT `FK_rank_participant` FOREIGN KEY (`rank_id`) REFERENCES `rank`(`id`)
);

CREATE TABLE `pairing` (
    `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
    `player_id` INT UNSIGNED NOT NULL,
    `opponent_id` INT UNSIGNED,
    `round` INT UNSIGNED,
    `color` CHAR(1),
    `handicap` INT UNSIGNED DEFAULT 0,
    `round_skip` TINYINT(1),
    `result` TINYINT(1),
    `is_technical` TINYINT(1),
    PRIMARY KEY (`id`),
    CONSTRAINT `FK_participant_player` FOREIGN KEY (`player_id`) REFERENCES `participant`(`id`),
    CONSTRAINT `FK_participant_opponent` FOREIGN KEY (`opponent_id`) REFERENCES `participant`(`id`)
);
