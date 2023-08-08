import psycopg2

IP_ADDRESS = "Deleted"
PORT = "Deleted"
DB_NAME = "Deleted"
ID = "Deleted"
PASSWD = "Deleted"


def createTable():
    try:
        connection = psycopg2.connect(
            dbname=DB_NAME, user=ID, password=PASSWD, host=IP_ADDRESS, port=PORT
        )
        cursor = connection.cursor()

        # DDL
        sql = "CREATE TABLE gene(\
          tax_id INTEGER NOT NULL DEFAULT 0,\
          gene_id INTEGER NOT NULL DEFAULT 0,\
          symbol VARCHAR(30) NOT NULL,\
          chro_num VARCHAR(20),\
          map_location VARCHAR(50),\
          description VARCHAR(200),\
          type_of_gene VARCHAR(30),\
          modified_date DATE,\
          PRIMARY KEY(gene_id)\
          );\
          \
          CREATE TABLE gene_synonyms(\
          synonyms VARCHAR(50) NOT NULL,\
          gene_id INTEGER,\
          PRIMARY KEY(synonyms, gene_id),\
          FOREIGN KEY(gene_id) REFERENCES gene(gene_id) ON DELETE CASCADE\
          );\
          \
          CREATE TABLE snp(\
          snp_id INTEGER NOT NULL DEFAULT 0,\
          chro_num VARCHAR(4),\
          pos_on_Chromo INT,\
          neighbor_gene VARCHAR(30),\
          anc_allele VARCHAR(4),\
          min_allele VARCHAR(4),\
          PRIMARY KEY(snp_id)\
          );\
          \
          CREATE TABLE disease(\
          OMIM_id INTEGER NOT NULL DEFAULT 0,\
          disease_name VARCHAR(200),\
          PRIMARY KEY(OMIM_id)\
          );\
          CREATE TABLE gene_disease(\
          OMIM_id INTEGER NOT NULL DEFAULT 0,\
          gene_symbol VARCHAR(30) NOT NULL,\
          PRIMARY KEY (OMIM_id, gene_symbol)\
          );\
          "
        cursor.execute(sql)
        connection.commit()
        connection.close()

    except psycopg2.Error as e:
        print(e)

    except RuntimeError as e:
        print(e)

    finally:
        connection.close()
    return


def createIndex():
    try:
        connection = psycopg2.connect(
            dbname=DB_NAME, user=ID, password=PASSWD, host=IP_ADDRESS, port=PORT
        )
        cursor = connection.cursor()

        sql = "\
          CREATE INDEX ix_gene_id ON gene_synonyms(gene_id);\
          CREATE INDEX ix_neighbor_gene ON snp(neighbor_gene);\
          CREATE INDEX ix_disease_name ON disease(disease_name);\
          "
        cursor.execute(sql)
        connection.commit()
        connection.close()

    except psycopg2.Error as e:
        print(e)

    except RuntimeError as e:
        print(e)

    finally:
        connection.close()
    return


dir_path = "/work/home/bis332/bio_data/"
# disease_OMIM.txt  gene_OMIM.txt  Homo_sapiens_gene_info.txt  SNP.txt


def insertDisease():
    filename = dir_path + "disease_OMIM.txt"
    with open(filename) as file:
        # disease_OMIM_ID disease_name
        header = file.readline()
        try:
            connection = psycopg2.connect(
                dbname=DB_NAME, user=ID, password=PASSWD, host=IP_ADDRESS, port=PORT
            )
            cursor = connection.cursor()

            for line in file:
                values = line.strip().split("\t")
                sql = f"INSERT INTO disease (OMIM_id, disease_name) values ({int(values[0])}, '{values[1].replace('$','').replace('[','').replace(']','')}');"
                cursor.execute(sql)

            connection.commit()
            connection.close()

        except psycopg2.Error as e:
            print(e)

        except RuntimeError as e:
            print(e)

        finally:
            connection.close()

        file.close()
    return


