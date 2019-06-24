import os
import configparser

from Database import Database
from Game import Game

db = Database()

def getCategories():
    print ("List of categories:")
    sql_cmd = ("SELECT DISTINCT category FROM games")
    db.cursor.execute(sql_cmd)
    result = db.cursor.fetchall()
    for r in result:
        print (r[0])

def showRomsInCategory(cat_name):
    print ("Rom list for category %s" % (cat_name))
    sql_cmd = ("SELECT game_name FROM games where category = (\"%s\")" % (cat_name))
    db.cursor.execute(sql_cmd)
    result = db.cursor.fetchall()
    for r in result:
        print (r[0])

def getOrientation_mame2010 (rom_name):
    sql_cmd = ("SELECT orientation FROM games_mame2010 WHERE game_name = (\"%s\")" % (rom_name))
    db.cursor.execute(sql_cmd)
    result = db.cursor.fetchall()
    return result[0]

def getOrientation (rom_name):
    sql_cmd = ("SELECT orientation FROM games WHERE game_name = (\"%s\")" % (rom_name))
    db.cursor.execute(sql_cmd)
    result = db.cursor.fetchall()
    return result[0]

def getRomInformation (rom_name):
    sql_cmd = ("SELECT description, game_name, romof, cloneof, orientation, nplayers, category, controls, buttons FROM games WHERE game_name = (\"%s\")" % (rom_name))
    db.cursor.execute(sql_cmd)
    result = db.cursor.fetchall()

    for r in result:
        print("Game Name : ", r[0])
        print("Rom Name : ", r[1])
        print("Rom of : ", r[2])
        print("Clone of: ", r[3])
        print("Orientation : ", r[4])
        print("NPlayers : ", r[5])
        print("Category : ", r[6])
        print("Controls : ", r[7])
        print("Buttons : ", r[8])
        #print(r)
    print ("%s items found" % (len(result)))


def writeGamelist (result, filename, active_games):

    fobj = open(filename, "w")

    fobj.write("menu \"One Player Games\"\n")
    fobj.write("    sorted = \"true\"\n")
    for r in result:
        print("Game Name : %s\nRom Name %s" % (r[0], r[1]))
        for g in active_games:
            if (r[1] == g.game_name):
                fobj.write("    game { rom = \"%s\" title = \"%s\" params = \";%s\" orientation = \"%s\"}\n" % (g.game_name, g.description, g.core, g.orientation))


    fobj.write("}")
    fobj.close()
    print (filename, " gamelist was written.")

def processOnePlayerGames(active_games):
    sql_cmd = ("SELECT description, game_name, orientation FROM games WHERE players =\"1\"")
    db.cursor.execute(sql_cmd)
    result = db.cursor.fetchall()

    fobj = open("gamelist_oneplayergames.conf", "w")

    fobj.write("menu \"One Player Games\"\n")
    fobj.write("    sorted = \"true\"\n")
    for r in result:
        #print("Game Name : %s\nRom Name %s" % (r[0], r[1]))
        for f in active_games:
            if (r[1] == f.split(".")[0]):
                print (r[2])
                fobj.write("    game { rom = \"%s\" title = \"%s\" params = \";mame2003plus\" orientation = a}\n" % (r[1], r[0]))


    fobj.write("}")
    fobj.close()
    #print ("%s items found" % (len(result)))


def getParentsMame2010():
    sql_cmd = ("SELECT DISTINCT description, game_name, category FROM games_mame2010 WHERE cloneof = \"None\" AND category NOT IN ('Casino', 'Electromechanical', 'System', 'Tabletop', 'Whac-A-Mole', 'Utilities', 'Slot Machine') ORDER BY category ASC")
    #sql_cmd = ("SELECT DISTINCT category FROM games WHERE cloneof = \"None\" AND category NOT IN ('Casino', 'Electromechanical', 'System', 'Tabletop', 'Whac-A-Mole', 'Utilities', 'Slot Machine') ORDER BY category ASC")
    db.cursor.execute(sql_cmd)
    result = db.cursor.fetchall()

    for r in result:
        print("Game Name : %s;Rom Name %s; Category %s" % (r[0], r[1], r[2]))
        #print("Category %s" % (r[0]))
    print ("%s items found" % (len(result)))


