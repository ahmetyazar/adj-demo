import sys
import logging
import rds_config
import pymysql

# rds settings
rds_host = "creditadjudication.cz3lpdttkjpo.us-east-1.rds.amazonaws.com"
name = rds_config.db_username
password = rds_config.db_password
db_name = rds_config.db_name
logger = logging.getLogger()
logger.setLevel(logging.INFO)
try:
    conn = pymysql.connect(rds_host, user=name, passwd=password, db=db_name,
                           connect_timeout=5)
except:
    logger.error("ERROR: Unexpected error: Could not connect to MySql instance.")
    sys.exit()
logger.info("SUCCESS: Connection to RDS mysql instance succeeded")


def handler(event, context):
    """
    This function fetches content from mysql RDS instance
    """
    with conn.cursor() as cur:
        # create Customers db and load some sample records
        cur.execute("drop database if exists PartyDb")
        cur.execute("create database PartyDb")
        cur.execute("use PartyDb")
        cur.execute("create table Party (partyID int NOT NULL AUTO_INCREMENT, " +
                    "partyType varchar(255) NOT NULL, " +
                    "legalName varchar(255) NOT NULL, " +
                    "corporateAddress varchar(255) NOT NULL, " +
                    "branchOfAccount varchar(255) NOT NULL, " +
                    "SICCode varchar(255) NOT NULL, " +
                    "financingType varchar(255) NOT NULL, " +
                    "PRIMARY KEY (partyID))")
        cur.execute('insert into Party (partyType, legalName, ' + 
                     'corporateAddress, branchOfAccount, SICCode, financingType)' +
                     ' values ("LegalEntity", "Center Agriculture", "456 Shepherd Ave. East, Toronto, ON M5G7K9",' +
                     '"Bayview Village", "Agriculture", "Line")')
        cur.execute('insert into Party (partyType, legalName, ' + 
                     'corporateAddress, branchOfAccount, SICCode, financingType)' +
                     ' values ("LegalEntity", "BMO Financial", "3356 Bay St., Toronto, ON M5G7K9",' +
                     '"Toronto Downtown", "Financial", "Loan")')
        cur.execute('insert into Party (partyType, legalName, ' + 
                     'corporateAddress, branchOfAccount, SICCode, financingType)' +
                     ' values ("Person", "Toys R Us", "66 Shepherd Ave. West, Toronto, ON L5L7K9",' +
                     '"Scarborough", "Consumer Goods", "LOC")')
        conn.commit()
        cur.execute("select * from PartyDb.Party")
        
        item_count = 0
        for row in cur:
            item_count += 1
            logger.info(row)
        logger.info("Added %d items from RDS MySQL table" % (item_count))
        
        cur.execute("create table PartyRelationship (partyID int NOT NULL, " +
                    "relatedPartyID int NOT NULL, " +
                    "relationshipType varchar(255) NOT NULL)")
        cur.execute('insert into PartyRelationship (partyID, relatedPartyID, ' + 
                    'relationshipType) values (2,1,"Parent")')
        conn.commit()
        cur.execute("select * from PartyDb.PartyRelationship")
        
        item_count = 0
        for row in cur:
            item_count += 1
            logger.info(row)
        logger.info("Added %d items from RDS MySQL table" % (item_count))        
 
        cur.execute("create table Score (scoreID int NOT NULL AUTO_INCREMENT," +
                    "partyID int NOT NULL, " +
                    "scoreType varchar(255) NOT NULL, " +
                    "score int NOT NULL, " +
                    "scoreDate DATETIME, " +   
                    "PRIMARY KEY (scoreID))")
        cur.execute('insert into Score (partyID, scoreType, score, scoreDate)' + 
                    ' values (1,"Behavior",456,"2016-08-17 22:52:21")')
        cur.execute('insert into Score (partyID, scoreType, score, scoreDate)' + 
                    ' values (1,"Credit",789,"2016-08-17 22:52:21")')
        cur.execute('insert into Score (partyID, scoreType, score, scoreDate)' + 
                    ' values (2,"Credit",567,"2017-04-17 22:52:21")')
        conn.commit()
        cur.execute("select * from PartyDb.Score")
        
        item_count = 0
        for row in cur:
            item_count += 1
            logger.info(row)
        logger.info("Added %d items from RDS MySQL table" % (item_count))  
       
                        
        # Create Facility database
        cur.execute("drop database if exists FacilityDb")
        cur.execute("create database FacilityDb")
        cur.execute("use FacilityDb")
        cur.execute("create table Facility ( facilityID int NOT NULL AUTO_INCREMENT, " +
                    "facilityType varchar(255) NOT NULL, " +
                    "status tinyint NOT NULL, " +
                    "startDate DATETIME, " +         
                    "PRIMARY KEY (facilityID))")
        cur.execute('insert into Facility (facilityType, status, startDate)' + 
                     ' values ("Line",1,"2010-05-17 22:52:21")')
        cur.execute('insert into Facility (facilityType, status, startDate)' + 
                     ' values ("Loan",1,"2015-08-17 22:52:21")')
        cur.execute('insert into Facility (facilityType, status, startDate)' + 
                     ' values ("LOC",0,"2016-08-17 22:52:21")')
        conn.commit()
        cur.execute("select * from FacilityDb.Facility")

        for row in cur:
            item_count += 1
            logger.info(row)
        logger.info("Added %d items from RDS MySQL table" % (item_count))
        
        
        cur.execute("create table FacilityParty ( facilityID int NOT NULL, " +
                    "partyID int NOT NULL, " +
                    "relationshipType varchar(255) NOT NULL, " +
                    "effectiveDate DATETIME, " +   
                    "expiryDate DATETIME, " +      
                    "PRIMARY KEY (facilityID, partyID))")
        cur.execute('insert into FacilityParty (facilityID, partyID, ' +
                    'relationshipType, effectiveDate, expiryDate) values (' +
                    '1,1,"Owner", "2010-05-17 22:52:21",NULL)')
        cur.execute('insert into FacilityParty (facilityID, partyID, ' +
                    'relationshipType, effectiveDate, expiryDate) values (' +
                    '1,3,"Guarantor", "2010-05-17 22:52:21",NULL)')
        cur.execute('insert into FacilityParty (facilityID, partyID, ' +
                    'relationshipType, effectiveDate, expiryDate) values (' +
                    '2,2,"Owner", "2010-05-17 22:52:21",NULL)')
        cur.execute('insert into FacilityParty (facilityID, partyID, ' +
                    'relationshipType, effectiveDate, expiryDate) values (' +
                    '3,3,"Owner", "2010-05-17 22:52:21",NULL)')
        conn.commit()
        cur.execute("select * from FacilityDb.FacilityParty")

        for row in cur:
            item_count += 1
            logger.info(row)
        logger.info("Added %d items from RDS MySQL table" % (item_count))
        
        cur.execute("create table Measure ( measureID int NOT NULL AUTO_INCREMENT, " +
                    "measureName varchar(255) NOT NULL, " +
                    "measureType varchar(255) NOT NULL, " +
                    "facilityID int NOT NULL, " +
                    "value int NOT NULL, " +
                    "effectiveDate DATETIME, " +   
                    "expiryDate DATETIME, " +
                    "PRIMARY KEY (measureID))")
        cur.execute('insert into Measure (measureName, measureType, facilityID, ' +
                    'value, effectiveDate, expiryDate) values (' +
                    '"CurrentBalance","Balance",1, 4354353.45, "2017-05-17 22:52:21",' +
                    '"2017-05-18 22:52:21")')
        cur.execute('insert into Measure (measureName, measureType, facilityID, ' +
                    'value, effectiveDate, expiryDate) values (' +
                    '"CurrentBalance","Balance",1, 4354353.45, "2017-05-18 22:52:21",' +
                    'NULL)')
        cur.execute('insert into Measure (measureName, measureType, facilityID, ' +
                    'value, effectiveDate, expiryDate) values (' +
                    '"CreditLimit","Limit",1, 777753.45, "2017-05-17 22:52:21",NULL)')
        conn.commit()
        cur.execute("select * from FacilityDb.Measure")

        for row in cur:
            item_count += 1
            logger.info(row)
        logger.info("Added %d items from RDS MySQL table" % (item_count))
        
        cur.execute("create table FacilityDb.BlockedCustomers ( " +
                    "blockedCustomerID int NOT NULL AUTO_INCREMENT, " +
                    "partyID int NOT NULL, " +
                    "effectiveDate DATETIME, " +
                    "PRIMARY KEY (blockedCustomerID))")
        conn.commit()

        # Create Fulfillment database
        cur.execute("drop database if exists FulfillmentDb")
        cur.execute("create database FulfillmentDb")
        cur.execute("use FulfillmentDb")
        cur.execute("create table BlockedCustomers ( " +
                    "blockedCustomerID int NOT NULL AUTO_INCREMENT, " +
                    "partyID int NOT NULL, " +
                    "effectiveDate DATETIME, " +
                    "PRIMARY KEY (blockedCustomerID))")
        conn.commit()

        # Create PotentialFraud and ProcessLimitIncrease tables
        cur.execute("create table FulfillmentDb.PotentialFraud ( " +
                    "potentialFraudID int NOT NULL AUTO_INCREMENT, " +
                    "partyID int NOT NULL, " +
                    "fraud int NOT NULL, " +
                    "PRIMARY KEY (potentialFraudID))")
        cur.execute('insert into FulfillmentDb.PotentialFraud (partyID, fraud) ' + \
                    'values (1,1)')
        conn.commit()

        cur.execute("create table FulfillmentDb.ProcessLimitIncrease ( " +
                    "processLimitIncreaseID int NOT NULL AUTO_INCREMENT, " +
                    "partyID int NOT NULL, " +
                    "facilityID int NOT NULL, " +
                    "newCreditLimit int, " +
                    "PRIMARY KEY (processLimitIncreaseID))")
        conn.commit()
        