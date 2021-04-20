df=read.csv('data/costs/insurance.csv')
boxplot(df$charges ~ df$region , col=rgb(0.3,0.5,0.4,0.6) , 
        ylab="Insurance Fee" , 
        xlab="Regions")+
theme_bw()