def insertGene():
    filename = dir_path + "Homo_sapiens_gene_info.txt"
    with open(filename) as file:
        # tax_id GeneID  Symbol  Synonyms        chromosome      map_location    description     type_of_gene    Modification_date
        # 0        1       2      3                   4              5              6                7                8
        header = file.readline()
        try:
            connection = psycopg2.connect(
                dbname=DB_NAME, user=ID, password=PASSWD, host=IP_ADDRESS, port=PORT
            )
            cursor = connection.cursor()

            for line in file:
                values = line.strip().split("\t")
                sql = f"INSERT INTO gene (tax_id, gene_id, symbol, chro_num, map_location, description, type_of_gene, modified_date) \
                Values ({int(values[0])}, {int(values[1])}, '{values[2]}', '{values[4]}', '{values[5]}', '{values[6].replace('$','')}', '{values[7]}', '{values[8][:4]+'-'+values[8][4:6]+'-'+values[8][6:]}');"
                cursor.execute(sql)
                if values[3] != "-":
                    for synonym in values[3].split("|"):
                        sql = f"INSERT INTO gene_synonyms (synonyms, gene_id) VALUES ('{synonym}', {int(values[1])});"
                        cursor.execute(sql)
                # else:
            connection.commit()
            connection.close()

        except psycopg2.Error as e:
            print(e)

        except RuntimeError as e:
            print(e)

        finally:
            connection.close()

        file.close()
    return


def insertDG():
    filename = dir_path + "gene_OMIM.txt"
    with open(filename) as file:
        # gene_symbol     disease_OMIM_ID
        #   0                 1
        header = file.readline()
        try:
            connection = psycopg2.connect(
                dbname=DB_NAME, user=ID, password=PASSWD, host=IP_ADDRESS, port=PORT
            )
            cursor = connection.cursor()

            for line in file:
                values = line.strip().split("\t")
                sql = f"INSERT INTO gene_disease (gene_symbol, OMIM_id) values ('{values[0]}', '{values[1]}');"
                cursor.execute(sql)

            connection.commit()
            connection.close()

        except psycopg2.Error as e:
            print(e)

        except RuntimeError as e:
            print(e)

        finally:
            connection.close()

        file.close()
    return


def insertSNP():
    filename = dir_path + "SNP.txt"
    with open(filename) as file:
        # SNP id  Chromosome      Position of SNP on the chromosome       Genes at the same position on the chromosome    Ancestral allele        Minor allele
        # 0         1                     2                                         3                                         4                       5
        header = file.readline()
        try:
            connection = psycopg2.connect(
                dbname=DB_NAME, user=ID, password=PASSWD, host=IP_ADDRESS, port=PORT
            )
            cursor = connection.cursor()

            for line in file:
                values = line.strip().split("\t")
                sql = f"INSERT INTO snp (snp_id, chro_num, pos_on_Chromo, neighbor_gene, anc_allele, min_allele) \
                Values ({int(values[0])}, '{values[1]}', {int(values[2])}, '{values[3]}', '{values[4]}', '{values[5]}');"
                cursor.execute(sql)

            connection.commit()
            connection.close()

        except psycopg2.Error as e:
            print(e)

        except RuntimeError as e:
            print(e)

        finally:
            connection.close()

        file.close()
    return


# e.g. update professor set pid='6', dep='103' from professor where name='F' AND id='1234';
def updateRecord(table, kwargs):
    # **kwargs = {set_attribute: [attr1, attr2, ...], set_value: [val1, val2, ...], cond: [cond_attr1, cond_attr2, ...], cond_val: [cond_val1, cond_val2, ...]}
    try:
        connection = psycopg2.connect(
            dbname=DB_NAME, user=ID, password=PASSWD, host=IP_ADDRESS, port=PORT
        )
        cursor = connection.cursor()

        updatesql = "UPDATE " + table
        setsql = " SET " + ", ".join(
            [
                attr + " = " + f"'{val}'"
                for attr, val in zip(kwargs["set_attribute"], kwargs["set_value"])
            ]
        )
        wheresql = " WHERE " + " AND ".join(
            [
                attribute + f" = '{value}'"
                for attribute, value in zip(kwargs["cond"], kwargs["cond_val"])
            ]
        )
        sql = updatesql + setsql + wheresql + " RETURNING *;"

        cursor.execute(sql)

        results = cursor.fetchall()
        for result in results:
            print("Updated: " + str(result))

        connection.commit()
        connection.close()

    except psycopg2.Error as e:
        print(e)

    except RuntimeError as e:
        print(e)

    finally:
        connection.close()
    return


