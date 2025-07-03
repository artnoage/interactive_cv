# Analysis of Universal Neural Optimal Transport

**Authors**: Jonathan Geuter, Gregor Kornhardt, Ingimar Tomasson, Vaios Laschos
**Year**: 2025
**Venue**: Proceedings of the 42nd International Conference on Machine Learning (ICML)
**Domain**: Computer Science
**Analysis Date**: 2025-07-03T16:08:45.862358

## Executive Summary

This paper introduces Universal Neural Optimal Transport (UNOT), a novel framework for rapidly approximating solutions to entropic Optimal Transport (OT) problems. The core challenge addressed is the high computational cost of traditional iterative solvers like the Sinkhorn algorithm, which is a bottleneck in many machine learning applications. UNOT reframes the problem as learning a mapping from pairs of probability measures to the dual potentials of their OT problem. To achieve this, it employs a Fourier Neural Operator (FNO), an architecture that is invariant to the discretization of the input measures, allowing UNOT to process distributions of varying resolutions.

The UNOT framework consists of two main components trained adversarially: a solver network (S_phi, the FNO) that predicts the dual potentials, and a generator network (G_theta) that creates challenging pairs of distributions for training. The training is self-supervised, using a bootstrapping loss where the solver is trained to predict the result of a few Sinkhorn iterations initialized with its own previous prediction. This avoids the need for ground-truth solutions. The authors provide a strong theoretical foundation, proving the universality of their generator and the validity of the bootstrapping loss. Empirically, UNOT demonstrates high accuracy in predicting OT distances and plans across diverse datasets and domains (Euclidean and spherical), significantly outperforming existing methods. A key practical result is its use as a state-of-the-art initializer for the Sinkhorn algorithm, achieving speedups of up to 7.4x.

## Phase 1: Rapid Reconnaissance

### Problem Addressed
The high computational cost of solving Optimal Transport (OT) problems, especially when they need to be solved repeatedly for many different pairs of distributions, as is common in various machine learning applications. Existing fast approximation methods often sacrifice accuracy, while previous neural approaches are typically limited to fixed-size inputs from a specific data distribution.

### Core Contribution
The development of UNOT, a universal neural OT solver that can accurately and rapidly predict entropic OT distances and plans for a given cost function, across different datasets and for discrete measures of variable resolutions. This is achieved by using a discretization-invariant Fourier Neural Operator trained with a novel adversarial, self-supervised bootstrapping objective.

### Initial Assessment
The paper is highly relevant and credible. It addresses a significant and well-known problem in computational OT. The proposed solution is novel, combining Fourier Neural Operators with an innovative adversarial training scheme. The authors provide strong theoretical justifications for their design choices and back up their claims with extensive and convincing experiments against relevant baselines. The work appears to be a significant advancement in the field of amortized optimization for OT.

### Claimed Contributions
- UNOT, the first neural OT solver capable of generalizing across datasets and input dimensions.
- A generator network G_theta that can provably generate any discrete distribution of a fixed dimension.
- A self-supervised bootstrapping loss that provably minimizes the loss against the ground truth dual potentials.
- Demonstration that UNOT accurately predicts OT distances across various datasets, costs, and domains with low error.
- Approximation of Wasserstein geodesics and barycenters, showing UNOT captures the geometry of Wasserstein space.
- A new state-of-the-art initialization for the Sinkhorn algorithm, providing significant speedups.

### Structure Overview
The paper is well-structured. Section 1 introduces the problem and contributions. Section 2 provides background on Optimal Transport and the Sinkhorn algorithm. Section 3 details the UNOT methodology, including the theoretical justification for using FNOs (Prop. 2), the generator design (Thm. 3), and the adversarial bootstrapping training algorithm (Prop. 5). Section 4 presents a comprehensive set of experiments validating UNOT's performance on various tasks (distance prediction, barycenters, geodesics, gradient flows). Section 5 discusses related work, and Section 6 concludes with a summary and future directions. The appendix provides proofs and further experimental details.

