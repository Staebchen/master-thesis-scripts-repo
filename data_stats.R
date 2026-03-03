# get libraries
library(rstatix)
library(dplyr)
library(glue)
library(ggplot2)
library(ggsignif)
library(plyr)
library(htester)

# name of the input csv file
file <- "pst_prosody"

# if values of dependent variable are numeric or not
dv_is_numeric = TRUE

#reduce for larger iv value counts as needed
font_size = 4

# labels, change as needed
x_axis <- "distance to following prosodic boundary"
y_axis <- "% of scores"
legend <- "scores"
y_violin <- "scores"

# data_pron
# read csv data into data_pron
data_pron <- read.csv2(glue("~/Uni/Masterstudium/Masterarbeit/rscript/{file}.csv"), header=TRUE)
# return first 6 rows of data_pron
head(data_pron)

# calculations & tests
if (dv_is_numeric == TRUE) {
  # get the mean of the scores for each Cat in sub_pron
  means <- tapply(data_pron$dep, data_pron$indep, mean)
  write.csv(means, glue("~/Uni/Masterstudium/Masterarbeit/rscript/{file}_means.csv"))
  
  # TESTS on data
  # Kruskal Wallis test of data_pron
  k <- kruskal.test(dep ~ indep, data = data_pron)
  k
  write.csv(htest_data_frame(k), glue("~/Uni/Masterstudium/Masterarbeit/rscript/{file}_kruskal.csv"))
  
  # oneway analysis of means test of data_pron
  oneway.test(dep ~ indep, data = data_pron)
  # analysis of variance test on data_pron
  anova_model <- aov(dep ~ indep, data = data_pron)
  summary(anova_model)
  
  # dunn test
  # dunn test compares kruskal results for all possible group pairs
  d <- dunn_test(dep ~ indep, data = data_pron, p.adjust.method = "bonferroni")
  # give new column to d with effect size r
  d$r <- d$statistic/sqrt(d$n1+d$n2)
  # print d with all rows
  print(d, n=nrow(d))
  write.csv(d, glue("~/Uni/Masterstudium/Masterarbeit/rscript/{file}_dunn.csv"))
  
  # make new dataframe out of means
  x <- as.data.frame(means)
  data_means <- data.frame(
    indep = rownames(x),
    means = as.list(x[1])
  )
  
  # make 2-length vectors for significance comparison
  vec_list <- vector(mode = "list", length = 0)
  for(i in 1:nrow(data_means)) {
    for(j in 1:nrow(data_means)) {
      if(!(i == j)) {
        if(!(list(c(data_means$indep[i], data_means$indep[j])) %in% vec_list)) {
          if (!(list(c(data_means$indep[j], data_means$indep[i])) %in% vec_list)){
            vec_list <- append(vec_list, list(c(data_means$indep[i], data_means$indep[j])))
          }
        }
      }
    }
  }
} else {
  c <- chisq.test(data_pron$indep, data_pron$dep)
  write.csv(head(c), glue("~/Uni/Masterstudium/Masterarbeit/rscript/{file}_chi2.csv"))
}

# # violin plot
# ggplot(data_pron, aes(x = indep, y = dep, fill=indep)) +
#   labs(x = x_axis, y = y_violin) +
#   geom_violin() +
#   geom_boxplot(width=0.1, outliers = FALSE) +
#   stat_summary(fun.y = mean, geom="point", size = 2, color="black") +
#   #stat_summary(fun.y = median, geom="point", size = 2, color="black") +
#   scale_fill_brewer(palette="Blues") + 
#   #  geom_signif(comparisons = list(c("content", "function")), map_signif_level=TRUE) +
#   theme(legend.position="none")
# # save
# ggsave(glue("{file}_violin.png"), plot = get_last_plot())

# # scatter plot
# ggplot(data_pron, aes(x = indep, y = dep)) +
#   labs(x = x_axis, y = y_violin) +
# #  geom_boxplot(notch=TRUE, outliers = FALSE) +
#   geom_point(position = position_jitter(seed = 1, width = 0.3, height = 0.1), size=0.5) +
#   stat_summary(fun.y = mean, geom="point", size = 2, color="blue")
# # save
# ggsave(glue("{file}_scatter.png"), plot = get_last_plot())

# create frequency data frame
freq <- as.data.frame(table(data_pron[, 1]))

# create bar charts
if (dv_is_numeric == TRUE){
  ggplot(data_pron, aes(x = as.character(indep), fill = factor(dep))) +
    labs(x = x_axis, y = y_axis, fill = legend) +
    geom_bar(position = "fill") +
    geom_text(inherit.aes = FALSE, data = data_means, aes(x = indep, y = 0.9, label = paste("m=", signif(means, 2))), vjust=0, fontface="bold", size=font_size) +
    geom_text(inherit.aes = FALSE, data = freq, aes(x = Var1, y = 0.85, label = paste("n=", Freq)), vjust=0, size=font_size) +
#    geom_signif(inherit.aes = FALSE, data = data_pron, aes(x = indep, y = dep), y_position = 0.9, comparisons = vec_list, map_signif_level=TRUE, step_increase = -0.1) +
    scale_fill_brewer(palette="Blues")
  # save
  ggsave(glue("{file}_bar.png"), plot = get_last_plot())
} else {
  ggplot(data_pron, aes(x = indep, fill = factor(dep))) +
    labs(x = x_axis, y = y_axis, fill = legend) +
    geom_bar(position = "fill") +
    geom_text(inherit.aes = FALSE, data = freq, aes(x = Var1, y = 0.9, label = paste("n=", Freq)), vjust=0, size=font_size) +
    scale_fill_brewer(palette="Blues")
  # save
  ggsave(glue("{file}_bar.png"), plot = get_last_plot())
}

