(gp_theory)=
# Theory on GP models

## Principle

In machine learning, Gaussian Process (GP) regression is a widely used tool for solving modelling problems {cite:p}`rasmussen2003gaussian`. The appeal of GP models comes from their flexibility and ease of encoding prior information into the model.

A GP is a generalization of the Gaussian probability distribution to infinite dimensions. Instead of having a mean vector and a covariance matrix, the Gaussian process $f(\mathbf{x})$ is a random function in a d-dimensional input space, characterized by a mean function $\mu: \mathbb{R}^d \rightarrow \mathbb{R}$ and a covariance	function $\kappa: \mathbb{R}^{d\times d} \rightarrow \mathbb{R}$

```{math}
:label: gpmodelgeneral
f\left(\mathbf{x}\right) \sim \mathrm{GP}(\mu(\mathbf{x}),\,\kappa(\mathbf{x}, \mathbf{x}^\prime))
```

The variable $\mathbf{x}$ is the input of the Gaussian process and not the state vector defined in the previous section. The notation of equation {eq}`gpmodelgeneral` implies that any finite collection of random variables $\{f(\mathbf{x}_i)\}^n_{i=1}$ has a multidimensional Gaussian distribution (Gaussian process prior)

```{math}
:label: jointgp
\left\{f(\mathbf{x}_1), f(\mathbf{x}_2), \ldots, f(\mathbf{x}_n)\right\} \sim
		 \mathcal{N}(\mathbf{\mu}, \mathbf{K})
```

where $\mathbf{K}_{i,\,j} = \kappa(\mathbf{x}_i, \mathbf{x}_j)$ defines the covariance matrix and $\mathbf{\mu}_i = \mu(\mathbf{x}_i)$ the mean vector, for $i,j = 1,2,\ldots,n$.

The mean function is often, without loss of generality, fixed to zero (e.g. $\mu(\mathbf{x}) = \mathbf{0}$) if no prior information is available; assumption regarding the mean behavior of the process can be encoded into the covariance function instead {cite:p}`solin2016stochastic`. Indeed, the choice of covariance function allows encoding any prior belief about the properties of the stochatic process $f(\mathbf{x})$, e.g. linearity, smoothness, periodicity, etc. New covariance functions can be formulated by combining existing covariance functions. The sum $\kappa(\mathbf{x}, \mathbf{x}^\prime) = \kappa_1(\mathbf{x}, \mathbf{x}^\prime) + \kappa_2(\mathbf{x}, \mathbf{x}^\prime)$, or the product $\kappa(\mathbf{x}, \mathbf{x}^\prime) = \kappa_1(\mathbf{x}, \mathbf{x}^\prime) \times \kappa_2(\mathbf{x}, \mathbf{x}^\prime)$ of two covariance functions is a valid covariance function.

The Gaussian process regression is concerned by the problem of estimating the value of an unknown function $f(t)$ at arbitrary time instant $t$ (i.e. test point) based on a noisy training data $\mathcal{D} = \left\{t_k, y_k\right\}^n_{k=1}$

```{math}
f(t) \sim \mathrm{GP}(0, \kappa(t, t^\prime))
```

```{math}
:label: gpmodel
y_k = f(t_k) + v_k
```

The joint distribution between the test point $f(t)$ and the training points $\left(f(t_1),\,f(t_2),\,\ldots,\,f(t_n)\right)$ is Gaussian with known statistics. Because the measurement model in equation {eq}`gpmodel` is linear and Gaussian, the joint distribution between the test point $f(t)$ and the measurements $\left(y_1,\,y_2,\,\ldots,\,y_n\right)$ is Gaussian with known statistics as well. From the property of the Gaussian distribution, the conditional distribution of $f(t)$ given the measurements has an analytical solution {cite:p}`sarkka2019applied`.

```{math}
:label: gpposterior
p\left(f(t) \mid \mathbf{y}\right) =
	p\left(\mathbb{E}[f(t)] \mid \mathbb{V}[f(t)]\right)
```

with mean and variance

```{math}
\mathbb{E}[f(t)] = \mathbf{k}^\text{T}\,\left(
		\mathbf{K} + \sigma^2_\varepsilon\,\mathbf{I}\right)^{-1}\,\mathbf{y}
```

```{math}
:label: gpposteriorstats
\mathbb{V}[f(t)] = \kappa(t, t) - \mathbf{k}^\text{T}\,
		\left(\mathbf{K} + \sigma^2_\varepsilon\,\mathbf{I}\right)^{-1}\,\mathbf{k}
```

where $\mathbf{K}_{i,\,j} = \kappa(t_i, t_j)$, $\mathbf{k} = \kappa(t, \mathbf{t})$ and, $\mathbf{t}$ and $\mathbf{y}$ are the time and measurement vectors from the training data $\mathcal{D}$.

The estimated function model represents dependencies between function values at different inputs through the correlation structure given by the covariance function. Thus, the function values at the observed points give information also of the unobserved points.

## Gaussian Processes for prediction of energy use

