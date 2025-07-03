# Geometric properties of cones with applications on the Hellinger-Kantorovich space, and a new distance on the space of probability measures

Vaios Laschos<sup>a</sup> and Alexander Mielkea,b

<sup>a</sup> Weierstraß-Institut für Angewandte Analysis und Stochastik, Berlin

b Institut für Mathematik, Humboldt-Universität zu Berlin

May 15, 2018

### Abstract

We study general geometric properties of cone spaces, and we apply them on the Hellinger– Kantorovich space (M(X), HKα,β). We exploit a two-parameter scaling property of the Hellinger-Kantorovich metric HKα,β, and we prove the existence of a distance SHKα,β on the space of Probability measures that turns the Hellinger–Kantorovich space (M(X), HKα,β) into a cone space over the space of probabilities measures (P(X), SHKα,β). We provide a two parameter rescaling of geodesics in (M(X), HKα,β), and for (P(X), SHKα,β) we obtain a full characterization of the geodesics. We finally prove finer geometric properties, including local-angle condition and partial K-semiconcavity of the squared distances, that will be used in a future paper to prove existence of gradient flows on both spaces.

## 1 Introduction

In [LMS16, LMS17], and independently in [KMV16] and [CP∗15b, CP∗15a], a new family of distances HKα,β on the space M(X) of arbitrary nonnegative and finite measures was introduced, where (X, d<sup>X</sup> ) is a geodesic, Polish space. This new family of Hellinger–Kantorovich distances generalize both the Kantorovich–Wasserstein distance (for α = 1 and β = 0) and the Hellinger-Kakutani distance (for α = 0 and β = 1), allowing for both transportation and creation/annihilation of mass, which is organized in a jointly optimal fashion depending on the ratio of the parameters α and β.

The origin of our work stems from the observation in [LMS16, Prop. 19] that the total mass m(s) = R X 1dµ(s) of a constant-speed geodesic [0, 1] <sup>∋</sup> <sup>s</sup> 7→ <sup>µ</sup>(s) <sup>∈</sup> <sup>M</sup>(X) is a quadratic function in s, viz.

$$
m(s) = (1-s)m(0) + sm(1) - s(1-s)\frac{4}{\beta}\mathsf{H}_{\alpha,\beta}^{2}(\mu(0),\mu(1)).
$$
\n(1.1)

We will show here that this formula is already a consequence of a simpler scaling property, that fully characterizes cone spaces, which in the case of HK<sup>2</sup> α,β, takes the form

$$
\mathsf{H}\mathsf{K}_{\alpha,\beta}^{2}(r_{0}^{2}\mu_{0},r_{1}^{2}\mu_{1})=r_{0}r_{1}\mathsf{H}\mathsf{K}_{\alpha,\beta}^{2}(\mu_{0},\mu_{1})+(r_{0}^{2}-r_{0}r_{1})\frac{4}{\beta}\mu_{0}(X)+(r_{1}^{2}-r_{0}r_{1})\frac{4}{\beta}\mu_{1}(X).
$$
 (1.2)

The property is proved independently in Theorem 3.3 based on the characterization of HK<sup>2</sup> α,β via the logarithmic-entropy functional LETℓ, cf. Theorem 3.1.

This suggests to write arbitrary measures <sup>µ</sup> <sup>∈</sup> <sup>M</sup>(X) \ {0} as

$$
\mu = r^2 \nu \quad \text{with} \quad [\nu, r] \in \mathcal{P}(X) \times (0, \infty), \quad \text{where } r = \sqrt{\mu(X)}, \ \nu = \frac{1}{r^2} \mu,
$$
 (1.3)

and P(X) denotes the probability measures. Thus, the set M(X) can be interpreted as a cone over P(X) in the sense of Section 2, and the Hellinger–Kantorovich distance has the form

$$
\mathsf{H}^2_{\alpha,\beta}(r_0^2\nu_0,r_1^2\nu_1) = \frac{4}{\beta}\Big(r_0^2 + r_1^2 - 2r_0r_1\cos\left(\mathsf{SHK}_{\alpha,\beta}(\nu_0,\nu_1)\right)\Big),
$$

where the so-called spherical Hellinger–Kantorovich distance on P(X) is simply defined by

$$
\mathsf{SK}_{\alpha,\beta}(\nu_0,\nu_1)=\arccos\left(1-\frac{\frac{\beta}{4}\mathsf{IK}_{\alpha,\beta}^2(\nu_0,\nu_1)}{2}\right).
$$

One main result is that SHKα,β is indeed a distance on the space of probability measures, such that the Hellinger–Kantorovich space (M(X), HKα,β) is indeed a cone space over the space of probability measures, namely (P(X), SHKα,β). This distance is a generalization of the spherical Hellinger distance, also called "Fisher-Rao distance" or "Bhattacharya distance 1" in [DeD09, Sec. 7.2+Sec. 14.2], in a similar way that the Hellinger-Kantorovich distance is a generalization of the Hellinger distance.

The fact that SHKα,β satisfies the triangle inequality will be derived in the abstract Section 2 for general distances d<sup>C</sup> satisfying a scaling property as in (1.2). We work on the cone (C, dC) over a general space (X, dX), and the sole additional assumption we need is that the distance d<sup>C</sup> is bounded on the set { [x, 1] : <sup>x</sup> <sup>∈</sup> <sup>X</sup> } ⊂ <sup>C</sup> by the constant 2, see Theorem 2.2. The latter bound follows easily for the Hellinger-Kantorovich distance from

$$
\frac{\beta}{4}\mathsf{H}\mathsf{K}^2_{\alpha,\beta}(\nu_0,\nu_1) \leq \frac{\beta}{4}\left(\frac{4}{\beta}\nu_0(X) + \frac{4}{\beta}\nu_1(X)\right) = 2 \leq 4.
$$

In Sections 2.2 to 2.4 we consider the case that (X, dX) is a geodesic space and that d<sup>C</sup> is given by

$$
\mathsf{d}_{\mathcal{C}}^2([x_0, r_0], [x_1, r_1]) = r_0^2 + r_1^2 - 2r_0r_1\cos_{\pi}(\mathsf{d}\chi(x_0, x_1)),\tag{1.4}
$$

where cosa(b) = cos(min{a, b}). In Sections 2.3 and 2.4 we show how geodesics in (C, <sup>d</sup>C) between [x0, r0] and [x1, r1] can be obtained from those between x<sup>0</sup> and x<sup>1</sup> in (X, dX). Based on this, we discuss how comparison angles and local angles behave when we move between the spherical space (X, dX) and the cone (C, dC). In particular, we discuss the local angle condition m-LAC, see Definition 2.15 and [Sav07, OPV14] for the usefulness of this in the theory of metric gradient flows. The main observation is that if dX(x0, xi) < π, x0<sup>i</sup> are constant-speed geodesics in X connecting x<sup>0</sup> with x<sup>i</sup> , and if z0<sup>i</sup> are the corresponding geodesics in C connecting z<sup>0</sup> = [x0, r0] and z<sup>i</sup> = [x<sup>i</sup> , r<sup>i</sup> ] with r0, r<sup>i</sup> > 0, then the upper angles satisfy the relation

$$
d_{\mathcal{C}}(z_0, z_i) d_{\mathcal{C}}(z_0, z_j) \cos (\measuredangle_{\text{up}}(z_{0i}, z_{0j})) = (r_0 - r_i \cos(d_{\mathcal{X}}(x_0, x_i)))(r_0 - r_j \cos(d_{\mathcal{X}}(x_0, x_j)))+ r_i r_j \sin(d_{\mathcal{X}}(x_0, x_i)) \sin(d_{\mathcal{X}}(x_0, x_j)) \cos (\measuredangle_{\text{up}}(\mathbf{x}_{0i}, \mathbf{x}_{0j})).
$$

Based on this, Theorem 2.21 establishes that the m-LAC condition transfers between (X, dX) and (<sup>C</sup> \ {0}, <sup>d</sup>C). We conclude the second section by proving some <sup>K</sup>-semiconcavity results. More specifically for any three points x0, x1, x<sup>2</sup> contained in a ball of radius D < π <sup>2</sup> we prove the following. if x<sup>01</sup> satisfies K-semiconcavity with respect to the observer x2, then for any z<sup>0</sup> = [x0, r0], z<sup>1</sup> = [x1, r1], z<sup>2</sup> = [x2, r2], we have that z01, satisfies K′ -semiconcavity with respect to the observer z2, where K′ depends only on K, r0, r1, r2, D. Conversely, if r<sup>0</sup> = r<sup>1</sup> and z<sup>01</sup> satisfies K-semiconcavity with respect to the observer z2, then x<sup>01</sup> satisfies K′ -semiconcavity with respect to the observer x2, where K′ depends only on K, r0, r2, D.

Section 3 shows that the abstract results apply in the specific case of the Hellinger-Kantorovich space (M(X), HKα,β), which takes the role of (C, dC), which then leads to the spherical space (P(X), SHKα,β). A direct characterization in the sense of [LMS17, Sec. 8.6] of the geodesic curves using a continuity and a Hamilton-Jacobi equation in the latter space is given in Theorem 3.7.

In Section 4.1 we provide additional geometric properties that hold for both spaces. Among them, is the local-angle condition, and some partial semiconcavity. In [LMS16], it was proved that K-semiconcavity, a property, which is associated among other things with the existence of gradient flows, does not hold in general. In this article, we prove that on the subsets of measures that have bounded density (both from below and above) with respect to some finite, locally doubling measure L, this property holds for sufficient large K depending only on the bounds and L. This result will be used in a consecutive paper to prove the existence of gradient flows. For this we provide a sharp estimate of the total mass of the calibration measure associated with the optimal entropy-transport problem. This estimate is used in our proofs, but it is also helpful for the numerical approximations of the Hellinger-Kantorovich distance.

To simplify the subsequent notations we use the simple relation HK<sup>2</sup> α,β = <sup>1</sup> <sup>β</sup> HK<sup>2</sup> α/β,1 , which shows that it suffices to work with a one-parameter family. We set HK<sup>2</sup> <sup>ℓ</sup> <sup>=</sup> HK<sup>2</sup> 1/ℓ <sup>2</sup>,4 , which allows us to recover HKα,β via HK<sup>2</sup> α,β = 4 <sup>β</sup> HK<sup>2</sup> <sup>ℓ</sup> with ℓ <sup>2</sup> = β/(4α).

## 2 Cones over metric spaces

### 2.1 Background and scaling property

In [Ber83] (see also [ABN86], [BrH99], and [BBI01]), the concept of the cone C over a metric space (X, <sup>d</sup>X), is introduced. The cone is the quotient of the product <sup>X</sup>×[0,∞), obtained by identifying together all points in <sup>X</sup> × {0} with a point <sup>0</sup>, called the apex or tip of the cone. The cone <sup>C</sup> is equipped with the distance d<sup>C</sup> given in (1.4). In [BBI01], one can find a proof that d<sup>C</sup> is a metric distance. The following results exhibits the scaling properties of such cone distances.

Lemma 2.1 (Cone distances have scaling properties) The cone distance d<sup>C</sup> in (1.4) satisfies the scaling property

$$
\forall [x_0, r_0], [x_1, r_1] \in \mathcal{C} : \quad \mathsf{d}_{\mathcal{C}}^2([x_0, r_0], [x_1, r_1]) = r_0 r_1 \mathsf{d}_{\mathcal{C}}^2([x_0, 1], [x_1, 1]) + (r_0 - r_1)^2. \tag{2.1}
$$

Moreover, any distance d<sup>C</sup> satisfying (2.1) (i.e. without assuming (1.4) a priori) satisfies the more general scaling property

$$
d_{\mathcal{C}}^{2}([x_{0}, r_{0}\widetilde{r}_{0}], [x_{1}, r_{1}\widetilde{r}_{1}]) = r_{0}r_{1}d_{\mathcal{C}}^{2}([x_{0}, r_{0}], [x_{1}, r_{1}]) + (\widetilde{r}_{0}^{2} - \widetilde{r}_{0}\widetilde{r}_{1})r_{0}^{2} + (\widetilde{r}_{1}^{2} - \widetilde{r}_{0}\widetilde{r}_{1})r_{1}^{2}
$$
(2.2)

for all <sup>r</sup>e<sup>0</sup> and <sup>r</sup>e1.

Proof: Statement (2.1) follows by using (1.4) twice, once as it is given, and once with r<sup>0</sup> = r<sup>1</sup> = 1, and then eliminating cosπ(dX(x0, x1)).

Statement (2.2) follows by using (2.1) twice, once as it is given, and once with r<sup>0</sup> r<sup>1</sup> replaced by <sup>r</sup>0re<sup>0</sup> and <sup>r</sup>1re1, respectively. After eliminating <sup>d</sup> 2 C ([x0, 1], [x1, 1]) the assertion follows.

While we were studying the Hellinger-Kantorovich space, we noticed that the scaling property (2.1) actually fully characterizes a cone space. We have the following general theorem, which allows us to derive the cone distance from the scaling property.

Theorem 2.2 (Scaling implies cone distance) For a metric space (C, dC), let assume that it exists a set <sup>X</sup>, that could possibly be identified with a subset of <sup>C</sup>, and a surjective function [·, ·] : <sup>X</sup> <sup>×</sup> [0,∞) <sup>→</sup> <sup>C</sup>, such that the distance <sup>d</sup><sup>C</sup> satisfies (2.1) and

$$
\forall x_0 \neq x_1 \in \mathcal{X} : \quad 0 < \mathbf{d}_{\mathcal{C}}^2([x_0, 1], [x_1, 1]) \le 4; \tag{2.3}
$$

then <sup>d</sup><sup>X</sup> : <sup>X</sup> <sup>×</sup> <sup>X</sup> <sup>→</sup> [0,∞) given by <sup>d</sup>X(x0, x1) = arccos 1 − d 2 C ([x0,1],[x1,1]) 2 ∈ [0, π] is a metric distance on X, and (C, dC) is a metric cone over (X, dX), i.e. (1.4) holds.

![](_page_3_Figure_0.jpeg)

Figure 1: Construction of the optimal radius r∗. The points A<sup>j</sup> have distance r<sup>j</sup> = 1 from the origin and thus correspond to <sup>z</sup><sup>j</sup> = [x<sup>j</sup> , 1], which gives <sup>D</sup>1<sup>j</sup> <sup>=</sup> <sup>|</sup>A1A<sup>j</sup> <sup>|</sup> <sup>=</sup> <sup>d</sup>C(z1, z<sup>j</sup> ) for <sup>j</sup> = 0 and <sup>2</sup>. The point A∗, which corresponds to z<sup>∗</sup> = [x1, r∗], is chosen such that |A0A∗| + |A∗A2| = |A0A2|.

Proof: Clearly, d<sup>X</sup> as defind in the assertion is symmetric and positive. Hence, it remains to establish the triangle inequality. Given <sup>x</sup>0, x1, x<sup>2</sup> <sup>∈</sup> <sup>X</sup>, we set

$$
D_{ij} = d_{\mathcal{C}}([x_i, 1], [x_j, 1])
$$
 and  $\phi_{ij} = \arccos\left(1 - \frac{D_{ij}^2}{2}\right)$ , for  $i \neq j \in \{0, 1, 2\}$ .

Hence, we have to show <sup>d</sup>X(x0, x2) = <sup>φ</sup><sup>02</sup> <sup>≤</sup> <sup>φ</sup><sup>01</sup> <sup>+</sup> <sup>φ</sup><sup>12</sup> <sup>=</sup> <sup>d</sup>X(x0, x1) + <sup>d</sup>X(x1, x2). If <sup>φ</sup><sup>01</sup> <sup>+</sup> <sup>φ</sup><sup>12</sup> <sup>≥</sup> <sup>π</sup> then there is nothing to show. Without loss of generality, we will have φ<sup>01</sup> = min{φ01, φ12} < π 2 , and φ<sup>01</sup> + φ<sup>12</sup> < π. We consider a comparison triangle in R 2 , as is depicted in Figure 1. In particular, A<sup>j</sup> are chosen on the unit circle such that φi,i+1 and Di,i+1 are the angle (arclength on the unit circle) and the Euclidean distance, respectively, between A<sup>i</sup> and Ai+1. Now, A<sup>∗</sup> is chosen as the intersection of OA<sup>1</sup> with the segment A0A2, see Figure 1.

With this choice of <sup>r</sup><sup>∗</sup> we retur to the cone (C, <sup>d</sup>C) and let <sup>r</sup><sup>∗</sup> <sup>=</sup> <sup>|</sup>OA∗<sup>|</sup> and <sup>z</sup><sup>0</sup> = [x0, 1], z<sup>1</sup> <sup>=</sup> [x1, r∗], z<sup>2</sup> = [x2, 1] <sup>∈</sup> <sup>C</sup>. The scaling property (2.1) for <sup>d</sup>C, gives

$$
\mathsf{d}_{\mathcal{C}}^2([x_0, 1], [x_1, r_*]) = 1 + r_*^2 - 2r_* \cos \phi_{01} = |\overline{A_0 A_*}|^2 \text{ and}
$$
  
$$
\mathsf{d}_{\mathcal{C}}^2([x_1, r_*], [x_2, 1]) = 1 + r_*^2 - 2r_* \cos \phi_{12} = |\overline{A_2 A_*}|^2.
$$

Using the triangle inequality for dC, we arrive at

$$
D_{02}^2 = d_{\mathcal{C}}^2([x_0, 1], [x_2, 1]) \le (d_{\mathcal{C}}([x_0, 1], [x_1, r_*]) + d_{\mathcal{C}}([x_1, r_*], [x_2, 1]))^2
$$
  
=  $(|\overline{A_0 A_*}| + |\overline{A_* A_2}|)^2 = |\overline{A_0 A_2}|^2 = 1 + 1 - 2 \cos(\phi_{01} + \phi_{12}).$  (2.4)

Thus, we conclude that <sup>φ</sup><sup>02</sup> = arccos 1 − D<sup>2</sup> 02 2 ≤ φ01+φ12, which is the desired triangle inequality for <sup>d</sup>X, namely <sup>d</sup>X(x0, x2) <sup>≤</sup> <sup>d</sup>X(x0, x1) + <sup>d</sup>X(x1, x2). Thus, inserting <sup>d</sup> 2 C ([x0, 1], [x1, 1]) = 2 − 2 cos(dX(x0, x1)) into (2.1), we have established (1.4), and consequently (2.2) follows as well.

As a first consequence we obtain the following result.

Corollary 2.3 Let <sup>X</sup> a set, and <sup>C</sup> the quotient of the product <sup>X</sup> <sup>×</sup> [0,∞), obtained by identifying together all points in <sup>X</sup> <sup>×</sup> <sup>0</sup>. If <sup>d</sup><sup>C</sup> : <sup>C</sup> <sup>×</sup> <sup>C</sup> <sup>→</sup> [0,∞) given by (1.4), for some <sup>d</sup><sup>X</sup> : <sup>X</sup> <sup>×</sup> <sup>X</sup> <sup>→</sup> [0,∞) is a metric distance on <sup>C</sup>, then <sup>d</sup><sup>X</sup> <sup>∧</sup> <sup>π</sup> is a metric distance on <sup>X</sup>.

Proof: By setting z<sup>0</sup> = [x0, 1], and z<sup>1</sup> = [x1, 1], we can recover both the positivity and symmetry property. For the proof of the triangle inequality, we just notice that d<sup>C</sup> satisfies the scaling property, and then the result is an application of Theorem 2.2.

From the perspective of (X, dX), we call (C, dC) the cone space over X; from the perspective of (C, <sup>d</sup>C), we call (X, <sup>d</sup><sup>X</sup> <sup>∧</sup> <sup>π</sup>) the spherical space in <sup>C</sup>.

### 2.2 Geodesics curves

We first recall the standard definition and hence introduce our notations.

Definition 2.4 Let (X, <sup>d</sup>X) be a metric space, and <sup>x</sup> : [0, τ ] <sup>→</sup> <sup>X</sup>, a continuous mapping. Furthermore, let <sup>T</sup> be the set of all partitions <sup>T</sup> <sup>=</sup> {0 = <sup>τ</sup><sup>0</sup> ≤ · · · ≤ <sup>τ</sup>n<sup>T</sup> <sup>=</sup> <sup>τ</sup>} of [0, τ ]. Then, the length of the curve x is given by Len(x) := sup<sup>T</sup> <sup>∈</sup><sup>T</sup> Pn<sup>T</sup> <sup>i</sup>=1 <sup>d</sup>X(x(τi),x(τi−1)).

Definition 2.5 Let (X, dX) be a metric space. We will call (X, dX) geodesic, if and only if for every two points <sup>x</sup>0, x<sup>1</sup> there exists a continuous mapping <sup>x</sup><sup>01</sup> : [0, τ ] <sup>→</sup> <sup>X</sup> such that

x01(0) = x0, x01(τ ) = x1, and dX(x0, x1) = Len(x01).

A function like that will be called a geodesic curve or simply a geodesic. A geodesic satisfying

$$
\mathsf{d}_{\mathfrak{X}}(\bm{x}_{01}(t_1),\bm{x}_{01}(t_2)) = C|t_2-t_1|
$$

for some constant C > 0, will be called a constant-speed geodesic. If C = 1, then the geodesic is called a unit-speed geodesic. Finally for <sup>x</sup>0, x<sup>1</sup> <sup>∈</sup> <sup>X</sup>, any geodesic <sup>x</sup><sup>01</sup> : [0, 1] <sup>→</sup> <sup>X</sup>, with x01(0) = x0, x01(1) = x<sup>1</sup> is called a geodesic joining x<sup>0</sup> to x1. We will denote the set of all such geodesics with Geod(x0, x1), i.e.

$$
Geod(x_0, x_1) := \{ \mathbf{x} : [0, 1] \to \mathfrak{X} \mid \mathbf{x}(0) = x_0, \ \mathbf{x}(1) = x_1, \ \mathbf{x} \ \text{is constant-speed geodesic} \}. \tag{2.5}
$$

In [BrH99, Chap. I, Prop. 5.10], the following Theorem is proved.

Theorem 2.6 Let (X, dX) be a geodesic space. Let also z<sup>0</sup> = [x0, r0] and z<sup>1</sup> = [x1, r1] be elements of C.

- 1. If <sup>r</sup>0, r<sup>1</sup> <sup>∈</sup> (0,∞) and <sup>d</sup>X(x0, x1) < π, then there is a bijection between Geod(x0, x1), and Geod(z0, z1).
- 2. In all other cases, Geod(z0, z1) has a unique element.

As a corollary, we get that C is geodesic, if and only if X is geodesic for points of distance less than π. In the following two Subsections 2.3 and 2.4 we give explicit correspondences in the sense of part 1. of the above theorem for the case of constant-speed geodesics.

## 2.3 Lifting from X into the cone

In [LMS16], it is proved that the constant-speed geodesics z01(t) connecting z<sup>0</sup> = [x0, r0] to z<sup>1</sup> = [x1, r1], with 0 < dX(x0, x1) < π, have the following parametrization

$$
\mathbf{z}_{01}(t) = [\mathbf{x}_{01}(\zeta_{01}(t)), \mathbf{r}_{01}(t)], \qquad (2.6)
$$

where x01(t) is a constant-speed geodesic joining x<sup>0</sup> to x<sup>1</sup> and where ζ01(t) and r01(t) are given by

$$
\mathbf{r}_{01}^{2}(t) = (1-t)^{2}r_{0}^{2} + t^{2}r_{1}^{2} + 2t(1-t)r_{0}r_{1}\cos(\mathbf{d}_{\mathcal{X}}(x_{0},x_{1})),
$$
\n
$$
\mathbf{\zeta}_{01}(t) = \frac{1}{\mathbf{d}_{\mathcal{X}}(x_{0},x_{1})}\arcsin\left(\frac{tr_{1}\sin(\mathbf{d}_{\mathcal{X}}(x_{0},x_{1}))}{\mathbf{r}_{01}(t)}\right)
$$
\n
$$
= \frac{1}{\mathbf{d}_{\mathcal{X}}(x_{0},x_{1})}\arccos\left(\frac{(1-t)r_{0} + t r_{1}\cos(\mathbf{d}_{\mathcal{X}}(x_{0},x_{1}))}{\mathbf{r}_{01}(t)}\right)
$$
\n
$$
= \frac{1}{\mathbf{d}_{\mathcal{X}}(x_{0},x_{1})}\arctan\left(\frac{tr_{1}\sin(\mathbf{d}_{\mathcal{X}}(x_{0},x_{1}))}{(1-t)r_{0} + t r_{1}\cos(\mathbf{d}_{\mathcal{X}}(x_{0},x_{1}))}\right).
$$
\n(2.7)

Alternatively if we want the parametrization with respect to dC, (2.7) becomes

