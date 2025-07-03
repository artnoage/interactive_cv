# Analysis of Geometric properties of cones with applications on the Hellinger-Kantorovich space, and a new distance on the space of probability measures

**Authors**: Vaios Laschos, Alexander Mielke
**Year**: 2018
**Venue**: arXiv preprint
**Domain**: Mathematics
**Analysis Date**: 2025-07-03T16:22:22.198100

## Executive Summary

This paper establishes a fundamental geometric connection between the space of finite, non-negative measures M(X) equipped with the Hellinger-Kantorovich distance (HK), and the space of probability measures P(X). The authors demonstrate that the HK distance possesses a specific two-parameter scaling property, which they prove is a defining characteristic of a metric cone. This insight allows them to interpret the Hellinger-Kantorovich space (M(X), HK) as a metric cone over a new space of probability measures, (P(X), SHK), where SHK is a novel 'spherical' distance introduced and proven to be a valid metric in this work.

The paper is structured in two main parts. First, it develops an abstract theory of metric cones, analyzing how geometric properties like geodesics, local angles, and K-semiconcavity are transferred between a cone space and its underlying 'spherical' base space. Key results include explicit formulas for lifting and projecting geodesics and a precise relationship between local angles in the two spaces. The second part applies this abstract framework to the Hellinger-Kantorovich space. The authors use the Logarithmic-Entropy-Transport (LET) formulation to prove the crucial scaling property for the HK distance. They then characterize the geodesics in the new space (P(X), SHK) via a system of continuity and Hamilton-Jacobi equations, analogous to the Otto calculus for Wasserstein spaces.
Finally, the paper investigates finer geometric properties essential for the theory of gradient flows. It proves that the Local Angle Condition (m-LAC) is stable under the cone construction for HK spaces, meaning (X, dX) has m-LAC if and only if (M(X), HK) and (P(X), SHK) do. While global K-semiconcavity is known to fail, the authors establish a crucial partial K-semiconcavity result on subsets of measures with bounded densities. These results provide the essential geometric groundwork for a forthcoming paper on the existence of gradient flows in these spaces, which has significant implications for the variational study of reaction-diffusion systems.

## Phase 1: Rapid Reconnaissance

### Problem Addressed
The paper addresses the problem of understanding the fundamental geometric structure of the Hellinger-Kantorovich (HK) space of measures. Prior work had introduced this space and studied some of its properties, but a deep geometric characterization was lacking. Specifically, the paper aims to formalize the intuition that the HK space, which allows for both mass transport and creation/annihilation, behaves like a cone, and to establish the geometric properties (like local curvature and semiconcavity) necessary to construct a theory of gradient flows on it.

### Core Contribution
The core contribution is the discovery and proof that the Hellinger-Kantorovich space (M(X), HK) is a metric cone over the space of probability measures (P(X)) endowed with a new, well-defined 'spherical' distance SHK. This is achieved by identifying a fundamental scaling property of the HK distance. This structural insight is then used to systematically transfer and analyze key geometric properties (geodesics, local angles, local angle condition, K-semiconcavity) from the base space to the HK and SHK spaces, paving the way for the study of gradient flows.

### Initial Assessment
The paper is a highly credible and significant contribution to metric geometry and optimal transport theory. The mathematical arguments are rigorous, well-structured, and build upon foundational work in the field. The authors clearly articulate their novel perspective—interpreting the HK space as a cone—and systematically develop the consequences of this insight. The work is relevant for researchers in geometric analysis, optimal transport, and the theory of partial differential equations, as it provides the necessary geometric tools for extending the powerful framework of gradient flows to a new class of metric spaces that model both transport and reaction.

### Claimed Contributions
- Proving that a specific scaling property fully characterizes cone spaces (Theorem 2.2).
- Proving that the Hellinger-Kantorovich distance HKα,β satisfies this scaling property (Theorem 3.3).
- Introducing a new distance, SHKα,β, on the space of probability measures P(X) and proving it turns (M(X), HKα,β) into a cone space over (P(X), SHKα,β).
- Providing a full characterization of geodesics in both (M(X), HKα,β) and (P(X), SHKα,β), including a two-parameter rescaling formula.
- Establishing finer geometric properties, including the transfer of the local-angle condition (m-LAC) between the spaces.
- Proving partial K-semiconcavity of the squared distances on specific subsets of measures, which is a key step towards proving the existence of gradient flows.

