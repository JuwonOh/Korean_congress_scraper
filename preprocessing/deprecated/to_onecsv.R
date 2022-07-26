library(dplyr)
library(readr)
library(ggplot2)
library(plotly)
library(grid)
library(gridExtra)
library(DT)
library(GGally)
library(randomForest)
library(stringr)
library(udpipe)
library(tidyverse)
library(tidytext)
library(purrr)
library(data.table)

setwd('~/Dropbox/Korean_Legislature')

## load draft lagislation
draft_path <- "~/Dropbox/Korean_Legislature/data/Legislation/Draft"
draft_list <- list.files(draft_path , pattern="*.json", full.names=TRUE)
draft <- purrr::map_df(draft_list, function(x) { 
  purrr::map(jsonlite::fromJSON(x), function(y) ifelse(is.null(y), NA, y)) 
})
draft['bill_result'] <- 'draft'

## load modification legislation
modification_path <- "~/Dropbox/Korean_Legislature/data/Legislation/Modification"
modification_list <- list.files(modification_path, pattern="*.json", full.names=TRUE)
modification <- purrr::map_df(modification_list, function(x) { 
  purrr::map(jsonlite::fromJSON(x), function(y) ifelse(is.null(y), NA, y)) 
})
modification['bill_result'] <- 'modification'

## load rejected legislation
rejected_path <- "~/Dropbox/Korean_Legislature/data/Legislation/rejected"
rejected_list <- list.files(rejected_path, pattern="*.json", full.names=TRUE)
rejected <- purrr::map_df(rejected_list, function(x) { 
  purrr::map(jsonlite::fromJSON(x), function(y) ifelse(is.null(y), NA, y)) 
})
rejected ['bill_result'] <- 'rejected'

## making raw csv file

raw_result <- rbind(draft, modification, rejected)
write.csv(raw_result, file = "raw_result.csv", fileEncoding = "UTF-8")

## loading csv file
raw_file <- read.csv('raw_result.csv', fileEncoding = "UTF-8")
raw_file <- raw_file %>% separate(url, c('url', 'remove', 'billNo'), "=")  

raw_file <- select(raw_file, -1:-3)

## change names for english 

names(raw_file)[8:15] <- c("abstention", "nonattendance", "trip", "vacation", "absent", "agree", "date", "disagree")

## remain only votting bill

vote <- filter(raw_file, vote_result != " ")

## seperate_bill status
abstention <- select(vote, 'billNo':'abstention', 'date', 'bill_result')
abstention['vote'] <- 'abstention'
abstention <- separate_rows(abstention, abstention, convert = TRUE)
names(abstention)[8] <- 'name'

nonattendance <- select(vote, 'billNo':"scraping_date", "nonattendance", 'date', 'bill_result')
nonattendance['vote'] <- "nonattendance"
nonattendance <- separate_rows(nonattendance, nonattendance, convert = TRUE)
names(nonattendance)[8] <- 'name'

trip <- select(vote, 'billNo':"scraping_date", 'trip', 'date', 'bill_result')
trip['vote'] <- 'trip'
trip <- separate_rows(trip, trip, convert = TRUE)
names(trip)[8] <- 'name'

vacation <- select(vote, 'billNo':"scraping_date", "vacation", 'date', 'bill_result')
vacation['vote'] <- "vacation" 
vacation <- separate_rows(vacation, vacation, convert = TRUE)
names(vacation)[8] <- 'name'

absent <- select(vote, 'billNo':"scraping_date", "absent", 'date', 'bill_result')
absent['vote'] <- "absent"
absent <- separate_rows(absent, absent, convert = TRUE)
names(absent)[8] <- 'name'

agree <- select(vote, 'billNo':"scraping_date", "agree", 'date', 'bill_result')
agree['vote'] <- "agree"
agree <- separate_rows(agree, agree, convert = TRUE)
names(agree)[8] <- 'name'

