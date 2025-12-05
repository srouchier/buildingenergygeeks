(rnn_intro)=
# Recurrent Neural Networks

## Motivation

In the previous sections, we explored autoregressive models (AR, ARX, ARMAX) which assume a linear relationship between past and future values. While powerful, these models have limitations when dealing with complex, non-linear temporal dependencies often found in building energy data.

Recurrent Neural Networks (RNNs) are a class of artificial neural networks designed to recognize patterns in sequences of data, such as text, genomes, handwriting, or the spoken word, and importantly for us, time series data.

## Vanilla RNN

A "Vanilla" RNN processes a sequence of inputs $x_1, x_2, \dots, x_t$ by maintaining a hidden state $h_t$ that acts as a memory of the previous inputs.

At each time step $t$, the hidden state $h_t$ is updated based on the current input $x_t$ and the previous hidden state $h_{t-1}$:

```{math}
:label: rnn_hidden
h_t = \tanh(W_{hh} h_{t-1} + W_{xh} x_t + b_h)
```

The output $y_t$ is then computed from the hidden state:

```{math}
:label: rnn_output
y_t = W_{hy} h_t + b_y
```

Where:
*   $W_{hh}, W_{xh}, W_{hy}$ are weight matrices.
*   $b_h, b_y$ are bias vectors.
*   $\tanh$ is the hyperbolic tangent activation function.

### The Vanishing Gradient Problem

Vanilla RNNs suffer from the vanishing gradient problem. During backpropagation through time, gradients can become extremely small, making it difficult for the network to learn long-term dependencies. This limits their effectiveness for sequences where the relevant information is far in the past.

## Long Short-Term Memory (LSTM)

LSTMs were designed to overcome the vanishing gradient problem. They introduce a more complex cell structure with "gates" that control the flow of information.

An LSTM cell maintains a cell state $C_t$ (long-term memory) and a hidden state $h_t$ (short-term memory).

The gates are:
1.  **Forget Gate ($f_t$):** Decides what information to discard from the cell state.
2.  **Input Gate ($i_t$):** Decides what new information to store in the cell state.
3.  **Output Gate ($o_t$):** Decides what to output based on the cell state.

The mathematical formulation is:

```{math}
:label: lstm_gates
\begin{aligned}
f_t &= \sigma(W_f \cdot [h_{t-1}, x_t] + b_f) \\
i_t &= \sigma(W_i \cdot [h_{t-1}, x_t] + b_i) \\
\tilde{C}_t &= \tanh(W_C \cdot [h_{t-1}, x_t] + b_C) \\
C_t &= f_t * C_{t-1} + i_t * \tilde{C}_t \\
o_t &= \sigma(W_o \cdot [h_{t-1}, x_t] + b_o) \\
h_t &= o_t * \tanh(C_t)
\end{aligned}
```

Where $\sigma$ is the sigmoid function.

## Gated Recurrent Unit (GRU)

GRUs are a simplified variation of LSTMs. They combine the forget and input gates into a single "update gate" and merge the cell state and hidden state.

The gates are:
1.  **Update Gate ($z_t$):** Determines how much of the past information needs to be passed along to the future.
2.  **Reset Gate ($r_t$):** Determines how much of the past information to forget.

The formulation is:

```{math}
:label: gru_gates
\begin{aligned}
z_t &= \sigma(W_z \cdot [h_{t-1}, x_t] + b_z) \\
r_t &= \sigma(W_r \cdot [h_{t-1}, x_t] + b_r) \\
\tilde{h}_t &= \tanh(W \cdot [r_t * h_{t-1}, x_t] + b) \\
h_t &= (1 - z_t) * h_{t-1} + z_t * \tilde{h}_t
\end{aligned}
```

GRUs are computationally more efficient than LSTMs and often achieve comparable performance.

## Application to Building Energy

In the context of building energy, we can use these architectures to predict future energy consumption based on past consumption and external factors like weather.

*   **Input ($x_t$):** Weather data (temperature, solar radiation), occupancy schedules, and past energy consumption.
*   **Output ($y_t$):** Predicted energy consumption for the next time step(s).

In the following notebook, we will implement these models using TensorFlow/Keras.
