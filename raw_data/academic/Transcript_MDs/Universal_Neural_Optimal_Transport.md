# Universal Neural Optimal Transport

Jonathan Geuter 1 2 \* Gregor Kornhardt 3 \* Ingimar Tomasson 3 \* Vaios Laschos <sup>4</sup>

## Abstract

Optimal Transport (OT) problems are a cornerstone of many applications, but solving them is computationally expensive. To address this problem, we propose UNOT (Universal Neural Optimal Transport), a novel framework capable of accurately predicting (entropic) OT distances and plans between discrete measures for a given cost function. UNOT builds on Fourier Neural Operators, a universal class of neural networks that map between function spaces and that are discretization-invariant, which enables our network to process measures of variable resolutions. The network is trained adversarially using a second, generating network and a self-supervised bootstrapping loss. We ground UNOT in an extensive theoretical framework. Through experiments on Euclidean and non-Euclidean domains, we show that our network not only accurately predicts OT distances and plans across a wide range of datasets, but also captures the geometry of the Wasserstein space correctly. Furthermore, we show that our network can be used as a stateof-the-art initialization for the Sinkhorn algorithm with speedups of up to 7.4×, significantly outperforming existing approaches.

## <span id="page-0-3"></span>1. Introduction

Optimal Transport [\(Villani,](#page-11-0) [2009;](#page-11-0) [Peyre & Cuturi](#page-11-1) ´ , [2019\)](#page-11-1) plays an increasing role in various areas in machine learning, such as domain adaptation [\(Courty et al.,](#page-9-0) [2017\)](#page-9-0), singlecell genomics [\(Schiebinger et al.,](#page-11-2) [2019\)](#page-11-2), imitation learning [\(Dadashi et al.,](#page-10-0) [2020\)](#page-10-0), imaging [\(Schmitz et al.,](#page-11-3) [2018\)](#page-11-3), dataset adaptation [\(Alvarez-Melis & Fusi,](#page-9-1) [2021\)](#page-9-1), and signal processing [\(Kolouri et al.,](#page-10-1) [2017\)](#page-10-1). Oftentimes, an entropic

![](_page_0_Figure_9.jpeg)

<span id="page-0-2"></span>Figure 1. Errors on the OT distance after *a single* Sinkhorn iteration for the default initialization (Ones), the Gaussian one [\(Thorn](#page-11-4)[ton & Cuturi,](#page-11-4) [2022\)](#page-11-4), and ours (UNOT), for c(x, y) = ∥x − y∥ 2 .

regularizer is added, as this allows for efficient computation of the solution via the Sinkhorn algorithm [\(Cuturi,](#page-10-2) [2013\)](#page-10-2). The entropic OT problem between probability measures µ ∈ P(X ), ν ∈ P(Y) on Polish spaces X , Y, given a cost function c : X × Y → R ∪ {∞}, is defined as

<span id="page-0-1"></span>
$$
\mathrm{OT}_{\epsilon}(\mu,\nu) = \inf_{\pi \in \Pi(\mu,\nu)} \int_{\mathcal{X} \times \mathcal{Y}} c \, \mathrm{d}\pi - \epsilon KL(\pi || \mu \otimes \nu), \tag{1}
$$

where Π(µ, ν) is the set of all *transport plans* (i.e. measures on X × Y that admit µ resp. ν as their marginals), KL(π||µ ⊗ ν) = R log(π/µ ⊗ ν)dπ is the KL divergence of π from µ ⊗ ν, and ϵ > 0 is a regularizing coefficient.[1](#page-0-0)

Many of these applications require solving problem [\(1\)](#page-0-1) repeatedly, such as in single-cell perturbations [\(Bunne et al.,](#page-9-2) [2022;](#page-9-2) [2023b](#page-9-3)[;a\)](#page-9-4), Natural Language Processing [\(Xu et al.,](#page-12-0) [2018\)](#page-12-0), flow matching with OT couplings [\(Tong et al.,](#page-11-5) [2024;](#page-11-5) [Pooladian et al.,](#page-11-6) [2023\)](#page-11-6), or even seismology [\(Engquist &](#page-10-3) [Froese,](#page-10-3) [2013\)](#page-10-3). However, solving OT problems is computationally expensive, and fast approximation methods are an active area of research. Variations of the transport problem, such as (generalized) sliced Wasserstein distances [\(Kolouri](#page-10-4) [et al.,](#page-10-4) [2015;](#page-10-4) [2019\)](#page-11-7), reduce computational complexity at

<sup>\*</sup>Equal contribution <sup>1</sup>Harvard John A. Paulson School of Engineering and Applied Sciences <sup>2</sup>Kempner Institute at Harvard University <sup>3</sup>Department of Mathematics, Technische Universitat¨ Berlin, Germany <sup>4</sup>Weierstrass Institute, Berlin, Germany. Correspondence to: Jonathan Geuter <jonathan.geuter@gmx.de>.

*Proceedings of the* 42 nd *International Conference on Machine Learning*, Vancouver, Canada. PMLR 267, 2025. Copyright 2025 by the author(s).

<span id="page-0-0"></span><sup>1</sup> For a background on OT, see Appendix [A.](#page-13-0)

the cost of accuracy via random projections. Two previous works are aimed at predicting good initializations for the Sinkhorn algorithm, which can iteratively solve problem [\(1\)](#page-0-1). In [\(Thornton & Cuturi,](#page-11-4) [2022\)](#page-11-4), initializations are computed from OT problems between Gaussians. [\(Amos et al.,](#page-9-5) [2023\)](#page-9-5) train a neural network to predict transport plans and costs via the entropic *dual OT problem* (Section [2\)](#page-1-0). While their framework shares some similarities with ours (see Section [5\)](#page-8-0), it is inherently limited to measures of fixed dimension from the training dataset. Instead, we present a *Universal Neural OT* (UNOT) solver which, given discrete measures µ ∈ P(X ) and ν ∈ P(Y) of variable resolution (viewed as *discretizations* of continuous measures; see Section [3.1\)](#page-2-0), can accurately predict the OT cost and plan associated with problem [\(1\)](#page-0-1). To this end, we leverage Fourier Neural Operators (FNOs) [\(Kovachki et al.,](#page-11-8) [2024\)](#page-11-8), a discretization-invariant class of neural networks that can process inputs of variable sizes. An FNO S<sup>ϕ</sup> is trained to predict a solution to the dual OT problem (Section [2\)](#page-1-0) given two measures (µ, ν), from which the primal problem [\(1\)](#page-0-1) can be solved. Training is self-supervised with an adversarial *generator* network G<sup>θ</sup> which creates training distributions Gθ(z) = (µ, ν) from z ∼ ρ<sup>z</sup> = N (0, I) (see Section [3.4\)](#page-4-0). We want to highlight that in contrast to most neural OT frameworks, such as [\(Bunne et al.,](#page-9-4) [2023a;](#page-9-4) [Uscidda & Cuturi,](#page-11-9) [2023;](#page-11-9) [Korotin](#page-11-10) [et al.,](#page-11-10) [2023\)](#page-11-10), we *generalize across OT problems* (given a fixed cost). GeONet [\(Gracyk & Chen,](#page-10-5) [2024\)](#page-10-5) also uses Neural Operators to learn Wasserstein geodesics. In Section [4,](#page-4-1) we show that UNOT significantly outperforms GeONet on approximating geodesics, despite not being trained on them.

### Our contributions are as follows:

- present UNOT, the first neural OT solver capable of generalizing across datasets and input dimensions
- introduce a generator G<sup>θ</sup> (Section [3.3\)](#page-3-0) which can provably generate any discrete distribution (of fixed dimension) during training (in fact, we prove this result for a very general class of residual networks, see Theorem [3](#page-3-1) and Corollary [4\)](#page-3-2)
- propose a self-supervised bootstrapping loss which provably minimizes the loss against the ground truth dual potentials (Proposition [5\)](#page-4-2)
- show that UNOT can accurately predict OT distances across various datasets, costs, and domains of different dimensions up to a few percent error, and that it accurately captures the geometry of the Wasserstein space by approximating barycenters (Section [4\)](#page-4-1)
- approximate Wasserstein geodesics through barycenters and OT plans predicted by UNOT (Section [4\)](#page-4-1)
- demonstrate how UNOT sets a new state-of-the-art for initializing the Sinkhorn algorithm while maintaining its desirable properties, such as parallelizability and differentiability (Section [4\)](#page-4-1)

## <span id="page-1-0"></span>2. Background

We give a brief overview of optimal transport, and how it relates to UNOT. For a more thorough introduction, see Appendix [A.1](#page-13-1) or [\(Peyre & Cuturi](#page-11-1) ´ , [2019;](#page-11-1) [Villani,](#page-11-0) [2009\)](#page-11-0).

Notation. We write vectors in bold (x, u, etc.) and matrices in capitals (X, U, etc.). 1<sup>n</sup> ∈ R <sup>n</sup> denotes the all-ones vector, ∆n−<sup>1</sup> the simplex in R <sup>n</sup>, and all elements in ∆n−<sup>1</sup> with positive entries are denoted by ∆ n−1 >0 . P(X ) denotes the space of probability measures on X , and Pp(X ) the set of probability measures with finite p-th moments. For µ ∈ P(X ) and a map T, we denote by T#µ the *pushforward* of µ under T, i.e. the measure µ ◦ T −1 . S <sup>2</sup> = {x ∈ R 3 : ∥x∥ = 1} is the unit sphere in R 3 .

### 2.1. Optimal Transport

Unregularized Optimal Transport. The unregularized problem takes the form infπ∈Π(µ,ν) R X×Y c(x, y)dπ(x, y), akin to [\(1\)](#page-0-1) without the regularization term. In the case where X = Y, c(x, y) = d(x, y) p for p ≥ 1 and a metric d on X , the *Wasserstein-*p *distance* is defined as

$$
W_p(\mu,\nu) = \inf_{\pi \in \Pi(\mu,\nu)} \left( \int_{\mathcal{X} \times \mathcal{X}} d(x,y)^p \mathrm{d}\pi(x,y) \right)^{\frac{1}{p}}, \tag{2}
$$

which is indeed a distance on the space Pp(X ) of Borel measures with finite p-th moments [\(Villani,](#page-11-0) [2009\)](#page-11-0).

Dual Optimal Transport Problem. The regularized Kantorovich problem [\(1\)](#page-0-1) admits a dual formulation:

<span id="page-1-1"></span>
$$
\sup_{f \in L^1(\mu), g \in L^1(\nu)} \int_{\mathcal{X}} f(x) d\mu(x) + \int_{\mathcal{Y}} g(y) d\nu(y) - i^{\epsilon}(f, g),
$$
\n(3)

where

$$
\iota^{\epsilon}(f,g) = \epsilon \int_{\mathcal{X}\times\mathcal{Y}} e^{\frac{1}{\epsilon}(f(x)+g(y)-c(x,y))} - 1 \mathrm{d}\mu(x) \mathrm{d}\nu(y).
$$

It can be shown that if c ∈ L 1 (µ ⊗ ν), the values of the primal [\(1\)](#page-0-1) and the dual [\(3\)](#page-1-1) coincide [\(Nutz,](#page-11-11) [2022\)](#page-11-11).

Disrete Optimal Transport. We want to apply UNOT to *discretizations* of measures µ ∈ P(X ), ν ∈ P(Y) (see Section [3.1\)](#page-2-0). To this end, consider measures µ and ν that are supported on finitely many points x1, ..., x<sup>m</sup> ∈ X , y1, ..., y<sup>n</sup> ∈ Y resp, i.e. µ = P<sup>m</sup> <sup>i</sup>=1 aiδ<sup>x</sup><sup>i</sup> , ν = P<sup>n</sup> <sup>j</sup>=1 b<sup>j</sup> δ<sup>y</sup><sup>j</sup> . By abusing notation, we can write µ ∈ R m ≥0 and ν ∈ R n ≥0 . [2](#page-1-2) Note that the dual potentials in problem [\(3\)](#page-1-1) are elements in L 1 (µ) resp. L 1 (ν), hence we can abuse notation again and consider the potentials f ∈ R <sup>m</sup> and g ∈ R <sup>n</sup> to be vectors as well. This point of view gives rise to *discrete optimal*

<span id="page-1-2"></span><sup>2</sup>Whenever we view a discrete measure or a function as a vector, we will use bold characters.

*transport*. We set C ∈ R <sup>m</sup>×<sup>n</sup> via Cij = c(x<sup>i</sup> , y<sup>j</sup> ), and view transport plans as matrices Π ∈ R <sup>m</sup>×<sup>n</sup> (see Appendix [A.1](#page-13-1) for a more thorough introduction to discrete OT). The following proposition shows that the plan Π can be recovered from the dual vectors f and g [\(Peyre & Cuturi](#page-11-1) ´ , [2019\)](#page-11-1).

<span id="page-2-2"></span>Proposition 1. *Define the Gibbs kernel* K = exp(−C/ϵ)*. The unique solution* Π *of the discrete OT problem is given by*

<span id="page-2-5"></span>
$$
\Pi = \text{diag}(\boldsymbol{u}) K \text{diag}(\boldsymbol{v}) \tag{4}
$$

*for two positive scaling vectors* u *and* v *unique up to a scaling constant (i.e.* λu*,* 1 λ v *for* λ > 0*). Furthermore,* (u, v) *are linked to a solution* (f, g) *of the dual problem via*

$$
(\boldsymbol{u},\boldsymbol{v})=(\exp(\boldsymbol{f}/\epsilon),\exp(\boldsymbol{g}/\epsilon))\,.
$$

In Section [3.1,](#page-2-0) we show how the solution to the entropic dual between discrete (µn, νn) converges to the solution of the continuous dual [\(3\)](#page-1-1) as (µn, νn) converge to continuous measures (µ, ν) in some way, which will be crucial for the design of our network Sϕ.

### 2.2. The Sinkhorn Algorithm

The Sinkhorn Algorithm [1](#page-2-1) can iteratively solve the discrete dual problem and was introduced in [\(Cuturi,](#page-10-2) [2013\)](#page-10-2). It requires an initialization v <sup>0</sup> ∈ R <sup>n</sup>, which is typically set to 1n, and µ and ν to be positive everywhere.

<span id="page-2-1"></span>Algorithm 1 Sinkhorn(µ, ν > 0, K = exp(−C/ϵ), ϵ, v 0 ) 1: for l = 0, ..., N do 2: u <sup>l</sup>+1 ← µ./Kv l 3: v <sup>l</sup>+1 ← ν./K<sup>⊤</sup>u l+1 4: end for 5: Π ← diag(u l )Kdiag(v l ), OTϵ(µ, ν) ← ⟨C, Π⟩ 6: return u, v, Π, OTϵ(µ, ν)

In the algorithm, ./ is to be understood as element-wise division. Sinkhorn and Knopp [\(Sinkhorn & Knopp,](#page-11-12) [1967\)](#page-11-12) showed that the iterates u l and v l from the algorithm converge to the vectors u and v from Proposition [1.](#page-2-2)

### 2.3. Predicting Dual Potentials

Given discrete measures µ and ν, UNOT should ultimately be used to approximate the associated transport plan and cost. However, given an optimal dual potential v, the corresponding potential u can be computed as

<span id="page-2-3"></span>
$$
u = \mu. / Kv,
$$
 (5)

which also holds at convergence of the Sinkhorn algorithm. Thus, solving for the m × n-dimensional plan Π can be reduced to a n-dimensional problem over v. Since computations in the log space tend to be more stable [\(Peyre &´](#page-11-1)

[Cuturi,](#page-11-1) [2019\)](#page-11-1), we will instead let UNOT predict the dual potential g = ϵ log(v), i.e.

$$
S_{\boldsymbol{\phi}}(\boldsymbol{\mu},\boldsymbol{\nu})=\boldsymbol{g},\quad \boldsymbol{\mu}\in\mathcal{P}(\mathcal{X}),\boldsymbol{\nu}\in\mathcal{P}(\mathcal{Y}).
$$

The prediction g can then be used to solve the entropic OT problem via the relationship [\(5\)](#page-2-3) and Proposition [1,](#page-2-2) or to initialize the Sinkhorn algorithm via v <sup>0</sup> = exp(g/ϵ).

Note that the solution to the entropic dual is not unique (see Proposition [1\)](#page-2-2). How we account for this non-uniqueness is explained in Section [3.4.](#page-4-0) However, when endowing R <sup>m</sup> × R <sup>n</sup> with the equivalence relation (u1, v1) ∼ (u2, v2) ⇔ ∃λ > 0 : (u1, v1) = (λu2, 1 λ v2) (i.e. accounting for the non-uniqueness of the dual solution), the map (µ, ν) 7→ v, mapping two measures to the associated dual potential in the quotient space, is Lipschitz continuous [\(Carlier et al.,](#page-9-6) [2022\)](#page-9-6), which supports its learnability by a neural network.

## 3. Universal Neural Optimal Transport

Consider the OT problem between two (grayscale) images, encoded as vectors in µn, ν<sup>n</sup> ∈ R <sup>n</sup>. These can be viewed as discrete measures on P([0, 1]<sup>2</sup> ), which discretize continuous measures µ, ν ∈ P([0, 1]<sup>2</sup> ), where the discretization depends on the resolution of the image, and the continuous measures correspond to the images at "infinite" resolution. UNOT should predict the corresponding dual potential g<sup>n</sup> ∈ R <sup>n</sup> solving [\(3\)](#page-1-1) *independent* of the resolution n. [3](#page-2-4) In Section [3.1,](#page-2-0) we establish a convergence result for the dual potentials as n → ∞, which justifies the use of Neural Operators [\(Kovachki et al.,](#page-11-8) [2024\)](#page-11-8) as a parametrization of Sϕ; also see Section [3.2.](#page-3-3) Furthermore, as we want UNOT to work across datasets, we require a generator G<sup>θ</sup> that can provably generate any pair of distributions during training (Section [3.3\)](#page-3-0). In Section [3.4,](#page-4-0) we construct an adversarial training objective for S<sup>ϕ</sup> and Gθ. Further details about hyperparameter and architecture choices can be found in Appendix [C.](#page-26-0) The implementation and model weights are available at [https:](https://github.com/GregorKornhardt/UNOT) [//github.com/GregorKornhardt/UNOT](https://github.com/GregorKornhardt/UNOT).

### <span id="page-2-0"></span>3.1. Convergence of Dual Potentials

In this section, we prove convergence of the discrete dual potentials g<sup>n</sup> as n goes to infinity. For brevity, this section is kept informal; see Appendix [B](#page-20-0) for a formal treatment. Assume now that X = Y ⊆ R <sup>N</sup> is compact, and c(x, y) is Lipschitz continuous in both its arguments. For absolutely continuous µ, ν ∈ P(X ), denote by (µn)n∈<sup>N</sup>, (νn)n∈<sup>N</sup> ⊂ P(X ) *discretizing sequences* of µ and ν (formally defined in

<span id="page-2-4"></span><sup>3</sup>Note that while we consider images as an example, the learning task is the same for any setting where discrete measures of varying resolution share an underlying continuous cost function, which arises in settings such as single-cell genomics, fluid dynamics, point cloud processing, or economics.

Appendix [B\)](#page-20-0). While a solution (fn, gn) of the discrete dual problem between µ<sup>n</sup> and ν<sup>n</sup> is only defined µ<sup>n</sup> - resp. ν<sup>n</sup> a.e., it can be canonically extended to all of X [\(Feydy et al.,](#page-10-6) [2018\)](#page-10-6) (see Appendix [B](#page-20-0) for details). The following proposition shows that the extended potentials (fn, gn) converge to the solution (f, g) of the continuous entropic problem.

<span id="page-3-4"></span>Proposition 2. *(Informal) Let* (µn)n∈<sup>N</sup>*,* (νn)n∈<sup>N</sup> *be discretizing sequences for absolutely continuous* µ, ν ∈ P(X )*. Let* (fn, gn) *be the (unique) extended dual potentials of* (µn, νn) *such that* fn(x0) = 0 *for some* x<sup>0</sup> ∈ X *and all* n*. Let* (f, g) *be the (unique) dual potentials of* (µ, ν) *such that* f(x0) = 0*. Then* f<sup>n</sup> *and* g<sup>n</sup> *converge uniformly to* f *and* g *on all of* X *.*

A formal version and its proof can be found in Appendix [B.](#page-20-0) This proposition is crucial in designing our network Sϕ, as we discuss in the following section.

### <span id="page-3-3"></span>3.2. Fourier Neural Operators

Fourier Neural Operators (FNOs) [\(Kovachki et al.,](#page-11-8) [2024\)](#page-11-8) are neural networks mapping between infinite-dimensional function spaces. More precisely, a neural operator is a map F : A → U between Banach spaces A and U of functions a ∈ A : D<sup>a</sup> → R d ′ <sup>a</sup> and u : D<sup>u</sup> → R d ′ <sup>u</sup> respectively, for bounded domains D<sup>a</sup> ⊂ R <sup>d</sup><sup>a</sup> and D<sup>u</sup> ⊂ R <sup>d</sup><sup>u</sup> . An input function a ∈ A evaluated at points x1, ..., x<sup>n</sup> ∈ R <sup>d</sup><sup>a</sup> can be encoded as a vector a = [a(x1), ..., a(xn)] ∈ R n×d ′ <sup>a</sup> ; the same applies to the output function u ∈ U, which can be written as u = [u(y1), ..., u(ym)] ∈ R m×d ′ <sup>u</sup> , corresponding to the values at y1, ..., y<sup>m</sup> ∈ R <sup>d</sup><sup>u</sup> . At its core, an FNO applies a sequence of L "kernel layers" to the input vector a. In each of these layers, a fixed number of Fourier features of the discrete Fourier transform of the input is computed, the features are transformed by a (C-valued) linear layer (we use a two-layer network in practice instead, as we found it to improve performance), and then mapped back by the inverse Fourier transform. Importantly, neural operators are by construction discretization-invariant when inputs and outputs correspond to discretizations of underlying functions. This is exactly what Proposition [2](#page-3-4) guarantees: the dual potentials corresponding to measures µ<sup>n</sup> and ν<sup>n</sup> converge uniformly to the continuous potentials corresponding to the limiting distributions µ and ν as the resolution of µ<sup>n</sup> and ν<sup>n</sup> increases. Hence, FNOs are a natural choice of architecture in our setting. More details on FNOs, and how we implemented Sϕ, can be found in Appendix [A.5.](#page-17-0)

### <span id="page-3-0"></span>3.3. Generating Measures for Training

UNOT is trained on pairs of distributions generated by a generator network G<sup>θ</sup> of the following form:

$$
G_{\theta}: \mathbb{R}^{d} \to \mathcal{P}(\mathcal{X}) \times \mathcal{P}(\mathcal{X})
$$
  
$$
z \sim \rho_{z} \mapsto R \left[ \text{ReLU} \left( \text{NN}_{\theta}(z) + \lambda I_{d,d'}(z) \right) + \delta \right], \quad (6)
$$

where ρ<sup>z</sup> = N (0, Id) is a Gaussian prior, NN<sup>θ</sup> is a trainable neural network (in practice, we use a 5-layer fully connected MLP, see Appendix [C\)](#page-26-0), Id,d′ is an interpolation operator matching the generator's output dimension d ′ and acting as a skip connection reminiscent of ResNets [\(He et al.,](#page-10-7) [2016\)](#page-10-7), and λ > 0 is a constant for the skip connection. δ > 0 is a small constant needed to generate our targets with the Sinkhorn algorithm, as outlined in Section [3.4.](#page-4-0) R denotes renormalizing to two probability measures and downsampling them to random dimensions in a set range, such that S<sup>ϕ</sup> trains on measures of varying resolutions, which is known to improve NO training [\(Li et al.,](#page-11-13) [2024a\)](#page-11-13). More specifically, if we write [x1, x2] = ReLU (NNθ(z) + λ Id,d′ (z)) + δ for two vectors x<sup>1</sup> and x<sup>2</sup> of equal size (say both with n samples), R first maps them to [x1/ P i (x1)<sup>i</sup> , x2/ P i (x2)<sup>i</sup> ] and then uses 2D bilinear interpolation to downsample them to m samples each. The generator is universal in the following sense:

<span id="page-3-1"></span>Theorem 3. *Let* 0 < λ ≤ 1 *and* G<sup>θ</sup> : R <sup>d</sup> → R <sup>d</sup> *be defined via*

$$
G_{\theta}(z) = \text{ReLU}(NN_{\theta}(z) + \lambda z),
$$

*where* z ∼ ρ<sup>z</sup> = N (0, I)*, and where* NN<sup>θ</sup> : R <sup>d</sup> → R d *is Lipschitz continuous with* Lip(NNθ) = L < λ*. Then* G<sup>θ</sup> *is Lipschitz continuous with* Lip(q) < L + λ*, and* G˜(z) := NNθ(z) + λz *is invertible on* R d *. Furthermore, for any* x ∈ R d ≥0 *it holds*

$$
\rho_{G_{\boldsymbol{\theta} \# \rho_{\boldsymbol{z}}}}(\boldsymbol{x}) \geq \frac{1}{(L+\lambda)^d} \mathcal{N}\left(\tilde{\mathrm{G}}_{\boldsymbol{\theta}}^{-1}(\boldsymbol{x}) | 0, I\right).
$$

*In other words,* Gθ#ρ<sup>z</sup> *has positive density at any nonnegative* x ∈ R d ≥0 *.*

This shows that any pair of discrete probability measures (µ, ν) of joint dimension d can be generated by Gθ. A direct consequence of the theorem is an extension to functions that are compositions of functions G˜ <sup>θ</sup> as above, which covers a wide class of ResNets. Both proofs can be found in Appendix [B.](#page-20-0)

<span id="page-3-2"></span>Corollary 4. *Let* G˜ <sup>θ</sup> = G˜ <sup>θ</sup><sup>1</sup> ◦ G˜ <sup>θ</sup><sup>1</sup> ◦ ... ◦ G˜ <sup>θ</sup><sup>R</sup> *be a composition of functions* G˜ θi *, each of which is of the form as in Theorem [3.](#page-3-1) Let* z ∼ ρ<sup>z</sup> = N (0, I)*. Then*

$$
\rho_{\tilde{G}_{\theta\#}\rho_{\mathbf{z}}}(\mathbf{x}) \geq \frac{1}{(L+\lambda)^{Rd}} \mathcal{N}\left(\tilde{\mathbf{G}}_{\theta}^{\phantom{-1}-1}(\mathbf{x})|0,I\right)
$$

*for any* x ∈ R d *. As in Theorem [3,](#page-3-1) this also holds for any* x ∈ R d ≥0 *if* G˜ <sup>θ</sup> *is followed by a ReLU activation.*

<span id="page-3-5"></span>Although the more general Corollary [4](#page-3-2) is not needed for our purposes, it might be of independent interest to the research community. Note that the generator in Theorem [3](#page-3-1) does not exactly match our generator's architecture. A discussion of how the theorem relates to our setting, as well as further details on the generator, can be found in Appendix [C.](#page-26-0)

![](_page_4_Figure_1.jpeg)

Figure 2. Generated pair of training samples (lighter=more mass).

Figure [2](#page-4-3) shows a pair of samples generated by Gθ. The generator seems to layer highly structured shapes with more blurry ones. More examples, as well as an analysis of the performance of S<sup>ϕ</sup> on samples generated by G<sup>θ</sup> over the course of training, can be found in Appendix [D.6.](#page-32-0)

### <span id="page-4-0"></span>3.4. UNOT Training Algorithm

Given a pair of distributions (µ, ν) = Gθ(z) (in this section, we will remove the subscript n for clarity), Sϕ(µ, ν) =: g<sup>ϕ</sup> should predict the true dual potential g associated with µ and ν. Hence, we could simply compute the true potential g with the Sinkhorn algorithm and use L2(gϕ, g) := ∥g<sup>ϕ</sup> − g∥ 2 2 as our training loss. However, it would be prohibitively expensive to run the Sinkhorn algorithm until convergence. Hence, we instead employ a bootstrapping loss on the prediction gϕ. Let τ<sup>k</sup> : (µ, ν, gϕ) 7→ gτ<sup>k</sup> denote running the Sinkhorn algorithm on (µ, ν) with initialization v <sup>0</sup> = exp(gϕ/ϵ) for a very small number of iterations k, i.e. warmstarting the Sinkhorn algorithm with the current prediction gϕ, and returning ϵ log v = gϕ. [4](#page-4-4) To ensure uniqueness and improve training, we shift gτ<sup>k</sup> to have zero sum; this corresponds to the non-uniqueness of the dual potentials, see Proposition [1.](#page-2-2) Minimizing L2(gϕ, gτ<sup>k</sup> ) implies minimizing the ground truth loss L2(gϕ, g) against the true potential g.

<span id="page-4-2"></span>Proposition 5. *For two discrete measures* (µ, ν) *with* n *particles, let* g *be an optimal dual potential,* g<sup>ϕ</sup> = Sϕ(µ, ν)*, and* gτ<sup>k</sup> = τk(µ, ν, gϕ)*. Without loss of generality, assume that* P i g<sup>i</sup> = P i g<sup>τ</sup><sup>k</sup> <sup>i</sup> = 0*. Then*

$$
L_2(\boldsymbol{g}_{\boldsymbol{\phi}},\boldsymbol{g}) \leq c(K,k,n) L_2(\boldsymbol{g}_{\boldsymbol{\phi}},\boldsymbol{g}_{\tau_k})
$$

*for some constant* c(K, k, n) > 1 *depending only on the Gibbs kernel* K*,* k *and* n*.*

The proposition shows that minimizing L2(gϕ, g<sup>τ</sup><sup>k</sup> ) implies minimizing L2(gϕ, g), i.e. the loss between the prediction and the ground truth potential. The proof is based on the Hilbert projective metric [\(Peyre & Cuturi](#page-11-1) ´ , [2019\)](#page-11-1) and can be found in Appendix [B.](#page-20-0)

Training objective. Having defined the loss for Sϕ, as well

<span id="page-4-5"></span><span id="page-4-3"></span>

| Algorithm 2 UNOT Training Algorithm                           |
|---------------------------------------------------------------|
| 1: in cost c, reg parameter ϵ, prior ρz, learning rates {αi}i |
| {βi}i<br>, Sinkhorn target generator τk                       |
| 2: for i = 1, 2, , T do                                       |
| z ← sample(ρz)<br>3:                                          |
| (µ, ν) ← Gθ(z)<br>4:                                          |
| b<br>b<br>for mini-batch (µ<br>, ν<br>) in (µ, ν) do<br>5:    |
| b<br>b<br>← Sϕ(µ<br>gϕ<br>, ν<br>)<br>6:                      |
| b<br>b<br>gτk<br>← τk(µ<br>, ν<br>, gϕ)<br>7:                 |
| ϕ ← ϕ − αi∇ϕ<br>L2(gτk<br>, gϕ)<br>8:                         |
| end for<br>9:                                                 |
| b<br>for mini-batch z<br>in z do<br>10:                       |
| b<br>(µθ, νθ) ← Gθ(z<br>)<br>11:                              |
| ← Sϕ(µθ, νθ)<br>gθ<br>12:                                     |
| gτk<br>← τk(µθ, νθ, gθ)<br>13:                                |
| θ ← θ + βi∇θ<br>L2(gτk<br>, gθ)<br>14:                        |
| end for<br>15:                                                |
| 16: end for                                                   |

,

as the target generation procedure, the training objective for S<sup>ϕ</sup> and G<sup>θ</sup> consists of S<sup>ϕ</sup> trying to minimize the loss L2(gϕ, g), while G<sup>θ</sup> attempts to maximize it, similar to the training objective in GANs [\(Goodfellow et al.,](#page-10-8) [2014\)](#page-10-8). Putting everything together, our adversarial training objective for S<sup>ϕ</sup> and G<sup>θ</sup> reads

<span id="page-4-6"></span>
$$
\max_{\theta} \min_{\phi} \mathbb{E}_{\mathbf{z} \sim \rho_{\mathbf{z}}} \left[ L_2 \left( \tau_k \left( \mathbf{G}(\mathbf{z}), \mathbf{S}(\mathbf{G}(\mathbf{z})) \right), \mathbf{S}_{\phi}(\mathbf{G}_{\theta}(\mathbf{z})) \right) \right],\tag{7}
$$

where S and G without subscripts denote no gradient tracking, as the target is not backpropagated through. The training algorithm can be seen in Algorithm [2.](#page-4-5) In practice, training will be batched, which we omitted for clarity. Note that vectors g with subscripts θ or ϕ are backpropagated through with respect to these parameters, whereas target vectors (with subscript τk) are not.

# <span id="page-4-1"></span>4. Experiments

Training Details. We test UNOT in three different settings: a) with c(x, y) = ∥x − y∥ 2 2 on the unit square X = [0, 1]<sup>2</sup> ; b) with c(x, y) = ∥x − y∥<sup>2</sup> on [0, 1]<sup>2</sup> ; c) with the *spherical distance* c(x, y) = arccos(⟨x, y⟩) on the unit sphere S <sup>2</sup> = {x ∈ R 3 : ∥x∥ = 1}. For each of these settings, we train a separate model on 200M samples z, where training samples (µ, ν) are between 10×10 and 64×64 dimensional (randomly downsampled in Gθ). Training takes around 35h on an H100 GPU. S<sup>ϕ</sup> is an FNO with 26M parameters optimized with AdamW [\(Loshchilov & Hutter,](#page-11-14) [2019\)](#page-11-14); G<sup>θ</sup> is a fully connected MLP with 272k parameters optimized with Adam [\(Kingma & Ba,](#page-10-9) [2017\)](#page-10-9). In the spherical setting c(x, y) = arccos(⟨x, y⟩) we parametrize S<sup>ϕ</sup> with a *Spherical FNO* (SFNO) [\(Bonev et al.,](#page-9-7) [2023\)](#page-9-7) instead, which is essentially an FNO adapted to the sphere; for more details

<span id="page-4-4"></span><sup>4</sup>The Sinkhorn algorithm requires input measures to be positive; this is the reason we add the constant δ > 0 in the generator.

UNOT (OURS) ONES GAUSS MNIST 3 ± 5 16 ± 9 10 ± 7 CIFAR 3 ± 6 80 ± 22 52 ± 19 CIFAR-MNIST 4 ± 4 32 ± 15 13 ± 9 LFW 7 ± 8 78 ± 20 35 ± 14 BEAR 4 ± 6 41 ± 16 25 ± 13 LFW-BEAR 4 ± 6 53 ± 18 29 ± 13

<span id="page-5-4"></span>Table 1. Mean number of iterations needed to achieve 0.01 relative error on the OT distance for c(x, y) = ∥x − y∥ 2 .

<span id="page-5-5"></span>Table 2. Relative speedup of Sinkhorn with UNOT and cost c(x, y) = ∥x − y∥ 2 . Time in s to achieve 0.01 relative error on the OT distance.

|             | UNOT (OURS) | ONES       | SPEEDUP |
|-------------|-------------|------------|---------|
| MNIST       | 1.2 · 10−3  | 1.5 · 10−3 | 1.25    |
| CIFAR       | 9.5 · 10−4  | 7.1 · 10−3 | 7.4     |
| CIFAR-MNIST | 1.3 · 10−3  | 2.7 · 10−3 | 2.07    |
| LFW         | 3.0 · 10−3  | 1.5 · 10−2 | 5       |
| BEAR        | 2.6 · 10−3  | 1.0 · 10−2 | 3.8     |
| LFW-BEAR    | 2.7 · 10−3  | 1.2 · 10−2 | 4.4     |

on FNOs and SFNOs see Appendix [A.5.](#page-17-0) We highlight that S<sup>ϕ</sup> is relatively small, such that its runtime vanishes compared to the runtime of even just a few Sinkhorn iterations, making it much cheaper to run than Sinkhorn (see Section [4.1\)](#page-5-0). We set k (the number of Sinkhorn iterations in τk) to 5, and ϵ = 0.01. Additional training details can be found in Appendix [C.](#page-26-0)

We demonstrate the performance of the three models on various tasks, such as predicting transport distances, initializing the Sinkhorn algorithm, computing Sinkhorn divergence barycenters, and approximating Wasserstein geodesics. For the Euclidean settings a) and b) (from above), we view images as discrete distributions on the unit square, and test on MNIST (28×28), grayscale CIFAR10 (28×28), the teddy bear class from the [Google Quick, Draw!](https://github.com/googlecreativelab/quickdraw-dataset) dataset (64×64), and Labeled Faces in the Wild (LFW, 64×64), as well as cross-datasets CIFAR-MNIST and LFW-Bear (where µ comes from one dataset and ν from the other). For the spherical setting c), we project these images onto the unit sphere in R 3 (for details, see Appendix [D.1\)](#page-28-0). Unless otherwise noted, we perform a single Sinkhorn iteration on g = Sϕ(µ, ν) in all experiments in order to compute the second potential f. Errors are averaged over 500 samples. Additional experiments, including a sweep over input sizes 10 × 10 to 64 × 64, as well as variants of UNOT for fixed input dimension or variable ϵ, can be found in Appendix [D.](#page-28-1)

### <span id="page-5-0"></span>4.1. Predicting Transport Distances

We compare the convergence of the Sinkhorn algorithm in terms of relative error on the transport distance OTϵ(µ, ν) for our learned initialization v <sup>0</sup> = exp(Sϕ(µ, ν)/ϵ) to

![](_page_5_Figure_9.jpeg)

<span id="page-5-3"></span>Figure 3. Relative error on the OT distance for Sinkhorn with our initialization (UNOT), compared to the default (Ones) and Gaussian initialization (Gauss) [\(Thornton & Cuturi,](#page-11-4) [2022\)](#page-11-4).

the default initialization 1<sup>n</sup> and the Gaussian initialization from [\(Thornton & Cuturi,](#page-11-4) [2022\)](#page-11-4), which is based on closed-form solutions for Gaussian distributions. Note that the Gaussian initialization is only valid for c(x, y) = ∥x − y∥ 2 , hence we omit it when c(x, y) = ∥x − y∥ or c(x, y) = arccos(⟨x, y⟩). [5](#page-5-1) We do not compare to Meta OT [\(Amos et al.,](#page-9-5) [2023\)](#page-9-5) here, as their approach is inherently dataset dependent and breaks down when testing on out-of-distribution data.[6](#page-5-2) For completeness, we include a detailed comparison in Appendix [D.2,](#page-28-2) which shows that UNOT significantly outperforms Meta OT on all datasets except MNIST, the training dataset of Meta OT. Surprisingly, UNOT also almost matches Meta OT on MNIST, despite not having seen any MNIST samples during training, while Meta OT was explicitly trained on them.

Figure [1](#page-0-2) (Section [1\)](#page-0-3) shows the relative error on OTϵ(µ, ν) after *a single* Sinkhorn iteration for c(x, y) = ∥x − y∥ 2 , and Figure [4](#page-6-0) shows the same plot for c(x, y) = ∥x − y∥ on the square, and c(x, y) = arccos(⟨x, y⟩) on the sphere. In Figure [3,](#page-5-3) we plot the relative error on the OT distance over the number of Sinkhorn iterations for c(x, y) = ∥x − y∥ 2 (for the equivalent plots for the other cost functions, please see Appendix [D.7\)](#page-33-0), demonstrating that UNOT can be used as a state-of-the-art initialization. Table [1](#page-5-4) shows the average number of Sinkhorn iterations needed to achieve 0.01 relative error on OTϵ(µ, ν) for c(x, y) = ∥x − y∥ 2 . In Table [2](#page-5-5) we show the relative speedup achieved by initializing the Sinkhorn algorithm with UNOT implemented in JAX over the default initialization (on a batch size of 64 in float32

<span id="page-5-1"></span><sup>5</sup> If the cost function is not ∥x − y∥ 2 , the Gaussian initialization is not theoretically justified. Empirically, we noted that it behaves similar to the default initialization in these cases.

<span id="page-5-2"></span><sup>6</sup>We note that it should be possible to finetune UNOT on specific datasets as well; however, we have not tested this.

![](_page_6_Figure_1.jpeg)

Figure 4. Error on the OT distance after a single Sinkhorn iteration with UNOT vs. the default initialization (Ones) for cost ∥x − y∥ on the square [0, 1]<sup>2</sup> (left) and arccos(⟨x, y⟩) on the sphere {x ∈ R 3 : ∥x∥ = 1} (right).

![](_page_6_Figure_3.jpeg)

<span id="page-6-7"></span>Figure 5. Sinkhorn divergence barycenters computed with UNOT via eq. [\(10\)](#page-6-1) (top) vs. ground truth (bottom) of between 5 to 10 MNIST samples of the same digit per barycenter.

on an NVIDIA 4090). We achieve an average speedup of 3.57 on 28 × 28 datasets and 4.4 on 64 × 64 datasets.[7](#page-6-2) For comparison, the relative speedup achieved in [\(Amos et al.,](#page-9-5) [2023\)](#page-9-5) was 1.96 (for a model trained only on MNIST).

### <span id="page-6-9"></span>4.2. Sinkhorn Divergence Barycenters

The *Wasserstein barycenter* for a set of measures {ν1, ..., ν<sup>N</sup> } ⊂ P2(X ) and λ ∈ ∆<sup>n</sup>−<sup>1</sup> is defined as

<span id="page-6-8"></span>
$$
\mu = \underset{\mu' \in \mathcal{P}_2(X)}{\arg \min} \sum_i \lambda_i W_2^2(\mu', \nu_i). \tag{8}
$$

To make this problem tractable, consider the Sinkhorn divergence barycenter

<span id="page-6-5"></span><span id="page-6-0"></span>
$$
\mu = \underset{\mu' \in \mathcal{P}_2(X)}{\arg \min} \sum_i \lambda_i \, \text{SD}_{\epsilon}(\mu', \nu_i),\tag{9}
$$

where the *Sinkhorn divergence*[8](#page-6-3) between µ and ν is

$$
SD_{\epsilon}(\mu, \nu) = OT_{\epsilon}(\mu, \nu) - \frac{1}{2} OT_{\epsilon}(\mu, \mu) - \frac{1}{2} OT_{\epsilon}(\nu, \nu).
$$

Now for discrete measures µ, ν, denote by (f, g) the dual potentials for OTϵ(µ, ν), and by p that for OTϵ(µ, µ). [9](#page-6-4) Writing µ = P <sup>i</sup> aiδx<sup>i</sup> for some a ∈ R <sup>n</sup>, the gradient of [\(9\)](#page-6-5) w.r.t a is given by (cf. [\(Feydy et al.,](#page-10-6) [2018\)](#page-10-6)):

<span id="page-6-1"></span>
$$
\nabla_{\mathbf{a}} \text{SD}_{\epsilon}(\boldsymbol{\mu}, \boldsymbol{\nu}) = \boldsymbol{f} - \boldsymbol{p}.\tag{10}
$$

Hence, we can solve [\(9\)](#page-6-5) with (projected) gradient descent, where S<sup>ϕ</sup> predicts f and p in [\(10\)](#page-6-1). [10](#page-6-6) Further details and a pseudocode can be found in Appendix [A.2.](#page-14-0) Throughout this section, we set c(x, y) = ∥x − y∥ 2 , and always run 200 gradient steps using gradients from [\(10\)](#page-6-1). Figure [5](#page-6-7) shows UNOT barycenters vs. the true barycenters (computed with the POT library) of between 5 and 10 MNIST samples of the same digit per barycenter. In Appendix [D.7,](#page-33-0) we also provide quantitative results for barycenters with different initializations. In Figure [6,](#page-7-0) we show barycenters computed between four shapes. UNOT accurately predicting barycenters demonstrates it captures the geometry of the Wasserstein space beyond predicting distances.

<span id="page-6-2"></span><sup>7</sup>We did not optimize the network S<sup>ϕ</sup> much for efficiency, and more efficient implementations likely exist. Note that FNOs process complex numbers, but PyTorch is heavily optimized for real number operations. With kernel support for complex numbers, UNOT will likely be much faster. In addition, computation times can vary significantly across hardware, batch sizes, precision, etc.

<span id="page-6-3"></span><sup>8</sup> It can be seen as a *debiased* version of OTϵ(µ, ν), and we use it as an approximation of the squared Wasserstein distance.

<span id="page-6-4"></span><sup>9</sup> If both measures are identical, the dual potentials can be chosen to be identical as well.

<span id="page-6-6"></span><sup>10</sup>To be precise, this solves the barycenter problem on the discrete space {x1, ..., xn}.

![](_page_7_Figure_1.jpeg)

Figure 6. UNOT barycenters computed between four shapes (corners) by linearly interpolating λ = (λ1, λ2, λ3, λ4) from eq. [\(9\)](#page-6-5) between the four unit vectors, and solving via eq. [\(10\)](#page-6-1) with UNOT.

### <span id="page-7-3"></span>4.3. Calculating Geodesics

Let µ, ν ∈ P2(X ) be two measures such that ν = T#µ for an *optimal transport map* T : X → X (which exists for the non-entropic optimal transport problem under certain conditions, see Appendix [A.1\)](#page-13-1). The *Wasserstein geodesic* between µ and ν, also called *McCann interpolation*, is the constant-speed geodesic between µ and ν and given by

$$
\mu_t : [0,1] \to \mathcal{P}_2(\mathcal{X}), \quad t \mapsto [(1-t)\mathrm{Id} + tT]_{\#}\mu.
$$

It can be interpreted as the shortest path between µ and ν. The Wasserstein barycenter [\(8\)](#page-6-8) between (µ,(1 − t)) and (ν, t) (i.e. where 1−t and t are the weights λ<sup>i</sup> from equation [\(8\)](#page-6-8)) turns out to be equal to µ<sup>t</sup> [\(Agueh & Carlier,](#page-9-8) [2011\)](#page-9-8). This gives us two methods to approximate the Wasserstein geodesic between µ and ν: Either by iteratively computing barycenters as in Section [4.2,](#page-6-9) or by computing the (entropic) transport plan from equation [\(4\)](#page-2-5) as an approximation to T (we are leaving out some technicalities for brevity here, which can be found in Appendix [A.3\)](#page-15-0). We compare the geodesics computed by UNOT to the ground truth geodesic (obtained from the true OT plan), as well as to GeONet [\(Gracyk & Chen,](#page-10-5) [2024\)](#page-10-5), a recently proposed framework that also uses Neural Operators to learn Wasserstein geodesics *directly* by parametrizing a coupled PDE system encoding the optimality conditions of the dynamic OT problem. Akin to [\(Amos et al.,](#page-9-5) [2023\)](#page-9-5), GeONet is inherently dataset dependent. Figure [8](#page-8-1) shows the McCann interpolation between two MNIST digits using the ground truth OT plan, the OT plan computed by UNOT, barycenters computed by UNOT, and the GeONet geodesic, where we use the UNOT model trained with c(x, y) = ∥x − y∥ 2 again. We see that despite

![](_page_7_Picture_7.jpeg)

Figure 7. Sinkhorn divergence particle flow between distributions of images, from noise to LFW (64x64). Gradients computed via eq. [\(11\)](#page-7-1) and [\(10\)](#page-6-1) with UNOT. Bottom row is target images.

<span id="page-7-2"></span><span id="page-7-0"></span>GeONet being *trained to predict geodesics on MNIST*, while UNOT *does not train on geodesics, nor on MNIST*, both geodesics computed by UNOT are significantly closer to the ground truth than the GeONet geodesic.

### <span id="page-7-4"></span>4.4. Wasserstein on Wasserstein Gradient Flow

Oftentimes in machine learning, the distributions of interest are not images, but *distributions over images*, such as in generative modeling. In this experiment, we show that UNOT can successfully transport distributions over images as well. Let µ, ˆ νˆ ∈ P2((P2([0, 1]<sup>2</sup> ), c), W2), i.e. the space of distributions over images equipped with the Wasserstein distance (and P([0, 1]<sup>2</sup> ) being equipped with c(x, y) = ∥x − y∥ 2 ). Denote by SDˆ <sup>ϵ</sup>(ˆµ, νˆ) the Sinkhorn divergence between µˆ and νˆ, where we use SDϵ(µ, ν) as the ground cost between µ, ν ∈ P2([0, 1]<sup>2</sup> ) as an approximation of W<sup>2</sup> 2 (µ, ν). Writing µˆ = 1 n P<sup>n</sup> i δµ<sup>i</sup> , νˆ = 1 n P<sup>n</sup> j δνj for µi , ν<sup>j</sup> ∈ P2([0, 1]<sup>2</sup> ), we let UNOT approximate the particle flow <sup>∂</sup> ∂tµˆ<sup>t</sup> = −∇µˆ<sup>t</sup> [SDˆ <sup>ϵ</sup>(ˆµt, νˆ)], for which we can derive the gradient via (see [\(Li et al.,](#page-11-15) [2024b\)](#page-11-15)):

<span id="page-7-1"></span>
$$
\frac{\partial \hat{\text{SD}}_{\epsilon}(\hat{\mu}, \hat{\nu})}{\partial \mu_k} = \sum_j \frac{\partial \text{SD}_{\epsilon}(\mu_k, \nu_j)}{\partial \mu_k} \Pi_{kj}, \quad k = 1, ..., n,
$$
\n(11)

where Πkj is an optimal transport plan between µ<sup>k</sup> and ν<sup>j</sup> . These gradients can be approximated by UNOT via equation [\(10\)](#page-6-1) as before; further details can be found in Appendix [A.4.](#page-17-1) In Figure [7,](#page-7-2) we plot the particle flow from Gaussian noise µˆ to a distribution νˆ over 10 images, where we visualize µˆ<sup>t</sup> after every 10 gradient steps (using AdamW [\(Loshchilov &](#page-11-14) [Hutter,](#page-11-14) [2019\)](#page-11-14) with gradients computed via equation [\(10\)](#page-6-1)). We can see that the UNOT flow converges quickly.

![](_page_8_Figure_1.jpeg)

<span id="page-8-1"></span>Figure 8. McCann interpolations computed with the true OT plan, UNOT OT plan, UNOT barycenters, and GeONet (top to bottom).

## <span id="page-8-0"></span>5. Related Work

Neural OT. Typically, neural OT approaches aim at solving individual instances of (high-dimensional) OT problems. In [\(Korotin et al.,](#page-11-10) [2023\)](#page-11-10), a maximin formulation for the dual problem is derived and two networks, parametrizing the transport plan and the dual potential resp., are trained adversarially. In [\(Bunne et al.,](#page-9-4) [2023a\)](#page-9-4), transport maps between continuous input distributions conditioned on a context variable are learned. Another interesting recent paper [\(Uscidda](#page-11-9) [& Cuturi,](#page-11-9) [2023\)](#page-11-9) suggests a universal regularizer, called the *Monge gap*, to learn OT maps and distances. Unlike these works, we focus on *generalizing across* OT problems.

Initializing Sinkhorn. There exists very little literature on initializing the Sinkhorn algorithm. [\(Thornton & Cuturi,](#page-11-4) [2022\)](#page-11-4) propose using dual vectors recovered from the unregularized 1D optimal transport problem, or from closed-form transport maps in a Gaussian (mixture) setting, and were able to significantly speed up convergence. [\(Amos et al.,](#page-9-5) [2023\)](#page-9-5) propose a neural approach, training a single network to predict the optimal dual potential f of the discrete dual problem, and their loss is simply the (negative) dual objective [\(3\)](#page-1-1). This approach works well when training on low-dimensional datasets such as MNIST, and is elegant as it does not require ground truth potentials, i.e. is fully unsupervised, but it is not able to generalize to out-of-distribution data, and can only be used for input measures of fixed size.

OT for Machine Learning. Leveraging OT to formulate new machine learning methods has seen a surge in popularity in recent years, and it has been applied to a wide range of problems. Relevant works include the celebrated Wasserstein GAN [\(Arjovsky et al.,](#page-9-9) [2017\)](#page-9-9), multi-label learning [\(Frogner et al.,](#page-10-10) [2015\)](#page-10-10), inverse problems in physics [\(En](#page-10-11)[gquist & Yang,](#page-10-11) [2019\)](#page-10-11), point cloud processing [\(Geuter et al.,](#page-10-12) [2025;](#page-10-12) [Fishman et al.,](#page-10-13) [2025\)](#page-10-13), or few-shot image classification to compute distances between images [\(Zhang et al.,](#page-12-1) [2020\)](#page-12-1). In flow matching OT can be used to straighten paths [\(Lipman et al.,](#page-11-16) [2023;](#page-11-16) [Tong et al.,](#page-11-5) [2024;](#page-11-5) [Pooladian et al.,](#page-11-6) [2023\)](#page-11-6). Approximating Wasserstein gradient flows with the JKO scheme has been explored in numerous works [\(Alvarez-](#page-9-1)[Melis & Fusi,](#page-9-1) [2021;](#page-9-1) [Alvarez-Melis et al.,](#page-9-10) [2022;](#page-9-10) [Bunne et al.,](#page-9-2) [2022;](#page-9-2) [Choi et al.,](#page-9-11) [2024\)](#page-9-11). The theory of Wasserstein gradient flows has also been used to study learning dynamics in various settings, such as for overparametrized two-layer networks [\(Chizat & Bach,](#page-9-12) [2018\)](#page-9-12) or simplified transformers [\(Geshkovski et al.,](#page-10-14) [2024\)](#page-10-14).

Generative Adversarial Networks. GANs [\(Goodfellow](#page-10-8) [et al.,](#page-10-8) [2014\)](#page-10-8), like other types of generative models, aim at generating samples from a distribution ρdata, given access to a finite number of samples. In contrast, we do not have access to samples from the target distribution. However, our loss function [\(7\)](#page-4-6) shares similarities with the adversarial GAN loss. Given prior samples z ∼ ρ<sup>z</sup> and data samples x ∼ ρdata, the GAN objective for a generator G is

$$
\min_{\mathrm{G}} \max_{\mathrm{D}} \mathbb{E}_{\bm{x} \sim \rho_{\text{data}}} \left[ \log \mathrm{D}(\bm{x}) \right] + \mathbb{E}_{\bm{z} \sim \rho_{\bm{z}}} \left[ \log (1 - \mathrm{D}(\mathrm{G}(\bm{z})) ) \right],
$$

where D is the *discriminator*, which predicts the probability that a sample came from the target distribution rather than the generator. Note that while our generator *maximizes* the objective, the GAN generator *minimizes* it.

## 6. Discussion

We presented UNOT, a neural OT solver capable of solving entropic OT problems universally across datasets, for a given cost function. Leveraging Neural Operators, UNOT can process distributions of varying resolutions supported on grids. UNOT's training involves a *generator* network G<sup>θ</sup> producing synthetic training samples for the predictive network Sϕ, where both networks are trained jointly via a self-supervised adversarial loss. S<sup>ϕ</sup> predicts the potential of the dual OT problem, and our training objective provably minimizes the loss w.r.t. the ground truth potentials. We show that UNOT is universal in the sense that the generator can create any discrete distributions during training, and empirically verify this through experiments on Euclidean and non-Euclidean image datasets of varying resolutions. UNOT consistently predicts OT distances up to 1-3% relative error, and approximates barycenters and geodesics in Wasserstein space by solving for the OT plan. Furthermore, we demonstrate that UNOT can be used as a state-of-the-art initialization for the Sinkhorn algorithm, achieving speedups of up to 7.4×. Current limitations are that UNOT does not extrapolate well to measures with significantly higher resolutions than the training samples, nor generalizes to cost functions other than the training cost. Scaling UNOT to higher resolutions, as well as applying it to other data modalities or non-uniform grids, are interesting directions for future research.

## Acknowledgements

For this work, Vaios Laschos has been funded by Deutsche Forschungsgemeinschaft (DFG) - Project-ID 318763901 - SFB1294.

# Impact Statement

This paper presents work whose goal is to advance the field of Machine Learning. There are many potential societal consequences of our work, as optimal transport has a vast range of applications, but none of these we feel must be specifically highlighted here.

## References

- <span id="page-9-8"></span>Agueh, M. and Carlier, G. Barycenters in the Wasserstein space. *SIAM Journal on Mathematical Analysis*, 43(2): 904–924, 2011. doi: 10.1137/100805741. URL [https:](https://doi.org/10.1137/100805741) [//doi.org/10.1137/100805741](https://doi.org/10.1137/100805741).
- <span id="page-9-1"></span>Alvarez-Melis, D. and Fusi, N. Dataset Dynamics via Gradient Flows in Probability Space. In Meila, M. and Zhang, T. (eds.), *Proceedings of the 38th International Conference on Machine Learning*, volume 139 of *Proceedings of Machine Learning Research*, pp. 219–230. PMLR, 18– 24 Jul 2021. URL [https://proceedings.mlr.](https://proceedings.mlr.press/v139/alvarez-melis21a.html) [press/v139/alvarez-melis21a.html](https://proceedings.mlr.press/v139/alvarez-melis21a.html).
- <span id="page-9-10"></span>Alvarez-Melis, D., Schiff, Y., and Mroueh, Y. Optimizing Functionals on the Space of Probabilities with Input Convex Neural Networks. *Transactions on Machine Learning Research*, 2022. URL [https://openreview.net/](https://openreview.net/forum?id=dpOYN7o8Jm) [forum?id=dpOYN7o8Jm](https://openreview.net/forum?id=dpOYN7o8Jm).
- <span id="page-9-5"></span>Amos, B., Luise, G., Cohen, S., and Redko, I. Meta Optimal Transport. In Krause, A., Brunskill, E., Cho, K., Engelhardt, B., Sabato, S., and Scarlett, J. (eds.), *Proceedings of the 40th International Conference on Machine Learning*, volume 202 of *Proceedings of Machine Learning Research*, pp. 791–813. PMLR, 23–29 Jul 2023. URL [https://proceedings.mlr.press/](https://proceedings.mlr.press/v202/amos23a.html) [v202/amos23a.html](https://proceedings.mlr.press/v202/amos23a.html).
- <span id="page-9-9"></span>Arjovsky, M., Chintala, S., and Bottou, L. Wasserstein Generative Adversarial Networks. In Precup, D. and Teh, Y. W. (eds.), *Proceedings of the 34th International Conference on Machine Learning*, volume 70 of *Proceedings of Machine Learning Research*, pp. 214–223. PMLR, 06– 11 Aug 2017. URL [https://proceedings.mlr.](https://proceedings.mlr.press/v70/arjovsky17a.html) [press/v70/arjovsky17a.html](https://proceedings.mlr.press/v70/arjovsky17a.html).
- <span id="page-9-15"></span>Behrmann, J., Grathwohl, W., Chen, R. T. Q., Duvenaud, D., and Jacobsen, J.-H. Invertible Residual Networks. *Proceedings of the International Conference on Machine Learning*, 2019. doi: 10.48550/ARXIV.1811.00995. URL <https://arxiv.org/abs/1811.00995>.

- <span id="page-9-14"></span>Bonciocat, A.-I. and Sturm, K.-T. Mass transportation and rough curvature bounds for discrete spaces. *Journal of Functional Analysis*, 256(9):2944–2966, 2009. ISSN 0022-1236. doi: https://doi.org/10.1016/j.jfa.2009.01. 029. URL [https://www.sciencedirect.com/](https://www.sciencedirect.com/science/article/pii/S0022123609000305) [science/article/pii/S0022123609000305](https://www.sciencedirect.com/science/article/pii/S0022123609000305).
- <span id="page-9-7"></span>Bonev, B., Kurth, T., Hundt, C., Pathak, J., Baust, M., Kashinath, K., and Anandkumar, A. Spherical Fourier Neural Operators: Learning Stable Dynamics on the Sphere, 2023. URL [https://arxiv.org/abs/](https://arxiv.org/abs/2306.03838) [2306.03838](https://arxiv.org/abs/2306.03838).
- <span id="page-9-2"></span>Bunne, C., Papaxanthos, L., Krause, A., and Cuturi, M. Proximal Optimal Transport Modeling of Population Dynamics. In *Proceedings of The 25th International Conference on Artificial Intelligence and Statistics*, volume 151 of *Proceedings of Machine Learning Research*, pp. 6511–6528. PMLR, 28–30 Mar 2022. URL [https://proceedings.mlr.press/](https://proceedings.mlr.press/v151/bunne22a.html) [v151/bunne22a.html](https://proceedings.mlr.press/v151/bunne22a.html).
- <span id="page-9-4"></span>Bunne, C., Krause, A., and Cuturi, M. Supervised Training of Conditional Monge Maps, 2023a. URL [https://](https://arxiv.org/abs/2206.14262) [arxiv.org/abs/2206.14262](https://arxiv.org/abs/2206.14262).
- <span id="page-9-3"></span>Bunne, C., Stark, S. G., Gut, G., et al. Learning singlecell perturbation responses using neural optimal transport. *Nature Methods*, 20:1759–1768, 2023b. doi: 10.1038/ s41592-023-01969-x. URL [https://doi.org/10.](https://doi.org/10.1038/s41592-023-01969-x) [1038/s41592-023-01969-x](https://doi.org/10.1038/s41592-023-01969-x).
- <span id="page-9-6"></span>Carlier, G., Chizat, L., and Laborde, M. Lipschitz Continuity of the Schrodinger Map in Entropic Optimal Transport, ¨ 2022.
- <span id="page-9-16"></span>Chang, B., Meng, L., Haber, E., Ruthotto, L., Begert, D., and Holtham, E. Reversible architectures for arbitrarily deep residual neural networks, 2017.
- <span id="page-9-13"></span>Chewi, S., Niles-Weed, J., and Rigollet, P. Statistical optimal transport, 2024. URL [https://arxiv.org/](https://arxiv.org/abs/2407.18163) [abs/2407.18163](https://arxiv.org/abs/2407.18163).
- <span id="page-9-12"></span>Chizat, L. and Bach, F. On the global convergence of gradient descent for over-parameterized models using optimal transport, 2018. URL [https://arxiv.org/abs/](https://arxiv.org/abs/1805.09545) [1805.09545](https://arxiv.org/abs/1805.09545).
- <span id="page-9-11"></span>Choi, J., Choi, J., and Kang, M. Scalable Wasserstein Gradient Flow for Generative Modeling through Unbalanced Optimal Transport, 2024. URL [https://](https://arxiv.org/abs/2402.05443) [arxiv.org/abs/2402.05443](https://arxiv.org/abs/2402.05443).
- <span id="page-9-0"></span>Courty, N., Flamary, R., Habrard, A., and Rakotomamonjy, A. Joint distribution optimal transportation for domain adaptation. In *Advances*

*in Neural Information Processing Systems*, volume 30, 2017. URL [https://proceedings.](https://proceedings.neurips.cc/paper/2017/file/0070d23b06b1486a538c0eaa45dd167a-Paper.pdf) [neurips.cc/paper/2017/file/](https://proceedings.neurips.cc/paper/2017/file/0070d23b06b1486a538c0eaa45dd167a-Paper.pdf) [0070d23b06b1486a538c0eaa45dd167a-Paper](https://proceedings.neurips.cc/paper/2017/file/0070d23b06b1486a538c0eaa45dd167a-Paper.pdf). [pdf](https://proceedings.neurips.cc/paper/2017/file/0070d23b06b1486a538c0eaa45dd167a-Paper.pdf).

- <span id="page-10-2"></span>Cuturi, M. Sinkhorn Distances: Lightspeed Computation of Optimal Transport. In Burges, C., Bottou, L., Welling, M., Ghahramani, Z., and Weinberger, K. (eds.), *Advances in Neural Information Processing Systems*, volume 26. Curran Associates, Inc., 2013. URL [https://proceedings.](https://proceedings.neurips.cc/paper/2013/file/af21d0c97db2e27e13572cbf59eb343d-Paper.pdf) [neurips.cc/paper/2013/file/](https://proceedings.neurips.cc/paper/2013/file/af21d0c97db2e27e13572cbf59eb343d-Paper.pdf) [af21d0c97db2e27e13572cbf59eb343d-Paper](https://proceedings.neurips.cc/paper/2013/file/af21d0c97db2e27e13572cbf59eb343d-Paper.pdf). [pdf](https://proceedings.neurips.cc/paper/2013/file/af21d0c97db2e27e13572cbf59eb343d-Paper.pdf).
- <span id="page-10-0"></span>Dadashi, R., Hussenot, L., Geist, M., and Pietquin, O. Primal Wasserstein Imitation Learning, 2020. URL <https://arxiv.org/abs/2006.04678>.
- <span id="page-10-3"></span>Engquist, B. and Froese, B. D. Application of the Wasserstein metric to seismic signals, 2013. URL [https:](https://arxiv.org/abs/1311.4581) [//arxiv.org/abs/1311.4581](https://arxiv.org/abs/1311.4581).
- <span id="page-10-11"></span>Engquist, B. and Yang, Y. Seismis imaging and optimal transport. *Communications in Information and Systems*, 19(2):95–145, 2019. URL [https://www.intlpress.com/site/pub/](https://www.intlpress.com/site/pub/pages/journals/items/cis/content/vols/0019/0002/a001/index.php) [pages/journals/items/cis/content/](https://www.intlpress.com/site/pub/pages/journals/items/cis/content/vols/0019/0002/a001/index.php) [vols/0019/0002/a001/index.php](https://www.intlpress.com/site/pub/pages/journals/items/cis/content/vols/0019/0002/a001/index.php).
- <span id="page-10-17"></span>Fefferman, C., Mitter, S., and Narayanan, H. Testing the manifold hypothesis. *Journal of the American Mathematical Society*, 29(4):983–1049, 2016. URL [https://www.ams.org/journals/jams/](https://www.ams.org/journals/jams/2016-29-04/S0894-0347-2016-00852-4/) [2016-29-04/S0894-0347-2016-00852-4/](https://www.ams.org/journals/jams/2016-29-04/S0894-0347-2016-00852-4/).
- <span id="page-10-6"></span>Feydy, J., Sejourn ´ e, T., Vialard, F.-X., ichi Amari, S., ´ Trouve, A., and Peyr ´ e, G. Interpolating between Optimal ´ Transport and MMD using Sinkhorn Divergences, 2018. URL <https://arxiv.org/abs/1810.08278>.
- <span id="page-10-13"></span>Fishman, N., Gowri, G., Yin, P., Gootenberg, J., and Abudayyeh, O. Generative Distribution Embeddings, 2025. URL <https://arxiv.org/abs/2505.18150>.
- <span id="page-10-16"></span>Franklin, J. and Lorenz, J. On the scaling of multidimensional matrices. *Linear Algebra and its Applications*, 114-115:717–735, mar-apr 1989. URL [https://doi.](https://doi.org/10.1016/0024-3795(89)90490-4) [org/10.1016/0024-3795\(89\)90490-4](https://doi.org/10.1016/0024-3795(89)90490-4).
- <span id="page-10-10"></span>Frogner, C., Zhang, C., Mobahi, H., Araya, M., and Poggio, T. A. Learning with a Wasserstein Loss. In *Advances in Neural Information Processing Systems*, volume 28. Curran Associates, Inc., 2015. URL [https://proceedings.](https://proceedings.neurips.cc/paper/2015/file/a9eb812238f753132652ae09963a05e9-Paper.pdf) [neurips.cc/paper/2015/file/](https://proceedings.neurips.cc/paper/2015/file/a9eb812238f753132652ae09963a05e9-Paper.pdf)

[a9eb812238f753132652ae09963a05e9-Paper](https://proceedings.neurips.cc/paper/2015/file/a9eb812238f753132652ae09963a05e9-Paper.pdf). [pdf](https://proceedings.neurips.cc/paper/2015/file/a9eb812238f753132652ae09963a05e9-Paper.pdf).

- <span id="page-10-14"></span>Geshkovski, B., Letrouit, C., Polyanskiy, Y., and Rigollet, P. A mathematical perspective on transformers, 2024. URL <https://arxiv.org/abs/2312.10794>.
- <span id="page-10-12"></span>Geuter, J., Bonet, C., Korba, A., and Alvarez-Melis, D. DDEQs: Distributional Deep Equilibrium Models through Wasserstein Gradient Flows. In *Proceedings of the 28th International Conference on Artificial Intelligence and Statistics (AISTATS 2025)*, 2025. URL <https://arxiv.org/abs/2503.01140>.
- <span id="page-10-8"></span>Goodfellow, I., Pouget-Abadie, J., Mirza, M., Xu, B., Warde-Farley, D., Ozair, S., Courville, A., and Bengio, Y. Generative Adversarial Nets. In Ghahramani, Z., Welling, M., Cortes, C., Lawrence, N., and Weinberger, K. (eds.), *Advances in Neural Information Processing Systems*, volume 27. Curran Associates, Inc., 2014. URL [https://proceedings.](https://proceedings.neurips.cc/paper/2014/file/5ca3e9b122f61f8f06494c97b1afccf3-Paper.pdf) [neurips.cc/paper/2014/file/](https://proceedings.neurips.cc/paper/2014/file/5ca3e9b122f61f8f06494c97b1afccf3-Paper.pdf) [5ca3e9b122f61f8f06494c97b1afccf3-Paper](https://proceedings.neurips.cc/paper/2014/file/5ca3e9b122f61f8f06494c97b1afccf3-Paper.pdf). [pdf](https://proceedings.neurips.cc/paper/2014/file/5ca3e9b122f61f8f06494c97b1afccf3-Paper.pdf).
- <span id="page-10-15"></span>Goswami, S., Bora, A., Yu, Y., and Karniadakis, G. E. Physics-informed deep neural operator networks, 2022. URL <https://arxiv.org/abs/2207.05748>.
- <span id="page-10-19"></span>Gouk, H., Frank, E., Pfahringer, B., and Cree, M. J. Regularisation of Neural Networks by Enforcing Lipschitz Continuity, 2020.
- <span id="page-10-5"></span>Gracyk, A. and Chen, X. GeONet: a neural operator for learning the Wasserstein geodesic, 2024. URL [https:](https://arxiv.org/abs/2209.14440) [//arxiv.org/abs/2209.14440](https://arxiv.org/abs/2209.14440).
- <span id="page-10-20"></span>Hashan, A. M. Facial expression images, 2022. URL <https://www.kaggle.com/ds/2366449>.
- <span id="page-10-7"></span>He, K., Zhang, X., Ren, S., and Sun, J. Deep Residual Learning for Image Recognition. In *2016 IEEE Conference on Computer Vision and Pattern Recognition (CVPR)*, pp. 770–778, 2016. doi: 10.1109/CVPR.2016.90.
- <span id="page-10-18"></span>Jacobsen, J.-H., Smeulders, A., and Oyallon, E. i-RevNet: Deep Invertible Networks, 2018.
- <span id="page-10-9"></span>Kingma, D. P. and Ba, J. Adam: A Method for Stochastic Optimization, 2017. URL [https://arxiv.org/](https://arxiv.org/abs/1412.6980) [abs/1412.6980](https://arxiv.org/abs/1412.6980).
- <span id="page-10-4"></span>Kolouri, S., Zou, Y., and Rohde, G. K. Sliced Wasserstein Kernels for Probability Distributions, 2015. URL <https://arxiv.org/abs/1511.03198>.
- <span id="page-10-1"></span>Kolouri, S., Park, S. R., Thorpe, M., Slepcev, D., and Rohde, G. K. Optimal Mass Transport: Signal processing and

machine-learning applications. *IEEE Signal Processing Magazine*, 34(4):43–59, 2017. doi: 10.1109/MSP.2017. 2695801.

- <span id="page-11-7"></span>Kolouri, S., Nadjahi, K., Simsekli, U., Badeau, R., and Rohde, G. Generalized Sliced Wasserstein Distances. In Wallach, H., Larochelle, H., Beygelzimer, A., d'Alche-Buc, F., Fox, E., and Garnett, R. ´ (eds.), *Advances in Neural Information Processing Systems*, volume 32. Curran Associates, Inc., 2019. URL [https://proceedings.neurips.](https://proceedings.neurips.cc/paper_files/paper/2019/file/f0935e4cd5920aa6c7c996a5ee53a70f-Paper.pdf) [cc/paper\\_files/paper/2019/file/](https://proceedings.neurips.cc/paper_files/paper/2019/file/f0935e4cd5920aa6c7c996a5ee53a70f-Paper.pdf) [f0935e4cd5920aa6c7c996a5ee53a70f-Paper](https://proceedings.neurips.cc/paper_files/paper/2019/file/f0935e4cd5920aa6c7c996a5ee53a70f-Paper.pdf). [pdf](https://proceedings.neurips.cc/paper_files/paper/2019/file/f0935e4cd5920aa6c7c996a5ee53a70f-Paper.pdf).
- <span id="page-11-10"></span>Korotin, A., Selikhanovych, D., and Burnaev, E. Neural optimal transport, 2023. URL [https://arxiv.org/](https://arxiv.org/abs/2201.12220) [abs/2201.12220](https://arxiv.org/abs/2201.12220).
- <span id="page-11-8"></span>Kovachki, N., Li, Z., Liu, B., Azizzadenesheli, K., Bhattacharya, K., Stuart, A., and Anandkumar, A. Neural Operator: Learning Maps Between Function Spaces, 2024. URL <https://arxiv.org/abs/2108.08481>.
- <span id="page-11-13"></span>Li, S., Yu, X., Xing, W., Kirby, M., Narayan, A., and Zhe, S. Multi-Resolution Active Learning of Fourier Neural Operators, 2024a. URL [https://arxiv.org/abs/](https://arxiv.org/abs/2309.16971) [2309.16971](https://arxiv.org/abs/2309.16971).
- <span id="page-11-15"></span>Li, X., Lu, F., Tao, M., and Ye, F. X. F. Robust first and second-order differentiation for regularized optimal transport, 2024b. URL [https://arxiv.org/abs/](https://arxiv.org/abs/2407.02015) [2407.02015](https://arxiv.org/abs/2407.02015).
- <span id="page-11-18"></span>Li, Z., Kovachki, N., Azizzadenesheli, K., Liu, B., Bhattacharya, K., Stuart, A., and Anandkumar, A. Neural operator: Graph kernel network for partial differential equations, 2020. URL [https://arxiv.org/abs/](https://arxiv.org/abs/2003.03485) [2003.03485](https://arxiv.org/abs/2003.03485).
- <span id="page-11-19"></span>Li, Z., Kovachki, N., Azizzadenesheli, K., Liu, B., Bhattacharya, K., Stuart, A., and Anandkumar, A. Fourier neural operator for parametric partial differential equations, 2021. URL [https://arxiv.org/abs/](https://arxiv.org/abs/2010.08895) [2010.08895](https://arxiv.org/abs/2010.08895).
- <span id="page-11-16"></span>Lipman, Y., Chen, R. T. Q., Ben-Hamu, H., Nickel, M., and Le, M. Flow matching for generative modeling, 2023. URL <https://arxiv.org/abs/2210.02747>.
- <span id="page-11-14"></span>Loshchilov, I. and Hutter, F. Decoupled Weight Decay Regularization, 2019. URL [https://arxiv.org/](https://arxiv.org/abs/1711.05101) [abs/1711.05101](https://arxiv.org/abs/1711.05101).
- <span id="page-11-11"></span>Nutz, M. Introduction to Entropic Optimal Transport, 2022. URL [https://www.math.columbia.edu/](https://www.math.columbia.edu/~mnutz/docs/EOT_lecture_notes.pdf) [˜mnutz/docs/EOT\\_lecture\\_notes.pdf](https://www.math.columbia.edu/~mnutz/docs/EOT_lecture_notes.pdf).

- <span id="page-11-1"></span>Peyre, G. and Cuturi, M. Computational Optimal Trans- ´ port: With Applications to Data Science. *Foundations and Trends® in Machine Learning*, 11(5-6):355–607, 2019. ISSN 1935-8237. doi: 10.1561/2200000073. URL <http://dx.doi.org/10.1561/2200000073>.
- <span id="page-11-6"></span>Pooladian, A.-A., Ben-Hamu, H., Domingo-Enrich, C., Amos, B., Lipman, Y., and Chen, R. T. Q. Multisample flow matching: Straightening flows with minibatch couplings, 2023. URL [https://arxiv.org/abs/](https://arxiv.org/abs/2304.14772) [2304.14772](https://arxiv.org/abs/2304.14772).
- <span id="page-11-20"></span>Santambrogio, F. Optimal transport for applied mathematicians. *Birkauser, NY ¨* , 55(58-63):94, 2015.
- <span id="page-11-17"></span>Santambrogio, F. Euclidean, Metric, and Wasserstein gradient flows: an overview, 2016. URL [https://arxiv.](https://arxiv.org/abs/1609.03890) [org/abs/1609.03890](https://arxiv.org/abs/1609.03890).
- <span id="page-11-2"></span>Schiebinger, G., Shu, J., Tabaka, M., Cleary, B., Subramanian, V., Solomon, A., Gould, J., Liu, S., Lin, S., Berube, P., Lee, L., Chen, J., Brumbaugh, J., Rigollet, P., Hochedlinger, K., Jaenisch, R., Regev, A., , and Lander, E. S. Optimal-Transport Analysis of Single-Cell Gene Expression Identifies Developmental Trajectories in Reprogramming. *Cell*, 176(4):928–943, 2019.
- <span id="page-11-3"></span>Schmitz, M. A., Heitz, M., Bonneel, N., Ngole, F., Coeur- ` jolly, D., Cuturi, M., Peyre, G., and Starck, J.-L. Wasser- ´ stein Dictionary Learning: Optimal Transport-Based Unsupervised Nonlinear Dictionary Learning. *SIAM Journal on Imaging Sciences*, 11(1):643–678, jan 2018. doi: 10.1137/17m1140431. URL [https://doi.org/10.](https://doi.org/10.1137%2F17m1140431) [1137%2F17m1140431](https://doi.org/10.1137%2F17m1140431).
- <span id="page-11-21"></span>Serrurier, M., Mamalet, F., Fel, T., Bethune, L., and Boissin, ´ T. On the explainable properties of 1-Lipschitz Neural Networks: An Optimal Transport Perspective, 2023.
- <span id="page-11-12"></span>Sinkhorn, R. and Knopp, P. Concerning nonnegative Matrices and doubly stochastic Matrices. *Pacific Journal of Mathematics*, 21(2), 1967.
- <span id="page-11-4"></span>Thornton, J. and Cuturi, M. Rethinking Initialization of the Sinkhorn Algorithm, 2022. URL [https://arxiv.](https://arxiv.org/abs/2206.07630) [org/abs/2206.07630](https://arxiv.org/abs/2206.07630).
- <span id="page-11-5"></span>Tong, A., Fatras, K., Malkin, N., Huguet, G., Zhang, Y., Rector-Brooks, J., Wolf, G., and Bengio, Y. Improving and generalizing flow-based generative models with minibatch optimal transport, 2024. URL [https:](https://arxiv.org/abs/2302.00482) [//arxiv.org/abs/2302.00482](https://arxiv.org/abs/2302.00482).
- <span id="page-11-9"></span>Uscidda, T. and Cuturi, M. The Monge Gap: A Regularizer to Learn All Transport Maps, 2023.
- <span id="page-11-0"></span>Villani, C. *Optimal Transport Old and New*. Springer, 2009.

- <span id="page-12-0"></span>Xu, H., Wang, W., Liu, W., and Carin, L. Distilled Wasserstein Learning for Word Embedding and Topic Modeling. In Bengio, S., Wallach, H., Larochelle, H., Grauman, K., Cesa-Bianchi, N., and Garnett, R. (eds.), *Advances in Neural Information Processing Systems*, volume 31. Curran Associates, Inc., 2018. URL [https://proceedings.neurips.](https://proceedings.neurips.cc/paper_files/paper/2018/file/22fb0cee7e1f3bde58293de743871417-Paper.pdf) [cc/paper\\_files/paper/2018/file/](https://proceedings.neurips.cc/paper_files/paper/2018/file/22fb0cee7e1f3bde58293de743871417-Paper.pdf) [22fb0cee7e1f3bde58293de743871417-Paper](https://proceedings.neurips.cc/paper_files/paper/2018/file/22fb0cee7e1f3bde58293de743871417-Paper.pdf). [pdf](https://proceedings.neurips.cc/paper_files/paper/2018/file/22fb0cee7e1f3bde58293de743871417-Paper.pdf).
- <span id="page-12-1"></span>Zhang, C., Cai, Y., Lin, G., and Shen, C. DeepEMD: Few-Shot Image Classification With Differentiable Earth Mover's Distance and Structured Classifiers. In *2020 IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)*, pp. 12200–12210, 2020. doi: 10.1109/CVPR42600.2020.01222.

The Appendix is structured as follows: In Appendix [A](#page-13-0) we give a more thorough background on OT, as well as additional technical details for our experiments on computing barycenters and geodesics. Appendix [B](#page-20-0) contains all proofs omitted in the paper. In Appendix [C,](#page-26-0) we provide additional training details, and Appendix [D](#page-28-1) contains additional experiments and materials.

## <span id="page-13-0"></span>A. Background

### <span id="page-13-1"></span>A.1. Optimal Transport

In this section, we recall some properties of optimal transport. First, we define the unregularized continuous problems for completeness.

<span id="page-13-3"></span>Problem A.1 (Kantorovich Optimal Transport Problem). For µ ∈ P(X ), ν ∈ P(Y), and a cost c : X × Y → R ∪ {∞} the Kantorovich problem takes the form

<span id="page-13-2"></span>
$$
\inf_{\pi \in \Pi(\mu,\nu)} \int c(x,y) \, d\pi(x,y) \tag{12}
$$

The infimum in [\(12\)](#page-13-2) is called the *transport cost*, and the minimizer π, if it exists, the *optimal transport plan*.

The continuous dual problem is similar to the regularized dual [\(3\)](#page-1-1). For a more thorough overview of OT, we refer the reader to [\(Villani,](#page-11-0) [2009;](#page-11-0) [Peyre & Cuturi](#page-11-1) ´ , [2019;](#page-11-1) [Chewi et al.,](#page-9-13) [2024\)](#page-9-13).

<span id="page-13-4"></span>Problem A.2 (Dual Optimal Transport Problem). For µ, ν and c as before, the dual problem reads

$$
\sup_{\substack{f\in L^{1}(\mu), g\in L^{1}(\nu)\\f+g\leq c}} \int_{\mathcal{X}} f(x) \mathrm{d}\mu(x) + \int_{\mathcal{Y}} g(y) \mathrm{d}\nu(y),
$$

where f + g ≤ c is to be understood as f(x) + g(y) ≤ c(x, y) for all x, y.

An important concept in optimal transport are *transport maps*.

Definition A.3 (Transport Maps). A map T : X → Y is called a *transport map* between µ and ν if ν = T#µ. If there exists an optimal transport plan π such that π = (Id, T)#µ, T is called an *optimal transport map*.

Of course, not every transport plan admits a transport map; however, every transport map yields an optimal transport plan via π = (Id, T)#µ. For sufficient conditions for the existence of both transport plans and maps, we refer the reader to [\(Villani,](#page-11-0) [2009\)](#page-11-0).

In the paper we mentioned that if µ and ν are supported on finitely many points, one can rewrite the problems [A.1](#page-13-3) and [A.2](#page-13-4) with vectors. We now define the discrete problems carefully.

Problem A.4 (Discrete Optimal Transport Problem). For two discrete measures µ ∈ ∆m−<sup>1</sup> and ν ∈ ∆n−<sup>1</sup> , and a cost matrix C ∈ R <sup>m</sup>×<sup>n</sup>, the discrete OT problem is defined as

$$
L(\boldsymbol{\mu},\boldsymbol{\nu}):=\min_{\Pi\in\Pi(\boldsymbol{\mu},\boldsymbol{\nu})}\langle C,\Pi\rangle
$$

Here, Π(µ, ν) denotes the set of all *transport plans* between µ and ν, i.e. matrices Π ∈ R m×n ≥0 s.t. Π1<sup>n</sup> = µ and Π<sup>⊤</sup>1<sup>m</sup> = ν. The problem has a dual formulation:

Problem A.5 (Discrete Dual Optimal Transport Problem). For two discrete measures µ ∈ ∆<sup>m</sup>−<sup>1</sup> and ν ∈ ∆<sup>n</sup>−<sup>1</sup> , and a cost matrix C ∈ R <sup>m</sup>×<sup>n</sup>, the discrete dual OT problem is defined as

$$
D(\boldsymbol{\mu},\boldsymbol{\nu}) := \max_{\substack{\boldsymbol{f} \in \mathbb{R}^m, \ \boldsymbol{g} \in \mathbb{R}^n \\ \boldsymbol{f} + \boldsymbol{g} \leq C}} \langle \boldsymbol{f}, \boldsymbol{\mu} \rangle + \langle \boldsymbol{g}, \boldsymbol{\nu} \rangle
$$

Here, <sup>f</sup> <sup>+</sup> <sup>g</sup> <sup>≤</sup> <sup>C</sup> is to be understood as <sup>f</sup><sup>i</sup> <sup>+</sup> <sup>g</sup><sup>j</sup> <sup>≤</sup> <sup>C</sup>ij for all <sup>i</sup> <sup>∈</sup> <sup>J</sup>mK, <sup>j</sup> <sup>∈</sup> <sup>J</sup>nK. In the special case where <sup>X</sup> <sup>=</sup> <sup>Y</sup> and <sup>C</sup> corresponds to a metric, i.e. Cij = d(x<sup>i</sup> , y<sup>j</sup> ), the *Wasserstein distance of order* p *between* µ *and* ν for p ∈ [1, ∞) is defined as:

$$
W_p(\boldsymbol{\mu}, \boldsymbol{\nu}) = \left(\min_{\pi \in \Pi(\boldsymbol{\mu}, \boldsymbol{\nu})} \sum_{i,j} C_{ij}^p \Pi_{ij}\right)^{\frac{1}{p}}.
$$

This definition coincides with the definition from the paper for continuous measures, if they are supported on finitely many points.

For completeness, we also state the entropically regularized primal and dual problem in the discrete case. The discrete problem is typically formulated with an entropy term instead of the KL divergence as in equation [\(1\)](#page-0-1), but the two can be shown to be equivalent [\(Chewi et al.,](#page-9-13) [2024\)](#page-9-13).

Definition A.6 (Entropy). For a matrix P = [pij ]ij ∈ R <sup>m</sup>×n, we define its entropy H(P) as

$$
H(P) := -\sum_{i=1}^{m} \sum_{j=1}^{n} p_{ij} \log p_{ij}
$$

if all entries are positive, and H(P) := −∞ if at least one entry is negative. For entries pij = 0, we use the convention 0 log 0 = 0, as x log x x→0 −−−→ 0.

The entropic optimal transport problem is defined as follows.

<span id="page-14-1"></span>Problem A.7 (Entropic Discrete Optimal Transport Problem). For ϵ > 0, the entropic optimal transport problem is defined as:

$$
\mathrm{OT}_{\epsilon}(\boldsymbol{\mu},\boldsymbol{\nu}) := \min_{\Pi \in \Pi(\boldsymbol{\mu},\boldsymbol{\nu})} \langle C,\Pi \rangle - \epsilon \, \mathrm{H}(\Pi).
$$

Note that this is identical to the unregularized optimal transport problem, except that the unregularized one does not contain the regularization term −ϵH(Π). As the objective in Problem [A.7](#page-14-1) is ϵ-strongly convex, the problem admits a unique solution [\(Peyre & Cuturi](#page-11-1) ´ , [2019\)](#page-11-1).

The *Gibbs kernel* is defined as K = exp(−C/ϵ). Then the entropic dual problem reads:

<span id="page-14-2"></span>Problem A.8 (Entropic Discrete Dual Problem).

$$
\max_{\bm{f}_{\bm{\epsilon}} \in \mathbb{R}^m, \ \bm{g}_{\bm{\epsilon}} \in \mathbb{R}^n} \langle \bm{f}_{\bm{\epsilon}}, \bm{\mu} \rangle + \langle \bm{g}_{\bm{\epsilon}}, \bm{\nu} \rangle - \epsilon \left\langle e^{\bm{f}_{\bm{\epsilon}}/\epsilon}, K e^{\bm{g}_{\bm{\epsilon}}/\epsilon} \right\rangle.
$$

Again, without the regularization term −ϵ e <sup>f</sup>ϵ/ϵ, Kegϵ/ϵ , this equals the regular optimal transport dual; note, however, that the unregularized dual is subject to the constraint f + g ≤ C.

In both the continuous, as well as the discrete setting, there is *duality*, i.e. the optima of the primal and dual problems coincide. In addition, the optimizers are intrinsically linked, akin to Proposition [1](#page-2-2) for the discrete entropic problem. We refer the reader to [\(Villani,](#page-11-0) [2009;](#page-11-0) [Peyre & Cuturi](#page-11-1) ´ , [2019\)](#page-11-1) for more details.

### <span id="page-14-0"></span>A.2. Calculating the Barycenter

Recall the Sinkhorn divergence barycenter for a set of discrete measures {ν1, ..., ν<sup>N</sup> } ⊂ P2(X ),

$$
\boldsymbol{\mu} = \underset{\boldsymbol{\mu}' \in \mathcal{P}_2(X)}{\arg \min} \sum_i \alpha_i \, \text{SD}_{\epsilon}(\boldsymbol{\mu}', \boldsymbol{\nu}_i).
$$

For a solution (f, g) to the dual problem [A.8](#page-14-2) between two measures µ = P <sup>i</sup> aiδ<sup>x</sup><sup>i</sup> and ν = P j b<sup>j</sup> δ<sup>y</sup><sup>j</sup> , it holds

$$
\mathrm{SD}_{\epsilon}(\boldsymbol{\mu},\boldsymbol{\nu})=\langle \boldsymbol{\mu}, \boldsymbol{f}-\boldsymbol{p}\rangle + \langle \boldsymbol{\nu}, \boldsymbol{g}-\boldsymbol{q}\rangle,
$$

see [\(Feydy et al.,](#page-10-6) [2018\)](#page-10-6). Here, p and q are the optimal potentials for (µ, µ) and (ν, ν) resp. (if both measures in the OT problem are the same, the dual potentials can be chosen to be equal).

From this identity, we immediately get

$$
\nabla_{\boldsymbol{a}} \, \text{SD}_{\epsilon}(\boldsymbol{\mu}, \boldsymbol{\nu}) = \boldsymbol{f} - \boldsymbol{p}.
$$

Note that this is not a gradient with respect to the measure µ; instead, we view µ as a vector, and compute the gradient w.r.t. the entries in that vector. This means we essentially compute the barycenter on the discrete space {x1, ..., xn}.

A pseudocode for how to approximate the Sinkhorn divergence barycenter with UNOT is given in Algorithm [3.](#page-15-1) Note that instead of using softmax to project back to probability measures, one could also just rescale; however, softmax proved better in practice. We also run a single Sinkhorn iteration on the output of S<sup>ϕ</sup> in practice, as it improved visual quality of the barycenters; however, this is not strictly needed.

### Algorithm 3 Barycenter Computation

<span id="page-15-1"></span>1: in set of measures {νi}<sup>i</sup> ⊂ ∆n−<sup>1</sup> , initial µ<sup>0</sup> ∈ ∆n−<sup>1</sup> , weights λ ∈ ∆n−<sup>1</sup> 2: µ ← µ<sup>0</sup> 3: for i = 1, 2, ..., T do 4: p ← Sϕ(µ, µ) 5: for ν<sup>i</sup> in {νi}<sup>i</sup> do 6: f<sup>i</sup> ← Sϕ(ν<sup>i</sup> , µ) //switch the order of the arguments to get f<sup>i</sup> instead of g<sup>i</sup> 7: end for 8: µ ← softmax (µ − P <sup>i</sup> λi(f<sup>i</sup> − pk)) 9: end for

Barycenters can be far when Transport Distances are close. We now give a simple example that illustrates that merely predicting transport distances accurately does *not* necessarily imply predicting barycenters accurately, at least in the nonregularized setting. Let µ be the measure with mass 1/2 at the two points (0, −1) and (0, 1) in R 2 . Let ν<sup>1</sup> be the measure with mass 1/2 at each of the points (−1, 0) and (1, −ϵ) for a small ϵ > 0, and ν<sup>2</sup> a measure with mass 1/2 at each of the two points (−1, 0) and (1, ϵ). Then as ϵ goes to 0, the transport distances between between µ and ν<sup>1</sup> resp. µ and ν<sup>2</sup> become arbitrarily close. However, the unique Wasserstein-p barycenter (for p > 1) between µ and ν<sup>1</sup> has mass 1/2 at each of the points (−1/2, 1/2) and (1/2, −(1 + ϵ)/2), whereas the barycenter between µ and ν<sup>2</sup> has mass 1/2 at each of the points (−1/2, −1/2) and (1/2,(1 + ϵ)/2), so no matter how small ϵ gets, the barycenters will always be far apart.

### <span id="page-15-0"></span>A.3. Geodesics

In Section [4.3,](#page-7-3) we saw that the McCann interpolation between two measures µ, ν ∈ P2(X ) is a constant-speed geodesic. In this section, we provide additional background on constant-speed geodesics, and establish a connection between constantspeed geodesics in P2([0, 1]<sup>2</sup> ) and the notion of *strong-*ϵ *quasi-geodesics* in the discretized space P( [[n]]<sup>2</sup> n ). This makes our approximation of geodesics as in Section [4.3](#page-7-3) more rigorous.

First, we recall the definition of constant-speed geodesics.

Definition A.9. A curve ω : [0, 1] → (P2(X ), W2) is called *constant-speed geodesic* between ω(0) and ω(1) if it satisfies

$$
W_2(\omega(t), \omega(s)) = |t - s| W_2(\omega(0), \omega(1)), \quad \forall t, s \in [0, 1].
$$

It turns out that for convex X ⊂ R d , constant-speed geodesics are equivalent to push-forwards under transport plans, and if the starting point ω(0) is absolutely continuous, this is equal to the McCann interpolation.

Theorem A.10. *Let* X ⊂ R <sup>d</sup> *be convex. Then a curve* ω : [0, 1] → (P2(X ), W2) *is a constant-speed geodesic between* ω(0) *and* ω(1) *if and only if it is of the form*

$$
\omega(t) = (p_t)_{\#} \pi
$$

*for an optimal transport plan* π *between* ω(0) *and* ω(1)*, where the interpolation* p<sup>t</sup> *is given by* pt(x, y) = (1 − t)x + ty*. If, in addition,* ω(0) *is absolutely continuous, then we can write*

$$
\omega(t) = [(1-t)\mathrm{Id} + tT]_{\#}\omega(0)
$$

*for an optimal transport map* T *from* ω(0) *to* ω(1)*.*

This theorem holds, in fact, for any Wasserstein-p space for p > 1, see [\(Santambrogio,](#page-11-17) [2016\)](#page-11-17).

Now, denote by µ<sup>t</sup> the McCann interpolation between µ and ν. As mentioned in Section [4.2,](#page-6-9) we can express µ<sup>t</sup> as the following barycenter:

$$
\mu_t = \underset{\mu' \in \mathcal{P}_2(\mathcal{X})}{\arg \min} ((1-t)W_2^2(\mu', \mu) + tW_2^2(\mu', \nu)),
$$

which we approximate by the Sinkhorn Divergence barycenter

<span id="page-16-0"></span>
$$
\mu_t = \underset{\mu' \in \mathcal{P}_2(\mathcal{X})}{\arg \min} \left( (1-t) \, \text{SD}_{\epsilon}(\mu', \mu) + t \, \text{SD}_{\epsilon}(\mu', \nu) \right),\tag{13}
$$

which is justified by the fact that Sinkhorn Divergences converge to the OT cost as ϵ → 0, and that they are reliable loss functions, in the sense that weak convergence of a sequence of measures is equivalent to convergence of the Sinkhorn divergence, see [\(Feydy et al.,](#page-10-6) [2018\)](#page-10-6). As also shown in [\(Feydy et al.,](#page-10-6) [2018\)](#page-10-6), the gradient of the Sinkhorn Divergence w.r.t. the vector a, when writing a discrete measure µ as µ = P <sup>i</sup> aiδx<sup>i</sup> , is given by

<span id="page-16-1"></span>
$$
\nabla_a \text{SD}_{\epsilon}(\mu, \nu) = f - p. \tag{14}
$$

However, if we now do a simple gradient descent on [\(13\)](#page-16-0) using [\(14\)](#page-16-1), we are not actually computing the barycenter on the space P2(X ) anymore, as we only consider gradients w.r.t. a, which does not allow particles to *move*, but merely to *teleport mass* to other particles. In particular, if X is a discrete space, there exist no constant-speed geodesics between different points anymore, as can easily be seen from the following example. Let µ<sup>0</sup> = δx<sup>0</sup> and µ<sup>1</sup> = δx<sup>1</sup> be two Dirac measures for some x0, x<sup>1</sup> ∈ X. Assume there would exist a constant speed geodesic ω joining µ<sup>0</sup> and µ1. Then for t > 0,

$$
W_2(\omega(t), \omega(0)) = tW_2(\omega(1), \omega(0)).
$$

However, since the space is discrete, this implies that x<sup>0</sup> = x1, i.e. the only constant-speed geodesics are constant. We therefore work with the following approximation of geodesics.

Definition A.11 (Quasi-Isometry). Let (X1, d1) and (X2, d2) be metric spaces. f : X<sup>1</sup> → X<sup>2</sup> is called a (λ, ϵ)-quasiisometry if there exist λ ≥ 0 and ϵ > 0 such that for all x, y ∈ X<sup>1</sup>

$$
\frac{1}{\lambda}d_1(x,y) - \epsilon \le d_2(f(x), f(y)) \le \lambda d_1(x,y) + \epsilon
$$

If in addition there exists a C > 0 such that for all z ∈ X<sup>2</sup> there exist an x ∈ X<sup>1</sup> such that d2(f(x), z) ≤ C, f is called quasi-isometry.

We can then use this to define quasi-geodesics. [\(Bonciocat & Sturm,](#page-9-14) [2009\)](#page-9-14) introduced a similar concept called h-rough geodesics, for which they just used the upper bound.

Definition A.12 (Strong-ϵ Quasi-Geodesics). A strong-ϵ quasi-geodesic in a metric space (X , d) is a map γ : [0, 1] → X such that for all s, t ∈ [0, 1],

$$
d(\gamma_0, \gamma_1)|t - s| - \epsilon \leq d(\gamma_t, \gamma_s) \leq d(\gamma_0, \gamma_1)|t - s| + \epsilon.
$$

Now let X = [0, 1]<sup>2</sup> , and denote by [[n]]<sup>2</sup> <sup>n</sup> ⊂ [0, 1]<sup>2</sup> the discrete space consisting of all x<sup>i</sup> of the form x<sup>i</sup> = 1 2n , 1 2n + k 1 n , 0 + j 0, 1 n , for k, j = 0, ..., n − 1. We can then show that (P2([0, 1]<sup>2</sup> ), W2) is quasi-isometric to (P( [[n]]<sup>2</sup> n ), W2). Proposition A.13. *The metric space* (P2([0, 1]<sup>2</sup> ), W2) *is* (1, <sup>√</sup> 1 2n )*-quasi-isometric to* (P( [[n]]<sup>2</sup> n ), W2)*, i.e. there exist an* f : (P2([0, 1]<sup>2</sup> ), W2) → (P( [[n]]<sup>2</sup> n ), W2) *such that for all* µ, ν ∈ P2([0, 1]) *it holds that*

$$
W_2(\mu,\nu) - \frac{1}{\sqrt{2n}} \le W_2(f(\mu), f(\nu)) \le W_2(\mu,\nu) + \frac{1}{\sqrt{2n}}.
$$

*Proof.* We split the space [0, 1]<sup>2</sup> into squares via N(xi) := (x<sup>i</sup> + [− 1 2n , 1 2n ] 2 ). We define f : P([0, 1]<sup>2</sup> ) → P( [[n]]<sup>2</sup> n ) by

$$
f(\mu) = \sum_{x_i \in X} \left( \int_{N(x_i)} \mathrm{d}\mu \right) \delta_{x_i}.
$$

By triangle inequality, we have

$$
W_2(f(\mu), f(\nu)) \le W_2(\mu, \nu) + W_2(\mu, f(\mu)) + W_2(\nu, f(\nu))
$$
  
$$
W_2(\mu, \nu) \le W_2(f(\mu), f(\nu)) + W_2(\mu, f(\mu)) + W_2(\nu, f(\nu))
$$

For any measure µ ∈ P([0, 1]), denoting by T : [0, 1]<sup>2</sup> → [[n]]<sup>2</sup> n the map that sends each point to the corresponding midpoint xi , we get

$$
W_2^2(\mu, f(\mu)) \le \int_{[0,1]^2} |T(x) - x|^2 \, \mathrm{d}\mu \le \int_{[0,1]^2} \frac{2}{4n^2} \, \mathrm{d}\mu = \frac{2}{4n^2}.
$$

Therefore we have a (1, <sup>√</sup> 1 2n )-quasi-isometry between both spaces.

We also need to show that there exist a C > 0 such that for all µ ∈ P( [[n]]<sup>2</sup> n ) there exist a ν ∈ P([0, 1]<sup>2</sup> ) with

$$
W_2(f(\nu), \mu) < C.
$$

Choosing C = <sup>√</sup> 1 2n and ν = µ concludes the proof.

We immediately get the following corollary.

Corollary A.14. *Constant-speed geodesics* P2([0, 1]<sup>2</sup> ) *are strong-*ϵ *quasi-geodesics in* P([[n]]2/n)*.*

This justifies doing gradient descent on [\(13\)](#page-16-0) using the discrete space gradient [\(14\)](#page-16-1) to approximate the geodesic, as we can approximate the constant-speed geodesic with a strong-ϵ-quasi-geodesic in the discrete space.

### <span id="page-17-1"></span>A.4. Wasserstein on Wasserstein Distance

In this section, we provide additional details on how to solve the particle flow

<span id="page-17-2"></span>
$$
\frac{\partial}{\partial t}\hat{\mu}_t = -\nabla_{\hat{\mu}_t}[\hat{\text{SD}}_{\epsilon}(\hat{\mu}_t, \hat{\nu})]
$$
\n(15)

from Section [4.4.](#page-7-4) Recall that µ, ˆ νˆ ∈ P2(P2([0, 1]<sup>2</sup> , c), W2), µˆ = 1 n P i δµ<sup>i</sup> , νˆ = 1 n P j δνj for µ<sup>i</sup> , ν<sup>j</sup> ∈ P2([0, 1]<sup>2</sup> ). From [\(Li et al.,](#page-11-15) [2024b\)](#page-11-15), we get that

$$
\frac{\partial \hat{\text{SD}}_{\epsilon}(\hat{\mu}, \hat{\nu})}{\partial \mu_k} = \sum_j \frac{\partial \text{SD}_{\epsilon}(\mu_k, \nu_j)}{\partial \mu_k} \Pi_{kj},
$$

where Πkj is an optimal transport plan between µ<sup>k</sup> and ν<sup>j</sup> . Now as in the previous section, we can approximate ∂ SDϵ(µk,ν<sup>j</sup> ) ∂µ<sup>k</sup> = fkj − pk, where fkj is the dual potential from OTϵ(µk, ν<sup>j</sup> ), and p<sup>k</sup> that of OTϵ(µk, µk). As before, we can approximate these gradients with UNOT, which lets us solve [\(15\)](#page-17-2) with a simple gradient descent scheme, as shown in Section [A.2.](#page-14-0) As in Section [A.2,](#page-14-0) we add a single Sinkhorn iteration on the predictions made by S<sup>ϕ</sup> as it improves visual quality, but this is not strictly necessary.

### <span id="page-17-0"></span>A.5. Fourier Neural Operators

In this section, we describe FNOs in more detail. The main breakthrough for Neural Operators came in the combination with approximating solutions to partial differential equations (PDEs) [\(Li et al.,](#page-11-18) [2020;](#page-11-18) [2021;](#page-11-19) [Goswami et al.,](#page-10-15) [2022\)](#page-10-15). Many problems, including PDEs, can be numerically solved by discretizing infinite-dimensional input and output functions. Neural Operators are a class of neural networks that parametrize functions F : A → U, where A and U are Banach spaces whose elements are functions a : D<sup>a</sup> → R d ′ <sup>a</sup> and u : D<sup>u</sup> → R d ′ <sup>u</sup> respectively, for bounded domains D<sup>a</sup> ⊂ R <sup>d</sup><sup>a</sup> and D<sup>u</sup> ⊂ R <sup>d</sup><sup>u</sup> . One of the main advantages of Neural Operators is that they can generalize over different grid discretizations, unlike traditional neural networks, which makes them particularly well-suited for solving PDEs,[11](#page-17-3) and they are universal approximators for continuous operators acting on Banach spaces [\(Kovachki et al.,](#page-11-8) [2024\)](#page-11-8). While our space P([0, 1]<sup>2</sup> ) is not

<span id="page-17-3"></span><sup>11</sup>For example, an FNO could be used to solve PDEs of the form ∆u = a with Dirichlet boundary conditions, for which we get a unique solution u for every a. The FNO then maps each a ∈ A to the corresponding solution u ∈ U.

Universal Neural Optimal Transport

![](_page_18_Figure_1.jpeg)

Figure 9. Fourier Neural Operator architecture, adapted from [\(Kovachki et al.,](#page-11-8) [2024\)](#page-11-8). The input measures (µ, ν) are passed through a point-wise lifting operator P which is then followed by L Fourier operators and point-wise non-linearity operators. After the last Fourier layer, we project back to the output potential g with a point-wise operator Q.

technically a Banach space, the space of finite signed measures with the total variation norm is, and P([0, 1]<sup>2</sup> ) is a subset. We note that approximation theory for Neural Operators usually

A neural operator usually has the following form:

<span id="page-18-0"></span>
$$
F: \mathcal{A} \to \mathcal{U}
$$
$$
a \mapsto Q \circ B_L \circ \dots \circ B_1 \circ P(a),
$$

which in our setting becomes

$$
S_{\phi}: \mathcal{P}([0,1]^2) \times \mathcal{P}([0,1]^2) \to L^1([0,1]^2)
$$
  
$$
(\mu, \nu) \mapsto Q \circ B_L \circ \dots \circ B_1 \circ P(\mu, \nu).
$$

Here, P is a *lifting map*, B<sup>i</sup> are the *kernel layers*, and Q is a *projection* back to the target space.

Different versions of neural operators have been proposed, which mostly differ in how the kernel layers B<sup>i</sup> are defined. Our network S<sup>ϕ</sup> is parametrized as a *Fourier Neural Operator* (FNO) [\(Kovachki et al.,](#page-11-8) [2024\)](#page-11-8), where the kernel layers act on Fourier features of the inputs. We outline details for all the layers in the following.

- Lifting (P). The lifting map is a pointwise map {a : D<sup>a</sup> → R d ′ <sup>a</sup> } 7→ {v<sup>0</sup> : D<sup>0</sup> → R <sup>d</sup>v<sup>0</sup> }, which maps the input a to a function v<sup>0</sup> by mapping points in R d ′ <sup>a</sup> to points in R <sup>d</sup>v<sup>0</sup> . We use a 2D convolutional layer for P, and in our setting, D<sup>a</sup> = [0, 1]<sup>2</sup> × [0, 1]<sup>2</sup> , as we can view elements in P([0, 1]<sup>2</sup> ) as maps [0, 1]<sup>2</sup> → R when dealing with discretizations of measures.
- Iterative Fourier Layer (Bi). The network has L Fourier layers B<sup>i</sup> . In each of them, we map {v<sup>i</sup> : D<sup>i</sup> → R <sup>d</sup>vi } 7→ {vi+1 : Di+1 → R <sup>d</sup>vi+1 } by first applying the (discrete) Fourier transform F from which we select a fixed number of Fourier features, then a neural network NN on these features, and then the inverse Fourier transform F −1 . Note that the Fourier features are complex, hence the network NN is also complex (with multiplications in C). Each Fourier layer also contains a *bypass layer*, which is similar to a skip connection, but contains a layer W which is typically a 2D convolution; cmp Figure [9.](#page-18-0) Hence, the output of the Fourier layer is given by σ(F −1 (NN(F(v)) + b + W v), where σ is an activation.
- Projection (Q). The projection Q is the analogue to the lifting layer, mapping the hidden representation to the output function {v<sup>L</sup> : D<sup>L</sup> → R dv<sup>L</sup> } 7→ {u : D<sup>u</sup> → R d ′ <sup>u</sup> }. In our setting, D<sup>u</sup> = [0, 1]<sup>2</sup> .

In contrast to [\(Kovachki et al.,](#page-11-8) [2024\)](#page-11-8), we found that a Fourier layer containing a two-layer neural network NN instead of just a linear layer worked better in practice. Our bypass layer is still a linear layer W.

On the unit sphere S 2 , we use Spherical FNOs (SFNOs) [\(Bonev et al.,](#page-9-7) [2023\)](#page-9-7) instead of regular FNOs, which respect the geometry of S 2 . SFNOs leverage the Fourier transform on the sphere F S 2 , which can be viewed as a change of basis into an orthogonal basis of L 2 (S 2 ), instead of the regular Fourier transform F for flat geometries. Everything else about our architecture remains the same.

Details on hyperparameter choices can be found in Appendix [C.](#page-26-0)

## <span id="page-20-0"></span>B. Proofs

This section contains all proofs, as well as further technical details omitted in the paper. For convenience, we restate the statements from the paper.

We start off by rigorously restating Proposition [2.](#page-3-4) Let X ⊂ R <sup>N</sup> be a compact set. We start off with a natural definition of discretization of a continuous measure, which applies, for example, to discrete images as discretizations of an underlying "ground truth" continuous image.

Definition B.1 (Discretization of Measures). Let µ ∈ P(X ) be an absolutely continuous measure, and let X<sup>n</sup> = {x n 1 , ..., x<sup>n</sup> <sup>n</sup>} ⊂ X . The *discretization of* µ *on* X<sup>n</sup> is defined as the measure µ<sup>n</sup> ∈ P(X ) supported on Xn, where

$$
\boldsymbol{\mu}_n(x_i^n) = \int_{\Omega_i} \mathrm{d}\mu,
$$

with

$$
\Omega_i^n = \{ x \in \mathcal{X} : ||x - x_i^n|| \le ||x - y|| \ \forall y \in \mathcal{X} \}.
$$

Note that the intersections Ω n <sup>i</sup> ∩ Ω n j have Lebesgue measure zero, so this is well-defined.

We cannot guarantee that an arbitrary sequence of discretizations µ<sup>n</sup> converges weakly to µ as n → ∞; simply consider the case where all the x n i are identical for all n and i. Hence, we need to ensure that the discretization is uniform over all of X in some way.

Definition B.2 (Uniform Discretization). Let X<sup>n</sup> = {x n i , ..., x<sup>n</sup> <sup>n</sup>} be subsets of X for all n ∈ N. Then we call the sequence (Xn)n∈<sup>N</sup> a *uniform discretization* of X if for all x ∈ X ,

$$
\lim_{n \to \infty} \min_{i=1,...,n} \|x - x_i^n\| = 0.
$$

While this may seem like a "pointwise discretization" at first, it turns out to be uniform, as an Arzela-Ascoli type argument ` shows.

<span id="page-20-3"></span>Theorem B.3. *Let* X ⊂ R <sup>d</sup> *be compact, and let* {Xn}n≥<sup>1</sup> *be a sequence of finite subsets of* X *with* |Xn| = n *for each* n*. The following are equivalent:*

- <span id="page-20-1"></span>*1.* limn→∞ sup x∈X min y∈X<sup>n</sup> ∥x − y∥ = 0.
- <span id="page-20-2"></span>*2.* <sup>∀</sup> <sup>x</sup> ∈ X : limn→∞ min y∈X<sup>n</sup> ∥x − y∥ = 0.

*Proof.* [\(1\)](#page-20-1) =⇒ [\(2\)](#page-20-2). If supx∈X miny∈X<sup>n</sup> ∥x − y∥ → 0, then in particular for each fixed x ∈ X we have

$$
\min_{y \in \mathcal{X}_n} ||x - y|| \le \sup_{z \in \mathcal{X}} \min_{y \in \mathcal{X}_n} ||z - y|| \longrightarrow 0.
$$

[\(2\)](#page-20-2) =⇒ [\(1\)](#page-20-1). Define

$$
f_n(x) = \min_{y \in \mathcal{X}_n} ||x - y||, \qquad x \in \mathcal{X}.
$$

By hypothesis [\(2\)](#page-20-2), fn(x) → 0 for every x ∈ X . Moreover for any x, z ∈ X ,

$$
\left|f_n(x) - f_n(z)\right| = \left|\min_{y \in \mathcal{X}_n} \|x - y\| - \min_{y \in \mathcal{X}_n} \|z - y\|\right| \le \|x - z\|,
$$

so {fn} is equicontinuous on the compact set X . Since f<sup>n</sup> → 0 pointwise, the Arzela–Ascoli theorem upgrades to uniform ` convergence of the entire sequence (instead of just a subsequence):

$$
\lim_{n \to \infty} \sup_{x \in \mathcal{X}} f_n(x) = \lim_{n \to \infty} \sup_{x \in \mathcal{X}} \min_{y \in \mathcal{X}_n} ||x - y|| = 0.
$$

Hence [\(1\)](#page-20-1) holds, completing the proof.

Note that condition (1) in Theorem [B.3](#page-20-3) is equivalent to Definition 1 of a "discrete refinement" in [\(Kovachki et al.,](#page-11-8) [2024\)](#page-11-8).

The following lemma holds.

<span id="page-21-1"></span>Lemma B.4 (Weak Convergence of Discretizations of Measures). *Let* µ ∈ X *be absolutely continuous, and* (µn)n∈<sup>N</sup> *be a sequence of discretizations of* µ *supported on a uniform discretization* (Xn)n∈<sup>N</sup> *of* X *. Then* µ<sup>n</sup> *converges weakly to* µ*.*

*Proof.* Let f ∈ Cb(X ) be a test function. We have to show that

$$
\int_{\mathcal{X}} f d\mu_n \xrightarrow{n \to \infty} \int_{\mathcal{X}} f d\mu.
$$

Since X is compact and f : X → R is continuous, by the Heine–Cantor theorem f is uniformly continuous. Hence, for every ε > 0 there exists δ > 0 such that

$$
||x - y|| < \delta \quad \Longrightarrow \quad |f(x) - f(y)| < \varepsilon \quad \text{for all } x, y \in \mathcal{X}.
$$

Since

$$
\sup_{x \in \mathcal{X}} \min_{1 \le i \le n} ||x - x_i^n|| \xrightarrow[n \to \infty]{} 0,
$$

we can choose n ′ such that for all n ≥ n ′ ,

$$
\sup_{x \in \mathcal{X}} \min_{1 \le i \le n} \|x - x_i^n\| < \delta.
$$

In particular, for each x ∈ X , there is some x n <sup>i</sup> ∈ X<sup>n</sup> with ∥x − x n i ∥ < δ, giving

<span id="page-21-0"></span>
$$
|f(x) - f(x_i^n)| < \varepsilon \quad \text{whenever } \|x - x_i^n\| < \delta. \tag{16}
$$

Let

$$
\Omega_i^n = \left\{ x \in \mathcal{X} : \|x - x_i^n\| \le \|x - x_j^n\| \text{ for all } j = 1, \dots, n \right\}
$$

as above. These sets form a partition of X (up to measure-zero boundaries). Then for all n ≥ n ′ , we have (using equation [\(16\)](#page-21-0)):

$$
\left| \int_{\mathcal{X}} f d\mu_n - \int_{\mathcal{X}} f d\mu \right| = \left| \sum_{i=1}^n \int_{\Omega_i^n} (f(x_i^n) - f(x)) d\mu(x) \right|
$$
  
$$
\leq \sum_{i=1}^n \int_{\Omega_i^n} |f(x_i^n) - f(x)| d\mu(x)
$$
  
$$
\leq \sum_{i=1}^n \epsilon \mu(\Omega_i^n)
$$
  
$$
= \epsilon,
$$

and letting ϵ → 0 finishes the proof.

In Proposition [2,](#page-3-4) we used the "canonical extension" for dual potentials. For a pair of dual variables (f, g) solving the dual problem [\(3\)](#page-1-1) between µ and ν, their canonical extensions are defined by f and g satisfying the following conditions:

$$
f(x) = -\epsilon \log \int_{\mathcal{X}} \exp\left(\frac{1}{\epsilon} (g(y) - c(x, y))\right) d\nu(y),
$$
$$
g(x) = -\epsilon \log \int_{\mathcal{X}} \exp\left(\frac{1}{\epsilon} (f(y) - c(x, y))\right) d\mu(y).
$$

We refer to [\(Santambrogio,](#page-11-20) [2015;](#page-11-20) [Feydy et al.,](#page-10-6) [2018\)](#page-10-6) for more details.

We can now state and prove a formal version of Proposition [2.](#page-3-4)

Proposition 2. *(Formal) Let* c(x, y) : X ×X → R *be Lipschitz continuous in both its arguments, and* X ⊂ R <sup>N</sup> *compact. Let* (µn)n∈N*,* (νn)n∈<sup>N</sup> *be discretization sequences for absolutely continuous* µ, ν ∈ P(X )*, supported on a uniform discretization* (Xn)n∈<sup>N</sup> *of* X *. Let* (fn, gn) *be the (unique) extended dual potentials of* (µn, νn) *such that* fn(x0) = 0 *for some* x<sup>0</sup> ∈ X *and all* n*. Let* (f, g) *be the (unique) dual potentials of* (µ, ν) *such that* f(x0) = 0*. Then* f<sup>n</sup> *and* g<sup>n</sup> *converge uniformly to* f *and* g *on all of* X *.*

*Proof.* By Lemma [B.4,](#page-21-1) we know that µ<sup>n</sup> ⇀ µ and ν<sup>n</sup> ⇀ ν. The statement now follows immediately from Proposition 13 in [\(Feydy et al.,](#page-10-6) [2018\)](#page-10-6).

Theorem 3. *Let* 0 < λ ≤ 1 *and* G<sup>θ</sup> : R <sup>d</sup> → R <sup>d</sup> *be defined via*

$$
G_{\theta}(z) = \text{ReLU}(NN_{\theta}(z) + \lambda z),
$$

*where* z ∼ ρ<sup>z</sup> = N (0, I)*, and where* NN<sup>θ</sup> : R <sup>d</sup> → R d *is Lipschitz continuous with* Lip(NNθ) = L < λ*. Then* G<sup>θ</sup> *is Lipschitz continuous with* Lip(q) < L + λ*, and* G˜(z) := NNθ(z) + λz *is invertible on* R d *. Furthermore, for any* x ∈ R d ≥0 *it holds*

$$
\rho_{G_{\boldsymbol{\theta} \# P_{\boldsymbol{z}}}(\boldsymbol{x}) \geq \frac{1}{(L+\lambda)^d} \mathcal{N}\left(\tilde{\mathrm{G}}_{\boldsymbol{\theta}}^{-1}(\boldsymbol{x}) | 0, I\right).
$$

*In other words,* Gθ#ρ<sup>z</sup> *has positive density at any non-negative* x ∈ R d ≥0 *.*

*Proof.* Since the Lipschitz constant of the sum of two functions is bounded by the sum of the Lipschitz constants of the two functions, we have

$$
\operatorname{Lip}(\tilde{\mathcal{G}}_{\theta}) \leq L + \lambda.
$$

From Theorem 1 in [\(Behrmann et al.,](#page-9-15) [2019\)](#page-9-15), it follows that G˜ <sup>θ</sup> is invertible, and Lemma 2 therein implies

$$
\mathrm{Lip}(\tilde{\mathrm{G}}_{\boldsymbol{\theta}}^{-1}) \leq \frac{1}{\lambda - L}.
$$

The Lipschitz continuity of G˜ θ −1 implies that for any h, z ∈ R <sup>d</sup> with h ̸= 0, we have

$$
\begin{aligned} \left\| \nabla \tilde{\mathbf{G}}_{\theta}(\boldsymbol{z}) \boldsymbol{h} \right\| &= \lim_{t \to 0} \left\| \frac{\tilde{\mathbf{G}}_{\theta}(\boldsymbol{z} + t \boldsymbol{h}) - \tilde{\mathbf{G}}_{\theta}(\boldsymbol{z})}{t} \right\| \\ &\geq \frac{1}{\mathrm{Lip}(\tilde{\mathbf{G}}_{\theta}^{-1})} \lim_{t \to 0} \left\| \frac{\tilde{\mathbf{G}}_{\theta}^{-1}(\tilde{\mathbf{G}}_{\theta}(\boldsymbol{z} + t \boldsymbol{h})) - \tilde{\mathbf{G}}_{\theta}^{-1}(\tilde{\mathbf{G}}_{\theta}(\boldsymbol{z}))}{t} \right\| \\ &= \frac{1}{\mathrm{Lip}(\tilde{\mathbf{G}}_{\theta}^{-1})} \left\| \boldsymbol{h} \right\| \\ &\geq 0, \end{aligned}
$$

which shows that ∇G˜ <sup>θ</sup> is invertible everywhere. Hence, by the inverse function theorem, we get

$$
\nabla \tilde{\mathbf{G}}_{\theta}^{-1}(\mathbf{x}) = \nabla \tilde{\mathbf{G}}_{\theta}^{-1} (\tilde{\mathbf{G}}_{\theta} (\tilde{\mathbf{G}}_{\theta}^{-1}(\mathbf{x}))) = (\nabla \tilde{\mathbf{G}}_{\theta} (\tilde{\mathbf{G}}_{\theta}^{-1}(\mathbf{x})))^{-1}
$$

for any x ∈ R d . Furthermore, similar to above, we have

$$
\left\|\nabla \tilde{\mathbf{G}}_{\boldsymbol{\theta}}(\boldsymbol{z})\boldsymbol{e}_i\right\| = \lim_{t\to 0}\left\|\frac{\tilde{\mathbf{G}}_{\boldsymbol{\theta}}(\boldsymbol{z}+t\boldsymbol{e}_i)-\tilde{\mathbf{G}}_{\boldsymbol{\theta}}(\boldsymbol{z})}{t}\right\| \leq \mathrm{Lip}(\tilde{\mathbf{G}}_{\boldsymbol{\theta}})\lim_{t\to 0}\left\|\frac{\boldsymbol{z}+t\boldsymbol{e}_i-\boldsymbol{z}}{t}\right\| \leq L+\lambda,
$$

where e<sup>i</sup> is the i th unit vector. Hence, we get from Hadamard's inequality that

$$
|\text{det}\nabla \tilde{\text{G}}_{\boldsymbol{\theta}}(\boldsymbol{z})| \leq \Pi_i \left\| \nabla \tilde{\text{G}}_{\boldsymbol{\theta}}(\boldsymbol{z}) \boldsymbol{e}_i \right\| \leq \Pi_i (L+\lambda) = (L+\lambda)^d.
$$

Putting everything together, by change of variables, we get for any x ∈ R d :

$$
\rho_{\tilde{G}_{\theta\#\rho_{\boldsymbol{z}}}}(\boldsymbol{x}) = \rho_{\boldsymbol{z}}(\tilde{G}_{\theta}^{-1}(\boldsymbol{x})) \left| \det \nabla \tilde{G}_{\theta}^{-1}(\boldsymbol{x}) \right|
$$
  
\n
$$
= \rho_{\boldsymbol{z}}(\tilde{G}_{\theta}^{-1}(\boldsymbol{x})) \left| \det \nabla \tilde{G}_{\theta}(\tilde{G}_{\theta}^{-1}(\boldsymbol{x})) \right|^{-1}
$$
  
\n
$$
\geq \frac{1}{(L+\lambda)^{d}} \rho_{\boldsymbol{z}}(\tilde{G}_{\theta}^{-1}(\boldsymbol{x}))
$$
  
\n
$$
= \frac{1}{(L+\lambda)^{d}} \mathcal{N}(\tilde{G}_{\theta}^{-1}(\boldsymbol{x}) | 0, I).
$$

Now clearly, if x ∈ R d ≥0 , then

$$
\rho_{\mathrm{G}_{\boldsymbol{\theta}}\# \rho_{\boldsymbol{z}}}(\boldsymbol{x}) \geq \rho_{\tilde{\mathrm{G}}_{\boldsymbol{\theta}}\# \rho_{\boldsymbol{z}}}(\boldsymbol{x}),
$$

as for any z with G˜(z) = x, we also have G(z) = x. Thus, we also have

$$
\rho_{\mathbf{G}_{\boldsymbol{\theta}}\# \rho_{\mathbf{z}}}(\boldsymbol{x}) \geq \frac{1}{(L+\lambda)^d} \mathcal{N}(\tilde{\mathbf{G}}_{\boldsymbol{\theta}}^{-1}(\boldsymbol{x}) | 0, I),
$$

which finishes the proof.

Corollary 4. *Let* G˜ <sup>θ</sup> = G˜ θ<sup>1</sup> ◦ G˜ θ<sup>1</sup> ◦ ... ◦ G˜ <sup>θ</sup><sup>R</sup> *be a composition of functions* G˜ θi *, each of which is of the form as in Theorem [3.](#page-3-1) Let* z ∼ ρ<sup>z</sup> = N (0, I)*. Then*

$$
\rho_{\tilde{G}_{\boldsymbol{\theta} \# \rho_{\boldsymbol{z}}}(\boldsymbol{x}) \geq \frac{1}{(L+\lambda)^{Rd}} \mathcal{N}\left(\tilde{\mathrm{G}}_{\boldsymbol{\theta}}^{-1}(\boldsymbol{x}) | 0, I\right)
$$

*for any* x ∈ R d *. As in Theorem [3,](#page-3-1) this also holds for any* x ∈ R d ≥0 *if* G˜ <sup>θ</sup> *is followed by a ReLU activation.*

*Proof.* Consider the case where G˜ <sup>θ</sup> = G˜<sup>1</sup> θ<sup>1</sup> ◦ G˜<sup>2</sup> θ<sup>2</sup> . Then for any x ∈ R d , we get from the proof of Theorem [3](#page-3-1) above:

$$
\rho_{\tilde{G}_{\theta\#\rho_{\mathbf{z}}}}(\mathbf{x}) \geq \frac{1}{(L+\lambda)^d} \rho_{\tilde{G}_{\theta_2\#\rho_{\mathbf{z}}}^2}((\tilde{G}_{\theta_1}^1)^{-1}(\mathbf{x}))
$$
\n
$$
\geq \frac{1}{(L+\lambda)^{2d}} \mathcal{N}\left(\left(\tilde{G}_{\theta_2}^2\right)^{-1}\left(\left(\tilde{G}_{\theta_1}^1\right)^{-1}(\mathbf{x})\right)|0,I\right)
$$
\n
$$
=\frac{1}{(L+\lambda)^{2d}} \mathcal{N}(\tilde{G}_{\theta}^{-1}(\mathbf{x})|0,I).
$$

The claim now follows by induction over the layers of G˜ <sup>θ</sup>. Note that if G˜ <sup>θ</sup> is followed by a ReLU activation, this inequality also holds for any x ∈ R d ≥0 , similar to Theorem [3.](#page-3-1)

Next, we prove Proposition [5.](#page-4-2) The proof is based on the *Hilbert projective metric*. For two vectors u, v ∈ R n <sup>+</sup>, it is defined as

$$
d_H(\boldsymbol{u}, \boldsymbol{v}) := \max_i [\log(\boldsymbol{u}_i) - \log(\boldsymbol{v}_i)] - \min_i [\log(\boldsymbol{u}_i) - \log(\boldsymbol{v}_i)],
$$

and can be shown to be a distance on the projective cone R n <sup>+</sup>/ ∼, where u ∼ u ′ if u = ru ′ for some r > 0 [\(Peyre & Cuturi](#page-11-1) ´ , [2019;](#page-11-1) [Franklin & Lorenz,](#page-10-16) [1989\)](#page-10-16). For f = log(u) and g = log(v), we thus define the following loss:

$$
\mathrm{L}_H({\bm f},{\bm g}) := \max_i [{\bm f_i}-{\bm g_i}] - \min_i [{\bm f_i}-{\bm g_i}].
$$

<span id="page-23-0"></span>Lemma B.5. *Let* f, g ∈ R <sup>n</sup>*. Then*

$$
\mathrm{L}_H(\bm{f},\bm{g})\leq \sqrt{2}\|\bm{f}-\bm{g}\|_2.
$$

√

n LH(f, g).

*If, in addition,* P i f<sup>i</sup> = P i g<sup>i</sup> = 0*, then*

∥f − g∥<sup>2</sup> ≤

*Proof.* Let h = f − g. For the first inequality, observe that LH(f, g) = max<sup>i</sup> h<sup>i</sup> − min<sup>i</sup> h<sup>i</sup> . Let j ∗ and k <sup>∗</sup> be the indices achieving max<sup>i</sup> h<sup>i</sup> and min<sup>i</sup> h<sup>i</sup> , respectively. Define the vector e such that e<sup>j</sup> <sup>∗</sup> = 1, ek<sup>∗</sup> = −1, and e<sup>i</sup> = 0 for all other i. Then: √

$$
\mathrm{L}_H({\bm f},{\bm g})={\bm e}\cdot{\bm h}\leq\|{\bm e}\|_2\,\|{\bm h}\|_2=\sqrt{2}\,\|{\bm f}-{\bm g}\|_2\,.
$$

Now assume that P i f<sup>i</sup> = P i g<sup>i</sup> = 0. Set M = max<sup>i</sup> h<sup>i</sup> and m = min<sup>i</sup> h<sup>i</sup> . If all h<sup>i</sup> = 0, both statements are trivial. Hence, assume at least one of the h<sup>i</sup> is not zero. Since P <sup>i</sup> h<sup>i</sup> = P i f<sup>i</sup> − g<sup>i</sup> = 0, this implies M > 0 and m < 0. For any index i, h<sup>i</sup> ≤ M, and thus

$$
(\mathbf{h}_i)^2 \le M^2 \le (M-m)^2 = \mathcal{L}_H(\mathbf{f},\mathbf{g})^2.
$$

Summing over all indices, we have:

$$
\|\bm{f}-\bm{g}\|_2^2 = \|\bm{h}\|_2^2 = \sum_{i=1}^n (\bm{h}_i)^2 \leq n \cdot \mathrm{L}_H(\bm{f},\bm{g})^2.
$$

Taking the square root yields:

$$
\|\bm{f}-\bm{g}\|_2\leq \sqrt{n}\;\mathrm{L}_H(\bm{f},\bm{g}).
$$

This finishes the proof.

Proposition 5. *For two discrete measures* (µ, ν) *with* n *particles, let* g *be a potential solving the dual problem,* g<sup>ϕ</sup> = Sϕ(µ, ν)*, and* gτ<sup>k</sup> = τk(µ, ν, gϕ) *the target. Without loss of generality, assume that* P i g<sup>i</sup> = P i gτ<sup>k</sup> <sup>i</sup> = 0*. Then*

$$
L_2(\boldsymbol{g}_{\boldsymbol{\phi}}, \boldsymbol{g}) \leq c(K, k, n) L_2(\boldsymbol{g}_{\boldsymbol{\phi}}, \boldsymbol{g}_{\tau_k})
$$

*for some constant* c(K, k, n) > 1 *depending only on the Gibbs kernel* K*,* k *and* n*.*

*Proof.* We first show a similar inequality as in Proposition [5](#page-4-2) for the Hilbert loss. A well-known fact about the Hilbert metric is that positive matrices (in our case, the Gibb's kernel K) act as strict contractions on positive vectors with respect to the Hilbert metric (cf. Theorem 4.1 in [\(Peyre & Cuturi](#page-11-1) ´ , [2019\)](#page-11-1)). More precisely, we have

$$
d_H(Kv, Kv') \leq \lambda(K) d_H(v, v')
$$

for any positive vectors v, v ′ ∈ R <sup>n</sup>, where

$$
\lambda(K) := \frac{\sqrt{\eta(K)} - 1}{\sqrt{\eta(K)} + 1}, \quad \eta(K) := \max_{i, j, k, l} \frac{K_{ik} K_{jl}}{K_{jk} K_{il}}.
$$

The same inequality also holds for K<sup>⊤</sup> in place of K. Note that by definition, η(K) ≥ 1, hence 0 < λ(K) < 1. Now consider a starting vector v 0 to the Sinkhorn algorithm, and let v <sup>l</sup> denote the l th iterate of the vector. Denote by v ⋆ the limit liml→∞ v <sup>l</sup> of the algorithm. Then (letting ′/ ′ denote element-wise division):

$$
d_H(\mathbf{v}^{l+1}, \mathbf{v}^*) = d_H(\mathbf{\nu}/K^{\top}\mathbf{u}^{l+1}, \mathbf{\nu}/K^{\top}\mathbf{u}^*)
$$
  
\n
$$
= d_H(K^{\top}\mathbf{u}^{l+1}, K^{\top}\mathbf{u}^*)
$$
  
\n
$$
\leq \lambda(K) d_H(\mathbf{u}^{l+1}, \mathbf{u}^*)
$$
  
\n
$$
= \lambda(K) d_H(\mathbf{\mu}/K\mathbf{v}^l, \mathbf{\mu}/K\mathbf{v}^*)
$$
  
\n
$$
= \lambda(K) d_H(K\mathbf{v}^l, K\mathbf{v}^*)
$$
  
\n
$$
\leq \lambda(K)^2 d_H(\mathbf{v}^l, \mathbf{v}^*) ,
$$

where we used the Hilbert metric inequality twice, once on K and once on K<sup>⊤</sup>. Iteratively applying this inequality and translating into log-space notation, this gives us

$$
\mathrm{L}_H(\boldsymbol{g}_{\tau_k},\boldsymbol{g})\leq \lambda(K)^{2k}\,\mathrm{L}_H(\boldsymbol{g}_{\boldsymbol{\phi}},\boldsymbol{g}).
$$

For now, assume that P i g<sup>ϕ</sup><sup>i</sup> = 0. By triangle inequality,

$$
\mathop{\rm L{}}\nolimits_H(\bm{g} _{\bm{\phi}} ,\bm{g} )\leq \mathop{\rm L{}}\nolimits_H(\bm{g} _{\bm{\phi}} ,\bm{g} _{\tau_k} )+\mathop{\rm L{}}\nolimits_H(\bm{g} _{\tau_k} ,\bm{g} )\leq \mathop{\rm L{}}\nolimits_H(\bm{g} _{\bm{\phi}} ,\bm{g} _{\tau_k} )+\lambda (K)^{2k}\mathop{\rm L{}}\nolimits_H(\bm{g} _{\bm{\phi}} ,\bm{g} ),
$$

which gives us

$$
\operatorname{L}_H(\boldsymbol{g}_{\boldsymbol{\phi}},\boldsymbol{g})\leq \frac{1}{1-\lambda(K)^{2k}}\operatorname{L}_H(\boldsymbol{g}_{\boldsymbol{\phi}},\boldsymbol{g}_{\tau_k})=:c(K,k)\operatorname{L}_H(\boldsymbol{g}_{\boldsymbol{\phi}},\boldsymbol{g}_{\tau_k}).
$$

Combining this with Lemma [B.5](#page-23-0) yields

<span id="page-25-0"></span>
$$
\|\boldsymbol{g}_{\phi}-\boldsymbol{g}\|_{2} \leq \sqrt{n}L_{H}(\boldsymbol{g}_{\phi},\boldsymbol{g}) \leq \sqrt{n}c(K,k)L_{H}(\boldsymbol{g}_{\phi},\boldsymbol{g}_{\tau_{k}}) \leq 2\sqrt{n}c(K,k)\left\|\boldsymbol{g}_{\phi}-\boldsymbol{g}_{\tau_{k}}\right\|_{2} = c(K,k,n)\left\|\boldsymbol{g}_{\phi}-\boldsymbol{g}_{\tau_{k}}\right\|_{2},\tag{17}
$$

from which the claim follows by squaring both sides. We are left with proving the general case when P i gϕ<sup>i</sup> ̸= 0. Write g<sup>ϕ</sup> = gˆ<sup>ϕ</sup> + g¯ϕ, where g¯<sup>ϕ</sup> is equal to <sup>1</sup> n P i gϕ<sup>i</sup> in each entry, s.t. gˆ<sup>ϕ</sup> sums to zero. We then get

<span id="page-25-1"></span>
$$
L_2(g_{\phi}, g) = ||\hat{g}_{\phi} - g||^2 + ||\bar{g}_{\phi}||^2, \qquad (18)
$$

as

$$
\langle \hat{\bm{g}}_{\bm{\phi}} - \bm{g}, \bar{\bm{g}}_{\bm{\phi}} \rangle = 0.
$$

Similarly, we get

<span id="page-25-2"></span>
$$
L_2(g_{\phi}, g_{\tau_k}) = \|\hat{g}_{\phi} - g_{\tau_k}\|^2 + \|\bar{g}_{\phi}\|^2.
$$
 (19)

Combining equations [\(17\)](#page-25-0), [\(18\)](#page-25-1) and [\(19\)](#page-25-2), we get

$$
\begin{aligned} \mathrm{L}_2(\bm{g}_{\bm{\phi}},\bm{g}) &= \left\|\hat{\bm{g}}_{\bm{\phi}} - \bm{g}\right\|^2 + \left\|\bar{\bm{g}}_{\bm{\phi}}\right\|^2 \\ & \leq c\,\mathrm{L}_2(\hat{\bm{g}}_{\bm{\phi}},\bm{g}_{\tau_k}) + \left\|\bar{\bm{g}}_{\bm{\phi}}\right\|^2 \\ &= c\left(\mathrm{L}_2(\bm{g}_{\bm{\phi}},\bm{g}_{\tau_k}) - \left\|\bar{\bm{g}}_{\bm{\phi}}\right\|^2\right) + \left\|\bar{\bm{g}}_{\bm{\phi}}\right\|^2 \\ &= c\,\mathrm{L}_2(\bm{g}_{\bm{\phi}},\bm{g}_{\tau_k}) + (1-c)\left\|\bar{\bm{g}}_{\bm{\phi}}\right\|^2 \\ & \leq c\,\mathrm{L}_2(\bm{g}_{\bm{\phi}},\bm{g}_{\tau_k}), \end{aligned}
$$

where the last inequality follows from the fact that 1 − c < 0. This finishes the proof.

*Remark* B.6*.* Looking at the proof of Proposition [5,](#page-4-2) one might wonder why we didn't opt for the Hilbert projective metric as the loss directly. We tried using it instead of L2, and it works quite well, but training with L2 seems to have an edge, probably because the indifference of the Hilbert projetive metric to constant shifts is not a helpful inductive bias for deep learning.

## <span id="page-26-0"></span>C. Training Details

Generator Architecture. Recall that the generator is of the form

$$
G_{\theta}: \mathbb{R}^{d} \to \mathcal{P}(X) \times \mathcal{P}(X)
$$
  
$$
z \sim \rho_{\mathbf{z}} \mapsto R \left[ \text{ReLU} \left( \text{NN}_{\theta}(z) + \lambda I_{d,d'}(z) \right) + \delta \right],
$$

where we set λ = 1.0, δ = 1e-6 (note we *first* normalize, then add δ, and then *normalize again* in practice), and z is of size 2 · 10 × 10. R normalizes and randomly downsizes output distributions to resolutions between 10 × 10 and 64 × 64 (per distribution). This improves generalization of the FNO S<sup>ϕ</sup> across resolutions, which is true for FNOs in general [\(Li et al.,](#page-11-13) [2024a\)](#page-11-13). NN<sup>θ</sup> is a five-layer fully connected MLP, where all hidden layers are of dimension 0.04 · 64<sup>2</sup> , and the output is of dimension 2 · 64<sup>2</sup> . All layers except the output layer contain Batch Normalization and ELU activations; the last layer has a sigmoid activation only. We note the architecture might seem strange, as the network is relatively deep, while the hidden layers are relatively narrow. However, this architecture worked best amongst an extensive sweep of architectures.

Applying Theorem [3.](#page-3-1) In the following, we discuss the relation between our generator G<sup>θ</sup> and Theorem [3](#page-3-1) in more detail. Note that Theorem [3](#page-3-1) is not directly applicable to our setting for a few reasons: First, we add a small constant η to the generator's output. This constant ensures that all training samples are positive everywhere, and vastly improves learning speed as it ensures that all inputs are active. However, this is not restrictive of the problem, as the Sinkhorn algorithm requires inputs to be positive anyways. Second, in Theorem [3](#page-3-1) both in- and outputs to G<sup>θ</sup> have the same dimension. This could be achieved in our setting by choosing the input dimension equal to the output dimension, i.e. Id,n equal to the identity. However, in practice, using lower-dimensional inputs achieves significantly better results. This can be argued for by the manifold hypothesis [\(Fefferman et al.,](#page-10-17) [2016\)](#page-10-17), i.e. the fact that typically, datasets live on low-dimensional manifolds embedded in high-dimensional spaces. Depending on the application, i.e. the expected target dataset dimension, the dimension of the input can be adjusted accordingly. Finally, note that the theorem assumes that NN<sup>θ</sup> is Lipschitz continuous with Lipschitz constant L < λ, where λ is the scaling factor of the skip connection. We do not enforce this constraint, as not doing so yields empirically better results. Still, Theorem [3](#page-3-1) goes to show that our algorithm's performance is not bottlenecked by the generator's inability to generalize. We note that a bound on the Lipschitz constant is not necessary for invertibility of ResNets; other approaches have been suggested in the literature, e.g. through the lens of ODEs [\(Chang et al.,](#page-9-16) [2017\)](#page-9-16) or by partitioning input dimensions [\(Jacobsen et al.,](#page-10-18) [2018\)](#page-10-18). It is also possible to directly divide by the Lipschitz constant of each layer [\(Serrurier et al.,](#page-11-21) [2023\)](#page-11-21); these approaches could be studied in future research.

We will now describe how one can bound the Lipschitz constant of the generator. Since λ = 1.0, we need to make sure that the Lipschitz constant of net<sup>θ</sup> is smaller than 1 in order for Theorem [3](#page-3-1) to be applicable. Since the Lipschitz constant of a composition of functions is bounded by the product of the Lipschitz constants of each component function, this means we have to bound the product of the Lipschitz constants of components of netθ. ELU is Lipschitz continuous with constant 1, whereas sigmoid's Lipschitz constant is 0.25. Furthermore, for a batch normalization layer BN, we have

$$
\|\mathbf{BN}(x) - \mathbf{BN}(y)\| = \left\|\frac{x - \mu_b}{\sigma_b} - \frac{y - \mu_b}{\sigma_b}\right\| = \frac{1}{\sigma_b} \|x - y\|,
$$

where µ<sup>b</sup> and σ<sup>b</sup> denote the empirical mean and standard deviation of the batch. Since we draw our data from a standard normal Gaussian, we have E[σb] = 1, i.e. in expectation, the batch normalization layer is Lipschitz with constant 1. Hence, all that remains is to bound the product of Lipschitz constants of the three linear layers by (any number smaller than) 4 (because the constant of sigmoid is 0.25, this will ensure that the network has a Lipschitz constant smaller than 1), for which it suffices to bound the operator norms of the weight matrix of each layer. In practice, these can be approximated with the power method as in [\(Gouk et al.,](#page-10-19) [2020\)](#page-10-19) to find a lower bound on the Lipschitz constant of each linear layer, and these bounds can be used to add a soft constraint to the loss. Empirically, this suffices to bound the Lipschitz constant of the generator. Alternatively, one can use a hard constraint as outlined in [\(Behrmann et al.,](#page-9-15) [2019\)](#page-9-15). However, empirically, this proved detrimental to training, hence we did *not* control the Lipschitz constant during our training. Yet, Theorem [3](#page-3-1) is still of value, as it goes to show that our algorithm's performance is not bottlenecked by the generator's inability to generalize. We leave properly enforcing the Lipschitz constraint for future research.

Architecture of Sϕ. Our FNO architecture follows the general structure outlined in Section [A.5.](#page-17-0) We set d<sup>v</sup><sup>i</sup> = 64 for all i; recall this is the hidden dimension in the Fourier layer. We set the number of Fourier features selected from the Fourier transform to 10 × 10, i.e. 10 along each of the two dimensions of the domain. The (complex) weight matrices of the neural network in Fourier space, i.e. the one acting on the Fourier features, are tensors of shape (d<sup>v</sup><sup>i</sup> , 4d<sup>v</sup><sup>i</sup> , Nmodes<sup>x</sup> , Nmodes<sup>y</sup> ) =

(64, 256, 10, 10) and (4dv<sup>i</sup> , dv<sup>i</sup> , Nmodes<sup>x</sup> , Nmodes<sup>y</sup> ) = (256, 64, 10, 10) respectively, i.e. the hidden dimension is four times the hidden dimension of v<sup>i</sup> . Note that since these are complex layers, each layer has two (real) weight tensors of this shape, one for the real and one for the complex part. These layers are the only complex layers in the network Sϕ. The inputs to the layer are of shape (dv<sup>i</sup> , Nmodes<sup>x</sup> , Nmodes<sup>y</sup> ) = (64, 10, 10) (in C) and multiplied along all dimensions by the weights, i.e. for input xˆ ∈ C <sup>64</sup>,10,<sup>10</sup> and weight matrix A ∈ C <sup>64</sup>,256,10,<sup>10</sup> (the first of the two layers):

$$
\hat{y}_{o,n,m} = \sum_{i} A_{i,o,n,m} \hat{x}_{i,n,m}.
$$

The activation used within this network, as well as after each Fourier block, is GeLU. The lifting layer P, bypass layer W, and projection layer Q are 2D convolutions with kernel size 1.

<span id="page-27-0"></span>Hyperparameters. In Table [3](#page-27-0) we present all relevant hyperparameters again for convenience.

| Hyperparameter                        | Value                |
|---------------------------------------|----------------------|
| # params Gθ                           | 272k                 |
| # layers Gϕ                           | 5                    |
| hidden dims Gϕ                        | (164, 164, 164, 164) |
| δ (eq. (6))                           | 1e-6                 |
| λ (eq. (6))                           | 1                    |
| d (dimension of latent z)             | 2 · 10 × 10 = 200    |
| optimizer Gϕ                          | Adam                 |
| activations Gϕ                        | ELU                  |
| β1<br>(initial learning rate Gθ<br>)  | 0.001                |
| learning rate decay Gθ                | 1                    |
| weight decay Gϕ                       | 0                    |
| # params Sϕ                           | 26M                  |
| Number of Fourier layers              | 4                    |
| dvi<br>(dim. in Fourier blocks)       | 64                   |
| hidden dim. of Fourier NN             | 256                  |
| # layers in Fourier NN                | 2                    |
| Nmodesx<br>(# Fourier modes)          | 10                   |
| Nmodesy<br>(# Fourier modes)          | 10                   |
| optimizer Sϕ                          | AdamW                |
| σ (activation in Sϕ)                  | GeLU                 |
| α1<br>(initial learning rate Sϕ)      | 1e-4                 |
| learning rate decay Sϕ                | 0.9999               |
| weight decay Sθ                       | 1e-4                 |
| minimum training sample size          | 10 × 10              |
| maximum training sample size          | 64 × 64              |
| # training samples                    | 200M                 |
| batch size                            | 5000                 |
| mini batch size                       | 64                   |
| T (number batches)                    | 40k                  |
| ϵ (for Sinkhorn targets)              | 0.01                 |
| k (# Sinkhorn iterations for targets) | 5                    |

Table 3. Training hyperparameters.

Code. Source code for UNOT, including the weights for the model used in the experiments, can be found at [https:](https://github.com/GregorKornhardt/UNOT) [//github.com/GregorKornhardt/UNOT](https://github.com/GregorKornhardt/UNOT).

## <span id="page-28-1"></span>D. Additional Experiments and Materials

### <span id="page-28-0"></span>D.1. Test Sets

In Figure [10](#page-28-3) we show samples from our test datasets. For some of the experiments in the appendix, we included two additional datasets, the "cars" class which is also from the Quick, Draw! dataset, and the [Facial Expressions](https://www.kaggle.com/datasets/mhantor/facial-expression) dataset [\(Hashan,](#page-10-20) [2022\)](#page-10-20), which consists of 48×48-dimensional greyscale images. The datasets are very diverse, and range in dimensionality from very low (MNIST) to fairly low (BEARS, CARS), medium high (CIFAR) and very high (EXPRESSIONS, LFW).

Figure [11](#page-29-0) shows samples from our spherical datasets (where only part of the sphere is visible here). To create a grid on the sphere, we sample elevation angles θ uniformly in -− π 2 , π 2 and azimuthal angles φ uniformly in -0, 2π . Concretely, we set

$$
\theta_i = -\frac{\pi}{2} + \frac{i}{n-1} \pi
$$
,  $\varphi_j = \frac{2\pi j}{n-1}$ ,  $i, j = 0, ..., n-1$ ,

and form the n × n grid (θ<sup>i</sup> , φ<sup>j</sup> ) i,j . Each pair (θ<sup>i</sup> , φ<sup>j</sup> ) is mapped to a point on the sphere by

$$
x = \cos(\theta_i) \cos(\varphi_j), \quad y = \cos(\theta_i) \sin(\varphi_j), \quad z = \sin(\theta_i).
$$

![](_page_28_Figure_8.jpeg)

<span id="page-28-3"></span>Figure 10. Test dataset samples on the unit square.

### <span id="page-28-2"></span>D.2. Comparison with Meta OT

We trained a Meta OT [\(Amos et al.,](#page-9-5) [2023\)](#page-9-5) network with the official GitHub implementation[12](#page-28-4) and compared it against UNOT on our test datasets, where we rescaled all datasets to 28 × 28, as Meta OT does not natively support inputs of varying sizes. In Table [D.2,](#page-28-2) we report the relative errors on the OT distance (in %) after a single Sinkhorn iteration.

<span id="page-28-4"></span><sup>12</sup><https://github.com/facebookresearch/meta-ot>

![](_page_29_Picture_1.jpeg)

Figure 11. Test dataset samples on the sphere.

Table 4. Relative Errors on the OT distance (in %) after a single Sinkhorn iteration with UNOT's initialization, compared to Meta OT [\(Amos et al.,](#page-9-5) [2023\)](#page-9-5), the Gaussian initialization [\(Thornton & Cuturi,](#page-11-4) [2022\)](#page-11-4), and the default initialization. Datasets rescaled to 28 × 28 such that the Meta OT network can process them.

<span id="page-29-0"></span>

|             | MNIST       | CIFAR       | MNIST-CIFAR | LFW         | BEAR        | LFW-BEAR    |
|-------------|-------------|-------------|-------------|-------------|-------------|-------------|
| UNOT (ours) | 2.7 ± 2.4   | 1.3 ± 1.1   | 2.8 ± 2.6   | 1.5 ± 1.3   | 2.0 ± 1.6   | 1.8 ± 1.3   |
| MetaOT      | 2.4 ± 1.8   | 23.1 ± 15.7 | 11.4 ± 5.8  | 24.6 ± 15.7 | 11.8 ± 8.3  | 31.0 ± 14.8 |
| Gauss       | 18.1 ± 10.0 | 19.7 ± 7.6  | 32.2 ± 8.7  | 21.1 ± 6.5  | 20.4 ± 8.3  | 19.3 ± 6.4  |
| Ones        | 39.5 ± 13.4 | 47.4 ± 20.2 | 74.5 ± 6.9  | 56.9 ± 15.4 | 54.2 ± 13.5 | 66.4 ± 10.8 |

We see that UNOT outperforms Meta OT on all datasets except MNIST, which is to be expected, as Meta OT is explicitly trained on MNIST, while UNOT is not trained on any MNIST data. However, surprisingly, we see that UNOT almost matches Meta OT's performance on MNIST, suggesting strong coverage of MNIST-like distributions by our generator network during training.

### D.3. MLP-UNOT

We mention that in applications of fixed-size distributions, one can replace the Neural Operator with an MLP and achieve similar results for a fraction of the training cost. We note that since the MLP acts on a fixed discrete space one does not need to have equispaced samples. In experiments, we found the MLP approach to also be very reliable for fixed-size inputs, and to vastly outperform the standard initialization of the Sinkhorn algorithm. Notably, it can be trained in just a few minutes to relative errors below 5%.

### <span id="page-30-1"></span>D.4. Generalization across Resolutions

In this section, we show that UNOT successfully generalizes across resolutions. To this end, we downsample resp. upsample our test datasets to resolutions between 10 × 10 and 64 × 64. Figure [12](#page-30-0) shows the relative errors on the transport distance over this range of resolutions after a single Sinkhorn iteration, compared against the default and the Gaussian initializations. (In Section [D.5,](#page-31-0) we also provide some results on upsampling the dimension of the data beyond 64 × 64, i.e. beyond the largest resolution that the network saw during training.) We see that UNOT generalizes very well across all resolutions between 10 × 10 and 64 × 64.

![](_page_30_Figure_3.jpeg)

<span id="page-30-0"></span>Figure 12. Relative error on the transport distance over the image resolution, ranging from 10 × 10 to 64 × 64.

### <span id="page-31-0"></span>D.5. Variable Epsilon

In this section, we provide experimental results on a variant of UNOT that also receives the parameter ϵ as an input. Instead of the pair of measures (µ, ν) encoded as a tensor of size (B, 2, n, n), we use an input size of (B, 3, n, n), where the third channel is equal to ϵ everywhere. During training, we sample epsilon randomly per sample from a distribution with values between 0.01 and 1. Otherwise, training is identical to the training of regular UNOT. In Figure [13,](#page-31-1) we plot the relative errors over ϵ ranging from 0.01 to 1 on the x-axis, and the resolution of the data ranging from 10 × 10 to 70 × 70 on the y-axis (where we downsample resp. upsample the data to these dimensions, cf. Section [D.4;](#page-30-1) note that we still only trained on image resolutions between 10 × 10 and 64 × 64). This variant of UNOT seems to do surprisingly well across different values of ϵ and across a wide range of resolutions, with relatively stable performance across different values of ϵ. However, we can see that when the resolution gets smaller than around 15 × 15, or close to 70 × 70, the error increases.

![](_page_31_Figure_3.jpeg)

<span id="page-31-1"></span>Figure 13. Relative error on the transport distance, over the resolution and varying values of ϵ.

### <span id="page-32-0"></span>D.6. Generated Measures

Figure [14](#page-32-1) shows images created by the generator. The generator creates very different images over the course of training, including highly structured distributions, large areas of mass, and distributions with mass concentrated in very small areas.

![](_page_32_Picture_3.jpeg)

Figure 14. Pairs of training samples before and after 20%, 40%, 60%, 80%, and 100% of training, from left to right (lighter=more mass). Top row: actual training images; bottom row: training samples visualized with a smaller skip constant λ to accentuate learned features.

In Table [D.6,](#page-32-1) we also report the average OT distance error of samples created by the generator at various stages of training. We can see that the generator indeed creates samples that are initially difficult, but that it quickly picks up on them, and by the end of training is capable of predictions for samples from all stages of training.

Table 5. Relative error on OT distance for samples created after 10, 20, ..., 70% of training. Errors for all samples computed at the time of their creation (i.e., after 10, 20, ...% of training) and at the end of training.

<span id="page-32-1"></span>

| Error after % of Training | 0%    | 10%  | 20%  | 30%  | 40%  | 50%  | 60%  | 70%  |
|---------------------------|-------|------|------|------|------|------|------|------|
| At Generation             | 53.2% | 3.1% | 2.1% | 1.6% | 1.8% | 1.7% | 2.1% | 1.9% |
| At End of Training        | 2.0%  | 1.6% | 1.4% | 1.1% | 1.6% | 1.5% | 2.0% | 1.9% |

### <span id="page-33-0"></span>D.7. Additional Experiments

We provide additional results from our experiments in this section. In Table [6,](#page-33-1) we show the average Wasserstein-2 distance of barycenters computed by gradient descent using equation [\(10\)](#page-6-1) to the true barycenter, where we compute the gradient in equation [\(10\)](#page-6-1) from the different initializations and a single Sinkhorn iteration. Figures [15](#page-33-2) and [16](#page-34-0) show the relative error on the OT distance over Sinkhorn iterations for c(x, y) = ∥x − y∥ (on the square) and c(x, y) = arccos(⟨x, y⟩) (on the sphere) resp., complementing Figure [3.](#page-5-3)

In Figure [17,](#page-34-1) we plot the relative error on the transport distance w.r.t. computation time when initializing the Sinkhorn algorithm with UNOT, and compare against the default initialization. We see that particularly on higher dimensional data, UNOT is significantly faster than Sinkhorn. However, interestingly, on MNIST the default initialization actually seems to be faster. We note that these results heavily depend on the hardware used, and that we did not optimize our FNO architecture for performance, so a more efficient architecture would probably lead to even more significant speedups. We have not included the initialization from [\(Thornton & Cuturi,](#page-11-4) [2022\)](#page-11-4) in the plots, as it was very slow for us, even slower than the standard initialization, despite our best efforts to implement it as efficiently as possible. However, from [\(Thornton & Cuturi,](#page-11-4) [2022;](#page-11-4) [Amos et al.,](#page-9-5) [2023\)](#page-9-5) it seems like the speedup should be somewhere between 1.1x and 2x, depending on the dataset, which would make it significantly slower than UNOT on most of our datasets. We mention again that FNOs process complex numbers, but PyTorch is heavily optimized for real number operations. With kernel support for complex numbers, UNOT will likely be much faster.

Finally, in Figures [18](#page-35-0) and [19,](#page-36-0) we plot the *marginal constraint violation* (MCV), defined as

<span id="page-33-3"></span>
$$
\frac{\left\|1_{m}^{T}\Pi - \boldsymbol{\nu}^{T}\right\|_{1} + \left\|\Pi1_{n} - \boldsymbol{\mu}\right\|_{1}}{2}
$$
\n(20)

for a transport plan Π, again for a single Sinkhorn iteration (Figure [18\)](#page-35-0) and over iterations (Figure [19\)](#page-36-0). The MCV measures how far the transport plan is from the marginals µ and ν. It is often used as a stopping criterion for the Sinkhorn algorithm, as the ground truth OT distance is unknown in practice. We compute the predicted transport plan for UNOT via equation [\(4\)](#page-2-5).

<span id="page-33-1"></span>Table 6. Average W<sup>2</sup> distance from the predicted barycenter to the true barycenter on MNIST after 100 gradient steps.

![](_page_33_Figure_8.jpeg)

<span id="page-33-2"></span>Figure 15. Relative Error on the OT distance on the unit square with c(x, y) = ∥x − y∥ for the UNOT initialization compared to the default one, over number of Sinkhorn iterations. Note the y-axis has been rescaled for CIFAR and LFW to fit the curve for the default initialization, and that the Gaussian initialization does not exist for the Euclidean cost function.

![](_page_34_Figure_1.jpeg)

Figure 16. Relative Error on the OT distance on the unit sphere with c(x, y) = arccos(⟨x, y⟩) for the UNOT initialization compared to the default one, over number of Sinkhorn iterations. Note that the Gaussian initialization does not exist for the spherical cost function.

<span id="page-34-1"></span><span id="page-34-0"></span>![](_page_34_Figure_3.jpeg)

Figure 17. Comparison of relative errors on the transport distance over computation time in seconds. Evaluated on an NVIDIA 4090. The x-offset of the UNOT curves corresponds to the time needed for the forward pass through Sϕ.

![](_page_35_Figure_1.jpeg)

<span id="page-35-0"></span>Figure 18. Average marginal constraint violation (see eq. [\(20\)](#page-33-3)) after a single Sinkhorn iteration, for the unit square domain with c(x, y) = ∥x − y∥ 2 (top) and c(x, y) = ∥x − y∥ (middle), and the unit sphere with c(x, y) = arccos(⟨x, y⟩) (bottom). Note that the Gaussian initialization exists only for the squared Euclidean distance cost.

![](_page_36_Figure_1.jpeg)

<span id="page-36-0"></span>Figure 19. Average marginal constraint violation (see eq. [\(20\)](#page-33-3)) over number of Sinkhorn iterations, for the unit square domain with c(x, y) = ∥x − y∥ 2 (top) and c(x, y) = ∥x − y∥ (middle), and the unit sphere with c(x, y) = arccos(⟨x, y⟩) (bottom). Note that the Gaussian initialization exists only for the squared Euclidean distance cost.