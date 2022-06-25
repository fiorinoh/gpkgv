import argparse

def main():
    parser = argparse.ArgumentParser(description = 'Geopackage validator')
    parser.add_argument("geopackage", type = open, help = "geopackage to validate")
    parser.add_argument("specification", type = open, help = "geopackage specification")
    parser.add_argument("-r", "--report", type = argparse.FileType('w', encoding = 'utf-8'), help = "validation report")
    parser.add_argument("-v", "--verbose", action = "store_true", help = "increase output verbosity")
    parser.parse_args()

if __name__ == '__main__':
    main()