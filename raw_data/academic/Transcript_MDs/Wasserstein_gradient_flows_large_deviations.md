# [arXiv:1203.0676v2 \[math.AP\] 28 Mar 2012](http://arxiv.org/abs/1203.0676v2)

# Wasserstein gradient flows from large deviations of thermodynamic limits

Manh Hong Duong<sup>1</sup> , Vaios Laschos<sup>1</sup> and Michiel Renger<sup>2</sup>

<sup>1</sup> Department of Mathematical sciences, University of Bath,

2 ICMS and Dep. of Math. and Comp. Sciences, TU Eindhoven.

April 8, 2019

## Abstract

We study the Fokker-Planck equation as the thermodynamic limit of a stochastic particle system on one hand and as a Wasserstein gradient flow on the other. We write the rate functional, which characterizes the large deviations from the thermodynamic limit, in such a way that the free energy appears explicitly. Next we use this formulation via the contraction principle to prove that the discrete time rate functional is asymptotically equivalent in the Gamma-convergence sense to the functional derived from the Wasserstein gradient discretization scheme.

### 1 Introduction

<span id="page-0-1"></span>Since the seminal work of Jordan, Otto and Kinderlehrer [\[JKO98\]](#page-24-0), it has become clear that there are many more partial differential equations that can be written as a gradient flow than previously known. Two important insights have contributed to this: the generalisation of gradient flows to metric spaces and the specific choice of the Wasserstein metric as the dissipation mechanism. The paper by Jordan, Kinderlehrer and Otto introduced a gradient-flow structure by approximation in discrete time. More recent work have shown how these ideas can be studied in continuous time [\[Ott01\]](#page-24-1), and how they can be generalised to any metric space [\[AGS08\]](#page-23-0). This paper is mainly concerned with the time-discrete scheme, which we shall now explain.

A gradient flow in L 2 (**R** d ) is an evolution equation of the form

<span id="page-0-0"></span>
$$
\frac{\partial \rho}{\partial t} = -\text{grad}_{L^2} \mathcal{F}(\rho),\tag{1}
$$

for some functional F. For a gradient flow it is natural to use the following time-discrete variational scheme. If ρ<sup>0</sup> is the solution at time t = 0, then the solution at time τ > 0 is approximated by the minimiser of the functional

$$
\rho \mapsto \mathcal{F}(\rho) + \frac{1}{2\tau} ||\rho - \rho_0||^2_{L^2(\mathbb{R}^d)}.
$$

Indeed, the Euler-Lagrange equation is then <sup>ρ</sup><sup>τ</sup> <sup>−</sup>ρ<sup>0</sup> <sup>τ</sup> = −gradL<sup>2</sup>F(ρ<sup>τ</sup> ), which clearly approximates [\(1\)](#page-0-0) as τ → 0. In the same manner, one can define a variational scheme by minimising the functional

<span id="page-1-3"></span>
$$
\rho \mapsto \mathcal{F}(\rho) + \frac{1}{2\tau} W_2^2(\rho, \rho_0),\tag{2}
$$

where W<sup>2</sup> is the Wasserstein metric. Convergence of this variational scheme was first proven in [\[JKO98\]](#page-24-0) with the choice of F(ρ) := S(ρ) + E(ρ), where

$$
\mathcal{E}(\rho) = \int_{\mathbb{R}^d} \Psi(x)\rho(dx) \quad \text{and} \quad \mathcal{S}(\rho) := \begin{cases} \int_{\mathbb{R}^d} \rho(x) \log \rho(x) dx, & \text{for } \rho(dx) = \rho(x) dx \\ \infty, & \text{otherwise,} \end{cases}
$$
 (3)

for some potential Ψ. In this case, the minimisers converge to the solution of the Fokker-Planck equation

<span id="page-1-1"></span><span id="page-1-0"></span>
$$
\frac{\partial \rho}{\partial t} = \Delta \rho + \text{div}(\rho \nabla \Psi). \tag{4}
$$

Later, in [\[Ott01\]](#page-24-1), this result was extended to more general F, but we will be concerned with the specific choice [\(3\)](#page-1-0). Physically, S can be interpreted as entropy, E as internal energy, and F as the corresponding Helmholtz free energy (if the temperature effects are hidden in Ψ); hence it is not surprising that this free energy should decay along solutions of [\(4\)](#page-1-1). However, it is not intuitively clear why the dissipation of free energy must be described by the Wasserstein metric.

As we will explain in Section [3,](#page-6-0) for systems in equilibrium, the stochastic fluctuations around the equilibrium are characterised by a free energy similar to [\(3\)](#page-1-0). Recent developments suggest a similar principle for systems away from equilibrium [\[L´eo07,](#page-24-2) [ADPZ10,](#page-23-1) [PR11,](#page-24-3) [DLZ10,](#page-23-2) [ADPZ12\]](#page-23-3). To explain this, consider N independent random particles in **R** <sup>d</sup> with positions Xk(t), initially distributed by some <sup>ρ</sup><sup>0</sup> ∈ P(**<sup>R</sup>** d ), where the probability distribution of each particle evolves according to [\(4\)](#page-1-1). Define the corresponding empirical process

$$
L_N: t \mapsto \frac{1}{N} \sum_{k=1}^N \delta_{X_k(t)}.
$$

Then, as a consequence of the Law of Large Numbers, at each τ ≥ 0 the empirical measure L<sup>N</sup> (τ ) converges almost surely in the narrow topology as N → ∞ to the solution of the Fokker-Planck equation [\(4\)](#page-1-1) with initial condition ρ<sup>0</sup> [\[Dud89\]](#page-23-4); this is sometimes known as the thermodynamic limit. The rate of this convergence is characterised by a large deviation principle. Roughly speaking, this means that there exists a <sup>J</sup><sup>τ</sup> : <sup>P</sup>(**<sup>R</sup>** d ) → [0, ∞] such that (see Section [3\)](#page-6-0)

$$
\text{Prob}\left(L_N(\tau) \approx \rho \,|\, L_N(0) \approx \rho_0\right) \sim \exp\left(-N J_\tau(\rho|\rho_0)\right) \quad \text{as } N \to \infty.
$$

In [\[L´eo07,](#page-24-2) Prop. 3.2] and [\[PR11,](#page-24-3) Cor. 13], it was found that

<span id="page-1-2"></span>
$$
J_{\tau}(\rho|\rho_0) = \inf \left\{ \mathcal{H}(\gamma|\rho_0 \otimes p_{\tau}) : \gamma \in \Pi(\rho_0, \rho) \right\},\tag{5}
$$

where H is the relative entropy (discussed in Section [3\)](#page-6-0), p<sup>t</sup> is the fundamental solution of the Fokker-Planck equation [\(4\)](#page-1-1) and Π(ρ0, ρ) is the set of all Borel measures in **R** 2d that have first and second marginal ρ<sup>0</sup> and ρ respectively. In this paper, we characterise a class of potentials Ψ and initial data ρ<sup>0</sup> for which [\(5\)](#page-1-2) is equal to

<span id="page-2-2"></span>
$$
J_{\tau}(\rho|\rho_0) = \inf_{\rho_{(\cdot)} \in C_{W_2}(\rho_0, \rho)} \left\{ \frac{1}{4\tau} \int_0^1 \left\| \frac{\partial \rho_t}{\partial t} \right\|_{-1, \rho_t}^2 dt + \frac{\tau}{4} \int_0^1 \left\| \text{grad}\,\mathcal{F}(\rho_t) \right\|_{-1, \rho_t}^2 dt + \frac{1}{2} \mathcal{F}(\rho_1) - \frac{1}{2} \mathcal{F}(\rho_0) \right\} .
$$
\n(6)

where the k · k−1,ρ norm and the exact meaning of grad F will be defined in the sequel. In the main theorem, by using the above equality, we show that the Wasserstein scheme [\[JKO98\]](#page-24-0) has the same asymptotic behavior with J<sup>τ</sup> for τ → 0, in terms of Gamma-convergence (see [\[Bra02\]](#page-23-5) for an exposition of Gamma-convergence).

<span id="page-2-3"></span>Theorem 1.1. Let <sup>ρ</sup><sup>0</sup> <sup>=</sup> <sup>ρ</sup>0(x)dx ∈ P2(**R**) be absolutely continuous with respect to the Lesbegue measure with ρ0(x) is bounded from below by a positive constant in every compact set. Assume that F(ρ0), k∆ρ0k 2 −1,ρ<sup>0</sup> and R **R** |∇Ψ(x)| <sup>2</sup> <sup>ρ</sup>0(dx) are all finite, and that <sup>Ψ</sup> <sup>∈</sup> <sup>C</sup> 2 (**R**) satisfies either Assumption [4.1](#page-7-0) or [4.4](#page-8-0) (introduced in Section [4\)](#page-7-1). Then we have

<span id="page-2-0"></span>
$$
J_{\tau}(\cdot|\rho_0) - \frac{W_2^2(\rho_0, \cdot)}{4\tau} \xrightarrow[\tau \to 0]{\tau} \frac{1}{2} \mathcal{F}(\cdot) - \frac{1}{2} \mathcal{F}(\rho_0), \qquad \text{in } \mathcal{P}_2(\mathbb{R}). \tag{7}
$$

Here <sup>P</sup>2(**R**) denotes the space of probability measures on **<sup>R</sup>** having finite second moment. As we will prove, the Gamma-convergence result holds if <sup>P</sup>2(**R**) is equipped with the narrow topology, as well as if we equip it with the Wasserstein topology. More precisely: we will prove the lower bound in the narrow topology (Theorem [5.1\)](#page-14-0), and the existence of the recovery sequence (Theorem [6.1\)](#page-15-0) in the Wasserstein topology. In the Wasserstein topology, the Gamma-convergence [\(7\)](#page-2-0) immediately implies:

<span id="page-2-1"></span>
$$
\tau J_{\tau}(\cdot | \rho_0) \xrightarrow[\tau \to 0]{\Gamma} \frac{1}{4} W_2^2(\rho_0, \cdot) \qquad \text{in } \mathcal{P}_2(\mathbb{R}). \tag{8}
$$

For a system of Brownian particles, i.e. Ψ ≡ 0, statement [\(8\)](#page-2-1) can also be found in [\[L´eo07\]](#page-24-2). Together, the two statements [\(7\)](#page-2-0) and [\(8\)](#page-2-1) make up an asymptotic development of the rate J<sup>τ</sup> for small τ , i.e.

$$
J_{\tau}(\rho|\rho_0) \approx \frac{1}{2}\mathcal{F}(\rho) - \frac{1}{2}\mathcal{F}(\rho_0) + \frac{1}{4\tau}W_2^2(\rho_0, \rho).
$$

Apart from the factor 1/2 and the constant F(ρ0), which do not affect the minimisers, this approximation indeed corresponds to the functional defining the time-discrete variational scheme [\(2\)](#page-1-3) from [\[JKO98\]](#page-24-0).

For Ψ = 0, the main statement [\(7\)](#page-2-0) was proven in [\[ADPZ10\]](#page-23-1) in a subset of <sup>P</sup>2(**R**) consisting of measures that are sufficiently close to a uniform distribution on a compact interval. In [\[PR11\]](#page-24-3), it was proven that whenever [\(7\)](#page-2-0) holds for Ψ = 0, then it also holds for any Ψ ∈ C 2 b (**R** d ). Both papers make use of the specific form of the fundamental solution of [\(4\)](#page-1-1). In [\[DLZ10\]](#page-23-2), [\(7\)](#page-2-0) was shown for Gaussian measures on the real line. In our approach, using the path-wise large deviations, we can avoid using the fundamental solution, allowing us to prove the statement in a much more general context.

All theorems in this paper also work in higher dimensions, except for the existence of the recovery sequence in the main theorem. This has to do with the fact that in one dimension the optimal transport plan between two measures with equal tails will be the identity at the tails. However, this argument fails in higher dimensions. We belief that the recovery sequence also exists in higher dimensions but this is left for future research.

The required concepts of this paper are introduced in Section [2.](#page-3-0) In Section [3,](#page-6-0) we explain the concept of large deviations in the case of an equilibrium system, introduce the dynamical particle system that we study more precisely, and discuss the conditional large deviations for this system. The alternative form of the functional J<sup>h</sup> is proven in Section [4](#page-7-1) via the path-wise large deviation principles. Finally, in Section [5](#page-14-1) we prove the Gamma-convergence lower bound, and in Section [6](#page-15-1) the existence of the recovery sequence.

### 2 Preliminaries

<span id="page-3-0"></span>By the nature of this study, we need a combination of techniques from probability theory, mostly from the theory of large deviations, and from functional analysis, mostly from the gradient flow calculus as set out in [\[AGS08\]](#page-23-0). Let us introduce these concepts here.

To begin, let us discuss the topological measure spaces. Unless otherwise stated, the space of probability measures <sup>P</sup>(**<sup>R</sup>** d ) will be endowed with the narrow topology, defined by convergence against continuous bounded test functions:

$$
\rho_t \to \rho
$$
 as  $t \to 0$  if and only if  $\int_{\mathbb{R}^d} \phi \, d\rho_t \to \int_{\mathbb{R}^d} \phi \, d\rho$  for all  $\phi \in C_b(\mathbb{R}^d)$ .

We sometimes identify measures with densities when possible, which is typically the case if a measure has finite entropy. The space <sup>P</sup>2(**<sup>R</sup>** d ) = <sup>ρ</sup> ∈ P(**<sup>R</sup>** d ) : R |x| <sup>2</sup> ρ(dx) < ∞ will be endowed with the topology generated by the Wasserstein metric W2. The Wasserstein distance of two measures <sup>ρ</sup>0, ρ ∈ P2(**<sup>R</sup>** d ) is defined via

$$
W_2^2(\rho_0, \rho) = \inf_{\gamma \in \Pi(\rho_0, \rho)} \left\{ \int_{\mathbb{R}^n} \int_{\mathbb{R}^n} |x - y|^2 d\gamma \right\}.
$$

Convergence in the Wasserstein topology can be characterised as (see e.g. [\[Vil03,](#page-24-4) [AGS08\]](#page-23-0)):

$$
\rho_t \to \rho
$$
 as  $t \to 0$  if and only if *(i)*  $\rho_t \to \rho$  narrowly, and  
\n*(ii)* 
$$
\int_{\mathbb{R}^d} |x|^2 d\rho_t \to \int_{\mathbb{R}^d} |x|^2 d\rho.
$$

We write <sup>C</sup>([0, 1],P(**<sup>R</sup>** d )) for the space of narrowly continuous curves [0, 1] → P(**<sup>R</sup>** d ), and <sup>C</sup>(ρ0, ρ) for the space of narrowly continuous curves [0, 1] → P(**<sup>R</sup>** d ) starting in ρ<sup>0</sup> and ending in ρ. Similarly, for Wasserstein-continuous curves in <sup>P</sup>2(**<sup>R</sup>** d ) we write C<sup>W</sup><sup>2</sup> ([0, 1],P2(**<sup>R</sup>** d )) and C<sup>W</sup><sup>2</sup> (ρ0, ρ).

Furthermore, we use two different notions of absolutely continuous curves. The first notion is taken from [\[DG87,](#page-23-6) Def. 4.1]. Let D = C ∞ c (**R** d ) be the space of test functions with the corresponding topology (see [\[Rud73,](#page-24-5) Sect. 6.3]), let D′ be its dual, consisting of the associated distributions, and let <sup>h</sup>, <sup>i</sup> be the dual pairing between <sup>D</sup>′ and <sup>D</sup>. We will identify a measure <sup>ρ</sup> ∈ P(**<sup>R</sup>** d ) with a distribution by setting <sup>h</sup>ρ, f<sup>i</sup> := <sup>R</sup> f dρ. Denote by D<sup>K</sup> ⊂ D the subspace of all Schwartz functions with compact support <sup>K</sup> <sup>⊂</sup> **<sup>R</sup>** d . Then a curve ρ(·) : [0, 1] → D′ is said to be absolutely continuous in the distributional sense if for each compact set <sup>K</sup> <sup>⊂</sup> **<sup>R</sup>** d there is a neighborhood U<sup>K</sup> of 0 in D<sup>K</sup> and an absolutely continuous function <sup>G</sup><sup>K</sup> : [0, 1] <sup>→</sup> **<sup>R</sup>** such that

$$
|\langle \rho_{t_2}, f \rangle - \langle \rho_{t_1}, f \rangle| \leq |G_K(t_2) - G_K(t_1)|,
$$

for all 0 < t1, t<sup>2</sup> < 1 and f ∈ UK. We denote by AC([0, 1]; D′ ) the set of all absolutely continuous maps in distributional sense. Note that if a map ρ(·) : [0, 1] → D′ is absolutely continuous then the derivative in the distributional sense ˙ρ<sup>t</sup> = lim<sup>τ</sup>→<sup>0</sup> 1 τ (ρ<sup>t</sup>+<sup>τ</sup> − ρt) exists for almost all t ∈ [0, 1].

Secondly, we say a curve ρ(·) : [0, 1] → P2(**<sup>R</sup>** d ) is absolutely continuous in the Wasserstein sense if there exists a g ∈ L 1 (0, 1) such that

$$
W_2(\rho_{t_1}, \rho_{t_2}) \le \int_{t_1}^{t_2} g(t) dt
$$

for all 0 < t<sup>1</sup> ≤ t<sup>2</sup> < 1 (see for example [\[AGS08\]](#page-23-0)). We denote the set of absolutely continuous curves as AC<sup>W</sup><sup>2</sup> ([0, 1];P2(**<sup>R</sup>** d )).

For an absolutely continuous curve <sup>ρ</sup>(·) there is a unique Borel field <sup>v</sup><sup>t</sup> <sup>∈</sup> <sup>V</sup> := {∇<sup>p</sup> : <sup>p</sup> ∈ D}<sup>L</sup> 2 (ρt) such that the continuity equation holds [\[AGS08,](#page-23-0) Th. 8.3.1]:

<span id="page-4-2"></span>
$$
\frac{\partial \rho_t}{\partial t} + \text{div}(\rho_t v_t) = 0 \qquad \text{in distributional sense.} \tag{9}
$$

This motivates the identification of the tangent space[1](#page-4-0) of <sup>P</sup>2(**<sup>R</sup>** d ) at ρ with all s ∈ D′ for which there exists a v ∈ V such that

<span id="page-4-1"></span>
$$
s + \operatorname{div}(\rho v) = 0 \qquad \text{in distributional sense.} \tag{10}
$$

The following inner product on the tangent space at ρ is the metric tensor corresponding to the Wasserstein metric [\[Ott01\]](#page-24-1)

$$
(s_1, s_2)_{-1,\rho} := \frac{1}{2} \int_{\mathbb{R}^d} v_1 \cdot v_2 \, d\rho,
$$

where v<sup>1</sup> and v<sup>2</sup> are associated with s<sup>1</sup> and s<sup>2</sup> through [\(10\)](#page-4-1). The corresponding norm coincides with the dual operator norm on D′

$$
||s||_{-1,\rho}^2 := \sup_{p \in \mathcal{D}} \left\{ \langle s, p \rangle - \frac{1}{2} \int_{\mathbb{R}^d} |\nabla p|^2 d\rho \right\}.
$$
 (11)

This norm is closely related to the Wasserstein metric through the Benamou-Brenier formula [\[BB00\]](#page-23-7)

$$
W_2(\rho_0, \rho_1)^2 = \min \left\{ \int_0^1 \|\frac{\partial \rho_t}{\partial t}\|_{-1, \rho_t}^2 dt : \rho_t|_{t=0} = \rho_0 \text{ and } \rho_t|_{t=1} = \rho_1 \right\}.
$$
 (12)

<span id="page-4-0"></span><sup>1</sup>Here we like to point out that in [\[AGS08\]](#page-23-0) the tangent space is identified with the set of velocity fields V .

Observe that, in approximation, any small perturbation ρ<sup>t</sup> from a <sup>ρ</sup> ∈ P2(**<sup>R</sup>** d ) can be specified by a potential p ∈ D such that [\(9\)](#page-4-2) holds with ρ<sup>0</sup> = ρ and v = ∇p. Following [\[FK06,](#page-24-6) Definition 9.36], for any <sup>F</sup> : <sup>P</sup>(**<sup>R</sup>** d ) → [−∞, +∞], we write, if it exists, grad F(ρ) for the unique element in D′ such that for each p ∈ D and each ρ(·) : [0, <sup>∞</sup>) → P(**<sup>R</sup>** d ) satisfying [\(9\)](#page-4-2) with ρ<sup>0</sup> = ρ and v = ∇p, we have

$$
\lim_{t \to 0^+} \frac{\mathcal{F}(\rho_t) - \mathcal{F}(\rho)}{t} = \langle \text{grad}\,\mathcal{F}(\rho), p \rangle.
$$

Let F(ρ) = E(ρ) + S(ρ) be the free energy defined as in [\(3\)](#page-1-0). By [\[FK06,](#page-24-6) Theorem D.28], if F(ρ) < ∞, then

$$
\operatorname{grad} \mathcal{F}(\rho) = -(\Delta \rho + \operatorname{div}(\rho \nabla \Psi)) \quad \text{in} \quad \mathcal{D}'(\mathbb{R}^d).
$$

The following functional plays a central role in this paper

<span id="page-5-4"></span>
$$
\|\Delta \rho\|_{-1,\rho}^2 = \begin{cases} \int_{\mathbb{R}^d} \frac{|\nabla \rho(x)|^2}{\rho(x)} dx & \text{if } \rho(dx) = \rho(x) dx \text{ and } \sqrt{\rho} \in H^1(\mathbb{R}^d), \\ \infty & \text{otherwise,} \end{cases}
$$
(13)

where ∇ρ is the distributional derivative of ρ. This functional is also known as the Fisher information.

We conclude this section with two results that we will need.

<span id="page-5-0"></span>Lemma 2.1. [\[AGS08,](#page-23-0) Th. 8.3.1] Let ρ(·) : (0, τ ) → P(**<sup>R</sup>** d ) be a narrowly continuous curve and let v(·) : (0, τ ) → V be a vector field such that the continuity equation [\(9\)](#page-4-2) holds. If

<span id="page-5-1"></span>
$$
\rho_0 \in \mathcal{P}_2(\mathbb{R}^d) \ and \ \int_0^\tau \left\|v_t\right\|_{L^2(\rho_t)}^2 dt < \infty \tag{14}
$$

then <sup>ρ</sup><sup>t</sup> ∈ P2(**<sup>R</sup>** d ) for all 0 < t < τ and ρ(·) is absolutely continuous in the Wasserstein sense.

Remark 2.2. We point out that the hypothesis in Lemma [2.1](#page-5-0) requires a priori that the curve ρ(·) lies in <sup>P</sup>2(**<sup>R</sup>** d ), but the proof actually shows that the condition [\(14\)](#page-5-1) implies the whole curve to be in <sup>P</sup>2(**<sup>R</sup>** d ) (and it is absolutely continuous in the Wasserstein sense).

<span id="page-5-2"></span>Lemma 2.3. Assume that ρ(·) : (0, τ ) → P2(**<sup>R</sup>** d ) is a Wasserstein-absolutely continuous curve.

1. If Ψ ∈ C 2 (**R** d ) is convex, bounded from below, and it satisfies the conditions

$$
\mathcal{E}(\rho_t) < \infty \quad \forall t \in [0, \tau] \text{ and } \int_0^{\tau} \int_{\mathbb{R}^d} |\nabla \Psi(x)|^2 \rho_t(x) dx dt < +\infty,
$$

then t 7→ E(ρt) is absolutely continuous.

2. If

$$
\mathcal{S}(\rho_t) < \infty \quad \forall t \in [0, \tau] \text{ and } \int_0^{\tau} ||\Delta \rho_t||_{-1, \rho_t}^2 dt < \infty,
$$

then t 7→ S(ρt) is absolutely continuous.

If the conditions in both parts are satisfied, then grad F(ρt) exists and the following chain rule holds

<span id="page-5-3"></span>
$$
\frac{d}{dt}\mathcal{F}(\rho_t) = \left(\text{grad}\,\mathcal{F}(\rho_t), \frac{\partial}{\partial t}\rho_t\right)_{-1,\rho_t}.\tag{15}
$$

<span id="page-6-0"></span>Proof. This Lemma is a direct consequence of [\[AGS08,](#page-23-0) Th. 10.3.18]. Since the functionals E(ρ) and S(ρ) are lower semicontinuous and geodesically convex, we only need to check condition [\[AGS08,](#page-23-0) 10.1.17]. This condition in turn is satisfied by the Cauchy-Schwartz inequality hf, giL2(a,b) ≤ kfkL2(a,b)kgkL2(a,b) and the assumptions.

### 3 Particle system and conditional large deviations

In this section we first explain the concept of large deviations with a simple model particle system. Then, we introduce the dynamic particle system that we study more precisely, and discuss the large deviation principle for this system.

Consider a system of independent random particles in **R** d (without dynamics), where the positions X1, . . . , X<sup>N</sup> are identically distributed with law ρ0. Then as a consequence of the law of large numbers L<sup>N</sup> → ρ<sup>0</sup> almost surely in the narrow topology as N → ∞ [\[Dud89,](#page-23-4) Th. 11.4.1]. Naturally, this implies weak convergence:

$$
\lim_{N \to \infty} \text{Prob}(L_N \in C) = \delta_{\rho_0}(C)
$$

for all continuity sets <sup>C</sup> ⊂ P(**<sup>R</sup>** d ) in the narrow topology. A large deviation principle quantifies the exponential rate of convergence to 0 (or 1). More precisely, we say the system satisfies a large deviation principle in <sup>P</sup>(**<sup>R</sup>** d ) with (unique) rate <sup>J</sup> : <sup>P</sup>(**<sup>R</sup>** d ) → [0, ∞] if J is lower semicontinuous, and for all sets <sup>U</sup> ⊂ P(**<sup>R</sup>** d ) there holds (see, for example [\[DZ87\]](#page-24-7))

$$
-\inf_{U^{\circ}} J \le \liminf_{N \to \infty} \frac{1}{N} \log \text{Prob}(L_N \in U^{\circ}) \le \limsup_{N \to \infty} \frac{1}{N} \log \text{Prob}(L_N \in \overline{U}) \le -\inf_{\overline{U}} J.
$$

In addition, we say a rate functional is good if it has compact sub-level sets. By Sanov's Theorem [\[DZ87,](#page-24-7) Th. 6.2.10], our model example indeed satisfies a large deviation principle, where the good rate functional J(ρ) is the relative entropy

$$
\mathcal{H}(\rho|\rho^0) := \begin{cases} \int \log(\frac{d\rho}{d\rho^0}) d\rho, & \text{if } \rho \ll \rho^0, \\ \infty, & \text{otherwise.} \end{cases}
$$
\n(16)

In this example we see the (relative) entropy appearing naturally from a limit of a simple particle system.

Let us now consider our particle system with dynamics, and study its Sanov-type large deviations. To define the system more precisely, let X1(t), · · · , X<sup>N</sup> (t) be a sequence of independent random processes in **R** d . Assume that the initial values are fixed deterministically by some X1(0) = x1, . . . X<sup>N</sup> (0) = x<sup>N</sup> in such a way that [2](#page-6-1)

<span id="page-6-2"></span>
$$
L_N(0) \to \rho_0
$$
 *narrowly for some given*  $\rho_0 \in \mathcal{P}(\mathbb{R}^d)$ . (17)

<span id="page-6-1"></span><sup>2</sup>The reason behind this specific initial condition is that we want to somehow condition on L<sup>N</sup> = ρ, which is a measure-0 set.

The evolution of the system is prescribed by the same transition probability for each particle Prob(Xk(t) ∈ dy|Xk(0) = x) = pt(dy|x). Naturally, for such probability there must hold pt(dy|x) → δx(dy) narrowly as t → 0, and it should evolve according to [\(4\)](#page-1-1). We thus define p<sup>t</sup> to be the fundamental solution of [\(4\)](#page-1-1) [3](#page-7-2) .

Again by the law of large numbers <sup>L</sup><sup>N</sup> (<sup>τ</sup> ) <sup>→</sup> <sup>ρ</sup><sup>τ</sup> almost surely in <sup>P</sup>(**<sup>R</sup>** d ), where ρ<sup>τ</sup> = ρ<sup>0</sup> ∗ p<sup>τ</sup> , the solution of [\(4\)](#page-1-1) at time τ with initial condition ρ0. In addition, the empirical measure L<sup>N</sup> (τ ) satisfies a large deviation principle

$$
\text{Prob}\left(L_N(\tau) \approx \rho\right) \sim \exp\left(-NJ_\tau(\rho|\rho_0)\right) \quad \text{as } N \to \infty.
$$

<span id="page-7-1"></span>with good rate functional [\(5\)](#page-1-2). Observe that J<sup>τ</sup> (· |ρ0) ≥ 0 is minimised by ρ<sup>0</sup> ∗ p<sup>τ</sup> .

### 4 Large deviations of trajectories

In this section we prove, under suitable assumptions for ρ<sup>0</sup> and Ψ, the equivalence of the rate functionals [\(5\)](#page-1-2) and [\(6\)](#page-2-2). The latter form will be used to prove the main Gamma convergence theorem. First, the large deviations of the empirical process is derived. To this aim we will need to distinguish between two different types of potentials Ψ. Next, we transform these large deviation principles back to the large deviations of the empirical measure L<sup>N</sup> (τ ) by a contraction principle, and finally show that the resulting rate functionals are the same for both cases.

In the first case we consider potentials that satisfy the following

<span id="page-7-0"></span>Assumption 4.1 (The subquadratic case). Let Ψ ∈ C 2 (**R** d ) such that

- 1. Ψ is bounded from below,
- 2. there is a C > 0 such that |x||∇Ψ(x)| ≤ C(1 + |x| 2 ) for all <sup>x</sup> <sup>∈</sup> **<sup>R</sup>** d ,
- 3. Ψ is convex,
- 4. ∆Ψ is bounded.

Note that the second assumption indeed implies |Ψ(x)| ≤ C(1 + |x| 2 ). Under Assumption [4.1,](#page-7-0) combined with initial condition [\(17\)](#page-6-2), the empirical process {L<sup>N</sup> (t)}0≤t≤<sup>τ</sup> satisfies a large deviation principle in <sup>C</sup>([0, τ ],P(**<sup>R</sup>** d )) with good rate functional [\[DG87,](#page-23-6) Th. 4.5]

<span id="page-7-3"></span>
$$
\tilde{J}_{\tau}(\rho_{(\cdot)}) = \begin{cases} \frac{1}{4} \int_0^{\tau} \|\frac{\partial \rho_t}{\partial t} - \Delta \rho_t - \text{div}(\rho_t \nabla \Psi)\|_{-1,\rho_t}^2 dt, & \text{if } \rho_{(\cdot)} \in \text{AC}([0,\tau]; \mathcal{D}'),\\ \infty, & \text{otherwise.} \end{cases}
$$
(18)

<span id="page-7-2"></span><sup>3</sup>Equivalently, we can define the dynamics of X1, . . . , X<sup>N</sup> by the It¯o stochastic equations

dXk(t) = −∇Ψ(Xk(t)) dt + √ 2 dWk(t), k = 1, · · · , N

where W1, . . . , W<sup>N</sup> are independent Wiener processes.

It follows from a contraction principle [\[DZ87,](#page-24-7) Th. 4.2.1] and a change of variables t 7→ t/τ that

<span id="page-8-1"></span>
$$
J_{\tau}(\rho|\rho_0) = \inf_{\rho_{(\cdot)} \in C(\rho_0, \rho)} \frac{1}{4\tau} \int_0^1 \left\| \frac{\partial \rho_t}{\partial t} - \tau (\Delta \rho_t + \text{div}(\rho_t \nabla \Psi)) \right\|_{-1, \rho_t}^2 dt.
$$
 (19)

Remark 4.2. The first assumption guarantees that the functional <sup>E</sup> : <sup>P</sup>(**<sup>R</sup>** d ) → (−∞, ∞] is well defined. The last two assumptions are not necessary to derive [\(18\)](#page-7-3); however we will need them in the sequel. Especially the last one is a technical assumption that we will need in Lemma [4.7.](#page-9-0) It can be relaxed in several ways, but for simplicity we chose not to.

Remark 4.3. In [\(19\)](#page-8-1) we implicitly set <sup>1</sup> 4τ R 1 0 k ∂ρt ∂t − τ (∆ρ<sup>t</sup> + div(ρt∇Ψ))k 2 −1,ρt dt = ∞ if the curve is not absolutely continuous in distributional sense. Therefore, from now on, we shall only consider curves in C(ρ0, ρ) or C<sup>W</sup><sup>2</sup> (ρ0, ρ) that are absolutely continuous in distributional sense.

In the second case we require a combination of assumptions on Ψ that were taken from [\[FK06\]](#page-24-6) and [\[FN11\]](#page-24-8):

<span id="page-8-0"></span>Assumption 4.4 (The superquadratic case). Let Ψ ∈ C 4 (**R** d ) such that:

- 1. There is some <sup>λ</sup><sup>Ψ</sup> <sup>∈</sup> **<sup>R</sup>** such that <sup>z</sup> <sup>T</sup> <sup>D</sup><sup>2</sup>Ψ(x)<sup>z</sup> <sup>≥</sup> <sup>λ</sup><sup>Ψ</sup> <sup>|</sup>z<sup>|</sup> 2 for all x, z <sup>∈</sup> **<sup>R</sup>** d ;
- 2. R **<sup>R</sup>**<sup>d</sup> Ψ(x)e <sup>−</sup>2Ψ(x) dx < <sup>∞</sup>;
- 3. Ψ has superquadratic growth at infinity, i.e. lim|x|→∞ Ψ(x) |x| <sup>2</sup> = +∞;
- 4. There exists an <sup>ω</sup> <sup>∈</sup> <sup>C</sup>(**R**+) with <sup>ω</sup>(0) = 0 such that for all x, y <sup>∈</sup> **<sup>R</sup>** d

$$
\Psi(y) - \Psi(x) \le \omega(|y - x|)(1 + \Psi(x)),
$$
  
$$
|\Psi(y) - \Psi(x)|^2 \le \omega(|y - x|)(1 + |\nabla\Psi(x)|^2 + \Psi(x));
$$

5. ζ := |∇Ψ| <sup>2</sup> − 2∆Ψ has superquadratic growth at infinity, i.e. lim|x|→∞ ζ(x) |x| <sup>2</sup> = +∞;

6. There is some <sup>λ</sup><sup>ζ</sup> <sup>∈</sup> **<sup>R</sup>** such that <sup>z</sup> <sup>T</sup> D<sup>2</sup> ζ(x)z ≥ λ<sup>ζ</sup> |z| 2 for all x, z <sup>∈</sup> **<sup>R</sup>** d .

Whenever Assumption [4.4](#page-8-0) and initial condition [\(17\)](#page-6-2) hold, then by [\[FK06,](#page-24-6) Th. 13.37] the process {L<sup>N</sup> (t)}0≤t≤<sup>τ</sup> satisfies a large deviation principle in C<sup>W</sup><sup>2</sup> ([0, τ ],P2(**<sup>R</sup>** d )) with good rate functional [\(18\)](#page-7-3).

Remark 4.5. Contrary to the subquadratic case, the latter is actually a large deviation principle on the set of all continuous paths in <sup>P</sup>2(**<sup>R</sup>** d ) with respect to the Wasserstein topology. Although we strongly believe that this is also true for the subquadratic case, it is very difficult to prove due to the fact that the functional J˜ <sup>τ</sup> does not have Wasserstein-compact sub-level sets, and therefore it can't be a good rate functional in C<sup>W</sup><sup>2</sup> ([0, τ ],P2(**<sup>R</sup>** d )) when Ψ is subquadratic.

Again, by a contraction principle and a simple change of variables, it follows from [\(18\)](#page-7-3) that [\(5\)](#page-1-2) must be equal to:

$$
J_{\tau}(\rho|\rho_0) = \inf_{\rho(\cdot) \in C_{W_2}(\rho_0, \rho)} \frac{1}{4\tau} \int_0^1 \left\| \frac{\partial \rho_t}{\partial t} - \tau (\Delta \rho_t + \text{div}(\rho_t \nabla \Psi)) \right\|_{-1, \rho_t}^2 dt.
$$
 (20)

Observe that in this case the infimum is taken over Wasserstein-continuous curves, while in the subquadratic case [\(19\)](#page-8-1) the infimum was over narrowly continuous curves. However, we will prove that under the extra assumption that <sup>ρ</sup><sup>0</sup> ∈ P2(**<sup>R</sup>** d ) and F(ρ0) is finite, even in the subquadratic case the infimum can be taken over C<sup>W</sup><sup>2</sup> (ρ0, ρ). Actually, we will prove something even stronger, that we will need in the sequel, namely the following:

<span id="page-9-3"></span>Proposition 4.6. Let Ψ ∈ C 2 (**R** d ) satisfy Assumption [4.1.](#page-7-0) Let <sup>ρ</sup><sup>0</sup> ∈ P2(**<sup>R</sup>** d ) with F(ρ0) < ∞, and assume <sup>ρ</sup>(·) <sup>∈</sup> <sup>C</sup>(ρ0, ρ) with <sup>J</sup>˜ <sup>τ</sup> (ρ(·)) finite. Then <sup>ρ</sup><sup>t</sup> ∈ P2(**<sup>R</sup>** d ) for every t. Furthermore, the curve ρ(·) lies in AC<sup>W</sup><sup>2</sup> [0, 1];P2(**<sup>R</sup>** d ) and F(ρt) is absolutely continuous with respect to t. Finally there holds:

$$
\frac{1}{4\tau} \int_0^1 \left\| \frac{\partial \rho_t}{\partial t} - \tau (\Delta \rho_t + \text{div}(\rho_t \nabla \Psi)) \right\|_{-1,\rho_t}^2 dt
$$
\n
$$
= \frac{1}{4\tau} \int_0^1 \left\| \frac{\partial \rho_t}{\partial t} \right\|_{-1,\rho_t}^2 dt + \frac{\tau}{4} \int_0^1 \left\| \text{grad } \mathcal{F}(\rho_t) \right\|_{-1,\rho_t}^2 dt + \frac{1}{2} \mathcal{F}(\rho_1) - \frac{1}{2} \mathcal{F}(\rho_0).
$$

Before we prove this theorem we prove two auxiliary lemmas.

<span id="page-9-0"></span>Lemma 4.7. Assume that

- 1. Ψ ∈ C 2 (**R** d ) satisfies Assumption [4.1,](#page-7-0)
- 2. R Ψρ0(dx) < ∞,
- 3. ρ(·) ∈ C(ρ0, ρ),
- 4. J˜ <sup>τ</sup> (ρ(·)) < ∞.

Then

<span id="page-9-1"></span>
$$
\int_0^\tau \int_{\mathbb{R}^d} |\nabla \Psi(x)|^2 \rho_t(dx) dt < \infty.
$$
 (21)

Proof. For simplicity we take τ = 1. We will prove the following statement: there exist 0 < δ ≤ 1 and α, β > 0 that depend only on Ψ such that

<span id="page-9-2"></span>
$$
\alpha \sup_{t \in [0,\delta]} \int_{\mathbb{R}^d} |\Psi| \, d\rho_t + \beta \int_0^{\delta} \int_{\mathbb{R}^d} |\nabla \Psi|^2 \, d\rho_t \, dt \le 8 \tilde{J}_1(\rho(\cdot)) + \frac{4}{e} |\inf \Psi| + \frac{2}{e} \int_{\mathbb{R}^d} \Psi \, d\rho_0 + \frac{2\delta}{e} ||\Delta \Psi||_{\infty}.\tag{22}
$$

Obviously [\(21\)](#page-9-1) follows from [\(22\)](#page-9-2) by repeating it 1/δ times.

We will approximate Ψ by a sequence of C 2 c (**R** d ) functions which are allowed in the definition of the norm k · k−1. To account for the compact support we use the usual bump function:

<span id="page-10-1"></span>
$$
\eta(x) := \begin{cases} \exp\left(\frac{-1}{1-|x|^2}\right), & |x| \le 1\\ 0, & |x| > 1. \end{cases}
$$

Define ηk(x) := η(x/k). Then the following estimates hold

$$
|\eta_k(x)| \le 1/e, \qquad |\nabla \eta_k(x)| \le \frac{1}{k} \qquad \text{and} \qquad |\Delta \eta_k(x)| \le \frac{1}{k^2} \|\Delta \eta\|_{\infty} < \infty. \tag{23}
$$

<span id="page-10-0"></span>Since ηkΨ ∈ D the rate functional [\(18\)](#page-7-3) is bounded from below by

$$
4\tilde{J}_{1}(\rho_{(\cdot)}) = \int_{0}^{1} \sup_{p \in \mathcal{D}} \left( \langle \partial_{t}\rho_{t} - \Delta \rho_{t} - \text{div}(\rho_{t}\nabla\Psi), p \rangle - \frac{1}{2} \int_{\mathbb{R}^{d}} |\nabla p|^{2} d\rho_{t} \right) dt
$$
  
\n
$$
\geq \int_{0}^{s} \left( \langle \partial_{t}\rho_{t} - \Delta \rho_{t} - \text{div}(\rho_{t}\nabla\Psi), \eta_{k}\Psi \rangle - \frac{1}{2} \int_{\mathbb{R}^{d}} |\nabla(\eta_{k}\Psi)|^{2} d\rho_{t} \right) dt
$$
\n(24)

for any s ∈ [0, 1]. We now estimate each term in the right-hand side of [\(24\)](#page-10-0). For the first term, we have

<span id="page-10-2"></span>
$$
\int_0^s \langle \partial_t \rho_t, \eta_k \Psi \rangle dt = \int_{\mathbb{R}^d} \eta_k \Psi d\rho_s - \int_{\mathbb{R}^d} \eta_k \Psi d\rho_0 \ge \int_{\mathbb{R}^d} \eta_k |\Psi| d\rho_s - \frac{2}{e} |\inf \Psi| - \int_{\mathbb{R}^d} \eta_k \Psi d\rho_0. \tag{25}
$$

For the second part, we find

<span id="page-10-3"></span>
$$
-\int_{0}^{s} \langle \Delta \rho_t, \eta_k \Psi \rangle dt = -\int_{0}^{s} \int_{\mathbb{R}^d} (\Psi \Delta \eta_k + 2\nabla \eta_k \cdot \nabla \Psi + \eta_k \Delta \Psi) d\rho_t dt
$$
  
\n
$$
\geq -\int_{0}^{s} \int_{\mathbb{R}^d} (|\Delta \eta_k| |\Psi| + |\nabla \eta_k| (|\nabla \Psi|^2 + 1) + \eta_k |\Delta \Psi|) d\rho_t dt
$$
  
\n
$$
\stackrel{(23)}{\geq} - \int_{0}^{s} \int_{[-k,k]^d} \left( \frac{1}{k^2} ||\Delta \eta||_{\infty} |\Psi| + \frac{1}{k} (|\nabla \Psi|^2 + 1) + \frac{1}{e} |\Delta \Psi| \right) d\rho_t dt
$$
  
\n
$$
\geq -\frac{s}{k^2} ||\Delta \eta||_{\infty} \sup_{t \in [0,s]} \int_{[-k,k]^d} |\Psi| d\rho_t - \frac{1}{k} \int_{0}^{s} \int_{[-k,k]^d} |\nabla \Psi|^2 d\rho_t dt - \frac{s}{k} - \frac{s}{e} ||\Delta \Psi||_{\infty}.
$$
  
\n(26)

Finally, for the last part

<span id="page-11-0"></span>
$$
\int_{0}^{s} \left( \langle -\operatorname{div}(\rho_{t} \nabla \Psi), \eta_{k} \Psi \rangle - \frac{1}{2} \int_{\mathbb{R}^{d}} |\nabla(\eta_{k} \Psi)|^{2} d\rho_{t} \right) dt \n= \int_{0}^{s} \int_{\mathbb{R}^{d}} \left( -\frac{1}{2} |\nabla \eta_{k}|^{2} \Psi^{2} + (1 - \eta_{k}) \nabla \eta_{k} \cdot \Psi \nabla \Psi + (1 - \frac{1}{2} \eta_{k}) \eta_{k} |\nabla \Psi|^{2} \right) d\rho_{t} dt \n\stackrel{(23)}{\geq} \int_{0}^{s} \int_{[-k,k]^{d}} \left( -\frac{1}{2k^{2}} \Psi^{2} - \left| \frac{2}{k} \Psi \right| \left| \frac{1}{2} \nabla \Psi \right| + \frac{3}{4} \eta_{k} |\nabla \Psi|^{2} \right) d\rho_{t} dt \n\geq \int_{0}^{s} \int_{[-k,k]^{d}} \left( -\frac{5}{2k^{2}} \Psi^{2} + \left( \frac{3}{4} \eta_{k} - \frac{1}{8} \right) |\nabla \Psi|^{2} \right) d\rho_{t} dt \n\geq \int_{0}^{s} \int_{[-k,k]^{d}} \left( -\frac{5C(1+k^{2})}{2k^{2}} |\Psi| + \left( \frac{3}{4} \eta_{k} - \frac{1}{8} \right) |\nabla \Psi|^{2} \right) d\rho_{t} dt \n\geq -\frac{5sC(1+k^{2})}{2k^{2}} \sup_{t \in [0,s]} \int_{[-k,k]^{d}} |\Psi| d\rho_{t} + \int_{0}^{s} \int_{[-k,k]^{d}} \left( \left( \frac{3}{4} \eta_{k} - \frac{1}{8} \right) |\nabla \Psi|^{2} \right) d\rho_{t} dt,
$$
\n(27)

where the fourth line follows from Young's inequality, and in the fifth line we used the subquadratic assumption. Substituting [\(25\)](#page-10-2), [\(26\)](#page-10-3) and [\(27\)](#page-11-0) into [\(24\)](#page-10-0) we get

$$
\int_{\mathbb{R}^d} \eta_k |\Psi| \, d\rho_s + \int_0^s \int_{[-k,k]^d} \frac{3}{4} \eta_k |\nabla \Psi|^2 \, d\rho_t \, dt \le 4 \tilde{J}_1(\rho_{(\cdot)}) + \frac{2}{e} |\inf \Psi| + \int_{\mathbb{R}^d} \eta_k \Psi \, d\rho_0 + \frac{s}{k} + \frac{s}{e} ||\Delta \Psi||_{\infty} + \left(\frac{s}{k^2} ||\Delta \eta||_{\infty} + \frac{5sC(1+k^2)}{2k^2} \right) \sup_{t \in [0,s]} \int_{[-k,k]^d} |\Psi| \, d\rho_t + \left(\frac{1}{8} + \frac{1}{k} \right) \int_0^s \int_{[-k,k]^d} |\nabla \Psi|^2 \, d\rho_t \, dt.
$$

If we first discard the first term on the left-hand side and maximise the equation over s ∈ [0, δ] for some 0 < δ ≤ 1, then discard the second term and maximise, the sum of the inequalities can be written as

<span id="page-11-1"></span>
$$
\sup_{t \in [0,\delta]} \int_{\mathbb{R}^d} \left( \eta_k - \frac{2\delta}{k^2} \|\Delta \eta\|_{\infty} - \frac{5\delta C(1+k^2)}{k^2} \right) |\Psi| \, d\rho_t + \int_0^{\delta} \int_{[-k,k]^d} \left( \frac{3}{4} \eta_k - \frac{1}{4} - \frac{2}{k} \right) |\nabla \Psi|^2 \, d\rho_t \, dt
$$
  
$$
\leq 8\tilde{J}_1(\rho_{(\cdot)}) + \frac{4}{e} |\inf \Psi| + 2 \int_{\mathbb{R}^d} \eta_k \Psi \, d\rho_0 + \frac{2\delta}{k} + \frac{2\delta}{e} \|\Delta \Psi\|_{\infty}.
$$
 (28)

Taking the supremum over k ≥ 1, the inequality [\(28\)](#page-11-1) becomes

$$
\begin{split}\n&\left(\frac{1}{e} - 5\delta C\right) \sup_{t \in [0,\delta]} \int_{\mathbb{R}^d} |\Psi| \, d\rho_t + \left(\frac{3}{4e} - \frac{1}{4}\right) \int_0^\delta \int_{\mathbb{R}^d} |\nabla \Psi|^2 \, d\rho_t \, dt \\
&\leq 8\tilde{J}_1(\rho_{(\cdot)}) + \frac{4}{e} |\inf \Psi| + 2 \sup_k \left\{ \int_{\mathbb{R}^d} \eta_k \Psi \, d\rho_0 \right\} + 2\delta + \frac{2\delta}{e} \|\Delta \Psi\|_{\infty} \\
&\leq 8\tilde{J}_1(\rho_{(\cdot)}) + \frac{8}{e} |\inf \Psi| + \frac{2}{e} \int_{\mathbb{R}^d} \Psi \, d\rho_0 + 2\delta + \frac{2\delta}{e} \|\Delta \Psi\|_{\infty},\n\end{split}
$$

as sup<sup>k</sup> R ηkΨ dρ<sup>0</sup> ≤ sup<sup>k</sup> R <sup>η</sup>k|Ψ<sup>|</sup> dρ<sup>0</sup> <sup>≤</sup> <sup>1</sup>/e <sup>R</sup> <sup>|</sup>Ψ<sup>|</sup> dρ<sup>0</sup> <sup>≤</sup> <sup>1</sup>/e <sup>R</sup> (Ψ + 2| inf Ψ|) dρ0. Take δ such that α > 0. Now that we know that the suprema are finite, we can take the limit k → ∞ of [\(28\)](#page-11-1), which proves [\(22\)](#page-9-2).

The second auxiliary lemma is:

<span id="page-12-0"></span>Lemma 4.8. Let ǫ > <sup>0</sup> and <sup>ρ</sup>(x) dx ∈ P(**<sup>R</sup>** d ) be given. Let θ(x) := 1 2π d <sup>2</sup> e −|x| 2 <sup>2</sup> be the density of the d-dimensional normal distribution. We define θǫ(x) := ǫ −d θ( x ǫ ) and ρ<sup>ǫ</sup> := ρ ∗ θ<sup>ǫ</sup> . Then there exists a constant C<sup>ǫ</sup> that depends only on ǫ such that k∆(ρǫ)k 2 <sup>−</sup>1,ρ<sup>ǫ</sup> < C<sup>ǫ</sup> .

Proof. We have

$$
\nabla \rho_{\epsilon}(x) = (\rho * \nabla \theta_{\epsilon})(x) = \int_{\mathbb{R}^d} \rho(x - y) \nabla \theta_{\epsilon}(y) dy = -\epsilon^{-2} \int_{\mathbb{R}^d} \rho(x - y) y \theta_{\epsilon}(y) dy.
$$

Furthermore

$$
|\nabla \rho_{\epsilon}(x)|^2 \leq \epsilon^{-4} \int_{\mathbb{R}^d} \rho(x-y)|y|^2 \theta_{\epsilon}(y) \, dy \int_{\mathbb{R}^d} \rho(x-y) \theta_{\epsilon}(y) \, dy \leq \epsilon^{-4} \rho_{\epsilon}(x) \int_{\mathbb{R}^d} \rho(x-y)|y|^2 \theta_{\epsilon}(y) \, dy.
$$

Now

$$
\|\Delta(\rho_{\epsilon})\|_{-1,\rho_{\epsilon}}^{2} = \int_{\mathbb{R}^{d}} \frac{|\nabla \rho_{\epsilon}(x)|^{2}}{\rho_{\epsilon}(x)} dx \leq \epsilon^{-4} \int_{\mathbb{R}^{d}} \int_{\mathbb{R}^{d}} \rho(x-y)|y|^{2} \theta_{\epsilon}(y) dy dx
$$
  
$$
= \epsilon^{-4} \int_{\mathbb{R}^{d}} \int_{\mathbb{R}^{d}} \rho(x-y) dx |y|^{2} \theta_{\epsilon}(y) dy
$$
  
$$
\leq \epsilon^{-4} \int_{\mathbb{R}^{d}} |y|^{2} \theta_{\epsilon}(y) dy := C_{\epsilon}.
$$

We are now ready to proceed with the

Proof of Proposition [4.6.](#page-9-3) Let ρ(·) satisfy the assumptions (of Proposition [4.6\)](#page-9-3). By Lemma [4.7](#page-9-0) we have

$$
\int_0^1 \int_{\mathbb{R}^d} |\nabla \Psi(x)|^2 \rho_t(dx) dt < \infty
$$

and therefore

$$
\frac{1}{4\tau}\int_0^1 \|\frac{\partial \rho_t}{\partial t} - \tau \Delta \rho_t\|_{-1,\rho_t}^2 dt < \frac{1}{2\tau}\int_0^1 \left\|\frac{\partial \rho_t}{\partial t} - \tau (\Delta \rho_t + \text{div}(\rho_t \nabla \Psi))\right\|_{-1,\rho_t}^2 dt \n+ \frac{\tau}{2}\int_0^1 \int_{\mathbb{R}^d} |\nabla \Psi|^2 \rho_t(dx) dt < \infty.
$$

Take a 0 < s ≤ 1. Since

$$
\frac{1}{4\tau} \int_0^s \left\| \frac{\partial \rho_t}{\partial t} - \tau \Delta \rho_t \right\|_{-1,\rho_t}^2 dt < \infty \tag{29}
$$

we have that k ∂ρt ∂t −τ∆ρtk 2 <sup>−</sup>1,ρ<sup>t</sup> < ∞ for almost every t. By [\[FK06,](#page-24-6) Lem. D.34] there is a v<sup>t</sup> ∈ L 2 (ρt) such that

$$
\frac{\partial \rho_t}{\partial t} - \tau \Delta \rho_t = -\operatorname{div}(v_t \rho_t)
$$

in distributional sense. Take θǫ(x) as in Lemma [4.8.](#page-12-0) Then we have

$$
\frac{\partial \rho_{t,\epsilon}}{\partial t} - \tau \Delta \rho_{t,\epsilon} = - \operatorname{div}(v_{t,\epsilon} \rho_{t,\epsilon}),
$$

where

$$
\rho_{t,\epsilon} = \rho_t * \theta_{\epsilon}(x), \qquad v_{t,\epsilon} = \frac{(v_t \,\rho_t) * \theta_{\epsilon}(x)}{\rho_{t,\epsilon}}.
$$

By [\[AGS08,](#page-23-0) Th. 8.1.9] we have

$$
\frac{1}{4\tau} \int_0^s \left\| \frac{\partial \rho_{t,\epsilon}}{\partial t} - \tau \Delta \rho_{t,\epsilon} \right\|_{-1,\rho_t}^2 dt = \frac{1}{4\tau} \int_0^s \left\| v_{t,\epsilon} \right\|_{L^2(\rho_{t,\epsilon})}^2 dt \le \frac{1}{4\tau} \int_0^s \left\| v_t \right\|_{L^2(\rho_t)}^2 dt = \frac{1}{4\tau} \int_0^s \left\| \frac{\partial \rho_t}{\partial t} - \tau \Delta \rho_t \right\|_{-1,\rho_t}^2 dt. \tag{30}
$$

Furthermore by Lemma [4.8](#page-12-0) we have that

<span id="page-13-0"></span>
$$
\int_0^s \|\Delta \rho_{t,\epsilon}\|_{-1,\rho_{t,\epsilon}}^2 dt \le C_{\epsilon},\tag{31}
$$

and therefore

<span id="page-13-1"></span>
$$
\int_0^s \left\| \frac{\partial \rho_{t,\epsilon}}{\partial t} \right\|_{-1,\rho_{t,\epsilon}}^2 dt < \infty. \tag{32}
$$

From [\(31\)](#page-13-0) and since <sup>ρ</sup>(0) ∈ P2(**<sup>R</sup>** d ), by using [\[FK06,](#page-24-6) Lem. D.34] and Lemma [2.1](#page-5-0) we get that the curve <sup>ρ</sup>t,ǫ is absolutely continuous in <sup>P</sup>2(**<sup>R</sup>** d ). In addition, it is a straightforward that S(ρt,ǫ) is finite for every 0 < t ≤ s. From [\(31\)](#page-13-0), [\(32\)](#page-13-1) and by Lemma [2.3,](#page-5-2) S(ρt,ǫ) is absolutely continuous with respect to t. Hence we obtain

$$
\frac{1}{4\tau} \int_0^s \left\| \frac{\partial \rho_{t,\epsilon}}{\partial t} + \tau \Delta \rho_{t,\epsilon} \right\|_{-1,\rho_t}^2 dt \n= \frac{1}{4\tau} \int_0^s \left\| \frac{\partial \rho_{t,\epsilon}}{\partial t} \right\|_{-1,\rho_t}^2 dt + \frac{\tau}{4} \int_0^s \left\| \Delta \rho_{t,\epsilon} \right\|_{-1,\rho_t}^2 dt + \frac{1}{2} \int_0^s \left( \text{grad } \mathcal{S}(\rho_{t,\epsilon}), \frac{\partial \rho_{t,\epsilon}}{\partial t} \right)_{-1,\rho_t} dt \n= \frac{1}{4\tau} \int_0^s \left\| \frac{\partial \rho_{t,\epsilon}}{\partial t} \right\|_{-1,\rho_t}^2 dt + \frac{\tau}{4} \int_0^s \left\| \Delta \rho_{t,\epsilon} \right\|_{-1,\rho_t}^2 + \frac{1}{2} \mathcal{S}(\rho_{s,\epsilon}) - \frac{1}{2} \mathcal{S}(\rho_{0,\epsilon}).
$$

It follows that

$$
\frac{1}{4\tau}\int_0^s \left\|\frac{\partial \rho_{t,\epsilon}}{\partial t}\right\|_{-1,\rho_t}^2 dt + \frac{\tau}{4}\int_0^s \|\Delta \rho_{t,\epsilon}\|_{-1,\rho_t}^2 dt + \frac{1}{2}\mathcal{S}(\rho_{s,\epsilon}) - \frac{1}{2}\mathcal{S}(\rho_{0,\epsilon}) \leq \frac{1}{4\tau}\int_0^1 \left\|\frac{\partial \rho_t}{\partial t} - \tau \Delta \rho_t\right\|_{-1,\rho_t}^2 dt.
$$

Now letting ǫ go to zero and by the lower semicontinuity of the entropy and the Fisher information functionals we get <sup>S</sup>(ρs) <sup>&</sup>lt; <sup>∞</sup> and <sup>R</sup> <sup>s</sup> 0 k∆ρtk 2 −1,ρt dt < ∞. Therefore

$$
\int_0^s \left\|\frac{\partial \rho_t}{\partial t}\right\|_{-1,\rho_t}^2 dt \le 2 \left( \int_0^s \left\|\frac{\partial \rho_t}{\partial t} - \tau \Delta \rho_t\right\|_{-1,\rho_t}^2 dt + \tau^2 \int_0^s \left\|\Delta \rho_t\right\|_{-1,\rho_t}^2 dt \right) < \infty.
$$

and

$$
\int_0^s \left\| \Delta \rho_t + \text{div} \, \rho_t \nabla \Psi \right\|_{-1,\rho_t}^2 dt \le 2 \left( \int_0^s \|\Delta \rho_t\|_{-1,\rho_t}^2 dt + \int_0^s \int_{\mathbb{R}^d} |\nabla \Psi(x)|^2 \rho_t(x) \, dx \, dt \right) < \infty.
$$

By Lemma [2.1](#page-5-0) and Lemma [2.3](#page-5-2) again, the curve ρ<sup>t</sup> is in AC<sup>W</sup><sup>2</sup> [0, 1];P2(**<sup>R</sup>** d ) . Moreover, t 7→ F(ρt) is absolutely continuous and [\(15\)](#page-5-3) holds. Hence we have

$$
\frac{1}{4\tau} \int_0^1 \left\| \frac{\partial \rho_t}{\partial t} - \tau (\Delta \rho_t + \text{div}(\rho_t \nabla \Psi)) \right\|_{-1,\rho_t}^2 dt
$$
\n
$$
= \frac{1}{4\tau} \int_0^1 \left\| \frac{\partial \rho_t}{\partial t} \right\|_{-1,\rho_t}^2 dt + \frac{\tau}{4} \int_0^1 \left\| \Delta \rho_t + \text{div}(\rho_t \nabla \Psi)) \right\|_{-1,\rho_t}^2 dt + \frac{1}{2} \mathcal{F}(\rho_1) - \frac{1}{2} \mathcal{F}(\rho_0).
$$

This finishes the proof of the Lemma.

Remark 4.9. For the superquadratic case, the above lemma was proved by Feng and Nguyen in [\[FN11\]](#page-24-8) by using probabilistic tools. In addition, they obtain an estimate for the growth of F along the curves.

Now the following is a straightforward result:

<span id="page-14-1"></span>Corollary 4.10. Let <sup>ρ</sup><sup>0</sup> ∈ P2(**<sup>R</sup>** d ) with F(ρ0) < ∞. If Ψ ∈ C 2 (**R** d ) satisfies either Assumption [4.1](#page-7-0) or [4.4,](#page-8-0) then

$$
J_{\tau}(\rho|\rho_0) = \inf_{\rho_{(\cdot)} \in C_{W_2}(\rho_0, \rho)} \frac{1}{4\tau} \int_0^1 \left\| \frac{\partial \rho_t}{\partial t} - \tau (\Delta \rho_t + \text{div}(\rho_t \nabla \Psi)) \right\|_{-1, \rho_t}^2 dt.
$$

### 5 Lower bound

In this section we prove the lower bound of the Gamma convergence [\(7\)](#page-2-0) in our main result, Theorem [1.1.](#page-2-3)

<span id="page-14-0"></span>Theorem 5.1 (Lower bound). Under the assumptions of Theorem [1.1,](#page-2-3) we have for any ρ<sup>1</sup> ∈ <sup>P</sup>2(**<sup>R</sup>** d ) and all sequences ρ τ <sup>1</sup> ∈ P2(**<sup>R</sup>** d ) narrowly converging to ρ<sup>1</sup>

<span id="page-14-2"></span>
$$
\liminf_{\tau \to 0} \left( J_{\tau}(\rho_1^{\tau} | \rho_0) - \frac{W_2^2(\rho_0, \rho_1^{\tau})}{4\tau} \right) \ge \frac{1}{2} \mathcal{F}(\rho_1) - \frac{1}{2} \mathcal{F}(\rho_0).
$$
 (33)

Proof. Take any sequence ρ τ <sup>1</sup> ∈ P2(**<sup>R</sup>** d ) narrowly converging to a <sup>ρ</sup><sup>1</sup> ∈ P2(**<sup>R</sup>** d ). We only need to consider those ρ τ 1 for which J<sup>τ</sup> (ρ τ 1 |ρ0) < ∞. For each such ρ τ 1 , by the definition of infimum there exists a curve ρ τ <sup>t</sup> <sup>∈</sup> <sup>C</sup>(ρ0, ρ<sup>τ</sup> 1 ) satisfying

$$
\frac{1}{4\tau} \int_0^1 \left\| \frac{\partial \rho_t^{\tau}}{\partial t} - \tau (\Delta \rho_t^{\tau} + \operatorname{div}(\rho_t^{\tau} \nabla \Psi)) \right\|_{-1, \rho_t^{\tau}}^2 dt \le J_{\tau}(\rho_1^{\tau} | \rho_0) + \tau < \infty.
$$
 (34)

By Lemma [4.6](#page-9-3) for the subquadratic case and [\[FN11,](#page-24-8) Lem. 2.6] for the superquadratic case, we have

$$
J_{\tau}(\rho_{1}^{\tau}|\rho_{0}) + \tau \geq \frac{1}{4\tau} \int_{0}^{1} \left\| \frac{\partial \rho_{t}^{\tau}}{\partial t} - \tau(\Delta \rho_{t}^{\tau} + \text{div}(\rho_{t}^{\tau} \nabla \Psi)) \right\|_{-1,\rho_{t}^{\tau}}^{2} dt
$$
  
\n
$$
= \frac{1}{4\tau} \int_{0}^{1} \left\| \frac{\partial \rho_{t}^{\tau}}{\partial t} + \tau \operatorname{grad} \mathcal{F}(\rho_{t}^{\tau})) \right\|_{-1,\rho_{t}^{\tau}}^{2} dt
$$
  
\n
$$
= \frac{1}{4\tau} \left( \int_{0}^{1} \left\| \frac{\partial \rho_{t}^{\tau}}{\partial t} \right\|_{-1,\rho_{t}^{\tau}}^{2} dt + 2\tau(\mathcal{F}(\rho_{1}^{\tau}) - \mathcal{F}(\rho_{0})) + \tau^{2} \int_{0}^{1} \left\| \operatorname{grad} \mathcal{F}(\rho_{t}^{\tau}) \right\|_{-1,\rho_{t}^{\tau}}^{2} dt \right)
$$
  
\n
$$
= \frac{1}{2} (\mathcal{F}(\rho_{1}^{\tau}) - \mathcal{F}(\rho_{0})) + \frac{1}{4\tau} \int_{0}^{1} \left\| \frac{\partial \rho_{t}^{\tau}}{\partial t} \right\|_{-1,\rho_{t}^{\tau}}^{2} dt + \frac{\tau}{4} \int_{0}^{1} \left\| \operatorname{grad} \mathcal{F}(\rho_{t}^{\tau}) \right\|_{-1,\rho_{t}^{\tau}}^{2} dt
$$
  
\n
$$
\geq \frac{1}{2} (\mathcal{F}(\rho_{1}^{\tau}) - \mathcal{F}(\rho_{0})) + \frac{1}{4\tau} \int_{0}^{1} \left\| \frac{\partial \rho_{t}^{\tau}}{\partial t} \right\|_{-1,\rho_{t}^{\tau}}^{2} dt
$$
  
\n
$$
\geq \frac{1}{2} (\mathcal{F}(\rho_{1}^{\tau}) - \mathcal{F}(\rho_{0})) + \frac{1}{4\tau} W_{2}^{2}(\rho_{0}, \rho_{1}^{\tau}).
$$

In the last inequality above we have used the Benamou-Brenier formula for the Wasserstein distance [\[BB00\]](#page-23-7). Finally, using ρ τ <sup>1</sup> → ρ<sup>1</sup> narrowly with the narrow lower semi-continuity of F, we find that

$$
\liminf_{\tau \to 0} \left( J_{\tau}(\rho_1^{\tau}|\rho_0) - \frac{W_2^2(\rho_0, \rho_1^{\tau})}{4\tau} \right) \ge \frac{1}{2} \mathcal{F}(\rho_1) - \frac{1}{2} \mathcal{F}(\rho_0).
$$

### 6 Recovery sequence

<span id="page-15-1"></span>In this section we prove the upper bound of the Gamma convergence [\(7\)](#page-2-0). This will conclude the proof of Theorem [1.1.](#page-2-3)

<span id="page-15-0"></span>Theorem 6.1 (Recovery sequence). Under the assumptions of Theorem [1.1,](#page-2-3) for any <sup>ρ</sup><sup>1</sup> ∈ P2(**R**) there exists a sequence ρ τ <sup>1</sup> ∈ P2(**R**) converging to <sup>ρ</sup><sup>1</sup> in the Wasserstein metric such that

$$
\limsup_{h \to 0} \left( J_h(\rho_1^{\tau} | \rho_0) - \frac{W_2^2(\rho_0, \rho_1^{\tau})}{4h} \right) \le \frac{1}{2} S(\rho_1) - \frac{1}{2} S(\rho_0). \tag{35}
$$

As mentioned in Section [1,](#page-0-1) our approach for the recovery sequence only works for d = 1. Hence throughout this section, we will consider d = 1.

The existence of the recovery sequence is proven by making use of the following denseness argument, which is also interesting in its own[4](#page-15-2) :

<span id="page-15-3"></span>Proposition 6.2. Let (X, d) be a metric space and let <sup>Q</sup> be a dense subset of <sup>X</sup>. If {Kn, n <sup>∈</sup> **<sup>N</sup>**} and K<sup>∞</sup> are functions from X to **R** such that:

<span id="page-15-2"></span><sup>4</sup>A more or less similar idea can be found in [\[Bra02,](#page-23-5) Remark 1.29]; Proposition [6.2](#page-15-3) is slightly stronger.

(a) Kn(q) → K∞(q) for all q ∈ Q,

2

2

(b) for every x ∈ X there exists a sequence q<sup>n</sup> ∈ Q with q<sup>n</sup> → x and K∞(qn) → K∞(x),

then for every x ∈ X there exists a sequence r<sup>n</sup> ∈ Q, with r<sup>n</sup> → x such that Kn(rn) → K∞(x).

Proof. The proof is by a diagonal argument. Take any x ∈ X and take the corresponding sequence q<sup>n</sup> → x such that K∞(qn) → K∞(x). By assumption, for any q ∈ Q and L > 0 there exists a nL,q such that for any n ≥ nL,q there holds d(Kn(q), K∞(q)) < 1/L. Define

$$
l_n := \begin{cases} 1, & 1 \le n < n_{2,q_2}, \\ 2, & n_{2,q_2} \le n < \max\{n_{2,q_2}, n_{3,q_3}\}, \\ \dots \end{cases}
$$

Take the subsequence r<sup>n</sup> := q<sup>l</sup><sup>n</sup> . Observe that l<sup>n</sup> → ∞ as n → ∞ such that indeed q<sup>l</sup><sup>n</sup> → x, and:

$$
d(K_n(q_{l_n}), K_\infty(x)) \leq \underbrace{d(K_n(q_{l_n}), K_\infty(q_{l_n}))}_{\leq \frac{1}{l_n}} + d(K_\infty(q_{l_n}), K_\infty(x)) \to 0.
$$

For a fixed ρ<sup>0</sup> satisfying the assumptions of Theorem [1.1,](#page-2-3) we want to apply Proposition [6.2](#page-15-3) to the situation where

$$
X = \mathcal{P}_2(\mathbf{R}),
$$
  
\n
$$
Q = Q(\rho_0) = \left\{ \rho = \rho(x)dx \in \mathcal{P}_2(\mathbf{R}) : \rho(x) \text{ is bounded from below by a positive constant in every compact set } \mathcal{F}(\rho), \|\Delta \rho\|_{-1,\rho}^2, \int_{\mathbf{R}} |\nabla \Psi(x)|^2 \rho(x) dx < \infty, \text{ and there exists a } M > 0 \text{ such that } \rho_0(x) = \rho(x) \text{ for all } |x| > M \right\},
$$
  
\n
$$
K_n(\rho) = J_{h_n}(\rho|\rho_0) - \frac{W_2^2(\rho_0, \rho)}{4h_n}, \text{ where } h_n \text{ an arbitrary sequence converging to zero,}
$$
  
\n
$$
K_{\infty}(\rho) = \frac{1}{2}\mathcal{F}(\rho) - \frac{1}{2}\mathcal{F}(\rho_0).
$$

Assumption (a) of Proposition [6.2,](#page-15-3) i.e. pointwise convergence for every ρ<sup>1</sup> ∈ Q(ρ0), can be proven as follows. Take ρ<sup>1</sup> ∈ Q(ρ0) and let ρ<sup>t</sup> be the geodesic that connects ρ<sup>0</sup> and ρ1. In the following Lemma [6.3,](#page-17-0) we will prove that k∆ρtk 2 −1,ρt and R **R** |∇Ψ(x)| <sup>2</sup>ρt(x)dx are uniformly bounded, so that we have

$$
\int_0^1 \left\| \frac{\partial \rho_t}{\partial t} - \tau (\Delta \rho_t + \text{div}(\rho_t \nabla \Psi)) \right\|_{-1,\rho_t}^2 dt
$$
  
$$
\leq 3 \int_0^1 \left\| \frac{\partial \rho_t}{\partial t} \right\|_{-1,\rho_t}^2 dt + 3\tau^2 \int_0^1 \|\Delta \rho_t\|_{-1,\rho_t}^2 dt + 3\tau^2 \int_0^1 \|\text{div}(\rho_t \nabla \Psi)\|_{-1,\rho_t}^2 dt < \infty.
$$

By applying Lemma [4.6](#page-9-3) for the subquadratic case or [\[FN11,](#page-24-8) Lem. 2.6] for the superquadratic case:

$$
\lim_{\tau \to 0} \left( J_{\tau}(\rho_1 | \rho_0) - \frac{W_2^2(\rho_0, \rho_1)}{4\tau} \right) \le \lim_{\frac{\tau}{2} \to 0} \left[ \tau \int_0^1 \left( \int_{\mathbb{R}} \left( \frac{(\rho_t'(x))^2}{\rho_t(x)} + |\nabla \Psi(x)|^2 \rho_t(x) \right) dx \right) dt \right. \\
\left. + \frac{1}{2} \mathcal{F}(\rho_1) - \frac{1}{2} \mathcal{F}(\rho_0) \right] = \frac{1}{2} \mathcal{F}(\rho_1) - \frac{1}{2} \mathcal{F}(\rho_0).
$$

The pointwise convergence then follows from this together with the lower bound [\(33\)](#page-14-2).

To prove the uniform bounds:

<span id="page-17-0"></span>Lemma 6.3. Let Ψ ∈ C 2 (**R**) be convex. Let <sup>ρ</sup><sup>0</sup> <sup>=</sup> <sup>ρ</sup>(x)dx ∈ P2(**R**) be asolutely continuous with respect to the Lesbegue measure, where ρ(x) is bounded from below by a positive constant in every compact set. Let ρ<sup>1</sup> ∈ Q(ρ0) and ρ<sup>t</sup> be the geodesic that connects ρ<sup>0</sup> and ρ1. Assume that F(ρ0) , k∆ρ0k 2 −1,ρ<sup>0</sup> and R **R** |∇Ψ(x)| <sup>2</sup>ρ0(x)dx are all finite. Then F(ρt), k∆ρtk 2 −1,ρt and R **R** |∇Ψ(x)| <sup>2</sup>ρt(x) dx are uniformly bounded with respect to t.

Proof. Let T(x) be the optimal map that transports ρ0(dx) to ρ1(dx). The geodesic that connects ρ<sup>0</sup> and ρ<sup>1</sup> is defined by

$$
\rho_t(x) = ((1-t)x + tT(x))_{\sharp}\rho_0(x).
$$

First we prove that k∆ρtk 2 −1,ρt is uniformly bounded with respect to t. In the real line, the map T(x) can be determined via the cumulative distribution functions as follows [\[Vil03,](#page-24-4) Section 2.2]). Let F(x) and G(x) be respectively the cumulative distribution functions of ρ(dx) and ρ1(dx), i.e.

$$
F(x) = \int_{-\infty}^{x} \rho_0(x) \, dx; \quad G(x) = \int_{-\infty}^{x} \rho_1(x) \, dx.
$$

Then T = G<sup>−</sup><sup>1</sup> ◦ F. We have

<span id="page-17-1"></span>
$$
F(M) + \int_{M}^{+\infty} \rho_0(x) dx = G(M) + \int_{M}^{+\infty} \rho_1(x) dx = 1.
$$
 (36)

From [\(36\)](#page-17-1) and by the assumption that ρ0(x) = ρ1(x) for all |x| > M we find that F(M) = G(M). Hence for all x such that |x| > M we have

$$
F(x) = F(M) + \int_M^x \rho_0(x) dx = G(M) + \int_M^x \rho_1(x) dx = G(x).
$$

Consequentially, for all x with |x| > M we have T(x) = (G<sup>−</sup><sup>1</sup> ◦F)(x) = x. Therefore T ′ (x) = 1 for all |x| > M. This, together with the fact that T is a C 1 function, implies that T ′ (x) is bounded. Moreover T(x) satisfies the Monge - Amp`ere equation.

$$
\rho_0(x) = \rho_1(T(x))T'(x).
$$

or equivalently (since ρ1(x) > 0),

$$
T'(x) = \frac{\rho_0(x)}{\rho_1(T(x))}.
$$
\n(37)

Since the densities ρ0, ρ<sup>1</sup> are absolutely continuous (recall that √ρ 0 , √ρ 1 ∈ H<sup>1</sup> (**R**)) and T ′ (x) in C <sup>1</sup> and strictly positive, we get

$$
\frac{T''(x)}{T'(x)} = (\log(T'(x)))'
$$
  
=  $(\log(\rho_0(x)) - \log(\rho_1(T(x)))'$   
=  $\frac{\rho'_0(x)}{\rho_0(x)} - \frac{\rho'_1(T(x))T'(x)}{\rho_1(T(x))}$ .

Set Tt(x) = tx + (1 − t)T(x). For 0 ≤ t ≤ 1 we have

<span id="page-18-1"></span><span id="page-18-0"></span>
$$
\rho_t(x) = \rho_1(T_t(x))T'_t(x),\tag{38}
$$

Since ρ1(Tt(x)) and T ′ t (x) are both absolutely continuous so is ρt(x). Hence the derivative appeared in [\(13\)](#page-5-4) for k∆ρtk 2 −1,ρt is the classical derivative. Substituting [\(38\)](#page-18-0) into [\(13\)](#page-5-4) we get

$$
\int_{\mathbb{R}} \frac{(\rho_t'(x))^2}{\rho_t(x)} dx = \int_{\mathbb{R}} \frac{[(\rho_1(T_t(x))T_t'(x))^2]}{\rho_1(T_t(x))T_t'(x)} dx \n= \int_{\mathbb{R}} \frac{[\rho_1'(T_t(x))T_t'(x)^2 + \rho_1(T_t(x))T_t''(x)]^2}{\rho_1(T_t(x))T_t'(x)} dx \n\leq 2 \int_{\mathbb{R}} \frac{(\rho_1'(T_t(x)))^2(T_t'(x))^4}{\rho_1(T_t(x))T_t'(x)} dx + 2 \int_{\mathbb{R}} \frac{(\rho_1(T_t(x))T_t''(x))^2}{\rho_1(T_t(x))T_t'(x)} dx \n= 2 \int_{\mathbb{R}} \frac{(\rho_1'(T_t(x)))^2}{\rho_1(T_t(x))^2} (T_t'(x))^3 dx + 2 \int_{\mathbb{R}} \rho_1(T_t(x)) \frac{(T_t''(x))^2}{T_t'(x)} dx
$$
\n(39)

Note that in the inequality above we have used the Cauchy - Schwarz inequality (a+b) <sup>2</sup> ≤ 2(a <sup>2</sup>+b 2 ). To proceed we will estimate each term in the right hand side of [\(39\)](#page-18-1) using the fact that |T ′ (x)| is bounded and k∆ρ0k 2 −1,ρ<sup>0</sup> , k∆ρ1k 2 <sup>−</sup>1,ρ<sup>1</sup> < ∞. For the first part we have

<span id="page-18-2"></span>
$$
\int_{\mathbb{R}} \frac{(\rho'_1(T_t(x)))^2}{\rho_1(T_t(x))} (T'_t(x))^3 dx = \int_{\mathbb{R}} \frac{(\rho'_1(T_t(x)))^2}{\rho_1(T_t(x))} (T'_t(x))(T'_t(x))^2 dx
$$
  
\n
$$
\leq C^2 \int_{\mathbb{R}} \frac{(\rho'_1(T_t(x)))^2}{\rho_1(T_t(x))} (T'_t(x)) dx
$$
  
\n
$$
= C^2 \int_{\mathbb{R}} \frac{(\rho'_1(x))^2}{\rho_1(x)} dx
$$
  
\n
$$
= C^2 \|\Delta \rho_1\|_{-1,\rho_1}^2.
$$
 (40)

Let B be the ball of radius M centered at the origin. Since T ′′(x) = 0 for all |x| > M we can restrict our calculation for the second part in the ball B.

$$
\int_{\mathbb{R}} \rho_1(T_t(x)) \frac{(T_t''(x))^2}{T_t'(x)} dx = \int_{B} \rho_1(T_t(x)) \frac{(T_t''(x))^2}{T_t'(x)} dx \n= \int_{B} \rho_1(T_t(x)) T_t'(x) \left(\frac{T'(x)(1-t)}{T_t'(x)}\right)^2 \left(\frac{T''(x)}{T'(x)}\right)^2 dx \n= \int_{B} \rho_1(T_t(x)) T_t'(x) \left(\frac{T'(x)(1-t)}{T_t'(x)}\right)^2 \left(\frac{T''(x)}{T'(x)}\right)^2 dx \n= \int_{B} \rho_1(T_t(x)) T_t'(x) \left(\frac{T'(x)(1-t)}{t+(1-t)T'(x)}\right)^2 \left(\frac{\rho_0'(x)}{\rho_0(x)} - \frac{\rho_1'(T(x))T'(x)}{\rho_1(T(x))}\right)^2 dx \n\leq 2 \int_{B} \rho_1(T_t(x)) T_t'(x) \left(\frac{\rho_0'(x)}{\rho_0(x)}\right)^2 dx \n+ 2 \int_{B} \rho_1(T_t(x)) T_t'(x) \left(\frac{\rho_1'(T(x))T'(x)}{\rho_1(T(x))}\right)^2 dx \n= 2 \int_{B} \frac{\rho_1(T_t(x))T_t'(x)}{\rho_0(x)} \left(\frac{(\rho_0'(x))^2}{\rho_0(x)}\right) dx \n+ 2 \int_{B} \frac{\rho_1(T_t(x))T_t'(x)T'(x)}{\rho_1(T(x))} \left(\frac{(\rho_1'(T(x)))^2}{\rho_1(T(x))}\right)^2 T'(x) dx \n\leq C \left(\int_{B} \frac{(\rho_0(x))^2}{\rho_0(x)} dx + \int_{B} \frac{(\rho_1'(T(x)))^2}{\rho_1(T(x))}\right)^2 T'(x) dx \n\leq C (\|\Delta \rho_0\|_{-1,\rho_0}^2 + \|\Delta \rho_1\|_{-1,\rho_1}^2). \tag{41}
$$

From [\(39\)](#page-18-1), [\(40\)](#page-18-2) and [\(41\)](#page-19-0) we find that

$$
\|\Delta \rho_t\|_{-1,\rho_t}^2 = \int_{\mathbb{R}} \frac{(\rho_t'(x))^2}{\rho_t(x)} dx \le C (\|\Delta \rho_0\|_{-1,\rho_0}^2 + \|\Delta \rho_1\|_{-1,\rho_1}^2).
$$

It remains to prove the boundedness of the functional R **R** |∇Ψ(x)| <sup>2</sup>ρt(x)dx.

Since 
$$
T(x) = x
$$
 for  $|x| > M$  we have  $\rho_t(x) = \rho_1(x)$  for  $|x| > M$ . Hence  
\n
$$
\int_{\mathbb{R}} |\nabla \Psi(x)|^2 \rho_t(x) dx = \int_{B} |\nabla \Psi(x)|^2 \rho_t(x) dx + \int_{|x| > M} |\nabla \Psi(x)|^2 \rho_t(x) dx
$$
\n
$$
= \int_{B} |\nabla \Psi(x)|^2 \rho_t(x) dx + \int_{|x| > M} |\nabla \Psi(x)|^2 \rho_1(x) dx
$$
\n
$$
\leq C \int_{B} \rho_t(x) dx + \int_{|x| > M} |\nabla \Psi(x)|^2 \rho_1(x) dx
$$
\n
$$
\leq C + \int |\nabla \Psi(x)|^2 \rho_1(x) dx < \infty.
$$

Finally the result for F(ρt) comes from the fact that F is geodesically convex.

Finally, to prove assumption (b) of Proposition [6.2,](#page-15-3) i.e. the existence of the recovery sequence in the dense set.

<span id="page-19-0"></span>

Lemma 6.4. Let <sup>ρ</sup>0, ρ<sup>1</sup> ∈ P2(**R**) and <sup>Ψ</sup> <sup>∈</sup> <sup>C</sup> 2 (**R**) with Ψ(x) <sup>&</sup>gt; <sup>−</sup><sup>A</sup> <sup>−</sup> <sup>B</sup>|x<sup>|</sup> 2 for some positive constants (this includes both our cases). Assume that ρ<sup>0</sup> is bounded from below by a positive constant in every compact set and that F(ρ0), k∆ρ0k 2 −1,ρ<sup>0</sup> and R **<sup>R</sup>**<sup>n</sup> |∇Ψ(x)| <sup>2</sup>ρ1(x) dx are all finite. Then, there exists a sequence k<sup>n</sup> ∈ Q(ρ0) such that k<sup>n</sup> → ρ<sup>1</sup> with respect to Wasserstein distance, and F(kn) → F(ρ1).

Proof. We will assume that <sup>F</sup>(ρ1) <sup>&</sup>lt; <sup>∞</sup>, otherwise the construction is trivial. Let <sup>n</sup> <sup>∈</sup> **<sup>N</sup>**. Since R **R** ρ0(x)x <sup>2</sup> dx < <sup>∞</sup> and <sup>R</sup> **R** ρ0(x)|Ψ(x)| dx < ∞ there is a set A<sup>1</sup> of finite Lebesgue measure such that for every x ∈ A<sup>1</sup> we have that ρ0(x) < min{ 1 n|Ψ(x)| , 1 nx<sup>2</sup> }. Similarly there is a set A<sup>2</sup> of finite Lebesgue measure such that for every x ∈ A<sup>2</sup> we have that ρ1(x) < min{ 1 n|Ψ(x)| , 1 nx<sup>2</sup> }. We can even ask for A<sup>2</sup> to contain only Lebesgue points of ρ<sup>1</sup> to compensate for the lack of continuity.

Let M<sup>n</sup> > 1 with M<sup>n</sup> ∈ A<sup>1</sup> ∩ A<sup>2</sup> such that

$$
\int_{B^c(0,M_n)} \left[ \rho_i(x) + |\rho_i(x) \log \rho_i(x)| + \rho_i(x)x^2 + \rho_i(x)|\Psi(x)| \right] dx < \frac{1}{n}, \quad i = 1, 2.
$$

Let θ<sup>ǫ</sup> be as in Lemma [4.8.](#page-12-0) By the theory of mollifications there is a θ<sup>ǫ</sup>(n) that satisfies the following

• R B(0,Mn) (ρ Mn <sup>1</sup> ∗ θ<sup>ǫ</sup>(n))(x) − ρ1(x)  dx < <sup>1</sup> n , • R B(0,Mn) ((ρ Mn <sup>1</sup> ∗ θ<sup>ǫ</sup>(n))(x) − ρ1(x))Ψ(x)  dx < <sup>1</sup> n , • R B(0,Mn) (ρ Mn <sup>1</sup> ∗ θ<sup>ǫ</sup>(n))(x) log(ρ Mn <sup>1</sup> ∗ θ<sup>ǫ</sup>(n))(x) − ρ1(x) log ρ1(x) dx < 1 n , • (ρ Mn <sup>1</sup> ∗ θ<sup>ǫ</sup>(n))(Mn) < min{ 1 nΨ(Mn) , 1 n }, • (ρ Mn <sup>1</sup> ∗ θ<sup>ǫ</sup>(n))(x) > 0, ∀x ∈ B(0, Mn),

where

$$
\rho_1^{M_n} = \begin{cases} \rho_1(x) & \text{if } |x| \le M_n \\ 0 & \text{if } |x| > M_n. \end{cases}
$$

Since Ψ(x) is continuous, there is a 0 < a < 1 such that for x ∈ [−M<sup>n</sup> − a, −M<sup>n</sup> + a] ∪ [M<sup>n</sup> − a, M<sup>n</sup> + a] we have ρ0(Mn) < min{ 1 n|Ψ(x)| , 1 nx<sup>2</sup> } and (ρ Mn <sup>1</sup> ∗ θ<sup>ǫ</sup>(n))(Mn) < min{ 1 n|Ψ(x)| , 1 nx<sup>2</sup> }. Now define

$$
g_{1,n}(x) = \begin{cases} (\rho_1^{M_n} * \theta_{\epsilon(n)})(x) & \text{if } |x| \le M_n, \\ (\rho_1^{M_n} * \theta_{\epsilon(n)})(M_n)(\frac{x - M_n + a}{a})^2 & \text{if } M_n < x < M_n + a, \\ (\rho_1^{M_n} * \theta_{\epsilon(n)})(M_n)(\frac{x + M_n + a}{a})^2 & \text{if } -M_n - a < x < -M_n, \\ 0 & \text{if } |x| \ge M_n + a, \end{cases}
$$

and

$$
g_{2,n}(x) = \begin{cases} 0 & \text{if } |x| \le M_n - a, \\ \rho_0(M_n) \left(\frac{M_n - x}{a}\right)^2 & \text{if } M_n - a < x < M_n, \\ \rho_0(M_n) \left(\frac{M_n + a - x}{a}\right)^2 & \text{if } -M_n < x < -M_n + a, \\ \rho_0(x) & \text{if } |x| \ge M_n. \end{cases}
$$

It is easy to check that k∆gi,nk 2 −1,gi,n [5](#page-21-0) and R gi,n|∇Ψ| <sup>2</sup> are finite for each i = 1, 2 and n ∈ N. Also,

$$
S(g_{1,n}) = \int_{B(0,M_n)} (g_{1,n}(x) \log g_{1,n}(x) - \rho_1(x) \log (\rho_1(x)) dx + \int_{B(0,M_n)} \rho_1(x) \log (\rho_1(x)) dx
$$
  
+ 
$$
\int_{M_n < |x| < M_n + a} g_{1,n}(x) \log (g_{1,n}(x)) dx \to S(\rho_1) \quad \text{as } n \to \infty.
$$

Furthermore, by construction we have kg1,nk<sup>1</sup> → 1, kg2,nk<sup>1</sup> → 0 and we can finally define kn(x) by

$$
k_n(x) := g_{1,n}(x) \frac{1 - \|g_{2,n}\|_1}{\|g_{1,n}\|_1} + g_{2,n}(x),\tag{42}
$$

where k · k<sup>1</sup> is the L 1 (**R**) norm. We have that k<sup>n</sup> is absolutely continuous and

$$
\begin{split}\n\|\Delta k_{n}\|_{-1,k_{n}}^{2} &= \int_{\mathbb{R}} \frac{\left(k_{n}'(x)\right)^{2}}{k_{n}(x)} \, dx \leq \int_{\mathbb{R}} \frac{\left(\left(g_{1,n}(x)\frac{1-\|g_{2,n}\|_{1}}{\|g_{1,n}\|_{1}} + \int_{\mathbb{R}} g_{2,n}(x)\right)'\right)^{2}}{g_{1,n}(x)\frac{1-\|g_{2,n}\|_{1}}{\|g_{1,n}\|_{1}} + g_{2,n}(x)} \, dx \\
&\leq \int_{\mathbb{R}} \frac{2\left(g_{1,n}'(x)\frac{1-\|g_{2,n}\|_{1}}{\|g_{1,n}\|_{1}}\right)^{2}}{g_{1,n}(x)\frac{1-\|g_{2,n}\|_{1}}{\|g_{1,n}\|_{1}} + g_{2,n}(x)} \, dx + \int_{\mathbb{R}} \frac{2\left(g_{2,n}'(x)\right)^{2}}{g_{1,n}(x)\frac{1-\|g_{2,n}\|_{1}}{\|g_{1,n}\|_{1}} + g_{2,n}(x)} \, dx \\
&\leq \int_{\mathbb{R}} \frac{1-\|g_{2,n}\|_{1}}{\|g_{1,n}\|_{1}} \frac{2(g_{1,n}'(x))^{2}}{g_{1,n}(x)} \, dx + \int_{\mathbb{R}} \frac{2(g_{2,n}'(x))^{2}}{g_{2,n}(x)} \, dx \\
&\leq \frac{2(1-\|g_{2,n}\|_{1})}{\|g_{1,n}\|_{1}} \|\Delta g_{1,n}\|_{-1,g_{1,n}}^{2} + 2\|\Delta g_{2,n}\|_{-1,g_{2,n}}^{2}.\n\end{split}
$$

<span id="page-21-0"></span><sup>5</sup>This is a slight abuse of notation since gi,n are actually sub-probability measures.

Hence k∆knk 2 <sup>−</sup>1,k<sup>n</sup> < ∞. For the entropy functional we have:

$$
|\mathcal{S}(k_n) - \mathcal{S}(g_{1,n})| = \left| \int_{\mathbb{R}} k_n(x) \log(k_n(x)) dx - \int_{\mathbb{R}} g_{1,n}(x) \log(g_{1,n}(x)) dx \right|
$$
  
\n
$$
\leq \underbrace{\int_{B(0,M_n-a)} \left| k_n(x) \log(k_n(x)) - g_{1,n}(x) \log(g_{1,n}(x)) \right| dx}_{(I)}
$$
  
\n
$$
+ \underbrace{\int_{M_n-a \leq |x| \leq M_n+a} \left| k_n(x) \log(k_n(x)) - g_{1,n}(x) \log(g_{1,n}(x)) \right| dx}_{(II)}
$$
  
\n
$$
+ \underbrace{\int_{B^c(0,M_n+a)} \left| k_n(x) \log(k_n(x)) - g_{1,n}(x) \log(g_{1,n}(x)) \right| dx}_{(III)}
$$

We now show that each of the three parts convergence to 0 as n → ∞. For the first part:

$$
(I) = \int_{B(0,M_n-a)} \left| g_{1,n}(x) \frac{1 - \|g_{2,n}\|_1}{\|g_{1,n}\|_1} \log \left( g_{1,n}(x) \frac{1 - \|g_{2,n}\|_1}{\|g_{1,n}\|_1} \right) - g_{1,n}(x) \log(g_{1,n}(x)) \right| dx
$$
  
= 
$$
\left| 1 - \frac{1 - \|g_{2,n}\|_1}{\|g_{1,n}\|_1} \right| \int_{B(0,M_n-a)} \left| g_{1,n}(x) \log(g_{1,n}(x)) \right| dx
$$
  
+ 
$$
\frac{1 - \|g_{2,n}\|_1}{\|g_{1,n}\|_1} \log \frac{1 - \|g_{2,n}\|_1}{\|g_{1,n}\|_1} \int_{B(0,M_n-a)} |g_{1,n}(x)| dx \to 0.
$$

For the second part:

$$
(II) \leq \int_{M_n - a \leq |x| \leq M_n + a} \left( |k_n(x) \log(k_n(x))| + |g_{1,n}(x) \log(g_{1,n}(x))| \right) dx
$$
  
= 
$$
\int_{M_n - a \leq |x| \leq M_n + a} \left| (g_{1,n}(x) \frac{1 - \|g_{2,n}\|_1}{\|g_{1,n}\|_1} + g_{2,n}(x)) \log(g_{1,n}(x) \frac{1 - \|g_{2,n}\|_1}{\|g_{1,n}\|_1} + g_{2,n}(x)) \right| dx
$$
  
+ 
$$
\int_{M_n - a \leq |x| \leq M_n + a} |g_{1,n}(x) \log(g_{1,n}(x))| dx.
$$

Since g1,n(x), g2,n(x) are smaller than <sup>1</sup> n in M<sup>n</sup> − a ≤ |x| ≤ M<sup>n</sup> + a, the right hand side converges to zero.

Part (III) is smaller than <sup>1</sup> n by the first property of M<sup>n</sup> and therefore it converges to zero. Finally

$$
\int_{\mathbb{R}} |k_n(x) - \rho_1(x)| |\Psi(x)| dx = \int_{\mathbb{R}} |g_{1,n}(x)| \frac{1 - \|g_{2,n}\|_1}{\|g_{1,n}\|_1} + g_{2,n}(x) - \rho_1(x)| |\Psi(x)| dx
$$
  
\n
$$
\leq \left(\frac{1 - \|g_{2,n}\|_1}{\|g_{1,n}\|_1}\right) \int_{\mathbb{R}} |g_{1,n}(x) - \rho_1(x)| |\Psi(x)| dx
$$
  
\n
$$
+ \left|1 - \frac{1 - \|g_{2,n}\|_1}{\|g_{1,n}\|_1}\right| \int_{\mathbb{R}} |\Psi(x)| \rho_1(x) dx + \int_{\mathbb{R}} |\Psi(x)| g_{2,n}(x) dx \to 0
$$

Hence the second property of Proposition [6.2](#page-15-3) is satisfied.

# Acknowledgements

We would like to thank Nicolas Dirr, Mark Peletier and Johannes Zimmer for their initial suggestion and support during the project. The current proof of Lemma [4.7](#page-9-0) without probabilistic tools was done after a discussion with Mark Peletier. We also thank Jin Feng, Truyen Nguyen and Patrick van Meurs for their helpful discussion and comments. Manh Hong Duong has received funding from the ITN "FIRST" of the Seventh Framework Programme of the European Community's (grant agreement number 238702).

### References

- <span id="page-23-1"></span>[ADPZ10] S. Adams, N. Dirr, M. A. Peletier, and J. Zimmer. From a large-deviations principle to the Wasserstein gradient flow: a new micro-macro passage. Communications in Mathematical Physics, 307(3):791–815, 2011.
- <span id="page-23-3"></span>[ADPZ12] S. Adams, N. Dirr, M. A. Peletier, and J. Zimmer. Large deviations and gradient flows. Arxiv preprint <http://arxiv.org/abs/1201.4601>, 2012.
- <span id="page-23-0"></span>[AGS08] L. Ambrosio, N. Gigli, and G. Savar´e. Gradient flows in metric spaces and in the space of probability measures. Lectures in Mathematics. ETH Z¨urich. Birkhauser, Basel, 2nd edition, 2008.
- <span id="page-23-7"></span>[BB00] J.D. Benamou and Y. Brenier. A computational fluid mechanics solution to the Monge-Kantorovich mass transfer problem. Numer. Math., 84(3):375–393, 2000.
- <span id="page-23-5"></span>[Bra02] A. Braides. Gamma convergence for beginners. Oxford University Press, Oxford, 2002.
- <span id="page-23-6"></span>[DG87] D.A. Dawson and J. G¨artner. Large deviations from the McKean-Vlasov limit for weakly interacting diffusions. Stochastics, 20(4):247–308, 1987.
- <span id="page-23-2"></span>[DLZ10] Nicolas Dirr, Vaios Laschos, and Johannes Zimmer. Upscaling from particle models to entropic gradient flows (submitted). 2010.
- <span id="page-23-4"></span>[Dud89] R.M. Dudley. Real analysis and probability. Wadsworth & Brooks/Cole, Pacific Grove, CA, USA, 1989.

- <span id="page-24-7"></span>[DZ87] A. Dembo and O. Zeitouni. Large deviations techniques and applications, volume 38 of Stochastic modelling and applied probability. Springer, New York, NY, USA, 2nd edition, 1987.
- <span id="page-24-6"></span>[FK06] J. Feng and T.G. Kurtz. Large deviations for stochastic processes, volume 131 of Mathematical surveys and monographs. American Mathematical Society, Providence, RI, USA, 2006.
- <span id="page-24-8"></span>[FN11] J. Feng and T. Nguyen. Hamilton-Jacobi equations in space of measures associated with a system of convervations laws. Journal de Math´ematiques Pures et Appliqu´ees, 97(4):318–390, 2011.
- <span id="page-24-0"></span>[JKO98] R. Jordan, D. Kinderlehrer, and F. Otto. The variational formulation of the Fokker-Planck equation. SIAM Journal on Mathematical Analysis, 29(1):1–17, 1998.
- <span id="page-24-2"></span>[L´eo07] C. L´eonard. A large deviation approach to optimal transport. <arxiv.org/abs/0710.1461v1>, 2007.
- <span id="page-24-1"></span>[Ott01] F. Otto. The geometry of dissipative evolution equations: the porous medium equation. Communications in partial differential equations, 26(1&2):101–174, 2001.
- <span id="page-24-3"></span>[PR11] M. Peletier and M. Renger. Variational formulation of the Fokker-Planck equation with decay: a particle approach (submitted). <http://arxiv.org/abs/1108.3181>, 2011.
- <span id="page-24-5"></span>[Rud73] W. Rudin. Functional Analysis. McGraw-Hill, New York, NY, USA, 1973.
- <span id="page-24-4"></span>[Vil03] C. Villani. Topics in optimal transportation, volume 58 of Graduate Studies in Mathematics. American Mathematical Society, Providence, 2003.