# 24.1.2015 I.Zliobaite
# compare score distributions of three shooters

wd <- getwd() 
wd <- substr(wd,1,nchar(wd)-6)
wd <- paste(wd,'3_data/collected_by_hand/',sep='')

input_file_base <- '_swedishcup2015'
shooters <- c('iz','pfs','myk')
starts <- c('a','b','c')

data <-c(1:120)
for (ind_shooter in 1:3)
{
  data_now <- c()
  for (ind_start in 1:3)
  {
    file_now <- paste(wd,shooters[ind_shooter],input_file_base,starts[ind_start],'.txt',sep='')
    dt <- read.csv(file_now,header = FALSE)
    data_now <- rbind(data_now,dt)
  }
  data <- cbind(data,data_now)
}


  
data <- data[,2:4]
colnames(data) <- shooters

br_vec <- seq(8,11,by=0.2)

for (sk in 1:3)
{
  hist(data[,shooters[sk]],breaks = br_vec,main = shooters[sk])
  file_name <- paste('plots_swedishcup/fig_hist_',shooters[sk],'.png',sep='')
  dev.copy(png,file_name)
  dev.off()
}
boxplot(data)
dev.copy(png,'plots_swedishcup/fig_boxplot.png')
dev.off()