### Key Findings
- UNOT can predict entropic OT distances with a relative error of only 1-3% after a single Sinkhorn iteration, vastly outperforming standard initializations.
- Initializing the Sinkhorn algorithm with UNOT's prediction leads to significant acceleration, with speedups of up to 7.4x compared to the standard implementation.
- The use of Fourier Neural Operators (FNOs) allows UNOT to successfully generalize across measures of different resolutions (from 10x10 to 64x64 in experiments).
- UNOT accurately captures the geometry of the Wasserstein space, enabling high-quality approximation of Wasserstein barycenters and geodesics, even outperforming specialized models like GeONet.
- The adversarial training scheme with a generator and a bootstrapping loss is effective for training the solver without requiring a pre-computed dataset of OT solutions.
- The framework is versatile and can be adapted to different domains (e.g., Euclidean square, sphere) by swapping the FNO with a domain-appropriate variant (e.g., Spherical FNO).

## Research Context

**Historical Context**: Optimal Transport, a field with roots in the 18th century, has become a powerful tool in modern machine learning. The introduction of entropic regularization and the Sinkhorn algorithm (Cuturi, 2013) made OT computationally feasible for larger problems, leading to its widespread adoption.

**Current State**: Despite the Sinkhorn algorithm, computing OT remains a bottleneck in applications requiring repeated calculations (e.g., generative models, single-cell biology). Research has focused on faster approximations, like sliced-Wasserstein distances, or on learning to accelerate solvers.

**Prior Limitations**: Previous attempts to learn OT solvers had significant limitations. 'Meta OT' (Amos et al., 2023) was tied to a specific dataset and input dimension. Other methods like Gaussian initialization (Thornton & Cuturi, 2022) are only applicable to specific cost functions (squared L2). There was no general-purpose, fast neural solver that could handle variable resolutions and generalize across datasets.

**Advancement**: UNOT overcomes these limitations by introducing a 'universal' solver for a given cost function. Its key innovation is the use of discretization-invariant Fourier Neural Operators, which allows it to generalize across input resolutions and datasets, a major step forward from prior work.

## Methodology Analysis

### Key Technical Innovations
- Framing the OT problem as learning a continuous operator from pairs of measures to dual potentials, and using a Fourier Neural Operator (FNO) to approximate this operator.
- A novel adversarial training loop involving a generator (G) and a solver (S), where G learns to create 'hard' OT problems to train S.
- A self-supervised bootstrapping loss, where the training target for the solver is generated by running a few Sinkhorn iterations initialized with the solver's own output. This avoids the costly computation of ground-truth solutions.

### Mathematical Framework
- The framework is built on the theory of entropic Optimal Transport, particularly its dual formulation.
- Proposition 2 provides the theoretical justification for using a discretization-invariant architecture by showing that the dual potentials of discrete measures converge uniformly to their continuous counterparts.
- Theorem 3 proves that the generator network, based on a ResNet-like architecture, is universal and can generate any pair of discrete distributions, ensuring comprehensive training.
- Proposition 5 uses the contraction property of the Sinkhorn operator in the Hilbert projective metric to prove that minimizing the bootstrapping loss effectively minimizes the loss against the true, unknown dual potential.

## Domain-Specific Analysis (Computer Science)

### Problem Formulation
The paper formulates the task of solving an OT problem as a supervised learning problem, but one where the labels are generated on-the-fly. The input is a pair of discrete measures (µ, ν) on a grid, and the target is the corresponding entropic dual potential g. The key is that this is treated as learning an operator S: P(X) x P(Y) -> L^1(ν), which is then discretized.

### Algorithm System Design
The system comprises two neural networks: S_phi (an FNO) and G_theta (an MLP). S_phi is the solver, designed for discretization invariance. G_theta is the generator, designed to be expressive (Theorem 3). They are trained in a minimax game (Algorithm 2), where G_theta tries to find difficult (µ, ν) pairs for S_phi, and S_phi tries to solve them. The loss for S_phi is L2(S_phi(µ,ν), target), where the target is computed via a few Sinkhorn steps (the 'τ_k' operator). This self-referential target generation is a core design choice.

### Evaluation
The evaluation is comprehensive. It tests the primary claim (fast and accurate OT distance prediction) and demonstrates utility in downstream tasks that rely on OT (barycenters, geodesics, gradient flows). Baselines are well-chosen and represent the state-of-the-art in Sinkhorn initialization. The use of multiple datasets (MNIST, CIFAR, LFW, etc.) and cross-dataset evaluation effectively demonstrates the claimed generalization capability, which was a major weakness of prior work like Meta OT.

### Reproducibility
High. The paper provides a link to the source code and model weights. The appendices contain extensive details on network architectures, hyperparameters (Table 3), and experimental setup, which should allow for straightforward reproduction of the results.