# e.g. DELTE FROM professor where pid='6' AND dep='103'
def deleteRecord(table, kwargs):
    # **kwargs = {attribute: [attr1, attr2, ...], value: [val1, val2, ...]}
    try:
        connection = psycopg2.connect(
            dbname=DB_NAME, user=ID, password=PASSWD, host=IP_ADDRESS, port=PORT
        )
        cursor = connection.cursor()

        wheresql = " WHERE " + " AND ".join(
            [
                attribute + f" = '{value}'"
                for attribute, value in zip(kwargs["attribute"], kwargs["value"])
            ]
        )
        sql = "DELETE FROM " + table + wheresql + " RETURNING *;"
        cursor.execute(sql)

        results = cursor.fetchall()
        for result in results:
            print("Deleted: " + str(result))

        connection.commit()
        connection.close()

    except psycopg2.Error as e:
        print(e)

    except RuntimeError as e:
        print(e)

    finally:
        connection.close()
    return


# e.g. INSERT INTO professor (pid, name) VALUES (1, kim)
def insertRecord(table, kwargs):
    # kwargs = {attribute: [attr1, attr2, ...], value: [val1, val2, ...]}
    try:
        connection = psycopg2.connect(
            dbname=DB_NAME, user=ID, password=PASSWD, host=IP_ADDRESS, port=PORT
        )
        cursor = connection.cursor()

        def addquote(x):
            return "'" + str(x) + "'"

        sql = f"INSERT INTO {table} ({', '.join(kwargs['attribute'])}) Values ({', '.join(map(addquote, kwargs['value']))}) RETURNING *;"
        cursor.execute(sql)

        results = cursor.fetchall()
        for result in results:
            print("Inserted: " + str(result))

        connection.commit()
        connection.close()

    except psycopg2.Error as e:
        print(e)

    except RuntimeError as e:
        print(e)

    finally:
        connection.close()
    return


def searchGenebySymbol(symbol):
    try:
        connection = psycopg2.connect(
            dbname=DB_NAME, user=ID, password=PASSWD, host=IP_ADDRESS, port=PORT
        )
        cursor = connection.cursor()

        sql = f"SELECT gene.*, STRING_AGG(gene_synonyms.synonyms, ', ') FROM gene LEFT JOIN gene_synonyms ON gene.gene_id = gene_synonyms.gene_id \
              WHERE gene.symbol = '{symbol}' OR gene_synonyms.gene_id IN (\
              SELECT gene_id FROM gene_synonyms WHERE synonyms = '{symbol}') GROUP BY gene.gene_id;"
        cursor.execute(sql)

        rs = cursor.fetchall()
        for r in rs:
            print(r)

        connection.close()

    except psycopg2.Error as e:
        print(e)

    except RuntimeError as e:
        print(e)

    finally:
        connection.close()
    return


def searchGenebyChro(chro_num):
    try:
        connection = psycopg2.connect(
            dbname=DB_NAME, user=ID, password=PASSWD, host=IP_ADDRESS, port=PORT
        )
        cursor = connection.cursor()

        sql = f"SELECT DISTINCT symbol FROM gene WHERE chro_num = '{chro_num}';"
        cursor.execute(sql)

        rs = cursor.fetchall()

        print(",".join([str(r[0]) for r in rs]))

        connection.close()

    except psycopg2.Error as e:
        print(e)

    except RuntimeError as e:
        print(e)

    finally:
        connection.close()
    return


def searchGenebyId(gene_id):
    try:
        connection = psycopg2.connect(
            dbname=DB_NAME, user=ID, password=PASSWD, host=IP_ADDRESS, port=PORT
        )
        cursor = connection.cursor()

        sql = f"SELECT gene.*, STRING_AGG(gene_synonyms.synonyms, ', ') FROM gene LEFT JOIN gene_synonyms ON gene.gene_id = gene_synonyms.gene_id WHERE gene.gene_id = '{gene_id}' GROUP BY gene.gene_id;"
        cursor.execute(sql)

        rs = cursor.fetchall()
        for r in rs:
            print(r)

        connection.close()

    except psycopg2.Error as e:
        print(e)

    except RuntimeError as e:
        print(e)

    finally:
        connection.close()
    return


