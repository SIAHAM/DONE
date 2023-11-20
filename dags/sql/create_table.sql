drop  table IF EXISTS passages_corona; 
drop  table IF EXISTS departements; 
drop  table IF EXISTS tranches_dage; 

CREATE TABLE IF NOT EXISTS tranches_dage(
      Code_tranches_dage VARCHAR(10),
      Age INT,
      PRIMARY KEY (Code_tranches_dage )
    );

CREATE TABLE IF NOT EXISTS departements (
    num_dep VARCHAR(5),
    dep_name VARCHAR(50),
    region_name VARCHAR(50),
    PRIMARY KEY (num_dep)
   );

CREATE TABLE IF NOT EXISTS passages_corona (
    dep VARCHAR(5),
    date_de_passage DATE,
    sursaud_cl_age_corona INT,
    nbre_pass_corona INT,
    nbre_pass_tot INT,
    nbre_hospit_corona INT,
    nbre_pass_corona_h INT,
    nbre_pass_corona_f INT,
    nbre_pass_tot_h INT,
    nbre_pass_tot_f INT,
    nbre_hospit_corona_h INT,
    nbre_hospit_corona_f INT,
    nbre_acte_corona INT,
    nbre_acte_tot INT,
    nbre_acte_corona_h INT,
    nbre_acte_corona_f INT,
    nbre_acte_tot_h INT,
    nbre_acte_tot_f INT,
    PRIMARY KEY (date_de_passage, sursaud_cl_age_corona)

);   