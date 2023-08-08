# Create table and insert data

import psycopg2
import csv
from prettytable import PrettyTable
import sys
import io

IP_ADDRESS = "Deleted"
PORT = "Deleted"
DB_NAME = "Deleted"
ID = "Deleted"
PASSWD = "Deleted"

"""## 1. Create Table & Index"""


def createTable():
    try:
        connection = psycopg2.connect(
            dbname=DB_NAME, user=ID, password=PASSWD, host=IP_ADDRESS, port=PORT
        )
        cursor = connection.cursor()

        # table from previous db
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
            CREATE TABLE disease(\
              OMIM_id INTEGER NOT NULL DEFAULT 0,\
              disease_name VARCHAR(150),\
              PRIMARY KEY(OMIM_id)\
            );\
            CREATE TABLE gene_disease(\
              OMIM_id INTEGER NOT NULL DEFAULT 0,\
              gene_symbol VARCHAR(30) NOT NULL,\
              PRIMARY KEY (OMIM_id, gene_symbol)\
            );\
            "
        cursor.execute(sql)

        new_sql = "CREATE TABLE gene_pathway(\
              smpdb_id VARCHAR(10) NOT NULL,\
              gene_symbol VARCHAR(10) NOT NULL,\
              pathway_name VARCHAR(100),\
              pathway_subject VARCHAR(20),\
              uniprot_id VARCHAR(20),\
              locus VARCHAR(30),\
              PRIMARY KEY (smpdb_id, gene_symbol, uniprot_id)\
            );\
            CREATE TABLE pathway(\
              pathway_id INTEGER NOT NULL,\
              smpdb_id VARCHAR(10) NOT NULL,\
              PRIMARY KEY (pathway_id)\
            );\
            CREATE TABLE compound(\
              compound_id INTEGER NOT NULL,\
              name VARCHAR(300),\
              annotation VARCHAR(15000),\
              PRIMARY KEY (compound_id)\
            );\
            CREATE TABLE compound_pathway(\
              cp_id INTEGER NOT NULL, \
              compound_id INTEGER NOT NULL,\
              pathway_id INTEGER NOT NULL,\
              PRIMARY KEY (cp_id)\
            );\
            CREATE TABLE food(\
              food_id INTEGER NOT NULL,\
              food_name VARCHAR(60),\
              food_group VARCHAR(30),\
              PRIMARY KEY(food_id)\
            );\
            CREATE TABLE compound_food(\
              cpf_id INTEGER NOT NULL,\
              compound_id INTEGER NOT NULL,\
              food_id INTEGER NOT NULL,\
              amount NUMERIC(8,2) NOT NULL DEFAULT 0,\
              PRIMARY KEY(cpf_id)\
            );\
            CREATE TABLE health(\
              health_effect_id INTEGER NOT NULL,\
              name VARCHAR(70),\
              description VARCHAR(700),\
              PRIMARY KEY(health_effect_id)\
            );\
            CREATE TABLE compound_health(\
              compound_id INTEGER NOT NULL,\
              health_effect_id INTEGER NOT NULL,\
              PRIMARY KEY(compound_id, health_effect_id)\
            );\
            "
        cursor.execute(new_sql)
        connection.commit()

        connection.close()
    except psycopg2.Error as e:
        pass

    except RuntimeError as e:
        pass

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
          CREATE INDEX ix_disease_name ON disease(disease_name);\
          CREATE INDEX ix_smpdb_id ON pathway(smpdb_id);\
          CREATE INDEX ix_compound_id ON compound_food(compound_id);\
          CREATE INDEX ix_food_id ON compound_food(food_id);\
          "
        cursor.execute(sql)
        connection.commit()
        connection.close()

    except psycopg2.Error as e:
        pass

    except RuntimeError as e:
        pass

    finally:
        connection.close()
    return


"""## 2. Insert data"""


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
            pass

        except RuntimeError as e:
            pass

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
            pass

        except RuntimeError as e:
            pass

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
            pass

        except RuntimeError as e:
            pass

        finally:
            connection.close()

        file.close()
    return


# Compound.csv  CompoundsHealthEffect.csv  CompoundsPathway.csv  Content.csv
# Food.csv  HealthEffect.csv  Pathway.csv  SMP_proteins.csv