def searchSNPbyId(snp_id):
    try:
        connection = psycopg2.connect(
            dbname=DB_NAME, user=ID, password=PASSWD, host=IP_ADDRESS, port=PORT
        )
        cursor = connection.cursor()

        sql = f"SELECT * FROM SNP WHERE snp_id = '{snp_id}';"
        cursor.execute(sql)

        rs = cursor.fetchall()
        for r in rs:
            print(r)

        connection.close()

    except psycopg2.Error as e:
        print(e)

    except RuntimeError as e:
        print(e)

    finally:
        connection.close()
    return


def searchSNPbyGene(neighbor_gene):
    try:
        connection = psycopg2.connect(
            dbname=DB_NAME, user=ID, password=PASSWD, host=IP_ADDRESS, port=PORT
        )
        cursor = connection.cursor()

        # 1. search synonyms, gene symbol of symbol
        subsql = f"SELECT gene_synonyms.synonyms FROM gene NATURAL JOIN gene_synonyms \
              WHERE gene.symbol = '{neighbor_gene}' OR gene_synonyms.gene_id IN (\
              SELECT gene_id FROM gene_synonyms WHERE synonyms = '{neighbor_gene}') UNION SELECT gene.symbol FROM gene NATURAL JOIN gene_synonyms \
              WHERE gene.symbol = '{neighbor_gene}' OR gene_synonyms.gene_id IN (\
              SELECT gene_id FROM gene_synonyms WHERE synonyms = '{neighbor_gene}')"

        # 2. search snp by gene symbol and its synonyms
        sql = f"SELECT * FROM SNP WHERE neighbor_gene = ANY (" + subsql + ");"

        cursor.execute(sql)

        rs = cursor.fetchall()
        for r in rs:
            print(r)

        connection.close()

    except psycopg2.Error as e:
        print(e)

    except RuntimeError as e:
        print(e)

    finally:
        connection.close()
    return


def searchSNPbyDisease(disease_name):
    try:
        connection = psycopg2.connect(
            dbname=DB_NAME, user=ID, password=PASSWD, host=IP_ADDRESS, port=PORT
        )
        cursor = connection.cursor()

        # 1. search omim_id by disease_name
        # 2. search neighbor_gene by omim_id
        sql = f"SELECT gene_symbol FROM gene_disease WHERE omim_id = (SELECT OMIM_id FROM disease WHERE disease_name = '{disease_name}');"
        cursor.execute(sql)
        neighbor_gene = cursor.fetchone()[0]

        # 3. search snp by neighbor_gene and its synonyms
        subsql = f"SELECT gene_synonyms.synonyms FROM gene LEFT JOIN gene_synonyms ON gene.gene_id = gene_synonyms.gene_id \
              WHERE gene.symbol = '{neighbor_gene}' OR gene_synonyms.gene_id IN (\
              SELECT gene_id FROM gene_synonyms WHERE synonyms = '{neighbor_gene}') UNION SELECT gene.symbol FROM gene LEFT JOIN gene_synonyms ON gene.gene_id = gene_synonyms.gene_id \
              WHERE gene.symbol = '{neighbor_gene}' OR gene_synonyms.gene_id IN (\
              SELECT gene_id FROM gene_synonyms WHERE synonyms = '{neighbor_gene}')"

        sql = f"SELECT * FROM SNP WHERE neighbor_gene = ANY (" + subsql + ");"
        cursor.execute(sql)

        rs = cursor.fetchall()

        print(",".join([str(r[0]) for r in rs]))

        connection.close()

    except psycopg2.Error as e:
        print(e)

    except RuntimeError as e:
        print(e)

    finally:
        connection.close()
    return


