# Analysis of Training Generative Networks with Arbitrary Optimal Transport costs.

**Authors**: Vaios Laschos, Jan Tinapp, Klaus Obermayer
**Year**: 2020
**Venue**: Preprint (arXiv submission implied by format)
**Domain**: Computer Science
**Analysis Date**: 2025-07-03T16:25:39.130562

## Executive Summary

This paper introduces a novel algorithm, termed the 'Assignment Method', for training generative networks (GNs) by minimizing the optimal transport (OT) distance for an arbitrary, user-defined cost function. The core innovation is an auxiliary neural network, the 'assigner', which learns the Kantorovich potential from the dual formulation of the OT problem. Unlike Wasserstein GANs (WGANs), which are implicitly tied to the Euclidean distance (leading to the Wasserstein-1 metric), this method allows for the explicit use of any cost function, such as the squared Euclidean distance (for the Wasserstein-2 metric) or perceptual metrics like the Structural Similarity Index (SSIM) for images.

The training process involves two main steps. First, the assigner network is trained to balance the assignments of generated data points to real data points, ensuring that, in expectation, each real point is the target for an equal number of generated points. This is achieved by updating the assigner's potential based on assignment counts. Second, the generator is trained to minimize the transport cost between its outputs and their assigned real targets. The authors provide a mathematical justification for the method's computational feasibility, showing that the gradient of the complex dual objective can be simplified to a tractable 'assignment cost'.

Experiments on MNIST and Fashion-MNIST datasets demonstrate that the Assignment Method, using both squared Euclidean and SSIM costs, can achieve lower Wasserstein-1 distances to the true data distribution compared to standard GANs and WGANs. The use of SSIM is shown to produce visually sharper and more structurally coherent images. The primary drawback acknowledged by the authors is the method's high computational complexity, which scales with the product of the number of generated samples and the size of the real dataset, making it challenging for very large datasets.

## Phase 1: Rapid Reconnaissance

### Problem Addressed
The primary problem addressed is the limitation of existing Wasserstein GANs (WGANs) to a single, implicit metric (Wasserstein-1, based on Euclidean distance). This prevents the use of more suitable, domain-specific cost functions for measuring the distance between generated and real data distributions, which could improve the quality and relevance of the generated samples.

### Core Contribution
The core contribution is a new training algorithm, the 'Assignment Method', that enables generative networks to be trained by minimizing the optimal transport distance for any arbitrary, user-specified cost function. This is achieved through a novel use of an auxiliary network that learns the dual potential by balancing assignments, effectively decoupling the training process from the constraints of the Wasserstein-1 metric.

### Initial Assessment
The paper is highly relevant and credible. It addresses a significant and well-understood limitation in the field of generative modeling. The proposed method is theoretically grounded in optimal transport theory, and the authors provide a clear mathematical justification for their approach. They are transparent about the method's major limitation (computational cost) and support their claims with experimental evidence, including comparisons to established baselines. The work serves as a strong proof-of-concept for a more flexible approach to training GANs.

### Claimed Contributions
- A proof of concept that the dual formulation for arbitrary optimal transport problems can be used to create an applicable algorithm for training generative networks, moving beyond the Wasserstein-1 case.
- A rigorous mathematical justification showing that the gradient of the dual objective can be simplified by exchanging the gradient with the arg inf operator, making the approach computationally feasible. This avoids evaluating the critic on generated points and allows for better approximation of the theoretical error function.

### Structure Overview
The paper is well-structured. It begins with an introduction to GANs and WGANs, motivating the need for arbitrary cost functions. Section 2 provides the necessary background on optimal transportation theory. Section 3 presents the mathematical justification for the proposed 'Assignment Method'. Section 4 offers a heuristic comparison between the new method and WGANs. Section 5 provides pseudocode and a practical comparison of advantages and disadvantages. Sections 6 and 7 detail the experimental setup, results, and discussion, followed by a conclusion and an appendix with proofs.

