USE `interlegis`;

--
--
-- Table structure for table `ordem_dia_presenca`   --- alterações em 16/07/2010 ---
--
-- Esta atualização deve ser aplicada por aqueles que tenham instalado o SAPL versão 2.3 antes de 16/07/2010.
-- Caso a instalação tenha sido feita após esta data, não há a necessidade de rodar este script, pois esta correção já consta na definição das tabelas do banco no arquivo sapl.sql.
--
-- Alteração feita para atender a possibilidade de se ter mais de uma sessão plenaria no dia
--
--

ALTER TABLE `ordem_dia_presenca` 
   ADD COLUMN `cod_sessao_plen` int(11) DEFAULT 0 NOT NULL;

ALTER TABLE `ordem_dia_presenca` 
   ADD COLUMN `cod_presenca_ordem_dia` int(11) NOT NULL AUTO_INCREMENT;

ALTER TABLE `ordem_dia_presenca` 
   ADD PRIMARY KEY (`cod_presenca_ordem_dia`);

ALTER TABLE `ordem_dia_presenca` 
   ADD KEY `idx_orddiapres_sessao_plenaria` (`cod_sessao_plen`);

--
-- Dumping data for table `ordem_dia_presenca`
--
LOCK TABLES `ordem_dia_presenca` WRITE;
\*!40000 ALTER TABLE `ordem_dia_presenca` DISABLE KEYS */;
\*!40000 ALTER TABLE `ordem_dia_presenca` ENABLE KEYS  */;
UNLOCK TABLES;

--
--                                              --- fim das alterações 16/07/2010 ---
--

