library(tidyverse)
library(readxl)
library(lubridate)

cnames <- read_excel("data/ornlbtricdatafromcc3fy2014.xlsx", skip=1, n_max=1) %>% names()
df <- read_excel("data/ornlbtricdatafromcc3fy2014.xlsx", skip=4, col_names=cnames, na="NAN")


df2 <- df %>%
  mutate(datetime = ymd_hms(TIMESTAMP),
         date = as_date(datetime),
         e_hp = HP_in_Tot + HP_out_Tot,
         e_dhw = HW_Tot,
         e_fan = Fantech_Tot,
         e_other = main_Tot - e_hp - e_dhw - e_fan,
         ti = ((Din_tmp_Avg + Grt_tmp_Avg + Brkf_tmp_Avg + Kit_tmp_Avg + BedM_tmp_Avg +
                  Bed3_tmp_Avg + Bed2_tmp_Avg + BedB_tmp_Avg + Mbath_tmp_Avg)/9 - 32) * 5/9,
         tg = (garage_tmp_Avg-32)*5/9,
         ts = (FanTsup_tmp_Avg-32)*5/9,
         te = (Outside_Tmp_Avg-32)*5/9,
         isol = SlrW1_Avg,
         ws = wind_speed_mean) %>%
  group_by(date) %>%
  summarise(ti = mean(ti),
            te = mean(te),
            isol = sum(isol),
            e_hp = sum(e_hp),
            e_dhw = sum(e_dhw),
            e_fan = sum(e_fan),
            e_other = sum(e_other),
            ts = mean(ts),
            tg = mean(tg),
            ws = mean(ws),
            .groups='drop')


# Let's only keep winter for now
df2.drop(df2.index[(df2.index < pd.to_datetime('2013-11-01')) |
                     (df2.index >= pd.to_datetime('2014-04-01'))], inplace=True)
