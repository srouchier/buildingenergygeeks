data {
  int<lower=0> N_train;     // data points (training)
  int<lower=0> N;           // data points (all)
  int<lower=0> K;       // number of predictors
  int<lower=0> P;       // AR order (how many lags of y are used)
  int<lower=0> Q;       // MA order
  int<lower=0> R;       // X order (how many lags of predictors are used)

  matrix[N, K] x;       // predictor matrix (training and test)
  vector[N_train] y;    // output data
}

parameters {
  real alpha;                 // mean coefficient
  row_vector[P] phi;          // AR coefficients
  row_vector[Q] theta;        // MA coefficients
  matrix[K, R+1] beta;        // coefficients of explanatory variables
                              // R+1 because lag 0 is included
  real<lower=0> sigma;        // error term
}
transformed parameters {
  // array[6] int ii = reverse(linspaced_int_array(6, 2, 7));
  // Then a[ii] evaluates to a[7], …, a[2].
  vector[N_train] f;
  vector[N_train] epsilon;
  row_vector[P] invphi = phi[reverse(linspaced_int_array(P, 1, P))];
  row_vector[Q] invtheta = theta[reverse(linspaced_int_array(Q, 1, Q))];
  matrix[K, R+1] invbeta = beta[:, reverse(linspaced_int_array(R+1, 1, R+1))];

  for (n in 1:P) {
    f[n] = alpha;
  }
  for (n in P+1:N_train) {
    f[n] = alpha + invphi * y[n-P:n-1] + trace(invbeta * x[n-R:n,:]);
  }

  for (n in 1:Q) {
    epsilon[n] = 0;
  }
  for (n in Q+1:N_train) {
    epsilon[n] = y[n] - (f[n] + invtheta * epsilon[n-Q:n-1]);
  }

}

model {
  // The first P rows don't contribute to training
  for (n in Q+1:N_train) {
    epsilon[n] ~ normal(0, sigma);
    }
}

generated quantities {
  vector[N_train] log_lik;
  vector[N] y_hat;
  vector[N] psi;

  for (n in 1:P) {
    log_lik[n] = 0;
    psi[n] = 0;
    y_hat[n] = y[n];
  }

  // this should raise an error if P < Q
  for (n in P+1:N_train) {
    psi[n] = 0;
    log_lik[n] = normal_lpdf(y[n] | f[n] + invtheta * epsilon[n-Q:n-1], sigma);
    y_hat[n] = normal_rng(f[n] + invtheta * epsilon[n-Q:n-1], sigma);
  }

  psi[N_train] = 1; // psi_0
  for (n in N_train+1:N) {

    if (n-N_train <= Q) {
      psi[n] = theta[n-N_train];
    } else {
      psi[n] = 0;
    }
    for (j in 1:P) {
      psi[n] += phi[j] * psi[n-j];
    }

    y_hat[n] = normal_rng(alpha + invphi * y_hat[n-P:n-1] + trace(invbeta * x[n-R:n,1:K]), sigma * sqrt(sum(psi[N_train:(n-1)]^2)));
  }
}