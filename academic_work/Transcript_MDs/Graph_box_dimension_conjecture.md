# ON A CONJECTURE REGARDING THE UPPER GRAPH BOX DIMENSION OF BOUNDED SUBSETS OF THE REAL LINE

Abstract. Let X ⊂ R be a bounded set; we introduce a formula that calculates the upper graph box dimension of X (i.e. the supremum of the upper box dimension of the graph over all uniformly continuous functions defined on X). We demonstrate the strength of the formula by calculating the upper graph box dimension for some sets and by giving an "one line" proof, alternative to the one given in [\[1\]](#page-12-0), of the fact that if X has finitely many isolated points then its upper graph box dimension is equal to the upper box dimension plus one. Furthermore we construct a collection of sets X with infinitely many isolated points, having upper box dimension a taking values from zero to one while their graph box dimension takes any value in [max{2a, 1}, a + 1], answering this way, negatively to a conjecture posed in [\[1\]](#page-12-0).

## 1. Introduction

Let X be a set, let also Cu(X) be the set of all uniformly continuous functions on X equipped with the uniform norm k · k<sup>∞</sup> . In [\[1\]](#page-12-0), the concept of the upper graph box dimension was introduced, i.e.

$$
\overline{dim}_{gr,B}(X) = \sup_{f \in C_u(X)} \overline{dim}_B(gradph(f))
$$

and it was proved, that a typical element (in the sense of Baire) in the set Cu(X), has a graph with upper box dimension equal to the upper graph box dimension of the set. To put it in another way, it was proved that a typical element in Cu(X) has a graph with upper box dimension as high as allowed by the set. The proof given, made no use of any properties of the set X. It was in the lines of "if the set X can accommodate a function having graph with upper box dimension bigger or equal than b, then a typical function will do as well". In [\[1\]](#page-12-0), it was proved that

<span id="page-0-0"></span>
$$
1 \le \overline{\dim}_{gr,B}(X) \le \overline{\dim}_B(X) + 1 \tag{1}
$$

and for the case where X has finitely many isolated points, it was proven that

$$
\overline{dim}_{gr,B}(X) = \overline{dim}_B(X) + 1,
$$

while the general case remained open. It was conjectured that the upper graph box dimension of X is either equal to the upper box dimension of X plus one or just one.

In this paper, we introduce a formula that calculates the upper graph box dimension of a set X. By using this formula we refine inequality [1,](#page-0-0) we give a straightforward alternative proof of the fact, that if X has finitely many isolated points then its upper graph box dimension is equal to the upper box dimension plus one and even more we use the formula to calculate the upper graph box dimension for a collection of natural sets. We conclude by constructing a collection of sets having all possible values allowed by the refined inequality, and disproving this way the conjecture in [\[1\]](#page-12-0).

Remark 1. In [\[4\]](#page-13-0) and [\[3\]](#page-13-1), it was respectively proved that when X = [0, 1], a typical function in Cu(X) has a graph with Hausdorff dimension equal to 1 and packing dimension equal to 2. Although we are not aware of any extensions of these results in general sets X, we strongly believe that for a typical element in Cu(X) we always have dimH(graph(f)) = dim<sup>H</sup> (X) and dimp(graph(f)) = dimp(X)+ 1, and therefore a concept like the upper graph dimension is useful only for the box dimension.

For simplicity we will assume that X ⊂ [0, 1]. We start by recalling the definition of the upper box dimension of subsets of R d . For δ > 0, let

$$
\mathcal{Q}_{\delta}^{d} = \left\{ \prod_{i=1}^{d} [n_i \delta, (n_i + 1)\delta] \middle| n_1, \dots, n_d \in Z \right\}
$$
 (2)

denote the standard <sup>δ</sup>−grid in <sup>R</sup> d , and for a subset X of R <sup>d</sup> we write

$$
N_{\delta}(X) = \left| \left\{ Q \in \mathcal{Q}_{\delta}^{d} | Q \cap X \neq 0 \right\} \right| \tag{3}
$$

for the number of cubes in <sup>Q</sup><sup>d</sup> δ that intersects X. The upper box dimension of X is now defined by

$$
\overline{\dim}_B(X) = \limsup_{\delta \to 0} \frac{\log N_{\delta}(X)}{-\log \delta}.
$$
\n(4)

The reader is referred to Falconer's [\[2,](#page-13-2) p. 42] for a thorough discussion on the properties of the box dimension. One property that we are going to use here, regards the alternative type of boxes that can be used in the definition. More specifically, we will be working with δ-meshes of disjoint cubes of the form [m1δ,(m<sup>1</sup> + 1)δ) × [m2δ,(m<sup>2</sup> + 1)δ).

Also note that ([\[2\]](#page-13-2)) it is enough to consider limits as δ tends to 0 through any decreasing sequence δ<sup>k</sup> - as long as δk+1 ≥ cδk. Taking δ<sup>k</sup> = 1 <sup>k</sup> we can log N 1 k (F)

work with limits of log k as <sup>k</sup> <sup>∈</sup> <sup>N</sup> tends to infinity.

For f ∈ Cu(X), we will write graph(f) to denote the graph of f, ie.

$$
\mathrm{graph}(f) = \{(x, f(x)) | x \in X\}.
$$

With a slight abuse of notation, we are going to write Nδ(f) instead of Nδ(graph(f)).

With P(X) we are going to define all the polygonic functions restricted in X.

Finally we define the sequence

$$
g_m(X) = \sum_{k=1}^m \min\{m, \#(X \cap [\frac{k-1}{m}, \frac{k}{m}])\}.
$$

## 2. equivalence of definitions and applications of the formula

In the first part, we are going to prove that we can use g<sup>m</sup> to calculate the upper graph box dimension of a set. More specifically we have

#### <span id="page-2-2"></span>Theorem 2.

$$
\overline{dim}_{gr,B}(X) = \limsup_{m \to \infty} \frac{\log(g_m)}{\log(m)}.
$$

Afterwards we are giving an alternative proof to the fact, that if X has finitely many isolated points, then

$$
\overline{dim}_{gr,B}(X) = \overline{dim}_B(X) + 1.
$$

We conclude the section, by providing some natural examples of sets where g<sup>m</sup> can be used to calculate their upper graph box dimension.

<span id="page-2-1"></span>Lemma 1. Let f ∈ P(X), δ<sup>0</sup> > 0, p > 0 and ǫ > 0. It exists δ<sup>1</sup> : δ<sup>0</sup> > δ<sup>1</sup> > 0 and g ∈ P(X) with g > 0, such that ||g||<sup>∞</sup> < p and

$$
\frac{\log N_{\delta_1}(g+f)}{-\log \delta_1} \ge \limsup_{m \to \infty} \frac{\log g_m}{\log m} - \epsilon
$$

Proof. If a = lim sup m→∞ log g<sup>m</sup> log m then there exists a subsequence gm<sup>k</sup> with m<sup>k</sup> →

<sup>∞</sup> such that <sup>a</sup> = lim <sup>m</sup>k→∞ log gm<sup>k</sup> log m<sup>k</sup> . That means that ∀ǫ > 0 there exists a k<sup>0</sup> ∈ N such that

<span id="page-2-0"></span>
$$
\forall m_k > m_{k_0} \Rightarrow |a - \frac{\log g_{m_k}}{\log m_k}| < \frac{\epsilon}{2}.\tag{5}
$$

Let now arbitrary δ > 0 of the form <sup>1</sup> <sup>m</sup>. We will construct a function <sup>g</sup>δ,p <sup>∈</sup> <sup>P</sup>(X) as follows. For every interval <sup>I</sup><sup>k</sup> = [ (k−1) n , k m ] we select n<sup>k</sup> = min{mp, #X ∩ Ik)} elements of I<sup>k</sup> ∩ X, we will call b k i , i ∈ {1, ..., nk}. We do this ∀k : I<sup>k</sup> ∩ X 6= ∅ and we end up with a finite subset of X. For every b k <sup>i</sup> we define a point (b k i , g1(b k i )) in a way that, no two points occupy the same box and g1(b k i ) < p for all k ∈ {1, ..., m}, i ∈ {1, ..., nk}. If we consider g<sup>1</sup> to be the polygonal line joining all (b k i , g1(b k i )) then gδ,p is the restriction of g<sup>1</sup> in X. From its construction ||gδ,p|| < p and Nδ(gδ,p) ≥ P<sup>m</sup> <sup>k</sup>=1 min{pm, #X ∩ [ (k−1) m , k m ]}.

Since f is polygonic it satisfies the assumptions of lemma [4](#page-12-1) for some constant c, and therefore from lemmas [3](#page-11-0) and [4](#page-12-1) we have that Nδ(f + gδ,p) ≥ Nδ(gδ,p) 2c .

We have:

$$
N_{\delta}(f + g_{\delta, p}) \ge \frac{N_{\delta}(g_{\delta, p})}{2c} \ge c' \sum_{k=1}^{m} \min\{pm, \#(X \cap [(k-1)/m, k/m])\}
$$
  
$$
\ge c'' \sum_{k=1}^{m} \min\{m, \#(X \cap [(k-1)/m, k/m])\}.
$$

Where c ′′ depends on p. Using the above we have

$$
\frac{\log (N_{\delta}(f+g_{\delta,p}))}{\log \delta} \ge \frac{\log (c'' \sum_{k=1}^{m} \min\{m, \#X \cap [(k-1)/m, k/m]\})}{\log \delta}
$$
$$
= \frac{\log c''}{\log m} + \frac{\log (\sum_{k=1}^{m} \min\{m, \#X \cap [(k-1)/m, k/m]\})}{\log m}.
$$

We can select a sufficiently large m0, such that for m > m<sup>0</sup> we get log <sup>c</sup> ′′ logm > −ǫ/2. Now if we select δ<sup>1</sup> = 1 m1 with m<sup>1</sup> ∈ {mk}k∈<sup>N</sup> satisfying

$$
m_1 > \max\{m_{k_0}, m_0, \frac{1}{\delta_0}\},\
$$

we will have that:

$$
\frac{\log N_{\delta_1}(g_{\delta_1,p}+f)}{-\log \delta_1} = \frac{\log N_{\delta_1}(g_{\delta_1,p}+f)}{\log m_1}
$$
  
$$
\geq \frac{\sum_{k=1}^{m_1} \min\{m_1, \#X \cap [(k-1)/m_1, k/m_1]\}}{\log m_1} - \frac{\epsilon}{2}
$$
  
$$
\geq \limsup_{m \to \infty} \frac{\log g_m}{\log m} - \frac{\epsilon}{2} - \frac{\epsilon}{2} = \limsup_{m \to \infty} \frac{\log g_m}{\log m} - \epsilon.
$$

Proof of Theorem 1. First we will show that

$$
\overline{dim}_{gr,B}(X) \ge \limsup_{m \to \infty} \frac{\log g_m}{\log m}
$$

For simplicity let <sup>a</sup> = lim supm→∞ log gm log <sup>m</sup> . Let <sup>f</sup>1(x) = <sup>1</sup> 4 x, F<sup>1</sup> = f1, δ<sup>1</sup> = 1 2 and. Let also assume that for i ∈ {1, 2..., n − 1}, we have chosen f<sup>i</sup> , F<sup>i</sup> , and δ<sup>i</sup> to satisfy

(1) 
$$
F_i = \sum_{j=1}^{i} f_j,
$$
  
\n(2)  $\frac{\log N_{\delta_i}(F_i)}{-\log \delta_i} \ge a - \frac{1}{i},$   
\n(3)  $\delta_i < \max\{\frac{1}{i}, \delta_{i-1}\},$   
\n(4)  $||f_i||_{\infty} \le \min\{\frac{\delta_1}{2^i}, \frac{\delta_2}{2^{i-1}}, \dots, \frac{\delta_i}{2}, \frac{1}{2^i}\}.$ 

By Lemma [1](#page-2-1) for g = Fn−1, δ = δn−1, p = min{ δ1 <sup>2</sup>n−<sup>1</sup> , δ2 <sup>2</sup>n−<sup>2</sup> , . . . , δn−<sup>1</sup> 2 , 1 2<sup>n</sup> } and ǫ = 1 n , we find f<sup>n</sup> ∈ P(X), δ<sup>n</sup> > 0, with ||fn||<sup>∞</sup> ≤ p and δ<sup>n</sup> < min{ 1 n , δn−1} such that log <sup>N</sup>δn (Fn) − log δ<sup>n</sup> ≥ a − 1 n .

Since ||fn||<sup>∞</sup> ≤ 1 <sup>2</sup><sup>n</sup> , we have that F<sup>i</sup> converges uniformly to some F ∈ Cu(X).

Also for n ∈ N, since ||f<sup>i</sup> || < δn 2 <sup>i</sup>−n+1 , ∀i > n we have P<sup>∞</sup> <sup>i</sup>=n+1 ||f<sup>i</sup> || < δ<sup>n</sup> and therefore by Lemma [2](#page-11-1)

$$
\frac{\log N_{\delta_n}(F)}{-\log \delta_n} \ge \frac{\log \frac{1}{2}N_{\delta_n}(F_n)}{-\log \delta_n} = \frac{\log 2}{\log \delta_n} + \frac{N_{\delta_n}(F_n)}{\log \delta_n} \ge a - \frac{1}{n} + \frac{\log 2}{\log \delta_n}.
$$

So we will have that limδn→<sup>0</sup> log Nδn (F) − log δ<sup>n</sup> ≥ a. Since F ∈ Cu(X) that means that dimgr,B(X) ≥ a.

Now we will show that dimgr,B(X) ≤ limm→∞ log gm log m .

Again <sup>a</sup> = lim supm→∞ log gm log m . It is obvious that ∀m, ∀f N <sup>1</sup> m (f) ≤ gm. log N 1 m (f)

That means that for every f , lim supm→∞ log <sup>m</sup> ≤ a. Since we can simply take limits for δ<sup>m</sup> = 1 <sup>m</sup> we have

$$
\overline{dim}_{gr,B}(X) = \sup_{f \in C_u(X)} \limsup_{\delta \to 0} \frac{\log N_{\delta}(f)}{-\log \delta} = \sup_{f \in C_u(X)} \limsup_{m \to \infty} \frac{\log N_{\frac{1}{m}}(f)}{\log m} \le a.
$$

<span id="page-4-0"></span>Corollary 1. Let X be a subset of [0,1] with finitely many isolated points. Then

$$
\overline{dim}_{gr,B}(f) = \overline{dim}_B(X) + 1.
$$

Proof. If a set has finitely many isolated points we may remove those without affecting the box dimensions of the set. So every point in X can be considered an accumulation point. So we will have min{m, #(X ∩ [ k−1 <sup>m</sup> , k <sup>m</sup>])} = m for at least half the boxes that intersect with X - the half are taken to account for edge behavior. That gives

$$
\overline{dim}_{gr,B}(K) = \limsup_{m \to \infty} \frac{\log g_m}{\log m} = \limsup_{m \to \infty} \frac{\log \frac{1}{2} m N_{1/m}(K)}{\log m} =
$$
  
$$
1 + \limsup_{m \to \infty} \frac{N_{1/m}(K)}{\log m} = 1 + \overline{dim}_B(K).
$$

Corollary 2. Let A = {an} , a<sup>n</sup> = 1 np . We have dimB(A) = <sup>1</sup> <sup>p</sup>+1 and dimgr,B(A) = <sup>2</sup> p+1 Proof. For <sup>f</sup>(x) = <sup>1</sup> x p , x > 0 we have f ′ (x) = <sup>−</sup>px(−p−1) <sup>&</sup>lt; 0 and <sup>f</sup> ′′(x) = (p + 1)px(−p−2) > 0

From the relationship f(k) − f(k + 1) = (k − k − 1) · f ′ (u) = −f ′ (u), for u ∈ (k, k + 1) and the fact that |f ′ (x)| = −f ′ (x) is a decreasing function we have that b<sup>n</sup> = a<sup>n</sup> − an+1 is a decreasing sequence. That means that for the smallest n<sup>0</sup> such that f ′ (n0) < 1/m we have

$$
\forall n > n_0 \Rightarrow a_n - a_{n+1} < \frac{1}{m} \text{ and } \forall n < n_0 \Rightarrow a_n - a_{n+1} > \frac{1}{m}. \tag{6}
$$

This tells us that for n ≤ n<sup>0</sup> we cannot have two distinct a<sup>n</sup> in the same box (that would mean their distance is < 1 m ). Likewise for n > n<sup>0</sup> we cannot have a box with no element of {an} in it (that would mean we have a distance that is > 1 <sup>m</sup>).

So to "count" the number of boxes that have elements of {an} inside them all we need to do is find n0, find which box an<sup>0</sup> lies in and add n<sup>0</sup> − 1 to the number of that box. That means we are counting all boxes that are closer to 0 than the box an<sup>0</sup> is in (including that box) and we are counting one box for every element of our sequence before n0.

This gives us

$$
f'(x) = \frac{1}{m}
$$
$$
-px^{(-p-1)} = \frac{1}{m}
$$
$$
x = p + \sqrt[1]{mp}
$$
$$
n_0 = [p + \sqrt[1]{mp}]
$$

Since <sup>k</sup>−<sup>1</sup> <sup>m</sup> < an<sup>0</sup> ≤ k <sup>m</sup> ⇒ k − 1 < man<sup>0</sup> ≤ k ⇒ an<sup>0</sup> lies in box number [man<sup>0</sup> ].

To calculate the dimension of set A we must now calculate

$$
\lim_{m \to \infty} \frac{\log(n_0 + [ma_{n_0}])}{\log m} = \lim_{m \to \infty} \frac{\log\left(\left[\sqrt[p+1]{mp}\right] + \left[m \cdot \frac{1}{\left[\sqrt[p+1]{mp}\right]^p}\right]\right)}{\log m} \tag{7}
$$

The above limit exists and is equal with

$$
\lim_{m \to \infty} \frac{\log\left(\sqrt[p+1]{mp} + m \cdot \frac{1}{(\sqrt[p+1]{mp})^p}\right)}{\log m} = \lim_{m \to \infty} \frac{\log\left((mp)^{\frac{1}{p+1}} + m \cdot \frac{1}{(mp)^{p/p+1}}\right)}{\log m}
$$
\n
$$
= \lim_{m \to \infty} \frac{\log\frac{m(p+1)}{(mp)^{p/p+1}}}{\log m} = \lim_{m \to \infty} \frac{\log(m(p+1)) - \log((mp)^{p/p+1})}{\log m}
$$
\n
$$
= 1 - \frac{p}{p+1} = \frac{1}{p+1}.
$$

Since trere exists a limit it follows that dimB(A) = dimB(A) = dimB(A). Using the same reasoning we can calculate the graph dimension of set A. What we need is to count g<sup>m</sup> = P<sup>m</sup> <sup>k</sup>=1 min{m, #(K ∩ [ k−1 <sup>m</sup> , k m])}. The difference is that we now want the box for which f ′ (n0) < 1 <sup>m</sup><sup>2</sup> . From that box on we will have m or more boxes of our grid meeting with our function whereas before that we will have less than m.

Then we will calculate n<sup>0</sup> plus m times the box that n<sup>0</sup> lies in. Similar with the above we will have:

$$
n_0 = \left[\sqrt[p+1]{m^2p}\right]
$$
  
$$
a_{n_0}
$$
 lies in box 
$$
[ma_{n_0}] = [m \frac{1}{\left(\sqrt[p+1]{m^2p}\right)^p}]
$$

And since we need to count each box until [man<sup>0</sup> ] m times we need to calculate:

$$
\lim_{m \to \infty} \frac{\log \left( \left[ \sqrt[p+1]{m^2 p} \right] + m \cdot \left[ m \cdot \frac{1}{\left[ \sqrt[p+1]{m^2 p} \right]^p} \right] \right)}{\log m}
$$

for <sup>p</sup> p+1 ≤ 1 <sup>2</sup> ⇒ p ≤ 1 we have that when m → ∞ ⇒ man<sup>0</sup> → a ≥ 1. Using the inequality man<sup>0</sup> < [man<sup>0</sup> ] < 2man<sup>0</sup> we have

$$
\lim_{m \to \infty} \frac{\log \left( \sqrt[p+1]{m^2 p} + m \cdot m \cdot \frac{1}{(\sqrt[p+1]{m^2 p})^p} \right)}{\log m} =
$$
$$
\lim_{m \to \infty} \frac{\log \left( (m^2 p)^{\frac{1}{p+1}} + m^2 \cdot \frac{1}{(m^2 p)^{p/p+1}} \right)}{\log m} =
$$
$$
\lim_{m \to \infty} \frac{\log \frac{m^2 (p+1)}{(m^2 p)^{p/p+1}}}{\log m} = \lim_{m \to \infty} \frac{\log (m^2 (p+1)) - \log ((m^2 p)^{p/p+1})}{\log m} =
$$
$$
2(1 - \frac{p}{p+1}) = \frac{2}{p+1}
$$

For <sup>p</sup> <sup>p</sup>+1 > 1 <sup>2</sup> ⇒ p > 1 we have that when m → ∞ ⇒ man<sup>0</sup> → 0 ⇒ [man<sup>0</sup> ] = 1. This gives:

$$
\lim_{m \to \infty} \frac{\log \left( \sqrt[p+1]{m^2 p} + m \right)}{\log m} =
$$
$$
\lim_{m \to \infty} \frac{\log \left( (m^2 p)^{\frac{1}{p+1}} + m \right)}{\log m} =
$$
$$
\lim_{m \to \infty} \frac{\log \left( m^{\frac{2}{p+1}} (p^{\frac{1}{p+1}} + m^{\frac{p-1}{p+1}}) \right)}{\log m} = \frac{2}{p+1} + \frac{p-1}{p+1} = 1.
$$

## 3. construction of sets and refinement of [\(1\)](#page-0-0)

In this section, we are going to refine [\(1\)](#page-0-0), in the sense of Corollary [3,](#page-7-0) that for every set X ⊂ [0, 1] we have

$$
max{1, 2\overline{\dim}_B(X)} \le \overline{\dim}_{gr, B}(X) \le 1 + \overline{\dim}_B(X).
$$

Furthermore we are going to prove that the new inequality is sharp, by constructing a set with dimB(X) = a and dimgr,B(X) = b , for every choice of 0 < a ≤ 1 and b such that

$$
max{1, 2a} \le b \le 1 + a.
$$

<span id="page-7-1"></span>Theorem 3. If a set X has dim X = a then dimgr,B(X) ≥ 2a

Proof. Since dimB(X) = a, we have that

$$
\limsup_{m \to \infty} \frac{\log N_{1/m}(X)}{\log m} = a.
$$

If for each m we consider the set P <sup>m</sup> that contains exactly one element of X for each box that intersects with X when we divide [0, 1] in m boxes then N1/m(X) = |P <sup>m</sup>|. Since there are no two elements of <sup>P</sup> <sup>m</sup> in the same box, if we divide [0, 1] in [√ m] boxes (which define intervals I<sup>k</sup> for k ∈ {1, ..., [ √ m]}) we see that in each one of these boxes we have at most [√ m ]+ 2 elements of P <sup>m</sup>. If that is not true then the width of that box would have to be strictly larger than [√ m] · 1 m ≥ 1 [ √ m ] , which is this is impossible. This means that |P <sup>m</sup> <sup>∩</sup> <sup>I</sup>k| ≤ [ √ <sup>m</sup>] + 2 <sup>≤</sup> 2[<sup>√</sup> m ] for all k. Now for the graph dimension we have

$$
\overline{dim}_{gr,B}(X) = \limsup_{m \to \infty} \frac{\log g_m(X)}{\log m} \ge \limsup_{m \to \infty} \frac{\log g_{\lfloor \sqrt{m} \rfloor}(X)}{\log[\sqrt{m}]}
$$
  
\n
$$
\ge \limsup_{m \to \infty} \frac{\log \frac{1}{2} \sum_{k=1}^{\lfloor \sqrt{m} \rfloor} \min\{2[\sqrt{m}], \#(X \cap I_k)\}}{\frac{1}{2} \log m}
$$
  
\n
$$
\ge \limsup_{m \to \infty} \frac{\log \frac{1}{2} \sum_{k=1}^{\lfloor \sqrt{m} \rfloor} \min\{2[\sqrt{m}], \#(P^m \cap I_k)\}}{\frac{1}{2} \log m}
$$
  
\n
$$
\ge \limsup_{m \to \infty} \frac{\log \frac{1}{2} \sum_{k=1}^{\lfloor \sqrt{m} \rfloor} \#(P^m \cap I_k)\}}{\frac{1}{2} \log m}
$$
  
\n
$$
\ge \limsup_{m \to \infty} \frac{\log \frac{1}{2} |P^m|}{\frac{1}{2} \log m} = 2 \limsup_{m \to \infty} \frac{\log N_{1/m}(X)}{\log m} = 2a.
$$

<span id="page-7-0"></span>Corollary 3. If a set X has dim X = a then

$$
\max\{1, 2a\} \le \overline{\dim}_{gr, B}(X) \le a+1.
$$

Proof. The proof is a straightforward combination of Theorem [3](#page-7-1) and [\(1\)](#page-0-0).

## 4. Construction of sets

Theorem 4. Let 0 < a ≤ 1 and b with max{2a, 1} ≤ b ≤ a + 1, then it exists a compact set X with dimB(X) = a and dimgr,B(X) = b.

Proof. For 0 < a ≤ 1 and b = a + 1, any perfect set X with dimB(X) = a will do, due to Corollary [1.](#page-4-0) We will do the construction only for a > 0 and <sup>b</sup> with max{2a, <sup>1</sup>} ≤ b < a + 1. Let <sup>x</sup><sup>n</sup> = 2<sup>n</sup> n , 0 <sup>≤</sup> c < 1 and <sup>X</sup>n,i <sup>=</sup> <sup>n</sup> i xn − j xn+2 , j = 1, ..., [x c n ] o where i ∈ {1, ..., [x a n ] = kn} . We also set

<span id="page-8-1"></span>
$$
X_n = \bigcup_{i=1}^{n=k_n} X_{n,i} \text{ and } X = \bigcup_{n=1}^{\infty} X_n \bigcup \{0\}.
$$

For xn, with n sufficiently big we have:

(a) 
$$
x_n^a \ge 1 + x_1^2 + ... x_{n-1}^2
$$
,  
\n(b)  $\lim_{n \to \infty} \frac{\log x_{n+1}}{\log x_n} = \infty$ . (8)

Furthermore for n sufficiently big is easy to check the following properties:

$$
(a) \frac{i-1}{x_n} \le \inf X_{n,i} \le \sup X_{n,i} \le \frac{i}{x_n},
$$
  
\n
$$
(b) \quad \operatorname{diam}(X_{n,i}) \le \frac{1}{x_{n+1}},
$$
  
\n
$$
(c) \quad \frac{x_n^a}{2x_n} \le \sup X_n \le \frac{x_n^a}{x_n},
$$
  
\n
$$
(d) \quad |X_n| \le x_n^2.
$$
  
\n(9)

First we are going to calculate the upper box dimension of X and in the sequel, its upper graph box dimension.

For x<sup>n</sup> ≤ m ≤ xn+1 we have

$$
N_{\frac{1}{m}}(X) \le 1 + N_{\frac{1}{m}}(X_{n+1}) + N_{\frac{1}{m}}(X_n) + x_{n-1}^2 + x_{n-2}^2 + \dots + x_1^2.
$$

Now since diam(Xn,i) < 1 xn+1 ≤ 1 <sup>m</sup> we have that at most 2k<sup>n</sup> ≤ 2[x a n ] < 2x a n boxes intersecting Xn. Also by [\(9,](#page-8-0)c) we have

<span id="page-8-0"></span>
$$
\frac{mx_{n+1}^a}{2x_{n+1}} \le N_{\frac{1}{m}}(X_{n+1}) \le \frac{mx_{n+1}^a}{x_{n+1}} + 1,
$$

therefore by using [\(8](#page-8-1), a) we get

$$
\frac{\log N_{\frac{1}{m}}(X)}{\log m} < \frac{\log \frac{mx_{n+1}^a}{x_{n+1}} + 3x_n^a}{\log m} \n< \max \left\{ \frac{\log 2 \frac{mx_{n+1}^a}{x_{n+1}}}{\log m}, \frac{\log 6x_n^a}{\log m} \right\} \n< \max \left\{ \frac{\log 2 + \log m - \log x_{n+1}^{1-a}}{\log m}, \frac{\log 6 + a \log x_n}{\log m} \right\} \n< \max \left\{ 1 + \frac{\log 2 - \log x_{n+1}^{1-a}}{\log m}, \frac{\log 6 + a \log x_n}{\log m} \right\} \n< \max \left\{ 1 + \frac{\log 2 - \log x_{n+1}^{1-a}}{\log x_{n+1}}, \frac{\log 6 + a \log x_n}{\log x_n} \right\} \n< \max \left\{ a + \frac{\log 2}{\log x_{n+1}}, a + \frac{\log 6}{\log x_n} \right\}.
$$

Now by letting m, x<sup>n</sup> go to infinity, and by observing [\(8](#page-8-1), b) we get

$$
\overline{\dim}_B(X) \leq a.
$$

To get the lower bound, we just look at scales m = xn.

$$
\overline{dim}_B(X) = \limsup_{m \to \infty} \frac{\log N_{\frac{1}{m}}(X)}{\log m} \ge \limsup_{n \to \infty} \frac{\log N_{\frac{1}{x_n}}(X_n)}{\log x_n}
$$
$$
\ge \limsup_{n \to \infty} \frac{\log(\frac{x_n^a}{2x_{n-1}})}{\log x_n} \stackrel{(8,b)}{=} a.
$$

Now for gm(X) we have

$$
g_m(X) \le g_m\left(\bigcup_{i=n+2}^{\infty} X_i\right) + g_m\left(\bigcup_{i=1}^{n+1} X_i\right) \le m + \sum_{i=1}^{m+1} g_m(X_i)
$$
  
$$
\le m + g_m(X_{n+1}) + x_n^{a+c} + \sum_{i=1}^{n-1} x_i^2 \stackrel{(8,a)}{\le} 2m + g_m(X_{n+1}) + x_n^{a+c},
$$

where for gm(Xn+1) we have

<span id="page-9-0"></span>
$$
g_m(X_{n+1}) \le \begin{cases} \frac{m^2 x_{n+1}^a}{x_{n+1}} + m & m \le x_{n+1}^{\frac{1+c}{2}}\\ x_{n+1}^{a+c} & m \ge x_{n+1}^{\frac{1+c}{2}} \end{cases}
$$
(10)

The first estimate comes from the fact that we have at most Nm(Xn+1) = mx<sup>a</sup> n+1 xn+1 + 1 boxes occupied by points of Xn+1, and we can utilize at most m points in every one of these boxes, while the second comes from the fact that we have at most kn+1[x c <sup>n</sup>+1] < xa+<sup>c</sup> <sup>n</sup>+1 points in Xn+1 in total.

Thus we get

$$
\frac{\log g_m(X)}{\log m} < \frac{\log (3m + (g_m(X_{n+1}) - m) + x_n^{a+c})}{\log m} \n< \max \left\{ \frac{\log 6m}{\log m}, \frac{\log 3(g_m(X_{n+1}) - m)}{\log m}, \frac{\log 3x_n^{a+c}}{\log m} \right\} \n< \max \left\{ 1 + \frac{\log 6}{\log m}, \frac{\log 3(g_m(X_{n+1}) - m)}{\log m}, \frac{\log 3 + (a+c)\log x_n}{\log x_n} \right\}.
$$

It is easy to see from [\(10\)](#page-9-0) that

$$
\frac{\log (g_m(X_{n+1}) - m)}{\log m} \le \frac{\log x_{n+1}^{a+c}}{\log x_{n+1}^{\frac{1+c}{2}}} \le 2\frac{a+c}{1+c}.
$$

Therefore we have

$$
\frac{\log g_m(X)}{\log m} \le \max\left\{1 + \frac{\log 6}{\log m}, 2\frac{a+c}{1+c}, a+c+\frac{\log 3}{\log x_n}\right\},\,
$$

and by letting m, x<sup>n</sup> go to infinity, and by observing that 2 <sup>a</sup>+<sup>c</sup> 1+<sup>c</sup> > a + c and recalling [\(8](#page-8-1), b) we have

$$
\overline{dim}_{gr,B}(X) < \max\{1, 2\frac{a+c}{1+c}\}.
$$

To get the lower bound, we just look at scales m = x 1+c 2 n+1 . First we need to observe that since <sup>i</sup> xn+1 ∈ Xn+1,i we have that for every 0 ≤ j ≤ [ x c+2a−1 2 n+1 2 ], is true that j x 1+c 2 <sup>n</sup>+1 , j+1 x 1+c 2 <sup>n</sup>+1 intersects at least x 1−c 2 n+1 −2 ≥ " x 1−c 2 n+1 2 # of the sets <sup>X</sup>n+1,i, thus containing at least " x 1−c 2 n+1 2 # − 2 ≥ " x 1−c 2 n+1 4 # of them, and therefore containing at least " x 1−c 2 n+1 4 # [x c <sup>n</sup>+1] ≥ " x 1+c 2 n+1 8 # points. Therefore g x 1+c 2 <sup>n</sup>+1 (Xn+1) <sup>&</sup>gt; " x 1+c 2 n+1 8 # ([x c+2a−1 2 n+1 2xn ] + 1) > x a+c n+1 16xn . Now we have

$$
\overline{dim}_{gr,B}(X) = \limsup_{m \to \infty} \frac{\log g_m(X)}{\log m} \ge \limsup_{n \to \infty} \frac{\left[\frac{1+c}{x_{n+1}^2}\right]^{(X_{n+1})}}{\log \left(\left[\frac{1+c}{x_{n+1}^2}\right]\right)}
$$
$$
\ge \limsup_{n \to \infty} \frac{\log \left(\frac{x_{n+1}^{a+c}}{16}\right)}{\log \left(\frac{1+c}{x_{n+1}^2}\right)} \ge 2\frac{a+c}{1+c}.
$$

Also dimgr,B(X) ≥ 1 trivially. Therefore

$$
\overline{dim}_{gr,B}(X) = \max\{1, 2\frac{a+c}{1+c}\}.
$$

Now by choosing c such that b = 2 <sup>a</sup>+<sup>c</sup> 1+<sup>c</sup> we get our result.

## Appendix A.

Here are some general results regarding functions in R and box counting that we use for the proof of Theorem [2.](#page-2-2) We will consider the δ-meshes as the union ∪i,j∈NB j <sup>i</sup> with B j <sup>i</sup> = [iδ,(i+ 1)δ)× [jδ,(j + 1)δ). That means that B<sup>i</sup> = ∪j∈NB j i is the i + 1 column of the mesh.

<span id="page-11-1"></span>Lemma 2. Let δ > 0 and f, g ∈ Cu(X) with g > 0 and ||g||<sup>∞</sup> ≤ δ. We have Nδ(f + g) ≥ 1 <sup>2</sup>Nδ(f).

Proof. For every x ∈ X and B j <sup>i</sup> we have that if (x, f(x)) ∈ B j i then (x,(f + g)(x)) ∈ B j <sup>i</sup> ∪ B j+1 i . Now let B<sup>i</sup> = ∪j∈NB j i be an arbitrary column, and B j1 i , ...Bj<sup>i</sup> i be the boxes in that column intersected from the graph of f(x). Finally let (xj<sup>1</sup> , f(xj<sup>1</sup> )), ...,(xj<sup>i</sup> , f(xj<sup>i</sup> )), be the points in the corresponding boxes. Wlog we can assume that i is even number. Then (xj<sup>2</sup> ,(f +g)(xj<sup>2</sup> )),(xj<sup>4</sup> ,(f +g)(xj<sup>4</sup> )), ...,(xj<sup>i</sup> ,(f +g)(xj<sup>i</sup> ), belong to different boxes. So f + g intersects with at least <sup>j</sup><sup>i</sup> 2 boxes of the B<sup>i</sup> column. Now by summing over all columns, we get what we want.

<span id="page-11-0"></span>Lemma 3. If given a <sup>δ</sup>-grid and two functions f, g (<sup>R</sup> <sup>→</sup> <sup>R</sup> <sup>+</sup>) such that g intersects with Nδ(g) boxes of the grid and f intersects with at most n<sup>f</sup> boxes at each column of the grid then their sum intersects with at least <sup>N</sup>δ(g) 2n<sup>f</sup> boxes of the grid.

Proof. We will first prove the result for a single column of boxes.

Let a<sup>m</sup> = (xm, g(xm)) be ni,g distinct points in which g intersects with the elements of the column B<sup>i</sup> . Let ni,f , ni,f+<sup>g</sup> be the number of boxes of column i that intersect with f, f + g respectively.

Every a<sup>m</sup> lies in a unique B j i since we are using disjoint boxes.

Since ∀x ∈ [iδ,(i+ 1)δ), we have that f(x) ∈ B j i for some <sup>j</sup> <sup>∈</sup> <sup>N</sup> and since f intersects with only ni,f elements of the column it follows that there is a subset <sup>G</sup> of <sup>N</sup> with exactly <sup>n</sup>j,f elements such that <sup>∀</sup><sup>x</sup> <sup>∈</sup> [jδ,(<sup>j</sup> + 1)δ) <sup>f</sup>(x) <sup>∈</sup> B j i and i ∈ G.

Now we will show that if (a, b) ∈ B j i and (a, c) <sup>∈</sup> <sup>B</sup><sup>l</sup> i then (a, b + c) lies in either B j+l i or in B j+l+1 i .

$$
a \in [i\delta, (i+1)\delta] \text{ and } (a,b) \in B_i^j \Leftrightarrow b \in [j,j+1)
$$
  
so  
$$
j \le b < j+1
$$
  
$$
l \le c < l+1 \Rightarrow
$$
  
$$
j+l \le b+c < j+l+2 \Rightarrow
$$
  
$$
b+c \in [j+l,j+l+1) \text{ or } b+c \in [j+l+1,j+l+2) \Rightarrow
$$
  
$$
(a,b+c) \in B_i^{j+l} \text{ or } (a,b+c) \in B_i^{j+l+1}
$$

Now we can show that f + g intersects with at least <sup>n</sup>i,g 2n<sup>f</sup> elements of the column. If ni,f+<sup>g</sup> < ni,g 2ni,f then the ni,g points (xm,(f + g)(xm)) (where x<sup>m</sup> are the first coordinates of the points am) lie in less than <sup>n</sup>i,g 2ni,f elements of the column. So there must be a set of at least 2ni,f + 1 of the x<sup>m</sup> (we will call them xm<sup>l</sup> ) for which all points (xm<sup>l</sup> ,(f + g)(xm<sup>l</sup> )) lie in B<sup>k</sup> i , for some <sup>k</sup> <sup>∈</sup> <sup>N</sup>.

The above is assuming that ni,g ≥ 2ni,f + 1, if this is not true we have the trivial case where ni,f+<sup>g</sup> ≥ 1 which is true.

Since all (xm<sup>l</sup> , f(xm<sup>l</sup> )) lie in at most ni,f elements of B<sup>i</sup> then in the 2ni,f + 1 of them there are at least 3 points (xm<sup>l</sup> , f(xm<sup>l</sup> )) that lie in B<sup>n</sup> i , for some <sup>n</sup> <sup>∈</sup> <sup>N</sup>.

If we combine this with the above and the fact that the corresponding points (xm<sup>l</sup> ,(f + g)(xm<sup>l</sup> )) are all in B<sup>k</sup> <sup>i</sup> we have 2 distinct points a<sup>i</sup> = (x<sup>i</sup> , g(xi)) in the same box (either B k−n i or B k−n−1 i ). Given the selection of {am} this is impossible.

Since ni,f ≤ n<sup>f</sup> we have ni,f+<sup>g</sup> ≥ ni,g 2n<sup>f</sup> . By summing over all j (the sum is finite) we obtain Nδ(f + g) ≥ Nδ(g) 2n<sup>f</sup> .

<span id="page-12-1"></span>Lemma 4. Let B j i a box covering of [0, 1]×R. Let also <sup>f</sup> a piecewise smooth function in [0, 1]. Let also assume that the derivative, where it is defined, is bounded by some constant k. Then f meets with each column of boxes B j i in at most k + 1 boxes.

#### References

<span id="page-12-0"></span>[1] Hyde, J., Laschos, V., Olsen, L., Petrykiewicz, I. and Shaw, X., On the box dimensions of graphs of typical continuous functions. Journal of Mathematical Analysis and Applications, 391 (2), pp. 567-581.

- <span id="page-13-1"></span>[2] Falconer, Kenneth . Fractal geometry Mathematical foundations and applications. Second edition, John Wiley and Sons, Inc., Hoboken, NJ, 2003.
- <span id="page-13-0"></span>[3] P. Humke, G. Petruska, The packing dimension of a typical continuous function is 2. Real Anal. Exchange 14 (1988/1989) 345358
- [4] R.D. Mauldin, S.C. Williams, On the Hausdorff dimension of some graphs. Trans. Amer. Math. Soc. 298 (1986) 793803.

<span id="page-13-2"></span>