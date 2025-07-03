#### RELATIONS BETWEEN L p - AND POINTWISE CONVERGENCE OF FAMILIES OF FUNCTIONS INDEXED BY THE UNIT INTERVAL.

Abstract. We construct a variety of mappings from the unit interval I into L p ([0, 1]), 1 ≤ p < ∞, to generalize classical examples of L p converging sequences of functions with simultaneous pointwise divergence. By establishing relations between the regularity of the functions in the image of the mappings and the topology of I, we obtain examples which are L p -continuous but exhibit discontinuity in a pointwise sense to different degrees. We conclude by proving a Lusin-type theorem, namely that if almost every function in the image is continuous, then we can remove a set of arbitrarily small measure from the index set I and establish pointwise continuity in the remainder.

# 1. Introduction

1.1. Motivation and Overview. Examples of sequences of real functions on a compact domain which have a limit in L p , but do not converge pointwise are well known. Their construction is based on the fact that any interval can be covered infinitely often by a sequence of subintervals of vanishing lengths. Take, for instance, the sequence (fi)i∈I of characteristic functions f<sup>i</sup> = χI<sup>i</sup> , i ∈ N, of the intervals I<sup>i</sup> = [ <sup>i</sup> 2 <sup>k</sup> − 1, i+1 2 <sup>k</sup> − 1], where k is the unique integer with 2<sup>k</sup> ≤ i < 2 <sup>k</sup>+1. After applying a suitable molifier to smoothen each member of the sequence, we can see that this pointwise divergence is not affected by the smoothness of the functions. In such examples, only the order of the index set is relevant. We can observe, however, that a simple topology is induced in a natural way by the convergence of the sequence. It is not obvious whether examples of this type can be extended to index sets of a more complex topological structure. We wish to address the case of a continuous curve f which maps I = [0, 1] into L p ([0, 1]) and generalize examples like the above. In our setting, the index set I has a non-trivial topological structure of its own, which turns out to interact with the regularity properties of the family {f<sup>t</sup> , t ∈ I}.

Curves such as {f<sup>t</sup> , t ∈ I} often appear in semigroup theory as solutions of PDEs. However, the smoothing properties of the operators in these settings usually result in a high regularity for the solutions for every t > 0, and therefore pointwise convergence comes naturally. Even for the more anomalous case of t = 0, pointwise convergence can often be deduced by using tools from harmonic analysis or potential theory. In this paper, no underlying process is assumed. We investigate the pointwise behaviour of the curves in a purely real analytic way.

By making different assumptions regarding the properties of the functions ft , we construct two example curves in L <sup>p</sup> which lack pointwise convergence almost everywhere. The first example is constructed in Section 2, where we assume that {f<sup>t</sup> , t ∈ I} ⊂ C(Ω) and that almost all f<sup>t</sup> are smooth. In Section 3 we then show that the criteria on the regularity f<sup>t</sup> are optimal. We demonstrate that the structure of I renders "everywhere pointwise divergence" impossible, and that higher regularity always implies better pointwise convergence properties.

In Section 4 we remove the continuity requirement and construct a curve of highly irregular functions. For this curve, we not only have everywhere pointwise divergence, but also, for every subset T of I with positive measure, the restriction f|<sup>T</sup> exhibits pointwise divergence almost everywhere.

Finally, Section 5 is devoted to proving that the discontinuity of f<sup>t</sup> is necessary to obtain a curve that exhibits such a highly pointwise divergence. In particular, the example in Section 4 motivates a special case of our main result Theorem 5.2., which can be interpreted as a refined version of Lusin's Theorem in two variables.

1.2. Notation. Throughout, I is the unit interval [0, 1], equipped with the standard norm | · | and the corresponding Borel-σ-field. Lebesgue measure on I is denoted by µ. We study functions f : I × Ω −→ R of two real variables, we will usually, for t ∈ I, write f<sup>t</sup> for the function f(t, ·) in one real variable to stress the difference between "time" and "space", but revert to write f as a function of two variables when it is notationally more convenient. The spacial domain Ω ⊂ R of the functions f<sup>t</sup> , t ∈ I, can be chosen to be any interval of R equipped with its Borel σ-field and Lebesgue measure. We take Ω = [0, 1] for convenience in the construction of the examples. We denote Lebesgue measure by λ to avoid confusion with the "time" interval I, whenever we refer to space, i.e. when measuring sets in the domain and range of the real functions f<sup>t</sup> , t ∈ [0, 1].

L p (Ω, R, λ) = L p , for 1 ≤ p < ∞, denotes the space of real-valued pintegrable functions on Ω, equipped with the topology induced by the seminorm k · kp. Furthermore, we write W1,p for the space of all absolutely continuous functions with derivatives belonging to L <sup>p</sup> and use the standard notation C(Ω) and C∞(Ω) for the space of continuous real valued functions on Ω and the space of real valued smooth functions on Ω \ ∂Ω.

Remark 1.1. Note that we do not identify almost everywhere indentical members of L p , since all our constructions are pointwise. To prove lack of convergence at a point t, we choose a sequence t<sup>n</sup> converging to t and assure, that ft<sup>n</sup> diverges pointwise on a set of positive measure. Therefore the established irregularity can not be avoided by choosing different "versions" of f<sup>t</sup> and trivial counterexamples like the continuous transport of a set of measure zero are excluded.

# 2. Construction of the first example

We begin by showing that there is a L p -continuous curve of continuous functions, along which pointwise convergence can be established almost nowhere. Moreover, this irregularity is achieved while keeping almost all functions along the curve smooth.