### Structure Overview
The paper is organized into four main sections. Section 1 introduces the Hellinger-Kantorovich distance and motivates the work by observing a scaling property. Section 2 develops the abstract theory of metric cones, discussing scaling, geodesics, local angles, the Local Angle Condition (m-LAC), and K-semiconcavity. Section 3 applies this abstract theory to the Hellinger-Kantorovich space, proving it is a cone space, defining the new spherical distance SHK, and characterizing its geodesics. Section 4 investigates the finer geometric properties (m-LAC and K-semiconcavity) of the HK and SHK spaces, establishing stability results that are crucial for future applications to gradient flows.

### Key Findings
- The Hellinger-Kantorovich space (M(X), HK) is a metric cone over the space of probability measures (P(X), SHK).
- A distance on a space C = X x [0,inf) satisfying the scaling property d_C^2([x0,r0],[x1,r1]) = r0*r1*d_C^2([x0,1],[x1,1]) + (r0-r1)^2 is equivalent to it being a cone distance.
- The Local Angle Condition (m-LAC) is a stable property that transfers between a space (X, dX) and its associated HK and SHK spaces.
- Geodesics in the SHK space can be characterized by a coupled system of a generalized continuity equation and a Hamilton-Jacobi equation, analogous to the Wasserstein space.
- While global K-semiconcavity fails, it holds on subsets of measures that have densities (with respect to a locally doubling measure) bounded from above and below. This is sufficient for studying many gradient flows.
- The total mass of an optimal transport plan between two measures in the LET formulation is bounded by the geometric mean of the masses of the measures being transported (Lemma 4.3).

## Research Context

**Historical Context**: The work is situated in the field of analysis on metric spaces, particularly the study of spaces of measures. It builds on the classical theory of optimal transport (Kantorovich-Wasserstein distance) and the theory of gradient flows in metric spaces, famously developed for Wasserstein spaces by Ambrosio, Gigli, and Savaré (AGS).

**Current State**: The Hellinger-Kantorovich (HK) distance was recently introduced ([LMS16], [KMV16], [CP*15b]) as a way to interpolate between pure transport (Wasserstein) and pure mass creation/annihilation (Hellinger). At the time of this paper, the geometric properties of the HK space were still being actively explored.

**Prior Limitations**: Prior to this work, the geometric structure of the HK space was not fully understood. While some properties of geodesics were known (e.g., the quadratic evolution of mass), there was no unifying geometric picture like the one provided by the cone space interpretation. Furthermore, key properties needed for gradient flow theory, such as the Local Angle Condition and K-semiconcavity, had not been established for the HK space.

**Advancement**: This paper provides a major advancement by establishing the cone structure of the HK space. This simplifies the understanding of its geometry and allows for the systematic transfer of geometric properties from the base space. The introduction of the SHK distance and the proofs of m-LAC stability and partial K-semiconcavity are crucial steps that enable the application of gradient flow theory to this new setting.

## Methodology Analysis

### Key Technical Innovations
- The identification of the scaling property (Eq. 2.1) as the defining characteristic of a cone space, and the proof that it implies the triangle inequality for the spherical distance (Theorem 2.2).
- The use of the Logarithmic-Entropy Transport (LET) formulation to prove that the HK distance satisfies this exact scaling property.
- The development of explicit formulas relating comparison angles and local angles between a cone and its base space (Proposition 2.20), which is the key to proving the stability of the m-LAC property.
- The use of distributional derivatives to rigorously analyze the transfer of K-semiconcavity between spaces in a non-smooth setting (Lemma 2.23).

### Mathematical Framework
- The paper is grounded in the theory of metric geometry, particularly geodesic metric spaces and Alexandrov spaces (spaces with curvature bounds).
- It heavily utilizes the concept of a metric cone over a metric space, as defined in works like [BBI01].
- It employs tools from optimal transport theory, specifically the Kantorovich-Wasserstein distance and the static LET formulation for the HK distance.
- The analysis of K-semiconcavity relies on concepts from convex analysis and the theory of functions of bounded variation, including the use of distributional derivatives.