### Key Findings
- The proposed 'Assignment Method' successfully trains generative networks using arbitrary cost functions like squared Euclidean distance and SSIM.
- Using the squared Euclidean distance (related to Wasserstein-2) leads to faster and more stable gradient descent, resulting in a lower final Wasserstein-1 distance compared to WGANs.
- Using the SSIM cost function produces images that are perceptually sharper and more structurally sound, demonstrating the benefit of using domain-specific costs.
- The method can prevent mode collapse by ensuring generated points are spread evenly across the real data distribution, a property verified by their proposed 'Assignment Variance' metric.
- The training of the assigner network requires iterating over the entire real dataset for each batch of generated points, leading to a high computational cost of O(mN), where m is the generated batch size and N is the real dataset size.

## Research Context

**Historical Context**: The paper builds upon the progression of generative models from the original Generative Adversarial Networks (GANs) by Goodfellow et al. (2014), which suffered from training instability and mode collapse, to Wasserstein GANs (WGANs) by Arjovsky et al. (2017).

**Current State**: WGANs stabilized GAN training by using the Wasserstein-1 distance as a loss function. This was a major breakthrough. However, the standard WGAN framework is intrinsically linked to the 1-Lipschitz constraint, which corresponds to using the Euclidean distance as the ground cost in the underlying optimal transport problem.

**Prior Limitations**: The key limitation of WGANs and their variants (like WGAN-GP) is their inability to easily incorporate arbitrary transport cost functions. While some works claim to use other costs, the authors argue these are typically just WGANs with an added regularization term, rather than a true implementation of a different OT problem.

**Advancement**: This paper provides a novel framework that directly implements the dual formulation of the general optimal transport problem for any continuous cost function `c`. This generalizes the WGAN approach and allows the cost to be tailored to the data's intrinsic geometry (e.g., perceptual similarity for images).

## Methodology Analysis

### Key Technical Innovations
- Introduction of the 'assigner' network (ψ_w) which learns the Kantorovich potential of the OT problem.
- A novel loss function for the assigner (the 'assignment cost', Eq. 13) based on balancing the number of generated points assigned to each real point, rather than directly maximizing the OT dual objective.
- A mathematical justification (Theorem 7.1) for simplifying the gradient calculation by exploiting the piecewise constant nature of the `arg inf` assignment function, making the method computationally tractable.

### Mathematical Framework
- The method is rooted in the Kantorovich dual formulation of the optimal transport problem (Theorem 2.3).
- The core of the method is to find the potential ψ that maximizes the dual objective: `sup_ψ { ∫ ψ^c dμ - ∫ ψ dν }`, where `ψ^c(x) = inf_y {c(x,y) + ψ(y)}`.
- The paper proves that the gradient of this objective with respect to the parameters of ψ can be approximated by a simpler 'assignment cost' that only depends on the counts of assignments, under certain assumptions.

## Domain-Specific Analysis (Computer Science)

### Problem Formulation
The problem is framed as learning a generator `G_θ` such that the distribution of its outputs `P_θ` minimizes the optimal transport distance `T_c(P_θ, P_r)` to the real data distribution `P_r` for an arbitrary cost `c`.

### Algorithm
Algorithm 1 ('WGAN2', better named 'Assignment GAN') details a two-timescale update rule. An inner loop trains the 'assigner' network `ψ_w` for `ncritic` steps to balance assignments. An outer loop updates the generator `G_θ` by moving generated points towards their assigned real targets to minimize the cost `c`.

### Evaluation
The evaluation uses standard image datasets (MNIST, Fashion-MNIST). Performance is measured quantitatively with the Wasserstein-1 distance (a standard measure of distribution similarity) and a novel 'Assignment Variance' metric to assess how well the method achieves its own objective of balanced assignments. Visual inspection of generated samples is also used.

### Reproducibility
The authors provide pseudocode, key hyperparameters (α, m, ncritic), and a link to a GitHub repository, which strongly supports reproducibility.

### Broader Impact
The work could enable the development of highly specialized generative models for various scientific and creative domains by allowing practitioners to inject domain knowledge through the choice of the cost function. However, its practical impact is currently limited by its computational demands.

## Critical Examination

