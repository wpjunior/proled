-- -----------------------------------------------------
-- Alter Table `interlegis`.`ordem_dia`
-- -----------------------------------------------------

ALTER TABLE `interlegis`.`ordem_dia`
    ADD COLUMN `txt_resultado` TEXT  AFTER `ind_excluido`,
    ADD COLUMN `tip_votacao` INT(11)  NOT NULL AFTER `txt_resultado`;

ALTER TABLE `interlegis`.`materia_legislativa`
    MODIFY COLUMN `num_origem_externa` VARCHAR(9) DEFAULT NULL,
    MODIFY COLUMN `num_ident_basica` VARCHAR(6) NOT NULL;

ALTER TABLE `interlegis`.`numeracao`
    MODIFY COLUMN `num_materia` VARCHAR(6) NOT NULL;

    
ALTER TABLE `interlegis`.`proposicao` MODIFY COLUMN `dat_envio` DATETIME  NOT NULL,
    MODIFY COLUMN `dat_recebimento` DATETIME  DEFAULT NULL,
    MODIFY COLUMN `dat_devolucao` DATETIME  DEFAULT NULL,
    ADD COLUMN `num_proposicao` INTEGER  DEFAULT NULL AFTER `txt_justif_devolucao`;
	
ALTER TABLE `interlegis`.`ordem_dia` ADD COLUMN `cod_sessao_plen` INTEGER  NOT NULL AFTER `cod_ordem`;

ALTER TABLE `interlegis`.`comissao` ADD COLUMN `dat_extincao` DATE  AFTER `dat_criacao`;

ALTER TABLE `interlegis`.`parlamentar` ADD COLUMN `ind_unid_deliberativa` TINYINT(4) NOT NULL AFTER `ind_ativo`;

ALTER TABLE `interlegis`.`unidade_tramitacao` ADD COLUMN `cod_parlamentar` INT(11) NOT NULL AFTER `cod_orgao`;

-- -----------------------------------------------------
-- Table `interlegis`.`sessao_plenaria`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `interlegis`.`sessao_plenaria` ;