## Domain-Specific Analysis (Mathematics)

### Mathematics
The paper is a work of pure mathematics, focusing on geometric analysis. The core of the paper is the proof of several theorems that characterize the geometric structure of the Hellinger-Kantorovich space. The methodology is deductive, starting from abstract definitions and progressively proving lemmas and theorems. The proofs are rigorous and technical, involving detailed calculations and logical arguments. For instance, the proof of the stability of m-LAC (Theorem 2.18) relies on a careful analysis of how comparison angles transform under the cone construction. Similarly, the proof of partial K-semiconcavity (Theorem 4.8) is a multi-step argument that combines abstract results about cones with specific estimates derived from the optimality conditions of the HK problem. The work's significance lies in providing the foundational geometric theory required for future analysis, particularly the study of PDEs as gradient flows.

## Critical Examination

### Assumptions
- The underlying space (X, dX) is assumed to be a geodesic, Polish space for most results.
- The analysis of geodesics and angles often requires the distance between points in the base space to be less than a threshold (e.g., dX < π or ℓdX < π/2), which corresponds to the regime where transport is favored over creation/annihilation.
- The proofs of K-semiconcavity for the HK space (Theorem 4.8) require the base space (X, dX) to satisfy K-semiconcavity on small balls and to be a doubling metric space admitting a locally doubling measure.

### Limitations
- The key result on K-semiconcavity (Theorem 4.8) is not global. It only holds for measures within the set M_L_delta(X), which have densities bounded from above and below with respect to a reference measure L. The paper does not address the semiconcavity properties for general measures.
- The paper is purely theoretical. It establishes the geometric framework but does not provide numerical methods for computing the new SHK distance or for implementing the gradient flows that it motivates.
- The applicability of the results is conditional on the properties of the base space (X, dX). If the base space does not satisfy m-LAC or local K-semiconcavity, the corresponding results for the HK/SHK spaces do not hold.

### Evidence Quality
- The evidence consists of rigorous mathematical proofs. The logic is deductive and self-contained within the established mathematical framework. The claims are well-supported by detailed derivations and references to foundational texts. The quality of the evidence is very high.

## Phase 2: Deep Dive - Technical Content

### Mathematical Concepts
- **Metric Cone** (Category: space): A space C formed by taking the quotient of X x [0,inf) where all points in X x {0} are identified as a single apex '0'. The distance is given by d_C^2([x0,r0],[x1,r1]) = r0^2 + r1^2 - 2*r0*r1*cos(min(pi, dX(x0,x1))).
- **Hellinger-Kantorovich Distance (HK_alpha,beta or HK_l)** (Category: metric): A family of distances on the space of non-negative finite measures M(X) that interpolates between the Wasserstein distance (transport) and the Hellinger distance (creation/annihilation).
- **Spherical Hellinger-Kantorovich Distance (SHK_l)** (Category: metric): A new distance on the space of probability measures P(X), derived from the HK distance via SHK_l(ν0,ν1) = arccos(1 - (1/2)HK_l^2(ν0,ν1)). This paper proves it is a valid metric.
- **Geodesic Space** (Category: space): A metric space where for any two points, there exists a path (a geodesic) connecting them whose length is equal to the distance between the points.
- **Comparison Angle** (Category: metric): An angle defined for a triplet of points in a metric space by comparing it to a triangle with the same side lengths in a model space of constant curvature κ (e.g., plane for κ=0, sphere for κ>0).
- **Local Angle (Upper/Lower)** (Category: metric): The angle between two geodesics emanating from the same point, defined as the limsup (for upper angle) or liminf (for lower angle) of the comparison angles of infinitesimal triangles.
- **Local Angle Condition (m-LAC)** (Category: principle): A condition on a geodesic metric space requiring that for any m geodesics starting at a point, a certain quadratic form involving the cosines of their upper angles is non-negative. It is a weak, first-order notion of non-negative curvature.
- **K-semiconcavity** (Category: principle): A property of a function f where f(t) - Kt^2 is concave. In this paper, it refers to the property that the function t -> d^2(x2, x01(t)) is K*d^2(x0,x1)-semiconcave for a geodesic x01 and an observer x2.
- **Logarithmic-Entropy Transport (LET) Functional** (Category: functional): A functional defined on transport plans whose minimization is equivalent to computing the squared HK distance. It consists of two relative entropy terms and a transport cost term.
- **Doubling Measure** (Category: space): A measure L on a metric space such that the measure of a ball of radius 2R is bounded by a constant times the measure of the ball of radius R.
- **Hamilton-Jacobi Equation** (Category: equation): A first-order, non-linear partial differential equation. In this context, it describes the evolution of the dual potential associated with a geodesic in the HK or SHK space.
- **Continuity Equation** (Category: equation): A partial differential equation that describes the transport of a quantity. Here, it is a generalized version that includes a source/sink term, describing the evolution of the measure along a geodesic.