def insertGenePathway():
    filename = dir_path + "SMP_proteins.csv"
    with open(filename, "r", newline="", encoding="utf-8") as file:
        reader = csv.reader(file)
        next(reader)  # skip header

        try:
            connection = psycopg2.connect(
                dbname=DB_NAME, user=ID, password=PASSWD, host=IP_ADDRESS, port=PORT
            )
            cursor = connection.cursor()

            for row in reader:
                if row[7]:
                    sql = f"INSERT INTO gene_pathway (smpdb_id, gene_symbol, pathway_name, pathway_subject, uniprot_id, locus) \
                  values ('{row[0]}', '{row[7]}', '{row[1]}', '{row[2]}', '{row[3]}', '{row[8]}');"
                    cursor.execute(sql)

            connection.commit()
            connection.close()

        except psycopg2.Error as e:
            pass

        except RuntimeError as e:
            pass

        finally:
            connection.close()

        file.close()
    return


def insertPathway():
    filename = dir_path + "Pathway.csv"
    with open(filename, "r", newline="", encoding="utf-8") as file:
        # compound_id name annotation
        reader = csv.reader(file)
        next(reader)  # skip header

        try:
            connection = psycopg2.connect(
                dbname=DB_NAME, user=ID, password=PASSWD, host=IP_ADDRESS, port=PORT
            )
            cursor = connection.cursor()

            for row in reader:
                sql = f"INSERT INTO pathway (pathway_id, smpdb_id) values ('{row[0]}', '{row[1]}');"
                cursor.execute(sql)

            connection.commit()
            connection.close()

        except psycopg2.Error as e:
            pass

        except RuntimeError as e:
            pass

        finally:
            connection.close()

        file.close()
    return


def insertCompound():
    filename = dir_path + "Compound.csv"
    with open(filename, "r", newline="", encoding="utf-8") as file:
        # compound_id name annotation
        reader = csv.reader(file)
        next(reader)  # skip header

        try:
            connection = psycopg2.connect(
                dbname=DB_NAME, user=ID, password=PASSWD, host=IP_ADDRESS, port=PORT
            )
            cursor = connection.cursor()

            for row in reader:
                name = row[2].replace("'", "''")
                ann = row[5].replace("'", "''").strip()
                sql = f"INSERT INTO compound (compound_id, name, annotation) values ({int(row[0])}, '{name}', '{ann}');"
                cursor.execute(sql)

            connection.commit()
            connection.close()

        except psycopg2.Error as e:
            pass

        except RuntimeError as e:
            pass

        finally:
            connection.close()

        file.close()
    return


def insertCompoundPathway():
    filename = dir_path + "CompoundsPathway.csv"
    with open(filename, "r", newline="", encoding="utf-8") as file:
        # compound_id name annotation
        reader = csv.reader(file)
        next(reader)  # skip header

        try:
            connection = psycopg2.connect(
                dbname=DB_NAME, user=ID, password=PASSWD, host=IP_ADDRESS, port=PORT
            )
            cursor = connection.cursor()

            for row in reader:
                sql = f"INSERT INTO compound_pathway (cp_id, compound_id, pathway_id) values ({int(row[0])}, {int(row[1])}, '{row[2]}');"
                cursor.execute(sql)

            connection.commit()
            connection.close()

        except psycopg2.Error as e:
            pass

        except RuntimeError as e:
            pass

        finally:
            connection.close()

        file.close()
    return


def insertFood():
    filename = dir_path + "Food.csv"
    with open(filename, "r", newline="", encoding="utf-8") as file:
        # compound_id name annotation
        reader = csv.reader(file)
        next(reader)  # skip header

        try:
            connection = psycopg2.connect(
                dbname=DB_NAME, user=ID, password=PASSWD, host=IP_ADDRESS, port=PORT
            )
            cursor = connection.cursor()

            for row in reader:
                name = row[1].replace("'", "''")
                sql = f"INSERT INTO food (food_id, food_name, food_group) values ({int(row[0])}, '{name}', '{row[11]}');"
                cursor.execute(sql)

            connection.commit()
            connection.close()

        except psycopg2.Error as e:
            pass

        except RuntimeError as e:
            pass

        finally:
            connection.close()

        file.close()
    return


