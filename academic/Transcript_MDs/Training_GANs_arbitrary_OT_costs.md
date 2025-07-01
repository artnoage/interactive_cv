# Training Generative Networks with Arbitrary Optimal Transport costs.

Vaios Laschos Fakult¨at Elektrotechnik und Informatik Technische Universit¨at Berlin vaios.laschos@tu-berlin.de.

Jan Tinapp Fakult¨at Elektrotechnik und Informatik Technische Universit¨at Berlin jan.tinappp@tu-berlin.de.

Klaus Obermayer Fakult¨at Elektrotechnik und Informatik Technische Universit¨at Berlin klaus.obermayer@tu-berlin.de.

April 21, 2020

#### Abstract

We propose a new algorithm that uses an auxiliary neural network to express the potential of the optimal transport map between two data distributions. In the sequel, we use the aforementioned map to train generative networks. Unlike WGANs, where the Euclidean distance is implicitly used, this new method allows to explicitly use any transportation cost function that can be chosen to match the problem at hand. For example, it allows to use the squared distance as a transportation cost function, giving rise to the Wasserstein-2 metric for probability distributions, which results in fast and stable gradient descends. It also allows to use image centered distances, like the structure similarity index, with notable differences in the results.

Keywords— Generative networks, learning probability distributions, model fitting, optimal transport, Wasserstein-2.

# 1 Introduction