### Methods
- **Cone Space Analysis** (Type: theoretical): Developing abstract geometric results for cone spaces and then applying them to the specific case of the Hellinger-Kantorovich space.
- **Scaling Argument** (Type: analytical): Exploiting a specific scaling property of the HK distance to establish its cone structure. This is the central methodological tool of the paper.
- **Variational Formulation (LET)** (Type: theoretical): Using the Logarithmic-Entropy Transport (LET) formulation of the HK distance to prove its fundamental properties, such as the scaling property.
- **Comparison Geometry** (Type: analytical): Using comparison triangles and comparison angles (from model spaces like the Euclidean plane or the sphere) to define and analyze local geometric properties like m-LAC.
- **Analysis with Distributional Derivatives** (Type: analytical): Using distributional (weak) derivatives to handle the second derivative of non-smooth functions (specifically, distance functions along geodesics) in the proofs of K-semiconcavity.
- **Optimal Transport Duality** (Type: theoretical): Using the optimality conditions (primal-dual relations) from the LET problem to derive bounds on the densities of the transported mass (Lemma 4.9).

### Algorithms
- **Lifting Geodesics from Base to Cone** (Purpose: To construct a geodesic in the cone space (C, dC) from a geodesic in the base space (X, dX).)
  - Key Idea: A constant-speed geodesic z01(t) in the cone is constructed as [x01(ζ(t)), r(t)], where x01 is a geodesic in the base space, and the radius r(t) and reparameterization ζ(t) are given by explicit formulas (Eq. 2.7) that depend on the initial/final radii and the distance in the base space.
  - Complexity: N/A (Analytical construction)
- **Projecting Geodesics from Cone to Base** (Purpose: To construct a geodesic in the base space (X, dX) from a geodesic in the cone space (C, dC).)
  - Key Idea: This is the inverse of the lifting procedure. Given a geodesic in the cone, the corresponding geodesic in the base space is obtained by a specific time reparameterization β01(t) (Eq. 2.12), which is the inverse of ζ01(t) from the lifting algorithm.
  - Complexity: N/A (Analytical construction)

## Critical Analysis Elements

## Evaluation & Validation

**Evaluation Approach**: The paper's claims are validated through rigorous mathematical proofs rather than empirical evaluation. There are no datasets, metrics, or baselines in the computational sense. The validation is entirely theoretical and deductive.

## Proof Scrutiny (for Mathematical Papers)

**Proof Strategy**: The overall strategy is to first establish general results for abstract metric cones (Section 2) and then show that the Hellinger-Kantorovich space is a specific instance of this structure (Section 3). The proofs often involve direct calculation using the definitions of the distances and geodesics, combined with tools from analysis (e.g., distributional derivatives for semiconcavity) and comparison geometry (e.g., comparison triangles for the triangle inequality).

**Key Lemmas**: Lemma 2.1 (Scaling properties of cone distances), Lemma 2.19 (Connecting comparison angles in cone and base), Lemma 2.23 (Relating semiconcavity of d^2 and 1-cos(d)), Lemma 4.3 (Estimate on total mass of optimal plan), Lemma 4.9 (Bounds on optimal densities for 'nice' measures).

**Potential Gaps**: The proofs appear to be solid and complete. The arguments are detailed and logically sound. No obvious gaps or hand-wavy arguments were detected. The use of distributional derivatives in Section 2.7 is appropriate for handling the non-smooth nature of the distance functions and makes the argument rigorous.