def insertCompoundFood():
    filename = dir_path + "Content.csv"
    with open(filename, "r", newline="", encoding="utf-8") as file:
        # compound_id name annotation
        reader = csv.reader(file)
        next(reader)  # skip header

        try:
            connection = psycopg2.connect(
                dbname=DB_NAME, user=ID, password=PASSWD, host=IP_ADDRESS, port=PORT
            )
            cursor = connection.cursor()

            for row in reader:
                if row[2] == "Compound":
                    sql = f"INSERT INTO compound_food (cpf_id, compound_id, food_id, amount) values ({int(row[0])}, {int(row[1])}, '{row[3]}', '{row[10] if row[10] else 0}');"
                    cursor.execute(sql)

            connection.commit()
            connection.close()

        except psycopg2.Error as e:
            pass

        except RuntimeError as e:
            pass

        finally:
            connection.close()

        file.close()
    return


def insertHealth():
    filename = dir_path + "HealthEffect.csv"
    with open(filename, "r", newline="", encoding="utf-8") as file:
        # compound_id name annotation
        reader = csv.reader(file)
        next(reader)  # skip header

        try:
            connection = psycopg2.connect(
                dbname=DB_NAME, user=ID, password=PASSWD, host=IP_ADDRESS, port=PORT
            )
            cursor = connection.cursor()

            for row in reader:
                name = row[1].replace("'", "''")
                des = row[2].strip() + row[9].strip()
                des = des.replace("'", "''")
                des = des.replace("\xa0", " ")
                sql = f"INSERT INTO health (health_effect_id, name, description) values ({int(row[0])}, '{name}', '{des}');"
                cursor.execute(sql)

            connection.commit()
            connection.close()

        except psycopg2.Error as e:
            pass

        except RuntimeError as e:
            pass

        finally:
            connection.close()

        file.close()
    return


def insertCompoundHealth():
    filename = dir_path + "CompoundsHealthEffect.csv"
    with open(filename, "r", newline="", encoding="utf-8") as file:
        # compound_id name annotation
        reader = csv.reader(file)
        next(reader)  # skip header

        try:
            connection = psycopg2.connect(
                dbname=DB_NAME, user=ID, password=PASSWD, host=IP_ADDRESS, port=PORT
            )
            cursor = connection.cursor()

            for row in reader:
                sql = f"INSERT INTO compound_health (compound_id, health_effect_id) values ({int(row[1])}, '{int(row[2])}');"
                cursor.execute(sql)

            connection.commit()
            connection.close()

        except psycopg2.Error as e:
            pass

        except RuntimeError as e:
            pass

        finally:
            connection.close()

        file.close()
    return


"""## 3. Query"""
"""
3-0. Search compound info by disease name
"""


def searchCombyOMIM(name):
    try:
        connection = psycopg2.connect(
            dbname=DB_NAME, user=ID, password=PASSWD, host=IP_ADDRESS, port=PORT
        )
        cursor = connection.cursor()

        firstsql = f"SELECT gd.gene_symbol from gene_disease gd where gd.OMIM_id = ( \
                  SELECT omim_id from disease where disease_name = '{name}');"
        cursor.execute(firstsql)
        rs = cursor.fetchall()
        symbol = [r[0] for r in rs]
        syn = set(symbol)

        for gene in symbol:
            secondsql = f"SELECT gene_synonyms.synonyms FROM gene NATURAL JOIN gene_synonyms WHERE gene.symbol = '{gene}'"
            cursor.execute(secondsql)
            rs = cursor.fetchall()
            for r in rs:
                syn.add(r[0])

        syn_list = "', '".join(list(syn))

        sql = (
            f"SELECT cp.name, gp.pathway_subject \
                FROM compound cp \
                JOIN compound_pathway cpath ON cp.compound_id = cpath.compound_id \
                JOIN pathway path ON cpath.pathway_id = path.pathway_id \
                JOIN gene_pathway gp ON path.smpdb_id = gp.smpdb_id \
                WHERE gp.gene_symbol IN ('"
            + syn_list
            + "');"
        )

        cursor.execute(sql)
        rs = cursor.fetchall()

        columns = [desc[0] for desc in cursor.description]
        table = PrettyTable(["#"] + columns)
        for i, row in enumerate(rs, start=1):
            table.add_row([i] + list(row))
        print(table)

        connection.close()

    except psycopg2.Error as e:
        print(e)

    except RuntimeError as e:
        print(e)

    finally:
        connection.close()
    return