<span id="page-2-0"></span>Theorem 2.1. Let 1 ≤ p < ∞ and K ⊂ [0, 1] be a meager Fσ. There is a continuous mapping f of [0, 1] into L p (Ω), satisfying

(i) f<sup>t</sup> is absolutely continuous for all t ∈ [0, 1],

(ii) f<sup>t</sup> ∈ C∞(Ω) for every t ∈ K,

but also

(A) for every t ∈ K there exists a sequence (tn)n∈<sup>N</sup> with limn→∞ t<sup>n</sup> = t such that

$$
\lambda(\lbrace x \in \Omega : (f_{t_n}(x))_{n \in \mathbb{N}} \text{ is } Cauchy \rbrace) = 0.
$$

In particular, if µ(K) = 1, then the conditions in (ii) and (A) hold for µ-a.e. t ∈ [0, 1].

Proof. Without loss of generality, we will assume that {0, 1} ⊂ K. We can represent K = S<sup>∞</sup> <sup>i</sup>=1 K<sup>i</sup> , where {0, 1} ⊂ K<sup>1</sup> ⊂ K<sup>2</sup> ⊂ . . . are closed nowhere dense subsets of [0, 1]. For each i, the complement K<sup>C</sup> i can be represented as a countable union S<sup>∞</sup> <sup>j</sup>=1(ri,j , si,j ) of disjoint open intervals, whose lengths we denote by li,j = µ((ri,j , si,j )). In this setting define

$$
f^{(i)}(t,x) = \varphi_i(t)\gamma_i(t,x),
$$

where

$$
\varphi_i(t) = \begin{cases}\n\frac{2j}{l_{i,j}}(t - r_{i,j}) & \text{if } t \in (r_{i,j}, r_{i,j} + \frac{l_{i,j}}{2j}), \\
1 & \text{if } t \in [r_{i,j} + \frac{l_{i,j}}{2j}, s_{i,j} - \frac{l_{i,j}}{2j}], \\
\frac{2j}{l_{i,j}}(t - s_{i,j}) & \text{if } t \in (s_{i,j} - \frac{l_{i,j}}{2j}, s_{i,j}), \\
0 & \text{otherwise}\n\end{cases}
$$

and

$$
\gamma_i(t,x) = \begin{cases} \frac{1}{4^i} \exp\left(\frac{-\pi \left(x - \frac{t - r_{i,j}}{l_{i,j}}\right)^2}{l_{i,j}^{2p}}\right) & \text{if } t \in (r_{i,j}, s_{i,j}) \text{ for some } j \in \mathbb{N} \\ 0 & \text{and } x \in [0, 1], \\ 0 & \text{otherwise.} \end{cases}
$$

A straightforward calculation shows that, for all i ∈ N, f (i) (t, x) ≤ 4 −i for all (t, x) ∈ [0, 1]×Ω, and thus kf (i) (t, ·)k<sup>p</sup> ≤ 4 −i for all t ∈ [0, 1]. For fixed i ∈ N we next show L p -continuity of f (i) in the first variable. We will prove it for t being approximated from the right and the rest can be proved analogously. Application of the triangle inequality and convexity of (·) <sup>p</sup> yield that, for all t, u ∈ [0, 1],

<span id="page-3-0"></span>
$$
||f^{(i)}(t,\cdot)-f^{(i)}(u,\cdot)||_p^p
$$
  
\n
$$
\leq 2^{p-1} (|\varphi_i(t)-\varphi_i(u)|^p ||\gamma_i(t,\cdot)||_p^p + |\varphi_i(u)|^p ||\gamma_i(t,\cdot)-\gamma_i(u,\cdot)||_p^p).
$$
 (1)

