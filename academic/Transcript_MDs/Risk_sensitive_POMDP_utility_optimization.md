# Risk-Sensitive Partially Observable Markov Decision Processes as Fully Observable Multivariate Utility Optimization problems

Arsham Afsardeir <sup>∗</sup> Andreas Kapetanis† Vaios Laschos ‡ Klaus Obermayer §

July 19, 2022

#### Abstract

We provide a new algorithm for solving Risk Sensitive Partially Observable Markov Decisions Processes, when the risk is modeled by a utility function, and both the state space and the space of observations is finite. This algorithm is based on an observation that the change of measure and the subsequent introduction of the information space that is used for exponential utility functions, can be actually extended for sums of exponentials if one introduces an extra vector parameter that tracks the "expected accumulated cost" that corresponds to each exponential. Since every increasing function can be approximated by sums of exponentials in finite intervals, the method can be essentially applied for any utility function, with its complexity depending on the number of exponentials.

Keywords: MDP, Partial Observability, Risk Sensitivity, Utility Function, Sums of Exponentials

# 1 Introduction

In the classical theory of Markov Decision Processes (MDPs), one deals with controlled Markovian stochastic processes (Sn) taking values on a Borel space S. These processes are controlled via a series of actions (An), according to a policy π, that changes the underlying state transition probabilities P(Sn+1|Sn, An) of (Sn). The goal is to find a policy π that optimizes the expected value

$$
\mathcal{I}_N(s_0, \pi) = \mathbb{E}_{s_0}^{\pi} \left[ \sum_{n=0}^{N-1} \beta^n C(S_n, A_n, S_{n+1}) \right],
$$

where β ∈ (0, 1] is called discount factor, C : S × A × S → R is the cost function, s<sup>0</sup> ∈ S<sup>n</sup> is the initial state and N ∈ N ∪ {∞} (the case where β = 1 and N = ∞ at the same time, will be excluded in this work). The inclusion of risk-sensitivity and partial observability are natural extensions to this standard model.

In classical MDPs, one makes the assumption that the controlled process (Sn) takes values on a set of states S which is always accessible to the controller. However, in several real-life applications the real state is not directly

<sup>∗</sup>Fakultät Elektrotechnik und Informatik, Technische Universität Berlin, Marchstr. 23, 10587, Berlin, Germany. Partially supported by DFG project OB 102/29-1.

<sup>†</sup> Institute of Mathematics, Technische Universität Berlin, Str. des 17. Juni 136, 10623 Berlin, Germany.

<sup>‡</sup>WIAS Berlin. For the biggest part, V.L. was supported by DFG project OB 102/27-1. For the completion of the work, V.L. was supported by DFG under Germany´s Excellence Strategy – The Berlin Mathematics Research Center MATH+ (EXC-2046/1, project ID: 390685689).

<sup>§</sup>Fakultät Elektrotechnik und Informatik, Technische Universität Berlin, Marchstr. 23, 10587, Berlin, Germany. Partially supported by DFG project OB 102/27-1.

