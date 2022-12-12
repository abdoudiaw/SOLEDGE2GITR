# Copyright 2022, SOLEDGE contributors
# Authors: Abdou Diaw
# License: 3-Clause-BSD-LBNL
"""
This test file is part SOLEDGE-GITR.

It writes fluid data from SOLEDGE to a SQLITE DB.

"""
# -------
# Imports
# -------
import sqlite3
import argparse
import os
import csv
import numpy as np
import collections
import copy
import warnings

# ----------
# Parameters
# ----------
def getSQLArrGenString(fName, dType, length):
    """
    Check quantities are in required format.
    """
    tString = ""
    if dType == int:
        tString = "INT"
    elif dType == float:
        tString = "REAL"
    else:
        raise Exception('Requested Incompatible SQL Trype')
    retStr = ""
    return retStr
    
    
def ProcessSOLEDGE(dbname, filepath,filename):
    """
    Loads data and write into a SQL DB file.
    """
    fgDB = sqlite3.connect(dbname, timeout=45.0)
    fgCursor = fgDB.cursor()

    gndString = ""
    gndString = "CREATE TABLE IF NOT EXISTS SOLEDGE(R REAL, Z REAL, "
    gndString += "BPHI REAL, BR REAL, BZ REAL, "
    gndString += "TE REAL, NE REAL, VE REAL, "
    gndString += "TI REAL, NI REAL, VI REAL);"

    sqlDB = sqlite3.connect(dbname)
    sqlCursor = sqlDB.cursor()
    sqlCursor.execute(gndString)

    txt = os.path.join(filepath, filename)

    trainingEntries = np.loadtxt(txt, comments='#')
    ZBARvalues = collections.namedtuple('Tablequantities', 'R Z BPHI BR BZ TE VE NE TI VI NI')
    for row in trainingEntries:
            res = ZBARvalues(R=row[0], Z=row[1], BPHI=row[2],
                        BR=row[3], BZ=row[4], TE=row[5],
                        NE=row[6], VE=row[7], TI=row[8],
                        NI=row[9], VI=row[10])
                        
            sqlCursor = sqlDB.cursor()
            insString = "INSERT INTO SOLEDGE VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
            insArgs = (res.R, res.Z, res.BPHI, res.BR, res.BZ,
            res.TE, res.NE, res.VE, res.TI, res.NI, res.VI
            )
            sqlCursor.execute(insString, insArgs)
            sqlDB.commit()
            sqlCursor.close()


# Specify data path, input filename, and output file name
B_path='./'
B_filename='data.txt'
dbname='data.db'
ProcessSOLEDGE(dbname, B_path,B_filename)

