# Exit Time Risk-Sensitive Control for Systems of Cooperative Agents

Paul Dupuis<sup>∗</sup> , Vaios Laschos† , and Kavita Ramanan‡

August 23, 2018

#### Abstract

We study a sequence of many-agent exit time stochastic control problems, parameterized by the number of agents, with risk-sensitive cost structure. We identify a fully characterizing assumption, under which each such control problem corresponds to a risk-neutral stochastic control problem with additive cost, and sequentially to a risk-neutral stochastic control problem on the simplex that retains only the distribution of states of agents, while discarding further specific information about the state of each agent. Under some additional assumptions, we also prove that the sequence of value functions of these stochastic control problems converges to the value function of a deterministic control problem, which can be used for the design of nearly optimal controls for the original problem, when the number of agents is sufficiently large.

## <span id="page-0-0"></span>1 Introduction

#### 1.1 Motivation and Background

In this paper, we study many-agent exit time stochastic control problems with risk-sensitive cost. Each agent occupies a state that takes values in a finite set X , and by controlling the transition rates between states for each agent, we try to keep the system away from a "ruin" set K, for as long as possible and with the least cost. We prove, under suitable assumptions, that for every finite number n of agents the control problem is equivalent to one with an additive cost structure. Moreover, when K ⊂ X <sup>n</sup> can be identified with a subset of the simplex of probability measures P(X ), in the sense that for every permutation σ of {1, 2, . . . , n} we have σK = K, then we can replace the original problem by one on P n (X ) = P(X ) ∩ 1 n Z d , getting in this way a control problem whose state is the empirical measure on the states of the individual agents. We also study the behavior as n → ∞ of the sequence of suitable renormalized value functions, and prove uniform convergence to the value function of a deterministic control problem.

We first describe the model without control, which we call the "base" or "nominal" model. Let X = {e1, . . . , ed}, where e<sup>i</sup> is the ith unit vector in R d . Let also γ = {γxy}(x,y)∈X ×X denote the rates of an ergodic Markov jump process on X . This process has the generator

<span id="page-0-1"></span>
$$
\mathcal{L}_{\gamma}[f](x) = \sum_{y \in \mathcal{X}} \gamma_{xy} \left[ f(y) - f(x) \right],\tag{1.1}
$$

<sup>∗</sup>Research supported in part by AFOSR FA9550-12-1-0399

<sup>†</sup>Research supported in part by AFOSR FA9550-12-1-0399

<sup>‡</sup>Research supported in part by AFOSR FA9550-12-1-0399 and PI NSF DMS-171303

for functions f : X 7→ R. For n ∈ N, consider n agents that move independently and stochastically, with each taking values in X = {e1, . . . , ed}. Then the dynamics of these agents can be represented by a stochastic process taking values in X n . Let x <sup>n</sup> = (x n 1 , . . . , x<sup>n</sup> n ) denote a generic element of X n . Also, for x, y ∈ X , i ∈ {1, . . . , n}, let vxy := y−x and let v n i,xy = (0, . . . , 0, vxy, 0, . . . , 0) be a d×n matrix with all columns equal to zero apart from the ith column, which is equal to the vector vxy. Also, let Z := {(x, y) ∈ X ×X : γxy > 0}, and define Z<sup>x</sup> := {y ∈ X : (x, y) ∈ Z} to be the set of allowed transitions from x. Then the generator of the state process of the base model takes the form

<span id="page-1-0"></span>
$$
\mathcal{L}_{\gamma}^{n}[f](\boldsymbol{x}^{n}) = \sum_{i=1}^{n} \sum_{y \in \mathcal{Z}_{x_{i}^{n}}} \gamma_{x_{i}^{n}y} \left[ f(\boldsymbol{x}^{n} + \boldsymbol{v}_{i,x_{i}^{n}y}^{n}) - f(\boldsymbol{x}^{n}) \right],
$$
\n(1.2)

for f : X n 7→ R. Note that the span of Z is the hyperplane

<span id="page-1-2"></span>
$$
\mathcal{H} := \left\{ \sum_{(x,y)\in\mathcal{Z}} a_{xy} \mathbf{v}_{xy} : a_{xy} > 0, (x,y) \in \mathcal{Z} \right\},\tag{1.3}
$$

which, since γ is ergodic, coincides with the hyperplane through the origin that is parallel to P(X ). We claim that the set H does not change if the axy are allowed to be arbitrary real numbers. To see why this is true, note that by ergodicity, for any two states (x, y) ∈ Z there is a sequence of states x = x1, ..., x<sup>j</sup> = x that satisfies y = x<sup>2</sup> and the property that (x<sup>i</sup> , xi+1) ∈ Z for <sup>i</sup> = 1, . . . , j <sup>−</sup>1, and hence, <sup>P</sup>j−<sup>1</sup> <sup>i</sup>=1 vxixi+1 = 0. Repeating this for every possible (x, y) ∈ Z, there are strictly positive integers bxy such that P (x,y)∈Z bxyvxy = 0, which implies the claim.

Next we introduce the empirical measure process. This process is obtained by projecting from X <sup>n</sup> onto P n (X ) = P(X ) ∩ 1 n Z <sup>d</sup> ⊂ P(<sup>X</sup> ), and has the generator

<span id="page-1-1"></span>
$$
\mathcal{M}_{\gamma}^{n}[f](\boldsymbol{m}) = n \sum_{(x,y)\in\mathcal{Z}} \gamma_{xy} m_{x} \left[ f\left(\boldsymbol{m} + \frac{1}{n} \boldsymbol{v}_{xy}\right) - f(\boldsymbol{m}) \right]. \tag{1.4}
$$

One can interpret the base model introduced above as a collection of independent agents with each evolving according to the transition rate γ. This is the "preferred" or "nominal" dynamics, and is what would occur if no "outside influence" or other form of control acts on the agents. If a controller should wish to change this behavior, then it must pay a cost to do so. We would like to model the situation in which limited information about the system state, and in particular information relating only to the empirical measure of the states of all agents, is used to produce a desired behavior of the group of agents, which again will be characterized in terms of their empirical measure.

To precisely formulate the control problem, we consider a continuous "reward" function R : P(X ) → [0,∞), where we recall

$$
\mathcal{P}(\mathcal{X}) := \left\{ \boldsymbol{m} \in \mathbb{R}^{\mathcal{X}} : m_x \ge 0 \text{ for all } x \in \mathcal{X} \text{ and } \sum_{x \in \mathcal{X}} m_x = 1 \right\}
$$

is the simplex of probability measures on X . We also have a cost function C = {Cxy : [0,∞) → [0,∞]}(x,y)∈Z . In the controlled setting, the jump rates of each agent can be perturbed from γ to u, and we let χ <sup>n</sup> denote the corresponding controlled state occupied by the collection of agents. If the problem is of interest over the interval [0, T], where T can be a random variable, and the initial state is x <sup>n</sup> <sup>=</sup> {<sup>x</sup> n i }i≤<sup>n</sup> ∈ X <sup>n</sup> , then there is a collective risk-sensitive cost (paid by the coordinating controller) equal to

$$
\mathbb{E}_{\mathbf{x}^n} \left[ \exp \left( \int_0^T \left( \sum_{i=1}^n \sum_{y \in \mathcal{Z}_{\chi_i^n(t)}} \gamma_{\chi_i^n(t)y} C_{\chi_i^n(t)y} \left( \frac{u_{\chi_i^n(t)y}(t,i)}{\gamma_{\chi_i^n(t)y}} \right) - nR(L(\mathbf{\chi}^n(t))) \right) dt \right) \right],
$$
 (1.5)

where for any x <sup>n</sup> <sup>=</sup> {<sup>x</sup> n i }i≤<sup>n</sup> ∈ X <sup>n</sup> , define

<span id="page-2-2"></span>
$$
L(\boldsymbol{x}^n) := \sum_{i=1}^n \delta_{x_i^n}.
$$
\n(1.6)

Here, the control process u takes values in a space that will be defined later, and for a collection of n|Z| independent Poisson random measures (PRM) {N<sup>1</sup> i,xy}1≤i≤n,(x,y)∈Z with intensity measure equal to Lebesgue measure, the controlled dynamics are given by

<span id="page-2-0"></span>
$$
\chi_i^n(t) = x_i^n + \sum_{(x,y)\in\mathcal{Z}} \mathbf{v}_{xy} \int_{(0,t]} \int_{[0,\infty)} 1_{[0,1_x(\chi_i^n(s-))u_{xy}(s,i)]}(r) N_{i,xy}^1(ds dr). \tag{1.7}
$$

Thus χ n i changes from state x to y with rate uxy. The formulation of the dynamics in terms of a stochastic differential equation will be convenient in the analysis to follow.

In this paper we present two results. The first is that, under additional assumptions on the cost C, for each n, the risk-sensitive control problem is equivalent to an ordinary control problem with the cost function F = {Fxy}(x,y)∈Z , where Fxy is defined by

<span id="page-2-1"></span>
$$
F_{xy}(q) := \sup_{u \in (0,\infty)} G_{xy}(u,q) \text{ and } G_{xy}(u,q) := \left[ u\ell\left(\frac{q}{u}\right) - \gamma_{xy} C_{xy}\left(\frac{u}{\gamma_{xy}}\right) \right],\tag{1.8}
$$

with

<span id="page-2-3"></span>
$$
\ell(q) := q \log q - q + 1, \qquad \text{for } q \ge 0.
$$
\n
$$
(1.9)
$$