def getParents():
    sql_cmd = ("SELECT DISTINCT description, game_name, category FROM games WHERE cloneof = \"None\" AND category NOT IN ('Casino', 'Electromechanical', 'System', 'Tabletop', 'Whac-A-Mole', 'Utilities', 'Slot Machine') ORDER BY category ASC")
    #sql_cmd = ("SELECT DISTINCT category FROM games WHERE cloneof = \"None\" AND category NOT IN ('Casino', 'Electromechanical', 'System', 'Tabletop', 'Whac-A-Mole', 'Utilities', 'Slot Machine') ORDER BY category ASC")
    db.cursor.execute(sql_cmd)
    result = db.cursor.fetchall()

    for r in result:
        print("Game Name : %s;Rom Name %s; Category %s" % (r[0], r[1], r[2]))
        #print("Category %s" % (r[0]))
    print ("%s items found" % (len(result)))

def getRomOfGames():
    sql_cmd = ("SELECT description, game_name, romof FROM games WHERE cloneof = \"None\" AND romof NOT IN (\"None\")")
    db.cursor.execute(sql_cmd)
    result = db.cursor.fetchall()

    for r in result:
        print("Game Name : %s;Rom Name %s ;ROMOF %s" % (r[0], r[1], r[2]))
        #print(r)
    print ("%s items found" % (len(result)))

def getRomOfNeogeo():
    sql_cmd = ("SELECT description, game_name, romof FROM games WHERE romof =(\"neogeo\")")
    db.cursor.execute(sql_cmd)
    result = db.cursor.fetchall()

    for r in result:
        print("Game Name : %s;Rom Name %s;ROMOF %s" % (r[0], r[1], r[2]))
        #print(r)
    print ("%s items found" % (len(result)))

def getRomOfPgm():
    sql_cmd = ("SELECT description, game_name, romof FROM games WHERE romof =(\"pgm\")")
    db.cursor.execute(sql_cmd)
    result = db.cursor.fetchall()

    for r in result:
        print("Game Name : %s;Rom Name %s;ROMOF %s" % (r[0], r[1], r[2]))
        #print(r)
    print ("%s items found" % (len(result)))

def getCategory(rom_name):
    sql_cmd = ("SELECT category FROM games WHERE game_name =\"%s\"" % (rom_name))
    db.cursor.execute(sql_cmd)
    result = db.cursor.fetchall()
    return result

def getOnePlayerGames():
    sql_cmd = ("SELECT description, game_name FROM games WHERE players =\"1\"")
    db.cursor.execute(sql_cmd)
    result = db.cursor.fetchall()

    for r in result:
        print("Game Name : %s\nRom Name %s" % (r[0], r[1]))
        #print(r)
    print ("%s items found" % (len(result)))

def getGamesFrom1981():
    sql_cmd = ("SELECT description, game_name FROM games WHERE year =\"1981\"")
    db.cursor.execute(sql_cmd)
    result = db.cursor.fetchall()

    for r in result:
        print("Game Name : %s\nRom Name %s" % (r[0], r[1]))
    print ("%s items found" % (len(result)))

    return result

def buildActiveArcadeGames (config):
    # get file list for roms from harddisk
    # and build a game list arry
    arcade_rom_path = config.get('System', 'arcade_rom_path')
    folder_list = os.listdir (arcade_rom_path)
    active_games = []
    for folder in folder_list:
        gamelist = os.listdir(arcade_rom_path + "\\" + folder)
        for g in gamelist:
            game = Game()
            game.game_name = g.split(".")[0]
            game.folder = folder
            game.core = config.get('Folders', folder)
            active_games.append (game)

    # attach orientation for each game
    # use mame2010 database
    for g in active_games:
        g.orientation = getOrientation_mame2010(g.game_name)[0]
        if g.orientation == "0":
            g.orientation = "H"
        else:
            g.orientation = "V"
        print (g.game_name, ";", g.core, ";", g.orientation)

