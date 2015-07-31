# 2015 07 31 I.Zliobaite
# analyzing differences between 

input_directory <- 'scores'
output_directory <- 'plots/'


files <- list.files(input_directory)

for (sk in 1:length(files))
{
  file_now <- files[sk]
  date_now <- substr(file_now,1,11)
  file_now <- paste(input_directory,file_now,sep='/')
  plot_name_now <- paste(output_directory,date_now,'.pdf',sep='')
  data_now <- read.csv(file_now, header = FALSE, sep = ',')
  n <- dim(data_now)[1]
  p <- dim(data_now)[2]
  data_scores <- c()
  for (sk2 in 1:n)
  {
    scores_now <- data_now[sk2,4:p]
    data_scores <- rbind(data_scores,cbind(sum(scores_now),sum(floor(scores_now))))
  }
  colnames(data_now) <- c('full score','decimal score')
  pdf(plot_name_now)
  plot(data_scores[,2],data_scores[,1],main = date_now)
  dev.off()
}