## Critical Examination

### Assumptions
- The input measures are discretizations on a uniform, equispaced grid, which is a requirement for the standard FNO architecture used.
- The cost function is fixed for a given trained model. The model does not generalize across different cost functions.
- The generator architecture is capable of producing a sufficiently diverse and challenging set of training examples to ensure the solver becomes robust and general.
- The bootstrapping target (from k Sinkhorn steps) is a sufficiently good proxy for the true dual potential to provide a useful learning signal. Proposition 5 supports this, but the constant `c` could be large.
- The Lipschitz condition (L < λ) in Theorem 3, which guarantees generator invertibility and coverage, is not enforced in practice, with the authors noting that not enforcing it yields better empirical results.

### Limitations
- The model must be retrained for each new cost function, limiting its universality.
- The model does not extrapolate well to resolutions significantly higher than those seen during training.
- The current implementation is designed for measures on uniform grids and does not directly apply to unstructured point clouds.
- The performance on higher-dimensional domains (d > 3) is not explored.

### Evidence Quality
- The evidence is strong and multi-faceted. It includes theoretical proofs for key components of the methodology (generator universality, loss convergence).
- The empirical evidence is extensive, covering multiple datasets, cost functions (by training separate models), and tasks.
- The comparisons to strong baselines (Meta OT, Gaussian Init) are direct and clearly show the advantages of UNOT, especially in out-of-distribution generalization.

## Phase 2: Deep Dive - Technical Content

