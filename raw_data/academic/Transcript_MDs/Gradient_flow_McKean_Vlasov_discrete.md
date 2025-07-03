# GRADIENT FLOW STRUCTURE FOR MCKEAN-VLASOV EQUATIONS ON DISCRETE SPACES

MATTHIAS ERBAR, MAX FATHI, VAIOS LASCHOS, AND ANDRE SCHLICHTING ´

Abstract. In this work, we show that a family of non-linear mean-field equations on discrete spaces can be viewed as a gradient flow of a natural free energy functional with respect to a certain metric structure we make explicit. We also prove that this gradient flow structure arises as the limit of the gradient flow structures of a natural sequence of N-particle dynamics, as N goes to infinity.

## 1. Introduction

In this work, we are interested in the gradient flow structure of McKean-Vlasov equations on finite discrete spaces. They take the form

<span id="page-0-0"></span>
$$
\dot{c}(t) = c(t)Q(c(t))\tag{1.1}
$$

where c(t) is a flow of probability measures on a fixed finite set X = {1, . . . , d}, and Qxy(µ) is collection of parametrized transition rates, that is for each µ ∈ P(X ), Q(µ) is a Markov transition kernel.

Such non-linear equations arise naturally as the scaling limit for the evolution of the empirical measure of a system of N particles undergoing a linear Markov dynamics with mean field interaction. Here the interaction is of mean field type if the transition rate Q<sup>N</sup> <sup>i</sup>;x,y for the i-th particle to jump from site x to y only depends on the empirical measure of the particles.