disagree <- select(vote, 'billNo':"scraping_date", "disagree", 'date', 'bill_result')
disagree['vote'] <- "disagree"
disagree <- separate_rows(disagree, disagree, convert = TRUE)
names(disagree)[8] <- 'name'

vote <- rbind(abstention,nonattendance, trip, vacation, absent,agree,disagree)
vote <- vote[!is.na(vote$name),]  # for each status NA

vote$vote_result <- gsub("\\|", ",", vote$vote_result)
vote$initiator <- gsub(",", "", vote$initiator)
vote$title <- gsub("[$*?[^{|\\#%&~_/<=>!,:;`\")(}@-],", "", vote$title)

## big problem: two sungtae kim and two choi kyunghwan

kim1 <- readxl::read_xlsx('data/hand_html/kim1.xlsx') ## floor leader
kim1['name'] <- "김성태(원)"
kim2 <- readxl::read_xlsx('data/hand_html/kim2.xlsx') ## 
kim2['name'] <- "김성태(비례)"
choi1 <- readxl::read_xlsx('data/hand_html/choi(park).xlsx') ## jail
choi1['name'] <- "최경환(감옥)"
choi2 <- readxl::read_xlsx('data/hand_html/choi(nation).xlsx')## nation party
choi2['name'] <- "최경환(국)"

names(first)

same_name <- rbind(kim1, kim2, choi1, choi2)
same_name <- same_name %>% select("billNo", "procResultCd", "resultVote","name" )
names(same_name) <- c("billNo", "bill_result", "vote", "name")

same_name$bill_result <- gsub("원안가결", "draft", same_name$bill_result)
same_name$bill_result <- gsub("수정가결", "modification", same_name$bill_result)
same_name$bill_result <- gsub("부결", "rejected", same_name$bill_result)
same_name$bill_result <- as.factor(same_name$bill_result)

same_name$vote <- gsub("찬성", "agree", same_name$vote)
same_name$vote <- gsub("기권", "absent", same_name$vote)
same_name$vote <- gsub("반대", "disagree", same_name$vote)

temp <- filter(raw_file, vote_result != " ")

names(temp)
names(same_name)
temp <- select(temp, 'billNo':"scraping_date", 'date', 'bill_result')

temp1 <- merge(same_name, temp, by = c("billNo","bill_result"))

vote <- rbind(temp1, vote)


## bill result need more advanced function : https://community.rstudio.com/t/split-uneven-length-vectors-to-columns-with-tidyr/2704/4
vote <- vote %>% separate(vote_result, c('total', 'agree', 'abstention', 'nonattendance', 'trip', 'vacation', 'absent'), ",")  

## loading invididual information

individual <- readxl::read_xlsx('data/data-assembly/assembly_modified.xlsx')
names(individual)[1] <- "name"
individual <- select(individual, c("name", "birth", "party","district","committee","when_elected"))
individual %>% filter(name == "김성태")

total <- merge(individual, vote, by = 'name')

TEMP <- total[is.na(total$party),]  
## Let's look at the congressman who have dropped out in the middle.

vote_name <- unique(vote$name)
data_name <- unique(individual$name)
setdiff(vote_name, data_name)
# supply individual information by exel "박남춘" "최명길" "박준영" "김경수" "오세정" "윤종오" "문미옥" "이철우" "노회찬" "안철수" "배덕광" "박찬우" "송기석" "김종인" "양승조" "권석창" "여영국" "정점식" "정은혜" "김종태"


`%nin%` = Negate(`%in%`)
first <- total %>% filter(name %nin% "최경환"|name %nin% "김성태")

xlsx::write.xlsx(first, file = "data/fisrt_complete.xlsx")



unique(same_name$vote)
unique(raw_file$)

c("abstention", "nonattendance", "trip", "vacation", "absent", "agree", "date", "disagree")




read.csv("data/fisrt_complete.csv")

bill <- read_csv("data/fisrt_complete.csv")

library(pryr)
object_size(first)
