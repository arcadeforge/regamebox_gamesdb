# include <sqlite3.h>
# include <stdio.h>

int callback(void *nused, int argc, char **argv, char **col);

int main(void) {
    printf("%s\n", sqlite3_libversion());
    sqlite3 *db;
    char *err_msg = 0;

    int rc = sqlite3_open("games.db", &db);
    if ( rc != SQLITE_OK ) 
        printf ("can not open db.\n");
    else
        printf ("open db.\n");

    printf("building query\n");
    char *rom_name = "1942";
    //char *sql = "SELECT description, game_name, romof, cloneof, orientation, nplayers, category FROM games WHERE game_name = (\"%s\")" , rom_name);

    char *sql = "SELECT description, game_name, romof, cloneof, orientation, nplayers, category FROM games WHERE game_name = (\"1942\")";
    //char *sql = "SELECT * FROM games";
    rc = sqlite3_exec(db, sql, callback, 0, &err_msg);

    if ( rc != SQLITE_OK ) 
    {
        printf("failed to select data: %s\n", &err_msg);

        sqlite3_free(err_msg);
        sqlite3_close(db);
        return 1;
    }
    else 
    {
        printf("success select data\n");

    }


    sqlite3_close(db);
    return 0;
}

int callback(void *nused, int argc, char **argv, char **col)
{
    nused = 0;
    for (int i=0; i < argc; i++)
    {
        printf("%s = %s\n", col[i], argv[i] ? argv[i] : "NULL");
    }
    printf ("\n");
    return 0;
}