def searchDiseasebyName(disease_name):
    try:
        connection = psycopg2.connect(
            dbname=DB_NAME, user=ID, password=PASSWD, host=IP_ADDRESS, port=PORT
        )
        cursor = connection.cursor()

        sql = f"SELECT OMIM_id, disease_name, STRING_AGG(gene_disease.gene_symbol,', ') FROM disease NATURAL JOIN gene_disease WHERE disease.disease_name = '{disease_name}' GROUP BY omim_id;"
        cursor.execute(sql)

        rs = cursor.fetchall()
        for r in rs:
            print(r)

        connection.close()

    except psycopg2.Error as e:
        print(e)

    except RuntimeError as e:
        print(e)

    finally:
        connection.close()
    return


def searchDiseasebyGene(symbol):
    try:
        connection = psycopg2.connect(
            dbname=DB_NAME, user=ID, password=PASSWD, host=IP_ADDRESS, port=PORT
        )
        cursor = connection.cursor()

        # 1. search synonyms, gene symbol of symbol
        subsql = f"SELECT gene_synonyms.synonyms FROM gene NATURAL JOIN gene_synonyms \
              WHERE gene.symbol = '{symbol}' OR gene_synonyms.gene_id IN (\
              SELECT gene_id FROM gene_synonyms WHERE synonyms = '{symbol}') UNION SELECT gene.symbol FROM gene NATURAL JOIN gene_synonyms \
              WHERE gene.symbol = '{symbol}' OR gene_synonyms.gene_id IN (\
              SELECT gene_id FROM gene_synonyms WHERE synonyms = '{symbol}')"

        # 2. search disease by any symbol and its synonyms
        sql = (
            f"SELECT OMIM_id, disease_name, STRING_AGG(gene_disease.gene_symbol,', ') FROM disease NATURAL JOIN gene_disease WHERE gene_disease.gene_symbol = ANY ("
            + subsql
            + ") GROUP BY omim_id;"
        )
        cursor.execute(sql)

        rs = cursor.fetchall()

        for r in rs:
            print(r)

        connection.close()

    except psycopg2.Error as e:
        print(e)

    except RuntimeError as e:
        print(e)

    finally:
        connection.close()

    return


def searchDiseasebySNP(snp_id):
    try:
        connection = psycopg2.connect(
            dbname=DB_NAME, user=ID, password=PASSWD, host=IP_ADDRESS, port=PORT
        )
        cursor = connection.cursor()

        # search neighbor_gene, chro_num by snp
        sql = f"SELECT neighbor_gene, chro_num FROM snp WHERE snp_id = {snp_id};"
        cursor.execute(sql)
        neighbor_gene, chro_num = cursor.fetchone()

        # 1. search synonyms, symbol of neighbor_gene with same chro_num
        # 2. search omim_id by gene symbol
        # 3. search disease_name by omim_id
        sql = f"SELECT OMIM_id, disease_name, STRING_AGG(gene_disease.gene_symbol,', ') FROM disease NATURAL JOIN gene_disease WHERE OMIM_id in \
            (SELECT OMIM_id FROM gene_disease WHERE gene_symbol in \
              (SELECT gene_synonyms.synonyms FROM gene NATURAL JOIN gene_synonyms \
              WHERE gene.chro_num = '{chro_num}' AND (gene.symbol = '{neighbor_gene}' OR gene_synonyms.gene_id IN (\
              SELECT gene_id FROM gene_synonyms WHERE synonyms = '{neighbor_gene}')) UNION SELECT gene.symbol FROM gene NATURAL JOIN gene_synonyms \
              WHERE gene.chro_num = '{chro_num}' AND (gene.symbol = '{neighbor_gene}' OR gene_synonyms.gene_id IN (\
              SELECT gene_id FROM gene_synonyms WHERE synonyms = '{neighbor_gene}')))) GROUP BY omim_id ORDER BY disease_name ; "
        cursor.execute(sql)

        rs = cursor.fetchall()
        for r in rs:
            print(r)

        connection.close()

    except psycopg2.Error as e:
        print(e)

    except RuntimeError as e:
        print(e)

    finally:
        connection.close()
    return


