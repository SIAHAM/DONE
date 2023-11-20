CREATE TABLE IF NOT EXISTS analyse_prix(
      code_commune VARCHAR(10),
      prix_moyen FLOAT
    );

CREATE TABLE IF NOT EXISTS departements (
    num_dep VARCHAR(2) PRIMARY KEY,
    dep_name VARCHAR(50),
    region_name VARCHAR(50)
   );

