# install.packages("RMySQL")
library(RMySQL)
mydb <- dbConnect(MySQL(), user='root', password='example', dbname='nl_cow', host='srv-cdms')
dbListTables(mydb)
data <- fetch(dbSendQuery(mydb, "select * from MilkInfo"))

# Reference: https://mkmanu.wordpress.com/2014/07/24/r-and-mysql-a-tutorial-for-beginners/