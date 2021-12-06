from models.parser import Parser
from models.db_model import DB_Model

def main():
    # connects to MySQL DB, removes tables (if exits), and creates tables
    db = DB_Model()

    parser = Parser()
    # parses table records / instances into Python lists
    parser.process_file()
    
    # assign the record lists to their respective MySQL tables
    # assigning magazine records
    db.assign_table_recs(parser.magazines, "magazine")
    # assigning customer records
    db.assign_table_recs(parser.customers, "customer")

    db.print_records()
    db.destructor()

if __name__ == "__main__":
    main()