### Mathematical Concepts
- **Optimal Transport (OT)** (Category: theory): A mathematical theory for finding the most efficient way to transport mass from one distribution to another, given a cost function.
- **Entropic Regularized OT** (Category: problem): A variant of the OT problem (Eq. 1) that adds a KL-divergence (or entropy) regularizer to the objective, making the problem strictly convex and solvable efficiently with the Sinkhorn algorithm.
- **Transport Plan (π)** (Category: space): A joint probability measure on the product space X x Y whose marginals are the source (µ) and target (ν) measures. It describes how mass is moved from µ to ν.
- **Dual OT Problem** (Category: problem): A dual formulation of the OT problem (Eq. 3) involving finding a pair of functions (potentials) f and g, whose supremum equals the infimum of the primal problem.
- **Dual Potentials (f, g)** (Category: function): The functions that are the variables in the dual OT problem. UNOT learns to predict these potentials.
- **Gibbs Kernel (K)** (Category: operator): A kernel matrix defined as K = exp(-C/ε), where C is the cost matrix and ε is the regularization parameter. It is central to the Sinkhorn algorithm.
- **Wasserstein-p distance (W_p)** (Category: metric): A metric on the space of probability measures, defined as the p-th root of the optimal transport cost when the cost function is d(x,y)^p for some metric d (Eq. 2).
- **Pushforward Measure (T#µ)** (Category: operator): The measure obtained by applying a map T to a measure µ. If T is a transport map, then ν = T#µ.
- **Sinkhorn Divergence (SD_ε)** (Category: functional): A debiased version of the entropic OT cost, defined as SD_ε(µ,ν) = OT_ε(µ,ν) - 0.5*OT_ε(µ,µ) - 0.5*OT_ε(ν,ν). It is used for computing barycenters.
- **Wasserstein Barycenter** (Category: problem): The measure that minimizes the weighted sum of squared Wasserstein distances to a given set of measures (Eq. 8).
- **Wasserstein Geodesic (McCann Interpolation)** (Category: path): The shortest path between two measures in the Wasserstein space, which can be constructed by interpolating an optimal transport map.
- **Hilbert Projective Metric (d_H)** (Category: metric): A metric defined on the cone of positive vectors, used in the convergence proof of the bootstrapping loss (Proposition 5).
- **Polish Space** (Category: space): A separable completely metrizable topological space, the standard setting for modern OT theory.
- **Banach Space** (Category: space): A complete normed vector space. Neural Operators are defined as maps between Banach spaces of functions.

### Methods
- **Fourier Neural Operator (FNO)** (Type: algorithmic): A neural network architecture that learns mappings between function spaces. It is discretization-invariant because it performs key operations in Fourier space, making it suitable for learning to solve problems on grids of varying resolutions. Used as the solver network S_phi.
- **Adversarial Training** (Type: algorithmic): A training paradigm involving two networks, a generator and a solver (or discriminator), competing in a minimax game. Here, the generator creates hard examples to maximize the solver's loss, and the solver minimizes it, leading to a more robust solver.
- **Self-Supervised Bootstrapping** (Type: algorithmic): A training technique where the model generates its own targets. In UNOT, the target for the solver network is created by running a few Sinkhorn iterations initialized with the solver's own prediction. This avoids needing pre-computed ground-truth solutions.
- **Gradient Descent on Barycenter Objective** (Type: computational): An iterative method used to find the Sinkhorn divergence barycenter by taking gradient steps. UNOT is used to rapidly compute the gradients (Eq. 10) needed for each step.
- **Wasserstein Gradient Flow** (Type: theoretical): A concept describing the evolution of distributions as a gradient flow on the Wasserstein space. The paper demonstrates UNOT can approximate the particle flow for a 'Wasserstein on Wasserstein' problem.

### Algorithms
- **UNOT Training Algorithm** (Purpose: To train the solver (S_phi) and generator (G_theta) networks.)
  - Key Idea: An adversarial minimax loop. The generator G_theta creates a batch of measure pairs (µ,ν). The solver S_phi predicts a dual potential g_phi. A target g_tau_k is created by warm-starting Sinkhorn with g_phi for k steps. S_phi is updated to minimize L2(g_phi, g_tau_k). G_theta is updated to maximize the same loss.
  - Complexity: Training is computationally expensive (35h on an H100), dominated by the large number of samples and the forward/backward passes through the FNO. Inference is extremely fast.
- **Sinkhorn Algorithm** (Purpose: To iteratively solve the discrete entropic OT problem.)
  - Key Idea: An iterative algorithm that alternately updates two scaling vectors (u, v) by matrix-vector multiplications with the Gibbs kernel K until they converge. The optimal plan is then recovered from u and v. UNOT provides a high-quality initialization for v.
  - Complexity: Each iteration is O(mn). The number of iterations depends on the desired accuracy and the regularization ε. UNOT reduces the number of required iterations.
- **Barycenter Computation (via UNOT)** (Purpose: To compute the Sinkhorn divergence barycenter of a set of measures.)
  - Key Idea: Use projected gradient descent on the barycenter objective (Eq. 9). In each step, use UNOT to quickly compute the necessary gradients (Eq. 10), which are differences of dual potentials.
  - Complexity: Dominated by the number of gradient steps times the cost of running UNOT forward passes. Much faster than using the full Sinkhorn algorithm to compute gradients at each step.

## Critical Analysis Elements

## Evaluation & Validation

**Datasets**: MNIST (28x28), grayscale CIFAR10 (28x28), Google Quick, Draw! (Bear, 64x64), Labeled Faces in the Wild (LFW, 64x64). Also cross-dataset pairs (e.g., CIFAR-MNIST). For the spherical domain, these images are projected onto the unit sphere.

**Metrics**: Relative error on the OT distance, number of Sinkhorn iterations to reach 0.01 relative error, wall-clock time for convergence, visual quality of barycenters and geodesics, marginal constraint violation (MCV).

**Baselines**: Standard Sinkhorn initialization (vector of ones), Gaussian initialization (Thornton & Cuturi, 2022), Meta OT (Amos et al., 2023), GeONet (Gracyk & Chen, 2024) for geodesics.

**Results**: UNOT consistently outperforms baselines in terms of accuracy and speed, especially on out-of-distribution datasets. It achieves speedups of 1.25x to 7.4x. It nearly matches the specialized Meta OT on its training data (MNIST) and vastly outperforms it elsewhere. It produces visually superior geodesics compared to the specialized GeONet model.

## Proof Scrutiny (for Mathematical Papers)

**Proof Strategy**: The paper provides proofs for its three main theoretical claims. Prop. 2 relies on results from prior work (Feydy et al., 2018) on the stability of dual potentials. Thm. 3 uses the inverse function theorem and properties of Lipschitz maps, inspired by work on invertible ResNets (Behrmann et al., 2019). Prop. 5 uses the contraction property of the Sinkhorn operator with respect to the Hilbert projective metric, a standard result in the analysis of the Sinkhorn algorithm.

**Key Lemmas**: Lemma B.4 establishes weak convergence of the defined measure discretizations. Lemma B.5 relates the Hilbert projective metric loss to the L2 loss, which is crucial for bridging the theoretical contraction property with the practical L2 training objective.

**Potential Gaps**: The proof of Theorem 3 relies on the condition that the Lipschitz constant of the residual block `NN_theta` is less than the skip connection weight `λ` (L < λ). The authors state they do not enforce this in practice as it hurts performance. While the theorem shows the generator *can* be universal, it doesn't guarantee the trained generator *is* universal. However, the empirical results suggest the generator is sufficiently expressive.

## Phase 3: Synthesis & Future Work

### Key Insights
- Reframing OT solving as learning a continuous operator is a highly effective strategy for amortization, and FNOs are a natural fit for this due to their discretization invariance.
- Adversarial training with a generator creating 'on-the-fly' hard examples is a powerful paradigm for training robust optimization solvers without needing a static dataset.
- A self-supervised bootstrapping loss, where a model provides its own improving targets, can effectively replace the need for expensive ground-truth labels in learning-to-optimize settings.
- Learned dual potentials capture not just the transport cost but also the underlying geometry of the Wasserstein space, making them useful for downstream tasks like barycenter and geodesic computation.
- Generalization across datasets and resolutions is achievable for neural OT solvers, overcoming a major limitation of previous work and moving closer to a practical, universal tool.

### Future Work
- Scaling UNOT to handle significantly higher resolutions than those seen during training.
- Generalizing UNOT to be conditioned on the cost function, rather than requiring a separate model for each cost.
- Adapting the framework to work with non-uniform grids or unstructured point clouds, possibly by using Graph Neural Operators.
- Applying the UNOT framework and its adversarial bootstrapping training methodology to other data modalities and other iterative optimization problems.
- Investigating more principled ways to enforce or handle the Lipschitz constraint on the generator network to better align theory and practice.

### Practical Implications
- Significant acceleration of computational pipelines that rely heavily on OT, such as in single-cell genomics for trajectory inference, domain adaptation in computer vision, and generative modeling (e.g., flow matching).
- Enabling new applications of OT where real-time performance is critical and was previously unattainable with iterative solvers.
- Providing a drop-in, high-performance initializer for existing Sinkhorn algorithm implementations, improving their efficiency with minimal code changes.
- The model can be used as a fast, differentiable proxy for the OT distance or plan in larger end-to-end learning systems.

## Context & Connections

### Research Areas
- Optimal Transport
- Machine Learning
- Numerical Optimization
- Deep Learning
- Generative Models
- Neural Operators
- Amortized Inference

### Innovations
- First neural OT solver that generalizes across datasets and resolutions for a fixed cost function.
- Use of Fourier Neural Operators for solving OT problems.
- A novel adversarial, self-supervised training framework with a generator and a bootstrapping loss for learning to solve optimization problems.

### Applications
- **Domain**: Machine Learning
  - Use Case: Sinkhorn Algorithm Acceleration
  - Impact: Provides a state-of-the-art initialization that can speed up the algorithm by up to 7.4x, making OT more practical for large-scale problems.
- **Domain**: Computer Graphics / Vision
  - Use Case: Wasserstein Barycenters and Geodesics
  - Impact: Enables fast and accurate computation of image interpolations and averages that respect the geometric structure of the data.
- **Domain**: Generative Modeling
  - Use Case: Wasserstein Gradient Flows
  - Impact: Allows for efficient approximation of particle flows for training generative models, as demonstrated with the Wasserstein-on-Wasserstein flow experiment.
- **Domain**: Computational Biology
  - Use Case: Single-cell genomics
  - Impact: Could accelerate the analysis of cell development trajectories, which often relies on repeated OT calculations.

### People Mentioned
- Jonathan Geuter
- Gregor Kornhardt
- Ingimar Tomasson
- Vaios Laschos
- Cédric Villani
- Gabriel Peyré
- Marco Cuturi
- Nicolas Courty
- Geoffrey Schiebinger
- Remi Dadashi
- Michael A. Schmitz
- David Alvarez-Melis
- Soheil Kolouri
- Charlotte Bunne
- Huan Xu
- Aude Tong
- Amir-Hossein Pooladian
- Bjorn Engquist
- Brandon Amos
- Adam Gracyk
- Nikolaos Kovachki
- Thomas Uscidda
- Alexander Korotin
- Guillaume Carlier
- Ilya Loshchilov
- Frank Hutter
- Diederik P. Kingma
- Jimmy Ba
- Kaiming He
- Ian Goodfellow
- Boris Bonev
- Martial Agueh
- Martin Arjovsky
- Jean Feydy
- Richard Sinkhorn
- Paul Knopp
- Jake Thornton
- Marcel Nutz
- Yann LeCun
- Yoshua Bengio

### Institutions Mentioned
- Harvard John A. Paulson School of Engineering and Applied Sciences
- Kempner Institute at Harvard University
- Department of Mathematics, Technische Universität Berlin, Germany
- Weierstrass Institute, Berlin, Germany
- Deutsche Forschungsgemeinschaft (DFG)

### Theoretical Results
- Proposition 1: The optimal discrete entropic transport plan Π can be recovered from dual scaling vectors u and v as Π = diag(u) K diag(v), where K is the Gibbs kernel.
- Proposition 2 (Informal): The extended dual potentials (f_n, g_n) for discrete measures converge uniformly to the continuous dual potentials (f, g) as the discretization becomes finer.
- Theorem 3: A generator G_theta with a ResNet-like structure (residual connection with weight λ > Lipschitz constant of the network block) is invertible and its pushforward measure has positive density on the non-negative orthant, meaning it can generate any non-negative vector.
- Corollary 4: The universality result of Theorem 3 extends to deep ResNets formed by composing such blocks.
- Proposition 5: Minimizing the L2 loss between the predicted potential g_phi and the k-step bootstrapped target g_tau_k provides an upper bound for the L2 loss against the true ground truth potential g, justifying the bootstrapping training objective.

### Related Concepts
- Sliced Wasserstein Distance
- Generative Adversarial Networks (GANs)
- Residual Networks (ResNets)
- Invertible Neural Networks
- Manifold Hypothesis
- Partial Differential Equations (PDEs)
- Flow Matching

### Connections to Other Work
**Builds On**:
- Sinkhorn Algorithm (Cuturi, 2013)
- Fourier Neural Operators (Kovachki et al., 2024)
- GANs training paradigm (Goodfellow et al., 2014)
- Invertible ResNets theory (Behrmann et al., 2019)

**Enables**:
- Faster computation in applications using Wasserstein gradient flows (Alvarez-Melis et al., 2021)
- More efficient flow matching for generative models (Tong et al., 2024; Pooladian et al., 2023)

**Related To**:
- Meta Optimal Transport (Amos et al., 2023) - UNOT is a more general approach that is not dataset-specific.
- Rethinking Initialization of the Sinkhorn Algorithm (Thornton & Cuturi, 2022) - UNOT provides a learned, more powerful initialization.
- GeONet (Gracyk & Chen, 2024) - UNOT, though not specialized for geodesics, is shown to compute them more accurately.
- Neural Optimal Transport (Korotin et al., 2023) - UNOT focuses on generalizing across OT problems, whereas this work solves individual instances.

## Thinking Patterns Observed

**Systems Thinking**: The UNOT framework is designed as a system of two interacting components (generator and solver) that are co-adapted through an adversarial process to achieve a global objective (a robust, general solver).

**Pattern Recognition**: The core idea is to recognize the problem of solving OT as a pattern-matching task: mapping input measure patterns to output potential patterns. The FNO is chosen specifically for its ability to handle these patterns across different scales/resolutions.

**Reasoning By Analogy**: The training process is analogous to GANs, with a generator and a 'discriminator' (the solver). The use of FNOs is analogous to their application in solving PDEs, where they also learn operators between function spaces.

**Probabilistic Reasoning**: The entire paper is grounded in the language of probability measures. The generator learns a distribution over OT problems, and the solver operates on these distributions.

## Quality Assessment

**Coherence**: The paper is highly coherent. The problem statement, proposed method, theoretical justification, and experimental validation are all tightly interwoven. Each component of the methodology (FNO, generator, bootstrapping loss) is motivated by a specific need and supported by theory or prior work.

**Completeness**: The paper is very complete. It includes a thorough background, detailed methodology, extensive experiments, a discussion of limitations, and a comprehensive appendix with proofs and additional details. The authors address the 'what', 'why', and 'how' at every stage.

**Bias Assessment**: The authors are transparent about the limitations of their work, such as the lack of generalization across cost functions and to very high resolutions. The experimental comparisons are fair, using official implementations of baselines where possible and testing on a wide range of data to avoid cherry-picking results. There is no obvious bias detected.

---
*Analysis performed on: 2025-07-03T16:08:45.862358*
