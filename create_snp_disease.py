import psycopg2

IP_ADDRESS = "Deleted"
PORT = "Deleted"
DB_NAME = "Deleted"
ID = "Deleted"
PASSWD = "Deleted"

try:
    connection = psycopg2.connect(
        dbname=DB_NAME, user=ID, password=PASSWD, host=IP_ADDRESS, port=PORT
    )
    cursor = connection.cursor()

    # DDL
    sql = "CREATE TABLE gene(\
        tax_id INTEGER NOT NULL DEFAULT 0,\
        gene_id INTEGER NOT NULL DEFAULT 0 PRIMARY KEY,\
        symbol VARCHAR(30) UNIQUE,\
        chro_num VARCHAR(20),\
        map_location VARCHAR(30),\
        description VARCHAR(50),\
        type_of_gene VARCHAR(30),\
        modified_date DATE\
        );\
        \
        CREATE TABLE snp(\
        snp_id INTEGER NOT NULL DEFAULT 0 PRIMARY KEY,\
        chro_num VARCHAR(20),\
        pos_on_Chromo BIGINT,\
        neighbor_gene VARCHAR(30),\
        anc_allele VARCHAR(5),\
        min_allele VARCHAR(5),\
        CONSTRAINT fk_gene_symbol FOREIGN KEY(neighbor_gene) REFERENCES gene(symbol)\
        );\
        CREATE TABLE disease(\
        OMIM_id INTEGER NOT NULL DEFAULT 0 PRIMARY KEY,\
        disease_name VARCHAR(50)\
        );\
        CREATE TABLE gene_disease(\
        OMIM_id INTEGER NOT NULL DEFAULT 0,\
        gene_symbol VARCHAR(30),\
        PRIMARY KEY (OMIM_id, gene_symbol),\
        CONSTRAINT fk_omim_id FOREIGN KEY(OMIM_id) REFERENCES disease(OMIM_id),\
        CONSTRAINT fk_gene_id FOREIGN KEY(gene_symbol) REFERENCES gene(symbol)\
        );\
        CREATE TABLE gene_synonyms(\
        synonyms VARCHAR(30),\
        symbol VARCHAR(30),\
        CONSTRAINT fk_synonym FOREIGN KEY(symbol) REFERENCES gene(symbol)\
        );"
    cursor.execute(sql)

    connection.close()

except psycopg2.Error as e:
    print(e)

except RuntimeError as e:
    print(e)

finally:
    connection.close()
