-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema receta
-- -----------------------------------------------------
DROP SCHEMA IF EXISTS `receta` ;

-- -----------------------------------------------------
-- Schema receta
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `receta` DEFAULT CHARACTER SET utf8 ;
USE `receta` ;

-- -----------------------------------------------------
-- Table `receta`.`users`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `receta`.`users` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `first_name` VARCHAR(255) NULL,
  `last_name` VARCHAR(255) NULL,
  `email` VARCHAR(45) NULL,
  `password` VARCHAR(45) NULL,
  `gen` VARCHAR(45) NULL,
  `birthday` VARCHAR(45) NULL,
  `created_at` DATETIME NULL DEFAULT NOW(),
  `updated_at` DATETIME NULL DEFAULT NOW(),
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `receta`.`recetas`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `receta`.`recetas` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `users_id` INT NOT NULL,
  `name` VARCHAR(255) NULL,
  `Under` ENUM("Yes", "No") NULL,
  `description` TEXT NOT NULL,
  `instruction` LONGTEXT NULL,
  `created_at` DATETIME NULL DEFAULT now(),
  `updated_at` DATETIME NULL DEFAULT now(),
  INDEX `fk_recetas_users_idx` (`users_id` ASC) VISIBLE,
  PRIMARY KEY (`id`),
  CONSTRAINT `fk_recetas_users`
    FOREIGN KEY (`users_id`)
    REFERENCES `receta`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
