create table PartyRelationship (partyID int NOT NULL, relatedPartyID int NOT NULL, relationshipType varchar(255) NOT NULL);
insert into PartyRelationship (partyID, relatedPartyID, relationshipType) values (2,1,"Parent");

create table Facility ( facilityID int NOT NULL AUTO_INCREMENT, facilityType varchar(255) NOT NULL, status tinyint NOT NULL, startDate DATETIME, PRIMARY KEY (facilityID));

insert into Facility (facilityType, status, startDate) values ("Line",1,"2010-05-17 22:52:21");

create table FacilityParty ( facilityID int NOT NULL, partyID int NOT NULL, relationshipType varchar(255) NOT NULL, effectiveDate DATETIME, expiryDate DATETIME, PRIMARY KEY (facilityID, partyID));

insert into FacilityParty (facilityID, partyID, relationshipType, effectiveDate, expiryDate) values (1,1,"Owner", "2010-05-17 22:52:21",NULL);


create table Measure ( measureID int NOT NULL AUTO_INCREMENT, measureName varchar(255) NOT NULL, measureType varchar(255) NOT NULL, facilityID int NOT NULL, value int NOT NULL, effectiveDate DATETIME, expiryDate DATETIME, PRIMARY KEY (measureID));

insert into Measure (measureName, measureType, facilityID, value, effectiveDate, expiryDate) values ("CurrentBalance","Balance",1, 4354353.45, "2017-05-17 22:52:21","2017-05-18 22:52:21");
