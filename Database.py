import xml.etree.ElementTree as ET
import sqlite3
import configparser

from Game import Game

f_error = open("error_db.txt", "w")

class Database:

    def connect(self):
        self.connection = sqlite3.connect("games.db")
        self.cursor = self.connection.cursor()


    #def __init__(self):
        #connection = sqlite3.connect("games.db")
        #cursor = connection.cursor()

    # takes mame2010 database as basis and adds missing 2003 roms
    def build_games_db(self):
        f_error.write ("Writing games db.\n")
        try:
            self.cursor.execute("""DROP TABLE games;""")
            self.connection.commit()
        except:
            f_error.write ("No Table to delete.\n")


        sql_cmd ="CREATE TABLE games ( \
            game_name VARCHAR(30) NOT NULL, \
            cloneof VARCHAR(30), \
            romof VARCHAR(30), \
            year VAR_CHAR(4), \
            manufacturer VARCHAR(30), \
            description VARCHAR(120), \
            players VARCHAR(15), \
            controls VARCHAR(15), \
            screen VARCHAR(30), \
            orientation VARCHAR(30), \
            rotation VARCHAR(4), \
            width VARCHAR(4), \
            height VARCHAR(4), \
            refresh VARCHAR(20), \
            category VARCHAR(40), \
            subcategory VARCHAR(40), \
            nplayers VARCHAR(20), \
            PRIMARY KEY (game_name));"

        self.cursor.execute(sql_cmd)
        self.connection.commit()

        result_mame2003 = self.execute("SELECT * FROM games_mame2003plus")
        result_mame2010 = self.execute("SELECT * FROM games_mame2010")

        # copy all m2010 in final db
        for m2010 in result_mame2010:

            sql_cmd = ("INSERT INTO games (game_name, cloneof, romof, year, manufacturer, description, players, controls, screen, rotation, orientation, width, height, refresh, category, subcategory, nplayers) VALUES \
                    (\"%s\", \"%s\", \"%s\", \"%s\", \"%s\", \"%s\", \"%s\", \"%s\", \"%s\", \"%s\", \"%s\", \"%s\", \"%s\", \"%s\", \"%s\", \"%s\", \"%s\");"  \
                    % (m2010[0], m2010[1], m2010[2], m2010[3], m2010[4], m2010[5], m2010[6], m2010[7], m2010[8], m2010[9], m2010[10], m2010[11], m2010[12], m2010[13], m2010[14], m2010[15], m2010[16]))
            print (sql_cmd)
            self.cursor.execute(sql_cmd)
            self.connection.commit()

        # look if m2003 games are missing in m2010
        # if yes add them
        ctr = 0
        ctr_found = 0
        for m2003 in result_mame2003:
            found = False
            for m2010 in result_mame2010:
                if m2003[0] == m2010[0]:
                    found = True

            if found == False:
                ctr = ctr +1

                sql_cmd = ("INSERT INTO games (game_name, cloneof, romof, year, manufacturer, description, players, controls, screen, rotation, orientation, width, height, refresh, category, subcategory, nplayers) VALUES \
                        (\"%s\", \"%s\", \"%s\", \"%s\", \"%s\", \"%s\", \"%s\", \"%s\", \"%s\", \"%s\", \"%s\", \"%s\", \"%s\", \"%s\", \"%s\", \"%s\", \"%s\");"  \
                        % (m2003[0], m2003[1], m2003[2], m2003[3], m2003[4], m2003[5], m2003[6], m2003[7], m2003[8], m2003[9], m2003[10], m2003[11], m2003[12], m2003[13], m2003[14], m2003[15], m2003[16]))
                print (sql_cmd)
                self.cursor.execute(sql_cmd)
                self.connection.commit()
            else:
                ctr_found = ctr_found +1

        print (ctr, " missing games")
        print (ctr_found, " matching games")


        f_error.close()




    def build_db_fbaneo(self):
        f_error.write ("Writing fbaneo db.\n")
        try:
            self.cursor.execute("""DROP TABLE games_fbaneo;""")
            self.connection.commit()
        except:
            f_error.write ("No Table to delete.\n")

        config_cat = configparser.RawConfigParser()
        config_cat.read('catver.ini')

        config_nplayers = configparser.RawConfigParser()
        config_nplayers.read('nplayers.ini')

        sql_cmd ="CREATE TABLE games_fbaneo ( \
            game_name VARCHAR(30) NOT NULL, \
            cloneof VARCHAR(30), \
            romof VARCHAR(30), \
            year VAR_CHAR(4), \
            manufacturer VARCHAR(30), \
            description VARCHAR(120), \
            players VARCHAR(15), \
            controls VARCHAR(15), \
            screen VARCHAR(30), \
            orientation VARCHAR(30), \
            rotation VARCHAR(4), \
            width VARCHAR(4), \
            height VARCHAR(4), \
            refresh VARCHAR(20), \
            category VARCHAR(40), \
            subcategory VARCHAR(40), \
            nplayers VARCHAR(20), \
            PRIMARY KEY (game_name));"

        self.cursor.execute(sql_cmd)
        self.connection.commit()

        #root = ET.parse('test.xml').getroot()
        root = ET.parse('fbaneo.xml').getroot()
        gamelist = []

        for game_tag in root.findall('game'):

            g = Game()

            gamelist.append(g)

            game_name = game_tag.get('name')

            g.game_name = game_name
            #print (g.game_name)

            try:
                cloneof = game_tag.get('cloneof')
            except:
                cloneof = ""
                f_error.write ("no cloneof found for %s\n" % (game_name))

            try:
                romof = game_tag.get('romof')
            except:
                romof = ""
                f_error.write ("no romof found for %s\n" % (game_name))

            try:
                cat = config_cat.get('Category', game_name)
                category = cat.split(" / ")[0]
                subcategory = cat.split("/")[1].strip()
            except:
                # man könnte auch die sampleof nehmen
                cat_tmp = self.getCategoryFromParent(cloneof)
                category = cat_tmp.split(";")[0]
                subcategory = cat_tmp.split(";")[1]
                #f_error.write ("no category or subcategory found for %s\n" % (game_name))
                f_error.write ("for game %s taken parents %s cat *%s* and subcat *%s*\n" % (game_name, cloneof, category, subcategory))

            try:
                nplayers = config_nplayers.get('NPlayers', game_name)

            except:
                # man könnte auch die sampleof nehmen
                nplayers = ""
                f_error.write ("no nplayers found for %s\n" % (game_name))

            mf_tag = game_tag.find('manufacturer')
            manufacturer = mf_tag.text

            try:
                year_tag = game_tag.find('year')
                year = year_tag.text
            except:
                f_error.write ("no year found for %s\n" % (game_name))
                year = "n/a"

            desc_tag = game_tag.find('description')
            description = desc_tag.text

            try:
                input_tag = game_tag.find('input')
                players = input_tag.get('players')
                control = input_tag.get('control')
            except:
                f_error.write ("no input found for %s\n" % (game_name))
                players = "n/a"
                control = "n/a"
            try:
                video_tag = game_tag.find('video')
                screen = video_tag.get('screen')
                orientation = video_tag.get('orientation')
                width = video_tag.get('width')
                height = video_tag.get('height')
                refresh = video_tag.get('refresh')
            except:
                f_error.write ("no video found for %s\n" % (game_name))
                screen = "n/a"
                orientation = "n/a"
                width = "n/a"
                height = "n/a"
                refresh = "n/a"
            #print ("%s ; %s; %s ; %s; %s ; %s; %s; %s ; %s; %s ; %s" % (game_name, description, manufacturer, year, players, control, screen, orientation, width, height, refresh))

            sql_cmd = ("INSERT INTO games_fbaneo (game_name, cloneof, romof, year, manufacturer, description, players, controls, screen, orientation, width, height, refresh, category, subcategory, nplayers) VALUES \
                (\"%s\", \"%s\", \"%s\", \"%s\", \"%s\", \"%s\", \"%s\", \"%s\", \"%s\", \"%s\", \"%s\", \"%s\", \"%s\", \"%s\", \"%s\", \"%s\");"  \
                % (game_name, cloneof, romof, year, manufacturer, description, players, control, screen, orientation, width, height, refresh, category, subcategory, nplayers))
            print (sql_cmd)
            self.cursor.execute(sql_cmd)
            self.connection.commit()

        print()
        print ("******job finished******")
        print ("%d games processed" % (len(gamelist)))
        #f_error.close()




    # -- for mame2003plus --
    def build_db_mame2003plus(self):
        f_error.write ("Writing mame2003plus db.\n")
        try:
            self.cursor.execute("""DROP TABLE games_mame2003plus;""")
            self.connection.commit()
        except:
            f_error.write ("No Table to delete.\n")

        config_cat = configparser.RawConfigParser()
        config_cat.read('catver.ini')

        config_nplayers = configparser.RawConfigParser()
        config_nplayers.read('nplayers.ini')

        sql_cmd ="CREATE TABLE games_mame2003plus ( \
            game_name VARCHAR(30) NOT NULL, \
            cloneof VARCHAR(30), \
            romof VARCHAR(30), \
            year VAR_CHAR(4), \
            manufacturer VARCHAR(30), \
            description VARCHAR(120), \
            players VARCHAR(15), \
            controls VARCHAR(15), \
            screen VARCHAR(30), \
            orientation VARCHAR(30), \
            rotation VARCHAR(4), \
            width VARCHAR(4), \
            height VARCHAR(4), \
            refresh VARCHAR(20), \
            category VARCHAR(40), \
            subcategory VARCHAR(40), \
            nplayers VARCHAR(20), \
            PRIMARY KEY (game_name));"

        self.cursor.execute(sql_cmd)
        self.connection.commit()

        #root = ET.parse('test.xml').getroot()
        root = ET.parse('mame2003-plus.xml').getroot()
        gamelist = []

        for game_tag in root.findall('game'):

            g = Game()

            gamelist.append(g)

            game_name = game_tag.get('name')

            g.game_name = game_name
            #print (g.game_name)

            try:
                cloneof = game_tag.get('cloneof')
            except:
                cloneof = ""
                f_error.write ("no cloneof found for %s\n" % (game_name))

            try:
                romof = game_tag.get('romof')
            except:
                romof = ""
                f_error.write ("no romof found for %s\n" % (game_name))

            try:
                cat = config_cat.get('Category', game_name)
                category = cat.split(" / ")[0]
                subcategory = cat.split("/")[1].strip()
            except:
                # man könnte auch die sampleof nehmen
                cat_tmp = self.getCategoryFromParent(cloneof)
                category = cat_tmp.split(";")[0]
                subcategory = cat_tmp.split(";")[1]
                #f_error.write ("no category or subcategory found for %s\n" % (game_name))
                f_error.write ("for game %s taken parents %s cat *%s* and subcat *%s*\n" % (game_name, cloneof, category, subcategory))

            try:
                nplayers = config_nplayers.get('NPlayers', game_name)

            except:
                # man könnte auch die sampleof nehmen
                nplayers = ""
                f_error.write ("no nplayers found for %s\n" % (game_name))

            mf_tag = game_tag.find('manufacturer')
            manufacturer = mf_tag.text

            try:
                year_tag = game_tag.find('year')
                year = year_tag.text
            except:
                f_error.write ("no year found for %s\n" % (game_name))
                year = "n/a"

            desc_tag = game_tag.find('description')
            description = desc_tag.text

            try:
                input_tag = game_tag.find('input')
                players = input_tag.get('players')
                control = input_tag.get('control')
            except:
                f_error.write ("no input found for %s\n" % (game_name))
                players = "n/a"
                control = "n/a"
            try:
                video_tag = game_tag.find('video')
                screen = video_tag.get('screen')
                orientation = video_tag.get('orientation')
                width = video_tag.get('width')
                height = video_tag.get('height')
                refresh = video_tag.get('refresh')
            except:
                f_error.write ("no video found for %s\n" % (game_name))
                screen = "n/a"
                orientation = "n/a"
                width = "n/a"
                height = "n/a"
                refresh = "n/a"
            #print ("%s ; %s; %s ; %s; %s ; %s; %s; %s ; %s; %s ; %s" % (game_name, description, manufacturer, year, players, control, screen, orientation, width, height, refresh))

            sql_cmd = ("INSERT INTO games_mame2003plus (game_name, cloneof, romof, year, manufacturer, description, players, controls, screen, orientation, width, height, refresh, category, subcategory, nplayers) VALUES \
                (\"%s\", \"%s\", \"%s\", \"%s\", \"%s\", \"%s\", \"%s\", \"%s\", \"%s\", \"%s\", \"%s\", \"%s\", \"%s\", \"%s\", \"%s\", \"%s\");"  \
                % (game_name, cloneof, romof, year, manufacturer, description, players, control, screen, orientation, width, height, refresh, category, subcategory, nplayers))
            print (sql_cmd)
            self.cursor.execute(sql_cmd)
            self.connection.commit()

        print()
        print ("******job finished******")
        print ("%d games processed" % (len(gamelist)))
        #f_error.close()


    def build_db_mame2010(self):

        f_error.write ("Writing mame2010 db.\n")
        try:
            self.cursor.execute("""DROP TABLE games_mame2010;""")
            self.connection.commit()
        except:
            f_error.write ("No Table to delete.\n")

        config_cat = configparser.RawConfigParser()
        config_cat.read('catver.ini')

        config_nplayers = configparser.RawConfigParser()
        config_nplayers.read('nplayers.ini')

        sql_cmd ="CREATE TABLE games_mame2010 ( \
            game_name VARCHAR(30) NOT NULL, \
            cloneof VARCHAR(30), \
            romof VARCHAR(30), \
            year VAR_CHAR(4), \
            manufacturer VARCHAR(30), \
            description VARCHAR(120), \
            players VARCHAR(15), \
            controls VARCHAR(15), \
            screen VARCHAR(30), \
            orientation VARCHAR(30), \
            rotation VARCHAR(4), \
            width VARCHAR(4), \
            height VARCHAR(4), \
            refresh VARCHAR(20), \
            category VARCHAR(40), \
            subcategory VARCHAR(40), \
            nplayers VARCHAR(20), \
            PRIMARY KEY (game_name));"

        self.cursor.execute(sql_cmd)
        self.connection.commit()

        #root = ET.parse('test.xml').getroot()
        root = ET.parse('mame2010.xml').getroot()
        gamelist = []

        for game_tag in root.findall('game'):

            g = Game()

            gamelist.append(g)

            game_name = game_tag.get('name')

            g.game_name = game_name
            #print (g.game_name)

            try:
                cloneof = game_tag.get('cloneof')
            except:
                cloneof = ""
                f_error.write ("no cloneof found for %s\n" % (game_name))

            try:
                romof = game_tag.get('romof')
            except:
                romof = ""
                f_error.write ("no romof found for %s\n" % (game_name))

            try:
                cat = config_cat.get('Category', game_name)
                category = cat.split(" / ")[0]
                subcategory = cat.split("/")[1].strip()
            except:
                # man könnte auch die sampleof nehmen
                cat_tmp = self.getCategoryFromParent(cloneof)
                category = cat_tmp.split(";")[0]
                subcategory = cat_tmp.split(";")[1]
                #f_error.write ("no category or subcategory found for %s\n" % (game_name))
                f_error.write ("for game %s taken parents %s cat *%s* and subcat *%s*\n" % (game_name, cloneof, category, subcategory))

            try:
                nplayers = config_nplayers.get('NPlayers', game_name)

            except:
                # man könnte auch die sampleof nehmen
                nplayers = ""
                f_error.write ("no nplayers found for %s\n" % (game_name))

            mf_tag = game_tag.find('manufacturer')
            manufacturer = mf_tag.text

            try:
                year_tag = game_tag.find('year')
                year = year_tag.text
            except:
                f_error.write ("no year found for %s\n" % (game_name))
                year = "n/a"

            desc_tag = game_tag.find('description')
            description = desc_tag.text

            try:
                input_tag = game_tag.find('input')
                players = input_tag.get('players')
                control_tag = input_tag.find('control')
                control = control_tag.get('type')
            except:
                f_error.write ("no input found for %s\n" % (game_name))
                players = "n/a"
                control = "n/a"
            try:
                video_tag = game_tag.find('display')
                screen = video_tag.get('type')
                rotation = video_tag.get('rotate')
                if (rotation == "0"):
                    orientation = "horizontal"
                else:
                    orientation = "vertical"
                width = video_tag.get('width')
                height = video_tag.get('height')
                # more info possible
                refresh = video_tag.get('refresh')
            except:
                f_error.write ("no video found for %s\n" % (game_name))
                screen = ""
                rotation = ""
                orientation = ""
                width = ""
                height = ""
                refresh = ""
            #print ("%s ; %s; %s ; %s; %s ; %s; %s; %s ; %s; %s ; %s" % (game_name, description, manufacturer, year, players, control, screen, orientation, width, height, refresh))

            sql_cmd = ("INSERT INTO games_mame2010 (game_name, cloneof, romof, year, manufacturer, description, players, controls, screen, rotation, orientation, width, height, refresh, category, subcategory, nplayers) VALUES \
                (\"%s\", \"%s\", \"%s\", \"%s\", \"%s\", \"%s\", \"%s\", \"%s\", \"%s\", \"%s\", \"%s\", \"%s\", \"%s\", \"%s\", \"%s\", \"%s\", \"%s\");"  \
                % (game_name, cloneof, romof, year, manufacturer, description, players, control, screen, rotation, orientation, width, height, refresh, category, subcategory, nplayers))
            print (sql_cmd)
            self.cursor.execute(sql_cmd)
            self.connection.commit()

        print()
        print ("******job finished******")
        print ("%d games processed" % (len(gamelist)))
        #f_error.close()



    def build_db_mame2016(self):

        f_error.write ("Writing mame2016 db.\n")
        try:
            self.cursor.execute("""DROP TABLE games_mame2016;""")
            self.connection.commit()
        except:
            f_error.write ("No Table to delete.\n")

        config_cat = configparser.RawConfigParser()
        config_cat.read('catver.ini')

        config_nplayers = configparser.RawConfigParser()
        config_nplayers.read('nplayers.ini')

        sql_cmd ="CREATE TABLE games_mame2016 ( \
            game_name VARCHAR(30) NOT NULL, \
            cloneof VARCHAR(30), \
            romof VARCHAR(30), \
            year VAR_CHAR(4), \
            manufacturer VARCHAR(30), \
            description VARCHAR(120), \
            players VARCHAR(15), \
            controls VARCHAR(15), \
            screen VARCHAR(30), \
            orientation VARCHAR(30), \
            rotation VARCHAR(4), \
            width VARCHAR(4), \
            height VARCHAR(4), \
            refresh VARCHAR(20), \
            category VARCHAR(40), \
            subcategory VARCHAR(40), \
            nplayers VARCHAR(20), \
            PRIMARY KEY (game_name));"

        self.cursor.execute(sql_cmd)
        self.connection.commit()

        #root = ET.parse('test.xml').getroot()
        root = ET.parse('mame2016.xml').getroot()
        gamelist = []

        #for game_tag in root.findall('game'):
        for game_tag in root.findall('machine'):

            g = Game()

            gamelist.append(g)

            game_name = game_tag.get('name')

            g.game_name = game_name
            #print (g.game_name)

            try:
                cloneof = game_tag.get('cloneof')
            except:
                cloneof = ""
                f_error.write ("no cloneof found for %s\n" % (game_name))

            try:
                romof = game_tag.get('romof')
            except:
                romof = ""
                f_error.write ("no romof found for %s\n" % (game_name))

            try:
                cat = config_cat.get('Category', game_name)
                category = cat.split(" / ")[0]
                subcategory = cat.split("/")[1].strip()
            except:
                # man könnte auch die sampleof nehmen
                cat_tmp = self.getCategoryFromParent(cloneof)
                category = cat_tmp.split(";")[0]
                subcategory = cat_tmp.split(";")[1]
                #f_error.write ("no category or subcategory found for %s\n" % (game_name))
                f_error.write ("for game %s taken parents %s cat *%s* and subcat *%s*\n" % (game_name, cloneof, category, subcategory))

            try:
                nplayers = config_nplayers.get('NPlayers', game_name)

            except:
                # man könnte auch die sampleof nehmen
                nplayers = ""
                f_error.write ("no nplayers found for %s\n" % (game_name))

            mf_tag = game_tag.find('manufacturer')
            manufacturer = mf_tag.text

            try:
                year_tag = game_tag.find('year')
                year = year_tag.text
            except:
                f_error.write ("no year found for %s\n" % (game_name))
                year = "n/a"

            desc_tag = game_tag.find('description')
            description = desc_tag.text

            try:
                input_tag = game_tag.find('input')
                players = input_tag.get('players')
                control_tag = input_tag.find('control')
                control = control_tag.get('type')
            except:
                f_error.write ("no input found for %s\n" % (game_name))
                players = "n/a"
                control = "n/a"
            try:
                video_tag = game_tag.find('display')
                screen = video_tag.get('type')
                rotation = video_tag.get('rotate')
                if (rotation == "0"):
                    orientation = "horizontal"
                else:
                    orientation = "vertical"
                width = video_tag.get('width')
                height = video_tag.get('height')
                # more info possible
                refresh = video_tag.get('refresh')
            except:
                f_error.write ("no video found for %s\n" % (game_name))
                screen = ""
                rotation = ""
                orientation = ""
                width = ""
                height = ""
                refresh = ""
            #print ("%s ; %s; %s ; %s; %s ; %s; %s; %s ; %s; %s ; %s" % (game_name, description, manufacturer, year, players, control, screen, orientation, width, height, refresh))

            sql_cmd = ("INSERT INTO games_mame2016 (game_name, cloneof, romof, year, manufacturer, description, players, controls, screen, rotation, orientation, width, height, refresh, category, subcategory, nplayers) VALUES \
                (\"%s\", \"%s\", \"%s\", \"%s\", \"%s\", \"%s\", \"%s\", \"%s\", \"%s\", \"%s\", \"%s\", \"%s\", \"%s\", \"%s\", \"%s\", \"%s\", \"%s\");"  \
                % (game_name, cloneof, romof, year, manufacturer, description, players, control, screen, rotation, orientation, width, height, refresh, category, subcategory, nplayers))
            print (sql_cmd)
            self.cursor.execute(sql_cmd)
            self.connection.commit()

        print()
        print ("******job finished******")
        print ("%d games processed" % (len(gamelist)))
        #f_error.close()


    def getCategoryFromParent(self, rom_name):
        try:
            sql_cmd = ("SELECT category, subcategory FROM games WHERE game_name =\"%s\"" % (rom_name))
            self.cursor.execute(sql_cmd)
            result = self.cursor.fetchone()
            return (result[0] + ";" + result[1])
        except:
            return "None;None"

    #--executing query--
    def execute(self, query):
        try:
            self.cursor.execute(query)
            result = self.cursor.fetchall()
            #for r in result:
            #    print(r)
            print ("%s items found" % (len(result)))
            return result
        except:
            print ("Error in Mysql-query: ", query)
            print ("or database not connected!")


    #------closing------
    def close(self):
        self.cursor.close()
        self.connection.close()