### Assumptions
- Assumption 3.1: The level sets of the cost function `c(x, ·)` have Lebesgue measure zero. This is crucial for ensuring unique minimizers in the assignment step and holds for all norms.
- The distribution of the generator, `μ`, is absolutely continuous with respect to the Lebesgue measure. This is a strong assumption, as GANs are known to learn distributions on low-dimensional manifolds.
- The number of generated samples `m` used to train the assigner is 'sufficiently big' to approximate the true distribution. The paper suggests `m` should be on the order of `N` (real dataset size) to prevent mode collapse.

### Limitations
- Computational Complexity: The algorithm has a high computational cost, described as O(mN) per assigner step, as it requires finding the minimum cost assignment over all `N` real points for each of the `m` generated points. This makes it impractical for large datasets.
- Scalability: The need to access the entire real dataset `X` in every assigner step poses a significant memory and computational bottleneck, limiting scalability.
- Limited Experiments: The experiments are conducted on relatively simple, low-resolution datasets (MNIST, Fashion-MNIST). The authors admit they were unable to produce results on more complex datasets like Cifar10.

### Evidence Quality
- The quantitative evidence (lower W-1 distance) is strong, showing superior performance to baselines on the tested datasets.
- The qualitative evidence (visual inspection of generated images) supports the hypothesis that the SSIM cost leads to better perceptual quality.
- The theoretical justification is the strongest part of the paper, with clear theorems and derivations, although some details rely on the appendix or are stated without full proof (e.g., the appeal to Large Deviations theory).

## Phase 2: Deep Dive - Technical Content