We now distinguish three cases. Firstly, if t ∈ (ri,j , si,j ) for some j ∈ N, then the right hand side of [\(1\)](#page-3-0) vanishes as u converges to t, since ϕ<sup>i</sup> is continuous and γi(t, ·) is L p -continuous in t. Secondly, if t = ri,j for some j ∈ N, then limu→<sup>t</sup> ϕ(u) = ϕ(t) = 0. Thus the right hand side of [\(1\)](#page-3-0) can be made arbitrarily small by chosing u close to t, since it is bounded by a positive multiple of |ϕ(u)| p , due to the uniform boundedness of γ<sup>i</sup> . Finally, if t is not contained in any of the intervals {[ri,j , si,j )}j∈N, then either f (i) (u, ·) ≡ 0 for all u in a set of the form [t, t+ǫ) or t is an accumulation point, from the right, of a subsequence ((ri,j<sup>k</sup> , si,j<sup>k</sup> ))k∈<sup>N</sup> of nonempty intervals with limk→∞ li,j<sup>k</sup> = 0. In the latter case, we can assume w.l.o.g. that (si,j<sup>k</sup> )k∈<sup>N</sup> is montonically decreasing and that u in [\(1\)](#page-3-0) is an element of (t, si,j<sup>k</sup> ). Both γ<sup>i</sup> and ϕ<sup>i</sup> are uniformly bounded and γi(t, ·) ≡ 0. The sum in [\(1\)](#page-3-0) is therefore bounded by a constant multiple of µ((t, si,j<sup>k</sup> )). As u approximates t from the right, k can be chosen larger and the bound can be made arbitrarily small, since limk→∞ si,j<sup>k</sup> = t. This shows that f (i) is L p -continuous from the right in t. Combining all three cases, f (i) (t, ·) is thus L p -continuous for all t in the compact interval [0, 1] and is therefore also uniformly continuous on K<sup>C</sup> i . We set

$$
f_t(x) = \sum_{i=1}^{\infty} f^{(i)}(t, x),
$$

which defines a function f : [0, 1] −→ L<sup>p</sup> (Ω) for which the properties stated in the theorem can be verified. To show that f is a continuous mapping of the unit interval into (L p (Ω), k · kp) we fix ε > 0, choose l ∈ N such that 2 <sup>−</sup><sup>l</sup> < ε 2 and estimate for t, u ∈ I, using the triangle inequality and Fatou's Lemma

$$
\left(\int_{\Omega} |f_u(x) - f_t(x)|^p dx\right)^{\frac{1}{p}}
$$
\n
$$
= \left(\int_{\Omega} \left|\sum_{i=1}^{\infty} \left(f^{(i)}(u,x) - f^{(i)}(t,x)\right)\right|^p dx\right)^{\frac{1}{p}}
$$
\n
$$
\leq \sum_{i=1}^{\infty} \left(\int_{\Omega} |f^{(i)}(u,x) - f^{(i)}(t,x)|^p dx\right)^{\frac{1}{p}}
$$
\n
$$
= \sum_{i=1}^l \left(\int_{\Omega} |f^{(i)}(u,x) - f^{(i)}(t,x)|^p dx\right)^{\frac{1}{p}}
$$
\n
$$
+ \sum_{i=l}^{\infty} \left(\int_{\Omega} |f^{(i)}(u,x) - f^{(i)}(t,x)|^p dx\right)^{\frac{1}{p}}
$$
\n
$$
\leq \frac{2}{4^i}
$$

The finite left hand side summand can be made smaller than <sup>ε</sup> 2 by choosing u close to t and the right hand side summand is bounded by 2−<sup>l</sup> and therefore by <sup>ε</sup> 4 . Since t and ε can be chosen arbitrarily, we conclude that L p -continuity holds for every t ∈ [0, 1].

Recalling K = S<sup>∞</sup> <sup>i</sup>=1 K<sup>i</sup> , for any t ∈ K there exists an index i for which t ∈ K<sup>i</sup> . Hence f(t, ·) is a finite sum of C∞(Ω)-functions and therefore smooth, so (ii) holds. For (i), absolute continuity only needs to be verified for t ∈ KC. Clearly all f (i) (t, ·) are absolutely continuous and so are the finite sums P<sup>k</sup> <sup>i</sup>=1 f (i) (t, ·). For existence of the derivative <sup>d</sup> dx f(t, x), we note that

$$
\frac{\mathrm{d}}{\mathrm{d}x} \frac{1}{4^i} \exp\left(\frac{-\pi \left(x - \frac{t - r_{i,j}}{l_{i,j}}\right)^2}{l_{i,j}^{2p}}\right)
$$
\n
$$
= -\frac{1}{4^i} \frac{2\pi}{l_{i,j}^{2p}} \left(x - \frac{t - r_{i,j}}{l_{i,j}}\right) \frac{1}{4^i} \exp\left(\frac{-\pi \left(x - \frac{t - r_{i,j}}{l_{i,j}}\right)^2}{l_{i,j}^{2p}}\right),
$$

which is still summable in i. Hence the first derivative of f<sup>t</sup> exists and it is continuous for all t ∈ K<sup>C</sup> a.e. on Ω, which implies absolute continuity.

The next step is to show that (A) holds. We do so by constructing for every t ∈ K a sequence (tn)n∈<sup>N</sup> such that f(tn, ·) has the desired property. We observe first, that if we fix i, j ∈ N, x ∈ [ 1 j , 1− 1 j ] and set τ<sup>x</sup> = ri,j +xli,j , then continuity of f(τx, ·) implies that the sets I<sup>x</sup> = {y : f(τx, y) > 2 3 4 <sup>−</sup>1} are open. The defintions of f (i) and f imply that f(τx, x) ≥ 4 −i , thus x ∈ I<sup>x</sup> and S x I<sup>x</sup> is an open cover of the interval [ <sup>1</sup> j , 1 − 1 j ]. By compactness, we can find a finite subcover, i.e. there is an integer k and a k-tuple τ = τ 1 , τ <sup>2</sup> , ..., τ <sup>k</sup> , where τ <sup>l</sup> ∈ (ri,j , si,j ), for 1 ≤ l ≤ k, with the property that for every x ∈ [ 1 j , 1− <sup>1</sup> j ] there exists an index l(x) ∈ {1, . . . , k} such that f (i) (τ l(x) , x) > 2 3 4 −i .

Now let t ∈ K be fixed and let i = i(t) = min{j ∈ N : t ∈ Kj}. Since K<sup>i</sup> is nowhere dense, there exists a subsequence of intervals (ri,j<sup>n</sup> , si,j<sup>n</sup> ) n∈N indexed by (jn) = (jn(t)) with endpoints ri,j<sup>n</sup> , si,j<sup>n</sup> converging to t. Thus for each one of the intervals (ri,j<sup>n</sup> , si,j<sup>n</sup> ) we can apply the above argument and find k = k(n) ∈ N and a k-tuple τ (n) = τ 1 (n), τ <sup>2</sup> (n), ..., τ <sup>k</sup> (n) , such that τ l (n) ∈ (ri,j<sup>n</sup> , si,j<sup>n</sup> ), 1 ≤ l ≤ k, and for every x ∈ [ 1 jn(t) , 1 − 1 jn(t) ] there is l = l(x, n) ∈ {1, . . . , k} satisfying f (i) (τ l (n), x) > 2 3 4 −i . Note also thatf (i) (ri,j<sup>n</sup> , ·) = f (i) (si,j<sup>n</sup> , ·) ≡ 0.

Finally, we consider now the sequence (tm)m∈<sup>N</sup> obtained by concatenating the k(n) + 2-tuples (ri,j<sup>n</sup> , τ <sup>1</sup> (n), τ <sup>2</sup> (n), . . . , τ <sup>k</sup> (n), si,j<sup>n</sup> ) in increasing order in n. Fix x<sup>0</sup> ∈ [0, 1], n<sup>0</sup> ∈ N and ε = 1 6 4 −i . Since t /∈ K<sup>h</sup> for any h < i we know that the functions f (h) (τ, ·) are uniformly continuous around t for every h < i, i.e there is a δ > 0 such that Pi−<sup>1</sup> <sup>h</sup>=1 f (h) (t, ·) − f (h) (τ, ·) < 1 4 i for every τ with |t − τ | ≤ δ. Since t<sup>n</sup> converges to t there is n<sup>1</sup> ∈ N such that for every n ∈ N with n > n<sup>1</sup> we have |t<sup>n</sup> −t| < δ and by construction of t<sup>n</sup> there are n, m > max{n0, n1} such that f (i) (tm, x0) − f (i) (tn, x0) > 2 3 4 −i . For these n, m we have

$$
f(t_m, x) - f(t_n, x) = \sum_{h=1}^{\infty} (f^{(h)}(t_m, x) - f^{(h)}(t_n, x))
$$
  
\n
$$
= \sum_{h=1}^{i-1} (f^{(h)}(t_m, x) - f^{(h)}(t_n, x)) + f^{(i)}(t_m, x) - f^{(i)}(t_n, x)
$$
  
\n
$$
+ \sum_{h=i}^{\infty} (f^{(h)}(t_m, x) - f^{(h)}(t_n, x))
$$
  
\n
$$
\geq \frac{2}{3 \cdot 4^i} - \frac{1}{4 \cdot 4^i} - \sum_{h=i}^{\infty} \frac{1}{4^h} = \frac{2}{3 \cdot 4^i} - \frac{1}{4 \cdot 4^i} - \frac{1}{4 \cdot 4^i} = \varepsilon,
$$

so f(tn, x) n∈N is not Cauchy.

# 3. Optimality of the conditions in Theorem [2.1](#page-2-0)

In this section we show that Theorem [2.1](#page-2-0) is sharp in two senses. Firstly, the following argument shows that K in Theorem [2.1](#page-2-0) cannot be non-meager, thus the example is best possible in the sense of Baire category. In particular, we cannot obtain divergence on the whole of I.

Proposition 3.1. Let f be a continuous map of [0, 1] into L p (Ω). If f<sup>t</sup> is continuous for every t, then there is a comeagre subset T ⊂ [0, 1] such that for any t ∈ I and any sequence (tn)n∈<sup>N</sup> with limit t

$$
\lim_{n \to \infty} f_{t_n}(x) = f_t(x) \quad \text{for all } x \in \Omega.
$$

Proof. Define for 0 < q < p the sets

$$
T_{pq} = \{ t \in [0,1] : \exists x(t) \in \Omega \text{ with } f_t(x(t)) < q < p < \limsup_{s \to t} f_s(x(t)) \}.
$$

We first want to prove by contradiction that Tpq are nowhere dense sets. Let us assume that there are q < p such that Tpq is dense in an open ball B(t0, r0), with t<sup>0</sup> ∈ Tpq. We then have that no open subset S of the ball B(t0, r0) is disjoint from Tpq.

We start by demonstrating that for any such S and any choice of δ > 0 and sufficiently small ρ > 0, there exist t ∈ S and r < ρ such that for every s ∈ B(t, r) we have ω(s, δ) > q − p, where ω(s, δ) = sup{|fs(x) − fs(y)| : |x − y| < δ}.

By assumption, there is t<sup>1</sup> ∈ S ∩Tpq, hence there is a point x(t1) ∈ Ω with ft<sup>1</sup> (x(t1)) < q < p < lim sups→t<sup>1</sup> fs(x(t1)). Since ft<sup>1</sup> (x(t1)) < q, there exists 0 < δ<sup>1</sup> < δ such that ft<sup>1</sup> (y) < q, for all y ∈ B(x(t1), δ1), by continuity of ft<sup>1</sup> . Moreover, f is L p -continuous, hence there is r<sup>1</sup> > 0 such that for every s ∈ B(t1, r1), there exists x u (s) ∈ B(x(t1), δ1) for which fs(x u (s)) < q. We choose now a second point t<sup>2</sup> ∈ B(t1, r1) with ft<sup>2</sup> (x(t1)) > p and by continuity of ft<sup>2</sup> we can fix δ<sup>2</sup> > 0 such that ft<sup>2</sup> (y) > p for all y ∈ B(x(t1), δ2). Using L p -continuity again, we can find r<sup>2</sup> > 0 such that for every s ∈ B(t2, r2) there exists x l (s) ∈ B(x(t2), δ2) with fs(x l (s)) > p. The above assertion now holds for the choices t = t2, r = min{r1, r2,sup{|t<sup>2</sup> −s|, s ∈ ∂B(t1, r1)}} and δ = δ1.

Applying the above construction to vanishing sequences (ρn)n∈N,(δn)n∈N, we can find points t<sup>n</sup> and radii r<sup>n</sup> < ρ<sup>n</sup> with B(tn+1, rn+1) ⊂ B(tn, rn) and ω(s, δn) > q − p for every s ∈ B(tn, rn). Since limn→∞ r<sup>n</sup> = 0, we have that limn→∞ t<sup>n</sup> = t<sup>∞</sup> for some t<sup>∞</sup> ∈ [0, 1]. Moreover, we have that ω(t∞, δn) > p − q for every n ∈ N, which contradicts the assumption that ft is continuous for every t ∈ [0, 1], hence our initial assumption that Tpq is not nowhere dense cannot be true.

We can apply the same argument to the sets

$$
S_{pq} = \{t : \exists x(t) \in \Omega \text{ such that } f_t(x(t)) > q > p > \liminf_{s \to t} f_s(x(t))\},\
$$

and the comeager set T mentioned in the theorem is the complement of

$$
\bigcup_{p,q \in \mathbb{Q}} (T_{pq} \cup S_{pq}).
$$

Secondly, we can prove that we cannot make the regularity requirement (i) in Theorem [2.1](#page-2-0) stronger.

<span id="page-7-0"></span>Proposition 3.2. Let f be a continuous mapping of [0, 1] into L p (Ω) ∩ W1,q(Ω), where 1 ≤ p < ∞ and q > 1. Then there is an open dense set T ⊂ [0, 1] such that for all t ∈ T and any sequence (tn)n∈<sup>N</sup> with limit t,

$$
\lim_{n \to \infty} f_{t_n}(x) = f_t(x) \text{ for all } x \in \Omega.
$$

For the proof of Proposition [3.2,](#page-7-0) we need to establish an auxiliary lemma about the relation between L p -continuity and pointwise continuity.

<span id="page-7-2"></span>Lemma 3.3. Let f be L p -continuous and S ⊂ [0, 1] an open interval. If f<sup>t</sup> ∈ W1,q(Ω) for some q > 1 and {f<sup>t</sup> ;t ∈ S} is bounded in W1,q(Ω), then f is pointwise continuous for every t ∈ S, i.e. limn→∞ ft<sup>n</sup> (x) = ft(x) for every sequence (tn)n∈<sup>N</sup> converging to t and every x ∈ Ω.

Proof. Fix ε > 0. Since f<sup>t</sup> ∈ W1,q(Ω), invoking the Sobolev Imbedding Theorem (see, e.g., [\[1,](#page-12-0) Part II of Theorem 4.12 with m = n = 1, j = 0, n = 1, p = q and λ = 1 − 1/q]), we can assume that f<sup>t</sup> is H¨older-continuous with exponent q ′ = 1 − 1 q and constant C<sup>t</sup> > 0 independent of t, i.e. we have for all t ∈ S,

<span id="page-7-1"></span>
$$
|f_t(x) - f_t(y)| \le C_t |x - y|^{q'}, \quad \text{for all } x, y \in \Omega.
$$
 (2)

The proof of this part of the Sobolev Imbedding Theorem (see, e.g., [\[1,](#page-12-0) p. 100, proof of Lemma 4.28]) demonstrates that the H¨older constant C<sup>t</sup> is bounded by a constant multiple of kftk1,q, using the boundedness of {f<sup>t</sup> ;t ∈ S} we can therefore assume that [\(2\)](#page-7-1) holds uniformly on S with C<sup>t</sup> ≡ C. Now, fixing x ∈ Ω and any s, t ∈ S and then applying the triangle inequality and [\(2\)](#page-7-1), we obtain, for all y ∈ Ω,

$$
|f_t(x) - f_s(x)| \le |f_t(x) - f_t(y)| + |f_t(y) - f_s(y)| + |f_s(x) - f_s(y)|
$$
  
$$
\le 2C|x - y|^{q'} + |f_t(y) - f_s(y)|.
$$

Integrating both sides in y on the interval B(x, η 2 ) = (x − η 2 , x − η 2 ), where 0 < η < min{ ε 2 , 2 <sup>q</sup>p′ <sup>ε</sup> 4C }, yields

$$
\left(\int_{B(x,\frac{\eta}{2})} |f_t(x) - f_s(x)|^p dy\right)^{\frac{1}{p}} \le \left(\int_{B(x,\frac{\eta}{2})} (2C|x - y|^{q'})^p dy\right)^{\frac{1}{p}} + \left(\int_{B(x,\frac{\eta}{2})} |f_t(y) - f_s(y)|^p dy\right)^{\frac{1}{p}}
$$

and thus

$$
\eta^{\frac{1}{p}}|f_t(x) - f_s(x)| \leq \eta^{\frac{1}{p}}\varepsilon + \|f_t - f_s\|_p.
$$

This implies

$$
|f_t(x) - f_s(x)| \le \frac{\varepsilon}{2} + \frac{\|f_t - f_s\|_p}{\eta^{\frac{1}{p}}}
$$

and using L p continuity of f we derive that

$$
|f_t(x) - f_s(x)| \le \varepsilon,
$$

for all s sufficiently close to t.

We are now ready to prove Proposition [3.2.](#page-7-0)

Proof of Proposition [3.2.](#page-7-0) Let f<sup>t</sup> ∈ W1,q(Ω), q > 1 for every t ∈ [0, 1]. Since ft is absolutely integrable for all t, we can expand each f<sup>t</sup> into a Fourier series

$$
f^{(m)}(t,x) = \sum_{n=-m}^{n=m} c_n(t)e^{in\pi(x-\frac{1}{2})}
$$

for which we have limm→∞ f (m) (t, ·) = f<sup>t</sup> , w.r.t. k · k1,q, see e.g. [\[2,](#page-12-1) p. 78]. Using L p -continuity of f we obtain that the coefficients cn(t) = R Ω f<sup>t</sup> exp − inπ(· − 1 2 ) dλ are continuous in t and furthermore g (m) (t) = kf (m) (t, ·)k1,q is a continuous function. Hence g(t) = kftk1,q can be represented as a limit of continuous functions and therefore the set of points of continuity of g is comeager Gδ, see e.g. [\[3,](#page-12-2) Theorem 7.3]. This implies that g(t) is locally bounded on an open dense set. Thus the assumptions of Lemma [3.3](#page-7-2) are satisfied and its application yields the statement of the theorem.

# 4. Construction of the second example

If the requirement (i) in Theorem [2.1](#page-2-0) is dropped, then it is possible to create an example where we not only have everywhere pointwise divergence, but also divergence is obtained on every subset of I with positive measure.

<span id="page-8-0"></span>Theorem 4.1. There exists a continuous function f : [0, 1] −→ L<sup>p</sup> (Ω), such that for all measurable sets T ⊂ [0, 1] with µ(T) > 0 and every t ∈ T with Lebesgue density one, there exists a sequence (tn)n∈<sup>N</sup> ⊂ T with limn→∞ t<sup>n</sup> = t and λ(At) = 1, where A<sup>t</sup> = {x : limn→∞ ft<sup>n</sup> (x) 6= ft(x)}

Proof. Let {qm, m ∈ N} ⊂ I \ {0} be dense and assign to each q<sup>m</sup> a sequence (sm,k)k∈<sup>N</sup> defined by

$$
s_{m,k} = q_m - \frac{1}{k + r(m)}
$$
, where  $r(m) = \min \{ r : q_m - \frac{1}{r} \ge 0 \}.$ 

Setting Sm,k = [sm,k, sm,k+1], we note that the vanishing intervals {Sm,k}k∈<sup>N</sup> partition [0, qm]. To partition the spacial domain, set

$$
b_{m,k}(t) = \max\left\{0, \frac{t - s_{m,k}}{s_{m,k+1} - s_{m,k}} - \frac{s_{m,k+1} - t}{4^{k+m}}\right\}
$$

and

$$
c_{m,k}(t) = \min\left\{1, \frac{t - s_{m,k}}{s_{m,k+1} - s_{m,k}} + \frac{t - s_{m,k}}{4^{k+m}}\right\},\,
$$

assigning to every Sm,k (possibly empty) intervals Im,k(t) = [bm,k(t), cm,k(t)] of maximal length µ(Sm,k) × 4 <sup>−</sup>(k+m) which emerge, move through Ω at linear speed µ(Sm,k) <sup>−</sup><sup>1</sup> and vanish as t ∈ I varies. Denoting by χ<sup>A</sup> the characteristic function of a set A, we define functions f (m,k) (t, ·) : Ω −→ L p (Ω) by

$$
f^{(m,k)}(t,x) = 2^{m} \chi_{S_{m,k}}(t) \chi_{I_{m,k}(t)}(x).
$$

These functions satisfy kf (m,k) (t, ·)k<sup>p</sup> ≤ 1 2m+<sup>k</sup> for all t ∈ I and one also checks easily that f (m,k) (t, ·) is Lp-continuous in the first variable for all t ∈ I. We can now set

$$
f_t(x) = \sum_{k,m=1}^{\infty} f^{(m,k)}(t,x)
$$

and the limit f is well defined in L p , since f (m,k) (t, x) ≥ 0 and

$$
\sum_{m,k=1}^{\infty} \|f^{(m,k)}(t,\cdot)\|_{p} < \infty.
$$

Let T ⊂ I be of positive measure λ(T) > 0, and let t ∈ T have density 1 with respect to T. We inductively construct a sequence (tn)n∈<sup>N</sup> ⊂ T with limn→∞ t<sup>n</sup> = t such that

$$
\limsup_{n \to \infty} f(t_n, x) = \infty \neq f(t, x), \text{ for almost all } x \in [0, 1].
$$

To this end, let (γi)i∈<sup>N</sup> ⊂ (0, 1) be strictly increasing with limit 1 and initiate the construction at stage i = 0 with arbitrary t<sup>0</sup> ∈ T and n<sup>0</sup> = m<sup>0</sup> = 0. Assume now, we have completed stages 0, . . . , i − 1 of the construction, i.e. we have chosen the initial members of the sequence t0, . . . , tn<sup>1</sup> , . . . , tn<sup>2</sup> , . . . , tni−<sup>1</sup> . Since t is a point of density 1 in T, we can fix ρ<sup>i</sup> ∈ (0, t) \ { <sup>1</sup> l ; l ∈ N} such that for every ρ < ρ<sup>i</sup> ,

<span id="page-9-0"></span>
$$
\mu(T \cap (t - \rho, t]) \ge \gamma_i \rho. \tag{3}
$$

Let now l ∈ N be the unique integer with <sup>1</sup> <sup>l</sup>+1 < ρ<sup>i</sup> < 1 l and choose m<sup>i</sup> > mi−<sup>1</sup> such that

<span id="page-9-1"></span>
$$
t - \rho_i + \frac{1}{l+1} < q_{m_i} < t \text{ and } t - q_{m_i} < \frac{\gamma_i}{l+1}.\tag{4}
$$

By [\(3\)](#page-9-0) and the first inequality of [\(4\)](#page-9-1), we have

$$
\mu\left(T\cap\left[q_{m_i}-\frac{1}{l+1},q_{m_i}\right]\right) \geq \mu\left(T\cap\left[q_{m_i}-\frac{1}{l+1},t\right]\right) - (t-q_{m_i})
$$
$$
\geq \gamma_i(t-q_{m_i}+\frac{1}{l+1}) - (t-q_{m_i}),
$$

and by the second inequality of [\(4\)](#page-9-1) we get

$$
\mu\left(T\cap\left[q_m-\frac{1}{l+1},q_m\right]\right)\geq\frac{\gamma_i^2}{l+1}.
$$

Since the intervals {Smi,k; k ∈ N} partition [qm<sup>i</sup> − 1 <sup>l</sup>+1 , qm<sup>i</sup> ], there must be k ∈ N such that µ(Smi,k ∩ T) ≥ (smi,k+1 − smi,k)γ 2 i . We denote the index of this interval by k<sup>i</sup> .

For z > 0 and J ⊂ Ω, we write zJ = {za; a ∈ I} and let also intJ denote the interior of a set J. Note that if r ∈ intSm,k, then r − sm,k ∈ (sm,k+1 − sm,k)intIm,k(r). Using this fact and the scale and translation invariance of Lebesgue measure, we obtain

<span id="page-10-0"></span>
$$
\lambda \left( \bigcup_{r \in S_{m_i, k_i} \cap T} \text{int} I_{m_i, k_i}(r) \right)
$$
\n
$$
= \frac{\lambda \left( \bigcup_{r \in T \cap \text{int} S_{m_i, k_i}} (s_{m_i, k_i+1} - s_{m_i, k_i}) \text{int} I_{m_i, k_i}(r) \right)} (s_{m_i, k_i+1} - s_{m_i, k_i})
$$
\n
$$
\geq \frac{\lambda \left( \bigcup_{r \in T \cap \text{int} S_{m_i, k_i}} \{r - s_{m, k}\} \right)}{s_{m_i, k_i+1} - s_{m_i, k_i}} = \frac{\lambda \left( \bigcup_{r \in (S_{m_i, k_i} \cap T)} \{r\} \right)}{s_{m_i, k_i+1} - s_{m_i, k_i}}
$$
\n
$$
= \frac{\mu(S_{m_i, k_i} \cap T)}{s_{m_i, k_i+1} - s_{m_i, k_i}} \geq \gamma_i^2.
$$
\n(5)

Since Lebesgue measure is inner regular, we can thus find a compact set K ⊂ S r∈Smi ,ki ∩T intImi,k<sup>i</sup> (r) with

$$
\lambda(K) \geq \gamma_i \lambda \left( \bigcup_{r \in S_{m_i,k_i} \cap T} \text{int} I_{m_i,k_i}(r) \right),\,
$$

and the compactness of K allows us to select tni−1+1, . . . , tn<sup>i</sup> from Smi,kmi ∩T such that

$$
\lambda \left( \bigcup_{r \in \{t_{n_{i-1}+1}, \dots, t_{n_i}\}} \text{int} I_{m_i, k_i}(r) \right) \geq \gamma_i \lambda \left( \bigcup_{r \in S_{m_i, k_i} \cap T} \text{int} I_{m_i, k_i}(r) \right)
$$

and therefore, combined with [\(5\)](#page-10-0),

λ x : ftni+<sup>j</sup> (x) ≥ 2 m<sup>i</sup> for at least one j ∈ {1, 2, .., n<sup>i</sup> − ni−1} ≥ γ 3 i ,

which concludes the construction and finishes the proof, since (γi)i∈<sup>N</sup> converges to 1.

#### 5. Necessity of discontinuity of f<sup>t</sup> in Theorem [4.1](#page-8-0)

In this section we prove our final and most general result, namely that dropping continuity with respect to x for almost every t is essential in order to be able to construct an extremely irregular curve like in Theorem [4.1.](#page-8-0) We show, that if the function f<sup>t</sup> is continuous for every t, then a refined version of Lusin's theorem in 2 variables holds.

<span id="page-11-0"></span>Theorem 5.1. Let f : [0, 1] × Ω −→ R be Borel measurable such that f<sup>t</sup> is a continuous function for µ-a.e t ∈ Ω. Then, for every ε > 0, there is a set T<sup>ε</sup> ⊂ [0, 1] with µ(T C ε ) < ε such that the restriction

$$
f_{|T_{\varepsilon}\times\Omega}:(T_{\varepsilon}\times\Omega,|\cdot|\otimes|\cdot|)\longrightarrow(\mathbb{R},|\cdot|)
$$

is a continuous function.

Note that in Theorem [5.1](#page-11-0) only the fact that f is a measurable function in [0, 1] × Ω is needed and there is no L p -continuity assumed. However, as L p -continuity guarantees that f is a measurable function in [0, 1] × Ω, the claimed necessity in Theorem [4.1](#page-8-0) is a straightforward consequence.

Corollary 5.2. Let f be a continuous function from [0, 1] to L p (Ω). If f<sup>t</sup> ∈ L p (Ω) is continuous for µ-a.e t ∈ [0, 1], then the assertion in Theorem [5.1](#page-11-0) holds.

Before we proceed with the proof of Theorem [5.1](#page-11-0) we would like to point out the difference between Theorem [5.1](#page-11-0) and the classical result of Lusin. In Lusin's theorem an arbitrarily small set of I × Ω is removed in order to establish continuity on the remainder. In our case the stronger assumption of continuity with respect to one variable entails the information that this small set is of the form T C <sup>ε</sup> × Ω, so it is only necessary to remove a "slice" in the space-time domain.

For the proof of Theorem [5.1](#page-11-0) we also need the following preliminary result.

<span id="page-11-2"></span>Lemma 5.3. Let F = {f<sup>t</sup> ;t ∈ I} be a family of continuous functions. Then, for every ε > 0, there is a set S<sup>ε</sup> ⊂ I, such that µ(S C ε ) < ε, with the property that F<sup>ε</sup> := {f<sup>t</sup> ;t ∈ Sε} is equicontinuous.

Proof. Let ω<sup>δ</sup> denote the δ-oscillation functional,

<span id="page-11-1"></span>
$$
\omega_{\delta}(g) := \sup\{|g(x) - g(y)| : |x - y| < \delta\} \tag{6}
$$

and set ωn(t) = ω <sup>1</sup> n (ft) on F. We have limn→∞ ωn(t) = 0 for every t, since all f<sup>t</sup> are continuous. From Egorov's Theorem (see, e.g. [\[3,](#page-12-2) Theorem 8.3]) we deduce that for every ε > 0, there exists a set S<sup>ε</sup> with µ(S C ǫ ) < ε such that ωn<sup>|</sup> <sup>S</sup><sup>ε</sup> converges uniformly. Now, fixing ε > 0, we wish to show that the uniform convergence of ω<sup>n</sup> to zero implies equicontinuity of Fε.

Let η > 0. Since limn→∞ ω<sup>n</sup> = 0 uniformly on Sε, there exists n<sup>0</sup> ∈ N such that for all n > n0,

ω<sup>n</sup> < η for every t ∈ Sε.

Hence, choosing δ = 1 n0 in [\(6\)](#page-11-1) and evaluating ω<sup>δ</sup> on Fε, we obtain

$$
\sup\{|f_t(x) - f_t(y)| : |x - y| < \delta\} < \eta.
$$

This means F<sup>ε</sup> is equicontinuous, since η was choosen arbitrarily.

From Lemma [5.3](#page-11-2) and Lusin's Theorem we can finally deduce Theorem [5.1.](#page-11-0)

Proof of Theorem [5.1.](#page-11-0) Since f is Borel measurable, we have that f x , where f x (t) := f(t, x), is a Borel measurable function for every x ∈ [0, 1]. We can therefore choose a dense countable subset X = {xn; n ∈ N} ⊂ Ω such that f <sup>x</sup><sup>n</sup> is Borel measurable for every n ∈ N. By Lusin's theorem, for every function f <sup>x</sup>n, n ∈ N, and any fixed small parameter ε there is a set U<sup>n</sup> ⊂ [0, 1] such that µ((Un) <sup>C</sup>) < ε <sup>2</sup>n+1 and f xn |Un is continuous. Now define V <sup>ε</sup> 2 := T<sup>∞</sup> <sup>n</sup>=1 U<sup>n</sup> and apply Lemma [5.3](#page-11-2) to the family {f(t, ·);t ∈ [0, 1]} to obtain a set S<sup>ε</sup> 2 such that {f(t, ·);t ∈ S<sup>ε</sup> 2 } is equicontinuous. Now, T<sup>ε</sup> := S<sup>ε</sup> 2 ∩ V <sup>ε</sup> 2 , is the desired set. It remains to prove that the restriction f|Tε×<sup>Ω</sup> is a continuous function, and we are going to use the sequential definition of continuity to do so.

Let (t0, y0) ∈ T<sup>ε</sup> × Ω. Let also a sequence (tn, yn) ∈ T<sup>ε</sup> × Ω such that limn→∞(tn, yn) = (t0, y0). Finally let η > 0. By equicontinuity of {f(t, ·);t ∈ Tε} there exists a δ > 0 such that

$$
|f(t,y') - f(t,y)| < \frac{\eta}{3} \text{ for all } t \in T_{\epsilon} \text{ and } y', y \in \Omega \text{ with } |y'-y| < \delta.
$$

By density of X in Ω, there exists a x<sup>0</sup> such that |y0−x0| < δ 2 . Since y<sup>n</sup> → y0, we can find a n<sup>1</sup> such that |y<sup>n</sup> − y0| < <sup>δ</sup> 2 and thus |y<sup>n</sup> − x0| < δ, ∀n ∈ N with n > n1. Furthermore by continuity of f(·, x0) in T<sup>ǫ</sup> there exists a n<sup>2</sup> such that ∀n > n<sup>2</sup> we have kf(tn, x0) − f(t0, x0)k < η 3

Now, for n > max{n1, n2} we have

$$
|| f(t_n, y_n) - f(t_0, y_0) || \le || f(t_n, y_n) - f(t_n, x_0) || + || f(t_n, x_0) - f(t_0, x_0) ||
$$
  
+ 
$$
|| f(t_0, x_0) - f(t_0, y_0) || \le \frac{\eta}{3} + \frac{\eta}{3} + \frac{\eta}{3} = \eta
$$

#### References

- <span id="page-12-0"></span>[1] R.A. Adams, J.J. Fournier, Sobolev spaces, 2nd ed., Pure and Applied Mathematics (Amsterdam), 140. Elsevier/Academic Press, Amsterdam, 2003.
- <span id="page-12-2"></span><span id="page-12-1"></span>[2] N.K. Bary, A treatise on trigonometric series, Pergamon, Oxford, 1964.
- [3] J.C. Oxtoby, Measure and category. A survey of the analogies between topological and measure spaces, Graduate Texts in Mathematics, Vol. 2, Springer-Verlag, New York-Berlin, 1971.
- [4] W. Rudin, Real and complex analysis, 3rd ed., McGraw-Hill, New York, 1987.