## Phase 3: Synthesis & Future Work

### Key Insights
- The Hellinger-Kantorovich space (M(X), HK) is not just an ad-hoc construction but possesses a deep, intrinsic geometric structure: it is a metric cone.
- This cone structure provides a powerful unifying framework, explaining previously observed properties (like the quadratic evolution of mass along geodesics) and allowing for the systematic study of its geometry.
- The Local Angle Condition (m-LAC), a weak form of non-negative curvature, is a remarkably stable property that transfers from a base space to its HK and SHK counterparts, unlike stronger curvature bounds.
- A new, geometrically meaningful metric (SHK) on the space of probability measures naturally emerges as the 'base' of the HK cone.
- While the HK space is not globally K-semiconcave (a desirable property for gradient flows), it does possess this property on important, well-behaved subsets of measures, which is sufficient to ground a theory of gradient flows for many applications.

### Future Work
- To prove the existence of gradient flows on both the Hellinger-Kantorovich space (M(X), HK) and the Spherical Hellinger-Kantorovich space (P(X), SHK). This is explicitly stated as the goal of a forthcoming paper.
- To apply the gradient flow framework to study specific evolution equations, such as reaction-diffusion systems, by formulating them as gradient flows of an energy functional on these spaces.
- To extend the gradient flow existence theory to cases where K-semiconcavity holds only on a collection of subsets, as is the case for the HK space.
- To develop numerical methods for approximating the Hellinger-Kantorovich and Spherical Hellinger-Kantorovich distances, for which the estimate on the calibration measure in Lemma 4.3 is noted to be helpful.

### Practical Implications
- The primary practical implication is the potential to develop a new variational framework (gradient flows) for studying and simulating reaction-diffusion systems, which are ubiquitous in science and engineering.
- The geometric insights and characterization of geodesics could lead to more efficient and stable numerical algorithms for computing the HK distance, which is useful in applications where mass is not conserved (e.g., comparing images with different brightness levels).
- The new SHK distance on probability measures could find applications in statistics and machine learning for comparing distributions where a blend of transport and density difference is meaningful.

## Context & Connections

### Research Areas
- Metric Geometry
- Optimal Transport Theory
- Geometric Analysis
- Analysis on Metric Spaces
- Calculus of Variations
- Partial Differential Equations
- Gradient Flows

### Innovations
- The conceptual leap of identifying the Hellinger-Kantorovich space as a metric cone.
- The introduction of the Spherical Hellinger-Kantorovich (SHK) distance on the space of probability measures.
- The proof that the Local Angle Condition (m-LAC) is stable under the cone construction for HK spaces.
- The characterization of geodesics in the SHK space via a Hamilton-Jacobi/Continuity equation system.

### Applications
- **Domain**: Partial Differential Equations
  - Use Case: Variational formulation of reaction-diffusion systems
  - Impact: Provides a new way to understand the structure, solutions, and long-time behavior of these equations by interpreting them as gradient-driven flows on a geometric landscape.
- **Domain**: Numerical Analysis
  - Use Case: Approximation of the Hellinger-Kantorovich distance
  - Impact: The theoretical results, such as the sharp estimate on the mass of the optimal plan (Lemma 4.3), can inform and improve the design of numerical algorithms.

### People Mentioned
- Vaios Laschos
- Alexander Mielke
- A. D. Aleksandrov
- V. N. Berestovskii
- I. G. Nikolaev
- L. Ambrosio
- N. Gigli
- G. Savaré
- S. Alexander
- V. Kapovitch
- A. Petrunin
- D. Burago
- Y. Burago
- S. Ivanov
- M. R. Bridson
- A. Häfliger
- L. Chizat
- G. Peyré
- B. Schmitzer
- F.-X. Vialard
- M. M. Deza
- E. Deza
- L. C. Evans
- R. F. Gariepy
- J. Heinonen
- S. Kondratyev
- L. Monsaingeon
- D. Vorotnikov
- M. Liero
- S. Lisini
- S.-i. Ohta
- K.-T. Sturm
- Marios Stamatakis