def showStatistics():
    try:
        connection = psycopg2.connect(
            dbname=DB_NAME, user=ID, password=PASSWD, host=IP_ADDRESS, port=PORT
        )
        cursor = connection.cursor()

        print("(relname, # of live tuples, # of inserts, # of updates, # of deletions)")
        sql = "SELECT relname, n_live_tup, n_tup_ins, n_tup_upd, n_tup_del FROM pg_stat_user_tables;"
        cursor.execute(sql)
        rs = cursor.fetchall()
        for r in rs:
            print(r)

        connection.close()

    except psycopg2.Error as e:
        print(e)

    except RuntimeError as e:
        print(e)

    finally:
        connection.close()
    return


# 고쳐야 될 것
# 3. ui 매끄럽게

if __name__ == "__main__":
    # create table and index
    createTable()
    createIndex()
    # insert data from file
    insertGene()
    insertDisease()
    insertSNP()
    insertDG()

    # greeting
    print("------------------------------")
    print("BIPro Spring Class 2023-05-10")
    print("Hello ! we are team 6")
    print("------------------------------")
    active = True
    while active:
        # print option
        print(
            "1: SearchGeneBySymbol - Given a gene symbol, find all gene information",
            "2: SearchGeneByChro - Given a chromosome id, find all gene symbols located in the chromosome",
            "3: SearchGeneById - Given a gene id, find all gene information",
            sep="\n",
        )
        print(
            "4: SearchSNPById - Given a SNP ID, find all diseases associated with the SNP",
            "5: SearchSNPByGene - Given a gene, serach SNPs occuring in the gene",
            "6: SearchSNPByDisease - Given a disease name, find all SNP IDs associated with the disease",
            sep="\n",
        )
        print(
            "7: SearchDiseaseByName - Given a disease_name, find all OMIM data",
            "8: SearchDiseaseByGene - Give a gene symbol, find all OMIM data",
            "9: SearchDiseaseBySNP - Given a SNP ID, find all disease names associated with the SNP",
            sep="\n",
        )
        print(
            "i: insert", "u: update", "d: delete", "s: statistics", "e: exit", sep="\n"
        )
        print("Enter option you want to execute: ")
        print("------------------------------")
        x = input()
        if x == "u":
            cond = {"set_attribute": [], "set_value": [], "cond": [], "cond_val": []}
            print("table options : gene / gene_synonyms / snp / disease / gene_disease")
            print("Enter table name: ")
            tableName = input()
            if tableName == "gene":
                print(
                    "attribute options : tax_id / gene_id / symbol / chro_num / map_location / description / type_of_gene / modified_date"
                )
            if tableName == "gene_synonyms":
                print("attribute options : synonyms / gene_id")
            if tableName == "snp":
                print(
                    "attribute options : snp_id / chro_num / pos_on_Chromo / neighbor_gene / anc_allele / min_allele"
                )
            if tableName == "disease":
                print("attribute options : OMIM_id / disease_name")
            if tableName == "gene_disease":
                print("attribute options : OMIM_id / gene_symbol")
            print("Enter conditional attributes in csv format (attr1,attr2,...): ")
            cond["cond"] = input().split(",")
            for attr in cond["cond"]:
                print(f"Enter value for {attr}: ")
                cond["cond_val"].append(input())
            print("Enter attributes to update in csv format (attr1,attr2,...): ")
            cond["set_attribute"] = input().split(",")
            for attr in cond["set_attribute"]:
                if attr == "modified_date":
                    print("Please enter date in YYYY-MM-DD format")
                else:
                    print(f"Enter value for {attr}: ")
                cond["set_value"].append(input())
            updateRecord(tableName, cond)

        elif x == "d":
            cond = {"attribute": [], "value": []}
            print("table options : gene / gene_synonyms / snp / disease / gene_disease")
            print("Enter table name: ")
            tableName = input()
            if tableName == "gene":
                print(
                    "attribute options : tax_id / gene_id / symbol / chro_num / map_location / description / type_of_gene / modified_date"
                )
            if tableName == "gene_synonyms":
                print("attribute options : synonyms / gene_id")
            if tableName == "snp":
                print(
                    "attribute options : snp_id / chro_num / pos_on_Chromo / neighbor_gene / anc_allele / min_allele"
                )
            if tableName == "disease":
                print("attribute options : OMIM_id / disease_name")
            if tableName == "gene_disease":
                print("attribute options : OMIM_id / gene_symbol")
            print("Enter attributes in csv format (attr1,attr2,...): ")
            cond["attribute"] = input().strip().split(",")
            for attr in cond["attribute"]:
                print(f"Enter value for {attr}: ")
                cond["value"].append(input())
            deleteRecord(tableName, cond)

        elif x == "i":
            cond = {"attribute": [], "value": []}
            print("table options : gene / gene_synonyms / snp / disease / gene_disease")
            print("Enter table name: ")
            tableName = input()
            if tableName == "gene":
                print(
                    "attribute options : tax_id / gene_id / symbol / chro_num / map_location / description / type_of_gene / modified_date"
                )
            if tableName == "gene_synonyms":
                print("attribute options : synonyms / gene_id")
            if tableName == "snp":
                print(
                    "attribute options : snp_id / chro_num / pos_on_Chromo / neighbor_gene / anc_allele / min_allele"
                )
            if tableName == "disease":
                print("attribute options : OMIM_id / disease_name")
            if tableName == "gene_disease":
                print("attribute options : OMIM_id / gene_symbol")
            print("Enter attributes in csv format (attr1,attr2,...): ")
            cond["attribute"] = input().split(",")
            for attr in cond["attribute"]:
                if attr == "modified_date":
                    print("Please enter date in YYYY-MM-DD format")
                else:
                    print(f"Enter value for {attr}: ")
                cond["value"].append(input())
            insertRecord(tableName, cond)

        elif x == str(1):
            print("Enter gene symbol: ")
            symbol = input()
            print(
                "gene " + symbol + " information stored in the gene table is as follows"
            )
            print(
                "tax_id / gene_id / symbol / chro_num / map_location / description / type_of_gene / modified_date / gene_synonyms "
            )
            searchGenebySymbol(symbol)

        elif x == str(2):
            print("Enter chromosome ID: ")
            chro_num = input()
            print(
                "gene symbols located in the chromosome id "
                + chro_num
                + " are as follows"
            )
            searchGenebyChro(chro_num)

        elif x == str(3):
            print("Enter gene ID: ")
            gene_id = input()
            print(
                "gene ID "
                + gene_id
                + " information stored in the gene table is as follows"
            )
            print(
                "tax_id / gene_id / symbol / chro_num / map_location / description / type_of_gene / modified_date / gene_synonyms "
            )
            searchGenebyId(gene_id)

        elif x == str(4):
            print("Enter snp ID: ")
            snp_id = input()
            print("SNP data with snp id " + snp_id + " are as follows")
            print(
                "snp_id / chro_num / pos_on_Chromo / neighbor_gene / anc_allele / min_allele"
            )
            searchSNPbyId(snp_id)

        elif x == str(5):
            print("Enter gene symbol: ")
            symbol = input()
            print("SNP data associated with gene " + symbol + " are as follows")
            print(
                "snp_id / chro_num / pos_on_Chromo / neighbor_gene / anc_allele / min_allele"
            )
            searchSNPbyGene(symbol)

        elif x == str(6):
            print("Enter disease name: ")
            disease_name = input()
            print(
                "SNP IDs associated with the disease "
                + disease_name
                + " are as follows"
            )
            searchSNPbyDisease(disease_name)

        elif x == str(7):
            print("Enter disease name: ")
            disease_name = input()
            print(
                "OMIM data associated with the disease "
                + disease_name
                + " are as follows"
            )
            print(" OMIM_id / disease_name / genes affecting disease")
            searchDiseasebyName(disease_name)

        elif x == str(8):
            print("Enter gene symbol: ")
            symbol = input()
            print("Disease associated with gene " + symbol + " are as follows")
            searchDiseasebyGene(symbol)

        elif x == str(9):
            print("Enter snp id: ")
            snp_id = input()
            print(
                "Disease that can be affected by snp id " + snp_id + " are as follows"
            )
            searchDiseasebySNP(snp_id)

        elif x == "e":
            active = False
            break

        elif x == "s":
            showStatistics()

        else:
            print("Input character is not recognized!")

        print("------------------------------")
        print("Would you like to continue? [y/n]")
        if input() == "n":
            active = False
        print("------------------------------")
