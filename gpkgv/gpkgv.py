import argparse
import pglast
import sqlite3
import sys

def parseSQL(filename: str):
    root = None
    fd = open(filename, 'r')
    sqlFile = fd.read()
    fd.close()
    try:
        root = pglast.parse_sql(sqlFile)
    except pglast.parser.ParseError as e:
        print(e)
    return root

def isGeopackage(filename: str):
    try:
        conn = sqlite3.connect(filename)
        cursor = conn.cursor()
        # Get all the tables of the database
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        conn.close()
        # 'tables' must contain 'gpkg_spatial_ref_sys' etc. as specified by the OGC
        return any([item[0].startswith('gpkg') for item in tables])
    except sqlite3.Error as e:
        return False

def parseCommandLine():
    
    parser = argparse.ArgumentParser(description = 'GeoPacKaGe Validator')

    parser.add_argument("geopackage", type = argparse.FileType('r'), help = "geopackage to validate")
    parser.add_argument("specification", type = argparse.FileType('r', encoding = 'utf-8'), help = "geopackage specification")
    # Create report file if option -r
    parser.add_argument("-r", "--report", type = argparse.FileType('w', encoding = 'utf-8'), help = "validation report")
    parser.add_argument("-v", "--verbose", action = "store_true", help = "increase output verbosity")
    
    return parser.parse_args()

def main():
    # Get the arguments and options of the command line
    args = parseCommandLine()
    # Test whether args.geopackage is a geopackage file
    if not isGeopackage(args.geopackage.name):
        sys.exit(f'file {args.geopackage.name} is not a geopackage')
    # Test whether args.specification is a SQL file
    root = parseSQL(args.specification.name)
    if root is None:
        sys.exit(f'file {args.specification.name} is not a proper SQL file')

if __name__ == '__main__':
    main()