#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2 #basic library to interact with psql database
import psycopg2.extras #imported this to have dictionary cursor
import bleach #to make it script safe

def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database without any constraint"""
    DB  = connect()
    cur = DB.cursor()

    cur.execute("""delete from matches""")
    DB.commit()
    DB.close()


def deletePlayers():
    """Remove all the player records from the database without any constraint"""
    DB  = connect()
    cur = DB.cursor()

    cur.execute("""delete from players""")
    DB.commit()
    DB.close()


def countPlayers():
    """Returns the number of players currently registered in the tournament"""
    DB  = connect()
    cur = DB.cursor(cursor_factory=psycopg2.extras.DictCursor)

    cur.execute("""select count(*) as count from players""")
    count = cur.fetchone()["count"] #such fetching possible because of dictionary cursor
    DB.close()

    return count


def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """

    DB  = connect()
    cur = DB.cursor()

    #inserting

    safe_name = bleach.clean(name) #cleaning name input using bleach
    cur.execute("""insert into players(player_name) values(%s)""",(safe_name,))
    DB.commit()
    DB.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """

    DB  = connect()
    cur = DB.cursor()

    #created a view on top of matches table to fetch player standings directly, definition in sql file
    #results already sored in view based on wins
    cur.execute("""select * from player_standings""")
    standings = cur.fetchall()
    DB.close()

    return standings


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """

    DB  = connect()
    cur = DB.cursor()

    cur.execute("""insert into matches(winner,loser) values(%s,%s)""",(winner,loser,))
    DB.commit()
    DB.close()


def swissPairings():
    """Returns a list of pairs of players for the next round of a match.

    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    DB  = connect()
    cur = DB.cursor()

    #fetch players by standings
    cur.execute("""select player_id, player_name from player_standings""")
    standings = cur.fetchall()

    swiss_pairings = [] #final pairing list of matches

    num_of_players = len(standings)
    num_of_players = (num_of_players - (num_of_players%2)) #taking care of edge case of odd players

    #loop over all players by standings and group two players
    i = 0
    while(i < num_of_players):
        #merging two tuples like (id1,name1) and (id2,name2) to (id1,name1,id2,name2)
        swiss_pairings.append(standings[i] + standings[i+1])
        i += 2

    return swiss_pairings