### Mathematical Concepts
- **Optimal Transport Distance (Tc)** (Category: metric): The minimum cost to transport mass from one probability distribution (μ) to another (ν), given a cost function c(x,y). Defined in Definition 2.2.
- **Kantorovich Duality** (Category: principle): A fundamental theorem in optimal transport that provides a dual formulation for the transport problem, recasting it as a maximization problem over potential functions (φ, ψ). Stated in Theorem 2.3.
- **c-transform (ψ^c)** (Category: operator): The Legendre-Fenchel type transform of a potential function ψ, defined as ψ^c(x) = inf_y {c(x,y) + ψ(y)}. It is a key component of the dual formulation.
- **Wasserstein-1 Distance (W1)** (Category: metric): A specific case of the optimal transport distance where the cost function c(x,y) is the Euclidean distance d(x,y). Its dual form involves 1-Lipschitz functions.
- **Wasserstein-2 Distance (W2)** (Category: metric): Related to the optimal transport distance where the cost function is the squared Euclidean distance, c(x,y) = d(x,y)^2.
- **Push-forward measure (T#μ)** (Category: operator): A measure induced on a space Y by mapping a measure μ from space X via a map T. Defined in Definition 2.1.
- **Borel Measure** (Category: theory): A measure defined on the σ-algebra of Borel sets of a topological space. The paper considers probability measures on a compact metric space.
- **arg inf** (Category: operator): The operator that returns the argument (input value) that minimizes a function. Used in Eq. 9 to define the assignment map.

### Methods
- **Assignment Method** (Type: algorithmic): The novel training procedure proposed in the paper. It uses an 'assigner' network to learn the OT potential by balancing assignments between generated and real data, and then trains the generator to minimize the user-specified transport cost based on these assignments.
- **WGAN with Weight Clipping** (Type: algorithmic): The original WGAN method by Arjovsky et al. used as a baseline. It enforces the 1-Lipschitz constraint on the critic by clipping its weights.
- **WGAN with Gradient Penalty (WGAN-GP)** (Type: algorithmic): An improved WGAN method by Gulrajani et al. used as a baseline. It enforces the Lipschitz constraint by adding a penalty term to the critic's loss based on the gradient norm.
- **LogSumExp** (Type: computational): Mentioned as a technique to create a smooth, differentiable approximation of the infimum operator, which was used in the authors' initial, unsuccessful attempts.

### Algorithms
- **Algorithm 1 (WGAN2 / Assignment GAN)** (Purpose: To train a generator G_θ and an assigner ψ_w to minimize the optimal transport distance T_c between the generated and real distributions for an arbitrary cost c.)
  - Key Idea: Iteratively train the assigner and the generator. Assigner training: for a batch of `m` generated points, find the best real-data assignment for each by minimizing `c(x,y) + ψ_w(y)`. Update `w` to equalize the number of assignments per real point. Generator training: for a new batch of generated points, find their assignments using the current assigner, and update `θ` to minimize the transport cost `c` for those assignments.
  - Complexity: The assigner update step has a complexity of O(m * N * C_cost + m * N * C_ψ), where `m` is the generated batch size, `N` is the real dataset size, `C_cost` is the cost of evaluating c(x,y), and `C_ψ` is the cost of evaluating ψ_w(y). If `m` scales with `N`, the complexity is roughly O(N^2).

## Critical Analysis Elements

## Evaluation & Validation

**Datasets**: MNIST and Fashion-MNIST, each reduced to 5000 examples and upscaled to 32x32.

**Metrics**: 1. **Wasserstein-1 Metric**: Calculated post-training using the POT library to measure the distance between the final generated distribution and the real data distribution. 2. **Assignment Variance**: A novel metric proposed by the authors to measure how evenly the generated points are assigned to the real points, indicating the absence of mode collapse with respect to the cost function.

**Baselines**: Vanilla GAN, WGAN (with weight clipping), and WGAN-GP (with gradient penalty).

**Results**: The proposed method with both 'Square' (squared Euclidean) and 'SSIM' costs achieved lower (better) Wasserstein-1 scores than all baselines on both datasets. It also achieved significantly lower Assignment Variance, indicating it successfully met its training objective.

## Proof Scrutiny (for Mathematical Papers)

**Proof Strategy**: The main theoretical argument hinges on justifying the simplification of the gradient of the dual objective (Eq. 12) into the assignment cost (Eq. 13). The strategy is to show that the `arg inf` map `y(x, w)` is piecewise constant with respect to `w`. This makes its derivative zero almost everywhere, allowing the derivative to be passed inside the sum and eliminating the complex `c(x, y(x,w))` term from the gradient calculation.

**Key Lemmas**: Theorem 7.1 in the appendix is the key result. It establishes that under Assumption 3.1, the minimizer `y(x,w)` is unique for almost every `x`, and for any finite sample of points, the assignments are stable in a small neighborhood of the weight vector `w`. This provides the formal justification for the gradient simplification.

**Potential Gaps**: The argument relies on `N` (number of generated samples) being large enough for the empirical distribution to be a good proxy for the true distribution. The paper appeals to Large Deviations theory to formalize this but does not provide the full argument. The assumption that the generator's distribution is absolutely continuous is strong and may not hold in practice for GANs.

## Phase 3: Synthesis & Future Work

### Key Insights
- The training of GANs via optimal transport can be generalized beyond the Wasserstein-1 metric by reframing the dual problem as an assignment-balancing task.
- The choice of cost function is not merely a theoretical detail but has a direct, practical impact on the qualitative nature of the generated samples (e.g., SSIM improves structural integrity).
- A direct approximation of the OT distance requires a global view of the distributions, challenging the paradigm of small-batch training common in GANs and suggesting why WGANs might work via a different heuristic (landscape shaping) rather than true distance approximation.
- There is a fundamental trade-off between the flexibility of the transport cost and the computational complexity of the training algorithm.
- The generator and the 'critic' (or 'assigner') can have a more cooperative relationship than the adversarial one in original GANs. Here, the assigner provides explicit targets for the generator to move towards.

### Future Work
- Developing more efficient algorithms to address the computational burden, possibly through approximate nearest neighbor search techniques adapted for the `c(x,y) + ψ(y)` metric.
- Exploring the use of novel, domain-specific cost functions for different data modalities beyond images, such as in chemistry, physics, or 3D modeling.
- Investigating architectural choices for the generator and assigner, as well as hyperparameter optimization, to improve performance and efficiency.
- Formalizing the relationship between the number of generated samples (`m`) and the real dataset size (`N`) required to guarantee convergence and prevent mode collapse.

### Practical Implications
- If the computational issues can be mitigated, this method would allow practitioners to inject specific domain knowledge into the GAN training process by designing custom cost functions.
- It could lead to generative models that produce outputs optimized for specific quality criteria, such as perceptual quality in images, physical plausibility in scientific simulations, or functional properties in material design.
- The ability to calculate a meaningful transport distance during training provides a quantitative tool for model selection and hyperparameter tuning, which is often a difficult task for GANs.

## Context & Connections

### Research Areas
- Generative Adversarial Networks (GANs)
- Optimal Transport
- Generative Modeling
- Machine Learning
- Computer Vision

### Innovations
- The 'Assignment Method': A novel training framework for GANs based on balancing assignments.
- Generalization of GAN training to arbitrary optimal transport costs.
- The 'Assignment Variance' metric for evaluating mode collapse with respect to a given cost function.

### Applications
- **Domain**: Computer Vision
  - Use Case: Image Generation
  - Impact: Allows for generating images that are optimized for perceptual quality (using costs like SSIM) rather than pixel-wise error, potentially leading to more realistic and visually appealing results.

### People Mentioned
- Ian Goodfellow
- Jean Pouget-Abadie
- Mehdi Mirza
- Martin Arjovsky
- Soumith Chintala
- Léon Bottou
- Ishaan Gulrajani
- Cédric Villani
- Zhou Wang

### Institutions Mentioned
- Technische Universität Berlin

### Theoretical Results
- Theorem 2.3 (Dual formulation): States the Kantorovich dual formulation for the general optimal transport problem.
- Theorem 3.3: Proves that if the assignment map `T_e` pushes the generated measure `μ` to the real measure `ν`, then the transport plan is optimal. This validates the training objective of the assigner.
- Theorem 7.1: Shows that under mild conditions, the assignment map `y(x,w)` is unique for almost every `x` and is locally constant with respect to the assigner's weights `w`, which is the key to the method's computational feasibility.

### Related Concepts
- Mode Collapse
- Kantorovich-Rubinstein Duality
- Gradient Penalty
- Weight Clipping
- Perceptual Loss Functions
- Large Deviations Theory

### Connections to Other Work
**Builds On**:
- Goodfellow et al., 'Generative adversarial nets' (2014) - The foundational GAN concept.
- Arjovsky et al., 'Wasserstein GAN' (2017) - The use of optimal transport (specifically W-1) to stabilize GAN training.
- Villani, 'Optimal transport: old and new' (2008) - The core mathematical theory of optimal transport.

**Related To**:
- Liu et al., 'Wasserstein GAN with Quadratic Transport Cost' - Another work attempting to use non-Euclidean costs, which the authors claim is a regularized WGAN rather than a true general OT method.
- Gulrajani et al., 'Improved Training of Wasserstein GANs' (2017) - The WGAN-GP baseline, which provides a more stable way to enforce the Lipschitz constraint than the original.

## Thinking Patterns Observed

**First Principles Thinking**: The authors go back to the fundamental dual formulation of optimal transport (Theorem 2.3) rather than incrementally modifying the existing WGAN algorithm. They re-derive a training objective from these principles.

**Systems Thinking**: The paper provides a heuristic analysis of the entire GAN/WGAN/Assignment-Method system, explaining why each works. They contrast the 'landscape shaping' heuristic of WGANs with their 'assignment balancing' mechanism, showing an understanding of the dynamics of the whole training process.

**Abstraction**: The method abstracts the cost function `c` away from the core algorithm, treating it as a plug-and-play component. This generalization is a key conceptual leap.

## Quality Assessment

**Coherence**: The paper is highly coherent. The motivation, theory, algorithm, and experiments all align to support the central thesis. The argument flows logically from problem to solution.

**Completeness**: The paper is very complete in its theoretical justification, providing proofs for its key claims in the appendix. However, it is less complete in its experimental validation, which is restricted to simple datasets.

**Bias**: The authors are upfront about the limitations of their method, particularly the high computational cost. They avoid overstating their claims and acknowledge areas for future improvement. There is no obvious bias.

---
*Analysis performed on: 2025-07-03T16:25:39.130562*