"""
3-1. Search food info (food_id, food_name, food_group) by disease name
"""


def searchFoodbyOMIM(name):
    try:
        connection = psycopg2.connect(
            dbname=DB_NAME, user=ID, password=PASSWD, host=IP_ADDRESS, port=PORT
        )
        cursor = connection.cursor()

        firstsql = f"SELECT gd.gene_symbol from gene_disease gd where gd.OMIM_id = ( \
                  SELECT omim_id from disease where disease_name = '{name}');"
        cursor.execute(firstsql)
        rs = cursor.fetchall()
        symbol = [r[0] for r in rs]
        syn = set(symbol)

        for gene in symbol:
            secondsql = f"SELECT gene_synonyms.synonyms FROM gene NATURAL JOIN gene_synonyms WHERE gene.symbol = '{gene}'"
            cursor.execute(secondsql)
            rs = cursor.fetchall()
            for r in rs:
                syn.add(r[0])

        syn_list = "', '".join(list(syn))

        sql = (
            f"SELECT DISTINCT cf.amount AS am, cf.food_id, cf.compound_id \
                FROM compound_food cf \
                JOIN compound c ON cf.compound_id = c.compound_id \
                JOIN compound_pathway cp ON c.compound_id = cp.compound_id \
                JOIN pathway p ON cp.pathway_id = p.pathway_id \
                JOIN gene_pathway gp ON p.smpdb_id = gp.smpdb_id \
                WHERE gp.gene_symbol IN ('"
            + syn_list
            + "') \
                ORDER BY am DESC;"
        )
        cursor.execute(sql)
        topamount = cursor.fetchall()
        top_food = {}  # food_id: [compound_id, amount]

        for r in topamount:
            if len(top_food) < 5:
                if r[1] not in top_food:
                    top_food[r[1]] = [r[2], r[0]]
            else:
                break
        top_food_l = "', '".join(map(str, top_food))

        if topamount:
            sql = (
                f"SELECT food_id, food_name, food_group from food f where f.food_id in ('"
                + top_food_l
                + "');"
            )
            cursor.execute(sql)
            rs = cursor.fetchall()
            table = PrettyTable(["food_name", "food_group", "compound_name", "amount"])

            for row in rs:
                sql = (
                    f"SELECT name from compound where compound_id = '"
                    + str(top_food[row[0]][0])
                    + "';"
                )
                cursor.execute(sql)
                name = cursor.fetchone()
                table.add_row([row[1], row[2]] + [name[0]] + [top_food[row[0]][1]])
            table.sortby = "amount"
            table.reversesort = True
            print(table)

        else:
            print("no food")

        connection.close()

    except psycopg2.Error as e:
        print(e)

    except RuntimeError as e:
        print(e)

    finally:
        connection.close()
    return


"""3-2. search health info by compound name """


def searchHealthbyCom(name):
    try:
        connection = psycopg2.connect(
            dbname=DB_NAME, user=ID, password=PASSWD, host=IP_ADDRESS, port=PORT
        )
        cursor = connection.cursor()
        name = name.replace("'", "''")

        sql = f"SELECT h.name, h.description \
                FROM health h\
                JOIN compound_health ch ON h.health_effect_id = ch.health_effect_id\
                JOIN compound c ON ch.compound_id = c.compound_id\
                WHERE c.name = '{name}';"

        cursor.execute(sql)

        rs = cursor.fetchall()

        columns = [desc[0] for desc in cursor.description]
        table = PrettyTable(["#"] + columns)
        table.max_width["description"] = 60
        table.align["description"] = "l"
        for i, row in enumerate(rs, start=1):
            table.add_row([i] + list(row))
        print(table)

        connection.close()

    except psycopg2.Error as e:
        print(e)

    except RuntimeError as e:
        print(e)

    finally:
        connection.close()
    return


""" 3-3. searh food info by compound name """


