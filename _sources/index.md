# Building energy probabilistic modelling

```{image} logo.png
:alt: logo
:width: 400px
:align: center
```

This website promotes the use of Bayesian inference and prediction for building energy use. It includes some background on the Bayesian data analysis workflow, and tutorials with common building energy models.

**Latest update: October 21th 2025**: this website is being migrated from bookdown (R) to jupyter-book (Python). Here is the current checklist of remaining chapters:

* [x] Background
* [x] Simple regression
* [ ] Time series: in progress
* [ ] State-space models
* [ ] Gaussian process

## Motivation

Data science offers promising prospects for improving the energy efficiency of buildings. Thanks to the availability of smart meters and sensor networks, along with increasingly accessible algorithms for data processing and analysis, statistical models may be trained to predict the energy use of HVAC systems or the indoor conditions. These trained models and their predictions then lead to various inferences: assessing the real impact of energy conservation measures; identifying HVAC faults or physical properties of the envelope in order to provide incentive for retrofitting; minimizing energy consumption through model	predictive control; detecting and diagnosing faults; etc.

The availability of measurements and computational power have given data mining methods an increasing popularity. The field of data analysis applied to building energy performance assessment however faces two main challenges to this day. Ironically, the first challenge is the abundance of data. Smart meters and building management systems deliver large amounts of information which can hide the few readings which are the most relevant to energy conservation. Automated monitoring and fault detection algorithms only do what they are told, and will hardly replace human intervention when it comes to understanding readings. The second challenge is the difficulty of data science. Without a principled methodology, it is very easy to draw erroneous conclusions, by incorrectly assuming that a model is properly trained. By lack of a background in statistics, building energy practitioners often lack the tools to ensure their inferences are correct.

## Content of the book

The topic of this book is statistical modelling and inference applied to building energy performance assessment. It has two target audiences: building energy researchers and practitioners who need a gentle introduction to statistical modelling; statisticians who may be interested in applications to energy performance.

The first part of the book covers the motivation and theoretical background.

* An overview of the possibilities of data analysis applied to building energy performance assessment, and of the main categories and challenges of data analysis methods.
* A quick description of building physics and how they can be formulated as statistical models.
* The main steps of a Bayesian workflow for statistical modelling and inference, which aims at making sure that models are well defined and trained for a given application.

Then, the rest of the book shows some applications. It is a series of Python notebooks classified into chapters, each focusing on a type of model. The notebooks are self-sufficient, and mention whether non-standard libraries or other software should be installed.

* Regression and mixture models
* Time series analysis
* State-space models for 
* Gaussian Process models

The target of the book is that the basics of Bayesian data analysis are explained to building energy practitioners who don't necessarily have a large background on statistics.

The book **does not** cover:

* Data acquisition and pre-processing, although a crucial step of data analysis, will not be explained in detail for each problem.
* Big data. The typical size of our data files is a few MB, up to a few GB for the largest sets. This is far from what computer scientists consider "big data".
* Machine learning. Even when the target of a particular problem is prediction rather than inference of physical properties, our statistical models will always have some degree of physical interpretability.
* Classification. Most of the methods shown are variations of regression problems, as our models will almost always have quantitative responses. There are however strong links with classification problems, especially when it comes to identifying occupant presence and behaviour.

## Software

This book is written and maintained with [jupyter-book](https://jupyterbook.org/en/stable/intro.html).

Tutorials use either [PyMC](https://www.pymc.io/welcome.html) or [Stan](https://mc-stan.org/) as a probabilistic programming library. Both have pros and cons.

From the perspective of a non-statistician, PyMC is probably easier to get started with, but Stan feels more flexible and has a much better documentation. I present examples with both and leave the reader to find their preference.

## About

I am [Simon Rouchier](https://srouchier.github.io/), lecturer at the [Université Savoie Mont Blanc](https://www.univ-smb.fr/), Chambéry, France.

This website is the beta version of a future book. It possibly still has some typos and inconsistencies: I welcome all feedback by [email](https://srouchier.github.io/) or through the book's [Github repo](https://github.com/srouchier/buildingenergygeeks).

<a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/"><img alt="Licence Creative Commons" style="border-width:0" src="https://i.creativecommons.org/l/by-nc-sa/4.0/88x31.png" /></a><br />Ce(tte) œuvre est mise à disposition selon les termes de la <a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/">Licence Creative Commons Attribution - Pas d’Utilisation Commerciale - Partage dans les Mêmes Conditions 4.0 International</a>.