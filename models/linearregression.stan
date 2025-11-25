data {
  int<lower=0> N;     // number of data items
  int<lower=0> K;     // number of predictors
  matrix[N, K] x;     // predictor matrix
  vector[N] y;        // outcome vector
}
parameters {
  real alpha;           // intercept
  vector[K] beta;       // coefficients for predictors
  real<lower=0> sigma;  // error scale
 }
model {
  y ~ normal(x * beta + alpha, sigma);  // likelihood
}
generated quantities {
  array[N] real log_lik;
  array[N] real y_hat;
  for (j in 1:N) {
    log_lik[j] = normal_lpdf(y[j] | x[j] * beta + alpha, sigma);
    y_hat[j] = normal_rng(x[j] * beta + alpha, sigma);
  }
}