$$
\mathbf{r}_{01}^{2}(t) = ((1-t)r_{0} + tr_{1})^{2} - r_{0}r_{1}t(1-t)\mathbf{d}_{\mathcal{C}}^{2}([x_{0}, 1], [x_{1}, 1])
$$
\n
$$
\boldsymbol{\zeta}_{01}(t) = \frac{1}{\mathbf{d}_{\mathcal{X}}(x_{0}, x_{1})} \arccos\left(\frac{(1-t)r_{0} + tr_{1}\left(1 - \frac{\mathbf{d}_{\mathcal{C}}^{2}([x_{0}, 1], [x_{1}, 1])}{2}\right)}{r_{01}(t)}\right).
$$
\n(2.8)

If we differentiate twice the first equation in (2.7), we get

$$
(\boldsymbol{r}_{01}^2)''(t) = r_0^2 + r_1^2 - 2r_0r_1\cos(\mathrm{d}x(x_0,x_1)) = \mathrm{d}^2_{\mathcal{C}}(z_0,z_1),
$$

from which we also recover the following formula

$$
r_{01}^{2}(t) = (1-t)r_{0}^{2} + tr_{1}^{2} - t(1-t)d_{\mathcal{C}}^{2}(z_{0}, z_{1}),
$$
\n(2.9)

which later applied to HKα,β will give (1.1). Furthermore (2.9), trivially gives convexity of r 2 <sup>01</sup>, i.e.

$$
r_{01}^2(t) \le (1-t)r_0^2 + tr_1^2. \tag{2.10}
$$

Finally for the case where <sup>d</sup>X(x0, x1) <sup>≤</sup> π 2 , we get

$$
r_{01}^{2}(t) \ge (1-t)^{2}r_{0}^{2} + t^{2}r_{1}^{2} \ge \frac{1}{2}\min\{r_{0}^{2}, r_{1}^{2}\}.
$$
\n(2.11)

## 2.4 Projecting from cone to X

We are now going to provide the inverse parametrization of the geodesics in (X, dX), with respect to the geodesics in (C, dC).

Theorem 2.7 For <sup>x</sup>0, x<sup>1</sup> <sup>∈</sup> <sup>X</sup>, with <sup>0</sup> <sup>&</sup>lt;dX(x0, x1) <π, and <sup>r</sup>0, r<sup>1</sup> <sup>&</sup>gt; <sup>0</sup> consider <sup>z</sup><sup>01</sup> <sup>∈</sup> Geod(z0, z1), where z<sup>0</sup> = [x0, r0], z<sup>1</sup> = [x1, r1]. Then,

$$
t \mapsto x_{01}(t) = \overline{x}_{01}(\beta_{01}(t)) \quad with \ \beta_{01}(t) = \frac{r_0 \sin(t d_{\mathcal{X}}(x_0, x_1))}{r_1 \sin((1-t) d_{\mathcal{X}}(x_0, x_1)) + r_0 \sin(t d_{\mathcal{X}}(x_0, x_1))}
$$
(2.12)

is an element of Geod(x0, x1). Furthermore

$$
r_{01}(\beta_{01}(t)) = \frac{r_0 r_1 \sin(\mathsf{d}_{\mathcal{X}}(x_0, x_1))}{r_1 \sin((1-t)\mathsf{d}_{\mathcal{X}}(x_0, x_1)) + r_0 \sin(t\mathsf{d}_{\mathcal{X}}(x_0, x_1))}.
$$
(2.13)

Proof: Since, by the proof of Theorem 2.6, z<sup>01</sup> is a geodesic in (C, dC), if and only if x<sup>01</sup> is a geodesic in (X, dX) and z01(t) = [x01(ζ01(t)), r01(t)], we just have to calculate the inverse of ζ01.

By using the third representation in (2.7), we get

$$
\tan\left(\zeta_{01}(t)\mathsf{d}_{\mathfrak{X}}(x_0,x_1)\right) = \frac{tr_1 \sin(\mathsf{d}_{\mathfrak{X}}(x_0,x_1))}{(1-t)r_0 + tr_1 \cos(\mathsf{d}_{\mathfrak{X}}(x_0,x_1))}.\tag{2.14}
$$

Let β<sup>01</sup> be the inverse of ζ01. By composing every elemet of (2.14) with β01, we get

$$
\tan(t\mathbf{d}\chi(x_0,x_1))=\frac{\beta_{01}(t)r_1\sin(\mathbf{d}\chi(x_0,x_1))}{(1-\beta_{01}(t))r_0+\beta_{01}(t)r_1\cos(\mathbf{d}\chi(x_0,x_1))},
$$

which gives

$$
\beta_{01}(t) = \frac{r_0 \tan(t d_{\mathcal{X}}(x_0, x_1))}{r_1 \sin(d_{\mathcal{X}}(x_0, x_1)) + r_0 \tan(t d_{\mathcal{X}}(x_0, x_1)) - r_1 \tan(t d_{\mathcal{X}}(x_0, x_1)) \cos(d_{\mathcal{X}}(x_0, x_1))}.
$$

Multiplying both the nominator and denominator with cos(tdX(x0, x1)), we get

$$
\beta_{01}(t) = \frac{r_0 \sin(t d_{\mathcal{X}}(x_0, x_1))}{r_1 \sin(d_{\mathcal{X}}(x_0, x_1)) \cos(t d_{\mathcal{X}}(x_0, x_1)) + \sin(t d_{\mathcal{X}}(x_0, x_1))(r_0 - r_1 \cos(d_{\mathcal{X}}(x_0, x_1)))}
$$

and by an application of sin(a) cos(b) − cos(a) sin(b) = sin(a − b), we get (2.12).

Now by using the first representation of (2.7), we get

$$
\sin(t\mathsf{d}\chi(x_0,x_1))=\frac{\beta_{01}(t)r_1\sin(\mathsf{d}\chi(x_0,x_1))}{r_{01}(\beta_{01}(t))},
$$

and combining with (2.12) we get (2.13).

Finally, we are now interested in the scaling properties of constant-speed geodesics on C is we simple change the radius of <sup>z</sup><sup>j</sup> = [x<sup>j</sup> , r<sup>j</sup> ] into <sup>r</sup>jre<sup>j</sup> . We will show that the constant-speed geodesic curves behave nicely under the two-parameter rescaling. In the sequel, for <sup>z</sup> = [x, r] <sup>∈</sup> <sup>C</sup>, and r ><sup>e</sup> <sup>0</sup>, we denote with rz, <sup>e</sup> the element [x, rre] <sup>∈</sup> <sup>C</sup>.

Proposition 2.8 For <sup>z</sup><sup>0</sup> = [x0, r0], z<sup>1</sup> = [x1, r1] <sup>∈</sup> <sup>C</sup> and <sup>r</sup>e0, <sup>r</sup>e<sup>1</sup> <sup>≥</sup> <sup>0</sup>, we have that if <sup>z</sup>01(·) = [x01(·), <sup>r</sup>01(·)] belongs in Geod(z0, z1), then <sup>z</sup>e01(·) = <sup>A</sup>01(·)z01(B01(·)), with

$$
A_{01}(t) = \tilde{r}_0 + (\tilde{r}_1 - \tilde{r}_0)t \quad and \quad B_{01}(t) = \frac{\tilde{r}_1 t}{A_{01}(t)},
$$
\n(2.15)

is an element of Geod(re0z0, <sup>r</sup>e1z1).

Proof: We first observe <sup>z</sup>e01(0) = <sup>r</sup>e0z<sup>0</sup> and <sup>z</sup>e01(1) = <sup>r</sup>e1z1, because <sup>A</sup>01(0) = <sup>r</sup>e<sup>0</sup> and <sup>A</sup>01(1) = <sup>r</sup>e1. Thus, to check that t 7→ z01(t) is a geodesic it suffices to show

$$
\mathsf{d}_{\mathcal{C}}(\overline{\boldsymbol{z}}_{01}(0),\overline{\boldsymbol{z}}_{01}(t))=t\,\mathsf{d}_{\mathcal{C}}(\overline{\boldsymbol{z}}_{01}(0),\overline{\boldsymbol{z}}_{01}(1))=t\,\mathsf{d}_{\mathcal{C}}(r_0z_0,r_1z_1),
$$

i.e. z<sup>01</sup> is a constant-speed geodesic. However, using (2.9), we first observe

$$
\boldsymbol{r}_{01}^2(B_{01}(t)) = (1 - B_{01}(t))\boldsymbol{r}_0^2 + B_{01}(t)\boldsymbol{r}_1^2 - B_{01}(t)(1 - B_{01}(t))\mathbf{d}_{\mathcal{C}}^2(z_0, z_1). \tag{2.16}
$$

With this, the abbreviation a<sup>t</sup> = A01(t), and the relations B01(t) = <sup>r</sup>e1<sup>t</sup> at and <sup>1</sup>−B01(t) = <sup>r</sup>e0(1−t) at we obtain

$$
d_{\mathcal{C}}^{2}(\overline{z}_{01}(0),\overline{z}_{01}(t)) = d_{\mathcal{C}}^{2}(\widetilde{r}_{0}z_{0},a_{t}z_{01}(B_{01}(t)))
$$
\n
$$
\stackrel{(2.1)}{=} \widetilde{r}_{0}a_{t}d_{\mathcal{C}}^{2}(z_{0},z_{01}(B_{01}(t))) + \widetilde{r}_{0}(\widetilde{r}_{0}-a_{t})r_{0}^{2} + a_{t}(a_{t}-\widetilde{r}_{0})r_{01}^{2}(B_{01}(t))
$$
\n
$$
\stackrel{z_{01} \text{ is good.}}{=} \widetilde{r}_{0}a_{t}\frac{\widetilde{r}_{1}^{2}t^{2}}{a_{t}^{2}}d_{\mathcal{C}}^{2}(z_{0},z_{1}) + \widetilde{r}_{0}(\widetilde{r}_{0}-a_{t})r_{0}^{2} + a_{t}(a_{t}-\widetilde{r}_{0})\left(\frac{\widetilde{r}_{0}(1-t)}{a_{t}}r_{0}^{2} + \frac{\widetilde{r}_{1}t}{a_{t}}r_{1}^{2} - \frac{\widetilde{r}_{0}\widetilde{r}_{1}t(1-t)}{a_{t}^{2}}d_{\mathcal{C}}^{2}(z_{0},z_{1})\right)
$$
\n
$$
\stackrel{*}{=} \widetilde{r}_{0}\widetilde{r}_{1}t^{2}d_{\mathcal{C}}^{2}(z_{0},z_{1}) + (\widetilde{r}_{0}^{2}-\widetilde{r}_{0}\widetilde{r}_{1})t^{2}r_{0}^{2} + (\widetilde{r}_{1}^{2}-\widetilde{r}_{0}\widetilde{r}_{1})t^{2}r_{1}^{2}\stackrel{(2.1)}{=} t^{2}d_{\mathcal{C}}^{2}(\widetilde{r}_{0}z_{0},\widetilde{r}_{1}z_{1}) = t^{2}d_{\mathcal{C}}^{2}(\overline{z}_{0},\overline{z}_{1}),
$$

where in <sup>∗</sup><sup>=</sup> we simply used the definition of <sup>a</sup><sup>s</sup> <sup>=</sup> <sup>A</sup>01(s). Thus, the assertion is shown.

### 2.5 Comparison and local angles

We now introduce comparison angles, see e.g. [Stu99, BBI01, AKP17], that are used to study notions of curvature and their properties, and subsequentially be utilized to generate gradient flows on metric spaces, cf. [Oht09, AKP17, Sav07, OPV14]. Since we relate the space (X, dX) with the cone (C, dC), we will see in the next subsection (cf. the proof of Theorem 2.21)) that it is natural to use comparison angles <sup>e</sup> <sup>κ</sup> for different <sup>κ</sup> on these two spaces.

Definition 2.9 (Comparison angles) Let (X, <sup>d</sup>X) be a metric space and <sup>x</sup>0, x1, x<sup>2</sup> <sup>∈</sup> <sup>X</sup> with <sup>x</sup><sup>0</sup> 6∈ {x1, x2}. For <sup>κ</sup> <sup>∈</sup> <sup>R</sup> we define <sup>a</sup><sup>κ</sup> via

$$
a_{\kappa}(x_0; x_1, x_2) := \begin{cases} \frac{d_{\mathcal{X}}^2(x_0, x_1) + d_{\mathcal{X}}^2(x_0, x_2) - d_{\mathcal{X}}^2(x_1, x_2)}{2d_{\mathcal{X}}(x_0, x_1) d_{\mathcal{X}}(x_0, x_2)} & \text{for } \kappa = 0, \\ \frac{\cos(\sqrt{\kappa} d_{\mathcal{X}}(x_1, x_2)) - \cos(\sqrt{\kappa} d_{\mathcal{X}}(x_0, x_1)) \cos(\sqrt{\kappa} d_{\mathcal{X}}(x_0, x_2))}{\sin(\sqrt{\kappa} d_{\mathcal{X}}(x_0, x_1)) \sin(\sqrt{\kappa} d_{\mathcal{X}}(x_0, x_2))} & \text{for } \kappa > 0, \\ \frac{\cosh(\kappa d_{\mathcal{X}}(x_0, x_1)) \cosh(\kappa d_{\mathcal{X}}(x_0, x_2)) - \cosh(\kappa d_{\mathcal{X}}(x_1, x_2))}{\sinh(\kappa d_{\mathcal{X}}(x_0, x_1)) \sinh(\kappa d_{\mathcal{X}}(x_0, x_2))} & \text{for } \kappa < 0, \end{cases}
$$

where k = √ <sup>−</sup>κ. The <sup>κ</sup>-comparison angle <sup>e</sup> <sup>κ</sup>(x0; <sup>x</sup>1, x2) <sup>∈</sup> [0, π] with vertex <sup>x</sup><sup>0</sup> is defined by the formula

$$
\widetilde{\sphericalangle}_{\kappa}(x_0; x_1, x_2) = \arccos(a_{\kappa}(x_0; x_1, x_2)).
$$

From now on, the value of κ in the previous definition will be refereed as the choice of model space M<sup>2</sup> (κ). This terminology is borrowed from the study of Alexandrov spaces, where the sphere (κ > 0), the plane (κ = 0), and the hyberbolic plane (κ < 0) are used as reference, cf. [Stu99, BBI01, AKP17]. Later, our main choice will be κ = 1 on the spherical space (hence the name) (X, dX) and κ = 0 on the cone (C, dC).

Let x<sup>01</sup> and x02, be two geodesics in (X, dX), emanating from the same initial point x<sup>0</sup> := x01(0) = x02(0). The following theorem guarantees that the set

$$
\mathcal{AP}(x_{01}, x_{02}) := \{c \in [-1, 1] \mid \exists \, 0 < s_k, t_k \to 0 : a_{\kappa}(x_0; x_{01}(t_k), x_{02}(s_k)) \to c\} \tag{2.17}
$$

of accumulation points of aκ(x0;x01(t),x02(s)) as t, s → 0 is independent of κ.

Proposition 2.10 Let (X, <sup>d</sup>X) be a metric space and <sup>x</sup><sup>01</sup> : [0, τ1] <sup>→</sup> <sup>X</sup>, <sup>x</sup><sup>02</sup> : [0, τ2] <sup>→</sup> <sup>X</sup> be two unit-speed geodesics, issuing from <sup>x</sup><sup>0</sup> <sup>∈</sup> <sup>X</sup>. Then, for <sup>κ</sup> <sup>∈</sup> <sup>R</sup> we have

$$
a_0(x_0; \mathbf{x}_{01}(t), \mathbf{x}_{02}(s)) - a_{\kappa}(x_0; \mathbf{x}_{01}(t), \mathbf{x}_{02}(s)) \to 0 \quad \text{for } t, s \to 0. \tag{2.18}
$$

We will provide an analytical proof here. For the reader with a more geometrically oriented mind we suggest the proof in [AKP17, Page 52, Lemma 6.3.1], which became known to us after the completion of the article.

Proof: We give here details for the case κ = 1. The other cases work exactly the same. For (t, s) <sup>∈</sup> (0, τ ] <sup>×</sup> (0, τ ] with τ < min{1/2, τ1, τ2} we set <sup>c</sup>t,s := <sup>d</sup>(x01(t),x02(s)). Using <sup>t</sup> <sup>=</sup> <sup>d</sup>(x0,x01(t)) and <sup>s</sup> <sup>=</sup> <sup>d</sup>(x0,x02(s)), the triangle inequality gives <sup>|</sup>t−s| ≤ <sup>c</sup>s,t <sup>≤</sup> <sup>t</sup>+s. This is equivalent to

$$
\exists \theta \in [-1, 1]:
$$
  $c_{t,s}^2 = s^2 + t^2 - 2st\theta,$ 

where θ equals a0(x0;x01(t),x02(s)). Now, defining the function

$$
G(s, t; \theta) = \theta - \frac{\cos \sqrt{s^2 + t^2 - 2st\theta} - \cos(s)\cos(t)}{\sin(s)\sin(t)},
$$

we see that (2.18) is established if we show kG(s, t; ·)k<sup>∞</sup> → 0 for s, t → 0, where k · k<sup>∞</sup> means the supremum over θ ∈ [−1, 1]. To establish the uniform convergence of G(s, t; ·) we decompose G in three parts, namely

$$
G(s, t; \theta) = G_1(s, t; \theta) + G_2(s, t; \theta) + G_3(s, t; \theta) \quad \text{with}
$$
  
\n
$$
G_1(s, t; \theta) := \theta - \frac{\sin(st\theta)}{\sin(s)\sin(t)} = \left(1 - \frac{F(s)F(t)}{F(st\theta)}\right)\frac{\sin(st\theta)}{\sin(s)\sin(t)},
$$
  
\n
$$
G_2(s, t; \theta) := \frac{\sin(st\theta) - \cos\sqrt{s^2 + t^2 - 2st\theta} + \cos\sqrt{s^2 + t^2}}{\sin(s)\sin(t)},
$$
  
\n
$$
G_3(s, t; \theta) := \frac{\cos(s)\cos(t) - \cos\sqrt{s^2 + t^2}}{\sin(s)\sin(t)},
$$

where the function F(r) = <sup>1</sup> r sin r can be analytically extended by F(0) = 1.

Using s, t ≤ 1/2 and |θ| ≤ 1 we easily obtain

$$
|G_1(s, t; \theta)| \le 6(s + t) \frac{st}{(s/2)(t/2)} \le 24(s + t) \to 0 \text{ for } s, t \to 0.
$$

For <sup>G</sup><sup>3</sup> we use that <sup>K</sup>(r) = 1<sup>−</sup> cos(<sup>√</sup> r) is an analytic function with K(0) = 0. Thus, with σ = s 2 and τ = t <sup>2</sup> we have

$$
\begin{aligned} &\left| \cos(s)\cos(t) - \cos\sqrt{s^2 + t^2} \right| = \left| (1 - K(\sigma))(1 - K(\tau)) - 1 + K(\sigma + \tau) \right| \\ &\le \left| K(\sigma) + K(\tau) - K(\sigma + \tau) - K(0) \right| + K(\sigma)K(\tau) \\ &\le \left| \int_0^{\sigma} \int_0^{\tau} K''(\hat{\sigma} + \hat{\tau}) \, d\hat{\tau} \, d\hat{\sigma} \right| + C_1^2 \sigma \tau \le (C_2 + C_1^2) \sigma \tau = (C_2 + C_1^2) s^2 t^2, \end{aligned}
$$

where <sup>C</sup><sup>1</sup> and <sup>C</sup><sup>2</sup> are bounds for <sup>|</sup>K′ (r)<sup>|</sup> and <sup>|</sup>K′′(r)<sup>|</sup> with <sup>r</sup> <sup>∈</sup> [0, <sup>1</sup>/2], repesctively. Inserting this into the definition of G<sup>3</sup> we find

$$
|G_3(s,t;\theta)| \le \frac{(C_2+C_1^2)s^2t^2}{(s/2)(t/2)} \le 4(C_2+C_1^2)st \to 0 \text{ for } s,t \to 0.
$$

The estimate for G<sup>2</sup> we use K again and rewrite the nominator as