Mean-field systems are commonly used in physics and biology to model the evolution of a system where the influence of all particles on a tagged particle is the average of the force exerted by each particle on the tagged particle. In the recent work [\[7\]](#page-35-0), it was shown that whenever Q satisfies suitable conditions a free energy of the form

<span id="page-0-1"></span>
$$
\mathcal{F}(\mu) = \sum_{x \in \mathcal{X}} \mu_x \log \mu_x + \sum_{x \in \mathcal{X}} \mu_x K_x(\mu) \tag{1.2}
$$

for some appropriate potential K : P(X ) × X → R (see Definition [2.3\)](#page-5-0) is a Lyapunov function for the evolution equation [\(1.1\)](#page-0-0), i.e. it decreases along the flow.

In this work, we show that this monotonicity is actually a consequence of a more fundamental underlying structure. Namely, we exibit a novel geometric structure on the space of probability measure P(X ) that allows to view the evolution equation [\(1.1\)](#page-0-0) as the gradient flow of the free energy F.

Date: October 26, 2016.

<sup>2010</sup> Mathematics Subject Classification. Primary: 60J27; Secondary: 34A34, 49J40, 49J45.

Key words and phrases. Gradient flow structure, weakly interacting particles systems, nonlinear Markov chains, McKean-Vlasov dynamics, mean-field limit, evolutionary Gamma convergence, transportation metric.

This gradient flow structure is a natural non-linear extension of the discrete gradient flow structures that were discovered in [\[31\]](#page-36-0) and [\[34\]](#page-36-1) in the context of linear equations describing Markov chains or more generally in [\[21\]](#page-35-1) in the context of L´evy processes.

Moreover, we shall show that our new gradient flow structure for the non-linear equation arises as the limit of the gradient flow structures associated to a sequence of meanfield N particle Markov chains. As an application, we use the stability of gradient flows to show convergence of these mean-field dynamics to solutions of the non-linear equation [\(1.1\)](#page-0-0), see Theorem [3.10.](#page-27-0)

1.1. Gradient flows in spaces of probability measures. Classically, a gradient flow is an ordinary differential equation of the form

$$
\dot{x}(t) = -\nabla \mathcal{F}(x(t)).
$$

By now there exists an extensive theory, initiated by De Giorgi and his collaborators [\[15\]](#page-35-2), giving meaning to the notion of gradient flow when the curve x takes values in a metric space.

Examples of these generalized gradient flows are the famous results by Otto [\[28,](#page-36-2) [37\]](#page-36-3) stating that many diffusive partial differential equations can be interpreted as gradient flows of appropriate energy functionals on the space of probability measures on R<sup>d</sup> equipped with the L <sup>2</sup> Wasserstein distance. These include the Fokker–Planck and the pourous medium equations. An extensive treatment of these examples in the framework of De Giorgi was accomplished in [\[2\]](#page-35-3).

Gradient flow structures allow to better understand the role of certain Lyapunov functionals as thermodynamic free energies. Recently, also unexpected connections of gradient flows to large deviations have been unveiled [\[1\]](#page-35-4) [\[16\]](#page-35-5), [\[19\]](#page-35-6), [\[24\]](#page-36-4), [\[25\]](#page-36-5).

Since the heat equation is the PDE that governs the evolution of the Brownian motion, a natural question was whether a similar structure can be uncovered for reversible Markov chains on discrete spaces. This question was answered positively in works of Maas [\[31\]](#page-36-0) and Mielke [\[34\]](#page-36-1), which state that the evolution equations associated to reversible Markov chains on finite spaces can be reformulated as gradient flows of the entropy (with respect to the invariant measure of the chain) for a certain metric structure on the space of probability measures over the finite space. In [\[23\]](#page-36-6), a gradient flow structure for discrete porous medium equations was also uncovered, based on similar ideas.

In Section 2, we shall highlight a gradient flow structure for [\(1.1\)](#page-0-0), which is a natural non-linear generalization of the structure discovered in [\[31\]](#page-36-0) and [\[34\]](#page-36-1) for such non-linear Markov processes. This structure explains why the non-linear entropies of [\[7\]](#page-35-0) are Lyapunov functions for the non-linear ODE. Moreover, we shall show in Section 3 that this structure is compatible with those of [\[31\]](#page-36-0) and [\[34\]](#page-36-1), in the sense that it arises as a limit of gradient flow structures for N-particle systems as N goes to infinity.

1.2. Convergence of gradient flows. Gradient flows have proven to be particularly useful for the study of convergence of sequences of evolution equations to some limit since they provide a very rigid structure. Informally, the philosophy can be summarized as follows: consider a sequence of gradient flows, each associated to some energy functional F <sup>N</sup> and some metric structure. If the sequence <sup>F</sup> <sup>N</sup> converges in some sense to a limit <sup>F</sup><sup>∞</sup> and if the metric structures converge to some limiting metric, then one would expect the sequence of gradient flows to converge to a limit that can be described as a gradient flow of <sup>F</sup><sup>∞</sup> for the asymptotic metric structure.

There are several ways of rigorously implementing this philosophy to actually prove convergence in concrete situations. The one we shall be using in this work is due to Sandier and Serfaty in [\[38\]](#page-36-7), and was later generalized in [\[40\]](#page-36-8). Other methods, based on discretization schemes, have been developed in [\[3\]](#page-35-7) and [\[13\]](#page-35-8). See also the recent survey [\[35\]](#page-36-9) for an extension of the theory to generalized gradient systems. In the context of diffusion equations, arguments similar to those of [\[40\]](#page-36-8) have been used in [\[25\]](#page-36-5) to study large deviations.

In the discrete setting, we can combine the framework of [\[31\]](#page-36-0) and [\[34\]](#page-36-1) with the method of [\[40\]](#page-36-8) to study scaling limits of Markov chains on discrete spaces. In this work, we shall use this method to study scaling limits of N-particle mean-field dynamics on finite spaces. While the convergence statement could be obtained through more classical techniques, such as those of [\[36,](#page-36-10) [41\]](#page-36-11), our focus here is on justifying that the gradient flow structure we present is the natural one, since it arises as the limit of the gradient flow structures for the N-particle systems.

While we were writing this article, we have been told by Maas and Mielke that they have also successfully used this technique to study the evolution of concentrations in chemical reactions. We also mention the work [\[27\]](#page-36-12), which showed that the metric associated to the gradient flow structure for the simple random walk on the discrete torus Z/NZ converges to the Wasserstein structure on P(T), establishing compatibility of the discrete and continuous settings in a typical example. The technique can also be used to prove convergence of interacting particle systems on lattices, such as the simple exclusion process (see [\[26\]](#page-36-13)). The technique is not restricted to the evolution of probability measures by Wasserstein-type gradient flows, but can be also applied for instance to coagulation-fragmentation processes like the Becker-D¨oring equations, where one can prove macroscopic limits (see [\[39\]](#page-36-14)).

1.3. Continuous mean-field particle dynamics. Let us briefly compare the scaling limit for discrete mean-field dynamics considered in this paper with the more classical analogous scaling limit for particles in the continuum decribed by McKean-Vlasov equations.

N-particle mean-field dynamics describe the behavior of N particles given by some spatial positions x1(t), . . . , x<sup>N</sup> (t), where each particle is allowed to interact through the empirical measure of all other particles.

In nice situations, when the number of particles goes to infinity, the empirical measure of the system <sup>1</sup> N Pδxi(t) converges to some probability measure µ(t), whose evolution is described by a McKean-Vlasov equation. In the continuous setting, with positions in R<sup>d</sup> , this can be for example a PDE of the form

$$
\partial_t \mu(t) = \Delta \mu(t) + \text{div}(\mu(t)(\nabla W * \mu(t)))
$$

where ∇W ∗µ is the convolution of µ with an interaction that derives from a potential W. The according free energy in this case is given by

$$
\mathcal{F}(\mu) = \begin{cases} \int \frac{d\mu}{dx}(x) \log \frac{d\mu}{dx}(x) dx + \frac{1}{2} \int \int W(x - y) \mu(dx) \mu(dy), & \mu \ll \mathcal{L}, \\ \infty, & \text{otherwise,} \end{cases}
$$

i.e. formally Kx(µ) = <sup>1</sup> 2 (W ∗ µ)(x) in [\(1.2\)](#page-0-1). More general PDEs, involving diffusion coefficients and confinement potentials, are also possible. We refer to [\[17,](#page-35-9) [41\]](#page-36-11) for more information on convergence of N-particle dynamics to McKean-Vlasov equations. We also refer to [\[14,](#page-35-10) [12\]](#page-35-11) for the large deviations behavior. An important consequence of this convergence is that, for initial conditions for which the particles are exchangeable, there is propagation of chaos: the laws of two different tagged particles become independent as the number of particles goes to infinity [\[41,](#page-36-11) Proposition 2.2].

It has been first noted in [\[9\]](#page-35-12) that McKean-Vlasov equations on R<sup>d</sup> can be viewed as gradient flows of the free energy in the space of probability measures endowed with the Wasserstein metric. This fact has been useful in the study of the long-time behavior of these equations (cf. [\[9,](#page-35-12) [10,](#page-35-13) [11,](#page-35-14) [32\]](#page-36-15) among others). The study of long-time behavior of particle systems on finite spaces has attracted recent interest (see for example [\[30\]](#page-36-16) for the mean-field Ising model), and we can hope that curvature estimates for such systems may be useful to tackle this problem, as they have been in the continuous setting. Since lower bounds on curvature are stable, the study of curvature bounds for the mean field limit (which is defined as convexity of the free energy in the metric structure for which the dynamics is a gradient flow, see for example [\[22\]](#page-35-15)) can shed light on this problem. We leave this issue for future work. We must also mention that Wasserstein distances have also been used to quantify the convergence of mean-field systems to their scaling limit, see for example [\[5\]](#page-35-16).

1.4. Outline. In Section [2,](#page-3-0) we introduce the gradient flow structure of the mean-field system [\(1.1\)](#page-0-0) on discrete spaces. In Section [3,](#page-17-0) we will obtain this gradient flow structure as the limit of the linear gradient flow structure associated with an N-particle system with mean-field interaction. The nonlinear gradient flow structure comes with a metric, whose properties will be studied in Section [4.](#page-28-0) We close the paper with two Appendices [A](#page-33-0) and [B,](#page-34-0) in which auxiliary results for the passage to the limit are provided.

## <span id="page-3-0"></span>2. Gradient flow structure of mean-field systems on discrete spaces

In this section, we derive the gradient flow formulation for the mean-field system [\(1.1\)](#page-0-0). First, we introduce the metric concept of gradient flows in Section [2.1.](#page-3-1) Then in Section [2.2](#page-4-0) we turn to the discrete setting. We give the precise assumptions on the Markov transition kernel Q(µ) in the system [\(1.1\)](#page-0-0) and state several necessary definitions for later use. In Section [2.3,](#page-7-0) we define curves of probability measures via a continuity equation and associate to them an action measuring their velocity. Based on this, we can introduce in Section [2.4](#page-8-0) a transportation distance on the space of probability measure on X . The gradient flow formulation is proven in Section [2.5](#page-9-0) as curves of maximal slope. Finally, the gradient structure is lifted to the space of randomized probability measures in Section [2.6,](#page-12-0) which is a preparation for the passage to the limit.

<span id="page-3-1"></span>2.1. Gradient flows in a metric setting. Let briefly recall the basic notions concerning gradient flows in metric spaces. For an extensive treatment we refer to [\[2\]](#page-35-3).

Let (M, d) be a complete metric space. A curve (a, b) ∋ t 7→ u(t) ∈ M is said to be locally p-absolutely continuous if there exists m ∈ L p loc((a, b)) such that

<span id="page-3-2"></span>
$$
\forall a \le s < t \le b: \qquad d(u(s), u(t)) \le \int_s^t m(r) \, dr. \tag{2.1}
$$

We write for short <sup>u</sup> <sup>∈</sup> AC<sup>p</sup> loc (a, b),(M, d) . For any such curve the metric derivative is defined by

$$
|u'(t)| = \lim_{s \to t} \frac{d(u(s), u(t))}{|s - t|}.
$$

The limit exists for a.e. t ∈ (a, b) and is the smallest m in [\(2.1\)](#page-3-2), see [\[2,](#page-35-3) Thm. 1.1.2].

Now, let Φ : M → R be lower semicontinuous function. The metric analogue of the modulus of the gradient of Φ is given by the following definition.

Definition 2.1 (Strong upper gradient). A function G : M → [0,∞], is a strong upper gradient for Φ if for every absolutely continuous curve u : (a, b) → M, the function G(u) is Borel and

$$
|\Phi(u(s)) - \Phi(u(t))| \le \int_s^t G(u(r))|u'|(r)dr, \quad \forall a < s \le t < b.
$$

By Young's inequality, we see that the last inequality implies that

$$
\Phi(u(s)) - \Phi(u(t)) \leq \frac{1}{2} \int_s^t |u'|^2(r) dr + \frac{1}{2} \int_s^t G^2(u(r)) dr,
$$

for any absolutely continuous curve u provided the G is a strong upper gradient.

The following definition formalizes what it means for a curve to be a gradient flow of the function Φ in the metric space (M, d). Shortly, it is a curve that saturates the previous inequality.

Definition 2.2 (Curve of maximal slope). A locally absolutely continuous curve u : (a, b) → M is called a curve of maximal slope for Φ with respect to its strong upper gradient G if for all a ≤ s ≤ t ≤ b we have the energy identity

<span id="page-4-1"></span>
$$
\Phi(u(s)) - \Phi(u(t)) = \frac{1}{2} \int_s^t |u'|^2(r) dr + \frac{1}{2} \int_s^t G^2(u(r)) dr . \tag{2.2}
$$

When Φ is bounded below one has a convenient estimate on the modulus of continuity of a curve of maximal slope u. By H¨older's inequality and [\(2.2\)](#page-4-1) we infer that for all s < t we have

$$
d(u(s), u(t)) \le \int_s^t |u'|(r)dr \le \sqrt{t-s} \left(\int_s^t |u'|^2(r)dr\right)^{\frac{1}{2}}
$$
  
$$
\le \sqrt{t-s} \sqrt{2(\Phi(u(0)) - \Phi_{\min})}.
$$

<span id="page-4-0"></span>2.2. Discrete setting. Let us now introduce the setting for the discrete McKean– Vlasov equations that we consider.

In the sequel, we will denote with P(X ), the space of probability measures on X , and P ∗ (X ) the set of all measures that are strictly positive, i.e.

$$
\mu \in \mathcal{P}^*(\mathcal{X}) \qquad \text{iff} \qquad \forall x \in \mathcal{X} : \mu_x > 0,
$$

and finally with P a (X ), the set of all measures that have everywhere mass bigger than a, i.e.

$$
\mu \in \mathcal{P}^a(\mathcal{X})
$$
 iff  $\forall x \in \mathcal{X} : \mu_x \ge a$ .

As in [\[6,](#page-35-17) [7\]](#page-35-0), we shall consider equations of the form [\(1.1\)](#page-0-0) where Q is Gibbs with some potential function K. Here is the definition of such transition rates, taken from [\[7\]](#page-35-0):

<span id="page-5-0"></span>Definition 2.3. Let K : P(X ) × X → R be such that for each x ∈ X , K<sup>x</sup> : P(X ) → R is a twice continuously differentiable function on P(X ). A family of matrices {Q(µ) ∈ <sup>R</sup>X ×X }µ∈P(X) is Gibbs with potential function K, if for each µ ∈ P(X ), Q(µ) is the rate matrix of an irreducible, reversible ergodic Markov chain with respect to the probability measure

<span id="page-5-1"></span>
$$
\pi_x(\mu) = \frac{1}{Z(\mu)} \exp(-H_x(\mu)), \qquad (2.3)
$$

with

$$
H_x(\mu) = \frac{\partial}{\partial \mu_x} U(\mu) , \quad U(\mu) = \sum_{x \in \mathcal{X}} \mu_x K_x(\mu) .
$$

In particular Q(µ) satisfies the detailed balance condition w.r.t. π(µ), that is for all x, y ∈ X

<span id="page-5-3"></span>
$$
\pi_x(\mu)Q_{xy}(\mu) = \pi_y(\mu)Q_{yx}(\mu) \tag{2.4}
$$

holds. Moreover, we assume that for each x, y ∈ X the map µ 7→ Qxy(µ) is Lipschitz continuous over P(X ).

In the above definition and in the following we use the convention that a function F(·) : P(X ) → R is regular if and only if it can be extended in an open neighborhood of <sup>P</sup>(<sup>X</sup> ) <sup>⊂</sup> <sup>R</sup><sup>d</sup> in which it is regular in the usual sense. Hereby, regular could be continuous, Lipschitz or differentiable. In particular, we use this for the (twice) continuously differentiable function K<sup>x</sup> and the Lipschitz continuous function Qxy from above.

<span id="page-5-4"></span>Remark 2.4. There are many ways of building a Markov kernel that is reversible with respect to a given probability measure. The most widely used method is the Metropolis algorithm, first introduced in [\[33\]](#page-36-17):

$$
Q_{xy}^{\text{MH}}(\mu) := \min\left(\frac{\pi_y(\mu)}{\pi_x(\mu)}, 1\right) = e^{-(H_y(\mu) - H_x(\mu))_+}, \text{ with } (a)_+ := \max\{0, a\}.
$$

By this choice of the rates it is only necessary to calculate H(µ) and not the partition sum Z(µ) in [\(2.3\)](#page-5-1), which often is a costly computational problem.

A general scheme for obtaining rates satisfying the detailed balance condition with respect to π in [\(2.3\)](#page-5-1) is to consider

$$
Q_{xy}(\mu) = \frac{\sqrt{\pi_y(\mu)}}{\sqrt{\pi_x(\mu)}} A_{xy}(\mu),
$$

where {A(µ)}µ∈P(X) is a family of irreducible symmetric matrices. If we choose Axy(µ) = <sup>α</sup>x,y min <sup>√</sup> πy(µ) √ πx(µ) , √ πx(µ) √ πy(µ) with α ∈ {0, 1} X ×X an irreducible symmetric adjacency matrix, we recover the Metropolis algorithm on the corresponding graph.

We will be interested in the non-linear evolution equation

<span id="page-5-2"></span>
$$
\dot{c}_x(t) = \sum_{y \in \mathcal{X}} c_y(t) Q_{yx}(c(t)), \qquad (2.5)
$$

with the convention Qxx(µ) = − P <sup>y</sup>6=<sup>x</sup> Qxy(µ). By the Lipschitz assumption on Q this equation has a unique solution.

One goal will be to express this evolution as the gradient flow of the associated free energy functional F : P(X ) → R defined by

<span id="page-6-1"></span>
$$
\mathcal{F}(\mu) := \sum_{x \in \mathcal{X}} \mu_x \log \mu_x + U(\mu), \quad \text{with} \quad U(\mu) := \sum_{x \in \mathcal{X}} \mu_x K_x(\mu). \quad (2.6)
$$

To this end, it will be convenient to introduce the so-called Onsager operator K(µ) : <sup>R</sup><sup>X</sup> <sup>→</sup> <sup>R</sup><sup>X</sup> . It is defined as follows:

Let Λ : R<sup>+</sup> × R<sup>+</sup> → R+, denote the logarithmic mean given by

$$
\Lambda(s,t) := \int_0^1 s^{\alpha} t^{1-\alpha} d\alpha = \frac{s-t}{\log s - \log t}.
$$

Λ is continuous, increasing in both variables, jointly concave and 1-homogeneous. See for example [\[31,](#page-36-0) [22\]](#page-35-15) for more about properties of this logarithmic mean. In the sequel we are going to use the following notation

<span id="page-6-4"></span>
$$
w_{xy}(\mu) := \Lambda(\mu_x Q_{xy}(\mu), \mu_y Q_{yx}(\mu)) \tag{2.7}
$$

since this term will appear very often. By the definition of Λ and the properties of Q we get that wxy is uniformly bounded on P(X ), by a constant Cw.

Now, we can define

<span id="page-6-2"></span>
$$
\mathcal{K}(\mu) := \frac{1}{2} \sum_{x,y} w_{xy}(\mu) \ (e_x - e_y) \otimes (e_x - e_y), \tag{2.8}
$$

where {ex}x∈X is identified with the standard basis of <sup>R</sup><sup>X</sup> . More explicitly, we have for <sup>ψ</sup> <sup>∈</sup> <sup>R</sup><sup>X</sup> :

$$
(\mathcal{K}(\mu)\psi)_x = \sum_y w_{xy}(\mu)(\psi_x - \psi_y).
$$

With this in mind, we can formally rewrite the evolution [\(2.5\)](#page-5-2) in gradient flow form:

<span id="page-6-3"></span>
$$
\dot{c}(t) = -\mathcal{K}(c(t))D\mathcal{F}(c(t)),\tag{2.9}
$$

where <sup>D</sup>F(µ) <sup>∈</sup> <sup>R</sup><sup>X</sup> is the differential of <sup>F</sup> given by <sup>D</sup>F(µ)<sup>x</sup> <sup>=</sup> <sup>∂</sup>µxF(µ).

Finally, let us introduce the Fisher information I : P(X ) → [0,∞] defined for µ ∈ P ∗ (X ) by

<span id="page-6-0"></span>
$$
\mathcal{I}(\mu) := \frac{1}{2} \sum_{(x,y)\in E_{\mu}} w_{xy}(\mu) \left( \log(\mu_x Q_{xy}(\mu)) - \log(\mu_y Q_{yx}(\mu)) \right)^2 \tag{2.10}
$$

where, for µ ∈ P(X ), we define the edges of possible jumps by

<span id="page-6-5"></span>
$$
E_{\mu} := \{(x, y) \in \mathcal{X} \times \mathcal{X} : Q_{xy}(\mu) > 0\}.
$$
 (2.11)

For <sup>µ</sup> ∈ P(<sup>X</sup> ) \ P<sup>∗</sup> (X ) we set I(µ) = +∞.

I gives the dissipation of F along the evolution, namely, if c is a solution to [\(2.5\)](#page-5-2) then

$$
\frac{d}{dt}\mathcal{F}(c(t)) = -\mathcal{I}(c(t)) \; .
$$

<span id="page-7-0"></span>2.3. Continuity equation and action. In the sequel we shall use the notation for the discrete gradient. Given a function <sup>ψ</sup> <sup>∈</sup> <sup>R</sup><sup>X</sup> we define <sup>∇</sup><sup>ψ</sup> <sup>∈</sup> <sup>R</sup>X ×X via <sup>∇</sup>xy<sup>ψ</sup> := <sup>ψ</sup><sup>y</sup> <sup>−</sup>ψ<sup>x</sup> for x, y ∈ X . We shall also use a notion of discrete divergence, given <sup>v</sup> <sup>∈</sup> <sup>R</sup>X ×X , we define δv <sup>∈</sup> <sup>R</sup><sup>X</sup> via (δv)<sup>x</sup> <sup>=</sup> 1 2 P y (vxy − vyx).

<span id="page-7-3"></span>Definition 2.5 (Continuity equation). Let T > 0 and µ, ν ∈ P(X ). A pair (c, v) is called a solution to the continuity equation, for short (c, v) <sup>∈</sup> CE<sup>~</sup> <sup>T</sup> (µ, ν), if

- (i) c ∈ C 0 ([0, T],P(X )), i.e. ∀x ∈ X : t 7→ cx(t) ∈ C 0 ([0, T], [0, 1]);
- (ii) c(0) = µ; c(T) = ν;
- (iii) <sup>v</sup> : [0, T] <sup>→</sup> <sup>R</sup>X ×X is measurable and integrable;
- (iv) The pair (c, v) satisfies the continuity equation for t ∈ (0, T) in the weak form, i.e. for all ϕ ∈ C 1 c ((0, T), R) and all x ∈ X holds

$$
\int_0^T \left[ \dot{\varphi}(t) \ c_x(t) - \varphi(t) \ (\delta v)_x(t) \right] dt = 0. \tag{2.12}
$$

<span id="page-7-2"></span>In a similar way, we shall write (c, ψ) <sup>∈</sup> CE<sup>T</sup> (µ, ν) if (c, w(c)∇ψ) <sup>∈</sup> CE<sup>~</sup> <sup>T</sup> (µ, ν) for <sup>ψ</sup> : [0, T] <sup>→</sup> <sup>R</sup><sup>X</sup> and (w(c)∇ψ)xy (t) := <sup>w</sup>xy(c(t))∇xyψ(t) defined pointwise. In the case T = 1 we will often neglect the time index in the notation setting CE( ~ µ, ν) := CE~ <sup>1</sup>(µ, ν). Also, the endpoints (µ, ν) will often be suppressed in the notation.

To define the action of a curve it will be convenient to introduce the function α : R × R<sup>+</sup> → R<sup>+</sup> defined by

<span id="page-7-1"></span>
$$
\alpha(v, w) := \begin{cases} \frac{v^2}{w} & , w > 0 \\ 0 & , v = 0 = w \\ +\infty & , \text{else} \end{cases}
$$
 (2.13)

Note that α is convex and lower semicontinuous.

Definition 2.6 (Curves of finite action). Given <sup>µ</sup> ∈ P(<sup>X</sup> ), <sup>v</sup> <sup>∈</sup> <sup>R</sup>X ×X and <sup>ψ</sup> <sup>∈</sup> <sup>R</sup><sup>X</sup> , we define the action of (µ, v) and (µ, ψ) via

$$
\vec{\mathcal{A}}(\mu, v) := \frac{1}{2} \sum_{x,y} \alpha(v_{xy}, w_{xy}(\mu)),
$$
\n
$$
\mathcal{A}(\mu, \psi) := \vec{\mathcal{A}}(\mu, w(\mu)\nabla\psi) = \frac{1}{2} \sum_{x,y} (\psi_y - \psi_x)^2 w_{xy}(\mu).
$$
\n(2.14)

Moreover, a solution to the continuity equation (c, v) ∈ CE<sup>T</sup> is called a curve of finite action if

<span id="page-7-4"></span>
$$
\int_0^T \vec{\mathcal{A}}(c(t), v(t)) dt < \infty.
$$

It will be convenient to note that for a given solution (c, v) to the continuity equation we can find a vector field ˜v = w(c)∇ψ of gradient form such that (c, v˜) still solves the continuity equation and has lower action.

<span id="page-8-2"></span>Proposition 2.7 (Gradient fields). Let (c, v) <sup>∈</sup> CE<sup>~</sup> <sup>T</sup> (µ, ν) be a curve of finite action, then there exists <sup>ψ</sup> : [0, T] <sup>→</sup> **<sup>R</sup>** <sup>X</sup> measurable such that (c, ψ) <sup>∈</sup> CE<sup>T</sup> (µ, ν) and

<span id="page-8-1"></span>
$$
\int_0^T \mathcal{A}(c(t), \psi(t)) dt \le \int_0^T \vec{\mathcal{A}}(c(t), v(t)) dt.
$$
 (2.15)

Proof. Given <sup>c</sup> ∈ P(<sup>X</sup> ) we will endow <sup>R</sup>X ×X with the weighted inner product

$$
\langle \Psi, \Phi \rangle_{\mu} := \frac{1}{2} \sum_{x,y} \Psi_{xy} \Phi_{xy} w_{xy}(\mu) ,
$$

such that <sup>A</sup>~(µ, v) = <sup>|</sup>Ψ<sup>|</sup> 2 µ if <sup>v</sup>xy <sup>=</sup> <sup>w</sup>xyΨxy. Denote by Ran(∇) := {∇<sup>ψ</sup> : <sup>ψ</sup> <sup>∈</sup> <sup>R</sup><sup>X</sup> } ⊂ RX ×X the space of gradient fields. Moreover, denote by

$$
\text{Ker}(\nabla^*_{\mu}) := \left\{ \Psi \in \mathbf{R}^{\mathcal{X} \times \mathcal{X}} : \sum_{x,y} (\Psi_{yx} - \Psi_{xy}) w_{xy}(\mu) = 0 \right\}
$$

the space of divergence free vector fields. Note that we have the orthogonal decomposition

$$
\mathbf{R}^{\mathcal{X}\times\mathcal{X}}=\mathrm{Ker}(\nabla_{\mu}^{*})\oplus^{\perp}\mathrm{Ran}(\nabla).
$$

Now, given (c, v) <sup>∈</sup> CE<sup>~</sup> <sup>T</sup> (µ, ν), we have <sup>A</sup>~(c(t), v(t)) <sup>&</sup>lt; <sup>∞</sup> for a.e. <sup>t</sup> <sup>∈</sup> [0, T]. Thus, from [\(2.13\)](#page-7-1) we see that for a.e. t and all x, y we have that vxy(t) = 0 whenever wxy(c(t)) = 0. Hence, we can define

$$
\Psi_{xy}(t) := \frac{v_{xy}(t)}{w_{xy}(c(t))}
$$
 for a.e.  $t \in [0, T]$ .

Then <sup>ψ</sup> : [0, T] <sup>→</sup> <sup>R</sup><sup>X</sup> can be given by setting <sup>∇</sup>ψ(t) to be the orthogonal projection of Ψ(t) onto Ran(∇) w.r.t. h·, ·ic(t) . The orthogonal decomposition above then implies immediately that (c, w∇ψ) <sup>∈</sup> CE<sup>~</sup> <sup>T</sup> (µ, ν) and that |∇ψ(t)| 2 <sup>c</sup>(t) ≤ |Ψ(t)| 2 <sup>c</sup>(t) <sup>=</sup> <sup>A</sup>~(c(t), v(t)) for a.e. <sup>t</sup> <sup>∈</sup> [0, T]. This yields [\(2.15\)](#page-8-1).

<span id="page-8-0"></span>2.4. Metric. We shall now introduce a new transportation distance on the space P(X ), which will provide the underlying geometry for the gradient flow interpretation of the mean field evolution equation [\(1.1\)](#page-0-0).

<span id="page-8-3"></span>Definition 2.8 (Transportation distance). Given µ, ν ∈ P(X ), we define

<span id="page-8-5"></span>
$$
\mathcal{W}^2(\mu, \nu) := \inf \left\{ \int_0^1 \mathcal{A}(c(t), \psi(t)) \, dt : (c, \psi) \in \text{CE}_1(\mu, \nu) \right\}.
$$
 (2.16)

<span id="page-8-4"></span>Remark 2.9. As a consequence of Proposition [2.7](#page-8-2) and the fact that for any µ ∈ P(X ) and <sup>ψ</sup> <sup>∈</sup> <sup>R</sup><sup>X</sup> give rise to <sup>v</sup> <sup>∈</sup> <sup>R</sup>X ×X via <sup>v</sup>xy <sup>=</sup> <sup>w</sup>xy(µ)∇xy<sup>ψ</sup> such that <sup>A</sup>(µ, ψ) = <sup>A</sup>~(µ, v) we obtain an equivalent reformulation of the function W:

$$
\mathcal{W}^2(\mu,\nu) = \inf \left\{ \int_0^1 \vec{\mathcal{A}}(c(t),v(t)) \, dt : (c,v) \in \vec{\mathrm{CE}}_1(\mu,\nu) \right\}.
$$

It turns out that W is indeed a distance.

<span id="page-9-2"></span>Proposition 2.10. The function W defined in Definition [2.8](#page-8-3) is a metric and the metric space (P(X ),W) is seperable and complete. Moreover, any two points µ, ν ∈ P(X ) can be joined by a constant speed W-geodesic, i.e. there exists a curve (γt)t∈[0,1] with γ<sup>0</sup> = µ and γ<sup>1</sup> = ν satisfying W(γs, γt) = |t − s|W(µ, ν) for all s, t ∈ [0, 1].

We defer the proof of this statement until Section [4.](#page-28-0) Let us give a characterization of absolutely continuous curves w.r.t. W.

<span id="page-9-3"></span>Proposition 2.11. A curve c : [0, T] → P(X ) is absolutely continuous w.r.t. W if and only if there exists <sup>ψ</sup> : [0, T]×X → <sup>R</sup> such that (c, ψ) <sup>∈</sup> CE<sup>T</sup> , and <sup>R</sup> <sup>T</sup> 0 p A(c(t), ψ(t)) dt < ∞. Moreover, we can choose ψ such that the metric derivative of c is given as |c ′ p (t)| = A(c(t), ψ(t)) for a.e. t.

Proof. The proof is identical to the one of [\[18,](#page-35-18) Thm. 5.17].

<span id="page-9-0"></span>2.5. Gradient flows. In this section, we shall present the interpretation of the discrete McKean-Vlasov equation as a gradient flow with respect to the distance W. We will use the abstract framework introduced in Section [2.1](#page-3-1) above, where (M, d) = (P(X ),W) and Φ = F.

Lemma 2.12. Let I : P(X ) → [0,∞] defined in [\(2.10\)](#page-6-0) denote the Fisher information and let <sup>F</sup> : <sup>P</sup>(<sup>X</sup> ) <sup>→</sup> <sup>R</sup> defined in [\(2.6\)](#page-6-1) denote the free energy. Then, <sup>√</sup> I is a strong upper gradient for F on (P(X ),W), i.e. for (c, ψ) ∈ CE<sup>T</sup> and 0 ≤ t<sup>1</sup> < t<sup>2</sup> ≤ T holds

<span id="page-9-1"></span>
$$
|\mathcal{F}(c(t_2)) - \mathcal{F}(c(t_1))| \le \int_{t_1}^{t_2} \sqrt{\mathcal{I}(c(t))} \sqrt{\mathcal{A}(c(t), \psi(t))} dt.
$$
 (2.17)

Proof. Let c : (a, b) → (P(X ),W) be a W−absolutely continuous curve with ψ the associated gradient potential such that (c, ψ) ∈ CE(c(a), c(b)) and |c ′ <sup>|</sup>(t) = <sup>p</sup> A(c(t), ψ(t)) for a.e. t ∈ (a, b). We can assume w.l.o.g. that the r.h.s. of [\(2.17\)](#page-9-1) is finite. For the proof, we are going to define the auxiliary functions

$$
\mathcal{F}_{\delta}(\mu) = \sum_{x \in \mathcal{X}} (\mu_x + \delta) \log(\mu_x + \delta) + U(\mu).
$$

The function Fδ(µ) are Lipschitz continuous and converge uniformly to F, as δ → 0. By Lemma [4.2,](#page-28-1) c is also absolutely continuous with respect to Euclidean distance. Therewith, since <sup>F</sup><sup>δ</sup> are Lipschitz continuous, we have that <sup>F</sup>δ(c) : (a, b) <sup>→</sup> **<sup>R</sup>** is absolutely continuous and hence

$$
\mathcal{F}_{\delta}(c(t_2)) - \mathcal{F}_{\delta}(c(t_1)) = \int_{t_1}^{t_2} \frac{d}{dt} \mathcal{F}_{\delta}(c)(t)dt = \int_{t_1}^{t_2} D\mathcal{F}_{\delta}(c(t))\dot{c}(t) dt,
$$

where DFδ(c(t)) is well-defined for a.e. t and given in terms of

$$
\partial_{e_x} \mathcal{F}_{\delta}(c(t)) = H_x(c(t)) + \log(c_x(t) + \delta) + 1.
$$

Now, we have by using the Cauchy-Schwarz inequality

$$
\int_{t_1}^{t_2} |D\mathcal{F}_{\delta}(c(t))\dot{c}(t)| dt \leq \int_{t_1}^{t_2} \left| \frac{1}{2} \sum_{x,y \in \mathcal{X}} (\psi_x - \psi_y)(\partial_{e_x} \mathcal{F}_{\delta}(c) - \partial_{e_y} \mathcal{F}_{\delta}(c)) w_{xy}(c) \right| dt
$$
  
\n
$$
\leq \int_{t_1}^{t_2} \sqrt{\frac{1}{2} \sum_{x,y \in \mathcal{X}} (\nabla_{xy} \psi)^2 w_{xy}(c)} \sqrt{\frac{1}{2} \sum_{x,y \in \mathcal{X}} (\partial_{e_x} \mathcal{F}_{\delta}(c) - \partial_{e_y} \mathcal{F}_{\delta}(c))^2 w_{xy}(c)} dt
$$
  
\n
$$
= \int_{t_1}^{t_2} \sqrt{\mathcal{A}(c, \psi)} \times \sqrt{\frac{1}{2} \sum_{x,y \in \mathcal{X}} (\log(c_x + \delta) + H_x(c) - \log(c_y + \delta) - H_y(c))^2 w_{xy}(c)} dt.
$$
  
\n
$$
\leq \int_{t_1}^{t_2} \sqrt{\mathcal{A}(c, \psi)} \sqrt{2\mathcal{I}(c) + C_H^2 \sum_{x,y \in \mathcal{X}} w_{xy}(c)} dt,
$$

where we dropped the t-dependence on c and ψ. For the last inequality, we observe that since <sup>H</sup><sup>x</sup> for <sup>x</sup> ∈ X are uniformly bounded and for a < b, δ > 0 it holds <sup>b</sup> a ≥ b+δ a+δ , it is easy to see that the quantity | log(cx(t) + δ) + Hx(c(t)) − log(cy(t) + δ) − Hy(c(t))| is bounded by | log(cx(t)) + Hx(c(t))−log(cy(t))− Hy(c(t))|+C<sup>H</sup> with C<sup>H</sup> only depending on H. Moreover, we observe that by definitions of H<sup>x</sup> and π from [\(2.3\)](#page-5-1), it holds

$$
\begin{aligned} \left| \log(\mu_x) + H_x(\mu) - \log(\mu_y) - H_y(\mu) \right| &= \left| \log \frac{\mu_x}{\pi_x(\mu)} - \log \frac{\mu_y}{\pi_y(\mu)} \right| \\ &= \left| \log \left( \mu_x Q_{xy}(\mu) \right) - \log \left( \pi_x(\mu) Q_{xy}(\mu) \right) - \log \left( \pi_y(\mu) Q_{yx}(\mu) \right) - \log \left( \mu_y Q_{yx}(\mu) \right) \right|. \end{aligned}
$$

Then, by the detailed balance condition [\(2.4\)](#page-5-3) the two middle terms cancel and we arrive at <sup>I</sup>(µ). Since, we assumed <sup>R</sup> <sup>t</sup><sup>2</sup> t1 p A(c(t), ψ(t))p I(c(t)) dt to be finite, we can apply the dominated convergence theorem and get the conclusion.

<span id="page-10-1"></span>Proposition 2.13. For any absolutely continuous curve (c(t))t∈[0,T] in P(X ) holds

<span id="page-10-0"></span>
$$
\mathcal{J}(c) := \mathcal{F}(c(T)) - \mathcal{F}(c(0)) + \frac{1}{2} \int_0^T \mathcal{I}(c(t)) \, dt + \frac{1}{2} \int_0^T \mathcal{A}(c(t), \psi(t)) \, dt \ge 0 \tag{2.18}
$$

Moreover, equality is attained if and only if (c(t))t∈[0,T] is a solution to [\(1.1\)](#page-0-0). In this case <sup>c</sup>(t) ∈ P<sup>∗</sup> (X ) for all t > 0.

In other words, solution to [\(1.1\)](#page-0-0) are the only gradient flow curves (i.e. curves of maximal slope) of F.

Proof. The first statement follows as above by Young's inequality from the fact that I is strong upper gradient for F.

Now let us assume that for a curve c, J (c) ≤ 0 holds. Then since [\(2.17\)](#page-9-1) holds for every curve we can deduce that we actually have

$$
\mathcal{F}(c(t_2)) - \mathcal{F}(c(t_1)) + \frac{1}{2} \int_{t_1}^{t_2} \mathcal{I}(c(t))dt + \frac{1}{2} \int_{t_1}^{t_2} \mathcal{A}(c(t), \psi(t))dt = 0, \quad 0 \le t_1 \le t_2 \le T.
$$

Since R <sup>T</sup> 0 I(c(t))dt < ∞, we can find a sequence ǫn, converging to zero, such that <sup>I</sup>(c(ǫn)) <sup>&</sup>lt; <sup>∞</sup>. By continuity of c, we can find a, ǫ > 0, such that <sup>c</sup>(t) ∈ P<sup>a</sup> (X ), for t ∈ [ǫn, ǫ<sup>n</sup> + ǫ]. Now, since I is Lipschitz in P a (X ), we can apply the chain rule for ǫ<sup>n</sup> ≤ t<sup>1</sup> ≤ t<sup>2</sup> ≤ ǫ<sup>n</sup> + ǫ and get

$$
\mathcal{F}(c(t_1)) - \mathcal{F}(c(t_2)) = \int_{t_1}^{t_2} \langle D\mathcal{F}(c(t)), \mathcal{K}(c(t))\nabla\psi(t) \rangle
$$
  
= 
$$
\frac{1}{2} \int_{t_1}^{t_2} \mathcal{A}(c(t), \psi(t))dt + \frac{1}{2} \int_{t_1}^{t_2} \mathcal{I}(c(t))dt,
$$

by comparison we get

$$
\langle D\mathcal{F}(c(t)), \mathcal{K}(c(t))\nabla\psi(t)\rangle = \sqrt{\mathcal{A}(c(t), \psi(t)) \mathcal{I}(c(t))} = \mathcal{A}(c(t), \psi(t)) = \mathcal{I}(c(t)),
$$

for t ∈ [ǫn, ǫ<sup>n</sup> + ǫ]. From which, by an application of the inverse of the Cauchy-Schwarz inequality, we get that ψx(t) − ψy(t) = ∂exF(c(t)) − ∂eyF(c(t)). Now we have

<span id="page-11-0"></span>
$$
\dot{c}(t) = -\mathcal{K}(c(t))D\mathcal{F}(c(t))
$$
\n
$$
= -\frac{1}{2} \sum_{x,y} w_{xy}(c(t)) \left( e_x - e_y \right) \left( \partial_{e_x} \mathcal{F}(c(t)) - \partial_{e_y} \mathcal{F}(c(t)) \right)
$$
\n
$$
= -\frac{1}{2} \sum_{x,y} \left( Q_{xy}(c(t))c_x(t) - Q_{yx}(c(t))c_y(t) \right) \left( e_x - e_y \right)
$$
\n
$$
= -\sum_x \left( \sum_y \left( Q_{xy}(c(t))c_x(t) - Q_{yx}(c(t))c_y(t) \right) \right) e_x = c(t)Q(c(t))
$$
\n(2.19)

on the interval [ǫn, ǫ<sup>n</sup> + ǫ]. We actually have that c(t) is a solution to ˙c(t) = c(t)Q(c(t)) on [ǫn, T]. Indeed, let T<sup>n</sup> = sup{t ′ <sup>≤</sup> <sup>T</sup> : ˙c(t) = <sup>c</sup>(t)Q(c(t)), <sup>∀</sup><sup>t</sup> <sup>∈</sup> [ǫn, t′ ]}. We have <sup>c</sup>(Tn) ∈ P<sup>b</sup> (X ), for some b > 0, because c is a solution to ˙c(t) = c(t)Q(c(t)), on [ǫn, Tn) and the dynamics are irreducible. Now if we apply the same argument for Tn, that we used for ǫn, we can extent the solution beyond Tn. If T<sup>n</sup> < T, then we will get a contradiction, Therefore T<sup>n</sup> = T. Now by sending ǫ<sup>n</sup> to zero we get that c is a solution to ˙c(t) = c(t)Q(c(t)), on [0, T].

Now on the other hand if c is a solution to ˙c(t) = c(t)Q(c(t)) on [0, T], we can get that for every ǫ > <sup>0</sup>, there exists a > <sup>0</sup>, such that <sup>c</sup>(t) ∈ P<sup>a</sup> (X ) on [ǫ, T]. The choice ψ(t) = DF(t), satisfies the continuity equation (see [\(2.19\)](#page-11-0)), and by applying the chain rule, we get that

$$
\mathcal{F}(c(T)) - \mathcal{F}(c(\epsilon)) + \frac{1}{2} \int_{\epsilon}^{T} \mathcal{I}(c(t))dt + \frac{1}{2} \int_{\epsilon}^{T} \mathcal{A}(c(t), \psi(t))dt = 0.
$$

Sending ǫ to zero concludes the proof.

Remark 2.14. Note that the formulation above contains the usual entropy entropyproduction relation for gradient flows. If c is a solution to [\(1.1\)](#page-0-0), then ψ(t) = −DF(c(t)) and especially it holds that A (c(t), −DF(c(t))) = I(c(t)). Therewith, [\(2.18\)](#page-10-0) becomes

$$
\mathcal{F}(c(T)) + \int_0^T \mathcal{I}(c(t)) dt = \mathcal{F}(c(0)).
$$

<span id="page-12-0"></span>2.6. Lifted dynamics on the space of random measures. It is possible to lift the evolution ˙c(t) = <sup>c</sup>(t)Q(c(t)) in <sup>P</sup>(<sup>X</sup> ) to an evolution for measures **<sup>C</sup>** on <sup>P</sup>(<sup>X</sup> ). This is convenient, if one does not want to start from a deterministic point but consider random initial data. The evolution is then formally given by

<span id="page-12-1"></span>
$$
\partial_t \mathbb{C}(t,\nu) + \text{div}_{\mathcal{P}(\mathcal{X})} \left( \mathbb{C}(t,\nu) \left( \nu Q(\nu) \right) \right) = 0, \quad \text{with} \quad \text{div}_{\mathcal{P}(\mathcal{X})} = \sum_{x \in \mathcal{X}} \partial_{e_x}.
$$
 (2.20)

Notation. In the following, all quantities connected to the space P(P(X )) will be denoted by blackboard-bold letters, like for instance random probability measures **<sup>M</sup>** <sup>∈</sup> <sup>P</sup>(P(<sup>X</sup> )) or functionals **<sup>F</sup>** : <sup>P</sup>(P(<sup>X</sup> )) <sup>→</sup> <sup>R</sup>.

The evolution [\(2.20\)](#page-12-1) also has a natural gradient flow structure that is obtained by lifting the gradient flow structure of the underlying dynamics. In fact, [\(2.20\)](#page-12-1) will turn out to be a gradient flow w.r.t. to the classical L 2 -Wasserstein distance on P(P(X )), which is build from the distance W on the base space P(X ). To establish this gradient structure, we need to introduce lifted analogues of the continuity equation and the action of a curve as well as a probabilistic representation result for the continuity equation.

<span id="page-12-3"></span>Definition 2.15 (Lifted continuity equation). A pair (**C**, **V**) is called a solution to the lifted continuity equation, for short (**C**, **<sup>V</sup>**) <sup>∈</sup> **CE**<sup>~</sup> <sup>T</sup> (**M**, **N**), if

- (i) [0, T] <sup>∋</sup> <sup>t</sup> 7→ **<sup>C</sup>**(t) ∈ P(P(<sup>X</sup> )) is weakly<sup>∗</sup> continuous,
- (ii) **C**(0) = **M**; **C**(T) = **N**;
- (iii) **<sup>V</sup>** : [0, T] × P(<sup>X</sup> ) <sup>→</sup> <sup>R</sup>X ×X is measurable and integrable w.r.t. **<sup>C</sup>**(t, dµ)dt,
- (iv) The pair (**C**, **<sup>V</sup>**) satisfies the continuity equation for <sup>t</sup> <sup>∈</sup> (0, T) in the weak form, i.e. for all ϕ ∈ C 1 c ((0, T) × P(X )) holds

$$
\int_0^T \int_{\mathcal{P}(\mathcal{X})} (\dot{\varphi}(t,\nu) - \langle \nabla \varphi(t,\nu), \delta \mathbb{V}(t,\nu) \rangle) \mathbb{C}(t, d\nu) dt = 0,
$$
\n(2.21)

<span id="page-12-2"></span>where <sup>δ</sup>**<sup>V</sup>** : <sup>P</sup>(<sup>X</sup> ) <sup>→</sup> <sup>R</sup>X ×X , is given by <sup>δ</sup>**V**(ν)<sup>x</sup> := <sup>1</sup> 2 P y (**V**xy(ν) <sup>−</sup> **<sup>V</sup>**yx(ν)).

Here we consider <sup>P</sup>(<sup>X</sup> ) as a subset of Euclidean space <sup>R</sup><sup>X</sup> with h·, ·i the usual inner product. In particular, <sup>∇</sup>ϕ(t, µ) = (∂µ<sup>x</sup> <sup>ϕ</sup>(t, µ))x∈X denotes the usual gradient on <sup>R</sup><sup>X</sup> and we have explicitly

$$
\langle \nabla \varphi(t, \nu), \delta \mathbb{V}(t, \nu) \rangle = \sum_{x \in \mathcal{X}} \partial_{\mu_x} \varphi(t, \mu) (\delta \mathbb{V}(t, \mu))_x
$$
  
= 
$$
\frac{1}{2} \sum_{x, y \in \mathcal{X}} \partial_{\mu_x} \varphi(t, \mu) \Big( \mathbb{V}_{xy}(t, \mu) - \mathbb{V}_{yx}(t, \mu) \Big).
$$

Thus, [\(2.21\)](#page-12-2) is simply the weak formulation of the classical continuity equation in R<sup>X</sup> . In a similar way, we shall write (**C**, **<sup>Ψ</sup>**) <sup>∈</sup> **CE**<sup>T</sup> (**M**, **<sup>N</sup>**) if **<sup>Ψ</sup>** : [0, T] × P(<sup>X</sup> ) <sup>→</sup> <sup>R</sup><sup>X</sup> is a function such that (**C**, **<sup>V</sup>**˜) <sup>∈</sup> **CE**<sup>~</sup> <sup>T</sup> (**M**, **N**) with **V**˜ xy(t, µ) = <sup>w</sup>xy(µ)∇xy**Ψ**(t, µ). In this case we have that <sup>δ</sup>**V**(µ) = <sup>K</sup>(µ)**Ψ**(µ), where <sup>K</sup>(µ) is the Onsager operator defined in [\(2.8\)](#page-6-2). Solutions to [\(2.20\)](#page-12-1) are understood as weak solutions like in Definition [\(2.15\)](#page-12-3). That is **C** is a weak solution to [\(2.20\)](#page-12-1) if (**C**, **Ψ** ∗ ) <sup>∈</sup> **CE**<sup>T</sup> with **<sup>Ψ</sup>** ∗ (ν) := −DF(ν). This leads, via the formal calculation

$$
\delta \mathbb{V}^*(\nu) := \mathcal{K}(\nu) \Psi^*(\nu) = -\mathcal{K}(\nu) D\mathcal{F}(\nu) = \nu Q(\nu),
$$

to the formulation: For all ϕ ∈ C 1 c ([0, T] × P(X )) we have

<span id="page-13-0"></span>
$$
\int_0^T \int_{\mathcal{P}(\mathcal{X})} \left( \dot{\varphi}(t,\nu) - \langle \nabla \varphi(t,\nu), \nu Q(\nu) \rangle \right) \mathbb{C}(t,d\nu) dt = 0.
$$
 (2.22)

By the Lipschitz assumption on Q the vector field νQ(ν) given by the components (νQ(ν))<sup>x</sup> = P y νyQxy(ν) is also Lipschitz. Then standard theory implies that equation [\(2.22\)](#page-13-0) has a unique solution (cf. [\[2,](#page-35-3) Chapter 8]).

Definition 2.16 (Lifted action). Given **<sup>M</sup>** ∈ P(P(<sup>X</sup> )), **<sup>V</sup>** : <sup>P</sup>(<sup>X</sup> ) <sup>→</sup> <sup>R</sup>X ×X and **<sup>Ψ</sup>** : <sup>P</sup>(<sup>X</sup> ) <sup>→</sup> <sup>R</sup><sup>X</sup> , we define the action of (**M**, **<sup>V</sup>**) and (**M**, **<sup>Ψ</sup>**) by

$$
\vec{\mathbb{A}}(\mathbb{M}, \mathbb{V}) := \int_{\mathcal{P}(\mathcal{X})} \vec{\mathcal{A}}(\nu, \mathbb{V}(\nu)) \mathbb{M}(d\nu),
$$
$$
\mathbb{A}(\mathbb{M}, \Psi) := \int_{\mathcal{P}(\mathcal{X})} \mathcal{A}(\nu, \Psi(\nu)) \mathbb{M}(d\nu).
$$

The next result tell us that is is sufficient to consider only gradient vector fields. It is the analog of Proposition [2.7.](#page-8-2)

<span id="page-13-5"></span>Proposition 2.17 (Gradient fields for Liouville equation). If (**C**, **<sup>V</sup>**) <sup>∈</sup> **CE**<sup>~</sup> <sup>T</sup> is a curve of finite action, then there exists **<sup>Ψ</sup>** : [0, T]×P(<sup>X</sup> ) <sup>→</sup> <sup>R</sup><sup>X</sup> measurable such that (**C**, **<sup>Ψ</sup>**) <sup>∈</sup> **CE**<sup>T</sup> and

<span id="page-13-1"></span>
$$
\int_0^T \mathbb{A}(\mathbb{C}(t), \Psi(t))dt \le \int_0^T \vec{\mathbb{A}}(\mathbb{C}(t), \mathbb{V}(t))dt.
$$
\n(2.23)

Proof. Given a solution (**C**, **<sup>V</sup>**) <sup>∈</sup> **CE**<sup>~</sup> <sup>T</sup> , for each t and ν ∈ P(X ) we apply the contruction in the proof of Proposition [2.7](#page-8-2) to **<sup>V</sup>**(ν) to obtain **<sup>Ψ</sup>**(t, ν) with <sup>A</sup>(ν, **<sup>Ψ</sup>**(t, ν)) <sup>≤</sup> <sup>A</sup>~(ν, **<sup>V</sup>**(t, ν)). It is readily checked that (**C**, **<sup>Ψ</sup>**) <sup>∈</sup> **CE**<sup>T</sup> . Integration against **<sup>C</sup>** and dt yields [\(2.23\)](#page-13-1).

Definition 2.18 (Lifted distance). Given **<sup>M</sup>**, **<sup>N</sup>** ∈ P(P(<sup>X</sup> )) we define

<span id="page-13-2"></span>
$$
\mathbb{W}^2(\mathbb{M}, \mathbb{N}) := \inf \left\{ \int_0^1 \mathbb{A}(\mathbb{C}(t), \Psi(t)) \, dt : (\mathbb{C}, \Psi) \in \mathbb{CE}_1(\mathbb{M}, \mathbb{N}) \right\} \,. \tag{2.24}
$$

Analogously to Remark [2.9](#page-8-4) we obtain an equivalent formulation of **W**:

<span id="page-13-3"></span>
$$
\mathbb{W}^2(\mathbb{M}, \mathbb{N}) = \inf \left\{ \int_0^1 \vec{\mathbb{A}}(\mathbb{C}(t), \mathbb{V}(t)) dt : (\mathbb{C}, \mathbb{V}) \in \widetilde{\mathbb{CE}}_1(\mathbb{M}, \mathbb{N}) \right\} .
$$
 (2.25)

The following result is a probabilistic representation via characteristics for the continuity equation. It is a variant of [\[2,](#page-35-3) Prop. 8.2.1] adapted to our setting.

<span id="page-13-4"></span>Proposition 2.19. For a given **<sup>M</sup>**, **<sup>N</sup>** ∈ P(P(<sup>X</sup> )) let (**C**, **<sup>Ψ</sup>**) <sup>∈</sup> **CE**<sup>T</sup> (**M**, **<sup>N</sup>**) be a solution of the continuity equation with finite action.

Then there exists a probability measure Θ on P(X ) × AC([0, T],P(X )) such that:

(1) Any (µ, c) ∈ supp Θ is a solution of the ODE

$$
\dot{c}(t) = \mathcal{K}(c(t))\Psi(t, c(t)) \quad \text{for a.e. } t \in [0, T],
$$
  
$$
c(0) = \mu.
$$

(2) For any 
$$
\varphi \in C_b^0(\mathcal{P}(\mathcal{X}))
$$
 and any  $t \in [0, T]$  holds

<span id="page-14-0"></span>
$$
\int_{\mathcal{P}(\mathcal{X})} \varphi(\nu) \mathbb{C}(t, d\nu) = \int_{\mathcal{P}(\mathcal{X}) \times \mathrm{AC}([0, T], \mathcal{P}(\mathcal{X}))} \varphi(c(t)) \Theta(d\mu_0, dc).
$$
\n(2.26)

Conversely any Θ satisfying (1) and

$$
\int_{\mathcal{P}(\mathcal{X}) \times \mathrm{AC}([0,T], \mathcal{P}(\mathcal{X}))} \int_0^T \mathcal{A}\left(c(t), \Psi(t, c(t))\right) dt \, \Theta(d\mu, dc) < \infty
$$

induces a family of measures **<sup>C</sup>**(t) via [\(2.26\)](#page-14-0) such that (**C**, **<sup>Ψ</sup>**) <sup>∈</sup> **CE**<sup>T</sup> (**M**, **<sup>N</sup>**).

We will also use the measure Θ on AC([0 ¯ , T],P(<sup>X</sup> )) given by

<span id="page-14-1"></span>
$$
\bar{\Theta}(dc) = \int_{\mathcal{P}(\mathcal{X})} \Theta(d\mu, dc) . \qquad (2.27)
$$

Therewith, note that [\(2.26\)](#page-14-0) can be rewritten as the pushforward **C**(t) = (et)#Θ under the ¯ evaluation map e<sup>t</sup> : AC([0, T],P(X )) ∋ c 7→ c(t) ∈ P(X ) defined for any ϕ ∈ C 0 b (P(X )) by

$$
\int_{\mathcal{P}(\mathcal{X})} \varphi(\nu) \ \mathbb{C}(t, d\nu) = \int_{\mathrm{AC}([0,T], \mathcal{P}(\mathcal{X}))} \varphi(c(t)) \ \bar{\Theta}(dc).
$$

Proof. Let (**C**, **<sup>Ψ</sup>**) <sup>∈</sup> **CE**<sup>T</sup> (**M**, **<sup>N</sup>**) be a solution of the continuity equation with finite action. Define **<sup>V</sup>** : [0, T] × P(<sup>X</sup> ) <sup>→</sup> <sup>R</sup>X ×X via **<sup>V</sup>**xy(t, ν) = <sup>w</sup>xy(ν)∇xy**Ψ**(t, ν) and note that <sup>δ</sup>**V**(t, ν) = <sup>K</sup>(ν)**Ψ**(t, ν). We view <sup>P</sup>(<sup>X</sup> ) as a subset of <sup>R</sup><sup>X</sup> and <sup>δ</sup>**<sup>V</sup>** as a time-dependent vector field on R<sup>X</sup> and note that (**C**, δ**V**) is a solution to the classical continuity equation in weak form

$$
\int_0^T \int_{\mathbf{R}^{\mathcal{X}}} \left( \dot{\varphi}(t,\nu) - \nabla \varphi(t,\nu) \delta \mathbb{V}(t,\nu) \right) \mathbb{C}(t, d\nu) dt = 0
$$

for all ϕ ∈ C 1 c (0, T) <sup>×</sup> <sup>R</sup><sup>X</sup> . Moreover, note that for any **<sup>Ψ</sup>** <sup>∈</sup> <sup>R</sup><sup>X</sup> we have by Jensens inequality

$$
|\mathcal{K}(\nu)\Psi|^2 = \sum_{x \in \mathcal{X}} \left| \sum_{y \in \mathcal{X}} w_{xy}(\nu) (\Psi_x - \Psi_y) \right|^2
$$
  
 
$$
\leq \sum_{x,y \in \mathcal{X}} C_w w_{xy}(\nu) |(\Psi_x - \Psi_y)|^2 = C_w \mathcal{A}(\nu, \Psi(\nu)),
$$

with

$$
C_w := \max_{x,y \in \mathcal{X}} \sup_{\nu \in \mathcal{P}(\mathcal{X})} w_{xy}(\nu) = \max_{x,y \in \mathcal{X}} \sup_{\nu \in \mathcal{P}(\mathcal{X})} \Lambda(\nu_x Q_{xy}(\nu), \nu_y Q_{yx}(\nu)).
$$

Since Q : P(X ) → R<sup>+</sup> is continuous, C<sup>w</sup> is finite. This yields the integrability estimate

$$
\int_0^T \int_{\mathbf{R}^d} |\delta \mathbb{V}(t,\nu)|^2 d\mathbb{C}(t,\nu) dt \leq C \int_0^T \mathbb{A}(\mathbb{C}(t), \Psi(t)) dt < \infty.
$$

Now, by the representation result [\[2,](#page-35-3) Proposition 8.2.1] for the classical continuity equation there exists a probability measure Θ on <sup>R</sup><sup>X</sup> <sup>×</sup> AC([0, T], <sup>R</sup><sup>X</sup> ) such that any (µ, c) <sup>∈</sup> supp Θ satisfies <sup>c</sup>(0) = <sup>µ</sup> and ˙c(t) = <sup>δ</sup>**V**(t, c(t)) in the sense weak sense [\(2.12\)](#page-7-2) and moreover, [\(2.26\)](#page-14-0) holds with <sup>P</sup>(<sup>X</sup> ) replaced by <sup>R</sup><sup>X</sup> . Since, **<sup>C</sup>**(t) is supported on <sup>P</sup>(<sup>X</sup> ) we find that Θ is actually a measure on P(X )×AC([0, T],P(X )), where absolute continuity is understood still w.r.t. the Euclidean distance. To see that Θ is the desired measure it remains to check that for Θ-a.e. (µ, c) we have that c is a curve of finite action. But this follows by observing that [\(2.26\)](#page-14-0) implies

$$
\int \int_0^T \mathcal{A}(c(t), \Psi(t, c(t))) dt \Theta(d\mu, dc) = \int_0^T \mathbb{A}(\mathbb{C}(t), \Psi(t)) dt < \infty.
$$

This finishes the proof of the first statement.

The converse, statement follows in the same way as in [\[2,](#page-35-3) Proposition 8.2.1]. Proposition 2.20 (Identification with Wasserstein distance). The distance **W** defined in [\(2.24\)](#page-13-2) coincides with the L 2 -Wasserstein distance on P(P(X )) w.r.t. the distance W on <sup>P</sup>(<sup>X</sup> ). More precisely, for **<sup>M</sup>**, **<sup>N</sup>** ∈ P(P(<sup>X</sup> )) there holds

$$
\mathbb{W}^2(\mathbb{M}, \mathbb{N}) = W^2_{\mathcal{W}}(\mathbb{M}, \mathbb{N}) := \inf_{\mathbb{G} \in \Pi(\mathbb{M}, \mathbb{N})} \left\{ \int_{\mathcal{P}(\mathcal{X}) \times \mathcal{P}(\mathcal{X})} \mathcal{W}^2(\mu, \nu) \, d\mathbb{G}(\mu, \nu) \right\},
$$

where Π(**M**, **<sup>N</sup>**) is the set of all probability measures on <sup>P</sup>(<sup>X</sup> ) × P(<sup>X</sup> ) with marginals **<sup>M</sup>** and **N**.

Proof. We first show the inequality "≥". For ε > 0 let (**C**, **<sup>Ψ</sup>**) be a solution to the continuity equation such that R <sup>1</sup> 0 **<sup>A</sup>**(**C**(t), **<sup>Ψ</sup>**(t))dt <sup>≤</sup> **<sup>W</sup>**<sup>2</sup> (**M**, **N**)+ε and let Θ be the measure ¯ on AC([0, T],P(X )) given by the previous Proposition. Then we obtain a coupling **<sup>G</sup>** <sup>∈</sup> Π(**M**, **<sup>N</sup>**) by setting **<sup>G</sup>** = (e0, e1)#Θ. This yields ¯

$$
W_{\mathcal{W}}^2(\mathbb{M}, \mathbb{N}) \le \int \mathcal{W}^2(\mu, \nu) d\mathbb{G}(\mu, \nu) = \int \mathcal{W}^2(c(0), c(1))d\bar{\Theta}
$$
  
\n
$$
\le \int \int_0^1 \mathcal{A}(c(t), \Psi(t, c(t)))dt d\bar{\Theta}(c) = \int_0^1 \mathbb{A}(\mathbb{C}(t), \Psi(t))dt \le \mathbb{W}^2(\mathbb{M}, \mathbb{N}) + \varepsilon.
$$

Since ε was arbitrary this yields the inequality "≥".

To prove the converse inequality "≤", fix an optimal coupling **<sup>G</sup>**, fix ε > 0 and choose for **G**-a.e. (µ, ν) a couple (c µ,ν , vµ,ν ) <sup>∈</sup> CE<sup>~</sup> <sup>1</sup>(µ, ν) such that

$$
\int_0^1 \vec{\mathcal{A}}(c^{\mu,\nu}(t), v^{\mu,\nu}(t))dt \le \mathcal{W}(\mu, \nu) + \varepsilon.
$$

Now, define a family of measures **<sup>C</sup>** : [0, 1] → P(P(<sup>X</sup> )) and a family of vector-valued measures <sup>V</sup> : [0, 1] → P(P(<sup>X</sup> ); <sup>R</sup>X ×X ) via

$$
d\mathbb{C}(t,\tilde{\nu}) = \int_{\mathcal{P}(\mathcal{X}) \times \mathcal{P}(\mathcal{X})} d\delta_{c^{\mu,\nu}(t)}(\tilde{\nu}) d\mathbb{G}(\mu,\nu) ,
$$
  
$$
V(t,\tilde{\nu}) = \int_{\mathcal{P}(\mathcal{X}) \times \mathcal{P}(\mathcal{X})} v^{\mu,\nu}(t) d\delta_{c^{\mu,\nu}(t)}(\tilde{\nu}) d\mathbb{G}(\mu,\nu) .
$$

Note that <sup>V</sup> (t) <sup>≪</sup> **<sup>C</sup>**(t) and define **<sup>V</sup>** : [0, 1]×P(<sup>X</sup> ) <sup>→</sup> <sup>R</sup>X ×X as the density of <sup>V</sup> w.r.t. **<sup>C</sup>**. By linearity of the continuity equations have that (**C**, **<sup>V</sup>**) <sup>∈</sup> **CE**<sup>~</sup> <sup>1</sup>(**M**, **N**). Moreover, we find

$$
\int_0^1 \vec{\mathbb{A}}(\mathbb{C}(t), \mathbb{V}(t)) dt = \int_0^1 \int \vec{\mathcal{A}}(c^{\mu,\nu}(t), v^{\mu,\nu}(t)) d\mathbb{G}(\mu, \nu) dt
$$
  
 
$$
\leq \int \mathcal{W}^2(\mu, \nu) d\mathbb{G}(\mu, \nu) + \varepsilon = W_W^2(\mathbb{M}, \mathbb{N}) + \varepsilon.
$$

Since ε was arbitrary, in view of [\(2.25\)](#page-13-3) this finishes the proof.

Finally, we can obtain a gradient flow structure for the Liouville equation [\(2.20\)](#page-12-1) in a straightforward manner by averaging the gradient flow structure of the underlying dynamical system.

To this end, given **<sup>M</sup>** ∈ P(P(<sup>X</sup> )) define the free energy by

$$
\mathbb{F}(\mathbb{M}) := \int_{\mathcal{P}(\mathcal{X})} \mathcal{F}(\nu) \, \mathbb{M}(d\nu) ,
$$

and define the Fisher information by

$$
\mathbb{I}(\mathbb{M}) := \mathbb{A}(\mathbb{M}, -D\mathbb{F}) = \int_{\mathcal{P}(\mathcal{X})} \mathcal{I}(\nu) \, \mathbb{M}(d\nu).
$$

<span id="page-16-1"></span>Proposition 2.21 (Gradient flow structure for Liouville equation). The Liouville equation [\(2.20\)](#page-12-1) is the gradient flow of **<sup>F</sup>** w.r.t. **<sup>W</sup>**. Moreover precisely, <sup>√</sup> **I** is a strong upper gradient for **<sup>F</sup>** on the metric space (P(P(<sup>X</sup> )), **<sup>W</sup>**) and the curves of maximal slope are precisely the solutions to [\(2.20\)](#page-12-1). In other words, for any absolutely continuous curve **C** in P(P(X )) holds

<span id="page-16-0"></span>
$$
\mathbb{J}(\mathbb{C}) := \mathbb{F}(\mathbb{C}(T)) - \mathbb{F}(\mathbb{C}(0)) + \frac{1}{2} \int_0^T \mathbb{I}(\mathbb{C}(t)) dt + \frac{1}{2} \int_0^T \mathbb{A}(\mathbb{C}(t), \Psi(t)) dt \ge 0 \qquad (2.28)
$$

with (**C**(t), **<sup>Ψ</sup>**(t)) <sup>∈</sup> **CE**<sup>T</sup> . Moreover, **<sup>J</sup>**(**C**) = 0 if and only if **<sup>C</sup>** solves [\(2.22\)](#page-13-0).

Proof. Let Θ be the disintegration of ¯ **C** from Proposition [2.19](#page-13-4) defined in [\(2.27\)](#page-14-1). The fact that <sup>√</sup> **I** is a strong upper gradient of **F** can be seen by integrating its defining inequality on the underlying level [\(2.17\)](#page-9-1) w.r.t. Θ¯

$$
|\mathbb{F}(\mathbb{C}(t_2)) - \mathbb{F}(\mathbb{C}(t_1))| \leq \int_{\mathrm{AC}([0,T];\mathcal{P}(\mathcal{X}))} |\mathcal{F}(c(t_2)) - \mathcal{F}(c(t_1))| \, \bar{\Theta}(dc)
$$
  
$$
\leq \int_{\mathrm{AC}([0,T];\mathcal{P}(\mathcal{X}))} \int_{t_1}^{t_2} \sqrt{\mathcal{I}(c(t))} \sqrt{\mathcal{A}(c(t), \psi(t))} \, dt \, \bar{\Theta}(dc).
$$

Then, using Jensen's inequality on the concave function (a, b) 7→ √ ab , we get the strong upper gradient property for <sup>√</sup> **I**.

The "if" part of the last claim is easily verified from the definition. Now, assume that **J**(**C**) = 0. Since **C** is absolutely continuous, we can apply Proposition [2.19](#page-13-4) and obtain the probabilistic representation Θ¯ ∈ P (AC([0, T] × P(<sup>X</sup> ))) [\(2.27\)](#page-14-1) such that **<sup>C</sup>**(t) = (et)#Θ. ¯ Then, [\(2.28\)](#page-16-0) can be obtained by just integrating <sup>J</sup> from [\(2.18\)](#page-10-0) along Θ and it holds ¯ <sup>J</sup> (c) = 0 for Θ-a.e. ¯ <sup>c</sup> <sup>∈</sup> AC([0, T],P(<sup>X</sup> )). These <sup>c</sup> are by Proposition [2.13](#page-10-1) solutions to [\(2.9\)](#page-6-3) and satisfy <sup>c</sup>(t) ∈ P<sup>∗</sup> (X ) for all t > 0. Then, we can conclude by the converse statement of Proposition [2.19](#page-13-4) that <sup>K</sup>(c(t))**Ψ**(t, c(t)) = −K(c(t))DF(c(t)), which implies since <sup>c</sup>(t) ∈ P<sup>∗</sup> (<sup>X</sup> ) for t > 0 up to a constant that **<sup>Ψ</sup>**(t, c(t)) = <sup>−</sup>DF(c(t)) and hence **<sup>C</sup>** solves [\(2.22\)](#page-13-0).

## <span id="page-17-0"></span>3. From weakly interacting particle systems to mean field systems

In this section, we will show how the gradient flow structure we described in the previous sections arises as the limit of gradient flow structures for N-particle systems with mean field interactions, in the limit N → ∞. Moreover, we show that the empirical distribution of the N-particle dynamics converges to a solution of the non-linear equation [\(1.1\)](#page-0-0).

Notation. For N an integer bold face letters are elements connected to the space X N and hence implicitly depending on <sup>N</sup>. Examples are vectors <sup>x</sup>, <sup>y</sup> ∈ X <sup>N</sup> , matrices <sup>Q</sup> <sup>∈</sup> R<sup>X</sup> <sup>N</sup> ×X <sup>N</sup> or measures µ ∈ P(X <sup>N</sup> ). For <sup>i</sup> ∈ {1, . . . , N} let <sup>e</sup> <sup>i</sup> be the placeholder for i-th particle, such that x · e <sup>i</sup> <sup>=</sup> <sup>x</sup><sup>i</sup> ∈ X is the position of the <sup>i</sup>-th particle. For <sup>x</sup> ∈ X <sup>N</sup> and y ∈ X we denote by x i;y the particle system obtained from x where the i-th particle jumped to site y

$$
\boldsymbol{x}^{i; y} := \boldsymbol{x} - (x_i - y)\boldsymbol{e}^i = (x_1, \dots, x_{i-1}, y, x_{i+1}, \dots, x_N).
$$

L <sup>N</sup> (x) will denote the empirical distribution for <sup>x</sup> ∈ X <sup>N</sup> , defined by

<span id="page-17-4"></span>
$$
L^{N}(\boldsymbol{x}) := \frac{1}{N} \sum_{i=1}^{N} \delta_{x_i}
$$
\n(3.1)

We introduce the discretized simplex P<sup>N</sup> (X ) ⊂ P(X ), given by

$$
\mathcal{P}_N(\mathcal{X}) := \left\{ L^N(\boldsymbol{x}) : \boldsymbol{x} \in \mathcal{X}^N \right\}.
$$

Let us introduce a natural class of mean-field dynamics for the N-particle system. We follow the standard procedure outlined in Remark [2.4.](#page-5-4)

In analog to Definition [2.3,](#page-5-0) we fix K : P(X ) × X → R such that for each x ∈ X , K<sup>x</sup> is a twice continuously differentiable function on P(X ) and set U(µ) := P <sup>x</sup>∈X µxKx(µ). For every natural number N define the probability measure π <sup>N</sup> for <sup>x</sup> ∈ X <sup>N</sup> by

<span id="page-17-2"></span><span id="page-17-1"></span>
$$
\boldsymbol{\pi}_{\boldsymbol{x}}^N := \frac{1}{\boldsymbol{Z}^N} \exp\left(-NU\left(L^N\boldsymbol{x}\right)\right),\tag{3.2}
$$

and Z<sup>N</sup> := P <sup>x</sup>∈X <sup>N</sup> exp −NU L <sup>N</sup> x is the partition sum. This shall be the invariant measure of the particle system and is already of mean-field form.

To introduce the dynamics, we use a family <sup>A</sup><sup>N</sup> (µ) <sup>∈</sup> <sup>R</sup>X ×X µ∈P<sup>N</sup> (X) of irreducible symmetric matrices and define the rate matrices <sup>Q</sup><sup>N</sup> (µ) <sup>∈</sup> <sup>R</sup>X ×X µ∈P<sup>N</sup> (X) for any x ∈ X <sup>N</sup> , y ∈ X , i ∈ {1, . . . N} by

$$
Q_{x_i,y}^N(L^N \boldsymbol{x}) := \sqrt{\frac{\pi_{\boldsymbol{x}^{i;y}}^N}{\pi_{\boldsymbol{x}}^N}} A_{x,y}^N(L^N \boldsymbol{x})
$$
  
= 
$$
\exp\left(-\frac{N}{2}\left(U(L^N \boldsymbol{x}^{i;y}) - U(L^N \boldsymbol{x})\right)\right) A_{x,y}^N(L^N \boldsymbol{x}).
$$
 (3.3)

Finally, the actual rates of the N-particle system are given in terms of the rate matrix

<span id="page-17-3"></span>
$$
\mathbf{Q}^N \in \mathbf{R}^{\mathcal{X}^N \times \mathcal{X}^N} : \qquad \mathbf{Q}_{\mathbf{x},\mathbf{x}^{i;y}}^N := Q_{x_i,y}^N(L^N(\mathbf{x})). \tag{3.4}
$$

By construction Q<sup>N</sup> is irreducible and reversible w.r.t. the unique invariant measure π N . Remark 3.1. The irreducible family of matrices A<sup>N</sup> (µ) µ∈P(X) encodes the underlying graph structure of admissible jumps and also the rates of the jumps. For instance, A<sup>N</sup> x,y(ν) = αx,y for any symmetric adjacency matrix α ∈ {0, 1} X ×X corresponds to Glauber dynamics on the corresponding graph. Another choice is A<sup>N</sup> x,y(L <sup>N</sup> x) := exp − N 2 <sup>U</sup>(<sup>L</sup> <sup>N</sup> <sup>x</sup>) <sup>−</sup> <sup>U</sup>(<sup>L</sup> <sup>N</sup> x i;y ) , which corresponds to Metropolis dynamics on the complete graph. In particular, all of these examples satisfy Assumption [1.](#page-18-0)

<span id="page-18-0"></span>Assumption 1 (Lipschitz assumptions on rates). There exists a family of irreducible symmetric matrices {A(µ)}µ∈P(X) such that µ 7→ A(µ) is Lipschitz continuous on P(X ) and the family A<sup>N</sup> (µ) µ∈P(X),N∈N of irreducible symmetric matrices satisfies

$$
\forall x, y \in \mathcal{X} : A_{x,y}^N \to A_{x,y} \quad on \mathcal{P}(\mathcal{X}) \text{ as } N \to \infty.
$$

<span id="page-18-2"></span>Lemma 3.2. Assume <sup>Q</sup><sup>N</sup> (µ) <sup>∈</sup> <sup>R</sup>X ×X µ∈P<sup>N</sup> (X) is given by [\(3.3\)](#page-17-1) with A<sup>N</sup> satisfying Assumption [1,](#page-18-0) then for all x, y ∈ X

<span id="page-18-1"></span>
$$
Q_{x,y}^N \to Q_{x,y} \qquad on \ \mathcal{P}(\mathcal{X}) \tag{3.5}
$$

with <sup>Q</sup>x,y(µ) = <sup>q</sup>πy(µ) <sup>π</sup>x(µ)Ax,y(µ) with π given in [\(2.3\)](#page-5-1). In particular, µ 7→ Qx,y(µ) is Lipschitz continuous on P(X ) for all x, y ∈ X .

Proof. By [\[6,](#page-35-17) Lemma 4.1] holds for <sup>x</sup> ∈ X <sup>N</sup> with <sup>µ</sup> <sup>=</sup> <sup>L</sup> <sup>N</sup> <sup>x</sup>, <sup>y</sup> ∈ X and <sup>i</sup> ∈ {1, . . . , N}

$$
\frac{\pi_{\boldsymbol{x}^{i;y}}^{N}}{\pi_{\boldsymbol{x}}^{N}} = N \left( U(L^{N} \boldsymbol{x}) - U(L^{N} \boldsymbol{x}^{i;y}) \right) = \partial_{\mu_{\boldsymbol{x}}} U(\mu) - \partial_{\mu_{\boldsymbol{y}}} U(\mu) + O(N^{-1})
$$
\n
$$
= \frac{\pi_{\boldsymbol{y}}(\mu)}{\pi_{\boldsymbol{x}}(\mu)} + O(N^{-1}),
$$

which shows by Assumption [1](#page-18-0) the convergence statement. The Lipschitz continuity follows, since A is assumed Lipschitz and the function µ 7→ ∂µxU(µ) = µx+ P <sup>y</sup> µy∂µxKy(µ) is continuously differentiable, since K is assumed twice continuously differentiable.

Remark 3.3. The mean-field behavior is manifested in the convergence statement [\(3.5\)](#page-18-1). The typical example we have in mind, as presented in Section 4 of [\[6\]](#page-35-17), is as follows: the mean-field model is described by

$$
K_x(\mu) := V(x) + \sum_y W(x, y)\mu_y
$$

where V is a potential energy and W an interaction energy between particles on sites x and y. For the N particle system, we can use a Metropolis dynamics, where possible jumps are those between configurations that differ by the position of a single particle, and reversible with respect to the measure

$$
\pi_{\bm{x}}^N = A^{-1} \exp(-U^N(\bm{x})); \quad U^N(\bm{x}) := \sum_{i=1}^N V(x_i) + \frac{1}{N} \sum_{i=1}^N \sum_{j=1}^N W(x_i, x_j).
$$

Note, the by the definition of the L <sup>N</sup> , we have the identity

$$
U^{N}(\boldsymbol{x}) = NU(L^{N}\boldsymbol{x}) \text{ with } U(\mu) = \sum_{x} \mu_{x} K_{x}(\mu),
$$

which makes it consistent with Definition [3.2.](#page-17-2) This is a typical class of mean-field spin systems from statistical mechanics.

In particular, the Curie-Weiss mean-field spin model for ferromagnetism is obtained by choosing X = {−, +}, V (−) = V (+) = W(−, −) = W(+, +) = 0 and W(−, +) = W(+, −) = β > 0. This is among the simplest models of statistical mechanics showing a phase transition in the free energy

$$
\mathcal{F}_{\beta}(\mu) := \sum_{\sigma \in \{-,+\}} (\log \mu_{\sigma} + K_{\sigma}(\mu)) \mu_{\sigma} = \mu_{-} \log \mu_{-} + \mu_{+} \log \mu_{+} + 2\beta\mu_{-}\mu_{+}
$$

at β = 1. For β ≤ 1 the free energy is convex whereas for β > 1 it is non-convex on P(X ). We will investigate this phase transition on the level of curvature for the mean-field system as well as for the finite particle system in future work.

3.1. Gradient flow structure of interacting N-particle systems. The N-particle dynamics on X <sup>N</sup> is now defined by the rate matrix Q<sup>N</sup> given as in [\(3.4\)](#page-17-3) with the generator

<span id="page-19-4"></span>
$$
\mathcal{L}^N f := \sum_{i=1}^N \sum_{y \in \mathcal{X}} (f(\boldsymbol{x}^{i; y}) - f(\boldsymbol{x})) \boldsymbol{Q}_{\boldsymbol{x}, \boldsymbol{x}^{i; y}}^N.
$$
 (3.6)

Likewise the evolution of an initial density µ<sup>0</sup> ∈ P(X <sup>N</sup> ) satisfies

<span id="page-19-1"></span>
$$
\dot{\mathbf{c}}(t) = \mathbf{c}(t)\mathbf{Q}^N. \tag{3.7}
$$

Since by construction the rate matrix Q<sup>N</sup> defined in [\(3.4\)](#page-17-3) satisfy the detailed balance condition w.r.t. π <sup>N</sup> [\(3.2\)](#page-17-2), this is the generator of a reversible Markov process w.r.t. π N on the finite space X <sup>N</sup> . Hence, we can use the framework developed in [\[31\]](#page-36-0) and [\[34\]](#page-36-1) to view this dynamics as a gradient flow of the relative entropy with respect to its invariant measure. Let us introduce the relevant quantities.

We define the relative entropy H(µ | π <sup>N</sup> ) for µ,π <sup>N</sup> ∈ P(<sup>X</sup> <sup>N</sup> ) by setting

$$
\mathcal{F}^N(\mu) := \mathcal{H}(\mu \mid \pi^N) = \sum_{\bm{x} \in \mathcal{X}^N} \mu_{\bm{x}} \log \frac{\mu_{\bm{x}}}{\pi_{\bm{x}}^N}.
$$

Furthermore we define the action of a pair µ ∈ P(X <sup>N</sup> ), <sup>ψ</sup> <sup>∈</sup> <sup>R</sup><sup>X</sup> <sup>N</sup> by

$$
\mathcal{A}^N(\mu, \psi) = \frac{1}{2} \sum_{x,y} (\psi_y - \psi_x)^2 w_{x,y}^N(\mu),
$$

where the weights w<sup>N</sup> x,y (µ) are defined like in [\(2.7\)](#page-6-4) as follows

<span id="page-19-3"></span>
$$
\boldsymbol{w}_{\boldsymbol{x},\boldsymbol{y}}^N(\boldsymbol{\mu}) := \Lambda\big(\boldsymbol{\mu}_{\boldsymbol{x}}\boldsymbol{Q}^N(\boldsymbol{x},\boldsymbol{y}),\boldsymbol{\mu}_{\boldsymbol{y}}\boldsymbol{Q}^N(\boldsymbol{y},\boldsymbol{x})\big).
$$
(3.8)

Then, a distance <sup>W</sup><sup>N</sup> on <sup>P</sup>(<sup>X</sup> <sup>N</sup> ) is given by

<span id="page-19-2"></span>
$$
\mathbf{W}^{N}(\boldsymbol{\mu},\boldsymbol{\nu})^{2} := \inf_{(\boldsymbol{c}(t),\boldsymbol{\psi}(t))} \int_{0}^{1} \boldsymbol{\mathcal{A}}^{N}(\boldsymbol{c}(t),\boldsymbol{\psi}(t))dt
$$
(3.9)

where the infimum runs over all pairs such that c is a path from µ to ν in P(X <sup>N</sup> ), and such that the continuity equation

<span id="page-19-0"></span>
$$
\dot{\mathbf{c}}_{\mathbf{x}}(t) + \sum_{\mathbf{y}} (\psi_{\mathbf{y}}(t) - \psi_{\mathbf{x}}(t)) \mathbf{w}_{\mathbf{x},\mathbf{y}}^N(\mathbf{c}(t)) = 0 \tag{3.10}
$$

holds. For details of the construction and the proof that this defines indeed a distance we refer to [\[31\]](#page-36-0). In particular, we note that for any absolutely continuous curve c : [0, T] → (P(X <sup>N</sup> ),W<sup>N</sup> ) there exist a function <sup>ψ</sup> : [0, T] <sup>→</sup> <sup>R</sup><sup>X</sup> <sup>N</sup> such that the continuity equation [\(3.10\)](#page-19-0) holds.

Finally, we define the N-particle Fisher information by

$$
\mathcal{I}^N(\mu) := \begin{cases} \frac{1}{2} \sum_{(\boldsymbol{x}, \boldsymbol{y}) \in E_{\boldsymbol{\mu}}} \boldsymbol{w}_{\boldsymbol{x}\boldsymbol{y}}^N(\mu) (\log(\mu_{\boldsymbol{x}} \boldsymbol{Q}_{\boldsymbol{x}\boldsymbol{y}}^N(\mu)) - \log(\mu_{\boldsymbol{y}} \boldsymbol{Q}_{\boldsymbol{y}\boldsymbol{x}}^N(\mu)))^2 & \mu \in \mathcal{P}^*(\mathcal{X}^N) \\ \infty. & \text{otherwise} \end{cases}
$$

We formulate the statement that [\(3.7\)](#page-19-1) is the gradient flow of F<sup>N</sup> w.r.t. W<sup>N</sup> again in terms of curves of maximal slope.

Proposition 3.4. For any absolutely continuous curve c : [0, T] → (P(X <sup>N</sup> ),W<sup>N</sup> ) the function J <sup>N</sup> given by

<span id="page-20-0"></span>
$$
\boldsymbol{\mathcal{J}}^N(\boldsymbol{c}) := \boldsymbol{\mathcal{F}}^N(\boldsymbol{c}(T)) - \boldsymbol{\mathcal{F}}^N(\boldsymbol{c}(0)) + \frac{1}{2} \int_0^T \boldsymbol{\mathcal{I}}^N(\boldsymbol{c}(t)) + \boldsymbol{\mathcal{A}}^N(\boldsymbol{c}(t), \boldsymbol{\psi}(t)) dt \qquad (3.11)
$$

is non-negative, where ψ<sup>t</sup> is such that the continuity equation [\(3.10\)](#page-19-0) holds. Moreover, a curve c is a solution to c˙(t) = c(t)Q<sup>N</sup> if and only if J <sup>N</sup> (c) = 0.

Proof. The proof is exactly the same as for Proposition [2.13,](#page-10-1) so we omit it.

3.2. Convergence of gradient flows. In this section we prove convergence of the empirical distribution of the N-particle system [\(3.7\)](#page-19-1) to a solution of the non-linear equation [\(1.1\)](#page-0-0). This will be done by using the gradient flow structure exibited in the previous sections together with the techniques developed in [\[40\]](#page-36-8) on convergence of gradient flows.

Heuristiclly, consider a sequence of gradient flows associated to a senquence of metric spaces and engergy functionals. Then to prove convergence of the flows it is sufficient to establish convergence of the metrics and the energy functionals in the sense that functionals of the type [\(3.11\)](#page-20-0) satisfy a suitable notion of Γ − lim inf estimate.

In the following Theorem [3.6](#page-20-1) we adapt the result in [\[40\]](#page-36-8) to our setting.

We consider the sequence of metric spaces S <sup>N</sup> := (P(<sup>X</sup> <sup>N</sup> ),W<sup>N</sup> ) with W<sup>N</sup> defined in [\(3.9\)](#page-19-2) and the limiting metric space **<sup>S</sup>** := (P(P(<sup>X</sup> )), **<sup>W</sup>**) with **<sup>W</sup>** defined in [\(2.24\)](#page-13-2). The following notion of convergence will provide the correct topology in our setting.

<span id="page-20-3"></span>Definition 3.5 (Convergence of random measures). A sequence µ <sup>N</sup> ∈ P(<sup>X</sup> <sup>N</sup> ) converges in <sup>τ</sup> topology to a point **<sup>M</sup>** ∈ P(P(<sup>X</sup> )) if and only if <sup>L</sup> N #(µ <sup>N</sup> ) ∈ P(P(<sup>X</sup> )) converges in distribution to **M**, where L <sup>N</sup> : <sup>X</sup> <sup>N</sup> → P(<sup>X</sup> ) is defined in [\(3.1\)](#page-17-4). Likewise, for c <sup>N</sup> (t) t∈[0,T] with c N <sup>t</sup> ∈ P(X <sup>N</sup> ): c <sup>N</sup> <sup>τ</sup><sup>→</sup> **<sup>C</sup>** if for all <sup>t</sup> <sup>∈</sup> [0, T], <sup>L</sup> N #c <sup>N</sup> (t) ⇀ **C**(t).

<span id="page-20-1"></span>Theorem 3.6 (Convergence of gradient flows `a la [\[40\]](#page-36-8)). Assume there exists a topology τ such that whenever a sequence c <sup>N</sup> <sup>∈</sup> AC([0, T],<sup>S</sup> <sup>N</sup> ) converges pointwise w.r.t. τ to a limit **<sup>C</sup>** <sup>∈</sup> AC([0, T], **<sup>S</sup>**), then this convergence is compatible with the energy functionals, that is

<span id="page-20-2"></span>
$$
\mathbf{c}^N \stackrel{\tau}{\to} \mathbb{C} \qquad \Rightarrow \qquad \liminf_{N \to \infty} \frac{1}{N} \mathcal{F}^N(\mathbf{c}^N(T)) \ge \mathbb{F}(\mathbb{C}(T)) - \mathcal{F}_0, \tag{3.12}
$$

for some finite constant F<sup>0</sup> ∈ R. In addition, assume the following holds

(1) lim inf-estimate of metric derivatives:

<span id="page-21-0"></span>
$$
\liminf_{N \to \infty} \frac{1}{N} \int_0^T \mathcal{A}^N(\mathbf{c}^N(t), \boldsymbol{\psi}^N(t)) dt \ge \int_0^T \mathbb{A}(\mathbb{C}(t), \Psi(t)) dt,
$$
\n(3.13)

where (c <sup>N</sup> , ψ<sup>N</sup> ) and (**C**(t), **Ψ**(t)) are related via the respective continuity equations in S <sup>N</sup> and **S**.

(2) lim inf-estimate of the slopes pointwise in t ∈ [0, T]:

<span id="page-21-1"></span>
$$
\liminf_{N \to \infty} \frac{1}{N} \mathcal{I}^N(c^N(t)) \ge \mathbb{I}(\mathbb{C}(t)).
$$
\n(3.14)

Let c <sup>N</sup> be a curve of maximal slope on (0, T) for J <sup>N</sup> [\(3.11\)](#page-20-0) such that c <sup>N</sup> (0) <sup>τ</sup><sup>→</sup> **<sup>C</sup>**(0) which is well-prepared in the sense that limN→∞ F<sup>N</sup> (c <sup>N</sup> (0)) = **F**(**C**(0)). Then **C** is a curve of maximal slope for **J** [\(2.28\)](#page-16-0) and

$$
\forall t \in [0, T), \quad \lim_{N \to \infty} \frac{1}{N} \mathcal{F}^N(\mathbf{c}^N(t)) = \mathbb{F}(\mathbb{C}(t))
$$
$$
\frac{1}{N} \mathcal{A}^N(\mathbf{c}^N, \psi^N) \to \mathbb{A}(\mathbb{C}, \Psi) \quad in \quad L^2[0, T]
$$
$$
\frac{1}{N} \mathcal{I}^N(\mathbf{c}^N) \to \mathbb{I}(\mathbb{C}) \quad in \quad L^2[0, T]
$$

Proof. Let us sketch the proof. The assumptions [\(3.12\)](#page-20-2), [\(3.13\)](#page-21-0), [\(3.14\)](#page-21-1) and the wellpreparedness of the initial data allow to pass in the limit in the individual terms of 1 <sup>N</sup> J <sup>N</sup> [\(3.11\)](#page-20-0) to obtain

$$
\liminf_{N\to\infty}\frac{1}{N}\boldsymbol{\mathcal{J}}^N(\boldsymbol{c}^N)\geq \mathbb{J}(\mathbb{C}).
$$

Hence, if each c <sup>N</sup> is a curve of maximal slope w.r.t. <sup>1</sup> <sup>N</sup> J <sup>N</sup> (c <sup>N</sup> ) then so is **C** w.r.t. **J**. The other statements also can be directly adapted from [\[40\]](#page-36-8).

3.3. Application. To apply Theorem [3.6,](#page-20-1) we first have to show the convergence of the energy [\(3.12\)](#page-20-2).

<span id="page-21-2"></span>Proposition 3.7 (lim inf inequality for the relative entropy). Let a sequence µ <sup>N</sup> <sup>∈</sup> <sup>P</sup>(<sup>X</sup> <sup>N</sup> ) be given such that <sup>µ</sup> <sup>N</sup> <sup>τ</sup><sup>→</sup> **<sup>M</sup>** as <sup>N</sup> → ∞, then

$$
\liminf_{N\to\infty}\frac{1}{N}\mathcal{H}(\boldsymbol{\mu}^N\mid \boldsymbol{\pi}^N)\geq \int_{\mathcal{P}(\mathcal{X})}(\mathcal{F}(\nu)-\mathcal{F}_0)\; \mathbb{M}(d\nu)=\mathbb{F}(\mathbb{M})-\mathcal{F}_0,
$$

where

$$
\mathcal{F}_0 := \inf_{\mu \in \mathcal{P}(\mathcal{X})} \mathcal{F}(\mu).
$$

Proof. First we note that the relative entropy can be decomposed as follows:

$$
\mathcal{H}(\boldsymbol{\mu}^N \mid \boldsymbol{\pi}^N) = \int \mathcal{H}(\boldsymbol{\mu}^N( \cdot \mid L^N = \nu) \mid \boldsymbol{\pi}^N( \cdot \mid L^N = \nu)) dL_{\#}^N \boldsymbol{\mu}^N(\nu) + \mathcal{H}(L_{\#}^N \boldsymbol{\mu}^N \mid L_{\#}^N \boldsymbol{\pi}^N)
$$

Let us denote by <sup>M</sup><sup>N</sup> the uniform probability measure on <sup>P</sup><sup>N</sup> (<sup>X</sup> ). Using the fact that relative entropy w.r.t. a probability measure is non-negative we arrive a the estimate

$$
\mathcal{H}(\boldsymbol{\mu}^{N} \mid \boldsymbol{\pi}^{N}) \geq \mathcal{H}(L_{\#}^{N} \boldsymbol{\mu}^{N} \mid L_{\#}^{N} \boldsymbol{\pi}^{N})
$$
\n
$$
= \mathcal{H}(L_{\#}^{N} \boldsymbol{\mu}^{N} \mid \boldsymbol{M}^{N}) + \mathbf{E}_{L_{\#}^{N} \boldsymbol{\mu}^{N}} \left[ \log \frac{d\boldsymbol{M}^{N}}{dL_{\#}^{N} \boldsymbol{\pi}^{N}} \right]
$$
\n
$$
\geq \mathbf{E}_{L_{\#}^{N} \boldsymbol{\mu}^{N}} \left[ \log \frac{d\boldsymbol{M}^{N}}{dL_{\#}^{N} \boldsymbol{\pi}^{N}} \right].
$$
\n(3.15)

For ν ∈ P<sup>N</sup> (X ) we set T<sup>N</sup> (ν) = <sup>x</sup> ∈ X <sup>N</sup> : <sup>L</sup> <sup>N</sup> (x) = ν . Then by the definition of π <sup>N</sup> [\(3.2\)](#page-17-2) and U(ν) [\(2.6\)](#page-6-1) we have

<span id="page-22-0"></span>
$$
L_{\#}^N \pi^N(\nu) = \frac{|\mathcal{T}_N(\nu)|}{\mathbf{Z}^N} \exp\big(-NU(\nu)\big) .
$$

From [\(3.15\)](#page-22-0) we thus conclude

$$
\frac{1}{N} \mathcal{H}(\boldsymbol{\mu}^{N} \mid \boldsymbol{\pi}^{N}) \geq -\frac{1}{N} \log |\mathcal{P}_{N}(\mathcal{X})| + \frac{1}{N} \log \mathbf{Z}^{N} \n- \frac{1}{N} \mathbb{E}_{L_{\#}^{N} \boldsymbol{\mu}^{N}} \big[ \log |\mathcal{T}_{N}| \big] + \mathbb{E}_{L_{\#}^{N} \boldsymbol{\mu}^{N}} [U] .
$$
\n(3.16)

The cardinality of <sup>P</sup><sup>N</sup> (<sup>X</sup> ) is given by N+d−<sup>1</sup> N <sup>≤</sup> <sup>N</sup>d−1/d! and hence

<span id="page-22-2"></span><span id="page-22-1"></span>
$$
\log |\mathcal{P}_N(\mathcal{X})| \le (d-1)\log N. \tag{3.17}
$$

Moreover, by Stirling's formula (cf. Lemma [A.1\)](#page-33-1), it follows that for any ν ∈ P<sup>N</sup> (X )

$$
-\frac{1}{N}\log|\mathcal{T}_N(\nu)| = -\frac{1}{N}\log\frac{N!}{\prod_{x\in\mathcal{X}}(N\nu(x))!}
$$
$$
=\sum_{x\in\mathcal{X}}\nu(x)\log\nu(x) + O\left(\frac{\log N}{N}\right) . \tag{3.18}
$$

Furthermore, we have

$$
\mathbf{Z}^N = \sum_{\nu \in \mathcal{P}_N(\mathcal{X})} e^{-NU(\nu)} |\mathcal{T}_N(\nu)|.
$$

Hence, by using Sanov's and Varadhan's theorem [\[20\]](#page-35-19) on the asymptotic evaluation of exponential integrals, it easily follows that

$$
\lim_{N \to \infty} \frac{1}{N} \log \mathbf{Z}^N = - \inf_{\nu \in \mathcal{P}(\mathcal{X})} \mathcal{F}(\nu) =: -\mathcal{F}_0.
$$
\n(3.19)

Combing now [\(3.16\)](#page-22-1) with [\(3.17\)](#page-22-2)-[\(3.19\)](#page-22-3) finishes the proof.

The other ingredient of the proof of Theorem [3.6](#page-20-1) consists in proving the convergence of the metric derivatives [\(3.13\)](#page-21-0) and slopes [\(3.14\)](#page-21-1).

<span id="page-22-4"></span>Proposition 3.8 (Convergence of metric derivative and slopes). Let c <sup>N</sup> be an element of AC([0, T],P(X <sup>N</sup> )), and choose <sup>ψ</sup><sup>N</sup> : [0, T] → P(<sup>X</sup> <sup>N</sup> ) such that (c <sup>N</sup> , ψ<sup>N</sup> ) solves the continuity equation. Furthermore, assume that

<span id="page-22-3"></span>
$$
\boldsymbol{c}^N \overset{\tau}{\to} \mathbb{C},
$$

with some measurable **<sup>C</sup>** : [0, T] → P(P(<sup>X</sup> )), and that

$$
\liminf_{N\to\infty}\int_0^T\frac{1}{N}\mathcal{A}^N(\mathbf{c}^N(t),\psi^N(t))dt<\infty.
$$

Then **<sup>C</sup>** <sup>∈</sup> AC ([0, T],P(P(<sup>X</sup> ))), and there exists **<sup>Ψ</sup>** : [0, T] → P(P(<sup>X</sup> )), for which (**C**, **<sup>Ψ</sup>**) satisfy the continuity equation and for which we have

$$
\liminf_{N \to \infty} \int_0^T \frac{1}{N} \mathcal{A}^N(\mathbf{c}^N(t), \mathbf{\psi}^N(t)) dt \ge \int_0^T \mathbb{A}(\mathbb{C}(t), \Psi(t)) dt
$$

and

$$
\liminf_{N \to \infty} \int_0^T \frac{1}{N} \mathcal{I}^N\left(\mathbf{c}^N(t)\right) dt \ge \int_0^T \mathbb{I}\left(\mathbb{C}(t)\right) dt.
$$

Proof. Let us summarize consequences of the assumption c <sup>N</sup> <sup>τ</sup><sup>→</sup> **<sup>C</sup>**. By Definition [3.5,](#page-20-3) this means L N #c <sup>N</sup> (t) ⇀ **<sup>C</sup>**(t) for all <sup>t</sup> <sup>∈</sup> [0, T]. For x, y ∈ X we define two auxiliary measures **Γ** <sup>N</sup>;x,y;1(t), **Γ** <sup>N</sup>;x,y;2(t) ∈ P P(X ) × P(X ) by setting

$$
\mathbb{\Gamma}^{N;x,y;1}(t,\nu,\mu) := \delta_{\nu^{N;x,y}}(\mu)\nu_x Q_{xy}^N(\nu) L_{\#}^N \mathbf{c}^N(t,\nu) \n\mathbb{\Gamma}^{N;x,y;2}(t,\nu,\mu) := \delta_{\mu^{N;y,x}}(\nu)\mu_y Q_{yx}^N(\mu) L_{\#}^N \mathbf{c}^N(t,\mu),
$$

where ν <sup>N</sup>;x,y := <sup>ν</sup> <sup>−</sup> δx−δy N . Then, we have **Γ** <sup>N</sup>;x,y;1(t, ν, µ) = **Γ** <sup>N</sup>;y,x;2(t, µ, ν). Due to [\(3.5\)](#page-18-1) from Lemma [3.2](#page-18-2) it holds

<span id="page-23-1"></span><span id="page-23-0"></span>
$$
\mathbb{\Gamma}^{N;x,y;1}(t,\nu,\mu) \rightharpoonup \delta_{\nu}(\mu)\nu_x Q_{xy}(\nu)\mathbb{C}(t,\nu) \tag{3.20}
$$

$$
\mathbb{\Gamma}^{N;x,y;2}(t,\nu,\mu) \rightharpoonup \delta_{\mu}(\nu)\mu_x Q_{xy}(\mu)\mathbb{C}(t,\mu). \tag{3.21}
$$

In the sequel, we will decompose the sum over all possible jumps of the particle system in different ways

$$
\sum_{\boldsymbol{x},\boldsymbol{y}}f(\boldsymbol{x},\boldsymbol{y})=\sum_{\substack{\nu,\mu\in\mathcal{P}_N(\mathcal{X})}}\sum_{\substack{\boldsymbol{x}:\mathit{L}^N\boldsymbol{x}=\nu\\ \boldsymbol{y}:\mathit{L}^N\boldsymbol{y}=\mu}}f(\boldsymbol{x},\boldsymbol{y})=\sum_{\substack{x,y\in\mathcal{X}\\ \nu\in\mathcal{P}_N(\mathcal{X})}}\sum_{i=1}^N\sum_{\substack{\boldsymbol{x}:\mathit{L}^N\boldsymbol{x}=\nu\\ x_i=\boldsymbol{x}}}f(\boldsymbol{x},\boldsymbol{x}^{i;y}).
$$

where x <sup>i</sup>;<sup>y</sup> <sup>=</sup> <sup>x</sup> <sup>−</sup> (x<sup>i</sup> <sup>−</sup> <sup>y</sup>)<sup>e</sup> <sup>i</sup> and <sup>f</sup> : <sup>X</sup> <sup>N</sup> × X <sup>N</sup> <sup>→</sup> <sup>R</sup> with <sup>f</sup>(x, <sup>y</sup>) = 0 unless <sup>y</sup> <sup>=</sup> <sup>x</sup> i;y for some i ∈ {1, . . . , N} and y ∈ X . We define the following vector field on P(X ) × P(X )

$$
\mathbf{v}^{N;x,y}(t,\nu,\mu) := \frac{1}{2N} \delta_{\nu^{N;x,y}}(\mu) \sum_{\substack{\boldsymbol{x}:L^N\boldsymbol{x}=\nu \\ \boldsymbol{y}:L^N\boldsymbol{y}=\mu}} \left( \boldsymbol{\psi}_{\boldsymbol{y}}^N(t) - \boldsymbol{\psi}_{\boldsymbol{x}}^N(t) \right) \boldsymbol{w}_{\boldsymbol{x}\boldsymbol{y}}^N \left( \boldsymbol{c}^N(t) \right) = \frac{1}{2N} \delta_{\nu^{N;x,y}}(\mu) \sum_{i=1}^N \sum_{\substack{\boldsymbol{x}:L^N\boldsymbol{x}=\nu \\ \boldsymbol{x}:=\boldsymbol{x}}} \left( \boldsymbol{\psi}_{\boldsymbol{x}^{i;y}}^N(t) - \boldsymbol{\psi}_{\boldsymbol{x}}^N(t) \right) \boldsymbol{w}_{\boldsymbol{x}\boldsymbol{x}^{i;y}}^N \left( \boldsymbol{c}^N(t) \right),
$$

where w<sup>N</sup> xy c <sup>N</sup> (t) is defined in [\(3.8\)](#page-19-3). From the definition of **v** <sup>N</sup>;x,y(t) and the Cauchy-Schwarz inequality, it follows that for ν, µ ∈ P(X ) with µ = ν <sup>N</sup>;x,y for some x, y ∈ X

$$
\left|\mathbf{v}^{N;x,y}(t,\nu,\mu)\right| \leq \left(\frac{1}{2N} \sum_{\substack{\boldsymbol{x}:L^N\boldsymbol{x}=\nu\\ \boldsymbol{y}:L^N\boldsymbol{y}=\mu}} \left(\boldsymbol{\psi}_{\boldsymbol{y}}^N(t)-\boldsymbol{\psi}_{\boldsymbol{x}}^N(t)\right)^2 \boldsymbol{w}_{\boldsymbol{x}\boldsymbol{y}}^N\left(\boldsymbol{c}^N(t)\right)\right)^{\frac{1}{2}} \times \\ \left(\frac{1}{2N} \sum_{i=1}^N \sum_{\substack{\boldsymbol{x}:L^N\boldsymbol{x}=\nu\\ \boldsymbol{x}_i=\boldsymbol{x}}} \boldsymbol{w}_{\boldsymbol{x}\boldsymbol{x}^{i;y}}^N\left(\boldsymbol{c}^N(t)\right)\right)^{\frac{1}{2}}.
$$

By using the identity

$$
\frac{1}{N}\sum_{i=1}^N \sum_{\substack{\bm{x}:L^N(\bm{x})=\nu \\ x_i=x}} c_{\bm{x}}^N(t) = \sum_{\bm{x}} \delta_{\nu}(L^N(\bm{x})) \ L_x^N(\bm{x}) \ c_{\bm{x}}^N(t) = L_{\#}^N c^N(t,\nu) \ \nu_x,
$$

and the fact that the logarithmic mean is jointly concave and 1-homogeneous, we can conclude

$$
\frac{1}{N}\sum_{i=1}^N\sum_{\substack{\boldsymbol x: L^N\boldsymbol x=\nu\\ x_i=x}}\boldsymbol w_{\boldsymbol x\boldsymbol x^{i;y}}^N\left(\boldsymbol c^N(t)\right)\leq \Lambda\big(\mathbb \Gamma^{N;x,y;1}(t,\nu,\nu^{N;x,y}),\mathbb \Gamma^{N;x,y;2}(t,\nu,\nu^{N;x,y})\big)\,,
$$

which first shows that **v** <sup>N</sup>;x,y(t) <sup>≪</sup> <sup>Λ</sup> **Γ** <sup>N</sup>;x,y;1(t), **Γ** <sup>N</sup>;x,y;2(t) as product measure on P(X ) × P(X ). Moreover, by summation and integration over any Borel I ⊂ [0, T] we get

<span id="page-24-0"></span>
$$
\int_{I} \sum_{\nu,\mu \in \mathcal{P}_N(\mathcal{X})} \left| \mathbf{v}^{N;x,y}(t,\nu,\mu) \right| \, dt \leq \left( \sqrt{T} \int_0^T \frac{1}{N} \mathcal{A}(\mathbf{c}^N(t),\psi(t)) \, dt \right)^{\frac{1}{2}} \times \qquad (3.22)
$$
\n
$$
\left( \frac{|I|}{2} \sum_{\nu,\mu \in \mathcal{P}_N(\mathcal{X})} \sup_{t \in I} \Lambda\big( \mathbb{F}^{N;x,y;1}(t,\nu,\mu),\mathbb{F}^{N;x,y;2}(t,\nu,\mu) \big) \right)^{\frac{1}{2}}.
$$

The second sum is uniformly bounded in <sup>N</sup>, since <sup>X</sup> is finite and by Lemma [3.2](#page-18-2) <sup>Q</sup><sup>N</sup> <sup>→</sup> <sup>Q</sup> uniformly with Q continuous in the first argument on the compact space P(X ). Now, from [\(3.22\)](#page-24-0), we conclude that for some subsequence and all x, y ∈ X we have **<sup>v</sup>** <sup>N</sup>;x,y ⇀ **v** x,y with **v** x,y a Borel measure on [0, T]×P(<sup>X</sup> )×P(<sup>X</sup> ). Using Jensen's inequality applied

to the 1-homogeneous jointly convex function <sup>R</sup> <sup>×</sup> <sup>R</sup><sup>2</sup> <sup>+</sup> <sup>∋</sup> (v, a, b) 7→ <sup>v</sup> 2 Λ(a,b) , we get

$$
\int_{0}^{T} \frac{1}{N} \mathcal{A} (c^{N}(t), \psi^{N}(t)) dt \n= \int_{0}^{T} \frac{1}{2} \sum_{x,y} \sum_{\nu \in \mathcal{P}_{N}(\mathcal{X})} \frac{1}{N} \sum_{i=1}^{N} \sum_{x:L^{N}x = \nu} \frac{\left( (\psi_{x^{i,y}}^{N}(t) - \psi_{x}^{N}(t)) w_{xx^{i,y}}^{N}(c^{N}(t)) \right)^{2}}{w_{xx^{i,y}}^{N}(c^{N}(t))} dt \n\ge \int_{0}^{T} \frac{1}{2} \sum_{x,y} \sum_{\nu \in \mathcal{P}_{N}(\mathcal{X})} \frac{\left( v^{N}(t, \nu, \nu^{N;x,y}) \right)^{2}}{\Lambda(\Gamma^{N;x,y;1}(t, \nu, \nu^{N;x,y}), \Gamma^{N;x,y;2}(t, \nu, \nu^{N;x,y}))} dt.
$$

The last term can be written as

$$
\frac{1}{2} \sum_{x,y} F(\mathbf{v}^{N;x,y}, \mathbb{F}^{N;x,y;1}, \mathbb{F}^{N;x,y;2}),
$$

where the functional F on triples of measure on [0, T] × P(X ) 2 is defined via

$$
F(\mathbf{v}, \mathbb{T}^1, \mathbb{T}^2) := \int_0^T \iint_{\mathcal{P}(\mathcal{X})^2} \alpha\left(\frac{d\mathbf{v}}{d\sigma}, \Lambda\left(\frac{d\mathbb{T}^1}{d\sigma}, \frac{d\mathbb{T}^2}{d\sigma}\right)\right) d\sigma dt,
$$

with α the function defined in [\(2.13\)](#page-7-1) and σ is any measure on [0, T] × P(X ) 2 such that **v**, **Γ** 1 , **Γ** <sup>2</sup> <sup>≪</sup> <sup>σ</sup>. The definition does not depend on the choice of <sup>σ</sup> by the 1-homogeneity of α and Λ. Then, by a general result on lower semicontinuity of integral functionals [\[8,](#page-35-20) Thm. 3.4.3] we can conclude, that

$$
\liminf_{N \to \infty} F(\mathbf{v}^{N;x,y}, \mathbb{F}^{N;x,y;1}, \mathbb{F}^{N;x,y;2}) \ge F(\mathbf{v}^{x,y}, \mathbb{F}^{x,y;1}, \mathbb{F}^{x,y;2}).
$$

In particular, this implies

$$
d\mathbf{v}^{x,y} \ll \Lambda\left(\frac{d\mathbb{T}^{x,y;1}}{d\sigma}, \frac{d\mathbb{T}^{x,y;2}}{d\sigma}\right)d\sigma,
$$

which by [\(3.20\)](#page-23-0) and [\(3.21\)](#page-23-1) is given in terms of

$$
\Lambda\bigg(\frac{d\mathbb{E}^{x,y;1}}{d\sigma}(t,\nu,\mu),\frac{d\mathbb{E}^{x,y;2}}{d\sigma}(t,\nu,\mu)\bigg)\,d\sigma = \delta_{\nu}(\mu)\Lambda(\nu_x Q_{xy}(\nu),\nu_y Q_{yx}(\nu))\,\mathbb{C}(t,d\nu)dt.
$$

Therefore, with the notation of Proposition [2.17,](#page-13-5) we obtain the statement

$$
\liminf_{N \to \infty} \int_0^T \frac{1}{N} \mathcal{A} \left( \mathbf{c}^N(t), \psi(t)^N \right) dt
$$
\n
$$
\geq \frac{1}{2} \sum_{x,y} \int_0^T \int_{\mathcal{P}(\mathcal{X})} \frac{(\mathbb{V}_{xy}(t,\nu))^2}{\Lambda(\nu_x Q_{xy}(\nu), \nu_y Q_{yx}(\nu))} \mathbb{C}(t, d\nu) dt
$$
\n
$$
= \int_0^T \vec{\mathbb{A}}(\mathbb{C}(t), \mathbb{V}(t)) dt \quad \text{with} \quad \mathbb{V}_{xy}(t, \nu) := \frac{d\mathbb{V}^{x,y}}{d\mathbb{C}(t)dt}.
$$

From the convergence of the vector field **v** <sup>N</sup>;x,y ⇀ **v** x,y it is straightforward to check that (**C**, **<sup>V</sup>**) <sup>∈</sup> **CE**<sup>~</sup> <sup>T</sup> (**C**0,**C**<sup>T</sup> ) and hence by the conclusion of Proposition [2.17,](#page-13-5) there exists **<sup>Ψ</sup>** : [0, T] × P(<sup>X</sup> ) <sup>→</sup> <sup>R</sup><sup>X</sup> such that

$$
\liminf_{N \to \infty} \frac{1}{N} \int_0^T \mathcal{A} \left( \mathbf{c}^N(t), \boldsymbol{\psi}^N(t) \right) dt \ge \int_0^T \vec{\mathbb{A}}(\mathbb{C}(t), \mathbb{V}(t)) dt \ge \int_0^T \mathbb{A}(\mathbb{C}(t), \Psi(t)) dt,
$$

which concludes the first part.

The lim inf estimate of the Fisher information follows by a similar but simpler argument. The convex 1-homogeneous function λ(a, b) = (a − b) (log a − log b) allows to rewrite

$$
\frac{1}{N} \mathcal{I}^{N}\left(\mathbf{c}^{N}(t)\right) dt
$$
\n
$$
= \frac{1}{2} \sum_{x,y} \sum_{\nu \in \mathcal{P}_{N}(\mathcal{X})} \frac{1}{N} \sum_{i=1}^{N} \sum_{\substack{x:L^{N}x = \nu \\ x_{i} = x}} \lambda\left(\mathbf{c}_{\mathbf{x}}^{N}(t) \mathbf{Q}_{\mathbf{x}}^{N}(t) \mathbf{c}_{\mathbf{x}}^{N}(t)\right), \mathbf{c}_{\mathbf{x}}^{N}(t) \mathbf{Q}_{\mathbf{x}}^{N}(t) \mathbf{Q}_{\mathbf{x}}^{N}(t) \mathbf{c}_{\mathbf{x}}^{N}(t) \mathbf{d}_{\mathbf{x}}^{N}(t) \mathbf{d}_{\mathbf{x}}^{N}(t) \mathbf{d}_{\mathbf{x}}^{N}(t) \mathbf{d}_{\mathbf{x}}^{N}(t) \mathbf{d}_{\mathbf{x}}^{N}(t) \mathbf{d}_{\mathbf{x}}^{N}(t) \mathbf{d}_{\mathbf{x}}^{N}(t) \mathbf{d}_{\mathbf{x}}^{N}(t) \mathbf{d}_{\mathbf{x}}^{N}(t) \mathbf{d}_{\mathbf{x}}^{N}(t) \mathbf{d}_{\mathbf{x}}^{N}(t) \mathbf{d}_{\mathbf{x}}^{N}(t) \mathbf{d}_{\mathbf{x}}^{N}(t) \mathbf{d}_{\mathbf{x}}^{N}(t) \mathbf{d}_{\mathbf{x}}^{N}(t) \mathbf{d}_{\mathbf{x}}^{N}(t) \mathbf{d}_{\mathbf{x}}^{N}(t) \mathbf{d}_{\mathbf{x}}^{N}(t) \mathbf{d}_{\mathbf{x}}^{N}(t) \mathbf{d}_{\mathbf{x}}^{N}(t) \mathbf{d}_{\mathbf{x}}^{N}(t) \mathbf{d}_{\mathbf{x}}^{N}(t) \mathbf{d}_{\mathbf{x}}^{N}(t) \mathbf{d}_{\mathbf{x}}^{N}(t) \mathbf{d}_{\mathbf{x}}^{N}(t) \mathbf{d}_{\mathbf{x}}^{N}(t) \mathbf{d}_{\mathbf{x}}^{N}(t) \mathbf{d}_{\mathbf{x}}^{N}(t) \mathbf{d}_{\mathbf{x}}^{N}(t) \mathbf{d}_{\mathbf{x}}^{N}(t) \mathbf{d}_{\mathbf{x}}^{N}(t) \mathbf{d}_{\mathbf{x}}^{N}(t) \mathbf{d}_{\mathbf{x}}^{N
$$

Then, the result follows by an application of [\[8,](#page-35-20) Thm. 3.4.3].

In order to apply Theorem [3.6,](#page-20-1) we still need to prove that a sequence of N-particle dynamics starting from nice initial conditions is tight.

<span id="page-26-1"></span>Lemma 3.9. Let X<sup>N</sup> be the continuous Markov jump process with generator [\(3.6\)](#page-19-4), then the sequence of laws of empirical measures is tight in the Skorokhod topology, i.e. it holds for any x ∈ X and ε > 0

<span id="page-26-0"></span>
$$
\lim_{\delta \to 0} \limsup_{N \to \infty} \mathbb{P}\left[\sup_{|t-s| \le \delta} \left| L_x^N(\mathbf{X}^N(t)) - L_x^N(\mathbf{X}^N(s)) \right| > \epsilon \right] = 0. \tag{3.23}
$$

The proof follows standard arguments for tightness of empirical measures of sequences of interacting particle systems. Since there is no original argument here, the exposition shall be brief, and we refer to [\[29\]](#page-36-18) for more details, in a more general context of interacting particle systems. For example, see the first step in the proof of Theorem 2.1 in [\[29\]](#page-36-18) for those arguments in the context of the simple exclusion process on a discrete torus.

Proof. The process

$$
M_x^N(t) = L_x^N(\mathbf{X}^N(t)) - L_x^N(\mathbf{X}^N(0))
$$
  
 
$$
- \int_0^t \sum_{y \neq x} L_x^N(\mathbf{X}^N(s)) Q_{xy}^N(L^N(\mathbf{X}^N(s))) - L_y^N(\mathbf{X}^N(s)) Q_{yx}^N(L^N(\mathbf{X}^N(s))) ds
$$

is a martingale. Since the rates are bounded,

$$
\left| \int_s^t \sum_{y \neq x} L_x^N(\mathbf{X}^N(r)) Q_{xy}^N(L^N(\mathbf{X}^N(r))) - L_y^N(\mathbf{X}^N(r)) Q_{yx}^N(L^N(\mathbf{X}^N(r))) \, dr \right| \leq C|t-s|
$$

and therefore, to prove [\(3.23\)](#page-26-0), it is enough to show that

$$
\mathbb{P}\left[\sup_{|t-s|\leq \delta} \left| M_x^N(t) - M_x^N(s) \right| > \epsilon \right]
$$

is small. To do so, we shall estimate the quadratic variation of the martingale. It is given by

$$
\langle M^{N}\rangle(t) = \frac{1}{N^{2}} \sum_{y \neq x} ((NL_{x}^{N}(\mathbf{X}^{N}(t)) - 1)^{2} - (NL_{x}^{N}(\mathbf{X}^{N}(t)))^{2}) Q_{xy}^{N}(L^{N}(\mathbf{X}^{N}(s))) +
$$
  
$$
((NL_{x}^{N}(\mathbf{X}^{N}(t)) + 1)^{2} - (NL_{x}^{N}(\mathbf{X}^{N}(t))^{2}) Q_{yx}^{N}(L^{N}(\mathbf{X}^{N}(s))) +
$$
  
$$
\frac{2}{N^{2}} \sum_{y \neq x} NL_{x}^{N}(\mathbf{X}^{N}(t)) (L_{x}^{N}(\mathbf{X}^{N}(s)) Q_{xy}^{N}(L^{N}(\mathbf{X}^{N}(s))) - L_{y}^{N}(\mathbf{X}^{N}(s)) Q_{yx}^{N}(L^{N}(\mathbf{X}^{N}(s))) ).
$$

Using the boundedness of the rates, it is straightforward to see that

$$
|\langle M^N \rangle(t)| \leq C N^{-1}.
$$

The quadratic variation of the martingale vanishes. From Doob's martingale inequality, we deduce that for any ǫ > 0

$$
\mathbb{P}\left[\sup_{0\leq s\leq t\leq T}|M_x^N(t)-M_x^N(s)|>\epsilon\right]\longrightarrow 0.
$$

Tightness of the sequence of processes follows.

We can now combine the work done so far to obtain our main result.

<span id="page-27-0"></span>Theorem 3.10 (Convergence of the particle system to the mean field equation). Let c <sup>N</sup> be a solution to [\(3.7\)](#page-19-1). Moreover assume its initial distribution to be well-prepared

$$
\frac{1}{N} \mathcal{F}^N(\mathbf{c}^N(0)) \to \mathbb{F}(\mathbb{C}(0)) - \mathcal{F}_0 \quad \text{with} \quad L^N_{\#} \mathbf{c}^N(0) \to \mathbb{C}(0) \quad \text{as } N \to \infty.
$$

Then it holds

$$
L_{\#}^N \mathbf{c}^N(t) \rightharpoonup \mathbb{C}(t) \qquad \text{for all } t \in (0, \infty),
$$

with **C** a weak solution to [\(2.20\)](#page-12-1) and moreover

<span id="page-27-1"></span>
$$
\frac{1}{N} \mathcal{F}^N(\mathbf{c}^N(t)) \to \mathbb{F}(\mathbb{C}(t)) - \mathcal{F}_0 \qquad \text{for all } t \in (0, \infty). \tag{3.24}
$$

Proof. Fix T > 0. By the tightness Lemma [3.9,](#page-26-1) we have that the sequence of empirical measures L N #c <sup>N</sup> : [0, T] → P(P(<sup>X</sup> )) is tight w.r.t. the Skorokhod topology [\[4,](#page-35-21) Theorem 13.2]. Hence, there exist a measurable curve **<sup>C</sup>** : [0, T] → P(P(<sup>X</sup> )) such that up to a subsequence L N #c <sup>N</sup> (t) weakly converges to **<sup>C</sup>**(t) for all <sup>t</sup> <sup>≥</sup> 0. By the Propositions [3.7](#page-21-2) and [3.8,](#page-22-4) we get from Theorem [3.6](#page-20-1) that [\(3.24\)](#page-27-1) holds and **C** is curve of maximal slope for the functional **J**. By Proposition [2.21,](#page-16-1) it is characterized as weak solution to [\(2.20\)](#page-12-1). By Lemma [3.2](#page-18-2) the limiting rate matrix Q is Lipschitz on P(X ) providing uniqueness of the Liouville equation [\(2.20\)](#page-12-1). Hence, the convergence actually holds for the full sequence.

Corollary 3.11. In the setting of Theorem [3.10](#page-27-0) assume in addition that

$$
L_{\#}^N \mathbf{c}^N(0) \rightharpoonup \delta_{c(0)} \qquad \text{for some} \qquad c(0) \in \mathcal{P}(\mathcal{X}) .
$$

Then it holds

$$
L_{\#}^N \mathbf{c}^N(t) \rightharpoonup \delta_{c(t)} \qquad \text{for all } t \in (0, \infty),
$$

with c a solution to [\(1.1\)](#page-0-0) and moreover

$$
\frac{1}{N} \mathcal{F}^N(\mathbf{c}^N(t)) \to \mathcal{F}(c(t)) - \mathcal{F}_0 \quad \text{for all } t \in (0, \infty) .
$$

<span id="page-28-0"></span>Proof. The proof is a direct application of Theorem [3.10](#page-27-0) and a variance estimate for the particle system (Lemma [B.1\)](#page-34-1).

# 4. Properties of the metric W

In this section, we give the proof of Propostion [2.10](#page-9-2) stating that W defines a distance on P(X ) and that the resulting metric space is seperable, complete and geodesic. The proof will be accomplished by a sequence of lemmas giving various estimates on and properties of W. Some work is needed in particular to show finiteness of W.

<span id="page-28-3"></span>Lemma 4.1. For µ, ν, and T > 0 we have

$$
\mathcal{W}(\mu,\nu) = \inf \left\{ \int_0^T \sqrt{\mathcal{A}(c(t), \psi(t))} dt : (c, \psi) \in \mathrm{CE}_T(\mu, \nu) \right\}.
$$

Proof. This follows from a standard reparametrization argument. See for instance [\[18,](#page-35-18) Thm. 5.4] for details in a similar situation.

From the previous lemma we easily deduce the triangular inequality

$$
\mathcal{W}(\mu,\eta) \le \mathcal{W}(\mu,\nu) + \mathcal{W}(\nu,\eta) \quad \forall \mu,\nu,\eta \in \mathcal{P}(\mathcal{X})\;, \tag{4.1}
$$

by concatenating two curves (c, ψ) ∈ CE<sup>T</sup> (µ, ν) and (c ′ , ψ′ ) ∈ CE<sup>T</sup> (ν, η) to form a curve in CE2<sup>T</sup> (µ, η).

The next sequence of lemmas puts W in relation with the total variation distance on P(X ). To proceed, we define similarly to [\[31\]](#page-36-0), for every µ ∈ P(X ), the matrix

<span id="page-28-2"></span>
$$
B_{xy}(\mu) := \begin{cases} \sum_{z \neq x} w_{xz}(\mu), & x = y, \\ -w_{xy}(\mu), & x \neq y \end{cases}
$$

Now [\(2.16\)](#page-8-5) can be rewritten as

$$
\mathcal{W}^{2}(\mu,\nu) = \inf \left\{ \int_{0}^{1} \langle B(c(t))\psi(t), \psi(t) \rangle \, dt : (c, \psi) \in \mathrm{CE}_{1}(\mu, \nu) \right\},\,
$$

where hψ, φi = P <sup>x</sup>∈X ψxφ<sup>x</sup> is the usual inner product on R<sup>X</sup> .

<span id="page-28-1"></span>Lemma 4.2. For any µ, ν ∈ P(X ) holds

$$
\mathcal{W}(\mu,\nu) \ge \frac{1}{\sqrt{2}} ||\mu - \nu||.
$$

Moreover, for every a > <sup>0</sup>, there exists a constant <sup>C</sup>a, such that for all µ, ν ∈ P<sup>a</sup> (X )

$$
\mathcal{W}(\mu,\nu)\leq C_a\|\mu-\nu\|.
$$

Proof. The proof of the lower bound on W can be obtained very similar to [\[22,](#page-35-15) Proposition 2.9].

Let us show the upper bound. Following Lemma A.1. in [\[31\]](#page-36-0), we notice that for µ ∈ P a (X ), the map ψ 7→ B(µ)ψ has an image of dimension d−1. In addition, the dimension of the space {a<sup>x</sup> : P <sup>x</sup>∈X a<sup>x</sup> = 0} is d−1, therefore the map is surjective. From the above we get that the matrix <sup>B</sup>(µ) restricts to an isomorphism <sup>B</sup>˜(µ), on the <sup>d</sup><sup>−</sup> 1 dimensional space {a<sup>x</sup> : Pa<sup>x</sup> = 0}. Now, since the mapping P a (<sup>X</sup> ) <sup>∋</sup> <sup>µ</sup> → kB˜−<sup>1</sup> (µ)k, is continuous with respect to the euclidean metric, we have an upper bound <sup>1</sup> c by compactness. Also P a (<sup>X</sup> ) <sup>∋</sup> <sup>µ</sup> → kB˜(µ)<sup>k</sup> has an upper bound <sup>C</sup> as a result of all entries in <sup>B</sup>(µ) being uniformly bounded. From that we get

$$
c\|\psi\|\leq \|B(\mu)\psi\|\leq C\|\psi\|, \forall \mu\in\mathcal{P}^a(\mathcal{X})
$$

for some suitable positive constants.

Similarly to the proof of Lemma 3.19 in [\[31\]](#page-36-0), for t ∈ [0, 1], we set c(t) = (1 − t)µ + tν and note that c(t) lies in P a (X ), since it is a convex set. Since ˙c(t) = ν−µ ∈ Ran B(c(t)), there exists a unique element ψ(t) for which we have ˙c(t) = B(c(t))ψ(t), and kψ(t)k ≤ 1 c kµ − νk.

From that we get

$$
\mathcal{W}^2(\mu,\nu) \le \int_0^1 \langle B(c(t))\psi(t), \psi(t) \rangle \ dt \le \frac{1}{c^2}C\|\mu-\nu\|^2.
$$

<span id="page-29-0"></span>Lemma 4.3. For every µ ∈ P(X ), ǫ > 0 there exists δ > 0 such that W(µ, ν) < ǫ, for every ν ∈ P(X ), with kµ − νk ≤ δ

The proof of this lemma is similar to the proof [\[31,](#page-36-0) Theorem 3.12] and uses comparison of W to corresponding quantity on the two point space X = {a, b}. However, significantly more care is needed in the present setting to implement this argument. The reason being that the set of pairs of points x, y with Qx,y(µ) > 0 now depends on µ.

Proof. Let ǫ > 0 and µ ∈ P(X ) be fixed. Since X is finite, it holds with E<sup>µ</sup> defined in [\(2.11\)](#page-6-5)

$$
\inf \{ Q_{xy}(\mu) : (x, y) \in E_{\mu} \} = a > 0.
$$

Let Br(µ) = {ν ∈ P(X ) : kν − µk < r} denote a r-neighborhood around µ. Since, Q(µ) is continuous in µ, there exists for η > 0 a δ<sup>1</sup> > 0 s.t.

$$
\forall \nu \in B_{\delta_1}(\mu) \quad \text{holds} \quad |Q(\nu) - Q(\mu)|_{L^{\infty}(\mathcal{X} \times \mathcal{X})} \le \eta.
$$

Especially, it holds by choosing η ≤ a/2 that E<sup>µ</sup> ⊆ E<sup>ν</sup> and in addition

$$
\inf \{ Q_{xy}(\nu) : (x, y) \in E_{\mu}, \nu \in B_{\delta_1}(\mu) \} \ge a/2.
$$

For the next argument, observe that by the concavity of the logarithmic mean and a first order Taylor expansion holds for a, b, s, t, η > 0

$$
\Lambda((s+\eta)a, (t+\eta)b) \leq \Lambda(sa, tb) + \eta (\partial_s \Lambda(sa, tb) + \partial_t \Lambda(sa, tb))
$$
  
= 
$$
\Lambda(sa, tb) + \eta (a\Lambda_1(sa, tb) + b\Lambda_2(sa, tb)),
$$

where Λ<sup>i</sup> is the i-th partial derivative of Λ. Therefore we can estimate for ν ∈ Bδ(µ).

$$
\Lambda(Q_{xy}(\nu)\nu(x), Q_{yx}(\nu)\nu(y)) - \Lambda(Q_{xy}(\mu)\nu(x), Q_{yx}(\mu)\nu(y))
$$
\n
$$
\leq \Lambda((Q_{xy}(\mu) + \eta)\nu(x), (Q_{yx}(\mu) + \eta)\nu(y)) - \Lambda(Q_{xy}(\mu)\nu(x), Q_{yx}(\mu)\nu(y))
$$
\n
$$
\leq \eta\Big(\nu(x)\Lambda_1(Q_{xy}(\mu)\nu(x), Q_{yx}(\mu)\nu(y)) + \nu(y)\Lambda_2(Q_{xy}(\mu)\nu(x), Q_{yx}(\mu)\nu(y))\Big)
$$
\n
$$
\leq \frac{2\eta}{a}\Big(Q_{xy}(\mu)\nu(x)\Lambda_1(Q_{xy}(\mu)\nu(x), Q_{yx}(\mu)\nu(y))
$$
\n
$$
+ Q_{yx}(\mu)\nu(y)\Lambda_2(Q_{xy}(\mu)\nu(x), Q_{yx}(\mu)\nu(y))\Big)
$$
\n
$$
= \frac{2\eta}{a}\Lambda(Q_{xy}(\mu)\nu(x), Q_{yx}(\mu)\nu(y)) \leq \Lambda(Q_{xy}(\mu)\nu(x), Q_{yx}(\mu)\nu(y)),
$$

Moreover, the last identity follows directly from the one-homogeneity of the logarithmic mean. Furthermore, we used η ≤ a 2 to obtain the last estimate. Repeating the argument for the other direction we get

$$
\frac{1}{2}\Lambda(Q_{xy}(\mu)\nu(x), Q_{yx}(\mu)\nu(y)) \leq \Lambda(Q_{xy}(\nu)\nu(x), Q_{yx}(\nu)\nu(y))
$$
\n
$$
\leq 2\Lambda(Q_{xy}(\mu)\nu(x), Q_{yx}(\mu)\nu(y))
$$
\n(4.2)

<span id="page-30-0"></span>Now, let c be an absolutely continuous curve with respect to WQ(µ) , where WQ(µ) is the distance that corresponds to the linear Markov process with fixed rates Q(µ), and lives inside the ball Bδ<sup>1</sup> (µ), then it is also absolutely continuous w.r.t. W, and if ψ solves the continuity equation for c, with respect to the rates Q(µ), then there exists a ψ˜, that solves the continuity equation with respect to the variable rates Q(c(t)) and

<span id="page-30-1"></span>
$$
\int_0^1 \mathcal{A}(c(t), \tilde{\psi}(t))dt \le 2 \int_0^1 \mathcal{A}_{Q(\mu)}(c(t), \psi(t))dt,
$$
\n(4.3)

where AQ(µ) is the action with fixed rate kernel Q(µ).

Indeed let ψ be a solution for the continuity equation for c with respect to the fixed rates Q(µ), i.e.

$$
\dot{c}_x(t) = \sum_y (\psi_y(t) - \psi_x(t)) \Lambda(c_x(t)Q_{xy}(\mu), c_y(t)Q_{yx}(\mu)).
$$

For (x, y) ∈ Eµ, and t ∈ [0, 1] we define

$$
\tilde{v}_{xy}(t) := (\psi_y(t) - \psi_x(t)) \Lambda(c_x(t)Q_{xy}(\mu), c_y(t)Q_{yx}(\mu)).
$$

Then, it is easy to verify that (c, <sup>v</sup>˜) <sup>∈</sup> CE( <sup>~</sup> <sup>c</sup>(0), c(1)) (cf. Definition [2.5\)](#page-7-3) and we can estimate

$$
\int_{0}^{1} \vec{\mathcal{A}}(c(t), \tilde{v}(t)) dt = \int_{0}^{1} \frac{1}{2} \sum_{x,y} \alpha(\tilde{v}_{xy}(t), \Lambda(c_x(t)Q_{xy}(c(t)), c_y(t)Q_{yx}(c(t)))) dt \n= \int_{0}^{1} \frac{1}{2} \sum_{x,y} (\psi_y(t) - \psi_x(t))^2 \frac{\Lambda(c_x(t)Q_{xy}(\mu), c_y(t)Q_{yx}(\mu))}{\Lambda(c_x(t)Q_{xy}(c(t)), c_y(t)Q_{yx}(c(t)))} \n\times \Lambda(c_x(t)Q_{xy}(\mu), c_y(t)Q_{yx}(\mu)) dt \n\leq \int_{0}^{1} \frac{1}{2} \sum_{x,y} (\psi_y(t) - \psi_x(t))^2 2\Lambda(c_x(t)Q_{xy}(\mu), c_y(t)Q_{yx}(\mu)) dt.
$$

Now, the existence of ψ˜ is a straightforward application of Lemma [2.7.](#page-8-2)

Having established [\(4.3\)](#page-30-1), the final result will follow by a comparison with the two-point space for the Wasserstein distance with fixed rate kernel Q(µ).

For ν ∈ Bδ(µ), we can find a sequence of at most (d − 1) measures µ <sup>i</sup> <sup>∈</sup> <sup>B</sup>δ(µ), such that µ <sup>0</sup> = µ and µ <sup>K</sup> = ν and

$$
supp (\mu^{i} - \mu^{i-1}) = \{x_i, y_i\} \in E_{\mu} \quad \text{for } i = 1, ..., K.
$$

Indeed we can use the following matching procedure: Find a pair (i, j) with µ<sup>i</sup> 6= ν<sup>i</sup> and µ<sup>j</sup> 6= ν<sup>j</sup> . Set h = min {|µ<sup>i</sup> − ν<sup>i</sup> |, |µ<sup>j</sup> − ν<sup>j</sup> |}. Then define µ 1 i := µi±h and µ 1 j := µ<sup>j</sup> ∓h with signs chosen as the sign of ν<sup>i</sup> − µ<sup>i</sup> . After this step at least (d − 1)-coordinates of µ 1 and ν agree. This procedure finishes after at most d − 1 steps, because the defect mass of the last pair will match. Therewith, we can compare with the two-point space [\[31,](#page-36-0) Lemma 3.14]

$$
\mathcal{W}_{Q(\mu)}(\mu^{i-1},\mu^i) \leq \frac{1}{\sqrt{2p_{x_iy_i}}}\left|\int_{1-2\mu^i_{x_i}}^{1-2\mu^{i-1}_{x_i}} \sqrt{\frac{\arctanh r}{r}}dr\right| \leq \frac{\delta_1}{2},
$$

with pxiy<sup>i</sup> = Qxiy<sup>i</sup> (µ)πx<sup>i</sup> q (µ). The last estimate follows from the fact, that the function arctanh r r dr, is integrable in [−1, 1]. Therefore, we can find a δ ≤ δ<sup>1</sup> such that for any a, b with <sup>|</sup><sup>a</sup> <sup>−</sup> <sup>b</sup>| ≤ δ, we have <sup>R</sup> <sup>1</sup>−2<sup>b</sup> 1−2a q arctanh r r dr ≤ δ1 <sup>2</sup> min{1, p 2pxiy<sup>i</sup> }. Finally, by Lemma [4.2,](#page-28-1) we can infer that any curve has Euclidean length smaller than its action value. We can conclude that the AQ(µ) -minimizing curve between any µ i−1 , µ<sup>i</sup> , stays inside the ball Bδ<sup>1</sup> (µ), from which we can further conclude that

$$
\mathcal{W}(\mu^{i-1}, \mu^i) \le 2\mathcal{W}_{Q(\mu)}(\mu^{i-1}, \mu^i) \le 2\frac{\delta_1}{2} = \delta_1
$$

By an application of the triangular inequality [\(4.1\)](#page-28-2), we get W(µ, ν) ≤ (d− 1)δ1, and the proof concludes if we pick <sup>δ</sup> such that (<sup>d</sup> <sup>−</sup> 1)δ<sup>1</sup> <sup>≤</sup> ǫ.

<span id="page-31-0"></span>Lemma 4.4. For µk, µ ∈ P(X ), we have

$$
W(\mu_k, \mu) \to 0 \quad \text{iff} \quad \|\mu_k - \mu\| \to 0.
$$

Moreover, the space P(X ), along with the metric W, is a complete space.

Proof. The proof is a direct application of Lemmas [4.2](#page-28-1) and [4.3.](#page-29-0)

<span id="page-32-2"></span>Theorem 4.5 (Compactness of curves of finite action). Let {(c k , v<sup>k</sup> )}k, with

$$
(c^k, v^k) \in \vec{\mathrm{CE}}_T(c^k(0), c^k(T)),
$$

be a sequence of weak solutions to the continuity equation with uniformly bounded action

<span id="page-32-0"></span>
$$
\sup_{k \in \mathbb{N}} \left\{ \int_0^T \vec{\mathcal{A}}(c^k(t), v^k(t)) dt \right\} \le C < \infty.
$$
 (4.4)

Then, there exists a subsequence and a limit (c, v), such that c k converges uniformly to c in [0, T], (c, v) <sup>∈</sup> CE<sup>~</sup> T c(0), c(T) and for the action we have

<span id="page-32-1"></span>
$$
\liminf_{k \to \infty} \int_0^T \vec{\mathcal{A}}(c^k(t), v^k(t)) dt \ge \int_0^T \vec{\mathcal{A}}(c(t), v(t)) dt.
$$
\n(4.5)

Proof. Let x, y ∈ X and (c k , v<sup>k</sup> ) be given as in the statement. Using the Cauchy-Schwarz inequality, we see that for any Borel I ⊂ [0, T] we have the a priori estimate on v k

$$
\int_{I} \frac{1}{2} \sum_{x,y} \left| v_{xy}^{k}(t) \right| dt \le \int_{0}^{T} \left( \overrightarrow{\mathcal{A}} \left( c^{k}(t), v^{k}(t) \right) \right)^{\frac{1}{2}} \left( \frac{1}{2} \sum_{x,y} w_{xy} \left( c(t) \right) \right)^{\frac{1}{2}} dt
$$
  
$$
\le \sqrt{CT} \sqrt{C_{w} |I|},
$$

with wxy (c(t)) from [\(2.7\)](#page-6-4). Since Q is continuous on P(X ) by Definition [2.3,](#page-5-0)

$$
\sup_{\nu \in \mathcal{P}(\mathcal{X})} \frac{1}{2} \sum_{x,y} w_{xy} (\nu) = C_w < \infty.
$$

Together with the assumption [\(4.4\)](#page-32-0), the whole r.h.s. is uniformly bounded in k. Therefore, for a subsequence holds v k xy ⇀ vxy as Borel measure on [0, T] and all x, y ∈ X . Now, we choose a sequence of smooth test functions ϕ ε in [\(2.12\)](#page-7-2), which converge to the indicator of the interval [t1, t2] as ε → 0. Therewith and using the above a priori estimate on v k , we deduce

$$
\left|c_x^k(t_2) - c_x^k(t_1)\right| \le \int_{t_1}^{t_2} \frac{1}{2} \sum_{y \in \mathcal{X}} \left( \left|v_{xy}^k(t)\right| + \left|v_{yx}^k(t)\right| \right) dt \le \sqrt{CC_w} \sqrt{|t_2 - t_1|}.
$$

Hence, c k is equi-continuous and therefore converges (upto a further subsequence) to some continuous curve c. This, already implies that we can pass to the limit in [\(2.12\)](#page-7-2) and obtain that (c, v) ∈ CE<sup>T</sup> .

Moreover, we can deduce since ν 7→ Q(ν) is continuous for all x, y ∈ X also c k 1;x,y := c k x (t)Qxy(c k (t)) → cx(t)Qxy(c(t)) =: c1;x,y(t) and analogue with c k 2;x,y := c k y (t)Qyx(c k (t)). We rewrite the action [\(2.14\)](#page-7-4) as

$$
\vec{\mathcal{A}}(c^k(t), v^k(t)) = \frac{1}{2} \sum_{x,y} \alpha\Big(v_{x,y}^k(t), \Lambda\Big(c^k_{1;x,y}(t), c^k_{2;x,y}(t)\Big)\Big)
$$

The conclusion [\(4.5\)](#page-32-1) follows now from [\[8,](#page-35-20) Thm. 3.4.3] by noting that (v, c1, c2) 7→ α(v,Λ(c1, c2)) is l.s.c., jointly convex and 1-homogeneous and hence

$$
\liminf_{k} \int_0^T \vec{\mathcal{A}}(c^k(t), v^k(t)) dt \ge \int_0^T \frac{1}{2} \sum_{x,y} \alpha(v_{x,y}(t), \Lambda(c_{1;x,y}(t), c_{2;x,y}(t))) dt
$$
$$
= \int_0^T \vec{\mathcal{A}}(c(t), v(t)) dt.
$$

We can now give the proof of Proposition [2.10:](#page-9-2)

Proof of Proposition [2.10.](#page-9-2) Symmetry of W is obvious, the coincidence axiom follows from Lemma [4.2](#page-28-1) and the triangular inequality from Lemma [4.1](#page-28-3) as indicated above. The finiteness of W comes by using Lemmas [4.2,](#page-28-1) [4.3](#page-29-0) and the triangular inequality. Thus W defines a metric. Completeness and separability follow directly from Lemmas [4.4](#page-31-0) and [4.2.](#page-28-1) By the direct method of the calculus of variations and the compactness results Proposition [4.5,](#page-32-2) we obtain for any µ, ν ∈ P(X ) a curve (γt)t∈[0,1] with minimal action connecting them, i.e. <sup>W</sup>(µ, ν) = <sup>R</sup> <sup>1</sup> <sup>0</sup> A(γ<sup>t</sup> , ψt)dt = R 1 0 |γ ′ t | <sup>2</sup>dt, where in the last equality we used Proposition [2.11.](#page-9-3) From this, it is easy to see that γ is a constant speed geodesic.

Appendix A. Stirling formula with explicit error estimate

<span id="page-33-1"></span><span id="page-33-0"></span>Lemma A.1. Let ν ∈ P<sup>N</sup> (X ), then it holds

$$
-\frac{\log(N+1)}{N} \le -\frac{1}{N} \log \frac{N!}{\prod_{x \in \mathcal{X}} (N\nu(x))!} - \sum_{x \in \mathcal{X}} \nu(x) \log \nu(x) \le \frac{|\mathcal{X}| \log N}{N} + \frac{1}{N}.
$$

Proof. We write

$$
- \log \frac{N!}{\prod_{x \in \mathcal{X}} (N\nu(x))!} = \sum_{x \in \mathcal{X}} \sum_{k=1}^{N\nu(x)} \log k - \sum_{k=1}^{N} \log k
$$
  
\n
$$
\geq \sum_{x \in \mathcal{X}} \int_{1}^{N\nu(x)} \log y \, dy - \int_{1}^{N+1} \log(y) \, dy
$$
  
\n
$$
= \sum_{x \in \mathcal{X}} \left( N\nu(x) \left( \log N\nu(x) - 1 \right) - 1 \right) - (N+1) \left( \log(N+1) - 1 \right) - 1
$$
  
\n
$$
= N \sum_{x \in \mathcal{X}} \nu(x) \log \nu(x) + NR_N,
$$

where the remainder R<sup>N</sup> can be estimated as follows

$$
R_N = \frac{|X|}{N} + \log \frac{N}{N+1} - \frac{\log(N+1)}{N} \ge -\frac{\log(N+1)}{N}
$$

for |X | ≥ 2 and N ≥ 1. The other bound can be obtained by shifting the integration bounds appropriately in the above estimate.

## Appendix B. Variance estimate for the particle system

<span id="page-34-1"></span><span id="page-34-0"></span>Lemma B.1. For the N-Particle process X<sup>N</sup> with generator [3.6](#page-19-4) holds for some C > 0 and all t ∈ [0, T] with T < ∞

$$
\forall x \in \mathcal{X} : \qquad \text{var}\Big(L_x^N(\mathbf{X}^N(t))\Big) \leq e^{Ct}\Big(\text{var}\left(L_x^N(\mathbf{X}^N(0))\right) + O(N^{-1})\Big).
$$

Proof. We denote with Nx(t) = NL<sup>N</sup> x (XN(t)) the empirical process of the particle number at site x. The empirical density process of particles at site x is then Nx(t)/N = L N x (XN(t)). Therewith, we have

$$
\frac{d}{dt} \operatorname{var}(N_x(t)) = \mathbb{E}[\mathcal{L}^N N_x^2(t)] - 2\mathbb{E}[N_x(t)]\mathbb{E}[\mathcal{L}^N N_x(t)]
$$
\n
$$
= \mathbb{E}\bigg[\sum_y N_x(t)(N_x^2(t) - (N_x(t) - 1)^2)Q_{xy}^N(L^N(\mathbf{X}^N(t)))
$$
\n
$$
+ \sum_y N_y(t)(N_x^2(t) - (N_x(t) + 1)^2)Q_{yx}^N(L^N(\mathbf{X}^N(t)))\bigg]
$$
\n
$$
- 2\mathbb{E}[N_x(t)]\mathbb{E}\bigg[\sum_y N_x(t)Q_{xy}^N(L^N(\mathbf{X}^N(t))) - N_y(t)Q_{yx}^N(L^N(\mathbf{X}^N(t)))\bigg]
$$
\n
$$
= 2\mathbb{E}[N_x(t)^2Q_{xy}(L^N(\mathbf{X}^N(t)))] - 2\mathbb{E}\bigg[\sum_y N_x(t)N_y(t)Q_{yx}^N(L^N(\mathbf{X}^N(t)))\bigg]
$$
\n
$$
- 2\mathbb{E}[N_x(t)]\mathbb{E}\bigg[\sum_y N_x(t)Q_{xy}^N(L^N(\mathbf{X}^N(t))) - N_y(t)Q_{yx}^N(L^N(\mathbf{X}^N(t)))\bigg] + O(N)
$$
\n
$$
\leq C \operatorname{var}(N_x(t)) + C \sum_{y \neq x} \operatorname{var}(N_x(t))^{1/2} \operatorname{var} N_y(t)^{1/2}
$$
\n
$$
\leq C \sum_y \operatorname{var}(N_y(t)) + O(N).
$$

In theses computations, we used the fact that Q<sup>N</sup> is uniformly bounded and that the state space is finite.

Hence

$$
\frac{d}{dt}\operatorname{var}(N_x(t)/N) \le C\sum_y \operatorname{var}(N_y(t)/N) + O(N^{-1})
$$

and therefore, using Gronwall's Lemma, as soon as the sum of initial variances goes to zero when N goes to infinity, it also goes to zero at any positive time, and uniformly on bounded time intervals.

### Acknowledgments

This work was done while the authors were enjoying the hospitality of the Hausdorff Research Institute for Mathematics during the Junior Trimester Program on Optimal Transport, whose support is gratefully acknowledged. We would like to thank Hong Duong for discussions on this topic. M.F. gratefully acknowledges funding from NSF

FRG grant DMS-1361185 and GdR MOMAS. M.E. and A.S. acknowledge support by the German Research Foundation through the Collaborative Research Center 1060 The Mathematics of Emergent Effects.

### References

- <span id="page-35-4"></span><span id="page-35-3"></span>[1] S. Adams, N. Dirr, M. A. Peletier and J. Zimmer, From a large-deviations principle to the Wasserstein gradient flow: a new micro-macro passage, Comm. Math. Phys., 307 (2011), 791–815.
- <span id="page-35-7"></span>[2] L. Ambrosio, N. Gigli and G. Savar´e, Gradient Flows in Metric Spaces and in the Space of Probability Measures, 2nd edition, Lectures in Mathematics ETH Z¨urich, Birkh¨auser Verlag, Basel, 2008.
- <span id="page-35-21"></span>[3] L. Ambrosio, G. Savar´e and L. Zambotti, Existence and stability for Fokker-Planck equations with log-concave reference measure, Probab. Theory Related Fields, 145 (2009), 517–564.
- <span id="page-35-16"></span>[4] P. Billingsley, Probability and Measure, 2nd edition, Wiley Series in Probability and Mathematical Statistics: Probability and Mathematical Statistics, John Wiley & Sons, Inc., New York, 1999.
- <span id="page-35-17"></span>[5] F. Bolley, A. Guillin and C. Villani, Quantitative concentration inequalities for empirical measures on non-compact spaces, Probab. Theory Related Fields, 137 (2007), 541–593.
- <span id="page-35-0"></span>[6] A. Budhiraja, P. Dupuis, M. Fischer and K. Ramanan, Limits of relative entropies associated with weakly interacting particle systems, Electron. J. Probab., 20 (2015), 22pp.
- [7] A. Budhiraja, P. Dupuis, M. Fischer and K. Ramanan, Local stability of Kolmogorov forward equations for finite state nonlinear Markov processes, Electron. J. Probab., 20 (2015), 30pp.
- <span id="page-35-20"></span>[8] G. Buttazzo, Semicontinuity, Relaxation and Integral Representation in the Calculus of Variations, vol. 207 of Pitman Research Notes in Mathematics Series, Longman Scientific & Technical, Harlow; copublished in the United States with John Wiley & Sons, Inc., New York, 1989.
- <span id="page-35-12"></span>[9] J. A. Carrillo, R. J. McCann and C. Villani, Kinetic equilibration rates for granular media and related equations: entropy dissipation and mass transportation estimates, Rev. Mat. Iberoamericana, 19 (2003), 971–1018.
- <span id="page-35-13"></span>[10] J. A. Carrillo, R. J. McCann and C. Villani, Contractions in the 2-Wasserstein length space and thermalization of granular media, Arch. Ration. Mech. Anal., 179 (2006), 217–263.
- <span id="page-35-14"></span>[11] P. Cattiaux, A. Guillin and F. Malrieu, Probabilistic approach for granular media equations in the non-uniformly convex case, Probab. Theory Related Fields, 140 (2008), 19–40.
- <span id="page-35-11"></span>[12] P. Dai Pra and F. den Hollander, McKean-Vlasov limit for interacting random processes in random media, J. Statist. Phys., 84 (1996), 735–772.
- <span id="page-35-8"></span>[13] S. Daneri and G. Savar´e, Lecture notes on gradient flows and optimal transport, in Optimal Transportation, vol. 413 of London Math. Soc. Lecture Note Ser., Cambridge Univ. Press, Cambridge, 2014, 100–144.
- <span id="page-35-10"></span>[14] D. A. Dawson and J. G¨artner, Large deviations from the McKean-Vlasov limit for weakly interacting diffusions, Stochastics, 20 (1987), 247–308.
- <span id="page-35-2"></span>[15] E. De Giorgi, A. Marino and M. Tosques, Problems of evolution in metric spaces and maximal decreasing curve, Atti Accad. Naz. Lincei Rend. Cl. Sci. Fis. Mat. Natur. (8), 68 (1980), 180–187.
- <span id="page-35-5"></span>[16] N. Dirr, V. Laschos and J. Zimmer, Upscaling from particle models to entropic gradient flows, J. Math. Phys., 53 (2012), 063704, 9 pp.
- <span id="page-35-18"></span><span id="page-35-9"></span>[17] R. Dobrushin, Vlasov equations, Functional Analysis and Its Applications, 13 (1979), 48–58,96.
- [18] J. Dolbeault, B. Nazaret and G. Savar´e, A new class of transport distances between measures, Calc. Var. Partial Differential Equations, 34 (2009), 193–231.
- <span id="page-35-6"></span>[19] M. H. Duong, V. Laschos and M. Renger, Wasserstein gradient flows from large deviations of manyparticle limits, ESAIM Control Optim. Calc. Var., 19 (2013), 1166–1188.
- <span id="page-35-19"></span>[20] P. Dupuis and R. S. Ellis, A Weak Convergence Approach to the Theory of Large Deviations, Wiley Series in Probability and Statistics: Probability and Statistics, John Wiley & Sons, Inc., New York, 1997, A Wiley-Interscience Publication.
- <span id="page-35-1"></span>[21] M. Erbar, Gradient flows of the entropy for jump processes, Ann. Inst. H. Poincar´e Probab. Statist., 50 (2014), 920–945.
- <span id="page-35-15"></span>[22] M. Erbar and J. Maas, Ricci curvature of finite Markov chains via convexity of the entropy, Arch. Ration. Mech. Anal., 206 (2012), 997–1038.

- <span id="page-36-6"></span><span id="page-36-4"></span>[23] M. Erbar and J. Maas, Gradient flow structures for discrete porous medium equations, Discrete Contin. Dyn. Syst., 34 (2014), 1355–1374.
- <span id="page-36-5"></span>[24] M. Erbar, J. Maas and M. Renger, From large deviations to Wasserstein gradient flows in multiple dimensions, Electron. Commun. Probab., 20 (2015), 1–12.
- <span id="page-36-13"></span>[25] [10.1016/j.matpur.2016.03.018] M. Fathi, A gradient flow approach to large deviations for diffusion processes, J. Math. Pures Appl., (2016).
- [26] M. Fathi and M. Simon, The gradient flow approach to hydrodynamic limits for the simple exclusion process, In P. Gon¸calves and A. J. Soares, From Particle Systems to Partial Differential Equations III: Particle Systems and PDEs III, Braga, Portugal, December 2014, 167–184, Springer International Publishing, Cham, 2016.
- <span id="page-36-12"></span><span id="page-36-2"></span>[27] N. Gigli and J. Maas, Gromov-Hausdorff convergence of discrete transportation metrics, SIAM J. Math. Anal., 45 (2013), 879–899.
- [28] R. Jordan, D. Kinderlehrer and F. Otto, The variational formulation of the Fokker-Planck equation, SIAM J. Math. Anal., 29 (1998), 1–17.
- <span id="page-36-18"></span><span id="page-36-16"></span>[29] C. Kipnis and C. Landim, Scaling Limits of Interacting Particle Systems, vol. 320 of Grundlehren der Mathematischen Wissenschaften, Springer-Verlag, Berlin, 1999.
- [30] D. A. Levin, M. J. Luczak and Y. Peres, Glauber dynamics for the mean-field Ising model: Cut-off, critical power law, and metastability, Probab. Theory Related Fields, 146 (2010), 223–265.
- <span id="page-36-15"></span><span id="page-36-0"></span>[31] J. Maas, Gradient flows of the entropy for finite Markov chains, J. Funct. Anal., 261 (2011), 2250– 2292.
- <span id="page-36-17"></span>[32] F. Malrieu, Convergence to equilibrium for granular media equations and their Euler schemes, Ann. Appl. Probab., 13 (2003), 540–560.
- <span id="page-36-1"></span>[33] [10.1063/1.1699114] N. Metropolis, A. W. Rosenbluth, M. N. Rosenbluth, A. H. Teller and E. Teller, Equations of state calculations by fast computing machines, J. Chem. Phys., 21 (1953), 1087–1091.
- [34] A. Mielke, Geodesic convexity of the relative entropy in reversible Markov chains, Calc. Var. Partial Differential Equations, 48 (2013), 1–31.
- <span id="page-36-9"></span>[35] A. Mielke, On evolutionary Γ-convergence for gradient systems, Springer International Publishing, Cham, 3 (2016), 187–249.
- <span id="page-36-10"></span><span id="page-36-3"></span>[36] K. Oelschl¨ager, A martingale approach to the law of large numbers for weakly interacting stochastic processes, Ann. Probab., 12 (1984), 458–479.
- [37] F. Otto, The geometry of dissipative evolution equations: The porous medium equation, Comm. Partial Differential Equations, 26 (2001), 101–174.
- <span id="page-36-7"></span>[38] E. Sandier and S. Serfaty, Gamma-convergence of gradient flows with applications to Ginzburg-Landau, Comm. Pure Appl. Math., 57 (2004), 1627–1672.
- <span id="page-36-14"></span>[39] A. Schlichting, Macroscopic limits of the Becker-D¨oring equations via gradient flows, arXiv: 1607.08735.
- <span id="page-36-8"></span>[40] S. Serfaty, Gamma-convergence of gradient flows on Hilbert and metric spaces and applications, Discrete Contin. Dyn. Syst., 31 (2011), 1427–1451.
- <span id="page-36-11"></span>[41] A.-S. Sznitman, Topics in Propagation of Chaos, in Ecole d' ´ Et´e de Probabilit´es de Saint-Flour ´ XIX—1989, vol. 1464 of Lecture Notes in Math., Springer, Berlin, 1991, 165–251.

University of Bonn, Germany E-mail address: erbar@iam.uni-bonn.de

University of California, Berkeley E-mail address: maxf@berkeley.edu

Weierstrass Institute E-mail address: Vaios.laschos@wias-berlin.de

University of Bonn, Germany E-mail address: schlichting@iam.uni-bonn.de