def searchFoodbyCom(name):
    try:
        connection = psycopg2.connect(
            dbname=DB_NAME, user=ID, password=PASSWD, host=IP_ADDRESS, port=PORT
        )
        cursor = connection.cursor()

        name = name.replace("'", "''")

        sql = f"SELECT f.food_name, f.food_group \
                FROM food f\
                JOIN compound_food cf ON f.food_id = cf.food_id\
                JOIN compound c ON cf.compound_id = c.compound_id\
                WHERE c.name = '{name}';\
                "

        cursor.execute(sql)

        rs = cursor.fetchall()

        columns = [desc[0] for desc in cursor.description]
        table = PrettyTable(["#"] + columns)
        for i, row in enumerate(rs, start=1):
            table.add_row([i] + [row[0].encode().decode("utf-8"), row[1]])

        stdout_wrapper = io.TextIOWrapper(
            sys.stdout.buffer, encoding="utf-8", line_buffering=True
        )
        temp_output = io.StringIO()
        sys.stdout = temp_output
        print(table)
        output_contents = temp_output.getvalue()
        sys.stdout = stdout_wrapper
        print(output_contents)

        connection.close()

    except psycopg2.Error as e:
        print(e)

    except RuntimeError as e:
        print(e)

    finally:
        connection.close()
    return


# 3-5.
def searchComp(name):
    try:
        connection = psycopg2.connect(
            dbname=DB_NAME, user=ID, password=PASSWD, host=IP_ADDRESS, port=PORT
        )
        cursor = connection.cursor()

        name = name.replace("'", "''")
        sql = f"SELECT annotation from compound where name = '{name}';"

        cursor.execute(sql)

        rs = cursor.fetchall()
        for r in rs:
            print(r[0])

        connection.close()

    except psycopg2.Error as e:
        print(e)

    except RuntimeError as e:
        print(e)

    finally:
        connection.close()
    return


# main function
"""
## 4. Main
"""

if __name__ == "__main__":
    createTable()
    createIndex()
    dir_path = "/work/home/bis332/bio_data/"
    # disease_OMIM.txt  gene_OMIM.txt  Homo_sapiens_gene_info.txt
    insertDisease()
    insertGene()
    insertDG()
    dir_path = "/work/home/project/phase3/"
    # Compound.csv  CompoundsHealthEffect.csv  CompoundsPathway.csv  Content.csv
    # Food.csv  HealthEffect.csv  Pathway.csv  SMP_proteins.csv
    insertGenePathway()
    insertPathway()
    insertCompound()
    insertCompoundPathway()
    insertFood()
    insertCompoundFood()
    insertHealth()
    insertCompoundHealth()

    # greeting
    print(
        "    ______                 ____        \n\
   / ____/ ____   ____    / __ \  ___   ___   \n\
  / /_    / __ \ / __ \  / / / / / _ \ / _ \ \n\
 / __/   / /_/ // /_/ / / /_/ / /  __//  __/\n\
/_/      \____/ \____/ /_____/  \___/ \___/ \n\
                                            "
    )
    print("------------------------------")
    active = True
    while active:
        # print option
        print("0: Find compounds related to a disease")
        print("1: Suggest healthy foods for a disease")
        print("2: Discover health effects of a compound")
        print("3: Get a list of foods with a specific compound")
        print("4: Learn about a compound's description")
        print("e: exit")
        print("------------------------------")
        print("Enter option you want to execute: ")
        x = input()
        if x == str(0):
            print("Enter disease name: ")
            omim_id = input()
            print("Compounds related to the disease " + omim_id + " are as follows")
            searchCombyOMIM(omim_id)
        elif x == str(1):
            print("Enter disease name: ")
            omim_id = input()
            print(
                "Suggestion of healthy foods for the disease "
                + omim_id
                + " are as follows"
            )
            searchFoodbyOMIM(omim_id)
        elif x == str(2):
            print("Enter compound name: ")
            compound_id = input()
            print("Health effects of a compound " + compound_id + " are as follows")
            searchHealthbyCom(compound_id)
        elif x == str(3):
            print("Enter compound name: ")
            compound_id = input()
            print("Foods which has compound " + compound_id + " are as follows")
            searchFoodbyCom(compound_id)
        elif x == str(4):
            print("Enter compound name: ")
            compound_id = input()
            print("Information of compound " + compound_id + " are as follows")
            searchComp(compound_id)
        elif x == "e":
            active = False
            break
        else:
            print("Input character is not recognized!")

        print("------------------------------")
        print("Would you like to continue? [y/n]")
        if input() == "n":
            active = False
        print("------------------------------")