$$
\sin(st\theta) + K(s^2 + t^2) - K(s2 + t^2 - 2st\theta) = \sin(st\theta) - st\theta + \int_0^1 (1 - 2K'(s^2 + t^2 - 2st\theta\eta)) d\eta \, st\theta.
$$

Using 1 = 2K′ (0) we can estimate the integral by the bound C<sup>2</sup> on K′′ and obtain

$$
|G_2(s,t;\theta)| \le \frac{|st\theta|^3/6 + 2C_2(t+s)^2st|\theta|}{(s/2)(t/2)} \le \frac{4}{6}s^2t^2 + 8C_2(t+s)^2 \to 0 \text{ for } s,t \to 0.
$$

With this, the desired uniform convergence G(s, t; ·) → 0 is established, and the proof is complete.

We are now going to introduce the notion of local angles.

Definition 2.11 (Local Angles) Let x01and x<sup>02</sup> be two geodesics in X emanating from the same initial point <sup>x</sup><sup>0</sup> := <sup>x</sup>01(0) = <sup>x</sup>02(0). The upper angle up(x01,x02) <sup>∈</sup> [0, π] and the lower angle lo(x01,x02) <sup>∈</sup> [0, π], between <sup>x</sup><sup>01</sup> and <sup>x</sup><sup>02</sup> are defined by

$$
\mathcal{K}_{\text{up}}(\boldsymbol{x}_{01},\boldsymbol{x}_{02}):=\limsup_{s,t\downarrow 0}\widetilde{\mathcal{K}}_0(x_0,\boldsymbol{x}_{01}(s),\boldsymbol{x}_{02}(t))=\arccos\big(\inf\mathcal{AP}(\boldsymbol{x}_{01},\boldsymbol{x}_{02})\big),\tag{2.19a}
$$

$$
\sphericalangle_{10}(\boldsymbol{x}_{01},\boldsymbol{x}_{02}) := \liminf_{s,t\downarrow 0} \widetilde{\sphericalangle}_{0}(x_0;\boldsymbol{x}_{01}(s),\boldsymbol{x}_{02}(t)) = \arccos\big(\sup \mathcal{AP}(\boldsymbol{x}_{01},\boldsymbol{x}_{02})\big).
$$
 (2.19b)

When up(x01,x02) = lo(x01,x02), we say that the (local) angle exists in the strict sense and write (x01,x02).

In the previous definition, we could use any model space M<sup>2</sup> (κ), since as we have seen in Proposition 2.10 the set of limit points of aκ(x0;x01(t),x02(s)) as t, s → 0, is independent of κ. It is also trivial that the above limits are invariant under re-parametrization, and that is why we are mostly going to use constant-speed geodesics for joining points.

### 2.6 Curvature and Local Angle Condition

Curvature is one of the most fundamental geometric properties in geodesic metric spaces, and it has applications in gradient flows (see [Oht09, AKP17, Sav07]). There are many equivalent characterizations, see [AKP17, BBI01, Ber83] for definitions and exposition. We are going to provide the one that is closer to our results, which was introduced in [Stu99].

Definition 2.12 We will say that a geodesic metric space (X, dX) has curvature not less than κ at a point x, if there is a neighborhood U of x, such that

$$
\sum_{i,j=1}^{m} b_i b_j a_{\kappa}(x_0; x_i, x_j) \ge 0
$$
\n(2.20)

for every <sup>m</sup> <sup>∈</sup> <sup>N</sup>, <sup>x</sup>0, x1, . . . , x<sup>m</sup> in U, and <sup>b</sup>1, . . . , b<sup>m</sup> <sup>∈</sup> [0,∞). We say that (X, <sup>d</sup>X) has curvature not less than κ "in the large", if we can take U = X. We shortly write curvX(x) > κ, if the space (X, <sup>d</sup>X) has curvature not less than κ, at x. We finally write curv<sup>X</sup> <sup>≥</sup> <sup>κ</sup> if the space (X, <sup>d</sup>X) has curvature not less than κ, in the large.

We would like to note at this point that curvX(x) > κ for every <sup>x</sup> <sup>∈</sup> <sup>X</sup>, does not a-priori imply that curvX > κ, since the second will require for (2.20) to hold for arbitrarily big triangles. However we recall the following beautiful theorem (see [BBI01, Th. 10.3.1]), which we will use at a later point.

Theorem 2.13 (Toponogov's Theorem) If a complete geodesic metric space (X, dX) has curvature not less than κ at every point, then it has curvature not less than κ in the large, i.e.

(∀<sup>x</sup> <sup>∈</sup> <sup>X</sup> : curvX(x) > κ) <sup>⇔</sup> curv<sup>X</sup> > κ

Concerning the curvatures of a cone C and its spherical space X, the following result is well-known.

Theorem 2.14 [BBI01, Thm. 4.7.1] Let (C, dC) be a cone over a geodesic metric space (X, dX) , and 0 its apex. Then, the following holds:

- (a) (∀<sup>z</sup> <sup>∈</sup> <sup>C</sup> \ {0} : curv<sup>C</sup> (z) > 0), if and only if curv<sup>X</sup> ≥ 1.
- (b) curv<sup>C</sup> <sup>≥</sup> <sup>0</sup>, if and only if curv<sup>X</sup> <sup>≥</sup> <sup>1</sup> and no triangle in <sup>X</sup> has perimeter greater than <sup>2</sup><sup>π</sup> (i.e. for any pairwise different <sup>x</sup>1, x2, x3, we have <sup>d</sup>X(x1, x2) + <sup>d</sup>X(x2, x3) + <sup>d</sup>X(x3, x1) <sup>≤</sup> <sup>2</sup>π).

The notion of curvature is not very stable when we take the cone (C, dC) over a space (X, dX) or when constructing the Wasserstein space (P2(X), W) over (X, dX). For the first statement, we recall the previous theorem and see that we need curv<sup>X</sup> ≥ 1 to achieve curv<sup>C</sup> ≥ 0, while any other "lower curvature bound" κ < 1 for (X, dX) is not enough to guarantee any "lower curvature bound" for (C, dC). For the second statement, we refer to [AGS05], where it is shown that we need curv<sup>X</sup> ≥ 0 to deduce curvP2(X) ≥ 0.

Hence, we are going to investigate a significantlly weaker but much more stable notion than lower curvature, which along with some other geometric properties, is enough enough to prove existence of gradient flows, cf. [OPV14, Part 1, Ch. 6]. The property that we are going to examine is the Local Angle Condition (LAC). As it will be shown, LAC is a property that is transferable from (X, <sup>d</sup>X) to (C\{0}, <sup>d</sup>C), but is also stable when we move to the Wasserstein and the Hellinger-Kantorovich space (M(X), HKℓ) over (X, dX).

Definition 2.15 For <sup>m</sup> <sup>∈</sup> <sup>N</sup>, a geodesic metric space (X, <sup>d</sup>X) satisfies <sup>m</sup>-LAC at a point <sup>x</sup>0, if for every choice of m non-trivial geodesics x0<sup>i</sup> starting at x<sup>0</sup> and positive real numbers b<sup>i</sup> , i ∈ {1, . . . m}, we have

$$
\sum_{i,j=1}^{m} b_i b_j \cos(\langle \mathbf{x}_{\text{up}}(\mathbf{x}_{0i}, \mathbf{x}_{0j}) \rangle \ge 0. \tag{2.21}
$$

If (X, dX) satisfies m-LAC at all points, we say that the space satisfies m-LAC.

We note that (X, dX) satisfying m-LAC at a point x<sup>∗</sup> is a fundamentally weaker notion than having curvX(x∗) <sup>≥</sup> <sup>κ</sup> for some <sup>κ</sup> <sup>∈</sup> <sup>R</sup>. For <sup>m</sup>-LAC, one has to look only at infinitesimal triangles with common vertex x∗, while for curvature bounds, one has to look at all triangles in a neighborhood of x∗. Furthermore, since the triangles used in the definition of m-LAC are arbitrarily small, by application of Proposition 2.10 the dependence on any specific κ disappears. Using loose terminology, one can say that curvature is a second order, while m-LAC is a first order property. Furthermore one could say that m-LAC captures, in a rough sense, the infinitesimally Euclidean nature around x<sup>∗</sup> of the "geodesically convex hulls" generated by m geodesics. By using geodesics in (2.20), taking limits, and recalling the fact that angles exist in spaces with curvature not less than a real number (see [BBI01]), one can easily retrieve the following theorem.

Theorem 2.16 Let (X, <sup>d</sup>X) a geodesic metric space and <sup>x</sup> a point in it. If curvX(x) <sup>≥</sup> <sup>κ</sup> for some <sup>κ</sup> <sup>∈</sup> <sup>R</sup>, then (X, <sup>d</sup>X) satisfies <sup>m</sup>-LAC at every <sup>x</sup><sup>0</sup> in a neighborhood <sup>U</sup> of <sup>x</sup> and for all <sup>m</sup> <sup>∈</sup> <sup>N</sup>.

For m = 1 and 2 the condition is trivially satisfied. For m = 3, which is the case needed for construction solutions for gradient flows, we have the following equivalent, more geometric characterization.

Theorem 2.17 ([Sav07, OPV14]) A geodesic metric space (X, dX) satisfies 3-LAC at x0, if and only if for all triples of geodesics x01,x02,x<sup>03</sup> emanating from x0, we have

$$
\langle \chi_{\text{up}}(\bm{x}_{01},\bm{x}_{02}) + \langle \chi_{\text{up}}(\bm{x}_{02},\bm{x}_{03}) + \langle \chi_{\text{up}}(\bm{x}_{03},\bm{x}_{01}) \leq 2\pi.
$$

We now provide one of our major abstract results. We will show that m-LAC is stable on lifting to cones and projecting to the spherical space inside a cone.

Theorem 2.18 Let (C, dC) be the cone over a geodesic metric space (X, dX). Then we have

- (a) If (C, <sup>d</sup>C) satisfies <sup>m</sup>-LAC at <sup>z</sup><sup>0</sup> = [x0, r0] for some <sup>x</sup><sup>0</sup> <sup>∈</sup> <sup>X</sup> and <sup>r</sup><sup>0</sup> <sup>&</sup>gt; <sup>0</sup>, then (X, <sup>d</sup>X) satisfies m-LAC at x0.
- (b) Conversely if (X, <sup>d</sup>X) satisfies <sup>m</sup>-LAC at <sup>x</sup>0, then <sup>z</sup><sup>0</sup> = (x0, r0) <sup>∈</sup> (C, <sup>d</sup>C) also satisfies it for every r<sup>0</sup> > 0.
- (c) (C, dC) satisfies 3-LAC at the apex 0 if and only if (X, dX) has perimeter less than 2π.
- (d) If (X, <sup>d</sup>X) has diameter less or equal to π/2, then (C, <sup>d</sup>C) satisfies <sup>m</sup>-LAC at <sup>0</sup> for all <sup>m</sup> <sup>∈</sup> <sup>N</sup>.

Before we prove this theorem, we provide some auxiliary lemmas. For notational economy, we again set φij = dX(x<sup>i</sup> , x<sup>j</sup> ) and Dij = dC(z<sup>i</sup> , z<sup>j</sup> ). We will use planar comparison angles (i.e. κ = 0) for the cone C, and spherical comparison angles (κ = 1) for the underlying space X (recall Definition 2.9).

Lemma 2.19 Let <sup>z</sup><sup>0</sup> = [x0, r0] <sup>∈</sup> <sup>C</sup> \ {0}, <sup>z</sup><sup>1</sup> = [x1, r1], <sup>z</sup><sup>2</sup> = [x2, r2] <sup>∈</sup> <sup>C</sup>, and <sup>0</sup> <sup>&</sup>lt; <sup>d</sup>X(x0, xi) < π, i ∈ {1, 2}. Let x0<sup>i</sup> ∈ Geod(x0, xi), for i = 1, 2. Let also z0<sup>i</sup> = [x0<sup>i</sup> , r0<sup>i</sup> ] be the corresponding constant-speed geodesics in C. Then, A0,C(t, s) := a0(z0; z01(t), z02(s)) and A1,X(t, s) := a1(x0;x01(t),x02(s)) are connected by the relation

$$
\mathcal{A}_{0,\mathcal{C}}(t,s) = \frac{(r_1 \cos(\phi_{01}) - r_0)(r_2 \cos(\phi_{02}) - r_0)}{D_{01} D_{02}} \n+ \frac{\sin(d_{\mathcal{X}}(x_0, \overline{x}_{01}(t))) \sin(d_{\mathcal{X}}(x_0, \overline{x}_{02}(s)))}{d_{\mathcal{X}}(x_0, \overline{x}_{01}(t)) d_{\mathcal{X}}(x_0, \overline{x}_{02}(s))} \frac{r_{01}(t) r_{02}(s) \zeta_{01}(t) \zeta_{02}(s) \phi_{01} \phi_{02}}{t s D_{01} D_{02}} \overline{\mathcal{A}}_{1,\mathcal{X}}(t,s).
$$
\n(2.22)

Proof: By the reparametrization rule(2.7) we have x0i(t) = x0i(ζ0<sup>i</sup> (t)), where

$$
\zeta_{0i}(t) = \frac{1}{\phi_{0i}} \arccos\left(\frac{(1-t)r_0 + tr_i \cos(\phi_{0i})}{\mathbf{r}_{0i}(t)}\right),\tag{2.23}
$$

from which we obtain

$$
\begin{aligned} \boldsymbol{r}_{0i}(t)\cos(\mathsf{d}_{\mathcal{X}}(x_{0},\overline{\boldsymbol{x}}_{0i}(t))) &= \boldsymbol{r}_{0i}(t)\cos(\boldsymbol{\zeta}_{0i}(t)\phi_{0i}) = (1-t)\boldsymbol{r}_{0} + \boldsymbol{tr}_{i}\cos(\phi_{0i}) \\ &= \boldsymbol{r}_{0} + \boldsymbol{t}(\boldsymbol{r}_{i}\cos(\phi_{0i}) - \boldsymbol{r}_{0}). \end{aligned} \tag{2.24}
$$

On the one hand the definition of the comparison angles a<sup>1</sup> on (X, dX) yields

$$
\cos(\mathbf{d}_{\mathcal{X}}(\overline{\boldsymbol{x}}_{01}(t),\overline{\boldsymbol{x}}_{02}(s))) = \cos(\mathbf{d}_{\mathcal{X}}(x_0,\overline{\boldsymbol{x}}_{01}(t)))\cos(\mathbf{d}_{\mathcal{X}}(x_0,\overline{\boldsymbol{x}}_{02}(s)))+\overline{\mathcal{A}}_{1,\mathcal{X}}(t,s)\sin(\mathbf{d}_{\mathcal{X}}(x_0,\overline{\boldsymbol{x}}_{01}(t)))\sin(\mathbf{d}_{\mathcal{X}}(x_0,\overline{\boldsymbol{x}}_{02}(s))).
$$
\n(2.25)

On the other hand, the definition of a<sup>0</sup> on (C, dC) and dC(z0, z0<sup>j</sup> (t)) = tD0<sup>j</sup> lead to

$$
\mathcal{A}_{0,\mathcal{C}}(t,s) = \frac{\mathsf{d}_{\mathcal{C}}^2(z_0, z_{01}(t)) + \mathsf{d}_{\mathcal{C}}^2(z_0, z_{02}(s)) - \mathsf{d}_{\mathcal{C}}^2(z_{01}(t), z_{02}(s))}{2tsD_{01}D_{02}}.
$$
\n(2.26)

The nominator of the right-hand side is equal to

$$
r_0^2 + r_{01}(t)^2 - 2r_0r_{01}(t)\cos(d_{\mathcal{X}}(x_0, \overline{x}_{01}(t))) + r_0^2 + r_{02}(s)^2 - 2r_0r_{02}(s)\cos(d_{\mathcal{X}}(x_0, \overline{x}_{02}(s))) - r_{01}(t)^2 - r_{02}(s)^2 + 2r_{01}(t)r_{02}(s)\cos(d_{\mathcal{X}}(\overline{x}_{01}(t), \overline{x}_{02}(s))) = \frac{2r_0^2 - 2r_0r_{01}(t)\cos(d_{\mathcal{X}}(x_0, \overline{x}_{01}(t))) - 2r_0r_{02}(s)\cos(d_{\mathcal{X}}(x_0, \overline{x}_{02}(s))) + \frac{2r_{01}(t)r_{02}(s)\cos(d_{\mathcal{X}}(x_0, \overline{x}_{01}(t)))\cos(d_{\mathcal{X}}(x_0, \overline{x}_{02}(s))) + 2r_{01}(t)r_{02}(s)\overline{A}_{1,\mathcal{X}}(t, s)\sin(d_{\mathcal{X}}(x_0, \overline{x}_{01}(t)))\sin(d_{\mathcal{X}}(x_0, \overline{x}_{02}(s))).
$$
\n(2.27)

Using (2.24) on the underlined terms on the last sum, we obtain

$$
2r_0^2 - 2r_0 (r_0 + t(r_1 \cos(\phi_{01}) - r_0)) - 2r_0 (r_0 + s(r_2 \cos(\phi_{02}) - r_0))
$$
  
+ 2 (r\_0 + t(r\_1 \cos(\phi\_{01}) - r\_0)) (r\_0 + s(r\_2 \cos(\phi\_{02}) - r\_0))  
= 2ts (r\_1 \cos(\phi\_{01}) - r\_0) (r\_2 \cos(\phi\_{02}) - r\_0).

So (2.26) takes the form

$$
\mathcal{A}_{0,\mathcal{C}}(t,s) = \frac{(r_1 \cos(\phi_{01}) - r_0)(r_2 \cos(\phi_{02}) - r_0)}{D_{01}D_{02}} \n+ \frac{r_{01}(t)r_{02}(s) \sin(d_{\mathcal{X}}(x_0, \overline{x}_{01}(t))) \sin(d_{\mathcal{X}}(x_0, \overline{x}_{02}(s)))}{tsD_{01}D_{02}} \overline{\mathcal{A}}_{1,\mathcal{X}}(t,s) \n= \frac{(r_1 \cos(\phi_{01}) - r_0)(r_2 \cos(\phi_{02}) - r_0)}{D_{01}D_{02}} \n+ \frac{\sin(d_{\mathcal{X}}(x_0, \overline{x}_{01}(t))) \sin(d_{\mathcal{X}}(x_0, \overline{x}_{02}(s)))}{d_{\mathcal{X}}(x_0, \overline{x}_{01}(t)) d_{\mathcal{X}}(x_0, \overline{x}_{02}(s))} \frac{r_{01}(t)r_{02}(s)\zeta_{01}(t)\zeta_{02}(s)\phi_{01}\phi_{02}}{tsD_{01}D_{02}} \overline{\mathcal{A}}_{1,\mathcal{X}}(t,s),
$$

which is the desired result (2.22).

Since local angles do not depend on the choice of model space M<sup>2</sup> (κ), the previous lemma provides a direct connection between the local angles of geodesics in (C, dC) and the the local angles of the corresponding geodesics in (X, dX).

Proposition 2.20 Let <sup>z</sup><sup>0</sup> = [x0, r0] <sup>∈</sup> <sup>C</sup> \ {0}, z<sup>1</sup> = [x1, r1], z<sup>2</sup> = [x2, r2] <sup>∈</sup> <sup>C</sup> \ {z0} and <sup>0</sup> <sup>&</sup>lt; <sup>d</sup>X(x0, xi) < π for <sup>i</sup> ∈ {1, <sup>2</sup>}. Let <sup>x</sup>0<sup>i</sup> <sup>∈</sup> Geod(x0, xi) for <sup>i</sup> = 1, <sup>2</sup>. Let also <sup>z</sup>0<sup>i</sup> = [x0<sup>i</sup> , r0<sup>i</sup> ] the corresponding geodesics in C. Then, AP(x01,x02) and AP(z01, z02) (see (2.17) for definition) satisfy the relation

$$
\mathcal{AP}(z_{01}, z_{02}) = \frac{(r_0 - r_1 \cos \phi_{01})(r_0 - r_2 \cos \phi_{02})}{d_e(z_0, z_1) d_e(z_0, z_2)} + \frac{r_1 r_2 \sin(\phi_{01}) \sin(\phi_{02})}{d_e(z_0, z_1) d_e(z_0, z_2)} \mathcal{AP}(x_{01}, x_{02}), \quad (2.28)
$$

where φ0<sup>j</sup> = dX(x0, x<sup>j</sup> ) and where the operations between set and real numbers are per element. More specifically we have

$$
\cos\left(\chi_{\text{up}}(z_{01}, z_{02})\right) = \frac{(r_0 - r_1 \cos\phi_{01})(r_0 - r_2 \cos\phi_{02}) + r_1 r_2 \sin(\phi_{01}) \sin(\phi_{02}) \cos\left(\chi_{\text{up}}(x_{01}, x_{02})\right)}{d_{\mathcal{C}}(z_0, z_1) d_{\mathcal{C}}(z_0, z_2)},\tag{2.29}
$$

and

$$
\cos\left(\measuredangle_{\text{up}}(\boldsymbol{x}_{01},\boldsymbol{x}_{02})\right) = \frac{\mathrm{d}_{\mathcal{C}}(z_0,z_1)\mathrm{d}_{\mathcal{C}}(z_0,z_2)\cos\left(\measuredangle_{\text{up}}(z_{01},z_{02})\right)}{r_1r_2\sin(\phi_{01})\sin(\phi_{02})} - \frac{(r_0-r_1\cos\phi_{01})(r_0-r_2\cos\phi_{02})}{r_1r_2\sin(\phi_{01})\sin(\phi_{02})}.
$$
\n(2.30)

Furthermore, when x<sup>0</sup> = x<sup>1</sup> or x<sup>0</sup> = x2, formula (2.29) holds trivially with the right-hand side of the sum being equal to zero.

Proof: By reparametrization (2.23) we have A0,X(t, s) = A0,X(ζ01(t), ζ02(s)), therefore A0,X(t, s) and A0,X(t, s) have the same accumulation points. Furthermore, Proposition 2.10 guarantees that A0,X(t, s) and A1,X(t, s) = a1(x0;x01(t),x02(s)) have the same accumulation points.

Let ℓ an accumulation point for A1,X(t, s) and tn, s<sup>n</sup> sequences that achieve that the limit ℓ. By using formula (2.22) in Lemma 2.19 and limτ→<sup>0</sup> sin(τ) <sup>τ</sup> = 1, we have

$$
\lim_{n \to \infty} A_{0,\mathcal{C}}(t_n, s_n) = \frac{(r_1 \cos(\phi_{01}) - r_0)(r_2 \cos(\phi_{02}) - r_0)}{D_{01} D_{02}} + \lim_{n \to \infty} \frac{r^{01}(t_n) r^{02}(s_n) \zeta_{01}(t_n) \zeta_{02}(s_n) \phi_{01} \phi_{02}}{t_n s_n D_{01} D_{02}} \lim_{n \to \infty} \overline{A}_{1,\mathcal{X}}(t_n, s_n).
$$

Using formula (2.7), we have limǫ→<sup>0</sup> ζ0<sup>i</sup> (ǫ) <sup>ǫ</sup> = r<sup>i</sup> sin(φ0i) r0φ0<sup>i</sup> and limǫ→<sup>0</sup> r0i(ǫ) = r0, and find

$$
\lim_{n \to \infty} A_{0,\mathcal{C}}(t_n, s_n) = \frac{(r_1 \cos(\phi_{01}) - r_0)(r_2 \cos(\phi_{02}) - r_0) + r_1 r_2 \sin(\phi_{01}) \sin(\phi_{02}) \ell}{D_{01} D_{02}}.
$$
(2.31)

Doing the same for all accumulation points of A0,C(t, s), we recover the desired formula (2.28).

The formulas for the upper local angle follow simply the taking the infimum of the sets of accumulation points, see (2.19).

We are now ready to establish the main result giving the connection between the local angle condition in (C, dC) and (X, dX), respectively.

#### Proof: [Theorem 2.21]

Since the local angle between geodesics depends only on their behavior in neighborhoods around point x<sup>0</sup> or z<sup>0</sup> respectively, for this proof we will assume, without any loss of generality, that dX(x0, xi) < π.

Part (a): Let now assume that <sup>z</sup><sup>0</sup> = [x0, r0] <sup>∈</sup> (<sup>C</sup> \ {0}) satisfies <sup>m</sup>-LAC for some <sup>m</sup> <sup>∈</sup> <sup>N</sup>. For <sup>x</sup><sup>0</sup> <sup>∈</sup> <sup>X</sup>, consider <sup>m</sup> non-trivial constant-speed geodesics <sup>x</sup>0<sup>i</sup> , connecting x<sup>0</sup> to x1, . . . , xm, respectively. Let x ǫ 0i (t) = x0i(ǫt) be defined on [0, 1] and consider the geodesics z ǫ 0i in C that corresponds to x ǫ 0i and r ǫ 0i (0) = r ǫ 0i (1) = <sup>r</sup>0. Let finally <sup>b</sup>1, . . . , b<sup>m</sup> <sup>≥</sup> <sup>0</sup>. Using up(<sup>x</sup> ǫ 0i ,x ǫ 0j ) = up(x0<sup>i</sup> ,x0<sup>j</sup> ) for all ǫ ∈ (0, 1), applying (2.30) with r<sup>i</sup> = r0, and using the simple limits limτ→<sup>0</sup> √ 2−2 cos(τ) sin(τ) = 1 and limτ→<sup>0</sup> 1−cos(τ) sin(τ) = 0, we have

$$
\sum_{i,j=1}^{m} b_i b_j \cos(\measuredangle_{\text{up}}(\boldsymbol{x}_{0i},\boldsymbol{x}_{0j})) = \lim_{\epsilon \to 0} \sum_{i,j=1}^{m} b_i b_j \cos(\measuredangle_{\text{up}}(\boldsymbol{x}_{0i}^{\epsilon},\boldsymbol{x}_{0j}^{\epsilon}))
$$
\n
$$
= \lim_{\epsilon \to 0} \sum_{i,j=1}^{m} b_i b_j \left( \frac{\sqrt{2-2\cos\mathrm{d}\chi(x_0,\boldsymbol{x}_{0i}(\epsilon))}\sqrt{2-2\cos\mathrm{d}\chi(x_0,\boldsymbol{x}_{0j}(\epsilon))}\cos(\measuredangle_{\text{up}}(\boldsymbol{z}_{0i}^{\epsilon},\boldsymbol{z}_{0j}^{\epsilon}))}{\sin(\mathrm{d}\chi(x_0,\boldsymbol{x}_{0i}(\epsilon)))\sin(\mathrm{d}\chi(x_0,\boldsymbol{x}_{0j}(\epsilon)))}
$$
\n
$$
- \frac{(\cos(\mathrm{d}\chi(x_0,\boldsymbol{x}_{0i}(\epsilon)))-1)(\cos(\mathrm{d}\chi(x_0,\boldsymbol{x}_{0j}(\epsilon)))-1)}{\sin(\mathrm{d}\chi(x_0,\boldsymbol{x}_{0i}(\epsilon)))\sin(\mathrm{d}\chi(x_0,\boldsymbol{x}_{0j}(\epsilon)))}
$$
\n
$$
= \lim_{\epsilon \to 0} \sum_{i,j=1}^{m} b_i b_j \cos(\measuredangle_{\text{up}}(\boldsymbol{z}_{0i}^{\epsilon},\boldsymbol{z}_{0j}^{\epsilon})) \geq 0.
$$

Part (b): We start by assuming that <sup>x</sup><sup>0</sup> <sup>∈</sup> <sup>X</sup> satisfies <sup>m</sup>-LAC for some <sup>m</sup> <sup>∈</sup> <sup>N</sup>. Let <sup>z</sup><sup>0</sup> <sup>=</sup> [x0, r0] <sup>∈</sup> <sup>C</sup> \ {0} and <sup>z</sup>01, . . . , <sup>z</sup>0m, m non-trivial constant-speed geodesics connecting <sup>z</sup><sup>0</sup> to some <sup>z</sup>1, . . . , z<sup>m</sup> <sup>∈</sup> <sup>C</sup>. By applying (2.29), for all <sup>b</sup> C <sup>i</sup> ≥ 0 we have

$$
\sum_{i,j=1}^{m} b_i^{\mathcal{C}} b_j^{\mathcal{C}} \cos(\measuredangle_{\text{up}}(z_{0i}, z_{0j}))
$$
\n
$$
= \sum_{i,j=1}^{m} b_i^{\mathcal{C}} b_j^{\mathcal{C}} \frac{(r_i \cos(\phi_{0i}) - r_0)(r_j \cos(\phi_{0j}) - r_0) + r_i r_j \sin(\phi_{0i}) \sin(\phi_{0j}) \cos(\measuredangle_{\text{up}}(x_{0i}, x_{0j}))}{D_{0i} D_{0j}}
$$
\n
$$
= \left(\sum_{i}^{m} b_i^{\mathcal{C}} \frac{(r_i \cos(\phi_{0i}) - r_0)}{D_{0i}}\right)^2 + \sum_{i,j=1}^{m} b_i^{\mathcal{C}} b_j^{\mathcal{C}} \frac{r_i r_j \sin(\phi_{0i}) \sin(\phi_{0j})}{D_{0i} D_{0j}} \cos(\measuredangle_{\text{up}}(x_{0i}, x_{0j})).
$$

Since x<sup>0</sup> satisfies m-LAC, the last term is non-negative as we may choose b X j := b C j r/D0<sup>j</sup> ≥ 0 as testvector. As the first term is a square we conclude that <sup>z</sup><sup>0</sup> <sup>∈</sup> (C, <sup>d</sup>C) satisfies <sup>m</sup>-LAC as well.

For parts (c) and (d) we have to study the geodesics z0<sup>i</sup> starting at the apex 0. For this we just notice that for such geodesics z01, z<sup>02</sup> ending at some z<sup>1</sup> = [x1, r1], z<sup>2</sup> = [x2, r2] the angle is equal to <sup>d</sup>X(x1, x2) <sup>∧</sup> π. Therefore by using Definition 2.17, we see that <sup>3</sup>-LAC is satisfied if and only if for every choice of pairwise different points <sup>x</sup>1, x2, x3, we have <sup>d</sup>X(x1, x2)∧<sup>π</sup> <sup>+</sup> <sup>d</sup>X(x2, x3)<sup>∧</sup> <sup>π</sup> <sup>+</sup> <sup>d</sup>X(x3, x1) <sup>∧</sup> <sup>π</sup> <sup>≤</sup> <sup>2</sup>π, which by applying the triangule inequality is easy to see that it holds if and only if for every choice of pairwise different points x1, x2, x3, we have dX(x1, x2)+dX(x2, x3)+ <sup>d</sup>X(x3, x1) <sup>≤</sup> <sup>2</sup>π. This shows part (c).

When the diameter is less than π/2, then all cosines are positive and therefore (2.21) is satisfied trivially for all <sup>m</sup> <sup>∈</sup> <sup>N</sup>. Hence, part (d) is shown as well.

We can now recover the following immediate result.

Corollary 2.21 Let (C, dC) be the cone over a geodesic metric space (X, dX).

- (a) If (C, dC) satisfies m-LAC, then (X, dX) does too.
- (b) Conversely if (X, <sup>d</sup>X) satisfies <sup>m</sup>-LAC, then (C, <sup>d</sup>C) satisfies it at every point in <sup>C</sup> \ {0}.
- (c) (C, dC) satisfies 3-LAC, if and only if (X, dX) satisfies 3-LAC and has perimeter less or equal to 2π.
- (d) If (X, dX) has diameter less or equal to π/2 and satisfies m-LAC for some m, then (C, dC) satisfies m-LAC.

### 2.7 K-semiconcavity

Another notion that we are going to introduce is the one of K-semiconcavity of a metric space (X, <sup>d</sup>X), on a set <sup>A</sup> <sup>⊂</sup> <sup>X</sup>. Before we do that, we are going to give the definition of <sup>K</sup>-semiconcave functions, and some lemmas that are going to be used in the proofs.

Definition 2.22 A function <sup>f</sup> : [0, 1] <sup>→</sup> <sup>R</sup> is called K-semiconcave, if and only if the mapping <sup>t</sup> 7→ <sup>f</sup>−Kt<sup>2</sup> is concave.

Of course, for smooth functions f this means f ′′(t) <sup>≤</sup> <sup>2</sup>K. The following result deals with semiconcave functions under composition. For a smooth K-semiconve function f[0, 1] → [a, b] and another smooth function <sup>g</sup> : [a, b] <sup>→</sup> <sup>R</sup> the composition satisfies (<sup>g</sup> ◦ <sup>f</sup>) ′′(t) = g ′ (f(t))f ′′ 1 (t) + g ′′(f1(t)) f ′ 1 (t) 2 . In the lemma below we will use the concave function g<sup>B</sup> : [0, π<sup>2</sup> ] ∋ v 7→ <sup>1</sup> <sup>−</sup> cos <sup>√</sup> v in Part B, where the term involving g ′′ can be estimated by 0, while in Part A we use g<sup>A</sup> : [0, 2[ ∋ w 7→ arccos(1−w) 2 , where g ′′ needs to be estimated on the range of f. A major part in the proof involves the proper treatment of the non-smooth situation where f ′′ is merely a measure.

Lemma 2.23 Let (X, <sup>d</sup>X) be a geodesic metric space, <sup>x</sup> <sup>∈</sup> <sup>X</sup>, and <sup>D</sup> <sup>&</sup>lt; π 2 . Let also x0, x1, x<sup>2</sup> ∈ <sup>B</sup>(x, <sup>D</sup>) <sup>⊂</sup> <sup>X</sup>, and <sup>x</sup><sup>01</sup> <sup>∈</sup> Geod(x0, x1), with <sup>x</sup><sup>2</sup> <sup>∈</sup>/ <sup>x</sup>01([0, 1]). Let finally <sup>f</sup>1, f<sup>2</sup> : [0, 1] <sup>→</sup> <sup>R</sup> given by <sup>f</sup>1(t) = 1 <sup>−</sup> cos(dX(x2,x01(t))) and <sup>f</sup>2(t) = <sup>d</sup> 2 X (x2,x01(t)) respectively. We have:

(A) If f<sup>1</sup> is d 2 X (x0, x1)K-semiconcave for some K >0, then <sup>f</sup><sup>2</sup> is 1+ 1+<sup>K</sup> π−2D d 2 X (x0, x1)-semiconcave.

(B) If f<sup>2</sup> is d 2 X (x0, x1)K-semiconcave for some K >0, then f<sup>1</sup> is (1+K) d 2 X (x0, x1)-semiconcave.

Proof: We are going to prove the result by taking second derivatives. Since the classical second derivatives are not enough to characterize convexity/concavity, we are going to make use of distributional derivatives (for definition see [Rud91]). More specifically, by [EvG15, Thm. 6.8], we have that a continuous function <sup>g</sup> : [0, 1] <sup>→</sup> <sup>R</sup> is convex if and only if its derivative is of bounded variation (for definition and properties, see [EvG15, Ch. 5]) and its second derivative is a finite positive measure. This means that a finite g is concave if and only if it exists a negative, finite measure µg, such that for every f ∈ C ∞,+ <sup>c</sup> ((0, 1)) = {<sup>f</sup> : (0, 1) <sup>→</sup> <sup>R</sup> : <sup>f</sup> is positive and smooth}, we have

$$
\int_0^1 g(t) f''(t) dt = \int_0^1 f(t) \mu_g(dt) \le 0.
$$
\n(2.32)

So, we just have to prove that if

$$
\int_0^1 (f_1(t) - K_1 t^2) f''(t) dt \le 0 \text{ for all } f \in C_c^{\infty,+}((0,1))
$$
\n(2.33)

for some K<sup>1</sup> > 0, then

$$
\int_0^1 (f_2(t) - K_2 t^2) f''(t) dt \le 0 \text{ for all } f \in C_c^{\infty,+}((0,1)),
$$
\n(2.34)

for some K<sup>2</sup> > 0, and vice-versa, where the relationship between K<sup>1</sup> and K2, will be specified later.

For abbreviation, we set v(t) = dX(x2,x01(t)). By applying the triangular inequality, we have

$$
|v(t) - v(s)| = |\mathsf{d}\chi(x_2, x_{01}(t)) - \mathsf{d}\chi(x_2, x_{01}(s))| \leq \mathsf{d}\chi(x_{01}(t), x_{01}(s)) \leq |t - s| \mathsf{d}\chi(x_0, x_1), \quad (2.35)
$$

from which we get that v(·) is Lipschits and |v ′ (t)| ≤ <sup>d</sup>X(x0, x1), almost everywhere. From (2.35) we can deduce that f1, f<sup>2</sup> are also Lipschitz, therefore the first classical derivative coincides with the first distributional one, and is given by:

$$
f_1'(t) = \sin(v(t)) v'(t), \qquad f_2'(t) = v(t)v'(t).
$$
\n(2.36)

If either of the assumptions are satisfied, which implies concavity we get that the derivative is of bounded variation. Now, since v is Lipschitz and bounded away from zero, we get that v ′ = f ′ 1 sin(v) , f ′ 2 v is of bounded variation, therefore its distributional derivative is a locally finite measure µ<sup>v</sup> ([EvG15, Th, 5.1]), and even more, it is straightforward to see the product rule for the second derivative holds true, i.e. we have

$$
\int_0^1 (f_1(t) - K_1 t^2) f''(t) dt \le 0 \iff \int_0^1 f(t) \left( \cos(v(t)) (v'(t))^2 dt + \sin(v(t)) \mu_v(dt) - K_1 dt \right) \le 0. \tag{2.37}
$$

Similarly we get

$$
\int_0^1 (f_2(t) - K_2 t^2) f''(t) dt \le 0 \quad \Leftrightarrow \quad \int_0^1 f(t) \left( (v'(t))^2 dt + v(t) \mu_v(dt) - K_2 dt \right) \le 0. \tag{2.38}
$$

Part (A). Let assume that (2.33) is true. By (2.37), we have:

$$
\int_{0}^{1} f(t) \left(\cos(v(t)) (v'(t))^{2} dt + \sin(v(t)) \mu_{v}(dt) - K_{1} dt\right) \leq 0 \Rightarrow
$$
\n
$$
\left(\min_{y \in [0,2\mathbb{D}]} \frac{\sin y}{y}\right) \int_{0}^{1} f(t) \left(\frac{v(t)}{\sin(v(t))} \cos(v(t)) (v'(t))^{2} dt + v(t) \mu_{v}(dt) - K_{1} \frac{v(t)}{\sin(v(t))} dt\right) \leq 0 \Rightarrow
$$
\n
$$
\int_{0}^{1} f(t) \left((v'(t))^{2} dt + v(t) \mu_{v}(dt) - K_{2} dt\right) \leq
$$
\n
$$
\int_{0}^{1} f(t) \left(-K_{2} + (v'(t))^{2} - \frac{v(t)}{\sin(v(t))} \cos(v(t)) (v'(t))^{2} + K_{1} \frac{v(t)}{\sin(v(t))}\right) dt,
$$
\n(2.39)

where we retrieve the last inequality by adding and subtracting. If we choose K<sup>2</sup> such that the second term is negative for every positive test function f, the we are done. We recall that |v ′ (t)| ≤ <sup>d</sup>X(x0, x1), v(t) <sup>≤</sup> <sup>2</sup><sup>D</sup> < π. Now if <sup>K</sup><sup>1</sup> <sup>=</sup> <sup>d</sup> 2 X (x0, x1)K, we can choose K<sup>2</sup> to be equal to 1 + 1+<sup>K</sup> π−2D d 2 X (x0, x1) and retrieve (2.38), independently of the choice of f ∈ C ∞,+ <sup>c</sup> ((0, 1)).

Part (B). Let assume that (2.34) is true. By (2.38), we have:

$$
\int_{0}^{1} f(t) \left( (v'(t))^{2} dt + v(t) \mu_{v}(dt) - K_{2} dt \right) \leq 0 \quad \Rightarrow
$$
\n
$$
\left( \min_{y \in [0,2\mathbb{D}]} \frac{y}{\sin y} \right) \int_{0}^{1} f(t) \left( \frac{\sin(v(t))}{v(t)} (v'(t))^{2} dt + \sin(v(t)) \mu_{v}(dt) - K_{2} \frac{\sin(v(t))}{v(t)} dt \right) \leq 0 \quad \Rightarrow
$$
\n
$$
\int_{0}^{1} f(t) \left( \cos(v(t)) (v'(t))^{2} dt + \sin(v(t)) \mu_{v}(dt) - K_{1} dt \right) \leq
$$
\n
$$
\int_{0}^{1} f(t) \left( -K_{1} + \cos(v(t)) (v'(t))^{2} - \frac{\sin(v(t))}{v(t)} (v'(t))^{2} + K_{2} \frac{\sin(v(t))}{v(t)} \right) dt
$$
\n(2.40)

Now, if K<sup>2</sup> = d 2 X (x0, x1)K, we can take K<sup>1</sup> = (1 + K) d 2 X (x0, x1) and retrieve (2.37), independently of the choice of f ∈ C ∞,+ <sup>c</sup> ((0, 1)).

We will use the result of Lemma 2.23 in the following rescaled form that allows to characterize K-semiconcavity by comparing the function with approximating parabolae.

Corollary 2.24 Let <sup>x</sup>0, x1, x<sup>2</sup> <sup>∈</sup> <sup>X</sup> and choose <sup>x</sup><sup>01</sup> <sup>∈</sup> Geod(x0, x1). Let <sup>f</sup><sup>1</sup> and <sup>f</sup><sup>2</sup> be as in Lemma 2.23. For t1, t<sup>2</sup> ∈ [0, 1] we set

$$
\tilde{x}_0^{[t_1,t_2]} = \boldsymbol{x}_{01}(t_1), \qquad \tilde{x}_1^{[t_1,t_2]} = \boldsymbol{x}_{01}(t_2), \qquad and \quad \tilde{f}_i^{[t_1,t_2]}(t) = f_i(t_1+t(t_2-t_1)).
$$

Then, the following three conditions are equivalent:

- (i) f<sup>i</sup> is Kd 2 X (x0, x1)-semiconcave if,
- (ii) for every t1, t<sup>2</sup> the mapping ˜f [t1,t2] i is Kd 2 X (˜x [t1,t2] 0 , x˜ [t1,t2] 1 )−semiconcave,
- (iii) for every t1, t2, t ∈ [0, 1] we have

$$
\tilde{f}_i^{[t_1,t_2]}(t) + Kt(1-t)\mathsf{d}^2_{\mathfrak{X}}(\tilde{x}_0^{[t_1,t_2]}, \tilde{x}_1^{[t_1,t_2]}) \ge (1-t)\tilde{f}_i^{[t_1,t_2]}(0) + t\tilde{f}_i^{[t_1,t_2]}(1). \tag{2.41}
$$

The next elementary lemma will be crucial to estimate the semiconcavities, where we crucially extract the factor t(1−t) that multiplies K on the right-hand side in (2.41).

Lemma 2.25 It exists C > 0, such that |sin(xt) − tsin(x)| ≤ Ct(1−t)x 3 , for all t ≤ 1, x ≤ π.

Proof: Using the Taylor series sin(y) = P<sup>∞</sup> n=0 (−1)n(y) 2n+1 (2n+1)! we obtain

$$
\sin(xt) - t\sin(x) = \sum_{n=0}^{\infty} (-1)^n \left( \frac{(tx)^{2n+1}}{(2n+1)!} - t\frac{x^{2n+1}}{(2n+1)!} \right) = \sum_{n=1}^{\infty} (-1)^n tx^3 \frac{(t^{2n}-1)x^{2n-2}}{(2n+1)!}.
$$

Using t ∈ [0, 1] and x ∈ [0, π] we find

$$
|\sin(xt) - t\sin(x)| \le tx^3 \sum_{n=1}^{\infty} \frac{(1 - t^{2n})x^{2n-2}}{(2n+1)!} \le tx^3(1-t) \sum_{n=1}^{\infty} \frac{4n\pi^{2n-2}}{(2n+1)!}.
$$

Setting C := P<sup>∞</sup> n=1 4nπ2n−<sup>2</sup> (2n+1)! < ∞ we arrive at the claimed estimate.

Next we define notions of local semiconcavity on a space (X, dX), we give a precise meaning of K-semiconcavity on a subset of X.

Definition 2.26 We say that (X, <sup>d</sup>X) satisfies <sup>K</sup>-semiconcavity along <sup>x</sup><sup>01</sup> <sup>∈</sup> Geod(x0, x1) for some <sup>x</sup>0, x<sup>1</sup> <sup>∈</sup> <sup>X</sup> with respect to the "observer" <sup>x</sup>2, if [0, 1] <sup>∋</sup> <sup>t</sup> 7→ <sup>f</sup>(t) = <sup>d</sup> 2 X (x2,x01(t)) is Kd 2 X (x0, x1)-semiconcave. Furthermore, we say that (X, <sup>d</sup>X) satisfies <sup>K</sup>-semiconcavity on <sup>A</sup> <sup>⊂</sup> <sup>X</sup> with respect to observers from <sup>B</sup> <sup>⊂</sup> <sup>X</sup>, if it satisfies <sup>K</sup>-semiconcavity along some geodesic x<sup>01</sup> ∈ Geod(x0, x1) for every x0, x<sup>1</sup> ∈ A, and with respect to every observer x<sup>2</sup> ∈ B. In the case <sup>A</sup> <sup>=</sup> <sup>B</sup>, we shortly say that (X, <sup>d</sup>X) satisfies <sup>K</sup>-semiconcavity on <sup>A</sup> <sup>⊂</sup> <sup>X</sup>. Finally we say that (X, dX) satisfies K-semiconcavity, if A = X.

We would like to remark that in the previous definition, x01(t) for t ∈ (0, 1) doesn't have to belong to A. Now, we are going to prove some results, that are going to be used in the last subsection to prove K′ -semiconcavity on "important" subsets of (M(X), HKℓ) or (P(X), SHKℓ), when (X, d<sup>X</sup> ) satisfies K-semiconcavity for some K > 0.

Proposition 2.27 Let (X, dX) be a geodesic metric space, and (C, dC) the cone over (X, dX). For three points <sup>z</sup><sup>0</sup> = [x0, r0], <sup>z</sup><sup>1</sup> = [x1, r1], <sup>z</sup><sup>2</sup> = [x2, r2] <sup>∈</sup> <sup>C</sup>, consider a geodesic <sup>x</sup><sup>01</sup> <sup>∈</sup> Geod(x0, x1), and the corresponding geodesic <sup>z</sup><sup>01</sup> in (C, <sup>d</sup>C). Finally let assume that for <sup>x</sup> <sup>∈</sup> <sup>X</sup> and <sup>D</sup> <sup>&</sup>lt; π 2 , we have <sup>x</sup>0, x1, x<sup>2</sup> <sup>∈</sup> <sup>B</sup> (x, <sup>D</sup>).

- (A) If (X, dX) satisfies K-semiconcavity along x01(t), with respect to x2, then (C, dC) satisfies K′ semiconcavity along z01(t) with respect to z2, where K′ can be chosen to depend continuously only on K, r0, r1, r2, D.
- (B) If <sup>x</sup><sup>0</sup> <sup>6</sup><sup>=</sup> <sup>x</sup>1, <sup>r</sup><sup>0</sup> <sup>=</sup> <sup>r</sup>1, and (C, <sup>d</sup>C) satisfies <sup>K</sup>-semiconcavity along <sup>z</sup>01(t) with respect to <sup>z</sup>2, then (X, dX) satisfies K′ -semiconcavity along x01(t) with respect to x2, where K′ can be chosen to depend continuously only on K, r0, r2, D.

Proof: From Theorem 2.7 we recall that for a geodesic z<sup>01</sup> (t) = [x<sup>01</sup> (t), r<sup>01</sup> (t)] is the corresponding geodesic in (X, dX) is given by

$$
t \mapsto x_{01}(t) = \overline{x}_{01}(\beta_{01}(t)) \text{ with } \beta_{01}(t) = \frac{r_0 \sin(t\phi_{01})}{r_1 \sin((1-t)\phi_{01}) + r_0 \sin(t\phi_{01})} \text{ with } \phi_{01} := \mathsf{d}_{\mathfrak{X}}(x_0, x_1).
$$
\n(2.42)

Later, we are going to use the fact that when r<sup>0</sup> = r1, we have

$$
\max_{t,s\in[0,1]} \frac{d_{\mathcal{C}}(z_{01}(t), z_{01}(s))}{d_{\mathcal{X}}(\overline{x}_{01}(t), \overline{x}_{01}(s))} = \max_{t,s\in[0,1]} \frac{d_{\mathcal{C}}(z_{01}(\beta(t)), z_{01}(\beta(s)))}{d_{\mathcal{X}}(x_{01}(t), x_{01}(s))} = \max_{t,s\in[0,1]} \frac{\beta(t) - \beta(s)}{t - s}
$$
\n
$$
\leq \max_{t} \beta'(t) \leq \max_{t\in[0,1]} \frac{\phi_{01}}{2\sin\left(\frac{\phi_{01}}{2}\right)} \frac{\cos(t\phi_{01})\cos\left(\frac{1-2t}{2}\phi_{01}\right) + \sin(\phi_{01})\sin\left(\left(\frac{1-2t}{2}\phi_{01}\right)\right)}{\cos^2\left(\frac{1-2t}{2}\phi_{01}\right)} \frac{\cos\left(t\phi_{01}\right)\cos\left(\frac{1-2t}{2}\phi_{01}\right)}{\cos^2\left(\frac{1-2t}{2}\phi_{01}\right)} \tag{2.43}
$$

Our proof relies on utilizing Corollary 2.24 for arbitrary t<sup>1</sup> and t<sup>2</sup> and noticing that the new r˜ [t1,t2] <sup>0</sup> = r<sup>01</sup> (t1) and r˜ [t1,t2] <sup>1</sup> = r<sup>01</sup> (t2) are bounded from below by some rmin > 0 that depend only on r0, r1, D. For notational convenience, we will drop the dependence on t1, t2, but we will use tilde ˜ for the new functions.

To compare the "concavity" magnitude of d 2 <sup>C</sup> with to the one of d 2 X along the respective geodesics and observers, we set

$$
\tilde{A}(t) = \frac{(1-t) d_{\mathcal{C}}^2(z_2, \tilde{z}_0) + t d_{\mathcal{C}}^2(z_2, \tilde{z}_1) - d_{\mathcal{C}}^2(z_2, \tilde{z}(t, \tilde{z}_0, \tilde{z}_1))}{t (1-t) d_{\mathcal{C}}^2(\tilde{z}_0, \tilde{z}_1)}.
$$
\n(2.44)

Using the formula for the cone distance d<sup>C</sup> we get

$$
\tilde{A}(t) = \frac{(1-t)\left[r_2^2 + \tilde{r}_0^2 - 2\tilde{r}_0r_2\cos\left(\mathrm{d}_{\mathcal{X}}(x_2, \tilde{x}_0)\right)\right] + t\left[r_2^2 + \tilde{r}_1^2 - 2\tilde{r}_1r_2\cos\left(\mathrm{d}_{\mathcal{X}}(x_2, \tilde{x}_1)\right)\right]}{t\left(1-t\right)\mathrm{d}_{\mathcal{C}}^2\left(\tilde{z}_0, \tilde{z}_1\right)}
$$
\n
$$
-\frac{\left[r_2^2 + \tilde{r}_{01}\left(t\right)^2 - 2r_2\tilde{r}_{01}\left(t\right)\cos\left(\mathrm{d}_{\mathcal{X}}(x_2, \tilde{x}_{01}\left(t)\right)\right)\right]}{t\left(1-t\right)\mathrm{d}_{\mathcal{C}}^2\left(\tilde{z}_0, \tilde{z}_1\right)}
$$
\n
$$
= 1 + r_2 \frac{\tilde{r}_{01}\left(t\right)\cos\left(\mathrm{d}_{\mathcal{X}}(x_2, \tilde{x}_{01}\left(t)\right)\right) - \left(1-t\right)\tilde{r}_0\cos\left(\mathrm{d}_{\mathcal{X}}(x_2, \tilde{x}_0)\right) - t\tilde{r}_1\cos\left(\mathrm{d}_{\mathcal{X}}(x_2, \tilde{x}_1)\right)}{t\left(1-t\right)\mathrm{d}_{\mathcal{C}}^2\left(\tilde{z}_0, \tilde{z}_1\right)}
$$
\n(2.45)

We compose A˜ (t) with β˜ (t) and find

$$
\frac{\tilde{A}(\tilde{\boldsymbol{\beta}}(t)) - 1}{r_2} = \frac{\tilde{r}_{01}(\tilde{\boldsymbol{\beta}}(t)) \cos \left(\mathrm{d}_{\mathcal{X}}(x_2, \tilde{x}_{01}(t))\right) - \left(1 - \tilde{\boldsymbol{\beta}}(t)\right) \tilde{r}_0 \cos \left(\mathrm{d}_{\mathcal{X}}(x_2, \tilde{x}_0)\right) - x \tilde{\boldsymbol{\beta}}(t) \tilde{r}_1 \cos \left(\mathrm{d}_{\mathcal{X}}(x_2, \tilde{x}_1)\right)}{\tilde{\boldsymbol{\beta}}(t) \left(1 - \tilde{\boldsymbol{\beta}}(t)\right) \mathrm{d}_{\mathcal{C}}^2(\tilde{z}_0, \tilde{z}_1)}.
$$

Recalling that r˜01 β˜ <sup>01</sup> (t) = r˜0r˜<sup>1</sup> sin(dX(˜x0,x˜1)) <sup>r</sup>˜<sup>1</sup> sin((1−t)dX(˜x0,x˜1))+˜r<sup>0</sup> sin(tdX(˜x0,x˜1)) we find

$$
\frac{\tilde{r}_{01}\left(\tilde{\boldsymbol{\beta}}_{01}\left(t\right)\right)}{\tilde{\boldsymbol{\beta}}_{01}\left(t\right)}=\frac{\tilde{r}_{1}\sin\left(\mathrm{d}_{\mathcal{X}}\left(\tilde{x}_{0},\tilde{x}_{1}\right)\right)}{\sin\left(t\mathrm{d}_{\mathcal{X}}\left(\tilde{x}_{0},\tilde{x}_{1}\right)\right)}\;\;\mathrm{and}\;\;\frac{1-\tilde{\boldsymbol{\beta}}_{01}\left(t\right)}{\tilde{\boldsymbol{\beta}}_{01}\left(t\right)}=\frac{\tilde{r}_{1}\sin((1-t)\,\mathrm{d}_{\mathcal{X}}\left(\tilde{x}_{0},\tilde{x}_{1}\right))}{\tilde{r}_{0}\sin\left(t\mathrm{d}_{\mathcal{X}}\left(\tilde{x}_{0},\tilde{x}_{1}\right)\right)}.
$$

Using the abbreviations φ˜ ij = d<sup>X</sup> (˜x<sup>i</sup> , x˜<sup>j</sup> ), φ˜ <sup>2</sup><sup>t</sup> <sup>=</sup> <sup>d</sup><sup>X</sup> (x2,x˜<sup>01</sup> (t)) for i, j ∈ {0, <sup>1</sup>, <sup>2</sup>} and <sup>t</sup> <sup>∈</sup> [0, 1] we can write A˜ β˜ (t) − 1 /r<sup>2</sup> as a product to estimate the terms individually:

$$
\frac{\tilde{A}(\tilde{\boldsymbol{\beta}}(\theta)) - 1}{r_2} = \frac{\tilde{r}_1 \sin(\tilde{\phi}_{01}) \cos(\tilde{\phi}_{2t}) - \tilde{r}_1 \sin((1-t)\tilde{\phi}_{01}) \cos(\tilde{\phi}_{20}) - \tilde{r}_1 \sin(t\tilde{\phi}_{01}) \cos(\tilde{\phi}_{21})}{\sin(t\tilde{\phi}_{01})(1-\tilde{\boldsymbol{\beta}}(t))d_c^2(\tilde{z}_0, \tilde{z}_1)}
$$
\n
$$
= \frac{\sin(\tilde{\phi}_{01}) \cos(\tilde{\phi}_{2t}) - \sin((1-t)\tilde{\phi}_{01}) \cos(\tilde{\phi}_{20}) - \sin(t\tilde{\phi}_{01}) \cos(\tilde{\phi}_{21})}{\sin(t\tilde{\phi}_{01}) \sin((1-t)\tilde{\phi}_{01})} \times \frac{\tilde{r}_1 \sin((1-t)\tilde{\phi}_{01}) + \tilde{r}_0 \sin(t\tilde{\phi}_{01})}{d_c^2(\tilde{z}_0, \tilde{z}_1)}
$$
\n(2.46)

Part (A). Let's first assume that (X, dX) satisfies K-semiconcavity along x<sup>01</sup> (t), with respect to x2. If the left term of the last line in (2.46) is negative then we directly get a bound for A˜ β˜ (t) by 1. If the aforementioned term is positive, we proceed as follows. Using d 2 C (˜z0, <sup>z</sup>˜1) <sup>≥</sup> 4˜r0r˜<sup>1</sup> sin<sup>2</sup> φ˜ <sup>01</sup>/2 , we can bound the last term in (2.46) by

$$
\frac{\max\{\tilde{r}_0, \tilde{r}_1\} \left[\sin\left(\left(1-t\right)\tilde{\phi}_{01}\right) + \sin\left(t\tilde{\phi}_{01}\right)\right]}{4\tilde{r}_0 \tilde{r}_1 \sin^2\left(\tilde{\phi}_{01}/2\right)} = \frac{\max\{\tilde{r}_0, \tilde{r}_1\} \sin\left(\tilde{\phi}_{01}/2\right) \cos\left(\frac{\left(1-2t\right)}{2}\tilde{\phi}_{01}\right)}{4\tilde{r}_0 \tilde{r}_1 \sin^2\left(\tilde{\phi}_{01}/2\right)} = \frac{\cos\left(\frac{\left(1-2t\right)}{2}\tilde{\phi}_{01}\right)}{4\min\{\tilde{r}_0, \tilde{r}_1\} \sin\left(\tilde{\phi}_{01}/2\right)} \le \frac{1}{4r_{\min}\sin\left(\tilde{\phi}_{01}/2\right)}.
$$
\n(2.47)

Now the K-semiconvexity of (X, dX) and Lemma 2.23 provide us with

$$
\cos\left(\mathsf{d}_{\mathcal{X}}(\tilde{\boldsymbol{x}}_{01}(t), x_2)\right) \leq (1-t)\cos\left(\mathsf{d}_{\mathcal{X}}\left(x_2, \tilde{x}_0\right)\right) + t\cos\left(\mathsf{d}_{\mathcal{X}}\left(x_2, \tilde{x}_1\right)\right) + t(1-t)\left(K+1\right)\mathsf{d}_{\mathcal{X}}^2\left(\tilde{x}_0, \tilde{x}_1\right). \tag{2.48}
$$

Hence, by combining (2.46), (2.47), (2.48) we get

$$
\frac{4r_{\min}(\tilde{A}(\tilde{\theta}(\theta))-1)}{r_2} \leq \frac{\cos(\tilde{\phi}_{20})((1-t)\sin(\tilde{\phi}_{01})-\sin((1-t)\tilde{\phi}_{01}))+\cos(\tilde{\phi}_{21})(t\sin(\tilde{\phi}_{01})-\sin(t\tilde{\phi}_{01}))}{\sin(\frac{\tilde{\phi}_{01}}{2})\sin(t\tilde{\phi}_{01})\sin((1-t)\tilde{\phi}_{01})} + (K+1)\frac{t(1-t)\sin(\tilde{\phi}_{01})\tilde{\phi}_{01}^2}{\sin(\frac{\tilde{\phi}_{01}}{2})\sin(t\tilde{\phi}_{01})\sin((1-t)\tilde{\phi}_{01})}.
$$

Exploiting Lemma 2.25 and using sin (2y) = sin (y) cos (y) we arrive at

$$
\frac{4r_{\min}(\tilde{A}(\tilde{\beta}(t)) - 1)}{r_2} \le \frac{\cos(\tilde{\phi}_{20})\left(Ct\left(1-t\right)\tilde{\phi}_{01}^3\right) + \cos(\tilde{\phi}_{21})\left(Ct\left(1-t\right)\phi_{01}^3\right)}{\sin(\frac{\tilde{\phi}_{01}}{2})\sin(t\tilde{\phi}_{01})\sin((1-t)\tilde{\phi}_{01})} + (K+1)\frac{2\cos(\frac{\tilde{\phi}_{01}}{2})\sin(\frac{\tilde{\phi}_{01}}{2})t\tilde{\phi}_{01}\left(1-t\right)\tilde{\phi}_{01}}{\sin(\frac{\tilde{\phi}_{01}}{2})\sin(t\tilde{\phi}_{01})\sin((1-t)\tilde{\phi}_{01})}.
$$
\n(2.49)

Finally we set M = maxy∈[0,2D] y sin(y) and use φ˜ ij <sup>∈</sup> [0, <sup>2</sup>D] to obtain

$$
\frac{4r_{\min}(\tilde{A}(\tilde{B}(t)) - 1)}{r_2} \le 2CM^3 + 2CM^3 + (K+1)M^2.
$$

In particular this implies

$$
\tilde{A}(t) \leq K'
$$
 with  $K' := r_2 \frac{2CM^3 + 2CM^3 + (K+1)M^2}{4r_{\min}} + 1.$ 

Thus, Part (A) is shown in view of Corollary 2.24.

Part (B). To derive the opposite conclusion we again start from (2.46) and obtain

$$
\cos\left(\tilde{\phi}_{2t}\right) - \frac{\sin\left(\left(1-t\right)\tilde{\phi}_{01}\right)}{\sin\left(\tilde{\phi}_{01}\right)}\cos\left(\tilde{\phi}_{20}\right) - \frac{\sin\left(t\tilde{\phi}_{01}\right)}{\sin\left(\tilde{\phi}_{01}\right)}\cos\left(\tilde{\phi}_{21}\right) \n= \frac{\tilde{A}\left(\tilde{B}\left(t\right)\right) - 1}{r_2} \frac{d_c^2\left(\tilde{z}_0, \tilde{z}_1\right)}{\tilde{r}_1\sin\left(\left(1-t\right)\tilde{\phi}_{01}\right) + \tilde{r}_0\sin\left(t\tilde{\phi}_{01}\right)}\frac{\sin\left(t\tilde{\phi}_{01}\right)\sin\left(\left(1-t\right)\tilde{\phi}_{01}\right)}{\sin\left(\tilde{\phi}_{01}\right)}.
$$

Using the <sup>K</sup>-semiconcavity in (C, <sup>d</sup>C) we can use <sup>A</sup>˜ (t) <sup>≤</sup> <sup>K</sup>, and with Lemma 2.25 we get

$$
\cos (\mathsf{d}_{\mathcal{X}} (x_2, x_{01} (t))) - (1-t) \cos (\mathsf{d}_{\mathcal{X}} (x_2, \tilde{x}_0)) - t \cos (\mathsf{d}_{\mathcal{X}} (x_2, \tilde{x}_1))
$$
\n
$$
= \left( (1-t) - \frac{\sin ((1-t) \tilde{\phi}_{01})}{\sin (\tilde{\phi}_{01})} \right) \cos (\tilde{\phi}_{20}) + \left( t - \frac{\sin (t \tilde{\phi}_{01})}{\sin (\tilde{\phi}_{01})} \right) \cos (\tilde{\phi}_{21})
$$
\n
$$
+ \frac{\tilde{A}(\tilde{\boldsymbol{\beta}}(t)) - 1}{r_2} \frac{\mathsf{d}_{\mathcal{C}}^2 (\tilde{z}_0, \tilde{z}_1)}{\tilde{r}_1 \sin ((1-t) \tilde{\phi}_{01}) + \tilde{r}_0 \sin (t \tilde{\phi}_{01})} \frac{\sin (t \tilde{\phi}_{01}) \sin ((1-t) \tilde{\phi}_{01})}{\sin (\tilde{\phi}_{01})}
$$
\n
$$
\leq \left( (1-t) - \frac{\sin ((1-t) \tilde{\phi}_{01})}{\sin (\tilde{\phi}_{01})} \right) \cos (\tilde{\phi}_{20}) + \left( t - \frac{\sin (t \tilde{\phi}_{01})}{\sin (\tilde{\phi}_{01})} \right) \cos (\tilde{\phi}_{21})
$$
\n
$$
+ \frac{K-1}{r_2} \mathsf{d}_{\mathcal{C}}^2 (\tilde{z}_0, \tilde{z}_1) \frac{1}{r_{\min \cos (\frac{(1-2t)}{2} \tilde{\phi}_{01})} \frac{1}{\sin (\frac{\tilde{\phi}_{01}}{2}) \sin (\tilde{\phi}_{01})} t (1-t) \tilde{\phi}_{01}^2}
$$
\n
$$
\leq \left[ 2 \frac{C \tilde{\phi}_{01}}{\sin (\tilde{\phi}_{01})} + \frac{K-1}{r_2} \frac{1}{r_{\min \cos (\frac{\tilde{\phi}_{01}}{2}) \cos (\frac{(1-2t)}{2} \tilde{\phi}_{01})} \frac{\mathsf{d}_{\mathcal{C}}^2 (\tilde{z}_0, \tilde{z}_1)}{\sin^2 (\frac{\tilde{\phi}_{01}}{2})} t (1-t) \tilde
$$

Using M = maxy∈[0,2D] y sin(y) as above and recalling (2.43) we arrive at the desired result

$$
\cos (d_{\mathcal{X}} (x_2, \tilde{x}_{01} (t))) - (1-t) \cos (d_{\mathcal{X}} (x_2, \tilde{x}_0)) - t \cos (d_{\mathcal{X}} (x_2, \tilde{x}_1)) \leq K' t (1-t) d_{\mathcal{X}}^2 (x_2, \tilde{x}_1)
$$

with K′ = 2CM + K−1 <sup>r</sup>minr<sup>2</sup> cos4(D)M<sup>2</sup> . Applying Corollary 2.24 once again, the proof of Proposition 2.27 is complete.

Now we directly recover the following Corollary.

Corollary 2.28 Let (X, dX) be a geodesic metric space, and (C, dC) the cone over (X, dX). If (X, <sup>d</sup>X) satisfies <sup>K</sup>-semiconcavity, for some <sup>K</sup> <sup>∈</sup><sup>R</sup> on a set <sup>A</sup>, then (C, <sup>d</sup>C)satisfies <sup>K</sup>′ -semiconcavity on (<sup>A</sup> <sup>∩</sup> <sup>B</sup>(x, <sup>D</sup>)) <sup>×</sup> [Rmin, Rmax], for every <sup>x</sup> <sup>∈</sup> <sup>X</sup>, <sup>D</sup> <sup>&</sup>lt; π 2 , Rmin > 0, Rmax > 0 where K′ can be chosen to depend only on K, Rmin, Rmax, d. On the other hand, if (C, dC) satisfies K-semiconcavity, for some <sup>K</sup> <sup>∈</sup> <sup>R</sup>, on a set of the form (<sup>A</sup> <sup>∩</sup> <sup>B</sup>(x, <sup>D</sup>))× {1}, then (X, <sup>d</sup>X) satisfies <sup>K</sup>′ -semiconcavity on (<sup>A</sup> <sup>∩</sup> <sup>B</sup>(x, <sup>D</sup>)), where <sup>K</sup>′ can be chosen to depend only on K, D.

# 3 Hellinger–Kantorovich space (M(X), HKℓ)

In the sequel we are going to work on spaces of measures over some underlying (geodesic) metric space (X, <sup>d</sup>X) and denote the associated cone by (C, <sup>d</sup>C). A typical example will be <sup>X</sup> = Ω <sup>⊂</sup> <sup>R</sup> d , where <sup>Ω</sup> convex, compact and equipped with the Euclidean metric <sup>d</sup>X(x, y) = <sup>|</sup>x−y|. All the abstract theory from above applies to these couples; however, our main interest lies in the case where (C, dC) is identified with (M(X), HKℓ) while the spherical space (X, dX) will be given in terms of the probability measures P(X) equipped with the metric SHKℓ, which is still to be constructed.

### 3.1 Notation and preliminaries

For the sequel, let (X, d<sup>X</sup> ) be a geodesic, Polish space. We will denote by M(X) the space of all nonnegative and finite Borel measures on X endowed with the weak topology induced by the duality with the continuous and bounded functions of Cb(X). The subset of measures with finite quadratic moment will be denoted by M2(X). The spaces P(X) and P2(X) are the corresponding subsets of probability measures.

If <sup>µ</sup> <sup>∈</sup> <sup>M</sup>(X) and <sup>T</sup> : <sup>X</sup> <sup>→</sup> <sup>Y</sup> is a Borel map, <sup>T</sup>♯<sup>µ</sup> will denote the push-forward measure on M(Y ), defined by

$$
T_{\sharp}\mu(B) := \mu(T^{-1}(B)) \quad \text{for every Borel set } B \subset Y. \tag{3.1}
$$

We will often denote elements of X×X by (x0, x1) and the canonical projections by π i : (x0, x1) → xi for <sup>i</sup> = 0, <sup>1</sup>. A transport plan on <sup>X</sup> is a measure <sup>M</sup><sup>01</sup> <sup>∈</sup> <sup>M</sup>(X×X) with marginals <sup>µ</sup><sup>i</sup> := π i <sup>♯</sup>M01.

Given a couple of measures <sup>µ</sup>0, µ<sup>1</sup> <sup>∈</sup> <sup>P</sup>2(X) with <sup>µ</sup>0(X) = <sup>µ</sup>1(X), its (quadratic) Kantorovich-Wasserstein distance Wd<sup>X</sup> is defined by

$$
\mathsf{W}_{\mathsf{d}_X}^2(\mu_0, \mu_1) := \min \left\{ \iint \mathsf{d}_X^2(x_0, x_1) \, \mathrm{d}M_{01}(x_0, x_1) \, \Big| \, M_{01} \in \mathcal{P}_2(X \times X), \ \pi_\sharp^i M_{01} = \mu_i, \ i = 0, 1 \right\}. \tag{3.2}
$$

We refer to [AGS05] for a survey on the Kantorovich–Wasserstein distance and related topics.

### 3.2 The logaritmic-entropy transport formulation

Here we first provide the definition of the HKℓ(µ0, µ1) distance in terms of a minimization problem that balances a specific transport problem of measures σ0µ<sup>0</sup> and σ1µ<sup>1</sup> with the relative entropies of σjµ<sup>j</sup> with respect to µ<sup>j</sup> . From this, the fundamental scaling property (1.2) of HK<sup>ℓ</sup> will follow, see Theorem 3.3.

For the characterization of the Hellinger–Kantorovich distance via the static Logarithmic-Entropy Transport (LET) formulation, we define the logarithmic entropy density F : [0,∞[ → [0,∞[ via F(r) = r log r − r + 1 and the cost function L<sup>ℓ</sup> : [0,∞[ → [0,∞] via Lℓ(R) = −2 log (cos (Rℓ)) for Rℓ < π 2 and L<sup>ℓ</sup> ≡ +∞ otherwise. For given measures µ0, µ<sup>1</sup> the LET functional LETℓ(· ; <sup>µ</sup>0, µ1) : <sup>M</sup>(<sup>X</sup> <sup>×</sup> <sup>X</sup>) <sup>→</sup> [0,∞[ reads

$$
\mathcal{L} \mathcal{E} \mathcal{T}_{\ell}(H_{01}; \mu_0, \mu_1) := \int_X F(\sigma_0) \mathrm{d}\mu_0 + \int_X F(\sigma_1) \mathrm{d}\mu_1 + \iint_{X \times X} L_{\ell}(\mathsf{d}_X(x_0, x_1)) \mathrm{d}H_{01} \tag{3.3}
$$

with η<sup>i</sup> := (πi)♯H<sup>01</sup> = σiµ<sup>i</sup> ≪ µ<sup>i</sup> . With this, the equivalent formulation of the Hellinger– Kantorovich distance as entropy-transport problem reads as follows.

Theorem 3.1 (LET formulation, [LMS17, Sec. 5]) For every <sup>µ</sup>0, µ<sup>1</sup> <sup>∈</sup> <sup>M</sup>(X) we have

$$
\mathsf{HK}_{\ell}^2(\mu_0, \mu_1) = \min \left\{ \mathcal{L} \mathcal{CT}_{\ell}(H_{01}; \mu_0, \mu_1) \, \middle| \, H_{01} \in \mathcal{M}(X \times X), \, (\pi_i)_{\sharp} H_{01} \ll \mu_i \right\}. \tag{3.4}
$$

An optimal transport plan H01, which always exists, gives the effective transport of mass. Note, in particular, that only η<sup>i</sup> ≪ µ<sup>i</sup> is required and the cost of a deviation of η<sup>i</sup> from µ<sup>i</sup> is given by the entropy functionals associated with F. Moreover, the cost function L<sup>ℓ</sup> is finite in the case ℓ dX(x0, x1) < <sup>π</sup> 2 , which highlights the sharp threshold between transport and pure absorption-generation mentioned earlier.

In general, optimal transport plans <sup>H</sup><sup>01</sup> <sup>∈</sup> <sup>M</sup>(<sup>X</sup> <sup>×</sup> <sup>X</sup>) are not unique. However, due to the strict convexity of F its marginals η<sup>i</sup> are unique such that the non-uniqueness of the plan H<sup>01</sup> is solely a property of the optimal transport problem for the cost Lℓ.

Theorem 3.2 (Optimality conditions [LMS17, Thm. 6.3]) For <sup>µ</sup>0, µ<sup>1</sup> <sup>∈</sup> <sup>M</sup>(X) let

$$
A'_i := \left\{ x \in X : \mathbf{\ell} \text{dist}(x, \text{supp}(\mu_{1-i})) < \frac{\pi}{2} \right\}, \quad A''_i := X \setminus A'_i,\tag{3.5}
$$

with the related decomposition

$$
\mu_i := \mu'_i + \mu''_i, \quad \mu'_i := \mu_i \mathsf{L} A'_i, \quad \mu''_i := \mu_i \mathsf{L} A''_i. \tag{3.6}
$$

(i) A plan <sup>H</sup><sup>01</sup> <sup>∈</sup> <sup>M</sup>(<sup>X</sup> <sup>×</sup>X) is optimal for the logarithmic entropy-transport problem in (3.4) for <sup>µ</sup>0, <sup>µ</sup><sup>1</sup> <sup>∈</sup> <sup>M</sup>(X) if and only if <sup>s</sup> LℓdH<sup>01</sup> < ∞ and its marginals η<sup>i</sup> are absolutely continuous with respect to µ<sup>i</sup> with densities σ<sup>i</sup> , which satisfy (we adopt the convention 0 · ∞ = 1 in (3.7c))

$$
\sigma_i = 0 \quad on \quad \text{supp}(\mu_i'') \subset A_i'' \tag{3.7a}
$$

$$
\sigma_i > 0 \quad on \quad X \setminus \text{supp}(\mu_i''), \tag{3.7b}
$$

$$
\sigma_0(x_0)\sigma_1(x_1) \ge \cos_{\pi/2}^2 (\ell \mathsf{d}_X(x_0, x_1)) \quad on \quad X \times X,\tag{3.7c}
$$

$$
\sigma_0(x_0)\sigma_1(x_1) = \cos_{\pi/2}^2 (\ell \, \mathsf{d}_X(x_0, x_1)) \quad H_{01} \text{-} a.e. \text{ on } A'_0 \times A'_1. \tag{3.7d}
$$

(ii) Moreover, we have that

$$
HK_{\ell}^{2}(\mu_{0}, \mu_{1}) = HK_{\ell}^{2}(\mu_{0}', \mu_{1}') + HK_{\ell}^{2}(\mu_{0}'', \mu_{1}''),
$$
\n(3.8a)

the couples (µ0, µ1) and (µ ′ 0 , µ′ 1 ) share the same optimal plans η, and (3.8b)

$$
\mathsf{HK}_{\ell}^2(\mu_0'', \mu_1'') = \mu_0''(X) + \mu_1''(X) = \mu_0(X \setminus A_0') + \mu_1(X \setminus A_1').
$$
 (3.8c)

We easily obtain upper bounds on HK<sup>2</sup> ℓ by inserting H<sup>01</sup> = 0 into the definition of LET<sup>ℓ</sup> in (3.4), viz, for <sup>µ</sup>0, µ<sup>1</sup> <sup>∈</sup> <sup>M</sup>(X) and <sup>ν</sup>0, ν<sup>1</sup> <sup>∈</sup> <sup>P</sup>(X) we have

$$
HK_{\ell}^{2}(\mu_{0}, \mu_{1}) \le \mu_{0}(X) + \mu_{1}(X) \quad \text{and} \quad HK_{\ell}^{2}(\nu_{0}, \nu_{1}) \le 2. \tag{3.9}
$$

# 3.3 Scaling property of HK<sup>ℓ</sup> and the definition of (P(X), SHKℓ).

Here we give the basic scaling property of the Hellinger–Kantorovich distance that is the basis of our interpretation of (M(X), HKℓ) as a cone space.

Theorem 3.3 (Scaling property of HKℓ) For all <sup>µ</sup>0, µ<sup>1</sup> <sup>∈</sup> <sup>M</sup>(X) and <sup>r</sup>0, r<sup>1</sup> <sup>≥</sup> <sup>0</sup> we have

$$
HK_{\ell}^{2}(r_{0}^{2}\mu_{0},r_{1}^{2}\mu_{1}) = r_{0}r_{1}HK_{\ell}^{2}(\mu_{0},\mu_{1}) + (r_{0}^{2}-r_{0}r_{1})\mu_{0}(X) + (r_{1}^{2}-r_{0}r_{1})\mu_{1}(X).
$$
 (3.10)

Evenmore, if H<sup>01</sup> is an optimal plan for the LET<sup>ℓ</sup> formulation of HKℓ(µ0, µ1), then H r0r<sup>1</sup> <sup>01</sup> = r0r1H<sup>01</sup> is an optimal plan for HKℓ(r 2 0µ0, r<sup>2</sup> <sup>1</sup>µ1).

Proof: Let <sup>H</sup> be the minimizer in the definition of LETℓ(·; <sup>µ</sup>0, µ1). We now calculate the scale version LETℓ(r0r1H01; r 2 0µ0, r<sup>2</sup> <sup>1</sup>µ1) as an upper estimate for inf LETℓ(·; <sup>r</sup> 2 0µ0, r<sup>2</sup> <sup>1</sup>µ1) = HKℓ(r 2 0µ0, r<sup>2</sup> <sup>1</sup>µ1) 2 . For the relative densities σ r0r<sup>1</sup> 0 and σ r0r<sup>1</sup> <sup>1</sup> we calculate

$$
\eta_0^{r_0 r_1} = r_0 r_1 \eta_0 = r_0 r_1 \sigma_0 \mu_0 = \frac{r_1}{r_0} \sigma_0 r_0^2 \mu_0 \quad \text{and} \quad \eta_1^{r_0 r_1} = r_0 r_1 \eta_1 = r_0 r_1 \sigma_1 \mu_1 = \frac{r_0}{r_1} \sigma_1 r_1^2 \mu_1,
$$

from which we obtain σ r0r<sup>1</sup> <sup>0</sup> = r1 r0 σ<sup>0</sup> and σ r0r<sup>1</sup> <sup>1</sup> = r0 r1 σ1. To determine LETℓ(r0r1H01; r 2 0µ0, r<sup>2</sup> <sup>1</sup>µ1) we first calculate the relative entropy for σ r0r<sup>1</sup> 0 :

$$
\int_{X} F(\sigma_0^{r_0 r_1}(x_0)) r_0^2 \mu_0(\mathrm{d}x_0) = \int_{X} (\sigma_0^{r_0 r_1}(x_0) \log(\sigma_0^{r_0 r_1}(x_0)) - \sigma_0^{r_0 r_1}(x_0) + 1) r_0^2 \mu_0(\mathrm{d}x_0)
$$
\n
$$
= \int \left( \frac{r_1}{r_0} \sigma_0(x_0) \log \left( \frac{r_1}{r_0} \sigma_0(x_0) \right) - \frac{r_1}{r_0} \sigma_0(x_0) + 1 \right) r_0^2 \mu_0(\mathrm{d}x_0)
$$
\n
$$
= \int_{X} \left( r_0 r_1 \left( \sigma_0(x_0) \log \sigma_0(x_0) - \sigma_0(x_0) + 1 \right) + r_0 r_1 \log \left( \frac{r_1}{r_0} \right) \sigma_0(x_0) + (r_0^2 - r_0 r_1) \right) \mu_0(\mathrm{d}x_0)
$$
\n
$$
= r_0 r_1 \int_{X} F(\sigma_0(x_0)) \mu_0(\mathrm{d}x_0) + r_0 r_1 \log \left( \frac{r_1}{r_0} \right) \eta_0(X) + (r_0^2 - r_0 r_1) \mu_0(X).
$$

Adding the corresponding term for σ r0r<sup>1</sup> <sup>1</sup> we see that the middle term cancels because we have η0(X) = η1(X), and we arrive at the following upper bound:

$$
\begin{split} \mathsf{HK}_{\ell}^{2}(r_{0}^{2}\mu_{0},r_{1}^{2}\mu_{1}) &\leq \mathcal{L}\mathcal{E}\mathcal{T}_{\ell}(r_{0}r_{1}H_{01};r_{0}^{2}\mu_{0},r_{1}^{2}\mu_{1}) \\ &= r_{0}r_{1}\left(\int_{X}F(\sigma_{0})\mu_{0}(dx_{0}) + \int_{X}F(\sigma_{1})\mu_{1}(dx_{1})\right) + (r_{0}^{2}-r_{0}r_{1})\mu_{0}(X) \\ &+ (r_{1}^{2}-r_{0}r_{1})\mu_{1}(X) + \iint_{X\times X}L_{\ell}(\mathsf{d}_{X}(x_{0},x_{1}))r_{0}r_{1}H_{01}(\mathrm{d}x_{0}\mathrm{d}x_{1}) \\ &= r_{0}r_{1}\mathcal{L}\mathcal{E}\mathcal{T}_{\ell}(H_{01};\mu_{0},\mu_{1}) + (r_{0}^{2}-r_{0}r_{1})\mu_{0}(X) + (r_{1}^{2}-r_{0}r_{1})\mu_{1}(X) \\ &= r_{0}r_{1}\mathsf{HK}_{\ell}^{2}(\mu_{0},\mu_{1}) + (r_{0}^{2}-r_{0}r_{1})\mu_{0}(X) + (r_{1}^{2}-r_{0}r_{1})\mu_{1}(X), \end{split}
$$

where in the last step we used that H<sup>01</sup> is optimal.

By replacing r<sup>j</sup> by 1/r<sup>j</sup> and µ<sup>j</sup> by r 2 <sup>j</sup>µ<sup>j</sup> this upper bound also yields

$$
\mathsf{HK}_{\ell}^2(\mu_0, \mu_1) \le \frac{1}{r_0 r_1} \mathsf{HK}_{\ell}^2(r_0^2 \mu_0, r_1^2 \mu_1) + \left(\frac{1}{r_0^2} - \frac{1}{r_0 r_1}\right) r_0^2 \mu_0(X) + \left(\frac{1}{r_1^2} - \frac{1}{r_0 r_1}\right) r_1^2 \mu_1(X).
$$

Multiplying both sides with r0r<sup>1</sup> and rearranging the terms, we obtain the desired lower bound for HK<sup>2</sup> ℓ (r 2 0µ0, r<sup>2</sup> <sup>1</sup>µ1), and the scaling relation (3.10) is proved.

The above theory for the Hellinger-Kantorovich distance HK<sup>ℓ</sup> and the abstract Theorem 2.2 allows us now to introduce a new metric distance on the probability measure P(X) via

$$
\text{SHK}_{\ell}(\nu_0, \nu_1) := \arccos\left(1 - \frac{1}{2}\text{HK}_{\ell}^2(\nu_0, \nu_1)\right) \quad \text{for } \nu_0, \nu_1 \in \mathcal{P}(X),\tag{3.11}
$$

where the mass bound (3.9) gives HKℓ(ν0, ν1) <sup>≤</sup> √ 2, which guarantees that the argument of "arccos" is in the interval [0, 1], so that SHK<sup>ℓ</sup> takes values in [0, π/2]. The mapping [·, ·] : <sup>P</sup>(X) <sup>×</sup> [0,∞) <sup>→</sup> <sup>M</sup>(X) is given via

$$
\mathcal{P}(X) \times [0, \infty) \ni (\nu, r) \mapsto [\nu, r] \stackrel{\sim}{=} r\nu \in \mathcal{M}(X).
$$

The general theory of Section 2 shows that SHK<sup>ℓ</sup> is indeed a metric and, even more, it is a geodesic metric if (X, d<sup>X</sup> ) is a geodesic space. It is shown in [LMS17] that HK<sup>ℓ</sup> is geodesic and hence our Theorem 2.7 shows that (P(X), SHKℓ) is a geodesic space. We summarize the result as follows.

Theorem 3.4 The Hellinger–Kantorovich space (M(X), HKℓ) can be identified with the cone over the spherical space (P(X), SHKℓ) in the above sense. Moreover, the latter has diameter less or equal to <sup>π</sup> 2 .

### 3.4 Cone space formulation

Amongst the many charaqctierizations of HK<sup>ℓ</sup> discussed in [LMS17] there is one that connects HK<sup>ℓ</sup> with the classic Kantorovich–Wasserstein distance on the cone C over the base space (X, ℓd<sup>X</sup> ) with metric

$$
\mathsf{d}^2_{\mathfrak{C},\ell}(z_0,z_1) := r_0^2 + r_1^2 - 2r_0r_1\cos_\pi(\ell\mathsf{d}_X(x_0,x_1)), \quad z_i = [x_i,r_i],\tag{3.12}
$$

where as above cosb(a) = cos(min{b, a}). Measures in <sup>M</sup>(X) can be "lifted" to measures in <sup>M</sup>(C), e.g. by considering the measure <sup>µ</sup> <sup>⊗</sup> <sup>δ</sup><sup>1</sup> for <sup>µ</sup> <sup>∈</sup> <sup>M</sup>(X). On the other, we can define the projection of measures in M2(C) onto measures in M(X) via

$$
\mathfrak{P}: \left\{ \begin{array}{ccc} \mathfrak{M}_2(\mathfrak{C}) & \to & \mathfrak{M}(X), \\ \lambda & \mapsto & \int_{r=0}^{\infty} r^2 \lambda(\cdot, \mathrm{d}r). \end{array} \right.
$$

For example, the lift λ = m0δ{0} + µ ⊗ 1 r(·) <sup>2</sup> δr(·) , with m<sup>0</sup> ≥ 0 and r : supp(µ) → ]0,∞[ arbitrary, gives Pλ = µ. Now, the cone space formulation of the Hellinger–Kantorovich distance of two measures <sup>µ</sup>0, <sup>µ</sup><sup>1</sup> <sup>∈</sup> <sup>M</sup>(X) is given as follows.

Theorem 3.5 (Optimal transport formulation on the cone) For <sup>µ</sup>0, µ<sup>1</sup> <sup>∈</sup> <sup>M</sup>(<sup>R</sup> d ) we have

$$
\mathsf{HK}_{\ell}^{2}(\mu_{0}, \mu_{1}) = \min \left\{ \mathsf{W}_{\mathsf{d}_{\mathfrak{C},\ell}}^{2}(\lambda_{0}, \lambda_{1}) \, \middle| \, \lambda_{i} \in \mathcal{P}_{2}(\mathfrak{C}), \, \mathfrak{P}\lambda_{i} = \mu_{i} \right\}
$$
(3.13a)

$$
= \min\left\{\iint\limits_{\mathfrak{C}\times\mathfrak{C}} d_{\mathfrak{C},\ell}^2(z_0,z_1) d\Lambda_{01}(z_0,z_1) \Big| \pi_\sharp^i \Lambda_{01} = \lambda_i, \text{ and } \mathfrak{P}\lambda_i = \mu_i\right\}.
$$
 (3.13b)

Remark 3.6 By [LMS17, Lem. 7.19], we also have

$$
\mathsf{HK}_{\ell}^{2}(\mu_{0}, \mu_{1}) = \min \Big\{ \iint\limits_{\mathfrak{C} \times \mathfrak{C}} \widetilde{\mathsf{d}}_{\mathfrak{C},\ell}^{2}(z_{0}, z_{1}) \mathrm{d}\Lambda_{01}(z_{0}, z_{1}) \Big| \pi_{\sharp}^{i} \Lambda_{01} = \lambda_{i} \text{ and } \mathfrak{P}\lambda_{i} = \mu_{i} \Big\},\tag{3.14}
$$

where <sup>e</sup><sup>d</sup> 2 C,ℓ ([x0, r0], [x1, r1]) = r 2 <sup>0</sup> + r 2 <sup>1</sup> − 2r0r<sup>1</sup> cosπ/<sup>2</sup> (ℓd<sup>X</sup> (x0, x1)) is defined with the earlier cut-off at π/2 instead of π as in (3.12).

The cone space formulation is reminiscent of classical optimal transport problems. Here, however, the marginals <sup>λ</sup><sup>i</sup> of the transport plan <sup>Λ</sup><sup>01</sup> <sup>∈</sup> <sup>M</sup>(<sup>C</sup> <sup>×</sup> <sup>C</sup>) are not fixed, and it is part of the problem to find an optimal pair of measures λ<sup>i</sup> satisfying the constraints Pλ<sup>i</sup> = µ<sup>i</sup> and having minimal Kantorovich–Wasserstein distance on the cone (C, dC).

The squared cone distance d<sup>C</sup> has an important scaling invariance: For an arbitrary Borel function θ : C <sup>2</sup> <sup>→</sup> ]0,∞[ , we define the transformation prd<sup>θ</sup> : C <sup>2</sup> <sup>→</sup> <sup>C</sup> <sup>2</sup> via

$$
\text{prd}_{\theta}(z_0, z_1) := ([x_0, r_0/\theta(z_0, z_1)]; [x_1, r_1/\theta(z_0, z_1)]), \text{ where } z_i = [x_i, r_i].
$$

Its dilation on measures <sup>Λ</sup><sup>01</sup> <sup>∈</sup> <sup>M</sup>(<sup>C</sup> 2 ) is defined by

$$
\mathrm{dil}_{\theta}(\Lambda_{01}) := (\mathrm{prd}_{\theta})_{\sharp}(\theta^2 \Lambda_{01}), \quad \text{whenever } \theta \in \mathrm{L}^2(\mathfrak{C}^2; \Lambda_{01}). \tag{3.15}
$$

Using the transformation rule, it is easy to see that

$$
\int_{\mathfrak{C}^2} d_{\mathfrak{C},\boldsymbol{\ell}}^2(z_0,z_1) d\Lambda_{01} = \int_{\mathfrak{C}^2} d_{\mathfrak{C},\boldsymbol{\ell}}^2(z_0,z_1) d\big(\text{dil}_{\theta}(\Lambda_{01})\big).
$$
\n(3.16)

# 3.5 Characterization of geodesics in (P(X), SHKℓ).

For X being a closed convex subset of R <sup>d</sup> with the Euclidean distance, we want to show that the goedesic curves can be characterized in terms of a generalized continuity equation and a Hamilton– Jacobi equation. Thus, (P(X), SHKℓ) has pseudo-Riemannian structure that is in complete analogy to that of (M(X), HKℓ) or that of the Wasserstein space (P(X), W2).

Indeed, according to [LMS16, Eqn. (5.1)] or [LMS17, Thm. 8.19] all constant-speed geodesics for HK<sup>ℓ</sup> are given as suitable solutions of the coupled system of equations

$$
\partial_t \mu + \frac{1}{\ell^2} \text{div}(\mu \nabla \xi) = 4\xi \mu, \quad \partial_t \xi + \frac{1}{2\ell^2} |\nabla \xi|^2 + 2\xi^2 = 0. \tag{3.17}
$$

Here ξ = ξ(t, x) is the dual potential, which satisfies the Hamilton–Jacobi equation, while the measure <sup>µ</sup>(t) <sup>∈</sup> <sup>M</sup>(X) follows the generlized continuity equation with transport via <sup>V</sup> <sup>=</sup> 1 ℓ <sup>2</sup> ∇ξ and growth-decay according to 4ξ.

We now want to derive the corresponding system for the spherical space (P(X), SHKℓ) by applying Theorem 2.7, which tells us that any geodesic <sup>s</sup> 7→ <sup>ν</sup>(s) <sup>∈</sup> <sup>P</sup>(X) is a rescaling of the geodesic for HK<sup>ℓ</sup> connecting ν<sup>0</sup> and ν1.

Theorem 3.7 (Equation for geodesics in(P(X), SHKℓ)) The geodesic curves <sup>s</sup> 7→ <sup>ν</sup>(s) lying in space (P(X), SHKℓ) are given by

$$
\partial_s \nu + \frac{1}{\ell^2} \text{div}(\nu \nabla \zeta) = 4(\zeta - \int_X \zeta \, d\nu) \nu, \quad \partial_s \zeta + \frac{1}{2\ell^2} |\nabla \zeta|^2 + 2(\zeta - \int_X \zeta \, d\nu)^2 = 0,\tag{3.18}
$$

where the equations have to be understood in the sense as described in [LMS17, Sec. 8.6].

Proof: We simply use the result in [LMS17, Thm. 8.19] and transform it as given the abstract projection from the cone (M(X), HKℓ) to the spherical space (P(X), SHKℓ), namely by a renormalizing of the mass and a rescaling of the arclength parameter. For this, we use the ansatz

$$
\nu(s) = n(s)\mu(\tau(s)) \quad \text{and} \quad \zeta(s, x) = a(s)\xi(\tau(s), x) + b(s),
$$

where the functions n, τ, a, and b have to be chosen suitably as functions of s, but will be independent of x ∈ X. In particular, we have

$$
\int_X \zeta(s, \cdot) d\nu(s) = b(s) + a(s) \int_X \xi(\tau(s), \cdot) d\nu(s) = b(s) + \frac{a(s)}{n(s)} \int_X \xi(\tau(s), \cdot) d\mu(s).
$$
 (3.19)

Using that (µ, ξ) solves (3.17), we obtain the relations

$$
\partial_s \nu + \frac{\dot{\tau}}{a\ell^2} \text{div}(\nu \nabla \zeta) = \left(\frac{4\dot{\tau}}{a}(\zeta - b) + \frac{\dot{n}}{n}\right)\nu, \quad \partial_s \zeta + \frac{\dot{\tau}}{a\ell^2}|\nabla \zeta|^2 + \frac{2\dot{\tau}}{a}(\zeta - b)^2 = \frac{\dot{a}}{a}(\zeta - b) + \dot{b}.
$$

To keep the transport terms, which involve the spatial derivatives, correct we choose τ such that <sup>τ</sup>˙ <sup>=</sup> <sup>a</sup> from now on. As <sup>ν</sup>(s) <sup>∈</sup> <sup>P</sup>(X), the term on the right-hand side of the continuity equation must have average 0, hence we impose

$$
4\int_X \zeta \,d\nu = 4b + \dot{n}/n. \tag{3.20}
$$

With this, we can rewrite the Hamilton–Jacobi equation for ζ in the form

$$
\partial_s \zeta + \frac{1}{\ell^2} |\nabla \zeta|^2 + 2(\zeta - \int_X \zeta \, d\nu)^2 = \left(\frac{\dot{a}}{a} - \frac{\dot{n}}{n}\right)\zeta + \dot{b} - \frac{\dot{a}}{a}b - 2b^2 + 2\left(\int_X \zeta \, d\nu\right)^2.
$$

Choosing further a = n the right-hand side simplifies further, because the term linear in ζ vanishes and the remaining term is ˙<sup>b</sup> + 2(b<sup>−</sup> R X ζ dν) 2 .

Now, we show starting from a solution (ν, ζ) of (3.18) we can find a solution (µ, ξ) of (3.17). We first solve ˙<sup>b</sup> + 2(b<sup>−</sup> R X ζ dν) <sup>2</sup> = 0 with b(s0) such that (3.19) holds at initial time s0. Then, a = n is determined from (3.20) with n(s0) = 1. Finally, the reparametrization t = τ (s) is obtained from τ˙(s) = a(s) and τ (s0) = t0. The inverse direction from a solution (µ, ξ) of (3.17) to a solution (ν, ζ) of (3.18) works similarly.

The dual dissipation potential R <sup>∗</sup> and the associated Onsager operator K, as described in [Mie11, LiM13, LM∗17] for (P(X), SHKℓ) are given formally as

$$
\mathcal{R}_{\ell}^{*}(\nu,\zeta) = \int_{X} \left( \frac{1}{2\ell^{2}} |\nabla \zeta|^{2} + 2(\zeta - \int_{X} \zeta d\nu)^{2} \right) d\nu \text{ and}
$$
$$
\mathbb{K}_{\ell}(\hat{\nu})\zeta = -\frac{1}{\ell^{2}} \text{div}(\hat{\nu}\nabla \zeta) + 4\hat{\nu}(\zeta - \int_{X} \zeta d\nu),
$$

where in the latter case ν is assumed to have the density νˆ with respect to the Lebesgue measure. Note that R ∗ ℓ (ν, ζ) is no longer affine in ν, but it is still concave, which reflects the fact that the set of geodesic curves connecting two measures <sup>ν</sup><sup>0</sup> and <sup>ν</sup><sup>1</sup> <sup>∈</sup> <sup>P</sup>(X) is still convex, a fact which is inherited from (M(X), HKℓ).

Thus, a gradient flow for a density E(ν) = R <sup>X</sup> E(ˆν) dx would formally take the form

$$
\partial_t \hat{\nu} = -\mathbb{K}_{\ell}(\hat{\nu}) \mathcal{D} \mathcal{E}(\hat{\nu}) = \frac{1}{\ell^2} \mathrm{div}(\hat{\nu} \nabla (E'(\hat{\nu}))) - 4\hat{\nu} \Big( E'(\hat{\nu}) - \int_X E'(\hat{\nu}) \hat{\nu} \, dx \Big).
$$

Existence results for such gradient-flow equations will be studied in a forthcoming paper. The next section provides first steps into this direction.

# 4 Finer geometric properties of the Hellinger–Kantorovich and the Spherical Hellinger–Kantorovich spaces

In this section we are going to prove that the metric space (X, d<sup>X</sup> ) satisfies m-LAC (cf. Definition 2.15), if and only if both (M(X), HKℓ) and (P(X), SHKℓ) satisfy m-LAC. This result is surprising since the cone (C, dC), which is intrinsically linked to (M(X), HKℓ), does not share this equivalence; however the disturbing role of the apex <sup>o</sup> <sup>∈</sup> <sup>C</sup> is irrelevant for HKℓ.

We are also going to prove that under the extra assumption that the metric space (X, d<sup>X</sup> ) satisfies K-semiconcavity on every ball B x, <sup>π</sup> 2ℓ , then (M(X), HKℓ) and (P(X), SHKℓ) satisfy K′ semiconcavity on some sets M L δ (X),P L δ (X) respectively, where K′ depends on δ, ℓ. We would like to remark that every space (X, <sup>d</sup><sup>X</sup> ), with curvature not less than κ, for some <sup>κ</sup> <sup>∈</sup> <sup>R</sup>, satisfies such a property [Oht09, Lemma 3.3] . As it is was mentioned in Section 2.6 (see [OPV14, Part 1, Ch. 6], [Sav07]), when these two properties hold in a space, and a functional F defined on that space is λ-convex, then for every point in the space there exists a unique gradient flow with respect to F starting on that point. In some parallel work, we are aiming to extend that result to cover cases where K-seminconcavity holds only on suitable collections of subsets, as long as the functionals F have the property that starting from any point that belongs in a set in the collection, then any minimizer in the JKO scheme, belongs in an another suitable subset in the class. This way, we are going to provide several examples of gradient flows in (M(X), HKℓ),(P(X), SHKℓ).

# 4.1 Stability of m-LAC between (X, dX), (M(X),HKℓ(X)), and (P(X), SHKℓ(X))

We will start by proving that the metric space (X, d<sup>X</sup> ) satisfies m-LAC, if and only if both (M(X), HKℓ) and (P(X), SHKℓ) satisfy it too. The proof of the first is a modification of the proof that if a metric space (X, d<sup>X</sup> ) satisfies m-LAC, then the Wasserstein space (P2(X), W2) over (X, d<sup>X</sup> ) also satisfies it, which was kindly communicated to us by Giuseppe Savaré (personal communication, May 2017). Because the cone (C, dC) over (X, d<sup>X</sup> ) does not necessarily satisfy m-LAC due to the degeneracy at the apex (see Theorem 2.21), one cannot use the argument verbatim. We will show the desired equivalence by exploiting that the minimizing plans satisfy the optimality conditions.

Proposition 4.1 Consider <sup>µ</sup><sup>0</sup> <sup>∈</sup> (M(X), HKℓ) such that (X, <sup>d</sup><sup>X</sup> ) satifies <sup>m</sup>-LAC for <sup>µ</sup>0-a.e. <sup>x</sup><sup>0</sup> <sup>∈</sup> X. Then, (M(X), HKℓ(X)) satisfies m-LAC at µ0.

Proof: For the proof, we are going to utilize the cone representation introduced in Section 3.4. Let <sup>µ</sup>01, . . . , <sup>µ</sup>0<sup>m</sup> be geodesics connecting <sup>µ</sup><sup>0</sup> <sup>∈</sup> <sup>M</sup>(X), with <sup>µ</sup><sup>i</sup> <sup>∈</sup> <sup>M</sup>(X), i <sup>=</sup> {1, . . . , m}. By an application of [LMS17, Thm. 8.4], we can find geodesics λ01, . . . , λ0<sup>m</sup> in P(C), such that Pλ0i(t) = µ0<sup>i</sup> (t) (the fact that we can have λ0i(0) to be equal to some fixed λ<sup>0</sup> for i = 1, . . . , m is given by [LMS17, Lemma 7.10]). By [Lis06, Thm. 6] we can find optimal geodesic plans <sup>Λ</sup>0→<sup>i</sup> <sup>∈</sup> P(C[0, 1]; C) in the sense that (et)♯Λ0→<sup>i</sup> = λ0i(t). By a refined version of the glueing lemma we can find a plan <sup>Λ</sup> <sup>∈</sup> <sup>P</sup>((C([0, 1]; <sup>C</sup>) <sup>m</sup>), such that π 0→i <sup>♯</sup> <sup>Λ</sup> <sup>=</sup> <sup>Λ</sup>0→<sup>i</sup> . For Λ-a.e. z = (z01, . . . , z0m) we have that <sup>z</sup>01, . . . , <sup>z</sup>0<sup>m</sup> are geodesics and <sup>z</sup>01(0) = · · · <sup>=</sup> <sup>z</sup>0m(0). We split the measure <sup>Λ</sup> in two parts Λ{0} and ΛC\{0} , such that Λ{0} (z0i(0) = {0}) = <sup>Λ</sup>(z0i(0) = {0}) and <sup>Λ</sup>C\{0} (z0i(0) 6= {0}) = <sup>Λ</sup>(z0i(0) <sup>6</sup><sup>=</sup> {0}). For <sup>Λ</sup>C\{0} let us set <sup>θ</sup>ij (z) = up(z0<sup>i</sup> , z0<sup>j</sup> ). Since m-LAC is satisfied for µ0-a.e. x<sup>0</sup> in (X, d<sup>X</sup> ), by an application of Theorem 2.18, we have that m-LAC is satisfied for (et)♯π 0→i <sup>♯</sup> <sup>Λ</sup>C\{0} -a.e. <sup>z</sup><sup>0</sup> in (C, <sup>d</sup>C), and therefore for <sup>Λ</sup>C\{0} -a.e. z = (z01, . . . , z0m). We will assume without any loss of generality that all geodesics have length equal to a. By applying Remark 3.6, where we introduced <sup>e</sup>dC,<sup>ℓ</sup> with the cut-off π/<sup>2</sup> instead of <sup>π</sup> as in <sup>d</sup>C,ℓ, we obtain

$$
a^2 \cos \xi_{\text{up}}(\mu_{0i}, \mu_{0j}) = \liminf_{s,t\downarrow 0} \frac{1}{2st} \left( \mathsf{HK}_{\ell}^2(\mu_0, \mu_{0i}(t)) + \mathsf{HK}_{\ell}^2(\mu_0, \mu_{0j}(s)) - \mathsf{HK}_{\ell}^2(\mu_{0i}(t), \mu_{0j}(s)) \right)
$$
  
\n
$$
\geq \liminf_{s,t\downarrow 0} \frac{1}{2st} \left( W_{d_{\mathfrak{C},\ell}}^2(\lambda_0, \lambda_{0i}(t)) + W_{d_{\mathfrak{C},\ell}}^2(\lambda_0, \lambda_{0j}(s)) - W_{\tilde{d}_{\mathfrak{C},\ell}}^2(\lambda_{0i}(t), \lambda_{0j}(s)) \right)
$$
  
\n
$$
\geq \liminf_{s,t\downarrow 0} \frac{1}{2st} \int \left( d_{\mathfrak{C},\ell}^2(z_0, z_{0i}(t)) + d_{\mathfrak{C},\ell}^2(z_0, z_{0j}(s)) - \tilde{d}_{\mathfrak{C},\ell}^2(z_{0i}(t), z_{0j}(s)) \right) d\mathbf{\Lambda}
$$
  
\n
$$
\geq \liminf_{s,t\downarrow 0} \frac{1}{2st} \int \left( d_{\mathfrak{C},\ell}^2(0, z_{0i}(t)) + d_{\mathfrak{C},\ell}^2(0, z_{0j}(s)) - \tilde{d}_{\mathfrak{C},\ell}^2(z_{0i}(t), z_{0j}(s)) \right) d\mathbf{\Lambda}^{\{0\}}
$$
  
\n
$$
+ \liminf_{s,t\downarrow 0} \frac{1}{2st} \int \left( d_{\mathfrak{C},\ell}^2(z_0, z_{0i}(t)) + d_{\mathfrak{C},\ell}^2(z_0, z_{0j}(s)) - \tilde{d}_{\mathfrak{C},\ell}^2(z_{0i}(t), z_{0j}(s)) \right) d\mathbf{\Lambda}^{\ell\setminus\{0\}}.
$$

The first term in the last sum is strictly positive. For the second term, we are able to use ed 2 C,ℓ (z0i(t), <sup>z</sup>0<sup>j</sup> (s)) <sup>≤</sup> <sup>d</sup> 2 C,ℓ (z0i(t), z0<sup>j</sup> (s)). Therefore, by applying Fatou's lemma we have

$$
a^2 \cos \xi_{\text{up}}(\mu_{0i}, \mu_{0j})
$$
  
\n
$$
\geq \int \liminf_{s,t\downarrow 0} \frac{1}{2st} \left( d^2_{\mathfrak{C},\ell}(z_0,z_{0i}(t)) + d^2_{\mathfrak{C},\ell}(z_0,z_{0j}(s)) - d^2_{\mathfrak{C},\ell}(z_{0i}(t),z_{0j}(s)) \right) d\Lambda^{\mathfrak{C}\setminus{\{0\}}}
$$
  
\n
$$
\geq \int \cos(\theta_{ij}(z)) d\Lambda^{\mathfrak{C}\setminus{\{0\}}}.
$$

Thus, applying part (b) of Theorem 2.21 for every choice of positive b<sup>i</sup> (i = 1, . . . , m) we find

$$
\sum_{i,j=1}^m \cos(\mu_{0i}, \mu_{0j}) b_i b_j \ge \frac{1}{a^2} \int \left( \sum_{i,j=1}^m \cos(\theta_{ij}(z)) b_i b_j \right) d\Lambda^{\mathfrak{C} \setminus \{0\}} \ge 0,
$$

which is the desired result for µ0.

We conclude this subsection with the following main result.

Theorem 4.2 The space (X, d<sup>X</sup> ) satisfies m-LAC, if and only if the space (M(X), HKℓ) satisfies m-LAC, if and only if the space (P(X), SHKℓ) satisfies m-LAC.

Proof: We simple collect the results from above.

((X, <sup>d</sup><sup>X</sup> ) <sup>⇒</sup> (M(X), HKℓ)): It is a straightforward application of Proposition 4.1.

((M(X), HKℓ) <sup>⇒</sup> (X, <sup>d</sup><sup>X</sup> )): We just use Dirac measures, and the fact that geodesics stay within the set of Dirac measures.

((M(X), HKℓ) <sup>⇔</sup> (P(X), SHKℓ)): The proof is a straightforward application of Theorem 2.21 part (d), using that (P(X), SHKℓ)) has diameter less than π/2 (see Theorem 3.4.)

### 4.2 K-semiconcavity on sets of measures with doubling properties

Here we are going to provide results related to K-semiconcavity. We will start with a general lemma that gives an estimate for the total mass of the minimizer in LET(·; <sup>µ</sup>0, µ1) (see Theorem 3.1). By B(X) we denote the collection of all Borel sets in (X, d<sup>X</sup> ).

Lemma 4.3 Let <sup>µ</sup>0, µ<sup>1</sup> <sup>∈</sup> <sup>M</sup>(X), and let <sup>H</sup><sup>01</sup> be a minimizer for LETℓ(·; <sup>µ</sup>0, µ1), then

$$
H_{01}(X \times X) \le \sqrt{\mu_0'(X)\mu_1'(X)} \le \sqrt{\mu_0(X)\mu_1(X)},\tag{4.1}
$$

where (µ ′ 0 , µ′ 1 ) is the reduced couple of (µ0, µ1). Furthermore, we have

$$
H_{01}(A \times X) \le \sqrt{\mu_0'(A)\mu_1'\left(A_{\frac{\pi}{2\ell}}\right)} \quad \text{for all } A \in \mathcal{B}(X),\tag{4.2}
$$

where <sup>A</sup><sup>b</sup> <sup>=</sup> { <sup>y</sup> <sup>∈</sup> <sup>X</sup> | ∀ <sup>x</sup> <sup>∈</sup> <sup>A</sup> : <sup>d</sup>X(x, y) <sup>≤</sup> <sup>b</sup> }. Finally, if <sup>X</sup> <sup>⊂</sup> <sup>R</sup> <sup>d</sup> and <sup>µ</sup>0, µ<sup>1</sup> <sup>≪</sup> <sup>L</sup>, and T : X → X is a function whose graph is the support of H<sup>01</sup> (such a function exists by [LMS17, Theorem 6.6]), then

$$
H_{01}(A \times T(A)) \le \sqrt{\mu_0'(A)\mu_1'(T(A))} \quad \text{for all } A \in \mathcal{B}(X). \tag{4.3}
$$

Proof: By (3.8c), (µ0, µ1) and (µ ′ 0 , µ′ 1 ), share the same optimal plans. Let σ<sup>i</sup> be the optimal densities <sup>d</sup>η<sup>i</sup> dµ′ i . Then, the optimality condition (3.7d), which is valid in the support of H01, gives

$$
H_{01}^{2}(X \times X) = \left(\int_{A'_{0} \times A'_{1}} 1 \mathrm{d}H_{01}\right)^{2} \stackrel{(3.7d)}{=} \left(\int_{A'_{0} \times A'_{1}} \frac{\cos\left(\ell d_{X}(x_{0}, x_{1})\right)}{\sqrt{\sigma_{0}(x_{0})\sigma_{1}(x_{1})}} \mathrm{d}H_{01}\right)^{2}
$$
  
$$
\stackrel{\cos \leq 1}{\leq} \left(\int_{A'_{0} \times A'_{1}} \frac{1}{\sqrt{\sigma_{0}(x_{0})\sigma_{1}(x_{1})}} \mathrm{d}H_{01}\right)^{2} \stackrel{C-S}{\leq} \left(\int_{A'_{0} \times A'_{1}} \frac{1}{\sigma_{0}(x_{0})} \mathrm{d}H_{01}\right) \left(\int_{A'_{0} \times A'_{1}} \frac{1}{\sigma_{1}(x_{1})} \mathrm{d}H_{01}\right)
$$
  
$$
= \int_{A'_{0}} \frac{1}{\sigma_{0}} \mathrm{d}\eta_{0} \int_{A'_{1}} \frac{1}{\sigma_{1}} \mathrm{d}\eta_{1} = \int_{A'_{0}} \mathrm{d}\mu_{0} \int_{A'_{1}} \mathrm{d}\mu_{1} = \mu'_{0}(X) \mu'_{1}(X).
$$

For showing (4.2) we define

$$
\sigma_{1,A} = \frac{dH_{01}(A \times \cdot)}{d\mu'_1}
$$
 and  $\sigma_1 = \frac{dH_{01}(X \times \cdot)}{d\mu'_1}$ .

such that <sup>0</sup> <sup>≤</sup> <sup>σ</sup>1,A <sup>≤</sup> <sup>σ</sup>1. We define two measures <sup>µ</sup><sup>e</sup> ′ 1 and µ ′ 1 via

$$
\widetilde{\mu}'_1(B) = \int_B \frac{\sigma_{1,A}(x_1)}{\sigma_1(x_1)} \mu'_1(\mathrm{d}x_1) \quad \text{and} \quad \overline{\mu}'_1(B) = \mu'_1(B) - \widetilde{\mu}'_1(B) \text{ for all } B \in \mathcal{B}(X). \tag{4.4}
$$

We have that (H01) (A×X), is a plan between (µ ′ 0 ) <sup>A</sup> and <sup>µ</sup><sup>e</sup> ′ 1 . In a similar way we see that (H01) ((X\A)×X) is a plan between (µ ′ 0 ) (X\A) and µ ′ 1 . Also it is straightforward to see that the sum of the cost of the two plans is equal to the cost of H01, therefore these plans must be both optimal. Now applying the first part, i.e. (4.1), w we have

$$
H_{01}(A \times X) = (H_{01} \sqcup (A \times X))(X \times X) \le \sqrt{\mu'_0(A)\widetilde{\mu}'_1(X)}
$$
  
 
$$
\le \sqrt{\mu'_0(A)\widetilde{\mu}'_1\left(A_{\frac{\pi}{2\ell}}\right)} \le \sqrt{\mu'_0(A)\mu'_1\left(A_{\frac{\pi}{2\ell}}\right)},
$$

which is the desired result (4.2).

Finally, if H<sup>01</sup> is an optimal plan for µ ′ 0 , µ′ 1 , and T : X → X is a function whose graph is the support of H01, then H<sup>01</sup> (A×T(A)) = H<sup>01</sup> (A×X) is an optimal plan between µ ′ <sup>0</sup> A and µ˜ ′ <sup>1</sup> T(A) = ˜µ ′ 1 , where µ˜ ′ 1 is defined as in (4.4). Now by applying the same argument as before, we have

$$
H_{01}(A \times T(A)) = (H_{01} \sqcup (A \times T(A)))(X \times X) = (H_{01} \sqcup (A \times X))(X \times X) \le \sqrt{\mu'_0(A)\widetilde{\mu}'_1(X)}
$$
  
$$
\le \sqrt{\mu'_0(A)(\widetilde{\mu}'_1 \sqcup T(A))(X)} \le \sqrt{\mu'_0(A)\widetilde{\mu}'_1(T(A))} \le \sqrt{\mu'_0(A)\mu'_1(T(A))},
$$

Before we proceed with the main result of this subsection, we are going to provide some definitions and extra notation. In the following we use the notation B(x, r) for metric balls in (X, d<sup>X</sup> ) and possibly in over metric spaces.

Definition 4.4 (Doubling metric space) A metric space (X, d<sup>X</sup> ) is called doubling, if for every D<sup>2</sup> ≥ D<sup>1</sup> > 0, there exists a constant C(D2/D1) ≥ 1, that depends only on the ratio, such that every ball of radius D<sup>2</sup> can be covered by C(D2/D1) balls of radius D1.

Definition 4.5 (Doubling measure on metric space) In (X, d<sup>X</sup> ), a Borel measure L is called doubling if for every <sup>D</sup><sup>2</sup> <sup>≥</sup> <sup>D</sup><sup>1</sup> <sup>&</sup>gt; <sup>0</sup>, it exists a constant <sup>C</sup>¯(D2/D1) <sup>≥</sup> <sup>1</sup>, that depends only on the ratio, that for every <sup>x</sup> <sup>∈</sup> X, we have <sup>L</sup>(B(x, <sup>D</sup>2)) <sup>≤</sup> <sup>C</sup>¯(D2/D1)L(B(x, <sup>D</sup>1)).

In [HK∗15, Hei01] one can find more information on doubling spaces and measures. The existence of a doubling measure in every complete doubling metric space is provided in [Hei01, Thm. 13.3]. We are mostly interested in X = R <sup>d</sup> or X = Ω, where Ω is a compact subset of R d with Lipschitz boundary, in which case the Lebesgue measure is doubling. We are also interested in manifolds of finite dimension with lower bounds on the Ricci curvature, where the volume measure is doubling, see [Stu06b, Stu06a].

Definition 4.6 (Locally doubling measure) In a metric space (X, d<sup>X</sup> ), a Borel measure L is called locally doubling, if for every M > 0 and M ≥ D<sup>2</sup> ≥ D<sup>1</sup> > 0 there exists a constant <sup>C</sup>¯M(D2/D1) <sup>≥</sup> <sup>1</sup> that depends only on the ratio <sup>D</sup>2/D<sup>1</sup> and on the upper bound <sup>M</sup> such that for every <sup>x</sup> <sup>∈</sup> <sup>X</sup> we have <sup>L</sup>(B(x, <sup>D</sup>2)) <sup>≤</sup> <sup>C</sup>¯M(D2/D1)L(B(x, <sup>D</sup>1)).

Since for our result it is easier to work with finite reference measures, we provide the following useful lemma, where we exchange the global doubling property with finiteness of the reference measure.

Lemma 4.7 For every doubling measure <sup>L</sup><sup>e</sup> we can find a finite locally doubling measure <sup>L</sup> that is equivalent to <sup>L</sup><sup>e</sup> (i.e. <sup>L</sup><sup>e</sup> <sup>≪</sup> <sup>L</sup> and <sup>L</sup> <sup>≪</sup> <sup>L</sup><sup>e</sup> ).

Proof: For some point <sup>x</sup><sup>a</sup> <sup>∈</sup> X, we define <sup>L</sup>(dx) = <sup>1</sup> (1+C¯(2))2d(xa,x) <sup>L</sup>e(dx). For the finiteness of <sup>L</sup>, we observe that

$$
\mathcal{L}(X) = \sum_{i=0}^{\infty} \int_{\overline{B(x_{\mathfrak{a}}, i+1)} \setminus B(x_{\mathfrak{a}}, i)} \frac{1}{(1+\bar{C}(2))^{2\mathfrak{d}(x_{\mathfrak{a}}, x)}} \widetilde{\mathcal{L}}(\mathrm{d}x) \le \sum_{i=0}^{\infty} \int_{\overline{B(x_{\mathfrak{a}}, i+1)}} \frac{1}{(1+\bar{C}(2))^{2i}} \widetilde{\mathcal{L}}(\mathrm{d}x)
$$
\n
$$
\le \sum_{i=0}^{\infty} \frac{\mathcal{L}(\overline{B(x_{\mathfrak{a}}, i+1)})}{(1+\bar{C}(2))^{2i}} \le \mathcal{L}(B(x_{\mathfrak{a}}, 1)) \sum_{i=0}^{\infty} \frac{\bar{C}(2)^{i+2}}{(1+\bar{C}(2))^{2i}} < \infty,
$$
\n
$$
(4.5)
$$

where C¯(2) is the doubling constant for L. We also have

$$
\frac{\mathcal{L}B(x,\mathfrak{D}_2)}{\mathcal{L}B(x,\mathfrak{D}_1)}\leq \frac{\tilde{\mathcal{L}}B(x,\mathfrak{D}_2)}{\tilde{\mathcal{L}}B(x,\mathfrak{D}_1)}\frac{(1+\bar{C}(2))^{2(\mathsf{d}(x_{\mathfrak{a}},x)+\mathfrak{D}_1)}}{(1+\bar{C}(2))^{2(\mathsf{d}(x_{\mathfrak{a}},x)-\mathfrak{D}_2)}}\leq \bar{C}(\mathfrak{D}_2/\mathfrak{D}_1)(1+\bar{C}(2))^{2(\mathfrak{D}_1+\mathfrak{D}_2)}.
$$

Therefore for M > 0, we conclude that L is locally doubling with constant C¯M(D2/D1) := C¯(D2/D1)(1 + C¯(2))6<sup>M</sup> , which proves the result.

For a finite, locally doubling measure <sup>L</sup> and <sup>δ</sup> <sup>∈</sup> (0, 1) we define the set

$$
\overline{\mathcal{M}}^{\mathcal{L}}_{\delta}(X) = \left\{ \mu \in \mathcal{M}(X) : \mu \ll \mathcal{L}, \ \delta \le \frac{d\mu}{d\mathcal{L}}(x) \le \frac{1}{\delta}, \text{ for } \mathcal{L}\text{-a.e. } x \in X \right\}.
$$
 (4.6)

For positive numbers d1, d2, we also define

$$
\widetilde{\mathcal{M}}_{\mathsf{d}_1,\mathsf{d}_2}^{\mathcal{L}}(X) = \left\{ \mu \in \mathcal{M}(X) : \forall x \in X : \ \mathsf{d}_2 \le \frac{\mu\left(B\left(x,\mathsf{d}_1\right)\right)}{\mathcal{L}\left(B\left(x,\mathsf{d}_1\right)\right)} \le \frac{1}{\mathsf{d}_2} \right\}.
$$
\n
$$
(4.7)
$$

It is straightforward to see that M L δ (X) <sup>⊂</sup> <sup>M</sup><sup>e</sup> <sup>L</sup> <sup>d</sup>1,δ(X). Furthermore all elements in <sup>M</sup> L δ (X) have total mass bounded by <sup>1</sup> <sup>δ</sup> <sup>L</sup>(X). The reason that we are using these two sets instead of just of one of them is that neither is geodesically closed in (M(X), HKℓ). However, as will be proved later, for each δ > 0 we can find ˜d1, ˜d<sup>2</sup> <sup>&</sup>gt; <sup>0</sup> such that for every <sup>µ</sup>0, µ<sup>1</sup> <sup>∈</sup> <sup>M</sup> L δ (X) we have <sup>µ</sup>01(t) <sup>∈</sup> <sup>M</sup><sup>e</sup> <sup>L</sup> d1,d<sup>2</sup> (X) for all t ∈ [0, 1].

Theorem 4.8 (K-semiconcavity for (M(X), HKℓ)) Let (X, d<sup>X</sup> ) be a doubling metric space. We also assume that (X, d<sup>X</sup> ) satisfies K-semiconcavity on every ball B x, <sup>π</sup> 2ℓ . Finally, let L be a finite, locally doubling measure, and M L δ (X) as in (4.6). Then, there exists <sup>K</sup>′ <sup>∈</sup> <sup>R</sup>, that depends only on K, δ such that (M(X), HKℓ) is K′ -semiconcave on M L δ (X)

The result is based on two facts. The first one is Corollary 2.28, i.e. that for R1, R<sup>2</sup> > 0 and 0 < Dˆ < π 2 it exists a <sup>K</sup>′ <sup>∈</sup> <sup>R</sup> that depends only on <sup>R</sup>1, R2, <sup>D</sup><sup>ˆ</sup> , K, <sup>ℓ</sup> such that for every <sup>x</sup> <sup>∈</sup> <sup>X</sup> the space (C, dC,ℓ) satisfies K′ -semiconcavity on Bℓd<sup>X</sup> (x, D) × [R1, R2]. The second is that when two measures, are "uniform" enough, and have bounded densities with respect to each other, then the transport happens in distances less than <sup>D</sup> ℓ , for some D with D < π/2, and also the densities with respect to the optimal plan are bounded. The result is established via of several intermediate results.

Lemma 4.9 Let (X, <sup>d</sup><sup>X</sup> ) be doubling, <sup>L</sup> a finite locally doubling measure, and <sup>M</sup><sup>e</sup> <sup>L</sup> d1,d<sup>2</sup> (X), as in (4.7) for 0 < d<sup>1</sup> < π 2ℓ and <sup>d</sup><sup>2</sup> <sup>&</sup>gt; <sup>0</sup>. Then, there exists <sup>0</sup> < Cmin <sup>≤</sup> <sup>C</sup>max, such that for every <sup>µ</sup>0, µ<sup>1</sup> <sup>∈</sup> <sup>M</sup><sup>e</sup> <sup>L</sup> d1,d<sup>2</sup> (X) and any optimal plan <sup>H</sup><sup>01</sup> for LETℓ(·; <sup>µ</sup>0, µ1) we have

$$
C_{\min} \le \sigma_i(x_i) \le C_{\max}, \quad \eta_i \text{-} a.e. \tag{4.8}
$$

where η<sup>i</sup> = π i #H<sup>01</sup> = σiµ<sup>i</sup> for i = 0, 1. Furthermore, any transportation happens in distances strictly less than some <sup>π</sup> 2ℓ , i.e. it exists D < π 2 that depends only on <sup>d</sup>1, <sup>d</sup>2, such that <sup>ℓ</sup>d<sup>X</sup> (x0, x1) <sup>≤</sup> D for H<sup>01</sup> almost every (x0, x1).

Proof: By the optimality conditions, we know that there exist sets A0, A<sup>1</sup> with µ0(X\A0) = η0(X\A0) = µ1(X\A1) = η1(X\A1) = 0, such that

$$
\sigma_0(x_0)\sigma_1(x_1) \ge \cos_{\frac{\pi}{2}}^2 (\ell d_X(x_0, x_1)) \quad \text{in} \quad A_0 \times A_1. \tag{4.9}
$$

By dividing with σ1(x1) and integrating with respect to µ<sup>0</sup> on B(x1, d1), we obtain

$$
\eta_0(B(x_1, \mathbf{d}_1)) \ge \frac{\cos_{\frac{\pi}{2}}^2 (\ell \mathbf{d}_1)}{\sigma_1(x_1)} \mu_0(B(x_1, \mathbf{d}_1)) \ge \frac{\cos_{\frac{\pi}{2}}^2 (\ell \mathbf{d}_1)}{\sigma_1(x_1)} \mathbf{d}_2 \mathcal{L}(B(x_1, \mathbf{d}_1)),
$$
(4.10)

for every x<sup>1</sup> ∈ A1. Using Lemma 4.3 we find

$$
\eta_0(B(x_1, d_1)) \leq \sqrt{\mu_0(B(x_1, d_1))\mu_1(B(x_1, d_1)\frac{\pi}{2\ell})}
$$
\n
$$
\leq \sqrt{\mu_0(B(x_1, d_1))\sqrt{C\left(\left(\frac{\pi}{2\ell} + d_1\right)/d_1\right)\mu_1(B(y, d_1))}}
$$
\n
$$
\leq \frac{1}{d_2}\sqrt{\mathcal{L}(B(x_1, d_1))}\sqrt{C\left(\left(\frac{\pi}{2\ell} + d_1\right)/d_1\right)\mu_1\sup_{y\in B_{\frac{\pi}{2\ell}}(x_1, d_1)}\mathcal{L}(B(y, d_1))}
$$
\n
$$
\leq \frac{1}{d_2}\sqrt{\mathcal{L}(B(x_1, d_1))}\sqrt{C\left(\left(\frac{\pi}{2\ell} + d_1\right)/d_1\right)\mathcal{L}(B(x_1, d_1)\frac{\pi}{2\ell})}}
$$
\n
$$
\leq \frac{1}{d_2}\mathcal{L}(B(x_1, d_1))\sqrt{C\left(\left(\frac{\pi}{2\ell} + d_1\right)/d_1\right)\mathcal{L}(B(x_1, d_1)\frac{\pi}{2\ell})}}
$$
\n
$$
\leq \frac{1}{d_2}\mathcal{L}(B(x_1, d_1))\sqrt{C\left(\left(\frac{\pi}{2\ell} + d_1\right)/d_1\right)\mathcal{L}(\frac{\pi}{2\ell} + d_1)/d_1}},
$$
\n(4.11)

where the constant C π <sup>2</sup>ℓ+d<sup>1</sup> /d<sup>1</sup> is as in the definition of doubling metric spaces to cover a set of radius <sup>π</sup> <sup>2</sup><sup>ℓ</sup> <sup>+</sup> <sup>d</sup><sup>1</sup> by balls of radius <sup>d</sup>1, and <sup>C</sup>¯ <sup>π</sup> ℓ π <sup>2</sup>ℓ+d<sup>1</sup> /d<sup>1</sup> is the doubling measure constant for radius less than <sup>π</sup> ℓ . We set Ce = q C π <sup>2</sup>ℓ+d<sup>1</sup> /d<sup>1</sup> C¯ π ℓ π <sup>2</sup>ℓ+d<sup>1</sup> /d<sup>1</sup> , and by combining (4.10) and (4.11), we derive the lower bound

$$
\sigma_1(x_1) \ge \cos_{\frac{\pi}{2}}^2 (\ell d_1) d_2^2 / \tilde{C} \quad \text{in} \quad A_1. \tag{4.12}
$$

Now, by the second optimality condition we have

$$
\sigma_0(x_0) = \frac{\cos_{\frac{\pi}{2}}^2 (\ell d_X(x_0, x_1))}{\sigma_1(x_1)} \le \frac{\tilde{C}}{\cos_{\frac{\pi}{2}}^2 (\ell d_1) d_2^2}, \quad H_{01}\text{-a.e. in } A_0 \times A_1. \tag{4.13}
$$

By interchaning the roles of σ<sup>0</sup> and σ<sup>1</sup> and combining all the inequalities we arrive at

$$
C_{\min} := \frac{\cos_{\frac{\pi}{2}}^2 (\ell \mathsf{d}_1) d_2^2}{\widetilde{C}} \le \sigma_i(x_i) \le \frac{\widetilde{C}}{\cos_{\frac{\pi}{2}}^2 (\ell \mathsf{d}_1) d_2^2} =: C_{\max}, \quad \eta_i \text{-a.e. in } A_i,
$$

which is the desired result.

Now by visiting the second optimality condition one more time, we get that cos<sup>2</sup> π 2 (ℓdX(x0, x1)) is bounded from below by a positive constant that depends only on the bounds of σ<sup>i</sup> , for H01-a.e. (x0, x1). Therefore by continuity of the cosine, we get that it exists D < <sup>π</sup> 2 such that for every <sup>µ</sup>0, µ<sup>1</sup> <sup>∈</sup> <sup>M</sup><sup>e</sup> <sup>L</sup> d1,d<sup>2</sup> (X), we have <sup>ℓ</sup>dX(x0, x1) <sup>≤</sup> <sup>D</sup>, for <sup>H</sup>01-a.e. (x0, x1).

The next result shows that the geodesic closure of M L δ (X) is contained in <sup>M</sup><sup>e</sup> <sup>L</sup> d1,d<sup>2</sup> (X) for suitably chosen d1, d2.

Lemma 4.10 Let (X, d<sup>X</sup> ) be doubling, L be a finite locally doubling measure, and M L δ (X) be as in (4.6). Then, for each δ > <sup>0</sup> there exist <sup>d</sup><sup>1</sup> <sup>∈</sup> (0, π 2ℓ ) and d<sup>2</sup> > 0 such that any constantspeed geodesic <sup>µ</sup><sup>01</sup> connecting <sup>µ</sup><sup>0</sup> to <sup>µ</sup><sup>1</sup> with <sup>µ</sup>0, µ<sup>1</sup> <sup>∈</sup> <sup>M</sup> L δ (X) satisfies <sup>µ</sup>01(t) <sup>∈</sup> <sup>M</sup><sup>e</sup> <sup>L</sup> d1,d<sup>2</sup> (X) for all t ∈ [0, 1].

Proof: It is straightforward to see that M L δ (X) is a subset of some <sup>M</sup><sup>e</sup> <sup>L</sup> min{ π 4ℓ , 1 2 },δ(X). Therefore, by Lemma 4.9, we find ˜<sup>d</sup> <sup>∈</sup> ]0, π/2[, which depends only on <sup>δ</sup>, such that <sup>ℓ</sup>dX(x0, x1) <sup>≤</sup> ˜d < <sup>π</sup> 2 holds for H01-a.a. (x0, x1). Let Λ<sup>01</sup> be the optimal plan in the cone definition, and Λ0→<sup>1</sup> the occurring plan on the geodesics. For x<sup>0</sup> ∈ X, we have

$$
\mu_{01}\left(t;B\left(x_0,\frac{\pi+2\tilde{d}}{4\ell}\right)\right) \geq \mathfrak{P}\left[\left(e_t\right)_{\sharp}\left(\Lambda_{0\to1}\right)\mathsf{L}\left\{x_{01}(0)\in B\left(x_0,\frac{\pi-2\tilde{d}}{4\ell}\right)\right\}\right](X),\qquad(4.14)
$$

since all points in B x0, π−2d˜ 4ℓ , will be transfered at most distance <sup>d</sup>˜ ℓ . Therefore will remain in a ball of radius B x0, π+2d˜ 4ℓ . Now µ˜01(t) = P h (et)<sup>♯</sup> (Λ0→1) n x01(0) ∈ B x0, π−2d˜ 4ℓ oi is a geodesic starting from µ<sup>0</sup> B x0, π−2d˜ 4ℓ . Let m˜ (t) = (µ˜01(t))(X). By (2.11) and recalling (1.3) we get

$$
\tilde{m}(t) \ge (1-t)^2 \tilde{m}(0) + t^2 \tilde{m}(1),
$$

which in turn for t ∈ -0, 1 2 , gives

$$
\mathfrak{P}\left[(e_{t})_{\sharp}(\Lambda_{0\to1})\mathsf{L}\left\{x_{01}(0)\in B\left(x_{0},\frac{\pi-2\tilde{d}}{4\ell}\right)\right\}\right](X)
$$
\n
$$
\geq (1-t)^{2}\mathfrak{P}\left[(e_{0})_{\sharp}(\Lambda_{0\to1})\mathsf{L}\left\{x_{01}(0)\in B\left(x_{0},\frac{\pi-2\tilde{d}}{4\ell}\right)\right\}\right](X)
$$
\n
$$
\geq (1-t)^{2}\mu_{0}\left(B\left(x_{0},\frac{\pi-2\tilde{d}}{4\ell}\right)\right)\geq \frac{1}{4}\mu_{0}\left(B\left(x_{0},\frac{\pi-2\tilde{d}}{4\ell}\right)\right)\geq \frac{\delta}{4}\mathcal{L}\left(B\left(x_{0},\frac{\pi-2\tilde{d}}{4\ell}\right)\right)\right) \leq \frac{\delta}{4}\mathcal{L}\left(B\left(x_{0},\frac{\pi-2\tilde{d}}{4\ell}\right)\right) \tag{4.15}
$$
\n
$$
\geq \frac{\delta}{4\tilde{C}_{M}\left(\left(\frac{\pi+2\tilde{d}}{4\ell}\right)/\left(\frac{\pi-2\tilde{d}}{4\ell}\right)\right)}\mathcal{L}\left(B\left(x_{0},\frac{\pi+2\tilde{d}}{4\ell}\right)\right).
$$

Combining 4.14 and 4.15, we get that

$$
\frac{\mu_{01}\left(t;B\left(x_{0},\frac{\pi+2\tilde{d}}{4\ell}\right)\right)}{\mathcal{L}\left(B\left(x_{0},\frac{\pi+2\tilde{d}}{4\ell}\right)\right)} \geq \frac{\delta}{4\tilde{C}_{M}\left(\left(\frac{\pi+2\tilde{d}}{4\ell}\right)/\left(\frac{\pi-2\tilde{d}}{4\ell}\right)\right)}
$$
(4.16)

We work in the same manner with the roles of µ<sup>0</sup> and µ<sup>1</sup> being reversed to recover the same estimate on the interval [1/2, 1], and this way we retrieve the lower bound with d<sup>1</sup> = π+2d˜ 4ℓ and d<sup>2</sup> = δ <sup>π</sup>+2d˜ π−2d˜ .

$$
a_2 = \frac{1}{4\tilde{C}_M\left(\left(\frac{\pi + 2\tilde{d}}{4\ell}\right) / \left(\frac{\pi - 2\tilde{d}}{4\ell}\right)\right)}.
$$
  
In a similar manner by

In a similar manner by utilizing (2.10) instead of (2.11), we obtain a corresponding upper bound.

Lemma 4.11 Let (X, <sup>d</sup><sup>X</sup> ) be doubling, <sup>L</sup> a finite, locally doubling measure, and let <sup>M</sup><sup>e</sup> <sup>L</sup> d1,d<sup>2</sup> (X) be as in (4.7). Then, there exist Rmin, Rmax > 0 that depend on d1, d2, such that for µ0, µ<sup>1</sup> with <sup>µ</sup>01(t) <sup>∈</sup> <sup>M</sup><sup>e</sup> <sup>L</sup> d1,d<sup>2</sup> (X) and <sup>µ</sup><sup>2</sup> <sup>∈</sup> <sup>M</sup><sup>e</sup> <sup>L</sup> d1,d<sup>2</sup> (X) we can find measures <sup>λ</sup>0, λ1, λ2, λ<sup>t</sup> <sup>∈</sup> <sup>P</sup>2(C[Rmin, Rmax]) with

Pλ<sup>i</sup> = µ<sup>i</sup> , Pλ<sup>t</sup> = µ01(t), WdC,<sup>ℓ</sup> (λ<sup>i</sup> , λt) = HKℓ(µ<sup>i</sup> , µ01(t)) for i = 0, 1, 2.

Proof: For <sup>i</sup> = 0, <sup>1</sup>, <sup>2</sup>, let <sup>H</sup>ti be the optimal plan in the definition of LETℓ(·; <sup>µ</sup><sup>i</sup> , µ(t)), and σ ti i , σti t the densities of η ti i , ηti <sup>t</sup> with respect to µ<sup>i</sup> , µ<sup>t</sup> . Let now the plans

$$
\Lambda_{ti}(\mathrm{d}z_i, \mathrm{d}z_t) = \delta_{\sqrt{\sigma_i^{ti}(x_i)}}(\mathrm{d}r_i)\delta_{\sqrt{\sigma_i^{ti}(x_t)}}(\mathrm{d}r_i)H_{ti}(\mathrm{d}x_i, \mathrm{d}x_t).
$$

For i = 0, 1, 2, we take θ ti([z<sup>t</sup> , z<sup>i</sup> ]) = <sup>r</sup> σ ti t (xt) σ t0 t (xt) , and we define Λ˜ ti = dil<sup>θ</sup> ti (Λti). Finally we set λ<sup>i</sup> = π i ♯Λ˜ ti for i = 0, 1, 2. It is straightforward to see that r<sup>i</sup> = r σ ti t (xt) σ t0 t (xt) q σ ti i (xi) for λi-a.e. z<sup>i</sup> = [x<sup>i</sup> , r<sup>i</sup> ], with i = 0, 1, 2. By Lemma 4.9, we now obtain

$$
R_{\min} := \frac{C_{\min}}{\sqrt{C_{\max}}} \le r_i \le \frac{C_{\max}}{\sqrt{C_{\min}}} =: R_{\max} \text{ for } \lambda_i\text{-a.e. } z_i = [x_i, r_i], \text{ for } i = 0, 1, 2.
$$

This proves the the claim that all λ<sup>i</sup> are supported in C[Rmin, Rmax].

Now we are able to conclude the proof of the main result of this section.

Proof: [Proof of Theorem 4.8] By Lemma 4.10 there exists 0 < d<sup>1</sup> < π 2ℓ and 0 < d<sup>2</sup> such that every geodesic <sup>µ</sup><sup>01</sup> connecting <sup>µ</sup>0, µ<sup>1</sup> <sup>∈</sup> <sup>M</sup> L δ (X) satisfies <sup>µ</sup>01(t) <sup>∈</sup> <sup>M</sup><sup>e</sup> <sup>L</sup> d1,d<sup>2</sup> (X) for all t ∈ [0, 1]. We also have <sup>µ</sup><sup>2</sup> <sup>∈</sup> <sup>M</sup><sup>e</sup> <sup>L</sup> d1,d<sup>2</sup> (X) <sup>⊃</sup> <sup>M</sup> L δ (X). We would like to utilize the equivalent definition of K−semiconcavity given in (2.41), therefore we will just take µ˜<sup>0</sup> = µ01(t1), µ˜<sup>1</sup> = µ01(t2), for t1, t<sup>2</sup> ∈ [0, 1], and µ˜01(t) = µ01(t(t<sup>2</sup> − t1) + t1). By Lemma 4.11, there exists Rmin, Rmax that depend on <sup>d</sup>1, <sup>d</sup>2, and therefore on δ, such that for every <sup>µ</sup>˜0, <sup>µ</sup>˜1, <sup>µ</sup>˜<sup>2</sup> <sup>∈</sup> <sup>M</sup><sup>e</sup> <sup>L</sup> d1,d<sup>2</sup> (X) and 0 < t < 1 we can find measures <sup>λ</sup>0, λ1, λ2, λ<sup>t</sup> <sup>∈</sup> <sup>P</sup>2(C[Rmin, Rmax]) with

$$
\mathfrak{P}\lambda_i = \tilde{\mu}_i, \quad \mathfrak{P}\lambda_t = \tilde{\mu}_{01}(t), \text{ and } \mathsf{W}_{\mathsf{d}_{\mathfrak{C},\ell}}(\lambda_i,\lambda_t) = \mathsf{HK}_{\ell}(\tilde{\mu}_i,\tilde{\mu}_{01}(t)), \quad i = 0, 1, 2. \tag{4.17}
$$

Using the geodesic property of µ˜<sup>01</sup> yields

$$
W_{d_{\mathfrak{C},\ell}}(\lambda_0,\lambda_t) + W_{d_{\mathfrak{C},\ell}}(\lambda_1,\lambda_t) = HK_{\ell}(\mu_0,\tilde{\mu}_{01}(t)) + HK_{\ell}(\mu_1,\tilde{\mu}_{01}(t))
$$
  
= HK<sub>\ell</sub>( $\tilde{\mu}_0,\tilde{\mu}_1$ )  $\leq W_{d_{\mathfrak{C},\ell}}(\lambda_0,\lambda_1)$ .

Hence, it is straightforward to see that there exists a geodesic λ<sup>01</sup> connecting λ0, λ1, such that λ01(t) = λ<sup>t</sup> . Furthermore, by [Lis06, Thm. 6] there is a plan Λ0→<sup>1</sup> on the geodesics such that Λts := (e<sup>t</sup> , es)♯Λ0→<sup>1</sup> is an optimal plan between λ(t) and λ(s). Now, by using a gluing lemma, we can find a plan Λ0→<sup>1</sup> 2t in <sup>P</sup>((C[0, 1]; <sup>C</sup>) <sup>×</sup> <sup>C</sup>), such that <sup>Λ</sup><sup>01</sup> = (e0, e1)<sup>♯</sup> π 0→1 <sup>♯</sup> <sup>Λ</sup>0→<sup>1</sup> 2t , and (et(π 0→1 ) <sup>×</sup> <sup>I</sup>)♯Λ0→<sup>1</sup> 2t is an optimal plan for WdC,<sup>ℓ</sup> (λ2, λ01(t)). Finally by applying the last part of Lemma 4.9, we get the existence of a D < <sup>π</sup> 2 such that ℓdX(x2, xt) < D for (et(π 0→1 ) × I)♯Λ0→<sup>1</sup> 2t almost every (z2, zt), similarly ℓdX(x0, x1) < D for Λ<sup>01</sup> almost every [z0, z1]. Therefore, for Λ0→<sup>1</sup> 2t almost every (z2, z(·, z0, z1)), where z(·, z0, z1) is a geodesic connecting z0, z1, we have <sup>x</sup>0, x1, x2,x¯(t, z0, z1) <sup>∈</sup> <sup>B</sup> (x¯(t, z0, z1), d). By Lemma 2.27 we get a <sup>K</sup>′ such that

$$
d_{\mathfrak{C},\ell}^2(z_2, z(t,z_0,z_1)) + K't(1-t)d_{\mathfrak{C},\ell}^2(z_0,z_1) \ge (1-t)d_{\mathfrak{C},\ell}^2(z_2,z_0) + t d_{\mathfrak{C},\ell}^2(z_2,z_1),
$$
\n(4.18)

for Λ0→<sup>1</sup> <sup>2</sup><sup>t</sup> almost every (z2, <sup>z</sup>(·, z0, z1)). By integrating with respect to <sup>Λ</sup>0→<sup>1</sup> 2t , we find

$$
\mathsf{W}_{\mathsf{d}_{\mathfrak{C},\ell}}^2(\lambda_2,\lambda_{01}(t)) + K't(1-t)\mathsf{W}_{\mathsf{d}_{\mathfrak{C},\ell}}^2(\lambda_0,\lambda_1) \ge (1-t)\mathsf{W}_{\mathsf{d}_{\mathfrak{C},\ell}}^2(\lambda_2,\lambda_0) + t\mathsf{W}_{\mathsf{d}_{\mathfrak{C},\ell}}^2(\lambda_2,\lambda_1). \tag{4.19}
$$

Using (4.17) we find the desired semiconcavity, and Theorem 4.8 is proved.

To obtain a similar result for the Spherical Hellinger–Kantorovich distance SHK<sup>ℓ</sup> we define

$$
\mathcal{P}_{\delta}^{\mathcal{L}}(X) := \left\{ \nu \in \mathcal{P}(X) \ : \ \nu = \frac{\mu}{\mu(X)}, \ \mu \in \overline{\mathcal{M}}_{\delta}^{\mathcal{L}}(X) \right\} \supset \mathcal{P}(X) \cap \overline{\mathcal{M}}_{\delta}^{\mathcal{L}}(X)
$$

as analog of M L δ (X), see (4.6). Now for the Spherical Hellinger-Kantorovich space (P(X), SHKℓ) satisfies the following analog of Theorem 4.8 for (M(X), HKℓ).

Theorem 4.12 ( K-semiconcavity for (P(X), SHKℓ)) Let (X, d<sup>X</sup> ) be a doubling metric space and assume that (X, d<sup>X</sup> ) satisfies K-semiconcavity on every ball B x, <sup>π</sup> 2ℓ . Furthermore, let L be a finite, locally doubling measure, and M L δ (X) as in (4.6). Then, there exists <sup>K</sup>′ <sup>∈</sup> <sup>R</sup>, which depends only on K, δ, ℓ, such that (P(X), SHKℓ) is K′ -semiconcave on P L δ (X).

Proof: For <sup>µ</sup> <sup>∈</sup> <sup>M</sup> L δ (X), we have <sup>δ</sup>L(X) <sup>≤</sup> <sup>µ</sup>(X) <sup>≤</sup> 1 <sup>δ</sup>L(X), therefore for <sup>ν</sup> <sup>=</sup> µ µ(X) , we have δ <sup>2</sup> <sup>≤</sup> dν dL (x) ≤ 1 δ <sup>2</sup> . We get that P L δ (X) <sup>⊂</sup> <sup>P</sup>(X) <sup>∩</sup> <sup>M</sup> L δ <sup>2</sup> (X). It is also trivial to see that it exists a D < <sup>π</sup> 2 , such that <sup>P</sup>(X) <sup>∩</sup> <sup>M</sup> L δ <sup>2</sup> (X) <sup>⊂</sup> <sup>B</sup>(ν0, <sup>D</sup>), for some <sup>ν</sup><sup>0</sup> <sup>∈</sup> <sup>P</sup>(X) <sup>∩</sup> <sup>M</sup> L δ <sup>2</sup> (X) <sup>⊂</sup> <sup>B</sup>(ν0, <sup>D</sup>). Now we apply Corollary 2.28 with combination with Theorem 4.8, and get the result.

Acknowledgment We would like to thank Anton Petrunin, Giuseppe Savaré, and Marios Stamatakis for useful communication in different stages of this project. We would like to especially thank Marios Stamatakis for providing us a first proof of Proposition 2.10.

## References

- [ABN86] A. D. Aleksandrov, V. N. Berestovskii, and I. G. Nikolaev. Generalized Riemannian spaces. Russian Mathematical Surveys, 41(3), 1–54, jun 1986.
- [AGS05] L. Ambrosio, N. Gigli, and G. Savaré. Gradient flows in metric spaces and in the space of probability measures. Lectures in Mathematics ETH Zürich. Birkhäuser Verlag, Basel, 2005.
- [AKP17] S. Alexander, V. Kapovitch, and A. Petrunin. Alexandrov geometry. Unpublished, 2017.
- [BBI01] D. Burago, Y. Burago, and S. Ivanov. A Course in Metric Geometry. Graduate Studies in Mathematics, 33, xiv+415, 2001.
- [Ber83] V. Berestovskii. Borsuk's problem on the metrization of a polyhedron. Soviet Math. Dokl, 1983.
- [BrH99] M. R. Bridson and A. Häfliger. Metric Spaces of Non-Positive Curvature. Springer-Verlag, BerlinSpringer, 1999.

- [CP∗15a] L. Chizat, G. Peyré, B. Schmitzer, and F.-X. Vialard. An interpolating distance between optimal transport and Fisher–Rao. arXiv:1506.06430v2, 2015.
- [CP∗15b] L. Chizat, G. Peyré, B. Schmitzer, and F.-X. Vialard. Unbalanced optimal transport: geometry and Kantorovich formulation. arXiv:1508.05216v1, 2015.
- [DeD09] M. M. Deza and E. Deza. Encyclopedia of Distances. Springer, 2009.
- [EvG15] L. C. Evans and R. F. Gariepy. Measure theory and fine properties of functions. Revised edition, 2015.
- [Hei01] J. Heinonen. Lectures on analysis on metric spaces. Springer-Verlag, New York, 2001.
- [HK∗15] J. Heinonen, P. Koskela, N. Shanmugalingam, and J. T. Tyson. Sobolev spaces on metric measure spaces: an approach based on upper gradients. Cambridge University Press, Cambridge, 2015.
- [KMV16] S. Kondratyev, L. Monsaingeon, and D. Vorotnikov. A new optimal transport distance on the space of finite Radon measures. Adv. Differ. Eqns., 21(11/12), 1117–1164, 2016.
- [LiM13] M. Liero and A. Mielke. Gradient structures and geodesic convexity for reactiondiffusion systems. Phil. Trans. Royal Soc. A, 371(2005), 20120346, 28, 2013.
- [Lis06] S. Lisini. Characterization of absolutely continuous curves in Wasserstein spaces. Calculus of Variations and Partial Differential Equations, 28(1), 85–120, oct 2006.
- [LM∗17] M. Liero, A. Mielke, M. A. Peletier, and D. R. M. Renger. On microscopic origins of generalized gradient structures. Discr. Cont. Dynam. Systems Ser. S, 10(1), 1–35, 2017.
- [LMS16] M. Liero, A. Mielke, and G. Savaré. Optimal transport in competition with reaction – the Hellinger–Kantorovich distance and geodesic curves. SIAM J. Math. Analysis, 48(4), 2869–2911, 2016.
- [LMS17] M. Liero, A. Mielke, and G. Savaré. Optimal entropy-transport problems and the Hellinger–Kantorovich distance. Invent. math., 2017. Accepted. WIAS preprint 2207, arXiv:1508.07941v2.
- [Mie11] A. Mielke. A gradient structure for reaction-diffusion systems and for energy-driftdiffusion systems. Nonlinearity, 24, 1329–1346, 2011.
- [Oht09] S.-i. Ohta. Gradient flows on Wasserstein spaces over compact Alexandrov spaces. American Journal of Mathematics, 131(2), 1–39, 2009.
- [OPV14] Y. Ollivier, H. Pajot, and C. Villani, editors. Optimal transport. Theory and applications. Cambridge: Cambridge University Press, 2014.
- [Rud91] W. Rudin. Functional analysis. McGraw-Hill, 1991.
- [Sav07] G. Savaré. Gradient flows and diffusion semigroups in metric spaces under lower curvature bounds. Comptes Rendus Mathematique, 345(3), 151–154, aug 2007.
- [Stu99] K.-T. Sturm. Metric spaces of lower bounded curvature. Exposition. Math., 17(1), 35–47, 1999.
- [Stu06a] K.-T. Sturm. On the geometry of metric measure spaces. Acta Mathematica, 196(1), 65–131, 2006.
- [Stu06b] K.-T. Sturm. On the geometry of metric measure spaces. II. Acta Mathematica, 196(1), 133–177, 2006.