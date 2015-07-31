# 2015 07 31 I.Zliobaite
# extract unique athlete IDs

input_directory <- 'athletes'
output_file <- 'athleteID_master.txt'

files <- list.files(input_directory)

IDs_all <-c()
for (sk in 1:length(files))
{
  file_now <- paste(input_directory,files[sk],sep='/')
  IDs_now <- read.csv(file_now, header = FALSE, sep = ',')
  IDs_all <- rbind(IDs_all,IDs_now)
}

un_IDs <- unique(IDs_all)

write.table(un_IDs, file = output_file, row.names = FALSE, col.names = FALSE, sep = ',', quote = FALSE)
