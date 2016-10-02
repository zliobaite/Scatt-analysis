# 2015 07 31 I.Zliobaite
# analyzing differences between 

input_directory <- 'scores'
output_directory <- 'plots/'
input_file_athletes <- 'athlete_bios.csv'

data_ath <- read.csv(input_file_athletes, header = TRUE, sep = ';')

files <- list.files(input_directory)

for (sk in 1:length(files))
{
  file_now <- files[sk]
  date_now <- substr(file_now,1,11)
  file_now <- paste(input_directory,file_now,sep='/')
  plot_name_now <- paste(output_directory,date_now,'.pdf',sep='')
  plot_name_now1 <- paste(output_directory,date_now,'_scores.pdf',sep='')
  plot_name_now2 <- paste(output_directory,date_now,'_variance.pdf',sep='')
  data_now <- read.csv(file_now, header = FALSE, sep = ',')
  n <- dim(data_now)[1]
  p <- dim(data_now)[2]
  data_scores <- c()
  for (sk2 in 1:n)
  {
    scores_now <- data_now[sk2,4:p]
    ind <- which(as.vector(data_ath[,'ID']) == as.vector(data_now[sk2,2]))
    data_scores <- rbind(data_scores,cbind(sum(scores_now),sum(floor(scores_now)),sd(scores_now),data_ath[ind,'yob']))
  }
  colnames(data_scores) <- c('decimal_score','rounded_score','sd','yob')
  if (data_scores[1,1]>500){
    ind <- which(data_scores[,2]>=570)
    data_scores <- data_scores[ind,]
  }else{
    ind <- which(data_scores[,2]>=380)
    data_scores <- data_scores[ind,]
  }
  ind1 <- which(data_scores[,'yob']<1985)
  ind2 <- which(data_scores[,'yob']>=1985)
  pdf(plot_name_now1, height = 5, width = 5)
  plot(data_scores[,2],data_scores[,1],main = date_now,xlab="round score",ylab="decimal score")
  points(data_scores[ind1,2],data_scores[ind1,1],col = 'black')
  points(data_scores[ind2,2],data_scores[ind2,1],col = 'red')
  legend("bottomright",c("born before 1985","born 1985 and younger"),pch = c(1,1),col=c('black','red'))
  dev.off()
  #pdf(plot_name_now2, height = 5, width = 5)
  #plot(data_scores[,1],data_scores[,3],main = date_now,xlab="decimal score",ylab="deviation")
  #points(data_scores[ind1,1],data_scores[ind1,3],col = 'black')
  #points(data_scores[ind2,1],data_scores[ind2,3],col = 'red')
  #legend("bottomright",c("born before 1985","born 1985 and younger"),pch = c(1,1),col=c('black','red'))
  #dev.off()
}


