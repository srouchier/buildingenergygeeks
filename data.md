# Data

All data used in this book are accessible in the project's [repository](https://github.com/srouchier/buildingenergygeeks/tree/master/data).

(building1298)=
## Building 1298

In 2019, the ASHRAE great energy predictor competition was featured on the Machine Learning platform [Kaggle](https://www.kaggle.com/c/ashrae-energy-prediction). The purpose of the competition was to find accurate energy prediction options to support energy-saving investments. Participants were challenged to build models across four energy types: electricity, chilled water, steam and hot water. Data were available at an hourly resolution, across 1,449 buildings located in 16 different North-American sites, over a three-year timeframe. In addition to meter data, the dataset provides basic information on each building (primary use, gross floor area, year of construction and number of floors, although most values are missing) and weather data from each site. Beyond the competition, the dataset may be used for non-commercial  purposes and academic research.

The training dataset provided in the competition covers the year 2016. In this book, data from only one of the buildings is used in several tutorials: Building 1298 is a 16,000 m$^2$ education building of unknown construction year and floor area. It is one of the few buildings of the dataset which has all 4 types of meters.

```{figure} /figures/alldata.png
---
name: building1298data
width: 600px
align: center
---
Insight of Building 1298 meters: electricity, chilled water and steam, hourly time step, shown here on a subset of 4 months of data.
```

The curated data can be downloaded [here](https://github.com/srouchier/buildingenergygeeks/blob/master/data/building_1298.csv)

(armadillo)=
## Armadillo box

The Armadillo Box is a demonstration building of 42 m$^2$ floor area, designed for the 2010 European Solar Decathlon by the ENSAG-GAIA-INES team. The envelope is a light wood framed construction with integrated insulation. Heating and cooling is performed by a “3 in 1” heat pump, and photovoltaic solar panels provide recharge for electric vehicles.

```{figure} /figures/rcexample_armadillo.jpg
---
name: rcexample_armadillo2
width: 400px
align: center
---
Armadillo Box
```

```{figure} /figures/rcexample01.png
---
name: rcexample012
width: 450px
align: center
---
```

The house is used for the demonstration of state-space models. A curated data file can be downloaded [here](https://github.com/srouchier/buildingenergygeeks/blob/master/data/statespace.csv).