In the seminal work of [\[9\]](#page-16-0), a ground breaking approach for training generative networks (GNs) was proposed. GNs try to generate new data given some training data x. This is achieved by treating the data as samples from an unknown empirical probability function P<sup>r</sup> and fitting a model P<sup>θ</sup> to give an estimate for this function. By drawing samples from Pθ, new data points can be generated that resemble the original dataset. The approach in [\[9\]](#page-16-0), proposes to use two neural networks one of which is the generator G(z) and the other acts as a discriminator D(x). The generator represents the model Pθ, while the discriminator gives a differentiable measure of how similar P<sup>θ</sup> is to Pr. To train the generator the two networks participate in a two-player minimax game where the discriminator is maximizing the

![](_page_1_Picture_0.jpeg)

Figure 1: The closest real point to a generated one, in respect to SSIM and the Euclidean distance respectively.

probability to detect if data shown to it comes from the generator or the training dataset. The generator is trying to fool the discriminator by minimizing the probability of generated data being detected. To train the networks the value function min G max D V (D, G) = Ex∼P<sup>r</sup> [log D(x)] + Ex∼P<sup>θ</sup> [log(1 − D(x))] is used by switching between taking the gradient with respect to the weights in G(x) and D(x).

As it is explained in [\[9\]](#page-16-0), the discriminator provides an error function for the generator. A fully trained discriminator will provide as a cost the relative entropy of the generated distribution P<sup>θ</sup> with respect to the real distribution Pr. However relative entropy is a good metric distance for two distributions, only when they have the same support. If the distributions have different supports the error function cannot provide any information for the points charged by P<sup>θ</sup> and not by Pr. In practice this means that if the discriminator is well trained then it does not provide a gradient for the generator to learn, which result to the phenomenon of mode collapse. To fix that, researchers suggested various technical solutions, among them being the introduction of vanishing noise, since by adding some noise, the two distributions have always the same support. However, most of these solutions were producing other problems in return.

### 1.1 WGANs and beyond

To deal with the issues that the original GANs exhibited, various new approaches were introduced, with the most noticeable being the Wasserstein GAN in [\[1\]](#page-16-1), that views the problem as an optimal transport task. In this approach the Wasserstein-1 distance between samples from the real distribution and samples from the current model is approximated and then minimized by changing the generator weights. In order to find the gradient to change the model, a differentiable way of calculating the Wasserstein-1 distance is required. This issue is resolved by introducing a neural network, the critic, that gets trained to approximate the Wasserstein distance between samples form both distributions.

<span id="page-1-0"></span>To adapt the model with respect to the distance, the following formula was used:

$$
W_1(\mathbb{P}_{\theta}, \mathbb{P}_r) := \sup_{\psi \in \text{Lip}_1} \left\{ \int \psi \, d\mathbb{P}_{\theta} - \int \psi \, d\mathbb{P}_r \right\}.
$$
 (1)

were ψ is encoded by the critic and kψk<sup>L</sup> ≤ 1 constrains it to be 1-Lipschitz. Before we proceed, we would like to emphasize that unlike GANs, in WGANs the two networks do not act in an antagonistic fashion. It is possible, at least in theory, to fully train the critic in every training step of the generator. Something like that is not advisable though, because it would be extremely expensive in computational time.

The simplicity for calculating the Wasserstein-1 distance comes from its dual formulation [\(1\)](#page-1-0). One needs a single function, that can be encoded by the critic neural network, to express ψ in [\(1\)](#page-1-0), which in the sequel can be used to train the generator. At the same time, for different transportation costs, a nice formula like this is not known. It is important to note that, when one trains the generator with Euclidian distance as an underlying transport cost, the generator produces elements that are closer to the real ones with respect to that distance. Something like that may not be enticing when one wants to deal with distributions of data that have a different intrinsic metric. For example, when one tries to measure distance between two images, the Euclidean distance between pixels may not the be the right choice as Figure 1 indicates. In this paper we propose a new algorithm for capturing the

![](_page_2_Figure_0.jpeg)

![](_page_2_Figure_1.jpeg)

<span id="page-2-0"></span>Figure 2: Visualization of the assignments of generated points, initially found in the middle, to a ring of gaussians.

optimal transport distance between two distributions, with arbitrary transport cost. This way, the manifold that the generator produces could potentially fit better to the real data distribution. Also as we will argue in the sequel, our proposed method allows to optimize the training to any desirable degree, restricted only by processing power, and it can ensure that no mode collapse occurs.

### 1.2 A new approach

Regardless of any mathematical complexity that the derivation of our training algorithm may exhibit, its heuristic explanation can be easily grasped. We start by taking two sets of points X1, X2. For visualization purposes one can think X<sup>1</sup> as the set of generated points and X<sup>2</sup> as the set of real points. For each point x in X1, we assign one point in set X2, through the formula

<span id="page-2-1"></span>
$$
y(x, w) = \underset{y \in \mathcal{X}_2}{\arg \inf} \{c(x, y) + \psi_w(y)\},\tag{2}
$$

where c : X<sup>1</sup> × X2, is some optimal transport cost and ψ<sup>w</sup> a function parametrized by the "weight values" w. Now, some real points in X<sup>2</sup> have many generated points in X<sup>1</sup> assigned to them, while at the same time, some others have no points assigned to them at all. For the real points that have many generated points assigned to them, we would like ψ<sup>w</sup> to increase, and for those who are under-assigned to decrease. It is shown that the assigner ψ<sup>w</sup> is trained to perfection, when all points are assigned equally, and in that case, ψ<sup>w</sup> coincides with the potential ("pregradient") of the optimal transport plan. We achieve that by using

<span id="page-2-2"></span>
$$
\sum_{j=1}^{\#\mathcal{X}_1} \left( \frac{\#\{\{x_i, 0 \le i \le \#\mathcal{X}_2 : y(x_i, w_0) = y_j\}}{\#\mathcal{X}_2} - \frac{1}{\#\mathcal{X}_1} \right) \psi_w(y_j),\tag{3}
$$

as a cost to our auxilary network. We observe that the change to the values of ψ<sup>w</sup> in a real point is weighted by the numbers of generated points assigned to it. Finally, the constant <sup>1</sup> #X1 that appears in the error function, can be understood as a normalization constant. When the assigner is trained to perfection, then one can use the assignments to send the generated points to the reals that are assigned. As a visual aid, one can look at Figure [2,](#page-2-0) where we treat the case of the real data being 2000 points generated by a ring of 10 Gaussians.

First contribution: A proof of concept that one can use dual formulations for arbitrary optimal transport problems, i.e.

<span id="page-3-0"></span>
$$
\sup_{\psi \in C_b(\mathcal{X})} \left\{ \int \psi^{supp(\nu),c} d\mu(x) - \int \psi d\nu(y) \left| \psi^{supp(\nu),c}(x) \right. = \inf_{y \in supp(\nu)} \left\{ c(x,y) + \psi(y) \right\} \right\},\tag{4}
$$

to recover an applicable algorithm for training generative networks with good results, and not only when the cost is the euclidean distance and the resulting metric is Wasserstein-1. It is reasonable to assume, that a generator trained with a method like that and with a cost functions that captures the geometry of the original dataset, will also reproduce that geometry.

Second contribution: We rigorously show, that from a probabilistic point of view, one can exchange the gradient with the arg inf operator in [\(2\)](#page-2-1), eventually reaching formula [\(3\)](#page-2-2). This makes the whole dual formulation approach computationally feasible. Calculating the gradient of [\(2\)](#page-2-1) instead, would require an infeasible number of statistically useless computations. Furthermore, in formula [\(2\)](#page-2-1), the critic is not evaluated for the generated points. Since the generated points do not directly occur in the error function as in [\(1\)](#page-1-0), any number of them can be generated, in order to achieve any desired proximity to the full theoretical error function [\(4\)](#page-3-0). On the other hand, all the real points contribute to the value of the error function, posing this way a restriction on the size of the original dataset, which is the main drawback of our approach.

### 1.3 Further comments and outline

In the vast literature of GANs and WGANs, there are various papers that claim the use of general metric distances. Among the most noticeable are [\[11\]](#page-17-0) and [\[4\]](#page-16-2), that produce state of the art results. However, in these papers a regularization term is added to a WGAN training cost to achieve some of the qualities of the transport cost that they claim to apply. Although really difficult to properly formulate and prove, we expect that no WGAN-like method, that uses a single function ψ can capture general optimal transportation in its entirety. This happens because many of the literariness that the Wasserstein-1 formulas enjoy, break in cases where the cost function is not a metric distance. We would like to emphasize at this point, that our algorithm, regardless of any criticism that may apply to it, does exactly that. It trains in a matter that real optimal transportation with general cost function, between the two distributions, is achieved. It does not train like other GANs/WGANs and it is not a variation of them.

We would finally like to mention, that although we run some comparative experiments with a good outcome, we restricted our experiments to very basic datasets like MNIST and FASHION-MNIST. We lacked both the expertise and the computational power to run more sophisticated tests with more demanding datasets. We do not claim our algorithm to be state of the art, but it acts as a proof of concept, and we aim to improve in various directions in the future. Furthermore we used the real Wasserstein distance, measured by an external application, between the whole real and generated distributions to show that at least from a mathematical perspective, our method minimizes better the distances that claim to capture.

The layout of the paper is the following. First we have a discussion on optimal transportation distances, and a short literature review on the special case of the Wasserstein-1 distance. We proceed with a mathematical analysis of our method, to which we will refer from now on as the assignment method. Next, we provide a heuristic description of the difference in training between GANs and the assignment method. Finally we provide our experimental results and we enumerate the strengths and drawbacks of the assignment method.

# 2 Optimal transportation

For the sequel, let (X , d<sup>X</sup> ) be a compact metric space. We will denote by M(X ) the space of all nonnegative and finite Borel measures on X endowed with the weak topology induced by the duality with the continuous and bounded functions of Cb(X ). The set P(X ) ⊂ M(X ) is the subset of probability measures. Let finally c : X × X → R <sup>+</sup>, a transportation "cost" function that is continuous with respect to the distance d<sup>X</sup> . For two measures µ, ν, a transport plan between µ and ν is a measure Q ∈ P(X ×X ) with marginals µ := π 0 ] Q, ν := π 1 ] Q. In the last line, we applied the following definition.

Definition 2.1. If µ ∈ P(X ) and T : X → Y is a Borel map, T]µ will denote the push-forward measure on Y, defined by

$$
T_{\sharp}\mu(B) := \mu(T^{-1}(B)) \quad \text{for every Borel set } B \subset Y. \tag{5}
$$

Now we define the optimal transport distance between two measures µ, ν.

Definition 2.2. Given a couple of measures µ, ν ∈ P(X ), their c-Optimal Transportation distance T<sup>c</sup> is defined by

$$
\mathcal{T}_c(\mu,\nu) := \min_{Q \in \mathcal{P}(\mathcal{X} \times \mathcal{X})} \left\{ \iint c(x,y) \, dQ(x,y) \, \Big| \, \pi_\sharp^0 Q = \mu \wedge \, \pi_\sharp^1 Q = \nu \right\}.
$$
 (6)

For the case where c = d<sup>X</sup> , we recover the so called Monge-Kantorovich distance or Wasserstein-1, i.e. W<sup>1</sup> = T<sup>d</sup><sup>X</sup> . Also when c = d 2 <sup>X</sup> , the square root of T<sup>d</sup> 2 X , gives the Wasserstein-2 distance, i.e. W<sup>2</sup> = q Td 2 X . In the sequel, we are going to denote the set of all integrable functions with respect to some probability measure µ, with L(µ). We are also going to use the notation supp(µ) for the support of µ. From [\[14\]](#page-17-1), we have:

<span id="page-4-0"></span>Theorem 2.3 (Dual formulation). For µ, ν ∈ P(X ), we have

$$
\mathcal{T}_{c}(\mu,\nu) := \sup_{\phi,\psi \in C_{b}(\mathcal{X})} \left\{ \int \phi \, d\mu(x) - \int \psi \, d\nu(y) \, \middle| \, \phi(x) + \psi(y) \le c(x,y) \right\}
$$
\n
$$
= \sup_{\psi \in C_{b}(\mathcal{X})} \left\{ \int \psi^{c} \, d\mu(x) - \int \psi \, d\nu(y) \, \middle| \, \psi^{c}(x) = \inf_{y \in \mathcal{X}} \{c(x,y) + \psi(y)\} \right\}
$$
\n
$$
= \sup_{\psi \in C_{b}(\mathcal{X})} \left\{ \int \psi^{supp(\nu),c} \, d\mu(x) - \int \psi \, d\nu(y) \, \middle| \, \psi^{supp(\nu),c}(x) = \inf_{y \in supp(\nu)} \{c(x,y) + \psi(y)\} \right\}.
$$
\n(7)

### 2.1 The case of the Wasserstein-1 distance: from weight clipping to the two-step approximation method

In [\[1\]](#page-16-1), the authors suggest the use of the Wasserstein-1 distance as an error function for training GANs. In order to implement the Wasserstein-1 distance, the authors used a special form of the dual formulation [\(7\)](#page-4-0) that holds only for the case of the Wasserstein-1 distance. Specifically, they used the fact that if ψ is a Lipschitz function with Lipschitz constant smaller than one, then ψ c is equal to ψ. This gives rise to the formula

$$
W_1(\mu,\nu) := \sup_{\psi \in \text{Lip}_1} \left\{ \int \psi \, d\mu(x) - \int \psi \, d\nu(y) \right\}.
$$
 (8)

In order to implement this form of the distance, one had to establish that during the training procedure the function ψ has to have Lipschitz constant of less than one. In order to achieve that, they introduced the method known as weight clipping, where any time a weight exceeds a specific limit, it is reduced so f can retain its Lipschitz constant. However, this first approach, although quite plausible, did not have any rigorous mathematical justification, and it is known to cause issues like stagnation or instability of the learning process, as it was pointed out in [\[10\]](#page-16-3). Following [\[1\]](#page-16-1), in several publications, authors tried to fix, improve or replace this method. Among the most notable papers, in [\[10\]](#page-16-3) the authors propose a method to stabilize the gradient. More recently, in [\[12\]](#page-17-2) the authors propose to first solve a linear programming problem and then use the solution to train the critic to mimic the solution. Evenmore the method [\[12\]](#page-17-2) allows for more general transportation costs, provided that they satisfy the triangular inequality. However, even in the method proposed in [\[12\]](#page-17-2), the squared distance is not applicable, since it does not satisfy the triangular inequality. Furthermore, this method requires a process that is outside the training circle, making it difficult to compare efficiency with established methods. We remind once more, that there are papers with state of the art results like [\[11\]](#page-17-0) and [\[4\]](#page-16-2), where it is claimed that more general optimal costs are reproduced. However, in these papers a regularization term is added to a WGAN training cost to achieve, only in part, the qualities of the transport cost that they claim to apply.

# 3 Mathematical justification for a new network type and error function: The Assignment method

Before we proceed, we will make the following assumption for the cost c, that it holds true for all norms.

<span id="page-5-2"></span>Assumption 3.1. For every x ∈ X , the level sets of c(x, ·), ie Xx,a = {y ∈ X : c(x, y) = a}, have Lebesgue measure zero.

Let now ψ<sup>w</sup> denote the function that corresponds to the assigning network (imagine that as the analogous of a critic) with weights w. We will also assume that ν = P<sup>M</sup> <sup>j</sup>=1 δ<sup>y</sup><sup>j</sup> is the distribution of all real points, and µ = P<sup>θ</sup> is the distribution of Gθ(z), where G<sup>θ</sup> is the generator, z ∼ p, and p is the "noise" latent distribution. We independently pick a sequence of points x<sup>i</sup> from Pθ. We denote with µ<sup>N</sup> = P<sup>N</sup> <sup>i</sup>=1 δ<sup>x</sup><sup>i</sup> the Nth-order empirical distribution by summing the first N points. Finally for every generated point x, we define y(x, w), as follows:

$$
y(x, w) = \underset{y \in supp(\nu)}{\arg \inf} \{c(x, y) + \psi_w(y)\}.
$$
 (9)

For fixed (x, w), y(x, w) is the point that is assigned by the formula for the dual. As we show in the appendix, this point is unique with probability one. If one point does not have a unique assignment then we arbitrary assign a point without loss of generality. By standard results in probability, we have that almost surely it holds µ<sup>N</sup> → µ, and therefore

<span id="page-5-0"></span>
$$
\mathbf{D}_{w} \left( \int \psi_{w}^{supp(\nu),c}(x) d\mu(x) - \int \psi_{w}(y) d\nu(y) \right)_{|w=w_{0}}
$$
\n
$$
= \int \mathbf{D}_{w} \left( \psi_{w}^{supp(\nu),c}(x) \right)_{|w=w_{0}} d\mu(x) - \int \mathbf{D}_{w} \left( \psi_{w}(y) \right)_{|w=w_{0}} d\nu(y)
$$
\n
$$
= \lim_{N \to \infty} \int \mathbf{D}_{w} \left( \psi_{w}^{supp(\nu),c}(x) \right)_{|w=w_{0}} d\mu_{N}(x) - \int \mathbf{D}_{w} \left( \psi_{w}(y) \right)_{|w=w_{0}} d\nu(y)
$$
\n
$$
= \lim_{N \to \infty} \mathbf{D}_{w} \left( \int \left( \psi_{w}(y(x,w)) + c(x, y(x,w)) \right) d\mu_{N}(x) - \int \psi_{w}(y) d\nu(y) \right)_{|w=w_{0}}
$$
\n
$$
= \lim_{N \to \infty} \mathbf{D}_{w} \left( \frac{1}{N} \sum_{i=1}^{N} \psi_{w}(y(x_{i},w)) - \frac{1}{M} \sum_{j=1}^{M} \psi_{w}(y_{j}) + \frac{1}{N} \sum_{i=1}^{N} c(x_{i}, y(x_{i},w)) \right)_{|w=w_{0}}
$$
\n(10)

where D<sup>w</sup> is the derivative with respect to w, in the first and third equality we applied Leibniz's rule, and in the second equality we used the fact that µ<sup>N</sup> → µ. Since w0, is fixed, with probability one, we get that the last term in [\(10\)](#page-5-0) is equal to

$$
\lim_{N \to \infty} \mathbf{D}_w \left( \frac{1}{N} \sum_{i=1}^N \psi_w(y(x_i, w_0)) - \frac{1}{M} \sum_{j=1}^M \psi_w(y_j) + \frac{1}{N} \sum_{i=1}^N c(x_i, y(x_i, w_0)) \right)_{|w=w_0}
$$
\n
$$
= \lim_{N \to \infty} \mathbf{D}_w \left( \frac{1}{N} \sum_{i=1}^N \psi_w(y(x_i, w_0)) - \frac{1}{M} \sum_{j=1}^M \psi_w(y_j) \right)_{|w=w_0}
$$
\n
$$
= \lim_{N \to \infty} \sum_{j=1}^M \left( \frac{\# \{ \{ x_i, 0 \le i \le N : y(x_i, w_0) = y_j \}}{N} - \frac{1}{M} \right) \mathbf{D}_w \left( \psi_w(y_j) \right)_{|w=w_0},
$$
\n(11)

<span id="page-5-1"></span>where in the [\(11\)](#page-5-1) one can notice that y does not vary with w anymore, and that is why the term D<sup>w</sup> 1 N P<sup>N</sup> <sup>i</sup>=1 c(xi, y(xi, w)) vanishes. This happens because, for small changes in w, the assignments do not change with probability one. The proof of that claim can be found in the appendix.

This proves that the error functions

<span id="page-6-0"></span>
$$
\int \psi_w^{supp(\nu),c}(x)d\mu(x) - \int \psi_w(y) d\nu(y) \tag{12}
$$

and

<span id="page-6-1"></span>
$$
\sum_{j=1}^{M} \left( \frac{\# \{ \{ x_i, 0 \le i \le N : y(x_i, w_0) = y_j \}}{N} - \frac{1}{M} \right) \psi_w(y_j), \tag{13}
$$

where N is picked sufficient big, can be used interchangeably for the "critic". We note that, by applying the theory of Large Deviations (see [\[7\]](#page-16-4)), one can prove that the probability of the distance between the gradients of [\(12\)](#page-6-0) and [\(13\)](#page-6-1), being bigger than some , decays exponential with the number of N.

The cost appearing in [\(13\)](#page-6-1), will be referred from now on as the assignment cost, and it is the one that we used to train our auxiliary network ("assigner"). In the next section we are going to further analyze the idea behind the assignment cost and compare it with the critic cost in WGANs. We conclude with what we believe to be an interesting remark.

Remark 3.2. By taking the derivative of [\(13\)](#page-6-1) one gets

$$
\sum_{j=1}^M \left( \frac{\#\{\{x_i, 0 \le i \le N : y(x_i, w_0) = y_j\}}{N} - \frac{1}{M} \right) \mathbf{D}_w \left( \psi_w(y_j) \right)_{|w=w_0}.
$$

If all points x<sup>i</sup> are assigned equally to every y, then the derivative is equal to zero and therefore the training halts. Although this would be sufficient for the generator to be trained, one can wonder if we end up with an optimal assignment between µ<sup>N</sup> and ν. Trying to answer this question we came up with a theorem that confirms that.

More specifically we have

<span id="page-6-3"></span>Theorem 3.3. Let µ, ν ∈ P(<sup>X</sup> ), ψ ∈ L(µ). We further assume that there exists a unique minimizer <sup>T</sup>e(x) of {c(x, y) + <sup>ψ</sup>(y)}, for <sup>µ</sup> almost every x. Then if <sup>T</sup>e]<sup>µ</sup> <sup>=</sup> ν, we have that (<sup>I</sup> <sup>×</sup> <sup>T</sup>e)]<sup>µ</sup> is an optimal plan.

We note that, by Theorem [7.1,](#page-15-0) if µ is an absolutely continuous measure, ν is purely atomic, and c satisfies Assumption [3.1](#page-5-2) then the map <sup>T</sup><sup>e</sup> is always defined. To reformulate, in order to know if <sup>ψ</sup> is a maximizer in the dual formulation for µ, ν, we only have to check that {c(x, y) + ψ(y)}, has a unique minimizer <sup>T</sup>e(x) for <sup>µ</sup> almost every x, and that minimizer satisfies <sup>T</sup>e]<sup>µ</sup> <sup>=</sup> ν.

# 4 Heuristic comparison between Assignment training and WGANs

Before we proceed with the comparison between WGANs and our method, we would like to share a little bit from the history of our research for educational purposes. We believe that the following will help new researchers, especially those coming from a pure mathematics background, clarify some things about how WGANs work, and avoid our mistakes.

<span id="page-6-2"></span>We start by, once more, reminding the reader about the dual formulation of the transport cost, i.e.

$$
\mathcal{T}_c(\mu,\nu) = \sup_{\psi \in C_b(\mathcal{X})} \left\{ \int \psi^{supp(\nu),c} d\mu(x) - \int \psi d\nu(y) \Big| \psi^{supp(\nu),c}(x) = \inf_{y \in supp(\nu)} \{c(x,y) + \psi(y)\} \right\}.
$$
 (14)

Note that, in order to calculate the dual function of ψ, one has to go through only the points that are in the supp(ν) and not through the whole space X . Our initial approach was to use small batches, in the same way that WGANs are traditionally trained, and with the hope that if the batches come closer then the full distributions of real and generated points will also come closer together. We note that in order to calculate the infimum in a differentiable way we applied a smooth maximum by using the LogSumExp function. Although this approach worked fine with low-dimension datasets having only a few nodes, it failed with datasets like MNIST. What we observed there was the production of blurred idealized versions of the digit.

Further experiments showed that an increase in the size of the batches for training both generator and critic positively increased the image quality. This lead us to believe that approximating the distance will only work when the number of samples is really high. When thinking of the problem as an optimal transport problem this becomes much clearer, as there is the possibility that samples from the closest manifold inside the data might not be in the batch we use for approximation. Furthermore if we think of each image from the MNIST dataset as a point in dimension R <sup>28</sup>x<sup>28</sup> of a probability distribution we would need significantly more samples to accurately capture a distribution or even find a sufficient approximation. As it was pointed out in [\[2\]](#page-16-5) and [\[3\]](#page-16-6), this line of reasoning, i.e. if the batches come closer then the full distributions of real and generated points will also come closer together, for why WGANs do work, is not valid anyway. By applying a simple mass concentration argument, they show, that in order for this argument to be valid, one needs to increase the batch size exponentially with the number of dimensions. Something like that is of course impossible in practice.

In order to understand why the WGAN method works with small batches, we came with the following heuristic explanation. When the critic is fed with some real points, its value value around these points increases, and when it is fed with some generated points, the value around them decreases. This is easy to understand by carefully dissecting the error function

<span id="page-7-0"></span>
$$
\sum_{x_i \sim \mathbb{P}_r} \psi(x_i) - \sum_{y_j \sim \mathbb{P}_{\theta}} \psi(y_j). \tag{15}
$$

Then, roughly speaking, the trained critic is encoding a landscape where the generated points are valleys and the real ones are hills. The generator follows that landscape to "roll down" the generated points to the reals. The idea of the gradient penalty, apart from its mathematical justification, enforces this explanation scheme, because in practice, it smoothens the landscape along the lines between real and fakes. Therefore we hypothesized that it is not the fact that the batches really capture the two distributions, which makes WGANs work, but that:

- When the learning rate is small enough, then it makes no practical difference between applying [\(15\)](#page-7-0) for many consecutive small batches or for a really big one. We believe that this is due to
  - 1. the linearity of the cost
  - 2. the fact that the critic network has enough degrees of freedom such that local changes do not significantly affect the rest of the network.
- Alternating between training critic and generator, is crucial for the generated points to go closer to the real ones.

To test this perception, that it is not the critic cost [\(15\)](#page-7-0) that in every step really captures the distance but the fact that when the learning rate is small enough, then it makes no practical difference between training the critic in many consecutive small batches or in a really big one, we trained WGANs with gradient penalty and with really small batches of 2 or 3 points. Given enough time, the result was almost as good as training with a batch of 64 or 128. At the same time, we also tried to train a perfect critic first and then train the generator, and this method failed even after thousand iterations of the critic.

Now, if one wants to train with a general transportation cost using [\(14\)](#page-6-2), this is not longer possible. In order for the dual of the critic to be defined properly then one has to go through a set of reals that capture well its distribution. If one tries to apply smaller batches the training fails. For visual purposes, we would like to note that unlike in WGANs, in the Assignment method, the assigner never goes through the generated points. Furthermore, the assigner does not create a landscape where real points are high and generated points are low so the generator can use to train. In the assignment method, the assigner increases at real points which are assigned to too many generated points and decreases otherwise. When the assigner is trained to optimality then the training of the generator happens through the assignment and the cost that shapes the assigner.

<span id="page-8-0"></span>Algorithm 1 WGAN2. We use the parameters α = 0.00005, m = 64, ncritic = 5.

Require: α is the learning rate. ncritic, the number of assigner iterations per generator iteration. m, the number of assignments per iteration of the assigner.

Require: w0, initial assigner parameters. θ0, initial generator parameters. X , Matrix containing all of the real samples.

1: while θ has not converged do

```
2: for t = 0, ..., ncritic do
3: for i = 0, ..., m do
4: Sample latent space z ∼ p(z)
5: Ki ← (X[argmin(Aw(X ) + cost(X , Gθ(z))], Gθ(z))
6: L
             i ← −Aw(Ki
                        (0))
7: end for
8: w ← RMSP rop 
                        Dw

                             1
                             m
                               Pm
                                 i=1 L
                                     i −
                                           1
                                         len(X )
                                              P
                                                x∈X Aw(x)

                                                           , w, α
9: end for
10: for i = 0, ..., m do
11: L
          i ← cost g(Ki
                    (0), Ki
                          (1))
12: end for
13: θ ← RMSP rop(Dθ
                       1
                       h
                        Ph
                          i=1 L
                               i
                               , w, α)
14: end while
```

# 5 Psudocode and comparison with WGANs

We have the following comments regarding our psudocode

- When m is relatively small, the whole training behavior resembles this of WGANs. However, one can use a different approach with the choice of m. If m is chosen to be at the same scale with the size of X , then the real distance between real and generated points can be captured, and evenmore achieve prevention of mode collapse. More specifcially, experimenting with various datasets of up to 10000 points, we noticed that 10 times the dataset will suffice. We expect that by some probabilistic arguments, the appropriate size of generate points can be estimated. Regardless of the size of m, the generated sets can be batched.
- Line [4.](#page-8-0) Traditionally the latent distribution p(z) is chosen to be a Gaussian. However we noticed that if we instead choose a collection of Gaussians with small variance the results are much better.
- Line [5](#page-8-0) and [11:](#page-8-0) cost <sup>g</sup> and cost have to coincide from a theoretical point of view. However, in practice, a computationally faster cost can be used for the assigner. For example, SSIM is computationally very demanding, and by using peak signal-to-noise ratio (PSNR) for the critic instead, one can get similar results in a small portion of the time. It also appears that the assigner trains the fastest, if we multiply the cost with a constant such that the diameter of the space is equal to one. This does not change the geometry of the fitted model.

### 5.1 Practical comparison between Assignment method and WGANs.

#### Advantages of Assignment method over WGANs.

1. Since, at every step, an actual estimate for the transport distance can be calculated (when the generated batch is big enough), the method provides a quantitative way to bound from above the full transport distance between the distributions. As a byproduct, this allows in only a few iterations, to check how different parameters affect the training. For example, we noticed that with Fashion MNIST one gets the best approximation when latent dimension is around 250. Contrary, with the classical MNIST dataset, no significant difference appear if we increase the latent dimension further than 100.

- 2. We can approach the original distribution in any desirable degree. Furthermore we can ensure that no mode collapse occurs.
- 3. Depending on the complexity of the generated set and cost function, it is possible for the assigner to be trained to optimality by itself and without any iterations with the generator. This way, we can calculate the transport distance between the two measures, and retrieve the optimal transport map.
- 4. The method does not not depend on the architecture of the network. It can work really well with the simple dense networks unlike the traditional WGANs where the assistance from using convolutional networks is noticeable.

#### Disadvantages of Assignment method over GANs and WGANs.

1. In its current version, the assignment algorithm requires to go through all the real points every time we generate a new point. This makes it quite demanding on computational time. It appears that each assigner training step requires mN computations, where m is the number of generated points and N is the number points in the original dataset. Now if one want to avoid mode collapse, should make m in a similar scale with N, which results to "perfect" training time being of order O(N 2 ).

# 6 Experiments

In the following section, we describe the layout for the experiments that were conducted. We will start by introducing the datasets and giving an intuition why these datasets are useful to compare the performance of different approaches. Afterwards, we will define metrics that can evaluate the performance of the results.

### 6.1 Datasets

In this section, we will describe the datasets that were used for the experiment. We would like to note, that we did not include the standard by now Cifar10 dataset, because we were not able to reproduce the claimed results of the other papers on this dataset at all. We believe that this was solely due to our inability to properly produce the required architecture for the generator. However, we trained our model with a dense generator with a reasonably good outcome. The interested reader, can use the code in the repository to check for themselves.

#### 6.1.1 MNIST

The MNIST dataset is a collection of handwritten digits from 0 to 9 and labels indicating the number it should represent as an integer. The individual images consist of 28x28 greyscale values 70000 images are part of the dataset. For the experiments, we reduce the number of images to 5000 examples upscale them to 32x32. The MNIST dataset is a typical dataset for comparing different GAN models because of their popularity in the machine learning community. Additionally, the numbers are easy to recognize and blurry images can be seen at a glance.

#### 6.1.2 Fashion-MNIST

The fashion-MNIST dataset was introduced in [\[16\]](#page-17-3) as an alternative dataset to the MNIST. The fashion-MNIST is a collection of pictures of clothings. The number of classes is kept the same to MNIST that represent ten different clothing types. The individual images consist of 28x28 greyscale values and the number of examples in the dataset is 70000. For our experiments, we reduce the number of images to 5000 examples and upscale them to 32x32. We chose this dataset for multiple reasons, first we we can visually detect blur in the generated images by looking at the sharpness of transition between clothings and black background. Secondly we can see if details in the image get generated like prints on t-shirts, zippers and wrinkles. Third we think that its interesting to see difference between the results of MNIST compared to this dataset because their main dimensions and pixel ranges are the same.

### 6.2 Metrics

Evaluating the performance of generative models is a nontrivial task. [\[13\]](#page-17-4) discussed the evaluation of generative image models and concluded that no single evaluation metric is accurate, and that the right choice depends on the application at hand. Similarly, in [\[6\]](#page-16-7), the authors concluded, after reviewing 24 quantitative and 5 qualitative measures, that there is no universal measure between model performances. We decided to follow a different route and use Wasserstein-1 as a metric for evaluation, since it functions as an error function for the generator in the case of WGANs. Furthermore, we introduce a second metric that indirectly evaluates the appearance of mode collapse.

#### 6.2.1 Wasserstein-1 metric

The Wasserstein-1 distance will now be used as a metric for evaluating the generated samples after training. By calculating the distance for a large number of samples from the generator and the dataset we can approximate how close both distributions are to each other. For the experiments, we choose to sample ten times the amount of generated points compared to the size of the original dataset to get an accurate representation of the distance between our learned model and the dataset. To find the Wasserstein-1 metric we relied on the external library POT: Python Optimal Transport (see [\[8\]](#page-16-8)) to solve the optimal transport problem that implements the algorithm proposed in "Displacement interpolation using Lagrangian mass transport" [\[5\]](#page-16-9).

#### 6.2.2 Assignment Variance

Apart from the Wasserstein-1 metric to determine how well the model has been trained we propose a metric that is depended on the cost function that the model uses. We evaluate with this metric how well a particular model achieves an equal spread of generated points around each of the real points in the dataset. To do this we take ten times the number of generated points compared to the amount of real points in the dataset. We then use the model specific cost function c and find the closest real point in the dataset. By counting how many generated points get assigned to a point in the real dataset we can determine if the model is spreading the points equally or if mode collapse is occurring in the model with respect to its cost c. To generate a single value we calculate the variance around the perfect result of ten assignments.

$$
\frac{1}{\#reals} * \sum_{i=1}^{\#reals} \sqrt{(\#assignments_i - 10)^2}.
$$
 (16)

# 7 Results and Discussion

In this section we will proceed with the results of our experiments and with our interpretation of them.

![](_page_11_Figure_1.jpeg)

<span id="page-11-0"></span>Figure 3: Generated samples for MNIST with GAN, WGAN and WGAN-GP. The closest real points were chosen by the cost function definition of the model. For vanilla GANs we used the Euclidean distance, since there is no cost function for this model.

![](_page_12_Figure_0.jpeg)

<span id="page-12-0"></span>Figure 4: Generated samples for MNIST with the assignment approach. The closest real points were chosen with respect to the cost function defined by the model.

|                     | GAN   | WGAN  | WGAN-GP | Square | SSIM |
|---------------------|-------|-------|---------|--------|------|
| Wasserstein Metric  | 15.80 | 12.59 | 10.69   | 9.68   | 9.67 |
| Assignment Variance |       | 0.46  | 0.29    | 0.14   | 0.21 |

<span id="page-12-1"></span>Table 1: Metrics applied on MNIST

We generated samples together with the closest real point based on the cost function of the method. Results from the models we use as comparison can be seen in figure [3](#page-11-0) and our results can be seen in [4.](#page-12-0) The original GAN approach seems to only produce two rather similar looking numbers while the other approaches produce a larger variety of numbers. The quality of the images seems similar to us while a little bit sharper for our squared and SSIM assignment. Additionally, we notice that WGAN, GAN-GP and the square assignment seem to produce numbers where pixels inside the lines of the numbers are missing or are not fully white while the SSIM assignment generated images are fully connected. We think this behavior reflects the fact that SSIM optimizes for the structural integrity of the number as well as equal luminance and contrast. The Wasserstein metric in Table [1](#page-12-1) reflects the perceived image quality showing the best results for our method. Then looking at the numbers for the variance from optimal assignment we can see that our methods indeed managed to achieve their training objective the closest by having an equal spread around the dataset points. In conclusion one can say that the experiments for MNIST show what we expected, the square distance is able to move the model closer to the real distribution by having a smoother gradient when points get close while the SSIM Assignment manages to produce perceptual more appealing images.

#### 7.0.2 Fashion MNIST

<span id="page-13-0"></span>![](_page_13_Picture_2.jpeg)

Figure 5: Generated samples for Fashion-MNIST with GAN, WGAN, and WGAN-GP.

![](_page_14_Figure_0.jpeg)

Figure 6: Generated samples for Fashion-MNIST for square Assignment and SSIM assignment.

<span id="page-14-0"></span>

|                     | GAN   | WGAN  | WGAN-GP | Square | SSIM |
|---------------------|-------|-------|---------|--------|------|
| Wasserstein Metric  | 11.03 | 11.19 | 9.15    | 3.40   | 7.17 |
| Assignment Variance |       | 1.99  | 0.82    | 0.01   | 0.05 |

<span id="page-14-1"></span>

|  | Table 2: Metrics for the Fashion-MNIST |
|--|----------------------------------------|
|--|----------------------------------------|

To judge the visual quality, we can check the blurriness of the clothes at the edges of transition from the background and additionally can see if smaller details are present like prints on t-shirts, zippers and wrinkles. The results in figure [5](#page-13-0) show the output of the models for comparison and [6](#page-14-0) the results of our approaches. The overall visual quality of the images seems to be equal except for WGAN showing artifacts and general blurriness. This might show that clipping the weights of the network prevents it from learning the more complicated Fashion-MNIST distribution function. Additionally GAN seems to show no obvious mode collapse that is in strong contrast to the MNIST results. We interpret that discrepancy as an indicator that the original GAN is very sensitive to the choice of the hyperparameters, and we are in no way claiming that original GAN is not able to capture the MNIST dataset. Another observation is that all GANs and even WGAN-GP, are producing points that seem to be far different from the real dataset but at the same time look realistic suggesting that it learned a model that found some underlying representation of the dataset. When looking at the details inside the clothings one can see that WGAN-GP as well as our approach produces some details but especially the SSIM assignment is reproducing a lot of the details. When examining the metrics in Table [2](#page-14-1) we can see that both of our approaches generate samples that are closer to the real distribution measured by the Wasserstein-1 distance. When looking at the variance from optimal assignment one can see that how well the approach respectively achieves its objective. For both of our assignment methods we can see that they generate an nearly equal amount of points around the real data points.

### 7.1 Conclusion

We explored the idea of training GNs with various optimal transport costs. As the first cost we choose the squared Euclidean norm, that should have a smoother gradient for points that lie close to each other. The second cost was the structural similarity index proposed by [\[15\]](#page-17-5), that tries to assess image quality by accounting for luminance, contrast and structure in the image that better reflect human perception of image quality. Choosing this cost allows us to train our generative model for generating images of high perceptual quality. To train generative models with these new costs a novel training procedure was introduced that allows us to use these costs but they can be exchanged for any metric. The downside is that the computational effort for a training step increases superlinear with respect to the number of points in the dataset. Our experiments show that it is indeed possible to train a model with our proposed cost and decrease the distance between the generated points and the points in the dataset compared to approaches by other authors. Furthermore, the experiment results with the SSIM cost shows that the cost indeed influences the appearance of the generated images. The Wasserstein-1 metric applied on the results, further shows that we are able to better approximate the distribution of both MNIST as well Fashion-MNIST datasets when using the assigning approach.

Several new research directions can build upon our work. There can be follow up work that tries to tackle the computational burden introduced by our approach. We think that the largest improvement can be achieved by exploring more efficient ways to find the closest neighbours between the real and generated points that are necessary for our algorithm. Secondly on can try new costs that better reflect the training objective one tries to achieve. Especially with datasets where the Euclidean distance is a poor choice for assessing the similarity between data points. At last, one can look at the architecture choices made for the neural networks, the optimizers and the hyperparameters to either optimize them in general or for a given dataset and training objective.

Our repository for the experiment can be found in https://github.com/artnoage/Optimal-Transport-GAN.

# Appendix

<span id="page-15-0"></span>Theorem 7.1. Let ψ<sup>w</sup> : X → R, a collection of functions parameterized by w. Let also assume that for every y ∈ X , ψw(y) is a continuous function with respect to w, and that c satisfies the Assumption [3.1.](#page-5-2) Finally, let P be a distribution in X , that is absolutely continuous with respect to the Lebesgue measure.

For w<sup>0</sup> and a finite set Y, we have that for almost every x ∈ X , the expression

$$
\psi_{w_0}(y) + c(x, y)
$$

has a unique minimizer in Y. Evermore with probability one, for every independent random sample, with respect to P of points {x1, .., xn, . . . } in X, we have that it exists δ({x1, . . . , xn}), such that

$$
\arg\min_{Y} \{ \psi_{w_0}(y) + c(x_i, y) \} = \arg\min_{Y} \{ \psi_w(y) + c(x_i, y) \}, \quad \forall w \in B(w_0, \delta(\{x_1, \dots, x_n\})).
$$
 (17)

Proof. Let assume that the set <sup>X</sup>e, of all points that have multiple minimizers has positive Lebesgue measure. Then, since <sup>Y</sup> is finite, there exists at least one <sup>y</sup><sup>0</sup> <sup>∈</sup> <sup>Y</sup> such that <sup>X</sup>e<sup>y</sup><sup>0</sup> of the points that are minimizers for

$$
\psi_{w_0}(y_0) + c(x, y_0)
$$

has positive Lebesgue measure. From that, we can induce that the set

$$
\{x \in \mathcal{X} : c(x, y_0) = \{\psi_{w_0}(y_0) + c(x_0, y_0)\} - \psi_{w_0}(y_0) = c(x_0, y_0)\},\
$$

where <sup>x</sup><sup>0</sup> is an arbitrary but fixed point in <sup>X</sup>e<sup>y</sup><sup>0</sup> , has positive measure. contradicts the assumption [3.1.](#page-5-2)

Now since the points x1, . . . , xn, . . . are sampled independently from P, with probability one, the expression ψ<sup>w</sup><sup>0</sup> (y) + c(xi, y), has unique minimizer y(xi), and further more it exists (xi), such that

$$
\psi_{w_0}(y) + c(x_i, y) > \psi_{w_0}(y(x_i)) + c(x_i, y(x_i)) + \epsilon(x_i), \quad \forall y \in Y \setminus \{y(x_i)\}.
$$
 (18)

Now if we pick δ({x1, . . . , xn}) such that

$$
|f_w(y_i)-f_{w_0}(y_i)| < \min_{x_i} \epsilon(x_i),
$$

we get the result.

We conclude with the proof of Theorem [3.3.](#page-6-3)

Proof of Theorem [3.3.](#page-6-3) Let <sup>Q</sup> be an optimal plan between <sup>µ</sup> and ν. By definition of T , <sup>e</sup> we have

$$
\psi(\widetilde{T}(x)) + c(x, \widetilde{T}(x)) = \psi^{supp(\nu),c}(x) = \inf_{y \in supp(\nu)} \{ \psi(y) + c(x,y) \} \leq \psi(y) + c(x,y) \quad \forall y \in supp(\nu).
$$

By integrating with respect to Q, we have

$$
\int \psi(\widetilde{T}(x)) + c(x, \widetilde{T}(x))dQ \le \int (c(x, y) + \psi(y)) dQ,
$$

which gives

$$
\int \psi(\widetilde{T}(x))d\mu + \int c(x,\widetilde{T}(x))d\mu \leq \int \psi(y)d\nu + \int c(x,y)dQ.
$$

Since <sup>T</sup>e]<sup>µ</sup> <sup>=</sup> ν, the last inequality gives us

$$
\int c(x,\widetilde{T}(x))d\mu \leq \int c(x,y)dQ,
$$

which proves that <sup>T</sup><sup>e</sup> is an optimal map.

# References

- <span id="page-16-1"></span>[1] Martin Arjovsky, Soumith Chintala, and L´eon Bottou. Wasserstein GAN. jan 2017.
- <span id="page-16-5"></span>[2] S Arora, R Ge, Y Liang, T Ma, Y Zhang Proceedings of the 34th, and undefined 2017. Generalization and equilibrium in generative adversarial nets (gans). dl.acm.org.
- <span id="page-16-6"></span>[3] Sanjeev Arora and Yi Zhang. Do GANs actually learn the distribution? An empirical study. jun 2017.
- <span id="page-16-2"></span>[4] Gil Avraham, Yan Zuo, and Tom Drummond. Parallel Optimal Transport GAN \*. Technical report.
- <span id="page-16-9"></span>[5] Nicolas Bonneel, Michiel van de Panne, Sylvain Paris, and Wolfgang Heidrich. Displacement interpolation using lagrangian mass transport. ACM Trans. Graph., 30(6):158:1–158:12, December 2011.
- <span id="page-16-7"></span>[6] Ali Borji. Pros and cons of gan evaluation measures. Computer Vision and Image Understanding, 179:4165, Feb 2019.
- <span id="page-16-4"></span>[7] A Dembo and O Zeitouni. Large Deviations Techniques and Applications, volume 38 of Stochastic Modelling and Applied Probability. Springer, New York, 2nd edition, 1987.
- <span id="page-16-8"></span>[8] R'emi Flamary and Nicolas Courty. Pot python optimal transport library, 2017.
- <span id="page-16-0"></span>[9] Ian Goodfellow, Jean Pouget-Abadie, Mehdi Mirza, Bing Xu, David Warde-Farley, Sherjil Ozair, Aaron Courville, and Yoshua Bengio. Generative adversarial nets. In Advances in neural information processing systems, pages 2672–2680, 2014.
- <span id="page-16-3"></span>[10] Ishaan Gulrajani, Faruk Ahmed, Martin Arjovsky, Vincent Dumoulin, and Aaron C. Courville. Improved Training of Wasserstein GANs, 2017.

- <span id="page-17-0"></span>[11] Huidong Liu, Xianfeng Gu, and Dimitris Samaras. Wasserstein GAN with Quadratic Transport Cost. Technical report.
- <span id="page-17-2"></span>[12] Huidong Liu, Xianfeng GU, and Dimitris Samaras. A Two-Step Computation of the Exact GAN Wasserstein Distance. ICML, pages 3165–3174, jul 2018.
- <span id="page-17-4"></span>[13] Lucas Theis, A¨aron van den Oord, and Matthias Bethge. A note on the evaluation of generative models. arXiv preprint arXiv:1511.01844, 2015.
- <span id="page-17-1"></span>[14] C´edric Villani. Optimal transport: old and new. page 998, 2008.
- <span id="page-17-5"></span>[15] Zhou Wang, A. C. Bovik, H. R. Sheikh, and E. P. Simoncelli. Image quality assessment: From error visibility to structural similarity. Trans. Img. Proc., 13(4):600–612, April 2004.
- <span id="page-17-3"></span>[16] Han Xiao, Kashif Rasul, and Roland Vollgraf. Fashion-mnist: a novel image dataset for benchmarking machine learning algorithms. CoRR, abs/1708.07747, 2017.