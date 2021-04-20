library(corrplot)
library(viridis)
library(ggplot2)

df=read.csv('correlation.csv')
matrix = df[1:7,2:8]

colnames(matrix)<-c('Age','Sex','BMI','N Dep','S Habit','Region','Charges')
corrplot.mixed(data.matrix(matrix), order = "hclust",number.cex = .9,lower.col = "black",
               upper.col=viridis(10000))