The first application of Gaussian Processes in building energy modelling is based on the developments of {cite:p}`kennedy2001bayesian` which they called *Bayesian calibration*. Bayesian model calibration refers to using a GP as a surrogate model to reproduce a reference model, then training a second GP as the discrepancy function between this model and observations, then evaluating the posterior distribution of calibration parameters. In this context GPs have static inputs and are not dynamic models.

```{math}
:label: koh
z_i = \zeta(\mathbf{x}_i) +e_i =\rho \, \eta(\mathbf{x}_i,\theta)+\delta(\mathbf{x}_i)+e_i
```

where $\mathbf{x}_i$ is a series of known model inputs, $z_i$ are observations, $\zeta(\mathbf{x}_i)$ is the true value of the real process, $\eta(\mathbf{x}_i,\theta)$ is a computer model output with parameter $\theta$, $\delta(\mathbf{x}_i)$ is the discrepancy function and $e_i \sim N(0,\lambda)$ are the observation errors. In Kennedy and O'Hagan's work, GP are used to represent prior information about both $\eta(\cdot,\cdot)$ and $\delta(\cdot)$. $\rho$ and $\lambda$ are hyperparameters, to be added to the list of hyperparameters of the covariance functions into a global hyperparameter vector $\phi$.

Before attempting prediction of the true phenomenon using the calibrated code, the first step is to derive the posterior distribution of the parameters $\theta$, $\beta$ (parameters of the GP mean functions) and $\phi$. Hyperparameters are estimated in two stages: $\eta(\cdot,\cdot)$ is estimated from a series of code outputs, and $\delta(\cdot)$ is estimated from observations. The authors restrict their study to having analytical, tractable posterior distributions that do not require methods such as MCMC. Therefore they fix the value of some hyperparameters to make these functions tractable, and have to resort to some simplifications.

The first application of this method to building energy modelling was the work of {cite:p}`heo2012calibration`. They followed the formulation of Bayesian calibration developed by Kennedy and O'Hagan, and used three sets of data as input: (1) monthly gas consumption values as observations $y(x)$, (2) computer outputs from exploring the space of calibration parameters $\eta(x,\theta)$, and (3) the prior PDF of calibration parameters $p(\theta)$. The model outputs $\eta(x,\theta)$ and the bias term $\delta(x)$ are both modeled as GPs. Calibration parameters are for instance: infiltration rate, indoor temperature, $U$-values, etc. With very little data, results are posterior PDFs which are very close to the priors.

GP learning scales poorly with the amount of data, which restricts its applicability to lower observation time steps. {cite:p}`kristensen2017bayesian` studied the influence of time resolution on the predictive accuracy and showed the advantage of higher resolutions. More recently, {cite:p}`chong2017bayesian` used the NUTS algorithm for the MCMC sampling in order to accelerate learning. Later, {cite:p}`chong2018guidelines` gave a summary of publications using Bayesian calibration in building energy. In {cite:p}`gray2018hybrid`, a hybrid model was implemented. A zero mean GP is trained to learn the error between the grey-box model and the reference data. As in the previous references, both models are added to obtain the final predicted output. They are trained in sequence: the GB model has some inputs $\mathbf{u}_\mathrm{GB}$ and is trained first; then the GP has some other inputs $\mathbf{u}_\mathrm{GP}$ and is trained on the GB model's prediction error. Results are the hyperparameters of the GP.

Models trained by this method are said to have very good prediction performance, since the GP predicts the inadequacy of the GB as a function of new inputs, not included in the physical model. However, the method may not be fit for the interpretation of physical parameters. Indeed, since the GB model is first trained independently from the GP, it is biased and its parameter estimates are not interpretable.

## Gaussian Processes for time series data

Gaussian process are non-parametric models, which means that the latent function $f(t)$ is represented by an infinite-dimensional parameter space. Unlike parametric methods, the number of parameters is not fixed, but grows with the size of the dataset $\mathcal{D}$, which is an advantage and a limitation. Non-parametric models are memory-based, which means that they can represent more complex mapping as the data set grows but in order to make predictions they have to "remember" the full dataset {cite:p}`frigola2015bayesian`.

The computational complexities of the analytical regression equations {eq}`gpposteriorstats` are cubic $\mathcal{O}(N^3)$ in the number of measurements $N$, which is not suited for long time series. However, for a certain class of covariance function, temporal Gaussian process regression is equivalent to state inference problem which can be solved with Kalman filter and Rauch-Tung-Striebel smoother {cite:p}`hartikainen2010kalman`. The computational complexity of these sequential methods is linear $\mathcal{O}(N)$ instead of cubic in the number of measurements $N$.

A stationary Gaussian process (i.e. the covariance function depends only on the time difference $\kappa(t, t^\prime) = \kappa(\tau)$, with $\tau=\lvert t - t^\prime \rvert$) can be exactly represented or well approximated by a stochastic state-space model:

```{math}
\mathrm{d}\mathbf{f} = \mathbf{A_{gp}} \, \mathbf{f} \, \mathrm{d}t
			+ \mathbf{\sigma}_{\mathbf{gp}} \, \mathrm{d}\mathbf{w}
```

```{math}
:label: gpssm
y_k = \mathbf{C}_{\mathbf{gp}} \, \mathbf{f}(t_k) + v_k
```