observable and only secondary information dependent on the state, can be observed. Partially Observable Markov Decision Processes (POMDPs) are a generalization of MDPs towards incomplete information about the current state. POMDPs extend the notion of MDPs by a set of observations Y and a set of conditional observation probabilities Q(·|s) given the "hidden" state s ∈ S. Q(y|s) namely represents the probability of observing y while being in state s. In risk-neutral POMDPs, one can introduce a new state space, called belief (state) space X = P(S), the set of probability measures on S, and a stochastic process (Xn) taking values in X , such that Xn(s) is the probability of S<sup>n</sup> being equal to the "hidden" state s ∈ S at time n, conditioned on the accumulated observations and actions up to time n. One can treat this new process on the belief space like a Completely Observable Markov Decision Process (COMDP) on X with classical tools, retrieve optimal or ε-optimal polices (i.e. policies with expected value at most ε-far from the optimal value), and then apply them to the original problem. It is remarkable that, due to the linearity of the expectation operator, the belief state is a so-called sufficient statistic. Broadly speaking, a sufficient statistic carries adequate information for the controller to make an optimal choice at a specific point in time. It also allows to separate the present cost from the future cost through a Bellman-style equation. For an introduction to sufficient statistics, we refer to [\(Hinderer, 1970\)](#page-25-0).

To introduce risk-sensitivity we will work with the classical theory of expected utility [\(Bäuerle & Rieder, 2014;](#page-24-0) [Jaquette, 1973\)](#page-25-1), where one tries to optimize

<span id="page-1-0"></span>
$$
\mathcal{I}_N(s_0, \pi) = \mathbb{E}_{s_0}^{\pi} \left[ U \left[ \sum_{n=0}^{N-1} \beta^n C(S_n, A_n, S_{n+1}) \right] \right],
$$
\n(1.1)

for some increasing and continuous function U : R → R. Note that the exponential utility function U = exp generates a performance index that belongs to several models of risk at the same time, and it has been extensively studied in many different settings [\(Borkar & Meyn, 2002;](#page-24-1) [Cavazos-Cadena, 2010;](#page-24-2) [Chung & Sobel, 1987;](#page-24-3) [Di Masi & Stettner,](#page-24-4) [2007;](#page-24-4) [Dupuis, Laschos, & Ramanan, 2019;](#page-24-5) [Fleming & Hernández-Hernández, 1997;](#page-25-2) [Hernández-Hernández & Marcus,](#page-25-3) [1996;](#page-25-3) [Howard & Matheson, 1972;](#page-25-4) [Levitt & Ben-Israel, 2001\)](#page-25-5). As mentioned above, [\(Bäuerle & Rieder, 2014\)](#page-24-0) treated problems with optimality criteria of form [\(1.1\)](#page-1-0).

To our best knowledge, there is only partial progress [\(Baras & James, 1997;](#page-24-6) [Bäuerle & Rieder, 2017;](#page-24-7) [Bäuerle](#page-24-8) [& Rieder, 2017;](#page-24-8) [Cavazos-Cadena & Hernández-Hernández, 2005;](#page-24-9) [Fan & Ruszczyński, 2018;](#page-24-10) [Fernandez-Gaucherand](#page-24-11) [& Marcus, 1997;](#page-24-11) [Hernández-Hernández, 1999;](#page-25-6) [Marecki & Varakantham, 2010\)](#page-25-7) when it comes to combining risksensitivity and partial observability, and most articles study the specific case of the exponential utility function. When risk is involved extra or alternative information is necessary to make an optimal decision. In the case of expected utilities additional information on the accumulated cost is necessary to make an optimal choice, even if the true state is known to the controller [\(Bäuerle & Rieder, 2014;](#page-24-0) [Marecki & Varakantham, 2010\)](#page-25-7). A common workaround to this problem is to assume that the controller is aware of the running cost through some mechanism. For example, the controller observes either the running cost directly [\(Marecki & Varakantham, 2010\)](#page-25-7), or a part of the whole process that is responsible for the cost [\(Bäuerle & Rieder, 2017\)](#page-24-7). [Fan and Ruszczyński](#page-24-10) [\(2018\)](#page-24-10) study cost functions that depend on both observable quantities and beliefs. In [Bäuerle and Rieder](#page-24-8) [\(2017\)](#page-24-8), a general approach for treating problems with risk measured by a utility function is introduced. It is shown there, that one can use probability measures on the product space X × R as state space. This way, the authors end up with an MDP on the state space P(X × R). As we will explain in the sequel, we take a different route that is computationally less demanding in several cases.

# 1.1 Our Contribution

It was shown in [Bäuerle and Rieder](#page-24-8) [\(2017\)](#page-24-8), that by using an exponential function as the utility function, the problem space would shrink dramatically . This proposition is incline to the concept of information vector which Cavazos-Cadena and Hernandez-Hernandez discussed [\(Cavazos-Cadena & Hernández-Hernández, 2005\)](#page-24-9). Both papers show, in two different conceptual systems, that this property of exponential utility function which transforms summation of costs to the product of their utilities, can be exploited to provide sufficient statistics for decision making in a much smaller representation. Consequently the model with exponential utility function has a computational advantage, however, it losses its generality due to the much narrower range of utility functions it can accept.

To extend the ideas related to exponential utility models, in this work we employ the idea of multi-variate optimization and show that by applying exponentials on a finite set of different running costs, we can use the information space approach in a more general way. More specifically, our multi-variate exponential utility model is able to reproduce more complex utility functions and at the same time benefit from simplicity of exponential utilities according to computation burden as well. In our method the exponential running costs are independent from each other, therefore, each term can represent an independent component of a target multivariate utility function. These components can be seen either as building blocks of a target function's formulation (in the case of utility functions equal to sum of exponential terms) or more generally as the elements of function approximator series (in case of approximating the target function).

In comparison to the purely exponential case, the utility functions we treat can be more behaviorally plausible as well. In behavioral economics and finance disciplines it is a common approach to assume people to use a mapping from objective values to subjective utilities and subsequently either apply maximization on the expected value of the utilities [\(Von Neumann & Morgenstern, 1947\)](#page-25-8) or their other distributional properties [\(Tversky & Kahneman,](#page-25-9) [1992\)](#page-25-9) [\(Al-Nowaihi, Bradley, & Dhami, 2008\)](#page-24-12). Consequently, the shape of people's utility function has a significant effect on their attitude toward risky choices. The shape of human utility function [\(Kalyanaram & Winer, 1995;](#page-25-10) [Mosteller & Nogee, 1951\)](#page-25-11) and the effect of contextual parameters on that, like amount of wealth [\(Markowitz, 1952\)](#page-25-12) and emotions [\(Bertram, Schulz, & Nelson, 2021\)](#page-24-13) has been investigated by different experimental paradigms. For a review see [Edwards](#page-24-14) [\(1954\)](#page-24-14). In their influential work, prospect theory, Kahneman and Tversky proposed an S-shaped utility function which is risk-averse (concave) in gains and risk-seeker(convex) in losses [\(Kahneman & Tversky, 1979,](#page-25-13) [2013\)](#page-25-14). They also addressed a set of experiments that confirm different risk tendencies in gain and loss situations. As one can expect, the flexibility of an exponential utility model is not sufficient to produce different risk tendencies between loosing and winning situations by a single function. In contrast, privileging the computational advantage of exponential utility functions, our risk-sensitive model can also address this phenomenon by exploiting either utility functions which are defined by linear combinations of multiple exponential forms (like sinh(.)) or utility functions which can be approximated by linear combinations of exponential terms in a specific interval of values (like Sigmoid function, see section 4). Therefore, it becomes possible to shape functions which have both positive and negative second order derivatives on the distinct intervals of their domain simultaneously. Capturing the dissimilarity of risk tendencies among losses and gains is a major advantage of the multi-variate model which gives us more explanatory ability in respect to behavioral modeling in comparison to exponential utility function.

In what follows we argue that it is actually possible to apply similar arguments to treat utility functions that are sums of exponentials, i.e. utility functions of the form

<span id="page-2-0"></span>
$$
\widehat{U}(t) = \sum_{i=1}^{i_{\text{max}}} w^i e^{\lambda^i t}.
$$
\n(1.2)

With slight abuse of notation, we observe that for a probability distribution θ<sup>0</sup> on S, we can write

$$
\widehat{\mathcal{I}}_N(\theta_0, \widehat{\pi}) = \widehat{\mathbb{E}}_{\theta_0}^{\widehat{\pi}} \left[ \sum_{i=1}^{i_{\text{max}}} w^i e^{\lambda^i \left( \sum_{n=0}^{N-1} \widehat{C}(S_n, A_n) \right)} \right] = \sum_{i=1}^{i_{\text{max}}} \widehat{\mathbb{E}}_{\theta_0}^{\widehat{\pi}} \left[ w^i e^{\lambda^i \left( \sum_{n=0}^{N-1} \widehat{C}(S_n, A_n) \right)} \right].
$$

Then, similar to [Cavazos-Cadena and Hernández-Hernández](#page-24-9) [\(2005\)](#page-24-9), by applying a change of measure argument, we identify a new state space X = P(S) <sup>i</sup>max × Y, a controlled transition matrix P(x 0 |x, a), and a collection of running costs C i : X × A × X → R, that depend on the next stage as well, such that for the resulting completely observable controlled processes (Xn). With x<sup>0</sup> = (θ0, . . . , θ0, y0) and a fixed but arbitrary y<sup>0</sup> ∈ Y, we have

$$
\widehat{\mathcal{I}}_{N}(\theta_{0},\widehat{\pi}) = \mathcal{I}_{N}(x_{0},\pi) = \mathbb{E}_{x_{0}}^{\pi} \left[ \sum_{i=1}^{i_{\max}} w^{i} e^{\lambda^{i} \left( \sum_{n=0}^{N-1} C^{i} (X_{n}, A_{n}, X_{n+1}) \right)} \right]. \tag{1.3}
$$

Note that (π, <sup>E</sup>) and (π, <sup>b</sup> <sup>E</sup>b) are connected in a straightforward manner, see Section [2.](#page-4-0)

To establish our method we exploit the results of [Bäuerle and Rieder](#page-24-0) [\(2014\)](#page-24-0) and extend that model to introduce multivariate utility functions U : R <sup>d</sup> → R, which are component-wise monotone and each variable corresponds to a different running cost. This gives rise to the following optimality equation:

<span id="page-3-0"></span>
$$
\mathcal{I}_N(x,\pi) := \mathbb{E}_x^{\pi} \left[ \mathcal{U} \left( \sum_{n=0}^{N-1} \beta^n \cdot \mathcal{C}(X_n, A_n, X_{n+1}) \right) \right]. \tag{1.4}
$$

Note that here C is a vector of different running costs and the dot product denotes the point-wise multiplication. Criteria like [\(1.4\)](#page-3-0) can arise when one is trying to solve a multi-objective task, with different running costs, each of the costs contributing in a different manner to a total cost. As an example, one can think of a policy maker allocating tax money to different public sectors (education, infrastructure, health, etc). For each of them, we get a different cost which can be the position in the global chart or any other comparison metric. However, the total utility, depends on how much each government prioritizes each of these aspects, something that is encoded in the choice of the utility function. In a similar manner to [Bäuerle and Rieder](#page-24-0) [\(2014\)](#page-24-0), we augment the space to keep track of each accumulated cost term. Furthermore we prove that the finite time discounted problem converges to the infinite time one, without the extra assumption demanding that the utility function is either convex or concave, appearing in [Bäuerle and Rieder](#page-24-0) [\(2014\)](#page-24-0).

Remark 1.1. For any two utility functions <sup>U</sup>1, <sup>U</sup><sup>2</sup> that are <sup>ε</sup>-close on some interval [<sup>N</sup> mins,u <sup>C</sup>b(s, u), N maxs,u <sup>C</sup>b(s, u)], an ε-optimal policy for U<sup>1</sup> is a 2ε-optimal policy for U<sup>2</sup> . Therefore, one can apply the method to solve RSPOMDPs with utility functions that can be approximated by functions of the form [\(1.2\)](#page-2-0). One can easily show that this includes all increasing real functions, by approximating F(t) = U(log(t)), by a polynomial P(t) = P<sup>k</sup> <sup>i</sup>=1 wkx k in the interval [exp(<sup>N</sup> mins,u <sup>C</sup>b(s, u)), exp(<sup>N</sup> maxs,u <sup>C</sup>b(s, u))], and the composing with the exponential on both sides.

The rest of the paper is structured as follows: In section 2 our multi-variate utility function and its mathematical modeling and construction are presented. Next, in section 3 we show and prove solution methods for this model and the utility functions from section 2 in both finite and infinite horizon cases. In section 4, we provide an extended version of a famous POMDP, the tiger problem, as a numerical example to explain the model and compare it with the general model of Bäuerle and Rieder. And finally, we discuss about the computational advantage of our model.

# <span id="page-4-0"></span>2 RSPOMDPs for sums of exponentials

In this section, we consider risk sensitve POMDPs with a class of utility functions that can be written as weighted sums of exponentials. We will show that it is possible to reformulate the problem in terms of a multi objective risk sensitive MDP with a new performance index that, in turn, can be treated with tools described in the next section.

# <span id="page-4-1"></span>2.1 The original setting

We start by describing the model for a risk sensitive POMDP, i.e. (S, <sup>Y</sup>, <sup>A</sup>, P , Q, <sup>b</sup> <sup>U</sup>b). <sup>S</sup>, <sup>Y</sup>, <sup>A</sup> will be three finite sets equipped with the discrete topology. In the sequel, S is the hidden state space, Y the set of observations, and <sup>A</sup> the set of controls. For every <sup>a</sup> ∈ A, we define a transition probability matrix <sup>P</sup>b(a) = <sup>h</sup> <sup>P</sup>b(<sup>s</sup> 0 |s; a) i s,s0∈S . Finally, we denote by <sup>Q</sup> = [Q(y|s)]y∈Y,s∈S the signal matrix and by <sup>C</sup><sup>b</sup> : S × A → <sup>R</sup> the cost function.

Now, for each <sup>n</sup> <sup>∈</sup> <sup>N</sup>, let <sup>H</sup>b<sup>n</sup> be the set of histories up to time n, where <sup>H</sup>b<sup>0</sup> <sup>=</sup> <sup>P</sup>(S), and <sup>H</sup>b<sup>n</sup> <sup>=</sup> <sup>H</sup>b<sup>n</sup>−<sup>1</sup> × A × Y. We denote by <sup>Π</sup>H<sup>b</sup> := <sup>n</sup> πb = <sup>f</sup>b<sup>0</sup>, <sup>f</sup>b<sup>1</sup>, . . .  <sup>f</sup>b<sup>n</sup> : <sup>H</sup>b<sup>n</sup> <sup>→</sup> A, n <sup>∈</sup> <sup>N</sup> o the set of deterministic polices that are functions of the history <sup>b</sup>h<sup>n</sup> = (θ, a0, y1, . . . , an−1, yn) up to time n. Given <sup>θ</sup> ∈ P(S), and <sup>π</sup><sup>b</sup> <sup>∈</sup> <sup>Π</sup>Hb, due to the Ionescu-Tulcea theorem, there exists a unique measure <sup>P</sup>b<sup>π</sup><sup>b</sup> θ on the Borel sets of Ω := S × (A × S × Y)<sup>∞</sup> that satisfies:

$$
\widehat{\mathbb{P}}_{\theta}^{\widehat{\pi}}(s_0, a_0, s_1, y_1, a_1, \ldots, a_{n-1}, s_n, y_n) := \theta(s_0) \prod_{k=0}^{n-1} \left( \widehat{P} \left( s_{k+1} | s_k; \widehat{f}_k \left( \widehat{h}_k \right) \right) Q \left( y_{k+1} | s_{k+1} \right) \right),
$$

The corresponding expectation operator is denoted by <sup>E</sup>bπ<sup>b</sup> θ . Finally, for each <sup>n</sup> <sup>∈</sup> <sup>N</sup>, we define the <sup>σ</sup>-fields <sup>F</sup>b<sup>n</sup>, <sup>G</sup>bn, by

$$
\widehat{\mathcal{F}}_n := \sigma((A_k, Y_{k+1}), k = 0, 1, \ldots, n-1), \quad \widehat{\mathcal{G}}_n := \sigma(S_0, (A_k, S_{k+1}, Y_{k+1}), k = 0, 1, \ldots, n-1).
$$

It is straightforward to see that the set of policies <sup>Π</sup><sup>H</sup>b, contains exactly the elements fbn n∈N , where <sup>f</sup>b<sup>n</sup> are <sup>F</sup>b<sup>n</sup>measurable functions from <sup>H</sup>b<sup>n</sup> to <sup>A</sup>.

# 2.2 Utility functions that are sums of exponentials

Let {λ i , i = 1, . . . , imax} ⊆ R \ {0} be a finite collection of risk parameters, and {w i , i = 1, . . . , imax} ⊆ R be a collection of weights. We define the utility function <sup>U</sup><sup>b</sup> : <sup>R</sup> <sup>→</sup> <sup>R</sup> by

$$
\widehat{U}(t) := \sum_{i=1}^{i_{\text{max}}} w^i e^{\lambda^i t},\tag{2.1}
$$

and introduce the performance index

<span id="page-4-2"></span>
$$
\widehat{\mathcal{I}}_{N}(\theta_{0},\widehat{\pi}) = \sum_{i=1}^{i_{\max}} w^{i} \widehat{\mathbb{E}}_{\theta_{0}}^{\widehat{\pi}} \left[ e^{\lambda^{i} \left[ \sum_{n=0}^{N-1} \widehat{C}(S_{n}, A_{n}) \right] } \right],
$$
\n(2.2)

and the corresponding value fuction

$$
\widehat{V}_N(\theta_0) := \inf_{\widehat{\pi} \in \mathbf{\Pi}_{\widehat{\mathcal{H}}}} \widehat{\mathcal{I}}_N(\theta_0, \widehat{\pi}).
$$
\n
$$
(\widehat{P})
$$

The goal is to minimize <sup>I</sup>b<sup>N</sup> (θ0, <sup>π</sup>b) over all policies <sup>π</sup><sup>b</sup> <sup>∈</sup> <sup>Π</sup>Hb. We want to show that we can instead work on the completely observable risk sensitive MDP on the space X with performance index

$$
\mathcal{I}_N(x_0, \pi) = \sum_{i=1}^{i_{\text{max}}} w^i \mathbb{E}_{x_0}^{\pi} \left[ e^{\lambda^i \left[ \sum_{n=0}^{N-1} C^i(X_n, A_n, X_{n+1}) \right]} \right], \tag{2.3}
$$

for some reconstructed cost functions C i ,measure and expectation operator P π θ , E π θ and corresponding value function

<span id="page-5-0"></span>
$$
\mathcal{V}_N(x) := \inf_{\pi \in \Pi_{\mathcal{H}}} \mathcal{I}_N(x, \pi), \tag{P}
$$

for set of histories H. The following subsection will establish these constructions and prove the claim. Now problem (P) falls in the framework of Section [3.1](#page-8-0) that provides the means to calculate the optimal value and optimal policies as presented in the next chapter.

# 2.3 Towards a completely observable problem

The aim of this subsection is to prove the following:

Theorem 2.1. Let a risk sensitive POMDP (S, <sup>Y</sup>, <sup>A</sup>, P , Q, <sup>b</sup> <sup>U</sup>b), with stochastic dynamics as in subsection [2.1](#page-4-1) and performance index given in [\(2.2\)](#page-4-2). Then, there exist operators G<sup>i</sup> : P(S)×A×Y → R, F i : P(S)×A×Y → P(S), i ∈ {1, . . . , imax}, and <sup>η</sup> : <sup>Π</sup><sup>H</sup><sup>b</sup> <sup>→</sup> <sup>Π</sup>H, such that the following Completely Observable MDP <sup>X</sup><sup>n</sup> with performance index I<sup>N</sup> (x0, π) is equivalent the original, i.e.

$$
\mathcal{I}_N(x_0,\eta(\widehat{\pi}))=\widetilde{\mathcal{I}_N}(\theta_0,\widehat{\pi}).
$$

The completely observable MDP is defined by the following:

- 1. The state space is X = P(S) <sup>i</sup>max × Y and the set of actions is A
- 2. The evolution of the information state θ i n is given by:

$$
\theta_{n+1}^i = F^i(\theta_n, A_n, Y_{n+1})
$$

and under the assumption that Y<sup>n</sup> are uniformly distributed on the set Y we arrive at the following transition rule for x = (θ 1 , . . . , θimax , y) ∈ X , a ∈ A,:

$$
P(x'|x;a) := \begin{cases} \frac{1}{|\mathcal{Y}|}, & \text{if } x' = (F^1(\theta^1, a, y'), \dots, F^{i_{\max}}(\theta^{i_{\max}}, a, y'), y'), \\ 0, & \text{otherwise.} \end{cases}
$$

3. The cost functions are given by: C : X × A × X → R, with:

$$
C^i(x, u, x') = G^i(\theta^i, u, y') + \log(|\mathcal{Y}|^{\frac{1}{\lambda^i}})
$$

4. The set of histories is given by H<sup>0</sup> = X , and H<sup>n</sup> = Hn−<sup>1</sup> × A × X . A policy π ∈ Π<sup>H</sup> takes the form π = (f0, . . . , fn, . . .), where f<sup>n</sup> : H<sup>n</sup> → A.

5. The optimization problem is governed by the performance index:

$$
\mathcal{I}_N(x_0,\pi)=\sum_{i=1}^{i_{\max}} w^i sign(\lambda^i)\mathbb{E}^{\pi}_{x_0}\left[e^{\lambda^i\left[\sum_{n=0}^{N-1} C^i(X_n,A_n,X_{n+1})\right]}\right],
$$

We remark that although η is not a bijection, it essentially behaves like one in the same way as the one explained in Section [3.2.3.](#page-11-0)

Proof. The transformation to the completely observable problem will be done by introducing a sufficient statistic information space realized through information state vectors ψ and θ. The goal is to eliminate the unobservable quantities appearing in

$$
\widehat{\mathbb{E}}_{\theta_0}^{\widehat{\pi}}\left[e^{\lambda^i\left[\sum_{n=0}^{N-1}\widehat{C}(S_n,A_n)\right]}\right].
$$

Towards this goal a new probability measure that eliminates the dependencies that hold the previous measure to the partially observable case is introduced. Namely, following [Cavazos-Cadena and Hernández-Hernández](#page-24-9) [\(2005\)](#page-24-9) and [Fleming and Hernández-Hernández](#page-25-2) [\(1997\)](#page-25-2) there exists a unique probability measure P πb θ on <sup>G</sup>b<sup>n</sup> and its expectation operator E πb θ given by:

$$
\mathbb{P}_{\theta}^{\widehat{\pi}}\left(s_0,a_0,s_1,y_1,a_1,\ldots,a_{n-1},s_n,y_n\right):=\theta(s_0)\prod_{k=0}^{n-1}\left(\frac{1}{|\mathcal{Y}|}\widehat{P}\left(s_{k+1}|s_k;\widehat{f}_k(h_k)\right)\right),
$$

for some <sup>θ</sup> <sup>∈</sup> <sup>P</sup>(S), <sup>π</sup><sup>b</sup> <sup>∈</sup> <sup>Π</sup><sup>H</sup>b. Note that <sup>θ</sup>(s0) = <sup>θ</sup><sup>0</sup> in our current set-up.

In what follows a relationship between <sup>E</sup>bπ<sup>b</sup> θ0 and E πb θ0 is constructed, in order for the latter to replace the former in the optimization problem.

The first important milestone in that direction makes use of the Radon-Nikodym theorem: Namely it can be noted that on the <sup>σ</sup>-field <sup>G</sup>bn, the Radon-Nikodyn derivative of <sup>P</sup>bπ<sup>b</sup> <sup>θ</sup> with respect to P πb θ is given by

$$
\frac{\partial \widehat{\mathbb{P}}_{\theta}^{\widehat{\pi}}}{\partial \mathbb{P}_{\theta}^{\widehat{\pi}}}\bigg|_{\widehat{\mathcal{G}}_n} = \prod_{k=0}^{n-1} \left(|\mathcal{Y}|Q(Y_{k+1}|S_{k+1})\right) =: Z_n,
$$

and therefore

$$
\widehat{\mathbb{E}}_{\theta_0}^{\widehat{\pi}} \left[ e^{\lambda^i \left[ \sum_{k=0}^n \widehat{C}(S_k, A_k) \right]} \right] = \mathbb{E}_{\theta_0}^{\widehat{\pi}} \left[ e^{\lambda^i \left[ \sum_{k=0}^n \widehat{C}(S_k, A_k) \right]} Z_n \right]. \tag{2.4}
$$

After establishing the defining relationship between the two measures for the change of measure in equation [\(2.4\)](#page-5-0) we now focus on the right part of the equation. This process will also lead to the construction of an information vector, on which the information space of the transformed MDP will be based, following the next steps:

1. First, let us define the positive and <sup>F</sup>b<sup>n</sup>-measurable random variable <sup>ψ</sup> i n , by

$$
\psi_n^i(s) := \mathbb{E}_{\theta_0}^{\widehat{\pi}} \left[ \mathbb{1}_{\{S_n = s\}} e^{\lambda^i \left[ \sum_{k=0}^n \widehat{C}(S_k, A_k) \right] Z_n \middle| \widehat{\mathcal{F}}_n \right].
$$

ψ<sup>n</sup> is a vector ∈ R |S| for each i ∈ {1, ..., imax}. Intuitively it can be understood, as (random) average accumulated cost up to time n of all outcomes that share the same observations and choices of controls leading to final state S<sup>n</sup> = s, given the information observable to or controlled by the agent up to this time step.

2. Using ψ<sup>n</sup> ,the notation R ψ i <sup>n</sup> = P <sup>s</sup>∈S ψ i n (s), , the linearity of the expectation operator and the tower property of conditional expectation we can then rewrite the right side of [2.4:](#page-5-0)

<span id="page-7-1"></span>
$$
\mathbb{E}_{\theta_0}^{\widehat{\pi}} \left[ e^{\lambda^i \left[ \sum_{k=0}^n \widehat{C}(S_k, A_k) \right]} Z_n \right] =
$$
\n
$$
\mathbb{E}_{\theta_0}^{\widehat{\pi}} \left[ \sum_{s \in \mathcal{S}} \mathbb{E}_{\theta_0}^{\widehat{\pi}} \left[ \mathbb{1}_{\{S_n = s\}} e^{\lambda^i \left[ \sum_{k=0}^n \widehat{C}(S_k, A_k) \right]} Z_n \right| \widehat{\mathcal{F}}_n \right] \right] = \mathbb{E}_{\theta_0}^{\widehat{\pi}} \left[ \int \psi_n^i \right] = \mathbb{E}_{\theta_0}^{\widehat{\pi}} \left[ \int \psi_0^i \prod_{k=1}^n \frac{\int \psi_k^i}{\int \psi_{k-1}^i} \right].
$$
\n(2.5)

3. Then note that setting ψ i <sup>0</sup> = θ0, ψ i n satisfies the following recursion:

<span id="page-7-0"></span>
$$
\psi_n^i = |\mathcal{Y}| M^i(A_{n-1}, Y_n) \psi_{n-1}^i
$$
\n(2.6)

for the matrix M(a, y) ∈ R |S|×|S| given by:

$$
M^i(a,y)[s,s'] := \left(e^{\lambda^i \widehat{C}(s,a)}\widehat{P}(s'|s;a)Q(y|s')\right)^{\intercal}.
$$

Inserting the recursion [2.6](#page-7-0) in [2.5](#page-7-1) yields:

<span id="page-7-2"></span>
$$
\mathbb{E}_{\theta_0}^{\widehat{\pi}}\left[\int \psi_n^i\right] = \mathbb{E}_{\theta_0}^{\widehat{\pi}}\left[|\mathcal{Y}|^n \int \psi_0^i \prod_{k=1}^n \int \left[M^i(A_{k-1}, Y_k) \frac{\psi_{k-1}^i}{\int \psi_{k-1}^i}\right]\right].\tag{2.7}
$$

Note that the integral R h M<sup>i</sup> (Ak−1, Yk) ψ i k−1 R ψ<sup>i</sup> k−1 i is to be understood in the same way as the previously introduced notation for R ψ i n . Also R ψ i <sup>0</sup> = 1 per definition.

4. Finally we normalize the information vector ψ i <sup>n</sup> by introducing θ i n , so that we arrive at an information state that is an element of P(S):

$$
\theta_n^i = \frac{\psi_n^i}{\int \psi_n^i},
$$

Replacing ψ i <sup>n</sup> with θ i n in [2.7](#page-7-2) yields:

<span id="page-7-3"></span>
$$
\mathbb{E}_{\theta_0}^{\widehat{\pi}}\left[\int \psi_n^i\right] = \mathbb{E}_{\theta_0}^{\widehat{\pi}}\left[\left|\mathcal{Y}\right|^n \prod_{k=1}^n \int M^i(A_{k-1}, Y_k) \theta_{k-1}^i\right] = \mathbb{E}_{\theta_0}^{\widehat{\pi}}\left[e^{\lambda^i \left(\sum_{k=1}^n \left(\frac{1}{\lambda^i} \log\left(\int [M^i(A_{k-1}, Y_k) \theta_{k-1}^i] + \log |Y|^{\frac{1}{\lambda^i}}\right)\right)\right]}, (2.8)
$$

where in the last step we have used the properties of the exponential and logarithmic functions in order to rewrite the operation in a more suitable form.

In steps 1-4 we have thus achieved our goal of rewriting [2.4](#page-5-0) only using quantities known to the agent. Namely we have shown:

$$
\widehat{\mathbb{E}}_{\theta_0}^{\widehat{\pi}} \left[ e^{\lambda^i \left[ \sum_{k=0}^n \widehat{R}(S_k, A_k) \right]} \right] = \mathbb{E}_{\theta_0}^{\widehat{\pi}} \left[ e^{\lambda^i \left( \sum_{k=1}^n \left( \frac{1}{\lambda^i} \log \left( \int [M^i(A_{k-1}, Y_k) \theta_{k-1}^i] \right) + \log |Y|^{\frac{1}{\lambda^i}} \right) \right)} \right]
$$

In addition we have constructed an information state θ i <sup>n</sup> ∈ P(S) for the transformed MDP.

As a last step we introduce the notation for the new optimization problem that leads to the direct claim of this theorem. First consider G : P(S) × A × Y → R, given by:

$$
G^i\left(\theta^i, a, y\right) := \frac{1}{\lambda^i} \log \left(\int M^i(u, y) \theta^i\right).
$$

This lets us rewrite [2.8:](#page-7-3)

$$
\mathbb{E}_{\theta_0}^{\widehat{\pi}}\left[e^{\lambda^i\left(\sum_{k=1}^n\left(\frac{1}{\lambda^i}\log\left(\int [M^i(A_{k-1},Y_k)\theta_{k-1}^i]\right)+\log|Y|^{\frac{1}{\lambda^i}}\right)\right)}\right]=\mathbb{E}_{\theta_0}^{\widehat{\pi}}\left[e^{\lambda^i\left(\sum_{k=1}^n\left(G(\theta_k^i,A_{k-1},Y_k)+\log|Y|^{\frac{1}{\lambda^i}}\right)\right)}\right]
$$

Furthermore we use use [2.6](#page-7-0) on θ i n :

$$
\theta^i_n = \frac{\psi^i_n}{\int \psi^i_n} = \frac{|\mathcal{Y}| M^i(A_{n-1}, Y_n) \psi^i_{n-1}}{\int |\mathcal{Y}| M^i(A_{n-1}, Y_n) \psi^i_{n-1}} = \frac{M^i(A_{n-1}, Y_n) \theta^i_{n-1}}{\int M^i(A_{n-1}, Y_n) \theta^i_{n-1}}
$$

We this recursion we can now write F : P(S) × A × Y → P(S) as a forward operation for the information state:

$$
F^i(\theta^i, a, y) := \frac{M^i(a, y)\theta^i}{\int M^i(a, y)\theta^i}.
$$

For the reformulation of the MDP we can now use the cost functions: C : X × A × X → R, with:

$$
C^{i}(x, u, x') = G^{i}(\theta^{i}, u, y') + \log(|\mathcal{Y}|^{\frac{1}{\lambda^{i}}})
$$

Furthermore, for the policies we have <sup>η</sup> : <sup>Π</sup><sup>H</sup><sup>b</sup> <sup>→</sup> <sup>Π</sup><sup>H</sup> such that (fn)n∈{0,...,N−1} <sup>=</sup> <sup>η</sup>((fbn)n∈{0,...,N−1}) satisfies

$$
f_n(x_0, a_0, \ldots, x_{n-1}, a_{n-1}, x_n) = \hat{f}_n(\theta_0, a_0, \ldots, y_{n-1}, a_{n-1}, y_n).
$$

# 3 MDP with Multivariate Utility Function

In this section, we describe a model for risk sensitive multi-objective sequential decision making on a Borel state and action space with multiple costs and a multivariate utility function. The performance index is the expected multivariate utility, where each variable corresponds to a different running cost. As a generalization to the classical MDP model, we allow for the cost to depend on the subsequent state in addition to the current state-action pair. We thereby follow and extend ideas from [Bäuerle and Rieder](#page-24-0) [\(2014\)](#page-24-0) and [Hernández-Lerma and Lasserre](#page-25-15) [\(1996\)](#page-25-15).

# <span id="page-8-0"></span>3.1 Notation and Assumptions

Throughout this section, we assume that an N-step Markov Decision Process is given by a Borel state space X , a Borel action space A, a Borel set D ⊆ X × A, and a regular conditional distribution P from X × D to [0, 1]. Given the current state x ∈ X , we assume that an action a ∈ D(x) may be chosen, where D(x) := {a ∈ A | (x, a) ∈ D} is the set of feasible actions. The transition probability to the next state is then given by the distribution P(·|x; a), according to the chosen action. The set of histories from up to time n is defined by

$$
\mathcal{H}_0 := \mathcal{X}, \qquad \mathcal{H}_n := \mathcal{H}_{n-1} \times \mathcal{A} \times \mathcal{X}, \quad n \in \mathbb{N}
$$

and h<sup>n</sup> = (x0, a0, . . . , xn) ∈ H<sup>n</sup> is a historical outcome up to time n.

Definition 3.1. The set of (history-dependent) policies is defined by

$$
\Pi_{\mathcal{H}} := \{ \pi = (f_0, f_1, \dots) \mid f_n : \mathcal{H}_n \to \mathcal{A}, \quad \forall h_n \in \mathcal{H}_n : f_n(h_n) \in D(x_n), \quad n \in \mathbb{N} \}.
$$

Similarly, the set of Markovian policies is defined by

$$
\Pi_{\mathcal{X}} := \{ \pi = (g_0, g_1, \dots) \mid g_n : \mathcal{X} \to \mathcal{A}, \quad \forall x \in \mathcal{X} : g_n(x) \in D(x), \quad n \in \mathbb{N} \}.
$$

Given an initial state x ∈ X and a history-dependent policy π = (f1, f2, . . .) ∈ ΠH, due to the Ionescu-Tulcea theorem, there exists a probability measure P π <sup>x</sup> on H<sup>∞</sup> and two stochastic processes (Xn)n, (An)<sup>n</sup> such that

$$
\mathbb{P}_x^{\pi}(X_0 \in B) = \delta_x(B), \ \mathbb{P}_x^{\pi}(X_{n+1} \in B \mid H_n, A_n) = P(X_{n+1} \in B \mid X_n, A_n)
$$

and

$$
A_n = f_n(H_n)
$$

for all Borel sets B ⊆ X . Canonically, Hn, Xn, A<sup>n</sup> are the history, state and action at time n. By E π <sup>x</sup> we denote the expectation operator corresponding to P π x . For more details of this construction, we refer to [Bäuerle and Rieder](#page-24-0) [\(2014\)](#page-24-0).

Throughout the whole section, we have the following standing assumptions:

#### Assumption 3.2.

- 1. The utility function U : R <sup>i</sup>max → R is continuous, and it exists 0 ≤ i<sup>τ</sup> ≤ imax , such that U is component-wise increasing in {i < i<sup>τ</sup> } and component-wise decreasing in {i > i<sup>τ</sup> }.
- 2. kUk<sup>∞</sup> < ∞.
- 3. The sets D(x), x ∈ X are compact.
- 4. The map x 7→ D(x) is upper semi-continuous, i.e. if x<sup>n</sup> → x ∈ X and a<sup>n</sup> ∈ D(xn), then (an) has an accumulation point in D(x).
- 5. The maps (x, a, x<sup>0</sup> ) 7→ C i (x, a, x<sup>0</sup> ), i = 1, . . . , imax, are continuous, and it holds c ≤ C i (·, ·, ·) ≤ c¯ for some fixed c, c¯ ∈ R.
- 6. P is weakly continuous.

Remark 3.3. Due to uniform boundedness of the cost functions C i , and the fact that we work on finite horizon problems with N < ∞ or infinite horizon problems with discount, we can observe that assumption 2 can be removed without any loss of generality.

For notational convenience, we define the vector valued function C : X × A × X → R <sup>i</sup>max by

$$
\mathbf{C}(x, a, x') := (C^1(x, a, x'), \dots, C^{i_{\max}}(x, a, x')) .
$$

# 3.2 Finite Horizon Problems

#### 3.2.1 Performance Index

After we have set the stage for Markov Decision Processes and their policies, we can now define a performance index that is the expected utility of several running costs.

Definition 3.4. Denote by N the number of steps of the MDP. We define the total cost I<sup>N</sup> (x, π) given an initial state x ∈ X , and a history dependent policy π ∈ Π<sup>H</sup> by

$$
\mathcal{I}_N(x,\pi) := \mathbb{E}^\pi_x \left[ \mathcal{U} \left( \sum_{n=0}^{N-1} \mathbf{C}(X_n, A_n, X_{n+1}) \right) \right],
$$

and the corresponding value function by

<span id="page-10-0"></span>
$$
\mathcal{V}_N(x) := \inf_{\pi \in \Pi_{\mathcal{H}}} \mathcal{I}_N(x, \pi).
$$
 (P)

#### 3.2.2 Augmented problem

The aim of what follows is to determine V<sup>N</sup> , and optimal policies in ([P](#page-10-0)). To this end, we augment the state space of the MDP to X × R <sup>i</sup>max . The second component models the so-far accumulated cost of the advancing MDP. In particular, <sup>X</sup>e<sup>n</sup> := (Xn, <sup>R</sup>n) ∈ X × <sup>R</sup> <sup>i</sup>max taking the value (x, r) = (x, r<sup>1</sup> , . . . , rimax ) implies that the MDP has advanced to state x and accumulated a cost amounting to r i in the i-th objective after the first n steps. In order to define transition probabilities of the augmented problem, we introduce the notion of a pushforward measure.

Definition 3.5. Given measurable spaces (S, <sup>F</sup>), (Se, <sup>F</sup>e), a measurable mapping <sup>T</sup> : S → <sup>S</sup><sup>e</sup> and a measure <sup>µ</sup> : F → [0, <sup>∞</sup>], the pushforward of <sup>µ</sup> is the measure induced on (Se, <sup>F</sup>e) by <sup>µ</sup> under <sup>T</sup> , i.e., the measure <sup>T</sup>#<sup>µ</sup> : F →<sup>e</sup> [0, <sup>∞</sup>] is given by

$$
(\mathcal{T}_{\#}\mu)(B) = \mu\left(\mathcal{T}^{-1}(B)\right) \text{ for } B \in \widetilde{\mathcal{F}}.
$$

In particular, if a function <sup>f</sup> is <sup>F</sup>e-measurable and <sup>T</sup>#µ-integrable, and <sup>f</sup> ◦ T is <sup>µ</sup>-integrable, then

$$
\int f \ d\mathcal{T}_{\#} \mu = \int f \circ \mathcal{T} \ d\mu.
$$

Now, we define the transition kernel <sup>P</sup><sup>e</sup> of the augmented problem by

$$
\widetilde{\mathbf{P}}(\cdot|\widetilde{x};a) = \widetilde{\mathbf{P}}(\cdot|(x,\mathbf{r});a) = (\mathcal{T}_{(x,\mathbf{r})}) \# \mathbf{P}(\cdot|x,a),\tag{3.1}
$$

where

$$
\mathcal{T}_{(x,\mathbf{r})}(x') = (x', \mathbf{C}(x, a, x') + \mathbf{r}).\tag{3.2}
$$

If X is finite, this leads to

$$
\widetilde{\mathbf{P}}(\widetilde{x}'|\widetilde{x};a) = \begin{cases}\n\mathbf{P}(x'|x;a), & \text{if } \widetilde{x} = (x,\mathbf{r}), \widetilde{x}' = (x',\mathbf{r} + \mathbf{C}(x,a,x')), \\
0, & \text{otherwise.} \n\end{cases}
$$
\n(3.3)

The histories for the augmented MDP are given by

$$
\widetilde{\mathcal{H}}_0 := \mathcal{X} \times \mathbb{R}^{i_{\max}}, \quad \widetilde{\mathcal{H}}_n := \widetilde{\mathcal{H}}_{n-1} \times \mathcal{D} \times (\mathcal{X} \times \mathbb{R}^{i_{\max}}), \quad n \in \mathbb{N}.
$$

The definition of history-dependent policies <sup>π</sup><sup>e</sup> <sup>∈</sup> <sup>Π</sup>He, Markovian policies <sup>π</sup><sup>e</sup> <sup>∈</sup> <sup>Π</sup>Xe, and the corresponding decision rules are changed accordingly.

Similar to the previous section, there exist a probability measure <sup>P</sup>e<sup>π</sup> <sup>x</sup> on <sup>H</sup>e<sup>∞</sup> and a coupled stochastic process (Xe)n∈<sup>N</sup> with <sup>X</sup>e<sup>n</sup> = (Xn, Rn), and a stochastic process (An)n∈N, such that

$$
\widetilde{\mathbb{P}}_{\widetilde{x}}^{\widetilde{\pi}}(\widetilde{X}_0 \in B) = \delta_{\widetilde{x}}(B), \quad \widetilde{\mathbb{P}}_{\widetilde{x}}^{\widetilde{\pi}}(\widetilde{X}_{n+1} \in B \mid \widetilde{H}_n, A_n) = \widetilde{P}(\widetilde{X}_{n+1} \in B \mid \widetilde{X}_n, A_n)
$$

and

$$
A_n = \widetilde{f}_n(\widetilde{H}_n)
$$

for all Borel sets <sup>B</sup> ⊆ X , and <sup>H</sup>n, <sup>X</sup>n, <sup>A</sup><sup>n</sup> are the history, state and action at time <sup>n</sup>, given an initial state <sup>x</sup><sup>e</sup> ∈ X ×<sup>R</sup> imax and a history-dependent policy <sup>π</sup><sup>e</sup> <sup>∈</sup> <sup>Π</sup>He. By induction, it is easy to prove that <sup>R</sup><sup>n</sup> <sup>=</sup> P<sup>n</sup>−<sup>1</sup> <sup>k</sup>=0 C(Xk, Ak, Xk+1) + r, Peπe xe -almost surely.

Definition 3.6. Denote by N ∈ N the number of steps of the MDP. For n = 1, . . . , N, we define the total cost <sup>I</sup>e<sup>n</sup>((x, <sup>r</sup>), <sup>π</sup>e) for the augmented problem, given the initial state <sup>x</sup> ∈ X , initial cost <sup>r</sup> <sup>∈</sup> <sup>R</sup> <sup>i</sup>max , and policy <sup>π</sup><sup>e</sup> <sup>∈</sup> <sup>Π</sup><sup>e</sup> by

$$
\widetilde{\mathcal{I}}_n(\widetilde{x}, \widetilde{\pi}) = \widetilde{\mathcal{I}}_n((x, r), \widetilde{\pi}) := \widetilde{\mathbb{E}}_{\widetilde{x}} \left[ \mathcal{U} \left( \sum_{k=0}^{n-1} \mathbf{C}(X_k, A_k, X_{k+1}) + r \right) \right] = \widetilde{\mathbb{E}}_{\widetilde{x}} \left[ \mathcal{U} \left( R_n \right) \right], \tag{3.4}
$$

and the corresponding value function by

<span id="page-11-1"></span>
$$
\widetilde{\mathcal{V}}_N(\widetilde{x}) := \inf_{\widetilde{\pi} \in \Pi_{\widetilde{\mathcal{H}}}} \widetilde{\mathcal{I}}_N(\widetilde{x}, \widetilde{\pi}).
$$
\n
$$
(\widetilde{P})
$$

#### <span id="page-11-0"></span>3.2.3 Policy bijection

For the sequel, let <sup>x</sup> ∈ X , and <sup>x</sup><sup>e</sup> = (x, <sup>0</sup>). Note that policies <sup>π</sup> = (f0, f1, . . .) <sup>∈</sup> <sup>Π</sup><sup>H</sup> of the original problem consist of functions <sup>f</sup><sup>n</sup> that are defined on <sup>H</sup>n, and policies <sup>π</sup><sup>e</sup> <sup>∈</sup> <sup>Π</sup><sup>H</sup><sup>e</sup> consist of functions <sup>f</sup>e<sup>n</sup> defined on <sup>H</sup>en. Therefore there is no simple bijectional correspondence between the two sets. However, the set of histories

$$
\widetilde{\mathcal{H}}_n^- = \{ \widetilde{h}_n \in \widetilde{\mathcal{H}}_n | \left( \exists k \in \{1, \dots, n-1\} : \mathbf{r}_k \neq \mathbf{r}_{k-1} + \mathbf{C}(x_k, a_k, x_{k+1}) \right) \vee (\mathbf{r}_0 \neq \mathbf{0}) \},\tag{3.5}
$$

is not accessible in the sense that these histories cannot occur. In a more rigorous manner, we have that <sup>P</sup>eπ<sup>e</sup> x˜ (He<sup>−</sup> n ) = 0, for all <sup>π</sup><sup>e</sup> <sup>∈</sup> <sup>Π</sup><sup>H</sup>e. For every policy <sup>π</sup><sup>e</sup> <sup>∈</sup> <sup>Π</sup><sup>H</sup>e, we may define a new "reduced" policy <sup>π</sup><sup>e</sup> red by

$$
\widetilde{f}_n^{\text{red}}(\widetilde{h}_n) = \begin{cases}\n a^{\text{red}}(x_n), & \text{if } \widetilde{h}_n \in \widetilde{\mathcal{H}}_n^-, \\
 \widetilde{f}_n(\widetilde{h}_n), & \text{otherwise,}\n\end{cases}\n\tag{3.6}
$$

where a red can be any arbitrary but fixed point in D(xn). Then for the set Πred <sup>H</sup><sup>e</sup> <sup>=</sup> {π<sup>e</sup> red <sup>∈</sup> <sup>Π</sup><sup>H</sup><sup>e</sup> : <sup>π</sup><sup>e</sup> <sup>∈</sup> <sup>Π</sup><sup>H</sup>e}, we can define a bijection to <sup>Π</sup>H. To do so, for <sup>π</sup> = (f0, f1, . . .) <sup>∈</sup> <sup>Π</sup>H, we define <sup>π</sup><sup>e</sup> red = (fered 0 , <sup>f</sup>ered 1 , . . .) ∈ Πred He , by

<span id="page-11-2"></span>
$$
\widetilde{f}_{n}^{\text{red}}\left((x_{0},0), a_{0}, \ldots, \left(x_{n-1}, \sum_{i=0}^{n-1} \mathbf{C}(x_{i}, a_{i}, x_{i+1})\right), a_{n-1}, \left(x_{n}, \sum_{i=0}^{n} \mathbf{C}(x_{i}, a_{i}, x_{i+1})\right)\right) =
$$
\n
$$
\begin{cases}\na^{\text{red}}, & \text{if } \widetilde{h}_{n} \in \widetilde{\mathcal{H}}_{n}^{-}, \\
f_{n}(x_{0}, a_{0}, \ldots, x_{n-1}, a_{n-1}, x_{n}), & \text{otherwise.} \n\end{cases}
$$
\n(3.7)

It is easy to see that the value function of ([P](#page-10-0)) coincides with the value function of ([P](#page-11-1)e) with <sup>r</sup> <sup>=</sup> <sup>0</sup>, i.e.

$$
\mathcal{V}_N(x) = \inf_{\pi \in \mathbf{\Pi}_{\mathcal{H}}} \mathcal{I}_N(x, \pi) = \inf_{\widetilde{\pi} \in \mathbf{\Pi}_{\widetilde{\mathcal{H}}}^{\text{red}}} \widetilde{\mathcal{I}}_N((x, 0), \widetilde{\pi}) = \inf_{\widetilde{\pi} \in \mathbf{\Pi}_{\widetilde{\mathcal{H}}}} \widetilde{\mathcal{I}}_N((x, 0), \widetilde{\pi}) = \widetilde{\mathcal{V}}_N((x, 0)).
$$

The next step is to derive a Bellman-style equation for the augmented problem ([P](#page-11-1)e). It can be shown that the minimizer of ([P](#page-11-1)e) is a Markovian policy.

#### 3.2.4 Bellman operator and first theorem

First, for a fixed m ∈ R, we define the set

∆ := v : X × R <sup>i</sup>max → R <sup>v</sup> is lower semi-continuous, <sup>v</sup>(x, ·) is continuous, <sup>k</sup>vk<sup>∞</sup> <sup>&</sup>lt; <sup>∞</sup>, inf x,d {v(x, r)} ≥ m, and for all x ∈ X is component-wise increasing (decreasing) in {i < i<sup>τ</sup> } (in {i > i<sup>τ</sup> }) .

For <sup>v</sup> <sup>∈</sup> <sup>∆</sup> and a Markovian decision rule <sup>g</sup><sup>e</sup> <sup>∈</sup> <sup>Π</sup>Xe, we define the operators

$$
T_{\tilde{g}}[v](\tilde{x}) = T_{\tilde{g}}[v](x, \mathbf{r}) = \int v(\tilde{x}') \tilde{P}(d\tilde{x}' | \tilde{x}, \tilde{g}(\tilde{x})) = \int v((x', r')) (\mathcal{T}_{(x, \mathbf{r})}) \# P(dx' | x, \tilde{g}(x, \mathbf{r}))
$$
$$
= \int v(x', \mathbf{C}(x, \tilde{g}(x, \mathbf{r}), x') + \mathbf{r}) P(dx' | x, \tilde{g}(x, \mathbf{r})),
$$

and

$$
T[v](x, r) = \inf_{a \in D(x)} \int v(x', C(x, a, x') + r) P(dx' | x, a),
$$

whenever the integrals exist. <sup>T</sup> is called the minimal cost operator. We say that a Markovian decision rule <sup>g</sup><sup>e</sup> is a minimizer of <sup>v</sup> if <sup>T</sup>ge[v] = <sup>T</sup>[v]. In this situation, <sup>g</sup>e(x, <sup>r</sup>) is a minimizer of

$$
\mathcal{D}(x) \ni a \mapsto \int v(x', \mathcal{C}(x, a, x') + \mathbf{r}) P(dx' \mid x, a)
$$

for every (x, r) ∈ X × R <sup>i</sup>max . We may now state the main result of this section:

<span id="page-12-0"></span>Theorem 3.7. Let <sup>V</sup>e0(x, <sup>r</sup>) := <sup>U</sup>(r). Then, the following holds:

a) For any Markovian policy <sup>π</sup><sup>e</sup> = (ge0, <sup>g</sup>e1, . . .) <sup>∈</sup> <sup>Π</sup><sup>X</sup>e, we have the cost iteration

$$
\widetilde{\mathcal{I}}_n((x,\boldsymbol{r}),\widetilde{\pi})=T_{\widetilde{g}_0}[\ldots[T_{\widetilde{g}_{n-1}}[\widetilde{\mathcal{V}}_0]]](x,\boldsymbol{r})
$$

for all n = 1, . . . , N.

b) If an optimal policy exists it is Markovian, i.e.

$$
\inf_{\widetilde{\pi} \in \mathbf{\Pi}_{\widetilde{\mathcal{H}}}} \mathcal{I}_N(\widetilde{x}, \widetilde{\pi}) = \inf_{\widetilde{\pi} \in \mathbf{\Pi}_{\widetilde{\mathcal{X}}}} \mathcal{I}_N(\widetilde{x}, \widetilde{\pi}).
$$

- c) The operator T : ∆ → ∆ is well-defined, and for every v ∈ ∆, there exists a minimizer of T[v].
- d) We get the Bellman-style equation

$$
\widetilde{\mathcal{V}}_n(x,\mathbf{r})=T[\widetilde{\mathcal{V}}_{n-1}](x,\mathbf{r})=\inf_{a\in D(x)}\int \widetilde{\mathcal{V}}_{n-1}(x',\mathbf{C}(x,a,x')+\mathbf{r})P(dx'\mid x,a)
$$

for all n = 1, . . . , N.

e) If <sup>g</sup><sup>e</sup> ∗ n is a minimizer of <sup>V</sup>e<sup>n</sup>−<sup>1</sup> for <sup>n</sup> = 1, . . . , N, then the history-dependent policy <sup>π</sup> <sup>∗</sup> = (f ∗ 0 , . . . , f <sup>∗</sup> N−1 ), defined by

$$
f_n^*(h_n) := \begin{cases} \widetilde{g}_N^*(x_0, 0) & \text{if } n = 0, \\ \widetilde{g}_{N-n}^*\left(x_n, \sum_{k=0}^{n-1} C(x_k, a_k, x_{k+1})\right) & \text{otherwise,} \end{cases}
$$

is an optimal policy for problem ([P](#page-10-0)).

For the proof of Theorem [3.7,](#page-12-0) we need the following lemma:

<span id="page-13-0"></span>Lemma 3.8. Let v : X × R <sup>i</sup>max → R be bounded and lower semi-continuous. Suppose

- 1. D(x) is compact,
- 2. x 7→ D(x) is upper semi-continuous,
- 3. (x, <sup>r</sup>, g, x <sup>e</sup> 0 ) 7→ v(x 0 , <sup>C</sup>(x, <sup>g</sup>e(x, <sup>r</sup>), x<sup>0</sup> ) + r) is lower semi-continuous.

Then, T v is is lower semi-continuous and there exists a minimizer <sup>g</sup><sup>e</sup> ∗ such that <sup>T</sup>ge<sup>∗</sup> <sup>v</sup> <sup>=</sup> T v.

Proof. By Lemma 17.11 in [Hinderer](#page-25-0) [\(1970\)](#page-25-0), (x, <sup>r</sup>, <sup>g</sup>e) 7→ <sup>T</sup>gev(x, <sup>r</sup>) is lower semi-continuous. The claim then follows from a similar argument to Proposition 2.4.3 in [Bäuerle and Rieder](#page-24-15) [\(2011\)](#page-24-15).

Proof of Theorem [3.7.](#page-12-0) The proof is similar to Theorem 2.3.4 and Theorem 2.3.8 in [Bäuerle and Rieder](#page-24-15) [\(2011\)](#page-24-15) with a different state space, see also [Bäuerle and Rieder](#page-24-0) [\(2014\)](#page-24-0).

ad a) An easy calculation shows that

$$
\widetilde{\mathcal{I}}_1((x,\mathbf{r}),\widetilde{\pi}) = \mathbb{E}_{x}^{\widetilde{\pi}}\Big[\mathcal{U}\left(\mathbf{C}(X_0,A_0,X_1)+\mathbf{r}\right)\Big] \n= \int \mathcal{U}\left(\mathbf{C}(x,\widetilde{g}_0(x,\mathbf{r}),x')+\mathbf{r}\right)P(dx'\mid x,\widetilde{g}_1(x,\mathbf{r})) = T_{\widetilde{g}_1}[\widetilde{\mathcal{V}}_0](x,\mathbf{r}).
$$

Now, let <sup>π</sup><sup>e</sup> <sup>+</sup> = (ge2, . . .). For <sup>n</sup> = 2, . . . , N, we get

$$
\widetilde{\mathcal{I}}_{n}((x, \mathbf{r}), \widetilde{\pi}) = \mathbb{E}_{x}^{\widetilde{\pi}} \left[ \mathcal{U} \left( \sum_{k=0}^{n-1} \mathbf{C}(X_{k}, A_{k}, X_{k+1}) + \mathbf{r} \right) \right]
$$
\n
$$
= \int \mathbb{E}_{x'}^{\widetilde{\pi}^{+}} \left[ \mathcal{U} \left( \sum_{k=0}^{n-2} \mathbf{C}(X_{k}, A_{k}, X_{k+1}) + \mathbf{r} + \mathbf{C}(x, \widetilde{g}_{1}(x, \mathbf{r}), x') \right) \right] P(dx' \mid x, \widetilde{g}_{0}(x, \mathbf{r}))
$$
\n
$$
= \int \widetilde{\mathcal{I}}((x', \mathbf{r}), \widetilde{\pi}^{+}) P(dx' \mid x, \widetilde{g}_{1}(x, \mathbf{r})) = T_{\widetilde{g}_{1}} [\widetilde{\mathcal{I}}_{n-1}(\cdot, \widetilde{\pi}^{+})](\widetilde{x}) = T_{\widetilde{g}_{1}}[\dots [T_{\widetilde{g}_{n-1}}[\widetilde{V}_{0}]]](x, \mathbf{r}).
$$

The claim follows then by induction.

- ad b) This follows from Theorem 2.2.3 in [Bäuerle and Rieder](#page-24-15) [\(2011\)](#page-24-15).
- ad c) Note that every <sup>v</sup> <sup>∈</sup> <sup>∆</sup> is bounded from below by <sup>m</sup>. By our assumptions, we get that (x, <sup>r</sup>, g, x <sup>e</sup> 0 ) 7→ v(x 0 , <sup>C</sup>(x, <sup>g</sup>e(x, <sup>r</sup>), x<sup>0</sup> ) + r) is lower semi-continuous, and bounded from below, i.e. we are in the setting of Lemma [3.8.](#page-13-0) Thus, <sup>T</sup>[v] is lower semi-continuous and there exists a minimizer <sup>g</sup><sup>e</sup> ∗ such that <sup>T</sup><sup>g</sup>e<sup>∗</sup> [v] = <sup>T</sup>[v].

For fixed x ∈ X , and a ∈ D(x), the map r 7→ R v(x 0 , C(x, a, x<sup>0</sup> ) + r)P(dx<sup>0</sup> | x, a) has the same monotonicities with respect to r 0 i s as v and it is continuous for every a ∈ D(x). The continuity can be proven with the dominated convergence theorem since kvk<sup>∞</sup> < ∞. Therefore, the infimum of these maps over all a ∈ D(x) is upper semi-continuous in r. With this, we have shown that T v(x, ·) is upper and lower semi-continuous, and therefore continuous, and respects the same monotonicities as v for all x ∈ X . Because v(x, ·) ≥ m, we have T[v](x, ·) ≥ m. The boundness assumption follows from the definition of T and the corresponding property of v. We have then shown that T : ∆ → ∆ is well-defined.

ad d) Let <sup>g</sup><sup>e</sup> ∗ <sup>n</sup> be a minimizer of Vn−<sup>1</sup> for n = 1, . . . , N and denote by π <sup>∗</sup> = (g<sup>e</sup> ∗ 1 , . . . , <sup>g</sup><sup>e</sup> ∗ <sup>N</sup> ) the associated policy. For n = 1, we get that

$$
\widetilde{\mathcal{V}}_1(x,\mathbf{r}) = \inf_{\widetilde{\pi} \in \mathbf{\Pi}_{\widetilde{\mathcal{X}}}} \mathbb{E}_{x}^{\widetilde{\pi}} \Big[ \mathcal{U}\left(\mathbf{C}(X_0, A_0, X_1) + \mathbf{r}\right) \Big] = \inf_{a \in D(x)} \int \mathcal{U}(\mathbf{C}(x, a, x') + \mathbf{r}) P(dx' \mid x, a) = T[\widetilde{\mathcal{V}}_0](x, \mathbf{r}),
$$

and obviously, <sup>V</sup>e<sup>1</sup>(x, <sup>r</sup>) = <sup>I</sup>e<sup>1</sup>((x, <sup>r</sup>), <sup>π</sup><sup>e</sup> ∗ ). Now, assume that <sup>I</sup>e<sup>n</sup>((x, <sup>r</sup>), <sup>π</sup><sup>e</sup> ∗ ) = <sup>V</sup>e<sup>n</sup>(x, <sup>r</sup>) for a fixed <sup>n</sup> ∈ {1, . . . , N}. Then,

$$
\widetilde{\mathcal{I}}_{n+1}((x,\mathbf{r}), \widetilde{\pi}^*) = T_{\widetilde{g}_1^*}[\widetilde{\mathcal{I}}_n(\cdot, (\widetilde{\pi}^*)^+)](x, \mathbf{r})
$$
 using (a),  
\n
$$
= T_{\widetilde{g}_1^*}[\widetilde{\mathcal{V}}_n](x, \mathbf{r})
$$
 by the induction hypothesis,  
\n
$$
= T[\widetilde{\mathcal{V}}_n](x, \mathbf{r})
$$
 by definition of  $\widetilde{g}_1^*$ .

By taking the infimum, we get

<span id="page-14-0"></span>
$$
\inf_{\widetilde{\pi} \in \Pi_{\widetilde{\mathcal{X}}}} \widetilde{\mathcal{I}}_{n+1}((x,\mathbf{r}),\widetilde{\pi}) = \widetilde{\mathcal{V}}_{n+1}(x,\mathbf{r}) \le \widetilde{\mathcal{I}}_{n+1}((x,\mathbf{r}),\widetilde{\pi}^*) = T[\widetilde{\mathcal{V}}_n](x,\mathbf{r}).
$$
\n(3.8)

On the other hand, with an arbitrary policy <sup>π</sup><sup>e</sup> = (ge1, . . . , <sup>g</sup>e<sup>N</sup> ),

$$
\widetilde{\mathcal{I}}_{n+1}((x,\boldsymbol{r}),\widetilde{\pi}) = T_{\widetilde{g}_1}[\widetilde{\mathcal{I}}_n(\cdot,\widetilde{\pi}^+)](x,\boldsymbol{r}) \qquad \text{using (a)},
$$
\n
$$
\geq T_{\widetilde{g}_1}[\widetilde{\mathcal{V}}_n](x,\boldsymbol{r}) \qquad \text{by the monotonicity of } T,
$$
\n
$$
\geq T[\widetilde{\mathcal{V}}_n](x,\boldsymbol{r}) \qquad \text{by taking the infimum.}
$$

By taking the infimum, we get

<span id="page-14-1"></span>
$$
\inf_{\widetilde{\pi} \in \Pi_{\widetilde{\mathcal{X}}}} \widetilde{\mathcal{I}}_{n+1}((x, \mathbf{r}), \widetilde{\pi}) = \widetilde{\mathcal{V}}_{n+1}(x, \mathbf{r}) \ge T[\widetilde{\mathcal{V}}_n](x, \mathbf{r}). \tag{3.9}
$$

From [\(3.8\)](#page-14-0) and [\(3.9\)](#page-14-1), it follows by induction that

$$
\widetilde{\mathcal{V}}_n(x,\mathbf{r})=T[\widetilde{\mathcal{V}}_{n-1}](x,\mathbf{r})=\widetilde{\mathcal{I}}_n((x,\mathbf{r}),\widetilde{\pi}^*)
$$

for all n = 1, . . . , N.

ad e) Consider the Markovian policy <sup>π</sup><sup>e</sup> <sup>∗</sup> = (g<sup>e</sup> ∗ 1 , . . . , <sup>g</sup><sup>e</sup> ∗ <sup>N</sup> ) as defined in (d). We have just shown that <sup>V</sup>e<sup>N</sup> (x, <sup>r</sup>) = <sup>I</sup>e<sup>N</sup> ((x, <sup>r</sup>), <sup>π</sup><sup>e</sup> ∗ ), i.e. <sup>π</sup><sup>e</sup> ∗ is a minimizer of ([P](#page-11-1)e), and therefore an optimal policy for the <sup>N</sup>-step MDP with states in X × R <sup>i</sup>max . The claim follows by [\(3.7\)](#page-11-2) in Section [3.2.3](#page-11-0) where the policy bijection is explored.

# 3.3 Discounted finite horizon problems

We now consider finite horizon problems with a discount vector β ∈ (0, 1)imax , and prove the corresponding analogon to Theorem [3.7.](#page-12-0) The techniques used are similar to those from [Bäuerle and Rieder](#page-24-0) [\(2014\)](#page-24-0), where they are applied to univariate utility functions. Similar to the previous setting, we define the total cost I<sup>N</sup> (x, π), given an initial state x ∈ X , and a history dependent policy π ∈ ΠH, by

<span id="page-15-0"></span>
$$
\mathcal{I}_N(x,\pi) := \mathbb{E}_x^{\pi} \left[ \mathcal{U} \left( \sum_{n=0}^{N-1} \beta^n \cdot \mathcal{C}(X_n, A_n, X_{n+1}) \right) \right], \tag{3.10}
$$

and the corresponding value function, by

$$
\mathcal{V}_N(x) := \inf_{\pi \in \Pi_{\mathcal{H}}} \mathcal{I}_N(x, \pi).
$$
 (P)

We remark that the dot product appearing in [\(3.10\)](#page-15-0) is a componentwise product, i.e.

$$
a · b = (a1b1,..., anbn)
$$
 for  $a = (a1,..., an), b = (b1,..., bn).$ 

#### 3.3.1 Augmented problem

Again, we consider an augmented state space X × R <sup>i</sup>max × (0, 1)imax , where the new components keep track of the decreasing discount factor. Policy augmentation is done similar to the previous section. The new transition kernel <sup>P</sup><sup>e</sup> of the augmented problem is given by

$$
\widetilde{P}(\cdot|\widetilde{x};a) = \widetilde{P}(\cdot|(x,\mathbf{r},\mathbf{z});a) = (\mathcal{T}_{(x,\mathbf{r},\mathbf{z})}) \# P(\cdot|x,a),\tag{3.11}
$$

where

$$
\mathcal{T}_{(x,\mathbf{r},\mathbf{z})}(x') = (x', \mathbf{z} \cdot \mathbf{C}(x, a, x') + \mathbf{r}, \mathbf{z} \cdot \mathbf{\beta}).\tag{3.12}
$$

On the augmented state space, given an initial state x ∈ X , initial cost r ∈ R <sup>i</sup>max , initial discount rates z ∈ (0, 1)imax , and a policy <sup>π</sup><sup>e</sup> <sup>∈</sup> <sup>Π</sup><sup>H</sup><sup>e</sup> the total cost <sup>I</sup>en((x, <sup>r</sup>, z), <sup>π</sup>e) for <sup>n</sup> = 1, ..., N is given by

$$
\widetilde{\mathcal{I}}_n(\widetilde{x}, \widetilde{\pi}) = \widetilde{\mathcal{I}}_n((x, r, z), \widetilde{\pi}) := \widetilde{\mathbb{E}}_{\widetilde{x}}^{\widetilde{\pi}} \left[ \mathcal{U} \left( \boldsymbol{z} \cdot \sum_{k=0}^{n-1} \beta^k \cdot \boldsymbol{C}(X_k, A_k, X_{k+1}) + \boldsymbol{r} \right) \right]. \tag{3.13}
$$

The corresponding value function is

$$
\widetilde{\mathcal{V}}_n(\widetilde{x}) := \inf_{\widetilde{\pi} \in \Pi_{\widetilde{\mathcal{H}}}} \widetilde{\mathcal{I}}_n(\widetilde{x}, \widetilde{\pi}).
$$
\n
$$
(\widetilde{P})
$$

#### 3.3.2 Bellman operator and second theorem

Let

∆ := v : X × R <sup>i</sup>max × (0, 1)<sup>i</sup>max → R <sup>v</sup> is lower semi-continuous, v(x, ·, ·) is continuous, and componentwise increasing for all x ∈ X , v(x, r, z) ≥ U(r) for all (x, r, z) ∈ X × R <sup>i</sup>max × (0, 1) .

For <sup>v</sup> <sup>∈</sup> <sup>∆</sup> and a Markovian decision rule <sup>g</sup>e, we define the operators

$$
T_{\tilde{g}}[v](\tilde{x}) = T_{\tilde{g}}[v](x, r, z) := \int v(\tilde{x}') \tilde{P}(d\tilde{x}' | \tilde{x}, \tilde{g}(\tilde{x})) = \int v((x', r', z')) (\mathcal{T}_{(x, r, z)}) \# P(dx' | x, \tilde{g}(x, r, z))
$$
$$
= \int v(x', z \cdot C(x, \tilde{g}(x, r, z), x') + r, z \cdot \beta) P(dx' | x, \tilde{g}(x, r, z)),
$$

and

$$
T[v](x, \boldsymbol{r}, \boldsymbol{z}) = \inf_{a \in D(x)} \int v(x', \boldsymbol{z} \cdot \boldsymbol{C}(x, a, x') + \boldsymbol{r}, \boldsymbol{z} \cdot \boldsymbol{\beta}) P(dx' | x, a),
$$

whenever the integrals exist. T is again called the minimal cost operator. We may now state the main theorem of this section.

Theorem 3.9. Let <sup>V</sup>e<sup>0</sup>(x, <sup>r</sup>, <sup>z</sup>) := <sup>U</sup>(r). The following holds:

a) For any Markovian policy <sup>π</sup><sup>e</sup> = (ge<sup>1</sup>, . . .) <sup>∈</sup> <sup>Π</sup>Xe, we have the cost iteration

$$
\widetilde{\mathcal{I}}_n((x,\boldsymbol{r},\boldsymbol{z}),\widetilde{\pi})=T_{\widetilde{g}_1}[\ldots[T_{\widetilde{g}_{n-1}}[\widetilde{\mathcal{V}}_0]]](x,\boldsymbol{r},\boldsymbol{z})
$$

for all n = 1, . . . , N.

b) The optimal policy is Markovian, i.e.

$$
\inf_{\widetilde{\pi}\in \mathbf{\Pi}_{\widetilde{\mathcal{H}}}}\mathcal{I}_N(\widetilde{x},\widetilde{\pi})=\inf_{\widetilde{\pi}\in \mathbf{\Pi}_{\widetilde{\mathcal{X}}}}\mathcal{I}_N(\widetilde{x},\widetilde{\pi}).
$$

- c) The operator T : ∆ → ∆ is well-defined, and for every v ∈ ∆, there exists a minimizer of T[v].
- d) We get the Bellman-style equation

$$
\widetilde{\mathcal{V}}_n(x,\mathbf{r},\mathbf{z})=T[\widetilde{\mathcal{V}}_{n-1}](x,\mathbf{r},\mathbf{z})=\inf_{a\in D(x)}\int \widetilde{\mathcal{V}}_{n-1}(x',\mathbf{z}\cdot\mathbf{C}(x,a,x')+\mathbf{r},\mathbf{z}\cdot\mathbf{\beta})P(dx'\mid x,a)
$$

for all n = 1, . . . , N.

e) If <sup>g</sup><sup>e</sup> ∗ n is a minimizer of <sup>V</sup>en−<sup>1</sup> for <sup>n</sup> = 1, . . . , N, then <sup>π</sup><sup>e</sup> <sup>∗</sup> = (g<sup>e</sup> ∗ 1 , . . . , <sup>g</sup><sup>e</sup> ∗ <sup>N</sup> ) is an optimal policy for (Pe). In this situation, the history-dependent policy π <sup>∗</sup> = (f ∗ 0 , . . . , f <sup>∗</sup> N−1 ), defined by

$$
f_n^*(h_n) := \begin{cases} \widetilde{g}_N^*(x_0, 0, 1) & \text{if } n = 0, \\ \widetilde{g}_{N-n}^*\left(x_n, \sum_{k=0}^{n-1} \beta^k \cdot \mathbf{C}(x_k, a_k, x_{k+1}), \beta^n\right) & \text{otherwise,} \end{cases}
$$

is an optimal policy for problem (P).

Proof. The proof is similar to the derivation of Theorem [3.7.](#page-12-0) We will only prove (a) by induction. To that end, note that

$$
\widetilde{\mathcal{I}}_1((x,\boldsymbol{r},\boldsymbol{z}),\widetilde{\pi}) = \widetilde{\mathbb{E}}_x^{\widetilde{\pi}} \bigg[ \mathcal{U}(\boldsymbol{z} \cdot \boldsymbol{C}(X_0,A_0,X_1) + \boldsymbol{r}) \bigg] \n= \int \mathcal{U}(\boldsymbol{z} \cdot \boldsymbol{C}(x,\widetilde{g}_0(x,\boldsymbol{r},\boldsymbol{z}),x') + \boldsymbol{r}) P(dx' \mid x,\widetilde{g}_0(x,\boldsymbol{r},\boldsymbol{z})) \n= T_{\widetilde{g}_1}[\widetilde{\mathcal{V}}_0](x,\boldsymbol{r},\boldsymbol{z}).
$$

Let <sup>π</sup><sup>e</sup> <sup>+</sup> = (ge<sup>2</sup>, <sup>g</sup>e<sup>3</sup>, . . .). For <sup>n</sup> = 2, . . . , N, we get

$$
\widetilde{\mathcal{I}}_{n}((x, r, z), \widetilde{\pi}) = \mathbb{E}_{x}^{\widetilde{\pi}} \left[ \mathcal{U} \left( z \sum_{k=0}^{n-1} \beta^{k} \mathbf{C}(X_{k}, A_{k}, X_{k+1}) + r \right) \right]
$$
\n
$$
= \int \mathbb{E}_{x'}^{\widetilde{\pi}^{+}} \left[ \mathcal{U} \left( z \cdot \sum_{k=0}^{n-2} \beta^{k+1} \cdot \mathbf{C}(X_{k}, A_{k}, X_{k+1}) + z \cdot \mathbf{C}(x, \widetilde{g}_{1}(x, r, z), x') + r \right) \right] P(dx' \mid x, \widetilde{g}_{1}(x, r, z))
$$
\n
$$
= \int \widetilde{\mathcal{I}}_{n-1}((x', z \cdot \mathbf{C}(x, \widetilde{g}_{1}(x, r, z) + r, \beta \cdot z), \widetilde{\pi}^{+}) P(dx' \mid x, \widetilde{g}_{1}(x, r, z))
$$
\n
$$
= T_{\widetilde{g}_{1}}[\widetilde{\mathcal{I}}_{n-1}(\cdot, \widetilde{\pi}^{+})](\widetilde{x}) = T_{\widetilde{g}_{1}}[T_{\widetilde{g}_{2}}[\dots [T_{\widetilde{g}_{n-1}}[\widetilde{\mathcal{V}}_{0}]]]](x, r, z).
$$

The claim follows then inductively.

# 3.4 Infinite horizon problems

In this section, we study the infinite horizon problem with discount factor β ∈ (0, 1)imax . For a vector a ∈ R <sup>i</sup>max , we will denote with a = min{a1, . . . , a<sup>i</sup>max }, a = max{a1, . . . , a<sup>i</sup>max }. The notion of T and ∆ from the previous section is unchanged. The total cost in this situation reads as

$$
\mathcal{I}_{\infty}(x,\pi) := \mathbb{E}^{\pi}_x \left[ \mathcal{U} \left( \sum_{n=0}^{\infty} \beta^n \cdot C(X_n, A_n, X_{n+1}) \right) \right],
$$

and <sup>V</sup>e<sup>∞</sup> is defined accordingly. We shall use the following definition:

Definition 3.10. For a continuous function F : R <sup>d</sup> → R, we define the modulus of continuity ω<sup>F</sup> (δ, R) on the ball B(0, R), by

$$
\omega_{\mathcal{F}}(\delta, R) = \sup \left\{ |\mathcal{F}(x) - \mathcal{F}(y)| \middle| x, y \in B(0, R), \|x - y\|_2 < \delta \right\} \tag{3.14}
$$

Note that the modulus of continuity is increasing in both variables, and it holds limδ→<sup>0</sup> ω<sup>F</sup> (δ, R) → 0.

**Theorem 3.11.** Let 
$$
\underline{b}(r, z) := \mathcal{U}\left(z \cdot \frac{c}{1-\beta} + r\right)
$$
 and  $\overline{b}(r, z) := \mathcal{U}\left(z \cdot \frac{\overline{c}}{1-\beta} + r\right)$ , where  $\frac{1}{a} = \left(\frac{1}{a_1}, \dots, \frac{1}{a_{i_{max}}}\right)$ .

- a) Let K be a compact subset of R <sup>i</sup>max . Then, T <sup>n</sup>[b] % <sup>V</sup>e<sup>∞</sup>, <sup>T</sup> <sup>n</sup>[U] % <sup>V</sup>e<sup>∞</sup>, and <sup>T</sup> n[ ¯b] & <sup>V</sup>e<sup>∞</sup> as <sup>n</sup> → ∞ uniformly on X × K × (0, 1)imax .
- b) <sup>V</sup>e<sup>∞</sup> is the unique solution of

$$
\begin{cases}\nv = T[v], \\
v \in \Delta, \\
\underline{b}(\cdot, \cdot) \le v(x, \cdot, \cdot) \le \overline{b}(\cdot, \cdot) \text{ for all } x \in \mathcal{X}.\n\end{cases}
$$

- c) There exists a decision rule g ∗ that minimizes <sup>V</sup>e<sup>∞</sup>.
- d) The history-dependent policy f <sup>∗</sup> = (f ∗ 0 , f <sup>∗</sup> 1 , . . .) given by

$$
f_n^*(h_n) = g^* \left( x_n, \sum_{k=0}^{n-1} \beta^k c(x_k, a_k, x_{k+1}), \beta^n \right)
$$

is an optimal policy for V∞.

Proof. ad a) For <sup>n</sup> <sup>∈</sup> <sup>N</sup> and (x, <sup>r</sup>, <sup>z</sup>) <sup>∈</sup> <sup>X</sup>e, it holds

$$
\mathcal{U}\left(z \cdot \sum_{k=0}^{\infty} \beta^{k} \cdot C(x_{n}, a_{n}, x_{n+1}) + r\right) - \mathcal{U}\left(z \cdot \sum_{k=0}^{n} \beta^{k} \cdot C(x_{n}, a_{n}, x_{n+1}) + r\right)
$$
\n
$$
\leq \omega_{\mathcal{U}}\left(\left\|z \cdot \beta^{n} \sum_{k=n}^{\infty} \beta^{k-n} \cdot C(x_{k}, a_{k}, x_{k+1})\right\|_{2}, \left\|z \cdot \sum_{k=0}^{\infty} \beta^{k} \cdot C(x_{n}, a_{n}, x_{n+1}) + r\right\|_{2}\right).
$$
\n
$$
\leq \omega_{\mathcal{U}}\left(i_{\max} \overline{z} \overline{\beta}^{n} \frac{\overline{c}}{1 - \overline{\beta}}, i_{\max} \overline{z} \frac{\overline{c}}{1 - \overline{\beta}} + \overline{r}\right)
$$
\n(3.15)

Now, we get

$$
\widetilde{\mathcal{V}}_n(x,\boldsymbol{r},\boldsymbol{z}) \leq \widetilde{\mathcal{I}}_{n,\widetilde{\pi}}(x,\boldsymbol{r},\boldsymbol{z}) \leq \widetilde{\mathcal{I}}_{\infty,\widetilde{\pi}}(x,\boldsymbol{r},\boldsymbol{z}) = \mathbb{E}_{x}^{\widetilde{\pi}}\left[\mathcal{U}\left(\boldsymbol{z}\cdot\sum_{k=0}^{\infty}\boldsymbol{\beta}^{k}\cdot\boldsymbol{C}(X_{n},A_{n},X_{n+1})+\boldsymbol{r}\right)\right] \n\leq \mathbb{E}_{x}^{\widetilde{\pi}}\left[\mathcal{U}\left(\boldsymbol{z}\cdot\sum_{k=0}^{n}\boldsymbol{\beta}^{k}\cdot\boldsymbol{C}(X_{n},A_{n},X_{n+1})+\boldsymbol{r}\right)\right]+\omega_{\mathcal{U}}\left(i_{\max}\overline{z}\overline{\beta}^{n}\frac{\bar{c}}{1-\overline{\beta}},i_{\max}\overline{z}\frac{\bar{c}}{1-\overline{\beta}}+\overline{r}\right) \n\leq \widetilde{\mathcal{I}}_{n,\widetilde{\pi}}(x,\boldsymbol{r},\boldsymbol{z})+\underline{\omega_{\mathcal{U}}}\left(i_{\max}\overline{z}\overline{\beta}^{n}\frac{\bar{c}}{1-\overline{\beta}},i_{\max}\left(\overline{z}\frac{\bar{c}}{1-\overline{\beta}}+\overline{r}\right)\right).
$$

Since K is compact, there exists R > 0 such that ¯d < R. Then, we have

$$
\varepsilon_n(x, r, z) \le \omega_{\mathcal{U}} \left( i_{\max} \overline{\beta}^n \frac{\overline{c}}{1 - \overline{\beta}}, i_{\max} \frac{\overline{c}}{1 - \overline{\beta}} + R \right),
$$

and since <sup>β</sup> <sup>∈</sup> (0, 1), we have <sup>ε</sup><sup>n</sup> & <sup>0</sup> uniformly. Because <sup>π</sup><sup>e</sup> was arbitrary, the previous inequality also holds for the infimum, i.e.

<span id="page-18-0"></span>
$$
\widetilde{\mathcal{V}}_n(x,\mathbf{r},\mathbf{z}) \le \widetilde{\mathcal{V}}_\infty(x,\mathbf{r},\mathbf{z}) \le \widetilde{\mathcal{V}}_n(x,\mathbf{r},\mathbf{z}) + \varepsilon_n(x,\mathbf{r},\mathbf{z}),\tag{3.16}
$$

and therefore <sup>V</sup>e<sup>n</sup> % <sup>V</sup>e<sup>∞</sup>.

Recall that C is componentwise bounded by c, c >¯ 0, and therefore, independent of the process (Xn),(An), the infinite time cost P<sup>∞</sup> <sup>n</sup>=0 β n · C(Xn, An, Xn+1) is componentwise bounded by <sup>c</sup> 1−β , c¯ 1−β . We have therefore <sup>b</sup> <sup>≤</sup> <sup>V</sup>e<sup>∞</sup> <sup>≤</sup> ¯b. Since <sup>T</sup> is increasing, we have with the previous result <sup>V</sup>en+1 <sup>=</sup> <sup>T</sup>[Ven] <sup>≤</sup> <sup>T</sup>[Ve<sup>∞</sup>], i.e. <sup>V</sup>e<sup>∞</sup> <sup>≤</sup> <sup>T</sup>[Ve<sup>∞</sup>]. Since z ∈ (0, ∞) <sup>i</sup>max , we observe that for every triple (x, r, z) and a ∈ D(x), we have

$$
\varepsilon'_{n}(x, r, z, a) := \int \varepsilon_{n}(x', z \cdot \mathbf{C}(x, a, x') + r, z \cdot \beta) P(dx' | x, a)
$$
  
\n
$$
\leq \omega \left( i_{\max} \overline{z} \overline{\beta}^{n+1} \frac{\overline{c}}{1 - \overline{\beta}}, i_{\max} \left( \overline{z} \overline{\beta} \frac{\overline{c}}{1 - \overline{\beta}} + \overline{r} + \overline{z} \overline{c} \right) \right)
$$
  
\n
$$
\leq \omega \left( i_{\max} \overline{z} \overline{\beta}^{n+1} \frac{\overline{c}}{1 - \overline{\beta}}, i_{\max} \overline{z} \frac{\overline{c}}{1 - \overline{\beta}} \right) = \varepsilon_{n+1}(x, r, z).
$$
\n(3.17)

Now, we get with [\(3.16\)](#page-18-0)

$$
T[\widetilde{\mathcal{V}}_{\infty}](x, r, z) \le T[\widetilde{\mathcal{V}}_n + \varepsilon_n](x, r, z) \le T[\widetilde{\mathcal{V}}_n](x, r, z) + \sup_{a \in \mathcal{D}(x)} \varepsilon'_n(x, r, z, a)
$$
  
 
$$
\le \widetilde{\mathcal{V}}_{n+1}(x, r, z) + \varepsilon_{n+1}(x, r, z),
$$
 (3.18)

but the last term converges to zero as <sup>n</sup> ∈ ∞. Therefore we have, <sup>V</sup>e<sup>∞</sup> <sup>≥</sup> <sup>T</sup>[Ve<sup>∞</sup>], i.e. <sup>V</sup>e<sup>∞</sup> <sup>=</sup> <sup>T</sup>[Ve<sup>∞</sup>]. We next show that T n[ ¯b] & <sup>V</sup>e<sup>∞</sup>, and <sup>T</sup> <sup>n</sup>[b] % <sup>V</sup>e<sup>∞</sup> as <sup>n</sup> → ∞. First, observe that

$$
T[\bar{b}](x, r, z) = \inf_{a \in D(x)} \int \mathcal{U}\left(z \cdot \beta \cdot \frac{\bar{c}}{1 - \beta} + z \cdot C(x, a, x') + r\right) P(dx'|x, a)
$$
  
$$
\leq \mathcal{U}\left(z \cdot \frac{\bar{c}}{1 - \beta} + r\right)
$$
  
$$
\leq \bar{b}(r, z),
$$

and the same holds true for

$$
T[\underline{b}](x,r,z) \geq \underline{b}(r,z).
$$

Since T is increasing, the sequences (T n[ ¯b])<sup>n</sup> and (T <sup>n</sup>[b])<sup>n</sup> are pointwise monotone and bounded, and therefore their pointwise limit exists. By iteration,

$$
T^{n}[\mathcal{U}](x, r, z) = \inf_{\pi \in \mathbf{\Pi}_{\widetilde{\mathcal{X}}}} \mathbb{E}_{x}^{\pi} \left[ \mathcal{U} \left( z \cdot \sum_{k=0}^{n-1} \beta^{k} \cdot C(X_{k}, A_{k}, X_{k+1}) + r \right) \right]
$$
  
$$
T^{n}[\overline{b}] (x, r, z) = \inf_{\pi \in \mathbf{\Pi}_{\widetilde{\mathcal{X}}}} \mathbb{E}_{x}^{\pi} \left[ \mathcal{U} \left( z \cdot \beta^{n} \frac{\overline{c}}{1 - \beta} + z \cdot \sum_{k=0}^{n-1} \beta^{k} \cdot C(X_{k}, A_{k}, X_{k+1}) + r \right) \right].
$$

We obtain

$$
0 \leq T^{n}[\bar{b}](x, r, z) - T^{n}[\underline{b}](x, r, z) \qquad \text{by monotonicity of } T \text{ and } T(0) = 0
$$
  
\n
$$
\leq T^{n}[\bar{b}](x, r, z) - T^{n}[\mathcal{U}](x, r, z) \qquad \text{by monotonicity of } T \text{ and } \mathcal{U}(r) \leq \underline{b}(x, r, z)
$$
  
\n
$$
\leq \sup_{\pi \in \Pi_{\widetilde{\mathcal{H}}}} \mathbb{E}_{x}^{\pi} \left[ \mathcal{U} \left( z \cdot \beta^{n} \frac{\bar{c}}{1 - \beta} + z \sum_{k=0}^{n-1} \beta^{k} \cdot C(X_{k}, A_{k}, X_{k+1}) + r \right) - \mathcal{U} \left( z \cdot \sum_{k=0}^{n-1} \beta^{k} \cdot C(X_{k}, A_{k}, X_{k+1}) + r \right) \right]
$$
  
\n
$$
= \varepsilon_{n}(x, r, z).
$$

For n → ∞, we obtain

$$
\lim_{n \to \infty} T^n[b] = \lim_{n \to \infty} T^n[\overline{b}] = \lim_{n \to \infty} T^n[\mathcal{U}] = \widetilde{\mathcal{V}}_{\infty},
$$

uniformly on compact sets. This proves (a).

ad b) <sup>V</sup>e<sup>∞</sup> is lower semi-continuous as a uniform limit on sets of the form X × <sup>K</sup> <sup>×</sup> (0, 1)imax , where <sup>K</sup> is a compact subset of R <sup>i</sup>max , of lower semi-continuous function. As proved in Theorem [3.7,](#page-12-0) T n[ ¯b](x, ·, ·) is continuous and componentwise monotonous for all x ∈ X . Since T n[ ¯b] & <sup>V</sup>e<sup>∞</sup>, <sup>V</sup>e<sup>∞</sup>(x, ·, ·) is upper semi-continuous and therefore continuous, and also preserves the same monotonicities for each <sup>x</sup> ∈ X . We have thereby shown <sup>V</sup>e<sup>∞</sup> <sup>∈</sup> <sup>∆</sup>.

It remains to show the uniqueness. To that end, suppose that there is <sup>v</sup> <sup>∈</sup> <sup>∆</sup>, <sup>v</sup> <sup>6</sup><sup>=</sup> <sup>V</sup>e<sup>∞</sup> such that <sup>v</sup> <sup>=</sup> <sup>T</sup>[v] with b ≤ v ≤ ¯b. Then, because T is increasing, T <sup>n</sup>[b] ≤ T <sup>n</sup>[v] = v ≤ T n[ ¯b], and with <sup>n</sup> ∈ ∞, we get <sup>V</sup>e<sup>∞</sup> <sup>≤</sup> <sup>v</sup> <sup>≤</sup> <sup>V</sup>e<sup>∞</sup>, i.e. <sup>v</sup> <sup>=</sup> <sup>V</sup>e<sup>∞</sup>, a contradiction. This proves (b).

- ad c) The claim follows similar to Theorem [3.7.](#page-12-0)
- ad d) Since <sup>V</sup>e<sup>∞</sup>(x, y, z) ≥ U(y), we obtain

$$
\widetilde{\mathcal{V}}_{\infty} = \lim_{n \to \infty} T_{g^*}^n[\widetilde{\mathcal{V}}_{\infty}] \ge \lim_{n \to \infty} T_{g^*}^n[\mathcal{U}] = \lim_{n \to \infty} \widetilde{\mathcal{I}}_n(\cdot, (g^*, g^*, \dots)) = \widetilde{\mathcal{I}}_{\infty}(\cdot, (g^*, g^*, \dots)) \ge \widetilde{\mathcal{V}}_{\infty},
$$

Hence f ∗ is optimal for <sup>I</sup>e<sup>∞</sup>. This finally proves (d).

# 4 Numerical example

# 4.1 Task design

To illustrate our method, we present a generalized version of the repetitive Tiger problem [\(Kaelbling, Littman, &](#page-25-16) [Cassandra, 1998\)](#page-25-16). In the classic Tiger problem, a decision-maker is faced with two close doors, behind one of which is a tiger (punishment) and behind the other is a treasure (reward). In the original version, the agent can either open a door or listen to tiger sound in order to gain more information about the true place of the tiger. The sound signal however, is not fully reliable and with a smaller probability (20%) it can be heard from the wrong door. Each time that agent opens a door, it takes the reward/punishment and the problem resets. By resetting the problem, the position of the tiger and the treasure would be determined randomly and would remain fixed for the entire next trial.

The version we will discuss here, has been generalized in three aspects: First, the constraint of deterministic state space has been relaxed and the position of the tiger can change during a trial. Here, there is a 10 % chance to change its position at the start of each epoch. In the second extension, the immediate reward (punishment) of opening the doors would not be observable for the agent during the repeats of the problem. Therefore, at any time before the end of the all trials, the agent can only have an estimation about its gains. At the end of all trials, the agent would observe the whole accumulated reward and punishments. And third, the action space is expanded in a way that makes the agent able to not only choose the correct option (treasure door) but also bet on its own decision in different levels of investment. Here, we define that the agent can open each door either conservatively (low stake actions), to gain a lower amount of reward and punishment (low stake rewards: Rewardcorr\_low and Rewardincorr\_low), or rush to the doors (high stake actions), to gain a bigger reward if it is the treasure, and to take more damage if the tiger is behind the door. (high stake rewards: Rewardcorr\_High and Rewardincorr\_High).

The underlying MDP of the experiment is depicted in fig [1.](#page-21-0) Here, the probabilities of getting observations (Otiger\_right and Otiger\_lef t) are depend on the agent's actions and the successive new state. As mentioned before, by doing the listen action there is a smaller probability that agent takes a false signal. Also, by doing each of open actions (regardless of their correctness or their stake type) the MDP will be reset and a random signal, with probability of 0.5 for pointing to each state, would be received. In other words, the signal which received after the re-initializing the problem, is uninformative in purpose of detecting the tiger's position. The observation function of the experiment's POMDP is shown in table 1.

# 4.2 Simulation results

In order to illustrate the competency of our method in replicating different risk sensitive behaviors, in this section we have tested our method on the extended tiger task by using four different utility functions which are composed by linear combinations of of exponential functions. Three out of them are adjusted to address risk-neutral, risk-seeking and risk-aversion decision-making. It means the utility functions are (near-)linear, convex and concave in the interval of possible rewards respectively. It should be mentioned that as in our method e 0 is not a valid term, linear combinations cannot replicate an exact linear function ( <sup>d</sup> <sup>2</sup>U dx<sup>2</sup> 6= 0). However, for the sake of being more intuitive we used a utility function with an infinitesimal second derivative in the interval of rewards to show the ability of the model to mimic different patterns of risk sensitivity (fig2.a). Last but not least, we have tested our model on the

![](_page_21_Figure_0.jpeg)

<span id="page-21-0"></span>Figure 1: MDP of the Extended Tiger task. The states of the MDP are Tiger\_right(TR) and Tiger\_left(TL). After each opening action (red and blue arrows), the environment would set to a state randomly and based on either choosing tiger door or treasure door as well as choosing either high stake or low stake action (thickness of the arrows), the non-observable reward will receive by agent. By doing listen action, the agent will pay a small cost and takes an informative signal about the position of the tiger. There is also a small chance that tiger changes its position.

|                                            | $\boldsymbol{0}_1$ :<br>Tiger_right | $O_2$ :<br>Tiger_left |
|--------------------------------------------|-------------------------------------|-----------------------|
| a: listen<br>s':Tiger_right                | 0.8                                 | 0.2                   |
| a: listen<br>$s'$ : Tiger_left             | 0.2                                 | 0.8                   |
| a:open_right(low/high)<br>s':Tiger_right   | 0.5                                 | 0.5                   |
| a: open_left(low/high)<br>$s'$ :Tiger_left | 0.5                                 | 0.5                   |
|                                            |                                     |                       |

Figure 2: Tabular representation of the Observation Function.

![](_page_22_Figure_0.jpeg)

Figure 3: Utility functions. a. Utility functions produce risk\_neutral, risk\_seeking and risk\_aversion decisions in the showed interval respectively. risk\_neutral: U<sup>1</sup> = 1.5e <sup>0</sup>.<sup>3</sup> −1.5e −0.3 , risk\_seeker: U<sup>2</sup> = e <sup>1</sup>.<sup>5</sup> −0.5e −0.1 , risk\_avers: U<sup>3</sup> = 0.6e <sup>0</sup>.<sup>05</sup> − 0.6e −2.5 . b. Approximation of Sigmoid function by weighted sum of five exponential functions.

task with a sigmoid utility function. As mentioned before, it is assumed that human uses S-shaped utility functions, like sigmoid function, in face with losses and gains. Therefore, regarding computational modeling of behavior, it is a crucial ability for a risk sensitive model to mimic such functions. Like the linear case, sigmoid function cannot be expressed by linear combinations of exponential functions. However, we can approximate the sigmoid in a specific interval by using a combination which contains enough numbers of exponential functions. Here, We fitted weighted sum of five exponential terms: 0.381∗e 0.2906 , 0.404∗e 0.2876 , −0.427∗e −0.0091 , −0.182∗e 0.6537 , 0.322∗e 0.2982 .

The simulation results have been presented in table 2. The results clearly show the effect of utility functions' shape on the risk attitude of the simulated agent. In table 2 we only present selected actions in trials with depth of planning equal to either one or two steps. As we have used deterministic greedy policy in our simulations, choosing between different action types (listening, low stake door openings and high stake door openings) in plannings with maximum depth of one or two only depends on environment dynamics, utility function, discount factor and initial wealth. In other words, in planning with depth one or two, choosing the type of actions(and not their directions) is independent from the observations from the environment side. Therefore, we can easily fix the other dynamics and examine only the effect of utility functions. In this simulations, we have fixed the environments dynamics to the above-mentioned values, with no discounting and the initial wealth equals to zero.

In the extended tiger problem, one can assume that high/low stake opening actions represent riskiness of the decisions. While the expected reward of them are equal, the deviation of outcomes in high stake cases are higher. [4](#page-23-0) shows that in the maximum planning-depth of two, risk-neutral agent prefers to gather more information (and pay its cost) in the first step, and then in the second step open the door with higher probability of being treasure in high stake mode.

|                         | Depth: 1 | Depth: 2 |       |
|-------------------------|----------|----------|-------|
|                         | Step 1   | Step 1   | step2 |
| $U_1$ :<br>risk-neutral | Low      | Listen   | High  |
| $U$ 2:<br>risk-seeking  | High     | High     | High  |
| $U$ 3:<br>risk-averse   | Low      | Listen   | Low   |
| $U$ 4:<br>Sigmoid       | High     | Listen   | High  |

#### <span id="page-23-0"></span>Figure 4: Actions with best value for each step under different utility functions.

However, the risk averse agent(u3) prefers to do the second action more conservatively and open the door in the low stake mode while in contrast with them, the risk-seeker agent (u2) prefers to perform risky actions in each step. The sigmoid-agent also behaves like the risk-neutral case, however it should be considered that S-shaped utilities make agents risk-averse toward positive accumulated outcomes and risk-averse in face with negative valuations of total expected rewards. In one step planning conditions, paying the certain cost of listening rather than doing a risky action with higher expected return seems irrational for all of used utility functions. However, risk-averse and risk-neutral cases prefer to choose low stake actions in a fifty-fifty situation while the risk-seeker and sigmoid agents prefer to risk more.

# 5 Discussion

The method we introduced works for problems which have finite set of states while using any increasing utility function. Our method calculates the exact utility values in case of weighted sum of exponential utility functions and approximate them for any other monotone function, contrasting [Bäuerle and Rieder](#page-24-8) [\(2017\)](#page-24-8) which is more general and doesn't need to approximate values. However the resulting augmented state space in Mutlivariate utility method is P(X ) <sup>i</sup>max × Y × R <sup>i</sup>max ⊂ R |X |×2×imax × Y, where imax is the number of exponential functions that make up the utility function, see [\(1.2\)](#page-2-0). In [Bäuerle and Rieder](#page-24-8) [\(2017\)](#page-24-8), the resulting state space is P(X × R) which is an infinite dimensional space, and even in cases where the wealth space is discretized appropriately, one ends up with a dimension of |X |·(partition size). Our method therefore has a clear computational advantage when imax is small. In the general case of approximating utility function, the lower dimensionality of Multivariate method brings the trade-off between accuracy of approximation and computational tractability to attention. One can expect that by increasing the number of exponential terms in the approximated utility function, the accuracy of approximated utility values would improve (become more similar to their exact non-approximated values) but in the cost of an increase in state space dimensionality. Moreover by increasing the depth of planning, the method introduced by [Bäuerle and Rieder](#page-24-8) [\(2017\)](#page-24-8) would also face with the trade-off between lack of accuracy and increase of state space complexity in case of using partitioned wealth-axis. Because, when the maximum depth of planning grows the possible amounts of wealth would also increase. Both mentioned accuracy/complexity trade-offs are heavily dependent on the dynamics of the problem as well as the utility function and can be subject of further studies. Last but not least, our proposed model is eligible to apply on problems which would be defined in a multi-variate manner. In this work we only discussed the ability of the Multivariate model to address monotone utility functions in a class of problems which only have one objective (wealth), however the problems with different separate running costs like: resource allocation in different governmental sectors or maximizing the overall utility of an economic actor while she uses different diminishing marginal utility functions in different goods or aspects of life are another area that our method can address and could be investigated more in terms of computational efficiency.

# References

- <span id="page-24-12"></span>Al-Nowaihi, A., Bradley, I., & Dhami, S. (2008). A note on the utility function under prospect theory. Economics letters, 99 (2), 337–339.
- <span id="page-24-6"></span>Baras, J. S., & James, M. R. (1997). Robust and Risk-Sensitive Output Feedback Control for Finite State Machines and Hidden Markov Models. Journal of Mathematics, Systems, Estimation and Control, 7 (3), 371–374.
- <span id="page-24-7"></span>Bäuerle, N., & Rieder, U. (2017). Partially observable risk-sensitive stopping problems in discrete time. arXiv preprint arXiv:1703.09509 .
- <span id="page-24-13"></span><span id="page-24-1"></span>Bertram, L., Schulz, E., & Nelson, J. D. (2021). Subjective probability is modulated by emotions.
- Borkar, V. S., & Meyn, S. P. (2002). Risk-Sensitive Optimal Control for Markov Decision Processes with Monotone Cost. Mathematics of Operations Research, 27 (1), 192–209.
- <span id="page-24-15"></span>Bäuerle, N., & Rieder, U. (2011). Markov Decision Processes with Applications to Finance. Berlin, Heidelberg: Springer.
- <span id="page-24-0"></span>Bäuerle, N., & Rieder, U. (2014). More Risk-Sensitive Markov Decision Processes. Mathematics of Operations Research, 39 (1), 105–120.
- <span id="page-24-8"></span>Bäuerle, N., & Rieder, U. (2017). Partially Observable Risk-Sensitive Markov Decision Processes. Mathematics of Operations Research, 42 (4), 1180–1196.
- <span id="page-24-2"></span>Cavazos-Cadena, R. (2010). Optimality equations and inequalities in a class of risk-sensitive average cost Markov decision chains. Mathematical Methods of Operations Research, 71 (1), 47–84.
- <span id="page-24-9"></span>Cavazos-Cadena, R., & Hernández-Hernández, D. (2005). Successive approximations in partially observable controlled Markov chains with risk-sensitive average criterion. Stochastics, 77 (6), 537–568.
- <span id="page-24-3"></span>Chung, K.-J., & Sobel, M. J. (1987). Discounted MDP's: Distribution Functions and Exponential Utility Maximization. SIAM Journal on Control and Optimization, 25 (1), 49–62.
- <span id="page-24-4"></span>Di Masi, G. B., & Stettner, L. (2007). Infinite Horizon Risk Sensitive Control of Discrete Time Markov Processes under Minorization Property. SIAM Journal on Control and Optimization, 46 (1), 231–252.
- <span id="page-24-5"></span>Dupuis, P., Laschos, V., & Ramanan, K. (2019). Exit time risk-sensitive control for systems of cooperative agents. Mathematics of Control, Signals, and Systems, 31 (3), 279–332.
- <span id="page-24-14"></span><span id="page-24-10"></span>Edwards, W. (1954). The theory of decision making. Psychological bulletin, 51 (4), 380.
- Fan, J., & Ruszczyński, A. (2018). Risk measurement and risk-averse control of partially observable discrete-time Markov systems. Mathematical Methods of Operations Research, 88 (2), 161–184.
- <span id="page-24-11"></span>Fernandez-Gaucherand, E., & Marcus, S. I. (1997). Risk-sensitive optimal control of hidden Markov models: Struc-

tural results. IEEE Transactions on Automatic Control, 42 (10), 1418–1422.

- <span id="page-25-2"></span>Fleming, W. H., & Hernández-Hernández, D. (1997). Risk-Sensitive Control of Finite State Machines on an Infinite Horizon I. SIAM Journal on Control and Optimization, 35 (5), 1790–1810.
- <span id="page-25-6"></span>Hernández-Hernández, D. (1999). Partially Observed Control Problems with Multiplicative Cost. In W. M. McEneaney, G. Yin, & Q. Zhang (Eds.), Stochastic Analysis, Control, Optimization and Applications (pp. 41–55). Basel: Birkhäuser.
- <span id="page-25-3"></span>Hernández-Hernández, D., & Marcus, S. I. (1996). Risk sensitive control of Markov processes in countable state space. Systems & Control Letters, 29 (3), 147–155.
- <span id="page-25-15"></span>Hernández-Lerma, O., & Lasserre, J.-B. (1996). Discrete-Time Markov Control Processes: Basic Optimality Criteria (Vol. 30). New York: Springer.
- <span id="page-25-0"></span>Hinderer, K. (1970). Foundations of Non-stationary Dynamic Programming with Discrete Time Parameter (Vol. 33). Berlin, Heidelberg: Springer.
- <span id="page-25-4"></span>Howard, R. A., & Matheson, J. E. (1972). Risk-Sensitive Markov Decision Processes. Management Science, 18 (7), 356–369.
- <span id="page-25-1"></span>Jaquette, S. C. (1973). Markov Decision Processes with a New Optimality Criterion: Discrete Time. The Annals of Statistics, 1 (3), 496–505.
- <span id="page-25-16"></span>Kaelbling, L. P., Littman, M. L., & Cassandra, A. R. (1998). Planning and acting in partially observable stochastic domains. Artificial intelligence, 101 (1-2), 99–134.
- <span id="page-25-14"></span><span id="page-25-13"></span>Kahneman, D., & Tversky, A. (1979). On the interpretation of intuitive probability: A reply to jonathan cohen.
- Kahneman, D., & Tversky, A. (2013). Prospect theory: An analysis of decision under risk. In Handbook of the fundamentals of financial decision making: Part i (pp. 99–127). World Scientific.
- <span id="page-25-10"></span>Kalyanaram, G., & Winer, R. S. (1995). Empirical generalizations from reference price research. Marketing science, 14 (3\_supplement), G161–G169.
- <span id="page-25-5"></span>Levitt, S., & Ben-Israel, A. (2001). On Modeling Risk in Markov Decision Processes. In A. M. Rubinov & B. M. Glover (Eds.), Optimization and Related Topics (Vol. 47, pp. 27–40). Springer US.
- <span id="page-25-7"></span>Marecki, J., & Varakantham, P. (2010). Risk Sensitive Planning in Partially Observable Environments. In Proceedings of the 9th International Conference on Autonomous Agents and Multiagent Systems (AAMAS) (pp. 1357–1368). Toronto, Canada.
- <span id="page-25-12"></span><span id="page-25-11"></span>Markowitz, H. (1952). The utility of wealth. Journal of political Economy, 60 (2), 151–158.
- Mosteller, F., & Nogee, P. (1951). An experimental measurement of utility. Journal of Political Economy, 59 (5), 371–404.
- <span id="page-25-9"></span>Tversky, A., & Kahneman, D. (1992). Advances in prospect theory: Cumulative representation of uncertainty. Journal of Risk and uncertainty, 5 (4), 297–323.
- <span id="page-25-8"></span>Von Neumann, J., & Morgenstern, O. (1947). Theory of games and economic behavior, 2nd rev.