CREATE  TABLE IF NOT EXISTS `interlegis`.`sessao_plenaria` (
  `cod_sessao_plen` INT(11) NOT NULL AUTO_INCREMENT ,
  `cod_andamento_sessao` INT(11) NULL ,
  `tip_sessao` TINYINT(4) NOT NULL ,
  `cod_sessao_leg` INT(11) NOT NULL ,
  `num_legislatura` INT(11) NOT NULL ,
  `tip_expediente` VARCHAR(10) NOT NULL ,
  `dat_inicio_sessao` DATE NOT NULL ,
  `dia_sessao` VARCHAR(15) NOT NULL ,
  `hr_inicio_sessao` VARCHAR(5) NOT NULL ,
  `hr_fim_sessao` VARCHAR(5) NULL ,
  `num_sessao_plen` INT(11) UNSIGNED NOT NULL ,
  `dat_fim_sessao` DATE NULL ,
  `ind_excluido` TINYINT(4) NOT NULL default '0' ,
  PRIMARY KEY (`cod_sessao_plen`) ,
  CONSTRAINT `fk_{B66AB9CE-C220-4D54-A8FF-9CA3E3DDB740}`
    FOREIGN KEY (`cod_sessao_leg` )
    REFERENCES `interlegis`.`sessao_legislativa` (`cod_sessao_leg` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_{039D36D8-2672-497E-9DA8-0CD4C69B678E}`
    FOREIGN KEY (`tip_sessao` )
    REFERENCES `interlegis`.`tipo_sessao_plenaria` (`tip_sessao` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_{6729818C-6E9B-4F54-8AFD-D43E610D2345}`
    FOREIGN KEY (`cod_andamento_sessao` )
    REFERENCES `interlegis`.`andamento_sessao` (`cod_andamento_sessao` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
PACK_KEYS = 0
ROW_FORMAT = DEFAULT;

INSERT INTO sessao_plenaria VALUES(0,0,0,0,0,0,'0000-00-00','','00:00','00:00',0,'0000-00-00',0);
UPDATE sessao_plenaria SET cod_sessao_plen = 0;

-- -----------------------------------------------------
-- Table `interlegis`.`tipo_sessao_plenaria`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `interlegis`.`tipo_sessao_plenaria` ;

CREATE  TABLE IF NOT EXISTS `interlegis`.`tipo_sessao_plenaria` (
  `tip_sessao` TINYINT(4) NOT NULL AUTO_INCREMENT ,
  `nom_sessao` VARCHAR(30) NOT NULL ,
  `ind_excluido` TINYINT(4) NOT NULL default '0' ,
  `num_minimo` INT(11) NOT NULL ,
  PRIMARY KEY (`tip_sessao`) )
PACK_KEYS = 0
ROW_FORMAT = DEFAULT;

-- -----------------------------------------------------
-- Table `interlegis`.`andamento_sessao`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `interlegis`.`andamento_sessao` ;

CREATE  TABLE IF NOT EXISTS `interlegis`.`andamento_sessao` (
  `cod_andamento_sessao` INT(11) NOT NULL AUTO_INCREMENT ,
  `nom_andamento` VARCHAR(100) NOT NULL ,
  `ind_excluido` TINYINT(4) UNSIGNED NOT NULL ,
  PRIMARY KEY (`cod_andamento_sessao`) )
PACK_KEYS = 0
ROW_FORMAT = DEFAULT;

-- -----------------------------------------------------
-- Table `interlegis`.`tipo_resultado_votacao`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `interlegis`.`tipo_resultado_votacao` ;

CREATE  TABLE IF NOT EXISTS `interlegis`.`tipo_resultado_votacao` (
  `tip_resultado_votacao` INT UNSIGNED NOT NULL AUTO_INCREMENT ,
  `nom_resultado` VARCHAR(100) NOT NULL ,
  `ind_excluido` TINYINT(4) UNSIGNED NOT NULL ,
  PRIMARY KEY (`tip_resultado_votacao`) )
PACK_KEYS = 0
ROW_FORMAT = DEFAULT;

-- -----------------------------------------------------
-- Table `interlegis`.`registro_votacao`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `interlegis`.`registro_votacao` ;

CREATE  TABLE IF NOT EXISTS `interlegis`.`registro_votacao` (
  `cod_votacao` INT(11) NOT NULL AUTO_INCREMENT ,
  `tip_resultado_votacao` INT UNSIGNED NOT NULL ,
  `cod_materia` INT(11) NOT NULL ,
  `cod_ordem` INT(11) NOT NULL ,
  `num_votos_sim` TINYINT(4) UNSIGNED NOT NULL ,
  `num_votos_nao` TINYINT(4) UNSIGNED NOT NULL ,
  `num_abstencao` TINYINT(4) UNSIGNED NOT NULL ,
  `txt_observacao` TEXT ,
  `ind_excluido` TINYINT(4) UNSIGNED NOT NULL ,
  PRIMARY KEY (`cod_votacao`) ,
  CONSTRAINT `fk_{70A39BB5-1A1F-4A39-A420-60F127A58F27}`
    FOREIGN KEY (`cod_ordem` )
    REFERENCES `interlegis`.`ordem_dia` (`cod_ordem` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_{32117E29-146C-4C59-A7DA-23DE5E48C69D}`
    FOREIGN KEY (`cod_materia` )
    REFERENCES `interlegis`.`materia_legislativa` (`cod_materia` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_{5BE62220-4750-4C6B-91FC-F1007F222354}`
    FOREIGN KEY (`tip_resultado_votacao` )
    REFERENCES `interlegis`.`tipo_resultado_votacao` (`tip_resultado_votacao` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
PACK_KEYS = 0
ROW_FORMAT = DEFAULT;

-- -----------------------------------------------------
-- Table `interlegis`.`sessao_plenaria_presenca`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `interlegis`.`sessao_plenaria_presenca` ;

CREATE  TABLE IF NOT EXISTS `interlegis`.`sessao_plenaria_presenca` (
  `cod_sessao_plen` INT(11) NOT NULL ,
  `cod_parlamentar` INT(11) NOT NULL ,
  `ind_excluido` TINYINT(4) UNSIGNED NULL ,
  PRIMARY KEY (`cod_sessao_plen`, `cod_parlamentar`) ,
  CONSTRAINT `fk_{081D831E-A85E-47DF-B026-63CDDC5B7199}`
    FOREIGN KEY (`cod_sessao_plen` )
    REFERENCES `interlegis`.`sessao_plenaria` (`cod_sessao_plen` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_{DC33E098-6E15-45BD-B505-78B0A05562F8}`
    FOREIGN KEY (`cod_parlamentar` )
    REFERENCES `interlegis`.`parlamentar` (`cod_parlamentar` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
PACK_KEYS = 0
ROW_FORMAT = DEFAULT;

-- -----------------------------------------------------
-- Table `interlegis`.`ordem_dia_presenca`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `interlegis`.`ordem_dia_presenca` ;

CREATE  TABLE IF NOT EXISTS `interlegis`.`ordem_dia_presenca` (
  `cod_parlamentar` INT(11) NOT NULL ,
  `ind_excluido` TINYINT(4) UNSIGNED NOT NULL ,
  `dat_ordem` DATE NOT NULL ,
  CONSTRAINT `fk_{0E3901A6-6BD1-4409-B003-C7D7E60539E1}`
    FOREIGN KEY (`cod_parlamentar` )
    REFERENCES `interlegis`.`parlamentar` (`cod_parlamentar` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
PACK_KEYS = 0
ROW_FORMAT = DEFAULT;

-- -----------------------------------------------------
-- Table `interlegis`.`oradores`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `interlegis`.`oradores` ;

CREATE  TABLE IF NOT EXISTS `interlegis`.`oradores` (
  `cod_sessao_plen` INT(11) NOT NULL ,
  `cod_parlamentar` INT(11) NOT NULL ,
  `num_ordem` TINYINT(4) NOT NULL ,
  `ind_excluido` TINYINT(4) NOT NULL default '0' ,
  PRIMARY KEY (`cod_sessao_plen`, `cod_parlamentar`) ,
  CONSTRAINT `fk_{74E12698-59FC-474E-9544-01984B69BC7C}`
    FOREIGN KEY (`cod_sessao_plen` )
    REFERENCES `interlegis`.`sessao_plenaria` (`cod_sessao_plen` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_{A63E6611-A33C-4831-976E-64D1DCF51F7D}`
    FOREIGN KEY (`cod_parlamentar` )
    REFERENCES `interlegis`.`parlamentar` (`cod_parlamentar` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
PACK_KEYS = 0
ROW_FORMAT = DEFAULT;

-- -----------------------------------------------------
-- Table `interlegis`.`mesa_sessao_plenaria`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `interlegis`.`mesa_sessao_plenaria` ;

CREATE  TABLE IF NOT EXISTS `interlegis`.`mesa_sessao_plenaria` (
  `cod_cargo` TINYINT(4) NOT NULL ,
  `cod_sessao_leg` INT(11) NOT NULL ,
  `cod_parlamentar` INT(11) NOT NULL ,
  `cod_sessao_plen` INT(11) NOT NULL ,
  `ind_excluido` TINYINT(4) UNSIGNED NULL ,
  PRIMARY KEY (`cod_cargo`, `cod_sessao_leg`, `cod_parlamentar`, `cod_sessao_plen`) ,
  CONSTRAINT `fk_{8CAD6510-37F8-4BBC-ACF3-3D7D5F0E9650}`
    FOREIGN KEY (`cod_cargo` )
    REFERENCES `interlegis`.`cargo_mesa` (`cod_cargo` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_{8515F0EE-645A-4173-9644-21EB4BAA0A5F}`
    FOREIGN KEY (`cod_sessao_leg` )
    REFERENCES `interlegis`.`sessao_legislativa` (`cod_sessao_leg` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_{1A054080-B309-48F8-AA71-74223C0DDC4B}`
    FOREIGN KEY (`cod_parlamentar` )
    REFERENCES `interlegis`.`parlamentar` (`cod_parlamentar` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_{66082FB0-63C1-4AE5-9674-4EEBAFE9C8A8}`
    FOREIGN KEY (`cod_sessao_plen` )
    REFERENCES `interlegis`.`sessao_plenaria` (`cod_sessao_plen` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
PACK_KEYS = 0
ROW_FORMAT = DEFAULT;

-- -----------------------------------------------------
-- Table `interlegis`.`tipo_expediente`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `interlegis`.`tipo_expediente` ;

CREATE  TABLE IF NOT EXISTS `interlegis`.`tipo_expediente` (
  `cod_expediente` INT(11) NOT NULL AUTO_INCREMENT ,
  `nom_expediente` VARCHAR(100) NOT NULL ,
  `ind_excluido` TINYINT(4) UNSIGNED NOT NULL ,
  PRIMARY KEY (`cod_expediente`) )
PACK_KEYS = 0
ROW_FORMAT = DEFAULT;

-- -----------------------------------------------------
-- Table `interlegis`.`expediente_sessao_plenaria`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `interlegis`.`expediente_sessao_plenaria` ;

CREATE  TABLE IF NOT EXISTS `interlegis`.`expediente_sessao_plenaria` (
  `cod_sessao_plen` INT(11) NOT NULL ,
  `cod_expediente` INT(11) NOT NULL ,
  `txt_expediente` TEXT NOT NULL ,
  `ind_excluido` TINYINT(4) NOT NULL default '0' ,
  PRIMARY KEY (`cod_sessao_plen`, `cod_expediente`) ,
  CONSTRAINT `fk_{1D13FB23-2229-4633-A69F-242C5EBB1D70}`
    FOREIGN KEY (`cod_sessao_plen` )
    REFERENCES `interlegis`.`sessao_plenaria` (`cod_sessao_plen` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_{7E6BF2B4-164F-4DD9-8AB5-5D78B3767037}`
    FOREIGN KEY (`cod_expediente` )
    REFERENCES `interlegis`.`tipo_expediente` (`cod_expediente` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
PACK_KEYS = 0
ROW_FORMAT = DEFAULT;

-- -----------------------------------------------------
-- Table `interlegis`.`registro_votacao_parlamentar`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `interlegis`.`registro_votacao_parlamentar` ;

CREATE  TABLE IF NOT EXISTS `interlegis`.`registro_votacao_parlamentar` (
  `cod_votacao` INT(11) NOT NULL ,
  `cod_parlamentar` INT(11) NOT NULL ,
  `ind_excluido` TINYINT(4) UNSIGNED NOT NULL ,
  `vot_parlamentar` VARCHAR(10) NOT NULL ,
  PRIMARY KEY (`cod_votacao`, `cod_parlamentar`) ,
  CONSTRAINT `fk_{52CE649A-52C6-45FF-99D1-15F58E4171EB}`
    FOREIGN KEY (`cod_votacao` )
    REFERENCES `interlegis`.`registro_votacao` (`cod_votacao` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_{3522BEA8-E908-455C-A2DF-EE3AB2E9527F}`
    FOREIGN KEY (`cod_parlamentar` )
    REFERENCES `interlegis`.`parlamentar` (`cod_parlamentar` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
PACK_KEYS = 0
ROW_FORMAT = DEFAULT;