### Institutions Mentioned
- Weierstraß-Institut für Angewandte Analysis und Stochastik, Berlin
- Institut für Mathematik, Humboldt-Universität zu Berlin

### Theoretical Results
- Theorem 2.2: A metric space satisfying a specific scaling property (2.1) and a boundedness condition (2.3) is a metric cone.
- Theorem 2.18: The m-LAC property transfers between a geodesic space (X, dX) and its cone (C\{0}, dC).
- Proposition 2.27: Establishes a quantitative relationship between K-semiconcavity along geodesics in a cone space and its base space.
- Theorem 3.1: The squared HK distance is the minimum of the Logarithmic-Entropy Transport (LET) functional.
- Theorem 3.3: The squared HK distance satisfies the fundamental cone scaling property (3.10).
- Theorem 3.4: The Hellinger-Kantorovich space (M(X), HK) is a cone over the spherical space (P(X), SHK).
- Theorem 3.7: Geodesics in (P(X), SHK) are characterized by a coupled system of a continuity equation and a Hamilton-Jacobi equation (3.18).
- Theorem 4.2: The space (X, dX) satisfies m-LAC if and only if (M(X), HK) and (P(X), SHK) satisfy m-LAC.
- Theorem 4.8: The space (M(X), HK) is K'-semiconcave on sets of measures with bounded densities (M_L_delta), provided the base space has local K-semiconcavity.
- Theorem 4.12: The space (P(X), SHK) is K'-semiconcave on corresponding sets of probability measures (P_L_delta).

### Related Concepts
- Wasserstein Space
- Hellinger-Kakutani Distance
- Alexandrov Spaces
- Ricci Curvature Lower Bounds
- Otto Calculus
- Gradient Structures
- Reaction-Diffusion Systems

### Connections to Other Work
**Builds On**:
- [LMS16, LMS17]: This paper is a direct continuation of the authors' previous work where the HK distance and its LET formulation were introduced and studied.
- [BBI01, BrH99]: It uses the foundational theory of metric geometry and cone spaces from these standard textbooks.
- [AGS05]: The motivation to study geometric properties like semiconcavity and LAC comes from the successful theory of gradient flows on Wasserstein spaces developed in this book.

**Enables**:
- A future paper by the authors on the existence of gradient flows on HK and SHK spaces.
- The development of a 'pseudo-Riemannian' or 'Otto-like' calculus for reaction-diffusion systems.

**Related To**:
- [KMV16], [CP*15a, CP*15b]: These are independent, concurrent works that also introduced and studied similar 'unbalanced' optimal transport distances.
- [Sav07, OPV14]: The definitions and utility of the Local Angle Condition are drawn from these works on gradient flows in metric spaces.

## Thinking Patterns Observed

**Pattern Recognition**: The key insight of the paper stems from recognizing that a formula for the mass evolution along a geodesic [LMS16, Prop. 19] is a symptom of a more fundamental pattern: a cone-like scaling property of the distance itself.

**Systems Thinking**: The paper treats the (Base Space, Cone Space) pair as an interconnected system. It systematically analyzes how properties and structures (geodesics, angles, curvature-like conditions) are transformed and related when moving between the different levels of the system.

**Abstraction And Generalization**: The authors abstract the problem away from the specific HK space to a general theory of cone spaces in Section 2. They prove general theorems there (e.g., Theorem 2.2, 2.18) and then apply them as powerful tools to the specific case of interest, demonstrating the generality and strength of their approach.

## Quality Assessment

**Coherence**: The paper is exceptionally coherent. It starts with a clear motivation, develops the necessary abstract theory in a self-contained manner, and then applies it systematically to the problem at hand. The narrative flows logically from the scaling property to the cone structure to the analysis of finer geometric properties.

**Completeness**: The paper is very complete in its arguments. The proofs are detailed and rigorous, and the necessary background concepts are either defined or properly referenced. It successfully achieves its stated goal of establishing the geometric groundwork for future work.

**Bias**: There is no discernible bias. The paper is a work of pure mathematics, and the claims are supported by logical proofs. The authors properly cite concurrent work by other groups on similar topics.

---
*Analysis performed on: 2025-07-03T16:22:22.198100*
