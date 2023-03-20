-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema DevsOnDeck
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema DevsOnDeck
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `DevsOnDeck` DEFAULT CHARACTER SET utf8 ;
USE `DevsOnDeck` ;

-- -----------------------------------------------------
-- Table `DevsOnDeck`.`developers`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `DevsOnDeck`.`developers` ;

CREATE TABLE IF NOT EXISTS `DevsOnDeck`.`developers` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `first_name` VARCHAR(45) NULL,
  `last_name` VARCHAR(45) NULL,
  `email` VARCHAR(45) NULL,
  `github_user` VARCHAR(80) NULL,
  `address` VARCHAR(200) NULL,
  `city` VARCHAR(45) NULL,
  `state` VARCHAR(45) NULL,
  `password` VARCHAR(500) NULL,
  `short_bio` VARCHAR(1000) NULL,
  `available` TINYINT(1) NULL,
  `created_at` DATETIME NULL,
  `updated_at` DATETIME NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `DevsOnDeck`.`skills`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `DevsOnDeck`.`skills` ;

CREATE TABLE IF NOT EXISTS `DevsOnDeck`.`skills` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NULL,
  `tipo` VARCHAR(4) NOT NULL,
  `devicon` VARCHAR(45) NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `DevsOnDeck`.`skills_of_developers`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `DevsOnDeck`.`skills_of_developers` ;

CREATE TABLE IF NOT EXISTS `DevsOnDeck`.`skills_of_developers` (
  `developer_id` INT NOT NULL,
  `skill_id` INT NOT NULL,
  INDEX `fk_developer_has_skills_skills1_idx` (`skill_id` ASC) VISIBLE,
  INDEX `fk_developer_has_skills_developer_idx` (`developer_id` ASC) VISIBLE,
  PRIMARY KEY (`developer_id`, `skill_id`),
  CONSTRAINT `fk_developer_has_skills_developer`
    FOREIGN KEY (`developer_id`)
    REFERENCES `DevsOnDeck`.`developers` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_developer_has_skills_skills1`
    FOREIGN KEY (`skill_id`)
    REFERENCES `DevsOnDeck`.`skills` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `DevsOnDeck`.`organizations`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `DevsOnDeck`.`organizations` ;

CREATE TABLE IF NOT EXISTS `DevsOnDeck`.`organizations` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `org_name` VARCHAR(45) NULL,
  `email` VARCHAR(45) NULL,
  `address` VARCHAR(150) NULL,
  `city` VARCHAR(45) NULL,
  `state` VARCHAR(45) NULL,
  `password` VARCHAR(500) NULL,
  `created_at` DATETIME NULL,
  `updated_at` DATETIME NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `DevsOnDeck`.`positions`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `DevsOnDeck`.`positions` ;

CREATE TABLE IF NOT EXISTS `DevsOnDeck`.`positions` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(80) NULL,
  `description` TEXT NULL,
  `created_at` DATETIME NULL,
  `updated_at` DATETIME NULL,
  `organization_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_positions_organizations1_idx` (`organization_id` ASC) VISIBLE,
  CONSTRAINT `fk_positions_organizations1`
    FOREIGN KEY (`organization_id`)
    REFERENCES `DevsOnDeck`.`organizations` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `DevsOnDeck`.`skills_of_positions`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `DevsOnDeck`.`skills_of_positions` ;

CREATE TABLE IF NOT EXISTS `DevsOnDeck`.`skills_of_positions` (
  `skill_id` INT NOT NULL,
  `position_id` INT NOT NULL,
  INDEX `fk_skills_has_positions_positions1_idx` (`position_id` ASC) VISIBLE,
  INDEX `fk_skills_has_positions_skills1_idx` (`skill_id` ASC) VISIBLE,
  PRIMARY KEY (`skill_id`, `position_id`),
  CONSTRAINT `fk_skills_has_positions_skills1`
    FOREIGN KEY (`skill_id`)
    REFERENCES `DevsOnDeck`.`skills` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_skills_has_positions_positions1`
    FOREIGN KEY (`position_id`)
    REFERENCES `DevsOnDeck`.`positions` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
