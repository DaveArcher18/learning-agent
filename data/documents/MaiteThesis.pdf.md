# Stacks, Spectra and Elliptic Cohomology 

Maite Charlotte Carli<br>Born 31st March 2002 in Hamburg, Germany<br>February 4, 2025

Master's Thesis Mathematics
Advisor: Dr. Jack Davies
Second Advisor: Prof. Dr. Markus Hausmann
Mathematisches Institut

Mathematisch-Naturwissenschaftliche Fakultät der
Rheinischen Friedrich-Wilhelms-Universität Bonn

.

# Contents 

Introduction ..... 2
Acknowledgements ..... 3
1 Stacks ..... 4
1.1 First Definitions ..... 4
1.2 Stacks and Hopf algebroids ..... 10
1.3 Hopf Algebroids, Spectra and the Moduli Stack of Formal Groups ..... 21
2 Constructing Spectra ..... 29
2.1 Formal Considerations ..... 29
2.2 The Landweber Exact Functor Theorem ..... 40
2.3 Proof of the Algebraic Landweber Theorem (Thm. 2.43) ..... 47
2.4 Landweber exactness for $P(n)$ ..... 50
3 Elliptic Cohomology ..... 53
3.1 Elliptic Curves over a Field ..... 53
3.2 Elliptic Curves over general Base Schemes ..... 59
3.3 The Moduli Stack of Elliptic Curves ..... 62
References ..... 65

# Introduction 

At the latest since Adams' and Atiyah's proof of the Hopf invariant one problem ([3]), which famously reduced a proof that took several dozens of pages ([1]) to one that could "fit on a postcard" using complex $K$-theory, homotopy theorists' interest in extraordinary cohomology theories was sparked. Nowadays, this is phrased in the language of spectra. Many examples of spectra arise from topological questions: given a ring $R$, the Eilenberg-MacLane spectrum $H R$ represents singular cohomology, counting the "holes" in spaces, the spectra $K U$ and $K O$ represent complex and real $K$-theory respectively, which are related to group completions of vector bundles over a space. When trying to classify unoriented manifolds up to cobordism, the unoriented cobordism spectrum $M O$ naturally arises, having the property that its homotopy groups are isomorphic to the cobordism classes of those manifolds. More generally, the study of manifolds with more structure (oriented, almost complex, symplectic...) up to cobordism gives rise to other Thom spectra such as $M S O, M U$ or $M S p$.
What about other examples, maybe some for which the geometric interpretation is still waiting to be discovered? One idea to construct new spectra is to twist a known homology theory. By this, we mean that, given a spectrum $E$ and a ring map $f: \pi_{*}(E) \rightarrow R$, one could consider the functor $h_{f}: h S p \rightarrow A b$ that sends a spectrum $X$ to $E_{*}(X) \otimes_{\pi_{*}(E)} R$ and hope that this defines an interesting homology theory represented by a new spectrum. However, as tensoring is in general only right exact, this construction might not send cofiber sequences to long exact sequences. In 1976, Landweber gave a criterion under which exactness of $h_{f}$ is guaranteed in the case where $E$ is the complex cobordism spectrum $M U$ in [11]. This statement is often referred to as the Landweber exact functor theorem. As the ring $\pi_{*}(M U)$ is known to represent formal group laws, this criterion made it possible to associate homology theories to elliptic curves via their formal group law. This connection was explored by Morava soon after the discovery of Landweber's result. Landweber, Ravenel and Stong than showed in [12] that the formal group law associated to the Jacobi quartic satisfies the conditions of Landweber's exact functor theorem. They also coined the term elliptic cohomology for these theories. To this day, it is still unclear what the geometric explanation for elliptic cohomology theories should be, but there are conjectured connections to conformal field theories proposed in particular by Witten and Segal; see [20].
It could thus be interesting to know if a similar approach could be used to construct homology theories from other spectra than $M U$, for example for cobordism rings with different structures. Maybe they could also give rise to new homology theories which correspond to other geometric phenomena, hidden until now. This thesis was written with this question in mind.

The criterion found by Landweber can be rephrased in terms of flatness of some map over the moduli stack of formal groups. In a sense that will be made precise (Prop. 1.68), this stack is associated to the Hopf algebroid $\left[\left(\pi_{*}(M U), M U_{*}(M U)\left[u^{ \pm}\right]\right)\right]$. Thus, one could try to construct stacks from Hopf algebroids associated to other spectra, wonder if flat maps over these stacks give rise to new homology theories and if there are criteria to determine which maps are flat. Unfortunately, this idea does not work well. The first problem arises at the very beginning: to associate a Hopf algebroid to a spectrum, the spectrum needs to be flat (see Cor. 1.49). This already reduces the number of spectra we can consider drastically. For example, $M S U$ is not flat (Ex. 1.47). So trying to construct $M S U$-oriented spectra in this way is hopeless. Moreover, if the spectrum is not even, the rings appearing in the Hopf algebroid are not commutative but only graded commutative, i.e. subject to the Koszul sign rule, which makes it difficult to define their associated stack. This is only a slight setback though as one could still try to consider the stack corresponding to the evenly and oddly graded parts of the rings separately. The formalism that showed that flat maps over the moduli stack of formal groups give rise to homology theories does go through to the general setting (Prop. 2.27 and Cor. 2.29). However, it is then very hard to recognise the flat maps. The criterion given by Landweber guaranteeing flatness of a map on the moduli stack of formal groups heavily relies on a good understanding of the Hopf algebroid $\left(M U_{*}, M U_{*}(M U)\right)$. In general, we simply do not have this. We do notice though that there is a verifiable criterion to identify flat maps over the stack associated to the spectrum $P(n)$ (Cor. 2.4) and construct homology theories from them. Morava K-theory can be recovered as one example. This observation was already made by Yagita in [26], but the approach taken here is slightly different. Even if, up to details, all the tools can be found in the literature, this approach seems to be uncommon.

# Outline 

In the first section, we introduce the reader to the world of stacks, setting up the language we will need afterward. We assume some familiarity with the basic concepts from algebraic geometry such as sheaves, schemes, their functor of points interpretation or Grothendieck topologies. We quickly specialise to the study of algebraic stacks and attempt to give plenty of details on the proofs and ideas that are often taken for granted in the literature. Then, in subsection 1.2, we explain the connection between Hopf algebroids and stacks, introducing the concepts we will need to prove the equivalence of categories between the 2-category of flat Hopf algebroids and that of rigidified algebraic stacks (Thm. 1.40). The last subsection brings spectra into the picture by constructing a Hopf algebroid associated to nice enough spectra (Cor. 1.3). Then, we define the stack associated to these spectra using the equivalence of categories from theorem 1.40. We detail the example of the moduli stack of formal groups as the stack associated to $M U$.

The second section is an attempt to construct new homology theories from known spectra as outlined above. We set up the machinery of quasicoherent sheaves over a stack to rephrase exactness of the functor $h_{f}$ in terms of exactness over the associated stack (Prop. 2.27). This gives two formal statements on how to construct homology theories from flat maps over a stack (Cor. 2.28 and Cor. 2.29). We accord particular care to gradings. Then, we specialise to $M U$ and reprove the Landweber exact functor theorem detailing the outline given in [15, Lect. 16]. Among other results on spectra arising from the Landweber exact functor theorem, we give a proof for the fact that these spectra are homotopy commutative ring spectra, a fact that is usually mentioned but not shown in the books. Finally, we generalise the proof just done to give a "Landweber exact functor theorem for $P(n)$ ".

Having understood that it is usually too hard to construct new homology theories from other spectra than $M U$, the last section focuses on the construction of spectra via the Landweber exact functor theorem and interesting formal group laws. These formal group laws arise from elliptic curves. In fact, we will describe the ideas mentioned above leading to the construction of elliptic homology theories. This section will underline the interplay between algebraic geometry and topology that was already running through the previous two sections. We begin by introducing elliptic curves, first over fields, than over a general base scheme and explain their relationship to formal groups. Then, we outline the construction of elliptic cohomology theories (Thm. 3.35). We conclude by taking advantage of the fact that we already introduced the stacky formalism and reinterpret some previous results in the light of the moduli stack of elliptic curves. In particular, we show that there is a flat map from this stack to the moduli stack of formal groups, giving particular care to representability of the map (Thm. 3.43).

## Acknowledgements

Mathematically speaking, I owe the most to my supervisor Dr. Jack Davies. Thank you, Jack, for the most enjoyable introduction to the beginnings of algebraic topology during last year's Topology II lecture and for demystifying the world of spectra in this Spring's Algebraic Topology II class. Thank you for encouraging me to take up a master's thesis in this wonderful area despite my important lack of background and for your endless patience with my numerous questions. I am deeply grateful for your unwavering support throughout the year, especially when it meant reading a motivation letter in the middle of Christmas break. It is, in my eyes, largely due to you that I am lucky enough to continue my topological journey in Utrecht. I could not have dreamt of any better mentor.
I am also obliged to Prof. Dr. Markus Hausmann for agreeing to be my second advisor and for helping me overcome my fear of spectral sequences during the excellent Algebraic Topology I lecture he taught this winter.
Finally, I would like to express my gratitude to my "topology friends", David Bowman and Emanuele Cortinovis for showing me how enlightening mathematical discussions can be. Many thanks to both of you for all these questions we solved together. Thank you, Ema, for always believing in me (mathematically and at the climbing gym). Thank you, David, for making me feel heard and, of course, for proofreading this thesis. You have been a great help with catching various typos. Hopefully, we caught them all.

# 1 Stacks 

In this section, the concept of (algebraic) stacks will be introduced. The formal setting provided by stacks will give rise to powerful tools for algebraic topology which we will begin to explore in subsection 1.3. We will have to wait until 2 to see a concrete application of the formalism provided by stacks to the task of constructing new spectra. We follow the approach taken in [18], mainly complemented by input from [13], but we will mostly detail the statements that seem to be taken for granted in the literature.

### 1.1 First Definitions

As just explained, we would like to introduce tools from algebraic geometry to algebraic topology. However, the main object of concern in algebraic geometry, sheaves with values in Sets, are often too rigid for topologists, as the following example highlights:

Example 1.1. Let $X$ be a topological space and let $O u v_{X}$ denote the poset of open subsets of $X$ ordered by inclusion. Define a presheaf $\operatorname{Vect}_{n}: O u v_{X}^{\text {op }} \rightarrow$ Sets given on objects by

$$
U \mapsto \operatorname{Vect}_{n}(U)=\{\text { isomorphism classes of n-dimensional vector bundles on } U\}
$$

Following the above philosophy, we would like this to be a sheaf. However, this would imply that whenever $X$ admits a cover $\left\{U_{i}\right\}_{i}$ of contractible opens, $\operatorname{Vect}_{n}(X)$ is trivial. Indeed, as the only $n$-dimensional vector bundle over a contractible space is the trivial one, each $\operatorname{Vect}_{n}\left(U_{i}\right)$ consists of a single element. By the sheaf condition, any object of $\operatorname{Vect}_{n}(X)$ must be equal to the glueing of its restrictions to the $U_{i}$. As each of these restrictions must be trivial and the glueing is unique, $\operatorname{Vect}_{n}(X)$ consists of a single element, the trivial $n$-bundle, as well. In a slogan, "sheaves only allow for glueing trivial objects in a trivial manner".
Hence, asking for $\operatorname{Vect}_{n}(U)$ to be a sheaf would yield very boring topology. For example, $\operatorname{Vect}_{1}\left(S^{1}\right)$ would be a single element as it can be covered by the contractible opens $U_{1}=S^{1} \backslash\{N\}$ and $U_{2}=S^{1} \backslash\{S\}$. We would then live in a world without the Möbius bundle.

The problem here is that a vector bundle is not characterised by its restrictions to some open sets, but by the datum that encodes how these restrictions are glued together. What object can describe this? One might expect it to be a 2 -categorical version of a sheaf that will keep track of the glueing of both objects and morphisms. This idea takes shape in the concept of the stack.

Definition 1.2. - A $T$-stack of groupoids on a site $(\mathcal{C}, T)$ is a pseudofunctor $\mathcal{X}: \mathcal{C}^{o p} \rightarrow$ Groupoids such that

1. For each $U \in O b(\mathcal{C}), Y, Z \in \mathcal{X}(U)$, the presheaf $\underline{\operatorname{Isom}}(Y, Z)^{1}$ on $U$ is a $T$-sheaf.
2. (effective descent) Given any $T$-cover $\left\{U_{i} \rightarrow U\right\}_{i}$, objects $E_{i} \in \mathcal{X}\left(U_{i}\right)$ and isomorphisms $f_{i j}:\left(E_{j}\right)\left|{ }_{U_{i} \times_{U} U_{j}} \rightarrow\left(E_{i}\right)\right|_{U_{i} \times_{U} U_{j}}$ such that $f_{i j} \circ f_{j k}=f_{i k}$ on $U_{i} \times_{U} U_{j} \times_{U} U_{k}$, there is an object $E \in \mathcal{X}(U)$ with isomorphisms $\phi_{i}: E|_{U_{i}} \rightarrow E_{i}$ such that $f_{i j} \circ \phi_{j}=\phi_{i}$ on $U_{i} \times_{U} U_{j}$.
- A pseudofunctor $\mathcal{X}$ satisfying only the first condition is a prestack.

Here the restriction $\left(E_{i}\right) \|_{U_{i} \times_{U} U_{j}}$ is notation for $\mathcal{X}\left(p_{i}\right)\left(E_{i}\right)$ where $p_{i}: U_{i} \times_{U} U_{j} \rightarrow U_{i}$ is the projection. Whenever the maps are clear, we will use this notation. When the stack is clear but the maps are not, we will also use $p_{i}^{*}$ to denote $\mathcal{X}\left(p_{i}\right)\left(E_{i}\right)$.
Let us go back to the example of vector bundles and attempt to see $\operatorname{Vect}_{n}$ as a stack.
Example 1.3. As observed before, in order to encode the isomorphism classes of vector bundles over some space in a meaningful way, we must not only keep track of the bundles themselves, but also of the isomorphisms between them.
This brings us to consider the pseudofunctor $\mathcal{V e c t}_{n}: \operatorname{Ouv}_{X}^{\text {op }} \rightarrow$ Groupoids where $\mathcal{V e c t}_{n}(U)$ is the category whose objects are n-dimensional vector bundles on $U$ and whose morphisms are the isomorphisms of vector bundles. This construction is pseudofunctorial as the restriction maps are given by pulling back vector bundles. This functor defines a stack (the Grothendieck topology on $O u v_{X}$ is the one induced from the topology on $X$ ):

[^0]
[^0]:    ${ }^{1}$ Observe that as $\mathcal{X}(U)$ is a groupoid, $\operatorname{Isom}_{\mathcal{X}(U)}(Y, Z)=\operatorname{Hom}_{\mathcal{X}(U)}(Y, Z)$. Hence, by isomorphism presheaf, we mean the usual internal Hom presheaf, i.e. the functor $\underline{\operatorname{Hom}}(Y, Z): \mathcal{C}_{/ U}^{\text {op }} \rightarrow$ Grpds given on objects by $V \mapsto \operatorname{Hom}_{\mathcal{X}(V)}(Y|_{V}, Z|_{V})$ where the restriction notation is as explained after the definition.

1. Let $U \in O u v_{X}, E, F \in \mathcal{V} e c t_{n}(U)$. Then, $\underline{\operatorname{Isom}}(E, F)$ forms a sheaf on $U$ in the usual way sets of functions form a sheaf.
2. Consider an open cover $\cup_{i} U_{i}=X$ and vector bundles $E_{i} \in \mathcal{V}$ ect $_{n}\left(U_{i}\right)$ together with isomorphisms $\varphi_{i j}: E_{i}\left|{ }_{U_{i} \cap U_{j}} \rightarrow E_{j}\right|_{U_{i} \cap U_{j}}$. These can be glued to an n-dimensional vector bundle $E$ on $X$ with isomorphism $\psi_{i}: E|_{U_{i}} \rightarrow E_{i}$ satisfying $\varphi_{i j} \circ \psi_{i}=\varphi_{j i} \circ \psi_{j}$ by setting $E=\sqcup_{i} E_{i} / \sim$ where $\sim$ is the equivalence relation given by $\left[(p, v) \in E_{i}\left|{ }_{U_{i} \cap U_{j}}\right| \sim\left[\left(p, \varphi_{i j}(v)\right) \in E_{j}\left|{ }_{U_{i} \cap U_{j}}\right|\right.\right.$ for all $\left.i, j\right)$. One should check that this indeed defines a vector bundle (i.e. that it is locally trivial).

The glueing is now possible because working over groupoids keeps track of the explicit glueings between the bundles on each cover.

In our applications, $\mathcal{C}$ will usually be the category of affine schemes and $T$ the fpqc-topology. Whenever not stated otherwise, from now on, a stack will be a contravariant pseudofunctor from affine schemes with the fpqc-topology to groupoids satisfying the conditions of definition 1.2. It is important to notice that no generality was lost when introducing stacks. As the following example shows, we can make sense of sheaves also in this context and still have all the usual framework to do algebraic geometry in.

Example 1.4. There is a functor $i:$ Sets $\rightarrow$ Groupoids given by mapping a set $A$ to the category with objects the elements of $A$ and whose only morphisms are the identity. Given a pseudofunctor $F:(\mathcal{C}, T) \rightarrow$ Sets, we wonder when $i \circ F$ is a stack. We would call this a discrete stack. As the only isomorphisms are the identities, the second condition of definition 1.2 rewrites with equalities instead of isomorphisms and becomes the glueing condition for sheaves. The first condition is equivalent to requiring uniqueness of the glued section. Hence, $i \circ F$ is a stack if and only if $F$ is a sheaf.
In particular, any scheme can be considered as a discrete stack by identifying the scheme with its functor of points and postcomposing with $i$. We will usually suppress $i$ from the notation and simply identify all sheaves with the corresponding stack wherever it makes sense.

Stacks form a 2-category.
Definition 1.5. A 1-morphism of stacks $\mathcal{X} \xrightarrow{F} \mathcal{Y}$ is a "natural transformation of pseudofunctors". More precisely, for every $U \in O b(\mathcal{C})$, one gets a functor $\mathcal{X}(U) \xrightarrow{F(U)} \mathcal{Y}(U)$ that is compatible with the restrictions i.e. given any $V \xrightarrow{i} U \in \operatorname{Mor}(\mathcal{C})$ then for all $x \in \mathcal{X}(U)$ there is a given isomorphism $F_{V}\left(i^{*}(x)\right) \cong i^{*}\left(F_{U}(x)\right)$ (this is part of the datum of a 1-morphism).
A 2-morphism of stacks $F \xrightarrow{\psi} G$ with $F, G: \mathcal{X} \rightarrow \mathcal{Y}$ two 1-morphisms is, for every $U \in O b(\mathcal{C})$, a natural transformation $\psi_{U}: F(U) \rightarrow G(U)$ that is compatible with the restriction maps i.e. such that the following diagram commutes for all $x \in O b(\mathcal{X}(U))$ and $V \xrightarrow{i} U \in \operatorname{Mor}(\mathcal{C})$ :

One checks that there is a well-defined associative composition of 1- and 2-morphisms as well as identities and that these define a 2-category Stacks whose objects are the stacks, 1- and 2-morphisms as just defined; see [13, (2.2), Def. 3.1] for details.

Remark 1.6. Given a stack $\mathcal{X}$, any object $x \in \mathcal{X}(U)$ corresponds, by the Yoneda lemma, to a morphism $U \rightarrow \mathcal{X}$, which, abusing notation, will also be denoted by $x$. More precisely, given an object $x$, we construct the morphism $x$ by setting $x\left(i d_{U}\right)=x$ and extending functorially. More precisely, given an object $f: V \rightarrow U \in U(V)$, we define $x(f):=f^{*}(x)=f^{*}\left(x\left(i d_{U}\right)\right)$. By construction, this defines a morphism of stacks. Conversely, a given morphism $F: U \rightarrow \mathcal{X}$ is associated to the object $F\left(i d_{U}\right)$. These constructions are inverses as pseudofunctoriality fixes an isomorphism $F(f)=F\left(f^{*}\left(i d_{U}\right)\right) \cong f^{*}\left(F\left(i d_{U}\right)\right)$.

Definition 1.7 ([13, Def. 3.6, (2.2)]). A morphism of stacks $\phi: \mathcal{X} \rightarrow \mathcal{Y}$ is an epimorphism if for all affine schemes $U$ and every $y \in O b(\mathcal{Y}(U))$ there exists a faithfully flat morphism $\varphi: U^{\prime} \rightarrow U$ and $x \in \mathcal{X}\left(U^{\prime}\right)$ such that $y \mid U^{\prime} \cong \phi(x)$.
It is a monomorphism if $\phi(U)$ is fully faithful for all $U$.
It is an isomorphism if $\phi(U)$ is an equivalence of categories for all $U$.

Remark 1.8. One can show that a morphism of stacks is an isomorphism if and only if it is both an epimorphism and a monomorphism. We will only use this statement once in the proof of 1.40 . We refer the reader to [13, Prop. 3.7, Cor 3.7.1] for the proof.

One can show that the category Stacks is complete and cocomplete as a 2-category (see [13, (2.2.14),(3.3)]). Except for fiber products, we will not need any of these constructions. Let us outline the construction for fiber products.

Example 1.9 ([13, (2.2.2), (3.3)]). Given a span of 1-morphisms of stacks $\mathcal{X} \xrightarrow{F} \mathcal{Z} \stackrel{G}{\leftarrow} \mathcal{Y}$, we define a pseudofunctor

$$
\mathcal{X} \times_{\mathcal{Z}} \mathcal{Y}: \operatorname{Aff}^{o p} \rightarrow \text { Groupoids }
$$

given on the objects by defining $\mathcal{X} \times_{\mathcal{Z}} \mathcal{Y}(U)$ to be the category whose objects are triples $(x, y, g)$ with $x \in O b(\mathcal{X}(U)), y \in O b(\mathcal{Y}(U))$ and $F(x) \xrightarrow{g} G(y) \in \operatorname{Mor}(\mathcal{Z}(U))$. A morphism $(x, y, g) \rightarrow\left(x^{\prime}, y^{\prime}, g^{\prime}\right)$ in $\mathcal{X} \times_{\mathcal{Z}} \mathcal{Y}(U)$ is a pair $\left(x \xrightarrow{f} x^{\prime}, y \xrightarrow{f^{\prime}} y^{\prime}\right) \in \operatorname{Mor}(\mathcal{X}(U)) \times \operatorname{Mor}(\mathcal{Y}(U))$ such that $G\left(f^{\prime}\right) \circ g=g^{\prime} \circ F(f)$. Given a morphism $V \xrightarrow{i} U$, we define $\mathcal{X} \times_{\mathcal{Z}} \mathcal{Y}(i)$ on objects by $\mathcal{X} \times_{\mathcal{Z}} \mathcal{Y}(i)\left(x, x^{\prime}, g\right)=\left(i^{*}(x), i^{*}\left(x^{\prime}\right), i^{*}(g)\right)$ and similarly on morphisms. One checks that this is well-defined and defines a stack which furthermore is the (2-categorical) limit ${ }^{2}$ of the span we began with.

Remark 1.10. It is often useful to notice the following connections between the sheaves of isomorphisms and certain fiber products. Consider two morphisms $x_{1}: \operatorname{Spec}(S) \rightarrow \mathcal{X}$ and $x_{2}: \operatorname{Spec}(T) \rightarrow \mathcal{X}$ to some stack $\mathcal{X}$, corresponding to objects $x_{1} \in \mathcal{X}(S)$ and $x_{2} \in \mathcal{X}(T)$ by remark 1.6. Then, there is an isomorphism

$$
\operatorname{Spec}(S) \times_{x_{1}, \mathcal{X}, x_{2}} \operatorname{Spec}(T) \cong \underline{\operatorname{Isom}}_{\operatorname{Spec}(S) \times \operatorname{Spec}(T)}\left(p_{S}^{*}\left(x_{1}\right), p_{T}^{*}\left(x_{2}\right)\right)
$$

where $p_{S}: \operatorname{Spec}(S) \times \operatorname{Spec}(T) \rightarrow \operatorname{Spec}(S)$ is the projection to $\operatorname{Spec}(S)$ and $p_{T}$ is the projection to $\operatorname{Spec}(T)$. This is clear as, by definition, an element of the fiber product $\operatorname{Spec}(S) \times_{x_{1}, \mathcal{X}, x_{2}} \operatorname{Spec}(T)(U)$ corresponds to a triple $\left(a: U \rightarrow \operatorname{Spec}(S), b: U \rightarrow \operatorname{Spec}(T), \phi: x_{1}^{*}(a) \cong x_{2}^{*}(b)\right)$ and an element of $\underline{\operatorname{Isom}}_{\operatorname{Spec}(S) \times \operatorname{Spec}(T)}\left(p_{S}^{*}\left(x_{1}\right), p_{T}^{*}\left(x_{2}\right)\right)(U)$ corresponds to a morphism $(a, b): U \rightarrow \operatorname{Spec}(S) \times \operatorname{Spec}(T)$ and an isomorphism $(a, b)^{*} p_{S}^{*}\left(x_{1}\right)=a^{*}\left(x_{1}\right) \cong(a, b)^{*} p_{T}^{*}\left(x_{2}\right)=b^{*}\left(x_{2}\right)$; see [6, Cor. 2.21].
The same argument shows that, for $T=S$,

$$
\underline{\operatorname{Isom}}_{\operatorname{Spec}(S)}\left(x_{1}, x_{2}\right) \cong \operatorname{Spec}(S) \times_{\left(x_{1}, x_{2}\right), \mathcal{X} \times \mathcal{X}, \Delta} \mathcal{X}
$$

where $\Delta$ denotes the diagonal. Indeed, an element of $\operatorname{Spec}(S) \times_{\left(x_{1}, x_{2}\right), \mathcal{X} \times \mathcal{X}, \Delta} \mathcal{X}(U)$ corresponds to a triple $\left(m \in \mathcal{X}(U), f: U \rightarrow \operatorname{Spec}(S), \phi:\left(f^{*}\left(x_{1}\right), f^{*}\left(x_{2}\right)\right) \cong(m, m)\right)$ which is precisely an isomorphism $f^{*}\left(x_{1}\right) \cong f^{*}\left(x_{2}\right)$; see $[6$, Thm. 2.30].
Similarly, one shows ([6, after Lem. 2.11]) that

$$
\left(\operatorname{Spec}(S) \times_{x_{1}, \mathcal{X}, x_{2}} \operatorname{Spec}(S)\right) \times_{\operatorname{Spec}(S) \times \operatorname{Spec}(S)} \operatorname{Spec}(S) \cong \underline{\operatorname{Isom}}\left(x_{1}, x_{2}\right)
$$

Summing up, one has the following three cartesian diagrams:
![img-0.jpeg](img-0.jpeg)

[^0]For any stack $\mathcal{T}$ with 1-morphisms $f, g$ and a 2-morphism $\psi$ that $\pi_{X} \circ f \cong \pi_{g} \circ g$, there exists a unique 1-morphism $h$ as in the diagram and unique 2-morphisms $\alpha$ and $\beta$ such that everything commutes appropriately.


[^0]:    ${ }^{2}$ i.e. it satisfies the following universal property:

![img-1.jpeg](img-1.jpeg)
and

$$
\begin{aligned}
& \underline{\underline{I s o m}_{\operatorname{Spec}(S)}\left(x_{1}, x_{2}\right) \longrightarrow \operatorname{Spec}(S) \times_{\mathcal{X}} \operatorname{Spec}(S)} \\
& \downarrow \\
& \operatorname{Spec}(S) \xrightarrow[\left(x_{1}, x_{2}\right)]{ } \operatorname{Spec}(S) \times \operatorname{Spec}(S) .
\end{aligned}
$$

Be warned that these diagrams are not strictly commutative, only commutative in the 2-categorical sense, i.e. there is an implicit given isomorphism witnessing commutativity. This isomorphism is given by the composition of the isomorphism between the fiber product and the isomorphism presheaf described above and $\phi$ coming from the construction of the pullback. In what follows, like was done here, we will usually not make these isomorphisms explicit and always keep in mind that the diagrams we consider are merely 2 -commutative.

Having pullbacks enables us to translate concepts used for morphisms of schemes to morphisms of stacks when they are nice enough.

Definition 1.11. A morphism of stacks $\phi: \mathcal{X} \rightarrow \mathcal{Y}$ is representable if, for any morphism $f: \operatorname{Spec}(R) \rightarrow \mathcal{Y}$ from an affine scheme (viewed as stack), the fiber product $\operatorname{Spec}(R) \times_{\mathcal{Y}} \mathcal{X}$ is equivalent to a scheme.

Although we will mostly deal with representable morphisms, let us mention that there exist reasonable morphisms between stacks that are not representable. We will have to wait until example 3.42 for an explicit example. The following lemma will be one of the main ingredients for the proofs in the remainder of this section.

Lemma 1.12. Consider a 2-cartesian diagram of stacks
![img-2.jpeg](img-2.jpeg)

If $f$ is representable, then so is $f^{\prime}$ (i.e. representable satisfies base change). Moreover, if $g$ and $g^{\prime}$ are epimorphisms and $f^{\prime}$ is representable, then $f$ is representable as well.

Proof. Suppose that $f$ is representable and consider some morphism $h: \operatorname{Spec}(R) \rightarrow \mathcal{Z}$. We need to show that $P$ in the following diagram is equivalent to a scheme
![img-3.jpeg](img-3.jpeg)

By pullback pasting, $P$ is equivalent to the fibre product $\mathcal{X} \times_{f, \mathcal{Y}, g \circ h} \operatorname{Spec}(R)$ which is a scheme as $f$ is representable. The proof of the second statement is more involved and can be looked up in [13, Lem. 4.4.3].

Representable morphisms allow for natural extensions of certain definitions made for schemes to stacks.
Definition 1.13. Let $\mathcal{P}$ be any property of morphisms of schemes that satisfies base change (such as affine, flat...). A representable morphism of stacks $\phi: \mathcal{X} \rightarrow \mathcal{Y}$ is said to satisfy $\mathcal{P}$ if for all morphisms from an arbitrary affine scheme $f: \operatorname{Spec}(R) \rightarrow \mathcal{Y}$, the base change of $f, f^{\prime}: \operatorname{Spec}(R) \times_{\mathcal{Y}} \mathcal{X} \rightarrow \operatorname{Spec}(R)$, satisfies $\mathcal{P}$ as morphism of schemes.

In what follows, we might say that a morphism satisfies the property $\mathcal{P}$ without specifying that it is representable. This will always be implicit. Let us give an example illustrating why the previous definition is sensible. As we are working with the fpqc-topology, one would expect a faithfully flat morphism of stacks to be some sort of covering. The following proposition shows that it is at least surjective up to a cover.

Proposition 1.14. If a representable morphism of stacks $\phi: \mathcal{X} \rightarrow \mathcal{Y}$ is faithfully flat and affine, then it is an epimorphism.

Proof. Let $U$ be some affine scheme. Recall from remark 1.6, that $y \in O b(\mathcal{Y}(U))$ defines a unique morphism of stacks $y: U \rightarrow \mathcal{Y}$. Form the following pullback diagram:
![img-4.jpeg](img-4.jpeg)

As $\phi$ is affine, $U \times_{\mathcal{Y}} \mathcal{X}$ is equivalent to some affine scheme. Hence, as was argued above for $y$, the morphism $x$ determines an element $x:=x\left(i d_{U \times \mathcal{Y} \mathcal{X}}\right) \in \mathcal{X}\left(U \times_{\mathcal{Y}} \mathcal{X}\right)$. As $\phi$ was assumed to be faithfully flat, so is $\phi^{\prime}$ and it exhibits $U \times_{\mathcal{Y}} \mathcal{X}$ as an fpqc-cover of $U$. Commutativity of the pullback diagram up to a 2 -isomorphism gives that $\left.y\right|_{U \times \mathcal{Y} \mathcal{X}}:=y \circ \phi^{\prime}\left(i d_{U \times \mathcal{Y} \mathcal{X}}\right) \cong \phi \circ x\left(i d_{U \times \mathcal{Y} \mathcal{X}}\right):=\phi(x)$ as claimed.

Remark 1.15. Let $\mathcal{P}$ be as in definition 1.13 and consider a 2-cartesian diagram of stacks
![img-5.jpeg](img-5.jpeg)

Observe that, by the same pullback pasting argument as in lemma 1.12, if $f$ satisfies $\mathcal{P}$, then so will $f^{\prime}$. If furthermore, $\mathcal{P}$ satisfies fpqc-descent and $g$ and $g^{\prime}$ are faithfully flat and affine and $f^{\prime}$ satisfies $\mathcal{P}$, then so does $f$.
To see this, notice first that by lemma 1.12 and proposition $1.14 f$ is also representable. Then, given a morphism $h: \operatorname{Spec}(R) \rightarrow \mathcal{Y}$, we need to show that its base change $h_{f}: \operatorname{Spec}(R) \times_{\mathcal{Y}} \mathcal{X} \rightarrow \operatorname{Spec}(R)$ satisfies $\mathcal{P}$. By proposition 1.14 , the morphism $g$ is an epimorphism. Hence, by definition, there exists a faithfully flat morphism $q: \operatorname{Spec}(S) \rightarrow \operatorname{Spec}(R)$ such that $h \circ q$ factors through $g$ as depicted in the following diagram
![img-6.jpeg](img-6.jpeg)

By base change, $f^{\prime \prime}$ satisfies $\mathcal{P}$. Consider further the diagram
![img-7.jpeg](img-7.jpeg)

By pullback pasting, all squares in the above diagram are cartesian and by base change $q^{\prime}$ is also faithfully flat. Then, by fpqc-descent $h_{f}$ satisfies $\mathcal{P}$ as was to be shown.

From now on, we will often use the previous remark tacitly. It seems reasonable to ask for all the morphisms from some affine scheme into a given stack to be representable. In the following, we will focus on a subcategory of stacks having this property. We will adopt the following definition in accordance with [16, Def. 4.37], as it will be the most convenient for what follows. In remark 1.19, another definition, common in the literature, will be discussed.

Definition 1.16. A stack $\mathcal{X}$ such that there exists some morphism $P: \operatorname{Spec}(S) \rightarrow \mathcal{X}$ that is representable, affine and faithfully flat is called algebraic. The map $P$ is a presentation for $\mathcal{X}$.
A rigidified algebraic stack is an algebraic stack $\mathcal{X}$ together with a given presentation $P$ (the presentation is now part of the data).
Definition 1.17. Rigidified algebraic stacks assemble into a 2-category $\mathcal{S}$. More precisely, the objects of $\mathcal{S}$ are presentations $P: \operatorname{Spec}(S) \rightarrow \mathcal{X}$ as defined in definition 1.16. A 1-morphism from a presentation $P: \operatorname{Spec}(S) \rightarrow \mathcal{X}$ to $P^{\prime}: \operatorname{Spec}\left(S^{\prime}\right) \rightarrow \mathcal{Y}$ is a pair $\left(f_{0}, f\right)$ where $f_{0}: \operatorname{Spec}(S) \rightarrow \operatorname{Spec}\left(S^{\prime}\right)$ is a morphism of affine schemes and $f: \mathcal{X} \rightarrow \mathcal{Y}$ a 1-morphism of stacks such that the following diagram is 2-commutative
![img-8.jpeg](img-8.jpeg)

Composition of 1-morphisms is component-wise. Given two 1-morphisms $\left(f_{0}, f\right),\left(g_{0}, g\right):(\operatorname{Spec}(S) \rightarrow$ $\mathcal{X}) \rightarrow\left(\operatorname{Spec}\left(S^{\prime}\right) \rightarrow \mathcal{Y}\right)$, a 2-morphism from $\left(f_{0}, f\right)$ to $\left(g_{0}, g\right)$ is simply a 2-morphism from $f$ to $g$ in the 2-category of stacks.
Remark 1.18. If $\mathcal{X}$ is algebraic, it follows from the definitions that any morphism $f: \operatorname{Spec}(R) \rightarrow \mathcal{X}$ is representable and even affine. Indeed, we want to see that given any morphism $g: \operatorname{Spec}\left(R^{\prime}\right) \rightarrow \mathcal{X}$, the pullback $\operatorname{Spec}\left(R^{\prime}\right) \times_{\mathcal{X}} \operatorname{Spec}(R)$ is equivalent to some affine scheme. Let $P: \operatorname{Spec}(S) \rightarrow \mathcal{X}$ be a presentation for $\mathcal{X}$ and consider the pullback square
![img-9.jpeg](img-9.jpeg)

As $P$ is representable and affine, $\operatorname{Spec}(R) \times_{\mathcal{X}} \operatorname{Spec}(S)$ is equivalent to an affine scheme which we call $\operatorname{Spec}(A)$. Moreover, by base change, $P^{\prime}$ is also representable, affine and faithfully flat. In particular, as affine morphisms are quasi-compact, $\left\{P^{\prime}\right\}$ is an fpqc-cover of $\operatorname{Spec}(R)$. As affine is a property that is fpqc-local on the target, it suffices to show that $g^{\prime \prime}$ in the following diagram is affine
![img-10.jpeg](img-10.jpeg)

Then, $g^{\prime}$ will be affine as well by fpqc-descent and this implies that $\operatorname{Spec}\left(R^{\prime}\right) \times_{\mathcal{X}} \operatorname{Spec}(R)=g^{\prime-1}(\operatorname{Spec}(R))$ is some affine scheme as wanted. We claim that $\operatorname{Spec}\left(R^{\prime}\right) \times_{\mathcal{X}} \operatorname{Spec}(A) \simeq \operatorname{Spec}(R) \times_{\mathcal{X}} \operatorname{Spec}\left(R^{\prime}\right) \times_{\mathcal{X}} \operatorname{Spec}(S)$ is equivalent to some affine scheme. Recall that by assumption $\operatorname{Spec}\left(R^{\prime}\right) \times_{\mathcal{X}} \operatorname{Spec}(S)$ is equivalent to an affine scheme which we denote by $\operatorname{Spec}(B)$. The claim then follows from pullback pasting and the following commutative diagram:
![img-11.jpeg](img-11.jpeg)

More precisely, as both inner squares are pullbacks, so is the outer square and $\operatorname{Spec}(R) \times_{\mathcal{X}} \operatorname{Spec}\left(R^{\prime}\right) \times_{\mathcal{X}}$ $\operatorname{Spec}(S) \simeq \operatorname{Spec}\left(A \otimes_{S} B\right)$ is affine. Then $g^{\prime \prime}$, being a map between affine schemes, is affine.

Remark 1.19. In the literature, for example in [18, Def. 6] or [13, Def. 4.1], one often finds algebraic stack to be defined as a stack $\mathcal{X}$ whose diagonal $\Delta_{\mathcal{X}}: \mathcal{X} \rightarrow \mathcal{X} \times \mathcal{X}$ is representable and affine and such that there exists some affine scheme $\operatorname{Spec}(S)$ together with a faithfully flat map $P: \operatorname{Spec}(S) \rightarrow \mathcal{X}$. Moreover, algebraic geometers often ask for $P$ to also be smooth (see [13, Def. 4.1]). This condition is usually dropped by algebraic topologists as, as we will see in remark 1.69, one of the most useful examples involves a non-smooth presentation. From this alternative definition arise two questions: why can we ask for $P$ to be faithfully flat, is it representable? Why is this the same as our definition? Both these questions are solved by the claim that the diagonal is representable if and only if any morphism $f: \operatorname{Spec}(R) \rightarrow \mathcal{X}$ is representable. For the proof, recall from general category theory that the following diagram is cartesian ("magic square")

$$
\begin{aligned}
& \operatorname{Spec}(R) \times_{\mathcal{X}} \operatorname{Spec}\left(R^{\prime}\right) \longrightarrow \operatorname{Spec}(R) \times \operatorname{Spec}\left(R^{\prime}\right) \\
& \downarrow \\
& \mathcal{X} \xrightarrow[\Delta_{\mathcal{X}}]{(f, g)} \mathcal{X} \times \mathcal{X}
\end{aligned}
$$

Hence if the diagonal is representable and affine, the pullback $\operatorname{Spec}(R) \times_{\mathcal{X}} \operatorname{Spec}(S)$ is equivalent to some affine scheme by definition.
For the converse, we need to show that given any morphism $(f, g): \operatorname{Spec}(R) \rightarrow \mathcal{X} \times \mathcal{X}$, its pullback along $\Delta_{\mathcal{X}}$ is equivalent to an affine scheme. Observe that $(f, g)$ factors through the diagonal of $\operatorname{Spec}(R)$ and fits into the following commutative diagram:
![img-12.jpeg](img-12.jpeg)

The right-hand square is cartesian as it is the magic square and the left-hand square is cartesian by construction. The pullback $\operatorname{Spec}(R) \times_{\mathcal{X}} \operatorname{Spec}(R)$ is equivalent to an affine scheme because both $f$ and $g$ are now assumed to be representable (actually it suffices for one of them to be representable). By pullback pasting, the top left corner is uniquely isomorphic to $\operatorname{Spec}(R) \times_{\mathcal{X} \times \mathcal{X}} \mathcal{X}$ which is thus equivalent to an affine scheme as claimed.
Remark 1.20. In view of the previous remark and remark 1.10, the condition that $\Delta$ is representable and affine is equivalent to all isomorphism sheaves being affine schemes.

# 1.2 Stacks and Hopf algebroids 

Hopefully, the previous subsection has made clear to the reader why it is convenient to introduce stacks in addition to sheaves if one wants to do algebraic geometry in a topological setting. Moreover, it should seem believable that, at least for rigidified algebraic stacks, many notions can be carried over. However, we have not given many examples of stacks yet and have provided no guidance for tasks like checking if a given morphism is representable or even flat. In this subsection, we expose a deep connection between certain algebraic objects, the flat Hopf algebroids, and rigidified algebraic stacks. In fact, as shown in theorem 1.40, these two categories are equivalent. This will have many useful properties in practice, which we will exploit throughout the remaining sections. For more concrete and geometric examples, as well as a link to certain ring spectra, the reader will have to wait until the next subsection.
Let us begin by introducing the main objects of interest for this section.
Definition 1.21. A groupoid object in affine schemes is a pair of affine schemes $\left(X_{0}, X_{1}\right)$ together with five morphisms of affine schemes: source $s: X_{1} \rightarrow X_{0}$, target $t: X_{1} \rightarrow X_{0}$, unit $e: X_{0} \rightarrow X_{1}$, composition $m: X_{1} \times_{s, X_{0}, t} X_{1} \rightarrow X_{1}$ and inverse $i: X_{1} \rightarrow X_{1}$ satisfying the following axioms:

1. $s \circ e=t \circ e=i d_{X_{0}}, t \circ i=s, s \circ i=t, s \circ m=s \circ p r_{2}, t \circ m=t \circ p r_{1}$.
2. (Associativity) $m$ is associative i.e. the following diagram commutes
![img-13.jpeg](img-13.jpeg)

3. (Neutral element) The composites $X_{1}=X_{1} \times_{s, X_{0}} X_{0} \xrightarrow{i d \times e} X_{1} \times_{s, X_{0}, t} X_{1} \xrightarrow{m} X_{1}$ and $X_{1}=$ $X_{0} \times_{X_{0}, t} X_{1} \xrightarrow{i d \times e} X_{1} \times_{s, X_{0}, t} X_{1} \xrightarrow{m} X_{1}$ are equal to the identity on $X_{1}$, i.e. $e$ is a two-sided neutral element for $m$.
4. (Inverses) The following two squares commute:

$$
\begin{array}{cccc}
X_{1} & \xrightarrow{i \times i d} X_{1} \times_{s, X_{0}, t} X_{1} & X_{1} \xrightarrow{i d \times i} X_{1} \times_{s, X_{0}, t} X_{1} \\
\downarrow & & \downarrow^{m} & \\
X_{0} & \text { e } & X_{1}, & \\
& & \\
& & \\
& & \\
& X_{0} & X_{1}
\end{array}
$$

and $i \circ i=i d_{X_{1}}$.
Example 1.22. Any affine scheme $X$ can be seen as a groupoid object in affine schemes by identifying it with $(X, X)$ and defining all the structure maps to be the identity.

The corresponding notion in the category of commutative rings under the equivalence of categories $\mathrm{Aff}^{\text {op }} \simeq C$ Rings is that of an Hopf algebroid.

Definition 1.23 ([19, Def. A1.1.1]). A Hopf algebroid is a cogroupoid object in commutative rings. More concretely, it is a pair of commutative rings $(A, \Gamma)$ together with five morphisms of rings left unit $\eta_{L}: A \rightarrow \Gamma$, right unit $\eta_{R}: A \rightarrow \Gamma$, $\operatorname{counit} \epsilon: \Gamma \rightarrow A$, diagonal $\psi: \Gamma \rightarrow \Gamma \otimes_{A} \Gamma$ and conjugation $c: \Gamma \rightarrow \Gamma$ satisfying relations dual to the ones in the previous definition.
A Hopf algebroid is flat if either the left or the right unit is a flat morphism of rings.
Remark 1.24. If the left unit $\eta_{L}$ of some Hopf algebroid is flat, then so will be its right unit $\eta_{R}$ as the relation $\eta_{R}=c \circ \eta_{L}$ exhibits the right unit as composition of two flat maps ( $c$ is flat being an automorphism). Moreover, in this case, both units are automatically faithfully flat as they admit $\epsilon$ as a left inverse and hence $\operatorname{Spec}\left(\eta_{L}\right)$ respectively $\operatorname{Spec}\left(\eta_{R}\right)$ must be surjective.

To any Hopf algebroid corresponds the groupoid object in affine schemes $(\operatorname{Spec}(A), \operatorname{Spec}(\Gamma))$ and the global sections of a groupoid of affine schemes yield a Hopf algebroid. We will move around freely between these two dual notions, but it should be clear from the context which point of view is adopted. We will often write $\left(X_{0}, X_{1}\right)$ for the groupoid object in schemes interpretation and $(A, \Gamma)$ for the Hopf algebroid specified by rings. In this section, we will usually adopt the schematic perspective. When spectra come into play, we will often prefer the ring notation. One should be warned however that the equivalence between the two notions is contravariant, in particular it sends limits to colimits and vice-versa. It is important not to get confused about this. Already in the following definition we make the announced identification between these two categories.

Definition 1.25. The 2-category of Hopf algebroids has as objects groupoid objects in affine schemes $\left(X_{0}, X_{1}\right)$. A 1-morphism $\left(f_{0}, f_{1}\right):\left(X_{0}, X_{1}\right) \rightarrow\left(Y_{0}, Y_{1}\right)$ consists of a pair of morphisms of affine scheme $f_{i}: X_{i} \rightarrow Y_{i}$ for $i=0,1$ which commutes with all the structure maps. Given two 1-morphisms $\left(f_{0}, f_{1}\right),\left(g_{0}, g_{1}\right):\left(X_{0}, X_{1}\right) \rightarrow\left(Y_{0}, Y_{1}\right)$, we define a 2 -morphism $c:\left(f_{0}, f_{1}\right) \rightarrow\left(g_{0}, g_{1}\right)$ as a morphism of affine schemes $X_{0} \rightarrow Y_{1}$ which is $f_{0}$ when postcomposed with the source and $g_{0}$ when postcomposed with the target. Moreover, we require it to be compatible with multiplication by asking the following diagram to commute:

The identity 2-morphism for $\left(f_{0}, f_{1}\right)$ is defined as $f_{0} \circ e$. Composition of 1-morphisms is componentwise and composition of 2 -morphisms $\left(f_{0}, f_{1}\right) \xrightarrow{c}\left(g_{0}, g_{1}\right) \xrightarrow{c^{\prime}}\left(h_{0}, h_{1}\right)$ is given by $c^{\prime} \circ c: X_{1} \xrightarrow{\left(c^{\prime}, c\right)}$ $Y_{1} \times_{s, Y_{0}, t} Y_{1} \xrightarrow{m} Y_{1}$. One checks that this defines a 2-category, which will follow easily from the axioms defining the groupoids, functoriality and naturality.
The 2 -subcategory whose objects are given by flat Hopf algebroids will be denoted by $\mathcal{H}$.
As announced, there is a surprisingly deep relationship between stacks and Hopf algebroids which we will investigate now.

Lemma 1.26. For any affine morphism of stacks $f: \operatorname{Spec}(R) \rightarrow \mathcal{X}$, the pair $(\operatorname{Spec}(R), \operatorname{Spec}(R) \times_{\mathcal{X}}$ $\operatorname{Spec}(R))$ can be given the structure of a Hopf algebroid.
Proof. We will only give the necessary maps, checking that they satisfy the desired properties is left to the reader. First, recall that, as $f$ was assumed to be affine, the pullback $\operatorname{Spec}(R) \times_{\mathcal{X}} \operatorname{Spec}(R)$ is equivalent to some affine scheme denoted by $\operatorname{Spec}(S)$. The source and target maps are given by the two canonical projections. The unit is given by the diagonal and the inverse comes from the switch map. The composition is given by projection onto the first and third coordinate under the identification $\operatorname{Spec}(S) \times_{\operatorname{Spec}(R)} \operatorname{Spec}(S) \cong \operatorname{Spec}(R) \times_{\mathcal{X}} \operatorname{Spec}(R) \times_{\mathcal{X}} \operatorname{Spec}(R)$.
Definition 1.27. A Hopf algebroid arising from a morphism of stacks $f$ as in lemma 1.26 is called associated Hopf algebroid to $f$. Given a rigidified algebraic stack $(\mathcal{X}, P: \operatorname{Spec}(R) \rightarrow \mathcal{X})$, the associated Hopf algebroid to the presentation $P$ is also referred to as the associated Hopf algebroid to $\mathcal{X}$.
Conversely, one can associate a prestack to a Hopf algebroid via the following construction.
Construction 1.28. Let $(A, \Gamma)$ be a Hopf algebroid, which we identify with its associated groupoid in affine schemes denoted by $\left(X_{0}, X_{1}\right)$. We associate a pseudofunctor $\left[X_{\bullet}\right]^{\prime}:$ (Aff, $f p q c)^{o p} \rightarrow$ Groupoids to it as follows.
First, let us define this functor on objects. Given some affine scheme $U,\left[X_{\bullet}\right]^{\prime}(U)$ is the groupoid whose objects are morphisms of affine schemes $U \rightarrow X_{0}$ and whose morphisms are morphisms of affine schemes $U \rightarrow X_{1}$. The source, target and composition maps are induced by the structure maps $s, t$ and $m$ of $\left(X_{0}, X_{1}\right)$. More concisely, $O b\left(\left[X_{\bullet}\right]^{\prime}(U)\right)=X_{0}(U), \operatorname{Mor}\left(\left[X_{\bullet}\right]^{\prime}(U)\right)=X_{1}(U)$ where we identified the scheme $X_{i}$ with the sheaf it represents.
More precisely, a morphism $\alpha: U \rightarrow X_{1}$ is in $\operatorname{Hom}_{\left[X_{\bullet}\right]^{\prime}(U)}\left(U \xrightarrow{f} X_{0}, U \xrightarrow{g} X_{0}\right)$ if $s \circ \alpha=f$ and $t \circ \alpha=g$. Given $\beta \in \operatorname{Hom}_{\left[X_{\bullet}\right]^{\prime}(U)}\left(U \xrightarrow{g} X_{0}, U \xrightarrow{h} X_{0}\right)$, the composition $\beta \circ \alpha$ is defined as

$$
\beta \circ \alpha:=m \circ(\alpha, \beta): U \rightarrow X_{1} \times_{X_{0}} X_{1} \rightarrow X_{1}
$$

where $(\alpha, \beta)$ is given by the universal property of the pullback as in the following diagram:
![img-14.jpeg](img-14.jpeg)

Observe that by the first axiom of definition 1.21 and 2 -commutativity of the above diagram, it holds that $s \circ m \circ(\alpha, \beta) \cong s \circ p r_{2} \circ(\alpha, \beta)=s \circ \alpha=f$ and similarly $t \circ m \circ(\alpha, \beta) \cong h$. Hence the composition is well-defined. It is associative because $m$ is (axiom 2 of definition 1.21). Given an object $f: U \rightarrow X_{0}$, define its identity morphism to be $i d_{f}:=e \circ f: U \rightarrow X_{0} \rightarrow X_{1}$. Note that $s \circ e=t \circ e=i d_{X_{0}}$, so $i d_{f}$ has $f$ as source and target. Given another object $g: U \rightarrow X_{0}$ and a morphism $\alpha: f \rightarrow g$, we claim that $\alpha \circ i d_{f} \cong \alpha$, i.e. up to isomorphism $i d_{f}$ is indeed a left neutral element. The proof that it is a right neutral element is symmetric and will be omitted. Recall that $\alpha \circ i d_{f}=m \circ(\alpha, e \circ f)$. Now observe that $(\alpha, e \circ f) \cong\left(i d_{X_{1}}, e \circ s\right) \circ \alpha$. Indeed, noting that, by definition of $\alpha$, it holds that $s \circ \alpha=f$, we have the following 2-commutative diagram:
![img-15.jpeg](img-15.jpeg)

However, the outermost square is the square used to define $(\alpha, e \circ f)$, hence as the lower square is a pullback, $(\alpha, e \circ f)$ and $\left(i d_{X_{1}}, e \circ s\right) \circ \alpha$ are canonically isomorphic. By axiom 3 of definition 1.21, one knows that $m \circ\left(i d_{X_{1}}, e \circ s\right)=i d_{X_{1}}$, hence $m \circ(\alpha, e \circ f) \cong m \circ\left(i d_{X_{1}}, e \circ s\right) \circ \alpha=\alpha$ as claimed.

Finally, $\left[X_{\bullet}\right]^{\prime}(U)$ is really a groupoid (not just a category), as any morphism $\alpha$ admits an inverse given by $i \circ \alpha$ as can be easily checked from axiom 4 (the details are similar to the previous and therefore omitted). On morphisms, the functor $\left[X_{\bullet}\right]^{\prime}$ is induced by restriction, i.e. $\left[X_{\bullet}\right]^{\prime}(V \xrightarrow{t} U):\left[X_{\bullet}\right]^{\prime}(U) \rightarrow\left[X_{\bullet}\right]^{\prime}(V)$ sending $U \rightarrow X_{0}$ to $V \xrightarrow{t} U \rightarrow X_{0}$, similarly for $X_{1}$. This is clearly functorial.

Lemma 1.29. The pseudofunctor constructed in construction 1.28 is a prestack.
Proof. We claim that given any affine scheme $U$ and two objects $f, g \in\left[X_{\bullet}\right]^{\prime}(U)$ the presheaf $\underline{\operatorname{Isom}}(f, g)$ is a sheaf. Lazily, one could just argue that this is clear as all objects involved are morphisms between schemes and it is well-known that these have the desired sheafy properties. However, let us write out the details now so we can be lazy with good conscience later. We need to show that, given any fpqccover $\left\{U_{i}\right\}_{i}$ of $U$ and a collection $\left\{\varphi_{i}\right\}_{i}$ of elements in $\left.\operatorname{Isom}\left(f \mid v_{i}, g\right)_{U_{i}}\right)$, which are all compatible on the intersections, there exists a unique $\varphi \in \underline{\operatorname{Isom}}(f, g)(U)$ which restricts to $\varphi_{i}$ on each $U_{i}$. Recall that each $\varphi_{i}$ is some morphism of affine schemes $U_{i} \rightarrow X_{1}$. As they agree on the intersections, they glue uniquely to some morphism of schemes $\varphi: U \rightarrow X_{1}$. Let us verify that $\varphi \in \underline{\operatorname{Isom}}(f, g)(U)$ i.e. that $s \circ \varphi=f$ and $t \circ \varphi=g$ (we already know it is necessarily an isomorphism). Note that $\left\{s \circ \varphi_{i}\right\}_{i}$ forms a collection of compatible morphisms of schemes from $U_{i} \rightarrow X_{0}$. As before, they glue uniquely to some morphism $U \rightarrow X_{0}$. Since by construction $s \circ \varphi_{i}=f \mid v_{i}$, uniqueness implies that they must glue to $f$. Now observe that $\left.s \circ \varphi\right|_{U_{i}}=s \circ \varphi_{i}=f_{i}$ by construction, so using uniqueness again one concludes that $s \circ \varphi=f$ as wanted. The argument for $g$ is completely analogous.

Remark 1.30 ([13, (2.4.3)]). Identifying the scheme $X_{0}$ with the discrete prestack it represents, it makes sense to talk about morphisms $X_{0} \rightarrow\left[X_{\bullet}\right]^{\prime}$.
There is a canonical 1-morphism of prestacks can : $X_{0} \rightarrow\left[X_{\bullet}\right]^{\prime}$ given by $\operatorname{can}_{U}: X_{0}(U) \rightarrow\left[X_{\bullet}\right]^{\prime}(U)$ defined as the identity on objects and mapping $i d_{U \xrightarrow{t} X_{0}}$ to $i d_{f}$ as constructed in construction 1.28 .
Moreover, there is a canonical 2-isomorphism can $\circ s \xrightarrow{\phi}$ can $\circ t$, i.e. for each affine scheme $U$, there exists a natural transformation (that moreover varies naturally in the $U$ ) $\phi_{(U)}: \operatorname{can} \circ s(U) \rightarrow \operatorname{can} \circ t(U)$ where $\operatorname{can} \circ s(U)$ is the functor $X_{1}(U) \xrightarrow{s^{*}} X_{0}(U) \xrightarrow{\text { can }}\left[X_{\bullet}\right]^{\prime}(U)$. As the only morphisms in $X_{1}(U)$ are the identities, naturality will be straightforward. Given an object $f: U \rightarrow X_{1}$, we wish to define a morphism $\phi_{U, f}: \operatorname{can} \circ s(U)(f) \rightarrow \operatorname{can} \circ t(U)(f)$ in $\left[X_{\bullet}\right]^{\prime}(U)$, i.e. $\phi_{U, f}$ is some morphism $U \rightarrow X_{1}$ from $s \circ f$ to $t \circ f$. What better choice is there than $f$ itself? Hence, we set $\phi_{U, f}=f$ and this defines the desired 2 -morphism.
The main takeaway is that there always is a "canonically" 2-commutative diagram
![img-16.jpeg](img-16.jpeg)

This diagram is cartesian as the induced map $\psi$ in the following diagram is an isomorphism:
![img-17.jpeg](img-17.jpeg)

Explicitly, $\psi(U)\left(\alpha: U \rightarrow X_{1}\right)=(s \circ \alpha, t \circ \alpha, \alpha)$ and the inverse is given by mapping an element of the pullback $\left(f: U \rightarrow X_{0}, g: U \rightarrow X_{0}, \beta: U \rightarrow X_{1}\right)$ to $\beta$. These constructions are inverses as the isomorphism between the two objects we consider together with the structure maps already encodes all the information. Of course, one would need to extend this definition to turn the inverse into an actual functor of 2-categories. This is left to the reader.

Remark 1.31. In [13, (2.4.3)], the existence of can and $\phi$ is mentioned together with the fact that $X_{1}$ is the pullback. It is then stated that "these satisfy a universal property which we will avoid to write down". After further reading, one infers from the proofs that this universal property should say: given

any morphism of prestacks $P: X_{0} \rightarrow \mathcal{X}$ and a 2 -isomorphism $\alpha: P \circ s \cong P \circ t$, there exists a unique morphism $P^{\prime}:\left[X_{\bullet}\right]^{\prime} \rightarrow \mathcal{X}$ such that $P \cong P^{\prime} \circ$ can. In other words, for any diagram of the following form such that the solid squares are 2 -commutative, there exists a unique dashed arrow and unique 2 -morphisms filling the new squares such that everything is 2 -commutative:
![img-18.jpeg](img-18.jpeg)

On objects, $P^{\prime}$ is defined by sending $f: U \rightarrow X_{0} \in O b\left(\left[X_{\bullet}\right]^{\prime}\right)$ to $P(f)$. A morphism $A: U \rightarrow X_{1}$ between two objects $f$ and $g$ is sent to $\alpha_{A}$ where $\alpha_{A}$ denotes the isomorphism $P \circ s(A)=P(f) \rightarrow P \circ t(A)=P(g)$ induced by $\alpha$. One checks that this extends to a well defined morphism between these prestacks.

We have now constructed a prestack $\left[X_{\bullet}\right]^{\prime}$ from a given Hopf algebroid $\left(X_{0}, X_{1}\right)$. However, in general there is no reason that $\left[X_{\bullet}\right]^{\prime}$ should satisfy the second condition of definition 1.2 and be a stack. The problem is that the compatibilities are only defined up to compatible isomorphisms and not equality. The fact that $X_{0}$ is a sheaf is not strong enough to control this (similar to how vector bundles form a stack and not a sheaf). Luckily, there is a canonical way to turn a prestack into a stack: stackification. This is the 2 -categorical analog of sheafification.
The following construction is given in [13, Lem. 3.2], but there is no discussion whatsoever on why it has the desired properties. We have made it our duty to fill in at least some of the gaps. A similarly brief overview can be found at [22, Tag 02ZM].

Theorem 1.32. For any prestack $\mathcal{X}$, there exists a canonically associated stack $\tilde{\mathcal{X}}$ together with a fully faithful 1-morphism of prestacks $i: \mathcal{X} \rightarrow \tilde{\mathcal{X}}$. Moreover, given any stack $\mathcal{Y}$, precomposition with $i$ induces a bijection $\operatorname{Hom}_{\text {Stacks }}(\tilde{\mathcal{X}}, \mathcal{Y}) \xrightarrow{i^{\prime}} \operatorname{Hom}_{\text {Prestacks }}(\mathcal{X}, U(\mathcal{Y}))$ where $U:$ Stacks $\rightarrow$ Prestacks denotes the forgetful functor. In other words, any morphism from $\mathcal{X}$ to a stack $\mathcal{Y}$ factors uniquely through $\tilde{\mathcal{X}}$ in a 2-commutative way. The stack $\tilde{\mathcal{X}}$ is known as stackification of $\mathcal{X}$ and the bijection induced by $i$ exhibits its universal property.

Proof. The idea is to just add in all the data one needs to make effective descent possible and then verify that this will satisfy all the desired properties.
Given a prestack $\mathcal{X}$ and an affine scheme $U$, we define $\tilde{\mathcal{X}}(U)$ as the groupoid whose objects are triples

$$
\left(\left\{U_{i} \rightarrow U\right\}_{i},\left\{X_{i}\right\}_{i},\left\{\varphi_{i i^{\prime}}\right\}\right)
$$

where $\left\{U_{i} \rightarrow U\right\}_{i}$ is a finite fpqc-cover of $U$, and $\left(\left\{X_{i}\right\}_{i},\left\{\varphi_{i i^{\prime}}\right\}\right)$ is a descent datum relative to this cover. More precisely, each $X_{i}$ is an object in $\mathcal{X}\left(U_{i}\right)$ and the $\varphi_{i i^{\prime}} \in \operatorname{Mor}\left(\mathcal{X}\left(U_{i} \times_{U} U_{j}\right)\right)$ give isomorphisms $\varphi_{i i^{\prime}}: X_{i} \mid U_{i} \times_{U} U_{j} \rightarrow X_{j} \mid U_{i} \times_{U} U_{j}$ satisfying the usual cocycle conditions. The morphisms between two objects $\left(\left\{U_{i} \rightarrow U\right\}_{i},\left\{X_{i}\right\}_{i},\left\{\varphi_{i i^{\prime}}\right\}\right)$ and $\left(\left(\left\{V_{j} \rightarrow U\right\}_{j},\left\{Y_{j}\right\}_{j},\left\{\psi_{j j^{\prime}}\right\}\right)\right)$ of $\tilde{\mathcal{X}}(U)$ are collections $\left\{a_{i j}\right\}_{i, j}$ where each $a_{i j} \in \operatorname{Mor}_{\mathcal{X}}\left(X_{i} \mid U_{i} \times_{U} V_{j}, Y_{j} \mid U_{i} \times_{U} V_{j}\right)$ compatibly with the descent data. This means that for all $i, i^{\prime}, j, j^{\prime}$ the following square commutes:
![img-19.jpeg](img-19.jpeg)

To define composition, we need to remember what it means for $\mathcal{X}$ to be a prestack. Consider two morphisms

$$
\left\{a_{i j}\right\}_{i, j}:\left(\left\{U_{i} \rightarrow U\right\}_{i},\left\{X_{i}\right\}_{i},\left\{\varphi_{i i^{\prime}}\right\}\right) \rightarrow\left(\left\{V_{j} \rightarrow U\right\}_{j},\left\{Y_{j}\right\}_{j},\left\{\psi_{j j^{\prime}}\right\}\right)
$$

and

$$
\left\{b_{j k}\right\}_{j, k}:\left(\left\{V_{j} \rightarrow U\right\}_{j},\left\{Y_{j}\right\}_{j},\left\{\psi_{j j^{\prime}}\right\}\right) \rightarrow\left(\left\{W_{k} \rightarrow U\right\}_{k},\left\{Z_{k}\right\}_{k},\left\{\psi_{k k^{\prime}}\right\}\right)
$$

One can a priori only define the composition

$$
\left.b_{j k}\right|_{U_{i} \times_{U} V_{j} \times_{U} W_{k}} \circ a_{i j}\left.\right|_{U_{i} \times_{U} V_{j} \times_{U} W_{k}}: X_{i} \right|_{U_{i} \times_{U} V_{j} \times_{U} W_{k}} \rightarrow Z_{k} \mid U_{i} \times_{U} V_{j} \times_{U} W_{k}
$$

Observe that $\left\{U_{i} \times_{U} V_{j} \times_{U} W_{k}\right\}_{j}$ is an fpqc-cover of $U_{i} \times_{U} W_{k}$. Moreover, the fact that the $a_{i j}$ and $b_{j k}$ were assumed to be compatible with the descent datum ensures that the $b_{j k} \mid U_{i} \times_{U} V_{j} \times_{U} W_{k} \circ a_{i j} \mid U_{i} \times_{U} V_{j} \times_{U} W_{k}$ agree on the intersections of the various $V_{j}$. As $\underline{\text { Isom }}_{\mathcal{X}}\left(X_{i} \mid U_{i} \times_{U} V_{j} \times_{U} W_{k}, Z_{k} \mid U_{i} \times_{U} V_{j} \times_{U} W_{k}\right)$ is a sheaf, the morphisms $\left\{b_{j k} \mid U_{i} \times_{U} V_{j} \times_{U} W_{k} \circ a_{i j} \mid U_{i} \times_{U} V_{j} \times_{U} W_{k}\right\}_{j}$ glue to the morphism which we define to be the composition $b_{j k} \circ a_{i j}: X_{i} \mid U_{i} \times_{U} V_{j} \rightarrow Z_{k} \mid U_{i} \times_{U} V_{j}$. It is left to the reader to verify that this is compatible with the descent data (which is essentially because it was glued from compatible morphisms) and that this makes $\tilde{\mathcal{X}}(U)$ into a groupoid.
On morphisms, $\tilde{\mathcal{X}}$ is defined in the obvious way. Given a morphism of affine schemes $f: V \rightarrow U$, we define $\tilde{\mathcal{X}}(f): \tilde{\mathcal{X}}(U) \rightarrow \tilde{\mathcal{X}}(V)$ on objects by

$$
\left(\left\{U_{i} \rightarrow U\right\}_{i},\left\{X_{i}\right\}_{i},\left\{\varphi_{i i^{\prime}}\right\}\right) \mapsto\left(\left\{U_{i} \times_{U} V \rightarrow V\right\}_{i},\left\{X_{i} \mid U_{i} \times_{U} V\right\}_{i},\left\{\varphi_{i i^{\prime}} \mid U_{i} \times_{U} V\right\}\right)
$$

As flat, quasicompact and surjective are all properties that satisfy base change, $\left\{U_{i} \times_{U} V \rightarrow V\right\}_{i}$ is a cover. The definition of $\tilde{\mathcal{X}}(f)$ on morphisms and the verification of functoriality are left to the reader.

The fact that $\tilde{\mathcal{X}}$ defines a prestack, i.e. that morphisms form a sheaf, carries over from the fact that $\mathcal{X}$ is a prestack. The argument is the same as the glueing argument done to define composition.
The second condition for $\tilde{\mathcal{X}}$ to form a stack, namely effective descent, is now almost trivially satisfied by construction. Indeed, we must show that given an fpqc-cover $\left\{W_{k} \rightarrow U\right\}_{k}$ and objects $E_{k}=\left(\left\{U_{i_{k}}^{k} \rightarrow W_{k}\right\}_{i},\left\{X_{i_{k}}^{k}\right\}_{i},\left\{\varphi_{\left[i_{k}\right)\left(i_{k}^{\prime}\right)}^{k}\right\}_{i}\right) \in \tilde{\mathcal{X}}\left(W_{k}\right)$ with a descent datum $\left\{\psi_{k k^{\prime}}\right\}_{k}$, there exists some object $E \in \tilde{\mathcal{X}}(U)$ whose restriction to each $W_{k}$ is isomorphic to $E_{k}$. The easiest idea, to just assemble all data into one, works. One sets $E=\left(\left\{W_{i k} \rightarrow W_{k} \rightarrow U\right\}_{i, k},\left\{X_{i_{k}}^{k}\right\}_{i, k},\{$ all descent data $\}\right)$ where by "all descent data" we mean all the $\left\{\varphi_{\left[i_{k}\right)\left(i_{k}^{\prime}\right)}^{k}\right\}_{i, k}$ to give the descent datum between elements coming from the same cover (like $X_{i}^{k}$ and $X_{i}^{k}$ ), but also the morphisms encoded in $\left\{\psi_{k k^{\prime}}\right\}_{k}$ to relate elements from different covers. More precisely, $\psi_{k k^{\prime}}$ is a morphism in $\tilde{\mathcal{X}}\left(W_{k} \times_{U} W_{k^{\prime}}\right)$ and hence consists of compatible morphisms $\left\{a_{i_{k}, j_{k^{\prime}}}: X_{i}^{k} \mid W_{k i} \times_{U} W_{k^{\prime} j} \rightarrow X_{j}^{k^{\prime}} \mid W_{k i} \times_{U} W_{k^{\prime} j}\right\}$. Each $a_{i_{k}, j_{k^{\prime}}}$ then gives the required descent datum from $\left.X_{i}^{k} \right|_{W_{k i} \times_{U} W_{k^{\prime} j}}$ to $\left.X_{j}^{k^{\prime}}\right|_{W_{k i} \times_{U} W_{k^{\prime} j}}$ (where we used pullback pasting).

The morphism $i: \mathcal{X} \rightarrow \tilde{\mathcal{X}}$ sends an object $x \in \mathcal{X}(U)$ to $\left(\left\{U \xrightarrow{i d_{U}} U\right\}, x, i d_{U}\right)$. A morphism $f: x \rightarrow y \in \mathcal{X}$ is sent to itself but now seen as $\left(\left\{U \xrightarrow{i d_{U}} U\right\}, x, i d_{U}\right) \xrightarrow{f}\left(\left\{U \xrightarrow{i d_{U}} U\right\}, y, i d_{U}\right) \in \tilde{\mathcal{X}}$ i.e. seen as morphism $\left.x\right|_{U \times_{U} U} \rightarrow y \mid_{U \times_{U} U}$ compatible with the descent data given by the identity. From this, it is clear that $i$ is fully faithful.

We will only outline why precomposition with $i$ induces the claimed bijection. The key observation is that for any object $\left(\left\{U_{i} \rightarrow U\right\}_{i},\left\{X_{i}\right\}_{i},\left\{\varphi_{i i^{\prime}}\right\}\right) \in \tilde{\mathcal{X}}(U)$, there exists a cover $\left\{V_{j} \rightarrow U\right\}$ and some $Y_{j} \in \mathcal{X}\left(V_{j}\right)$ such that $\left(\left\{U_{i} \rightarrow U\right\}_{i},\left\{X_{i}\right\}_{i},\left\{\varphi_{i i^{\prime}}\right\}\right) \mid V_{j} \cong i\left(Y_{j}\right)$. Indeed, the cover $\left\{U_{i} \rightarrow U\right\}_{i}$ itself can be chosen as the desired cover and the $X_{i}$ can be chosen for the $Y_{j}$. The descent datum itself then gives the desired isomorphisms:

$$
\begin{aligned}
\left(\left\{U_{i} \rightarrow U\right\}_{i},\left\{X_{i}\right\}_{i},\left\{\varphi_{i i^{\prime}}\right\}\right) \mid U_{j}:= & \\
& \left(\left\{U_{j} \times_{U} U_{i} \rightarrow U_{j}\right\}_{i},\left\{X_{i} \mid U_{j} \times_{U} U_{i}\right\}_{i},\left\{\varphi_{i i^{\prime}} \mid U_{j} \times_{U} U_{i}\right\}\right) \xrightarrow{\left\{\varphi_{i j}\right\}_{i}} i\left(X_{j}\right) \\
& :=\left(U_{j} \xrightarrow{i d_{U_{j}}} U_{j}, X_{j}, i d_{U_{j}}\right)
\end{aligned}
$$

Using this, one defines an inverse $\operatorname{Hom}_{\text {Stacks }}(\tilde{\mathcal{X}}, \mathcal{Y}) \stackrel{\psi}{\leftarrow} \operatorname{Hom}_{\text {Prestacks }}(\mathcal{X}, U(\mathcal{Y}))$ as follows. Given a morphism of prestacks $F: \mathcal{X} \rightarrow U(\mathcal{Y})$, we know how to define $\psi(F)$ on elements in the image of $i$, namely $\psi(F)(i(x)):=F(x)$. Then, we use the previous point to extend this definition to any object of $y \in \tilde{\mathcal{X}}(U)$ by finding a cover $\left\{U_{i} \rightarrow U\right\}_{i}$ such that $y \mid U_{i}$ is isomorphic to $i\left(x_{i}\right)$ for some $x_{i} \in \mathcal{X}\left(U_{i}\right)$. We define $\psi(F)\left(y \mid U_{i}\right):=F\left(i\left(x_{i}\right)\right)$. One then checks that these satisfy the effective descent condition and, as $\mathcal{Y}$ is a stack, glue to some object which we define to be $\psi(F)(y)$. The details that this definition makes $\psi(F)$ into a well-defined morphism of stacks are left to the reader.

Remark 1.33. Recall that a finite disjoint union of affine schemes is again affine. In particular, any finite fpqc-covering $\left\{U_{i} \xrightarrow{\varphi_{1}} U\right\}_{i}$ in the category of affine schemes is equivalent to the cover $\left\{\sqcup_{i} U_{i} \xrightarrow{\sqcup_{i} \varphi_{1}} U\right\}$ consisting of a single morphism. As the coverings $\left\{U_{i} \rightarrow U\right\}_{i}$ that appeared in the definition of objects of the stackification were required to be finite, we could also have described an object $x \in \mathcal{X}(U)$ as a triple $\left(\left\{U^{\prime} \rightarrow U\right\}, x^{\prime},\left\{\varphi_{12}\right\}\right)$ where $U^{\prime}$ is an fpqc-cover of $U, x^{\prime}$ is an object of $\mathcal{X}\left(U^{\prime}\right)$ and, denoting the two projections $U^{\prime} \times_{U} U^{\prime} \rightarrow U$ by $p_{1}$ and $p_{2}, \varphi_{12}$ gives an isomorphism $\varphi_{12}: p_{1}^{*}\left(x^{\prime}\right) \rightarrow p_{2}^{*}(x)$. We allowed finite covers in the previous proof because it clarified certain ideas like showing the effective descent property. However, in the following, we will often use the convention given in this remark as it is easier to deal with.

In view of this theorem, one can associate a stack $\left[X_{\bullet}\right]$ to any prestack $\left[X_{\bullet}\right]^{\prime}$ obtained from a Hopf algebroid. This stack has analogous properties to those of the prestack discussed in remarks 1.30 and 1.31, namely:

Remark 1.34. There is a canonical morphism $c:=i \circ$ can $: X_{0} \rightarrow\left[X_{\bullet}\right]$ and a canonical 2-morphism $c \circ s \xrightarrow{\varphi} c \circ t$. Moreover, fully faithfulness of $i$ implies that $X_{1}$ is also the pullback for $X_{0} \stackrel{c}{\rightarrow}\left[X_{\bullet}\right] \stackrel{c}{\leftarrow} X_{0}$. The stack $\left[X_{\bullet}\right]$ has the following universal property: given any morphism of stacks $P: X_{0} \rightarrow \mathcal{X}$ and a 2 -isomorphism $P \circ s \xrightarrow{\alpha} P \circ t$, there exists a unique morphism $\bar{P}:\left[X_{\bullet}\right] \rightarrow \mathcal{X}$ such that $\bar{P} \cong P \circ c$. Indeed, $\bar{P}$ is obtained from the universal property of stackification and the map $P^{\prime}$ constructed in remark 1.31.

Remark 1.35. If $\mathcal{X}$ is already a stack, then $i: \mathcal{X} \rightarrow \widetilde{\mathcal{X}}$ is an isomorphism of stacks as can be seen from the universal property of stackification applied both to $\mathcal{Y}=\mathcal{X}$ and $\mathcal{Y}=\widetilde{\mathcal{X}}$.
In particular, recall that we have seen in example 1.22 that for any affine scheme $X$, the pair $(X, X)$ defines a trivial Hopf algebroid. Unravelling the construction of $[(X, X)]^{\prime}$ one sees that this prestack is equivalent to the scheme $X$ seen as a prestack. As $X$ is already a stack, we conclude that $[(X, X)] \cong X$.

The proof of theorem 1.32 may have been long and technical, but in the end it was just verifying that adding all the effective descent data did what we wanted. For many applications, one gets away with just knowing the universal property and not having to look at the explicit construction. However, the following few propositions and corollaries exploit the specific construction of the associated stack functor and will prove to be very useful. This is one reason why the explicit construction was outlined here. The other reason was to notice how little geometric input this construction gives us. We only know that, up to a faithfully flat cover, the objects are those that $X_{0}$ represents. It is generally very difficult to understand the geometric meaning of the objects that do not lie in the image of $i$. Therefore, it will be nice to have the equivalence of categories of theorem 1.40 as it will give a translation between the algebraic and geometric worlds. We will see a concrete example of this in proposition 1.68. But first let us focus on the following important propositions.

Proposition 1.36. Up to a cover, any morphism of stacks $f: \operatorname{Spec}(R) \rightarrow\left[X_{\bullet}\right]$ factors through $X_{0}$. More precisely, there exists a faithfully flat morphism of schemes $\varphi: \operatorname{Spec}(S) \rightarrow \operatorname{Spec}(R)$, a morphism of schemes $a: \operatorname{Spec}(S) \rightarrow X_{0}$ and a 2-isomorphism witnessing the commutativity of the following diagram:
![img-20.jpeg](img-20.jpeg)

Proof. To begin with, recall from remark 1.6 that $f$ is entirely characterised by where it sends the identity of $\operatorname{Spec}(R)$. From remark 1.33, we know that $f\left(i d_{R}\right)$ is some triple

$$
\left(\operatorname{Spec}(S) \stackrel{\varphi}{\rightarrow} \operatorname{Spec}(R), \operatorname{Spec}(S) \xrightarrow{a} X_{0}, \xi_{12}\right)
$$

where $\varphi$ is an fpqc-covering and $\xi_{12}: p_{1}^{*}(a) \rightarrow p_{2}^{*}(a)$ the required descent datum.
We claim that the diagram
![img-21.jpeg](img-21.jpeg)

is 2 -commutative. By the above observation, it suffices to check that the two compositions are isomorphic on $i d_{S}$. We calculate

$$
f \circ \varphi\left(i d_{S}\right)=f(\varphi)=\varphi^{*}\left(f\left(i d_{R}\right)\right)=\left(\bar{\varphi}: \operatorname{Spec}\left(S \otimes_{R} S\right) \rightarrow \operatorname{Spec}(S), a \circ \bar{\varphi}, \varphi^{*}\left(\xi_{12}\right)\right)
$$

where $\bar{\varphi}$ denotes the base change of $\varphi$ along itself. On the other hand,

$$
c \circ a\left(i d_{S}\right)=c(a)=\left(i d_{\operatorname{Spec}(S)}, a, i d_{\operatorname{Spec}(S)}\right)
$$

We claim that $\left(\bar{\varphi}: \operatorname{Spec}\left(S \otimes_{R} S\right) \rightarrow \operatorname{Spec}(S), a \circ \bar{\varphi}, \varphi^{*}\left(\xi_{12}\right)\right)$ and $\left(i d_{\operatorname{Spec}(S)}, a, i d_{\operatorname{Spec}(S)}\right)$ are isomorphic in $\left[X_{\bullet} \mid(\operatorname{Spec}(S))\right.$. Recall from the associated stack construction that an isomorphism between these two objects consists of a morphism

$$
\left.\psi: a \circ \bar{\varphi}\right|_{\operatorname{Spec}(S) \times_{\operatorname{Spec}(S)} \operatorname{Spec}\left(S \otimes_{R} S\right)}=a \circ \bar{\varphi} \rightarrow\left.a\right|_{\operatorname{Spec}(S) \times_{\operatorname{Spec}(S)} \operatorname{Spec}\left(S \otimes_{R} S\right)}
$$

compatible with the descent data. Since by definition and construction it holds that

$$
\left.a\right|_{\operatorname{Spec}(S) \times_{\operatorname{Spec}(S)} \operatorname{Spec}\left(S \otimes_{R} S\right) \cong \operatorname{Spec}\left(S \otimes_{R} S\right)}=\bar{\varphi}^{*}(a)=a \circ \bar{\varphi}
$$

one can choose $\psi=i d_{a \circ \bar{\varphi}}$, which, by the proof of lemma 1.29 , was defined as $e \circ a \circ \bar{\varphi}$ where $e$ is the unit of $\left(X_{0}, X_{1}\right)$. This is clearly compatible with the descent datum, which concludes the proof.

Remark 1.37. This proposition makes it very easy to compute pullbacks of morphisms $\operatorname{Spec}(R) \rightarrow\left[X_{\bullet}\right]$ up to an fpqc cover. Suppose we wanted to calculate the pullback of the span $\operatorname{Spec}(R) \rightarrow\left[X_{\bullet}\right] \leftarrow \operatorname{Spec}\left(R^{\prime}\right)$ up to an fpqc cover. Then by proposition 1.36 , there exist faithfully flat morphisms $\varphi$ and $\varphi^{\prime}$ which factor as drawn below. Calculating the pullback of the span

$$
\operatorname{Spec}(S) \xrightarrow{\varphi} \operatorname{Spec}(R) \rightarrow\left[X_{\bullet}\right] \leftarrow \operatorname{Spec}\left(R^{\prime}\right) \stackrel{\varphi^{\prime}}{\leftarrow} \operatorname{Spec}\left(S^{\prime}\right)
$$

now comes down to pasting several pullbacks of affine schemes together as depicted in the diagram. Luckily, we know how to do this:
![img-22.jpeg](img-22.jpeg)

Here $\operatorname{Spec}\left(A_{i}\right)=X_{i}$.
Let us explore two very useful consequences of the previous proposition.
Corollary 1.38. A morphism $f: \operatorname{Spec}(R) \rightarrow\left[X_{\bullet}\right]$ is representable if and only if the fiber product $\operatorname{Spec}(R) \times_{f,\left[X_{\bullet}\right], c} X_{0}$ is equivalent to a scheme.
Moreover, if $f$ is representable, it satisfies $\mathcal{P}$ if and only if the base change of $f$ against $c$ satisfies $\mathcal{P}$. Here $\mathcal{P}$ denotes a property of morphisms of schemes that satisfies base change and is fpqc-local on the target.
Proof. Suppose that the fiber product $\operatorname{Spec}(R) \times_{f,\left[X_{\bullet}\right], c} X_{0}$ is equivalent to a scheme $Y$. We need to show that given any morphism $g: \operatorname{Spec}\left(R^{\prime}\right) \rightarrow\left[X_{\bullet}\right]$ the fiber product $\operatorname{Spec}(R) \times_{f,\left[X_{\bullet}\right], g} \operatorname{Spec}\left(R^{\prime}\right)$ is also equivalent to a scheme. By proposition 1.36 , we find an fpqc-cover $\varphi^{\prime}: \operatorname{Spec}\left(S^{\prime}\right) \rightarrow \operatorname{Spec}\left(R^{\prime}\right)$ such that $g \circ \varphi^{\prime}$ factors through $X_{0}$ as in the following diagram
![img-23.jpeg](img-23.jpeg)

From the previous diagram, we get that the outside square in the following diagram is a pullback. Hence, by pullback pasting, all squares are pullbacks
![img-24.jpeg](img-24.jpeg)

By construction, $\varphi^{\prime}$ is faithfully flat and affine, by base change so is $\varphi^{\prime \prime}$. In particular, by proposition 1.14 , both are epimorphisms. As $f^{\prime \prime}$ is a morphism between schemes it is tautologically representable. By the second part of lemma $1.12, f_{g}$ is also representable. This implies that $\operatorname{Spec}(R) \times_{\left[X_{\bullet}\right]} \operatorname{Spec}\left(R^{\prime}\right)$ must be equivalent to a scheme as it is equal to the fiber product $\operatorname{Spec}(R) \times_{\left[X_{\bullet}\right]} \operatorname{Spec}\left(R^{\prime}\right) \times_{f_{g}, \operatorname{Spec}\left(R^{\prime}\right), i d} \operatorname{Spec}\left(R^{\prime}\right)$ which is equivalent to a scheme by representability.
The second part follows by similar reasoning. Now we need to show that $f_{g}$ satisfies $\mathcal{P}$ assuming that $f^{\prime}$ does. By base change, so does $f^{\prime \prime}$ and as $\mathcal{P}$ was fpqc-local on the target, i.e. satisfies faithfully flat descent, it follows that $f_{g}$ satisfies $\mathcal{P}$ as claimed.

We will mainly apply this corollary when $\mathcal{P}$ is (faithfully) flat or affine. The stack associated to a flat Hopf algebroid is even nicer:

Corollary 1.39. The stack $\left[X_{\bullet}\right]$ associated to a flat Hopf algebroid $\left(X_{0}, X_{1}\right)$ is algebraic. In particular, in view of remark 1.18, any morphism $f: \operatorname{Spec}(R) \rightarrow\left[X_{\bullet}\right]$ is affine.

Proof. We claim that the canonical morphism $c$ constructed in remark 1.34 is representable, faithfully flat and affine. Hence, it can be chosen as a presentation for $\left[X_{\bullet}\right]$. Indeed, representabiltiy follows from corollary 1.38 and the fact that by construction the fiber product $X_{0} \times_{\left[X_{\bullet}\right]} X_{0}$ is equivalent to the affine scheme $X_{1}$ (see remark 1.34). To get that $c$ is faithfully flat and affine, by that same corollary, it suffices to check that the base change of $c$ against itself is faithfully flat and affine. By remark 1.34, this base change is either the source or the target map. It is affine as a morphism between affine schemes and flat by the definition of flat Hopf algebroids. It is faithfully flat by remark 1.24 .

We have now assembled all the tools to prove the highlight of this section:
Theorem 1.40 ([18, Thm. 8]). There is an equivalence of 2-categories between the 2-category $\mathcal{H}$ of flat Hopf algebroids as defined in definition 1.25 and the 2-category $\mathcal{S}$ of rigidified algebraic stacks constructed in definition 1.17 .

Proof. We will only give the definitions of the needed functors on the objects as the extension of this construction to 1- and 2-morphisms is technical. Moreover, unlike some details in previous arguments which do not seem to be given in the literature, this extension is done in [18, section 3.3] with great care. We define a functor $G: \mathcal{H} \rightarrow \mathcal{S}$ given on objects by $G\left(\left(X_{0}, X_{1}\right)\right)=\left(\left[X_{\bullet}\right], X_{0} \xrightarrow{c}\left[X_{\bullet}\right]\right)$. We have seen in corollary 1.39 that $\left[X_{\bullet}\right]$ is an algebraic stack and in remark 1.39 that the canonical presentation $c$ is affine and faithfully flat if $\left(X_{0}, X_{1}\right)$ is flat.
The inverse is given by the functor $K: \mathcal{S} \rightarrow \mathcal{H}$ which sends a rigidified algebraic stack $(\mathcal{X}, P: \operatorname{Spec}(R) \rightarrow$ $\mathcal{X})$ to its associated Hopf algebroid constructed in lemma 1.26. This Hopf algebroid is flat because the presentation is flat and, as the left and right unit are obtained as its base change, they are flat as well.

Let us check that (at least on the objects) these two functors are inverse equivalences. Observe that

$$
K \circ G\left(\left(X_{0}, X_{1}\right)\right)=\left(X_{0}, X_{0} \times_{\left[X_{\bullet}\right]} X_{0}\right) \cong\left(X_{0}, X_{1}\right)
$$

where the last isomorphism comes from remark 1.34. On the other hand,

$$
G \circ K((\mathcal{X}, P: \operatorname{Spec}(R) \rightarrow \mathcal{X}))=[(\operatorname{Spec}(R), \operatorname{Spec}(R) \times_{\mathcal{X}} \operatorname{Spec}(R))]
$$

For simplicity of notation, let us write

$$
X_{0}:=\operatorname{Spec}(R), X_{1}:=\operatorname{Spec}(R) \times_{\mathcal{X}} \operatorname{Spec}(R)) \text { and }\left[X_{\bullet}\right]:=[(\operatorname{Spec}(R), \operatorname{Spec}(R) \times_{\mathcal{X}} \operatorname{Spec}(R))]
$$

Recall from remark 1.34 that $P$ induces a morphism $\bar{P}:\left[X_{\bullet}\right] \rightarrow \mathcal{X}$ such that $P \cong \bar{P} \circ c$. We wish to argue that $\bar{P}$ is an isomorphism. For this, we will use that a 1-morphism of stacks is an isomorphism if and only if it is an epimorphism and a monomorphism as stated in remark 1.8. As $P$ was assumed to be faithfully flat, proposition 1.14 and remark 1.8 give that $P$ is an epimorphism. As $P \cong \bar{P} \circ c, \bar{P}$ must be an epimorphism as well.
It remains to see that $\bar{P}$ is a monomorphism. Recall that this means that for every affine scheme $U$ and for all $x_{1}, x_{2} \in O b\left(\left[X_{\bullet}\right](U)\right)$, the functor $\bar{P}(U)$ induces a bijection $\underline{\operatorname{Isom}}\left[X_{\bullet}\right]\left(x_{1}, x_{2}\right) \cong \underline{\operatorname{Isom}} \mathcal{X}\left(\bar{P}\left(x_{1}\right), \bar{P}\left(x_{2}\right)\right)$. This will follow from the observation that $\operatorname{Spec}(R) \times_{\mathcal{X}} \operatorname{Spec}(R)$ is a pullback both for

$$
\operatorname{Spec}(R) \xrightarrow{P} \mathcal{X} \stackrel{P}{\leftarrow} \operatorname{Spec}(R)
$$

(by definition) and for

$$
\operatorname{Spec}(R) \xrightarrow{c}[(\operatorname{Spec}(R), \operatorname{Spec}(R) \times_{\mathcal{X}} \operatorname{Spec}(R))]] \stackrel{c}{\leftarrow} \operatorname{Spec}(R)
$$

(by remark 1.30). Seeing it as a pullback along $P$, one sees that the elements of $\operatorname{Spec}(R) \times_{\mathcal{X}} \operatorname{Spec}(R)$ are of the form $\left(x, x^{\prime}, \psi: P(x) \cong P\left(x^{\prime}\right)\right)$ with $x, x^{\prime} \in O b(\operatorname{Spec}(R)(U))$ for some affine scheme $U$, but from the second perspective they are of the form $\left(x, x^{\prime}, \varphi: c(x) \cong c\left(x^{\prime}\right)\right)$. As $i:\left[X_{\bullet}\right]^{\prime} \rightarrow\left[X_{\bullet}\right]$ is fully faithful, any object of $\left[X_{\bullet}\right]^{\prime}$ is in the image of can, $c=i \circ$ can and $P \cong \bar{P} \circ c$, there must be the desired bijection. More formally, by the universal property of stackification, it suffices to check that $P^{\prime}$ is a monomorphism. Abusing notation and writing $x, x^{\prime}$ for both $x, x^{\prime} \in \operatorname{Spec}(R)(U)$ and $\operatorname{can}(x), \operatorname{can}\left(x^{\prime}\right) \in\left[X_{\bullet}\right]^{\prime}(U)$, recall from remark 1.10 that $\underline{\operatorname{Isom}}\left[X_{\bullet}\right]^{\prime}\left(x, x^{\prime}\right)$ is the pullback in
![img-25.jpeg](img-25.jpeg)
where $P$ is obtained by pasting pullbacks as in the following diagram
![img-26.jpeg](img-26.jpeg)

On the other hand, $\underline{\operatorname{Isom}} \mathcal{X}\left(P^{\prime}(x), P^{\prime}\left(x^{\prime}\right)\right)$ fits in the following pullback diagram
![img-27.jpeg](img-27.jpeg)
where $\bar{P}$ is obtained by pasting pullbacks
![img-28.jpeg](img-28.jpeg)
where all but the lower right squares are the same as in the diagram above. In particular, both $P$ and $\bar{P}$ are pullbacks of $A \rightarrow X_{1} \leftarrow B$, hence they must be isomorphic. Then, $\underline{\operatorname{Isom}} \mathcal{X}\left(P^{\prime}(x), P^{\prime}\left(x^{\prime}\right)\right)$ and $\underline{\operatorname{Isom}}\left[X_{\bullet}\right]\left(x, x^{\prime}\right)$ are also both pullbacks of the same diagram and isomorphic as needed to be shown.

Let us make the following warning.
Remark 1.41. The forgetful functor $\mathcal{U}: \mathcal{S} \rightarrow$ Stacks is not conservative. For example, it can happen that for a flat Hopf algebroid $\left(X_{0}, X_{1}\right)$ the stack $\mathcal{U}\left(\left[\left(X_{0}, X_{1}\right)\right]\right)$ is equivalent to some scheme $Y=\mathcal{U}([(Y, Y)])$ without $X_{0}$ nor $X_{1}$ being isomorphic to $Y$. An example of this phenomenon will be given in theorem 3.43. Another example of two nonisomorphic flat Hopf algebroids with the same underlying stack is explained in remark 2.32 .
It is true, however, that if the stacks $\mathcal{U}\left(\left[\left(X_{0}, X_{1}\right)\right]\right)$ and $\mathcal{U}\left(\left[\left(Y_{0}, Y_{1}\right)\right]\right)$ associated to the flat Hopf algebroids $\left(X_{0}, X_{1}\right)$ and $\left(Y_{0}, Y_{1}\right)$ are isomorphic, then these Hopf algebroids are weakly equivalent. This means that there is a chain of 1-morphisms of flat Hopf algebroids from $\left(X_{0}, X_{1}\right)$ to $\left(Y_{0}, Y_{1}\right)$ such that every one of these morphisms induces an isomorphism on the associated (nonrigidified) algebraic stacks. This is [18, Prop. 9].

Despite this warning, in the sequel we will often write $\left[\left(X_{0}, X_{1}\right)\right]$ for the stack (and not the rigidified algebraic stack) $\mathcal{U}\left(\left[\left(X_{0}, X_{1}\right)\right]\right)$ associated to the Hopf algebroid $\left(X_{0}, X_{1}\right)$. We trust that the reader can deduce which one is meant from the context.
One consequence of this equivalence of categories is that it is easy to calculate the pullbacks of rigidified algebraic stacks as we can calculate pullbacks of Hopf algebroids.

Remark 1.42 ([5, Ch. 4, Ex. 3.2]). One can show that in the category of flat Hopf algebroids, the pullback of

$$
\left(X_{0}, X_{1}\right) \xrightarrow{\left(f_{0}, f_{1}\right)}\left(Z_{0}, Z_{1}\right) \stackrel{\left(g_{0}, g_{1}\right)}{\longleftrightarrow}\left(Y_{0}, Y_{1}\right)
$$

is given by the Hopf algebroid $\left(X_{0} \times_{Y_{0}} Y_{1} \times_{Y_{0}} Z_{0}, X_{1} \times_{Y_{0}} Y_{1} \times_{Y_{0}} Z_{1}\right)$. By theorem 1.40 and as equivalences of categories preserve limits, this gives an easy way to compute the pullback of rigidified algebraic stacks; namely compute the associated Hopf algebroid and the pullback will be the associated stack to the pullback of Hopf algebroids.
But even more is true: we will show in remark 1.43 that the forgetful functor introduced in remark 1.41 commutes with fiber products, so

$$
\mathcal{U}\left(\left[\left(X_{0} \times_{Y_{0}} Y_{1} \times_{Y_{0}} Z_{0}, X_{1} \times_{Y_{0}} Y_{1} \times_{Y_{0}} Z_{1}\right)\right]\right) \cong \mathcal{U}\left(\left[\left(X_{0}, X_{1}\right)\right]\right) \times_{\mathcal{U}\left(\left[\left(Z_{0}, Z_{1}\right)\right]\right)} \mathcal{U}\left(\left(\left[Y_{0}, Y_{1}\right)\right]\right)
$$

As by corollary 1.38, it often suffices to analyse a particular pullback to understand certain properties of morphisms this observation will often prove useful. For example, $f: \mathcal{U}\left(\left[\left(X_{0}, X_{1}\right)\right]\right) \rightarrow \mathcal{U}\left(\left[\left(Y_{0}, Y_{1}\right)\right]\right)$ is representable if and only if the pullback of $f$ against the presentation $c:\left[\left(Y_{0}, Y_{0}\right)\right] \rightarrow\left[\left(Y_{0}, Y_{1}\right)\right]$ is equivalent to an affine scheme. By the previous observation, this pullback is given by the stack $\mathcal{U}\left(\left[\left(X_{0} \times_{Y_{0}} Y_{1} \times_{Y_{0}} Y_{0}, X_{1} \times_{Y_{0}} Y_{1} \times_{Y_{0}} Y_{0}\right]\right)$. In general however, it can be tricky to understand this associated stack. In lemma 3.43, we will encounter an explicit example of a nontrivial Hopf algebroid whose associated stack is equivalent to a scheme.

Remark 1.43. Consider three presentations (i.e. objects in $\mathcal{S}$ ), $F: \operatorname{Spec}(A) \rightarrow \mathcal{X}, G: \operatorname{Spec}(B) \rightarrow \mathcal{Y}$ and $F^{\prime}: \operatorname{Spec}\left(A^{\prime}\right) \rightarrow \mathcal{X}^{\prime}$ and suppose there are morphisms $\left(\alpha, \alpha_{0}\right): F \rightarrow G$ and $\left(\alpha^{\prime}, \alpha_{0}^{\prime}\right): F^{\prime} \rightarrow G$. Can we find a description for the fiber product $F \times_{G} F^{\prime}$ ? Form the following diagram of cartesian squares
![img-29.jpeg](img-29.jpeg)

We claim that $H: R \xrightarrow{h} P \xrightarrow{f} \mathcal{X} \times_{\mathcal{Y}} \mathcal{X}^{\prime}$ is the fiber product $F \times_{G} F^{\prime}$. By pullback pasting and remark 1.42, $R$ is equivalent to the affine scheme $\operatorname{Spec}\left(A \otimes_{B} \bar{B} \otimes_{B} A^{\prime}\right)$ where $\bar{B}$ is the ring such that $\operatorname{Spec}(\bar{B})=$ $\operatorname{Spec}(B) \times_{\mathcal{Y}} \operatorname{Spec}(B)$ which is an affine scheme by assumption. As $F$ and $F^{\prime}$ are presentations, by base change also $f, f^{\prime}$ and thus $h$ and $h^{\prime}$ are faithfully flat and affine. So $H$ is a presentation. It remains to show that it satisfies the universal property of the fiber product. Let $\tilde{F}: \operatorname{Spec}(S) \rightarrow \mathcal{Z}$ be a rigidified algebraic stack with morphisms $\left(\delta, \delta_{0}\right): \tilde{F} \rightarrow F$ and $\left(\delta^{\prime}, \delta_{0}^{\prime}\right): \tilde{F} \rightarrow F^{\prime}$ such that $\left(\alpha, \alpha_{0}\right) \circ\left(\delta, \delta_{0}\right) \cong\left(\alpha^{\prime}, \alpha_{0}^{\prime}\right) \circ\left(\delta^{\prime}, \delta_{0}^{\prime}\right)$.

Then, the universal property of $\mathcal{X} \times_{\mathcal{Y}} \mathcal{X}^{\prime}$ gives the existence of $\xi: \mathcal{Z} \rightarrow \mathcal{X} \times_{\mathcal{Y}} \mathcal{X}^{\prime}$ in the following diagram
![img-30.jpeg](img-30.jpeg)

The morphism $\xi_{0}: \operatorname{Spec}(S) \rightarrow R$ is obtained by the following diagram
![img-31.jpeg](img-31.jpeg)

The dotted square commutes by assumption, the two small triangles commute by the definition of morphisms of rigidified algebraic stacks and $\xi_{0}$ exists as the outer square is a pullback. Thus, if $\left(\xi, \xi_{0}\right)$ is a morphism of rigidified algebraic stacks, i.e. commutes with the presentations, $H$ satisfies the universal property of the fiber product as claimed. The last point follows from another diagram chase, which exploits that $P$ and $P^{\prime}$ are pullbacks.

Let us summarise some of the reasons why it is helpful to be able to think of rigidified algebraic stacks as Hopf algebroids:

- As seen in remark 1.37, it becomes easy to compute pullbacks from affine schemes. Even better, as explained in remark 1.42, we have an explicit expression for the pullback of any span of algebraic stacks. Notice that (fortunately, we would be in trouble otherwise) the expression found in remark 1.37 coincides with the one of remark 1.42 when identifying the affine scheme $X$ with the stack $[(X, X)]$ as explained in remark 1.35 .
- Properties that are stable under base change and satisfy fpqc-descent such as flatness etc. can be checked only against the presentation as seen in corollary 1.38. Moreover, if the morphism of which we want to determine the properties has an affine scheme as source, i.e. it is some $f: \operatorname{Spec}(R) \rightarrow[(\operatorname{Spec}(A), \operatorname{Spec}(\Gamma))]$, then, by the computation in remark 1.37, the question comes down to determining if $\operatorname{Spec}\left(R \otimes_{A} \Gamma\right) \rightarrow \operatorname{Spec}(A)$ has the desired property. This then often becomes a purely algebraic problem.
- Conversely, translating to stacks can transform a complicated algebraic problem into a more conceptual geometric problem. We will see instances of this in the following section (prop. 2.13, cor. 2.44).
- Theorem 1.40 sometimes gives maps of stacks for free. As we will see in the following subsection, in certain situations, it is easy to find morphisms of Hopf algebroids which we can transform into morphisms of stacks.
- As will be discussed in the following subsection, one can associate Hopf algebroids and hence stacks to nice enough spectra. Then, one can use algebro-geometric techniques to do topology.


# 1.3 Hopf Algebroids, Spectra and the Moduli Stack of Formal Groups 

In this subsection, we explore the link between stacks and spectra. As algebraic topologists, we will be happy to notice that for any nice enough homotopy commutative ring spectrum $(E, \eta, \mu)$ the pair $\left(\pi_{*}(E), E_{*}(E)\right)$ forms a Hopf algebroid:

Definition 1.44. A homotopy commutative ring spectrum $E$ is flat or of Adams type if $E_{*}(E)$ is flat as a left $\pi_{*}(E)$-module i.e. the morphism $\pi_{*}(\mathbb{S} \otimes E) \xrightarrow{\pi_{*}(\eta \otimes E)} \pi_{*}(E \otimes E)$ is flat.

Notation 1.45. From now on, we will usually write $E_{*}$ for the graded ring $\pi_{*}(E)$.
Remark 1.46. Even though the left and right module structure might differ, asking for $E_{*}(E)$ to be flat as left $E_{*}$-module is equivalent to asking for it as a right $E_{*}$-module. Indeed, $\pi_{*}(\eta \otimes E)=\pi_{*}(\tau \circ E \otimes \eta)$ where $\tau$ denotes the switch map. This is flat because the composition of flat maps is flat and $\pi_{*}(\tau)$ is flat as it is an isomorphism. More precisely, the following diagram commutes:
![img-32.jpeg](img-32.jpeg)

Example 1.47. - The sphere spectrum $\mathbb{S}$ is trivially of Adams type as $\mathbb{S}_{*}(\mathbb{S}) \cong \mathbb{S}$.

- Even though $H \mathbb{F}_{p_{*}}\left(H \mathbb{F}_{p}\right)$ is more complicated (it is the dual Steenrod algebra), it is an $\mathbb{F}_{p}$-vector space and as such flat over $\mathbb{F}_{p}=\pi_{*}\left(H \mathbb{F}_{p}\right)$. Hence, $H \mathbb{F}_{p}$ is flat. More generally, for any field $k, H k$ is flat.
- Recall that $M U_{*}(M U)=M U_{*}\left[b_{1}, b_{2}, \ldots\right]$ with $\left|b_{i}\right|=2 i$; see [19, Lem. 4.1.7.]. In particular, $M U_{*}(M U)$ is a free $M U_{*}$-module and $M U$ is of Adams type.
- As a special case of the future proposition $2.59, K U$ is flat.
- One can show that $M S p$ is flat; see [2, Lem. 28].
- It is well known that both $H \mathbb{Z}$ and $M S U$ are not flat ([19, after Prop. 2.2.6]).

Flatness of the spectrum is crucial because it is necessary for the following lemma to hold, which in turn will be crucial for the definition of the diagonal map.

Lemma 1.48 ([19, Lem. 2.7.7]). If $E$ is a flat spectrum, the composition

$$
\varphi_{E}: \pi_{*}(E \otimes E) \otimes_{\pi_{*}(E)} \pi_{*}(E \otimes E) \rightarrow \pi_{*}(E \otimes E \otimes E \otimes E) \xrightarrow{E \otimes \mu \otimes E} \pi_{*}(E \otimes E \otimes E)
$$

where the first arrow is induced by the exterior product, is an isomorphism.
Proof. We will show more generally that for any spectrum $X$ there are natural isomorphisms

$$
\varphi_{X}: \pi_{*}(X \otimes E) \otimes_{\pi_{*}(E)} \pi_{*}(E \otimes E) \rightarrow \pi_{*}(X \otimes E \otimes E \otimes E) \xrightarrow{X \otimes \mu \otimes E} \pi_{*}(X \otimes E \otimes E)
$$

Naturality is clear as all the involved morphisms are functorial.
Consider the family of spectra $Y$ such that $\varphi_{Y}$ is an isomorphism. Trivially, it contains $\varphi_{\mathbb{S}}$ and, as tensoring with $\mathbb{S}^{n}$ amounts to shifting, it also contains $\mathbb{S}^{n}$ for all $n \in \mathbb{Z}$. As filtered colimits and direct sums commute with $\pi_{*}(-)$, the family is closed under those. Hence, it remains to see that this family is also closed under cofibers to argue it contains all spectra. So consider an arbitrary morphism of spectra $f: X \rightarrow Y$ and denote its cofiber by $C$. As the tensor product, being a left adjoint, commutes with colimits, $X \otimes E \rightarrow Y \otimes E \rightarrow C \otimes E$ is a cofiber sequence and yields a long exact sequence on homotopy groups. The same holds for that cofiber sequence tensored with $E$ once again. As $E$ is flat by assumption, this sequence remains exact when applying $(-) \otimes_{E_{*}} E_{*}(E)$. By naturality, the following diagram with exact rows commutes:

One concludes by the five lemma that $\varphi_{C}$ is an isomorphism as well. Specialising to $\varphi_{E}$ gives the statement of the lemma.

With this isomorphism at hand, we can define the Hopf algebroid structure on $\left(E_{*}, E_{*}(E)\right)$.
Corollary 1.49. Let $(E, \eta, \mu)$ be a flat homotopy commutative ring spectrum. Then, $\left(E_{*}, E_{*}(E)\right)$ is a flat graded Hopf algebroid with respect to the following maps:

- The left and right units $\eta_{L}, \eta_{R}: \pi_{*}(E) \rightarrow \pi_{*}(E \otimes E)$ are induced by applying $\eta$ to the right or left respectively.
- The counit $\epsilon: \pi_{*}(E \otimes E) \rightarrow \pi_{*}(E)$ is induced by the multiplication.
- The diagonal $\psi_{E}: \pi_{*}(E \otimes E) \rightarrow \pi_{*}(E \otimes E) \otimes_{\pi_{*}(E)} \pi_{*}(E \otimes E)$ is induced by composing the morphism $\pi_{*}(E \otimes E) \xrightarrow{E \otimes \eta \otimes E} \pi_{*}(E \otimes E \otimes E)$ with $\varphi_{E}^{-1}$ from lemma 1.48.
- The conjugation $i: \pi_{*}(E \otimes E) \rightarrow \pi_{*}(E \otimes E)$ is induced by the switch map $\tau$.

Proof. The proof consists of straightforward checks, mostly relying on the properties of the multiplication and unit of a ring spectrum. For example that $e \circ \eta_{L}=i d$ is just unitality and functoriality. Details are given in [2, Lecture 3].

Example 1.50. The flat Hopf algebroid $\left(\mathbb{S}_{*}, \mathbb{S}_{*}(\mathbb{S})\right)$ is equivalent to the trivial Hopf algebroid obtained from the ring $\mathbb{S}$ with all structure maps the identity.

A more interesting example is given by the Hopf algebroid $\left(M U_{*}, M U_{*}(M U)\right)$. We will need the following facts and definitions, with which we assume the reader to be familiar. We recall them for completeness.

Definition 1.51 ([19, Def. A2.1.1.]). A formal group law over a ring $R$ is a formal power series $F \in R[[x, y]]$ such that:

- (unital) $F(x, 0)=F(0, x)=x$,
- (commutative) $F(x, y)=F(x, y)$,
- (associative) $F(F(x, y), z)=F(x, F(y, z))$ in $R[[x, y, z]]$.

Unitality implies that any formal group law is of the form $x+y+\Sigma_{i, j>1} a_{i j} x^{i} y^{j} a_{i j} \in R$ ([19, Prop. A2.1.3]). Moreover, one can show that any formal group law admits a formal inverse, i.e. a power series $i(x) \in R[[x]]$ such that $F(x, i(x))=0$; see [19, Prop. A2.1.2]. There is a universal formal group law:

Theorem 1.52 ([19, Thm. A2.1.8]). There is a ring $L$, called the Lazard ring, and a formal group law $F(x, y)=\Sigma_{i, j \geq 1} a_{i j} x^{i} y^{j}$, called the universal formal group law, defined over it such that for any formal group law $G$ over any commutative ring with unit $R$ there is a unique ring homomorphism $\theta: L \rightarrow R$ such that $G(x, y)=\Sigma_{i, j \geq 1} \theta\left(a_{i j}\right) x^{i} y^{j}$.
This ring is easy to construct, it is given by $L=\mathbb{Z}\left[a_{i j}\right] / I$ where $I$ is the ideal generated by the relations among the $a_{i j}$ so that the conditions of definition 1.51 are satisfied. We introduce a grading on $L$ by setting $\left|a_{i j}\right|=2(i+j-1)$. By the previous proposition, the Lazard ring represents the functor $F G L:$ Rings $\rightarrow$ Sets sending a ring to the set of formal group laws over it. The Lazard ring is (non-canonically) isomorphic to an even, infinitely generated polynomial ring:

Theorem 1.53 (Lazard, [19, Thm. A2.1.10]). $L \cong \mathbb{Z}\left[x_{1}, x_{2}, \ldots\right]$ with $\left|x_{i}\right|=2 i$ for $i>0$.
Definition 1.54 ([19, Def. A2.1.5.]). Let $F$ and $G$ be formal group laws over $R$. A homomorphism from $F$ to $G$ is a power series $f(x) \in R[[x]]$ with constant term 0 such that $f(F(x, y))=G(f(x), f(y))$. It is an isomorphism if it is invertible, i.e. if $f^{\prime}(0)$ is a unit in $R$, and a strict isomorphism if $f^{\prime}(0)=1$.

For a ring $R$, let $I(R)$ be the set of triples $(F, f, G)$ where $F$ and $G$ are formal group laws on $R$ and $f: F \rightarrow G$ is an isomorphism. Let $S I(R)$ be the set of triples $(F, f, G)$ where $F$ and $G$ are as before and $f$ is a strict isomorphism. It is easy to check that $I(-)$ and $S I(-)$ define functors from Rings to Sets that are represented by the rings $W:=L\left[b_{0}^{S}, b_{1}, b_{2}, \ldots\right]$ and $L B:=L\left[b_{1}, b_{2}, \ldots\right]$ respectively; see [19, Prop. A2.1.15.]. We introduce a grading on them by setting $\left|b_{i}\right|=2 i$.

Proposition 1.55 ([19, Thm. A2.1.16]). The pair $(L, L B)$ is a Hopf algebroid. The structure maps are obtained thanks to the Yoneda lemma:

- The left unit $\eta_{L}: L \rightarrow L B$ corresponds to the natural transformation $S I(-) \rightarrow F G L(-)$ sending a triple $(F, f, G) \in S I(R)$ onto the source $F$ of $f$. This is simply the inclusion of $L$ into $L\left[b_{1}, b_{2}, \ldots\right]$.

- The right unit $\eta_{R}: L \rightarrow L B$ corresponds to the natural transformation $S I(-) \rightarrow F G L(-)$ sending a triple $(F, f, G) \in S I(R)$ onto the target $G$ of $f$. Under the correspondence of theorem 1.52, this is the map classifying the formal group law $g\left(F\left(g^{-1}(x), g^{-1}(y)\right)\right)$ where $F$ denotes the universal formal group law and $g$ the power series $x+b_{1} x+b_{2} x^{2}+\cdots \in L B[[x]]$.
- The counit $\epsilon: L B \rightarrow L$ corresponds to the natural transformation $F G L(-) \rightarrow S I(-)$ sending a formal group law $F$ to the triple $\left(F, i d_{F}, F\right)$. This corresponds to sending all the $b_{i}$ to zero.
- The diagonal $\psi: L B \otimes_{L} L B \rightarrow L$ corresponds to the natural transformation $S I(-) \times S I(-) \rightarrow S I(-)$ encoding composition of strict isomorphisms.
- The conjugation $c: L B \rightarrow L B$ corresponds to the natural transformation $S I(-) \rightarrow S I(-)$ encoding the inversion of isomorphisms.
Remark 1.56. The isomorphism $L \cong \mathbb{Z}\left[x_{1}, x_{2}, \ldots\right]$ from theorem 1.53 can be constructed in such a way that the composite $L \xrightarrow{\text { fin }} L B \xrightarrow{\text { a }} \mathbb{Z}\left[b_{1}, b_{2}, \ldots\right]$ sends $x_{i}$ to $b_{i}+$ terms of degree $\geq 2$. Here $q: L B \cong \mathbb{Z}\left[x_{1}, x_{2}, \ldots\right]\left[b_{1}, b_{2}, \ldots\right] \rightarrow \mathbb{Z}\left[b_{1}, b_{2}, \ldots\right]$ is the quotient map. This is the content of $[19$, Thm. A2.1.10, 2)].

The link between these facts and the spectrum $M U$ will be made via the following lemma.
Lemma 1.57 ([19, Lem. 4.1.4]). Let $E$ be a complex oriented homotopy commutative ring spectrum with complex orientation $x_{E}$.

1. $E^{*}\left(\mathbb{C} P^{\infty}\right)=E_{*}\left[\left[x_{E}\right]\right]$.
2. $E^{*}\left(\mathbb{C} P^{\infty} \times \mathbb{C} P^{\infty}\right)=E_{*}\left[\left[x_{E} \otimes 1,1 \otimes x_{E}\right]\right]$.
3. Let $\mu: \mathbb{C} P^{\infty} \times \mathbb{C} P^{\infty} \rightarrow \mathbb{C} P^{\infty}$ be the $H$-space structure map. Then the element $\mu^{*}\left(x_{E}\right) \in E_{*}[[x, y]]$ is a formal group law over $E_{*}$.
As $M U$ is complex oriented, keeping the notation of the previous lemma, $\mu^{*}\left(x_{M U}\right)$ is a formal group law corresponding to a ring homomorphism $\theta_{M U}: L \rightarrow M U_{*}$ by theorem 1.52. This map is the key to the understanding of $\left(M U_{*}, M U_{*}(M U)\right)$.
Theorem 1.58 ([19, Thm. 4.1.6, Thm. 4.1.11]). The map $\theta_{M U}$, extended to $L B \rightarrow M U_{*}(M U)$ by mapping $b_{i}$ to $b_{i}^{M U}$, gives an isomorphism of Hopf algebroids $\left(M U_{*}, M U_{*}(M U)\right) \cong(L, L B)$ where $(L, L B)$ is the Hopf algebroid constructed in proposition 1.55.
The fact that $\theta_{M U}$ induces an isomorphism $L \cong M U_{*}$ is due to Quillen, the remaining statements are due to Landweber and Novikov.

Now that we can associate a flat Hopf algebroid to a spectrum of Adams type, we would like to use the equivalence of categories from theorem 1.40 to construct its associated stack. However, we need to take care because, for a given spectrum $E$, the ring $E_{*}$ is only graded commutative (i.e. it satisfies the Koszul sign rule) and we cannot in general apply $\operatorname{Spec}(-)$ to it. We will deal with this by only considering even spectra or the evenly graded part of $E_{*}$.
When we wish to emphasise the fact that a ring $A$ is graded, we will denote it by $\left\{A_{j}\right\}_{j \in \mathbb{Z}}$. When it is clear from the context, we will denote both the graded ring $\left\{A_{j}\right\}_{j \in \mathbb{Z}}$ and its ungraded counterpart $\oplus_{j} A_{j}$ by $A$. We keep this convention throughout.
Corollary 1.59. To any even, flat homotopy commutative ring spectrum $(E, \eta, \mu)$, one can associate a rigidified algebraic stack $\left[\left(E_{*}, E_{*}(E)\right)\right]$. We will usually denote its chosen presentation by $c: \operatorname{Spec}\left(E_{*}\right) \rightarrow$ $\left[\left(E_{*}, E_{*}(E)\right)\right]$
Proof. The rigidified algebraic stack $\left[\left(E_{*}, E_{*}(E)\right)\right]$ is, as the notation suggests, constructed as the stack associated to the Hopf algebroid $\left(E_{*}, E_{*}(E)\right)$ under the equivalence of categories of theorem 1.40. More precisely, given an affine scheme $U$, the objects of $\left[\left(E_{*}, E_{*}(E)\right)\right](U)$ are triples

$$
\left(\left\{U^{\prime} \rightarrow U\right\}, x^{\prime}: U^{\prime} \rightarrow \operatorname{Spec}\left(E_{*}\right), \xi_{12}\right)
$$

where $U^{\prime}$ is an fpqc-cover of $U$ and $\xi_{12}$ descent datum. The morphisms of $\left[\left(E_{*}, E_{*}(E)\right)\right](U)$ between objects $\left(\left\{U^{\prime} \rightarrow U\right\}, x^{\prime}: U^{\prime} \rightarrow \operatorname{Spec}\left(E_{*}\right), \xi_{12}\right)$ and $\left(\left\{U^{\prime \prime} \rightarrow U\right\}, x^{\prime \prime}: U^{\prime \prime} \rightarrow \operatorname{Spec}\left(E_{*}\right), \xi_{12}^{\prime}\right)$ are given by a morphism $U^{\prime} \times_{U} U^{\prime \prime} \rightarrow \operatorname{Spec}\left(E_{*}(E)\right)$ such that

$$
U^{\prime} \times_{U} U^{\prime \prime} \rightarrow \operatorname{Spec}\left(E_{*}(E)\right) \xrightarrow{\operatorname{Spec}\left(\eta_{L}\right)} \operatorname{Spec}\left(E_{*}\right)=x^{\prime} \mid U^{\prime} \times_{U} U^{\prime \prime}
$$

and

$$
U^{\prime} \times_{U} U^{\prime \prime} \rightarrow \operatorname{Spec}\left(E_{*}(E)\right) \xrightarrow{\operatorname{Spec}\left(\eta_{R}\right)} \operatorname{Spec}\left(E_{*}\right)=\left.x^{\prime \prime}\right|_{U^{\prime} \times_{U} U^{\prime \prime}}
$$

compatibly with the descent data. The presentation $c$ is given by sending a morphism $U \rightarrow \operatorname{Spec}\left(E_{*}\right) \in$ $O b\left(\operatorname{Spec}\left(E_{*}\right)(U)\right)$ to the object $\left(i d_{U}, U \rightarrow \operatorname{Spec}\left(E_{*}\right), i d_{U}\right) \in\left[\left(E_{*}, E_{*}(E)\right)\right](U)$.

The fact that this stack was constructed from a graded Hopf algebroid is remembered by the fact that it admits an action of the group scheme $\mathbb{G}_{m}=\operatorname{Spec}\left(\mathbb{Z}\left[u^{ \pm}\right]\right)$. Let us first explain how $\mathbb{G}_{m}$-actions correspond to gradings on a ring.

Proposition 1.60. Given a commutative ring $R$, there is a natural one-to-one correspondence between $\mathbb{G}_{m}$-actions on $\operatorname{Spec}(R)$ and $\mathbb{Z}$-gradings of $R$.

Proof. An action $\Phi: \mathbb{G}_{m} \times \operatorname{Spec}(R) \rightarrow \operatorname{Spec}(R)$ corresponds to a map $\phi: R \rightarrow R \otimes \mathbb{Z}\left[u^{ \pm}\right]$that is counital and coassociative. More precisely, counitality of the action corresponds to the identity $e v_{1} \circ \phi=i d_{R}$ where $e v_{1}: R\left[u^{ \pm}\right] \rightarrow R$ is defined by sending $t$ to 1 . Coassociativity states that $(\mu \otimes R) \circ \phi=\left(\mathbb{Z}\left[u^{ \pm}\right] \otimes \phi\right) \circ \phi$ where $\mu: \mathbb{Z}\left[u^{ \pm}\right] \rightarrow \mathbb{Z}\left[u^{ \pm}, s^{ \pm}\right]$maps $t$ to $t s$.
For $i \in \mathbb{Z}$, define $R_{i}:=\phi^{-1}\left(R\left\langle u^{i}\right\rangle\right)$ i.e. $R_{i}$ is the preimage of the polynomials of the form $r u^{i} \in R\left[u^{ \pm}\right]$. We claim that $\phi$ defines an isomorphism $R \cong \oplus_{i \in \mathbb{Z}} R_{i}$ with the summing map $\left(e v_{1}\right)$ as inverse. In particular, the $R_{i}$ give a grading on $R$. As seen above, counitality of $\phi$ ensures that $e v_{1}$ is a left inverse for $\phi$, i.e. that if $\phi(r)=\Sigma_{i \in \mathbb{Z}} r_{i} u^{i}$, then $\Sigma_{i \in \mathbb{Z}} r_{i}=r$. Coassociativity ensures that for $r_{i} \in R_{i}$ it holds that $\phi\left(r_{i}\right)=r_{i} u^{i}$ since it states that
$(\mu \otimes R) \circ \phi(r)=(\mu \otimes R)\left(\Sigma_{i \in \mathbb{Z}} r_{i} u^{i}\right)=\Sigma_{i \in \mathbb{Z}} r_{i} u^{i} s^{i}=\left(\mathbb{Z}\left[u^{ \pm}\right] \otimes \phi\right) \circ \phi(r)=\Sigma_{i \in \mathbb{Z}} \phi\left(r_{i}\right) s^{i}=\Sigma_{i \in \mathbb{Z}}\left(\Sigma_{j \in \mathbb{Z}}\left(r_{i}\right)_{j} u^{j}\right) s^{i}$.
Matching the degrees gives that $\phi\left(r_{i}\right)=r_{i} u^{i}$. Thus, $\phi \circ e v_{1}\left(\Sigma_{i \in \mathbb{Z}} r_{i} u^{i}\right)=\Sigma_{i \in \mathbb{Z}} r_{i} u^{i}$ i.e. $\phi \circ e v_{1}=i d_{R\left[u^{ \pm}\right]}$ as claimed.
Conversely, given a grading on $R$, i.e. some isomorphism $\alpha: R \cong \oplus_{i \in \mathbb{Z}} R_{i}$ one gets the map $\phi: R \rightarrow R\left[u^{ \pm}\right]$ as $r \mapsto \Sigma_{i \in \mathbb{Z}} \alpha(r)_{i} u^{i}$. This is counital as $r=\Sigma_{i \in \mathbb{Z}} \alpha(r)_{i}$ by construction and coassociative as $\alpha\left(r_{i}\right)=r_{i}$ (in other words $r_{i}$ is homogeneous by assumption). It is straightforward that these two constructions are inverses.

Example 1.61. The grading that was arbitrarily introduced on the Lazard ring after theorem 1.52 is more natural from this perspective. It is the one corresponding to the $\mathbb{G}_{m}$-action on $\operatorname{Spec}(L)$ by sending a pair $(r, F(x, y)) \in \mathbb{G}_{m}(R) \times \operatorname{Spec}(L)(R)=R^{\times} \times F G L(R)$ to the formal group law $r F\left(r^{-1} x, r^{-1} y\right)$.

By the previous proposition, a commutative, graded, flat Hopf algebroid $(A, \Gamma)$ corresponds to a $\mathbb{G}_{m^{-}}$ action on $\operatorname{Spec}(A)$ and a $\mathbb{G}_{m}$-action on $\operatorname{Spec}(\Gamma)$ which are compatible with all the structure maps as these were graded maps. By the equivalence of categories of theorem 1.40, these actions induce a map of stacks $\left[\left(\mathbb{G}_{m}, \mathbb{G}_{m}\right)\right] \times[(\operatorname{Spec}(A), \operatorname{Spec}(\Gamma))] \rightarrow[(\operatorname{Spec}(A), \operatorname{Spec}(\Gamma))]$ which is the $\mathbb{G}_{m}$-action on the stack that was announced above.
Another way to remember the grading of a Hopf algebroid $(A, \Gamma)$ while working with ungraded objects is by encoding it into $\Gamma$ as described in the following lemma. This approach will prove to be very useful in the next section.

Lemma 1.62. There is a functor $U$ : evenly graded Hopf algebroids $\rightarrow$ (ungraded) Hopf algebroids sending $\left(\left\{A_{2 j}\right\}_{j \in \mathbb{Z}},\left\{\Gamma_{2 k}\right\}_{k \in \mathbb{Z}}\right)$ to $\left(\oplus_{j} A_{2 j},\left(\oplus_{k} \Gamma_{2 k}\right)\left[u^{ \pm}\right]\right)$.

Proof. The structure maps are defined as follows:

- $\eta_{L}^{\left(A, \Gamma\left[u^{ \pm}\right]\right)}:=i \circ \eta_{L}^{(A, \Gamma)}$ where $i$ denotes the inclusion $\Gamma \hookrightarrow \Gamma\left[u^{ \pm}\right]$and $\eta_{L}^{(A, \Gamma)}$ is to be understood as $\oplus_{j} \eta_{L}^{\left(A_{j}, \Gamma_{j}\right)}$. We keep this notation throughout.
- $\eta_{R}^{\left(A, \Gamma\left[u^{ \pm}\right]\right)}(a)=u^{\frac{|a|}{2}} \eta_{R}^{(A, \Gamma)}(a)$.
- $\epsilon^{\left(A, \Gamma\left[u^{ \pm}\right]\right)}: \Gamma\left[u^{ \pm}\right] \rightarrow A$ is defined by $\left.\epsilon^{\left(A, \Gamma\left[u^{ \pm}\right]\right)}\right|_{\Gamma}=\epsilon^{(A, \Gamma)}$ and mapping $u$ to $1_{A}$.
- $c^{\left(A, \Gamma\left[u^{ \pm}\right]\right)}: \Gamma\left[u^{ \pm}\right] \rightarrow \Gamma\left[u^{ \pm}\right]$is defined by $c^{\left(A, \Gamma\left[u^{ \pm}\right]\right)}(\gamma)=u^{\frac{|\gamma|}{2}} c^{(A, \Gamma)}(\gamma)$ for $\gamma \in \Gamma$ and mapping $u$ to $u^{-1}$.
- $\psi^{\left(A, \Gamma\left[u^{ \pm}\right]\right)}: \Gamma\left[u^{ \pm}\right] \rightarrow \Gamma\left[v^{ \pm}\right] \otimes_{\eta_{L}, A, \eta_{R}} \Gamma\left[w^{ \pm}\right]$is defined by $\left.\psi^{\left(A, \Gamma\left[u^{ \pm}\right]\right)}\right|_{\Gamma \otimes_{A} \Gamma}=\psi^{(A, \Gamma)}$ and mapping $u$ to $v \otimes w$.

One checks that these maps define a Hopf algebroid structure on $\left(A, \Gamma\left[u^{ \pm}\right]\right)$because they were constructed from the structure maps of $(A, \Gamma)$. For example, for $a \in A$,

$$
c^{\left(A, \Gamma\left[u^{ \pm}\right]\right)} \circ \eta_{R}^{\left[A, \Gamma\left[u^{ \pm}\right]\right)}(a)=c^{\left(A, \Gamma\left[u^{ \pm}\right]\right)}\left(u^{\frac{|a|}{2}} \eta_{R}^{(A, \Gamma)}(a)\right)=u^{-\frac{|a|}{2}} u^{\frac{|a|}{2}} c^{(A, \Gamma)} \eta_{R}^{(A, \Gamma)}(a)=\eta_{L}^{(A, \Gamma)}(a)=\eta_{L}^{\left(A, \Gamma\left[u^{ \pm}\right]\right)}(a)
$$

hence $c^{\left(A, \Gamma\left[u^{ \pm}\right]\right)} \circ \eta_{R}^{\left(A, \Gamma\left[u^{ \pm}\right]\right)}=\eta_{L}^{\left(A, \Gamma\left[u^{ \pm}\right]\right)}$. The other identities are shown similarly.
A morphism of Hopf algebroids $\left(f_{1}, f_{2}\right):(A, \Gamma) \rightarrow\left(A^{\prime}, \Gamma^{\prime}\right)$ gets mapped to $\left(f_{1}, f_{2}[u]\right):\left(A, \Gamma\left[u^{ \pm}\right]\right) \rightarrow$ $\left(A^{\prime}, \Gamma^{\prime}\left[u^{ \pm}\right]\right)$where $f_{2}[u]$ is $f_{2}$ on $\Gamma$ and sends $u$ to $u$. This construction is clearly a morphism of Hopf algebroids and functorial.

Example 1.63. The Hopf algebroids $U\left(M U_{*}, M U_{*}(M U)\right)$ is isomorphic to $(L, W)$ where $W \cong L B\left[u^{ \pm}\right]$ is the ring representing (nonstrict) isomorphism of formal group laws introduced after definition 1.54. The structure maps are as described by lemma 1.62 and proposition 1.55 .

From the proof of corollary 1.59, it is not clear at all what the stacks $\left[\left(E_{*}, E_{*}(E)\right)\right]$ and $\left[\left(E_{*}, E_{*}(E)\left[u^{ \pm}\right]\right)\right]$ represent geometrically. This problem was already addressed shortly after the proof of theorem 1.32. For example, we know that the objects in $\left[\left(M U_{*}, M U_{*}(M U)\right)\right](\operatorname{Spec}(R))$ that are in the image of $i:\left[\left(M U_{*}, M U_{*}(M U)\right)\right]^{\prime} \rightarrow\left[\left(M U_{*}, M U_{*}(M U)\right)\right]$ as defined in theorem 1.32 correspond to morphisms $M U_{*} \cong L \rightarrow U$ i.e. they are formal group laws over $R$. But what about all the other ones, those that are not in the image of $i$ ? In this particular case, we get lucky as there is already a stack that was defined geometrically whose objects are candidates for answering this question:the moduli stack of formal groups for $(L, W)$ and the moduli stack of formal groups and strict isomorphisms for $\left(M U_{*}, M U_{*}(M U)\right)$.

Before we can define the stack that will be associated to $M U$, we need to introduce formal groups. They should be some sort of object that locally resembles a formal group law and satisfies effective descent. We begin by observing that a formal group law $F$ over a ring $R$ defines a functor $\mathcal{G}_{F}: \operatorname{Aff}_{\operatorname{Spec}(R)}^{\text {op }} \rightarrow A b$ by sending an $R$-algebra $A$ to its set of nilpotent elements with group structure given by $a+b=F(a, b)$. As $a, b \in \operatorname{Nil}(a), F(a, b)$ is a well-defined element despite $F$ being an infinite power series. The axioms defining a formal group law ensure that this does define an abelian group structure. Notice that endowing $A$ with the discrete topology and $R[[t]]$ with the $(t)$-adic one, the set of nilpotent elements of $A$ is also picked out by the functor $\operatorname{Spf}(R[[t]]):=\hat{\mathbb{A}}_{R}^{1}: \operatorname{Aff}_{\operatorname{Spec}(R)}^{\text {op }} \rightarrow$ Sets that maps $A$ to $\operatorname{Hom}_{\text {cts }}(R[[t]], A)$. It thus seems reasonable to define a formal group to be a functor $F: \mathrm{Aff}^{\text {op }} \rightarrow A b$ that is locally of the form $\operatorname{Spf}(R[[t]])$, i.e. locally a formal group law. If we want it to satisfy effective descent, we should also ask for it to be some sheaf. This is what we do.

Definition 1.64 ([16, Def. 3.7]). A formal group over an affine scheme $\operatorname{Spec}(R)$ is a Zariski sheaf $F: \operatorname{Aff}_{\operatorname{Spec}(R)}^{\text {op }} \rightarrow A b$ such that there exist a Zariski open cover $\left\{U_{i}=\operatorname{Spec}\left(R_{i}\right)\right\}_{i}$ of $\operatorname{Spec}(R)$ such that $\left.F\right|_{U_{i}}$ is equivalent to $\hat{\mathbb{A}}_{R_{i}}^{1}$.

Definition 1.65. A formal group $F$ over $R$ is coordinatizable if it is isomorphic to $\hat{\mathbb{A}}_{R}^{1}$.
Remark 1.66. This is a general construction: Let $R$ be a ring, $I$ an ideal of $A$ and equip $A$ with the minimal topology such that all $I^{n}$ are open and which is closed under translation. We define the formal spectrum of $(R, I)$ as the presheaf $\operatorname{Spf}(R): \operatorname{Aff}^{\text {op }} \rightarrow$ Sets sending a ring $B$ endowed with the discrete topology to the set $\operatorname{Hom}_{\text {cts }}(R[[t]], A)$.

We can now define the moduli stack of formal groups.
Definition 1.67. - The moduli stack of formal groups $\mathcal{M}_{F G}$ is the stack which associates to an affine scheme $\operatorname{Spec}(R)$ the groupoid $\mathcal{M}_{F G}(\operatorname{Spec}(R))$ whose objects are formal groups over $\operatorname{Spec}(R)$ and whose morphisms are isomorphisms of formal groups.

- The moduli stack of formal groups and strict isomorphisms $\mathcal{M}_{F G}^{s}$ is the stack which associates to an affine schems $\operatorname{Spec}(R)$ the groupoid $\mathcal{M}_{F G}^{s}(\operatorname{Spec}(R))$ whose objects are pairs $(F, \alpha)$ with $F$ a formal group over $\operatorname{Spec}(R)$ and $\alpha$ an isomorphism from $F$ to $\hat{\mathbb{A}}_{R}^{1}$, i.e. its objects are coordinatizable formal groups with a chosen coordinate. Its morphisms are isomorphisms of formal groups which respect this isomorphism in an obvious way; see [18, Sec. 6] or [15, Prop. 7, 2)] for a more geometric interpretation.

From this definition, it is very unclear why $\mathcal{M}_{F G}$ defines a stack for the fpqc-topology. While it seems believable that isomorphisms of two given formal groups assemble into a sheaf, i.e. that the first condition of definition 1.2 is satisfied, the second condition is difficult to prove. In the literature, there are essentially two approaches to this problem. In [6], Paul Goerss defines formal groups a little bit differently, specifically so that they "evidently satisfy the effective descent condition necessary to produce a moduli stack". More precisely, he defines formal groups as group objects in the category of formal Lie varieties with the additional property that their conormal sheaf is locally free of rank 1 (see [6, Def. 2.2]). With this at hand, the proof that the moduli stack of formal groups is a stack [6, Prop. 2.6] comes down to the facts that isomorphisms between formal Lie varieties form a sheaf ([6, Lem. 1.34]) and that in formal Lie varieties there is always a unique solution to descent problems ([6, Lem. 1.35]). Both these lemmas are shown by exploiting the definition of formal Lie varieties. From this approach, showing that $\mathcal{M}_{F G}$ is a stack is not so hard, but one would still have to argue why the formal Lie variety definition matches the usual definition of formal groups. This is some work.
In [18, Sec. 6], Niko Naumann has a different approach. He defines $\mathcal{M}_{F G}$ as some substack of the stack of commutative group objects in the stack of formal schemes. The stack of formal schemes is defined as the functor classifying formal schemes. To argue that this forms a stack, Naumann refers to [23], where it is argued between the lines that the stack of formal schemes is a stack by showing that faithfully flat descent arguments carry through to the formal setting ( $[23$, Prop. 2.70, Rmk. 4.52]). More precisely, $\mathcal{M}_{F G}$ is the substack consisting of objects that are fpqc-locally isomorphic to the formal scheme $\left(\hat{\mathbb{A}}^{1}, 0\right)$ as pointed formal schemes. Knowing this, it is clear that $\mathcal{M}_{F G}^{s}$ is a stack as well, as it can be identified with a $\mathbb{G}_{m}$-torsor over $\mathcal{M}_{F G}$ as explained in [18, Sec. 6]. Here, we will not say more about this and accept the fact that they all define stacks.
Now, one can wonder whether these stacks are algebraic and, if so, what Hopf algebroids they correspond to. Observe that $\mathcal{M}_{F G}$ admits a canonical morphism $c: \operatorname{Spec}(L) \rightarrow \mathcal{M}_{F G}$ classifying the universal formal group under the identification of remark 1.6. An analogous morphism $c^{*}$ exists for $\mathcal{M}_{F G}^{*}$. This is a good candidate for a presentation.

Proposition 1.68. The moduli stack of formal groups $\mathcal{M}_{F G}$ is algebraic. Moreover, the morphism $c: \operatorname{Spec}(L) \rightarrow \mathcal{M}_{F G}$ classifying the universal formal group is a presentation and $\left(\mathcal{M}_{F G}, c\right)$ is equivalent to $[(L, W)]$ under the equivalence of theorem 1.40.
The analogous statement holds for $\mathcal{M}_{F G}^{s}$, in particular $\left(\mathcal{M}_{F G}^{s}, P^{s}\right) \cong\left[\left(M U_{*}, M U_{*}(M U)\right)\right]$.
Proof. We need to show that $c: \operatorname{Spec}(L) \rightarrow \mathcal{M}_{F G}$ is affine and faithfully flat and that the fiber product $\operatorname{Spec}(L) \times_{\mathcal{M}_{F G}} \operatorname{Spec}(L)$ is equivalent to $\operatorname{Spec}(W)$.
For the first, we need to argue that the base change of any morphism $f: \operatorname{Spec}(R) \rightarrow \mathcal{M}_{F G}$ against $c$ is affine and faithfully flat. First, assume that $f$ classifies a coordinatizable formal group and denote its associated formal group law by $F$. Let $\operatorname{Spec}(B)$ be some affine scheme. By definition, an element in $\operatorname{Spec}(R) \times_{\mathcal{M}_{F G}} \operatorname{Spec}(L)(\operatorname{Spec}(B))$ is a triple

$$
\left(g: R \rightarrow B, g^{\prime}: L \rightarrow B, \phi: f(g) \xrightarrow{\cong} c\left(g^{\prime}\right)\right)
$$

This data is equivalent to the datum of a morphism $g: R \rightarrow B$ and an isomorphism $\phi: g^{*}(F) \rightarrow G$ of formal group laws over $B$, where $G$ is any formal group law on $B$ (it corresponds to $g^{\prime}$ ). From the description of isomorphisms of formal group laws, we know that $\phi$ is just some formal power series with coefficients in $B$, zero constant term and invertible linear coefficient. Hence, the datum $(g: R \rightarrow B, \phi)$ is precisely a morphism $g^{\prime \prime}: R\left[a_{0}^{S}, a_{1}, a_{2}, \ldots\right] \rightarrow B$ i.e. an element in $\operatorname{Spec}\left(R\left[a_{0}^{S}, a_{1}, a_{2}, \ldots\right]\right)(B)$ (the morphism $g$ corresponds to $\left.g^{\prime \prime}\right]_{R}$ and the image of $a_{i}$ determines the $i^{\text {th }}$ coefficient of $\phi$ ). Summing up, we have shown that $\operatorname{Spec}(R) \times_{\mathcal{M}_{F G}} \operatorname{Spec}(L) \cong \operatorname{Spec}\left(R\left[a_{0}^{S}, a_{1}, a_{2}, \ldots\right]\right)$ and in particular that the base change of $f$ along $P$ is faithfully flat and affine.
Now, let $f^{\prime}: \operatorname{Spec}\left(R^{\prime}\right) \rightarrow \mathcal{M}_{F G}$ be a general morphism. By definition, every formal group is locally coordinatizable. In particular, there exists $\operatorname{Spec}(R)$ and an open immersion $i: \operatorname{Spec}(R) \rightarrow \operatorname{Spec}\left(R^{\prime}\right)$ such that $f^{\prime} \circ i$ classifies a coordinatizable formal group. Now one argues, as usual, from the following diagram using that faithfully flat and affine satisfy Zariski descent and that $c^{\prime \prime}$ has both these properties by the previous paragraph, to conclude that $c^{\prime}$ satisfies them as well
![img-33.jpeg](img-33.jpeg)

Hence, $\left(\mathcal{M}_{F G}, c\right)$ is a rigidified algebraic stack. By the same argument as above,

$$
\operatorname{Spec}(L) \times_{\mathcal{M}_{F G}} \operatorname{Spec}(L) \cong L\left[a_{0}^{ \pm}, a_{1}, a_{2}, \ldots\right]=W
$$

Finally, the proof of theorem 1.40 gives that $\left(\mathcal{M}_{F G}, c\right)$ is equivalent to the associated stack of the Hopf algebroid $(L, W)$.

The argument for $\mathcal{M}_{F G}^{s}$ is analogous except that now the pullback classifies strict isomorphisms i.e. $\operatorname{Spec}(R) \times_{\mathcal{M}_{F G}^{s}} \operatorname{Spec}(L) \cong \operatorname{Spec}\left(R\left[a_{1}, a_{2}, \ldots\right]\right)$. This is still faithfully flat and affine over $\operatorname{Spec}(R)$. Moreover,

$$
\operatorname{Spec}(L) \times_{\mathcal{M}_{F G}^{s}} \operatorname{Spec}(L) \cong L\left[a_{1}, a_{2}, \ldots\right] \cong M U_{*}(M U)
$$

Thus, by theorem 1.40, $\mathcal{M}_{F G}^{s} \cong\left[\left(M U_{*}, M U_{*}(M U)\right)\right]$ as claimed; for details see [18, Thm. 34].
Remark 1.69. It is because of this example that we defined an algebraic stack as only having a faithfully flat and not a smooth presentation, unlike what is often required in algebraic geometry as discussed in remark 1.19. For $\operatorname{Spec}(L) \rightarrow \mathcal{M}_{F G}$ to be smooth, is equivalent to requiring the left or right unit $\operatorname{Spec}(W) \rightarrow \operatorname{Spec}(L)$ to be smooth, in particular of finite type. But $W$ is an infinitely generated polynomial ring over an infinitely generated polynomial ring and hence the units have no chance to be of finite type.

For a general flat ring spectrum, it is very difficult to get a geometric description of its associated stack. As the proof of proposition 1.68 shows, if we have guessed a candidate for the geometric interpretation, it is not so hard to show it is the right one. However, guessing the candidate is complicated. In this case, we were only able to do so because we had a good understanding of the geometric interpretation of $\operatorname{Spec}(L)$, were able to calculate $M U_{*}$ and had the tools to show that $\mathcal{M}_{F G}$ was a stack in itself, without seeing it as associated to some Hopf algebroid.

Remark 1.70. In the proof of proposition 1.68 , we have used that any formal group is coordinatizable up to a Zariski (hence fpqc) cover. This is the geometric analog to the statement of proposition 1.36, that any morphism from an affine scheme to the stack $\left[\left(X_{0}, X_{1}\right)\right]$ factors locally through $X_{0}$. In particular, this shows that if the stack $\left[\left(E_{*}, E_{*}(E)\right)\right]$ associated to some flat ring spectrum $E$ was a moduli stack of something, this something must be objects that are locally isomorphic to those represented by $\operatorname{Spec}\left(E_{*}\right)$.

# 2 Constructing Spectra 

In this section, we attempt to construct homology theories from flat maps over a stack associated to some spectrum. The method generalises the approach taken in [15, Lect. 15, 16] to prove the Landweber exact functor theorem. Most of the results here are a rephrasing of the results in that reference to this more general setting. We have added a lot of detail and given special care to the grading issues. In subsection 2.1, we begin by further formal considerations to extract homology theories out of the formalism surrounding stacks. Then, in 2.2, we specialise to the case of the moduli stack of formal groups in which Landweber gave a verifiable criterion of the previous formal considerations. Subsection 2.3 is devoted to the proof of the Landweber exact functor theorem and in subsection 2.4 we apply the newly acquired knowledge to give a criterion for a map to be flat over the stack associated to $P(n)$.

### 2.1 Formal Considerations

Throughout this section, we fix some even homotopy commutative ring spectrum of Adams type $E$. From a graded ring homomorphism $f: E_{*} \rightarrow R$, we would like to recover a homology theory. A naïve try would be to consider the functor $h_{f}: h S p \rightarrow A b X \mapsto E_{*}(X) \otimes_{E_{*}} R$. Here we have used that $E_{*}(X)$ is always a graded $E_{*}$-module and $R$ is seen as $E_{*}$-module via $f$. The tensor product is that of the category of graded rings. We will denote it like the tensor product in Rings, hoping that it is clear from the context which is meant.

Lemma 2.1. With the notations as above, if the functor $-\otimes_{E_{*}} R: \operatorname{gr} E_{*} \operatorname{Mod} \rightarrow \operatorname{gr} A b$ is exact, the functor $h_{f}$ defines a homology theory.

Proof. As $E_{*}(-)$ is a homology theory, $h_{f}$ is automatically homotopy invariant and satisfies the wedge axiom. It remains to see that $h_{f}$ takes fiber sequences to long exact sequences. Consider a fiber sequence $X \rightarrow Y \rightarrow Z \rightarrow X[1]$. As $E_{*}(-)$ is a homology theory, the sequence

$$
E_{*}(X) \rightarrow E_{*}(Y) \rightarrow E_{*}(Z) \rightarrow E_{*}(X[1])=E_{*-1}(X)
$$

is an exact sequence of graded $E_{*}$-modules, i.e. it is exact in all degrees. By assumption, the sequence

$$
E_{*}(X) \otimes_{E_{*}} R \rightarrow E_{*}(Y) \otimes_{E_{*}} R \rightarrow E_{*}(Z) \otimes_{E_{*}} R \rightarrow E_{*}(X[1]) \otimes_{E_{*}} R
$$

is an exact sequence of graded abelian groups. In particular, the sequences

$$
\left(E_{*}(X) \otimes_{E_{*}} R\right)_{n} \rightarrow\left(E_{*}(Y) \otimes_{E_{*}} R\right)_{n} \rightarrow\left(E_{*}(Z) \otimes_{E_{*}} R\right)_{n} \rightarrow\left(E_{*}(X[1]) \otimes_{E_{*}} R\right)_{n}
$$

are exact for all $n$. Combining this with the observation that

$$
\left(E_{*}(X[1]) \otimes_{E_{*}} R\right)_{n}=\left(E_{*-1}(X) \otimes_{E_{*}} R\right)_{n}=\left(E_{*}(X[1]) \otimes_{E_{*}} R\right)_{n-1}
$$

yields the desired long exact sequence

$$
\cdots \rightarrow\left(E_{*}(Z) \otimes_{E_{*}} R\right)_{n+1} \rightarrow\left(E_{*}(X) \otimes_{E_{*}} R\right)_{n} \rightarrow\left(E_{*}(Y) \otimes_{E_{*}} R\right)_{n} \rightarrow\left(E_{*}(Z) \otimes_{E_{*}} R\right)_{n} \rightarrow\left(E_{*}(X) \otimes_{E_{*}} R\right)_{n-1} \rightarrow
$$

However, in general the functor $-\otimes_{E_{*}} R$ is not exact.
Example 2.2. 1. It is easy to cook up some examples where cofiber sequences are not carried to long exact sequences for $E=H \mathbb{Z}$. Consider for example the cofiber sequence $\mathbb{R} P^{1} \rightarrow \mathbb{R} P^{2} \rightarrow \mathbb{R} P^{2} / \mathbb{R} P^{1}$ and $f: \mathbb{Z} \rightarrow \mathbb{Z} / 2$ the quotient map. The cofiber sequence gives rise to a long exact sequence

$$
0=H_{2}\left(\mathbb{R} P^{2}\right) \longrightarrow \mathbb{Z}=H_{2}\left(\mathbb{R} P^{2} / \mathbb{R} P^{1}\right) \xrightarrow{2} \mathbb{Z}=H_{1}\left(\mathbb{R} P^{1}\right) \longrightarrow \mathbb{Z} / 2 \mathbb{Z} \longrightarrow 0 \longrightarrow \ldots
$$

Clearly, this sequence does not remain exact when applying $(-) \otimes_{\mathbb{Z}} \mathbb{Z} / 2 \mathbb{Z}$. However, one could argue that this is not a good example as $H \mathbb{Z}$ is not of Adams type. So let us examine another case.
2. Let $E=\mathbb{S}$ be the sphere spectrum and $\eta: \mathbb{S} \rightarrow H \mathbb{Z} / 2 \mathbb{Z}$ the unit map of the Eilenberg-Mac Lane spectrum $H \mathbb{Z} / 2 \mathbb{Z}$. Consider the graded ring map $f:=\pi_{*}(\eta): \pi_{*}(\mathbb{S}) \rightarrow \pi_{*}(H \mathbb{Z} / 2 \mathbb{Z})$. As $\pi_{*}(H \mathbb{Z} / 2 \mathbb{Z})$ is concentrated in degree 0 , this map is zero in all nonzero degrees and it is the quotient

map $\mathbb{Z} \rightarrow \mathbb{Z} / 2 \mathbb{Z}$ in degree zero. In particular, by definition of the graded tensor product, for any spectrum $X$ it holds that $\left(\mathbb{S}_{*}(X) \otimes_{\pi_{*}(\mathbb{S})} \mathbb{Z} / 2 \mathbb{Z}\right)_{n}=\mathbb{S}_{n}(X) \otimes_{\mathbb{Z}} \mathbb{Z} / 2 \mathbb{Z}$.
Consider the cofiber sequence $\mathbb{S} \xrightarrow{2} \mathbb{S} \rightarrow \mathbb{S} / 2$. Recall that $\pi_{2}(\mathbb{S} / 2) \cong \mathbb{Z} / 4 \mathbb{Z}$. The cofiber sequence yields the following long exact sequence on homotopy groups ( $\mathbb{S}$-homology):

$$
\ldots \longrightarrow \pi_{2}(\mathbb{S})=\mathbb{Z} / 2 \mathbb{Z} \xrightarrow{2=0} \mathbb{Z} / 2 \mathbb{Z} \longrightarrow \mathbb{Z} / 4 \mathbb{Z}=\pi_{2}(\mathbb{S} / 2) \longrightarrow \mathbb{Z} / 2 \mathbb{Z} \xrightarrow{0} \ldots
$$

However, the sequence

$$
\ldots \rightarrow\left(\mathbb{S}_{*}(\mathbb{S}) \otimes_{\pi_{*}(\mathbb{S})} \mathbb{Z} / 2 \mathbb{Z}\right)_{2} \xrightarrow{\mathrm{II}}\left(\mathbb{S}_{*}(\mathbb{S}) \otimes_{\pi_{*}(\mathbb{S})} \mathbb{Z} / 2 \mathbb{Z}\right)_{2} \rightarrow\left(\mathbb{S}_{*}(\mathbb{S} / 2) \otimes_{\pi_{*}(\mathbb{S})} \mathbb{Z} / 2 \mathbb{Z}\right)_{2} \rightarrow\left(\mathbb{S}_{*}(\mathbb{S}) \otimes_{\pi_{*}(\mathbb{S})} \mathbb{Z} / 2 \mathbb{Z}\right)_{1} \xrightarrow{\mathrm{II}} \ldots
$$

is not exact since, by the above discussion,

$$
\begin{gathered}
\left(\mathbb{S}_{*}(\mathbb{S}) \otimes_{\pi_{*}(\mathbb{S})} \mathbb{Z} / 2 \mathbb{Z}\right)_{2}=\mathbb{Z} / 2 \mathbb{Z} \otimes \mathbb{Z} / 2 \mathbb{Z}=\mathbb{Z} / 2 \mathbb{Z}=\left(\mathbb{S}_{*}(\mathbb{S}) \otimes_{\pi_{*}(\mathbb{S})} \mathbb{Z} / 2\right)_{1} \\
\left(\mathbb{S}_{*}(\mathbb{S} / 2) \otimes_{\pi_{*}(\mathbb{S})} \mathbb{Z} / 2 \mathbb{Z}\right)_{2}=\mathbb{Z} / 4 \mathbb{Z} \otimes \mathbb{Z} / 2 \mathbb{Z}=\mathbb{Z} / 2 \mathbb{Z}
\end{gathered}
$$

and $\mathbb{Z} / 2$ cannot be an extension of twice itself.
Of course, if $f$ is a flat morphism, $h_{f}$ will preserve exact sequences. For example, when $E=H \mathbb{F}_{p}$ or more generally $H k$ for $k$ any field, $h_{f}$ will always be a homology theory as all modules over a field are flat. On the other hand, the existence of $f: E_{*} \rightarrow R$ forces $R$ to be a $k$-vector space, so the homology theories we obtain will not be very interesting. By the universal coefficient theorem, $h_{f}$ will only be of the form $H_{*}\left(-, \oplus_{i} k\right)$. Moreover, in general, requiring flatness of a map is quite restrictive:

Proposition 2.3 ([22, Tag 00HD]). An $R$-module $M$ is flat if and only if, for every finitely generated ideal $I \subseteq R$, the map $I \otimes_{R} M \rightarrow M$ is injective.

For example when $E=M U$, we would need $R$ to be flat over the Lazard ring $L$, an infinitely generated polynomial ring. In view of proposition 2.3 , this would imply that $R$ itself is infinitely generated as for each $n$ the morphism $\left(x_{1}, \ldots, x_{n}\right) \otimes R \rightarrow R, x \otimes r \mapsto f(x) r$ must be injective, so, setting $r=1, f$ must be injective.
Hence, we wonder: is there a more general criterion for when the functor $h_{f}$ sends fiber sequences to long exact sequences? The key is to have another intense stare at our construction and to observe that $E_{*}(X)$ has more structure than just that of an $E_{*}$-module, it is a so-called $\left(E_{*}, E_{*}(E)\right)$-comodule.

Definition 2.4. Let $(A, \Gamma)$ be a Hopf algebroid. A right $(A, \Gamma)$-comodule is a right $A$-module $M$ together with a right $A$-linear map $\rho: M \rightarrow M \otimes_{A, \eta_{L}} \Gamma$ that is counital, meaning that $(M \otimes \epsilon) \circ \rho=i d_{M}$, and coassociative i.e. $(M \otimes \psi) \circ \rho=(\rho \otimes \Gamma) \circ \rho$.
There is an obvious analogue for left $(A, \Gamma)$-comodule.
If $(A, \Gamma)$ is a graded Hopf algebroid, one can make sense of a graded $(A, \Gamma)$-comodule. This is a graded $A$-module $M$ such that the map $\rho$ is graded (now the tensor product is graded as well).

Proposition 2.5 ([19, Prop. 2.2.8]). Let $E$ be a spectrum of Adams type. Then E-homology is a functor to the category of graded $\left(E_{*}, E_{*}(E)\right)$-comodules.

Proof. In the proof of lemma 1.48, we constructed, for all spectra $X$, a natural isomorphism

$$
\varphi_{X}: E_{*}(X) \otimes_{E_{*}} E_{*}(E) \rightarrow \pi_{*}(X \otimes E \otimes E)
$$

Let $\eta_{E}$ denote the unit map of $E$. One checks that the map

$$
\rho_{X}: E_{*}(X)=\pi_{*}(X \otimes E) \xrightarrow{X \otimes \eta_{E} \otimes E} \pi_{*}(X \otimes E \otimes E) \xrightarrow{\varphi_{X}^{-1}} E_{*}(X) \otimes_{E_{*}} E_{*}(E)
$$

is graded, counital and coassociative and endows $E_{*}(X)$ with the desired comodule structure. This is an analogous argument to that of 1.49 , for details see the discussion and reference given there. By naturality, this construction is functorial.

Hence, to understand when the assignment $X \mapsto E_{*}(X) \otimes_{E_{*}} R$ defines a homology theory, we need to answer the following question:

Question 2.6. Given a graded ring map $f: E_{*} \rightarrow R$, when is the functor $-\otimes_{E_{*}} R: g r\left(E_{*}, E_{*}(E)\right)$ comod $\rightarrow$ $g r A b$ exact?

The answer will have a nice phrasing in terms of stacks. In order to make sense of this interpretation however, we first need to get rid of the graded categories. This is a step that is usually glossed over in the literature. We present the details to ideas hinted at in [16, Sec. 4]. For this, we will work in the generality of evenly graded Hopf algebroids.

Proposition 2.7. Let $(A, \Gamma)$ be an evenly graded Hopf algebroid. The functor $U$ from lemma 1.62 induces an equivalence of categories between the category of evenly graded $(A, \Gamma)$-comodules and (ungraded) $\left(A, \Gamma\left[u^{ \pm}\right]\right)$-comodules.

For the proof, we need the following easy lemma.
Lemma 2.8. Let $A=\left\{A_{j}\right\}_{j \in \mathbb{Z}}$ be a graded ring and let $M=\left\{M_{i}\right\}_{i \in \mathbb{Z}}$ and $\Gamma=\left\{\Gamma_{k}\right\}_{k \in \mathbb{Z}}$ be graded $\left\{A_{j}\right\}_{j \in \mathbb{Z}}$-modules. Then there is an isomorphism $\oplus_{h \in \mathbb{Z}}\left(M \hat{\otimes}_{A} \Gamma\right)_{h} \cong\left(\oplus_{i \in \mathbb{Z}} M_{i}\right) \otimes_{\oplus_{j \in \mathbb{Z}} A_{j}}\left(\oplus_{k \in \mathbb{Z}} \Gamma_{k}\right)$ where $\hat{\otimes}$ denotes the tensor product of graded rings.

Proof. By definition $\left(M \hat{\otimes}_{A} \Gamma\right)_{h}=\oplus_{i+k=h} M_{i} \otimes_{\mathbb{Z}} \Gamma_{k} /\left\langle a m \otimes \gamma-m \otimes a \gamma| | a|+|m|+|\gamma|=h\right\rangle$. Observe that the ideals

$$
\left\langle a m \otimes \gamma-m \otimes a \gamma \mid a \in \oplus_{j \in \mathbb{Z}} A_{j} m \in \oplus_{i \in \mathbb{Z}} M_{i}, \gamma \in \oplus_{k \in \mathbb{Z}} \Gamma_{k}\right\rangle
$$

and

$$
\left\langle a m \otimes \gamma-m \otimes a \gamma \mid a \in A_{j} \text { for some } j, m \in M_{i} \text { for some } i, \gamma \in \Gamma_{k} \text { for some } k\right\rangle
$$

coincide as the second is generated by a set of generators for the first. Thus

$$
\begin{aligned}
& \left(\oplus_{i \in \mathbb{Z}} M_{i}\right) \otimes_{\oplus_{j \in \mathbb{Z}} A_{j}}\left(\oplus_{k \in \mathbb{Z}} \Gamma_{k}\right) \\
& \cong\left(\oplus_{i \in \mathbb{Z}} M_{i}\right) \otimes_{\mathbb{Z}}\left(\oplus_{k \in \mathbb{Z}} \Gamma_{k}\right) /\left\langle a m \otimes \gamma-m \otimes a \gamma \mid a \in \oplus_{j \in \mathbb{Z}} A_{j} m \in \oplus_{i \in \mathbb{Z}} M_{i}, \gamma \in \oplus_{k \in \mathbb{Z}} \Gamma_{k}\right\rangle \\
& =\left(\oplus_{i \in \mathbb{Z}} M_{i}\right) \otimes_{\mathbb{Z}}\left(\oplus_{k \in \mathbb{Z}} \Gamma_{k}\right) /\left\langle a m \otimes \gamma-m \otimes a \gamma \mid a \in A_{j} \text { for some } j, m \in M_{i} \text { for some } i, \gamma \in \Gamma_{k} \text { for some } k\right\rangle
\end{aligned}
$$

Reordering the terms and pulling out the sums one gets

$$
\left(\oplus_{i \in \mathbb{Z}} M_{i}\right) \otimes_{\oplus_{j \in \mathbb{Z}} A_{j}}\left(\oplus_{k \in \mathbb{Z}} \Gamma_{k}\right) \cong \oplus_{h \in \mathbb{Z}}\left(\oplus_{i+k=h} M_{i} \otimes_{\mathbb{Z}} \Gamma_{k} /\left\langle a m \otimes \gamma-m \otimes a \gamma| | a|+|m|+|\gamma|=h\right\rangle\right)
$$

The left hand side is precisely $\oplus_{h \in \mathbb{Z}}\left(M \hat{\otimes}_{A} \Gamma\right)_{h}$ which proves the lemma.
Proof of proposition 2.7. First we simplify indexing via the equivalence of categories between the categories of evenly graded $(A, \Gamma)$-comodules and that of commutative graded $(A, \Gamma)$-comodules given by multiplying and dividing the degree by 2 . By category of commutative graded $(A, \Gamma)$-comodules we mean the category whose objects are graded $(A, \Gamma)$-comodules which are strictly commutative and not in the graded sense. We will denote it by $\operatorname{Cgdd}(A, \Gamma)$ comod.
We define a functor

$$
F: \operatorname{Cgdd}(A, \Gamma) \operatorname{comod} \rightarrow\left(A, \Gamma\left[u^{ \pm}\right]\right) \text { comodules }
$$

on objects as follows. Let $\left\{M_{i}\right\}_{i \in \mathbb{Z}}$ be a commutative graded $\left(\left\{A_{j}\right\}_{j},\left\{\Gamma_{k}\right\}_{k}\right)$-comodule. Then, set

$$
F\left(\left\{M_{i}\right\}_{i \in \mathbb{Z}}\right)=\oplus_{i} M_{i}
$$

To see that this is a $\left(\oplus_{j} A_{j},\left(\oplus_{k} \Gamma_{k}\right)\left[u^{ \pm}\right]\right)$-comodule, we need to describe the map

$$
\rho_{\oplus_{i} M_{i}}: \oplus_{i} M_{i} \rightarrow\left(\oplus_{i} M_{i}\right) \otimes_{\left(\oplus_{j} A_{j}\right)}\left(\oplus_{k} \Gamma_{k}\right)\left[u^{ \pm}\right]
$$

By lemma 2.8, there is an isomorphism $\left(\oplus_{i} M_{i}\right) \otimes_{\left(\oplus_{j} A_{j}\right)}\left(\oplus_{k} \Gamma_{k}\right)\left[u^{ \pm}\right] \cong\left(\oplus_{h}\left(M \hat{\otimes}_{A} \Gamma\right)_{h}\right)\left[u^{ \pm}\right]$. As $\left\{M_{i}\right\}_{i \in \mathbb{Z}}$ is a commutative graded $\left(\left\{A_{j}\right\}_{j},\left\{\Gamma_{k}\right\}_{k}\right)$-comodule, there is a counital map $\rho_{i}: M_{i} \rightarrow\left(M \hat{\otimes}_{A} \Gamma\right)_{i}$. Define $\rho_{\oplus_{i} M_{i}}$ as the map characterised by mapping $m_{i} \in M_{i}$ to $\rho_{i}\left(m_{i}\right) u^{i}$. This is counital by construction as $\rho_{i}$ is. On morphisms, $F$ is also given by taking direct sums and one easily verifies that this construction is functorial.
Conversely, let us define the functor

$$
G:\left(A, \Gamma\left[u^{ \pm}\right]\right) \operatorname{comod} \rightarrow \operatorname{Cgdd}(A, \Gamma) \text { comod }
$$

Given a $\left(\oplus_{j} A_{j},\left(\oplus_{k} \Gamma_{k}\right)\left[u^{ \pm}\right]\right)$-comodule $\tilde{M}$, define

$$
G(\tilde{M})_{i}:=\rho_{M}^{-1}\left(\left(\tilde{M} \otimes_{\left(\oplus_{j} A_{j}\right)}\left(\oplus_{k} \Gamma_{k}\right)\right)\left\langle u^{i}\right\rangle\right)
$$

To define the morphism $\rho_{G(\tilde{M})_{i}}: G(\tilde{M})_{i} \rightarrow\left(G(\tilde{M}) \hat{\otimes}_{A} \Gamma\right)_{i}$, we need to use the fact that $\tilde{M} \cong \oplus_{i} G(\tilde{M})_{i}$. We will show this at the end of the proof when showing that $G \circ F \simeq i d_{\left(A, \Gamma\left[u^{\pm}\right]\right) \text { comod }}$; the isomorphisms are given by $\alpha$ and $\beta$ defined there. Using this and lemma 2.8 again, we have

$$
\rho_{\tilde{M}}: G(\tilde{M})_{i} \rightarrow\left(\tilde{M} \otimes_{\left(\oplus_{j} A_{j}\right)}\left(\oplus_{k} \Gamma_{k}\right)\right)\left\langle u^{i}\right\rangle \cong \oplus_{h}(G(\tilde{M}) \hat{\otimes}_{A} \Gamma)_{h}\left\langle u^{i}\right\rangle
$$

which we can postcompose with the projection to $\left(G(\tilde{M}) \hat{\otimes}_{A} \Gamma\right)_{i}$ extended by sending $u^{i}$ to 1 to define $\rho_{G(\tilde{M})_{i}}$. Doing this for all $i \in \mathbb{Z}$ defines an evenly graded $(A, \Gamma)$-comodule $G(\tilde{M})$ (exploiting the fact that $\rho_{\tilde{M}}$ is counital). Again, one easily verifies that this is functorial.
These functors define an equivalence of categories. Given an evenly graded $\left(\left\{A_{j}\right\}_{j},\left\{\Gamma_{k}\right\}_{k}\right)$-comodule $\left\{M_{i}, \rho_{i}\right\}_{i \in \mathbb{Z}}$, it holds that

$$
G \circ F\left(\left\{M_{i}\right\}_{i \in \mathbb{Z}}\right)=\left\{\rho_{\oplus_{i} M_{i}}^{-1}\left(\left(\oplus_{i} M_{i}\right) \otimes_{\left(\oplus_{j} A_{j}\right)}\left(\oplus_{k} \Gamma_{k}\right)\left\langle u^{i}\right\rangle\right)\right\}_{i}
$$

By construction,

$$
\rho_{\oplus_{i} M_{i}}^{-1}\left(\left(\oplus_{i} M_{i}\right) \otimes_{\left(\oplus_{j} A_{j}\right)}\left(\oplus_{k} \Gamma_{k}\right)\left\langle u^{i}\right\rangle\right)=\rho_{i}^{-1}\left(\left(M \hat{\otimes}_{A} \Gamma\right)_{i}\right)=M_{i}
$$

as desired. It is easy to check from the definitions that the comodule structure also remains the same and thus $G \circ F=i d_{C g d d(A, \Gamma) \text { comod }}$.
For a $\left(\oplus_{j} A_{j},\left(\oplus_{k} \Gamma_{k}\right)\left[u^{\pm}\right]\right)$-comodule $(\tilde{M}, \rho)$, observe that $F \circ G(\tilde{M})=\bigoplus_{i}\left\{\rho^{-1}\left(\tilde{M} \otimes_{A} \Gamma\left\langle u^{i}\right\rangle\right)\right\}$. We claim that this is naturally isomorphic to $\tilde{M}$. Define

$$
\alpha: \tilde{M} \rightarrow \bigoplus_{i}\left\{\rho^{-1}\left(\tilde{M} \otimes_{A} \Gamma\left\langle u^{i}\right\rangle\right)\right\} \text { by } \alpha(m)=\left(i d_{M} \otimes \epsilon^{(A, \Gamma)}\left(\rho(m)_{i}\right)\right)_{i}
$$

where $\rho(m)_{i}$ denotes the coefficient of $u^{i}$ in $\rho(m)$. This is well-defined if

$$
i d_{M} \otimes \epsilon^{(A, \Gamma)}\left(\rho(m)_{i}\right) \in \rho^{-1}\left(\tilde{M} \otimes_{A} \Gamma\left\langle u^{i}\right\rangle\right)
$$

which is ensured by coassociativity. Indeed, coassociativity (used in the third equality) implies that for $m \in \tilde{M}$,

$$
\begin{aligned}
\left(\rho \otimes \Gamma\left[u^{\pm}\right]\right) \circ \rho(m) & =\left(\rho \otimes \Gamma\left[u^{\pm}\right]\right)\left(\Sigma_{i} m_{i} u^{i}\right) \\
& =\Sigma_{i} \rho \otimes \Gamma\left[u^{\pm}\right]\left(m_{i}\right) u^{i} \\
& =\left(i d_{M} \otimes \psi^{U(A, \Gamma)}\right) \circ \rho(m) \\
& =\Sigma_{i}\left(i d_{M} \otimes \psi^{(A, \Gamma)}\right)\left(m_{i}\right) v^{i} u^{i}
\end{aligned}
$$

Matching the degrees, one finds that

$$
\rho \otimes i d_{\Gamma\left[u^{\pm}\right]}\left(m_{i}\right)=\left(i d_{M} \otimes \psi^{(A, \Gamma)}\right)\left(m_{i}\right) v^{i}
$$

As $\rho \otimes_{A} i d_{\Gamma}$ endows $\tilde{M} \otimes_{A} \Gamma$ with a $\left(A, \Gamma\left[u^{\pm}\right]\right)$-comodule structure and $i d_{\tilde{M}} \otimes \epsilon^{(A, \Gamma)}$ is then a morphism of $\left(A, \Gamma\left[u^{\pm}\right]\right)$-comodules, the following diagram commutes:

$$
\begin{aligned}
& \tilde{M} \otimes_{A} \Gamma \xrightarrow{\rho \otimes i d_{\Gamma}} \tilde{M} \otimes_{A} \Gamma\left[v^{\pm}\right] \otimes_{A} \Gamma \\
& i d_{M} \otimes \epsilon^{(A, \Gamma)} \downarrow \quad \downarrow i d_{\tilde{M} \otimes_{A} \Gamma\left[v^{\pm}\right]} \otimes \epsilon^{(A, \Gamma)} \\
& \tilde{M} \otimes_{A} A \longrightarrow \rho \tilde{M} \otimes_{A} \Gamma\left[v^{\pm}\right] .
\end{aligned}
$$

Thus,
$\rho\left(\left(i d_{M} \otimes \epsilon^{(A, \Gamma)}\right)\left(\rho(m)_{i}\right)\right)=\left(i d_{\tilde{M} \otimes_{A} \Gamma\left[v^{\pm}\right]} \otimes \epsilon\right) \circ\left(\rho \otimes i d_{\Gamma}\right)\left(\rho(m)_{i}\right)=i d_{\tilde{M} \otimes_{A} \Gamma\left[v^{\pm}\right]} \otimes \epsilon\left(i d_{M} \otimes \psi^{(A, \Gamma)}\left(\rho(m)_{i}\right) v^{i}\right)=\rho(m)_{i} v^{i}$ as needed for well-definedness.
We conclude by constructing an inverse to $\alpha$ to prove the claim. Let $\beta: \oplus_{i}\left\{\rho^{-1}\left(\tilde{M} \otimes_{A} \Gamma\left\langle u^{i}\right\rangle\right)\right\} \rightarrow \tilde{M}$ denote the summing map. Counitality of $\rho$ and linearity of all the involved maps gives that

$$
\beta \circ \alpha(m)=\left(i d_{M} \otimes \epsilon^{U(A, \Gamma)}\right) \circ \rho(m)=m
$$

To show that $\alpha \circ \beta=i d_{\bigoplus_{i}\left\{\rho^{-1}\left(i d_{\tilde{M} \otimes_{A} \Gamma}\left\langle u^{i}\right\rangle\right)\right\}}$, observe that for an element $\left(m_{i}\right)_{i} \in \bigoplus_{i}\left\{\rho^{-1}\left(\tilde{M} \otimes_{A} \Gamma\left\langle u^{i}\right\rangle\right)\right\}$ it holds by definition that $\rho\left(m_{i}\right)=\tilde{m}_{i} u^{i}$ for some $\tilde{m}_{i} \in \tilde{M} \otimes_{A} \Gamma$. In particular, $\rho\left(\Sigma_{i} m_{i}\right)_{i}=\tilde{m}_{i}$. Hence,

$$
\alpha \circ \beta\left(\left(m_{i}\right)_{i}\right)=\left(i d_{\tilde{M}} \otimes \epsilon\right)\left(\rho\left(\Sigma_{i} m_{i}\right)_{i}\right)=\left(i d_{\tilde{M}} \otimes \epsilon^{U(A, \Gamma)}\right)\left(\rho\left(m_{i}\right)\right)\right)_{i}=\left(m_{i}\right)_{i}
$$

where the last equality is by counitality. One verifies that this isomorphism is natural and compatible with the comodule structure. Hence, $F \circ G$ is naturally isomorphic to $i d_{(A, \Gamma\left[u^{\pm}\right]) \text { comod }}$.

Thus, going back to question 2.6 , we can see any graded $\left(E_{*}, E_{*}(E)\right)$-comodule $M$ as two ungraded $\left(E_{*}, E_{*}(E)\left[u^{ \pm}\right]\right)$-comodules $M_{\text {even }}$ and $M_{\text {odd }}$ corresponding to the evenly and oddly graded parts of $M$. Then, it suffices to understand exactness for these two.
The category of ungraded $\left(E_{*}, E_{*}(E)\left[u^{ \pm}\right]\right)$-comodules has a nice interpretation in terms of certain sheaves on the associated stack. The precise statement is proposition 2.13. Before stating it, we need to introduce those sheaves. We present this in the general setting for an algebraic stack $\mathcal{X}$ with presentation $P$ : $\operatorname{Spec}(A) \rightarrow \mathcal{X}$ and associated Hopf algebroid $[(A, \Gamma)]$. We will keep this notation throughout the section.

Definition 2.9 ([15, Lect. 15, Def. 1]). A quasi-coherent sheaf on $\mathcal{X}$ is a rule which specifies, for every morphism $\eta: \operatorname{Spec}(R) \rightarrow \mathcal{X}$, an $R$-module $M(\eta)$. This rule is required to be functorial in the following sense: given a homomorphism $f: \operatorname{Spec}\left(R^{\prime}\right) \rightarrow \operatorname{Spec}(R)$ and $\eta^{\prime}: \operatorname{Spec}\left(R^{\prime}\right) \rightarrow \mathcal{X}$ such that $\eta \circ f \simeq \eta^{\prime}$, we have a canonical isomorphism $M\left(\eta^{\prime}\right) \cong M(\eta) \otimes_{R} R^{\prime}$.

We denote the category of quasi-coherent sheaves on $\mathcal{X}$ by $Q \operatorname{Coh}(\mathcal{X})$.
Remark 2.10. A quasicoherent sheaf $\mathcal{F}$ is entirely determined by its values on morphisms

$$
x: \operatorname{Spec}(S) \rightarrow \operatorname{Spec}(A) \xrightarrow{P} \mathcal{X}
$$

that factor through $\operatorname{Spec}(A)$. Indeed, by proposition 1.36 , for any morphism $y: \operatorname{Spec}(R) \rightarrow[(A, \Gamma)]$ there exists a faithfully flat cover $f: \operatorname{Spec}(S) \rightarrow \operatorname{Spec}(R)$ such that $y \circ f$ factors through $\operatorname{Spec}(A)$. The value of $\mathcal{F}(y)$ is then defined by $\mathcal{F}(x)$ and quasicoherence.

Evaluating quasicohenrent sheaves over $\mathcal{X}$ at a map $q: \operatorname{Spec}(R) \rightarrow \mathcal{X}$ defines a functor

$$
q^{*}: Q \operatorname{Coh}(\mathcal{X}) \rightarrow Q \operatorname{Coh}(\operatorname{Spec}(R)) \cong \operatorname{Mod}_{R}
$$

This functor has a right adjoint $q_{*}: \operatorname{Mod}_{R} \rightarrow Q \operatorname{Coh}(\mathcal{X})$. In concrete terms, for an $R$-module $N, q_{*}(N)$ is the quasi-coherent sheaf on $\mathcal{X}$ defined on morphisms $p: \operatorname{Spec}(S) \xrightarrow{P} \mathcal{X}$ by the formula $q_{*}(N)(p)=N \otimes_{R} B$, where $B$ is given by the pullback
![img-34.jpeg](img-34.jpeg)

The $S$-module structure on $q_{*}(N)(p)=N \otimes_{R} B$ is induced by $\pi_{S}$. By remark 2.10, this suffices to define $q_{*}(N)$.

Remark 2.11. If $q$ factors through $P$, there could a priori be two $A$-module structures on $q_{*}(N)(P)=$ $N \otimes_{R} B=N \otimes_{R} R \otimes_{A, s} \Gamma$ coming from the source and target maps between $A$ and $\Gamma$. It is important that we apply the above construction carefully and endow $q_{*}(N)(P)$ with the module structure coming from $\pi_{A}$, i.e. the map that we did not use to tensor over. More about this subtlety is explained around remark 2.25 .
![img-35.jpeg](img-35.jpeg)

Definition 2.12. A sequence of quasicoherent sheaves on $\mathcal{X}$ is called exact if it is exact when pulled back to $A$ via $P^{*}$.

The quasicoherent sheaves on $\mathcal{X}$ correspond to comodules on its associated Hopf algebroid.
Proposition 2.13 ([8, Thm. 2.2]). Let $(A, \Gamma)$ be an (ungraded) Hopf algebroid. There is an equivalence of categories between $(A, \Gamma)$-comodules and quasicoherent sheaves over $[(A, \Gamma)]$.

Proof. We only give the construction and the main ideas to define the structure maps. For a detailed proof see [8, Thm. 2.2] and [7, Ex. 1.12]. Let $M$ be an $(A, \Gamma)$-comodule. By remark 2.10, to define a quasicoherent sheaf $\mathcal{F}_{M}$ associated to $M$, it is enough to give its values on morphisms $x: \operatorname{Spec}(S) \rightarrow$

$\operatorname{Spec}(A) \xrightarrow{\text { can }}[(A, \Gamma)]$ that factor through $\operatorname{Spec}(A)$. Given $x: \operatorname{Spec}(S) \rightarrow[(A, \Gamma)]$ factoring through $\operatorname{Spec}(A)$, we define $\mathcal{F}_{M}(x):=M \otimes_{A} S$. To define the structure maps witnessing quasicoherence, observe that a 2 -commutative diagram
![img-36.jpeg](img-36.jpeg)
with $x, y$ both factoring through $\operatorname{Spec}(A)$ yields the dashed arrow $\phi$ in
![img-37.jpeg](img-37.jpeg)

This diagram corresponds to
![img-38.jpeg](img-38.jpeg)

In particular, this gives rise to a morphism $\alpha$ in the following diagram:
![img-39.jpeg](img-39.jpeg)

Now, we define the structure map $\mathcal{F}_{M}(R, y) \rightarrow \mathcal{F}_{M}(S, x)$ as

$$
R \otimes_{A} M \xrightarrow{R \otimes_{P}} R \otimes_{A} M \otimes_{A} \Gamma \xrightarrow{\alpha \otimes M} S \otimes_{A} M
$$

which induces the desired isomorphism $\mathcal{F}_{M}(R, y) \otimes_{R} S \rightarrow \mathcal{F}_{M}(S, x)$.
Conversely, given a quasicoherent sheaf $\mathcal{F}$ over $[(A, \Gamma)]$, one obtains an $A$-module

$$
M:=\mathcal{F}(\text { can }: A \rightarrow[(A, \Gamma)])
$$

This has an $(A, \Gamma)$-comodule structure via the composition $M \rightarrow M \otimes_{A, \eta_{L}} \Gamma \simeq \mathcal{F}(\operatorname{can} \circ s) \simeq \mathcal{F}(\operatorname{can} \circ t)$ where the first equivalence is quasicoherence and the second comes from the fact that can $\circ t$ and can $\circ s$ are isomorphic. It is shown in [8, Thm. 2.2] that this makes $M$ into an $(A, \Gamma)$-comodule.
We roughly check that these two constructions are inverses. The reader is invited to refer to the references to see that the structure maps also agree. Given an $(A, \Gamma)$-comodule $M$, observe that $\mathcal{F}_{M}(\text { can })=A \otimes_{A} M$. For a quasicoherent sheaf $\mathcal{G}$, it holds that

$$
\left.\mathcal{F}_{\mathcal{G}(\text { can })}(x: \operatorname{Spec}(R) \rightarrow[(A, \Gamma)])=R \otimes_{A} \mathcal{G}(\text { can }) \simeq \mathcal{G}(\text { can } \circ \tilde{x})=\mathcal{G}(x)\right)
$$

where the last equality comes from quasicoherence.
Remark 2.14. There is another more conceptual approach to the proof of this proposition which uses the fact that the presentation $\operatorname{Spec}(A) \rightarrow[(A, \Gamma)]$ is affine, hence quasicompact and is thus of so-called effective cohomological descent (see [13, Thm 13.5.5,i] for a definition and a proof). One can show that this implies that $P^{*}$ induces an equivalence $P^{*}: Q \operatorname{Coh}([(A, \Gamma)]) \rightarrow\left\{\operatorname{Mod}\left(\mathcal{O}_{A}\right)\right.$ + descent data $\}$ (see [18, Sec. 3.4]). Given an $A$-module $M$, this descent data is an isomorphism $\alpha: s^{*}(M) \rightarrow t^{*}(M)$ which by adjunction corresponds to some map $\psi_{l}: M \rightarrow s_{*} t^{*} M$. This is precisely the structure map constructed in the previous proof.

Now going back to the setting of question 2.6 , by construction, for the quasicoherent sheaf $\mathcal{F}_{A}$ corresponding to a $\left(E_{*}, E_{*}(E)\left[u^{ \pm}\right]\right)$-comodule $A$, it holds that $f^{*}\left(\mathcal{F}_{A}\right)=A \otimes_{E_{*}} R$. Moreover, by the definition of exactness in $Q \operatorname{Coh}\left(\left[\left(E_{*}, E_{*}(E)\right)\right]\right)$, a sequence of $\left(E_{*}, E_{*}(E)\left[u^{ \pm}\right]\right)$-comodules is exact if and only if the corresponding sequence of quasicoherent sheaves is exact. Hence, to answer question 2.6, it suffices to find a criterion under which exactness of the functor $f^{*}: Q \operatorname{Coh}\left(\left[\left(E_{*}, E_{*}(E)\left[u^{ \pm}\right]\right]\right) \rightarrow A b\right.$ is guaranteed. Exactness of $f^{*}$ will be related to the concept of flatness of quasicoherent sheaves which we introduce now, again in the broader generality of the algebraic stack $\mathcal{X}$.

Definition 2.15. A quasi-coherent sheaf $M$ on $\mathcal{X}$ is (faithfully) flat if, for every $\eta: \operatorname{Spec}(R) \rightarrow \mathcal{X}$, the $R$-module $M(\eta)$ is (faithfully) flat over $R$.

Let us recall a few basics from commutative algebra:
Lemma 2.16 ([22, Tag 00HI]). Let $M$ be an $R$-module and consider a ring map $f: R \rightarrow S$. Then, if $M$ is (faithfully) flat, $M \otimes_{R} S$ is a (faithfully) flat $S$-module.

Lemma 2.17 ([22, Tag 00HJ]). Let $R \rightarrow S$ be a faithfully flat ring map. Then an $R$-module $M$ is flat if and only if $M \otimes_{R} S$ is a flat $S$-module.

Lemma 2.18 ([22, Tag 0584]). Let $R$ be a ring. Let $S \rightarrow S^{\prime}$ be a flat map of $R$-algebras. Let $M$ be a module over $S$ and set $M^{\prime}=S^{\prime} \otimes_{S} M$. Then,

1. If $M$ is flat over $R$, then $M^{\prime}$ is flat over $R$.
2. If $S \rightarrow S^{\prime}$ is faithfully flat, then $M$ is flat over $R$ if and only if $M^{\prime}$ is flat over $R$.

Remark 2.19. Observe that $M \in Q \operatorname{Coh}(\mathcal{X})$ is flat if and only if $M(P)$ is a flat $A$-module. To prove this claim, we need to show that, if $M(P)$ is a flat $A$-module, the $R$-module $M(x: \operatorname{Spec}(R) \rightarrow \mathcal{X})$ is flat for any ring $R$ and any morphism $x$. First, consider a morphism $y: \operatorname{Spec}(S) \xrightarrow{g} \operatorname{Spec}(A) \xrightarrow{f} \mathcal{X}$ factoring through $\operatorname{Spec}(A)$. Then $M(y)$ is a flat $S$-module as, by quasicoherence, $M(y) \cong M(P) \otimes_{A} S$ and by lemma 2.16 the latter is a flat $S$-module. For a general morphism $x: \operatorname{Spec}(R) \rightarrow \mathcal{X}$, there exists a faithfully flat cover $f: \operatorname{Spec}(S) \rightarrow \operatorname{Spec}(R)$ such that $x \circ f$ factors through $\operatorname{Spec}(A)$. By the previous case $M(x \circ f)$ is flat if $M(P)$ is and by quasicoherence, $M(x \circ f) \cong M(x) \otimes_{R} S$. As $R \rightarrow S$ is faithfully flat, one concludes by lemma 2.17 that $M(x)$ is flat as well.

In fact, the specific presentation we chose does not matter:
Proposition 2.20. Let $\mathcal{X}$ be any algebraic stack and let $q: \operatorname{Spec}(S) \rightarrow \mathcal{X}$ be faithfully flat and affine. Then, $M \in Q \operatorname{Coh}(\mathcal{X})$ is flat if and only if $q^{*}(M)$ is a flat $S$-module.

Proof. The "only if" direction is straightforward from the definition of flat quasicoherent sheaves on a stack. For the other direction, assume $M \in Q \operatorname{Coh}(\mathcal{X})$ is such that $q^{*}(M)$ is flat. By definition, we need to show that given any morphism $f: \operatorname{Spec}(R) \rightarrow \mathcal{X}, f^{*}(M)$ is a flat $R$-module. Consider the following pullback square
![img-40.jpeg](img-40.jpeg)

Since $q$ is faithfully flat, so is $q^{\prime}$ i.e. $B$ is a faithfully flat $R$-module. Hence, in view of lemma 2.17, $f^{*}(M)$ is flat if and only if $f^{*}(M) \otimes_{R} B$ is a flat $B$-module. Since $M$ is quasicoherent and the diagram commutative, observe that $f^{*}(M) \otimes_{R} B \cong M\left(f \circ q^{\prime}\right)=M\left(q \circ f^{\prime}\right) \cong q^{*}(M) \otimes_{S} B$. Thus, it suffices to show that $q^{*}(M) \otimes_{S} B$ is a flat $B$-module. This is a direct consequence of the assumption and lemma 2.16 .

We can also make sense of what it means for a module to be flat over a stack:
Definition 2.21. Given $q: \operatorname{Spec}(R) \rightarrow \mathcal{X}$, we say that an $R$-module $N$ is flat (or faithfully flat) over $\mathcal{X}$ if $q_{*}(N)$ is a flat (or faithfully flat) quasi-coherent sheaf on $\mathcal{X}$.

As a quick sanity check, consider the following:
Proposition 2.22. A morphism $q: \operatorname{Spec}(R) \rightarrow \mathcal{X}$ is flat in the sense of definition 1.13 if and only if the $R$-module $R$ is flat over $\mathcal{X}$ (with respect to $q$ ) in the sense just defined.

Proof. Recall that we had set $\operatorname{Spec}(\Gamma):=\operatorname{Spec}(A) \times_{\mathcal{X}} \operatorname{Spec}(A)$. By corollary 1.38 , the morphism $q$ is flat in the sense of definition 1.13 if and only if its base change $q^{\prime}: \operatorname{Spec}\left(R \otimes_{A} \Gamma\right) \rightarrow \operatorname{Spec}(A)$ is flat
![img-41.jpeg](img-41.jpeg)

In other words, $q$ is flat if and only if $R \otimes_{A} \Gamma$ is a flat $A$-module. Observe that $R \otimes_{A} \Gamma=q_{*}(R)(P)$. We conclude as, by remark 2.19, flatness of $q_{*}(R)(P)$ as an $A$-module is equivalent to flatness of the quasicoherent sheaf $q_{*}(R)$, i.e. to flatness of $R$ over $\mathcal{X}$ as $R$-module.

We have already encountered the following result, but it will be so important for what follows that we grant it the status of a lemma.

Lemma 2.23. Consider a morphism $q: \operatorname{Spec}(R) \rightarrow \operatorname{Spec}(A) \xrightarrow{P} \mathcal{X}$ and an $R$-module $N$. Then, $N$ is flat over $\mathcal{X}$ if and only if $q_{*}(N)(P)=N \otimes_{R}\left(R \otimes_{A, s} \Gamma\right)=N \otimes_{A, s} \Gamma$, seen as an $A$-module via $t: A \rightarrow \Gamma$, is flat. Here $s$ and $t$ denote the source and target maps of the Hopf algebroid $(A, \Gamma)$.

Proof. This is clear from the definitions and remark 2.19.
Flatness of a module over a stack can be checked locally.
Lemma 2.24. Let $q: \operatorname{Spec}(R) \rightarrow \mathcal{X}$ be a morphism that does not factor through $\operatorname{Spec}(A)$. Let $N$ be an $R$-module and $f: \operatorname{Spec}(S) \rightarrow \operatorname{Spec}(R)$ be a faithfully flat cover such that $q \circ f$ factors through $\operatorname{Spec}(A)$. Then, the $R$-module $N$ is flat over $\mathcal{X}$ if and only if the $S$-module $N \otimes_{R} S$ is flat over $\mathcal{X}$.

Proof. Let $\operatorname{Spec}(B)$ denote the fiber product $\operatorname{Spec}(R) \times_{\mathcal{X}} \operatorname{Spec}(A)$ which we know to be affine as $P$ is an affine morphism. By remark $2.19, N$ is flat over $\mathcal{X}$ if and only if $P^{*} q_{*}(N)=N \otimes_{R} B$ is a flat $A$-module. As $f$ is faithfully flat, its base change $f^{\prime}: \operatorname{Spec}\left(S \otimes_{R} B\right) \rightarrow \operatorname{Spec}(B)$ is faithfully flat as well. Moreover, by pullback pasting in the next diagram, $\operatorname{Spec}\left(S \otimes_{R} B\right) \cong \operatorname{Spec}\left(S \otimes_{A} \Gamma\right)$
![img-42.jpeg](img-42.jpeg)

In particular, $B \rightarrow S \otimes_{A} \Gamma$ is faithfully flat and by lemma 2.18 2), $N \otimes_{R} B$ is a flat $A$-module if and only if $N \otimes_{R} B \otimes_{B} S \otimes_{A} \Gamma=N \otimes_{R} S \otimes_{A} \Gamma$ is a flat $A$-module. Observe that $N \otimes_{R} S \otimes_{A} \Gamma=P^{*}(f \circ q)_{*}\left(N \otimes_{R} S\right)$, thus $N \otimes_{R} S \otimes_{A} \Gamma$ is a flat $A$-module if and only if $N \otimes_{R} S$ is flat on $\mathcal{X}$.

Remark 2.25. Any flat $A$-module $N$ is flat over $\mathcal{X}$. Indeed, by lemma 2.17 , since $s: A \rightarrow \Gamma$ is assumed to be faithfully flat, $N$ is a flat $A$-module if and only if $N \otimes_{A, s} \Gamma$ is a flat $\Gamma$-module. By lemma 2.181 ) and as both units are faithfully flat, $N \otimes_{A} \Gamma$ is also a flat $A$-module with respect to the module structure coming from either $s$ or $t$. Flatness with respect to the module structure induced by $t$ is the condition for $N$ to be flat over $\mathcal{X}$.
We will show in example 2.58 1), that $\mathbb{Q}$ is flat over $\mathcal{M}_{F G}$, i.e. that $\mathbb{Q} \otimes_{q, L, \eta_{L}} W \otimes_{L, \eta_{R}}-$ is exact where $g: L \rightarrow \mathbb{Q}$ is zero in every non-trivial degree and the inclusion in degree zero. As $\mathbb{Q}$ is not an infinitely generated polynomial ring, it is not flat over the Lazard ring (as explained after prop. 2.3). Moreover, observe that $\mathbb{Q} \otimes_{L, \eta_{L}} W \otimes_{L, \eta_{L}}-$ is also not exact as multipication by any $x_{i} \in L$ is the zero map under that functor. Indeed, in $\mathbb{Q} \otimes_{L, \eta_{L}} W \otimes_{L, \eta_{L}} L$ it holds that $q \otimes w \otimes x_{i}=q \otimes \eta_{L}\left(x_{i}\right) w \otimes 1=g\left(x_{i}\right) q \otimes w \otimes 1=0$. Thus, this functor doesn't preserve exactness of the sequence $0 \rightarrow L \xrightarrow{x_{i}} L \rightarrow L /\left(x_{i}\right) \rightarrow 0$.

Hence, asking for flatness over $[(A, \Gamma)]$ is usually strictly weaker than requiring flatness over $A$. This does not, as one might at first think, come from the fact that we are asking $N \otimes_{A, s} \Gamma$ to be flat merely as an $A$-module rather than a $\Gamma$-module, but from the fact that we are asking for it to be flat with the $A$-module structure coming from a different map than that over which we tensored (namely $t$ rather than $s$ ). Observe that it doesn't matter if we consider $N \otimes_{A, t} \Gamma$ with $A$-module structure coming from $s$ instead. The fact that these units are in general different is the crucial point making it possible to find weaker conditions for flatness over a stack. In fact, the following proposition shows that if both units agreed, the flat modules over $[(A, \Gamma)]$ coincide with the flat modules over $A$.

Lemma 2.26. Let $N$ be an $A$-module and suppose that $N \otimes_{s, A} \Gamma$ seen as $A$-module via $s$ is flat. Then, $N$ is a flat $A$-module.

Proof. We wish to show that applying $-\otimes_{A} N$ to any exact sequence $0 \rightarrow M \rightarrow M^{\prime} \rightarrow M^{\prime \prime} \rightarrow 0$ of $A$-modules preserves exactness. As $N \otimes_{s, A} \Gamma$ is flat, we know that applying $N \otimes_{s, A} \Gamma \otimes_{A, s}-$ to the sequence preserves exactness. Now as $\Gamma$ is faithfully flat over $A$ via $s$ the previous sequence is exact if and only if the sequence $0 \rightarrow M \otimes_{A} N \rightarrow M^{\prime} \otimes_{A} N \rightarrow M^{\prime \prime} \otimes_{A} N \rightarrow 0$ is exact.

Now that we have highlighted the importance of the difference between the two units, we will no longer emphasise this and trust that the reader can keep track of the right module structures to consider (we already did this in lemma 2.24).

We can now prove a criterion for exactness of the pullback functor. This is a generalisation of [15, Lect. 15, Prop. 5].

Proposition 2.27. Consider a morphism of stacks $q: \operatorname{Spec}(R) \rightarrow \mathcal{X}$ and an $R$-module $N$. Then, $N$ is flat over $\mathcal{X}$ if and only if the functor $q^{*}(-) \otimes_{R} N: \operatorname{QCoh}(\mathcal{X}) \rightarrow \operatorname{Mod}_{R}$ is exact. In particular, when $N=R, q$ is flat if and only if the pullback functor $q^{*}(-)$ is exact.

Proof. First, consider the case when $q$ factors as $q: \operatorname{Spec}(R) \xrightarrow{\tilde{q}} \operatorname{Spec}(A) \rightarrow \mathcal{X}$. Let $P: \operatorname{Spec}(A) \rightarrow \mathcal{X}$ be the presentation and consider the following 2 -commutative diagram of cartesian squares
![img-43.jpeg](img-43.jpeg)

By assumption $P$ is faithfully flat, by base change, $P^{\prime}$ is faithfully flat as well. Hence, asking for $q^{*}(-) \otimes_{R} N$ to be exact is equivalent to asking for the functor $q^{*}(-) \otimes_{R} N \otimes_{R}\left(R \otimes_{A} \Gamma\right)$ to be exact. We claim that this functor is isomorphic to $P^{*}(-) \otimes_{A}\left(N \otimes_{A} \Gamma\right)$. Indeed, let $M \in \operatorname{QCoh}(\mathcal{X})$ be arbitrary. Observe that by quasicoherence

$$
q^{*}(M) \otimes_{R} N \otimes_{R}\left(R \otimes_{A} \Gamma\right) \cong\left(\left(R \otimes_{A} \Gamma\right) \otimes_{R} M(q)\right) \otimes_{R} N \cong M\left(q \circ P^{\prime}\right) \otimes_{R} N
$$

By commutativity of the above diagram, $M\left(q \circ P^{\prime}\right) \simeq M\left(P \circ q^{\prime}\right)$. By quasicoherence, we have the following chain of equivalences for the latter:

$$
M\left(P \circ q^{\prime}\right) \otimes_{R} N \simeq M(P) \otimes_{A}\left(\Gamma \otimes_{A} R\right) \otimes_{R} N \simeq M(P) \otimes_{A}\left(N \otimes_{A} \Gamma\right)
$$

All the isomorphisms were natural in $M$ which gives the desired isomorphism between the two functors. Hence, $M \mapsto q^{*}(M) \otimes_{R} N$ is exact if and only if the functor $M \mapsto P^{*}(M) \otimes_{A}\left(N \otimes_{A} \Gamma\right)$ is exact. We claim that this condition is equivalent to $N$ being flat over $\mathcal{X}$ (with respect to $q$ ). Indeed, recall that a sequence of quasicoherent sheaves on $\mathcal{X}$ is exact if and only if the sequence of $A$-modules induced by $P^{*}$ is exact. So the functor $M \mapsto M(P)$ is exact by definition. It remains to see that $-\otimes_{A}\left(N \otimes_{A} \Gamma\right)$ is an exact functor of $A$-modules if and only if $N$ is flat over $\mathcal{X}$. By definition, the latter means that $q_{*}(N)(P)=N \otimes_{R}\left(R \otimes_{A} \Gamma\right)$ is a flat $A$-module, which is exactly what was needed.
It remains to consider the case when $q: \operatorname{Spec}(R) \rightarrow \mathcal{X}$ does not factor through $\operatorname{Spec}(A)$. As usual, by proposition 1.36 , there exists a faithfully flat cover $f: \operatorname{Spec}(S) \rightarrow \operatorname{Spec}(R)$ such that $q \circ f$ factors through $\operatorname{Spec}(A)$. By lemma 2.24 , the $R$-module $N$ is flat over $\mathcal{X}$ if and only if the $S$-module $M \otimes_{R} S$ is flat over $\mathcal{X}$. By the previous discussion, this last condition is satisfied if and only if the functor $(q \circ f)^{*}(-) \otimes_{S} M \otimes_{R} S$ is exact. As $f$ is faithfully flat, $(q \circ f)^{*}(-) \otimes_{S} M \otimes_{R} S=f^{*} \circ q^{*}(-) \otimes_{R} M$ is exact if and only if $q^{*}(-) \otimes_{R} M$ is exact, which concludes the proof.

Corollary 2.28. Let $f: E_{*} \rightarrow R=\left\{R_{j}\right\}_{j \in \mathbb{Z}}$ be a graded ring map. If $f$ is such that the induced map $f$ : $\operatorname{Spec}\left(\otimes_{j} R_{j}\right) \rightarrow\left[\left(\left(E_{*}, E_{*}(E)\left[u^{\pm}\right]\right)\right)\right]$ is flat, then the functor $h_{f}: h S p \rightarrow A b$ defined by $X \mapsto E_{*}(X) \otimes_{E_{*}} R$ defines a homology theory.

Proof. We have already discussed in lemma 2.1 that it suffices to show that $-\otimes_{E_{*}} R$ preserves exact sequences. Let us write $\oplus_{i} E_{2 i}(X)$ and $\oplus_{i} E_{2 i+1}(X)$ for the ungraded $\left(E_{*}, E_{*}(E)\left[u^{\pm}\right]\right)$-comodules corresponding to $E_{\text {even }}(X)$ and $E_{\text {odd }}(X)$ respectively, under the equivalence of categories of proposition 2.7. Let $\mathcal{F}_{\oplus_{i} E_{2 i}(X)}$ denote the corresponding quasicoherent sheaf under the equivalence of proposition 2.13. Recall from the proof of that same proposition that

$$
f^{*}\left(\mathcal{F}_{\oplus_{i} E_{2 i}(X)}\right)=\mathcal{F}_{\oplus_{i} E_{2 i}(X)}(f)=\oplus_{i} E_{2 i}(X) \otimes_{\oplus_{i} E_{i}} \oplus_{j} R_{j}
$$

and similarly for the odd case. By proposition 2.27 , we know that the pullback functor $f^{*}(-)$ is exact. Hence, given a fiber sequence $X \rightarrow Y \rightarrow Z \rightarrow X[1]$, the sequence

$$
\oplus_{i} E_{2 i}(X) \otimes_{\oplus_{i} E_{i}} \oplus_{j} R_{j} \rightarrow \oplus_{i} E_{2 i}(Y) \otimes_{\oplus_{i} E_{i}} \oplus_{j} R_{j} \rightarrow \oplus_{i} E_{2 i}(Z) \otimes_{\oplus_{i} E_{i}} \oplus_{j} R_{j} \rightarrow \oplus_{i} E_{2 i}(X[1]) \otimes_{\oplus_{i} E_{i}} \oplus_{j} R_{j}
$$

is exact. The analogous statement holds for the odd case. The direct sum of the even and odd sequence is exact as well and, by distributivity of the tensor product, it gives exactness of

$$
\oplus_{i} E_{i}(X) \otimes_{\oplus_{i} E_{i}} \oplus_{j} R_{j} \rightarrow \oplus_{i} E_{i}(Y) \otimes_{\oplus_{i} E_{i}} \oplus_{j} R_{j} \rightarrow \oplus_{i} E_{i}(Z) \otimes_{\oplus_{i} E_{i}} \oplus_{j} R_{j} \rightarrow \oplus_{i} E_{i}(X[1]) \otimes_{\oplus_{i} E_{i}} \oplus_{j} R_{j}
$$

By lemma 2.8, this sequence is isomorphic to the sequence

$$
\oplus_{i}\left(E_{*}(X) \otimes_{E_{*}} R\right)_{i} \rightarrow \oplus_{i}\left(E_{*}(Y) \otimes_{E_{*}} R\right)_{i} \rightarrow \oplus_{i}\left(E_{*}(Z) \otimes_{E_{*}} R\right)_{i} \rightarrow \oplus_{i}\left(E_{*}(X[1]) \otimes_{E_{*}} R\right)_{i}
$$

whose exactness is in turn equivalent to exactness of

$$
E_{*}(X) \otimes_{E_{*}} R \rightarrow E_{*}(Y) \otimes_{E_{*}} R \rightarrow E_{*}(Z) \otimes_{E_{*}} R \rightarrow E_{*}(X[1]) \otimes_{E_{*}} R
$$

as graded abelian groups.
Corollary 2.29. Let $N=\left\{N_{j}\right\}_{j \in \mathbb{Z}}$ be a graded $E_{*}$-module. If $\oplus_{j} N_{j}$ is flat over $\left[\left(E_{*}, E_{*}(E)\left[u^{\pm}\right]\right)\right]$, then the assignment $X \mapsto E_{*}(X) \otimes_{E_{*}} N$ defines a homology theory.

Proof. Again, by lemma 2.1, it suffices to show that $-\otimes_{E_{*}} N$ preserves exact sequences. Consider the presentation $c: \operatorname{Spec}\left(E_{*}\right) \rightarrow\left[\left(E_{*}, E_{*}(E)\left[u^{\pm}\right]\right)\right]$. By proposition 2.27 , as $\oplus_{j} N_{j}$ is flat over $\left[\left(E_{*}, E_{*}(E)\left[u^{\pm}\right]\right)\right]$, for $M \in \operatorname{QCoh}\left(\left[\left(E_{*}, E_{*}(E)\left[u^{\pm}\right]\right)\right]\right)$, the functor $M \mapsto c^{*}(M) \otimes_{\oplus_{i} E_{i}} \oplus N_{j}$ is exact. By definition of exactness of quasicoherent schemes, $c^{*}$ is already an exact functor. Hence, $-\otimes_{\oplus E_{i}} \oplus_{j} N_{j}$ is an exact functor. We have seen in the proof of corollary 2.28 how to deduce that also the graded tensor product $-\otimes_{E_{*}} N$ is exact.

This gives the abstract formalism with which we can build a new homology theory from an even spectrum of Adams type $E$. It suffices to find interesting modules that are flat over its associated stack. More precisely, by lemma 2.23 , one needs to find a module $M$ such that $M \otimes_{E_{*}} E_{*}(E)$ is a flat $E_{*}$-module. However, this is still a difficult problem. For example, as the Hopf algebroid associated to the even part of $\mathbb{S}_{*}$ is trivial, trying to find flat modules over its associated stack comes down to finding flat $\mathbb{S}_{\text {even }}$-modules. This requires a good understanding of the homotopy groups of the sphere. For the spectrum $M S p$, we would need to understand flatness over the symplectic bordism ring. Even when $E_{*}$ is well-understood, determining this tensor product can be difficult as it also requires an understanding of the structure maps from the Hopf algebroid:

Example 2.30 ([15, Lect. 15, Ex. 7]). Fix some prime $p$ and consider the Lazard ring $L \cong \mathbb{Z}\left[x_{1}, x_{2}, \ldots\right]$. Let us write $v_{i}:=x_{p^{\prime}-1}$. Recall from proposition 1.68 that $\left[\left(M U_{*}, M U_{*}(M U)\left[u^{\pm}\right]\right)\right] \cong \mathcal{M}_{F G}$ and that $c: \operatorname{Spec}(L) \rightarrow \mathcal{M}_{F G}$ classifying the universal formal group law is a presentation. Consider the $L$-module $R:=\mathbb{Z}_{(p)}\left[v_{1}, v_{2}, \ldots\right] \cong L_{(p)} /\left(x_{i} \mid i \neq p^{k}-1\right)$ and let $q: L \rightarrow R$ be the quotient map. We claim that the map $\tilde{q}: \operatorname{Spec}(R) \rightarrow \operatorname{Spec}(L) \rightarrow \mathcal{M}_{F G}$ is flat. By corollary 1.38 , one needs to show that $q^{\prime}$ (which is the projection to $\operatorname{Spec}(W)$ composed with $\eta_{L}$ ) in the following pullback diagram is flat
![img-44.jpeg](img-44.jpeg)

The ring $B$ is given by

$$
L_{(p)} /\left(x_{i} \mid i+1 \neq p^{k}\right) \otimes_{L, \eta_{R}} L\left[b_{0}^{ \pm}, b_{1}, b_{2}, \ldots\right] \cong L_{(p)}\left[b_{0}^{ \pm}, b_{1}, b_{2}, \ldots\right] /\left(\eta_{R}\left(x_{i}\right) \mid i+1 \neq p^{k}\right)
$$

By remark $1.56, \eta_{R}\left(x_{i}\right)=b_{i}+$ terms of degree $\geq 2$. Thus, there is an isomorphism

$$
L_{(p)}\left[b_{0}^{ \pm}, b_{1}, b_{2}, \ldots\right] /\left(\eta_{R}\left(x_{i}\right) \mid i+1 \neq p^{k}\right) \cong L_{(p)}\left[b_{0}^{ \pm}, b_{i} \mid i+1=p^{k}\right]
$$

and $B$ is a polynomial ring over $L_{(p)}$. As such, it is a faithfully flat $L_{(p)}$-module and, as localisation preserves flatness, $B$ is a flat $L$-module as claimed. By corollary 2.28 , the functor $h_{q}: h S p \rightarrow A b, X \mapsto$ $M U_{*}(X) \otimes_{M U_{*}} R$ defines a homology theory called Brown-Peterson homology.

Note that understanding this example was only possible because we had some knowledge about $\eta_{R}$. This knowledge came out of the proof of the Lazard theorem, which is known to be difficult.
This example concentrated on a particular prime $p$. It seems natural to ask if we can phrase it in terms of the stack associated to $\left[\left(L_{(p)}, W_{(p)}\right)\right]$ instead of $\mathcal{M}_{F G}$. This stack is equivalent to the product $\mathcal{M}_{F G} \times \operatorname{Spec}\left(\mathbb{Z}_{(p)}\right)$ as by remark 1.42 and by definition

$$
\mathcal{M}_{F G} \times \operatorname{Spec}\left(\mathbb{Z}_{(p)}\right)=\mathcal{M}_{F G} \times_{\operatorname{Spec}(\mathbb{Z})} \operatorname{Spec}\left(\mathbb{Z}_{(p)}\right)=[(L, W)] \times_{[(\mathbb{Z}, \mathbb{Z})]}\left[\left(\mathbb{Z}_{(p)}, \mathbb{Z}_{(p)}\right)\right] \cong\left[\left(L_{(p)}, W_{(p)}\right]\right.
$$

Let $\pi_{\mathcal{M}_{F G}}: \mathcal{M}_{F G} \times \operatorname{Spec}\left(\mathbb{Z}_{(p)}\right) \rightarrow \mathcal{M}_{F G}$ denote the projection, $i: \operatorname{Spec}\left(L_{p}\right) \rightarrow \operatorname{Spec}(L)$ the localisation and let $c_{p}: \operatorname{Spec}\left(L_{(p)}\right) \rightarrow \mathcal{M}_{F G} \times \operatorname{Spec}\left(\mathbb{Z}_{(p)}\right)$ be the map induced by the universal property of the pullback from $c \circ i$, and the inclusion $\mathbb{Z}_{(p)} \rightarrow L_{(p)}$ in degree zero. Observe that $c_{p}$ is a presentation for $\mathcal{M}_{F G} \times \operatorname{Spec}\left(\mathbb{Z}_{(p)}\right)$ by base change and that by construction $\pi_{\mathcal{M}_{F G}} \circ c_{p}=c \circ i$. In particular, $\tilde{q}$ factors as $\pi_{\mathcal{M}_{F G}} \circ c_{p} \circ q_{p}$ where $q_{p}: \operatorname{Spec}(R) \rightarrow \operatorname{Spec}\left(L_{(p)}\right)$ is the quotient.

Lemma 2.31. The map $q: \operatorname{Spec}(R) \rightarrow \mathcal{M}_{F G} \times \operatorname{Spec}\left(\mathbb{Z}_{(p)}\right)$ defined as $q:=c_{p} \circ q$ is affine and faithfully flat.

Proof. We have to show that $q_{p}^{\prime}$ in the following pullback diagram is affine and faithfully flat.
![img-45.jpeg](img-45.jpeg)

As map between affine schemes, $q_{p}^{\prime}$ is clearly affine. As $R$ is $p$-local, $R \otimes_{L_{(p)}} W_{(p)}=\left(R \otimes_{L} W\right)_{(p)}=B_{p}$ where $B$ is as in example 2.30. As $B$ was already $p$-local, this pullback is also $B_{(p)}=B$ and we have already shown in example 2.30 that $B$ is faithfully flat over $L_{(p)}$.

Remark 2.32. As $q$ is faithfully flat and affine, it is also a presentation for $\mathcal{M}_{F G} \times \operatorname{Spec}\left(\mathbb{Z}_{(p)}\right)$. Observe that the fiber product $\operatorname{Spec}(R) \otimes_{q, \mathcal{M}_{F G} \times \operatorname{Spec}\left(\mathbb{Z}_{(p)}\right), q} \operatorname{Spec}(R)$ is given by $R \otimes_{L_{(p)}} W_{(p)} \otimes_{L_{(p)}} R$. By theorem 1.40,

$$
\mathcal{M}_{F G} \times \operatorname{Spec}\left(\mathbb{Z}_{(p)}\right) \cong\left[\left(R, R \otimes_{L_{(p)}} W_{(p)} \otimes_{L_{(p)}} R\right)\right]
$$

We noted before that $\mathcal{M}_{F G} \times \operatorname{Spec}\left(\mathbb{Z}_{(p)}\right)$ is associated to the Hopf algebroid $\left(L_{(p)}, W_{(p)}\right)$, so

$$
\left[\left(L_{(p)}, W_{(p)}\right)\right] \cong\left[\left(R, R \otimes_{L_{(p)}} W_{(p)} \otimes_{L_{(p)}} R\right)\right]
$$

However, the two Hopf algebroids are not isomorphic as $L_{(p)}$ has generators in all even degrees whereas $R$ only has generators in degrees $2\left(p^{i}-1\right)$. This gives a concrete example of the failure of the forgetful functor from rigidified algebraic stack to stacks to be full as mentioned in remark 1.41.

Having a tool to construct new homology theories is nice, but it would be better to be able to lift these theories to spectra. The following theorem provides us with a partial solution:

Theorem 2.33 (Brown representabilty, [15, Lect. 17, Thm. 1]). Let HomTh denote the category of homology theories. Then, the functor $h S p \rightarrow$ HomTh, $F \mapsto \pi_{*}\left((-) \otimes F\right):=F_{*}(-)$ is essentially surjective and full. In particular, given a spectrum $F$, a homology theory $h_{*}$ and a map of homology theories $\alpha: F_{*} \rightarrow h_{*}$, there is a map of spectra $\beta: F \rightarrow F^{\prime}$ and an isomorphism of homology theories $F_{*}^{\prime} \simeq h_{*}$ such that $\alpha$ is given by the composition $F_{*} \xrightarrow{\beta_{*}} F_{*}^{\prime} \simeq h_{*}$.

The fact that this functor is not fully faithful is due to the existence of so called phantom maps, nonnullhomotopic maps between spectra that induce the zero map on homology.

Corollary 2.34 ([15, Lect. 18, Cor. 3]). Every homology theory $h_{*}$ is represented by a spectrum $F$, which is uniquely defined up to (nonunique) homotopy equivalence.

Proof. The existence of $F$ follows from theorem 2.33. For the uniqueness, we note that if $F$ and $F^{\prime}$ are two spectra both inducing homology theories isomorphic to $h_{*}$, then, again by theorem 2.33, the isomorphism $F_{*} \rightarrow h_{*} \rightarrow F_{*}^{\prime}$ comes from a map of spectra, which is a homotopy equivalence by Whitehead's theorem.

Our takeaway is that the natural transformation between homology theories $H_{f}: E_{*} \rightarrow E_{*}(-) \otimes_{E_{*}}$ $R:=h_{f}$ always induces some morphism of spectra $\varphi: E \rightarrow E^{f}$ with $E_{*}^{f} \cong E_{*}(-) \otimes_{E_{*}} R$ such that $\pi_{*}(-\otimes \varphi)=H_{f}$. The spectrum $E^{f}$ is uniquely defined up to homotopy, but the morphism $\varphi$ might not be unique up to homotopy. There could be two nonhomotopic morhphisms $\alpha, \beta: E \rightarrow E^{f}$ such that $\alpha_{*} \cong \beta_{*} \cong h_{f}$ i.e. $\alpha$ and $\beta$ differ by a phantom map. In particular, in general, the construction that associates the spectrum $E^{f}$ to the homology theory $h_{f}$ by lifting the natural transformation $H_{f}$ cannot be made functorial in $f$ and we have no control on whether $E^{f}$ is a homotopy commutative ring spectrum or $E \xrightarrow{\varphi} E^{f}$ a map of homotopy commutative ring spectra. However, some situations are nice enough that we can exclude phantom maps. More on this will be discussed in subsection 2.2 (theorem 2.50 , corollary 2.51 , proposition 2.52 and remark 2.54 ).

Remark 2.35. Let $f: E_{*} \rightarrow R$ be a morphism exhibiting $R$ as an $E_{*}$-module that is flat over $\left[\left(E_{*}, E_{*}(E)\left[u^{ \pm}\right]\right)\right]$. Let $E^{f}$ be the spectrum associated to $h_{f}$ as discussed above. Then:

1. By construction, $E^{f}$ admits a morphism of spectra $E \rightarrow E^{f}$.
2. The $n^{\text {th }}$ homotopy group of $E^{f}$ is given by $R_{n}$, the elements of degree $n$ in $R$, as

$$
\pi_{n}\left(E^{f}\right)=E_{n}^{f}(\mathbb{S}) \cong\left(E_{*}(\mathbb{S}) \otimes_{E_{*}} R\right)_{n}=\left(E_{*} \otimes_{E_{*}} R\right)_{n} \cong R_{n}
$$

# 2.2 The Landweber Exact Functor Theorem 

When $E=M U$, there exists a calculable criterion to check whether a map into $\left[\left(M U_{*}, M U_{*}(M U)\left[u^{ \pm}\right]\right)\right]=$ $\mathcal{M}_{F G}$ is flat. This exploits the fact that we have a good understanding of $\mathcal{M}_{F G}$ as moduli stack of formal groups and an effective filtration of its p-localisations. Before stating the main result of this section, we need to, once more, recall a few more facts about formal group laws.

Definition 2.36. Let $F$ be a formal group law over a ring $R$. For a natural number $n$, define its $n$-series, $[n]_{F}(x)$, inductively as the power series defined by $[1]_{F}(x)=x$ and $[n]_{F}(x)=F([n-1]_{F}(x), x)$.

Observe that the $n$-series is an endomorphism of $F$.
Definition 2.37. Given a prime $p$ and a formal group law $F$ over $R$, we define $v_{i}^{F, p} \in R$ to be the coefficient in front of $x^{p^{\prime}}$ in the $p$-series $[p]_{F}$. We drop the superscript $F, p$ and simply write $v_{i}$ when the formal group law and the prime are clear from context.

Remark 2.38. By unitality of formal group laws, $v_{0}$, the coefficient in front of $x$ in $[p]_{F}$, will always be given by $p$.

Remark 2.39. The $p$-series of the universal formal group law defines elements $v_{i} \in L$. Refining the proof of Lazard's theorem (thm. 1.53), one can show that there is an isomorphism $L_{(p)} \cong \mathbb{Z}_{(p)}\left[x_{1}, x_{2}, \ldots\right]$ such that $x_{p^{\prime}-1}=v_{i}$ for all $i$; see [15, Lect. 13, Prop. 1]. In particular, the notation in example 2.30 was chosen compatibly with this isomorphism. Moreover, observe that, for a formal group law $F$ on some ring $R$ corresponding to a morphism $\theta_{F}: L \rightarrow R, \theta_{F}\left(v_{i}\right)=v_{i}^{F}$. We will use these observations tacitly in the following.

Definition 2.40. We say that a formal group law $F$ has height $\geq n$ at a prime $p$ if the elements $v_{i}^{F, p}$ vanish for for all $i<n$. If further $v_{n}^{F, p}$ is invertible, $F$ has height exactly $n$.

Lemma 2.41 ([15, Lect. 12, Rmk. 15]). Two isomorphic formal group laws have the same height.
Fix a prime $p$. We introduce three substacks of $\mathcal{M}_{F G} \times \operatorname{Spec}\left(\mathbb{Z}_{(p)}\right)$ :

Definition 2.42. The moduli stack of formal groups of height exactly $n, \mathcal{M}_{F G}^{n}$, is the stack which associates to an affine scheme $\operatorname{Spec}(R)$ the groupoid $\mathcal{M}_{F G}(\operatorname{Spec}(R))$ whose objects are formal groups over $\operatorname{Spec}(R)$ of height exactly $n$ at $p$ and whose morphisms are isomorphisms of formal groups.
The moduli stack of formal groups of height $\geq n, \mathcal{M}_{F G}^{\geq n}$, and the moduli stack of formal groups height $<n, \mathcal{M}_{F G}^{\geq n}$, are defined analogously, replacing "height exactly $n$ " by "height $\geq n$ " and "height $<n$ " respectively.

The stack $\mathcal{M}_{F G}^{n}$ will be a key ingredient for the proof of theorem 2.43, $\mathcal{M}_{F G}^{\geq n}$ will be needed for theorem 2.4 and $\mathcal{M}_{F G}^{\geq n}$ will appear in example 2.62 .
We can now state the main result of this section.
Theorem 2.43 (Algebraic Landweber Thm., [15, Lect. 16, Thm. 1]). Let $M$ be a module over the Lazard ring $L$. Then, $M$ is flat over $\mathcal{M}_{F G}$ if and only if, for every prime $p$, the elements $\left(v_{0}=p, v_{1}, v_{2}, \ldots\right) \in L$ form a regular sequence for $M$, i.e. multiplication by $\cdot v_{i}: M /\left(p, v_{1}, \ldots, v_{i-1}\right) \rightarrow M /\left(p, v_{1}, \ldots, v_{i-1}\right)$ is injective for all $i \in \mathbb{N}$.

The proof is long and deferred to subsection 2.3. Combining this theorem with results from the previous subsection, we get the following pleasant statement:

Corollary 2.44 (Landweber Exact Functor Theorem). Let $F$ be a graded formal group law over a graded ring $R$ (i.e. some morphism $M U_{*} \rightarrow R$ ) and let $h_{F}: h S p \rightarrow A b$ be the functor defined by $X \mapsto M U_{*}(X) \otimes_{M U_{*}} R$. Then $h_{F}$ is a homology theory if for every prime $p$ the sequence $p, v_{1}, v_{2}, \ldots$ is regular on $R$.

Proof. In view of corollary 2.28, it suffices to show that $R$ is a flat $L$-module over $\mathcal{M}_{F G}$. By theorem 2.43 , this is the case if and only if the $v_{i}$ form a regular sequence on $R$.

Remark 2.45. In accordance with [15, Lect. 17], we will from now on adopt the convention that $R$ is evenly graded. This is not a restriction as, since $L$ is evenly graded, any interesting map $L \rightarrow R$ factors through the even part of $R$ anyways. Moreover, we should mention that we can also apply corollary 2.44 to ungraded ring maps $F: L \rightarrow R$ by forcing a grading on $R$. More precisely, we replace $R$ by the graded ring $R\left[u^{ \pm}\right]$with $u$ in degree 2 and replace $F$ by the map that sends $x_{i}$ to $F\left(x_{i}\right) u^{i}$.

Remark 2.46. The previous statement was first shown by Peter Landweber in [11]. In this paper, no stack appears. Rather it is shown that, under the conditions of the corollary, the functor $-\otimes_{L} R$ : $(L, W) \operatorname{comod} \rightarrow A b$ is exact using methods from homological algebra. We have seen in proposition 2.27 and corollary 2.28 how exactness of this functor corresponds to flatness of the corresponding morphism of stacks.

Definition 2.47. A formal group law satisfying the assumption of theorem 2.43 is called Landweber exact.

It was discussed in the previous section how, given a Landweber exact formal group law $F$, one could lift the natural transformation $H_{F}: M U_{*}(-) \rightarrow h_{F}(-)$ to a map $\varphi: M U \rightarrow M U^{F}$ between spectra.

Definition 2.48. A spectrum arising from this construction is called Landweber exact.
Remark 2.49. Let $F: M U_{*} \rightarrow R$ be a graded Landweber exact formal group laws and let $M U^{F}$ be its associated spectrum. Recall from remark 2.35 that $\pi_{n}\left(M U^{F}\right)=R_{n}$. In particular, by the convention adopted in remark $2.45, M U^{F}$ is even.

We had run into the problem of phantom maps, but, as we will now see, all phantom maps vanish in the case of Landweber exact spectra. More precisely,

Theorem 2.50 ([15, Thm. 6, Lect. 17]). Let $E$ be a Landweber-exact spectrum, and let $E^{\prime}$ be an even spectrum. Then, every phantom map $f: E \rightarrow E^{\prime}$ is nullhomotopic. In particular, in view of remark 2.49, any phantom map between two Landweber exact spectra is nullhomotopic.

Theorem 2.33 implies:
Corollary 2.51. Denote by hLand the full subcategory of hSp spanned by Landweber exact spectra. Let HomTh denote the category of homology theories. Then, the functor hLand $\rightarrow$ HomTh, $E \mapsto E_{*}(-)$ is fully faithful.

For the proof, we refer the reader to the detailed discussion in [15, Lect. 17]. The key point is that the spectrum $M U$ is evenly generated meaning that any map from a finite spectrum to $M U$ factors through an even finite spectrum. This is due to the construction of $M U$ as homotopy colimit of Thom spectra associated to the finite-dimensional complex Grassmaninans which admit a finite cell decomposition with even cells. From this, one can deduce that any Landweber exact spectrum is evenly generated (see [15, Prop. 9, Lect. 17]). This evenness then obstructs the existence of phantom maps to an even spectrum (see $[15$, Prop. 10, Lect. 17]).

The nonexistence of phantom maps has the following nice consequence:
Proposition 2.52. Landweber exact spectra are homotopy commutative ring spectra. Moreover, the map $\varphi: M U \rightarrow M U^{F}$ lifted from $M U_{*}(-) \rightarrow h_{F}$ is a map of homotopy commutative ring spectra.

Proof. Let $F: L \rightarrow R$ be a Landweber exact formal group law and for clarity of notation let us denote its associated spectrum by $E$ instead of $M U^{F}$ during this proof.
The unit map is easy to define. It is given by $\eta_{E}: \mathbb{S} \xrightarrow{\eta_{M U}} M U \rightarrow E$ where $\eta_{M U}: \mathbb{S} \rightarrow M U$ is the unit of $M U$.
To define the multiplication $\mu_{E}: E \otimes E \rightarrow E$, we begin by constructing a map of homology theories $(E \otimes E)_{*}(-) \rightarrow E_{*}(-)$ which, by corollary 2.51 , can be uniquely lifted to the desired map of spectra. The key observation is that for any spectrum $X$, the $E \otimes E$-homology of $X$ can also be written in terms of $M U$. Indeed,

$$
\begin{aligned}
(E \otimes E)_{*}(X) & =\pi_{*}(E \otimes E \otimes X) & & \text { by definition } \\
& =E_{*}(E \otimes X) & & \\
& =M U_{*}(E \otimes X) \otimes_{M U_{*}} R & & \text { as } E \text { is Landwebwer exact } \\
& =\pi_{*}(M U \otimes E \otimes X) \otimes_{M U_{*}} R & & \text { definition again } \\
& =E_{*}(M U \otimes X) \otimes_{M U_{*}} R & & \\
& =M U_{*}(M U \otimes X) \otimes_{M U_{*}} R \otimes_{M U_{*}} R & & \text { Landweber exactness again } \\
& =\pi_{*}(M U \otimes M U \otimes X) \otimes_{M U_{*}} R \otimes_{M U_{*}} R & &
\end{aligned}
$$

Let $\mu_{M U}: M U \otimes M U \rightarrow M U$ denote the multiplication on $M U$. Multiplication on $R$ is $M U_{*}$-bilinear and hence descends to a map $m: R \otimes_{M U_{*}} R \rightarrow R$. Consider the map
$(E \otimes E)(X)=\pi_{*}(M U \otimes M U \otimes X) \otimes_{M U_{*}}\left(R \otimes_{M U_{*}} R\right) \xrightarrow{\pi_{*}\left(\mu_{M U} \otimes X\right) \otimes m} \pi_{*}(M U \otimes X) \otimes_{M U_{*}} R=E_{*}(X)$.
This defines a natural transformation of homology theories $(E \otimes E)_{*}(-) \rightarrow E_{*}(-)$ and, as explained in the beginning, induces $\mu_{E}: E \otimes E \rightarrow E$.
It remains to check that $\mu_{E}$ is unital, associative and commutative. As before, this is done by checking the properties on the induced homology theories and using fully faithfulness to conclude about the spectra case. We write out the details for unitality on the right, the other cases follow by similar arguments. We need to show that the following diagram commutes (naturally, to get a map between homology theories, but this is clear) for all spectra $X$ :
![img-46.jpeg](img-46.jpeg)

By the above, this can be rewritten as
![img-47.jpeg](img-47.jpeg)
where $i_{1}: R \rightarrow R \otimes_{M U_{*}} R$ is the inclusion into the tensor product to the right i.e. $r \mapsto 1 \otimes r$. Now, since $\mu_{M U} \circ \eta_{M U} \simeq i d_{M U}$ and $m \circ i_{1}=i d_{R}$, this diagram commutes.

By fully faithfulness, the corresponding diagram of spectra
![img-48.jpeg](img-48.jpeg)
must commute as well.
Finally, to see that $M U \rightarrow E$ is a ring map, we must verify that the following commutes:
![img-49.jpeg](img-49.jpeg)

Again this is clear on homology because
![img-50.jpeg](img-50.jpeg)
trivially commutes where $i_{2}, i_{2}^{\prime}$ are the inclusions into the tensor product to the left.
By this proposition, remark 2.35 specialises to the following observations:
Remark 2.53. Let $M U^{F}$ be the Landweber exact spectrum associated to a Landweber exact formal group law $F$. Then,

1. $M U^{F}$ is complex oriented via the map of homotopy commutative ring spectra $M U \rightarrow M U^{F}$ of proposition 2.52 .
2. $\pi_{*}\left(M U^{F}\right)$ is a graded ring isomorphic to $R$.

Remark 2.54. This enables us to construct a well defined functor from the category of Landweber exact formal group laws to homotopy commutative ring spectra by sending a Landweber exact formal group law to its associated homology theory and then lifting this to the spectrum it is represented by. The nonexistence of phantom maps ensures that this extends functorially to morphisms and, in view of proposition 2.52 , that all spectra in its image are homotopy commutative ring spectra.
Complex orientability of the spectrum $M U^{F}$ gives a second way to associate a formal group law to it:
Remark 2.55. As the spectrum $M U^{F}$ is complex oriented, $M U^{F^{*}}\left(\mathbb{C} P^{\infty}\right) \cong M U_{*}^{F}[[\tilde{z}]]$ with $\tilde{z}$ a complex orientation for $M U^{F}$. We claim that the image of $z$ under $\mu^{*}: M U^{F^{*}}\left(\mathbb{C} P^{\infty}\right) \rightarrow M U^{F^{*}}\left(\mathbb{C} P^{\infty} \times \mathbb{C} P^{\infty}\right)$ induced by the H-space multiplication of $\mathbb{C} P^{\infty}$ is again the formal group law $F$ used in the construction of $M U^{F}$. Let $\varphi: M U \rightarrow M U^{F}$ denote the map witnessing complex orientability of $M U^{F}$ and let $z$ denote the canonical complex orientation for $M U$. Consider the following commutative diagram
![img-51.jpeg](img-51.jpeg)

By construction, $\varphi_{*}(z)=\left.\tilde{z}, \varphi_{*}\right|_{M U_{*}}=F$ and $\mu^{*}(z)=x+y+\Sigma_{i, j>1} a_{i j} x^{i} y^{j}$ the universal formal group law. Hence, $\mu^{*}(\tilde{z})=\varphi_{*} \circ \mu^{*}(z)=x+y+\Sigma_{i, j>1} F\left(a_{i j}\right) x^{i} y^{j}$ which is the formal group law corresponding to $F$ as claimed.
Note that this argument shows more generally that for any complex oriented spectrum $E$ with complex orientation $e$, the formal group law $\mu^{*}(e)$ corresponds to $\pi_{*}(\varphi: M U \rightarrow E)$ where $\varphi$ is the map witnessing the complex orientation.

Thus, the associated formal group law of a spectrum constructed via the Landweber exact functor theorem from a formal group law $F$ is again $F$. The following corollary provides the converse, namely that a complex oriented spectrum with Landweber exact associated formal group law $F$ is homotopy equivalent to $M U^{F}$.

Corollary 2.56. If $E$ is a complex oriented ring spectrum whose formal group law is Landweber exact, the map $M U \xrightarrow{\varphi} E$ witnessing the complex orientation induces isomorphisms $M U_{*}(X) \otimes_{M U_{*} E_{*}} \cong E_{*}(X)$ for any spectrum $X$. In particular, there is a homotopy equivalence $E \simeq M U^{u_{*}(\varphi)}$.

Proof. Let $X$ be some spectrum. The map $\varphi$ induces $\varphi \otimes X: M U \otimes X \rightarrow E \otimes X$ and taking homotopy groups one obtains a map $M U_{*}(X) \xrightarrow{\varphi^{\prime}} E_{*}(X)$. By $E_{*}$-linearity, this induces a map of graded $E_{*}$-modules $\psi_{X}: M U_{*}(X) \otimes_{M U_{*} E_{*}} \xrightarrow{\psi_{X}} E_{*}(X)$ via the assignment $a \otimes e \mapsto e \cdot \varphi^{\prime}(a)$. Observe that $\psi$ is natural in $X$ as all the maps involved in the construction were natural. We want to show that $\psi$ is an isomorphism. Observe that $\psi_{\mathbb{S}}$ is trivially an isomorphism as $M U_{*}(\mathbb{S}) \otimes_{M U_{*} E_{*}} \cong E_{*} \cong E_{*}(\mathbb{S})$. Moreover, as the previous isomorphism held in all degrees, $\psi_{\mathbb{S}^{n}}$ is an isomorphism for all integers $n$.
Now consider the family of spectra $X$ where $\psi_{X}$ is an isomorphism. We have just shown that it contains $\mathbb{S}^{n}$ for all integers $n$. It is closed under filtered colimits and sums as both $E_{*}(-)$ and $M U_{*}(-) \otimes_{M U_{*} E_{*}}$ are homology theories by assumption and corollary 2.29. If this family is also closed under cofibers, then it contains all spectra.
For the last point, let $f: X \rightarrow Y$ be a map of spectra such that both $\psi_{X}$ and $\psi_{Y}$ are isomorphisms. Denote the cofiber of $f$ by $C$. As we are dealing with homology theories, they produce long exact sequences from cofiber sequences and give rise to the following diagram with exact rows which is commutative by naturality of $\psi$ :
![img-52.jpeg](img-52.jpeg)One concludes by the five lemma that $\psi_{C}$ is also an isomorphism.
Remark 2.57. This corollary justifies extending definition 2.48 to calling any complex oriented ring spectrum with a Landweber exact formal group law is Landweber exact. We will do this in what follows.

This gives a partial answer to the question of whether one can find an inverse (up to homotopy) to the construction that associates a formal group law to a complex oriented cohmology theory. The answer is yes if the formal group law is Landweber exact! The construction is given by sending a Landweber exact formal group law $F$ to $M U^{F}$. The discussion of phantom maps ensures that $M U^{F}$ is a homotopy commutative ring spectrum. Remark 2.55 and corollary 2.56 show that the two constructions are indeed inverses. Beware however that not all complex oriented cohomology theories arise from this construction. For example, $H \mathbb{Z}$ is complex oriented, but, as we will see in the next example, its formal group law is not Landweber exact.

We are now ready to look at some well-studied explicit examples and non-examples of Landweber exact formal group laws and their associated spectra.

Example 2.58. Throughout fix an arbitrary prime $p$.

1. The following is a non-example in many cases. Consider the additive formal group law $F_{a}(x, y)=$ $x+y$ over some ring $R$, which we know to arise from singular cohomology with coefficients in $R$. As $[p]_{F_{a}}(x)=p x, v_{0}=p, v_{i}=0$ for all $i>0$. For the Landweber exactness condition to hold, we need all primes $p$ to be nonzero divisors in $R$, so that multiplication by $v_{0}=p$ is injective, and multiplication by $v_{1}=0$ must be injective on $R / p$. In other words, $R$ must be torsion free and all primes must be units in $R$. In particular, for $F_{a}$ to be Landweber exact, we need $R$ to be a $\mathbb{Q}$-algebra. For such a ring, the cohomology theory arising through Landweber's exact functor theorem is indeed singular cohomology by corollary 2.56 .
2. Consider the multiplicative formal group law $F_{m}(x, y)=x+y+u x y$ which is well known to be associated to complex K-theory (then $u$ denotes the Bott element in degree -2 ). Its $p$-series is given by $[p]_{F_{m}}(x)=\frac{(1+u x)^{p}-1}{u}$. Hence $v_{0}=p$ (as always), but this time $v_{1}=u^{p-1}$ and $v_{i}=0$ for

all $i \geq 2$. Thus, a ring $R$ over which the multiplicative formal group law is Landweber exact must be torsion free and $u$ must be a unit.
Specialising to $K U_{*}=\mathbb{Z}\left[u^{ \pm 1}\right]$, one observes that $v_{1}$ is invertible in $K U_{*} / p$. Hence, the multiplicative formal group law over $K U_{*}$ is Landweber exact and, again by corollary 2.56 , the associated spectrum recovers complex $K$-theory. This gives an alternative proof of the famous Conner-Floyd isomorphism $M U_{*}(X) \otimes_{M U_{*}} K U_{*} \cong K U_{*}(X)$.
3. Let us revisit example 2.30. Recall that we had shown that the composite

$$
M U_{*} \rightarrow M U_{*(p)} \rightarrow M U_{*(p)} /\left(x_{l}: l \neq p^{i}-1\right)=\mathbb{Z}_{(p)}\left[v_{1}, v_{2}, \ldots\right]
$$

is flat over $\mathcal{M}_{F G}$. This is more easily seen from theorem 2.43 since the $v_{i}$, being polynomial generators, clearly define a regular sequence on $\mathbb{Z}_{(p)}\left[v_{1}, v_{2}, \ldots\right]$. As mentioned in example 2.30 , this defines Brown-Peterson homology, whose associated spectrum is denoted $B P$. Beware that this argument is circular though, as we will use flatness of this map to prove theorem 2.43.
4. If one further takes the quotient of $B P_{*}=\mathbb{Z}_{(p)}\left[v_{1}, v_{2}, \ldots\right]$ by the ideal $\left(v_{n+1}, v_{n+2}, \ldots\right)$ and inverts $v_{n}$, one gets another formal group law $M U_{*} \rightarrow \mathbb{Z}_{(p)}\left[v_{1}, v_{2}, \ldots, v_{n-1}, v_{n}^{ \pm}\right]$. This is Landweber exact by construction. As before the $v_{i}$ form a regular sequence up to $v_{n}$ because they are polynomial generators, and as $v_{n}$ is invertible, so $\mathbb{Z}_{(p)}\left[v_{1}, v_{2}, \ldots, v_{n-1}, v_{n}^{ \pm}\right] /\left(v_{1}, \ldots, v_{n}\right)=0$, there is nothing more to check. This gives rise to the so-called Johnson-Wilson theory, denoted by $E(n)$, which "sees things about formal groups laws of height less than $n+1$ ". This will be made more precise in example 2.62 .
5. This non-example will be the motivating example for subsection 2.4. The $n^{\text {th }}$ Morava K-theory $K(n)$ is not Landweber exact for any prime $p$ nor any natural number $n$. Recall that its homotopy groups are given by $K(n)_{*}=\mathbb{F}_{p}\left[v_{n}^{ \pm}\right]$. Its formal group law comes from the composition $M U_{*} \rightarrow$ $M U_{(p)}{ }_{*} \rightarrow K(n)_{*}$ sending $x_{p^{n}-1}$ to $v_{n}$ and all other polynomial generators to zero. In particular, its $p$-series is given by

$$
[p]_{K(n)_{*}}=p x+v_{n} x^{p^{n}-1}=v_{n} x^{p^{n}-1}
$$

This is not Landweber exact as, for all $i<n, v_{i}=0$ and $K(n)_{*} /\left(v_{0}, \ldots, v_{i-1}\right)=K(n)_{*} \neq 0$, so multiplication by $v_{i}$ on $K(n)_{*} /\left(v_{0}, \ldots, v_{i-1}\right)$ is not injective. More easily, it would have sufficed to observe that $K(n)_{*}$ is $p$-torsion, so multiplication by $v_{0}=p=0$ cannot be injective.

One could argue that these examples did not give anything new. They are all known cohomology theories which can also be constructed alternatively. For example, Landweber already knew $B P$ when writing [11] and even proved a version of the Landweber exact functor theorem for it. We will recover this as corollary 2.71. This construction of $B P$ and $E(n)$ is presumably one of the easier ones, it depends however on the choice of the $v_{i}$ as generators of the Lazard ring and this is a very noncanonical choice. The aim of section 3 will be to convince the skeptical reader that Landweber's exact functor theorem does open up new doors because it enables us to associate cohomology theories to certain algebraic geometric objects, namely elliptic curves. Section 3 will discuss how to associate a formal group law to an elliptic curve and show that this will be "generically" Landweber exact in a sense to be made precise.

Now that we can construct many new spectra, we should wonder if we can iterate the procedure described until now and obtain yet again interesting, unknown spectra by analysing flat maps over stacks associated to Landweber exact spectra. The first condition for this to work is that the Hopf algebroid associated to a Landweber exact spectrum is flat.

Proposition 2.59. Any Landweber exact spectrum $E$ is of Adams type. In particular, it admits an associated flat Hopf algebroid $\left(E_{*}, E_{*}(E)\right)$.

Proof. We need to show that the left unit $E_{*} \cong \pi_{*}(\mathbb{S} \otimes E) \xrightarrow{\eta_{E} \otimes E} \pi_{*}(E \otimes E)$ is flat. As $E$ is Landweber exact, recall that

$$
E_{*}(E)=M U_{*}(E) \otimes_{M U_{*}} E_{*}=M U_{*}(M U) \otimes_{M U_{*}} E_{*} \otimes_{M U_{*}} E_{*}
$$

Landweber exactness of $E$ is equivalent to $E_{*} \otimes_{L} W$ being a flat $L$-module, so $E_{*} \otimes_{M U_{*}} M U_{*}(M U)$ is a flat $M U_{*}$-module. By lemma $2.16 M U_{*}(M U) \otimes_{M U_{*}} E_{*} \otimes_{M U_{*}} E_{*}$ is a flat $E_{*}$-module as needed.

Example 2.60. For a fixed prime $p$, without knowing it, we have already met the flat Hopf algebroid $\left(B P_{*}, B P_{*}(B P)\right)$ in remark 2.32. We had shown there that the associated stack to this Hopf algebroid is $\mathcal{M}_{F G}^{s} \times \operatorname{Spec}\left(\mathbb{Z}_{(p)}\right)$. We can determine $B P_{*}(B P)$ more precisely. By example 2.30,

$$
B P_{*} \otimes_{M U_{*}, \eta_{B}} M U_{*}(M U) \cong L_{(p)}\left[b_{0}^{ \pm}, b_{i} \mid i+1=p^{k}\right]
$$

and thus

$$
B P_{*}(B P) \cong L_{(p)}\left[b_{0}^{ \pm}, b_{i} \mid i+1=p^{k}\right] \otimes_{L_{(p)}} \mathbb{Z}_{(p)}\left[v_{1}, v_{2}, \ldots\right] \cong \mathbb{Z}_{(p)}\left[v_{1}, v_{2}, \ldots\right]\left[b_{0}^{ \pm}, b_{i} \mid i+1=p^{k}\right]
$$

Summing up, we have the following isomorphisms:

$$
\begin{aligned}
{\left[\left(M U_{(p)_{*}},\left(M U_{(p)_{*}}\left(\left(M U_{(p)}\right)\right)\right)\right] } & \cong \mathcal{M}_{F G}^{s} \times \operatorname{Spec}\left(\mathbb{Z}_{(p)}\right) \\
& \cong\left[\left(\mathbb{Z}_{(p)}\left[v_{1}, v_{2}, \ldots\right], \mathbb{Z}_{(p)}\left[v_{1}, v_{2}, \ldots\right]\left[b_{0}^{ \pm}, b_{i} \mid i+1=p^{k}\right]\right)\right] \cong\left[\left(B P_{*}, B P_{*}(B P)\right)\right]
\end{aligned}
$$

However, trying to understand flat maps to the stack $\left[\left(E_{*}, E_{*}(E)\right)\right]$ rarely adds anything new to the picture:

Remark 2.61. Let $E$ be a Landweber exact spectrum. The map $M U_{*} \rightarrow E_{*}$ classifying its formal group law induces a morphism of Hopf algebroids $\left(M U_{*}, M U_{*}(M U)\left[u^{ \pm}\right]\right) \rightarrow\left(E_{*}, E_{*}(E)\left[u^{ \pm}\right]\right)$and thus a map of stacks $\phi:\left[\left(E_{*}, E_{*}(E)\left[u^{ \pm}\right]\right)\right] \rightarrow \mathcal{M}_{F G}$. Whenever $\phi$ is representable, it is flat. Indeed, as flatness can be checked locally on the base, it suffices to show that $\operatorname{Spec}\left(E_{*}\right) \xrightarrow{c_{E}}\left[\left(E_{*}, E_{*}(E)\left[u^{ \pm}\right]\right)\right] \xrightarrow{\phi} \mathcal{M}_{F G}$ is flat. By construction, this map is precisely the one classifying the formal group law $M U_{*} \rightarrow E_{*}$ used to construct $E$. By assumption, as $E$ is Landweber exact, this is flat.
Given an $E_{*}$-module $N$ that is flat over $\left[\left(E_{*}, E_{*}(E)\left[u^{ \pm}\right]\right)\right]$, there is an isomorphism

$$
E_{*}(X) \otimes_{E_{*}} N \cong M U_{*}(X) \otimes_{M U_{*}} E_{*} \otimes_{E_{*}} N
$$

and the arising homology theory $X \mapsto E_{*}(X) \otimes_{E_{*}} N$ is none other than the one we could have already constructed seeing $N$ as a $M U_{*}$-module that is flat over $\mathcal{M}_{F G}$. An advantage of this point of view arises when $E_{*}$ is so simple that flatness over $E_{*}$ becomes a reasonable condition. Then, this discussion shows that a flat $E_{*}$-module is also flat over $\mathcal{M}_{F G}$ without needing to check any regularity condition on the $v_{i}$.

Despite this, the Hopf algebroid associated to a Landweber exact spectrum might encode other interesting geometric information.

Example 2.62. We will show that, for a given prime $p$, the stack associated to the Hopf algebroid $\left(E(n), E(n)_{*}(E(n))\left[u^{ \pm}\right]\right)$is $\mathcal{M}_{F G}^{<n+1}$, the moduli stack of formal groups of height smaller than $n+1$. Let $\eta: L \rightarrow L_{(p)} \rightarrow \mathbb{Z}_{(p)}\left[v_{1}, \ldots, v_{n-1}, v_{n}^{ \pm}\right]=E(n)_{*}$ denote localisation at $p$ followed by the quotient map and let $P^{\prime}: \operatorname{Spec}\left(E(n)_{*}\right) \rightarrow \mathcal{M}_{F G}$ be the map classifying $\eta$. As $\eta$ corresponds to a formal group law of height strictly less than $n+1, P^{\prime}$ factors through $\mathcal{M}_{F G}^{<n+1}$ as

$$
\operatorname{Spec}\left(E(n)_{*}\right) \xrightarrow{P} \mathcal{M}_{F G}^{<n+1} \rightarrow \mathcal{M}_{F G}
$$

In view of theorem 1.40, it suffices to show that $P$ is affine and faithfully flat and that

$$
\operatorname{Spec}\left(E(n)_{*}\right) \times_{P, \mathcal{M}_{F G}^{<n+1}, P} \operatorname{Spec}\left(E(n)_{*}\right) \cong \operatorname{Spec}\left(E(n)_{*}(E(n))\right)
$$

As height stays unchanged under isomorphisms of formal groups,

$$
\operatorname{Spec}\left(E(n)_{*}\right) \times_{P, \mathcal{M}_{F G}^{<n+1}, P} \operatorname{Spec}\left(E(n)_{*}\right) \simeq \operatorname{Spec}\left(E(n)_{*}\right) \times_{P^{\prime}, \mathcal{M}_{F G}, P^{\prime}} \operatorname{Spec}\left(E(n)_{*}\right)
$$

We know that the latter is given by $\operatorname{Spec}\left(E(n)_{*} \otimes_{L} W \otimes_{L} E(n)_{*}\right)$. By Landweber exactness, this is precisely $\operatorname{Spec}\left(E(n)_{*}\left(E_{*}(n)\right)\right)$.
It remains to see that the base change of $P$ against any morphism $f: \operatorname{Spec}(S) \rightarrow \mathcal{M}_{F G}^{<n+1}$ is faithfully flat and affine. By base change, this is clear if $f$ factors through $P$ as the source map $s: \operatorname{Spec}\left(E(n)_{*}\left(E_{*}(n)\right) \rightarrow\right.$ $\operatorname{Spec}\left(E(n)_{*}\right)$ is faithfully flat by proposition 2.59 . The general case follows from the usual descent arguments and the observation that any morphism $f: \operatorname{Spec}(S) \rightarrow \mathcal{M}_{F G}^{<n+1}$ factors locally through $\operatorname{Spec}\left(E(n)_{*}\right)$ as it locally corresponds to a formal group law of height strictly less than $n+1$.

# 2.3 Proof of the Algebraic Landweber Theorem (Thm. 2.43) 

We will now give a proof of theorem 2.43. We follow the strategy from [15, Lect. 16], adding a lot of detail. Begin by considering an $L$-module $M$ that is Landweber exact. The aim is to show that it is flat over $\mathcal{M}_{F G}$. First, we reduce to checking flatness of the localisation at each prime over the localised stack as made precise in the next lemma.

Lemma 2.63. An $L$-module $M$ is flat over $\mathcal{M}_{F G}$ if and only if for each prime $p, M_{(p)}$ is flat over $\mathcal{M}_{F G} \times \mathbb{Z}_{(p)}$.

Proof. Recall that $\mathcal{M}_{F G} \times \operatorname{Spec}\left(\mathbb{Z}_{(p)}\right) \cong\left[\left(L_{(p)}, W_{(p)}\right)\right]$. By lemma $2.23, M$ is flat over $\mathcal{M}_{F G}$ if and only if $M \otimes_{L} W$ is a flat $L$-module. As $\left\{\operatorname{Spec}\left(\mathbb{Z}_{(p)}\right) \rightarrow \operatorname{Spec}(\mathbb{Z})\right\}_{p \text { prime }}$ is a Zariski cover and flatness can be checked Zariski locally, $M \otimes_{L} W$ is a flat $L$-module if and only if $\left(M \otimes_{L} W\right)_{(p)}=M_{(p)} \otimes_{L_{(p)}} W_{(p)}$ is a flat $L_{(p)}$-module. This is precisely the condition of $M_{(p)}$ being flat over $\mathcal{M}_{F G} \times \operatorname{Spec}\left(\mathbb{Z}_{(p)}\right)$ for all primes $p$.

Hence, it suffices to show that $M_{(p)}$ is flat over $\mathcal{M}_{F G} \times \operatorname{Spec}\left(\mathbb{Z}_{(p)}\right)$. For the remainder of the section, we fix an arbitrary prime $p$ and let $M$ denote an $L_{(p)}$-module which is Landweber exact at $p$.
We proceed in two main steps. First, we reduce the statement of flatness over $\mathcal{M}_{F G} \times \operatorname{Spec}\left(\mathbb{Z}_{(p)}\right)$ to an algebraic statement by exploiting example 2.30 . This will be how the $v_{i}$ come into play. All the tools needed for this are already in our hands. Understanding the algebraic statement is subdivided into three steps: a small argument to restrict to a finitely generated ring, a lemma that will allow inductive reasoning and some observations on the moduli stack of formal groups of height exactly $m$. This will be made more precise in due time.

Throughout this subsection, we will always write $R:=\operatorname{Spec}\left(\mathbb{Z}_{(p)}\left[v_{1}, v_{2}, \ldots\right]\right)$ and $c_{p}$ for the presentation of $\mathcal{M}_{F G} \times \operatorname{Spec}\left(\mathbb{Z}_{(p)}\right)$ introduced after example 2.30. As in that example, we define

$$
B:=\mathbb{Z}_{(p)}\left[v_{1}, v_{2}, \ldots\right]\left[b_{0}^{k}, b_{i} \mid i=p^{k}+1\right] \cong R \otimes_{L} W
$$

and by $q$ we will always refer to the faithfully flat morphism $q: \operatorname{Spec}(R) \rightarrow \mathcal{M}_{F G} \times \operatorname{Spec}\left(\mathbb{Z}_{(p)}\right)$ from lemma 2.31 .

Lemma 2.64. $M$ is flat over $\mathcal{M}_{F G} \times \operatorname{Spec}\left(\mathbb{Z}_{(p)}\right)$ if and only if the $R$-module $q^{*}\left(c_{p_{*}}(M)\right)=M \otimes_{L_{(p)}} B$ is flat over $R$.

Proof. This is clear from combining that $q$ is faithfully flat as shown in lemma 2.31 with proposition 2.20 .

For simplicity of notation, we will denote $M \otimes_{L_{(p)}} B$ by $M_{B}$ in what follows.
Now comes the point where one no longer gets away with formal considerations and has to dive into the commutative algebra surrounding $L$. We have just reduced to checking that $M_{B}$ is a flat $\mathbb{Z}_{(p)}\left[v_{1}, v_{2}, \ldots\right]-$ module. Even though this ring is considerably smaller than $L_{(p)}$, it is still infinitely generated and the next step is to reduce to checking flatness over finitely generated rings.

Lemma 2.65. To show that $M_{B}$ is a flat $\mathbb{Z}_{(p)}\left[v_{1}, v_{2}, \ldots\right]$-module, it suffices to show that it is a flat $\mathbb{Z}_{(p)}\left[v_{1}, v_{2}, \ldots, v_{n}\right]$-module along the inclusion $\mathbb{Z}_{(p)}\left[v_{1}, v_{2}, \ldots, v_{n}\right] \hookrightarrow \mathbb{Z}_{(p)}\left[v_{1}, v_{2}, \ldots\right]$ for all $n \in \mathbb{N}$.
Proof. Flatness of $M_{B}$ as $R$-module can be rephrased as requiring that for any $R$-module $N$ and all $i>0, \operatorname{Tor}_{i}^{R}\left(N, M_{B}\right)=0$. As this functor commutes with filtered colimits and any module can be obtained as filtered colimit over finitely presented modules, it suffices to show the statement for $N$ any finitely presented $R$-module. This means that there exist some integers $l, m>0$ such that there is a short exact sequence $R^{\oplus m} \xrightarrow{\alpha} R^{\oplus l} \rightarrow N \rightarrow 0$. Let $\left\{a_{k}\right\}_{k \leq m}$ denote a basis for $R^{\oplus m}$. Then, $N \cong R^{\oplus l} /\left(\alpha\left(a_{k}\right) \mid k \leq m\right)$. Observe that $\left(\alpha\left(a_{k}\right) \mid k \leq m\right)$ can reference only finitely many $v_{i}$. Hence, we can write $N \cong N_{0}\left[v_{n+1}, v_{n+2}, \ldots\right]$ where $n$ is the biggest integer such that $v_{n}$ appears in $\left(\alpha\left(a_{k}\right) \mid k \leq m\right)$ and $N_{0}$ is a $\mathbb{Z}_{(p)}\left[v_{1}, v_{2}, \ldots, v_{n}\right]$-module (more precisely $N_{0}=\mathbb{Z}_{(p)}\left[v_{1}, v_{2}, \ldots, v_{n}\right]^{\oplus l} /\left(\alpha\left(a_{k}\right) \mid k \leq m\right)$. Now one uses the fact that for a faithfully flat ring map $S \rightarrow R$, an $R$-module $M$ and an $S$-module $N_{0}$ it holds that $\operatorname{Tor}_{i}^{S}\left(N_{0}, M\right) \cong \operatorname{Tor}_{i}^{R}\left(N \otimes_{S} R, M\right)$ (see $\left[22\right.$, Tag $\left.00 \mathrm{M} 7\right]$ ). Setting $S=\mathbb{Z}_{(p)}\left[v_{1}, v_{2}, \ldots, v_{n}\right]$, $R=\mathbb{Z}_{(p)}\left[v_{1}, v_{2}, \ldots\right]$ and $M=M_{B}$, this yields

$$
\operatorname{Tor}_{i}^{R}\left(N=N_{0} \otimes_{R} S, M_{B}\right)=\operatorname{Tor}_{i}^{\mathbb{Z}_{(p)}\left[v_{1}, v_{2}, \ldots, v_{n}\right]}\left(N_{0}, M_{B}\right)
$$

Hence, we have reduced to showing that $M_{B}$ is flat over $\mathbb{Z}_{(p)}\left[v_{1}, v_{2}, \ldots, v_{n}\right]$ for all $n \in \mathbb{N}$.

For simplicity of notation, we will write $R_{n}:=\mathbb{Z}_{(p)}\left[v_{1}, v_{2}, \ldots, v_{n}\right]$ in what follows.
We are now in a good position to reason inductively. We aim to make use of the following lemma from commutative algebra.

Lemma 2.66 ([15, Lect. 16, Lem. 4]). Let $R$ be a commutative ring containing a nonzero-divisor $x$. Let $M$ be an $R$-module. Then, $M$ is flat over $R$ if and only if the following three conditions hold:

1. The element $x$ is a nonzero-divisor on $M$.
2. The quotient $M / x M$ is a flat $R /(x)$-module.
3. The module $M\left[x^{-1}\right]$ is flat over $R\left[x^{-1}\right]$.

In order to do so, we introduce the ideal $I_{m}:=\left(v_{0}, v_{1}, \ldots, v_{m-1}\right) \subseteq B$, and consider the $R_{n} / I_{m}$-module $M_{B} / I_{m} M_{B}$. For simplicity of notation, we will write $R_{n} / I_{m}:=R_{n, m}$. Observe that $M_{B} / I_{0} M_{B}=M_{B}$, $R_{n, 0}=\mathbb{Z}_{(p)}\left[v_{1}, v_{2}, \ldots, v_{n}\right]:=R_{n}$ and $R_{n, n+1}=\mathbb{F}_{p}$. In particular, $M_{B} / I_{n+1} M_{B}$ is a flat $R_{n, n+1}$-module since it is an $\mathbb{F}_{p}$ vector space. So if we could show by downward induction that $M_{B} / I_{m} M_{B}$ is a flat $R_{n, m}$-module, we would get that $M_{B}$ is a flat $R_{n}$ module for each $n$ which is all that remained to show.

Lemma 2.67. For any $m \leq n+1$, the quotient $M_{B} / I_{m} M_{B}$ is a flat $R_{n, m}$-module.
Proof. As announced, we proceed by downward induction and aim to apply lemma 2.66. We have already argued that the case $m=n+1$ is clear.
As we assumed that the $v_{i}$ form a regular sequence on $M$, it makes sense to choose $v_{m} \in M_{B} / I_{m} M_{B}$ to play the role of $x$ from lemma 2.66. Indeed, $v_{m}$ is a nonzero divisior on $M /\left(p, v_{1}, v_{2}, \ldots, v_{m-1}\right) M$ because it is part of a regular sequence. Flatness of $B$ over $L_{(p)}$ ensures that $v_{m}$ is also not a zero divisor on $M_{B} / I_{m} M_{B}=M \otimes_{L_{(p)}} B /\left(p, v_{1}, v_{2}, \ldots, v_{m-1}\right) M \otimes_{L_{(p)}} B \cong M /\left(p, v_{1}, v_{2}, \ldots, v_{m-1}\right) M \otimes_{L_{(p)}} B$. Hence, the first condition of lemma 2.66 is satisfied.
The second condition is fulfilled as by inductive assumption $\left(M_{B} / I_{m} M_{B}\right) /\left(v_{m}\right) \cong M_{B} / I_{m+1} M_{B}$ is flat over $R_{n, m+1} \cong R_{n, m} /\left(v_{m}\right)$.
It remains to show that $M_{B} / I_{m} M_{B}\left[v_{m}^{-1}\right]$ is flat over $R_{n, m}\left[v_{m}^{-1}\right]$. Actually, one can show that $M_{B} / I_{m} M_{B}\left[v_{m}^{-1}\right]$ is already flat over $R / I_{m}\left[v_{m}^{-1}\right]$. This is the content of lemma 2.68 which itself requires lemmas 2.69 and theorem 2.70. Thus, modulo lemma 2.68, all three conditions of lemma 2.66 are fulfilled.

It remains to show:
Lemma 2.68 ([15, Lect. 16, Claim 3]). For any integer $m \geq 0$, the module $M_{B} / I_{m} M_{B}\left[v_{m}^{-1}\right]$ is flat over $R / I_{m}\left[v_{m}^{-1}\right]$.

This will in turn follow from:
Lemma 2.69 ([15, Lect. 16, Claim 6]). Every quasicoherent sheaf on $\mathcal{M}_{F G}^{m}$ is flat.
For its proof we require the following technical statement:
Theorem 2.70 ([15, Thm 1, Lect 14]). Let $f(x, y), f^{\prime}(x, y) \in A[[x, y]]$ be formal group laws of height exactly $n>0$ and let $S$ be the ring that classifies isomorphisms between $f$ and $f^{\prime}$, i.e. $S=A\left[b_{0}^{+1}, b_{1}, b_{2}, \ldots\right] / I$, where $I$ is the ideal generated by all coefficients in the power series $f(g(x), g(y))-g\left(f^{\prime}(x, y)\right)$, where $g(t)=b_{0} t+b_{1} t^{2}+\ldots$. Then $S$ is isomorphic to the direct limit of a system of (injective) finite étale maps $A=A(1) \hookrightarrow A(2) \hookrightarrow \ldots$
Proof of lemma 2.69. Let $M \in Q \operatorname{Coh}\left(\mathcal{M}_{F G}^{m}\right)$. We need to show that, for every morphism $f: \operatorname{Spec}(A) \rightarrow$ $\mathcal{M}_{F G}^{m}, f^{*}(M)$ is a flat $A$-module. As usual, up to replacing $A$ by some covering, we may assume that $f$ factors through $\operatorname{Spec}(L)$ i.e. that $f$ represents a formal group law of height $m$.
We first treat the case when $m>0$. Let $\beta: \operatorname{Spec}\left(\mathbb{F}_{p}\right) \rightarrow \mathcal{M}_{F G}^{m}$ be a morphism classifying some formal group law of height $m$. Consider the pullback diagram
![img-53.jpeg](img-53.jpeg)

Since $f$ classifies a formal group law of height $m>0, v_{0}=p=0 \in A$ i.e. $A$ is an $\mathbb{F}_{p}$-algebra. In particular, we can see $\beta$ as a formal group law on $A$ by including $\mathbb{F}_{p}$ into $A$. Then, by the definition

of pullbacks of stacks, $S$ classifies the isomorphisms of formal group laws between $f$ and $\beta$. Hence, theorem 2.70 applies and gives that $f^{\prime}$ is étale. In particular, $f^{\prime}$ is faithfully flat. So, by lemma 2.16, it suffices to show that $f^{*}(M) \otimes_{A} S$ is a flat $S$-module. Now comes the usual quasi-coherence argument: $f^{*}(M) \otimes_{A} S \cong M\left(f \circ f^{\prime}\right) \cong M\left(\beta \circ \beta^{\prime}\right) \cong \beta^{*}(M) \otimes_{\mathbb{F}_{p}} S$. Thus, it suffices to show that $\beta^{*}(M) \otimes_{\mathbb{F}_{p}} S$ is a flat $S$-module. As $\beta^{\prime}$ is faithfully flat (any module over a field is flat and $\operatorname{Spec}(S) \rightarrow \operatorname{Spec}\left(\mathbb{F}_{p}\right)$ is surjective as $\operatorname{Spec}\left(\mathbb{F}_{p}\right)$ consists of a single point), the latter is equivalent to $\beta^{*}(M)$ being a flat $\mathbb{F}_{p}$-module. This is true since $\mathbb{F}_{p}$ is a field.
Let us now turn to the case $m=0$. Observe that a ring $A$ admitting a formal group law of height 0 must be a $\mathbb{Q}$-algebra, since $v_{0}=p$ must be invertible for all primes $p$. Furthermore, recall that over a $\mathbb{Q}$-algebra all formal groups laws are isomorphic ([19, Thm. A2.1.6]). Let $\beta: \mathbb{Q} \rightarrow \mathcal{M}_{F G}^{0}$ classify the additive formal group law and consider the following pullback diagram
![img-54.jpeg](img-54.jpeg)

It remains to show that $f^{\prime}$ is faithfully flat, before concluding as in the previous case. Recall that $S$ classifies the isomorphisms between $f$ and $\beta$, but since all formal group laws over $\mathbb{Q}$-algebras are isomorphic, $S$ does not depend on $f$ and $\beta$. Hence, to determine $S$ we may assume that $f$ classifies the additive formal group law as well. Moreover, $S$ is also the pullback in the following diagram
![img-55.jpeg](img-55.jpeg)

Here, we know that $S=A \otimes_{L} W \otimes_{L} \mathbb{Q}$ where both $A$ and $\mathbb{Q}$ are seen as $L$-modules via the additive formal group law. Unraveling the definitions in the case gives $S \cong A\left[b_{0}^{ \pm}, b_{1}, b_{2}, \ldots\right]$ which is faithfully flat over $A$ as wanted.

Proof of lemma 2.68. The pullback diagram
![img-56.jpeg](img-56.jpeg)
from example 2.30 and lemma 2.31 induces a pullback diagram
![img-57.jpeg](img-57.jpeg)

The stack $\mathcal{M}_{F G}^{m}$ appears here as $\operatorname{Spec}\left(L / I_{m}\left[v_{m}^{-1}\right]\right)$ precisely classifies formal group laws of height $m$. By lemma 2.69, the $\operatorname{Spec}\left(L_{(p)} / I_{m}\left[v_{m}^{-1}\right]\right)$-module $M / I_{m} M\left[v_{m}^{-1}\right]$ is flat over $\mathcal{M}_{F G}^{m}$. In particular,

$$
q^{*}\left(\gamma_{*}\left(M / I_{m} M\left[v_{m}^{-1}\right]\right)\right)=M / I_{m} M\left[v_{m}^{-1}\right] \otimes_{\operatorname{Spec}\left(L_{(p)} / I_{m}\left[v_{m}^{-1}\right]\right)} B / I_{m}\left[v_{m}^{-1}\right] \cong M_{B} / I_{m} M_{B}\left[v_{m}^{-1}\right]
$$

is a flat $\mathbb{Z}_{(p)}\left[v_{1}, v_{2}, \ldots\right] /\left(p, v_{1}, \ldots, v_{m-1}\right)\left[v_{m}^{-1}\right]$-module as wanted.
This was a long argument, so let us summarise the main steps again:

1. Reduce flatness of $M$ over $\mathcal{M}_{F G} \times \operatorname{Spec}\left(\mathbb{Z}_{(p)}\right)$ to an algebraic statement, namely to flatness of $M \otimes_{L_{(p)}} B:=M_{B}$ over $\mathbb{Z}_{(p)}\left[v_{1}, v_{2}, \ldots\right]$ (lemma 2.64). This exploits example 2.30 and proposition 2.20 .

2. Reduce to flatness of $M_{B}$ over $\mathbb{Z}_{(p)}\left[v_{1}, v_{2}, \ldots, v_{n}\right]:=R_{n}$ for all $n$ (lemma 2.65).
3. Show inductively for each $m \leq n+1$ that $M_{B} /\left(p, v_{1}, \ldots, v_{m-1}\right) M_{B}:=M_{B} / I_{m} M_{B}$ is flat over $\mathbb{Z}_{(p)}\left[v_{1}, v_{2}, \ldots, v_{n}\right] /\left(p, v_{1}, \ldots, v_{m-1}\right):=R_{n, m}$; the base case $m=n+1$ being clear because all modules over $\mathbb{F}_{p}$ are flat. The case $m=0$ yields the desired statement. For the inductive step, use an algebraic characterisation of flatness given in lemma 2.66 and the assumption of the $v_{i}$ forming a regular sequence on $M$. The conditions given in lemma 2.66 are fulfilled because

- $v_{m}$ is not a zero divisor on $M_{B} / I_{m} M_{B}$ because the $v_{i}$ form a regular sequence and $B$ is a flat $L_{(p)}$-module.
- $\left(M_{B} / I_{m} M_{B}\right) /\left(v_{m}\right) \cong M_{B} / I_{m+1} M_{B}$ is flat over $R_{n, m} /\left(v_{m}\right) \cong R_{n, m+1}$ by inductive assumption.
- $M_{B} / I_{m} M_{B}\left[v_{m}^{-1}\right]$ is flat over $R_{n, m}\left[v_{m}^{-1}\right]$ as it is already flat over $R /\left(p, v_{1}, \ldots, v_{m-1}\right)$ (lemma 2.68). This follows from the fact that any quasicoherent sheaf over the moduli stack of formal groups of height exactly $m$ is flat (lemma 2.69) whose proof relied on theorem 2.70.

The converse is a lot easier. Namely, if $M$ is an $L$-module that is flat over $\mathcal{M}_{F G}$ i.e. $M_{(p)}$ is flat over $\mathcal{M}_{F G} \times \operatorname{Spec}\left(\mathbb{Z}_{(p)}\right)$ for all primes $p$. By definition, this implies that $c_{p_{*}}\left(M_{(p)}\right)(q)=M_{(p)} \otimes_{L_{(p)}} B$ is flat over $\mathbb{Z}_{(p)}\left[v_{1}, v_{2}, \ldots\right]$. The $v_{i}$ form a regular sequence on $\mathbb{Z}_{(p)}\left[v_{1}, v_{2}, \ldots\right]$ i.e. for each $i$ there are short exact sequences

$$
0 \rightarrow \mathbb{Z}_{(p)}\left[v_{1}, v_{2}, \ldots\right] /\left(p, v_{1}, \ldots, v_{i-1}\right) \xrightarrow{v_{i}} \mathbb{Z}_{(p)}\left[v_{1}, v_{2}, \ldots\right] /\left(p, v_{1}, \ldots, v_{i-1}\right) \rightarrow \mathbb{Z}_{(p)}\left[v_{1}, v_{2}, \ldots\right] /\left(p, v_{1}, \ldots, v_{i}\right) \rightarrow 0
$$

These sequences remain exact when applying $(-) \otimes_{\mathbb{Z}_{(p)}\left[v_{1}, v_{2}, \ldots\right]} c_{p_{*}}\left(M_{(p)}\right)(q)$ to give exact sequences

$$
0 \longrightarrow M_{(p)} / I_{i} M_{(p)} \otimes_{L_{(p)}} B \xrightarrow{-v_{i}} M_{(p)} / I_{i} M_{(p)} \otimes_{L_{(p)}} B \longrightarrow M_{(p)} / I_{i} M_{(p)} \otimes_{L_{(p)}} B \longrightarrow 0
$$

which can be also seen as exact sequences of $L_{(p)}$-modules. Finally, as $B$ is faithfully flat over $L_{(p)}$, the $v_{i}$ form a regular sequence on $M$.

Note that this proof showed in particular that a morphism $\operatorname{Spec}(R) \rightarrow \mathcal{M}_{F G} \times \operatorname{Spec}\left(\mathbb{Z}_{(p)}\right)$ is flat if and only if the $v_{i}$ form a regular sequence on $R$. Remembering from example 2.60 that $\mathcal{M}_{F G} \times \operatorname{Spec}\left(\mathbb{Z}_{(p)}\right)$ is also equivalent to the stack $\left[\left(B P_{*}, B P_{*}(B P)\right)\right]$ yields the Landweber exact functor theorem for $B P$ :

Corollary 2.71. Let $F: B P_{*} \rightarrow R$ be graded and let $h_{F}: h S p \rightarrow A b$ be the functor defined by $X \mapsto B P_{*}(X) \otimes_{B P_{*}} R$. Then $h_{F}$ is a homology theory if for every prime $p$ the sequence $p, v_{1}, v_{2}, \ldots$ is regular on $R$.

# 2.4 Landweber exactness for $P(n)$ 

For each natural number $n$ and each prime $p$, there is one spectrum of Adams type that is close enough to $M U$ for flatness over its associated to stack to be a verifiable criterion, but far enough away to not be Landweber exact. In this subsection, we exploit the previously set up formalism to explore another version of Landweber exactness. To our knowledge, this was first proven by Nobuaki Yagita in [26]. The approach taken here is different, but, as it follows easily from well-known results, probably also well-known. Let us introduce our main player:

Definition 2.72. Fix a prime $p$. For each $k \leq 1$, let $x_{k}: \mathbb{S}[2 k] \rightarrow M U_{(p)}$ be a map of spectra representing $x_{k} \in \pi_{2 k}\left(M U_{(p)}\right)$. This is adjoint to a map of $M U$-modules $M U[2 k] \rightarrow M U_{(p)}$ which in turn factors through a map of $M U_{(p)}$-modules $t_{k}: M U_{(p)}[2 k] \rightarrow M U_{(p)}$. Set $C(k):=\operatorname{cof} i b\left(t_{k}\right)$ where the cofiber is taken in the category of $M U_{(p)}$-modules. Then, for each integer $n$, define the spectrum $P(n):=\bigotimes_{M U_{(p)}, k \neq p^{m}-1, m<n} C(k)$.

Observe that $P(0)=B P$. Let us fix a prime $p$ different from 2 for the remainder of this section. The case when $p=2$ is slightly different as $P(n)_{*}(P(n))$ has a different description at this prime 2 (see [25, Thm 2.2]). We will ignore this case.
The homotopy groups of $P(n)$ are easily calculated to be $P(n)_{*}=\mathbb{Z}_{(p)}\left[v_{n}, v_{n+1}, \ldots\right]$. This can for example be done by induction on $k$ using that $\pi_{*}(C(k))=L_{(p)} /\left(x_{k}\right)$. Furthermore,

Theorem 2.73 ([25, Thm 2.2]). For any prime $p, P(n)_{*}(P(n))$ is a flat Hopf algebroid over $P(n)_{*}$. If $p$ is odd, there is an isomorphism of left $P(n)_{*}$-algebras

$$
P(n)_{*}(P(n)) \cong P(n)_{*} \otimes_{B P_{*}} B P_{*}(B P) \otimes E\left(a_{0}, a_{1}, \ldots, a_{n-1}\right)
$$

where $E\left(a_{0}, a_{1}, \ldots, a_{n-1}\right)$ is an exterior algebra in generators $a_{i}$ of degree $2 p^{i}-1$. Modulo the generators $a_{i}$, the Hopf algebroid $\left(P(n)_{*}, P(n)_{*}(P(n)\right)$ is, for all primes, isomorphic to the Hopf algebroid $\left(B P_{*} / I_{n}, B P_{*}(B P) / I_{n}\right)$ with $I_{n}:=\left(v_{0}, \ldots, v_{n-1}\right)$ as in the previous subsection.
That $\left(B P_{*} / I_{n}, B P_{*}(B P) / I_{n}\right) \cong\left[\left(\mathbb{F}_{p}\left[v_{n}, v_{n+1}, \ldots\right], \mathbb{F}_{p}\left[v_{n}, v_{n+1}, \ldots\right]\left[u^{ \pm}, b_{i} \mid i+1=p^{k}\right]\right)\right]$ is a flat Hopf algebroid as implied in that theorem follows from the following proposition and the fact that $\left(B P_{*}, B P_{*}(B P)\right)$ is a flat Hopf algebroid by proposition 2.59 .
Proposition 2.74 ([9, Prop. 1.4.11]). If $(A, \Gamma)$ is a flat Hopf algebroid, then for any invariant ideal I the pair $(A / I, \Gamma / I)$ is a flat Hopf algebroid as well.
We can identify the stack associated to the Hopf algebroid $\left(B P_{*} / I_{n}, B P_{*}(B P)\left[u^{ \pm}\right] / I_{n}\right)$.
Proposition 2.75. Let $P^{\prime}: \operatorname{Spec}\left(\mathbb{F}_{p}\left[v_{n}, v_{n+1}, \ldots\right]\right) \rightarrow \mathcal{M}_{F G}$ be the map classifying the formal group law $L \rightarrow L_{(p)} \rightarrow \mathbb{F}_{p}\left[v_{n}, v_{n+1}, \ldots\right]$. As this has height $\geq n, P^{\prime}$ factors through $\mathcal{M}_{F G}^{\geq n}$. Denote this factorisation by $P: \operatorname{Spec}\left(\mathbb{F}_{p}\left[v_{n}, v_{n+1}, \ldots\right]\right) \rightarrow \mathcal{M}_{F G}^{\geq n}$. Then $\mathcal{M}_{F G}^{\geq n}$ is an algebraic stack with presentation $P$ and the rigidified algebraic stack $\left(\mathcal{M}_{F G}^{\geq n}, P\right)$ is equivalent to $\left[\left(B P_{*} / I_{n}, B P_{*}(B P)\left[u^{ \pm}\right] / I_{n}\right)\right)\right]$.
Proof. This proof is analogous to the proof of proposition 1.68 and will therefore be omitted.
Notice that the Hopf algebroid $\left(P(n)_{*}, P(n)_{*}(P(n))\left[u^{ \pm}\right]\right)$ is very similar to $\left(B P_{*} / I_{n}, B P_{*}(B P)\left[u^{ \pm}\right] / I_{n}\right)$. Only the second term differs by an exterior algebra. Hence, to understand flatness over the stack $\left[\left(P(n)_{*}, P(n)_{*}(P(n))\left[u^{ \pm}\right]\right)\right]$, we begin by understanding flatness over $\left[\left(B P_{*} / I_{n}, B P_{*}(B P)\left[u^{ \pm}\right] / I_{n}\right)\right]$.
Theorem 2.76. Let $M$ be a module over $B P_{*} / I_{n}$. Then, $M$ is flat over $\left[\left(B P_{*} / I_{n}, B P_{*}(B P)\left[u^{ \pm}\right] / I_{n}\right)\right]$ if and only if the elements $\left(v_{n}, v_{n+1}, v_{n+2}, \ldots\right) \in B P_{*} / I_{n}$ form a regular sequence for $M$.
Proof. The argument is exactly the same as the proof of theorem 2.43, except that now we always consider $m \geq n$ and instead of inducting down to zero we induct down to $n$. Let us give some more detail. Suppose the $v_{i}$ form a regular sequence for $M$. For simplicity of notation, write $B P_{*}(B P)\left[u^{ \pm}\right] / I_{n}:=B_{n}$. By lemma 2.23, it suffices to show that $M \otimes_{B P_{*} / I_{n}} B_{n}:=M_{B_{n}}$ is a flat $B P_{*} / I_{n}$-module. Observe that $B_{n}$ is a polynomial ring over $B P_{*} / I_{n}$ and is thus faithfully flat over it. The same proof as that of lemma 2.65 goes through, adapting the indices of the $v_{i}$, and proves that it suffices to show that $M \otimes_{B P_{*} / I_{n}} B_{n}$ is a flat $\mathbb{F}_{p}\left[v_{n}, v_{n+1}, \ldots, v_{l}\right]$-module for all $l \geq n$. Then, we consider the ideal $I_{n, m}=\left(v_{n}, \ldots, v_{m-1}\right) \subseteq B_{n}$ (which is trivial if $m \leq n$ ) and, for $l \geq m$, the $R_{n, m, l}:=\mathbb{F}_{p}\left[v_{n}, \ldots, v_{l}\right] / I_{n, m}$-module $M_{B_{n}} / I_{m, n} M_{B_{n}}$. As before, we aim to show by downward induction on $m$ that $M_{B_{n}} / I_{m, n} M_{B_{n}}$ is a flat $R_{n, m, l}$-module. The case $m=n$ is what we want to show, the case $m=l+1$ is clear as $R_{n, l+1, l}=\mathbb{F}_{p}$ is a field. We apply lemma 2.66 with $x=v_{m}$ and the argument is exactly the same as before. The converse is also analogous, except that now we do not even need to check the $p$-localisations for all primes, but we just work locally at the chosen prime.

From this, we deduce the result for $P(n)$.
Theorem 2.77. Let $M$ be a module over $P(n)_{*}$. Then, $M$ is flat over $\left[\left(P(n)_{*}, P(n)_{*}(P(n))\left[u^{ \pm}\right]\right)\right]$ if and only if the elements $\left(v_{n}, v_{n+1}, v_{n+2}, \ldots\right) \in P(n)_{*}$ form a regular sequence for $M$.
By corollary 2.28 , the following is immediate:
Corollary 2.78 (Landweber Exact Functor Theorem for $P(n)$ ). Let $F$ be a graded formal group law of height $\geq n$ over a graded ring $R$ (i.e. some morphism $P(n)_{*} \rightarrow R$ ) and let $h_{F}: h S p \rightarrow A b$ be the functor defined by $X \mapsto P(n)_{*}(X) \otimes_{P(n)_{*}} R$. Then $h_{F}$ is a homology theory if the sequence $v_{n}, v_{n+1}, \ldots$ is regular on $R$.
Proof of thm 2.77. By lemma 2.23, the module $M$ is flat over $\left[\left(P(n)_{*}, P(n)_{*}(P(n))\left[u^{ \pm}\right]\right)\right]$ if and only if $M \otimes_{P(n)_{*}} P(n)_{*}(P(n))\left[u^{ \pm}\right]$ is a flat $P(n)_{*}$-module. As $P(n)_{*} \cong B P_{*} / I_{n}$,

$$
P(n)_{*} \otimes_{B P_{*}} B P_{*}(B P) \cong B P_{*}(B P) / I_{n} \text { and } P(n)_{*}(P(n))=B P_{*}(B P) / I_{n} \otimes E\left(a_{0}, a_{1}, \ldots, a_{n-1}\right)
$$

By theorem 2.76, $M \otimes_{P(n)_{*}} B P_{*}(B P) / I_{n}$ is a flat $P(n)_{*}$-module if and only if $v_{n}, v_{n+1}, v_{n+2}, \ldots$ forms a regular sequence for $M$. As $M \otimes_{P(n)_{*}} P(n)_{*}(P(n)) \cong M \otimes_{P(n)_{*}} B P_{*}(B P) / I_{n} \otimes E\left(a_{0}, a_{1}, \ldots, a_{n-1}\right)$ is a flat $P(n)_{*}$-module if and only if $M \otimes_{P(n)_{*}} B P_{*}(B P) / I_{n}$ is, the theorem follows.

Example 2.79. Recall from example 2.58 that Morava K-theory, $K(n)$, is not Landweber exact as $K(n)_{*}=\mathbb{F}_{p}\left[v_{n}^{ \pm}\right]$is $p$-torsion and, more generally, all the $v_{i}$ for $i<n$ are zero. Using $P(n)$, there is a way to circumvent this obstruction. By theorem $2.77, \mathbb{F}_{p}\left[v_{n}^{ \pm}\right]$seen as $P(n)_{*}$-module via the morphism $\mathbb{F}_{p}\left[v_{n}, v_{n+1}, \ldots\right] \rightarrow \mathbb{F}_{p}\left[v_{n}^{ \pm}\right]$is $P(n)$-Landweber exact as $v_{n}$ is invertible in $\mathbb{F}_{p}\left[v_{n}^{ \pm}\right]$and thus $v_{n}, 0, \ldots$ forms a regular sequence. In particular, by corollary 2.56 , for any spectrum $X$, there is an isomorphism $K(n)_{*}(X) \cong P(n)_{*}(X) \otimes_{P(n)_{*}} \mathbb{F}_{p}\left[v_{n}^{ \pm}\right]$. For odd primes, using theorem 2.73 , this gives a way to calculate $\pi_{*}(K(n) \otimes K(n)):$

$$
\begin{aligned}
K(n)_{*}(K(n)) & \cong P(n)_{*}(K(n)) \otimes_{P(n)_{*}} \mathbb{F}_{p}\left[v_{n}^{ \pm}\right] \\
& \cong P(n)_{*}(P(n)) \otimes_{P(n)_{*}} \mathbb{F}_{p}\left[v_{n}^{ \pm}\right] \otimes_{P(n)_{*}} \mathbb{F}_{p}\left[v_{n}^{ \pm}\right] \\
& =P(n)_{*} \otimes_{B P_{*}} B P_{*}(B P) \otimes E\left(a_{0}, a_{1}, \ldots, a_{n-1}\right) \otimes_{P(n)_{*}} \mathbb{F}_{p}\left[v_{n}^{ \pm}\right] \otimes_{P(n)_{*}} \mathbb{F}_{p}\left[v_{n}^{ \pm}\right] \\
& \cong \mathbb{F}_{p}\left[v_{n}^{ \pm}\right]\left[t_{1}, t_{2}, \ldots\right] /\left(v_{n} t_{i}^{p^{n}}-v_{n}^{p^{i}} t_{i}\right) \otimes E\left(a_{0}, a_{1}, \ldots, a_{n-1}\right)
\end{aligned}
$$

For details on the last identification, see [27, Ex.1].

# 3 Elliptic Cohomology 

As promised in the previous section, we will now look into how the Landweber exact functor theorem and, more generally, the stacky formalism, give interesting spectra arising from algebraic geometry. We would like to define a map into the moduli stack of formal groups, hence we need an object to which one can naturally associate a formal group. A well-known source of formal group laws are elliptic curves. We begin by introducing elliptic curves over a field and explain how these give rise to formal group laws, then we generalise the discussion to elliptic curves over an arbitrary base scheme. Finally, we consider the moduli stack of elliptic curves, which we will also show to be algebraic, and briefly discuss the interplay between that and the moduli stack of formal groups. As our main focus lies on the question of how to apply these algebro-geometric concepts to topology, we will not prove many of the theorems specific to elliptic curves and instead give references and examples.

### 3.1 Elliptic Curves over a Field

Let us first consider the simple case of an elliptic curve over a field. Recall that a curve is a separated, integral scheme of finite type over some field $k$ and of dimenison 1.

Definition 3.1. An elliptic curve over a field $k$ is a smooth proper curve $E$ of genus 1 together with a chosen base point $e \in E(k)$.

Recall that the $k$-rational points of $E$ correspond to sections of the structure morphism $E \rightarrow \operatorname{Spec}(k)$, hence we can also think of $e$ as such a section. This approach is important when we generalise the notion of elliptic curve over any base scheme. In the remainder of this subsection, all elliptic curves are implicitly defined over some field $k$ if not stated differently.
Elliptic curves admit a nice, explicit description by the following theorem.
Theorem 3.2 ([21, III Prop 3.1]). Any elliptic curve $(E, e)$ over a field $k$ can be embedded into $\mathbb{P}_{k}^{2}$ and is cut out by an equation of the form

$$
Y^{2} Z+a_{1} X Y Z+a_{3} Y Z=X^{3}+a_{2} X^{2} Z+a_{4} X Z^{2}+a_{6} Z^{3}
$$

with $[0: 1: 0]$ as the chosen base point. Moreover, any smooth cubic given by an equation of this form is elliptic.

The idea is to apply Riemann-Roch to the divisor $n \cdot e$ and to make dimensional considerations to get the relation (1), for details see [21, III Prop 3.1].

Figure 1: Some examples of rational points of elliptic curves over $\mathbb{R}$ ([21, Fig. 3.1]).
![img-58.jpeg](img-58.jpeg)

Definition 3.3. Equation (1) is called a Weierstrass equation. An elliptic curve expressed in this equation is said to be in Weierstrass form.

The previous theorem states that every elliptic curve (over a field) admits a Weierstrass form.

Remark 3.4. Often one gives the Weierstrass equation on the chart $\{Z=1\}$ where, dehomogenising, it can be rewritten as

$$
y^{2}+a_{1} x y+a_{3} y=x^{3}+a_{2} x^{2}+a_{4} x+a_{6}
$$

with $x=\frac{X}{Z}, y=\frac{Y}{Z}$. One has to keep in mind that the base point is not in this chart. We say it is at infinity. When the curve is in Weierstrass form, the base point $[0: 1: 0]$ is also denoted $O$ and called the origin. Observe that in this convention the line through a given point $\left(x_{0}, y_{0}\right)$ on the curve and the base point at infinity is vertical i.e. given by the equation $x=x_{0}$ and that the tangent to the elliptic curve at $O$ only intersects the curve in $O$.

It usually happens that one elliptic curve can be described by several Weierstrass equations. Indeed, there are changes of variables that preserve the base point and the form of the equation. This gives an isomorphic elliptic curve, but a different Weierstrass equation. Let us look at a specific example.

Example 3.5. When the characteristic of the field is not 2, we can simplify the Weierstrass equation by completing the square. Equation (2) then becomes

$$
\left(y+\frac{1}{2}\left(a_{1} x+a_{3}\right)\right)^{2}=x^{3}+\left(a_{2}+\frac{1}{4} a_{1}^{2}\right) x^{2}+\left(a_{4}+\frac{1}{2} a_{1} a_{3}\right) x+a_{6}+\frac{1}{4} a_{3}^{2}
$$

Thus, getting rid of the denominators and under the change of variables $y \mapsto \frac{1}{2}\left(y-a_{1} x-a_{3}\right)$, this gives the new Weierstrass equation

$$
y^{2}=4 x^{3}+\left(4 a_{2}+a_{1}^{2}\right) x^{2}+2\left(2 a_{4}+a_{1} a_{3}\right) x+4 a_{6}+a_{3}^{2}
$$

describing the same elliptic curve. In the literature, the so-obtained coefficients are often denoted by $b_{2}:=4 a_{2}+a_{1}^{2}, b_{4}:=2 a_{4}+a_{1} a_{3}$ and $b_{6}:=4 a_{6}+a_{3}^{2}$.

Luckily, these changes of variables preserving the Weierstrass equation are well understood and easy to classify as the following proposition states.

Proposition 3.6 ([21, Prop. III 3.1.b]). Let $E$ be an elliptic curve over a field $k$. Then, any two Weierstrass equations for $E$ as in theorem 3.2 are related by a linear change of variables of the form $X=u^{2} X^{\prime}+r$ and $Y=u^{3} Y^{\prime}+s u^{2} X^{\prime}+t$ with $u \in k^{\times}$and $r, s, t \in k$. In other words, $\mathbb{Z}\left[u^{ \pm}, r, s, t\right]$ corepresents isomorphisms of elliptic curves in Weierstrass form.

For example, the change of variables from example 3.5 corresponds to the ring map $\mathbb{Z}\left[u^{ \pm}, r, s, t\right] \rightarrow k$ defined by $u \mapsto 1, s \mapsto \frac{1}{2} a_{1} t \mapsto \frac{1}{2} a_{3}$ and $r \mapsto 0$.
There is a quantity whose vanishing determines whether a curve cut out by a Weierstrass equation is smooth, hence elliptic, or not.

Definition 3.7. Given a Weierstrass equation, one defines its discriminant as the quantity

$$
\Delta=-b_{2}^{3} b_{8}-8 b_{4}^{3}-27 b_{6}^{2}+9 b_{2} b_{4} b_{6}
$$

where $b_{2}, b_{4}$ and $b_{6}$ are as in example 3.5 and $b_{8}=a_{1}^{2} a_{6}+4 a_{2} a_{6}-a_{1} a_{3} a_{4}+a_{2} a_{3}^{2}-a_{4}^{2}$.
Proposition 3.8 ([21, Prop. III 1.4.a]). A curve cut out by a Weierstrass equation is smooth if and only if its discriminant is non zero.

The proof comes down to explicit calculations checking under which conditions and at which points both partial derivatives of the Weierstrass equation might vanish. Figure 2 depicts the two types of singularities that can occur when the discriminant is zero. Compare this to the smooth curves from figure 1 and the non-zero values of $\Delta$ given there.

We can expect to obtain formal group laws from elliptic curves because of the following theorem.
Theorem 3.9 ([10, Thm 2.1.2]). An elliptic curve $(E, e)$ has the unique structure of an abelian group scheme over $k$ with $e$ as unity.

The proof goes by showing that the map of sets $E(k) \rightarrow \operatorname{Pic}^{0}(E), P \mapsto \mathcal{O}_{E}(P-e)$ is a bijection. This follows easily from Riemann-Roch. Here $\operatorname{Pic}^{0}(E)$ is the subgroup of the Picard group consisting of invertible sheaves of degree zero. In particular, it has a group structure which we can pull back to $E$ via this bijection to make $E$ into a group scheme. Alternatively, one can show that the elliptic curve $E$

Figure 2: Rational points of Weierstrass curves over $\mathbb{R}$ with zero discriminant ([21, Fig. 3.2]).
![img-59.jpeg](img-59.jpeg)
represents the functor $T \mapsto P i c^{0}(E / T)$ from $k$-schemes to abelian groups. Here $P i c^{0}(E / T)$ denotes the group of line bundles over $E \times_{k} T$ that restrict to a 0 -line bundle on each fibre of the projection to $T$ modulo the line bundles pulled back from $T$ via this projection. This is the approach taken in [10, Thm 2.1.2].
Untangling this description, remembering what divisors, Picard groups etc. represent, there is a more explicit description for the group law at least on rational points.
Construction 3.10. Consider two rational points $P, Q$ on the elliptic curve $(E, e)$. Let $L$ be the unique line through $P$ and $Q$. By Bézout's theorem, $L$ intersects $E$ in a third point which we call $R$. It could happen that this third point is $P$ or $Q$, but that is not a problem. Now let $L^{\prime}$ be the unique line through $R$ and $e$. Again this intersects $E$ in a third point and that third point is precisely $P+Q$. This construction is summarised graphically in the following figure.

Figure 3: Illustration of the group law on rational points of elliptic curves ([21, Fig. 3.3]).
![img-60.jpeg](img-60.jpeg)

Example 3.11. Let $E$ be an elliptic curve in Weierstrass form and consider a point $P=\left(x_{0}, y_{0}\right)$ on that curve in the chart $\{Z=1\}$. Let us determine an explicit formula for the inverse of $P$. We want to find $-P$ such that $P+(-P)=O$, i.e. such that the third intersection point of the line through $O$ and $R$ with the elliptic curve $E$, where $R$ is the third intersection point of the line through $P$ and $-P$ with $E$, is $O$. Such a line must be tangent to $O$, hence as the tangent to $E$ at $O$ only intersects $E$ at $O$ (remark 3.4), it must hold that $R=O$. Hence, $Q$ must be the third intersection point with $E$ and the line through $P$ and $O$. This line is vertical, given by the equation $x=x_{0}$. Hence, the $x$ coordinate of $-P$ is $x_{0}$ and its $y$ coordinate is the second solution to $y^{2}+a_{1} x_{0} y+a_{3} y=x_{0}^{3}+a_{2} x_{0}^{2}+a_{4} x_{0}+a_{6}$. Writing $\left(y-y_{0}\right)\left(y-y_{-P}\right)=y^{2}+a_{1} x_{0} y+a_{3} y-x_{0}^{3}-a_{2} x_{0}^{2}-a_{4} x_{0}+a_{6}$ and solving for $y_{-P}$, one finds that $-P=\left(x_{0},-y_{0}-a_{1} x_{0}-a_{3}\right)$.
In analogy to Lie algebras and Lie groups, we might expect to get a formal group law by investigating the group structure close to the origin. Let us begin by doing this for a very simple example.

Example 3.12. Consider the elliptic curve $E: y^{2}+y=x^{3}$ over $\widehat{\mathbb{F}}_{2}$. One calculates that for this curve $b_{2}=0, b_{6}=1$ and thus $\Delta=-27=1$, so this equation does define an elliptic curve. To understand its group law close to the origin, we first have to change to the chart $\{Y=1\}$ so that we work on an affine open containing the origin. We achieve this via the change of coordinates $z=-\frac{x}{y}=-\frac{X / Z}{Y / Z}=-\frac{X}{Y}$ and $w=-\frac{1}{y}=-\frac{Z}{Y}$. Observe that under this change of coordinates $O$ corresponds to $(0,0)$. The equation rewrites as $\frac{1}{w^{2}}-\frac{1}{w}=\frac{z^{3}}{w^{3}}$ i.e. $w=z^{3}+w^{2}$. Successively replacing this equation into itself we can express $w$ as a power series in $z$ :
$w=z^{3}+w^{2}=z^{3}+\left(z^{3}+w^{2}\right)^{2}=z^{3}+z^{6}+w^{4}=z^{3}+z^{6}+\left(z^{3}+w^{2}\right)^{4}=z^{3}+z^{6}+z^{12}+w^{8}=z^{3}+z^{6}+\ldots$
where working in characteristic 2 greatly simplifies the calculation. One can show inductively that

$$
w(z)=\Sigma_{i=0}^{\infty} z^{3 \cdot 2^{i}}=z^{3} \Sigma_{i=0}^{\infty} z^{3 \cdot\left(2^{i}-1\right)}
$$

Can we get a formula for the group law on $E$ in terms of this power series?
Let $Z_{1}:=\left(z_{1}, w\left(z_{1}\right)\right)$ and $Z_{2}:=\left(z_{2}, w\left(z_{2}\right)\right)$ be two points of $E$. To add them, we need to determine the third intersection point of $E$ with the line $L$ through these two points. This line's slope is given by

$$
\lambda\left(z_{1}, z_{2}\right)=\frac{w\left(z_{2}\right)-w\left(z_{1}\right)}{z_{2}-z_{1}}=\Sigma_{i=0}^{\infty} \frac{z_{2}^{3 \cdot 2^{i}}-z_{1}^{3 \cdot 2^{i}}}{z_{2}-z_{1}}
$$

Noticing that, in characteristic 2, for any natural number it holds that $z_{2}^{n}-z_{1}^{n}=\left(z_{1}+z_{2}\right) \Sigma_{i+j=n-1} z_{1}^{i} z_{2}^{j}$, we can rewrite $\lambda$ as the power series

$$
\lambda\left(z_{1}, z_{2}\right)=\Sigma_{k=0}^{\infty} \Sigma_{i+j=3 \cdot 2^{k}-1} z_{1}^{i} z_{2}^{j}
$$

The intercept of $L$ is given by

$$
\nu\left(z_{1}, z_{2}\right)=w\left(z_{1}\right)-\lambda\left(z_{1}, z_{2}\right) z_{1}
$$

and thus $L$ is given by the equation

$$
w=\lambda\left(z_{1}, z_{2}\right) z+\nu\left(z_{1}, z_{2}\right)
$$

The third intersection point is the third solution to the following system of equations:

$$
\left\{\begin{array}{l}
w=z^{3}+w^{2} \\
w=\lambda\left(z_{1}, z_{2}\right) z+\nu\left(z_{1}, z_{2}\right)
\end{array}\right.
$$

i.e. we need to find the third root of $z^{3}+\left(\lambda\left(z_{1}, z_{2}\right) z-\nu\left(z_{1}, z_{2}\right)\right)^{2}=\lambda\left(z_{1}, z_{2}\right) z+\nu\left(z_{1}, z_{2}\right)$. We know that $z_{1}$ and $z_{2}$ are solutions, hence it suffices to solve

$$
\left(z-z_{1}\right)\left(z-z_{2}\right)\left(z-z_{3}\right)=z^{3}+\left(\lambda\left(z_{1}, z_{2}\right) z-\nu\left(z_{1}, z_{2}\right)\right)^{2}-\lambda\left(z_{1}, z_{2}\right) z-\nu\left(z_{1}, z_{2}\right)
$$

for $z_{3}$. The quadratic term gives the equation $z_{1}+z_{2}+z_{3}=\lambda\left(z_{1}, z_{2}\right)^{2}$ i.e. $z_{3}=-z_{1}-z_{2}+\lambda\left(z_{1}, z_{2}\right)^{2}$. So the third intersection point is given by

$$
Z_{3}:=\left(-z_{1}-z_{2}+\lambda\left(z_{1}, z_{2}\right)^{2}, w\left(-z_{1}-z_{2}+\lambda\left(z_{1}, z_{2}\right)^{2}\right)\right)
$$

To get the sum of the first two points, we need to find the third intersection point of $E$ and the line through $O$ and $Z_{3}$, i.e. the inverse of $Z_{3}$. In the $x, y$ coordinates, it was calculated in example 3.11 that the inverse of a point $(x, y) \in E$ is given by $(x,-y-1)$. What does this become under the change of coordinates to $z$ and $w$ ? Observe that $x=\frac{z}{w}$ and $y=-\frac{1}{w}$. Hence, we can express both $x$ and $y$ as Laurent series in $z$. More precisely,

$$
x(z)=\frac{z}{w(z)}=\frac{z}{z^{3} \Sigma_{i=0}^{\infty} z^{3 \cdot\left(2^{i}-1\right)}}=\frac{1}{z^{2}}\left(1+z^{3}+z^{6}+z^{12}+z^{24}+\ldots\right)
$$

using that $\left(\Sigma_{i=0}^{\infty} z^{3 \cdot\left(2^{i}-1\right)}\right)\left(1+\Sigma_{i=0}^{\infty} z^{3 \cdot 2^{i}}\right)=1$ which can be shown inductively. Similarly, one gets that

$$
y(z)=\frac{1}{z^{3}}\left(1+\Sigma_{i=0}^{\infty} z^{3 \cdot 2^{i}}\right)
$$

The inverse $i_{Z}$ of some point $Z:=(z, w)$ can be obtained by calculating its inverse in $x, y$ coordinates and changing the variables back again as $z\left(i_{Z}\right)=\frac{x\left(i_{Z}\right)}{y\left(i_{Z}\right)}=\frac{x(Z)}{-y(Z)-1}$. In particular the $z$-coordinate of the inverse of $Z_{3}$, which we denote $i\left(z_{3}\right)$, is given by

$$
\begin{aligned}
i\left(z_{3}\right) & =\frac{x\left(z_{3}\right)}{-y\left(z_{3}\right)-1} \\
& =\frac{1}{z^{2}}\left(1+z^{3}+z^{6}+z^{12}+z^{24}+\ldots\right) /\left(\frac{1}{z^{3}}\left(1+\Sigma_{i=0}^{\infty} z^{3 \cdot 2^{i}}\right)+1\right) \\
& =\frac{z\left(1+z^{3}+z^{6}+z^{12}+z^{24}+\ldots\right)}{1+z^{3}+z^{6}+z^{12}+z^{24}+\ldots+z^{3}} \\
& =\frac{z\left(1+z^{6}+z^{12}+\ldots\right)+z z^{3}}{1+z^{6}+z^{12}+z^{24}+\ldots} \\
& =z+\frac{z^{4}}{1+z^{6}+z^{12}+z^{24}+\ldots} \\
& =z+z^{4}\left(1+z^{6}+z^{18}+z^{42}+z^{54}+\ldots\right)
\end{aligned}
$$

Hence the inverse of $Z_{3}$, i.e. $Z_{1}+Z_{2}$, is given by

$$
\left(z_{3}+z_{3}^{4}\left(1+z_{3}^{6}+z_{3}^{18}+z_{3}^{42}+z_{3}^{54}+\ldots\right):=\left(i\left(z_{3}\right), w\left(i\left(z_{3}\right)\right)\right.\right.
$$

In particular, the addition of $Z_{1}$ and $Z_{2}$ is entirely determined by the power series $w(z)$ and $i(z)$. This gives a power series
$F\left(z_{1}, z_{2}\right)=i\left(z_{3}\left(z_{1}, z_{2}\right)\right)=i\left(z_{1}+z_{2}+\lambda\left(z_{1}, z_{2}\right)^{2}\right)=z_{1}+z_{2}+\lambda\left(z_{1}, z_{2}\right)^{2}+\left(z_{1}+z_{2}+\lambda\left(z_{1}, z_{2}\right)^{2}\right)^{4}+\left(z_{1}+z_{2}+\lambda\left(z_{1}, z_{2}\right)^{2}\right)^{10}+\ldots$
We had calculated that

$$
\lambda\left(z_{1}, z_{2}\right)=z_{2}^{2}+z_{1} z_{2}+z_{2}^{2}+z_{1}^{5}+z_{1} z_{2}^{4}+z_{1}^{2} z_{2}^{3}+z_{1}^{3} z_{2}^{2}+z_{1}^{4} z_{2}^{2}+z_{2}^{5}+z_{1}^{11}+\ldots
$$

Matching the degrees gives that

$$
F\left(z_{1}, z_{2}\right)=z_{1}+z_{2}+z_{1}^{2} z_{2}^{2}+z_{1}^{2} z_{2}^{8}+z_{1}^{4} z_{2}^{6}+z_{1}^{6} z_{2}^{4}+z_{1}^{8} z_{2}^{2}+\text { terms of total degree at least } 16+\ldots
$$

where the term of total degree 4 comes from $\lambda^{2}$, the other terms of degree four, $z_{1}^{4}$ and $z_{2}^{4}$, appear twice, once in $\lambda^{2}$ and once from $\left(z_{1}+z_{2}+\lambda\left(z_{1}, z_{2}\right)^{2}\right)^{4}$ and cancel out, the terms of degree 10 are the terms of degree 5 in $\lambda$ which are then squared. These will not cancel out because all other degrees are higher.
The power series $F\left(z_{1}, z_{2}\right)$ is the $z$ coordinate of $Z_{1}+Z_{2}$, this implies that

$$
F\left(z_{1}, 0\right)=F\left(0, z_{1}\right)=\left(Z_{1}+0\right)_{z}=z_{1}
$$

i.e. $F$ is unital and that

$$
F\left(z_{1}, z_{2}\right)=\left(Z_{1}+Z_{2}\right)_{z}=\left(Z_{2}+Z_{1}\right)_{z}=F\left(Z_{2}, Z_{1}\right)
$$

i.e. $F$ is commutative. By the same argument, $F$ is also associative $\left(F\left(z_{1}, F\left(z_{2}, z_{3}\right)\right)=F\left(F\left(z_{1}, z_{2}\right), z_{3}\right)\right)$ because the group structure on the elliptic curve is. In other words, we have just associated a formal group law to the elliptic curve $E: y^{2}+y=x^{3}$ over $\mathbb{F}_{2}$ and we could even calculate its values explicitly (up to an arbitrary degree).
This method can be generalised to obtain a formal group law from any elliptic curve in Weierstrass form over a field. In more detail, given such a curve, one first changes to the coordinates $z, w$ and expresses $w$ as a power series in $z$. The first few terms admit reasonably nice expressions in terms of the $a_{i}$ from the Weierstrass equation (see [21, IV 1.1]). Then, one calculates the equation of the line between two points $Z_{1}$ and $Z_{2}$ and finds the third point of intersection $Z_{3}$ of the curve with that line. One expresses $x$ and $y$ as Laurent series in $z, w$ to compute the inverse of $Z_{3}$. The $z$-coordinate of this inverse is a power series in $z_{1}, z_{2}$. By the discussion at the beginning of this paragraph, this power series is a formal group law. Details to the calculations are given in [21, IV.1]. In particular, the general expression for the first terms of the formal group law associated to a general elliptic curve in Weierstrass form as in (2) is given by

$$
F\left(z_{1}, z_{2}\right)=z_{1}+z_{2}+2-a_{1} z_{1} z_{2}-a_{2}\left(z_{1}^{2} z_{2}+z_{1} z_{2}^{2}\right)+\left(2 a_{3} z_{1}^{3} z_{2}+\left(a_{1} a_{2}-3 a_{3}\right) z_{1}^{2} z_{2}^{2}+2 a_{3} z_{1} z_{2}^{3}\right)+\ldots
$$

Of course, this formula coincides with the calculations from example 3.12 .
In the next subsection, we will briefly discuss how one could derive the existence of these formal group laws from geometric considerations and what the underlying formal groups are.

Remark 3.13. If one defines $a_{i}$ to have degree $2 i$, it can be shown that the formal group law obtained above is graded (see [21, Prop IV 1.1] and [16, Prop. 3.28]).

Let us understand the heights of the formal group laws just constructed. We begin by going back to the curve from example 3.12 .

Example 3.14. Recall from example 3.12 that the formal group law associated to $y^{2}+y=x^{3}$ is given by

$$
F\left(z_{1}, z_{2}\right)=z_{1}+z_{2}+z_{1}^{2} z_{2}^{2}+z_{1}^{2} z_{2}^{8}+z_{1}^{4} z_{2}^{6}+z_{1}^{6} z_{2}^{4}+z_{1}^{8} z_{2}^{2}+\text { terms of total degree at least } 16+\ldots
$$

As we are working at the prime 2 , it suffices to calculate

$$
[2]_{F}(z)=F(z, z)=z^{4}+\text { terms of total degree at least } 16
$$

to determine the height of this formal group law. One reads off that $v_{0}=2=0$ (as expected), $v_{1}=0$ and $v_{2}=1$. Hence this is of height 2 .

What about another curve?
Example 3.15. Let us look at the height of the formal group law associated to $y^{2}+x y=x^{3}+1$ over $\widehat{\mathbb{F}}_{2}$. By equation (3), its associated formal group law begins as

$$
F\left(z_{1}, z_{2}\right)=z_{1}+z_{2}-z_{1} z_{2}+\ldots
$$

In particular, $[2]_{F}(z)=z^{2}+\ldots$ and this formal group law is of height one.
We have seen an example of a formal group law associated to an elliptic curve of height 1 and of height 2. This is all that can happen:

Theorem 3.16 ([21, Cor. IV 7.5]). Let $k$ be a field of positive characteristic and $E$ an elliptic curve over $k$. Then the formal group law associated to $E$ has either height 1 or height 2.

There are several ways to prove this, most of which build on the fact that the multiplication by $n$ map, $[n]$ defined by sending a point to its $n$-fold addition, is finite, flat and of degree $n^{2}$ ([16, Prop. 4.11]). Then, one can for example show that in characteristic $p$, the quantity $p^{h t([p])}$ is bounded by the degree of $[p]$. This is a special case of [21, Thm IV 7.4]. For an alternative, more algebraic proof, using the notion of formal completion (definition 3.31) we refer the reader to [16, Prop. 4.12].

Definition 3.17. An elliptic curve whose associated formal group law has height 1 is called ordinary. If it has height 2 , it is called supersingular.

Beware that a supersingular elliptic curve, being an elliptic curve, is still smooth and not singular. Here supersingular should be understood to mean rare as justified by theorem 3.20 .
The following theorem gives a useful criterion to determine whether an elliptic curve is supersingular.
Theorem 3.18 ([21, Thm. 4.1 a)]). Let $\widehat{\mathbb{F}}_{q}$ be a finite field of characteristic $p$ with $p \geq 3$ and $E$ be an elliptic curve over $\widehat{\mathbb{F}}_{q}$ given by a Weierstrass equation of the form $y^{2}=f(x)$ where $f(x)$ is a separable cubic. Then, $E$ is supersingular if and only if the coefficient of $x^{p-1}$ in $f(x)^{\frac{p-1}{2}}$ is zero.

We will use this theorem to understand for which primes $p$ the curve $y^{2}+y=x^{3}$ is supersingular over $\widehat{\mathbb{F}}_{p}$. The characteristic 2 case was considered in example 3.15, where we had shown this curve is supersingular.

Example 3.19. Recall from example 3.5, that when the characteristic of the base field is different from 2, we can simplify the Weierstrass equation by completing the square. In this case, the change of variables given in that example transforms the curve $y^{2}+y=x^{3}$ to the isomorphic curve $E: y^{2}=4 x^{3}+1$. One easily calculates that the discriminant is given by $\Delta_{E}=-27$. Thus, when the characteristic is also different from $3, E$ defines an elliptic curve. By theorem $3.18, E$ is supersingular over $\widehat{\mathbb{F}}_{p}$ for some prime $p$ if and only if $\left(4 x^{3}+1\right)^{\frac{p-1}{2}}=\Sigma_{k=0}^{\frac{p-1}{2}}\left(\frac{p-1}{k}\right)\left(4 x^{3}\right)^{k}$ has no term of degree $p-1$. As $p$ cannot divide $\left(\frac{p-1}{k}\right) 4^{k}$ as all the factors are strictly smaller than $p,\left(4 x^{3}+1\right)^{\frac{p-1}{2}}$ has a term of degree $p-1$ if and only if there exists $k$ such that $3 k=p-1$. That is $E$ is supersingular over $\widehat{\mathbb{F}}_{p}$ if and only if $p \equiv 1 \bmod 3$, so roughly at about half of the primes (to make this precise, see the Dirichlet theorem and the discussion on Dirichlet density, for example in [24]).

It is true in general that any elliptic curve associated to a Weierstrass equation with coefficients in $\mathbb{Z}$ is supersingular for infinitely many primes, but also ordinary for infinitely many primes (see [21, Exercise V 5.11]). A curve with complex multiplication (i.e. whose endomorphism ring is strictly bigger than $\mathbb{Z}$, see $[21$, Rmk. III 4.3]) will, as the previous example suggests, be supersingular at about half the primes (see [21, Example V 4.5 and after] for a discussion and references to more precise results). For curves without complex multiplication, the supersingular primes are much rarer but still infinite as the following two theorems due to Serre and Elkies imply:

Theorem 3.20 ([21, Thm. V 4.7]). Let $E / \mathbb{Q}$ be an elliptic curve without complex multiplication. Then the set of supersingular primes has density 0 .

Theorem 3.21 ([21, Thm. V 4.9]). Let $E / \mathbb{Q}$ be an elliptic curve without complex multiplication. Then there are infinitely many primes $p$ for which $E / \mathbb{F}_{p}$ is supersingular.

The following two results show that over $\overline{\mathbb{F}}_{p}$ ordinary elliptic curves are way more abundant than supersingular ones. This will be important when dealing with Landweber exactness.

Theorem 3.22 ([21, Thm. V 4.1.c]). Up to isomorphism, there are at most $\left[\frac{p}{12}\right]+2$ supersingular elliptic curves over $\overline{\mathbb{F}}_{p}$.

Proposition 3.23. There are infinitely many ordinary elliptic curves over $\overline{\mathbb{F}}_{p}$.
For the proof of this proposition, we introduce the following invariant.
Definition 3.24. Given a smooth Weierstrass equation, one defines its $j$-invariant as the quantity $j=\left(b_{2}^{2}-24 b_{4}\right)^{3} / \Delta$ where $b_{2}$ and $b_{4}$ are as defined in example 3.5 and $\Delta$ is the discriminant.

One can verify by (tedious) calculations that the $j$-invariant stays unchanged under a change of coordinates like that of proposition 3.6 , i.e. it is an invariant of the isomorphism classes of elliptic curves (see [21, III Table 3.1]). Hence, it deserves the name invariant. Over algebraically closed fields more is true:

Proposition 3.25 ([21, Prop. III 1.4.b,c]). Two elliptic curves are isomorphic over an algebraically closed field $\bar{k}$ if and only if they have the same $j$-invariant. Moreover, for any $j_{0} \in \bar{k}$, there exists an elliptic curve over $\bar{k}$ with $j$-invariant $j_{0}$. In other words, over algebraically closed fields, the $j$-invariant defines a bijection between the isomorphism classes of elliptic curves over that field and the field itself.

With these tools at hand, the proof of proposition 3.23 is very easy.
Proof. By the previous proposition, the $j$-invariant gives a bijection between isomorphism classes of elliptic curves over $\overline{\mathbb{F}}_{p}$ and elements of $\overline{\mathbb{F}}_{p}$. In particular, there are infinitely many elliptic curves over $\overline{\mathbb{F}}_{p}$. As by theorem 3.22 , only finitely many of them are supersingular, the infinitely many others must be ordinary.

# 3.2 Elliptic Curves over general Base Schemes 

Now that we have a way to obtain interesting formal group laws, we would like to use them to construct interesting spectra via the Landweber exact functor theorem. However, so far, we have only considered elliptic curves over fields and hence also only obtained formal group laws over fields. So, unless the field is of characteristic 0 , we have no chance of verifying Landweber exactness as the base field always contains torsion. Fortunately, there is a way to make sense of an elliptic curve over a general base scheme. This subsection begins by defining elliptic curves over general base schemes and then moves on to giving results on Landweber exactness of elliptic curves.

Definition 3.26. Let $S$ be a scheme. An elliptic curve $E$ over $S$ is a smooth proper morphism $p: E \rightarrow S$ with a section $e: S \rightarrow E$ such that for every morphism $x: \operatorname{Spec}(k) \rightarrow S$ with $k$ algebraically closed, $x^{*}(E)$ is an elliptic curve over $k$.

In other words, an elliptic curve over a scheme $S$ is a scheme over $S$ with a nice enough structure morphism such that all its geometric fibers are elliptic curves with compatible base points (all pulled back from the same section).
Elliptic curves over general base schemes keep many properties of elliptic curves over a field. For example, they locally still admit a description in terms of Weierstrass equations.

Theorem 3.27 ([17, Thm. 4.5]). For every elliptic curve $E$ over $S$, there exists an open Zariski cover $\left\{U_{i}=\operatorname{Spec}\left(R_{i}\right)\right\}_{i}$ of $S$ such that each base change $E \times_{S} U_{i}$ has a Weierstrass form (i.e. it can be embedded into $\mathbb{P}_{R_{i}}^{2}$ and cut out by equation (1) with $\Delta$ invertible).

This implies the following lemma.
Lemma 3.28. Any elliptic curve corresponds locally to a morphism from $\mathbb{Z}\left[a_{1}, a_{2}, \ldots, a_{6}, \Delta^{-1}\right]$ to some ring.

Proof. Consider an arbitrary elliptic curve $E$ over some scheme $S$. By theorem 3.27, there is an open cover $\left\{\operatorname{Spec}\left(R_{i}\right)\right\}_{i}$ of $S$ such that $\left.E\right|_{\operatorname{Spec}\left(R_{i}\right)}$ is in Weierstrass form, i.e. cut out by an equation

$$
y^{2}+\tilde{a}_{1} x y+\tilde{a}_{3} y=x^{3}+\tilde{a}_{2} x^{2}+\tilde{a}_{4} x+\tilde{a}_{6}
$$

with each $\tilde{a}_{j} \in R_{i}$. This equation corresponds to the morphism $\mathbb{Z}\left[a_{1}, \ldots, a_{6}, \Delta^{-1}\right] \rightarrow R_{i}$ sending $a_{j}$ to $\tilde{a}_{j}$.

Remark 3.29. By the previous lemma any elliptic curve in Weierstrass form can be obtained as a pullback from the curve corresponding to $i d_{\mathbb{Z}\left[a_{1}, \ldots, a_{6}, \Delta^{-1}\right]}$ and any elliptic curve locally corresponds to a pullback from that curve. The curve corresponding to $i d_{\mathbb{Z}\left[a_{1}, \ldots, a_{6}, \Delta^{-1}\right]}$ is cut out by

$$
y^{2}+a_{1} x y+a_{3} y=x^{3}+a_{2} x^{2}+a_{4} x+a_{6}
$$

when embedded into $\mathbb{P}_{\mathbb{Z}\left[a_{1}, \ldots, a_{6}, \Delta^{-1}\right]}^{2}$, denoted $E^{\text {univ }}$ and called the universal Weierstrass curve.
The other property that is preserved over general schemes is the group structure:
Theorem 3.30 ([10, Thm 2.1.2]). Every elliptic curve over some base scheme $S$ has the unique structure of a group scheme over $S$ with unit e.

These observations suggest that one should be able to associate a formal group $\hat{E}$ to a given elliptic curve $E$ over some scheme $S$. Roughly, by theorem 3.27 , locally, $E$ is in Weierstrass form over some ring $R_{i}$ and we have seen in example 3.12 and the following discussion how to associate a formal group law to an elliptic curve in Weierstrass form. This formal group law corresponds to a choice of global section/coordinate and a group structure on the formal scheme $\operatorname{Spf}\left(R_{i}[[x]]\right)$. One is then able to glue these different formal schemes and their group structures together (as they came from a compatible open cover) to get a formal group $\hat{E}$ associated to $E$. This idea is made rigorous with the following definition.

Definition 3.31. Let $X$ be a scheme over $S$ with an ideal sheaf $I \subset \mathcal{O}_{X}$ which corresponds to a closed subscheme. The formal completion $\hat{X}_{I}$ of $X$ at $I$ is the functor $S c h^{o p} \rightarrow$ Sets defined by

$$
\hat{X}_{I}(Y)=\left\{f: Y \rightarrow X: f^{*}(I) \text { locally nilpotent }\right\}
$$

where by locally nilpotent we mean that there exists an open cover such that $f^{*}(I)$ pulled back to every open of that cover is nilpotent.

Remark 3.32. Observe that if $X$ is an affine scheme $\operatorname{Spec}(A)$ so that $I$ corresponds to an ideal, also denoted $I$, of $A$, the formal completion $\hat{X}_{I}$ coincides with $\operatorname{colim}_{n} \operatorname{Spf}\left(A / I^{n}\right):=\operatorname{Spf}\left(\hat{A}_{I}\right)$.

Elliptic curves have a natural closed subscheme at which one could complete: the image of the unit section. The section $e: S \rightarrow E$ is a closed immersion as by assumption $E$ is separated i.e. its diagonal is a closed immersion and $e$ is obtained as a base change of the diagonal as depicted in the following diagram
![img-61.jpeg](img-61.jpeg)

One can show that the group scheme structure on $E$ endows the completion of $E$ at the closed subscheme cut out by $e$ with a group structure. Even more:

Theorem 3.33 ([16, Thm. 3.8]). The formal completion of an elliptic curve $E$ at the closed subscheme cut out by the section $e$ is a formal group.

If $E$ is an elliptic curve defined over a field $k$, it is not difficult to see that the the formal completion at $e$ is $\operatorname{Spf}(k[[x]])$ i.e. it is a coordinatizable formal group. Indeed, it suffices to consider the formal completion of some affine open $\operatorname{Spec}(B)$ around the rational point $e$, which corresponds to some prime ideal $p$ of $B$. By remark 3.32 , the formal completion $\hat{B}_{p}$ coincides with $\operatorname{Spf}\left(\hat{B}_{p}\right)$. By construction, $\hat{B}_{p}$ is a complete, local ring containing $k$. Smoothness ensures that it is also regular (if we choose $\operatorname{Spec}(B)$ small enough around $e$ ) and the fact that curves are of dimension 1 implies that it has Krull dimension 1. By Cohen's structure theorem, $\hat{B}_{p}$ is thus isomorphic to $k[[x]]$. More generally, one can show that for an elliptic curve in Weierstrass form over a ring $R$, the Weierstrass equation defines an isomorphism between the formal completion of the elliptic curve at $e$ and $\hat{\mathbb{A}}_{R}^{*}$ using the expression of $w$ in terms of $z$ from example 3.12: see $[16$, Section 3.8].

Definition 3.34. Given some elliptic curve $E$, we define the formal group associated to $E$, denoted by $\hat{E}$, as the formal completion of $E$ at the closed subscheme cut out by $e$.

This gives a way to associate a morphism $\operatorname{Spec}(R) \rightarrow \mathcal{M}_{F G}$ to any elliptic curve $E$ over $\operatorname{Spec}(R)$ by defining the morphism to be the one corresponding to the formal group $\hat{E}$. The algebraic Landweber exact functor theorem (thm. 2.43) gives a criterion for when this morphism is flat. In our case, this criterion can be simplified further:

Theorem 3.35 ([16, Thm 4.16]). Let $E$ be an elliptic curve over $\operatorname{Spec}(R)$. Then the corresponding formal group is Landweber exact i.e the morphism $\operatorname{Spec}(R) \rightarrow \mathcal{M}_{F G}$ corresponding to $\hat{E}$ is flat if and only if $R$ is torsion free and $v_{1}$ is a non-zero divisor on $R / p$ for all primes $p$.
Moreover, if $R$ is an integral domain, it suffices to show that, for every prime $p$, there exists a morphism $f: R \rightarrow k$ with $k$ a field of characteristic $p$ such that $f^{*}(E)$ is an ordinary elliptic curve over $k$.

Proof. As it suffices to check these conditions on the localisations at every prime $p$, let us assume without loss of generality that $R$ is $p$-local. In view of the algebraic Landweber exact functor theorem (2.43), the formal group is Landweber exact if and only if the $v_{i}$ form a regular sequence. The claim now is that it suffices to check that $v_{0}$ and $v_{1}$ are regular. Indeed, we claim that $v_{2}$ is a unit in $R /\left(p, v_{1}\right)$. Then, $R /\left(p, v_{1}, v_{2}\right)=0$ and the regularity condition for the other $v_{i}$ is trivially satisfied. The claim is proved by contradiction. Suppose $v_{2}$ was not a unit in $R /\left(p, v_{1}\right)$. Then, there exists some maximal ideal $\mathfrak{m} \subset R /\left(p, v_{1}\right)$ containing $v_{2}$. Consider the quotient morphism $q: R /\left(p, v_{1}\right) \rightarrow R /\left(p, v_{1}\right) /(\mathfrak{m}):=k$. Then, the elliptic curve $q^{*}(E)$ over $k$ has a formal group law of height strictly greater than 2 as $q$ induces a morphism of formal group laws which maps $v_{i}^{E}$ to $v_{i}^{\sigma^{*}(E)}$. This contradicts theorem 3.16 .
The second part follows by the same observation that $v_{i}^{f^{*}(E)}=f\left(v_{i}^{E}\right)$. If $f^{*}(E)$ is an ordinary elliptic curve, then $v_{1}^{f^{*}(E)} \neq 0$ and as $f$ is a ring homomorphism this implies that $v_{1}^{E}$, being the preimage of a non trivial element, could not have been trivial either. If $R / p$ is a domain, this implies $v_{1}^{E}$ is not a zero divisor.

Consider an elliptic curve $E$ over some ring $R$ that is in Weierstrass form (so that its associated formal group is coordinatizable, i.e. gives a formal group law) and suppose its associated formal group law is graded. If the formal group law $F: M U_{*} \rightarrow R$ associated to $E$ satisfies the conditions of theorem 3.35 , by the Landweber exact functor theorem (cor. 2.44), one obtains an associated homology theory $E l l_{*}^{E}: h S p \rightarrow A b, X \mapsto M U_{*}(X) \otimes_{M U_{*}} R$ where the $M U_{*}$-module structure on $R$ is given by $F$ and an associated homotopy commutative ring spectrum as explained in section 2.2 .

Definition 3.36. The homology theory $E l l_{*}^{E}$ thus constructed is called an elliptic homology theory.
Example 3.37. - As $\mathbb{Q} / p=0$ for all primes $p$ and $\mathbb{Q}$ is torsion free, any elliptic curve over $\mathbb{Q}$ is trivially Landweber exact. However, as all formal group laws over $\mathbb{Q}$ are isomorphic to the additive one, we will not get any interesting spectra from these elliptic curves. We will always get a rational spectrum.

- Consider the elliptic curve $E: y^{2}+y=x^{3}$ from example 3.12, now as elliptic curve over $\mathbb{Z}$. As any ring map $f: R \rightarrow k$ with $k$ a field of characteristic 2 must be unital, $f^{*}(E)$ is given by the equation $y^{2}+y=x^{3}$ now seen as curve over $k$. Recall that we have seen that this curve is supersingular over any field of characteristic 2. In particular, there is no ring map $f: R \rightarrow k$ with $k$ a field of characteristic 2 such that $f^{*}(E)$ is an ordinary elliptic curve and, by theorem 3.35 , the formal group law associated to $E$ is not Landweber exact.

- In view of theorem 3.21, the problem described in the last point will appear for any elliptic curve $E$ over $\operatorname{Spec}(\mathbb{Z})$ as it will be supersingular at infinitely many primes. However, $E$ will be Landweber exact if we force all the primes at which $E$ is supersingular to be invertible, i.e. if we consider $E$ over the ring $\mathbb{Z}\left[\frac{1}{p} \mid E\right.$ supersingular at $\left.p\right]$.

These examples hint at the fact that the art to get interesting spectra from elliptic curves is closely tied with the art of choosing nice enough rings over which the elliptic curves live. Popular choices are the ring of $p$-adics or the $p$-adics adjoin certain elements. However, the situation is not as bad as the above examples might lead to believe: some elliptic curves are "universally" Landweber exact.

Example 3.38. Consider the universal Weierstrass curve $E^{\text {univ }}$ from remark 3.29 over $\operatorname{Spec}\left(\mathbb{Z}\left[a_{1}, \ldots, a_{6}, \Delta^{-1}\right]\right)$. This is Landweber exact. Indeed, by the second part of theorem 3.35, it suffices to show that for every prime $p$, there exists some morphism $f: \mathbb{Z}\left[a_{1}, \ldots, a_{6}, \Delta^{-1}\right] \rightarrow k$ where $k$ is a field of characteristic $p$ such that $f^{*}\left(E^{\text {univ }}\right)$ is an ordinary elliptic curve over $k$. But by construction, any elliptic curve over $k$ can be obtained from a suitable pullback of the universal Weierstrass curve. By proposition 3.23, we know that there exists an ordinary elliptic curve over each $\overline{\mathbb{F}}_{p}$ for $p$ any prime so we can simply choose $f: \mathbb{Z}\left[a_{1}, \ldots, a_{6}, \Delta^{-1}\right] \rightarrow \overline{\mathbb{F}}_{p}$ classifying any ordinary elliptic curve we like.

This universal example screams out for an interpretation using the language of stacks. As we will see in the following section, this can be formalised.

# 3.3 The Moduli Stack of Elliptic Curves 

In this section, it is discussed how elliptic curves assemble into an algebraic stack. Then, the Landweber exactness of the universal Weierstrass curve is reinterpreted as flatness of a certain map of stacks (theorem 3.43).

From now on, we will write $A:=\mathbb{Z}\left[a_{1}, \ldots, a_{6}, \Delta^{-1}\right]$ for simplicity of notation.
Definition 3.39. The moduli stack of elliptic curves $\mathcal{M}_{\text {ell }}$ is the stack which associates to an affine scheme $\operatorname{Spec}(R)$ the groupoid $\mathcal{M}_{\text {ell }}(\operatorname{Spec}(R))$ whose objects are elliptic curves over $\operatorname{Spec}(R)$ and whose morphisms are isomorphisms of elliptic curves.

In the same way as for the definition of $\mathcal{M}_{F G}$ (def. 1.67), it is not at all clear why the moduli stack of elliptic curves forms a stack. Again, it is not too hard to show that it is a prestack, i.e. that the presheaf of isomorphisms is a sheaf. Uniqueness/faithfulness of the glueing essentially amounts to the fact that the fpqc-topology is subcanonical and existence of the glueing/fullness follows from the fact that each elliptic curve is a sheaf on the fpqc site (see [17, Lem. 3.3]). The effective descent condition is more involved as, a priori, the glueing of schemes given on a fpqc-covering might not be a scheme (but only a stack as we know for example from $\mathcal{M}_{F G}$ ). With some care, one can show that for the case of elliptic curves this does work out, using the section they come with. A detailed account of this can be found in [17, Thm. 3.2].

Theorem 3.40. The moduli stack of elliptic curves $\mathcal{M}_{\text {ell }}$ is algebraic. Moreover, the morphism classifying the universal Weierstrass curve, $f: \operatorname{Spec}(A) \rightarrow \mathcal{M}_{\text {ell }}$, is a presentation and $\left(\mathcal{M}_{\text {ell }}, f\right)$ is equivalent to $\left[\left(A, A\left[r, s, t, u^{ \pm}\right]\right)\right]$ under the equivalence of theorem 1.40 with $r, s, t$ and $u$ as in proposition 3.6.

Proof. This is similar to the proof of proposition 1.68. To show that $\mathcal{M}_{\text {ell }}$ is algebraic, we need to check that $f: \operatorname{Spec}(A) \rightarrow \mathcal{M}_{\text {ell }}$ is affine and faithfully flat. The rest of the statement follows if we prove that $\operatorname{Spec}(A) \times_{\mathcal{M}_{\text {ell }}} \operatorname{Spec}(A) \cong \operatorname{Spec}\left(A\left[r, s, t, u^{ \pm}\right]\right)$.
Consider any morphism $g: X \rightarrow \mathcal{M}_{\text {ell }}$ with $X$ a scheme. Let us denote the elliptic curve corresponding to $g$ by $E$. We want to show that the fibre product $X \times_{\mathcal{M}_{\text {ell }}} \operatorname{Spec}(A)$ is also a scheme and that the base change of $g$ against $f$ is affine and faithfully flat.
Let us begin by considering the case where $X=\operatorname{Spec}(R)$ is affine and where $E$ is in Weierstrass form. Let $\operatorname{Spec}(B)$ be some affine scheme. By definition, an element in $\operatorname{Spec}(R) \times_{\mathcal{M}_{\text {ell }}} \operatorname{Spec}(A)(\operatorname{Spec}(B))$ is a triple

$$
\left(h: R \rightarrow B, h^{\prime}: A \rightarrow B, \phi: g(h) \xrightarrow{\cong} f\left(h^{\prime}\right)\right)
$$

This data is equivalent to the datum of a morphism $h: R \rightarrow B$ and an isomorphism $\phi: h^{*}(E) \rightarrow E^{\prime}$ of elliptic curves over $B$ with $E^{\prime}$ the elliptic curve in Weierstrass form corresponding to $h^{\prime}$. From the description of isomorphisms of elliptic curves in Weierstrass form (see proposition 3.6), we know that $\phi$ is classified by elements $r, s, t, u$ in $R$ with $u$ invertible. Hence, the datum $(h: R \rightarrow B, \phi)$ is precisely

a morphism $h^{\prime \prime}: R\left[r, s, t, u^{\pm}\right] \rightarrow B$ i.e. an element in $\operatorname{Spec}\left(R\left[r, s, t, u^{\pm}\right]\right)\left(\operatorname{Spec}(B)\right)$. Summing up, we have shown that $\operatorname{Spec}(R) \times_{\mathcal{M}_{\text {ell }}} \operatorname{Spec}(A) \cong \operatorname{Spec}\left(R\left[r, s, t, u^{\pm}\right]\right)$and in particular that the base change of $g$ along $f$ is faithfully flat and affine in this case.
Now, let us go back to our general $g: X \rightarrow \mathcal{M}_{\text {ell }}$. Recall from theorem 3.27 that any elliptic curve is Zariski locally in Weierstrass form i.e. $X$ admits a Zariski open cover $\left\{\operatorname{Spec}\left(R_{i}\right) \xrightarrow{t_{i}} X\right\}$ such that $E|_{\operatorname{Spec}\left(R_{i}\right)}$ has a Weierstrass form. By the previous paragraph, the fiber product $F:=X \times_{\mathcal{M}_{\text {ell }}} \operatorname{Spec}(A)$ admits a Zariski open cover given by $\left\{\operatorname{Spec}\left(R_{i}\left[r, s, t, u^{\pm}\right]\right)=\operatorname{Spec}\left(R_{i}\right) \times_{\mathcal{M}_{\text {ell }}} \operatorname{Spec}(A)\right\}$. Hence, $F$ is a scheme. Moreover, as affine and faithfully flat are properties that can be checked locally on the target and the morphism $F \rightarrow X$ is locally given by $\operatorname{Spec}\left(R_{i}\left[r, s, t, u^{\pm}\right]\right) \rightarrow \operatorname{Spec}\left(R_{i}\right)$, the base change of $g$ along $f$ is affine and faithfully flat as needed.
Hence, $\left(\mathcal{M}_{\text {ell }}, f\right)$ is a rigidified algebraic stack. By the same argument as above, $\operatorname{Spec}(A) \times_{\mathcal{M}_{\text {ell }}} \operatorname{Spec}(A) \cong$ $A\left[r, s, t, u^{\pm}\right]$and we conclude by the proof of theorem 1.40 that $\mathcal{M}_{\text {ell }}$ is equivalent to the stack associated to the Hopf algebroid $\left(A, A\left[r, s, t, u^{\pm}\right]\right)$.

Remark 3.41. If one accepts that $\mathcal{M}_{\text {ell }}$ defines a stack, then the Hopf algebroid structure on $\left(A, A\left[r, s, t, u^{\pm}\right]\right)$ is given by theorem 1.40. However, one could also show independently that $\left(A, A\left[r, s, t, u^{\pm}\right]\right)$ admits a Hopf algebroid structure and then take the moduli stack of elliptic curves to be defined as the stack associated to that Hopf algebroid. This has the advantage that one does not have to take the fact that definition 3.39 really defines a stack for granted, but the disadvantage that the geometric description might be slightly unclear. The Hopf algebroid structure on $\left(A, A\left[r, s, t, u^{\pm}\right]\right)$ is detailed in [4, Sec. 3]. Let us mention that the left unit $\eta_{L}$ is given by the inclusion $A \rightarrow A\left[r, s, t, u^{\pm}\right]$, the right unit classifies the elliptic curve obtained from the universal Weierstrass curve and the universal change of coordinates $x \mapsto u^{2} x+r$ and $y \mapsto u^{3} y+s x+t$.

It is now time to give the promised example of a morphism of stacks that is not representable.
Example 3.42. The $j$-invariant introduced in definition 3.24 defines a morphism $j: \mathcal{M}_{\text {ell }} \rightarrow \operatorname{Spec}(\mathbb{Z}[x])$, locally mapping an elliptic curve to its $j$-invariant. This morphism cannot be representable. If it were, the fibre product $\mathcal{M}_{\text {ell }} \times_{j, \operatorname{Spec}(\mathbb{Z}[x]), i d} \operatorname{Spec}(\mathbb{Z}[x])=\mathcal{M}_{\text {ell }}$ must be equivalent to a scheme. This cannot be. Indeed, if it were equivalent to a scheme, for each affine scheme $\operatorname{Spec}(R)$ the groupoid $\mathcal{M}_{\text {ell }}(\operatorname{Spec}(R))$ would be set valued. In particular, any ellitpic curve could only have the identity as automorphism. This contradicts the fact that $[-1]$, multiplication by -1 , defines a non-trivial automorphism on every elliptic curve.

The stacks $\mathcal{M}_{\text {ell }}$ and $\mathcal{M}_{F G}$ are related by the morphism that sends an elliptic curve to its associated formal group. This morphism has nice properties.

Theorem 3.43. The morphism $\Phi: \mathcal{M}_{\text {ell }} \rightarrow \mathcal{M}_{F G}$ that sends an elliptic curve to its associated formal group is a flat morphism of stacks.

For the statement of this theorem to even make sense, we need to first argue why $\Phi$ is representable. This will follow from the following lemma.

Lemma 3.44 ([22, Tag 046T]), Given a ring map $f: A \rightarrow R$, consider its induced morphism of Hopf algebroids $\bar{f}:(A, A) \rightarrow\left(R, R \otimes_{A} R\right)$ and the corresponding morphism on the associated stacks $[f]:\left[\left(R, R \otimes_{A} R\right)\right] \rightarrow[(A, A)]$. If $f$ is faithfully flat, the induced morphism $[f]$ is an equivalence of stacks. In particular, $\left[\left(R, R \otimes_{A} R\right)\right]$ is equivalent to a scheme.

Proof. The structure maps of $\left(R, R \otimes_{A} R\right)$ correspond to the various projections as described in lemma 1.26. Then, the lemma is a special case of [22, Tag 046T]. Roughly, in [22, Tag 046S] it is shown that $[f]$ is always a monomorphism and faithful flatness ensures it is an epimorphism. Then, one concludes by remark 1.8. The special case considered here appears in the proof of [22, Tag 04ZN]. The cited lemmas are not too hard to prove, but they require the introduction of several new concepts, in particular that of restriction of groupoids; see [22, Tag 044A].

Remark 3.45. Beware that under the assumptions of lemma $3.44,[f]$ is only an equivalence in the category of stacks, but not in that of rigidified algebraic stacks. Indeed, by theorem 1.40, $[f]$ can only be an equivalence of rigidified algebraic stacks if $\bar{f}$ is an equivalence of flat Hopf algebroids. In general however, we might not even have a morphism $R \rightarrow A$ that would be needed to construct an inverse to $\bar{f}$. However, by remark 1.41, these Hopf algebroids will be weakly equivalent.

We can now show that $\Phi$ is representable and flat.

Proof of theorem 3.43. We first show that $\Phi$ is representable. We will even show more, namely that it is affine. Observe that $\left(L\left[u_{1}^{ \pm}, u_{2}, u_{3}, u_{4}\right], W\left[u_{1}^{ \pm}, u_{2}, u_{3}, u_{4}\right]\right)$ defines a flat Hopf algebroid where the structure maps come from those of $(L, W)$ extended by mapping the $u_{i}$ to themselves. We can factor the presentation $c:[(L, L)] \rightarrow[(L, W)] \cong \mathcal{M}_{F G}$ corresponding to the universal formal group through the stack $\left[\left(L\left[u_{1}^{ \pm}, u_{2}, u_{3}, u_{4}\right], W\left[u_{1}^{ \pm}, u_{2}, u_{3}, u_{4}\right]\right)\right]$ as follows. There is a morphism

$$
[i]:\left[\left(L\left[u_{1}^{ \pm}, u_{2}, u_{3}, u_{4}\right], W\left[u_{1}^{ \pm}, u_{2}, u_{3}, u_{4}\right]\right)\right] \rightarrow[(L, W)]
$$

corresponding to the morphism of Hopf algebroids $i$ given by the inclusion of $L$ into $L\left[u_{1}^{ \pm}, u_{2}, u_{3}, u_{4}\right]$ and the inclusion of $W$ into $W\left[u_{1}^{ \pm}, u_{2}, u_{3}, u_{4}\right]$. Moreover, define

$$
\alpha:[(L, L)] \rightarrow\left[\left(L\left[u_{1}^{ \pm}, u_{2}, u_{3}, u_{4}\right], W\left[u_{1}^{ \pm}, u_{2}, u_{3}, u_{4}\right]\right)\right]
$$

to be the morphism corresponding to $e v_{1}: L\left[u_{1}^{ \pm}, u_{2}, u_{3}, u_{4}\right] \rightarrow L$ which is the identity on $L$ and sends the $u_{i}$ to 1 , seen as object of $\left[\left(L\left[u_{1}^{ \pm}, u_{2}, u_{3}, u_{4}\right], W\left[u_{1}^{ \pm}, u_{2}, u_{3}, u_{4}\right]\right)\right](\operatorname{Spec}(L))$. Observe that $[i] \circ \alpha=c$. Indeed, by remark 1.6, both morphisms are determined by where they send $i d_{L}$. By defintion, $c\left(i d_{L}\right)$ is the universal formal group law which is represented by $i d_{L}$ and by construction

$$
[i] \circ \alpha\left(i d_{L}\right)=i\left(e v_{1}\right)=e v_{1} \circ i=i d_{L}
$$

as was to be shown.
By corollary 1.38 , to show that $\Phi$ is affine, it suffices to check that the fibre product $\mathcal{M}_{\text {ell }} \times_{\Phi, \mathcal{M}_{F G}, c} \operatorname{Spec}(L)$ is equivalent to an affine scheme. By the previous discussion, this fiber decomposes as the following diagram of 2 -cartesian squares:
![img-62.jpeg](img-62.jpeg)

As the stack $\left[\left(L\left[u_{1}^{ \pm}, u_{2}, u_{3}, u_{4}\right], W\left[u_{1}^{ \pm}, u_{2}, u_{3}, u_{4}\right]\right)\right]$ is algebraic, by remark 1.18, it suffices to show that $P$ is equivalent to an affine scheme. By remark 1.42,

$$
\begin{aligned}
P & =\left[\left(A \otimes_{L} W \otimes_{L} L\left[u_{1}^{ \pm}, u_{2}, u_{3}, u_{4}\right], A\left[u^{ \pm}, r, s, t\right] \otimes_{L} W \otimes_{L} W\left[u_{1}^{ \pm}, u_{2}, u_{3}, u_{4}\right]\right)\right. \\
& \cong\left[\left(A\left[u_{1}^{ \pm}, u_{2}, u_{3}, u_{4}\right]\left[b_{0}^{ \pm}, b_{1}, b_{2}, \ldots\right], A\left[u^{ \pm}, r, s, t\right]\left[b_{0}^{ \pm}, b_{1}, b_{2}, \ldots, u_{1}^{ \pm}, u_{2}, u_{3}, u_{4}, t_{0}^{ \pm}, t_{1}, t_{2}, \ldots\right]\right)\right] \\
& \cong\left[\left(A\left[u^{ \pm}, r, s, t\right]\left[b_{0}^{ \pm}, b_{1}, b_{2}, \ldots\right], A\left[u^{ \pm}, r, s, t\right]\left[b_{0}^{ \pm}, b_{1}, b_{2}, \ldots\right] \otimes_{A} A\left[u^{ \pm}, r, s, t\right]\left[b_{0}^{ \pm}, b_{1}, b_{2}, \ldots\right]\right)\right]
\end{aligned}
$$

As the inclusion $A \rightarrow A\left[u^{ \pm}, r, s, t\right]\left[b_{0}^{ \pm}, b_{1}, b_{2}, \ldots\right]$ is faithfully flat, lemma 3.44 applies and gives that $P \cong[(A, A)] \cong \operatorname{Spec}(A)$ as desired.

Now that it makes sense to ask about flatness of $\Phi$, let us see what one can say. As by theorem 3.40 the presentation $f: \operatorname{Spec}(A) \rightarrow \mathcal{M}_{\text {ell }}$ is faithfully flat and as flat satisfies faithfully flat descent, it suffices to show that $\Phi \circ f$ is flat. This morphism is the one corresponding to the formal group law associated to $E^{\text {univ }}$. We have seen in example 3.38 that this elliptic curve is Landweber exact. This concludes the proof.

This statement is not only conceptually nice, but also gives another way to construct Landweber exact formal group laws. Indeed, any flat morphism $g: \operatorname{Spec}(R) \rightarrow \operatorname{Spec}(A)$ gives rise to a flat morphism $\Phi \circ f \circ g: \operatorname{Spec}(R) \rightarrow \mathcal{M}_{F G}$. Of course, such a morphism will classify a Landweber exact elliptic curve, so in that sense we get nothing new, but checking flatness of $g$ might sometimes be easier than checking the conditions of 3.35 . Remember that at the beginning of subsection 2.2 , we had discussed that, to construct a new homology theory from $M U$ by tensoring with $M U_{*}$, it would suffice to consider any ring $R$ that is flat over $L$. Then we had observed that flatness over $L$ is very restrictive as $L$ is an infinitely generated polynomial ring. Now we have reduced to checking that $R$ is flat over $A$ which is only a polynomial ring with six generators. While maybe still restrictive, this is a lot better than the first naïve condition. One can also show that the morphism $\operatorname{Spec}\left(\mathbb{Z}\left[\frac{1}{2}\left[\left[b_{2}, b_{4}, b_{6}, \Delta^{-1}\right]\right) \rightarrow \mathcal{M}_{\text {ell }}$ classifying

the curve in the simplified Weierstrass form from example 3.5 is flat (see [16, Ex. 4.18]). Then we reduced to flat rings over $\mathbb{Z}\left[\frac{1}{8}\right]\left[b_{2}, b_{4}, b_{6}, \Delta^{-1}\right]$ which is even one generator less. Even better, one can show that in characteristics different from 2 and 3 , the Weierstrass equation can be further simplified to an expression with only two variable denoted by $c_{4}$ and $c_{6}$ (see [21, Sec. III.1]) and that the morphism $\operatorname{Spec}\left(\mathbb{Z}\left[\frac{1}{6}\right]\left[c_{4}, c_{6}, \Delta^{-1}\right]\right) \rightarrow \mathcal{M}_{\text {ell }}$ classifying this Weierstrass curve is flat as well. Then, we reduced to checking flatness over $\mathbb{Z}\left[\frac{1}{6}\right]\left[c_{4}, c_{6}, \Delta^{-1}\right]$ which is a lot smaller than the Lazard ring.

Remark 3.46. The previous observations are the starting point for the construction of topological modular forms. At this point, we have all the tools to construct a functor from the Grothendieck subsite of flat affine schemes over $\mathcal{M}_{\text {ell }}$ to $h S p$. The Grothendieck subsite of flat affine schemes over $\mathcal{M}_{\text {ell }}$ is the subsite of $\operatorname{Aff} / \mathcal{M}_{\text {ell }}$ whose objects are flat morphims $E: \operatorname{Spec}(R) \rightarrow \mathcal{M}_{\text {ell }}$. This functor maps an object $E$ to the spectrum corresponding to the elliptic homology theory $E l l_{*}^{E}$ associated to $E$ (i.e. the homology theory corresponding to $\Phi \circ f \circ E$ ). For details on how to define this on morphisms, see [5, Ch. 4.3]. Functoriality is ensured by the fact that for a given spectrum $X$, the $\left(M U_{*}, M U_{*}(M U)\right)$-comodule $E l l_{*}^{E}(X)$ corresponds to a quasicoherent sheaf on $\mathcal{M}_{F G}$. We would like to extend this functor to the entire fpqc-site over $\mathcal{M}_{\text {ell }}$ i.e. to also allow for morphisms from general schemes to $\mathcal{M}_{\text {ell }}$ and to lift it to the infinity category of spectra. As by proposition $2.52 E l l_{*}^{E}$ corresponds to a homotopy commutative ring spectrum, it seems reasonable to want such a lift to land in $C A l g$, the $E_{\infty}$-ring spectra. Once we have a lift to $S p$, the extension to the entire fpqc-site can be achieved by right Kan extending this lift. Goerss, Hopkins and Miller have successfully constructed such a lift, but from the small étale site of $\mathcal{M}_{\text {ell }}$. This is the sheaf $\mathcal{O}^{\text {top }}: \mathcal{M}_{\text {ell_etale }} \rightarrow C A l g$; see [5, Ch. 12]. The global sections of this sheaf, $\mathcal{O}^{\text {top }}\left(\mathcal{M}_{\text {ell }}\right)$ give a spectrum $T M F$; see [5, Ch. 4, Rmk 4.4]. This opens up a whole new world of homotopy theory, which is not the topic here. For more on this, see [16, Sec. 5] and [14].

# References 

[1] J. F. Adams. On the non-existence of elements of Hopf invariant one. Ann. Math. (2), 72:20-104, 1960. ISSN 0003-486X. doi: 10.2307/1970147. URL www.jstor.org/pss/1970147.
[2] J. F. Adams. Lectures on generalised cohomology. Category Theory Homology Theory Appl., Proc. Conf. Seattle Res. Center Battelle Mem. Inst. 1968, Vol. 3, Lect. Notes Math. 99, 1-138 (1969)., 1969 .
[3] J. F. Adams and M. F. Atiyah. K-theory and the Hopf invariant. Q. J. Math., Oxf. II. Ser., 17: 31-38, 1966. ISSN 0033-5606. doi: 10.1093/qmath/17.1.31.
[4] T. Bauer. Computation of the homotopy of the spectrum tmf. In Proceedings of the conference on groups, homotopy and configuration spaces, University of Tokyo, Japan, July 5-11, 2005 in honor of the 60th birthday of Fred Cohen, pages 11-40. Coventry: Geometry \& Topology Publications, 2008 .
[5] C. L. Douglas, J. Francis, A. G. Henriques, and M. A. Hill, editors. Topological modular forms. Based on the Talbot workshop, North Conway, NH, USA, March 25-31, 2007, volume 201 of Math. Surv. Monogr. Providence, RI: American Mathematical Society (AMS), 2014. ISBN 978-1-4704-1884-7.
[6] P. G. Goerss. Quasi-coherent sheaves on the moduli stack of formal groups, 2008. URL https: //arxiv.org/abs/0802.0996.
[7] J. P. C. Greenlees, editor. Axiomatic, enriched and motivic homotopy theory. Proceedings of the NATO Advanced Study Institute, Cambridge, UK, September 9-20, 2002, volume 131 of NATO Sci. Ser. II, Math. Phys. Chem. Dordrecht: Kluwer Academic Publishers, 2004. ISBN 1-4020-1833-9.
[8] M. Hovey. Morita theory for Hopf algebroids and presheaves of groupoids. Am. J. Math., 124(6): 1289-1318, 2002. ISSN 0002-9327. doi: 10.1353/ajm.2002.0033. URL muse.jhu.edu/journals/ american_journal_of_mathematics/toc/ajm124.6.html.
[9] M. Hovey. Homotopy theory of comodules over a Hopf algebroid. In Homotopy theory: relations with algebraic geometry, group cohomology, and algebraic $K$-theory. Papers from the international conference on algebraic topology, Northwestern University, Evanston, IL, USA, March 24-28, 2002, pages 261-304. Providence, RI: American Mathematical Society (AMS), 2004. ISBN 0-8218-3285-9.

[10] N. M. Katz and B. Mazur. Arithmetic moduli of elliptic curves, volume 108 of Ann. Math. Stud. Princeton University Press, Princeton, NJ, 1985. doi: 10.1515/9781400881710.
[11] P. S. Landweber. Homological properties of comodules over $M U_{*}(M U)$ and $B P_{*}(B P)$. Am. J. Math., 98:591-610, 1976. ISSN 0002-9327. doi: 10.2307/2373808.
[12] P. S. Landweber, D. C. Ravenel, and R. E. Stong. Periodic cohomology theories defined by elliptic curves. In The Čech centennial. A conference on homotopy theory dedicated to Eduard Čech on the occasion of his 100th birthday, June 22-26, 1993, Northeastern University, Boston, MA, USA, pages 317-337. Providence, RI: American Mathematical Society, 1995. ISBN 0-8218-0296-8.
[13] G. Laumon and L. Moret-Bailly. Champs algébriques, volume 39 of Ergeb. Math. Grenzgeb., 3. Folge. Berlin: Springer, 2000. ISBN 3-540-65761-4.
[14] J. Lurie. A survey of elliptic cohomology. In Algebraic topology. The Abel symposium 2007. Proceedings of the fourth Abel symposium, Oslo, Norway, August 5-10, 2007, pages 219-277. Berlin: Springer, 2009. ISBN 978-3-642-01199-3; 978-3-642-01200-6. doi: 10.1007/978-3-642-01200-6_9. URL nrs.harvard.edu/urn-3:HUL.InstRepos:8895113.
[15] J. Lurie. Chromatic homotopy theory, 2010. URL https://people.math.harvard.edu/ lurie/ $252 x . h t m l$.
[16] L. Meier. From elliptic genera to topological modular forms. 2023. URL https://webspace. science.uu.nl/ meier007/TMF-Lecture.pdf.
[17] L. Meier and V. Ozornova. Moduli stack of elliptic curves, 2017. URL https://webspace.science. uu.nl/ meier007/Mell.pdf.
[18] N. Naumann. The stack of formal groups in stable homotopy theory. Adv. Math., 215(2):569-600, 2007. ISSN 0001-8708. doi: 10.1016/j.aim.2007.04.007.
[19] D. C. Ravenel. Complex cobordism and stable homotopy groups of spheres. Providence, RI: AMS Chelsea Publishing, 2nd ed. edition, 2004. ISBN 0-8218-2967-X.
[20] G. Segal. What is an elliptic object? In Elliptic cohomology. Geometry, applications, and higher chromatic analogues. Selected papers of the workshop, Cambridge, UK, December 9-20, 2002, pages 306-317. Cambridge: Cambridge University Press, 2007. ISBN 978-0-521-70040-5.
[21] J. H. Silverman. The arithmetic of elliptic curves, volume 106 of Grad. Texts Math. New York, NY: Springer, 2nd ed. edition, 2009. ISBN 978-0-387-09493-9; 978-0-387-09494-6. doi: 10.1007/ $978-0-387-09494-6$.
[22] T. Stacks Project Authors. Stacks Project. https://stacks.math.columbia.edu.
[23] N. P. Strickland. Formal schemes and formal groups. In Homotopy invariant algebraic structures. A conference in honor of J. Michael Boardman. AMS special session on homotopy theory, Baltimore, MD, USA, January 7-10, 1998, pages 263-352. Providence, RI: American Mathematical Society, 1999. ISBN 0-8218-1057-X.
[24] A. Sutherland. Lecture 18: Dirichlet l-functions, primes in arithmetic progressions. https://math. mit.edu/classes/18.785/2016fa/LectureNotes18.pdf, 2016.
[25] U. Würgler. Morava $K$-theories: A survey. Algebraic topology, Proc. Conf., Poznań/Pol. 1989, Lect. Notes Math. 1474, 111-138 (1991)., 1991.
[26] N. Yagita. The exact functor theorem for BP/In-theory. Proc. Japan Acad., 52:1-3, 1976. ISSN 0021-4280. doi: $10.3792 /$ pja/1195518412.
[27] N. Yagita. A topological note on the Adams spectral sequence based on Morava's K- theory. Proc. Am. Math. Soc., 72:613-617, 1978. ISSN 0002-9939. doi: 10.2307/2042481.