def diffDB ():

    # check database mame2003 and mame2010
    result_games = db.execute("SELECT * FROM games")
    result_fbaneo = db.execute("SELECT * FROM games_fbaneo")

    ctr = 0
    ctr_found = 0
    for f in result_fbaneo:
        found = False
        for m in result_games:
            if m[0] == f[0]:
                found = True
        if found == False:
            ctr = ctr +1
            print (f[0], "; ", f[5], " not found")
            print ("trying to find parent ", f[2], " for ", f[0])
            sql_cmd = ("SELECT * from games where game_name is '%s'" % (f[2]))

            parent = db.execute(sql_cmd)
            if len(parent) > 0:
                print ("Parent : ", parent)
                print ("fba game : ", f)
                sql_cmd = ("INSERT INTO games (game_name, cloneof, romof, year, manufacturer, description, players, controls, screen, rotation, orientation, width, height, refresh, category, subcategory, nplayers) VALUES \
                (\"%s\", \"%s\", \"%s\", \"%s\", \"%s\", \"%s\", \"%s\", \"%s\", \"%s\", \"%s\", \"%s\", \"%s\", \"%s\", \"%s\", \"%s\", \"%s\", \"%s\");" \
                % (f[0], f[1], f[2], f[3], parent[0][4], f[5], parent[0][6], parent[0][7], parent[0][8], parent[0][9], parent[0][10], parent[0][11], parent[0][12], parent[0][13], parent[0][14], parent[0][15], parent[0][16]))

                print (sql_cmd)
                db.cursor.execute(sql_cmd)
                db.connection.commit()



        else:
            ctr_found = ctr_found +1

    print (ctr, " missing games")
    print (ctr_found, " matching games")



def main():

    db.connect()

    if sys.argv[1] == "init":
        print ("Initialisation of databases")
        #db.build_db_mame2003plus()
        #db.build_db_mame2010()
        #db.build_db_mame2016()
        #db.build_games_db()
        #db.build_db_fbaneo()

        #diffDB()

    else if sys.argv[1] == "list":
        # get current installed roms
        buildActiveArcadeGames(config)
        if sys.argv[1] == "1button":
            result = getOnePlayerGames()
            writeGamelist(result, "gamelist_1button.conf", active_games)


    # reading config
    else if sys.argv[1] == "config":

        config = configparser.RawConfigParser()
        config.read('gamelist.cfg')

        rom_path = config.get('System', 'rom_path')

        showYear1981 = config.getboolean('Collections', 'show_year_1981')
        showOnePlayerGames = config.getboolean('Collections', 'show_one_player_games')
        showCategories = config.getboolean('Collections', 'show_categories')


        if showOnePlayerGames:
            getOnePlayerGames()

        if showYear1981:
            getGamesFrom1981()

        if showCategories:
            getCategories()
    else
        print ("Help page for regamebox db")
        print ("First init db with python regamebox_db init")
        print ("")
        print ("Usage of parameter :")
        print ("    python regamebox_db list 1button   : list all 1 button games")
        print ("    python regamebox_db config   : list all games via gamelist.cfg")
        print ("    ")

        
    #getCategories
    #showRomsInCategory("Driving")



    #result = getGamesFrom1981()
    #writeGamelist(result, "gamelist_1981.conf", active_games)

    #getRomInformation("1942")
    
    # show all rom which are marked as romof and are no clones
    # theses games should be parents.
    #getRomOfGames()

    #getParents()
    #getRomOfNeogeo()
    #getRomOfPgm()


#    for file in active_games:
#        print (file.split(".")[0])

    #processOnePlayerGames(active_games)


    db.close()

if __name__ == "__main__":
    main()

