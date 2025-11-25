data {
  // This block declares all data which will be passed to the Stan model.
  // Training period
  int<lower=0> N;       // number of data items
  vector[N] x;      // outdoor temperature
  vector[N] y;      // outcome energy vector
  // Post period
  int<lower=0> N_post;        // number of data items
  vector[N_post] x_post;      // outdoor temperature
  vector[N_post] y_post;      // outcome energy vector
  // Priors
  array[2] real alpha_prior;
  array[2] real beta1_prior;
  array[2] real beta2_prior;
  array[2] real tau1_prior;
  array[2] real tau2_prior;
  array[2] real theta_prior;
}
parameters {
  // This block declares the parameters of the model.
  real alpha;      // baseline consumption
  real beta1;     // slope for heating
  real beta2;       // slope for cooling
  real tau1;      // low temperature break point
  real tau2;      // high temperature break point
  real<lower=0> sigma;  // error scale
  real theta;     // moving average
}
transformed parameters {
  vector[N] f;
  vector[N] epsilon;
  vector[N_post] f_post;
  for (n in 1:N) {
    f[n] = alpha + beta1 * fmax(tau1-x[n], 0) + beta2 * fmax(x[n]-tau2, 0);
  }
  epsilon[1] = y[1] - f[1];
  for (n in 2:N) {
    epsilon[n] = y[n] - f[n] - theta*epsilon[n-1];
  }
  for (n in 1:N_post) {
    f_post[n] = alpha + beta1 * fmax(tau1-x_post[n], 0) + beta2 * fmax(x_post[n]-tau2, 0);
  }
}
model {
  // Assigning prior distributions on some parameters
  alpha ~ normal(alpha_prior[1], alpha_prior[2]);
  beta1 ~ normal(beta1_prior[1], beta1_prior[2]);
  beta2 ~ normal(beta2_prior[1], beta2_prior[2]);
  tau1 ~ normal(tau1_prior[1], tau1_prior[2]);
  tau2 ~ normal(tau2_prior[1], tau2_prior[2]);
  theta ~ normal(theta_prior[1], theta_prior[2]);
  // Observational model
  for (n in 2:N) {
    y[n] ~ normal(f[n] + theta*epsilon[n-1], sigma);
  }
}
generated quantities {
  // This block is for posterior predictions. It is not part of model training
  array[N] real log_lik;
  array[N] real y_hat;
  array[N_post] real y_hat_post;
  real savings = 0;

  y_hat[1] = normal_rng(f[1], sigma);
  log_lik[1] = normal_lpdf(y[1] | f[1], sigma);
  for (n in 2:N) {
    y_hat[n] = normal_rng(f[n] + theta*epsilon[n-1], sigma);
    log_lik[n] = normal_lpdf(y[n] | f[n] + theta*epsilon[n-1], sigma);
  }
  
  // Forecasts with increased uncertainty due to the autocorrelation
  y_hat_post[1] = normal_rng(f_post[1], sigma);
  savings += y_hat_post[1] - y_post[1];
  for (n in 2:N_post) {
    y_hat_post[n] = normal_rng(f_post[n], sigma * sqrt(1+theta^2));
    savings += y_hat_post[n] - y_post[n];
  }
}