where the matrices of the system are defined by the choice of covariance function.

A list of widely used covariance function with this dual representation is given in {cite:p}`solin2016stochastic`, {cite:p}`sarkka2019applied`. As example, consider the Mat\'ern covariance function with decay parameter $\nu=3/2$

```{math}
:label: materncovariance
\kappa \left(\tau\right) = \sigma^2 \, \left(1 + \frac{\sqrt{3}\tau}{\ell}\right) \, \exp\left(-\frac{\sqrt{3}\tau}{\ell}\right)
```

which has the following equivalent state-space representation

```{math}
:label: maternssm
	\mathbf{A_{gp}} = \begin{pmatrix}
		0 & 1 \\[0.5em]
		-\lambda^2 & -2\lambda
	\end{pmatrix}
	\quad
	\mathbf{\sigma}_{\mathbf{gp}} = \begin{pmatrix}
		0 & 0 \\[0.5em]
		0 & 2\lambda^{3/2}\sigma
	\end{pmatrix}
	\quad
	\mathbf{C}_{\mathbf{gp}} =
		\begin{pmatrix} 1 & 0 \end{pmatrix}
```


with $\lambda=\sqrt{2\,\nu} / \ell$ and where $\sigma, \ell > 0$ are the magnitude and length-scale parameters.

The parameter $\ell$ controls the smoothness (i.e. how much time difference $\tau$ is required to observe a significant change in the function value) and the parameter $\sigma$ controls the overall variance of the function (i.e. the expected magnitude of function values).

## Latent Force Models

The stochastic part of the state-space model can accommodate for unmodelled disturbances, which do not have a significant influence on the thermal dynamics. This assumption holds if the disturbances have white noise properties and are uncorrelated accross time lags, which is seldom the case in practice {cite:p}`ghosh2015modeling`. Usually, the model complexity is increased to erase the structure in the model residuals. However, this strategy may lead to unnecessarily complex models because non-linear dynamics are often modelled by linear approximations. Increasing the model complexity often requires more prior knowledge about the underlying physical systems and additional measurements, which may not be available in practice.

Another strategy is to model these unknown disturbances as Gaussian processes with certain parametrized covariance structures {cite:p}`sarkka2018gaussian`. The resulting latent force model {cite:p}`alvarez2009latent` is a combination of parametric grey-box model and non-parametric Gaussian process model.

```{math}
\mathrm{d}\mathbf{x} = \left(\mathbf{A_{rc} \, \mathbf{x}
			+ \mathbf{M_{rc}} \, \mathbf{C_{gp}}\mathbf{f}
			+ \mathbf{B_{rc}} \, \mathbf{u}} \right) \, \mathrm{d}t
			+ \mathbf{\sigma}_{\mathbf{rc}} \, \mathrm{d}\mathbf{w}
```

```{math}
\mathrm{d}\mathbf{f} = \mathbf{A_{gp}} \, \mathbf{f} \, \mathrm{d}t
			+ \mathbf{\sigma}_{\mathbf{gp}} \, \mathrm{d}\mathbf{w}
```

```{math}
:label: lfmsde
y_k = \mathbf{C}_{\mathbf{rc}} \, \mathbf{x}(t_k) + v_k
```

where $\mathbf{M_{rc}}$ is the input matrix corresponding to the unknown latent forces.

The augmented state-space representation of the latent force model

```{math}
\mathrm{d}\mathbf{z} = \mathbf{A} \, \mathbf{z} \, \mathrm{d}t
			+ \mathbf{B} \, \mathbf{u} \, \mathrm{d}t
			+ \mathbf{\sigma} \, \mathrm{d}\mathbf{w}
```

```{math}
:label: lfmsde2
y_k = \mathbf{C} \, \mathbf{z}(t_k) + v_k
```

is obtained by combining the grey-box model and the gaussian process model {eq}`gpssm`, such that

```{math}
:label: lfmsde3
\begin{alignedat}{3}
\mathbf{z}&=\begin{pmatrix}
	\mathbf{x} \\
	\mathbf{f}
\end{pmatrix}
\quad &
\mathbf{A}&=\begin{pmatrix}
	\mathbf{A_{rc}} &  \mathbf{M_{rc}} \, \mathbf{C_{gp}} \\
	\mathbf{0} & \mathbf{A_{gp}}
\end{pmatrix}
\quad &
\mathbf{B}=\begin{pmatrix}
	\mathbf{B_{rc}} \\
	\mathbf{0}
\end{pmatrix}
\\
\mathbf{C}&=\begin{pmatrix} \mathbf{C}_{\mathbf{rc}} & \mathbf{0} \end{pmatrix}
\quad &
\mathbf{\sigma}&=\begin{pmatrix}
	\mathbf{\sigma}_{\mathbf{rc}} &  \mathbf{0} \\
	\mathbf{0} & \mathbf{\sigma}_{\mathbf{gp}}
\end{pmatrix}
\end{alignedat}
```

The latent force model representation allows to incorporate prior information about the overall dynamic of the physical system, but also about the behavior of the unknown inputs.
