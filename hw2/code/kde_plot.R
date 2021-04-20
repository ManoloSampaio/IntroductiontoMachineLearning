library(viridis)
library(ggplot2)
df=read.csv('data/costs/insurance.csv')
df$charges = log10(df$charges)
ggplot(data=df, aes(charges,fill=region,color=region)) +
  geom_density(alpha=0.2)+
  theme_bw()+
  theme(panel.border = element_blank(), panel.grid.major = element_blank(),
        panel.grid.minor = element_blank(), axis.line = element_line(colour = "black"))+
  xlab('Insurance Fee')+ylab('Density')
  #scale_fill_discrete_qualitative(palette = "Harmonic", nmax = 5, order = c(5, 1, 2))