Under the additional conditions we do not end up with a stochastic game, as is typically the case for risk-sensitive control problems, but rather a control problem with additive cost. Control problems are often substantially simpler than games, and in particular are often more tractable from a computational perspective. The second contribution, again under additional assumptions on C, is that the sequence of value functions, suitably renormalized, converges to the value function [\(4.3\)](#page-19-0) of a deterministic control problem. This convergence result is also helpful in the construction of near-optimal controls for a large n-agent system.

Example 1.1 As an example consider the issue of modeling the users of a resource such as energy. Here the agents would be households or similar entities. The state of an agent indicates their use of the common resource, and this usage evolves in a Markovian fashion. In exchange for a cost paid by the central controller to the individual agents, the agents agree to modify their behavior based on the current loading of the system. Thus an energy consumer would agree to give up control on if or when certain activities requiring energy consumption take place thus altering the evolution of his own state, but will be compensated for doing so by the central controller. The goal of the central controller, and the motivation for paying this cost, is to manage the group behavior so as to keep the system, as characterized by the empirical measure, in a desired operating region for as long as possible and with minimal cost. In this context, the use of risk sensitive cost is motivated in part by the resulting properties of robustness with respect to model error.

Remark 1.1 If one wishes, it is possible to work with sequences C<sup>n</sup> , R<sup>n</sup> of cost and reward functions, as long as some type of convergence is assumed for when n goes to infinity. The reader that is interested in such a generalization can look at a previous version of our paper in *[http: // www. wias-berlin. de/ preprint/ 2407/ wias\\_ preprints\\_ 2407\\_ 20180212. pdf](http://www.wias-berlin.de/preprint/2407/wias_preprints_2407_20180212.pdf)*

#### 1.2 Related literature and remarks

For ordinary discrete-time and continuous-time stochastic control problems (also referred to as Markov decision processes) [\[1,](#page-41-0) [17,](#page-42-0) [24,](#page-42-1) [27,](#page-42-2) [14\]](#page-42-3), one controls a random process to optimize an expected cost. The most common objective function that is optimized for continuous-time escape (or ruin) stochastic control problems are of the form

$$
J_T(x_0, \pi) = \mathbb{E}_{x_0, \pi} \left[ \int_0^T C(X_t, u_t) dt + P(X_T) \right],
$$
\n(1.10)

where C is some cost function that depends on the state x ∈ X and the control/action u ∈ U, and π is a policy or strategy that influences the dynamics {X<sup>t</sup> , t ≥ 0}, and P is a terminal cost that depends on the final state of the system. For risk-sensitive stochastic control problems one deals with optimality criteria of the form

$$
J_T(x_0, \pi) = g^{-1} \left( \mathbb{E}_{x_0, \pi} \left[ g \left( \int_0^T C(X_t, u_t) dt + P(X_T) \right) \right] \right), \tag{1.11}
$$

where g is a monotone convex/concave function, and C and P are as above. One motivation behind the use of risk-sensitive cost structures is that, depending on the type of monotonicity, variation from the average is more (risk-averting behavior) or less (risk-seeking behavior) penalized. One of the most studied cases is the entropic risk measure corresponding to gθ(x) = e θx, θ <sup>∈</sup> <sup>R</sup> (see [\[2,](#page-41-1) [7,](#page-41-2) [8,](#page-41-3) [13,](#page-42-4) [16,](#page-42-5) [18,](#page-42-6) [20,](#page-42-7) [21\]](#page-42-8) for discrete time and [\[10,](#page-41-4) [11,](#page-42-9) [15\]](#page-42-10) for continuous time). The function gθ(x) = e θx is special because it satisfies the property

$$
\frac{1}{\theta} \log \left( \mathbb{E} \left[ \exp \left( \theta X \right) \right] \right) = \tilde{X} + \frac{1}{\theta} \log \left( \mathbb{E} \left[ e^{\theta (X - \tilde{X})} \right] \right),
$$

where X is a random variable and X˜ its expectation. This property implies that the weight that is given to deviations from the expectation depends only on the difference from the expectation and not the expectation itself. It can be proved that the exponential is the only function that satisfies such a property (see [\[26\]](#page-42-11)). Furthermore, exponential integrals have a variational characterization involving entropy, which turns out to be convenient from the mathematical point of view, and also allows for an explicit analysis of the robust and model insensitivity properties of the resulting controls [\[9,](#page-41-5) [23\]](#page-42-12). In our problem θ is integrated into the choice of cost C.

#### 1.3 Notation

We now introduce some common notation that will be used throughout the article. For a locally compact Polish space S, the space of positive Borel measures on S is denoted by M(S). We use M<sup>f</sup> (S) and Mc(S) to denote the subspaces of M(S) consisting, respectively, of finite measures, and of measures that are finite on every compact subset. Letting Cc(S) denote the space of continuous functions with compact support, we equip Mc(S) with the weakest topology such that for every f ∈ Cc(S), the function ν → R S f dν, ν ∈ Mc(S), is continuous. Let B(S) be the Borel σ-algebra on S and P(S) the set of probability measures on (S,B(S)). Finally, for a second Polish space S ′ , we let

<span id="page-4-0"></span>
$$
\mathcal{F}(\mathcal{S}; \mathcal{S}') = \{ f : \mathcal{S} \to \mathcal{S}' : f \text{ measurable} \}
$$
\n(1.12)

denote the space of measurable functions from S to S ′ . For the finite set X and a > 0, let

<span id="page-4-1"></span>
$$
\mathcal{P}_*(\mathcal{X}) = \{ \mathbf{m} \in \mathcal{P}(\mathcal{X}) : m_x > 0 \text{ for all } x \in \mathcal{X} \} \text{ and } \mathcal{P}_a(\mathcal{X}) = \{ \mathbf{m} \in \mathcal{P}(\mathcal{X}) : m_x \ge a \text{ for all } x \in \mathcal{X} \}. \tag{1.13}
$$

For a set <sup>K</sup> ⊂ P(<sup>X</sup> ), the closure K, ¯ the complement <sup>K</sup><sup>c</sup> and the interior <sup>K</sup>◦ , will be considered with respect to the restriction of the Euclidean topology on the set P(X ). Let D([0,∞); S) denote the space of c`adl`ag functions on S, equipped with the Skorohod topology (see [\[4,](#page-41-6) Section 16]), i.e., the Skorohod space. This space is separable and complete [\[4,](#page-41-6) Theorem 16.3], and a set is relatively compact in D([0,∞); S), if and only if for every M < ∞, its natural projection on D([0, M]; S), is relatively compact [\[4,](#page-41-6) Theorem 16.4].

For <sup>M</sup>¯ <sup>=</sup> <sup>M</sup>c([0,∞) 2 ), let <sup>P</sup> be the probability measure on (M¯ ,B(M¯ )), under which the canonical map N(ω) = ω is a Poisson measure with intensity measure equal to Lebesgue measure on [0,∞) 2 . Let G<sup>t</sup> = σ{N((0, s] × A) : 0 ≤ s ≤ t, A ∈ B([0,∞))}, and let F<sup>t</sup> be the completion of G<sup>t</sup> under P. Let P be the corresponding predictable <sup>σ</sup>-field in [0,∞)×M¯ . For natural numbers k, k′ , we similarly define a measure P k,k′ on (M¯ <sup>k</sup> ′ ,B(M¯ <sup>k</sup> ′ )) under which the maps N<sup>k</sup> i (ω) = ω<sup>i</sup> , 1 ≤ i ≤ k ′ , are independent Poisson measures with intensity measure equal to k times the Lebesgue measure on [0,∞) 2 . {Gk,k′ t }, {Fk,k′ t }, and P k,k′ are defined analogously. Let <sup>A</sup> be the class of P \B([0,∞)) measurable maps <sup>φ</sup> : [0,∞)×M →¯ [0,∞), and <sup>A</sup><sup>b</sup> the subset of these maps that are uniformly bounded from below away from zero and above by a positive constant. Similarly we define <sup>A</sup>k,k′ to be the set of P k,k′ \ B([0,∞) k ′ ) measurable maps <sup>φ</sup> : [0,∞) <sup>×</sup> <sup>M</sup>¯ <sup>k</sup> ′ → [0,∞) k ′ , and A k,k′ b the subset of these maps for which each component is uniformly bounded from below and above by strictly positive constants.

## 2 Model Description

Throughout this section, fix n ∈ N, and let C and R be, respectively, the cost and reward functions introduced in Section [1.1.](#page-0-0)

#### 2.1 The many-agent control problem

For a subset K of X n , we define a risk-sensitive cost I n K : X <sup>n</sup> × A1,n|Z| <sup>b</sup> → [0,∞] that corresponds to the cost/reward up to the first time of hitting K as follows:

$$
\mathcal{I}_{\mathcal{K}}^n(\boldsymbol{x}^n,\boldsymbol{u}) := \mathbb{E}_{\boldsymbol{x}^n} \left[ \exp \left( \int_0^{T_{\mathcal{K}}} \left( \sum_{i=1}^n \sum_{y \in \mathcal{Z}_{\chi_i^n(t)}} \gamma_{\chi_i^n(t)y} C_{\chi_i^n(t)y} \left( \frac{u_{\chi_i^n(t)y}(t,i)}{\gamma_{\chi_i^n(t)y}} \right) - nR(L(\boldsymbol{\chi}^n(t))) \right) dt \right) \right], \quad (2.1)
$$

where Ex<sup>n</sup> denotes the expected value given χ n (0) = x n , {χ n (t), t ≥ 0} follows the dynamics given in [\(1.7\)](#page-2-0), and T<sup>K</sup> is the hitting time

<span id="page-5-0"></span>
$$
T_{\mathcal{K}} := \inf \left\{ t \in [0, \infty] : \chi^n(t) \in \mathcal{K} \right\}.
$$
\n
$$
(2.2)
$$

We define the value function <sup>W</sup><sup>n</sup> K : X <sup>n</sup> <sup>→</sup> [0,∞] by

<span id="page-5-1"></span>
$$
\mathcal{W}^n_{\mathcal{K}}(\boldsymbol{x}^n) := \inf_{\boldsymbol{u} \in \mathcal{A}_b^{1,n} \mid \mathcal{Z}|} \mathcal{I}^n_{\mathcal{K}}(\boldsymbol{x}^n, \boldsymbol{u}).
$$
\n(2.3)

Similarly, for a set K ⊂ X <sup>n</sup> we define the ordinary cost <sup>J</sup> n K : X <sup>n</sup> × A1,n|Z| <sup>b</sup> → [0,∞] and corresponding value function V n K : X <sup>n</sup> <sup>→</sup> [0,∞] by

$$
\mathcal{J}_{\mathcal{K}}^n(\boldsymbol{x}^n, \boldsymbol{q}) := \mathbb{E}_{\boldsymbol{x}^n} \left[ \int_0^{T_{\mathcal{K}}} \left( \frac{1}{n} \sum_{i=1}^n \sum_{y \in \mathcal{Z}_{\chi_i^n(t)}} F_{\chi_i^n(t)y}(q_{\chi_i^n(t)y}(t, i)) + R(L(\boldsymbol{\chi}^n(t))) \right) dt \right],
$$
\n(2.4)

where F = {Fxy}(x,y)∈Z} is defined in [\(1.8\)](#page-2-1), and

<span id="page-5-2"></span>
$$
\mathcal{V}_{\mathcal{K}}^n(\boldsymbol{x}^n) := \inf_{\boldsymbol{q} \in \mathcal{A}_b^{1,n} |\mathcal{Z}|} \mathcal{J}_{\mathcal{K}}^n(\boldsymbol{x}^n, \boldsymbol{q}),\tag{2.5}
$$

where the dynamics of {χ n (t), t ≥ 0} are now given by [\(1.7\)](#page-2-0) with u replaced by q, and the stopping time T<sup>K</sup> is, as earlier, given by [\(2.2\)](#page-5-0). We remark that the reason for two different notations for controls is to aid the reader, by associating one with the risk sensitive problem and one with the regular control problem. Moreover, there are occasions that both variables appear at the same time, as in the definition of F or that of the Hamiltonian. Specific conditions on the cost functions will be given in Section [3.1,](#page-6-0) and properties of F will be proved in Lemma [3.7.](#page-9-0) Note that for the many agent systems there are n|Z| PRMs, each with intensity 1

#### 2.2 The mean-field control problems

Suppose that we have some exchangeability in the sense that for every permutation σ of {1, 2, . . . , n}, σK = K. Then K can be identified with the subset

$$
K := \{ L(x^n) : x^n \in \mathcal{K} \},
$$

of the simplex of probability measures P(X ). Here, L is as defined in [\(1.6\)](#page-2-2). Then we can replace a control problem on X <sup>n</sup> by one on <sup>P</sup>(<sup>X</sup> ). In this case <sup>W</sup><sup>n</sup> K and V n K can be considered as functions on P n (X ), in the sense that we can find W<sup>n</sup> <sup>K</sup>, V <sup>n</sup> <sup>K</sup> : P n (<sup>X</sup> ) <sup>→</sup> [0,∞], such that <sup>W</sup><sup>n</sup> <sup>K</sup>(x n ) = W<sup>n</sup> <sup>K</sup>(L(x n )) and V n <sup>K</sup>(x n ) = V n <sup>K</sup>(L(x n )), where L is as defined in [\(1.6\)](#page-2-2). To see this, pick a starting point x <sup>n</sup> ∈ X <sup>n</sup> and some permutation <sup>σ</sup>. Then for any admissible control u, the total cost generated starting at x n is the same as that generated when starting from x n σ and picking u<sup>σ</sup> as the control. Therefore, for every x <sup>n</sup> ∈ X <sup>n</sup> , σ ∈ Sn, we have VK(x n ) = VK(x n σ ).

Define h n : D([0,∞);P n (<sup>X</sup> )) × An,|Z| <sup>b</sup> × P<sup>n</sup> (<sup>X</sup> ) <sup>×</sup> <sup>M</sup>¯ n,|Z| → D([0,∞); <sup>R</sup> d ) by

$$
h^n\left(\boldsymbol{\mu}, \boldsymbol{u}, \boldsymbol{m}, \frac{1}{n}\boldsymbol{N}^n\right)(t):=\boldsymbol{m}+\sum_{(x,y)\in\mathcal{Z}}\boldsymbol{v}_{xy}\int_{(0,t]}\int_{[0,\infty)}1_{[0,\mu_x(-s)u_{xy}(s)]}(r)\frac{1}{n}N^n_{xy}(dsdr).
$$

Since <sup>u</sup> ∈ An,|Z| b implies the rates uxy(s) are uniformly bounded, one can explicitly construct a unique D([0,∞);P n (X ))-valued process that satisfies

<span id="page-6-2"></span>
$$
\mu = h^n \left( \mu, \mathbf{u}, \mathbf{m}, \frac{1}{n} \mathbf{N}^n \right). \tag{2.6}
$$

[\[12\]](#page-42-13). Here µ is the controlled process, u is the control, m is an initial condition, and N<sup>n</sup> /n is scaled noise.

Now with T<sup>K</sup> := inf {t ∈ [0,∞] : µ(t) ∈ K}, the functions I n K, J<sup>n</sup> V : P n (<sup>X</sup> )×An,|Z| <sup>b</sup> <sup>→</sup> [0,∞] and <sup>W</sup><sup>n</sup> <sup>K</sup>, V <sup>n</sup> <sup>K</sup> : P n (X ) → [0,∞] are given by

$$
W_K^n(\boldsymbol{m}) := \inf_{\boldsymbol{u} \in \mathcal{A}_b^{n, |Z|}} I_K^n(\boldsymbol{m}, \boldsymbol{u}),\tag{2.7}
$$

where

$$
I_K^n(\boldsymbol{m},\boldsymbol{u}) := \mathbb{E}_{\boldsymbol{m}}\left[e^{n\int_0^{T_K}\left(\sum_{(x,y)\in\mathcal{Z}}\mu_x(t)\gamma_{xy}C_{xy}\left(\frac{u_{xy}(t)}{\gamma_{xy}}\right)-R(\mu(t))\right)dt}\cdot\boldsymbol{\mu} = h^n\left(\boldsymbol{\mu},\boldsymbol{u},\boldsymbol{m},\frac{1}{n}\boldsymbol{N}^n\right)\right],\tag{2.8}
$$

and

<span id="page-6-3"></span>
$$
V_K^n(\boldsymbol{m}) := \inf_{\boldsymbol{q} \in \mathcal{A}_b^{n, |\mathcal{Z}|}} J_K^n(\boldsymbol{m}, \boldsymbol{q}), \tag{2.9}
$$

where

$$
J_K^n(\boldsymbol{m}, \boldsymbol{q}) := \mathbb{E}_{\boldsymbol{m}} \left[ \int_0^{T_K} \left( \sum_{(x, y) \in \mathcal{Z}} \mu_x(t) F_{xy}(q_{xy}(t)) + R(\boldsymbol{\mu}(t)) \right) dt : \boldsymbol{\mu} = h^n \left( \boldsymbol{\mu}, \boldsymbol{q}, \boldsymbol{m}, \frac{1}{n} \mathbf{N}^n \right) \right].
$$
 (2.10)

For these control problems, there are |Z| PRMs, each with intensity n. In contrast, recall from the discussion prior to [\(1.7\)](#page-2-0) that the n-agent system dynamics are driven by n|Z| PRMS, each with intensity 1.

## 3 Equivalence of the control problems

In this section we prove that, after a natural renormalization, the value function <sup>W</sup><sup>n</sup> <sup>K</sup> defined in [\(2.3\)](#page-5-1) is linked to V n K defined in [\(2.5\)](#page-5-2) which, as noted before, is the value function of an ordinary stochastic control problem with a new cost function. Specifically, we show that <sup>−</sup> log(W<sup>n</sup> <sup>K</sup>)/n equals V n <sup>K</sup>, and that the many agent and the mean field control problem are equivalent when the exchangeability condition holds:

<span id="page-6-1"></span>
$$
-\frac{1}{n}\log(W_K^n(L(\boldsymbol{x}^n)))=V_K^n(L(\boldsymbol{x}^n))=\mathcal{V}_K^n(\boldsymbol{x}^n)=-\frac{1}{n}\log(\mathcal{W}_K^n(\boldsymbol{x}^n)).
$$
\n(3.1)

#### <span id="page-6-0"></span>3.1 The cost function

One of the aims of this paper is to identify cost structures that make sense for the problem formulation and for which the risk-sensitive problem is equivalent to a control problem (rather than a game). The only place where restrictions are needed are in the cost C paid by the centralized controller to the agents for deviating from the nominal rates γ. To see what conditions will be needed, we first discuss briefly the strategy to be used for the proof of [\(3.1\)](#page-6-1). The proof will use a related Bellman equation. Let H : P(X ) × R |Z| <sup>→</sup> <sup>R</sup> be given by

<span id="page-7-3"></span>
$$
H(\boldsymbol{m},\boldsymbol{\xi}) := \inf_{\boldsymbol{q}\in[0,\infty)^{|\mathcal{Z}|}}\left\{\sum_{(x,y)\in\mathcal{Z}}m_x\left(q_{xy}\xi_{xy} + F_{xy}(q_{xy})\right)\right\},\tag{3.2}
$$

where

<span id="page-7-4"></span>
$$
F_{xy}(q) := \sup_{u \in (0,\infty)} G_{xy}(u,q) \quad \text{and} \quad G_{xy}(u,q) := \left[ u\ell\left(\frac{q}{u}\right) - \gamma_{xy}C_{xy}\left(\frac{u}{\gamma_{xy}}\right) \right]. \tag{3.3}
$$

Consider the equation

<span id="page-7-0"></span>
$$
H(m, \Delta^n V(m)) + R(m) = 0 \text{ in } \mathcal{P}^n(\mathcal{X}) \setminus K,
$$
\n(3.4)

where ∆n<sup>V</sup> (m) denotes the |Z|-dimensional vector <sup>n</sup> V (m + vxy n ) − V (m) , and ∆<sup>n</sup> xyV (m) is the component n V (m + vxy n ) − V (m) xy , (x, y) ∈ Z. We will show that V n <sup>K</sup> is the unique solution V to [\(3.4\)](#page-7-0) that satisfies the boundary condition <sup>V</sup> (m) = 0 for <sup>m</sup> <sup>∈</sup> <sup>K</sup>. We will also prove that <sup>W</sup><sup>n</sup> <sup>K</sup> is the unique solution to the equation

<span id="page-7-1"></span>
$$
\sup_{\mathbf{u}\in(0,\infty)^{|\mathcal{Z}|}}\left\{\sum_{(x,y)\in\mathcal{Z}}m_x\left(u_{xy}\left(\frac{W(\mathbf{m})-W(\mathbf{m}+\frac{\mathbf{v}_{xy}}{n})}{W(\mathbf{m})}\right)-\gamma_{xy}C_{xy}\left(\frac{u_{xy}}{\gamma_{xy}}\right)\right)\right\}=-R(\mathbf{m})\tag{3.5}
$$

for <sup>m</sup> ∈ P<sup>n</sup> (X ) \ K with boundary condition W(m) = 1 for m ∈ K.

In the proof of the relation − 1 n log(W<sup>n</sup> <sup>K</sup>) = V n <sup>K</sup>, we will use the following lemma, which holds under suitable conditions on the cost functional specified in Assumption [3.2](#page-8-0) below. The proof of the lemma is given in Section [3.2](#page-9-1) (right after Lemma [3.9\)](#page-10-0).

<span id="page-7-2"></span>Lemma 3.1 Suppose Assumption [3.2](#page-8-0) below holds. Then, if <sup>V</sup>˜ : <sup>P</sup> n (X ) → [0,∞) is a solution to [\(3.4\)](#page-7-0) and <sup>V</sup>˜ (m) = 0 for <sup>m</sup> <sup>∈</sup> <sup>K</sup>, then <sup>W</sup>˜ <sup>=</sup> <sup>e</sup> −nV˜ : P n (<sup>X</sup> ) <sup>→</sup> (0,∞) is a solution of [\(3.5\)](#page-7-1) and <sup>W</sup>˜ (m) = 1 for <sup>m</sup> <sup>∈</sup> K.

We now provide an outline of the proof of Lemma [3.1](#page-7-2) and also provide motivation for the form of our main assumption, Assumption [3.2](#page-8-0) below, on the cost function. First, note that by [\(3.2\)](#page-7-3)-[\(3.3\)](#page-7-4), we have

$$
H(\mathbf{m}, \boldsymbol{\xi}) := \inf_{\boldsymbol{q} \in [0,\infty)^{|\mathcal{Z}|}} \left\{ \sum_{(x,y) \in \mathcal{Z}} m_x (q_{xy} \xi_{xy} + F_{xy}(q_{xy})) \right\}
$$
  
\n
$$
= \inf_{\boldsymbol{q} \in [0,\infty)^{|\mathcal{Z}|}} \sup_{\boldsymbol{u} \in (0,\infty)^{|\mathcal{Z}|}} \left\{ \sum_{(x,y) \in \mathcal{Z}} m_x (q_{xy} \xi_{xy} + G_{xy}(u_{xy}, q_{xy})) \right\}
$$
(3.6)  
\n
$$
= \inf_{\boldsymbol{q} \in [0,\infty)^{|\mathcal{Z}|}} \sup_{\boldsymbol{u} \in (0,\infty)^{|\mathcal{Z}|}} \left\{ \sum_{(x,y) \in \mathcal{Z}} m_x L_{xy}(u_{xy}, q_{xy}) \right\},
$$

.

<span id="page-7-5"></span>where, Lxy is defined, in terms of ξxy, γxy, Cxy, Lxy and the function ℓ defined in [\(1.9\)](#page-2-3), as

$$
L_{xy}(u,q) := q\xi_{xy} + u\ell\left(\frac{q}{u}\right) - \gamma_{xy}C_{xy}\left(\frac{u}{\gamma_{xy}}\right)
$$

The proof of Lemma [3.1](#page-7-2) will proceed by first showing that Isaac's condition holds, that is, that the supremum and infimum in [\(3.6\)](#page-7-5) can be exchanged:

<span id="page-8-1"></span>
$$
\inf_{\mathbf{q}\in[0,\infty)^{|\mathcal{Z}|}}\sup_{\mathbf{u}\in(0,\infty)^{|\mathcal{Z}|}}\left\{\sum_{(x,y)\in\mathcal{Z}}m_{x}L_{xy}(u_{xy},q_{xy})\right\}=\sup_{\mathbf{u}\in(0,\infty)^{|\mathcal{Z}|}}\inf_{\mathbf{q}\in[0,\infty)^{|\mathcal{Z}|}}\left\{\sum_{(x,y)\in\mathcal{Z}}m_{x}L_{xy}(u_{xy},q_{xy})\right\}.\tag{3.7}
$$

Equation [\(3.7\)](#page-8-1) is clearly equivalent to

<span id="page-8-3"></span>
$$
\inf_{q_{xy}\in[0,\infty)} \sup_{u_{xy}\in(0,\infty)} L_{xy}(u_{xy}, q_{xy}) = \sup_{u_{xy}\in(0,\infty)} \inf_{q_{xy}\in[0,\infty)} L_{xy}(u_{xy}, q_{xy}), \quad \forall (x, y) \in \mathcal{Z}.
$$
 (3.8)

<span id="page-8-0"></span>We show in Lemma [3.4](#page-8-2) below that [\(3.8\)](#page-8-3) holds under the following main assumption on the cost function.

<span id="page-8-4"></span>Assumption 3.2 R : P(X ) → [0,∞) is a continuous function. Moreover, for every (x, y) ∈ Z, Cxy : [0,∞) → [0,∞] is a convex function that satisfies the following:

<span id="page-8-5"></span>1. uC′ xy (u) − u is increasing on the maximal open interval where Cxy is finite;

2. 
$$
C_{xy}(1) = 0
$$
.

<span id="page-8-9"></span>The following result, which is proved in Appendix [A,](#page-36-0) shows that part [1](#page-8-4) of Assumption [3.2](#page-8-0) is close to being necessary for [\(3.7\)](#page-8-1) to hold.

Theorem 3.3 If [\(3.7\)](#page-8-1) is satisfied and for each (x, y) ∈ Z, Cxy is twice differentiable on some non-empty interval (u1,xy, u2,xy), then part [1](#page-8-4) of Assumption [3.2](#page-8-0) is satisfied on that interval.

Part [2](#page-8-5) of Assumption [3.2](#page-8-0) is not necessary, but it simplifies the analysis, and it is appropriate for the situation being modeled to have zero cost when there is no change from the nominal rates. The proof of Lemma [3.4,](#page-8-2) which relies on (a modification of) Sion's theorem (Corollary 3.3 in [\[25\]](#page-42-14)), is also deferred to Appendix [A.](#page-36-0) We proceed by providing a concrete example of a family of cost functions that satisfy Assumption [3.2.](#page-8-0)

<span id="page-8-8"></span>Example 3.1 The family of functions Cxy(u) = <sup>1</sup> pu<sup>p</sup> + u q q − p+q pq , where p ≥ 1 and q ≥ 1, satisfy Assumption [3.2.](#page-8-0) Clearly, <sup>C</sup>xy(1) = 0. The derivative of <sup>C</sup>xy is <sup>−</sup> <sup>1</sup> <sup>u</sup>p+1 + u q−1 , and so uC′ xy(u) <sup>−</sup> <sup>u</sup> <sup>=</sup> <sup>−</sup> <sup>1</sup> <sup>u</sup><sup>p</sup> + u <sup>q</sup> <sup>−</sup> u, which is always finite. Taking the derivative again gives <sup>p</sup> <sup>u</sup>p+1 <sup>+</sup> quq−<sup>1</sup> <sup>−</sup> <sup>1</sup>, which is always bigger than zero, since p <sup>u</sup>p+1 and quq−<sup>1</sup> are everywhere positive and bigger than one on the intervals [0, 1] and [1,∞), respectively.

<span id="page-8-2"></span>Lemma 3.4 Under Assumption [3.2,](#page-8-0) the relation [\(3.8\)](#page-8-3) holds for each (x, y) ∈ Z, and hence, the Isaac's condition stated in [\(3.7\)](#page-8-1), is satisfied.

<span id="page-8-6"></span>As an immediate corollary of the lemma, we have the following result:

Corollary 3.5 Under Assumption [3.2,](#page-8-0) for each m ∈ P(X ) and ξ ∈ R |Z| ,

$$
H(\mathbf{m}, \boldsymbol{\xi}) = \sum_{(x,y) \in \mathcal{Z}} m_x \gamma_{xy} (C_{xy})^* \left( 1 - e^{-\xi_{xy}} \right).
$$

where (Cxy) ∗ : (−∞, 1) → R is given by

<span id="page-8-7"></span>
$$
(C_{xy})^*(z) := \sup_{u>0} [zu - C_{xy}(u)]. \qquad (3.9)
$$

Proof. First, note that for each (x, y) ∈ Z, using the fact that ∂qLxy(u, q) = ξxy + log(q/u), and ∂qqLxy(u, q) > 0 for q > 0, we see that

$$
\inf_{q_{xy}\in[0,\infty)} L_{xy}(u_{xy}, q_{xy}) = u_{xy}(1 - e^{-\xi_{xy}}) - \gamma_{xy}C_{xy}\left(\frac{u_{xy}}{\gamma_{xy}}\right).
$$
\n(3.10)

Also note that, by the definition of (Cxy) ∗ ,

$$
\sup_{u_{xy}\in(0,\infty)} \left[ u_{xy}(1 - e^{-\xi_{xy}}) - \gamma_{xy} C_{xy} \left( \frac{u_{xy}}{\gamma_{xy}} \right) \right] = \gamma_{xy} (C_{xy})^*(1 - e^{-\xi_{xy}}). \tag{3.11}
$$

<span id="page-9-3"></span>The corollary is then a simple consequence of the above two observations, [\(3.6\)](#page-7-5) and Lemma [3.4.](#page-8-2)

We now summarize some other properties of the cost function that will be useful in the sequel.

Lemma 3.6 Under Assumption [3.2,](#page-8-0) the cost function Cxy satisfy the following on (0,∞):

- 1. for every (x, y) ∈ Z we have (Cxy) ′ (u) ≥ 1 − 1 u for u > 1, and therefore lim infu→∞(Cxy) ′ (u) ≥ 1,
- 2. for every (x, y) ∈ Z and u ∈ (0,∞) we have Cxy(u) ≥ − log u + u − 1.

Proof. It follows from the monotonicity that uC′ xy(u) − u ≥ −1 for u > 1, which gives the first statement. The second follows by comparing Cxy(u) with R <sup>u</sup> 1 -1 − 1 s ds and using Cxy(1) = 0.

<span id="page-9-0"></span>We conclude with a lemma that collects some properties of Fxy, and whose proof is provided in Appendix [B.](#page-38-0)

Lemma 3.7 For every (x, y) ∈ Z, let Fxy be as in [\(1.8\)](#page-2-1), where {Cxy} satisfy Assumption [3.2.](#page-8-0) Then the following properties hold:

$$
1. F_{xy}(q) \ge \gamma_{xy} \ell\left(\frac{q}{\gamma_{xy}}\right) \ge 0, \quad 2. F_{xy}(\gamma_{xy}) = 0, \quad 3. F_{xy} \text{ is convex on } [0, \infty).
$$

#### <span id="page-9-2"></span><span id="page-9-1"></span>3.2 Equivalence of the stochastic problems

Theorem 3.8 Let <sup>n</sup> <sup>∈</sup> <sup>N</sup>, K ⊂ X <sup>n</sup> , (resp. <sup>K</sup> ⊂ P<sup>n</sup> (X )), and C, R be as in Assumption [3.2.](#page-8-0) Then

$$
V_K^n(\boldsymbol{m}) = -\frac{1}{n}\log(W_K^n(\boldsymbol{m}))\tag{3.12}
$$

and

$$
\mathcal{V}_{\mathcal{K}}^n(\boldsymbol{x}^n) = -\frac{1}{n} \log(\mathcal{W}_{\mathcal{K}}^n(\boldsymbol{x}^n)).
$$
\n(3.13)

If, in addition, K ⊂ X <sup>n</sup> is invariant under permutations, and therefore can be identified with a subset of P n (X ), then

$$
-\frac{1}{n}\log(W_K^n(L(\mathbf{x}^n))) = V_K^n(L(\mathbf{x}^n)) = \mathcal{V}_K^n(\mathbf{x}^n) = -\frac{1}{n}\log(\mathcal{W}_K^n(\mathbf{x}^n)).
$$
\n(3.14)

<span id="page-10-0"></span>The proof of this result appears later in this section. Also, we will only prove the first equality and note that the third follows in a similar manner. We begin with some preparatory lemmas.

Lemma 3.9 Let <sup>n</sup> <sup>∈</sup> <sup>N</sup>, ∅ 6<sup>=</sup> <sup>K</sup> ⊂ P<sup>n</sup> (X ), and C, R be as in Assumption [3.2.](#page-8-0) Then, the equation [\(3.4\)](#page-7-0) has at least one solution.

Proof. For the proof we use the equivalent discrete time stochastic control problem. We consider the following set of controls

$$
A_a(\boldsymbol{m}) := \left\{ \boldsymbol{q} \in [0,\infty)^{|\mathcal{Z}|} : \frac{1}{a} \ge \sum_{(x,y) \in \mathcal{Z}} m_x q_{xy}(\boldsymbol{m}) \ge a \right\} \text{ and } A_{+}(\boldsymbol{m}) := \cup_{a > 0} A_a(\boldsymbol{m}). \tag{3.15}
$$

For such a control the probability of moving from state m to state m + 1 n vx, ˜ <sup>y</sup>˜ will be given by

$$
\frac{m_{\tilde{\pmb{x}}}q_{\tilde{\pmb{x}}\tilde{\pmb{y}}}(\pmb{m})}{\sum_{(\pmb{x},\pmb{y})\in\mathcal{Z}}m_{\pmb{x}}q_{\pmb{x}\pmb{y}}(\pmb{m})},
$$

and the (conditional) expected cost till the time of transition is given by

$$
\frac{\sum_{(x,y)\in \mathcal{Z}}m_{x}F_{xy}(q_{xy}(\boldsymbol m)) + R(\boldsymbol m)}{n\sum_{(x,y)\in \mathcal{Z}}m_{x}q_{xy}(\boldsymbol m)}
$$

Also, with some abuse of notation, we define the set of feedback controls

$$
A_a = \{ \mathbf{q} \in [0, \infty)^{|\mathcal{P}^n(\mathcal{X}) \times \mathcal{Z}|} : \mathbf{q}(m) \in A_a(m) \} \text{ and } A_+ = \cup_{a>0} A_a.
$$
 (3.16)

.

Given controlled transition probabilities as above, let µ(i) be the corresponding controlled discrete time process. We define the value function V¯ <sup>n</sup> <sup>K</sup>(m) : P(R d ) → [0,∞) by

<span id="page-10-1"></span>
$$
\bar{V}_K^n(\boldsymbol{m}) := \inf_{\boldsymbol{q} \in A_+} \mathbb{E}_{\boldsymbol{m}} \left[ \sum_{i=1}^{T_K} \frac{\sum_{(x,y) \in \mathcal{Z}} \mu_x(i) F_{xy}(q_{xy}(\boldsymbol{\mu}(i))) + R(\boldsymbol{\mu}(i))}{n \sum_{(x,y) \in \mathcal{Z}} \mu_x(i) q_{xy}(\boldsymbol{\mu}(i))} \right],
$$
\n(3.17)

where E<sup>m</sup> denotes expected value given µ(0) = m and T<sup>K</sup> := inf{i ∈ N : µ(i) ∈ K}.

To see that V¯ <sup>n</sup> <sup>K</sup>(m) is finite, we just have to use the original rates and note that the total cost is proportional to the expected exit time, which is finite by classical results on Markov chains. Since Fxy, R ≥ 0, and Fxy is convex with γxyℓ · <sup>γ</sup>xy as a lower bound (see Lemma [3.7\)](#page-9-0), one can see that we can find a constant a<sup>0</sup> > 0 such that only controls in Aa<sup>0</sup> (or any a < a0) should be considered. More specifically to see that a term in the sum appearing on the RHS of [\(3.17\)](#page-10-1) gets large when P (x,y)∈Z µx(i)qxy(µ(i)) gets small we bound the denominator by |Z| times the biggest term and the nominator by the same term and then we use the fact that Fxy(0) ≥ γxy. For the other bound we use the superlinearity of Fxy. Now by [\[3,](#page-41-7) Proposition 1.1 in Chapter 3], we have that this value function satisfies

$$
\bar{V}_K^n(\boldsymbol{m}) = \inf_{\boldsymbol{q} \in A_{a_0}(\boldsymbol{m})} \left\{ \frac{\sum_{(x,y) \in \mathcal{Z}} m_x F_{xy}(q_{xy}) + R(\boldsymbol{m})}{n \sum_{(x,y) \in \mathcal{Z}} m_x q_{xy}} + \sum_{(\tilde{x}, \tilde{y}) \in \mathcal{Z}} \frac{m_{\tilde{x}} q_{\tilde{x}\tilde{y}}}{\sum_{(x,y) \in \mathcal{Z}} m_x q_{xy}} \bar{V}_K^n \left( \boldsymbol{m} + \frac{1}{n} \boldsymbol{v}_{\tilde{x}\tilde{y}} \right) \right\}.
$$

It then follows that V¯ <sup>n</sup> K(m) satisfies the last display if and only if [with ∆<sup>n</sup> xyV¯ <sup>n</sup> <sup>K</sup>(m) := n V¯ <sup>n</sup> <sup>K</sup>(m + vxy n ) <sup>−</sup> <sup>V</sup>¯ <sup>n</sup> <sup>K</sup>(m) ]

$$
\inf_{\boldsymbol{q}\in A_{a_0}(\boldsymbol{m})}\left\{\sum_{(x,y)\in\mathcal{Z}}m_x\left(q_{xy}\Delta_{xy}^n\bar{V}_K^n(\boldsymbol{m})+F_{xy}(q_{xy})\right)\right\}+R(\boldsymbol{m})=0.
$$

Since a<sup>0</sup> can be chosen arbitrary small and the left side on the previous display is continuous with respect to q, we get

$$
\inf_{\boldsymbol{q}\in[0,\infty)^{|\mathcal{Z}|}}\left\{\sum_{(x,y)\in\mathcal{Z}}m_x\left(q_{xy}\Delta_{xy}^n\bar{V}_K^n(\boldsymbol{m})+F_{xy}(q_{xy})\right)\right\}+R(\boldsymbol{m})=0.
$$

Then using the definition [\(3.2\)](#page-7-3) this is the same as

$$
H^n\left(\mathbf{m}, \Delta^n \bar{V}_K^n(\mathbf{m})\right) + R(\mathbf{m}) = 0,
$$

and we also have the boundary condition V¯ <sup>n</sup> <sup>K</sup>(m) = 0 for all m ∈ K.

Proof of Lemma [3.1.](#page-7-2) Let V˜ be a solution to [\(3.4\)](#page-7-0). We then have H<sup>n</sup> (m, ∆nV˜ (m)) + R(m) = 0. Using Corollary [3.5](#page-8-6) and the definition [\(3.9\)](#page-8-7) of C ∗ , this implies

$$
\sup_{\mathbf{u}\in(0,\infty)^{|\mathcal{Z}|}}\left\{\sum_{(x,y)\in\mathcal{Z}}m_x\left(u_{xy}\left(1-e^{-n(\tilde{V}(m+\frac{vxy}{n})-\tilde{V}(m))}\right)-\gamma_{xy}C_{xy}\left(\frac{u_{xy}}{\gamma_{xy}}\right)\right)\right\}+R(m)=0.
$$

By making the substitution W˜ = e −nV˜ , we have

$$
\sup_{\boldsymbol{u}\in(0,\infty)^{|\mathcal{Z}|}}\left\{\sum_{(x,y)\in\mathcal{Z}}m_x\left(u_{xy}\left(1-\frac{\tilde{W}(\boldsymbol{m}+\frac{\boldsymbol{v}_{xy}}{n})}{\tilde{W}(\boldsymbol{m})}\right)-\gamma_{xy}C_{xy}\left(\frac{u_{xy}}{\gamma_{xy}}\right)\right)\right\}+R(\boldsymbol{m})=0,
$$

<span id="page-11-1"></span>which is the same as [\(3.5\)](#page-7-1).

Lemma 3.10 Let f : P n (<sup>X</sup> ) <sup>→</sup> <sup>R</sup>, <sup>m</sup> ∈ P<sup>n</sup> (<sup>X</sup> ), and <sup>q</sup> ∈ An,|Z| b be given, and let µ solve [\(2.6\)](#page-6-2). Then

$$
f(\boldsymbol{\mu}(t\wedge T_K)) - f(\boldsymbol{\mu}(t'\wedge T_K)) - \int_{t'\wedge T_K}^{t\wedge T_K} \sum_{(x,y)\in\mathcal{Z}} \mu_x(s) q_{xy}(s) \Delta_{xy}^n f(\boldsymbol{\mu}(s)) ds,
$$

is a martingale with respect to the filtration {Ft}.

<span id="page-11-0"></span>This is a classical result, and the proof entails a suitable application of Ito's formula (see [\[19,](#page-42-15) Chapter 2, Theorem 5.1] for more details).

Lemma 3.11 Let g : P n (<sup>X</sup> ) <sup>→</sup> (0,∞), <sup>m</sup> ∈ P<sup>n</sup> (<sup>X</sup> ), and <sup>u</sup> ∈ An,|Z| b be given, and let µ solve [\(2.6\)](#page-6-2). Then

$$
\frac{g(\boldsymbol{\mu}(t \wedge T_K))}{g(\boldsymbol{\mu}(t' \wedge T_K))} \exp \left\{-\int_{t' \wedge T_K}^{t \wedge T_K} \sum_{(x,y) \in \mathcal{Z}} \mu_x(s) u_{xy}(s) \frac{\Delta_{xy}^n g(\boldsymbol{\mu}(s))}{g(\boldsymbol{\mu}(s))} ds\right\}
$$
(3.18)

is a martingale with respect to the filtration F<sup>t</sup> . <span id="page-12-1"></span>Proof. The proof is a direct application of the corollary in [\[22,](#page-42-16) Page 66].

Lemma 3.12 Let <sup>m</sup> ∈ P<sup>n</sup> (<sup>X</sup> ) and <sup>u</sup> ∈ An,|Z| b . There exists a constant c > 0, that depends only on the bounds on <sup>u</sup>, the dimension <sup>d</sup>, the constant <sup>R</sup>max = max{R(m) : <sup>m</sup> ∈ P<sup>n</sup> (X )}, and the number n of agents, such that for every t ≥ t ′ <sup>≥</sup> <sup>0</sup>,

$$
\mathbb{E}_{m}\left[e^{-nR_{\max}(t\wedge T_K - t'\wedge T_K)}\Big|\mathcal{F}_{t'}\right] \geq c.
$$

Furthermore it is true that

$$
T_K < \infty \text{ a.s., and } \mathbb{E}_{m} \left[ e^{-nR_{\max}(T_K - t' \wedge T_K)} \Big| \mathcal{F}_{t'} \right] \geq c.
$$

Proof. We claim there exists g such that for all s

<span id="page-12-0"></span>
$$
\sum_{(x,y)\in\mathcal{Z}}\mu_x(s)u_{xy}(s)\frac{\Delta_{xy}^n g(\mu(s))}{g(\mu(s))}\geq nR_{\max}.\tag{3.19}
$$

To show the existence of such a g we use the following procedure. Since the one agent process with generator given in [\(1.1\)](#page-0-1) is ergodic, we have that the process on X n , with generator given in [\(1.2\)](#page-1-0), as well as the one on P n (X ), with generator given in [\(1.4\)](#page-1-1), are also ergodic. We split P n (X ) into sets {Ki}0≤i≤imax , where K<sup>0</sup> = K, and Ki+1 is generated inductively as the set of all points in P n (X ) that do not belong to K<sup>i</sup> but such that the process with generator [\(1.4\)](#page-1-1) can reach K<sup>i</sup> in one jump. Since the original process has d states, it is easy to see that imax ≤ d n . Since <sup>u</sup> ∈ An,|Z| b , there exist constants 0 < c<sup>1</sup> ≤ c<sup>2</sup> < ∞ such that c<sup>1</sup> ≤ uxy(t) ≤ c<sup>2</sup> for all t ≥ 0 a.s. Let g be defined by

$$
g(\boldsymbol{m}) \doteq \left(\frac{nR_{\max}+nd^2c_2+c_1}{c_1}\right)^{i_{\max}-i}, \text{ for } \boldsymbol{m} \in K_i.
$$

Let µ(·) be the process with control u. For 0 ≤ s ≤ t suppose that µ(s) ∈ K<sup>i</sup> for some i ≥ 1. Then there exists at least one (˜x, <sup>y</sup>˜) ∈ Z such that <sup>µ</sup>(s) + <sup>v</sup>x˜y˜ n ∈ Ki−1. Therefore

$$
\sum_{(x,y)\in\mathcal{Z}}\mu_x(s)u_{xy}(s)\frac{\Delta_{xy}^n g(\mu(s))}{g(\mu(s))} = \mu_{\tilde{x}}(s)u_{\tilde{x}\tilde{y}}(s)\frac{\Delta_{\tilde{x}\tilde{y}}^n g(\mu(s))}{g(\mu(s))} + n \sum_{(x,y)\in\mathcal{Z},(x,y)\neq(\tilde{x},\tilde{y})}\frac{g(\mu(s)+\frac{v_{xy}}{n})}{g(\mu(s))}\mu_x(s)u_{xy}(s)
$$
\n
$$
-n \sum_{(x,y)\in\mathcal{Z},(x,y)\neq(\tilde{x},\tilde{y})}\frac{g(\mu(s))}{g(\mu(s))}\mu_x(s)u_{xy}(s) \geq \mu_{\tilde{x}}(s)u_{\tilde{x}\tilde{y}}(s)\frac{\Delta_{\tilde{x}\tilde{y}}^n g(\mu(s))}{g(\mu(s))} - n \sum_{(x,y)\in\mathcal{Z}}\mu_x(s)u_{xy}(s)
$$
\n
$$
\geq c_1 \left(\frac{nR_{\max}+nd^2c_2+c_1}{c_1}-1\right) - nc_2d^2 \geq nR_{\max},
$$

where in the next to last inequality we used the fact that µx˜(s) ≥ 1 n (because otherwise there is no agent at x˜ to move), and that ∆<sup>n</sup> xyV (m) = n V (m + vxy n ) − V (m) .

Using Lemma [3.11,](#page-11-0) we have

$$
\mathbb{E}_{\boldsymbol{m}}\left[\frac{g(\boldsymbol{\mu}(t\wedge T_K))}{g(\boldsymbol{\mu}(t'\wedge T_K))}\exp\left\{-\int_{t'\wedge T_K}^{t\wedge T_K}\sum_{(x,y)\in\mathcal{Z}}\mu_x(s)u_{xy}(s)\frac{\Delta^n_{xy}g(\boldsymbol{\mu}(s))}{g(\boldsymbol{\mu}(s))}ds\right\}\bigg|\mathcal{F}_{t'}\right]=1,
$$

from which we get

$$
\mathbb{E}_{\boldsymbol{m}}\left[\exp\left\{-\int_{t'\wedge T_K}^{t\wedge T_K}\sum_{(x,y)\in\mathcal{Z}}\mu_x(s)u_{xy}(s)\frac{\Delta^n_{xy}g(\boldsymbol{\mu}(s))}{g(\boldsymbol{\mu}(s))}ds\right\}\bigg|\mathcal{F}_{t'}\right]\geq c\doteq\frac{\min_{\mathcal{P}^n(\mathcal{X})}g}{\max_{\mathcal{P}^n(\mathcal{X})}g}.
$$

By applying equation [\(3.19\)](#page-12-0)

$$
\mathbb{E}_{m}\left[e^{-nR_{\max}(t\wedge T_K - t'\wedge T_K)}\Big|\mathcal{F}_{t'}\right] \geq c.
$$

Now choose now τ > 0 such that e <sup>−</sup>nRmax<sup>τ</sup> <sup>≤</sup> c/2. We claim that

$$
(T_K \le t' + \tau) \Leftrightarrow (T_K \wedge (t' + 2\tau) - t' \wedge T_K) \le \tau.
$$

Indeed if t ′ <sup>≥</sup> <sup>T</sup>K, then both parts are trivially true. Let assume that <sup>t</sup> ′ <sup>≤</sup> <sup>T</sup>K, and <sup>T</sup><sup>K</sup> <sup>≤</sup> <sup>t</sup> ′ + τ. Then T<sup>K</sup> ∧ (t ′ + 2τ ) = TK, and t ′ <sup>∧</sup> <sup>T</sup><sup>K</sup> <sup>=</sup> <sup>t</sup> ′ , and therefore (T<sup>K</sup> ∧ (t ′ + 2<sup>τ</sup> ) <sup>−</sup> <sup>t</sup> ′ <sup>∧</sup> <sup>T</sup>K) = <sup>T</sup><sup>K</sup> <sup>−</sup> <sup>t</sup> ′ <sup>≤</sup> τ. If on the other hand t ′ <sup>≤</sup> <sup>T</sup><sup>K</sup> and (T<sup>K</sup> <sup>∧</sup> (<sup>t</sup> ′ + 2<sup>τ</sup> ) <sup>−</sup> <sup>t</sup> ′ <sup>∧</sup> <sup>T</sup>K) <sup>≤</sup> τ, we get (T<sup>K</sup> <sup>∧</sup> (<sup>t</sup> ′ + 2<sup>τ</sup> )) <sup>≤</sup> <sup>τ</sup> <sup>+</sup> <sup>t</sup> ′ , which gives that T<sup>K</sup> ≤ (t ′ + 2<sup>τ</sup> ), and therefore <sup>T</sup><sup>K</sup> = (T<sup>K</sup> <sup>∧</sup> (<sup>t</sup> ′ + 2<sup>τ</sup> )) <sup>≤</sup> <sup>t</sup> ′ + τ . Using the claim just proved gives

$$
\mathbb{P}_{m}(T_{K} \leq t' + \tau | \mathcal{F}_{t'}) = \mathbb{P}_{m}(T_{K} \wedge (t' + 2\tau) - t' \wedge T_{K} \leq \tau | \mathcal{F}_{t'}) = \mathbb{P}_{m}\left(e^{-nR_{\max}(T_{K} \wedge (t' + 2\tau) - t' \wedge T_{K})} \geq e^{-nR_{\max}\tau} | \mathcal{F}_{t'}\right).
$$

Let E<sup>1</sup> .<sup>=</sup> {<sup>e</sup> −nRmax(TK∧(t ′+2τ)−t ′∧TK) <sup>≥</sup> <sup>e</sup> <sup>−</sup>nRmax<sup>τ</sup> } and <sup>E</sup><sup>2</sup> .<sup>=</sup> <sup>E</sup><sup>c</sup> 1 . Then since T<sup>K</sup> ∧ (t ′ + 2<sup>τ</sup> ) <sup>−</sup> <sup>t</sup> ′ <sup>∧</sup> <sup>T</sup><sup>K</sup> <sup>≥</sup> <sup>0</sup>

$$
\mathbb{E}_{\boldsymbol{m}}\left[e^{-nR_{\max}(T_K\wedge(t'+2\tau)-t'\wedge T_K)}\Big|\mathcal{F}_{t'}\right] = \mathbb{E}_{\boldsymbol{m}}\left[1_{E_1}e^{-nR_{\max}^n(T_K\wedge(t'+2\tau)-t'\wedge T_K)}\Big|\mathcal{F}_{t'}\right] \n+ \mathbb{E}_{\boldsymbol{m}}\left[1_{E_2}e^{-nR_{\max}^n(T_K\wedge(t'+2\tau)-t'\wedge T_K)}\Big|\mathcal{F}_{t'}\right] \leq \mathbb{E}_{\boldsymbol{m}}\left[1_{E_1}\Big|\mathcal{F}_{t'}\right] + e^{-R_{\max}\tau}.
$$

From this, the first part of the lemma and e <sup>−</sup>nRmax<sup>τ</sup> <sup>≤</sup> c/2, we get

$$
\mathbb{P}_{m}\left(e^{-nR_{\max}(T_{K}\wedge(t'+2\tau)-t'\wedge T_{K})}\geq e^{-nR_{\max}^{n}\tau}|\mathcal{F}_{t'}\right)\geq \mathbb{E}_{m}\left[e^{-nR_{\max}(T_{K}\wedge(t'+2\tau)-t'\wedge T_{K})}\Big|\mathcal{F}_{t'}\right]-e^{-nR_{\max}\tau}\geq \frac{c}{2}.
$$

Now we have

$$
\mathbb{P}_{\mathbf{m}}(T_K = \infty) = \lim_{k \to \infty} \mathbb{P}_{\mathbf{m}}(T_K > k\tau) = \mathbb{P}_{\mathbf{m}}(T_K > 0) \lim_{k \to \infty} \prod_{k'=0}^k \left(1 - \mathbb{P}_{\mathbf{m}}\left(T_K \leq (k'+1)\tau \,|\, T_K > k'\tau\right)\right)
$$
  
\$\leq \lim\_{k \to \infty} \left(1 - \frac{c}{2}\right)^k = 0\$,

<span id="page-13-0"></span>where in the second inequality we iteratively used the formula for conditional probability. The remaining inequality is just an application of the monotone convergence theorem.

Lemma 3.13 Given <sup>m</sup> ∈ P<sup>n</sup> (<sup>X</sup> ), ǫ > <sup>0</sup> and <sup>u</sup> ∈ An,|Z| <sup>b</sup> with

$$
\mathbb{E}_{\boldsymbol{m}}\left[e^{n\int_0^{T_K}\left(\sum_{(x,y)\in\mathcal{Z}}\mu_x(t)C_{xy}\left(\frac{u_{xy}(t)}{\gamma xy}\right)-R(\mu(t))\right)dt}\right]<\infty,
$$

there exists <sup>u</sup>˜ ∈ An,|Z| b and τ < ∞, such that

$$
\sum_{(x,y)\in\mathcal{Z}}\tilde{\mu}_x(t)\gamma_{xy}C_{xy}\left(\frac{\tilde{u}_{xy}(t)}{\gamma_{xy}}\right)-R(\tilde{\mu}(t))\leq 0\ \ \text{for every}\ \ t>\tau,\quad\ \text{and}\quad\ I_K^n(\boldsymbol{m},\tilde{\boldsymbol{u}})\leq I_K^n(\boldsymbol{m},\boldsymbol{u})+\epsilon.
$$

Proof. Let such <sup>m</sup> ∈ P<sup>n</sup> (<sup>X</sup> ), ǫ > <sup>0</sup>, and <sup>u</sup> ∈ An,|Z| b be given, and let c > 0 from Lemma [3.12](#page-12-1) be such that

<span id="page-14-0"></span>
$$
\mathbb{E}_{m} \left[ e^{nR_{\max}(T_K - t'\wedge T_K)} \Big| \mathcal{F}_{t'} \right] \ge c \tag{3.20}
$$

for t ′ <sup>∈</sup> [0,∞). Since by Lemma [3.12](#page-12-1) <sup>T</sup><sup>K</sup> is finite a.s., we can find τ < <sup>∞</sup> such that

$$
\mathbb{E}_{m}\left[I_{\{T_{K}\geq\tau\}}e^{n\int_{0}^{T_{K}}\left(\sum_{(x,y)\in\mathcal{Z}}\mu_{x}(t)\gamma_{xy}C_{xy}\left(\frac{u_{xy}(t)}{\gamma_{xy}}\right)-R(\mu(t))\right)dt}\right]\leq\epsilon c.
$$

Now set <sup>u</sup>˜(t) = <sup>u</sup>(t) for <sup>t</sup> <sup>≤</sup> τ, and <sup>u</sup>˜(t) = <sup>γ</sup> so that <sup>C</sup>xy (˜uxy(t)/γxy) = 0 for <sup>t</sup> <sup>≥</sup> <sup>τ</sup> . Let <sup>µ</sup>˜ and <sup>T</sup>˜<sup>K</sup> be the corresponding controlled process and stopping time. Then the first claim of the lemma follows. The remaining claim follows from the following display, where the first inequality uses again that Cxy (1) = 0, the following equality uses that (u˜, µ˜, T˜K) had the same distribution as the original versions up till time τ , and the second inequality uses [\(3.20\)](#page-14-0):

$$
I_{K}^{n}(\boldsymbol{m},\tilde{\boldsymbol{u}}) = \mathbb{E}_{\boldsymbol{m}}\left[e^{n\int_{0}^{T_{K}}\left(\sum_{(x,y)\in\mathcal{Z}}\tilde{\mu}_{x}(t)\gamma_{xy}C_{xy}\left(\frac{\tilde{u}_{xy}(t)}{\gamma_{xy}}\right)-R(\tilde{\mu}(t))\right)dt}\right] \n\leq \mathbb{E}_{\boldsymbol{m}}\left[I_{\{T_{K}\leq\tau\}}e^{n\int_{0}^{T_{K}}\left(\sum_{(x,y)\in\mathcal{Z}}\tilde{\mu}_{x}(t)\gamma_{xy}C_{xy}\left(\frac{\tilde{u}_{xy}(t)}{\gamma_{xy}}\right)-R(\tilde{\mu}(t))\right)dt}\right] \n+ \mathbb{E}_{\boldsymbol{m}}\left[I_{\{T_{K}\geq\tau\}}e^{n\int_{0}^{T_{K}\wedge\tau}\left(\sum_{(x,y)\in\mathcal{Z}}\tilde{\mu}_{x}(t)\gamma_{xy}C_{xy}\left(\frac{\tilde{u}_{xy}(t)}{\gamma_{xy}}\right)-R(\tilde{\mu}(t))\right)dt}\right] \n+ \mathbb{E}_{\boldsymbol{m}}\left[I_{\{T_{K}\leq\tau\}}e^{n\int_{0}^{T_{K}}\left(\sum_{(x,y)\in\mathcal{Z}}\mu_{x}(t)\gamma_{xy}C_{xy}\left(\frac{u_{xy}(t)}{\gamma_{xy}}\right)-R(\mu(t))\right)dt}\right] \n+ \mathbb{E}_{\boldsymbol{m}}\left[I_{\{T_{K}\geq\tau\}}e^{n\int_{0}^{T_{K}\wedge\tau}\left(\sum_{(x,y)\in\mathcal{Z}}\mu_{x}(t)\gamma_{xy}C_{xy}\left(\frac{u_{xy}(t)}{\gamma_{xy}}\right)-R(\mu(t))\right)dt}\right] \n+ \mathbb{E}_{\boldsymbol{m}}\left[e^{n\int_{T_{K}\wedge\tau}^{T_{K}}\left(\sum_{(x,y)\in\mathcal{Z}}\mu_{x}(t)\gamma_{xy}C_{xy}\left(\frac{u_{xy}(t)}{\gamma_{xy}}\right)-R(\mu(t))\right)dt}\right] \n+ \frac{1}{C}\mathbb{E}_{\boldsymbol{m}}\left[e^{n\int_{0}^{T_{K}}\left(\sum_{(x,y)\in\mathcal{Z}}\mu_{x}(t)C_{xy}\left(\frac{u_{xy}(t)}{\gamma_{xy
$$

Proof of Theorem [3.8.](#page-9-2) We are first going to prove that V n <sup>K</sup> is the unique solution to [\(3.4\)](#page-7-0). We will prove that, by showing that if V˜ is any solution to [\(3.4\)](#page-7-0), then it has to coincide with V n <sup>K</sup>. Let <sup>V</sup>˜ be any solution to [\(3.4\)](#page-7-0), and let <sup>m</sup> ∈ P(<sup>X</sup> ). Let also <sup>q</sup> ∈ An,|Z| b be given and let µ solve [\(2.6\)](#page-6-2). By Lemma [3.10,](#page-11-1)

$$
\tilde{V}(\boldsymbol{\mu}(t\wedge T_K))-\tilde{V}(\boldsymbol{m})-\int_0^{t\wedge T_K}\sum_{(x,y)\in\mathcal{Z}}\mu_x(s)q_{xy}(s)\Delta^n\tilde{V}(\boldsymbol{\mu}(s))ds
$$

is a martingale. Taking expectation gives

$$
\mathbb{E}_{\boldsymbol{m}}\left[\tilde{V}(\boldsymbol{\mu}(t\wedge T_K))\right]-\mathbb{E}_{\boldsymbol{m}}\left[\int_0^{t\wedge T_K}\sum_{(x,y)\in\mathcal{Z}}\mu_x(s)q_{xy}(s)\Delta^n\tilde{V}(\boldsymbol{\mu}(s))ds\right]=\tilde{V}(\boldsymbol{m}),
$$

and since V˜ is a solution to [\(3.4\)](#page-7-0) and by [\(3.2\)](#page-7-3),

$$
\mathbb{E}_{\boldsymbol{m}}\left[\tilde{V}(\boldsymbol{\mu}(t\wedge T_K))\right]+\mathbb{E}_{\boldsymbol{m}}\left[\int_0^{t\wedge T_K}\left(\sum_{(x,y)\in\mathcal{Z}}\mu_x(s)F_{xy}(q_{xy}(s))+R(\boldsymbol{\mu}(s))\right)ds\right]\geq \tilde{V}(\boldsymbol{m}).
$$

By Lemma [3.12,](#page-12-1) T<sup>K</sup> < ∞ almost surely. Letting t → ∞, Lemma [3.7](#page-9-0) and the monotone convergence theorem imply

$$
J_K^n(\boldsymbol{m},\boldsymbol{q}) = \mathbb{E}_{\boldsymbol{m}}\left[\int_0^{T_K}\sum_{(x,y)\in\mathcal{Z}}\mu_x(t)F_{xy}(q_{xy}(s)) + R(\boldsymbol{\mu}(s))ds\right] \geq \tilde{V}(\boldsymbol{m}).
$$

Since <sup>q</sup> ∈ An,|Z| <sup>b</sup> was arbitrary we get V n <sup>K</sup>(m) <sup>≥</sup> <sup>V</sup>˜ (m). We will now prove the opposite inequality. Let ǫ > <sup>0</sup>. For <sup>m</sup> ∈ P<sup>n</sup> (X ), we can find q¯(m) that satisfies

<span id="page-15-0"></span>
$$
\sum_{(x,y)\in\mathcal{Z}} \left( \bar{q}_{xy}(\boldsymbol{m})n\left(\tilde{V}\left(\boldsymbol{m}+\frac{1}{n}v_{xy}\right)-\tilde{V}(\boldsymbol{m})\right)\right)+m_xF_{xy}(\bar{q}_{xy}(\boldsymbol{m}))\right)+R(\boldsymbol{m})\leq \epsilon\sum_{(x,y)\in\mathcal{Z}}m_xF_{xy}(\bar{q}_{xy}(\boldsymbol{m})).
$$
 (3.21)

To see that such a q¯(m) exists and it is actually bounded away from zero, we take a minimizing sequence q¯<sup>n</sup> (m) in the definition of H m, ∆nV˜ (m) (see [\(3.2\)](#page-7-3)). By using the continuity of the function P (x,y)∈Z q¯xy(m)n V˜ m+<sup>1</sup> n vxy <sup>−</sup> <sup>V</sup>˜ (m)) <sup>+</sup> <sup>m</sup>xFxy(¯qxy(m)) with respect to q¯<sup>n</sup> (m), we can assume that all qxy,n are strictly positive. Furthermore, with no loss of generality we can assume that the sequence is converging. If all elements converge to the original rates, by recalling [\(3.4\)](#page-7-0), we notice that we can just take those and the inequality is satisfied trivially. If on the other hand it converges to different values the right hand will be always bounded away from zero while the left hand will converge to zero by [\(3.4\)](#page-7-0), therefore for sufficiently large value of n, we will recover the desired control. We can construct a solution to [\(2.6\)](#page-6-2) with u replaced by the feedback control <sup>q</sup>¯(µ), and then obtain <sup>q</sup><sup>ˆ</sup> ∈ A|Z| b by setting qˆ(t) = q¯(µ(t)). Then

$$
\mathbb{E}_{\boldsymbol{m}}\left[\tilde{V}(\boldsymbol{\mu}(t\wedge T_K))\right]-\mathbb{E}_{\boldsymbol{m}}\left[\int_0^{t\wedge T_K}\sum_{(x,y)\in\mathcal{Z}}\mu_x(s)\bar{q}_{xy}(\boldsymbol{\mu}(s))\Delta^n\tilde{V}(\boldsymbol{\mu}(s))ds\right]=\tilde{V}(\boldsymbol{m}),
$$

and therefore by [\(3.21\)](#page-15-0)

$$
\mathbb{E}_{\boldsymbol{m}}\left[\tilde{V}(\boldsymbol{\mu}(t\wedge T_K))\right]+\mathbb{E}_{\boldsymbol{m}}\left[\int_0^{t\wedge T_K}\left((1-\epsilon)\sum_{(x,y)\in\mathcal{Z}}\mu_x(t)F^n(\bar{q}_{xy}(\boldsymbol{\mu}(s)))+R(\boldsymbol{\mu}(s))\right)ds\right]\leq \tilde{V}(\boldsymbol{m}).
$$

Again using Lemma [3.12](#page-12-1) and the monotone convergence theorem gives

$$
(1-\epsilon)\mathbb{E}_{\boldsymbol{m}}\left[\int_0^{T_K}\left(\sum_{(x,y)\in\mathcal{Z}}\mu_x(t)F^n(\bar{q}_{xy}(\boldsymbol{\mu}(s))) + R(\boldsymbol{\mu}(s))\right)ds\right] \leq \tilde{V}(\boldsymbol{m}),
$$

and therefore V n <sup>K</sup>(m) ≤ J n <sup>K</sup>(m, qˆ) ≤ 1 1−ǫ V˜ (m). Since ǫ is arbitrary we get V n <sup>K</sup>(m) = <sup>V</sup>˜ (m), which implies the uniqueness of V˜ . We now proceed with the proof that W<sup>n</sup> <sup>K</sup> is the unique solution to

<span id="page-16-0"></span>
$$
\sup_{\boldsymbol{u}\in(0,\infty)^{|\mathcal{Z}|}}\left\{\sum_{(x,y)\in\mathcal{Z}}\mu_x\left(u_{xy}\left(\frac{W(\boldsymbol{\mu})-W(\boldsymbol{\mu}+\frac{\boldsymbol{v}_{xy}}{n})}{W(\boldsymbol{\mu})}\right)-\gamma_{xy}C_{xy}\left(\frac{u_{xy}}{\gamma_{xy}}\right)\right)\right\}=-R(\boldsymbol{\mu}).\tag{3.22}
$$

Since V n <sup>K</sup> is a solution to [\(3.4\)](#page-7-0), by Lemma [3.1](#page-7-2) we get that <sup>1</sup> n log(V n <sup>K</sup>) is a solution to [\(3.22\)](#page-16-0), and thus uniqueness will imply <sup>1</sup> n log(V n <sup>K</sup>) = W<sup>n</sup> <sup>K</sup>. Let <sup>W</sup>˜ be any solution to [\(3.22\)](#page-16-0), <sup>m</sup> ∈ P<sup>n</sup> (<sup>X</sup> ), and <sup>u</sup> ∈ An,|Z| b , and let µ solve [\(2.6\)](#page-6-2). Further assume that there exists τ < ∞ such that for t > τ

<span id="page-16-2"></span>
$$
\sum_{(x,y)\in\mathcal{Z}}\mu_x(t)\gamma_{xy}C_{xy}\left(\frac{u_{xy}(t))}{\gamma_{xy}}\right) - R(\mu(t)) \le 0.
$$
\n(3.23)

To show J n <sup>K</sup>(m,u) <sup>≥</sup> <sup>W</sup>˜ (m) we can assume that <sup>J</sup> n <sup>K</sup>(m,u) < ∞, since otherwise there is nothing to prove. By Lemma [3.11](#page-11-0)

$$
\frac{\tilde{W}(\boldsymbol{\mu}(t\wedge T_K))}{\tilde{W}(\boldsymbol{m})}\exp\left\{-\int_0^{t\wedge T_K}\sum_{(x,y)\in\mathcal{Z}}\mu_x(s)u_{xy}(s)\frac{\Delta^n\tilde{W}(\boldsymbol{\mu}(s))}{\tilde{W}(\boldsymbol{\mu}(s))}ds\right\}
$$

is a martingale. Taking expectations gives

$$
\mathbb{E}_{\boldsymbol{m}}\left[\tilde{W}(\boldsymbol{\mu}(t\wedge T_K))\exp\left\{-\int_0^{t\wedge T_K}\sum_{(x,y)\in\mathcal{Z}}\mu_x(s)u_{xy}(s)\frac{\Delta^n\tilde{W}(\boldsymbol{\mu}(s))}{\tilde{W}(\boldsymbol{\mu}(s))}ds\right\}\right]=\tilde{W}(\boldsymbol{m}),
$$

and by [\(3.4\)](#page-7-0) and the definition of ∆<sup>n</sup>

$$
\mathbb{E}_{\boldsymbol{m}}\left[\tilde{W}(\boldsymbol{\mu}(t\wedge T_K))\exp\left\{\boldsymbol{n}\int_0^{t\wedge T_K}\left(\sum_{(x,y)\in\mathcal{Z}}\mu_x(s)\gamma_{xy}C_{xy}\left(\frac{u_{xy}(s)}{\gamma_{xy}}\right)-R(\boldsymbol{\mu}(s))\right)ds\right\}\right]\geq \tilde{W}(\boldsymbol{m}).
$$

We claim that

<span id="page-16-1"></span>
$$
\mathbb{E}_{m}\left[\tilde{W}(\mu(t\wedge T_{K}))\exp\left\{n\int_{0}^{\tau\wedge T_{K}}\left(\sum_{(x,y)\in\mathcal{Z}}\mu_{x}(s)\gamma_{xy}C_{xy}\left(\frac{u_{xy}(s)}{\gamma_{xy}}\right)-R(\mu(s))\right)ds\right\}\right]<\infty.
$$
 (3.24)

Since W˜ is uniformly bounded this term can be ignored. One can then bound what remains in [\(3.24\)](#page-16-1) by using

$$
\infty > J_K^n(\boldsymbol{m}, \boldsymbol{u}) = \mathbb{E}_{\boldsymbol{m}}\left[\exp\left\{n \int_0^{T_K} \left(\sum_{(x,y)\in \mathcal{Z}} \mu_x(s)\gamma_{xy}C_{xy}\left(\frac{u_{xy}(s)}{\gamma_{xy}}\right) - R(\boldsymbol{\mu}(s))\right) ds\right\}\right],
$$

breaking the integral over [0, T<sup>K</sup> ] into contributions over [0, τ ∧ TK] and [τ ∧ TK, TK], and then conditioning on F<sup>τ</sup> and using the lower bound on the term corresponding to [τ ∧ TK, TK] provided by Lemma [3.12](#page-12-1) (as in the proof of Lemma [3.13\)](#page-13-0). Since (by Lemma [3.12\)](#page-12-1) T<sup>K</sup> is finite almost surely, and [\(3.23\)](#page-16-2) holds for t ≥ τ , by dominated convergence theorem and [\(3.24\)](#page-16-1) it follows that

$$
J_K^n(\boldsymbol{m},\boldsymbol{u}) = \mathbb{E}\left[\exp\left\{n \int_0^{T_K} \left(\sum_{(x,y)\in\mathcal{Z}} \mu_x(s)\gamma_{xy}C_{xy}\left(\frac{u_{xy}(s)}{\gamma_{xy}}\right) - R(\boldsymbol{\mu}(s))\right) ds\right\}\right] \geq \tilde{W}(\boldsymbol{m}).
$$

By minimizing over all u that satisfy [\(3.23\)](#page-16-2) and applying Lemma [3.13,](#page-13-0) we get W<sup>n</sup> <sup>K</sup>(m) <sup>≥</sup> <sup>W</sup>˜ (m). Next let <sup>ǫ</sup> <sup>∈</sup> (0, <sup>1</sup>/2). For <sup>m</sup> ∈ P<sup>n</sup> (X ), t ≥ 0 we choose u¯(m, t) such that

<span id="page-17-0"></span>
$$
\sum_{(x,y)\in\mathcal{Z}} m_x \left( \bar{u}_{xy}(\boldsymbol{m},t) \left( \frac{\tilde{W}(\boldsymbol{m}) - \tilde{W}(\boldsymbol{m} + \frac{v_{xy}}{n})}{\tilde{W}(\boldsymbol{m})} \right) - \gamma_{xy} C_{xy} \left( \frac{\bar{u}_{xy}(\boldsymbol{m},t)}{\gamma_{xy}} \right) \right) \ge -R(\boldsymbol{m}) - \frac{\epsilon}{t^2 + 1}.
$$
 (3.25)

As before we can solve [\(2.6\)](#page-6-2) and then generate a corresponding element u of A n,|Z| b by composing ¯uxy(m, t) with the solution. It is easy to see that u is an element of A n,|Z| b , since very big or very small values of u¯xy(m, t) will make the left hand of [\(3.25\)](#page-17-0) tend to −∞. Arguing as before, for fixed t < ∞

$$
\mathbb{E}_{\boldsymbol{m}}\left[\tilde{W}(\boldsymbol{\mu}(t\wedge T_K))\exp\left\{\boldsymbol{n}\int_0^{T_K\wedge t}\left(\sum_{(x,y)\in\mathcal{Z}}\mu_x(s)\gamma_{xy}C_{xy}\left(\frac{\bar{u}_{xy}(\boldsymbol{\mu}(s),s)}{\gamma_{xy}}\right)-R(\boldsymbol{\mu}(s))-\frac{\epsilon}{s^2+1}\right)ds\right\}\right]\leq \tilde{W}(\boldsymbol{m}).
$$

By sending t → ∞ and using the boundary condition, Fatou's lemma gives

$$
\mathbb{E}_{\boldsymbol{m}}\left[\exp\left(\int_0^\infty -\frac{\epsilon}{s^2+1}ds\right)\exp\left\{\boldsymbol{n}\int_0^{T_K}\left(\sum_{(x,y)\in\mathcal{Z}}\mu_x(s)\gamma_{xy}C_{xy}\left(\frac{\bar{u}_{xy}(\boldsymbol{\mu}(s),s)}{\gamma_{xy}}\right)-R(\boldsymbol{\mu}(s))\right)ds\right\}\right]\leq \tilde{W}(\boldsymbol{m}),
$$

from which we get W<sup>n</sup> <sup>K</sup>(m) <sup>≤</sup> <sup>W</sup>˜ (m) exp[<sup>ǫ</sup> R <sup>∞</sup> 0 1/(s <sup>2</sup> + 1)ds]. Sending ǫ to zero shows W<sup>n</sup> <sup>K</sup>(m) <sup>≤</sup> <sup>W</sup>˜ (m).

The proof that V n <sup>K</sup>(x n ) = − 1 n log(W<sup>n</sup> <sup>K</sup>(x n )) is similar and thus omitted. It remains only to prove V n <sup>K</sup>(L(x n )) = V n <sup>K</sup>(x n ). We have established that V n <sup>K</sup> is the only function that satisfies

$$
\inf_{\boldsymbol{q}\in(0,\infty)^{|\mathcal{Z}|}}\left\{\sum_{(x,y)\in\mathcal{Z}}m_x\left(q_{xy}\Delta_{xy}^nV_K^n\left(\boldsymbol{m}\right)+F_{xy}(q_{xy})\right)\right\}=-R(\boldsymbol{m}),
$$

and that V n <sup>K</sup> is the only function that satisfies

<span id="page-17-1"></span>
$$
\inf_{\mathbf{q}\in(0,\infty)^{n|Z|}}\left\{\sum_{i=1}^{n}\sum_{y\in\mathcal{Z}_{x_i^n}}\left(q_{x_i^n y}\Delta_{i,x_i^n y}^n\mathcal{V}_K^n\left(\mathbf{x}^n\right)+F_{x_i^n y}(q_{x_i^n y})\right)\right\}=-nR(L(\mathbf{x}^n)).
$$
\n(3.26)

Since <sup>K</sup> ⊂ X <sup>n</sup> is invariant under permutations, and therefore can be identified with a subset of P n (X ), we have that there exists a function <sup>V</sup>¯ : <sup>P</sup> n (<sup>X</sup> ) <sup>→</sup> [0,∞) such that <sup>V</sup>¯ (L(<sup>x</sup> n )) = V n <sup>K</sup>(x n ), and therefore [\(3.26\)](#page-17-1) becomes

$$
\inf_{\boldsymbol{q}\in(0,\infty)^{n|{\cal Z}|}}\left\{\sum_{i=1}^n\sum_{y\in\mathcal{Z}_{x_i^n}}\left(q_{x_i^ny}\Delta_{i,x_i^ny}^n\bar{V}\left(L(\boldsymbol{x}^n)\right)+F_{x_i^ny}(q_{x_i^ny}\right)\right)\right\}=-nR(L(\boldsymbol{x}^n)).
$$

For ǫ > 0, let q¯ ∈ (0,∞) <sup>n</sup>|Z| satisfy

$$
\sum_{i=1}^n \sum_{y \in \mathcal{Z}_{x_i^n}} \left[ \bar{q}_{x_i^n y} \Delta_{i, x_i^n y}^n \bar{V} \left( L(x^n) \right) + F_{x_i^n y}(\bar{q}_{x_i^n y}) \right] \le -nR(L(x^n)) + \epsilon.
$$

Now pick q˜ ∈ (0,∞) |Z| by requiring nLx(x n )˜qxy = P<sup>n</sup> <sup>i</sup>=1 I<sup>x</sup> n <sup>i</sup> <sup>=</sup>xq¯<sup>x</sup> n i <sup>y</sup>, so that

$$
\sum_{(x,y)\in\mathcal{Z}}nL_x(\boldsymbol{x}^n)\tilde{q}_{xy}\Delta_{xy}^n\bar{V}(L(\boldsymbol{x}^n))+\sum_{i=1}^n\sum_{y\in\mathcal{Z}_{x_i^n}}F_{x_i^n y}(\bar{q}_{x_i^n y})\leq -nR(L(\boldsymbol{x}^n))+\epsilon.
$$

By using convexity of Fxy (see Lemma [3.7\)](#page-9-0) we get

$$
\sum_{(x,y)\in\mathcal{Z}}L_x(\boldsymbol{x}^n)\left[\tilde{q}_{xy}\Delta_{xy}^n\bar{V}\left(L(\boldsymbol{x}^n)\right)+F_{xy}(\tilde{q}_{xy})\right]\leq -R(L(\boldsymbol{x}^n))+\epsilon/n,
$$

and sending ǫ ↓ 0 gives

$$
\inf_{\boldsymbol{q}\in(0,\infty)^{|\mathcal{Z}|}}\left\{\sum_{(x,y)\in\mathcal{Z}}L_x(\boldsymbol{x}^n)\left[q_{xy}\Delta_{xy}^n\bar{V}\left(L(\boldsymbol{x}^n)\right)+F_{xy}(q_{xy})\right]\right\}\leq -R(L(\boldsymbol{x}^n)).
$$

The other direction is trivial, and follows if in [\(3.26\)](#page-17-1) one uses rates that are the same for all agents in the same position.

## 4 Discussion regarding convergence

Before we introduce the deterministic control problem, we define the set of admissible controls and controlled trajectories.

Definition 4.1 We define the space of paths and controls by

$$
\mathcal{C} = \{(\boldsymbol{\mu}, \boldsymbol{q}) \in \mathcal{D}([0, \infty); \mathcal{P}(\mathcal{X})) \times \mathcal{F}([0, \infty); [0, \infty)^{\otimes \mathcal{Z}}): \mu_x q_{xy} \text{ is locally integrable } \forall (x, y) \in \mathcal{Z}\},\
$$

where F [0,∞); [0,∞) ⊗Z was defined in [\(1.12\)](#page-4-0). We define Λ : C × P(X ) → D([0,∞); H) by

<span id="page-18-0"></span>
$$
\Lambda(\boldsymbol{\mu}, \boldsymbol{q}, \boldsymbol{m})(t) \doteq \boldsymbol{m} + \sum_{(x, y) \in \mathcal{Z}} \boldsymbol{v}_{xy} \int_{[0, t)} \mu_x(s) q_{xy}(s) ds. \tag{4.1}
$$

Also we define the set of all deterministic pairs that correspond to a solution of the equation µ = Λ(µ, q,m), i.e.,

$$
\mathcal{T}_m \doteq \{(\boldsymbol{\mu}, \boldsymbol{q}) \in \mathcal{C}: \boldsymbol{\mu} = \Lambda(\boldsymbol{\mu}, \boldsymbol{q}, \boldsymbol{m}), \boldsymbol{\mu}(0) = \boldsymbol{m}\}
$$

Finally we introduce the set of controls that generate controlled trajectories

<span id="page-19-3"></span>
$$
\mathcal{U}_{m} \doteq \left\{ \boldsymbol{q} \in \mathcal{F}([0,\infty);[0,\infty)^{\otimes \mathcal{Z}}): \exists \boldsymbol{\mu} \in \mathcal{D}([0,\infty); \mathcal{P}(\mathcal{X})) \text{ such that } (\boldsymbol{\mu},\boldsymbol{q}) \in \mathcal{T}_{m} \right\}. \tag{4.2}
$$

Then the deterministic control problems are given by

<span id="page-19-0"></span>
$$
V_K(\boldsymbol{m}) \doteq \inf_{(\boldsymbol{\mu}, \boldsymbol{q}) \in \mathcal{T}_m} J_K(\boldsymbol{m}, \boldsymbol{\mu}, \boldsymbol{q}), \qquad (4.3)
$$

with

$$
J_K(\boldsymbol{m}, \boldsymbol{\mu}, \boldsymbol{q}) \doteq \left\{ \int_0^{T_K} \left( \sum_{(x,y) \in \mathcal{Z}} \mu_x(t) F_{xy}(q_{xy}(t)) + R(\boldsymbol{\mu}(t)) \right) dt \right\}, \quad T_K \doteq \inf_{t \in [0,\infty]} \left\{ \boldsymbol{\mu}(t) \in K \right\}.
$$

<span id="page-19-2"></span>In this section we consider sets K ⊂ P(X ) that satisfy the following assumption.

## Assumption 4.2 K = K◦ 6= ∅.

For such sets we show that the sequence of values functions V n <sup>K</sup> converges uniformly to the function VK. To simplify the notation we will drop the index that corresponds to the set from the stopping time. We split the study of the convergence in two parts. In the first part, without making any extra assumptions on the cost functions and in great generality, we prove that for any sequence {mn}, with <sup>m</sup><sup>n</sup> ∈ P<sup>n</sup> (X ) converging in m ∈ P(X ),

$$
\liminf_{n\to\infty}V_K^n(\boldsymbol{m}^n)\geq V_K(\boldsymbol{m}).
$$

The other direction of the inequality, i.e., lim supn→∞ V n K(m<sup>n</sup> ) ≤ VK(m), is not as straightforward and its analysis can be quite involved. In order to avoid technical issues relating to controllability we will add some assumptions.

Before we present the extra assumptions on C we discuss an almost trivial choice for the cost function that will motivate these extra assumptions. As stated in Lemma [3.6,](#page-9-3) for every (x, y) ∈ Z we have Cxy(u) ≥ − log u + u − u. Actually the function Cxy(u) = − log u + u − 1 satisfies Assumption [3.2](#page-8-0) and therefore is an eligible cost function. Setting Cxy(u) ≡ C(u) = − log u + u − 1, we get

<span id="page-19-1"></span>
$$
G_{xy}(u,q) = u\ell\left(\frac{q}{u}\right) - \gamma_{xy}C_{xy}\left(\frac{u}{\gamma_{xy}}\right) = q\log\frac{q}{u} - q + u + \gamma_{xy}\log\frac{u}{\gamma_{xy}} - u + \gamma_{xy}
$$
(4.4)  
=  $q\log q + (\gamma_{xy} - q)\log u - q + \gamma_{xy}$ .

Examining [\(4.4\)](#page-19-1) and referring to the definition of Fxy in [\(1.8\)](#page-2-1), we observe that if qxy > γxy then the "maximizing player" (the one that picks u), can produce an arbitrarily large cost by making uxy as small as needed. If qxy < γxy, this player can produce an arbitrarily large cost by making uxy as big as needed. Hence the minimizing player must keep qxy = γxy, and the value function V (m) is infinite unless the solution of the equation ν˙(t) = ν(t)γ passes through K for the specific choice of initial data m. To resolve this difficulty we could start by imposing the following assumption on the cost.

$$
\lim_{u \to 0} u(C_{xy})'(u) = -\infty, \quad \liminf_{u \to \infty} \{u(C_{xy})'(u) - u\} \ge 0.
$$

This assumption makes F finite on (0,∞) and allows for some controllability. Specifically, if the first point is true and if m,m˜ ∈ Pa(X ) for some a > 0, then one can observe (see the proof of Lemma [3.7\)](#page-9-0) that the total cost V{m¯ } (m) for moving from point m to m˜ is uniformly bounded by cakm − m˜ k, where c<sup>a</sup> > 0 is an appropriate constant, where the minimizing player picks ˜qxy(t) to be uniformly bounded from above, but big enough to reach the desired point. In particular, the maximizing player cannot impose an arbitrarily large cost by taking uxy small. In an analogous fashion, the second point implies that the minimizer can choose controls so that the total cost V{m˜ } (m) for moving from point m to m˜ is uniformly bounded by c ′ a km − m˜ k by picking ˜qxy(t) bounded from below but small enough.

However, if m˜ is in the natural boundary of the simplex P(X ) an additional complication arises, because to reach the natural boundary it must be true that for at least one (x, y) ∈ Z the quantity ˜qxy(t) will scale like 1/µ˜x(t). In that case, the first point is not enough for a finite cost, since sending ˜qxy(t) to infinity in order to reach the natural boundary may result in an infinite total cost. Taking all these issues into account we end up with the following assumption.

Assumption 4.3 Let C, R be as in Assumption [3.2.](#page-8-0) Assume that for all (x, y) ∈ Z, the following are valid.

1. There exists p > 0 such that

<span id="page-20-0"></span>
$$
\lim_{u \to 0} u^{p+1} C'_{xy}(u) = -\infty.
$$

2.

<span id="page-20-2"></span>
$$
\liminf_{u \to \infty} \{ uC'_{xy}(u) - u \} \ge 0.
$$

It is straightforward to see that Assumption [4.3](#page-20-0) is satisfied by all functions in Example [3.1,](#page-8-8) with p, q > 1. Now we state the second main theorem of the paper.

Theorem 4.4 Let C, R, satisfy Assumption [4.3.](#page-20-0) Let also K be a closed subset of P(X ) that satisfies Assumption [4.2.](#page-19-2) Finally assume that in every compact subset of K<sup>c</sup> , R is bounded from below by a positive constant. Then the sequence of functions V n <sup>K</sup> defined in [\(2.9\)](#page-6-3) converges uniformly to V<sup>K</sup> defined in [\(4.3\)](#page-19-0).

<span id="page-20-1"></span>Before proceeding with the proof, we state some properties of Fxy.

Lemma 4.5 For every (x, y) ∈ Z, let Fxy be as in [\(1.8\)](#page-2-1), where Cxy satisfy Assumption [4.3.](#page-20-0) Then the following hold.

1. There exists a constant <sup>M</sup> <sup>∈</sup> (0,∞) and a decreasing function <sup>M</sup>¯ : (0,∞) <sup>→</sup> (0,∞), such that for every ǫ > 0 and every q ≥ ǫ,

$$
F_{xy}(q) \le q \log \frac{q}{\min \left\{ \gamma_{xy} \left( \gamma_{xy}/q \right)^{1/p}, M \right\}} + \bar{M}(\epsilon).
$$

2. Fxy is continuous on the interval (0,∞).

<span id="page-20-3"></span>The proof of the Lemma [4.5](#page-20-1) can be found in Appendix [B.](#page-38-0) It is worth mentioning that it is possible that Fxy(0) = ∞. In the sequel we will make use of the following remark, which states a property proved in [\[12,](#page-42-13) Proposition 4.14]

Remark 4.6 There exists D ≥ 1 and b<sup>1</sup> > 0, b<sup>2</sup> < ∞ such that for every m ∈ P(X), if ν(m, t) is the solution of ν˙(t) = ν(t)γ with initial point ν(0) = m, then

> 1. ∀x ∈ X , νx(m, t) ≥ b1t <sup>D</sup> and <sup>2</sup>. <sup>k</sup>ν(m, t) <sup>−</sup> <sup>m</sup>k ≤ <sup>b</sup>2t.

Before proceeding with the proof of Theorem [4.4,](#page-20-2) we prove that the function V (m) is continuous. We will actually prove something stronger. Recall that γ denotes the original unperturbed jump rates and the definitions of P∗(X ) and Pa(X ) in [\(1.13\)](#page-4-1).

<span id="page-21-2"></span>Theorem 4.7 There is a constant c¯ ∈ R that depends only the dimension d and the unperturbed rates γ, such that for every m ∈ P∗(X ), m˜ ∈ P(X ) there exists a control q ∈ Um, that generates a unique µ with (µ, q) ∈ Tm, satisfying

- 1. µ is a constant speed parametrization of the straight line that connects m and m˜ ,
- 2. the exit time T{m˜ } is equal to km − m˜ k,
- 3. γxy ≤ qxy(t) and µx(t)qxy(t) ≤ c¯.

Furthermore, if m,m˜ ∈ Pa(X ) then

$$
\gamma_{xy} \le q_{xy}(t) \le \frac{\bar{c}}{a},
$$

and we can find a constant c<sup>a</sup> < ∞ such that the total cost for applying the control is bounded above by cakm−m˜ k. Finally, for every ǫ > 0 there exists δ > 0, such that km¯ −m˜ k ≤ δ implies V{m˜ } (m¯ ), V{m¯ } (m˜ ) ≤ ǫ, and therefore as a function of two variables V is continuous on P(X ) × P(X ).

Proof. Recall the definitions above [\(1.3\)](#page-1-2), and let m ∈ P∗(X ), m˜ ∈ P(X ). We can find a positive constant c¯ that depend only the dimension d and on the rates γ, and also rates q such that

$$
1. q_{xy} \geq \gamma_{xy}, \quad 2. \sum_{(x,y)\in\mathcal{Z}} m_x q_{xy} \boldsymbol{v}_{xy} = \frac{\tilde{\boldsymbol{m}} - \boldsymbol{m}}{\|\tilde{\boldsymbol{m}} - \boldsymbol{m}\|}, \quad 3. \, \max\{m_x q_{xy}, (x,y)\in\mathcal{Z}\} \leq \bar{c}.
$$

Indeed, since [\(1.3\)](#page-1-2) holds, we can find a constant c < ∞ such that for every point m ∈ P∗(X ), there exist vectors qxymxvxy with qxym<sup>x</sup> ≤ c, and P (x,y)∈Z <sup>m</sup>xqxyvxy <sup>=</sup> <sup>m</sup>˜ <sup>−</sup><sup>m</sup> km˜ −mk . Now if for some (x1, y1) ∈ Z we do not have qx1y<sup>1</sup> ≥ γx1y<sup>1</sup> , then by ergodicity we can pick x1, x<sup>2</sup> = y1, x3, . . . , x<sup>j</sup> , with j ≤ d, such that Pj−<sup>1</sup> <sup>i</sup>=1 vxixi+1 = 0. If we pick the new qxixi+1 equal to maxxy{γxy}/mx<sup>i</sup> plus the original qxixi+1, then property 2 is still satisfied, but we now also have qx1y<sup>1</sup> ≥ γx1y<sup>1</sup> . We have to repeat the procedure at most |Z| times to enforce property 1, and can then set ¯c .= max{mxqxy,(x, y) ∈ Z}.

Let

<span id="page-21-1"></span>
$$
\tilde{\boldsymbol{\mu}}(t) = [(\tilde{\boldsymbol{m}} - \boldsymbol{m})t/ \|\tilde{\boldsymbol{m}} - \boldsymbol{m}\| + \boldsymbol{m}], \tag{4.5}
$$

and define q˜ ∈ U<sup>m</sup> by

<span id="page-21-0"></span>
$$
\tilde{\mu}_x(t)\tilde{q}_{xy}(t) = m_x q_{xy} \le \bar{c}.\tag{4.6}
$$

Then automatically

$$
\sum_{(x,y)\in\mathcal{Z}}\boldsymbol{v}_{xy}\int_{[0,t)}\tilde{\mu}_x(s)\tilde{q}_{xy}(s)ds=t\frac{\tilde{\boldsymbol{m}}-\boldsymbol{m}}{\|\tilde{\boldsymbol{m}}-\boldsymbol{m}\|}=\tilde{\boldsymbol{\mu}}(t)-\boldsymbol{m},
$$

and thus (µ˜, q˜) ∈ Tm. This will lead to hitting {m˜ } in time T{m˜ } = km − m˜ k. Using properties stated in Lemma [4.5](#page-20-1) we get

$$
\inf_{(\mu,q)\in\mathcal{T}_{m}}J_{\{\hat{m}\}}(m,\mu,q)\leq J_{\{\hat{m}\}}(m,\tilde{\mu},\tilde{q})\leq \sum_{(x,y)\in\mathcal{Z}}\int_{0}^{T_{\{\hat{m}\}}}\tilde{\mu}_{x}(t)F_{xy}(\tilde{q}_{xy}(t)) + R_{\max}T_{\{\hat{m}\}}\n\stackrel{(4.6)}{\leq}\sum_{(x,y)\in\mathcal{Z}}\int_{0}^{T_{\{\hat{m}\}}}\left(\tilde{\mu}_{x}(t)\tilde{q}_{xy}(t)\log\frac{\tilde{q}_{xy}(t)}{\min\left\{\gamma_{xy}\left(\gamma_{xy}/\tilde{q}_{xy}(t)\right)^{1/p},M\right\}} + \max_{(x,y)\in\mathcal{Z}}\tilde{M}(\gamma_{xy})\right)dt + R_{\max}T_{\{\hat{m}\}}\n\leq \sum_{(x,y)\in\mathcal{Z}}\int_{0}^{T_{\{\hat{m}\}}}\left|\tilde{\mu}_{x}(t)\tilde{q}_{xy}(t)\log\tilde{q}_{xy}(t)\right|dt + \sum_{(x,y)\in\mathcal{Z}}\int_{0}^{T_{\{\hat{m}\}}}\left|\tilde{\mu}_{x}(t)\tilde{q}_{xy}(t)\log\left(\gamma_{xy}/\tilde{q}_{xy}(t)\right)^{1/p}\right|dt +\n+\sum_{(x,y)\in\mathcal{Z}}\int_{0}^{T_{\{\hat{m}\}}}\left|\tilde{\mu}_{x}(t)\tilde{q}_{xy}(t)\log\gamma_{xy}\right|dt + \sum_{(x,y)\in\mathcal{Z}}\int_{0}^{T_{\{\hat{m}\}}}\left|\tilde{\mu}_{x}(t)\tilde{q}_{xy}(t)\log M\right|dt + c'T_{\{\hat{m}\}}\n\stackrel{(4.6)}{\leq}\frac{\tilde{\epsilon}}{\tilde{\epsilon}}\sum_{(x,y)\in\mathcal{Z}}\int_{0}^{T_{\{\hat{m}\}}}\left|\log\tilde{q}_{xy}(t)\right|dt + \tilde{c}\sum_{(x,y)\in\mathcal{Z}}\int_{0}^{T_{\{\hat{m}\}}}\left|\log\left(\gamma_{xy}/\tilde{q}_{xy}(t)\right)^{1/p}\right|dt + c''T_{\{\hat{m}\}}\n\stackrel{(4.6)}{\leq}\frac{\tilde{\epsilon}}{\tilde{\epsilon}}\sum_{(x,y)\in\mathcal{
$$

where the constants c ′ , c′′, c′′′ depend only on γ, c¯ and Rmax.

Now if m,m˜ ∈ Pa(X ), then all elements are bounded by a constant c<sup>a</sup> (that depends on γ, c, R¯ max, and a) times T{m˜ } = km˜ − mk, and therefore the first part of the theorem follows.

Let 1 > δ > 0, and m¯ ,m˜ ∈ P(X ), with km¯ − m˜ k < δ. We take m = ν(m¯ , δ), where ν(m¯ , t) is the solution of ν˙(t) = ν(t)γ, with initial data ν(0) = m¯ . Now by appropriate use of the inequality µ˜x(t) ≥ min{mx, mx(T{m˜ } − t)}, that we get from [\(4.5\)](#page-21-1), and using the last display, we get

$$
V_{\{\tilde{\boldsymbol{m}}\}}(\boldsymbol{m}) \leq c''''\left(\sum_{(x,y)\in\mathcal{Z}}\int_0^{T_{\{\tilde{\boldsymbol{m}}\}}}\left(|\log m_x| + |\log(T_{\{\tilde{\boldsymbol{m}}\}} - t)|\right)dt + T_{\{\tilde{\boldsymbol{m}}\}}\right).
$$

By a simple change of variable and Remark [4.6,](#page-20-3) we have

$$
V_{\{\tilde{\boldsymbol{m}}\}}(\boldsymbol{m}) \leq c'''' \left( \sum_{(x,y)\in\mathcal{Z}} \int_0^{b_2\delta} \left( |\log b_1\delta^D| + |\log t| \right) dt + b_2\delta \right).
$$

Therefore

$$
V_{\{\tilde{\boldsymbol{m}}\}}(\bar{\boldsymbol{m}}) \leq V_{\{\boldsymbol{m}\}}(\bar{\boldsymbol{m}}) + V_{\{\tilde{\boldsymbol{m}}\}}(\boldsymbol{m}) \leq \delta R_{\max} + c'''' \left(\sum_{(x,y)\in\mathcal{Z}} \int_0^{b_2\delta} \left(|\log b_1\delta^D| + |\log t|\right) dt + b_2\delta\right),
$$

and the right hand side can be made as small as desired by making δ small enough. The estimate for V{m¯ } (m˜ ) is proved in a symmetric way. This proves the last statement of the theorem.

## 5 Lower bound

For the proof of Theorem [4.4,](#page-20-2) we first prove the lower bound: for every sequence <sup>m</sup><sup>n</sup> ∈ P<sup>n</sup> (X ) and m ∈ P(X ), with <sup>m</sup><sup>n</sup> <sup>→</sup> <sup>m</sup>, we have

> lim inf n→∞ V n K(m<sup>n</sup> ) ≥ VK(m).

Without loss of generality we can assume that the liminf is actually a limit, otherwise we can just work with a subsequence. If the limit is ∞ then the conclusion is trivial, therefore we can assume that there is c ∈ R such that

<span id="page-23-2"></span>
$$
\sup_{n \in \mathbb{N}} V_K^n(\mathbf{m}^n) \le c. \tag{5.1}
$$

Let ǫ ∈ (0, 1). Recalling [\(2.9\)](#page-6-3), let q <sup>n</sup> ∈ An,|Z| b be such that

<span id="page-23-0"></span>
$$
\mathbb{E}_{\boldsymbol{m}^n} \left[ \int_0^{T^n} \left( \sum_{(x,y)\in \mathcal{Z}} \mu_x^n(t) F_{xy}(q_{xy}^n(t)) + R(\boldsymbol{\mu}^n(t)) \right) dt \right] < V_K^n(\boldsymbol{m}^n) + \epsilon,\tag{5.2}
$$

where µ <sup>n</sup> = h n (µ n , q n ,m<sup>n</sup> , N<sup>n</sup> /n) and T <sup>n</sup> .= inf {<sup>t</sup> <sup>∈</sup> [0,∞] : <sup>µ</sup> n (t) ∈ K} . For δ > 0 such that

$$
\|\bar{\mathbf{m}} - \tilde{\mathbf{m}}\| \le \delta \Rightarrow V_{\bar{\mathbf{m}}}(\tilde{\mathbf{m}}) \le \epsilon,
$$

we define K<sup>δ</sup> .<sup>=</sup> {<sup>m</sup> : <sup>d</sup>(m, K) <sup>≤</sup> <sup>δ</sup>} and <sup>T</sup> n,δ .= inf{<sup>t</sup> <sup>∈</sup> [0,∞] : <sup>µ</sup><sup>n</sup> (t) ∈ Kδ}.

The existence of such a δ is given by Theorem [4.7.](#page-21-2) Now for µ n , q <sup>n</sup> as in [\(5.2\)](#page-23-0) and T n,δ as above, we define the sequences µ n,δ(t) = µ n (t ∧ T n,δ),

$$
\boldsymbol{q}^{n,\delta}(t)=\begin{cases}\boldsymbol{q}^n(t) & t\leq T^{n,\delta}\\ \boldsymbol{\gamma} & T>T^{n,\delta}\end{cases}.
$$

We note that for t > T<sup>δ</sup> , q n,δ(t) does not actually generate µ n , but we define it this way to simplify some arguments later on. We will show that

$$
\liminf_{n \to \infty} \mathbb{E}_{\boldsymbol{m}^n} \left[ \int_0^{T^n} \left( \sum_{(x,y) \in \mathcal{Z}} \mu_x^n(t) F_{xy}(q_{xy}^n(t)) + R(\boldsymbol{\mu}^n(t)) \right) dt \right] \ge
$$
\n
$$
\liminf_{n \to \infty} \mathbb{E}_{\boldsymbol{m}^n} \left[ \int_0^{T^{n,\delta}} \left( \sum_{(x,y) \in \mathcal{Z}} \mu_x^{n,\delta}(t) F_{xy}(q_{xy}^{n,\delta}(t)) + R(\boldsymbol{\mu}^{n,\delta}(t)) \right) dt \right] \ge V_{K_\delta}(\boldsymbol{m}),
$$
\n(5.3)

<span id="page-23-1"></span>and then by an application of Theorem [4.7](#page-21-2) and [\(5.2\)](#page-23-0) deduce limn→∞ V n K(m<sup>n</sup> ) + 2ǫ ≥ VK(m). Since ǫ is arbitrary the lower bound will follow. The first inequality in [\(5.3\)](#page-23-1) is true since Fxy ≥ 0, R ≥ 0 and T n,δ <sup>≤</sup> <sup>T</sup> n . Therefore only the second inequality needs to be proved.

Before proceeding we introduce some auxiliary random measures. For (x, y) ∈ Z, qxy ∈ F([0,∞); [0,∞)), and t ∈ [0,∞), define

$$
\eta_{xy}(dr;t) \doteq \delta_{q_{xy}(t)}(dr)\mu_x(t).
$$

For each t ∈ [0,∞), (x, y) ∈ Z we have that ηxy(·;t) is a subprobability measure on [0,∞). Also we consider the measures θxy(drdt) = ηxy(dr;t)dt on [0,∞) × [0,∞) as equipped with the topology that generalizes the weak convergence of probability measures to general measures that have at most mass T on [0,∞) × [0, T]. This can be defined in terms of a distance (a generalization of the Prohorov metric) d<sup>T</sup> ,and the metric on measures on [0,∞) × [0,∞) is

<span id="page-24-1"></span>
$$
\sum_{T \in \mathbb{N}} 2^{-T} \left[ d_T(\boldsymbol{\mu}|_T, \boldsymbol{\nu}|_T) \vee 1 \right],\tag{5.4}
$$

where µ|<sup>T</sup> denotes the restriction to [0, T] in the last variable.

Let θ n,δ <sup>=</sup> {<sup>θ</sup> n,δ}(x,y)∈Z be the random measures that correspond to <sup>µ</sup> n,δ , q n,δ , according to the construction above. We observe that

$$
\boldsymbol{\mu}^{n,\delta}(t) = \boldsymbol{m}^n + \sum_{(x,y)\in\mathcal{Z}} \boldsymbol{v}_{xy} \int_0^{t\wedge T^{n,\delta}} \int_0^\infty r \theta_{xy}^{n,\delta}(drds) + \text{ a martingale},
$$

where the martingale will converge to zero as n → ∞, and that for every (x, y) ∈ Z,

<span id="page-24-0"></span>
$$
\mathbb{E}_{\boldsymbol{m}^n} \left[ \int_0^{T^{n,\delta}} F_{xy}(q_{xy}^{n,\delta}(t)) \mu_x^{n,\delta}(t) dt \right] = \mathbb{E}_{\boldsymbol{m}^n} \left[ \int_0^{T^{n,\delta}} \int_0^T F_{xy}(r) \theta_{xy}^{n,\delta}(dr) \right]. \tag{5.5}
$$

We will split the proof of [\(5.3\)](#page-23-1) in three parts. First we prove that (µ n,δ , θ n,δ, T n,δ) is tight. Then we show that for every limit point (µ δ , θ δ , T<sup>δ</sup> ), θ<sup>δ</sup> xy has the decomposition θ δ xy(drdt) = η δ xy(dr;t)dt, with P <sup>y</sup>∈X η δ xy([0,∞);t) = µ δ x (t), and for q <sup>δ</sup> defined by µ δ x (t)q δ xy(t) = <sup>R</sup> <sup>∞</sup> 0 rη<sup>δ</sup> xy(dr;t), that

$$
\boldsymbol{\mu}^{\delta}(t) = \boldsymbol{m} + \sum_{(x,y)\in\mathcal{Z}} \boldsymbol{v}_{xy} \int_0^{t\wedge T^{\delta}} \int_0^{\infty} r \theta_{xy}^{\delta}(drds) = \boldsymbol{m} + \sum_{(x,y)\in\mathcal{Z}} \boldsymbol{v}_{xy} \int_0^{t\wedge T^{\delta}} \mu_x^{\delta}(s) q_{xy}^{\delta}(s) ds.
$$

Finally, by an application of Fatou's Lemma, for such a q δ , we get

$$
\liminf_{n\to\infty} \mathbb{E}_{m^n} \Biggl[ \int_0^{T^n \delta} F_{xy}(r) \theta_{xy}^{n,\delta}(drdt) \Biggr] \geq \mathbb{E}_{m} \Biggl[ \int_0^{T^\delta} \int_{0}^{\infty} F_{xy}(r) \theta_{xy}^{\delta}(drdt) \Biggr] \geq \mathbb{E}_{m} \Biggl[ \int_0^{T^\delta} \int_{0}^{\infty} F_{xy}(r) \eta_{xy}^{\delta}(dr;t) dt \Biggr] \geq \mathbb{E}_{m} \Biggl[ \int_0^{T^\delta} F_{xy} \left( \int_0^{\infty} r \frac{\eta_{xy}^{\delta}(dr;t)}{\eta_{xy}^{\delta}([0,\infty);t)} \right) \eta_{xy}^{\delta}([0,\infty);t) dt \Biggr] = \mathbb{E}_{m} \Biggl[ \int_0^{T^\delta} F_{xy}(q_{xy}^{\delta}(t)) \mu_x^{\delta}(t) dt \Biggr],
$$

where for the third estimate, we applied Jensen's inequality. Together with µ n,δ <sup>→</sup> <sup>µ</sup> δ , Fxy, R ≥ 0 and another application of Fatou's Lemma, this gives [\(5.3\)](#page-23-1).

#### 5.1 Tightness of (µ n,δ , θ n,δ, T n,δ)

First, we prove that (µ n,δ(·), T n,δ), which takes values in <sup>D</sup>([0,∞);P(<sup>X</sup> ))<sup>×</sup> [0,∞) <sup>⊂</sup> <sup>D</sup>([0,∞); <sup>R</sup> d )× [0,∞), is tight. For that, we introduce some auxiliary random variables µ˜ n,δ in <sup>D</sup>([0,∞); <sup>R</sup> d ), to compare with µ n,δ, given by

<span id="page-25-0"></span>
$$
\tilde{\boldsymbol{\mu}}^{n,\delta}(t) = \boldsymbol{m}^n + \sum_{(x,y)\in\mathcal{Z}} \boldsymbol{v}_{xy} \int_0^{t \wedge T^{n,\delta}} \mu_x^n(s) q_{xy}^n(s) ds. \tag{5.6}
$$

Since γxyℓ (·/γxy) ≤ Fxy(·), recalling [\(5.1\)](#page-23-2), [\(5.2\)](#page-23-0) and that R is bounded away from zero in K<sup>δ</sup> = {m : <sup>d</sup>(m, K) <sup>≥</sup> <sup>δ</sup>} by a constant <sup>R</sup><sup>δ</sup> min, we get

<span id="page-25-1"></span>
$$
\mathbb{E}_{\boldsymbol{m}^n} \left[ \int_0^{T^{n,\delta}} \left( \sum_{(x,y)\in\mathcal{Z}} \mu^n_x(t) \gamma_{xy} \ell \left( \frac{q^n_{xy}(t)}{\gamma_{xy}} \right) \right) dt + R^{\delta}_{\min} T^{n,\delta} \right] \le c + 1,
$$
\n(5.7)

which shows tightness of {T n,δ}. By setting <sup>γ</sup>max = max{γxy : (x, y) ∈ Z}, we get

$$
\mathbb{E}_{\boldsymbol{m}^n} \left[ \int_0^{T^{n,\delta}} \left( \sum_{(x,y)\in\mathcal{Z}} \gamma_{\max} \frac{\mu_x^n(t)\gamma_{xy}}{\gamma_{\max}} \ell\left(\frac{q_{xy}^n(t)}{\gamma_{xy}}\right) \right) dt + R_{\min}^{\delta} T^{n,\delta} \right] \le c + 1.
$$

Using the fact that ℓ is convex and ℓ(1) = 0, by Jensen's inequality aℓ(b) ≥ ℓ(ab + 1 − a) for a ∈ [0, 1] and b ≥ 0. By setting a = µ n <sup>x</sup>(t)γxy γmax , the inequality above gives

$$
\mathbb{E}_{\mathbf{m}^n} \left[ \int_0^{T^{n,\delta}} \left( \sum_{(x,y)\in\mathcal{Z}} \gamma_{\max} \ell \left( \frac{\mu_x^n(t)}{\gamma_{\max}} q_{xy}^n(t) + 1 - \frac{(\mu_x^n(t)\gamma_{xy})}{\gamma_{\max}} \right) \right) dt + R_{\min}^{\delta} T^{n,\delta} \right] \leq c + 1.
$$

By applying Jensen's inequality once more

$$
\mathbb{E}_{\boldsymbol{m}^n} \left[ \int_0^{T^{n,\delta}} |\mathcal{Z}| \gamma_{\max} \ell \left( \frac{1}{|\mathcal{Z}| \gamma_{\max}} \sum_{(x,y) \in \mathcal{Z}} \mu_x^n(t) q_{xy}^n(t) + \sum_{(x,y) \in \mathcal{Z}} \left[ 1 - \frac{(\mu_x^n(t) \gamma_{xy})}{|\mathcal{Z}| \gamma_{\max}} \right] \right) dt + R_{\min}^{\delta} T^{n,\delta} \right] \leq c + 1.
$$

Now by multiplying with <sup>1</sup> |Z|γmax , using [\(5.6\)](#page-25-0) and the fact that q ≤ q ′ implies ℓ(q) ≤ ℓ(q ′ ) + 1, we get

$$
\mathbb{E}_{\boldsymbol{m}^n}\left[\int_0^{T^{n,\delta}}\ell\left(\frac{|\dot{\tilde{\mu}}^{n,\delta}(t)|}{|\mathcal{Z}|\gamma_{\max}}\right)dt+\left(\frac{1}{|\mathcal{Z}|\gamma_{\max}}R_{\min}^{\delta}-1\right)T^{n,\delta}\right] \leq \frac{c+1}{|\mathcal{Z}|\gamma_{\max}}.
$$

Finally, by using that for every ¯c > 0 there exists c<sup>1</sup> > 0, c<sup>2</sup> < ∞ such that ℓ(¯cq) ≥ c1ℓ(q) − c2, we get

$$
\mathbb{E}_{\boldsymbol{m}^n} \left[ \int_0^{T^{n,\delta}} c_1 \ell\left( |\dot{\boldsymbol{\mu}}^{n,\delta}(t)| \right) dt + \left( \frac{1}{|\mathcal{Z}| \gamma_{\max}} R_{\min}^{\delta} - 1 - c_2 \right) T^{n,\delta} \right] \le \frac{c+1}{|\mathcal{Z}| \gamma_{\max}},
$$

which implies

$$
\mathbb{E}_{\mathbf{m}^n} \left[ \int_0^{T^{n,\delta}} \ell\left( |\dot{\tilde{\boldsymbol{\mu}}}^{n,\delta}(t)| \right) dt + \frac{1}{|\mathcal{Z}| \gamma_{\max} c_1} R_{\min}^{\delta} T^{n,\delta} \right] \leq \frac{c+1}{|\mathcal{Z}| \gamma_{\max} c_1} + \frac{(c_2+1)}{c_1} \mathbb{E}_{\mathbf{m}^n} [T^{n,\delta}] \leq c',
$$

where

<span id="page-26-1"></span>
$$
c' = \frac{c+1}{|\mathcal{Z}|\gamma_{\text{max}}c_1} + \frac{(c+1)(c_2+1)}{c_1}.
$$
\n(5.8)

<span id="page-26-0"></span>It will follow from the following lemma that µ˜ n,δ is a tight sequence in <sup>D</sup>([0,∞); <sup>R</sup> d ). Let S be the elements (µ, T) of C([0,∞);P(X )) × [0,∞) that satisfy µ(t) = µ(T) for t ≥ T.

Lemma 5.1 For every positive number a, the function

$$
H(\boldsymbol{\mu}, T) = \begin{cases} \int_0^T \ell(|\dot{\boldsymbol{\mu}}(t)|) dt + aT, & \boldsymbol{\mu} \in AC([0, \infty); \mathbb{R}^d), T \in [0, \infty) \\ \infty, & otherwise, \end{cases}
$$

is a tightness function on S, where AC([0,∞); R d ) is the set of all absolutely continuous functions from [0,∞) to R d .

The proof of this lemma is in Appendix [C.](#page-40-0) Using the bound [\(5.1\)](#page-25-1), it follows from Lemma [5.1](#page-26-0) that {µ˜ n,δ} is tight in D([0,∞); R d ). Now we have that

$$
|\boldsymbol{\mu}^{n,\delta}(t)-\tilde{\boldsymbol{\mu}}^{n,\delta}(t)|\leq \sum_{(x,y)\in\mathcal{Z}}\left|\int_0^{t\wedge T^{n,\delta}}\mu^n_x(s)q^n_{xy}(s)ds-\int_0^{t\wedge T^{n,\delta}}\int_0^\infty1_{[0,\mu^n_x(s)q^n_{xy}(s)]}(r)\frac{1}{n}N^n_{xy}(dsdr)\right|,
$$

where the summands on the right side, denoted from now on by Q n,δ xy,t, are all martingales with quadratic variation Q n,δ xy,t that is bounded above by

$$
\frac{1}{n^2} \mathbb{E}_{\boldsymbol{m}^n} \left[ \int_0^{t \wedge T^{n,\delta}} \int_0^{\infty} 1_{[0,\mu_x^n(s)q_{xy}^n(s)]}(r) N_{xy}^n(ds dr) \right] = \frac{1}{n} \mathbb{E}_{\boldsymbol{m}^n} \left[ \int_0^{t \wedge T^{n,\delta}} \mu_x^n(s) q_{xy}^n(s) ds \right]
$$
\n
$$
\leq \frac{1}{n} \mathbb{E}_{\boldsymbol{m}^n} \left[ \int_0^{t \wedge T^{n,\delta}} (\ell(\mu_x^n(s)q_{xy}^n(s)) + e) ds \right] \stackrel{(5.8)}{\leq} \frac{c' + e \mathbb{E}_{\boldsymbol{m}^n} [T^{n,\delta} \wedge t]}{n} \leq \frac{c' + e \mathbb{E}_{\boldsymbol{m}^n} [T^{n,\delta}] \stackrel{(5.7)}{\leq} \frac{\left(\frac{(c+1)e}{R_{\min}^{\delta}} + c'\right)}{n},
$$

where in the first inequality of the last line, the estimate ab ≤ e <sup>a</sup> + ℓ(b), with a = 1, b = µ n x (s)q n xy(s) was used. By using the Burkholder-Gundy-Davis inequality, for every T ∈ (0,∞)

<span id="page-26-2"></span>
$$
\mathbb{E}_{\boldsymbol{m}^{n}}\left[\sup_{t\in[0,T]}|Q_{xy,t}^{n,\delta}|\right] \leq c_{BGD}\mathbb{E}_{\boldsymbol{m}^{n}}[\mathbb{Q}_{xy}^{n,\delta}]_{T}^{1/2} \leq c_{BGD}\sqrt{\frac{\left(\frac{(c+1)e}{R_{\min}^{\delta}}+c'\right)}{n}},\tag{5.9}
$$

from which we get that Em<sup>n</sup> [supt∈[0,T] |Q n,δ xy,t|] converges to zero as n → ∞. Recalling that we already proved {µ˜ n,δ} is tight in <sup>D</sup>([0,∞); <sup>R</sup> d ), it follows from Em<sup>n</sup> d(µ n,δ , µ˜ n,δ) → 0 that {(µ n,δ, T n,δ)} is tight as well.

To show that the variable θ n,δ is tight, we combine [\(5.5\)](#page-24-0) and [\(5.1\)](#page-23-2), [\(5.2\)](#page-23-0) and use the monotonicity with respect to δ to get

$$
\mathbb{E}_{\boldsymbol{m}^n}\left[\sum_{(x,y)\in\mathcal{Z}}\int_0^{T^{n,\delta}}\int_0^\infty F_{xy}(r)\theta_{xy}^{n,\delta}(drdt)+\int_0^{T^{n,\delta}}R(\boldsymbol{\mu}^{n,\delta}(t))\right]
$$

Since, by part 1 of Lemma [3.7,](#page-9-0) we have γxyℓ (·/γxy) ≤ Fxy(·), and q n,δ = γ for t > T n,δ, we get

$$
\mathbb{E}_{\mathbf{m}^n} \left[ \sum_{(x,y)\in\mathcal{Z}} \int_0^\infty \int_0^\infty \gamma_{xy} \ell\left(\frac{r}{\gamma_{xy}}\right) \theta_{xy}^{n,\delta} (drdt) \right] = \mathbb{E}_{\mathbf{m}^n} \left[ \sum_{(x,y)\in\mathcal{Z}} \int_0^{T^{n,\delta}} \int_0^\infty \gamma_{xy} \ell\left(\frac{r}{\gamma_{xy}}\right) \theta_{xy}^{n,\delta} (drdt) \right] < c+1.
$$

Now by using the fact that

$$
\tilde{H}(\theta) = \int_0^\infty \int_0^T \gamma_{xy} \ell\left(\frac{r}{\gamma_{xy}}\right) \theta(dr dt),
$$

is a tightness function on the space of measures on [0,∞) × [0, T] with mass no greater than T, we conclude that for every (x, y) ∈ Z, θn,δ xy is tight with the topology introduced in [\(5.4\)](#page-24-1).

#### 5.2 Distributional limits and the lower bound

From the previous two subsections we have that (µ n,δ , µ˜ n,δ , θ n,δ, T n,δ), is tight. For proving the lower bound, we can assume without loss that the sequence has a distributional limit (µ δ , µ˜ δ , θ δ , T<sup>δ</sup> ). By using the Skorohod representation theorem we can also assume the sequence of variables is on the same probability space (Ω, F, P), and that (µ δ , µ˜ δ , θ δ , T<sup>δ</sup> ) is an a.s. pointwise limit.

Consider any ω ∈ Ω for which there is convergence. Since by the definition of θ n,δ

$$
\theta_{xy}^{n,\delta}([0,\infty)\times A)=\int_{A\cap[0,T^{n,\delta}]} \hspace{-0.2cm}\mu^{n,\delta}_x(t)dt,\,\forall A\in\mathcal{B}(\mathbb{R}),
$$

for every continuity set A of θ δ xy([0,∞) × ·) we have

$$
\left| \theta_{xy}^{\delta}([0,\infty) \times A) - \int_{A \cap [0,T^{\delta}]} \mu_x^{\delta}(t) dt \right| \leq \left| \theta_{xy}^{\delta}([0,\infty) \times A) - \theta_{xy}^{n,\delta}([0,\infty) \times A) \right| + \left| \int_{A \cap [0,T^{n,\delta}]} \mu_x^{n,\delta}(t) dt - \int_{A \cap [0,T^{\delta}]} \mu_x^{\delta}(t) dt \right|
$$
  
\n
$$
\leq \left| \theta_{xy}^{\delta}([0,\infty) \times A) - \theta_{xy}^{n,\delta}([0,\infty) \times A) \right| + \left| \int_{A \cap [0,T^{\delta}]} \mu_x^{n,\delta}(t) dt - \int_{A \cap [0,T^{\delta}]} \mu_x^{\delta}(t) dt \right| + \int_{A \cap [min\{T^{n,\delta},T^{\delta}\}, \max\{T^{\delta},T^{n,\delta}\}]} \mu_x^{\delta}(t) dt
$$
  
\n
$$
\leq \left| \theta_{xy}^{\delta}([0,\infty) \times A) - \theta_{xy}^{n,\delta}([0,\infty) \times A) \right| + d(\mu_x^{n,\delta},\mu_x^{\delta}) + |T^{\delta} - T^{n,\delta}| \to 0.
$$

Therefore for every continuity set A of θ δ xy([0,∞) × ·)

$$
\theta_{xy}^{\delta}([0,\infty) \times A) = \int_{A \cap [0,T^{\delta}]} \mu_x^{\delta}(t) dt,
$$

from which we conclude that for all (x, y) ∈ Z, θ<sup>δ</sup> xy has the decomposition θ δ xy(drdt) = η δ xy(dr;t)dt, with η δ xy([0,∞);t) = µ δ x (t). Also, since R <sup>∞</sup> 0 R <sup>∞</sup> 0 ℓ(r)θ n,δ xy (drdt) is uniformly bounded and ℓ is superlinear, we have convergence of the first moments of the first marginal, i.e.,

$$
\int_{\mathbb{R}} f(t)r \theta_{xy}^{n,\delta}(drdt) \to \int_{\mathbb{R}} f(t)r \theta_{xy}^{\delta}(dt), \quad \forall f \in C_b(\mathbb{R}).
$$

Hence for q <sup>δ</sup> defined by µ δ x (t)q δ xy(t) = <sup>R</sup> <sup>∞</sup> 0 rη<sup>δ</sup> xy(dr;t), we get that for all (x, y) ∈ Z

<span id="page-28-0"></span>
$$
\int_0^\infty f(t)\mu_x^{n,\delta}(t)q_{xy}^{n,\delta}(t)dt \to \int_0^\infty f(t)\mu_x^{\delta}(t)q_{xy}^{\delta}(t)dt, \quad \forall f \in C_b(\mathbb{R}).\tag{5.10}
$$

Using the fact that d(µ n,δ , µ˜ n,δ) <sup>→</sup> 0 and [\(5.6\)](#page-25-0), we get

<span id="page-28-1"></span>
$$
\left|\boldsymbol{\mu}^{n,\delta}(t) - \boldsymbol{m}^n - \sum_{(x,y)\in\mathcal{Z}} \boldsymbol{v}_{xy} \int_0^{T^{n,\delta}\wedge t} \mu_x^{n,\delta}(s) q_{xy}^{n,\delta}(s) ds \right| = \left|\boldsymbol{\mu}^{n,\delta}(t) - \tilde{\boldsymbol{\mu}}^{n,\delta}(t)\right| \to 0,
$$
 (5.11)

for a.e. t. Applying [\(5.10\)](#page-28-0) for suitable choices of f and using [\(5.11\)](#page-28-1),

$$
\boldsymbol{\mu}^{\delta}(t) = \boldsymbol{m} + \sum_{(x,y) \in \mathcal{Z}} \boldsymbol{v}_{xy} \int_0^{T^{\delta} \wedge t} \mu^{\delta}_x(s) q^{\delta}_{xy}(s) ds
$$

for a.e. t, and since the left side is cadlag and the right side is continuous in the last display, equality holds for t ≥ 0. We conclude that q δ is the control that generates µ δ , and we also already noticed that µ δ x (t)q δ xy(t) = <sup>R</sup> <sup>∞</sup> 0 rη<sup>δ</sup> xy(dr;t). Finally, since µ n,δ(T n,δ) <sup>∈</sup> <sup>K</sup><sup>δ</sup> and <sup>d</sup>(<sup>µ</sup> n,δ , µ δ ) → 0, by continuity of µ <sup>δ</sup> we get µ δ (T δ ) ∈ Kδ. As discussed below [\(5.5\)](#page-24-0), this concludes the lower bound proof.

## 6 Upper bound

Before we proceed with the proof of the upper bound

$$
\limsup_{n\to\infty}V_K^n(\boldsymbol{m}^n)\leq V_K(\boldsymbol{m}),
$$

<span id="page-28-4"></span>we establish some preliminary lemmas. In the following lemmas, we make use of Tm, U<sup>m</sup> and Fxy, defined in [\(4.1\)](#page-18-0), [\(4.2\)](#page-19-3), and [\(3.3\)](#page-7-4) respectively. For the properties of Fxy, see Lemma [3.7.](#page-9-0)

Lemma 6.1 Let m ∈ P∗(X ), and q ∈ U<sup>m</sup> be such that (µ, q) ∈ Tm. Given T < ∞ and ǫ > 0, we can find a1, a2, a<sup>3</sup> ∈ (0,∞) and q˜ ∈ Um, with (µ˜, q˜) ∈ Tm, such that

<span id="page-28-2"></span>
$$
a_1 \leq \inf_{(x,y)\in\mathcal{Z},t\in[0,T]} \tilde{q}_{xy}(t) \leq \sup_{(x,y)\in\mathcal{Z},t\in[0,T]} \tilde{q}_{xy}(t) \leq a_2, \quad \inf_{x\in\mathcal{X},t\in[0,T]} \tilde{\mu}_x(t) > a_3, \quad \sup_{t\in[0,T]} \|\mu(t) - \tilde{\mu}(t)\| < \epsilon,
$$
  
and 
$$
\sum_{(x,y)\in\mathcal{Z}} \int_0^T \tilde{\mu}_x(t) F_{xy}(\tilde{q}_{xy}(t)) dt \leq \sum_{(x,y)\in\mathcal{Z}} \int_0^T \mu_x(t) F_{xy}(q_{xy}(t)) dt.
$$
 (6.1)

Proof. Recall that m ∈ P∗(X ) implies m<sup>x</sup> > 0 for all x ∈ X . Let ν(m, t) be the solution to the equation ν˙(t) = γν(t), with initial data m. By Remark [4.6,](#page-20-3) we know that there exists 1 ≥ a > 0 such that ν(m, t) ∈ Pa(X ), for every t ∈ [0, T]. We can assume without loss that the right hand side on the second line of [\(6.1\)](#page-28-2) is greater than zero, since if not true then the controlled rates are γ and the conclusion of the lemma is automatic. For <sup>ǫ</sup> <sup>2</sup> ≥ δ > 0, let

<span id="page-28-3"></span>
$$
\boldsymbol{\mu}^{\delta}(\cdot) \doteq \delta \boldsymbol{\nu}(\boldsymbol{m},\cdot) + (1-\delta)\boldsymbol{\mu}(\cdot),\tag{6.2}
$$

and note that µ δ x (t) > 0 for every t ∈ [0, T] and x ∈ X . Therefore, for δ as above and (x, y) ∈ Z, we can define

<span id="page-29-4"></span>
$$
q_{xy}^{\delta}(\cdot) = \gamma_{xy} \frac{\delta \nu_x(\boldsymbol{m},\cdot)}{\mu_x^{\delta}(\cdot)} + q_{xy}(\cdot) \frac{(1-\delta)\mu_x(\cdot)}{\mu_x^{\delta}(\cdot)}.
$$
\n(6.3)

Then it is straightforward to check that (µ δ , q δ ) ∈ Tm. Moreover, since δνx(m,t) µδ <sup>x</sup>(t) + (1−δ)µx(t) µδ <sup>x</sup>(t) = 1 for all t ∈ [0, T], by the convexity of F we obtain

$$
\sum_{(x,y)\in\mathcal{Z}}\int_0^T\mu_x^\delta(t)F_{xy}\left(q_{xy}^\delta(t)\right)dt = \sum_{(x,y)\in\mathcal{Z}}\int_0^T\mu_x^\delta(t)F_{xy}\left(\gamma_{xy}\frac{\delta\nu_x(m,t)}{\mu_x^\delta(t)} + q_{xy}\frac{(1-\delta)\mu_x(t)}{\mu_x^\delta(t)}\right)dt \le
$$
\n
$$
\sum_{(x,y)\in\mathcal{Z}}\int_0^T\mu_x^\delta(t)\frac{\delta\nu_x(m,t)}{\mu_x^\delta(t)}F_{xy}\left(\gamma_{xy}\right)dt + \sum_{(x,y)\in\mathcal{Z}}\int_0^T\mu_x^\delta(t)\frac{(1-\delta)\mu_x(t)}{\mu_x^\delta(t)}F_{xy}\left(q_{xy}(t)\right)dt \le (1-\delta)\sum_{(x,y)\in\mathcal{Z}}\int_0^T\mu_x(t)F_{xy}\left(q_{xy}(t)\right)dt,
$$

where in the second inequality, we used the fact that F <sup>∞</sup>(γxy) = 0 [see Lemma [3.7\]](#page-9-0). Therefore, we get a couple (µ δ , q δ ) ∈ T<sup>m</sup> with cost strictly less than the initial one, and with µ δ that satisfies

<span id="page-29-2"></span>
$$
\mu_x^{\delta}(t) \ge \delta a \quad \text{and} \quad \frac{(1-\delta)\mu_x(t)}{\mu_x^{\delta}(t)} \le \frac{(1-\delta)}{\delta a + (1-\delta)} \equiv c < 1,\tag{6.4}
$$

for all t ∈ [0, T]. However, since this couple does not necessarily satisfy condition [\(6.1\)](#page-28-2), we modify it even further. Specifically, we pick M ∈ (2γmax,∞) big enough such that

<span id="page-29-1"></span>
$$
\sum_{(x,y)\in\mathcal{Z}} \int_0^T \mu_x^\delta(t) \left| \min\left\{ q_{xy}^\delta(t), M\right\} - q_{xy}^\delta(t) \right| dt \le \frac{a\delta(1-\sqrt{c})}{\sqrt{2}},\tag{6.5}
$$

and define

<span id="page-29-0"></span>
$$
\boldsymbol{\mu}^{\delta, M}(t) = \int_0^t \sum_{(x,y)\in\mathcal{Z}} \mu_x^{\delta}(t) \min\left\{ q_{xy}^{\delta}(t), M\right\} \boldsymbol{v}_{xy} dt.
$$
 (6.6)

Then

<span id="page-29-3"></span>
$$
\left| \mu_x^{\delta, M}(t) - \mu_x^{\delta}(t) \right| \leq \left\| \mu^{\delta, M}(t) - \mu^{\delta}(t) \right\| \stackrel{(6.6)}{=} \left\| \sum_{(x,y)\in\mathcal{Z}} \int_0^T \left( \mu_x^{\delta}(t) \left( q_{xy}^{\delta}(t) - \min \left\{ q_{xy}^{\delta}(t), M \right\} \right) \right) \mathbf{v}_{xy} dt \right\|
$$
  
\n
$$
\leq \sum_{(x,y)\in\mathcal{Z}} \int_0^T \left| \mu_x^{\delta}(t) \left( q_{xy}^{\delta}(t) - \min \left\{ q_{xy}^{\delta}(t), M \right\} \right) \right| ||\mathbf{v}_{xy}|| dt \qquad (6.7)
$$
  
\n
$$
\leq \sqrt{2} \sum_{(x,y)\in\mathcal{Z}} \int_0^T \left( \mu_x^{\delta, M}(t) \left( q_{xy}^{\delta}(t) - \min \left\{ q_{xy}^{\delta}(t), M \right\} \right) \right) dt \stackrel{(6.5)}{\leq} a\delta(1 - \sqrt{c}),
$$

and therefore for t ∈ [0, T],

$$
\mu_x^{\delta,M}(t) \ge \mu_x^{\delta}(t) - \left| \mu_x^{\delta,M}(t) - \mu_x^{\delta}(t) \right| \stackrel{(6.4)}{\ge} a\delta - \left| \mu_x^{\delta,M}(t) - \mu_x^{\delta}(t) \right| \stackrel{(6.7)}{\ge} a\delta\sqrt{c}.
$$
 (6.8)

We also get

$$
\left|1 - \frac{\mu_x^{\delta, M}(t)}{\mu_x^{\delta}(t)}\right| \stackrel{(6.7)}{\leq} \frac{a\delta(1 - \sqrt{c})}{\min_x \mu_x^{\delta}(t)} \stackrel{(6.4)}{\leq} (1 - \sqrt{c})
$$

or

<span id="page-30-0"></span>
$$
\frac{\mu_x^{\delta}(t)}{\mu_x^{\delta,M}(t)} \ge \frac{1}{2 - \sqrt{c}} \quad \text{and} \quad \frac{\mu_x^{\delta}(t)}{\mu_x^{\delta,M}(t)} \le \frac{1}{\sqrt{c}} = \frac{\sqrt{c}}{c}.
$$
\n(6.9)

We deduce that µ δ,M(t) ∈ P∗(<sup>X</sup> ), for all <sup>t</sup> <sup>∈</sup> [0, T], and therefore can define

<span id="page-30-1"></span>
$$
q_{xy}^{\delta,M}(t) = \frac{\min\left\{q_{xy}^{\delta}(t), M\right\}\mu_x^{\delta}(t)}{\mu_x^{\delta,M}(t)},
$$
\n(6.10)

which will give (µ δ,M, q δ,M) ∈ Tm. We can see that [\(6.1\)](#page-28-2) is satisfied, since by [\(6.3\)](#page-29-4) and the first inequality in [\(6.9\)](#page-30-0) for the bound from below and the second inequality in [\(6.9\)](#page-30-0) for the bound from above we have

$$
\frac{\gamma_{xy}\delta\nu_x(\boldsymbol{m},\cdot)}{2}\leq q_{xy}^{\delta,M}(t)\leq M\frac{\sqrt{c}}{c}
$$

It is worth mentioning at this point that trying to get an estimate for the cost of (µ δ,M, q δ,M), with respect to the cost of (µ δ , q δ ), would require some extra properties of F. However, we can obtain an estimate of the cost (µ δ,M, q δ,M) with respect to the cost of the initial triplet (µ, q), by utilizing only the convexity of Fxy, and choosing the right parameters. Using the fact that Fxy is increasing on [γxy,∞) in the first inequality, and that Mµ<sup>δ</sup> x (t)/µδ,M <sup>x</sup> (t) ≥ γxy by [\(6.9\)](#page-30-0) and M ≥ 2γxy,

<span id="page-30-2"></span>
$$
F_{xy}\left(q_{xy}^{\delta,M}(t)\right) \stackrel{(6.10)}{=} F_{xy}\left(\frac{\min\left\{q_{xy}^{\delta}(t),M\right\}\mu_{x}^{\delta}(t)}{\mu_{x}^{\delta,M}(t)}\right) \leq F_{xy}\left(\frac{q_{xy}^{\delta}(t)\mu_{x}^{\delta}(t)}{\mu_{x}^{\delta,M}(t)}\right) \stackrel{(6.3)}{=} F_{xy}\left(\frac{q_{xy}^{\delta}(t)\mu_{x}^{\delta}(t)}{\mu_{x}^{\delta,M}(t)}\right) \stackrel{(6.3)}{=} F_{xy}\left(\frac{\mu_{x}^{\delta}(t)}{\mu_{x}^{\delta,M}(t)}\mu_{x}^{\delta}(t)\right) \quad (6.11)
$$

However, from [\(6.4\)](#page-29-2) and [\(6.9\)](#page-30-0), we have

$$
\frac{(1-\delta)\mu_x(t)}{\mu_x^{\delta,M}(t)} = \frac{(1-\delta)\mu_x(t)}{\mu_x^{\delta}(t)} \frac{\mu_x^{\delta}(t)}{\mu_x^{\delta,M}(t)} \le c \frac{\sqrt{c}}{c} = \sqrt{c} < 1.
$$

Therefore using the convexity of F we have

<span id="page-30-3"></span>
$$
F_{xy}\left(\gamma_{xy}\frac{\delta\nu_x(\mathbf{m},t)}{\mu_x^{\delta,M}(t)} + q_{xy}(t)\frac{(1-\delta)\mu_x(t)}{\mu_x^{\delta,M}(t)}\right) = F_{xy}\left(\frac{\left(1-\frac{(1-\delta)\mu_x(t)}{\mu_x^{\delta,M}(t)}\right)}{\left(1-\frac{(1-\delta)\mu_x(t)}{\mu_x^{\delta,M}(t)}\right)}\gamma_{xy}\frac{\delta\nu_x(\mathbf{m},t)}{\mu_x^{\delta,M}(t)} + q_{xy}(t)\frac{(1-\delta)\mu_x(t)}{\mu_x^{\delta,M}(t)}\right) \n\leq \left(1-\frac{(1-\delta)\mu_x(t)}{\mu_x^{\delta,M}(t)}\right)F_{xy}\left(\gamma_{xy}\frac{\delta\nu_x(\mathbf{m},t)}{\mu_x^{\delta,M}(t) - (1-\delta)\mu_x(t)}\right) + \frac{(1-\delta)\mu_x(t)}{\mu_x^{\delta,M}(t)}F_{xy}\left(q_{xy}(t)\right).
$$
\n(6.12)

Combining [\(6.11\)](#page-30-2) and [\(6.12\)](#page-30-3) and then using [\(6.2\)](#page-28-3), we obtain

<span id="page-31-0"></span>
$$
\mu_x^{\delta, M}(t) F_{xy} \left( q_{xy}^{\delta, M}(t) \right)
$$
\n
$$
\leq \left( \mu_x^{\delta, M}(t) - (1 - \delta) \mu_x(t) \right) F_{xy} \left( \gamma_{xy} \frac{\delta \nu_x(\mathbf{m}, t)}{\mu_x^{\delta, M}(t) - (1 - \delta) \mu_x(t)} \right) + (1 - \delta) \mu_x(t) F_{xy} \left( q_{xy}(t) \right)
$$
\n
$$
= \left( \mu_x^{\delta, M}(t) - \mu_x^{\delta}(t) + \delta \nu_x(M, t) \right) F_{xy} \left( \gamma_{xy} \frac{\delta \nu_x(\mathbf{m}, t)}{\mu_x^{\delta, M}(t) - \mu_x^{\delta}(t) + \delta \nu_x(\mathbf{m}, t)} \right) + (1 - \delta) \mu_x(t) F_{xy} \left( q_{xy}(t) \right).
$$
\n(6.13)

We can make |µ δ,M <sup>x</sup> (t) − µ δ x (t)| uniformly as close to zero as desired and therefore we can make the quantity γxy δνx(m,t) µ δ,Mx (t)−µ<sup>δ</sup> <sup>x</sup>(t)+δνx(m,t) as close to γxy as desired by picking M sufficiently large. Since Fxy (γxy) = 0 and Fxy (·) is continuous on (0,∞) by Lemma [4.5,](#page-20-1) we can pick M < ∞ such that for every t ∈ [0, T],

<span id="page-31-1"></span>
$$
F_{xy}\left(\gamma_{xy}\frac{\delta\nu_x(\boldsymbol{m},t)}{\mu_x^{\delta,M}(t)-\mu_x^{\delta}(t)+\delta\nu_x(\boldsymbol{m},t)}\right)\leq \frac{1}{2T}\int_0^T\mu_x(s)F_{xy}(q_{xy}(s))ds.
$$
\n(6.14)

Then from [\(6.13\)](#page-31-0) and [\(6.14\)](#page-31-1) and the fact that νx(m, t) ≤ 1 and [\(6.7\)](#page-29-3), for t ∈ [0, T]

$$
\sum_{(x,y)\in\mathcal{Z}}\int_0^T\mu_x^{\delta,M}(t)F_{xy}\left(q_{xy}^{\delta,M}(t)\right)dt \leq \sum_{(x,y)\in\mathcal{Z}}\int_0^T(2\delta)\left(\frac{1}{2T}\int_0^T\mu_x(s)F_{xy}(q_{xy}(s))ds\right)dt
$$
$$
+\int_0^T(1-\delta)\mu_x(t)F_{xy}(q_{xy}(t))dt = \sum_{(x,y)\in\mathcal{Z}}\int_0^T\mu_x(t)F_{xy}(q_{xy}(t))dt.
$$

<span id="page-31-3"></span>Next, we are going to prove the following result.

Lemma 6.2 (Law of large numbers) Let T ∈ (0,∞) be given. There exists a constant c < ∞ such that if (µ n , <sup>γ</sup>) ∈ T <sup>n</sup><sup>m</sup> (see [\(2.6\)](#page-6-2)), and (ν, <sup>γ</sup>) ∈ Tm, then

<span id="page-31-2"></span>
$$
\mathbb{P}\left(\sup_{t\in[0,T]}\|\boldsymbol{\mu}^n(t)-\boldsymbol{\nu}(\boldsymbol{m},t)\|\geq\epsilon\right)\leq\frac{c}{\epsilon\sqrt{n}}.\tag{6.15}
$$

Proof. We have

$$
\begin{split} \|\pmb{\mu}^{n}(t)-\pmb{\nu}(\pmb{m},t)\| &\leq \sum_{(x,y)} \left|\int_{0}^{t} \int_{0}^{\infty} 1_{[0,\mu_{x}^{n}(s)\gamma_{xy}]}(r) \frac{1}{n} N_{xy}^{n}(ds dr) - \int_{0}^{t} \int_{0}^{\infty} 1_{[0,\nu_{x}(m,s)\gamma_{xy}]}(r) ds dr \right| \\ &\leq \sum_{(x,y)} \left|\int_{0}^{t} \int_{0}^{\infty} 1_{[0,\mu_{x}^{n}(s)\gamma_{xy}]}(r) \frac{1}{n} N_{xy}^{n}(ds dr) - \int_{0}^{t} \int_{0}^{\infty} 1_{[0,\mu_{x}^{n}(s)\gamma_{xy}]}(r) ds dr \right| \\ &+ \sum_{(x,y)} \left|\int_{0}^{t} \int_{0}^{\infty} 1_{[0,\mu_{x}^{n}(s)\gamma_{xy}]}(r) ds dr - \int_{0}^{t} \int_{0}^{\infty} 1_{[0,\nu_{x}(m,s)\gamma_{xy}]}(r) ds \right| .\end{split}
$$

For a constant K that depends on d and the maximum of γxy,

$$
\sum_{(x,y)}\left|\int_0^t\int_0^\infty 1_{[0,\mu_x^n(s)\gamma_{xy}]}(r)dsdr-\int_0^t\int_0^\infty 1_{[0,\nu_x(m,s)\gamma_{xy}]}(r)ds\right|\leq K\sup_{0\leq s\leq t}\left\|\mu^n(s)-\nu(m,s)\right\|.
$$

Hence by Gronwall's inequality, for r ∈ [0, T]

$$
\|\mu^{n}(r)-\nu(m,r)\| \leq e^{KT} \sup_{0\leq t\leq r}\sum_{(x,y)}\left|\int_{0}^{t}\int_{0}^{\infty}1_{[0,\mu_{x}^{n}(s)\gamma_{xy}]}(r)\frac{1}{n}N^{n}_{xy}(dsdr)-\int_{0}^{t}\int_{0}^{\infty}1_{[0,\mu_{x}^{n}(s)\gamma_{xy}]}(r)dsdr\right|.
$$

Using the Burkholder-Gundy-Davis inequality as was done to obtain [\(5.9\)](#page-26-2),

$$
\mathbb{P}\left(\sup_{t\in[0,T]}\left|\int_0^t\int_0^\infty\mathbf{1}_{[0,\mu_x^n(s)\gamma_{xy}]}(r)\frac{1}{n}N_{xy}^n(dsdr)-\int_0^t\int_0^\infty\mathbf{1}_{[0,\mu_x^n(s)\gamma_{xy}]}(r)dsdr\right|\geq\epsilon\right)\leq\frac{\bar{c}}{\epsilon\sqrt{n}},
$$

and hence

$$
\mathbb{P}\left(\sup_{t\in[0,T]}\|\boldsymbol{\mu}^n(t)-\boldsymbol{\nu}(\boldsymbol{m},t)\|\geq\epsilon\right)\leq d^2\frac{e^{KT}\bar{c}}{\epsilon\sqrt{n}},
$$

<span id="page-32-0"></span>which is [\(6.15\)](#page-31-2).

We now obtain the following result.

Lemma 6.3 The sequence V n (m) is bounded, uniformly in n and m ∈ P(X).

Proof. Let τ = diameter(P(X )). By Remark [4.6,](#page-20-3) there exists a > 0 such that ν(m, τ ) ∈ P2a(X ) regardless of the initial data <sup>m</sup>. We can further assume that <sup>P</sup>a(<sup>X</sup> ) <sup>∩</sup> <sup>K</sup>◦ <sup>6</sup><sup>=</sup> <sup>∅</sup>, and in particular that there exists an element <sup>m</sup>˜ such that <sup>B</sup>(m˜ , a/2) ⊂ Pa(<sup>X</sup> ) <sup>∩</sup> <sup>K</sup>◦ .

Since m˜ ∈ Pa(X ), the first part of Theorem [4.7](#page-21-2) implies that for every point m in Pa(X ) we can find a control q<sup>m</sup> with the following properties: there is a unique µ such that (µ, qm) ∈ Tm; µ is a constant speed parametrization of the straight line that connects m to m˜ in time T{m˜ } = km − m˜ k; and the control q<sup>m</sup> satisfies

$$
\gamma_{xy} \le q_{\boldsymbol{m},xy}(t) \le \frac{c_1}{a}
$$

,

for t ∈ [0, T{m˜ } ],(x, y) ∈ Z, where c<sup>1</sup> > 0 is a constant that does not depend on a. For every m, we let

$$
q_{xy}(\boldsymbol{m},t) = \begin{cases} q_{\boldsymbol{m},xy}(t) & t \leq \|\boldsymbol{m} - \tilde{\boldsymbol{m}}\|, \\ \gamma_{xy} & t > \|\boldsymbol{m} - \tilde{\boldsymbol{m}}\|, \end{cases}
$$

denote the control that takes m to m˜ in time km − m˜ k, in the sense that it was described above, and after that time is equal to the original rates.

For i ∈ N we define a control for the interval iτ ≤ t < (i + 1)τ as follows. Let f(t−) denote the limit of f(s) from the left at time t, and recall that µ(m, ·) is the straight line that connects m to m˜ in time T{m˜ } , where m˜ is fixed and we explicitly indicate the dependence on m. Then set

$$
q_{xy}^n(t) = \begin{cases} q_{xy}(\boldsymbol{m}, t - i\tau) \frac{\mu_x^n(t-)}{\mu_x(\boldsymbol{m}, t - i\tau)}, & \text{if } \left( \sup_{s \in [i\tau, t]} \|\boldsymbol{\mu}(\boldsymbol{m}, t) - \boldsymbol{\mu}^n(t)\| \leq \frac{a}{2} \right) \text{ and } (\boldsymbol{\mu}^n(i\tau) = \boldsymbol{m} \in \mathcal{P}_a(\mathcal{X})) \\ \gamma_{xy}, & \text{otherwise.} \end{cases}
$$

,

The idea with these controls is that, within each time interval with length τ , the control considers the starting point m, and then if m ∈ Pa(X ), it attempts to force the process to follow the straight line to m˜ . If m /∈ Pa(X ) or the process goes close to the boundary of the simplex P(X ) \ P∗(X ), then we just use original rates to push the process inside Pa(X ). Since all controls used are bounded from above and below, the total cost is a multiple of E[T n ]. Thus we need only show this expected exit time is uniformly bounded.

By using [\(5.9\)](#page-26-2), we can find constant c < ∞ such that

$$
\mathbb{P}\left(\sup_{t\in[i\tau,(i+1)\tau]}\|\mu^n(t)-\mu(m,t)\|\geq \frac{a}{2}\left|\mu^n(i\tau)=m\in\mathcal{P}_a(\mathcal{X})\right)\leq c\frac{2}{\sqrt{n}a}
$$

from which we get

$$
\mathbb{P}(T^n > (i+1)\tau|\boldsymbol{\mu}^n(i\tau) \in \mathcal{P}_a(X)) \leq \inf_{\boldsymbol{m} \in \mathcal{P}_a(X)} \mathbb{P}\left(\sup_{t \in [i\tau, (i+1)\tau]} \|\boldsymbol{\mu}^n(t) - \boldsymbol{\mu}(\boldsymbol{m},t)\| \geq \frac{a}{2} \middle| \boldsymbol{\mu}^n(i\tau) = \boldsymbol{m}\right) \leq c \frac{2}{\sqrt{n}a}.
$$

By Lemma [6.2,](#page-31-3) we have that for some c ′ <sup>&</sup>lt; <sup>∞</sup>

$$
\mathbb{P}\left(\sup_{t\in[i\tau,(i+1)\tau]}\|\boldsymbol{\mu}^{n}(t)-\boldsymbol{\nu}(\boldsymbol{m},t)\|\geq \frac{a}{2}\,\bigg|\,\boldsymbol{\mu}^{n}(i\tau)=\boldsymbol{m}\notin\mathcal{P}_{a}(\mathcal{X})\right)\leq c'\frac{2}{a\sqrt{n}},
$$

which implies that

that

$$
\mathbb{P}\bigg(\!\!\mu^n((i+1)\tau) \notin \!\mathcal{P}_a(\mathcal{X})\bigg|\mu^n(i\tau) \notin \!\mathcal{P}_a(\mathcal{X})\!\!\bigg) \leq \hspace{-1mm}\inf_{\boldsymbol{m} \notin \mathcal{P}_a(\mathcal{X})} \hspace{-1mm}\mathbb{P}\bigg(\hspace{-1mm}\sup_{t \in [i\tau,(i+1)\tau]}\hspace{-1mm} \|\boldsymbol{\mu}^n(t) - \boldsymbol{\nu}(\boldsymbol{m},t)\| \geq \hspace{-1mm}\frac{a}{2}\hspace{-1mm}\bigg|\mu^n(i\tau) = \hspace{-1mm}\bm{m}\bigg) \leq \hspace{-1mm}\frac{2c'}{a\sqrt{n}}.
$$

Thus the probability to escape in the next 2τ units of time has a positive lower bound that is independent of n and the starting position. This implies the uniform upper bound on the mean escape time.

Now we proceed with the proof of the upper bound. Proof of upper bound. We will initially assume that m is in Pa(X ), for some a > 0. Recall that VK(m) < ∞. Let ǫ > 0. By the definition of VK(m), we can find a pair (µ, q) ∈ T<sup>m</sup> and a T ∈ [0,∞], such

$$
\int_0^T \left( \sum_{(x,y)\in\mathcal{Z}} \mu_x(t) F_{xy} \left( q_{xy}(t) \right) + R(\boldsymbol{\mu}(t)) \right) dt \leq V_K(\boldsymbol{m}) + \epsilon.
$$

Since we assumed that R is bounded from below by a positive constant for every compact subset of K<sup>c</sup> , we can furthermore find a δ such that for finite time T <sup>δ</sup> <sup>∈</sup> [0,∞) we have

$$
\int_0^{T^{\delta}} \left( \sum_{(x,y)\in\mathcal{Z}} \mu_x(t) F_{xy} (q_{xy}(t)) + R(\boldsymbol{\mu}(t)) \right) dt \leq V_K(\boldsymbol{m}) + \epsilon,
$$

and d(µ(T δ ), K) ≤ δ. By the second part of Theorem [4.7,](#page-21-2) we can extend the path so it can reach a point m˜ of K, with extra cost less than ǫ. Since K = (K◦ ), by a second application of Theorem [4.7,](#page-21-2) we can assume that m˜ is an internal point of K, by again adding an extra cost less than ǫ.

Let r > 0 be such that <sup>B</sup>(m˜ , r) <sup>⊂</sup> <sup>K</sup>◦ . From Lemma [6.1,](#page-28-4) without any loss of generality, we can assume that there exist a1, a2, a<sup>3</sup> ∈ (0,∞) such that

<span id="page-34-0"></span>
$$
a_1 \leq \inf_{(x,y)\in\mathcal{Z},t\in[0,S]} q_{xy}(t) \leq \sup_{(x,y)\in\mathcal{Z},t\in[0,S]} q_{xy}(t) \leq a_2, \inf_{x\in\mathcal{X},t\in[0,S]} \mu_x(t) > a_3, \ \|\mu(T) - \tilde{m}\| < \frac{r}{2},\tag{6.16}
$$

where the S used above is the one obtained by starting with T <sup>δ</sup> and adding segments as just described. Finally, we can assume the existence of a r<sup>1</sup> > 0 such that for every point m¯ in B(m, r1), we can find a path like the one described above, by connecting m¯ with a straight line to m. Of course this could generate a1, a2, a3, S different from the initial ones, though universal for all m¯ in B(m, r1), (see Theorem [4.7](#page-21-2) for details).

Now let <sup>m</sup><sup>n</sup> be a sequence that converges to <sup>m</sup>. For big enough n, we can assume that <sup>m</sup><sup>n</sup> <sup>∈</sup> <sup>B</sup>(m, r1). By the continuity of F on compact subsets of (0,∞), we can find r<sup>2</sup> > 0 such that if m1,m<sup>2</sup> ∈ P<sup>a</sup><sup>3</sup> 2 (X ) and km<sup>1</sup> − m2k ≤ r2, then for every q that satisfies [\(6.16\)](#page-34-0), we have

<span id="page-34-2"></span>
$$
\sum_{(x,y)\in\mathcal{Z}} \left| m_{1,x} F_{xy}(q_{xy}) - m_{2,x} F_{xy}\left(q_{xy} \frac{m_{1,x}}{m_{2,x}}\right) \right| \leq \frac{\epsilon}{S}.
$$
\n(6.17)

Now for every n ∈ N, we define the following control for the time interval [0, S],

<span id="page-34-1"></span>
$$
q_{xy}^n(t) = \begin{cases} q_{xy}(t) \frac{\mu_x^n(t-)}{\mu_x(t)}, & \text{if sup}_{s \in [0,t]} \|\boldsymbol{\mu}(t) - \boldsymbol{\mu}^n(t)\| \le r_2\\ \gamma_{xy}, & \text{otherwise.} \end{cases}
$$
(6.18)

Note that either µ n enters K by time S, or the control has switch to γxy before S. For every n, we define an auxiliary stopping time S <sup>n</sup> = inf{<sup>t</sup> <sup>∈</sup> [0, S] : <sup>k</sup><sup>µ</sup> n (t) − µ(t)k > r2}, and also we define Rmax = supm∈P(X) R(m). We can get an estimate of the cost accumulated up to time S, for the pair (µ n , q n ) ∈ T <sup>n</sup> <sup>m</sup><sup>n</sup> . Specifically,

$$
\mathbb{E}\left[\int_{0}^{S}\left(\sum_{(x,y)\in\mathcal{Z}}\mu_{x}^{n}(t)F_{xy}\left(q_{xy}^{n}(t)\right)+R(\boldsymbol{\mu}^{n}(t))\right)dt\right]
$$
\n
$$
\leq \mathbb{E}\left[\int_{0}^{S}\left(\sum_{(x,y)\in\mathcal{Z}}\mu_{x}^{n}(t)F_{xy}\left(q_{xy}^{n}(t)\right)+R(\boldsymbol{\mu}^{n}(t))\right)dt\cdot1_{\left\{\sup_{t\in[0,S]}\|\boldsymbol{\mu}(t)-\boldsymbol{\mu}^{n}(t)\|\leq r_{2}\right\}}\right]
$$
\n
$$
+\mathbb{P}\left(\sup_{t\in[0,S]}\|\boldsymbol{\mu}^{n}(t)-\boldsymbol{\mu}(t)\|>r_{2}\right)\times
$$
\n
$$
\left(\mathbb{E}\left[\int_{0}^{S^{n}}\left(\sum_{(x,y)\in\mathcal{Z}}\mu_{x}^{n}(t)F_{xy}\left(q_{xy}^{n}(t)\right)+R(\boldsymbol{\mu}^{n}(t))\right)dt\right|\sup_{t\in[0,S]}\|\boldsymbol{\mu}^{n}(t)-\boldsymbol{\mu}(t)\|>r_{2}\right]+SR_{max}\right)
$$

Now by [\(6.18\)](#page-34-1) the last quantity is equal to

$$
\mathbb{E}\left[\int_{0}^{S}\left(\sum_{(x,y)\in\mathcal{Z}}\mu_{x}^{n}(t)F_{xy}\left(q_{xy}(t)\frac{\mu_{x}^{n}(t-)}{\mu_{x}(t)}\right)+R(\boldsymbol{\mu}^{n}(t))\right)dt\cdot1_{\left\{\sup_{t\in[0,S]}\|\boldsymbol{\mu}(t)-\boldsymbol{\mu}^{n}(t)\|\leq r_{2}\right\}}\right]
$$
\n
$$
+\mathbb{P}\left(\sup_{t\in[0,S]}\|\boldsymbol{\mu}^{n}(t)-\boldsymbol{\mu}(t)\|>r_{2}\right)\times
$$
\n
$$
\left(\mathbb{E}\left[\int_{0}^{S^{n}}\left(\sum_{(x,y)\in\mathcal{Z}}\mu_{x}^{n}(t)F_{xy}\left(q_{xy}(t)\frac{\mu_{x}^{n}(t-)}{\mu_{x}(t)}\right)+R(\boldsymbol{\mu}^{n}(t))\right)dt\right|\sup_{t\in[0,S]}\|\boldsymbol{\mu}(t)-\boldsymbol{\mu}^{n}(t)\|>r_{2}\right]+SR_{max}\right).
$$

Then using [\(6.17\)](#page-34-2) with m1,x = µx(t), m2,x = µ n x (t−), for big enough n we can bound

$$
\mathbb{E}\left[\int_0^T \left(\sum_{(x,y)\in\mathcal{Z}}\mu_x^n(t)F_{xy}\left(q_{xy}^n(t)\right)+R(\boldsymbol{\mu}^n(t))\right)dt\right]
$$

above by

$$
V_K(\boldsymbol{m}) + 2\epsilon + \mathbb{P}\left(\sup_{t\in[0,S]}\|\boldsymbol{\mu}^n(t) - \boldsymbol{\mu}(t)\| > r_2\right)(V_K(\boldsymbol{m}) + SR_{\text{max}} + 2\epsilon).
$$

By using [\(5.9\)](#page-26-2), the probability that there was no exit in the time interval [0, S] is

$$
\mathbb{P}(S^n \geq S) \leq \mathbb{P}\left(\sup_{t \in [0,S]} \|\boldsymbol{\mu}^n(t) - \boldsymbol{\mu}(t)\| > r_2\right) \leq c \frac{1}{\sqrt{n}r_2}.
$$

Letting Vmax be the upper bound identified in Lemma [6.3](#page-32-0) for the given a > 0, the total cost satisfies

$$
V_K^n(\boldsymbol{m}^n) \leq \mathbb{E}\left[\int_0^S \left(\sum_{(x,y)\in\mathcal{Z}} \mu_x^n(t) F_{xy}\left(q_{xy}^n(t)\right) + R(\boldsymbol{\mu}^n(t))\right) dt + V(\boldsymbol{\mu}^n(S \wedge S^n))\right]
$$
  
\n
$$
\leq V_K(\boldsymbol{m}) + 2\epsilon + \mathbb{P}\left(\sup_{t \in [0,S]} \|\boldsymbol{\mu}^n(t) - \boldsymbol{\mu}(t)\| > r_2\right) (V_K(\boldsymbol{m}) + SR_{\text{max}} + 2\epsilon) + \mathbb{P}(S^n \geq S) V_{\text{max}}
$$
  
\n
$$
\leq V_K(\boldsymbol{m}) + 2\epsilon + 2(SR_{\text{max}} + V_{\text{max}} + 2\epsilon) \frac{c}{\sqrt{n}r_2}.
$$

By sending n to infinity we get the upper bound if m ∈ Pa(X ) for some a > 0. Next let m ∈ P(X ) \ P∗(X ). Let t<sup>0</sup> ≤ ǫ be such that VK(ν(m, t0)) ≤ VK(m) + ǫ, where ν(m, t) is the solution to the original equation after time t. We can find a r > 0 such that for every m˜ ∈ B(ν(m, t0), r), VK(m˜ ) ≤ VK(m) + 2ǫ. If q n (m¯ , t) is an ǫ-optimal control that corresponds to each initial condition m¯ , we define the control

$$
q_{xy}^n(t) = \begin{cases} \gamma_{xy}, & t \le t_0, \\ q_{xy}^n(\boldsymbol{\mu}^n(t_0), t - t_0), & t > t_0, \end{cases}
$$

which gives

$$
V_K^n(\boldsymbol{m}^n) \leq \mathbb{E}\left[\int_0^{T^n} \left(\sum_{(x,y)\in\mathcal{Z}} \mu_x^n(s) F_{xy}\left(q_{xy}^n(s)\right) + R(\boldsymbol{\mu}^n(s))\right) dt\right]
$$
  
\n
$$
\leq \mathbb{E}\left[\int_0^{t_0} \left(\sum_{(x,y)\in\mathcal{Z}} \mu_x^n(s) F_{xy}\left(\gamma_{xy}^n(s)\right) + R(\boldsymbol{\mu}^n(s))\right) dt\right]
$$
  
\n
$$
+ \mathbb{E}\left[\int_{t_0}^{T^n} \left(\sum_{(x,y)\in\mathcal{Z}} \mu_x^n(s) F_{xy}\left(q_{xy}^n(\boldsymbol{\mu}^n(t_0), s - t_0)\right) + R(\boldsymbol{\mu}^n(s))\right) dt\right] \leq t_0 R_{\max} + \mathbb{E}\left[V(\boldsymbol{\mu}^n(t_0))\right]
$$
  
\nLemma 6.3  
\n
$$
\leq \epsilon R_{\max} + P(\boldsymbol{\mu}^n(t_0) \in B(\boldsymbol{\nu}(m, t_0), r)) \left(V_K(\boldsymbol{m}) + 2\epsilon\right) + P(\boldsymbol{\mu}^n(t_0) \notin B(\boldsymbol{\nu}(m, t_0), r)) \left(V_{\max}(\boldsymbol{m}, t_0), r)\right) V_{\max}
$$
  
\n
$$
\leq V_K(\boldsymbol{m}) + (2 + R_{\max})\epsilon + P(\boldsymbol{\mu}^n(t_0) \notin B(\boldsymbol{\nu}(m, t_0), r)) \left(V_{\max}(\boldsymbol{m}, t_0), r)\right) V_{\max}.
$$

Now by an application of Lemma [6.2,](#page-31-3) we get that the last term goes to zero as n goes to ∞, and since ǫ is arbitrary, we get that lim sup V n K(m<sup>n</sup> ) ≤ VK(m).

## <span id="page-36-0"></span>A Properties of Hamiltonians

In this section we establish Lemma [3.4](#page-8-2) and Theorem [3.3.](#page-8-9) We start with the proof of Lemma [3.4.](#page-8-2)

Proof of Lemma [3.4.](#page-8-2) To prove the exchange between supremum and infimum, we will apply a modification of Sion's Theorem (Corollary 3.3 in [\[25\]](#page-42-14)), which states that if a continuous G(u, q) is quasi-concave for every u is some convex set U and quasi-convex for every q in some convex set Q, and if one of the two sets is compact, then we can exchange the supremum with the infimum. We start by investigating the validity of these properties when G = Lxy. Since ℓ is convex, for each u ≥ 0,

$$
L_{xy}(u,q) = q\xi + u\ell\left(\frac{q}{u}\right) - \gamma_{xy}C_{xy}\left(\frac{u}{\gamma_{xy}}\right)
$$

is convex with respect to q. It is easy to see that u 7→ Lxy(u, q) is not concave for each q ≥ 0. However we now show that under Assumption [3.2,](#page-8-0) for each q ≥ 0, u 7→ Lxy(u, q) is quasi-concave, or equivalently, that {u ≥ 0 : Lxy(u, q) ≥ c} is convex for every c ∈ R. By differentiating with respect to u we get

$$
\partial_u L_{xy}(u,q) = -\frac{q}{u} + 1 - (C_{xy})' \left(\frac{u}{\gamma_{xy}}\right).
$$

If we prove that for each q the set of roots for ∂uLxy(u, q) is an interval or a point we are done, because a real function that changes monotonicity from increasing to decreasing at most once is quasi-concave. However ∂uLxy(u, q) has the same roots as Q(u) = u(Cxy) ′ u <sup>γ</sup>xy − u + q. By part 1 of Assumption [3.2,](#page-8-0) Q(u) is increasing, which gives what is needed.

Thus, we are almost in a situation where we can apply Sion's theorem, except that our sets are [0,∞) and hence, non-compact. However, as we explain below, we can still apply this result by using the fact that limq→∞ Lxy(q, 1) = ∞. If we prove that

$$
\inf_{q\in[0,\infty)}\sup_{u\in(0,\infty)}L_{xy}(u,q)=\lim_{r\to\infty}\inf_{q\in[0,\infty)}\sup_{u\in\left[r,\frac{1}{r}\right]}L_{xy}(u,q),
$$

then we are done, since by Corollary 3.3 in [\[25\]](#page-42-14)

$$
\inf_{q \in [0,\infty)} \sup_{u \in (0,\infty)} L_{xy}(u,q) = \lim_{r \to \infty} \inf_{q \in [0,\infty)} \sup_{u \in [r,\frac{1}{r}]} L_{xy}(u,q) = \lim_{r \to \infty} \sup_{u \in [r,\frac{1}{r}]} \inf_{q \in [0,\infty)} L_{xy}(u,q) = \sup_{u \in (0,\infty)} \inf_{q \in [0,\infty)} L_{xy}(u,q).
$$

Let M := infq∈[0,∞) supu∈(0,∞) Lxy(u, q). We will assume that M < ∞, and note that the case M = ∞ is treated similarly. Since limq→∞ Lxy(q, 1) = ∞, we can find ˜q such that Lxy(q, 1) > 2M for every q ≥ q. ˜ Now we have

$$
\inf_{q\in[0,\infty)}\sup_{u\in(0,\infty)}L_{xy}(u,q)=\inf_{q\in[0,\tilde{q}]}\sup_{u\in(0,\infty)}L_{xy}(u,q),
$$

and

$$
\inf_{q\in[0,\tilde{q}]} \sup_{u\in[r,\frac{1}{r}]} L_{xy}(u,q) = \inf_{q\in[0,\infty)} \sup_{u\in[r,\frac{1}{r}]} L_{xy}(u,q),
$$

which gives

$$
\inf_{q \in [0,\infty)} \sup_{u \in (0,\infty)} L_{xy}(u,q) = \inf_{q \in [0,\tilde{q}]} \sup_{u \in (0,\infty)} L_{xy}(u,q) = \sup_{u \in (0,\infty)} \inf_{q \in [0,\tilde{q}]} L_{xy}(u,q) = \lim_{u \in (0,\infty)} \sup_{q \in [0,\tilde{q}]} L_{xy}(u,q) = \lim_{r \to \infty} \inf_{q \in [0,\tilde{q}]} \sup_{u \in [r,\frac{1}{r}]} L_{xy}(u,q) = \lim_{r \to \infty} \inf_{q \in [0,\infty)} \sup_{u \in [r,\frac{1}{r}]} L_{xy}(u,q).
$$

Proof of Theorem [3.3.](#page-8-9) Let H<sup>−</sup> (respectively, H+) denote the left-hand side (respectively, right-hand side), of [\(3.7\)](#page-8-1). Since each term in the sum that generates H<sup>+</sup> is bigger than the corresponding one in the sum of H−, we get equality for all of them. By the theory of the Legendre transform we know that infq∈[0,∞) supu∈(0,∞) {qξxy + Gxy(u, q)} is actually a concave function. Since we can exchange the order between the supremum and infimum, then supu∈(0,∞) infq∈[0,∞) {qξxy + Gxy(u, q)} must be a concave function as well. By using the formula

$$
\sup_{u \in (0,\infty)} \inf_{q \in [0,\infty)} \left\{ q\xi + G_{xy}(u,q) \right\} = \sum_{(x,y) \in \mathcal{Z}} m_x \gamma_{xy} \left( C_{xy} \right)^* \left( -\ell^* \left( -\xi_{xy} \right) \right)
$$

we have that (Cxy) ∗ (−ℓ ∗ (ξ)) = (Cxy) ∗ 1 − e ξ must also be concave. By differentiating with respect to ξ we get, e 2ξ ((Cxy) ∗ ) ′′ 1 − e ξ − e ξ ((Cxy) ∗ ) ′ 1 − e ξ ≤ 0, from which, by using the identity (f ∗ ) ′ = (f ′ ) −1 , we get

$$
e^{2\xi} \left( \left( (C_{xy})' \right)^{-1} \right)' \left( 1 - e^{\xi} \right) - e^{\xi} \left( (C_{xy})' \right)^{-1} \left( 1 - e^{\xi} \right) \leq 0.
$$

By substituting ˜u = 1 − e <sup>ξ</sup> we get

$$
(1 - \tilde{u}) \left( ((C_{xy})')^{-1} \right)' (\tilde{u}) - ((C_{xy})')^{-1} (\tilde{u}) \le 0, \quad \text{with } \tilde{u} \le 1
$$
  
\n
$$
(1 - \tilde{u}) \frac{1}{(C_{xy})'' \left( ((C_{xy})')^{-1} (\tilde{u}) \right)} - ((C_{xy})')^{-1} (\tilde{u}) \le 0, \quad \text{with } \tilde{u} \le 1
$$
  
\n
$$
(1 - (C_{xy})'(r)) \frac{1}{(C_{xy})''(r)} - r \le 0, \quad \text{with } (C_{xy})'(r) \le 1
$$
  
\n
$$
r (C_{xy})''(r) + (C_{xy})'(r) - 1 \ge 0, \quad \text{with } (C_{xy})'(r) \le 1.
$$

Now the last inequality implies that either (Cxy) ′ (u) ≥ 1 or that u(Cxy) ′ (u) − u is locally increasing and even more that if (Cxy) ′ (u0) ≥ 1 for some u0, then it must remain like that for every u ≥ u0. If that was not the case then we can find u<sup>1</sup> > u<sup>0</sup> such that u1(Cxy) ′ (u1) − u<sup>1</sup> < qˆ for some negative ˆq, while u0(Cxy) ′ (u0) − u<sup>0</sup> ≥ 0. By a suitable application of the mean value theorem we will get the existence of an r that the last inequality fails. If we set ˜uxy = inf{u : (Cxy) ′ (u) ≥ 1}, then the Assumption [3.2](#page-8-0) is recovered.

## <span id="page-38-0"></span>B Properties of Fxy

Proof of Lemma [3.7.](#page-9-0) (1) We have

$$
F_{xy}(q) = \sup_{u \in (0,\infty)} \left\{ u\ell\left(\frac{q}{u}\right) - \gamma_{xy} C_{xy}\left(\frac{u}{\gamma_{xy}}\right) \right\} \ge \gamma_{xy}\ell\left(\frac{q}{\gamma_{xy}}\right) - \gamma_{xy} C_{xy}\left(\frac{\gamma_{xy}}{\gamma_{xy}}\right) \ge \gamma_{xy}\ell\left(\frac{q}{\gamma_{xy}}\right) \ge 0.
$$

(2) We have

$$
F_{xy}(\gamma_{xy}) = \sup_{u \in (0,\infty)} G_{xy}(u, \gamma_{xy}) = \sup_{u \in (0,\infty)} \left\{ u\ell\left(\frac{\gamma_{xy}}{u}\right) - \gamma_{xy} C_{xy}\left(\frac{u}{\gamma_{xy}}\right) \right\}
$$
  
= 
$$
\sup_{u \in (0,\infty)} \left\{ \gamma_{xy} \log \gamma_{xy} - \gamma_{xy} \log u - \gamma_{xy} + u - \gamma_{xy} C_{xy}\left(\frac{u}{\gamma_{xy}}\right) \right\},
$$

and by applying part 2 of Lemma [3.6](#page-9-3)

$$
\gamma_{xy} C_{xy} \left( \frac{u}{\gamma_{xy}} \right) \ge \gamma_{xy} \log \gamma_{xy} - \gamma_{xy} \log u - \gamma_{xy} + u.
$$

Therefore Fxy(γxy) ≤ 0. However, by part (1) of this lemma Fxy(γxy) ≥ 0, and therefore the equality follows.

(3) By definition Fxy(q) = supu∈(0,∞) Gxy(u, q). Let a ∈ (0, 1) and 0 ≤ q<sup>1</sup> < q<sup>2</sup> < ∞, and let q = aq<sup>1</sup> + (1 − a)q2. Using the convexity of Gxy(u, q) for fixed u as a function of q, we have

$$
F_{xy}(aq_1 + (1 - a)q_2) = \sup_{u \in (0, \infty)} G_{xy}(u, aq_1 + (1 - a)q_2)
$$
  
\n
$$
\leq \sup_{u \in (0, \infty)} \{ aG_{xy}(u, q_1) + (1 - a)G_{xy}(u, q_2) \}
$$
  
\n
$$
\leq a \sup_{u \in (0, \infty)} G_{xy}(u, q_1) + (1 - a) \sup_{u \in (0, \infty)} G_{xy}(u, q_2)
$$
  
\n
$$
\leq aF_{xy}(q_1) + (1 - a)F_{xy}(q_2).
$$

<span id="page-39-1"></span>For the proof of Lemma [4.5](#page-20-1) that is given below, we will use the following auxiliary lemma. Recall the definition of Gxy in [\(1.8\)](#page-2-1).

Lemma B.1 If {C<sup>n</sup> } satisfies Assumption [4.3,](#page-20-0) then the following hold for every (x, y) ∈ Z.

1. There exists a positive real number M, that does not depend on (x, y), such that for the decreasing function M<sup>1</sup> xy : (0,∞) → [0,∞), given by

$$
M_{xy}^1(q) \doteq \min\left\{\gamma_{xy}\left(\frac{\gamma_{xy}}{q}\right)^{1/p}, M\right\},\,
$$

we have that Gxy(u, q) is increasing as a function of u on the interval (0, M<sup>1</sup> xy(q)].

2. There exists a decreasing function M<sup>2</sup> xy : (0,∞) <sup>→</sup> [0,∞), with <sup>M</sup><sup>2</sup> xy(q) <sup>≥</sup> <sup>M</sup><sup>1</sup> xy(q), such that Gxy(u, q) is decreasing as a function of u on the interval -M<sup>2</sup> xy(q),∞ .

Proof. By taking the derivative with respect to u in the definition [\(1.8\)](#page-2-1) we get

$$
-\frac{q}{u} - (C_{xy})' \left(\frac{u}{\gamma_{xy}}\right) + 1.
$$

(1) By part 2 of Assumption [4.3](#page-20-0) there exists M ∈ (0,∞) such that if u < M, then

$$
-\frac{q}{u} - (C_{xy})' \left(\frac{u}{\gamma_{xy}}\right) + 1 \ge -\frac{q}{u} + \left(\frac{\gamma_{xy}}{u}\right)^{p+1} + 1,
$$

and by taking u ≤ γxy (γxy/q) <sup>1</sup>/p we get

$$
-\frac{q}{u} + \left(\frac{\gamma_{xy}}{u}\right)^{p+1} + 1 \ge -\frac{q}{u} + \frac{q}{u} + 1 > 0.
$$

Therefore for

$$
M_{xy}^1(q) = \min\left\{\gamma_{xy} \left(\frac{\gamma_{xy}}{q}\right)^{1/p}, M\right\},\,
$$

we have − q <sup>u</sup> − (Cxy) ′ u <sup>γ</sup>xy + 1 <sup>≥</sup> 0 on the interval (0, M<sup>1</sup> xy(q)].

(2) By applying part 3 of Assumption [4.3,](#page-20-0) we get that there exists decreasing M˜ <sup>2</sup> xy(q) < ∞, such that if u > M˜ <sup>2</sup> xy(q) then

<span id="page-39-0"></span>
$$
\frac{u}{\gamma_{xy}}(C_{xy})'\left(\frac{u}{\gamma_{xy}}\right) - \frac{u}{\gamma_{xy}} \ge -\frac{q}{\gamma_{xy}}.\tag{B.1}
$$

Then M<sup>2</sup> xy(q) .= max{M<sup>1</sup> xy(q), M˜ <sup>2</sup> xy(q)}, is decreasing and bigger than <sup>M</sup><sup>1</sup> xy, and using [\(B.1\)](#page-39-0) we get

$$
-\frac{q}{u} - (C_{xy})' \left(\frac{u}{\gamma_{xy}}\right) + 1 = -\frac{q}{u} - \frac{\gamma_{xy}}{u} \left(\frac{u}{\gamma_{xy}} (C_{xy})' \left(\frac{u}{\gamma_{xy}}\right) - \frac{u}{\gamma_{xy}}\right) \le 0
$$

.

on the interval [M<sup>2</sup> xy(q),∞).

Proof of Lemma [4.5.](#page-20-1) (1) Let ǫ > 0, and q ≥ ǫ. By Lemma [B.1,](#page-39-1) we have that Gxy (u, q), as a function of u, is increasing on the interval (0, M<sup>1</sup> xy(q)]. Therefore for all <sup>u</sup> <sup>∈</sup> (0, M<sup>1</sup> xy(q)] we have

$$
u\ell\left(\frac{q}{u}\right) - \gamma_{xy}C_{xy}\left(\frac{u}{\gamma_{xy}}\right) \leq M_{xy}^1(q)\ell\left(\frac{q}{M_{xy}^1(q)}\right) - \gamma_{xy}C_{xy}\left(\frac{M_{xy}^1(q)}{\gamma_{xy}}\right) \leq M_{xy}^1(q)\ell\left(\frac{q}{M_{xy}^1(q)}\right)
$$
  
$$
\leq q \log\left(\frac{q}{M_{xy}^1(q)}\right) + M_{xy}^1(q) \leq q \log\left(\frac{q}{M_{xy}^1(q)}\right) + M_{xy}^1(\epsilon)
$$
  
$$
\leq q \log(q) - q \log\left(M_{xy}^1(q)\right) + M_{xy}^1(\epsilon)
$$
  
$$
\stackrel{M_{xy}^1(\epsilon) \leq M_{xy}^2(\epsilon)}{\leq} q \log(q) - q \log\left(M_{xy}^1(q)\right) + M_{xy}^2(\epsilon).
$$

By the second part of Lemma [B.1,](#page-39-1) we have that Gxy(u, q) is decreasing on the interval (M<sup>2</sup> xy(ǫ),∞). Therefore for all <sup>u</sup> <sup>∈</sup> (M<sup>2</sup> xy(ǫ),∞)

$$
u\ell\left(\frac{q}{u}\right) - \gamma_{xy}C_{xy}\left(\frac{u}{\gamma_{xy}}\right) \le M_{xy}^2(\epsilon)\ell\left(\frac{q}{M_{xy}^2(\epsilon)}\right) - \gamma_{xy}C_{xy}\left(\frac{M_{xy}^2(\epsilon)}{\gamma_{xy}}\right) \le M_{xy}^2(\epsilon)\ell\left(\frac{q}{M_{xy}^2(\epsilon)}\right)
$$
  
$$
\le q \log\left(\frac{q}{M_{xy}^2(\epsilon)}\right) + M_{xy}^2(\epsilon)
$$
  
$$
\le \gamma \log\left(\frac{q}{M_{xy}^2(\epsilon)}\right) + M_{xy}^2(\epsilon)
$$
  
$$
\le \gamma \log\left(\frac{q}{M_{xy}^2(\epsilon)}\right) + M_{xy}^2(\epsilon)
$$
  
$$
\le \gamma \log\left(\frac{q}{M_{xy}^2(\epsilon)}\right) + M_{xy}^2(\epsilon)
$$
  
$$
\le \gamma \log\left(\frac{q}{M_{xy}^2(\epsilon)}\right) + M_{xy}^2(\epsilon).
$$

Finally for the interval [M<sup>1</sup> xy(q), M<sup>2</sup> xy(ǫ)] we have

$$
u\ell\left(\frac{q}{u}\right) - \gamma_{xy}C_{xy}\left(\frac{u}{\gamma_{xy}}\right) \leq u\ell\left(\frac{q}{u}\right) = q\log q - q\log u - q + u
$$
  
$$
\leq q\log q - q\log(M_{xy}^1(q)) + M_{xy}^2(\epsilon).
$$

Now if we recall the definition of M<sup>1</sup> xy given in Lemma [B.1](#page-39-1) and set M¯ (q) .= max{M<sup>2</sup> xy(q) : (x, y) ∈ Z}, then

$$
G_{xy}(u,q) \le q \log \frac{q}{\min\left\{\gamma_{xy} \left(\frac{\gamma_{xy}}{q}\right)^{1/p}, M\right\}} + \bar{M}(\epsilon),
$$

and by taking supremum over u we end up with Fxy(q) satisfying the same bound.

(2) This is straightforward since Fxy is finite on the interval (0,∞), and convex.

## <span id="page-40-0"></span>C Tightness functionals

Proof of Lemma [5.1.](#page-26-0) Let c<sup>2</sup> > 0 and {(µ n , T <sup>n</sup> )} be a deterministic sequence in S with µ <sup>n</sup> absolutely continuous such that n

$$
\int_0^{T^n} \ell(|\dot{\boldsymbol{\mu}}^n(t)|) dt + c_1 T^n \le c_2
$$

and |µ˙ n (t)| = 0 for t > T <sup>n</sup>. We need to show that H has level sets with compact closure. Since all elements are positive, we have that T <sup>n</sup> ≤ c2/c1. Let µ¯ <sup>n</sup> denote the restriction of µ n to [0, c2/c1]. If we prove that µ¯ n converges along some subsequence then we are done. Using the inequality ab ≤ e ca + ℓ(b)/c, which is valid for a, b ≥ 0, and c ≥ 1, we have that

$$
|\boldsymbol{\mu}^{n}(t) - \boldsymbol{\mu}^{n}(s)| \leq \int_{t}^{s} |\dot{\boldsymbol{\mu}}^{n}(r)| dr \leq (t - s)e^{c} + \frac{c_{2}}{c}.
$$

This shows that {µ¯ <sup>n</sup>} are equicontinuous. Since <sup>µ</sup>¯ n (t) takes values in the compact set P(X ), by the Arzela-Ascoli theorem there is a convergent subsequence.

## <span id="page-41-0"></span>References

- [1] Aristotle Arapostathis, Vivek S. Borkar, Emmanuel Fern´andez-Gaucherand, Mrinal K. Ghosh, and Steven I. Marcus. Discrete-Time Controlled Markov Processes with Average Cost Criterion: A Survey. SIAM Journal on Control and Optimization, 31(2):282–344, mar 1993.
- <span id="page-41-1"></span>[2] Guadalupe Avila-Godoy and Emmanuel Fern´andez-Gaucherand. Controlled Markov chains with exponential risk-sensitive criteria: modularity, structured policies and applications. In Decision and Control, 1998. Proceedings of the 37th IEEE Conference on, volume 1, pages 778–783. IEEE, 1998.
- <span id="page-41-7"></span><span id="page-41-6"></span>[3] Dimitri P. Bertsekas. Dynamic Programming and Optimal Control: Approximate Dinamic Programming, volume 2. Athena Scientific, 2012.
- [4] Patrick Billingsley. Probability and measure. Wiley Series in Probability and Mathematical Statistics. John Wiley & Sons, Inc., New York, third edition, 1995.
- [5] V. S. Borkar and S. P. Meyn. Risk-Sensitive Optimal Control for Markov Decision Processes with Monotone Cost. Mathematics of Operations Research, 27(1):192–209, feb 2002.
- [6] Rolando Cavazos-Cadena. Optimality equations and inequalities in a class of risk-sensitive average cost Markov decision chains. Mathematical Methods of Operations Research, 71(1):47–84, feb 2010.
- <span id="page-41-2"></span>[7] Kun-Jen Chung and Matthew J. Sobel. Discounted MDP's: Distribution Functions and Exponential Utility Maximization. SIAM Journal on Control and Optimization, 25(1):49–62, jan 1987.
- <span id="page-41-3"></span>[8] Giovanni B. Di Masi and Lukasz Stettner. Infinite Horizon Risk Sensitive Control of Discrete Time Markov Processes under Minorization Property. SIAM Journal on Control and Optimization, 46(1):231– 252, jan 2007.
- <span id="page-41-5"></span><span id="page-41-4"></span>[9] P. Dupuis, M. R. James, and I. R. Petersen. Robust properties of risk–sensitive control. Math. Control Signals Systems, 13:318–332, 2000.
- [10] P. Dupuis, M.R. James, and I. Petersen. Robust properties of risk-sensitive control. In Proceedings of the 37th IEEE Conference on Decision and Control (Cat. No.98CH36171), volume 2, pages 2365–2370. IEEE.

- <span id="page-42-13"></span><span id="page-42-9"></span>[11] P. Dupuis and WM McEneaney. Risk-sensitive and robust escape criteria. SIAM journal on control and optimization, 35(6):2021–2049, 1997.
- <span id="page-42-4"></span>[12] Paul Dupuis, Kavita Ramanan, and Wei Wu. Large Deviation Principle For Finite-State Mean Field Interacting Particle Systems. arXiv:1601.06219, page 62, jan 2016.
- <span id="page-42-3"></span>[13] W. H. Fleming and D. Hern´andez-Hern´andez. Risk-Sensitive Control of Finite State Machines on an Infinite Horizon I. SIAM Journal on Control and Optimization, 35(5):1790–1810, sep 1997.
- <span id="page-42-10"></span>[14] W. H. Fleming and H. M. Soner. Asymptotic expansions for Markov processes with Levy generators. Appl. Math. Optimization, 19:203–223, 1989.
- <span id="page-42-5"></span>[15] M K Ghosh and Subhamay Saha. Risk-sensitive control of continuous time Markov chains. Stochastics: An International Journal of Probability and Stochastic Processes, (October 2014):37–41, 2014.
- <span id="page-42-0"></span>[16] Daniel Hernandez-Hern´andez and Steven I. Marcus. Risk sensitive control of Markov processes in countable state space. Systems & Control Letters, 29(3):147–155, nov 1996.
- <span id="page-42-6"></span>[17] O Hern´andez-Lerma and J B Lasserre. Further Topics in Discrete Time Markov Control Processes. Springer, 1999.
- <span id="page-42-15"></span>[18] RA Howard and JE Matheson. Risk-sensitive Markov decision processes. Management science, 1972.
- [19] Nobuyuki Ikeda and Shinzo Watanabe. Stochastic differential equations and diffusion processes, volume 24 of North-Holland Mathematical Library. North-Holland Publishing Co., Amsterdam; Kodansha, Ltd., Tokyo, second edition, 1989.
- <span id="page-42-8"></span><span id="page-42-7"></span>[20] Anna Jaskiewicz. Average optimality for risk-sensitive control with general state space. Annals of Applied Probability, 17(2):654–675, apr 2007.
- [21] Steven I. Marcus, Emmanuel Fernandez-Gaucherand, Daniel Hernandez-Hernandez, Stefano P Coraluppi, and Pedram Fard. Risk Sensitive Markov Decision Processes. In Systems and Control in the 21st Century, page 17. Birkh¨auser Boston, Boston, MA, 1997.
- <span id="page-42-16"></span><span id="page-42-12"></span>[22] Stewart N. Ethier and Thomas G. Kurtz. Markov Processes. In SpringerReference, page 544. 1986.
- <span id="page-42-1"></span>[23] I.R. Petersen, M.R. James, and P. Dupuis. Minimax optimal control of stochastic uncertain systems with relative entropy constraints. Automatic Control, IEEE Transactions on, 45(3):398–412, 2000.
- <span id="page-42-14"></span>[24] M.L. Puterman. Markov decision processes. In D.P. Heyman and M.J. Sobel, editors, Stochastic Models, Volume 2, chapter 8. North Holland, Amsterdam, 1991.
- <span id="page-42-11"></span>[25] M Sion. On general minimax theorems. Pacific J. Math, 1958.
- [26] Peter Whittle. Optimal Control: Basics and Beyond. Wiley-Interscience series in systems and optimization, page 464, 1996.
- <span id="page-42-2"></span>[27] G. Xianping and O. Hern´andez-Lerma. Continuous-time Markov decision processes : theory and applications. Springer, 2009.