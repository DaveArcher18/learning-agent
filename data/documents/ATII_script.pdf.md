# V4D2 - Algebraic Topology II So24 (Stable and chromatic homotopy theory) 

Jack Morgan Davies (davies@math.uni-bonn.de)
September 9, 2024 Beta v3.8

# Contents 

Introduction ..... 2
Motivation ..... 2
Administration ..... 9
Background ..... 9
Notation ..... 9
$1 \infty$-categories ..... 10
1.1 Recollections on simplicial sets ..... 10
1.2 Basic notions and constructions in $\infty$-category theory ..... 14
1.3 Examples of $\infty$-categories ..... 16
1.4 Fibrations of simplicial sets ..... 24
1.5 Mapping animae ..... 30
1.6 Initial and terminal objects ..... 34
1.7 Slice categories ..... 35
1.8 Limits and colimits in $\infty$-categories ..... 39
1.9 Loose ends and an outlook (not discussed in lectures) ..... 46
2 The $\infty$-category of spectra ..... 51
2.1 Definition of Sp and its basic properties ..... 51
2.2 Examples of spectra ..... 63
2.3 Homology and cohomology ..... 69
2.4 Atiyah-Hirzebruch spectral sequence ..... 79
2.5 Rationalisation and Bousfield localisation ..... 81
2.6 Completion at a prime ..... 85
2.7 Outlook (not discussed in lectures) ..... 91
3 Chromatic homotopy theory ..... 93
3.1 Complex-oriented cohomology theories ..... 93
3.2 Formal group laws ..... 100
3.3 The topological universality of MU ..... 105
3.4 Quillen's theorem and Landweber's exact functor theorem ..... 112
3.5 The Morava $K$-theory spectra ..... 117
3.6 Not-yet typed notes ..... 124
3.7 The Nilpotence theorem ..... 125
3.8 The Thick subcategory theorem ..... 125
3.9 The Periodicity theorem ..... 125
3.10 Bousfield classes of $\mathrm{K}(n)$ and $E(n)$ ..... 125
3.11 Lubin-Tate and Morava $E$-theories ..... 125
References ..... 133

# Introduction 

The goal of these lectures is to introduce and explore the $\infty$-category Sp of spectra; the homotopy theoretic objects representing generalised cohomology theories. Actually, we have three specific subgoals: to discuss enough higher category theory to honestly define the $\infty$-category Sp , to prove many of the basic facts about spectra from the modern perspective of this $\infty$ category, and finally, to use all of these foundations to discuss the basics of chromatic homotopy theory-these three topics make up the three parts of these notes.

In a little more detail: in $\S 1$, we will define $\infty$-categories, see some of the initial examples and build up enough theory to define and manipulate limits and colimits in $\infty$-categories; in $\S 2$, we define the $\infty$-category of spectra Sp , whose homotopy category is $\mathrm{h} \mathrm{Sp}=\mathrm{SHC}$, and prove basic categorical facts, produce our favourite examples of spectra, and study the generalised (co)homology of spectra in some detail; and in $\S 3$, we finally get to some chromatic homotopy theory, starting with complex orientations and formal groups laws, and hopefully getting as fact as the construction of Morava $K$-theory spectra and the statement of the thick subcategory and nilpotence theorems.

## Motivation

Let us approach the content of these lectures through the eyes of a student who has completed Topology I and II and Algebraic Topology I at Universität Bonn.

## Stable homotopy theory (§2)

In Topology I and II, we saw the definitions of singular homology and cohomology and proved many facts both about these theories and about topology and algebra using these theories. In Algebraic Topology II, we also saw the first honest example of a generalised cohomology theory, that being $\mathrm{MU}^{*}(-)$ of complex cobordism. If we want to study cohomology theories in general, then we would like a category Cohom whose objects are cohomology theories and whose morphisms are natural transformations of functors. Such a category exists, but it is terrible. For example, we might want to perform various operations inside Cohom, such as taking quotients, kernels, and so on. However, if $E^{*}(-)$ is a cohomology theory, then $E^{*}(-) / 2$, defined by taking the cokernel of the multiplication-by-2 map on $E^{*}(X)$ for each space $X$, is not necessarily a cohomology theory-taking quotients will generally not preserve exact sequences.

When then take some inspiration as seen in Topology II: the Brown representability theorem. Associated to each cohomology theory $E^{*}(-)$ are sequences of based spaces $E_{n}$ for $n \geqslant 0$, weak homotopy equivalences $\sigma_{n}: E_{n} \simeq \Omega E_{n+1}$, and elements $\iota_{n} \in E^{n}\left(E_{n}\right)$ such that for each path-connected based space $X$ the natural homomorphism of abelian groups

$$
\left[X, E_{n}\right]_{*} \xrightarrow{\simeq} E^{n}(X) \quad f \mapsto f^{*}\left(\iota_{n}\right)
$$

is an isomorphism. The suspension isomorphism is then given the above isomorphism, twice, the equivalence $\sigma_{n}$, and the suspension-loop adjunction:

$$
E^{n}(X) \simeq\left[X, E_{n}\right]_{*} \xrightarrow{\sigma_{n}, \simeq}\left[X, \Omega E_{n+1}\right]_{*} \simeq\left[\Sigma X, E_{n+1}\right]_{*} \simeq E^{n+1}(\Sigma X)
$$

This suggests that perhaps a category of such collections of sequences $E=\left(E_{n}, \sigma_{n}\right)$ could be worth studying. The objects of the stable homotopy category SHC are all isomorphic to one of these sequences $\left(E_{n}, \sigma_{n}\right)$, which we will call a spectrum. The morphisms $f: E \rightarrow F$ in SHC should be homotopy classes of maps of based spaces $f_{n}: E_{n} \rightarrow F_{n}$ such that the there exists a homotopy in the diagram based spaces
![img-0.jpeg](img-0.jpeg)

With SHC at hand, we would now like to have a collection of useful and interesting spectra, understand some generic features of this category, and to recast and generalise previous results internally to SHC.

Singular cohomology $H^{*}(X ; A)$ is represented by the spectrum simply denoted by $A$ with spaces $A_{n}=K(A, n)$ and the weak homotopy equivalences $K(A, n) \simeq \Omega K(A, n+1)$ are those corresponding to the uniqueness of Eilenberg-Mac Lane spaces. The reason we write $A$ for this Eilenberg-Mac Lane spectrum is because the assignment sending an abelian group to its associated Eilenberg-Mac Lane spectrum is a fully faithful functor into SHC; we will prove the stronger $\infty$-categorical version of this in Th.2.2.14. This is one motivation to view SHC as a generalisation of the category of abelian groups - although this analogy is even neater from an $\infty$-categorical perspective.

One can then define positive shifts of spectra $E[k]$ as $E[k]_{n}=E_{k+n}$ for $k \geqslant 0$. The Steenrod squaring operations $S q^{n}$ from Topology II then define morphisms of spectra $\mathbf{F}_{2} \rightarrow \mathbf{F}_{2}[n]$. In fact, Serre's computation of the cohomology of Eilenberg-Mac Lane spaces from Algebraic Topology I can be used to show that the homotopy groups of the function spectrum $\mathbf{F}_{2}^{\mathbf{F}_{2}}$ are in bijection with the Steenrod algebra $\mathcal{A}$.

In fact, even the Thom isomorphism from Algebraic Topology I can be recognised by an equivalence of spectra. Indeed, a potential Thom class for an $n$-dimensional vector bundle

$\xi$ over a space $X$ is an element $u$ inside $H^{n}(\operatorname{Th}(\xi) ; \mathbf{Z})$, or equivalently a map of spectra $u: \operatorname{Th}(\xi) \rightarrow \mathbf{Z}[n]$. One can then check that the map of spectra

$$
\operatorname{Th}(\xi) \otimes \mathbf{Z} \xrightarrow{\otimes \mathbf{Z}} X_{+} \otimes \operatorname{Th}(\xi) \otimes \mathbf{Z} \xrightarrow{X_{+} \otimes u \otimes \mathbf{Z}} X_{+} \otimes \mathbf{Z}[n] \otimes \mathbf{Z} \xrightarrow{X_{+} \otimes \mu} X_{+} \otimes \mathbf{Z}[n]
$$

where the first map $i: \operatorname{Th}(\xi) \rightarrow X_{+} \otimes \operatorname{Th}(\xi)$ is given by the map of vector bundles $\xi \rightarrow \varepsilon_{0} \times \xi$ over $\Delta: X \rightarrow X \times X$ and $\mu$ is the multiplication on $\mathbf{Z}$, is an equivalence, ie, reproduces a homological Thom isomorphism, if and only if $u$ is a Thom class in the usual sense.

There is much more we can do just with SHC. For example, there is a Whitehead, a homology Whitehead, and a Hurewicz theorem for spectra; see Ths.2.2.7, 2.3.28 and 2.3.32, respectively. One can also show that SHC is a triangulated category, which will follow from our higher categorical statement that Sp is stable; see Th.2.1.18 and Rmk.2.1.19. We will also discuss a kind of Serre spectral sequence with coefficients in a generalised (co)homology theory $E^{*}(-)$ and how to localise the category of spectra at $E$-homology equivalences, for example, given by rationalisation; see $\S 2.4$ and $\S 2.5$, respectively.

This theory, and the examples it produces, are a key first step to understand SHC. These ideas also highlight the geometric connections between the stable homotopy category and bordism groups as well as the algebraic connections between abelian groups and spectra. A deeper, and perhaps more surprising connection, comes from a connection between SHC and arithmetic geometry.

# Chromatic homotopy theory (§3) 

A simple observation is made in Pr.3.2.5, which goes back to work of Quillen, Adams, and Morava, that for a certain natural class of cohomology theories $E$, the $E$-cohomology of $\mathbf{C P}^{\infty}$ has the structure of a formal group law - this is a power series $f_{E}(x, y)$ in two variables with coefficients in the homotopy groups of $E$ such that $f_{E}(x, 0)=x$ (unitality), $f_{E}(x, y)=f_{E}(y, x)$ (commutativity), and $f_{E}\left(x, f_{E}(y, z)\right)=f_{E}\left(f_{E}(x, y), z\right)$ (associativity). The construction of this $f_{E}(x, y)$ is very simple too: the multiplication map $m: \mathbf{C P}^{\infty} \times \mathbf{C P}^{\infty} \rightarrow \mathbf{C P}^{\infty}$ induces a ring homomorphism

$$
E^{*} \llbracket t \llbracket \simeq E^{*}\left(\mathbf{C P}^{\infty}\right) \xrightarrow{m} E^{*}\left(\mathbf{C P}^{\infty} \times \mathbf{C P}^{\infty}\right) \simeq E^{*} \llbracket x, y \rrbracket
$$

and $f_{E}(x, y)$ is just defined as the image of $t$ inside $E^{*} \llbracket x, y \rrbracket$-all of the unnamed isomorphisms above come from our assumptions on this class of particular $E$. The class of $E$ includes singular cohomology with integer coefficients, if the reader wants to try that example our herself.

The above construction is unassuming, however, it is the springboard for an incredibly deep mutual relationship between formal group laws and the stable homotopy category. The stable homotopy category captures a lot of information about formal group laws. For example, if $E=\mathrm{MU}$ is the spectrum of complex cobordism, then $f_{\mathrm{MU}}(x, y)$ is the universal formal group law; see $\S 3.3$. On the other hand, the geometry of the moduli stack of formal group laws plays a huge role in the global behaviour of SHC. As another example, there are spectra $\mathrm{K}(p, n)$

associated to each prime $p$ and a choice of $p$-typical formal group law of height $n$, which is both an exhaustive collection of fields in SHC (Th.3.5.8) and define all localising subcategories of SHC (??.). This connection between formal groups laws and stable homotopy theory has led to many advances in stable homotopy theory throughout the last 60 years, and is currently an omnipresent feature of homotopy theory as a whole.

# Higher category theory (§1) 

To ground our homotopy theory in modern times, we will use $\infty$-categories to discuss stable and chromatic homotopy theory. We do this now, because we have been working around an annoying problem for a few semesters now: homotopy theory is very categorical, however, many things we do in category theory do not respect homotopy theory. The following examples already came up in Topology I:
Example 0.0.2. Consider the diagram of inside the category of topological spaces:
![img-1.jpeg](img-1.jpeg)

The diagram trivially commutes, and the horizontal maps are weak equivalences. However, the pushout of the top span is $S^{2}$, and the pushout of the bottom diagram is $*$; two homotopically distinct topological spaces. In other words: pushouts do not preserve homotopy equivalences.

We have already seen a solution to this as well: we replace our pushouts with homotopy pushouts, our pullbacks with homotopy pullbacks, fibres with homotopy fibres, quotients with mapping cones, sequential colimits with mapping telescopes, and so on. The problem with these constructions, is that they are not (in any obvious way, at least) limits or colimits inside a category. ${ }^{1}$

One solution to these problems is to work in the category of topological spaces as we did in Topology I \& II as well as Algebraic Topology II. This suffices for certain applications, but

[^0]for any anima $Y$. However, the homotopy fibre of a similar map $2: K(\mathbf{Z}, 2) \rightarrow K(\mathbf{Z}, 2)$ is $K(\mathbf{Z} / 2 \mathbf{Z}, 1)$, and taking a further homotopy fibre of the map $K(\mathbf{Z} / 2 \mathbf{Z}, 1) \rightarrow K(\mathbf{Z}, 2)$ yields the fibre sequence

$$
K(\mathbf{Z}, 1) \rightarrow K(\mathbf{Z} / 2 \mathbf{Z}, 1) \rightarrow K(\mathbf{Z}, 2)
$$

Apply $[P,-]$ to this fibre sequence induces a short exact sequence of groups, but from our calculations above this short exact sequence would take the form $0 \rightarrow \mathbf{Z} / 2 \mathbf{Z} \rightarrow 0$, a contradiction. Of course, an $\infty$-categorical limit of this diagram does exist-it is simply $\mathbf{R P}^{2}$.


[^0]:    ${ }^{1}$ Despite the name, these are not limits or colimits in the homotopy category. In fact, the homotopy category does not always have limits and colimits. We steal the following example from Neil Strickland: let us work in the homotopy category of based anima, and consider the span $* \leftarrow S^{1} \xrightarrow{\circ} S^{1}$, where 2 induces multiplication by 2 on the fundamental group. If this had a pushout $P$ in the homotopy category of based anima, then in particular the universal property of a pushout would give us the calculation

if we want to understand some of the finer points about the homotopy theory of topological spaces, or the homotopy theory of anima ${ }^{2}$, as we will say for the rest of these lectures, or of spectra, we need to work more systematically. In previous years, we might work with model categories, but the more recent trend is to work with $\infty$-categories.

Roughly speaking, an $\infty$-category is a concept equipped with objects, morphisms (which we now call 1-morphisms) between objects, 2-morphisms between 1-morphisms (which look like homotopies), 3-morphisms between 2-morphisms (which look like homotopies between homotopies), and so on, which are all as associative and unital as one would like, all up to higher homotopy.

How does this fix our problem above though? Well, all of this added flexibility with higher homotopies is suggestive when we remember the definition of a homotopy fibre of a map of based topological spaces $f: X \rightarrow Y$, for example:

$$
\operatorname{hofib}(f)=\left\{(x, \gamma) \in X \times Y^{I} \mid \gamma(0)=x \& \gamma(1)=y_{0}\right\}
$$

In other words, the homotopy fibre of $f$ is not all of the points in $X$ which map to the base-point $y_{0}$ of $Y$, but rather the topological spaces of points in $X$ and a homotopy between its image and $y_{0}$. One can now imagine that homotopy limits, or limits in an $\infty$-category, of more complicated diagrams would involve not just 1-homotopies, but perhaps 2-homotopies or higher. To package all of this information and all of these combinatorics is usually done using simplicial sets, as inspired by Boardman-Vogt [BV73], Joyal [Joy02], and Lurie [Lur09b], so that is where we will start in $\S 1$.

Many basic facts about stable and chromatic homotopy theory do not need $\infty$-categories, or even model categories, however, one does need $a$ model for the stable homotopy category SHC to study spectra in any depth. In the distant past, between the 1970s and the 1990s, one might have been content with Boardman's model of SHC from his thesis [Boa64] (an accessible resource for this material [Ada74, §III]) where this category is constructed by hand. However, the analogy between classical algebra, with abelian groups and rings, and higher algebra, with spectra and ring spectra, can only be explored with a stronger homotopical foundation. Let us give two glaring examples how this lack of higher structure can be problematic:

- On a very basic level, SHC simply does not have all limits and colimits. ${ }^{3}$ If we cannot freely apply categorical techniques too SHC what can we be expected to do with this

[^0]
[^0]:    ${ }^{2}$ To emphasise our step into the $\infty$-categorical world too, we will no longer refer to topological spaces as such-instead, we call the free $\infty$-category on a single element that of anima, with singular anima, and denote it by $\mathscr{A} \mathrm{n}$. This reflects the fact that this $\infty$-category $\mathscr{A} \mathrm{n}$ does not capture the geometry of its objects, but rather precisely their homotopical heart, their anima. This is a recent tradition of Dustin Clausen and Peter Scholze and further reduces the emphasis on the loaded word space, which is overused in mathematics.
    ${ }^{3}$ For example, suppose the colimit of the maps of spectra $\mathbf{S} \xrightarrow{2} \mathbf{S} \xrightarrow{3} \mathbf{S} \xrightarrow{4} \cdots$ exists in SHC, and write it as $C$. From the universal property of a colimit we would have, for any other spectrum $X$, isomorphisms of abelian groups

    $$
    \operatorname{SHC}(C, X) \simeq \lim \operatorname{SHC}(\mathbf{S}, X) \simeq \lim \pi_{0} X \simeq \operatorname{Ab}(\mathbf{Q}, X)
    $$

category! Algebraists also complain about the derived category of a ring for the same reason.

- Experience tells us that one of the most useful features of ordinary cohomology $H^{*}(X ; R)$ with coefficients in a ring $R$, as opposed to homology $H_{*}(X ; R)$, is that $H^{*}(X ; R)$ can be granted a natural ring structure using the cup product. Brown representability can then be used to show that this cup product can also be constructed from a kind of product structure $K(R, m) \wedge K(R, n) \rightarrow K(R, m+n)$ between the represented Eilenberg-Mac Lane spaces; this was an exercise in Topology II. This leads to a product structure on the Eilenberg-Mac Lane spectrum $R$ for the integers in SHC. In fact, using the tensor product of spectra, this product structure recognises $R$ as a commutative monoid object in SHC. This structure allows us to say that the function spectrum $R^{X}$, where $X$ is an anima, also known as the spectrum whose homotopy groups yield the singular cohomology of $X$ with $R$-coefficients, also inherits a commutative monoid structure. For similar formal reasons, the spectrum $R \otimes X$ representing the singular cohomology of $X$ with $R$ coefficients is an $R$-module. However, just like the category SHC is neither complete nor cocomplete, then the category of homotopy commutative ring spectra $\mathrm{CAlg}(\mathrm{SHC})$ is neither complete nor cocomplete. Worse still, is the fact that for a homotopy commutative ring spectrum $E$, the category $\operatorname{Mod}_{E}(\mathrm{SHC})$ does not come with a natural triangulation. Much of the utility of SHC over a category of cohomology theories comes from the fact that it's triangulated (or the homotopy category of a stable $\infty$-category).

From the early 1990s until now, model categories have been one method to secure stable homotopy theory upon sound foundations. There are many benefits to model category theory, most notably, from the perspective of a lecture course, accessibility and simplicity; see [BR20, Sch12] for example.

Since Lurie's treatise on $\infty$-categories [Lur09b], born out of an attempt to formally ground his PhD thesis [Lur04], we have had yet another option. Although the basics of the theory of $\infty$-categories is undoubtably more abstract than the basics of model category theory, the pay-off at the end of the day is enormous - the language of higher category theory simultaneously provides a more flexible framework than model categories (working in settings without (co)completeness assumptions and nothing need be derived or replaced to get the "right" answer), but also a more powerful and self-reflective model for homotopy theory (there exists an $\infty$-category of $\infty$-categories). There is also an argument to be made that $\infty$-categories get closer to the essence of pure homotopy theory, where as model categories provide a rigid model-we have essentially built homotopy theory into our category theory from the get-go.

We also know that mapping into a cofibre sequence $X \rightarrow Y \rightarrow Z$ in SHC yields an exact sequence

$$
\operatorname{SHC}(C, X) \rightarrow \operatorname{SHC}(C, Y) \rightarrow \operatorname{SHC}(C, Z)
$$

Applying this to the cofibre sequence $\mathbf{Q} \rightarrow \mathbf{Q} / \mathbf{Z} \rightarrow \mathbf{Z}[1]$ of Eilenberg-Mac Lane spectra (with a shift), we obtain the exact sequence

$$
\operatorname{Ab}(\mathbf{Q}, \mathbf{Q}) \rightarrow \operatorname{Ab}(\mathbf{Q}, \mathbf{Q} / \mathbf{Z}) \rightarrow 0
$$

which cannot be exact as the outer terms are countable and the middle term is uncountable.

We do not aim to cover all of the basics of higher category theory in this course. The obvious omissions include a rigorous discussion of the Yoneda lemma, adjoints, presentability, and the theory of symmetric monoidal $\infty$-categories and $\infty$-operads, however, the student equipped with the knowledge from these lectures should find these topics more approachable than ever. Moreover, the fact we do not discuss these topics directly will not stop us from using some of these tools from time to time, as advertisement for their utility.

At the end of the day, we really just want to provide a rigorous mathematical home to practice stable homotopy theory in these lectures, and every approach to define SHC as a 1-category, or the shadow of something more structured, takes time. It just makes sense to spend this time building the required higher categorical framework, which will not only allow us to play inside the worlds of stable and chromatic homotopy theory, but will also gives the students a powerful and pliable base on which to build many other pieces of mathematics.

# Administration 

- This course will be taught by Liz Tatum and Jack Davies.
- Lectures are on Mondays from 14:15 until 15:45 in the großer Hörsaal and Wednesdays from 8:15 until 9:45 in the kleiner Hörsaal.
- The assistant for the course is Lucas Piessevaux. Please contact them for any questions regarding the course through this email: lucas@math.uni-bonn.de.
- Please get in contact with your potential tutor, either via email or talk to them in tutorials, to arrange how to submit your exercises - per email probably works best.
- There will be notes for this course, you are reading them now, which will be updated each week after the Wednesday lecture. These can be found on the eCampus page and also on Jack's website. If you find any mistakes or typos, please email Lucas.
- There will be a handful of homework sheets, which will appear on the eCampus page and also on Jack's website on Wednesday afternoon, and will be due 12 days later just before a Monday lecture. You require a total grade of $50 \%$ or more to be able to attempt the exam. The exam will be written.
- The exam dates are:
- $1^{\text {st }}$ attempt on Wednesday $24^{\text {th }}$ July at 9-11 in the große Hörsaal.
$-2^{\text {nd }}$ attempt on Monday $23^{\text {rd }}$ September at 13-15 in the große Hörsaal.


## Background

This course assumes that students have taken Topology I and II as well as Algebraic Topology I in Bonn. Essentially, the students should have the background of all of the main chapters of Hatcher's Algebraic Topology text [Hat02], plus knowledge about the Brown representability, Steenrod squares, the Serre spectral sequence, complex $K$-theory, characteristic classes, and bordism spectra. Of course, not everything will be totally necessary, but we will also try not to reprove anything already discussed in previous courses, if possible.

References include [Ada74, BR20, Lur09b, Lur17, Lura, Lurb, Mei19].

## Notation

If $\mathcal{C}$ is a 1-category, we will write $\mathcal{C}(X, Y)$ for the mapping set (all of our categories will be locally small) of objects from $X$ to $Y$. On the other hand, if $\mathcal{C}$ is an $\infty$-category, we will write $\operatorname{Map}_{\mathcal{C}}(X, Y)$ for the mapping anima (simplicial set) of maps from $X$ to $Y$.

# Chapter 1 

## $\infty$-categories

There are many reasons for studying $\infty$-categories-you might have already come up with your own reasons and there are plenty discussed in the introduction above. We have, however, already come across problems where $\infty$-categories offer an elegant solution. The main example for this course, will be defining morphisms between spectra, the objects representing cohomology theories, and the associated $\infty$-category Sp .

We don't claim to do the fanciest $\infty$-category theory in these notes; for that, the reader can enjoy an afternoon of reading [Lur09b, §1] themselves. What we want to do here, is to set-up just enough foundations to define the $\infty$-category of spectra Sp , and at that moment we will jump into the stable homotopy theory. Extra little pieces of $\infty$-category theory can then be added later as needed.

### 1.1 Recollections on simplicial sets

We have already seen the basics of simplicial sets a few times through Topology I \& II and Algebraic Topology I, so we will be quick with some of the following recollections.

Definition 1.1.1. Let $\Delta$ be the category whose objects finite nonempty totally ordered sets and morphisms are order preserving maps. Up to isomorphism, each object can be represented by a tuple

$$
[n]=\{0<1<\cdots<n-1<n\}
$$

for some $n \geqslant 0$.
An important collections of morphisms in $\Delta$ are the following.
Definition 1.1.2. A coface map is the unique order preserving injection $\delta^{i}:[n-1] \rightarrow[n]$ which skips $i$, for $0 \leqslant i \leqslant n$; we suppress the $n$ in our notation for $\delta^{i}$. A codegeneracy map is the unique order preserving surjection $\sigma^{i}:[n] \rightarrow[n-1]$ which hits $i$ twice, for $0 \leqslant i \leqslant n-1$.

Exercise 1.1.3. Write down the relations between the coface and the codegeneracy maps-we have already seen them in Topology I and II.

Exercise 1.1.4. Show that all morphisms in $\Delta$ can be written as a composition of $\sigma^{i}$ 's and $\delta^{j}$ 's. In other words, the codegeneracy and coface maps generate the category $\Delta$.
Definition 1.1.5. A simplicial set is a functor $\Delta^{\text {op }} \rightarrow$ Set. A morphism of simplicial sets is a natural transformation, so we define the category sSet as the functor (presheaf) category Fun( $\Delta^{\text {op }}$, Set). More concretely, and using Exc.1.1.4 this is a collection of sets $X_{n}$ for each $n \geqslant 0$ together with a collection of morphisms, the face maps $d_{i}: X_{n} \rightarrow X_{n-1}$, and the degeneracies $s_{i}: X_{n-1} \rightarrow X_{n}$, dual to the $\delta^{i}$ and $\sigma^{i}$ in Df.1.1.2, which satisfy the dual relation to those from Exc.1.1.3.

The following is a collection of exercises to help the reader (re)familiarise themselves with simplicial sets.
Exercise 1.1.6. Write down the initial and terminal objects in sSet. Prove that sSet is complete and cocomplete and write a formula for the $n$-simplices of a limit or colimit.
Exercise 1.1.7. We say that a simplicial set $X$ is discrete if all simplices in positive degree are degenerate, in other words, for every map $f:[n] \rightarrow[m]$ in $\Delta$, the induced map $f^{*}: X_{m} \rightarrow X_{n}$ is a bijection of sets. Show that the functor sending a set $S$ to the constant simplicial set $\underline{S}$, defined by $\underline{S}_{n}=S$ for all $n \geqslant 0$ and whose simplicial structure maps are all the identity, is left adjoint to the functor sending a simplicial set $X$ to its set of 0 -simplices. Show that this constant simplicial set functor is fully faithful, and that its essential image is precisely those discrete simplicial sets.

We will implicitly use the above exercise to consider Set as a fully subcategory of sSet.
Exercise 1.1.8. Show that the category of simplicial sets sSet is Cartesian closed, meaning that there exists an internal homomorphism simplicial set $Y^{X}$ between any two simplicial sets $X$ and $Y$ and natural bijections

$$
\operatorname{sSet}\left(Z, Y^{X}\right) \simeq \operatorname{sSet}(X \times Z, Y)
$$

for all $Z$. Hint: apply Rmk.1.1.11 for a clue on a potential formula for $\left(Y^{X}\right)_{n}$.
Now to some examples! As these examples are pretty central to the theory of simplicial sets and $\infty$-categories, we will officially make them definitions.
Definition 1.1.9. Given a topological space $X$, we have seen the singular (simplicial) set Sing $X$ from previous courses. To remind the reader, $(\operatorname{Sing} X)_{n}$ is the set of continuous maps $\left|\Delta^{n}\right| \rightarrow X$, where $\left|\Delta^{n}\right|$ is the topological $n$-simplex:

$$
\left|\Delta^{n}\right|=\left\{x=\left(x_{0}, \ldots, x_{n}\right) \in \mathbf{R}_{\geqslant 0}^{n+1} \mid \sum_{i=0}^{n} x_{i}=1\right\}
$$

From a more categorical perspective, the collection of objects $\left|\Delta^{n}\right|$ inside the category of topological spaces form a cosimplicial object, so a functor $\Delta \rightarrow$ Top, where the coface maps are induce by including these $n$-simplices into the boundaries of their higher dimensional counterparts, and the codegeneracy maps project into a subsimplex of their boundary. The functor Sing $X$ is then defined by mapping out of a cosimplicial topological space into a fixed $X$ :

$$
\operatorname{Sing} X=\operatorname{Top}\left(\left|\Delta^{\bullet}\right|, X\right)
$$

Definition 1.1.10. We define the simplicial set $\Delta^{n}$ as that represented by $[n]$ for some $n \geqslant 0$ :

$$
\Delta_{i}^{n}=\operatorname{Cat}([i],[n])
$$

We use similar notation as the topological $n$-simplex as the geometric realisation of this simplicial set is precisely the topological object. Similarly, as $n$-varies, $\Delta^{\bullet}$ cosimplicial object in sSet. Pictorially, one can write down the nondegenerate simplices ${ }^{1}$ of low dimensional $\Delta^{n}$ 's as follows:

$$
\Delta^{0}=\stackrel{x_{0}}{\bullet} \quad \Delta^{1}=\stackrel{x_{0}}{\bullet} \xrightarrow{x_{01}} \stackrel{x_{1}}{\bullet}
$$

![img-2.jpeg](img-2.jpeg)
![img-3.jpeg](img-3.jpeg)

Actually, the pictures above more closely resemble the image of maps $\Delta^{n} \rightarrow X$ into a simplicial set $X$. In the $\Delta^{2}$ example, there is a 2 -simplex which should be labelled 012 , and in the $\Delta^{3}$ example, there are 42 -simplices $(012,013,023,123)$ and a 3 -simplex $(0123)$ also not included in the notation.

The following observation is simply an application of the Yoneda lemma.
Remark 1.1.11 (Yoneda lemma and $n$-simplices). Let $X$ be a simplicial set. Then the set of $n$-simplices of $X$, written as $X_{n}$, are in bijection with the morphisms of simplicial sets $\Delta^{n} \rightarrow X$. Indeed, we define $\Delta^{n}$ as the presheaf $\Delta^{\text {op }} \rightarrow$ Set represented by $[n]$, hence we have the following natural equivalence by the Yoneda lemma:

$$
\operatorname{sSet}\left(\Delta^{n}, X\right)=\operatorname{Nat}(\Delta(-,[n]), X) \simeq X([n])=X_{n}
$$

Exercise 1.1.12. Use Exc.1.1.8 and Rmk.1.1.11 to show that if $X$ is a limit of simplicial sets $X_{i}$, then the natural map of mapping simplicial sets

$$
X^{T} \rightarrow \lim X_{i}^{T}
$$

is an isomorphism for all simplicial sets $T$.
We will often define (and have defined) simplicial sets using Rmk.1.1.11; see Df.1.1.9, Df.1.3.7, Df.1.3.17, and Df.1.7.1.

[^0]
[^0]:    ${ }^{1}$ It's not crucially important in these lectures, but a simplex $x \in X_{n}$ of a simplicial set $X$ is said to be nondegenerate if it is not in the image of the any of the degeneracy maps $s_{i}$.

Definition 1.1.13. For a nonnegative $n \geqslant 0$, we define the boundary of the $n$-simplex $\partial \Delta^{n}$ as the smallest subsimplicial set of $\Delta^{n}$ containing all $(n-1)$-simplicies by all nondegenerate simplices of dimension strictly less than $n$, in other words, the largest subsimplicial set of $\Delta^{n}$ which does not contain the unique nondegenerate $n$-simplex of $\Delta^{n}$. In particular, $\partial \Delta^{n}$ looks like $\Delta^{n}$ but with the single nondegenerate $n$-simplex $012 \cdots n$ removed. For some $0 \leqslant i \leqslant n$, we define the $i$-horn of $\Delta^{n}$ as the largest subsimplicial set of $\partial \Delta^{n}$ not containing the $(n-1)$ simplex $012 \cdots \bar{i} \cdots n$, so the unique nondegenerate $(n-1)$-simplex not containing $i$. The notation is supposed to suggest the picture (especially $\Lambda_{1}^{2}$ ):
![img-4.jpeg](img-4.jpeg)

In these cases above, the $\Lambda_{i}^{2}$ 's really do not contain any nondegenerate 2-simplices. The trick is:

To get $\Lambda_{i}^{n}$, delete the $(n-1)$-simplex of $\partial \Delta^{n}$ opposite the 0 -simplex $i$.
These horns play a fundamental role is defining what an $\infty$-category is.
Definition 1.1.14. An $\infty$-category is a simplicial set $C$ such that for each map $f: \Lambda_{i}^{n} \rightarrow C$, where $0<i<n$, there is a lift $L$ in the diagram of simplicial sets
![img-5.jpeg](img-5.jpeg)
where $\iota$ is the inclusion. A functor of $\infty$-categories is simply a map of simplicial sets.
Let us continue with this definition for a moment - it's justification will come through how one can implement analogues of ideas in classical category theory, how this concept captures homotopy theory, and our examples.

At this stage, we should mention that this is not morally what an $\infty$-category is. Such an object is something that we can do higher category theory with and within, regardless of how we actually define such an object. It is for this reason that the concept we have just defined is often called a quasicategory, and then one shows that this concept behaves well enough to be considered as a model for higher category theory; we'll see this over the next few weeks. Other models include simplicial and topological categories, as well as complete Segal spaces; some of these approaches are discussed in [Lur09b, §1].

Warning 1.1.16. One can (and should, at some stage) worry about size issues. For example, for us, an $\infty$-category has a set's worth of objects, but we all know that most categories we like have a class' worth of objects. This is a serious problem, but it's one that goes away once one whispers the words "Grothendieck universes". We leave the interested student to explore [Lur09b, §1.2.15] until her heart is content, but we will ignore such issues in this course. In short, only when you deal with functor categories and accessibility (also presentability) do these issues raise their heads again. Have a look at [Shu08] for a big discussion on why this topic is not to be totally ignored.
Exercise 1.1.17. Show tht $\partial \Delta^{n}$ is not an $\infty$-category for $n \geqslant 2$. Show that $\Lambda_{i}^{n}$ is not an $\infty$-category for $n \geqslant 3$ and all $0 \leqslant i \leqslant n$.

# 1.2 Basic notions and constructions in $\infty$-category theory 

Now that we have a notion of $\infty$-category, we would like to define all of the usual things from category theory.

Definition 1.2.1. Let $\mathcal{C}$ be an $\infty$-category. An object of $\mathcal{C}$ is a 0 -simplex, so an element of $\mathcal{C}_{0}$ or equivalently a map of simplicial sets $\Delta^{0} \rightarrow \mathcal{C}$. A morphism inside $\mathcal{C}$ is a 1 -simplex $f$, or equivalently a map of simplicial sets $g: \Delta^{1} \rightarrow \mathcal{C}$, whose domain is the 0 -simplex $f(0)=d_{1}(f)$ and whose codomain is the 0 -simplex $f(1)=d_{1}(f)$. Writing the domain of $f$ as $X$ and the codomain as $Y$, we will often write $f: X \rightarrow Y$ for a morphism in $\mathcal{C}$. We write $s_{0}(X)$ for the identity map on $X \in \mathcal{C}$ and is written as $\operatorname{id}_{X}: X \rightarrow X$.

Let us now make some definitions which play with the inner-horn condition of (1.1.15).
Definition 1.2.2. A homotopy between two morphisms $f, g: X \rightarrow Y$ in an $\infty$-category $\mathcal{C}$ is precisely a 2 -simplex $\sigma$ in $\mathcal{C}$ such that $d_{2}(\sigma)=f, d_{1}(\sigma)=g$, and $d_{0}(\sigma)=\operatorname{id}_{Y}$. Pictorially:
![img-6.jpeg](img-6.jpeg)

In this situation, we say that $f$ and $g$ are homotopic.
Exercise 1.2.3. Show that "the other" obvious definition of homotopy is equivalent to this one (using $\operatorname{id}_{X}$ instead). In other words, calling these two a priori different notions of left homotopic and right homotopic, show that two morphisms in an $\infty$-category $\mathcal{C}$ are left homotopic if and only if they are right homotopic.
Exercise 1.2.4. Show the notion of "homotopic" from above defines an equivalence relation on the set of morphisms between two fixed objects in an $\infty$-category.

Construction 1.2.5. Let $f$ and $g$ be two composable morphisms in an $\infty$-category $\mathcal{C}$, meaning that the codomain of $f$ matches the domain of $g: d_{0}(f)=d_{1}(g)$. Using the definition of an

$\infty$-category, the following solid diagram of simplicial sets admits a lift:
![img-7.jpeg](img-7.jpeg)

As indicated by the second diagram above, the first diagram does not only admit a lift $h$, but also a 2 -simplex $\sigma$ which witnesses that " $f$ composed with $g$ is $h$ ". We call $h$ a candidate for the composition $g \circ f$.

In the definition of an $\infty$-category, we do not ask such a candidate to be unique in any sense, so there could exist many such objects. This is not a problem though, both technically and morally. Indeed, we will see later that the simplicial set of all potential compositions is contractible, meaning that in a homotopy theoretic way, there is a unique choice of composition - the only difference here is that in the world of homotopy theory, the one point set is characterised by being contractible rather than literally being a set containing a single element. We've had not problems in classical category theory when we say "a colimit is unique up to unique isomorphism", and we won't have any problems with this homotopical style of uniqueness here.

Definition 1.2.6. Let $\mathcal{C}$ be an $\infty$-category. Define the homotopy category $\mathrm{hC}$ of $\mathcal{C}$ as the category whose objects are those of $\mathcal{C}$, whose morphisms are homotopy classes of morphisms in $\mathcal{C}$, and with composition given by Con.1.2.5.

Let us check well-definedness, in other words, that two candidates for composition agree in the homotopy category, ie, they agree up to homotopy. Let $f: X \rightarrow Y$ and $g: Y \rightarrow Z$ be two composable morphisms in $\mathcal{C}$, and let us write $h_{1}$ and $h_{2}$ for two candidate compositions, together with the 2 -cells $\sigma_{1}$ and $\sigma_{2}$ recognising that they are such candidates. To construct a homotopy between $h_{1}$ and $h_{2}$, consider the map $\Lambda_{1}^{3} \rightarrow \mathcal{C}$ as indicated by the diagram:
![img-8.jpeg](img-8.jpeg)
where the vertical map at the back is $g$ and the horizontal map at the front is $h_{2}$. To see this is indeed a $\Lambda_{1}^{3}$, we need to also fill in some of the 2 -cells, and this is done by setting the left 2 -cell to be $\sigma_{1}$, the right 2 -cell to be "identity 2 -cell" (so $s_{0}(g)$ ), and the upper 2-cell to be $\sigma_{2}$. As $\mathcal{C}$ is an $\infty$-category, we obtain a lift of this map, which in particular produces the lower 2-cell, giving us a homotopy between $h_{1}$ and $h_{2}$.

Exercise 1.2.7. Prove that $\mathrm{hC}$ is a well-defined 1-category, ie, as we just showed well-definedness of composition, show that composition is associative and unital.

Exercise 1.2.8. A commutative square in an $\infty$-category $C$ is a map of simplicial sets $\Delta^{1} \times \Delta^{1} \rightarrow$ $C$, which we usually draw as
![img-9.jpeg](img-9.jpeg)

Importantly, notice that a 2-cell is required, ie, it is not a choice of 1-morphisms such that the indicated composites are equal: there is a choice of a 2-cell witnessing this "equality" or "homotopy relation". Show that such a commutative square in an $\infty$-category induces a commutative square in $\mathrm{h} C$ in the sense you are used to. Conversely, show that given a commutative square in $\mathrm{h} C$, show that there exists a lift to a commutative square in $C$. How unique is such a lift?

# 1.3 Examples of $\infty$-categories 

Of course, our main goal will be to construct the $\infty$-category of spectra, which will take us a little while longer. In the meantime, there are three natural sources of $\infty$-categories for us; Kan complexes, nerves of 1-categories, and nerves of simplicial categories.

Definition 1.3.1. A simplicial set $X$ is called a Kan complex if for each $0 \leqslant i \leqslant n$ and each map $f: \Lambda_{i}^{n} \rightarrow X$, then for each diagram of the form (1.1.15), there exists a lift $L$.

Exercise 1.3.2. Let $X_{i}$ be a collection of nonempty simplicial sets and let $X$ be its product. Show that $X$ is a Kan complex if and only if each $X_{i}$ is a Kan complex.
Exercise 1.3.3. First, show that a group object in the category of simplicial sets is equivalent to a functor from $\Delta^{\text {op }}$ to the category of groups. Let's call such objects simplicial groups. Show that a simplicial group is a Kan complex.

Tautologically, all Kan complexes are $\infty$-categories. In fact, this gives us our first supply of $\infty$-categories.

Proposition 1.3.4. Let $X$ be a topological space. Then $\operatorname{Sing}(X)$ is a Kan complex.
Proof. This follows by adjunction. Indeed, we want to show that for all solid diagrams of simplicial sets
![img-10.jpeg](img-10.jpeg)
where exists a dashed arrow above such that the diagram commutes. By adjunction, this is equivalent to finding a dashed arrow in the category of topological spaces
![img-11.jpeg](img-11.jpeg)

Formulated into the language of Topology I \& II and Algebraic Topology I, we need to show that for each topological space $X$, the unique map $X \rightarrow *$ is a Serre fibration. We already know this though, so we're done.

It turns out that Kan complexes only give a very specific kind of $\infty$-category.
Proposition 1.3.5. Let $\mathcal{C}$ be an $\infty$-category. Then $\mathrm{hC}$ is a groupoid, ie, every morphism is an isomorphism, if and only if $\mathcal{C}$ is a Kan complex.

We will prove this using a little more technology later, see $\S 1.4$. This result also encourages some to call Kan complexes $\infty$-groupoids.

End of lecture 1 and week 1

Definition 1.3.6. A functor of $\infty$-categories is simply a morphism of simplicial sets.
This is one of the unreasonably simple definitions, but nevertheless, it works very well. It is clear then that Sing: $\mathcal{F}$ op $\rightarrow$ sSet defines a functor from topological spaces to $\infty$-categories, viewed for now as a subcategory of sSet.

Another collection of $\infty$-categories comes in the form of 1-categories.
Definition 1.3.7. Let $\mathcal{C}$ be an ordinary 1-category. We define a simplicial set $N(\mathcal{C})$ by setting $N(\mathcal{C})_{0}$ to be the objects of the category $\mathcal{C}$, and for positive $n$ we define $N(\mathcal{C})_{n}$ as the set of $n$-composable morphisms in $\mathcal{C}$. The face and degeneracy maps either compose morphisms or insert an identity morphism. To state this more formally, we can set that $N(\mathcal{C})_{n}$ is given by the set of functors Cat $([n], \mathcal{C})$, considering $[n]$ as a poset, with structure maps in our simplicial set being induced by varying $[n]$. Similar to Df.1.1.9, this construction is really given by mapping out of the cosimplicial object $[n]$ in Cat.

Considering $[n]$ as a poset for a moment, a functor $[0] \rightarrow \mathcal{C}$ to a category $\mathcal{C}$ is simply picking an object in $\mathcal{C},[1] \rightarrow \mathcal{C}$ is choosing a morphism between two objects, $[2] \rightarrow \mathcal{C}$ is choosing two composable morphisms, $[3] \rightarrow \mathcal{C}$ is choosing three composable morphisms, and so on. In particular, the simplicies of $N(\mathcal{C})$ understand the objects of $\mathcal{C}$, the morphisms of $\mathcal{C}$, as well as all of the composition laws-sounds it understands everything about $\mathcal{C}$, honestly.

The following exercise shows that passing from 1-categories to $\infty$-categories with this nerve construction does not loose any information. Moreover, it shows that the essential image of this nerve functor is rather boring - it also does not take the full advantage of $\infty$-categories!
Exercise 1.3.8. Prove the following facts about the nerve functor $N$ : Cat $\rightarrow$ sSet.

1. $N$ factors through the subcategory of sSet defined by $\infty$-categories.
2. The essential image of $N$ are those $\infty$-category with unique inner horn fillings.
3. $N$ is fully faithful.

4. The functor $N$ : Cat $\rightarrow$ sSet has a left adjoint, when restricted to the subcategory of $\infty$-categories, given by taking the homotopy category.
5. For an $\infty$-category $\mathcal{C}$, the unit map $\mathcal{C} \rightarrow N \mathrm{~h} \mathcal{C}$ is surjective on $n$-simplices for all $n \geqslant 0$.

Exercise 1.3.9. What kind of conditions must hold in a category $\mathcal{C}$ if $N(\mathcal{C})$ is a Kan complex?
Exercise 1.3.10. Show that the nerve functor $N$ : Cat $\rightarrow$ sSet commutes with finite products. Show that a natural transformation of functors of 1-categories $\alpha: F \Rightarrow G: \mathcal{C} \rightarrow \mathscr{D}$ induces a map of simplicial sets $N(\mathcal{C}) \times \Delta^{1} \rightarrow N(\mathscr{D})$ such that restriction to $N(\mathcal{C}) \times \Delta^{\{0\}}$ is $N(F)$ and restriction to $N(\mathcal{C}) \times \Delta^{\{1\}}$ is $N(G)$. Show that if $F: \mathcal{C} \rightarrow \mathscr{D}$ and $G: \mathscr{D} \rightarrow \mathcal{C}$ are two adjoint functors, then $N(\mathcal{C})$ and $N(\mathscr{D})$ are homotopy equivalent-here we define a homotopy equivalence of simplicial sets as one might expect from Topology I or II except we use $\Delta^{1}$ as our "interval object".

These two families of examples are nice, but they do not highlight what is interesting about $\infty$-categories at all! They just show that the homotopy theory of simplicial sets and the category theory of 1-categories fits nicely into this framework. To see a truly new example, we will use categories enriched in simplicial sets.

Definition 1.3.11. A simplicial category is a category $\Pi$ enriched over simplicial sets. This means that each mapping set $\Pi(X, Y)$ comes with the structure of a simplicial set, meaning that the zeroth simplices of the simplicial set $\Pi(X, Y)$ define the original set of morphisms, and the composition map

$$
\Pi(Y, Z) \times \Pi(X, Y) \rightarrow \Pi(X, Z)
$$

refines to a map of simplicial sets using the Cartesian product of simplicial sets. A simplicial functor of simplicial categories is a functor $F: \Pi \rightarrow \Pi$ equipped with maps of simplicial sets $\Pi(X, Y) \rightarrow \Pi(F X, F Y)$ which refine the usual structure of a functor. Write sCat for the category of simplicial categories and simplicial functors.

Exercise 1.3.12. Show that sSet has a natural simplicial category structure, or in other words, construct internal simplicial mapping sets internal to sSet.
Exercise 1.3.13. Show that a topological category $\Pi$ can be upgraded to a simplicial category using the singular set functor.

As we can already do homotopy theory with simplicial sets, it follows that we can already use simplicial categories as a model for higher categories! However, they will prove to be too technical for us (and most others) to use, so we will only use them as a source of $\infty$-categories. This will come in the form of a simplicial nerve functor; see [Lur09b, §1.1.5].

Definition 1.3.14. For each $n \geqslant 0$, define a simplicial category $\mathfrak{C}\left[\Delta^{n}\right]$ as follows:

- The objects of $\mathfrak{C}\left[\Delta^{n}\right]$ are the elements of $[n]$.
- Given $i, j \in[n]$, we define the simplicial set $\mathfrak{C}\left[\Delta^{n}\right](i, j)$ to be empty if $j<i$, and otherwise as the nerve of the poset $P_{i, j}$, itself defined as all subsets $I$ of $[n]$ such that $i, j \in I$ and for all $k \in I$, we have $i \leqslant k \leqslant j$.

- For $i \leqslant j \leqslant k$, the composition map

$$
\mathfrak{C}\left[\Delta^{n}\right](j, k) \times \mathfrak{C}\left[\Delta^{n}\right](i, j) \rightarrow \mathfrak{C}\left[\Delta^{n}\right](i, k)
$$

is induced from taking the nerve of the map of partially ordered sets $P_{j, k} \times P_{i, j} \rightarrow P_{i, k}$ which sends $\left(I_{1}, I_{2}\right)$ to the union $I_{1} \cup I_{2}$.

The simplicial category $\mathfrak{C}\left[\Delta^{n}\right]$ is a thickened up version of $[n]$ itself-the higher simplices of $\mathfrak{C}\left[\Delta^{n}\right]$ parametrise all possible choices of composition of morphisms. More explicitly, first notice that both categories have the same objects, by definition. Given $i \leqslant j$, then in $[n]$ there is a unique morphism $i \rightarrow j$, where as in $\mathfrak{C}\left[\Delta^{n}\right]$ there is a vertex in $\mathfrak{C}\left[\Delta^{n}\right](i, j)$ for each subset $S \subseteq[n]$ containing both $i$ and $j$, and such that if $k \in S$ then $i \leqslant k \leqslant j$. However, although there are many different maps from $i \rightarrow j$ in $\mathfrak{C}\left[\Delta^{n}\right]$, the simplicial set $\mathfrak{C}\left[\Delta^{n}\right](i, j)$ is always contractible, its geometric realisation is homeomorphic to the cube $\left|\Delta^{1}\right|^{\jmath-i-1}$, meaning that all choices are canonically equivalent.

More explicitly, notice that $\mathfrak{C}\left[\Delta^{0}\right]$ and $\mathfrak{C}\left[\Delta^{1}\right]$ are simply [0] and [1], respectively. For a more interesting example, consider $\mathfrak{C}\left[\Delta^{2}\right]$. This is the simplicial category whose objects are labelled $0,1,2$, and with morphism simplicial sets $N P_{0,1}, N P_{1,2}$, and $N P_{0,2}$-we will suppress settheoretic notation such as brackets when discussing the morphisms. The first two simplicial sets are just the constant simplicial sets on a unique morphism, denoted as 01 and 12, respectively. Moreover, the composition law in $\mathfrak{C}\left[\Delta^{2}\right]$ tells us that the composite of 01 with 12 is just there union 012 , which is a morphism from 0 to 2 . The whole simplicial set of morphisms $N P_{0,2}$ has two vertices corresponding to the two subsets 02 and 012 , and as these sets are contained within each other, there is a 1 -simplex in $N P_{0,2}$ connecting them. This means a map $02: 0 \rightarrow 2$ and a homotopy from 02 to the composition $12 \circ 01=012$. In other words, we can draw $\mathfrak{C}\left[\Delta^{2}\right]$ as the 2 -simplex
![img-12.jpeg](img-12.jpeg)

We can make the connection between $[n]$ and $\mathfrak{C}\left[\Delta^{n}\right]$ more concrete too: considering $[n]$ as a simplicial category with mapping simplicial sets constant, written as $[n]$, then there is a functor $\varepsilon: \mathfrak{C}\left[\Delta^{n}\right] \rightarrow[n]$ crushing all higher simplices in simplicial mapping sets. As all of the simplicial mapping sets in $\mathfrak{C}\left[\Delta^{n}\right]$ are contractible, this map is an equivalence of simplicial categories - a concept we have not, and will not define. Regardless, this functor $\varepsilon$ can be used to show that $\mathfrak{C}\left[\Delta^{n}\right]$ is the "free simplicial category" associated to the category $[n]$, as it yields the following natural isomorphism for any simplicial category $\Pi$

$$
\operatorname{sCat}\left(\mathfrak{C}\left[\Delta^{n}\right], \Pi \mid \stackrel{\varepsilon^{*}, \simeq}{\longleftrightarrow} \operatorname{sCat}([n], \Pi \mid) \simeq \operatorname{Cat}([n], \Pi \mid) ;\right.
$$

this last equivalence used the fact that the constant simplicial set functor from Set to sSet is left adjoint to the forgetful functor.
Exercise 1.3.16. Check that the assignment $\Delta \rightarrow$ sCat, from the simplex category to the category of simplicial categories, sending $[n]$ to $\mathfrak{C}\left[\Delta^{n}\right]$ defines a cosimplicial object, ie, a cosimplicial simplicial category (never say that again).

Definition 1.3.17. Let $m$ be a simplicial category. The simplicial (or coherent) nerve $N m$ of $m$ is the simplicial set defined by the formula

$$
\operatorname{sSet}\left(\Delta^{n}, N m\right)=\operatorname{sCat}\left(\mathfrak{C}\left[\Delta^{n}\right], m\right)
$$

Example 1.3.18. Let $C$ be a 1-category, which we consider as a simplicial category by setting all of the mapping simplicial sets to be constant, written as $\underline{C}$. Then the simplicial nerve of $\underline{C}$ is naturally equivalent to the usual nerve over $C$. Indeed, this follows from (1.3.15) and the Yoneda lemma, as

$$
N \underline{C}_{n} \simeq \operatorname{sSet}\left(\Delta^{n}, N \underline{C}\right) \simeq \operatorname{sCat}\left(\mathfrak{C}\left[\Delta^{n}\right], \underline{C}\right) \simeq \operatorname{Cat}([n], C)=\operatorname{sSet}\left(\Delta^{n}, N C\right) \simeq N C_{n}
$$

Warning 1.3.19. Given a simplicial category $m$, we can consider this as a 1-category by forgetting all of the higher simplices. The usual nerve of this 1-category is not equivalent to the simplicial nerve of $m$.

Despite the warning above, we will write $N m$ for the simplicial nerve construction, even though it might be confused with the usual nerve of Df.1.3.7; the reader will just have to understand what we mean from context.

What's important to us about this simplicial nerve construction, is that it can be used to produce $\infty$-categories.

Proposition 1.3.20. Let $m$ be a simplicial category such that for all $X, Y$ in $m$ the simplicial set $m(X, Y)$ is a Kan complex; see Df.1.3.1. Then $N m$ is an $\infty$-category.

Proof. Given a map of simplicial sets $f: \Lambda_{i}^{n} \rightarrow N m$ with $0<i<n$, we want to construct a lift $F: \Delta^{n} \rightarrow N m$. Unwinding the definitions, this translates into the lifting problem of simplicial sets
![img-13.jpeg](img-13.jpeg)
where $S$ is the subsimplicial set of $\mathfrak{C}\left[\Delta^{n}\right](0, n)$ spanned by all of the subsets excluding the maximal subset $\{0, \ldots, n\}$ and the maximal subset less the element $i$. A priori one might expect to have lifting problems mapping into $m(f(j), f(k))$ for each $j \leqslant k$, however, the inner horn $\Lambda_{i}^{n}$ is a union of $(n-1)$-simplices of $\Delta^{n}$, so only this maximal length case is of interest.

Our assumption about the simplicial mapping sets for $m$ being Kan complexes now comes into play. As $m(f(0), f(n))$ is a Kan complex, so we know we can solve lifting problems for all horn inclusions $\Lambda_{j}^{k} \subseteq \Delta^{k}$ for all $0 \leqslant j \leqslant k$. In particular, we can explicitly see in this case that the inclusion $S \subseteq \mathfrak{C}\left[\Delta^{n}\right](0, n)$ is a finite pushout of such horn inclusions; geometrically, $\mathfrak{C}\left[\Delta^{n}\right](0, n)$ is an $(n-1)$-cube $\left|\Delta^{1}\right|^{n-1}$ and $S$ is the subcomplex given by removing the interior and the $i$ th face.

Proposition 1.3.21. Let $m$ be a simplicial category such that $m(X, Y)$ is a Kan complex. Then the morphism sets $\mathrm{h} N m(X, Y)$ can be naturally identified with $\pi_{0} m(X, Y)=$ $\pi_{0}|\mathcal{M}(X, Y)|$.

Proof. From the definition of the homotopy category of an $\infty$-category, it suffices to check that two maps $f, g: X \rightarrow Y$ in $N \mathcal{M}$ are homotopic à la Df.1.2.2 if and only if there is a map of simplicial sets $H: \Delta^{1} \rightarrow \mathcal{M}(X, Y)$ such that $H(0)=f$ and $H(1)=g$. This comes down to a calculation of the 2 -simplices of $N \mathcal{M}$, which falls out of our computation of $\mathfrak{C}\left[\Delta^{2}\right]$ above; see the discussion after Df.1.3.14.

One of our favourite examples of a simplicial category satisfies the conditions of Pr.1.3.20. Exercise 1.3.22. Show that in Kan, the full simplicial subcategory of sSet spanned by the Kan complexes, the mapping simplicial sets are all themselves Kan complexes.

This leads us to one of the most fundamental definitions in this course.
Definition 1.3.23. We define the $\infty$-category of anim $\boldsymbol{e}$ as the simplicial nerve of Kan, and denote it by $\mathcal{A}$ n. The $\infty$-category of pointed anim $\boldsymbol{e}$ is the simplicial nerve of $\mathrm{Kan}_{*}$ of pointed Kan complexes.

As the singular set functor Sing: $\mathcal{T}$ op $\rightarrow$ sSet sends topological spaces to Kan complexes, see Pr.1.3.4, we see that for each literal topological space $X$, we have an object $X$ inside $\mathcal{A}$ n (with an implicit singular set functor). The word anima will be used from now on to discuss a Kan complex (or a topological space via Sing) as an object in this $\infty$-category.
Remark 1.3.24. It is a little disappointing, perhaps, to define such a fundamental $\infty$-category so explicitly, rather than defining it using purely the theory of $\infty$-categories. However, the reader should recall how they first dealt with 1-category theory, and how the 1-category of sets was just placed in their lap, with all of the usual baggage of set theory, and then one proves fundamental results like the Yoneda lemma etc. Something similar is happening here, and in our opinion, the easiest way to introduce these concepts to the reader for the first time is with the explicit definition given above. On the other hand, the $\infty$-category of animæ does have a universal property: it is the free $\infty$-category generated by a single element under colimits; see both [Lur09b, Th.5.1.5.6 \& Cor.5.1.5.8].

We will see many facts about $\infty$-categories which we will need later, and we will also see many facts about 1 -categories generalised to $\infty$-categories.

Definition 1.3.25. We define the $\infty$-category of $\infty$-categories Cat $_{\infty}$ as the simplicial nerve of the simplicial subcategory of sSet spanned by the $\infty$-categories and we take simplicial mapping sets to be the largest Kan complex within the given simplicial mapping set.

Notation 1.3.26. Now that we have seen the classical and the simplicial nerve functors, we will often suppress them from our notation. This means that if $C$ is a classical 1-category or $\mathcal{M}$ is a simplicial category whose mapping simplicial sets are all Kan complexes, then we will discuss there properties freely in the language of $\infty$-categories by implicitly applying a classical or simplicial nerve functor.

Strictly speaking, the only two $\infty$-category we really need to define using the simplicial nerve for this course are $\mathcal{A}$ n and $\mathrm{Cat}_{\infty}$. From these we will eventually end up with the $\infty$ category of spectra and everything we want about it.

The following exercise discusses another classical construction of an $\infty$-category whose homotopy category the reader may already be familiar with: the (bounded below) derived category of a ring.
Exercise 1.3.27. Fix a commutative ring $R .^{2}$ Let us write $\operatorname{Ch}(R)$ for the 1-category of $R$-chain complexes and $\operatorname{Ch}(R)_{\geqslant 0}$ for the subcategory spanned by $R$-chain complexes concentrated in nonnegative degrees.

1. Show that the inclusion functor $\operatorname{Ch}(R)_{\geqslant 0} \rightarrow \operatorname{Ch}(R)$ has a right adjoint $\tau_{\geqslant 0}$, which is given concretely on objects by sending an $R$-chain complex $M_{*}$ to $\tau_{\geqslant 0} M_{*}$ defined level-wise as follows:

$$
\left(\tau_{\geqslant 0} M_{*}\right)_{n}= \begin{cases}M_{n} & n \geqslant 1 \\ \operatorname{ker}\left(\partial: M_{0} \rightarrow M_{-1}\right) & n=0 \\ 0 & n \leqslant-1\end{cases}
$$

Show that the counit of this adjunction $\tau_{\geqslant 0} M_{*} \rightarrow M_{*}$ induces an isomorphism on homology in nonnegative degrees.
2. Let $C_{*}(-; R): \operatorname{sSet} \rightarrow \operatorname{Ch}(R)$ be the normalised Moore complex functor, quasi-isomorphic to that of Topology I and II, sending a simplicial set $X$ to the chain complex $C_{*}(X ; R)$ where $C_{n}(X ; R)$ is the free $R$-module on the nondegenerate $n$-simplicies $X_{n}^{\text {nd }}$ of $X$ and with boundary map given by

$$
\partial(\sigma)=\sum_{i=0}^{n}(-1)^{i} \begin{cases}d_{i}(\sigma) & d_{i}(\sigma) \in X_{n-1}^{\mathrm{nd}} \\ 0 & d_{i}(\sigma) \notin X_{n-1}^{\mathrm{nd}}\end{cases}
$$

on a nondegenerate $n$-simplex $\sigma$. Show that $n \mapsto C_{*}\left(\Delta^{n} ; R\right)$ defines a cosimplicial object in $\operatorname{Ch}(R)$.
3. Let DK: $\operatorname{Ch}(R) \rightarrow$ sSet be the functor defined by sending $M_{*}$ to $\operatorname{Ch}(R)\left(C_{*}\left(\Delta^{n} ; R\right), M_{*}\right)$. Upgrade $\operatorname{Ch}(R)$ to a simplicial category by letting $\operatorname{Ch}(R)\left(M_{*}, N_{*}\right)$ be the simplicial set $\tau_{\geqslant 0} \operatorname{DK}\left(\left[M_{*}, N_{*}\right]_{*}\right)$, where $\left[M_{*}, N_{*}\right]_{*}$ is the internal homomorphism $R$-chain complex.

Using the above exercise, combined with Exc.1.3.3 to see that the mapping simplicial sets are all Kan complexes, we find ourselves in the position to define $\mathscr{D}^{-}(R)$.

Definition 1.3.28. Let $\operatorname{Ch}(R)_{0}^{-}$denote the subcategory of $\operatorname{Ch}(R)$ spanned by projective $R$-chain complexes which are bounded above. We define $\mathscr{D}^{-}(R)$ as the simplicial nerve of $\operatorname{Ch}(R)_{0}^{-}$.

An object of $\mathscr{D}^{-}(R)$ is just a bounded above projective $R$-chain complex, morphisms are morphisms of complexes, and the higher morphisms can also be related to homotopies of complexes.

The definition of the unbounded derived category requires more work; see [Lur17, §1.3].

[^0]
[^0]:    ${ }^{2}$ Further generalisations to various abelian category is possible, see [Lur17, §1.3]

With $\infty$-categories such as $\mathcal{A} \mathrm{n}, \mathrm{Cat}_{\infty}$, and $\mathscr{D}^{-}(R)$ now at hand, let us mention a few ways we can work with these objects.

Definition 1.3.29. Let Ab be the category of abelian groups, considered to be a simplicial category by setting all higher simplices in mapping simplicial sets to be degenerate. Then the $\pi_{n}$ functor

$$
\operatorname{Kan}_{*} \xrightarrow{|-|} \mathcal{J}_{\mathrm{op}_{*}} \xrightarrow{\pi_{n}} \mathrm{Ab}
$$

from pointed Kan complexes to Ab is simplicial, so there is an associated functor of $\infty$ categories

$$
\pi_{n}: \mathcal{A}_{\mathrm{n}_{*}} \rightarrow \mathrm{Ab}
$$

from Eg.1.3.18.
Exercise 1.3.30. Give an alternative construction of $\pi_{n}$ using the adjunction found in Exc.1.3.8.
Replacing $\pi_{n}$ with $\pi_{1}$ (resp. $\pi_{0}$ ) and Ab with the category of groups (resp. sets), we obtain the expected $\pi_{0}$ and $\pi_{1}$ functors too.

Theorem 1.3.31 (Whitehead theorem for animæ). Let $f: X \rightarrow Y$ be a morphism in $\mathcal{A} \mathrm{n}_{*}$. Then $f$ is an equivalence in $\mathrm{h} \mathcal{A} \mathrm{n}$ if and only if $\pi_{n} f$ is an isomorphism for all $n \geqslant 0$.

Proof. First, notice that if $f$ is an equivalence, then it induces an isomorphism on all homotopy groups. This is purely formal, as a functor of $\infty$-categories sends equivalences to equivalences, and $\pi_{n}$ are all functors of $\infty$-categories by definition. Conversely, given a map $f: X \rightarrow Y$ inside $\mathcal{A} \mathrm{n}_{*}$ inducing an equivalence on all homotopy groups. We know that morphisms in $\mathcal{A} \mathrm{n}_{*}$ are precisely given by the 1 -simplices of $N \mathrm{Kan}_{*}$, which we know to be simply the morphisms inside $\mathrm{Kan}_{*}$, so our given $f$ can be chosen to be a map of pointed Kan complexes. Now we use the simplicial Whitehead theorem, which states that a morphism of Kan complexes inducing an isomorphism on all homotopy groups is necessarily a homotopy equivalence, which yields our desired homotopy inverse.

In particular, notice that the proof above would have fallen a part if we had used all of sSet as our definition for $\mathcal{A}$ n, as the mapping simplicial sets in sSet are not generally Kan complexes.

We also define equivalences for a general $\infty$-category.
Definition 1.3.32. A morphism $f: X \rightarrow Y$ in an $\infty$-category $C$ is called an equivalence if its image in $\mathrm{h} C$ is an isomorphism.

We, and others, sometimes call equivalences in $\infty$-categories isomorphisms.
In some of our favourite $\infty$-categories we will have a kind of Whitehead's theorem, ie, we can check if a morphism is an equivalence by checking if it induces an isomorphism on all homotopy groups; see Ths.1.3.31 and 2.2.7.

# 1.4 Fibrations of simplicial sets 

Before we continue with our study of $\infty$-categories, we have to improve our study of fibrations of simplicial sets. The goal of this section is to construct functor $\infty$-categories (Pr.1.4.17) and $\infty$-subcategories (Df.1.4.19), prove that hC is a groupoid if and only if $C$ is a Kan complex (1.3.5), and set-up some theory that will come later.

Notation 1.4.1. If we want to specify a pretty obvious map $\Delta^{i} \rightarrow \Delta^{n}$, then we might write $\Delta^{S} \rightarrow \Delta^{n}$ where $S \subseteq[n]$ with $|S|=i$. The indicated map is induced by post-composition with the inclusion $S \rightarrow[n]$ after identifying $[i]$ with $S$ as a poset. For example, $\Delta^{(1)} \rightarrow \Delta^{1}$ indicates the inclusion of $\Delta^{0}$ into $\Delta^{1}$ at the terminal point.

Definition 1.4.2. Let $f: X \rightarrow Y$ be a map of simplicial sets. We say that $f$ is an inner (resp. left, right) fibration if for all solid diagrams of the form
![img-14.jpeg](img-14.jpeg)
where $\Lambda_{i}^{n} \rightarrow \Delta^{n}$ is the natural inclusion and $0<i<n$ (resp. $0 \leqslant i<n, 0<i \leqslant n$ ), one can find a dashed arrow rending the above diagram commutative. In other words, $f$ has the right lifting property with respect to all of the indicated horn inclusions.

The following exercises might help familiarise the reader with the concepts of left and right fibration.
Exercise 1.4.3. Given a simplicial set $X$ and a 1-category $C$, show that a map of simplicial sets $X \rightarrow C$ is an inner fibration if and only if $X$ is an $\infty$-category.
Exercise 1.4.4. Let $F: C \rightarrow \mathscr{D}$ be a right or left fibration of $\infty$-categories. Show that $F$ is conservative, meaning that if $F f$ is an equivalence in $\mathscr{D}$, then $f$ is an equivalence in $C$.
Exercise 1.4.5. Let $F: C \rightarrow \mathscr{D}$ be a left fibration of $\infty$-categories. Show that for all objects $Y$ in $C$ and equivalences $f: X \rightarrow F Y$, there exists a morphism $\tilde{f}: \tilde{X} \rightarrow Y$ in $C$ such that $F \tilde{f}=f$. Can you formulate and prove the analogous statement for right fibrations?
Exercise 1.4.6. We call a map of simplicial sets $X \rightarrow Y$ a trivial Kan fibration if it has the right lifting property with respect to the inclusions $\partial \Delta^{n} \rightarrow \Delta^{n}$ for all $n \geqslant 0$. Show that a trivial Kan fibration $X \rightarrow Y$ induces a homotopy equivalence upon taking geometric realisations.

Dual to the various fibrations, are various "nice inclusions", which we call anodyne maps.
Definition 1.4.7. A map of simplicial sets $A \rightarrow B$ is inner (resp. left, right) anodyne if it has the left lifting property with respect to all inner (resp. left, right) fibrations.

Now, we have to commit ourselves to some combinatorics of simplicial sets.
Definition 1.4.8. A class of morphisms $S$ in a category $C$ is weakly saturated if the following three conditions hold:

1. $S$ is closed along arbitrary base change (pushouts) in $C$.
2. $S$ is closed under transfinite composition in $C$.
3. $S$ is closed under the formation of retracts in $C$.

Given an arbtitrary class of morphisms $S$ in $C$, then the weakly saturated hull of $S$ is the smallest collection of morphisms in $C$ which is weakly saturated and contains $S$.

The reason for being interested in weakly saturated classes is that they often allow us to boil down general statements to specific ones. For example:

Proposition 1.4.9. The weakly saturated hull of $\left\{\partial \Delta^{n} \rightarrow \Delta^{n}\right\}_{0 \leqslant n}$ in sSet is the class of morphisms of simplicial sets which are level-wise injective.

The proof of this proposition is outlined in the following exercise.
Exercise 1.4.10. Let $X$ be a simplicial set and $A \subset X$ a simplicial subset.

1. For any $k \geqslant-1$, we define the simplicial subset $\mathrm{Sk}^{k} X \subseteq X$ by setting $\left(\mathrm{Sk}^{k} X\right)_{n}$ to be the union of all $f^{*}(x) \in X_{n}$, for all $f:[n] \rightarrow[j]$ in $\Delta$ with $0 \leqslant j \leqslant k$. In particular, $\mathrm{Sk}^{-1} X$ is empty. Show that there are natural maps $\mathrm{Sk}^{k} X \rightarrow \mathrm{Sk}^{k+1} X$ and that the colimit along these maps is naturally isomorphic to $X$.
2. Show that for all $k \geqslant 0$, the commutative diagram of simplicial sets
![img-15.jpeg](img-15.jpeg)
where the $X_{k}^{\text {nd }}$ indicates the $k$-vertices of $X$ which are nondegenerate, so not in the image of any maps $f^{*}: X_{j} \rightarrow X_{k}$ for $j<k$, is a pushout.
3. Show that $A \subseteq X$ can be written as a countable composite of pushouts and coproducts of inclusions $\partial \Delta^{n} \rightarrow \Delta^{n}$. In particular, prove Pr.1.4.9.

Exercise 1.4.11. If $C$ is an $\infty$-category, show by way of example that $\mathrm{Sk}_{n} C$ might not necessarily be an $\infty$-category. What if $C$ is a Kan complex?

With minimal changes, one can also calculated weakly saturated hulls of various horn inclusions.

Proposition 1.4.12. The weakly saturated hull of $\left\{\Lambda_{i}^{n} \rightarrow \Delta^{n}\right\}_{0 \leqslant i<n}$ in sSet is the class of left anodyne maps. The weakly saturated hull of $\left\{\Lambda_{i}^{n} \rightarrow \Delta^{n}\right\}_{0<i<n}$ in sSet is the class of inner anodyne maps.

The rest of this section is exploiting this idea of weakly saturated hulls and some combinatorics of simplicial sets. First, a reworking of the definition of an $\infty$-category.

Definition 1.4.13. Let $K$ and $C$ be simplicial sets. We define the simplicial set Fun $(K, C)$ as the internal mapping simplicial set from $K$ to $C$.

We will shortly see (Pr.1.4.17) that if $C$ is an $\infty$-category, then Fun $(K, C)$ is also an $\infty$ category, and will be called the $\infty$-category of functors from $K$ to $C$-it will be useful that $K$ is not necessarily an $\infty$-category. Let us first reformulate the Kan condition with mapping simplicial sets.
Proposition 1.4.14 (Homotopy lifting property). Let $X$ be a simplicial set. Then the following conditions are equivalent:

1. $X$ is a Kan complex.
2. For every $n \geqslant 0$ and every solid commutative diagram of simplicial sets
![img-16.jpeg](img-16.jpeg)
there is a lifting indicated by the dashed arrow.
3. For every level-wise injection of simplicial sets $A \rightarrow B$ and every solid commutative diagram of simplicial sets
![img-17.jpeg](img-17.jpeg)
there is a lifting indicated by the dashed arrow.
In particular, the last condition shows that any level-wise injection of simplicial sets has the homotopy lifting property. In other words, we would not be out of line calling such maps cofibrations as in Topology I.

The following statement is proven similarly to the above, except there are a few more sticky details; see [Lur09b, §2.3.2] and [Lurb, Tag 007F] for more.
Proposition 1.4.15. Let $C$ be a simplicial set. Then the following conditions are equivalent:

1. $C$ is an $\infty$-category.
2. For every $n \geqslant 0$ and every solid commutative diagram of simplicial sets
![img-18.jpeg](img-18.jpeg)
there is a lifting indicated by the dashed arrow.

3. For every level-wise injection of simplicial sets $A \rightarrow B$ and every solid commutative diagram of simplicial sets
![img-19.jpeg](img-19.jpeg)
there is a lifting indicated by the dashed arrow.
Notice that this theorem implies something we have always said about the composition in an $\infty$-category: that it is unique up to contractible choice. Indeed, take two composable morphisms $f: X \rightarrow Y$ and $g: Y \rightarrow Z$ in some $\infty$-category $\mathcal{C}$. The anima of compositions is given by the formula

This is the fibre of the right-vertical maps in Pr.1.4.15, which are trivial Kan fibrations by Pr.1.4.15, meaning they lift against all boundary inclusions of simplices. This means that these right vertical maps are weak homotopy equivalences (see Exc.1.4.16) and hence has contractible fibres.
Exercise 1.4.16. Prove that a map $f: X \rightarrow Y$ of topological spaces which admits solutions to all lifting diagrams where the left-hand vertical map is an inclusion $S^{n} \rightarrow D^{n+1}$, is a weak homotopy equivalence. In particular, show its homotopy fibre is contractible. Compare with Exc.1.4.6.

The proof of Pr.1.4.14 will be the first real combinatorial test of these lectures (for the lecturer at least).

Proof. Clearly $3 \Rightarrow 2$ and $2 \Rightarrow 3$ follows from the weakly saturated hulls from Pr.1.4.9. Indeed, if we assume 2, then we formally see that $X^{\Delta^{1}} \rightarrow X$ admits lifts against anything in the weakly saturated hull of the boundary inclusions $\partial \Delta^{n} \rightarrow \Delta^{n}$. For $1 \Rightarrow 2$, we let $X$ be a Kan complex and by some formal manipulations, we are left to show every map

$$
f:\left(\partial \Delta^{n} \times \Delta^{1}\right) \underset{\partial \Delta^{n} \times\{0\}}{\cup}\left(\Delta^{n} \times\{0\}\right) \rightarrow X
$$

can be extended over $\Delta^{n} \times \Delta^{1}$. We will now define a series of subcomplexes of $\Delta^{n} \times \Delta^{1}$, denoted as $A(i)$ for each $0 \leqslant k \leqslant n+1$, such that $A(i)$ is a pushout of $A(i-1)$ along $\Lambda_{i}^{n+1} \rightarrow \Delta^{n+1}, A(0)$ is the domain of $f$, and $A(n+1)=\Delta^{n} \times \Delta^{1}$. Given such subcomplexes, we would be done, as we would obtain all of the desired lifts as $X$ is a Kan complex. To define these complexes, notice that the $n$-simplices of $\Delta^{n} \times \Delta^{1}$ are indexed by order preserving maps $[n+1] \rightarrow[n] \times[1]$. We then define a collection of $(n+1)$-simplices of $\Delta^{n} \times \Delta^{1}$ as the maps

$$
\sigma_{k}:[n+1] \rightarrow[n] \times[1] \quad \sigma_{k}(m)= \begin{cases}(m, 0) & m \leqslant k \\ (m-1,1) & m>k\end{cases}
$$

In other words, these $(n+1)$-simplices start at $(0,0)$, follow the back face of $\Delta^{n}$, so $\Delta^{n} \times \Delta^{\{0\}}$ up to $k$, before then cross over to front $\Delta^{n}$, so $\Delta^{n} \times \Delta^{\{1\}}$. For instance, in the example below for $n=1, \sigma_{0}$ is the upper-right 2 -simplex and $\sigma_{1}$ is the lower-left 2 -simplex:
![img-20.jpeg](img-20.jpeg)

This is maybe even better viewed in the $n=2$-case:
![img-21.jpeg](img-21.jpeg)

Here, vertices in the image of $\sigma_{0}$ are all of the vertices in the right 2 -simplex as well as $(0,0)$, and the vertices in the image of $\sigma_{2}$ are all of the vertices in the left 2 -simplex as well as $(1,2)$. In particular, notice that $\sigma_{n}$, when restricted to $\Lambda_{0}^{n}$, lies within $A(0)$. We then define $A(1)$ as the pushout of the inclusion $\Lambda_{0}^{n+1} \rightarrow \Delta^{n+1}$ along this restriction of $\sigma_{n}$ to $\Lambda_{0}^{n}$, which factors through $A(0)$. We continue, in this manner, and inductively define $A(k+1)$ by gluing $\Delta^{n+1}$ to $A(k)$ via $\sigma_{n-k}$ restricted to $\Lambda_{n-k}^{n+1}$, which we note factors through $A(k) \subseteq \Delta^{n} \times \Delta^{1}$. For example, we have the following inclusions $A(0) \subseteq A(1) \subseteq A(2)$ for $n=1$ :
![img-22.jpeg](img-22.jpeg)

This gives our desired filtration in terms of iterated pushouts of horn inclusions, which we can therefore lift upon.

# End of lecture 3 

Conversely, to see that $3 \Rightarrow 1$, we start with an arbitrary $f: \Lambda_{i}^{n} \rightarrow X$ for some $0 \leqslant i \leqslant n$. For $0<j \leqslant n$, define a morphism $r_{j}:[n] \times[1] \rightarrow[n]$ as the identity on $[n] \times\{1\}$ and the map sending $(m, 0)$ to $m$ if $m \neq j$ and $m-1$ if $m=j$. We also define $r_{0}$ similarly, except now $r_{0}(m, 0)$ is $m$ for $m \neq 0$ and 1 for $m=0$. These are homotopies between the projection $\Delta^{n} \rightarrow \Delta^{n}$ onto the $(n-1)$-simplex not containing $j$ as a vertex and the identity on $\Delta^{n}$. In particular, notice that for $i \neq j$, we have $r_{j}\left(\Delta^{n} \times \Delta^{\{0\}}\right) \subseteq \Lambda_{i}^{n} \subseteq \Delta^{n}$-in fact, it is contained within $\Delta^{[n]-j}$-and that $r_{j}\left(\Lambda_{i}^{n} \times \Delta^{1}\right) \subseteq \Lambda_{i}^{n}$. This allows us to define morphisms

$$
g_{0}: \Lambda_{i}^{n} \times \Delta^{1} \xrightarrow{r_{j}} \Lambda_{i}^{n} \xrightarrow{f} X
$$

$$
g_{1}: \Delta^{n} \times \Delta^{\{0\}} \xrightarrow{r_{j}} \Lambda_{i}^{n} \xrightarrow{f} X
$$

for some $j \neq i$. Notice that by design, these maps $g_{0}$ and $g_{1}$ agree on $\Lambda_{i}^{n} \times\{0\}$ and that $g_{0}$ restricted to $\Lambda_{i}^{n} \times \Delta^{\{1\}}$ is precisely $f$, as $r$ is the identify on $\Delta^{n} \times \Delta^{\{1\}}$. This gives a commutative diagram of simplicial sets
![img-23.jpeg](img-23.jpeg)
where $g_{0}$ is more honestly the adjoint of $g_{0}$ defined above. From our hypotheses we obtain a lift $L$ in the above diagram, and the solution to our original lifting problem involving $f$ is then the restriction of the adjunction of $L$ to $\Delta^{n} \times \Delta^{\{1\}}$, as $g_{0}$ restricted to $\Lambda_{i}^{n} \times \Delta^{\{1\}}$ is $f$.

The first real use of these equivalent definition of Kan complexes and $\infty$-categories comes with functor $\infty$-categories.

Proposition 1.4.17. Let $K$ be a simplicial set and $\mathcal{C}$ be an $\infty$-category. Then the mapping simplicial set $\mathcal{C}^{K}$ is an $\infty$-category, which we denote by $\operatorname{Fun}(K, \mathcal{C})$.

Proof. Using Pr.1.4.15, the lifting problem we want to solve is
![img-24.jpeg](img-24.jpeg)
for any level-wise injection $A \rightarrow B$. By adjunction, this is equivalent to the lifting problem
![img-25.jpeg](img-25.jpeg)
which by Pr.1.4.15 we know has a solution as $\mathcal{C}$ is an $\infty$-category.
Exercise 1.4.18. Determine the data of a functor $F: \operatorname{Sing}(X) \rightarrow N \mathcal{C}$, where $X$ is a topological space and $\mathcal{C}$ is a 1-category, and relate it to the concept of local systems from Algebraic Topology I.

Using the theory of inner fibrations, we can also define $\infty$-subcategories.
Definition 1.4.19. Let $\mathcal{C}$ be an $\infty$-category. An $\infty$-subcategory of $\mathcal{C}$ is a simplicial subset $\mathcal{C}_{0}$ of $\mathcal{C}$ such that the inclusion $\mathcal{C}_{0} \rightarrow \mathcal{C}$ is an inner fibration.

Exercise 1.4.20. Let $\mathcal{C}$ and $\mathscr{D}$ be $\infty$-categories, $\mathscr{D}_{0}$ be an $\infty$-subcategory of $\mathscr{D}$, and $f: \mathcal{C} \rightarrow \mathscr{D}$ a functor of $\infty$-categories.

1. Show that $\mathscr{D}_{0}$ is an $\infty$-category.
2. Show that $f^{-1} \mathscr{D}_{0}$ is an $\infty$-subcategory of $\mathcal{C}$.
3. Show that given a 2 -simplex $\sigma: \Delta^{2} \rightarrow \mathscr{D}$ which witnesses that $h: X \rightarrow Z$ is the composition of $f: X \rightarrow Y$ with $g: Y \rightarrow Z$, such that $f, g$ both lie in $\mathscr{D}_{0}$, then $h$ and $\sigma$ also both lie in $\mathscr{D}_{0}$ as well. In particular, show that if $X$ is equivalent to an object $Y$ in $\mathscr{D}$, and $X$ lies in $\mathscr{D}_{0}$, then $Y$ also lies in $\mathscr{D}_{0}$.
4. If $\mathcal{C}$ is a 1-category, show that subcategories of $\mathcal{C}$ are in natural bijection with the $\infty$-subcategories of its nerve.

Theorem 1.4.21 ([Lurb, Tag 01CP]). Let $\mathcal{C}$ be an $\infty$-category. Then the natural map $\mathcal{C} \rightarrow \mathrm{hC}$ induces a bijection of sets between subcategories of $\mathrm{hC}$ and $\infty$-subcategories of $\mathcal{C}$.

Proof. First notice that by part 2 of Exc.1.4.20, the pullback of a subcategory $\mathcal{C}_{0}$ of hC along the natural unit map $\eta: \mathcal{C} \rightarrow N \mathrm{~hC}$ is indeed a subcategory of $\mathcal{C}$. Moreover, such a subcategory $\mathcal{C}_{0}$ of hC is also uniquely determined by its pullback to $\mathcal{C}$, as the unit map is surjective on $n$-simplices by part 5 of Exc.1.3.8. It now suffices to show that all $\infty$-subcategories of $\mathcal{C}$ are the result of such a construction. Given an $\infty$-subcategory $\mathscr{D}_{0}$ of $\mathcal{C}$, we obtain a functor $\mathrm{h} \mathscr{D}_{0} \rightarrow \mathrm{~h} \mathcal{C}$ which is clearly injective on objects and is also fully faithful by part 3 of Exc.1.4.20, so we can regard $\mathrm{h} \mathscr{D}_{0}$ as a subcategory of hC . This then induces a natural inclusion of simplicial sets $\mathscr{D}_{0}$ to $\eta^{-1}\left(\mathrm{~h} \mathscr{D}_{0}\right)$ along the unit, which we want to now show is an equality. To do this, we will show that a map $\sigma: \Delta^{n} \rightarrow \mathcal{C}$ is contained in $\mathscr{D}_{0}$ if and only if the induced map $[n] \rightarrow \mathrm{hC}$ is contained in $\mathrm{h} \mathscr{D}_{0}$. This is clear for $n=0$, and for $n=1$ we again appeal to part 3 of Exc.1.4.20. For $n \geqslant 1$, we consider all restrictions of $\sigma: \Delta^{n} \rightarrow \mathcal{C}$ to $\Delta^{1} \simeq N(\{i<i+1\})$ for all $0 \leqslant i \leqslant n-1$. Now we use the $(n=1)$-case to see that if $[n] \rightarrow \mathrm{hC}$ factors through $\mathrm{h} \mathscr{D}_{0}$ then we see that the restriction of $\sigma$ to Spine ${ }^{n}$ factors through $\mathscr{D}_{0}$. Now, we use the fact that Spine ${ }^{n} \subseteq \Delta^{n}$ is inner anodyne, see Exc.1.4.22 below, to finish the proof.

Exercise 1.4.22. Let $n \geqslant 1$ and consider the subcomplex Spine ${ }^{n}$ of $\Delta^{n}$ given buy the union of all the $N(\{i<i+1\}) \simeq \Delta^{1}$ for $0 \leqslant i \leqslant n-1$. Prove that the inclusion Spine ${ }^{n} \rightarrow \Delta^{n}$ is inner anodyne. (Hint: you might want to come back to this after Pr.1.7.9.) In particular, show that for any $\infty$-category $\mathcal{C}$, the natural map $\operatorname{Fun}\left(\Delta^{n}, \mathcal{C}\right) \rightarrow \operatorname{Fun}\left(\right.$ Spine $\left.^{n}, \mathcal{C}\right)$ is a trivial Kan fibration; recall the definition from Exc.1.4.6.
Exercise 1.4.23. Let $X$ be a simplicial set. Show that the map

$$
\operatorname{Fun}\left(\Delta^{1}, X\right) \rightarrow \operatorname{Fun}\left(\partial \Delta^{1}, X\right)
$$

induced by the inclusion $\partial \Delta^{1} \rightarrow \Delta^{1}$, is an inner fibration.

# 1.5 Mapping animæ 

In many ways, the category of sets plays a key role in classical category theory. For example, the mapping objects in a (locally small) category $\mathcal{C}$ are naturally sets. This does not seem so remarkable, but this observation leads to the Yoneda lemma and the formulation of universal

properties, just to name a few. In $\infty$-category theory, the objects which parametrise the collections of morphisms between two objects will naturally be animc.

Definition 1.5.1. Let $X, Y$ be two objects in an $\infty$-category $\mathcal{C}$. We define the mapping anima between $X$ and $Y$ as the pullback of simplicial sets

$$
\operatorname{Map}_{\mathcal{C}}(X, Y)=\operatorname{Fun}\left(\Delta^{1}, \mathcal{C}\right) \underset{\operatorname{Fun}\left(\partial \Delta^{1}, \mathcal{C}\right)}{\times}\{(X, Y)\}
$$

induced by the inclusion $\partial \Delta^{1} \rightarrow \Delta^{1}$ and the identification $\operatorname{Fun}\left(\partial \Delta^{1}, \mathcal{C}\right) \simeq \mathcal{C} \times \mathcal{C}$. One can write this with more symmetry as

$$
\operatorname{Map}_{\mathcal{C}}(X, Y) \cong\{X\}_{\underset{\mathcal{C}, s}{\times}} \operatorname{Fun}\left(\Delta^{1}, \mathcal{C}\right) \underset{t, \mathcal{C}}{\times}\{Y\}
$$

where $s$ and $t$ are the source and target maps, given by the inclusions $\Delta^{\{0\}} \rightarrow \Delta^{1}$ and $\Delta^{\{1\}} \rightarrow$ $\Delta^{1}$, respectively.

A priori the above definition only yields a simplicial set, rather than an anima, however, the following will justify our use of the word anima.

Proposition 1.5.2. If $\mathcal{C}$ is an $\infty$-category and $X, Y$ are two objects in $\mathcal{C}$, then $\operatorname{Map}_{\mathcal{C}}(X, Y)$ is a Kan complex.

This will only be clear using the theory from $\S 1.4$.
Sketch of proof. By definition, we see that $\operatorname{Map}_{\mathcal{C}}(X, Y)$ sits in a pullback of simplicial sets
![img-26.jpeg](img-26.jpeg)

The right-hand vertical map is an inner fibration, see Exc.1.4.23, hence the left-hand vertical map is also an inner fibration, so $\operatorname{Map}_{\mathcal{C}}(X, Y)$ is an $\infty$-category. To see this $\infty$-category is a Kan complex, ie, an $\infty$-groupoid, we use Pr.1.3.5 which reduces us to show that all morphisms in $\operatorname{Map}_{\mathcal{C}}(X, Y)$ are isomorphisms. Another way to phrase this is that the left-vertical functor above is conservative, meaning that the image of a morphism is an isomorphism if and only if the morphism itself is an isomorphism. As conservative functors are closed under pullback, see Exc.1.5.3 below, we are reduced to showing that the right-hand vertical map above is conservative. In other words, we want to show that a morphism in $\operatorname{Fun}\left(\Delta^{1}, \mathcal{C}\right)$, so a $\Delta^{1} \times \Delta^{1}$ diagram in $\mathcal{C}$ of the form
![img-27.jpeg](img-27.jpeg)
is an equivalence between $f$ and $g$ if and only if each $h_{i}$ are equivalences as morphisms in $\mathcal{C}$. The "only if" direction is obvious, and for the "if" direction, let us note that this is clearly

true classically, and that for $\infty$-categories this involves a lot more combinatorial work, similar to the proof of Pr.1.4.14 but even more complicated; see [Lurb, Tag 01DK] for (further links and references to) a full proof.

Exercise 1.5.3. Using the language found in the proof of Pr.1.5.2, show that conservative functors of $\infty$-categories are closed under pullback.

These mapping animæ are enrichments of the mapping sets in classical category theory.
Exercise 1.5.4. Show that if $\mathcal{C}$ is the nerve of a 1-category and $X, Y$ are objects of $\mathcal{C}$, then $\operatorname{Map}_{\mathcal{C}}(X, Y)$ is discrete and is in bijection with the set of maps $\mathcal{C}(X, Y)$.
Exercise 1.5.5. Show that if $\mathcal{C}$ is a Kan complex and $x, y \in \mathcal{C}$ are two points, then $\operatorname{Map}_{\mathcal{C}}(x, y)$ is the simplicial set of paths between these points. If you want a bit more of a technical challenge, then show that if $\mathcal{C}$ is Sing $X$ for a topological space $X$, then $\operatorname{Map}_{\mathcal{C}}(x, y)$ is naturally equivalent to the singular simplicial set of the topological space of paths from $x$ to $y$ into $X$ with the compact-open topology.
Exercise 1.5.6. Show that the simplicial mapping set between two $\infty$-categories, viewed as objects in sSet, is again an $\infty$-category.
Exercise 1.5.7. Let $\mathcal{C}$ be an $\infty$-category, $K$ a simplicial set, $X, Y$ objects of $\mathcal{C}$, and $\underline{X}, \underline{Y}: K \rightarrow$ $\mathcal{C}$ the associated constant functors. Show that there is a canonical isomorphism of simplicial sets

$$
\operatorname{Map}_{\operatorname{Fun}(K, \mathcal{C})}(\underline{X}, \underline{Y}) \cong \operatorname{Fun}\left(K, \operatorname{Map}_{\mathcal{C}}(X, Y)\right)
$$

Exercise 1.5.8. Let $X, Y$ be two animæ. Show that the anima $\operatorname{Map}_{\mathcal{A}_{\mathrm{R}}}(X, Y)$ can be represented by the mapping simplicial set $Y^{X}$.

The above exercise generalises to general Kan-enriched simplicial categories; see [Lurb, Tag 01LA].

We want to use these mapping animæ as one uses hom-sets in classical category theory. For example, one can discuss the composition rule in an $\infty$-category using these objects.
Exercise 1.5.9. Given objects $X, Y, Z$ in $\mathcal{C}$, construct a "composition map"

$$
\operatorname{Map}_{\mathcal{C}}(Y, Z) \times \operatorname{Map}_{\mathcal{C}}(X, Y) \rightarrow \operatorname{Map}_{\mathcal{C}}(X, Z)
$$

between mapping animæ in the category sSet.
As discussed previously, this exercise gives us a particular choice of composition between two maps in an $\infty$-category. We have actually already seen that any choice is equivalent to any other. Indeed, by Pr.1.4.15, we see that if $\mathcal{C}$ is an $\infty$-category, then the natural map of $\infty$-categories

$$
\operatorname{Fun}\left(\Delta^{2}, \mathcal{C}\right) \rightarrow \operatorname{Fun}\left(\Lambda_{1}^{2}, \mathcal{C}\right)
$$

is a trivial Kan fibration of simplicial sets, defined in Exc.1.4.6, and in particular, is an equivalence of $\infty$-categories. There is some language that goes with this: we say that composition in an $\infty$-category $\mathcal{C}$ is essentially unique or unique up to contractible choice. This is decent homotopy-theoretic analogue to uniqueness.

Exercise 1.5.10. Show that if $F: \mathcal{C} \rightarrow \mathscr{D}$ is a functor of $\infty$-categories, then there is an induced map of animæ

$$
\operatorname{Map}_{\mathcal{C}}(X, Y) \rightarrow \operatorname{Map}_{\mathscr{D}}(F X, F Y)
$$

for every $X, Y$ in $\mathcal{C}$.
We can now define fully faithfulness of $\infty$-categories using mapping animæ.
Definition 1.5.11. A functor of $\infty$-categories $F: \mathcal{C} \rightarrow \mathscr{D}$ is fully faithful if the induced map

$$
\operatorname{Map}_{\mathcal{C}}(X, Y) \rightarrow \operatorname{Map}_{\mathscr{D}}(F X, F Y)
$$

is an equivalence of anima for all objects $X, Y$ inside $\mathcal{C}$.
Exercise 1.5.12. Show that the inclusion of Kan complexes into $\infty$-categories, viewed as a subcategory of sSet, defines a fully faithful functor of $\infty$-categories $\mathcal{A} \mathrm{n} \rightarrow \mathrm{Cat}_{\infty}$. Construct a functor Cat $_{\infty} \rightarrow \mathcal{A}$ n which "takes maximal sub-Kan complexes", and which seems like a right adjoint to the previous fully faithful functor on mapping animæ (to be defined shortly).

Theorem 1.5.13. A functor of $\infty$-categories $F: \mathcal{C} \rightarrow \mathscr{D}$ is an equivalence if and only if it is fully faithful and essentially surjective, meaning the induced map on homotopy categories is essentially surjective.

It would not take us too far off course to prove this theorem, but we also won't use this proposition very often; for a proof of Th.1.5.13, see[Lurb, Tag 01JX].

Please use Th.1.5.13 in the following exercise though!
Exercise 1.5.14. Let $F: \mathcal{C} \rightarrow \mathscr{D}$ and $G: \mathscr{D} \rightarrow \mathcal{C}$ be two functors of $\infty$-categories. Suppose that $F$ is left adjoint to $G$, meaning we are given a natural transformation of presheaves

$$
\operatorname{Map}_{\mathscr{D}}(F(-),-) \simeq \operatorname{Map}_{\mathcal{C}}(-, G(-)): \mathcal{C}^{\mathrm{op}} \times \mathscr{D} \rightarrow \mathcal{A} \mathrm{n}
$$

which is an equivalence. Suppose that $G$ is conservative, meaning that a morphism $f$ in $\mathcal{C}$ is an equivalence if and only if $G(f)$ is an equivalence, and that $F$ is fully faithful. Show that $F$ and $G$ are equivalences and in fact mutual inverses.

There are also some fun alternative expressions for various mapping animae.
Exercise 1.5.15. Let $\mathcal{C}$ be an $\infty$-category, $X$ an object, and write $\mathcal{C}_{X /}$ for the slice category $\mathcal{C}_{p /}$ where $p: \Delta^{0} \rightarrow \mathcal{C}$ is defined by $X$. Show that for any two morphisms $f: X \rightarrow Y$ and $g: X \rightarrow Z$ in $\mathcal{C}$, viewed now as objects in both $\mathcal{C}_{X /}$ and Fun $\left(\Delta^{1}, \mathcal{C}\right)$, the evident commutative diagrams of animæ
![img-28.jpeg](img-28.jpeg)
are homotopy pullbacks of Kan complexes. In particular, find an example which shows that $\pi_{0} \operatorname{Map}_{\mathcal{C}_{X /}}(f, g)$ does not have to be in bijection with $(\mathrm{hC})_{X /}(f, g)$. (Hint: the key phrase is "data vs. properties".)

# 1.6 Initial and terminal objects 

Mapping animæ are useful, especially as they can be used to write down universal properties just as mapping sets are used in classical category theory.

For example, we say that an object $X$ in a 1-category $\mathcal{C}$ is initial if for all objects $Y$ in $\mathcal{C}$ there exists a unique map $X \rightarrow Y$. In other words, the natural map of sets $\mathcal{C}(X, Y) \rightarrow *$, where * is the one-point set, is a isomorphism in Set. This leads us immediately to the definition of an initial object in an $\infty$-category, once we have a way of talking about an anima $X$ being "equivalent to a point in $\mathcal{A} \mathrm{n}$ ".

Definition 1.6.1. We say that an anima $X$ is contractible if the natural map $X \rightarrow *$ is an equivalence in $\mathcal{A} \mathrm{n}$.

Definition 1.6.2. Recall the geometric realisation functor $|-|:$ sSet $\rightarrow$ Top, discussed in Topology I and II, which for this course we define as the colimit

$$
|X|=\operatorname{colim}_{\Delta^{n} \rightarrow X}\left|\Delta^{n}\right|
$$

taken over all of the morphisms from $\Delta^{n}$ into $X$ for various $n \geqslant 0$.
Exercise 1.6.3. Prove that $|-|$ is left adjoint to Sing. Given a simplicial set $X$ and a 0 -simplex $0 \in X_{0}$, we define $\pi_{n}\left(X, x_{0}\right)$ as $\pi_{n}\left(|X|,\left|x_{0}\right|\right)$. We say that $X$ is contractible ${ }^{3}$ if $|X|$ is so. Show that this definition of contractible matches that of Df.1.6.1.

Definition 1.6.4. Let $\mathcal{C}$ be an $\infty$-category. We say that an object $X$ in $\mathcal{C}$ is an initial object if the mapping anima $\operatorname{Map}_{\mathcal{C}}(X, Y)$ is contractible for all other objects $Y$ in $\mathcal{C}$.

The following exercise concern the uniqueness of initial objects.
Exercise 1.6.5. Show that if $X$ and $X^{\prime}$ are both initial objects of an $\infty$-category $\mathcal{C}$, then there they are equivalent. In particular, show that the $\infty$-subcategory of $\mathcal{C}$ spanned by all initial objects is itself an anima. Moreover, show that this anima of initial objects in $\mathcal{C}$ is itself contractible.

To shorten our discussions, we will often say phrases like "...and by duality...". For this to make any sense, we need a theory of opposite $\infty$-categories.

Definition 1.6.6. Let $\mathcal{C}$ be a simplicial set. The opposite of $\mathcal{C}$ is defined by reversing the order of the face and degeneracy maps, so $d_{i}^{\text {op }}=d_{n-i}$ in degree $n$, and similarly for the degeneracies. We write the opposite of $\mathcal{C}$ as $\mathcal{C}^{\text {op }}$. Clearly $\left(\mathcal{C}^{\text {op }}\right)^{\text {op }}=\mathcal{C}$.

By construction, notice that $\operatorname{Map}_{\mathcal{C}^{\text {op }}}(X, Y)$ is naturally isomorphic to $\operatorname{Map}_{\mathcal{C}}(Y, X)$, so this behaves as expected.
Exercise 1.6.7. If $\mathcal{C}$ is a Kan complex, show that $\mathcal{C}^{\text {op }}$ is naturally equivalent to $\mathcal{C}$. Show that, $\left(\Delta^{n}\right)^{\text {op }} \cong \Delta^{n}$ and that $\left(\Lambda_{i}^{n}\right)^{\text {op }} \cong \Lambda_{n-i}^{n}$.

[^0]
[^0]:    ${ }^{3}$ There is a "simplicial homotopy theory", which are purposely avoiding in this course, where we can discuss homotopy-theoretic concepts, such as contractibility, of simplicial sets directly.

Definition 1.6.8. Let $C$ be an $\infty$-category. We say that an object $X$ in $C$ is a terminal object if it is initial in $C^{\text {op }}$. Concretely, this means that $\operatorname{Map}_{C}(Y, X)$ is contractible for every $Y$ in $C$.

First, let us compare this definition with the classical definition of initial and terminal objects.

Exercise 1.6.9. Show that if $C$ is the nerve of a 1-category, then $X$ is an initial object of $C$ if and only if it is an initial object of $C$ in a 1-categorical sense.

The following two exercises outline a question that was asked in class: "is an initial object in $C$ the same as an initial object in hC". The answer is no!
Exercise 1.6.10. Show that if $C$ is an $\infty$-groupoid such that as an $\infty$-category it has an initial (or terminal) object, then $C$ is contractible.
Exercise 1.6.11. Show that if $X$ is an initial object of an $\infty$-category $C$, then it is also an initial object of the 1-category hC. Moreover, show that the converse is false by considering the case where $C=X$ is a simply connected anima.

End of lecture 4 and week 2

# 1.7 Slice categories 

In traditional category theory, we can define the colimit of a diagram in a category, as the initial object in a slice category. We would like to repeat this process for $\infty$-categories.

Onto another application now, concerning joins of simplicial sets.
Definition 1.7.1. Given two simplicial sets $X$ and $Y$, we define their join $X \star Y$ as the simplicial set with $n$-simplices

$$
(X \star Y)_{n}=X_{n} \sqcup Y_{n} \sqcup \coprod_{i+j=n-1} X_{i} \times Y_{j}
$$

To define the degeneracy and face maps, let us make a more functorial definition: for each nonempty finite linearly ordered set $I$, we set $X \star Y(I)=\bigcup_{I_{1} \sqcup I_{2}} X\left(I_{1}\right) \times Y\left(I_{2}\right)$, where the coproduct is taken over all disjoint decompositions of $I=I_{1} \sqcup I_{2}$, where $x_{1}<x_{2}$ for all $x_{1} \in I_{1}$ and $x_{2} \in I_{2}$.

In other words, the

- 0 -simplices of $X \star Y$ are the 0 -simplices of $X$ and $Y$, the
- 1-simplices are the 1 -simplices of $X$ and $Y$, plus a 1 -simplex labelled $(x, y)$ for each pair of 0 -simplices $(x, y) \in X_{0} \times Y_{0}$, the
- 2-simplices are the 2 -simplices of $X$ and $Y$, together with pairs $(x, f) \in X_{0} \times Y_{1}$ and $(g, y) \in X_{1} \times Y_{0}$, and so on.

The degeneracy and face maps are rigged up so that the faces of $(x, y)$ are $x$ and $y$, respectively.

There is a relation to a classical join construction for 1-categories.
Exercise 1.7.2. Calculate $N C \star N \mathscr{D}$ for 1-categories $C$ and $\mathscr{D}$.
Exercise 1.7.3. Show there is an equivalence of simplicial sets $\Delta^{i} \star \Delta^{j} \cong \Delta^{i+j+1}$.
Proposition 1.7.4. If $C$ and $\mathscr{D}$ are two $\infty$-categories, then $C \star \mathscr{D}$ is also an $\infty$-category.
Proof. Suppose we are given a map $\Lambda_{i}^{n} \rightarrow C \star \mathscr{D}$ for some $0<i<n$ which we would like to extend. If the image of this map lies in $C$ or $\mathscr{D}$, then we are done as these simplicial sets are $\infty$-categories. Otherwise, $p$ carries the vertices $\{0, \ldots, j\}$ to $C$ and $\{j+1, \ldots, n\}$ to $\mathscr{D}$, for some $0 \leqslant j<n$. It is an exercise below (Exc.1.7.5) to see that these restrictions of our given map to these simplices are inner horns or simplexes. By individually lifting these restrictions to $\Delta^{j} \rightarrow C$ and $\Delta^{n-(j+1)} \rightarrow \mathscr{D}$ and then applying $\star$, we obtain our desired lift $\Delta^{n} \rightarrow C \star \mathscr{D}$.

Exercise 1.7.5. Let $K, X, Y$ be simplicial sets. Show that a $K \rightarrow X \star Y$ is precisely the data of a triple $\left(\pi: K \rightarrow \Delta^{1}, f^{0}: K^{0} \rightarrow X, f^{1}: K^{1} \rightarrow Y\right)$, where $K^{i}$ is the inverse image of $\{i\} \subseteq \Delta^{1}$ under $\pi$. (Hint: use the fact that each simplicial set comes with a canonical map $X \rightarrow \Delta^{0}$, hence each join comes with a canonical map $X \star Y \rightarrow \Delta^{0} \times \Delta^{0} \simeq \Delta^{1}$.)
Exercise 1.7.6. Given two simplicial sets $X, Y$, construct an isomorphism between $(X \star Y)^{\text {op }}$ and $Y^{\text {op }} \star X^{\text {op }}$.
Exercise 1.7.7. If $X$ and $Y$ are Kan complexes, is $X \star Y$ necessarily a Kan complex?
Exercise 1.7.8. Show that the objects of $C \star \mathscr{D}$ are either an object in $C$ or an object in $\mathscr{D}$, and that one has the following identification of their mapping animæ:

$$
\operatorname{Map}_{C \star \mathscr{D}}(X, Y)= \begin{cases}\operatorname{Map}_{C}(X, Y) & X, Y \in C \\ \operatorname{Map}_{\mathscr{D}}(X, Y) & X, Y \in \mathscr{D} \\ \Delta^{0}=* & X \in C, Y \in \mathscr{D} \\ \varnothing & X \in \mathscr{D}, Y \in C\end{cases}
$$

The following is a useful "base change" property of the join construction with respect to various anodyne maps.

Proposition 1.7.9. Let $i: A_{0} \subseteq A$ and $j: B_{0} \subseteq B$ be simplicial sets with chosen simplicial subsets and write $k$ for the inclusion

$$
k:\left(A_{0} \star B\right) \underset{A_{0} \star B_{0}}{\vee}\left(A \star B_{0}\right) \rightarrow A \star B
$$

If $i$ is left anodyne, then $k$ is left anodyne. If $j$ is left anodyne, then $k$ is inner anodyne.
This proposition is strangely not symmetric, but this is due to the fact that the join construction is not symmetric.

Proof. Let us prove the first statement; the second follows similarly. Let $S$ be the class of all morphisms of simplicial sets $i: A_{0}^{\prime} \rightarrow A^{\prime}$ such that the induced map $k^{\prime}$ is left anodyne against all inclusions $j$. This class of morphisms is weakly saturated, meaning that this class is closed under base change (pushouts), transfinite composition, and the formation of retracts. To prove that this class contains all left anodyne maps, our desired statement, it suffices to show that it contains each horn inclusion $\Lambda_{i}^{n} \rightarrow \Delta^{n}$ for $0 \leqslant i<n$. Let $T$ now be the class of all inclusions $j$ such that $k$ is left anodyne against one of these fixed horn inclusions. This class $T$ is also weakly saturated, so to show that it contains all inclusions, it suffices to prove the inclusions $\partial \Delta^{m} \rightarrow \Delta^{m}$ are contained in $T$. In this particular case though, where $i$ is the left horn inclusion $\Lambda_{i}^{n} \rightarrow \Delta^{n}$ and $j$ is the boundary inclusion $\partial \Delta^{m} \rightarrow \Delta^{m}$, we see that the inclusion $k$ is equivalent the inclusion $\Lambda_{i}^{m+n+1} \rightarrow \Delta^{m+n+1}$, see the following exercise, which is left anodyne as $0 \leqslant i<n \leqslant n+m+1$.

Exercise 1.7.10. In the situation of Pr.1.7.9, show that if $i$ is a left horn inclusion $\Lambda_{i}^{n} \rightarrow \Delta^{n}$ and $j$ is the boundary inclusion $\partial \Delta^{n} \rightarrow \Delta^{n}$, then $k$ is the claimed left horn inclusion $\Lambda_{i}^{m+n+1} \rightarrow$ $\Delta^{m+n+1}$ claimed in the proof above.

Be warned: the join construction $\star$ is not commutative. For example:
Definition 1.7.11. Let $\mathcal{C}$ be an $\infty$-category, $K$ be a simplicial set, and $p: K \rightarrow \mathcal{C}$ be a map of simplicial sets. We define a cone of $p$ as an extension of $p$ to a map of simplicial sets $\tilde{p}: \Delta^{0} \star K \rightarrow \mathcal{C}$, meaning that $\left.\tilde{p}\right|_{K}=p$. A cocone is an extension to $K \star \Delta^{0}$.

The following picture gives an example of a cone and and a cocone of a diagram $p: \Delta^{1} \rightarrow \mathcal{C}$ defined by the arrow $X_{01}: X_{0} \rightarrow X_{1}$, respectively:
![img-29.jpeg](img-29.jpeg)

Definition 1.7.12. Let $\mathcal{C}$ be an $\infty$-category, $K$ be a simplicial set, and $p: K \rightarrow \mathcal{C}$ be a map of simplicial sets. We define a simplicial set $\mathcal{C}_{/ p}$ by the universal property

$$
\operatorname{sSet}\left(X, \mathcal{C}_{/ p}\right)=\operatorname{sSet}_{p}(X \star K, \mathcal{C})
$$

where the subscript $p$ refers to all maps of simplicial sets such that their restriction to $K$ is precisely $p$. We call $\mathcal{C}_{/ p}$ the overcategory of $p$. The undercategory is defined similarly:

$$
\operatorname{sSet}\left(X, \mathcal{C}_{p /}\right)=\operatorname{sSet}_{p}(K \star X, \mathcal{C})
$$

Proposition 1.7.13. In the above situation, $\mathcal{C}_{/ p}$ and $\mathcal{C}_{p /}$ are also $\infty$-categories. Moreover, there are forgetful functors of $\infty$-categories $\mathcal{C}_{/ p} \rightarrow \mathcal{C}$ and $\mathcal{C}_{p /} \rightarrow \mathcal{C}$ which only remember the cone/cocone point.

Proof. The projection map $C_{p /} \rightarrow C$ is constructed by pulling back against the unique map $\varnothing \rightarrow K$. We then have the following general claim regarding such maps.
Claim 1.7.14. The projection map $C_{p /} \rightarrow C$ is a left fibration.
Using this claim, we see that $C_{p /}$ is an $\infty$-category as $C$ is. For $C_{/ p}$ we take opposite categories.

To prove the claim, we set up a lifting problem
![img-30.jpeg](img-30.jpeg)
with $0 \leqslant i<n$, which is equivalent to the lifting problem
![img-31.jpeg](img-31.jpeg)
by adjunction and the definition of slice categories. Now we refer to the second statement of Pr.1.7.9, which states that the left-vertical map is inner anodyne, and by Pr.1.4.12 and the fact that $C$ is an $\infty$-category we see that a solution exists.

The following justifies why this definition is a generalisation of the classical definition, at least in simple cases.
Exercise 1.7.15. Let $C$ be a 1-category, $X$ be an object of $C$, and consider the 1-categorical slice construction $C_{X /}$, where objects are morphisms $f: X \rightarrow Y$ in $C$ and morphisms are $h: Y_{1} \rightarrow Y_{2}$ in $C$ such that $f_{2}=h \circ f_{1}$. Show that the simplicial sets $\left(N C_{X /}\right)$ and $(N C)_{X /}$ are isomorphic.

We will see an alternative expression for the mapping spaces of slice categories in Exc.1.5.15.
Definition 1.7.16. Let $*$ be a terminal object of $\mathcal{A}$ n, so any contractible anima. We write $\mathcal{A} \mathrm{n}_{*}$ for the $\infty$-category of pointed anim $\alpha$, defined as the slice $\mathcal{A} \mathrm{n}_{* /}$.
Exercise 1.7.17. Show that $\mathrm{Kan}_{*}$ is a model for $\mathcal{A} \mathrm{n}_{*}$. This reconciles Df.1.3.29 with Df.1.7.16.
Exercise 1.7.18. Let $C$ be an $\infty$-category with a terminal object $*$. Prove that the overcategory $C_{* /}$ is pointed, meaning it has both an initial object $\varnothing$ and a terminal object $*$, and the map $\varnothing \rightarrow *$ is an equivalence.
Exercise 1.7.19. Show that if $F: C \rightarrow \mathscr{D}$ is a functor of $\infty$-categories, then for any simplicial set $K$ and any map $p: K \rightarrow C$, there is an induced map $C_{/ p} \rightarrow \mathscr{D}_{/ F p}$ such that the diagram of $\infty$-categories
![img-32.jpeg](img-32.jpeg)

commutes.
Exercise 1.7.20. Show that this is well-defined up to equivalence of $\infty$-categories, meaning that if $F: \mathcal{C} \rightarrow \mathscr{D}$ is a functor of $\infty$-categories inducing an isomorphism inside $\mathrm{h} \mathrm{Cat}_{\infty}$, then the associated map $\mathcal{C}_{/ p} \rightarrow \mathscr{D}_{/ F p}$ of the previous exercise is an equivalence.

# 1.8 Limits and colimits in $\infty$-categories 

Classically, a colimit is an initial object of the undercategory $\mathcal{C}_{p /}$. Now that we have these concepts for $\infty$-categories, we can define limits and colimits in this world.

Definition 1.8.1. Let $\mathcal{C}$ be an $\infty$-category, $K$ a simplicial set, and $p: K \rightarrow \mathcal{C}$ a map of simplicial sets. A colimit for $p$ is an initial object of $\mathcal{C}_{p /}$, and a limit is a terminal object of $\mathcal{C}_{/ p}$.

End of lecture 5
In other words, a colimit is a diagram $\widetilde{p}: K \star \Delta^{0} \rightarrow \mathcal{C}$ which extends $p$, with a certain universal property. In general, we will say that a cocone witness $\widetilde{p}(\infty)$ as a colimit of $p$, where $\infty$ is the cocone point, if this cocone is initial in $\mathcal{C}_{p /}$. We will also write colim ${ }_{K} p=\widetilde{p}(\infty)$, and similarly for limits. There is some ambiguity in this definition, and we have been saying phrases like "a colimit" and "a limit", using the indefinite article. Just like many other concepts in higher category theory though, such concepts are only defined up to contractible choice.
Exercise 1.8.2. Formulate what the simplicial set of limits of a certain diagram $p: K \rightarrow \mathcal{C}$ must be, and show it to be contractible. Same for colimits if you want more practice.

Let us now consider some examples of limits - the discussion of colimits is analogous and dual.

Before that, we would like to recall some notions from Topology I and II, now in the realm of simplicial sets.

Definition 1.8.3. Given a span of simplicial sets $X \rightarrow Z \leftarrow Y$, we will assume they are also Kan complexes, the homotopy pullback of this span is written as $X \times{ }_{Z}^{h} Y$ and is defined by the pullback of simplicial sets
![img-33.jpeg](img-33.jpeg)
where the path simplicial set $P f$ is defined using the right-hand pullback of simplicial sets above. We leave it as an exercise to the reader that all of the above simplicial sets are in fact Kan complexes.

In particular, notice that the vertices of the homotopy pullback are triples of $(x, y, \gamma)$ where $x \in X_{0}, y \in Y_{0}$, and $\gamma: \Delta^{1} \rightarrow Z$ is a path with $\gamma(0)=f(x)$ and $\gamma(1)=g(y)$.

The map $s_{0}^{*}: P f \rightarrow Z$, given by evaluating a path $\gamma: \Delta^{1} \rightarrow X$ at 1 , is a Kan fibration; the proof is similar to statements proven in Topology II (of [Hat02, Pr4.64]) but in sSet. In particular, this means that $Y$ is a point, then $X \times{ }_{Z}^{h} Y$ is the homotopy fibre defined in Topology II. We have fibrantly replaced the right-hand leg of the pullback diagram to obtain a homotopy pullback.

Before we start our first example of a limit in an $\infty$-category, we need to have a better understanding of the simplices in the slice categories in question.
Example 1.8.4 (Simplices of slices over $\partial \Delta^{1}$ ). Let $p: \partial \Delta^{1} \rightarrow C$ be a functor into an $\infty$-category $C$. By definition, we know that the $n$-simplices of $C_{/ p}$ are given by

$$
\operatorname{sSet}\left(\Delta^{n}, C_{/ p}\right)=\operatorname{sSet}_{p}\left(\Delta^{n} \star \partial \Delta^{1}, C\right) \subseteq \operatorname{sSet}\left(\Delta^{n} \star \partial \Delta^{1}, C\right)
$$

Let us identify $\Delta^{n} \star \partial \Delta^{1}$ with the union of two $\Delta^{n+1}$ 's along a common $\Delta^{n}$ defined to be opposite $\Delta^{\{n+1\}}$, and write $\infty_{0}$ and $\infty_{1}$ for these two endpoints. We then see that the $n$ simplices of $C_{/ p}$ are pairs of $(n+1)$-simplices of $C$ such that the two endpoints $\infty_{0}$ and $\infty_{1}$ are $p(0)$ and $p(1)$, respectively, and such that these $(n+1)$-simplicies agree along the common $n$-simplex opposite these end points. For $n=0$, this means a cone with the shape $\Lambda_{0}^{2}$ of a span $p(0) \leftarrow T \rightarrow p(1)$. For $n=1$, this means a pair of objects $X, Y$ with maps $f_{i}: X \rightarrow p(i)$, $g_{i}: Y \rightarrow p(i)$, and $h: X \rightarrow Y$, and homotopies $H_{i}: f_{i} \simeq g_{i} \circ h$ :
![img-34.jpeg](img-34.jpeg)

Exercise 1.8.5. Generalise the previous example and replace $\partial \Delta^{1}$ with an arbitrary coproduct of $\Delta^{0}$ 's.

Okay, finally, onto our first explicit example of a limit in an $\infty$-category.
Example 1.8.6 (Products of animæ). Let $X_{0}, X_{1}$ be a pair of animæ. Let us choose a representative for each anima $X_{i}$ by a Kan complex also denoted by $X_{i}$. We claim that the limit of the diagram $p: I \rightarrow \mathcal{A}$ n defined by this collection of animæ is represented by the product $X=X_{0} \times X_{1}$ taken in simplicial sets. To see this, let us first note that $X$ is a Kan complex, which follows from the universal property of a product in sSet; see Exc.1.3.2. To see that $X$ represents the limit of $p$, ie, the cone $\left(X, p_{i}\right)$ is terminal, where $p_{i}: X \rightarrow X_{i}$ are the canonical projections, let $\left(T, q_{i}\right)$ be another cone of animæ, so a Kan complex $T$ together with maps $q_{i}: T \rightarrow X_{i}$. We want to now show that $\operatorname{Map}_{\mathcal{A}_{\mathcal{N}_{p}}}(T, X)$ is contractible, so we would like to compare this mapping anima with some more tractible ones. In general, we can use Pr.1.7.13

to see that there is a forgetful functor $\mathcal{C}_{/ p} \rightarrow \mathcal{C}$ given by evaluation of our cones on their cone point. By Exc.1.5.10, this induces a map of mapping animæ

$$
\operatorname{Map}_{\mathcal{C}_{/ p}}\left(T, \prod X_{i}\right) \rightarrow \operatorname{Map}_{\mathcal{C}}\left(T, \prod X_{i}\right)
$$

In fact, this map fits into a commutative diagram of animæ
![img-35.jpeg](img-35.jpeg)
where $\mathcal{C}=\mathcal{A} \mathrm{n}$-we will come back to the case of general $\mathcal{C}$ later. We claim that this diagram is a pullback of animæ, meaning that we can identify the top-left Kan complex with the homotopy pullback of Kan complexes defined in Df.1.8.3. We will only discuss this for the 0 -simplices for simplicity of notation - try to do the analysis for some of the higher simplices at home! We want to then show that the 0 -simplices of the mapping anima

$$
\operatorname{Map}_{\mathcal{C}_{/ p}}\left(\left(T, q_{i}\right),\left(X, p_{i}\right)\right)
$$

where $\mathcal{C}=\mathcal{A} \mathrm{n}$, can be naturally (in $T$ ) identified with triples $\left(f, H_{0}, H_{1}\right)$ of a map of animæ $f: T \rightarrow X$ and homotopies $H_{i}: q_{i} \simeq p_{i} \circ f$. We will do this calculation using Eg.1.8.4 and the definition of mapping animæ. Indeed, this works for a general $\infty$-category $\mathcal{C}$, and we see that

$$
\operatorname{Map}_{\mathcal{C}_{/ p}}\left(\left(T, q_{i}\right),\left(X, p_{i}\right)\right)=\left(\mathcal{C}_{/ p}\right)^{\Delta^{1}} \underset{\left(\mathcal{C}_{/ p}\right)^{2}}{\times}\left\{\left\{\left(T, q_{i}\right),\left(X, p_{i}\right)\right\}\right\}
$$

is the collection of pairs of 2 -simplices in $\mathcal{C}$ whose endpoints are $X_{0}$ and $X_{1}$, respectively, who agree on the 1 -simplex opposite their end points, and who agree with the spans $\left(T, p_{0}, p_{1}\right)$ and $\left(X, q_{0}, q_{1}\right)$, respectively away from their common edge:
![img-36.jpeg](img-36.jpeg)

This proves the claim that (1.8.7) is a homotopy pullback. It follows from the universal property of $X=X_{0} \times X_{1}$ as a product of simplicial sets that the right-hand vertical map of (1.8.7) is an isomorphism of simplicial sets, hence a weak homotopy equivalence. Just like in Topology I and II, the homotopy pullback of a weak homotopy equivalence is a weak homotopy equivalence, so we see the left-hand vertical map of (1.8.7) is weak homotopy equivalence of Kan complexes. In other words, the desired mapping space is contractible, and $X=X_{0} \times X_{1}$ represents the $\infty$-categorical product of $X_{0}$ and $X_{1}$.

Warning 1.8.9. There is one final thing left to check, which we mentioned in the lectures but did not suggest how to prove it, although it is quite simple in this case-we need to show that our choice of representative Kan complexes $X_{0}$ and $X_{1}$ for the animæ $X_{0}$ and $X_{1}$ is independent of the answer. In other words, we should show that if we replace either of these Kan complexes with homotopy equivalent Kan complexes, then we still obtain the universal property above. This is easy though, as if $X_{0} \simeq X_{0}^{\prime}$ then clearly $X_{0} \times X_{1} \simeq X_{0}^{\prime} \times X_{1}$-this argument becomes more subtle for more difficult diagram shapes, but we also won't mention this point again.
Warning 1.8.10. The case for products in $\mathcal{A} \mathrm{n}$ is an outlier, in the sense that it is almost never the case that a limit in an $\infty$-category is given by a limit in the underlying Kan-enriched simplicial category the underlying simplicial set or something-this is a very unique case for products.
Exercise 1.8.11. Repeat Eg.1.8.6, with all of the details, for products indexed on an arbitrary discrete set.

There is actually quite a lot about the previous example of a binary product which we can generalise to an arbitrary $\infty$-category.
Example 1.8.12 (Products in $C$ ). Consider a discrete simplicial set $I$. Then a map $p: I \rightarrow C$ to an $\infty$-category $C$ is precisely a choice of objects $X_{i}$ in $C$. The limit of $p$ is called the product of the $X_{i}$ 's, when it exists, and will be written as $\prod X_{i}$, and $X_{0} \times X_{1}$ if $I=\{0,1\}$ as in Eg.1.8.6. By definition, $\prod X_{i}$ is a cone $\Delta^{0} \star I \rightarrow C$ extending $p$, so it comes with maps $p_{i}: \prod X_{i} \rightarrow X_{i}$. Also by definition the cone $\prod X_{i}$ equipped with these $p_{i}$ 's is the terminal cone, meaning that for all other cones, so tuples $\left(T, q_{i}\right)$ where $q_{i}: T \rightarrow X_{i}$ is a choice of map in $C$ for each $i \in I$, the mapping anima

$$
\operatorname{Map}_{C_{/ p}}\left(\left(T, q_{i}\right),\left(\prod X_{i}, p_{i}\right)\right)
$$

is contractible. We want to rewrite the universal property of $\prod X_{i}$, meaning we want to calculate $\operatorname{Map}_{C}\left(T, \prod X_{i}\right)$ for an arbitrary object $T$ in $C$. To do this, we consider (1.8.7) again. The discussion surrounding this diagram of animæ shows that this square is a homotopy pullback of simplicial sets, and in particular, as the simplicial set in the lower-left-hand corner is a singelton, this diagram is a homotopy fibre sequence of Kan complexes. Just as in Topology II, this homotopy fibre sequence induces a long exact sequence on homotopy groups for any choice of basepoint. As the upper-left-hand anima is contractible as $\prod X_{i}$ is a terminal cone, then we see the right-hand vertical map induces an equivalence on all homotopy groups for all basepoints. By Whitehead's theorem for Kan complexes, we see this map of animæ is a homotopy equivalence, which gives us our desired universal property for $\prod X_{i}$ :

$$
\operatorname{Map}_{C}\left(T, \prod X_{i}\right) \xrightarrow{\simeq} \prod \operatorname{Map}_{C}\left(T, X_{i}\right)
$$

We summarise this universal property by saying that maps into a product are a choice of maps into each of the factors. In particular, if $C=\mathrm{Cat}_{\infty}$, then the objects of a product $\prod_{i} C_{i}$ of $\infty$-categories are precisely a collection of objects $X_{i} \in C_{i}$ for each $i$.
Exercise 1.8.13. Show that if $C_{i}$ is a collection of $\infty$-categories indexed on a discrete set $I$, then there is a natural equivalence of mapping animæ

$$
\operatorname{Map}_{\prod C_{i}}\left(\left(X_{i}\right),\left(Y_{i}\right)\right) \simeq \prod \operatorname{Map}_{C_{i}}\left(X_{i}, Y_{i}\right)
$$

Next, we want to think about fibre products of animæ-the discussion will be entirely similar to Eg.1.8.6, with a few added complications. To begin with, let's think about the slice category in question.
Example 1.8.14 (Simplices of slices over $\Lambda_{2}^{2}$ ). Let $p: \Lambda_{2}^{2} \rightarrow C$ be a functor into an $\infty$-category $C$. Again, we know the $n$-simplices of $C_{/ p}$ are

$$
\operatorname{sSet}\left(\Delta^{n}, C_{/ p}\right)=\operatorname{sSet}_{p}\left(\Delta^{n} \star \Lambda_{2}^{2}, C\right)
$$

so we really just need to compute $\Delta^{n} \star \Lambda_{2}^{2}$. This is given by an $(n+2)$-simplex where the final 1 -simplex has been subdivided; this is to be expected as $\Lambda_{2}^{2}$ is homotopy equivalent to $\Delta^{1}$, and $\Delta^{n} \star \Delta^{1} \cong \Delta^{n+2}$.
Example 1.8.15 (Pullbacks of animæ). Let $f: X \rightarrow Z$ and $g: Y \rightarrow Z$ be maps of animæ which we represent by maps between Kan complexes. We now claim that $X \times_{Z}^{h} Y$, the homotopy pullback of Df.1.8.3, is a representative for the limit of the diagram $p: \Lambda_{2}^{2} \rightarrow \mathcal{A}$ n, defined by $f$ and $g$, in $\mathcal{A}$ n. Again, to see this, we again consider the commutative diagram of Kan complexes
![img-37.jpeg](img-37.jpeg)
where $C=\mathcal{A} \mathrm{n},\left(T, q_{X}, q_{Y}, \alpha\right)$ is an arbitrary cone over $p$, so $q_{S}: T \rightarrow S$ is a map of animæ for $S \in\{X, Y\}$ and $\alpha$ is a homotopy witnessing the commutativity of the following diagram of animæ:
![img-38.jpeg](img-38.jpeg)

To see the square of mapping animæ above is homotopy pullback of simplicial sets, let's analyse what is going on with its 0 -simplices - the higher simplices again follow with more analysis. In other words, let's naturally identify the 0 -simplices of the top-left-hand mapping animæ with tuples consisting of a 1-morphism $f: T \rightarrow X \times_{Z}^{h} Y$, a pair of 2-morphisms $\beta_{S}: q_{S} \simeq p_{S} \circ f$ for $S \in\{X, Y\}$, and a 3 -morphism $H$ between $\alpha$ and the following diagram
![img-39.jpeg](img-39.jpeg)
where the 2-morphisms are left implicit. Yet again, this follows from the definition of mapping animæ and the identification of 0 - and 1 -simplices of $C_{/ p}$ in this case found in Eg.1.8.14; we

leave the details to the reader. In other words, homotopy pullback $X \times{ }_{Z}^{b} Y$ is an $\infty$-categorical pullback, or equivalently, a Cartesian diagram in $\mathcal{A}$ n is a homotopy pullback in sSet of Kan complexes. We will write $X \times{ }_{Z}^{b} Y$ as $X \times{ }_{Z} Y$ for the rest of these notes based on this example. Exercise 1.8.16. Prove all of the claims in the previous example.

A similar universal property holds for products in a general $\infty$-category.
Example 1.8.17 (Pullbacks in $\mathcal{C}$ ). Let $X \rightarrow Z \leftarrow Y$ be a span in an $\infty$-category $\mathcal{C}$. Suppose that the pullback $X \times_{Z} Y$, so the limit of the above span, exists in $\mathcal{C}$. Copying the arguments of Eg.1.8.15, we obtain the following diagram of mapping animæ
![img-40.jpeg](img-40.jpeg)
which is furthermore a pullback in the $\infty$-category $\mathcal{A}$ n, where the pullback in the lower-righthand corner is also taken in $\mathcal{A}$ n and $\left(T, q_{X}, q_{Y}, \alpha\right)$ is an arbitrary cone over our span. The contractiblity of the top-left-hand anima shows us the desired universal property of $X \times_{Z} Y$ :

$$
\operatorname{Map}_{\mathcal{C}}\left(T, X \times_{Z} Y\right) \xrightarrow{\simeq} \operatorname{Map}_{\mathcal{C}}(T, X) \underset{\operatorname{Map}_{\mathcal{C}}(T, Z)}{\times} \operatorname{Map}_{\mathcal{C}}(T, Y)
$$

In particular, a map $T \rightarrow X \times_{Z} Y$ is simply a pairs of maps $T \rightarrow X$ and $T \rightarrow Y$ plus a homotopy between their postcompositions down to $Z$ along $f$ and $g$. Given $\infty$-categories $\mathcal{C}, \mathscr{D}, \mathcal{E}$ and functors $F: \mathcal{C} \rightarrow \mathcal{E}$ and $G: \mathscr{D} \rightarrow \mathcal{E}$, then the objects of $\mathcal{C} \times_{\mathcal{E}} \mathscr{D}$ are exactly triples $(X, Y, \alpha)$ where $X \in \mathcal{C}, Y \in \mathscr{D}$, and $\alpha: F(X) \simeq G(Y)$.
Exercise 1.8.18. Show that binary products defined as above are the same as the limit of the $\operatorname{cospan} X \rightarrow * \leftarrow Y$.

We can continue in this fashion: for each diagram shape $K$, we come up with an explicit expression for homotopy limits over such a diagrams inside $\mathcal{A}$ n, prove that this explicit expression is indeed the $\infty$-categorical limit inside $\mathcal{A}$ n by analysing mapping spaces of $\mathcal{A} \mathrm{n}_{\text {/p }}$ for general $p: K \rightarrow \mathcal{A}$ n, and then obtain a nice universal property for mapping into such shaped limits in a general $\infty$-category $\mathcal{C}$.
Exercise 1.8.19. Formulate and prove dual versions of Egs.1.8.6, 1.8.12, 1.8.15 and 1.8.17, for coproducts and pushouts.

We will make one more example explicit, but we will leave most of the details to the reader. Exercise 1.8.20. Let $K=N\left(\mathbf{N}^{\mathrm{op}}\right)=\mathbf{N}^{\mathrm{op}}$, and let's drop the nerve notation for simplicity, be the simplicial set of the natural numbers with its usual ordering where we have implicitly taken a nerve, and let $p: \mathbf{N}^{\mathrm{op}} \rightarrow \mathcal{A}$ n be an $\mathbf{N}^{\mathrm{op}}$-shaped diagram of animæ:

$$
p=\cdots \xrightarrow{f_{4}} X_{3} \xrightarrow{f_{3}} X_{2} \xrightarrow{f_{2}} X_{1} \xrightarrow{f_{1}} X_{0}
$$

Let us write $X=\lim X_{i}$ for the mapping microscope of this diagram, so this means the limit of

$$
\cdots \xrightarrow{f_{4}^{\prime}} P_{3} \xrightarrow{f_{3}^{\prime}} P_{2} \xrightarrow{f_{2}^{\prime}} P_{1} \xrightarrow{f_{1}^{\prime}} X_{0}
$$

where we have inductively fibrantly replaced $f_{i}: X_{i} \rightarrow X_{i-1} \rightarrow P_{i-1}$ as in Df.1.8.3. In particular, 0 -simplices of $X$ are a collection of objects $x_{i} \in X_{i}$ for each $i \geqslant 0$ plus a collection of paths $\gamma_{i}: \Delta^{1} \rightarrow X_{i-1}$ such that $\gamma_{i}(0)=x_{i-1}$ and $\gamma_{i}(1)=f_{i}\left(x_{i}\right)$. Show that $X$ is the $\infty$-categorical limit of $p$ inside $\mathcal{A}$ n. Given a diagram $p: \mathbf{N}^{\mathrm{op}} \rightarrow C$ into an arbitrary $\infty$-category $C$ such that its limit $X$ exists, show that the natural map of animæ

$$
\operatorname{Map}_{C}(T, X) \xrightarrow{\simeq} \lim \operatorname{Map}_{C}\left(T, X_{i}\right)
$$

is an equivalence for all $T$ in $C$.
In other words, mapping from an object $T$ into a sequential limit $\lim X_{i}$ is precisely the data of a collection of maps $T \rightarrow X_{i}$ and a collection of homotopies between $T \rightarrow X_{i} \rightarrow X_{i-1}$ and $T \rightarrow X_{n-1}$. In particular and of much importance to us, given a sequential diagram of $\infty$-categories $\cdots C_{1} \xrightarrow{f_{1}} C_{0}$ with limit $C$, then an object of $C$ is a collection of objects $X_{i} \in C$ together with equivalences $f_{i} X_{i} \simeq X_{i-1}$.

Suffice to say, if we look at diagrams of different shapes, we also have to come up with a general version of homotopy limit. This can be done, and actually works for all general Kan-enriched simplicial categories.
Theorem 1.8.21 ([Lur09b, Th.4.2.4.1]). Let $F: g \rightarrow m$ be a simplicial functor between fibrant simplicial categories. Then a cocone of $F$ is a homotopy colimit in $m$ if and only if the image of this cocone in the simplcial nerve of $m$ is a colimit in this $\infty$-category.

We will not prove the above theorem, not only because its proof is lengthy and technical, but because we won't need it! Most of the limits and colimits we will be taking either products or coproducts, pullbacks or pushouts, and sequential limits or colimits. In a precise sense, this is also all one needs to check.
Proposition 1.8.22 ([Lur09b, Pr.4.4.2.6]). If an $\infty$-category has all products and pullbacks, then it has all limits indexed by (small) simplicial sets.
Corollary 1.8.23. Both $\mathcal{A}$ n and Cat ${ }_{\infty}$ are complete and cocomplete, meaning they both admit all $K$-indexed limits and colimits for all (small) simplicial sets $K$.
Proof. Combining Pr.1.8.22 with Egs.1.8.6 and 1.8.15 we see that $\mathcal{A}$ n is complete. To see $\mathcal{A}$ n is cocomplete, we use Exc.1.8.19 and the dual of Pr.1.8.22. It is also relatively simple to show that the product and coproduct of Kan enriched simplicial categories yields the $\infty$ categorical product and coproduct inside $\mathrm{Cat}_{\infty}$. The construction of pullbacks and pushouts of Kan enriched simplicial categories is a little more technical, and we omit the details; see [Lan21, Th.4.3.37].

The following are three fun exercises dealing with $\infty$-categorical limits and colimits.
Exercise 1.8.24. Show that $\mathcal{A}$ n is generated under colimits by its terminal object. Hint: from * we get all discrete animæ, so those $X$ with homotopy groups concentrated in degree 0 , using coproducts. In particular, we have $*$ and $S^{0}$, from which we can take iterated pushouts and get all spheres $S^{n}$. We can now use a skeletal filtration on an arbitrary anima $X$ by fixing a Kan complex representing $X$ and applying the ideas of Exc.1.4.10. Taking a filtered colimits of the pushouts defining this skeletal filtration finishes the job.

Exercise 1.8.25. Show that products and pullbacks in an $\infty$-category all commute with each other. Likewise, show that all coproducts and pushouts commute with one another. ${ }^{4}$
Exercise 1.8.26. Let $C_{i}$ be a diagram of $\infty$-categories with limit $C$. Suppose the shape of this diagram is either an arbitrary product or a pullback. ${ }^{5}$ Show that the natural functors of $\infty$-categories

$$
\operatorname{Fun}(\mathscr{D}, C) \rightarrow \lim \operatorname{Fun}\left(\mathscr{D}, C_{i}\right)
$$

is an equivalence of $\infty$-categories for all $\infty$-categories $\mathscr{D}$.

End of lecture 6 and week 3

# 1.9 Loose ends and an outlook (not discussed in lectures) 

In this little section, we want to mention something which we promised in class, but skipped the proof of, as well as give some perspective on some of the other useful facets of higher categories.

First, we want to prove Pr.1.3.5 using Clm.1.7.14.
Proof of Pr.1.3.5. Recall, we want to show that if an $\infty$-category $C$ is such that all morphisms are isomorphisms, then $C$ is in fact a Kan complex.
Claim 1.9.1. For each morphism $f: \Delta^{1} \rightarrow C$ inside $C$, then $f$ is an equivalence if and only if for every $n \geqslant 2$ and every map $g: \Lambda_{0}^{n} \rightarrow C$ such that its restriction to $\{0<1\}$ is $f$ there exists a lift of $g$ to $\Delta^{n}$.

Assuming this claim, then we see that to see $C$ is a Kan complex, we need to show all maps $\Lambda_{i}^{n} \rightarrow C$ extend over $\Delta^{n}$. The cases for $0<i<n$ follow as $C$ is an $\infty$-category, the case $i=0$ follows from the claim, and $i=n$ follows from the claim applied to $C^{\text {op }}$, and we are done.

Okay, back to the proof of Clm.1.9.1. If $f$ satisfies this lifting property, then to construct a homotopy inverse to $f$ we consider the diagram $\Lambda_{0}^{2} \rightarrow C$ of the form
![img-41.jpeg](img-41.jpeg)

[^0]
[^0]:    ${ }^{4}$ This exercise does work in general, but we have not shown that in general a limit $X$ of a diagram $X_{i}$ in an $\infty$-category $C$ has the universal property that

    $$
    \operatorname{Map}_{C}(T, X) \xrightarrow{\simeq} \lim \operatorname{Map}_{C}\left(T, X_{i}\right)
    $$

    is an equivalence of animæ for all objects $T$ of $C$; see [Lurb, Tag 02WA], for some discussion in this direction.
    ${ }^{5}$ C.f. the previous footnote.

from which we obtain a candidate $f^{-1}: Y \rightarrow X$ and a homotopy between $f^{-1} \circ f \simeq \operatorname{id}_{X}$. To obtain the other homotopy, we consider the diagram $\Lambda_{0}^{3} \rightarrow \mathcal{C}$ defined by the picture
![img-42.jpeg](img-42.jpeg)
where all of the arrows are either the obvious identities, $f$, or $f^{-1}$, the first 2 -simplicex is defined by the above lift, and the second are degenerate, ie, the natural 2 -simplex witnessing $f \circ \operatorname{id}_{X} \simeq f$, for example. The assumed lifting properties then give us a filling of this diagram, and $d_{0}$ of this filling witnesses $f \circ f^{-1} \simeq \operatorname{id}_{Y}$.

Conversely, suppose we are given that $f$ is an equivalence and a map $g: \Lambda_{0}^{n} \rightarrow \mathcal{C}$ we wish to extend. We now use Exc.1.7.10: we claim that the left horn inclusion $\Lambda_{0}^{n} \rightarrow \Delta^{n}$ is precisely obtained from taking the pushout of joins along $\Lambda_{0}^{1} \rightarrow \Delta^{1}$ on the left and $\partial \Delta^{n-2} \rightarrow \Delta^{n}$ on the right. In this case, the desired lifting problem is equivalent to the lifting problem
![img-43.jpeg](img-43.jpeg)
where $\varphi$ is adjoint to $g$ restricted to $\Delta^{\{0\}} \star \Delta^{\{2, \ldots, n\}}$ and $\psi$ is adjoint to $g$ restricted to $\Delta^{\{0,1\}} \star$ $\partial \Delta^{\{2, \ldots, n\}}$. We know that the projection $p$ from $\mathcal{C}_{/ g(\partial \Delta\{2, \ldots, n\})}$ to $\mathcal{C}$ is a right fibration (its the dual of Pr.1.7.9) and a similar argument also shows that $q$ is a right fibration. As $p$ is a right fibration it is conservative by Exc.1.4.4. We then see that $\psi$ is an equivalence, as $p(\psi)=f$ which is assumed to be an equivalence. We now use the lifting property of equivalences through right fibrations of Exc.1.4.5, to lift $\psi$ in the diagram, which gives us our desired lift. And we're done!

Exercise 1.9.2. Fill in some of the gaps in the above proof by showing that $q$ is indeed a right fibration.

The goal of these lectures is to discuss Sp with an $\infty$-categorical perspective. What we have done so far will enable us to define Sp and prove many basic things, but there are many more facets of higher category theory which would really aid our understanding of Sp , such as the Yoneda lemma, which we will assume from now on, the presentability of Sp , which we will ignore, and monoidal structures, which we will give a brief overview of now.

Classically, we say that a symmetric monoidal category $\mathcal{C}$ is a choice of bifunctor $\otimes: \mathcal{C} \otimes$ $\mathcal{C} \rightarrow \mathcal{C}$ which acts like a tensor product on $\mathcal{C}$, meaning there are is a choice of unit object $\mathbf{1}$

and a choice of natural equivalences

$$
(X \otimes Y) \otimes Z \simeq X \otimes(Y \otimes Z) \quad \mathbf{1} \otimes X \simeq X \simeq X \otimes \mathbf{1} \quad X \otimes Y \simeq Y \otimes X
$$

natural in $X, Y, Z \in \mathcal{C}$, such that the two diagrams
![img-44.jpeg](img-44.jpeg)
commute; we let the reader fill in exactly which natural transformation is occurring in each position.

Simple examples include any category with finite products, then the finite product defines a monoidal structure with unit the empty product, ie, the terminal object, and the category of $R$-module and the tensor product $\otimes_{R}$ with unit $R$ itself.

We now find ourselves in a situation though: how can we generalise this to $\infty$-categories. As written, a symmetric monoidal category is already a lot of separate pieces of data, and you can imagine that in a higher categorical world, the triangle and pentagon above would now have to be witnessed to commute by a choice of homotopy, which itself would have to fit in a myriad of different diagrams with various 3 -cells, and these 3 -cells too would have to work well together, and so on. This extra data is not for nothing too - we need a way to systematically discuss associativity of a symmetric monoidal structure for higher collections of objects, above the order 4 collection of objects above. It is a theorem of Mac Lane that the axioms above suffice to determine all higher potentially bracket compositions, but in the higher categorical world we should not expect this. It becomes too much far too soon.

Let us then rework the idea of a symmetric monoidal $\infty$-category then into a language better suited to a higher categorical translation - what follows is also very elegantly put in the introduction to [Lur17, §2].

We would like a definition of a symmetric monoidal category which does not say "here is how to multiply two things together, and here is a sequence of data to multiple more than two things", we would like it to say "here is the collection of all the ways to multiple many things together, and all of the possible ways they can interact". In a way, we turn a minimal

definition into a maximal one. In terms of category theory and homotopy theory, this often gives a more functorial definition.

Let $\mathcal{C}$ be a symmetric monoidal category. We define a category $\mathcal{C}^{\otimes}$ to have as objects finite sequences of elements $\left(X_{1}, \ldots, X_{n}\right)$ in $\mathcal{C}$, these are a choice of $n$-many things we want to tensor together, we just haven't chosen in what order of bracketing yet, and where morphisms are defined as follows: a morphism from $\left(X_{1}, \ldots, X_{n}\right)$ to $\left(Y_{1}, \ldots, Y_{m}\right)$ is a subset $S \subseteq\{1, \ldots, n\}$ and a map of finite sets $\varphi: S \rightarrow\{1, \ldots, m\}$, together with a collection of morphisms $f_{i}: \oplus_{\varphi(j)=i} X_{j} \rightarrow Y_{i}$ for $1 \leqslant i \leqslant m$. The tensor product $\oplus_{\varphi(j)=i} X_{j}$ is well-defined up to canonical isomorphism inside $\mathcal{C}$ from the axioms of a symmetric monoidal category. This is supposed to be thought of as a collection of morphisms $\otimes_{i} f_{i}: \otimes X_{j} \rightarrow \otimes Y_{i}$, where we have chosen a particular partition of $\otimes X_{j}$ into bracketed according to $\varphi$. We will let the reader think about how composition can be defined in $C^{\otimes}$.

There is a natural functor $\pi: C^{\otimes} \rightarrow \operatorname{Fin}_{*}$, from the category defined above to the category of finite sets with a distinguished base-point, which sends an object $\left(X_{1}, \ldots, X_{n}\right)$ to the finite set $\{1, \ldots, n\}_{+}=\langle n\rangle$, our notation for the union of $\{1, \ldots, n\}$ with a disjoint base-point. Let us write $C_{\langle n\rangle}^{\otimes}$ for the fibre of $\pi$ over some $\langle n\rangle \in \operatorname{Fin}_{*}$.

There are now two key observations to make:

1. Firstly, the functor $\pi$ is a kind of categorical fibration. More specifically, an op-fibration. This means that for each object $\left(X_{1}, \ldots, X_{n}\right)$ of $C^{\otimes}$ and each morphism $f:\langle n\rangle \rightarrow\langle m\rangle$ in $\operatorname{Fin}_{*}$, there is a morphism $\widetilde{f}:\left(X_{1}, \ldots, X_{n}\right) \rightarrow\left(Y_{1}, \ldots, Y_{m}\right)$ in $C^{\otimes}$ such that $\pi \widetilde{f}=f$, so $\widetilde{f}$ is a lift of $f$, and which is furthermore universal, meaning the natural map
$C^{\otimes}\left(\left(Y_{1}, \ldots, Y_{m}\right),\left(Z_{1}, \ldots, Z_{l}\right)\right) \xrightarrow{\tilde{f}^{*} \times \pi} C\left(\left(X_{1}, \ldots, X_{n}\right),\left(Z_{1}, \ldots, Z_{l}\right)\right) \underset{\operatorname{Fin}_{*}(\langle n\rangle,\langle l\rangle)}{\times} \operatorname{Fin}_{*}(\langle m\rangle,\langle l\rangle)$
is an bijection, for any third object $\left(Z_{1}, \ldots, Z_{l}\right)$ of $C^{\otimes} .{ }^{6}$ This property of being an opfibration means that any map $f:\langle n\rangle \rightarrow\langle m\rangle$ induces a functor $F: C_{\langle n\rangle}^{\otimes} \rightarrow C_{\langle m\rangle}^{\otimes}$ which is unique up to canonical isomorphism. Indeed, just fix this $f$ and some object $\left(X_{1}, \ldots, X_{n}\right)$ in $C_{\langle n\rangle}^{\otimes}$, then the image of this object under $F$ is the universal $\left(Y_{1}, \ldots, Y_{m}\right)$ chosen above. Try to see if you can write down what $F$ does on morphisms.
2. Secondly, the fibres of $\pi$, the categories $C_{\langle n\rangle}^{\otimes}$ are equivalent to $C^{n}$. This is kind of obvious from our presentation so far, but notice we can write down this equivalence purely in terms of the op-fibration structure of $\pi$ : notice that $C_{\langle 1\rangle}^{\otimes}=\mathcal{C}$. Now, let $r_{n}^{i}:\langle n\rangle \rightarrow\langle 1\rangle$ be the map sending every $j \in\langle n\rangle$ to $*$, unless $j=i$. Here $1 \leqslant i \leqslant n$. Then the equivalence above is given by

$$
\prod_{i=1}^{n} R_{n}^{i}: C_{\langle n\rangle}^{\otimes} \xrightarrow{\simeq} \prod_{i=1}^{n} C_{\langle 1\rangle}^{\otimes}
$$

[^0]
[^0]:    ${ }^{6}$ In particular, $C^{\otimes}$ is actually the Grothendieck construction $\left\lvert\,{ }^{\text {Fin } *} C^{1}-\right)$ of a functor of 2-categories $\operatorname{Fin}_{*} \rightarrow$ Cat $_{1}$ to the 2-category of 1-categories, which sends $\langle n\rangle$ to $C^{n}$ and does the obvious thing on morphisms.

These properties of $\pi$ actually fully determine the symmetric monoidal structure on $C$, up to symmetric monoidal equivalence. What we mean, is that if $p: \mathscr{D} \rightarrow \operatorname{Fin}_{*}$ is an op-fibration such that the map $\prod_{i=1}^{n} R_{n}^{i}$ is an equivalence for all $n$, then $\mathscr{D}_{\langle 1\rangle}$ has a symmetric monoidal structure, unique up to symmetric monoidal equivalence by the fact that $\mathscr{D} \simeq \mathscr{D}_{\langle 1\rangle}^{\otimes}$. Indeed, this is rather fun to unpack: from the second condition above set to $n=0$, we see that $\mathscr{D}_{\langle 0\rangle}$ is the category $*$ with a single object and a single morphism, ie, the terminal category. The unique map $\langle 0\rangle \rightarrow\langle 1\rangle$ then gives us a functor $* \rightarrow \mathscr{D}_{\langle 1\rangle}$ which will be our choice of unit object. To construct the tensor product, consider the composition

$$
\mathscr{D}_{\langle 1\rangle} \times \mathscr{D}_{\langle 1\rangle} \stackrel{\infty}{\leftarrow} \mathscr{D}_{\langle 2\rangle} \xrightarrow{\langle 2\rangle \rightarrow\langle 1\rangle} \mathscr{D}_{\langle 1\rangle}
$$

where the indicated map above sends $2,1 \mapsto 1$ and preserves the base-point. It is fun exercise now to construct the natural transformations capturing the associativity and unitality, as well as the pentagon axiom and so on.

What is very useful about this description of a symmetric moniodal $\infty$-category as an opfibration with a nice property, is that it does not concern itself with the Mac Lane pentagon theorem stating that if the pentagon commutes then everything else works-everything else is simply contained in the data of the op-fibration. It is the difference between a minimal definition and a maximal definition.

We can now define what a symmetric monoidal $\infty$-category is.
Definition 1.9.3. A symmetric monoidal $\infty$-category is a coCartesian fibration $C \rightarrow N\left(\mathrm{Fin}_{*}\right)$.
Of course, we need to know what a coCartesian fibration is-suffice it to say that for now, it is a variation on the theory of fibrations of simplicial sets we discussed in $\S 1.4$. A majority of [Lur17] is a quest to show that the above definition is both practical and fruitful, and in particular, that is leads to an $\infty$-category of $\mathbf{E}_{\infty}$-rings $\operatorname{CAlg}(\mathrm{Sp})$.

# Chapter 2 

## The $\infty$-category of spectra

From now on in the course we will continue to use the language of $\infty$-categories, that will be our language for homotopy theory from now on, but the specifics will become less and less relevant as we continue. These foundations are sturdy as well as flexible, but what we really want to study now is stable homotopy theory, so objects in the $\infty$-category Sp and the relationships between these objects, algebra, and geometry.
Warning 2.0.1. From this moment on, we are not going to detail all of the $\infty$-category theory we will use. What is used will be indicated and referenced, but in the interest of time, we have decided that we have seen enough lean higher category theory for this course. In particular, we will often "define functors" by writing down a formula. This is absolutely not allowed in the realm of $\infty$-categories, or even 1-categories strictly speaking, as much more data is needed. In the first few instances, we will leave it to the reader to show these "assignments" can be refined to functors of $\infty$-categories. As the semester goes on, we will stop making these remarks explicitly, and leave it to the reader to justify some of these statements.

### 2.1 Definition of Sp and its basic properties

Recall that the $\infty$-category of pointed animæ is defined as the slice $\mathcal{A} \mathrm{n}_{*}=\mathcal{A} \mathrm{n}_{*} /$.
Definition 2.1.1. Given a pointed anima $X$, we write $\Sigma X$ for the colimit of the span $* \leftarrow$ $X \rightarrow *$ and $\Omega X$ for the limit of the $\operatorname{cospan} * \rightarrow X \leftarrow *$. We call $\Sigma X$ the suspension of $X$ and $\Omega X$ the loops of $X$.

Using Eg.1.8.15, we see that if we choose a model of $X$ as a Kan complex, then $\Omega X$ can be modelled by the pullback of simplicial sets of the $\operatorname{cospan} P * \rightarrow X \leftarrow *$, where $P * \rightarrow X$ is a fibrant replacement for the map $* \rightarrow X$ defined by the base-point of $X$. From this, we see that $\Omega X$ is our usual based loop anima of $X$. Dually, we see that if we choose a model of $X$ as a Kan complex, then $\Sigma X$ can be modelled by the pushout in the 1-category of simplicial sets of the span $C X \leftarrow X \rightarrow *$, where $C X$ is the reduced cone of $X$. Indeed, the dual argument of Eg.1.8.15 is to cofibrantly replace $X \rightarrow *$, in other words, to make this map a level-wise injection of simplicial sets, and we can easily model this by $X \rightarrow X \star \Delta^{0}=C X$ as $C X$ is

contractible in this case. It follows that $\Sigma X$ is our old friend the reduced suspension from previous courses.
Exercise 2.1.2. Show that $\Sigma$ and $\Omega$ induce endofunctors $\mathcal{A} \mathrm{n}_{*} \rightarrow \mathcal{A} \mathrm{n}_{*}$.
This leads us to a definition of the $\infty$-category of spectra!
Definition 2.1.3. The $\infty$-category of spectra Sp is the limit inside Cat $_{\infty}$

$$
\mathrm{Sp}=\lim \left(\cdots \xrightarrow{\Omega} \mathcal{A} \mathrm{n}_{*} \xrightarrow{\Omega} \mathcal{A} \mathrm{n}_{*} \xrightarrow{\Omega} \mathcal{A} \mathrm{n}_{*}\right)
$$

Using our discussion of limits and colimits of this form in $\S 1.8$, in particular Exc.1.8.20, we see that an object in the $\infty$-category Sp is precisely a collection of pointed animæ $X_{n}$ for each $n \geqslant 0$, together with an equivalence $\Omega X_{n+1} \simeq X_{n}$ inside $\mathcal{A} \mathrm{n}_{*}$. In other words, an object in Sp is an $\Omega$-spectrum as seen in Topology II. Moreover, by we can now unpack what a morphism between spectra is.
Example 2.1.4. Consider a functor $p: K \rightarrow \mathrm{Cat}_{\infty}$ where $K$ is a simplicial set and let us write $C_{k}$ for the $\infty$-category $p(k)$. The $\infty$-category of $\infty$-categories has all limits and colimits by Cor.1.8.23, so we can take the limit of this diagram and obtain an $\infty$-category $C$. We now claim that for all objects $X$ and $Y$ inside $C$, that there is a canonical equivalence of animæ

$$
\operatorname{Map}_{C}(X, Y) \xrightarrow{\simeq} \lim \operatorname{Map}_{C_{i}}\left(p_{i} X, p_{i} Y\right)
$$

where $p_{i}: C \rightarrow C_{i}$ are the functors in the structure of $C$ as a cone over $p$. Indeed, following an argument similar to Cor.1.8.23, it suffices to prove the above statement for arbitrary products and pullbacks. In this case, we use the Fubini theorem of Exc.1.8.25 inside Cat $_{\infty}$, Exc.1.8.26, and the definition of a mapping anima: ${ }^{1}$

$$
\begin{aligned}
& \operatorname{Map}_{C}(X, Y) \simeq \operatorname{Fun}\left(\Delta^{1}, C\right) \underset{\operatorname{Fun}\left(\partial \Delta^{1}, C\right)}{\times}\left\{(X, Y)\right\} \simeq \lim \operatorname{Fun}\left(\Delta^{1}, C_{i}\right) \underset{\lim \operatorname{Fun}\left(\partial \Delta^{1}, C_{i}\right)}{\times}\left\{\left\{p_{i} X, p_{i} Y\right\}\right\} \\
& \simeq\left(\lim \operatorname{Fun}\left(\Delta^{1}, C_{i}\right) \underset{\operatorname{Fun}\left(\partial \Delta^{1}, C_{i}\right)}{\times}\left\{\left\{p_{i} X, p_{i} Y\right\}\right\}\right) \simeq \lim \operatorname{Map}_{C_{i}}\left(p_{i} X, p_{i} Y\right)
\end{aligned}
$$

Using Eg.2.1.4, we see that for two spectra $X, Y$, the mapping anima $\operatorname{Map}_{\mathrm{Sp}}(X, Y)$ can be written as the limit of animæ

$$
\lim \left(\cdots \rightarrow \operatorname{Map}_{\mathcal{A} \mathrm{n}_{*}}\left(X_{n+1}, Y_{n+1}\right) \xrightarrow{\Omega} \operatorname{Map}_{\mathcal{A} \mathrm{n}_{*}}\left(\Omega X_{n+1}, \Omega Y_{n+1}\right) \simeq \operatorname{Map}_{\mathcal{A} \mathrm{n}_{*}}\left(X_{n}, Y_{n}\right) \rightarrow \cdots\right)
$$

where the first map is induced by the functor $\Omega: \mathcal{A} \mathrm{n}_{*} \rightarrow \mathcal{A} \mathrm{n}_{*}$ and the second from the given equivalences $\Omega X_{n+1} \simeq X_{n}$ for both $X$ and $Y$. We will often just write this mapping anima as this limit

$$
\operatorname{Map}_{\mathrm{Sp}}(X, Y) \simeq \lim \operatorname{Map}_{\mathcal{A} \mathrm{n}_{*}}\left(X_{n}, Y_{n}\right)
$$

[^0]
[^0]:    ${ }^{1}$ Here we also need to use the fact that $\operatorname{Fun}(K,-): \mathrm{Cat}_{\infty} \rightarrow \mathrm{Cat}_{\infty}$ commutes with limits. This can be shown using the universal property of limits, the Yoneda lemma, and the fact that $\operatorname{Map}_{\mathrm{Cat}_{\infty}}(C \times \mathscr{D}, \mathscr{E}) \simeq$ $\operatorname{Map}_{\mathrm{Cat}_{\infty}}(C, \operatorname{Fun}(\mathscr{D}, \mathscr{E}))$-this last fact follows as products and functor categories are defined on the nose in sSet and mapping animæ in Cat $_{\infty}$ can be modelled by taking the groupoid core $(-)^{\approx}$, a right adjoint, of the internal mapping simplicial sets.

Using Exc.1.8.20, we see that a morphism of spectra $f: X \rightarrow Y$ is a morphisms $f_{n}: X_{n} \rightarrow Y_{n}$ of pointed animæ for each $n \geqslant 0$ and a collection of homotopies $H_{n}: \sigma_{n}^{Y} \Omega f_{n+1} \simeq f_{n} \sigma_{n}^{X}$, where $\sigma_{n}^{X}: \Omega X_{n+1} \simeq X_{n}$ is the given structure map. In other words, $H_{n}$ witnesses the commutativity of the diagram
![img-45.jpeg](img-45.jpeg)

Definition 2.1.5. We define the stable homotopy category as the homotopy category h Sp of the $\infty$-category of spectra.

In particular, objects of h Sp are $\Omega$-spectra and the set of maps between two spectra $X, Y$ is given by a sequence of pointed maps $f_{n}: X_{n} \rightarrow Y_{n}$ and a choice of homotopy $H_{n}$ as above, and these tuples are only specified "up to homotopy" themselves.
Remark 2.1.6. Recall from Topology II that Brown representability states that for any cohomology theory $E^{*}$ on the category of pointed CW-complexes, we obtain a sequence of pointed CW-complexes $E_{n}$ and weak homotopy equivalences $\Omega E_{n+1} \simeq E_{n}$. In particular, we constructed an assignment (not a functor!) from the objects in the 1-category of cohomology theories to the objects in the stable homotopy category. By the Yoneda lemma, a natural transformation $f^{*}: E^{*} \rightarrow F^{*}$ of cohomology theories induces a collection of pointed maps $f_{n}: E_{n} \rightarrow F_{n}$ such that $\left[\sigma_{n}^{Y} \Omega f_{n+1}\right]=\left[f_{n} \sigma_{n}^{X}\right]$ agree as homotopy classes of maps, but no particular homotopy is chosen. In particular, it is not very difficult to make a consistent choice of homotopies witnessing the above equality of homotopy classes which then compose together well. In other words, it is very difficult, perhaps impossible, to refine this assignment from Brown representability to a functor from cohomology theories to the stable homotopy category.

The following is a consequence of our definition of Sp.
Corollary 2.1.7. The adjoint functors $\Omega$ and $\Sigma$ on Sp are mutual inverses.
Recall from Exc.1.5.14 that for us, an adjunction of $\infty$-categories is a pair of functors $F: \mathcal{C} \rightarrow \mathscr{D}$ and $G: \mathscr{D} \rightarrow \mathcal{C}$ together with a natural transformation of presheaves

$$
\operatorname{Map}_{\mathscr{D}}(F(-),-) \simeq \operatorname{Map}_{\mathcal{C}}(-, G(-)): \mathcal{C}^{\mathrm{op}} \times \mathscr{D} \rightarrow \mathscr{A} \mathrm{n}
$$

which is an equivalence. There are other equivalent definitions in the literature; see [Lurb, Tag 02C9].

Proof. Clearly $\Omega$ is an equivalence, this is by definition of Sp.
Indeed, to see this, we note that $\Omega: \mathrm{Sp} \rightarrow \mathrm{Sp}$ is induced by taking horizontal limits in the following clearly commutative diagram of $\infty$-categories:
![img-46.jpeg](img-46.jpeg)

In this sense, we can see that $\Omega X$ has $n$th anima $\Omega X_{n} \simeq X_{n-1}$, in other words, $\Omega$ shifts the pointed animæ comprising a spectrum up by one, with $(\Omega X)_{0}=\Omega X_{0}$ simply being what it is. The candidate inverse to $\Omega$, denoted by $\Omega^{-1}$ is then given by shifting in the other direction, so $\Omega^{-1}(X)$ has $n$th anima $X_{n+1}$. We then see clearly that $\Omega^{-1} \Omega \simeq \mathrm{id}_{\mathrm{Sp}}$-just write this down. For the other composite, we see that

$$
\Omega \Omega^{-1} X=\Omega\left(X_{1}, X_{2}, X_{3}, \ldots\right)=\left(\Omega X_{1}, X_{1}, X_{2}, \ldots\right)
$$

which is naturally equivalent to $\left(X_{0}, X_{1}, X_{2}, \ldots\right)$ using the structure map $\Omega X_{1} \simeq X_{0}$ for $X$.
As $\Omega^{-1}$ is left adjoint to $\Omega$, we then use the uniqueness of adjoints to see that $\Omega^{-1} \simeq \Sigma$.
With this in mind, we will write $\Sigma^{-n}=\Omega^{n}$ for positive integers $n>0$. There is a potential for sign errors with this notation! For example, we would like to say $\Sigma^{n} \Sigma \Sigma^{-n}$ is "equivalent" to $\Sigma$. This is true, but if $n$ is odd, one will pick up some signs when passing these $\Sigma^{n}$ 's past the $\Sigma$. We will see if this comes up in any proofs later on for us.
Exercise 2.1.8. Show that for a spectrum $X$, the suspension $\Sigma^{n} X$ is equivalent to the shift $X[n]$ given by $X[n]_{i}=X_{i+n}$ where $X_{d}=\Omega^{-d} X_{0}$ for $d<0$. The structure maps for $X[n]$ come from the structure maps for $X$ or the tautological equivalence $X_{d}=\Omega^{-d} X_{0} \simeq \Omega \Omega^{-d-1} X_{0}=\Omega X_{d+1}$ for $d \leqslant 0$.

Notation 2.1.9. The shift notation $[n]=\Sigma^{n}$ is great, so let's switch to that from now! We will also write $[-n]=\Omega^{n}$.

The following proposition is crucial in comparing spectra with based animæ. The functor $\Omega^{\infty}: \mathrm{Sp} \rightarrow \mathcal{A} \mathrm{n}_{*}$ defined by the projection onto the zeroth factor in the limit diagram defining Sp; it sends a spectrum $X=\left\{X_{n}\right\}$ to $X_{0}$.

Proposition 2.1.10. The functor $\Omega^{\infty}$ fits into an adjunction

$$
\Sigma^{\infty}: \mathcal{A} \mathrm{n}_{*} \rightleftarrows \mathrm{Sp}: \Omega^{\infty}
$$

where $\Sigma^{\infty} X$ the suspension spectrum of the pointed anima $X$.
Proof. To construct the adjoint to $\Omega^{\infty}$, we will use the following:
Claim 2.1.11. The functor $\Omega: \mathcal{A} \mathrm{n}_{*} \rightarrow \mathcal{A} \mathrm{n}_{*}$ commutes with filtered ${ }^{2}$ colimits.
Proof of claim. To see that for any filtered diagram $X: I \rightarrow \mathcal{A} \mathrm{n}_{*}$, the natural map

$$
\Omega\left(\operatorname{colim} X_{i}\right)=\operatorname{Map}_{\mathcal{A} \mathrm{n}_{*}}\left(S^{1}, \operatorname{colim} X_{i}\right) \rightarrow \operatorname{colim} \operatorname{Map}_{\mathcal{A} \mathrm{n}_{*}}\left(S^{1}, X_{i}\right)=\operatorname{colim} \Omega\left(X_{i}\right)
$$

is an equivalence of based animæ, we want to show it induces a weak equivalence on homotopy groups using Whitehead's theorem; see Th.1.3.31. However, this follows from the fact that

[^0]
[^0]:    ${ }^{2}$ The adjective filtered will appear a few times to come, and in every case, we want to consider our diagram to be indexed by the nerve of a filtered 1-category; generalisations are of course possible, but unnecessary for us here. Recall that a category $I$ is said to be filtered if it is nonempty, for all $x, y \in I$ there is a common $z$ such that $x \rightarrow z$ and $x \rightarrow z$ in $I$, and for any pair of parallel arrows $f, g: x \rightarrow y$, there is a common arrow $h: y \rightarrow z$ such that $h f=g h$.

filtered colimits commute with homotopy groups; this was an exercise in Topology I using the fact that sphere are compact animæ. ${ }^{3}$

Let us now write $Q: \mathcal{A} \mathrm{n}_{*} \rightarrow \mathcal{A} \mathrm{n}_{*}$ for the functor defined by the formula $Q X=\operatorname{colim} \Omega^{n} \Sigma^{n} X$; as an exercise, show this does in fact define a functor of $\infty$-categories. The above claim then gives us the natural equivalence

$$
\Omega Q \Sigma X=\Omega \operatorname{colim} \Omega^{n} \Sigma^{n+1} X \stackrel{\simeq}{\leftarrow} \operatorname{colim} \Omega^{n+1} \Sigma^{n+1} X \simeq Q X
$$

of pointed animæ. This then leads us to a spectrum $\Sigma^{\infty} X$ whose $n$th anima is $Q \Sigma^{n} X$; again, as an exercise, show this assignment actually defines a functor $\Sigma^{\infty}: \mathcal{A} \mathrm{n}_{*} \rightarrow \mathrm{Sp}$ of $\infty$-categories. There is also a natural map $\varepsilon: X \rightarrow \Omega^{\infty} \Sigma^{\infty} X=Q X$ given by inserting $X$ into the zeroth component of this colimit. To see that $\Sigma^{\infty}$ is left adjoint to $\Omega^{\infty}$, we'll show this natural map acts as a unit and provide us with our natural isomorphism desired for an adjunction. In other words, let us see that the following composite of maps of animæ

$$
\operatorname{Map}_{\mathrm{Sp}}\left(\Sigma^{\infty} X, Y\right) \xrightarrow{\Omega^{\infty}} \operatorname{Map}_{\mathcal{A} \mathrm{n}_{*}}\left(\Omega^{\infty} \Sigma^{\infty} X, \Omega^{\infty} Y\right) \xrightarrow{\varepsilon} \operatorname{Map}_{\mathcal{A} \mathrm{n}_{*}}\left(X, \Omega^{\infty} Y\right)
$$

is an equivalence. To see this, consider the commutative diagram of animæ
![img-47.jpeg](img-47.jpeg)
where the squares commute from the naturality of the unit map for the suspension-loop adjunction of pointed animæ, and the triangles commute by definition of the diagonal maps. Taking limits in the vertical direction yields $\operatorname{Map}_{\mathcal{A} \mathrm{n}_{*}}\left(Q \Sigma^{k} X, Y_{k}\right)$ in the $k$ th column (from the right) from the universal property of the colimit defining $Q$ :

$$
\lim \operatorname{Map}_{\mathcal{A} \mathrm{n}_{*}}\left(\Omega^{n} \Sigma^{n+k} X, Y_{k}\right) \simeq \operatorname{Map}_{\mathcal{A} \mathrm{n}_{*}}\left(\operatorname{colim} \Omega^{n} \Sigma^{n+k} X, Y_{k}\right) \simeq \operatorname{Map}_{\mathcal{A} \mathrm{n}_{*}}\left(Q \Sigma^{k} X, Y_{k}\right)
$$

Taking a subsequent limit in the horizontal $\Omega$-direction yields the mapping anima

$$
\lim \operatorname{Map}_{\mathcal{A} \mathrm{n}_{*}}\left(Q \Sigma^{k} X, Y_{k}\right) \simeq \operatorname{Map}_{\mathcal{A} \mathrm{n}_{*}}\left(\Sigma^{\infty} X, Y\right)
$$

[^0]
[^0]:    ${ }^{3}$ To be honest, we only saw in Topology I that mapping telescopes, so homotopy colimits in topological spaces indexed by the natural numbers as a poset, commute with homotopy groups. However, in our proof of Pr.2.1.10, as well as a future uses in Pr.2.1.17 and the application of Lm.2.1.33 to prove Pr.2.1.32, we will only use colimits of shape $\mathbf{N}$.

from the definition of $\Sigma^{\infty}$ and the expression for the mapping animæ of spectra. Also notice that the projection from this limit to the lower-right corner of the above diagram is precisely the desired map (2.1.12) which we want to show is an equivalence. This projection map is an equivalence though, which can be easily seen from the facts that the diagonal maps are equivalences, a consequence of the suspension-loop adjunction on pointed animæ, and that these diagonal maps define a cofinal subdiagram of the above.

Exercise 2.1.13. Show that the assignments $Q: \mathscr{A} \mathrm{n}_{*} \rightarrow \mathscr{A} \mathrm{n}_{*}$ and $\Sigma^{\infty}: \mathscr{A} \mathrm{n}_{*} \rightarrow \mathrm{Sp}$ as defined above do in fact yield functors of $\infty$-categories.(Hint: use the universal property of a limit.)
Exercise 2.1.14. Show that the functor $Q: \mathscr{A} \mathrm{n}_{*} \rightarrow \mathscr{A} \mathrm{n}_{*}$ preserves the zero object and sends pushout squares to pullback squares. We call such functors linear functors due to their appearance in Goodwillie's calculus of functors; see [Goo90].

To help us with some proofs coming up, we would like to know that each spectrum can be written as a filtered colimit of suspension spectra-for a moment, we will assume that filtered colimits of spectra exist, which will be proven in the first half of Pr.2.1.17.

Proposition 2.1.15. Let $X$ be a spectrum. Then there is a natural equivalence of spectra

$$
\operatorname{colim}_{n}\left(\left(\Sigma^{\infty} X_{n}\right)[-n]\right) \xrightarrow{\simeq} X
$$

from the standard presentation of $X$-the maps in the colimit above are given level-wise by the composite
$\left(\Sigma^{\infty} X_{n}\right)[-n]_{k}=\left(\Sigma^{\infty} X\right)_{k-n}=Q \Sigma^{k-n} X_{n} \simeq Q \Sigma^{k-n} \Omega X_{n+1} \xrightarrow{\varepsilon} Q \Sigma^{k-n-1} X_{n+1}=\left(\Sigma^{\infty} X_{n+1}\right)[-n-1]_{k}$ where $\varepsilon$ is the counit of the suspension-loop adjunction on $\mathcal{A} \mathrm{n}_{*}$.

To prove this proposition, and many others to come, we will use the $\infty$-categorical Yoneda lemma: let $K$ be a simplicial set and set $\Pi$ to be the simplicial category $\mathfrak{C}[K]$, which we define as the colimit

$$
\mathfrak{C}[K]=\operatorname{colim}_{\Delta^{n} \rightarrow K} \mathfrak{C}\left[\Delta^{n}\right]
$$

We then obtain a simplicial functor $\Pi^{\mathrm{op}} \times \Pi \rightarrow$ Kan by sending $(X, Y)$ to the Kan complex Sing $|\mathfrak{C}[K](X, Y)|$-we don't want to do a straight-up sSet-enriched Yoneda functor, as this functions up to isomorphism rather than homotopy equivalence, and $\mathrm{sSet}^{\Pi \mathrm{op}}$ is not generally a correct model for the $\infty$-category of functors from $\Pi^{\mathrm{op}}$ to $\mathcal{A} \mathrm{n}$. Precomposing the functor above with the natural comparison functor $\mathfrak{C}\left[K^{\mathrm{op}} \times K\right] \rightarrow \Pi^{\mathrm{op}} \times \Pi$ then yields a map of simplicial sets $K^{\mathrm{op}} \times K \rightarrow \mathcal{A} \mathrm{n}$ by adjunction, and then $\mathcal{L}: K \rightarrow \operatorname{Fun}\left(K^{\mathrm{op}}, \mathcal{A} \mathrm{n}\right)$ by another adjunction.

Theorem 2.1.16 ( $\infty$-categorical Yoneda lemma). Let $K$ be a simplicial set. Then the functor $\mathcal{L}: K \rightarrow \operatorname{Fun}\left(K^{\mathrm{op}}, \mathcal{A} \mathrm{n}\right)$ is fully faithful.

A proof can be found in [Lur09b, Pr.5.1.3.1] or [Lurb, Tag 03LZ]

Proof. By the Yoneda lemma Th.2.1.16, it suffices to show there is a natural equivalence between both of the functors represented by these spectra. Consider the natural equivalences of mapping animæ

$$
\begin{aligned}
& \operatorname{Map}_{\mathrm{Sp}}\left(\operatorname{colim}\left(\Sigma^{\infty} X_{n}\right)[-n], Y\right) \simeq \lim \operatorname{Map}_{\mathrm{Sp}}\left(\left(\Sigma^{\infty} X_{n}\right)[-n], Y\right) \simeq \lim \operatorname{Map}_{\mathrm{Sp}}\left(\Sigma^{\infty} X_{n}, Y[n]\right) \\
& \quad \simeq \lim \operatorname{Map}_{\mathcal{A}_{\mathrm{n}_{\star}}}\left(X_{n}, \Omega^{\infty} Y[n]\right) \simeq \lim \operatorname{Map}_{\mathcal{A}_{\mathrm{n}_{\star}}}\left(X_{n}, Y_{n}\right) \simeq \operatorname{Map}_{\mathrm{Sp}}(X, Y)
\end{aligned}
$$

where the first equivalence comes from the universal property of colimits, the second from the fact that $\Sigma^{-n}$ has natural inverse equivalence $\Sigma^{n}$ by definition, the third from the suspension spectrum adjunction of Pr.2.1.10, the forth from the natural equivalence $\Omega^{\infty} Y[n] \simeq Y_{n}$, and finally the fifth from the expression for the mapping animæ in Sp from its definition as a limit. The only natural equivalence up for debate is the forth one, but this follows from the definition of Sp and Exc.2.1.8.

End of lecture 7 and week 4

This standard presentation helps us with some formal arguments.
Proposition 2.1.17. The $\infty$-category Sp has all limit and colimits.
Proof. Suppose we have a diagram $p: K \rightarrow \mathrm{Sp}$ which we want to take the limit or the colimit of. Writing $p(k)$ for the spectrum given by the image of $k \in K$, then we claim that $X=$ $\left\{\lim p(k)_{n}\right\}_{n \geqslant 0}$ defines a spectrum and is the desired limit. To define its structure maps, we consider the composite

$$
X_{n}=\lim p(k)_{n} \simeq \lim \Omega p(k)_{n+1} \simeq \Omega \lim p(k)_{n+1}
$$

using the facts that each $p(k)$ is a spectrum and that limits commute with limits; this is Exc.1.8.25. To see this is the desired limit, we again appeal to Exc.1.8.25 and our knowledge of the mapping animæ between spectra
$\operatorname{Map}_{\mathrm{Sp}}(Y, X)=\lim \operatorname{Map}_{\mathcal{A}_{\mathrm{n}_{\star}}}\left(Y_{n}, \lim p(k)_{n}\right) \simeq \lim \lim \operatorname{Map}_{\mathcal{A}_{\mathrm{n}_{\star}}}\left(Y_{n}, p(k)_{n}\right) \simeq \lim \operatorname{Map}_{\mathcal{A}_{\mathrm{n}_{\star}}}(Y, p(k)) ;$
this simultaneously constructs a cone structure for $X$ too!

For filtered colimits, we can mimic the above argument, using the fact that $\Omega$ commutes with filtered colimits; see Clm.2.1.11. For general colimits, say given a diagram $p: K \rightarrow \mathrm{Sp}$, we claim that the spectrum

$$
X=\operatorname{colim}_{n}\left(\Sigma^{\infty} \operatorname{colim}_{k \in K} p(k)_{n}\right)[-n]
$$

is a colimit for $p$. Indeed, it exists as Sp has filtered colimits and $\mathcal{A} \mathrm{n}_{\star}$ has all colimits. Moreover, writing all of the spectra $p(k)$ in their standard presentation of Pr.2.1.15 allows us see that $X$ is a cocone for $p$. To see $X$ has the correct universal property, we observe the natural equivalences of animæ for any spectrum $Y$

$$
\operatorname{Map}_{\mathrm{Sp}}(X, Y) \simeq \lim _{n} \operatorname{Map}_{\mathrm{Sp}}\left(\left(\Sigma^{\infty} \operatorname{colim}_{k \in K} p(k)_{n}\right)[-n], Y\right) \simeq \lim _{n} \lim _{k \in K} \operatorname{Map}_{\mathrm{Sp}}\left(\Sigma^{\infty} p(k)_{n}, Y[n]\right)
$$

$$
\simeq \lim _{n, k \in K} \operatorname{Map}_{\mathrm{Sp}}\left(\left(\Sigma^{\infty} p(k)_{n}\right)[-n], Y\right) \simeq \lim _{k \in K} \operatorname{Map}_{\mathrm{Sp}}(p(k), Y)
$$

and we are done.
Let us now study these limits and colimits inside Sp. In fact, we want show that Sp is a stable $\infty$-category.

Theorem 2.1.18 (Stability). The $\infty$-category Sp is stable, meaning that Sp has a zero object, Sp has finite limits and colimits, and a commutative square of spectra is a pushout if and only if it is a pullback.

Remark 2.1.19. Stable $\infty$-categories have many pleasant features, including the fact that their homotopy categories naturally come equipped with the structure of triangulated category.

Proof of Th.2.1.18. First, let's discuss the zero object. Let 0 be the spectrum defined by the sequence of animæ $(*, *, *, \ldots)$. This clearly defines a spectrum, because $\Omega(*)$ is contractible, hence there is a unique (up to contractible choice) equivalence $\Omega(*)\simeq *$. Notice that for any other spectrum $X$, we have

$$
\operatorname{Map}_{\mathrm{Sp}}(0, X) \simeq \lim \operatorname{Map}_{\mathscr{I}_{n_{*}}}\left(*, X_{n}\right) \simeq \lim * \simeq *
$$

as $*$ is an initial object in the category of based animæ. In particular, 0 is the initial object of Sp. A similar calculation shows that 0 is also the terminal object in the $\infty$-category Sp. By definition, 0 is a zero object in Sp , meaning it is both initial and terminal. ${ }^{4}$

It remains to show that given a commutative diagram of spectra
![img-48.jpeg](img-48.jpeg)
then this square is a pullback if and only if it is a pushout. Let's first assume that the above square is a pushout. Then we can continue taking pushouts to obtain the expanded commutative diagram of spectra
![img-49.jpeg](img-49.jpeg)

[^0]
[^0]:    ${ }^{4}$ This implies that the mapping anima $\operatorname{Map}_{\mathrm{Sp}}(X, Y)$ are naturally pointed anima, as there is always an essentially unique map of spectra $0: X \rightarrow Y$ given as the composite $X \rightarrow 0 \rightarrow Y$. We call this the zero map.

where we have used the pasting law, which we revisit below Exc.2.1.21, a few times. There is a natural map $W \rightarrow X \times_{Z} Y$ which we want to show is an equivalence, and the above diagram shows that there is a maps between the limits of various subdiagrams. For example, the map $W \rightarrow W[1][-1]$ comes from the universal property of the square with corners $W, 0,0$, and $W[1]$, and similarly for $j$. This induces the commutative diagram of spectra
![img-50.jpeg](img-50.jpeg)
where the vertical maps are induced by the unit maps for the suspension-loop adjunction. These vertical maps are equivalences by Cor.2.1.7, and the rest follows. Indeed, to see our desired map $f$ is an equivalence, it suffices to see that $j$ is an equivalence. We claim that the inverse to $j$ is $f \circ h^{-1}$, which we check to be a left and right inverse inside h Sp explicitly:

$$
j \circ\left(f \circ h^{-1}\right) \simeq h \circ h^{-1} \simeq \operatorname{id}_{W[1][-1]} \quad\left(f \circ h^{-1}\right) \circ j \simeq\left(i^{-1} \circ g\right) \circ j \simeq i^{-1} \circ i \simeq \operatorname{id}_{X \times Y}
$$

This shows that a pushout is necessarily a pullback. The converse is similar, but dual, expanding (2.1.20) into a larger diagram with a series of pullbacks, et cetera.

Exercise 2.1.21. Prove the pasting law for pushouts: given a commutative diagram in an $\infty$-category $C$ of the form
![img-51.jpeg](img-51.jpeg)
where the left square is a pushout, then the right square is a pushout if and only if the whole rectangle is a pushout. If the reader enjoyed this, formulate and prove the dual statement for pullbacks.
Exercise 2.1.22. Let $C$ be an $\infty$-category with finite limits and colimits, all filtered colimits, and such that the functor $\Omega: C_{*} \rightarrow C_{*}$ commutes with filtered colimits. Show that the limit of $\infty$-categories

$$
\operatorname{Sp}(C)=\lim \left(\cdots \xrightarrow{\Omega} C_{*} \xrightarrow{\Omega} C_{*} \xrightarrow{\Omega} C_{*}\right)
$$

is stable, in the sense of Th.2.1.18. Show that if $C$ is stable, then the natural map $\Omega^{\infty}: \operatorname{Sp}(C) \rightarrow$ $C$ is an equivalence of $\infty$-categories.
Exercise 2.1.23. Show that if $K$ is a simplicial set and $C$ is an $\infty$-category, then there is a natural functor

$$
\operatorname{Fun}(K, \operatorname{Sp}(C)) \xrightarrow{\simeq} \operatorname{Sp} \operatorname{Fun}(K, C)
$$

which is an equivalence.
There are many lovely formal consequences of stability. First, the preadditivity of Sp.

Corollary 2.1.24. Given two spectra $X, Y$, then the natural map

$$
X \sqcup Y \xrightarrow{\simeq} X \times Y
$$

is an equivalence. In particular, we will now write $X \oplus Y$ for the direct sum of spectra.
Remark 2.1.25. Using the direct sum, we immediately see that the mapping animæ of spectra have a monoid structure

$$
\operatorname{Map}_{\mathrm{Sp}}(X, Y) \times \operatorname{Map}_{\mathrm{Sp}}(X, Y) \stackrel{\oplus}{\simeq} \operatorname{Map}_{\mathrm{Sp}}(X \oplus X, Y \oplus Y) \rightarrow \operatorname{Map}_{\mathrm{Sp}}(X, Y)
$$

where the last map is simultaneous precomposition with the diagonal map $X \rightarrow X \times X$ and postcomposition with the fold map $Y \sqcup Y \rightarrow Y$.
Remark 2.1.26. There is also a $[-1]$-map of spectra, as the sphere $\mathbf{S}$ has such an involutionusing the isomorphism $\pi_{0} \mathbf{S} \simeq \mathbf{Z}$ where the identity $\mathbf{S} \rightarrow \mathbf{S}$ hits 1 , this $[-1]$-map is simply the endomorphism of $\mathbf{S}$ corresponding to $-1 \in \mathbf{Z}$.

Proof of Cor.2.1.24. Taking the product of the pullback squares of spectra
![img-52.jpeg](img-52.jpeg)
yields the pullback square
![img-53.jpeg](img-53.jpeg)

By Th.2.1.18, this square is not only a pullback but also a pushout, meaning the natural map $X \sqcup Y \rightarrow X \times Y$ is an equivalence, and we are done.

Now to fibres and cofibres.
Definition 2.1.27. Let $f: X \rightarrow Y$ be a map of spectra. Define $F f$ (resp. $C f$ ), the fibre (resp. cofibre) of $f$, as the limit (resp. colimit) of the diagram of spectra

$$
X \xrightarrow[0]{f} Y
$$

A diagram of spectra of the form

$$
X \xrightarrow{f} Y \xrightarrow{g} Z
$$

equipped with a null homotopy $g f \simeq 0$ is a fibre sequence (resp. cofibre sequence) if the natural map $X \rightarrow F f$ (resp. $C f \rightarrow Z$ ) induced up the null homotopy is an equivalence.

We have seen (homotopy) fibres and cofibres of pointed animæ in Topology I and II, and they behaves very differently in this context. For example, a cofibre sequence of pointed animæ induces a long exact sequence on homology groups, but not homotopy groups: try $S^{1} \rightarrow * \rightarrow S^{2}$, for example. Conversely, a fibre sequence of pointed animæ induces a long exact sequence on homotopy groups but not homology groups; the latter problem is exactly why the Serre spectral sequence of Algebraic Topology I is interesting.

In the category of spectra, the natural map between the fibre and the cofibre is actually an equivalence.

Corollary 2.1.28. Let $f: X \rightarrow Y$ be a map of spectra. Then there is a natural equivalence of spectra

$$
F f[1] \simeq C f
$$

Proof. Consider the diagram of spectra
![img-54.jpeg](img-54.jpeg)

The left-hand square is a pullback by definition and the right-hand square is a pushout by definition. According to Th.2.1.18 and the pasting law (Exc.2.1.21), all squares and rectangles in the above diagram are pushouts and pullbacks, which immediately gives the desired result.

Stable $\infty$-categories have many great properties. In particular, one can often define their homotopy groups, and these groups behave much more like a homology theory than the homotopy groups of animæ; see Prs.2.1.31, 2.1.32 and 2.1.35.

Definition 2.1.29. Let $X$ be a spectrum and $n$ an integer. We define $\pi_{n} X$, the $n$th homotopy group of $X$ as the set

$$
\pi_{n} X=\pi_{0} \operatorname{Map}_{\mathrm{Sp}}\left(\mathbf{S}^{n}, X\right)
$$

where $\mathbf{S}^{n}=\mathbf{S}[n]$ and $\mathbf{S}=\Sigma^{\infty} S^{0}$ is called the sphere spectrum. This set has a natural abelian group structure which can be seen using the natural bijection

$$
\pi_{n} X=\pi_{0} \operatorname{Map}_{\mathrm{Sp}}\left(\mathbf{S}^{n}, X\right) \simeq \pi_{0} \operatorname{Map}_{\mathrm{Sp}}\left(\mathbf{S}[2], X[-n+2]\right) \simeq \pi_{0} \operatorname{Map}_{\mathcal{A}_{n_{*}}}\left(S^{2}, \Omega^{\infty} X[-n+2]\right)
$$

which is $\pi_{2}$ of the pointed anima $\Omega^{\infty} X[-n+2]$.
Exercise 2.1.30. Show this definition of homotopy groups is the same as the one seen in Topology II, so a colimit of homotopy groups of the animæ $X_{n}$ of a spectrum $X$ along the structure maps.

We can now prove that the homotopy groups of spectra satisfy the Eilenberg-Steenrod axioms of a homology theory. First, the suspension isomorphism.

Proposition 2.1.31 (Suspension isomorphism). Let $X$ be a spectrum. Then there is a natural isomorphism $\pi_{n} X \simeq \pi_{n+1} X[n+1]$ for all integers $n$.

Proof. This follows straight from our definition of $\pi_{n}$, as well as there are natural equivalences

$$
\pi_{n} X=\pi_{0} \operatorname{Map}_{\mathrm{Sp}}\left(\mathbf{S}^{n}, X\right) \simeq \pi_{0} \operatorname{Map}_{\mathrm{Sp}}\left(\mathbf{S}^{n+1_{i}} X[1]\right)=\pi_{n+1} X[1]
$$

using that [1]: $\mathrm{Sp} \rightarrow \mathrm{Sp}$ is an equivalence; see Cor.2.1.7.
The direct sum axiom is also immediate, however, we will need a lemma about filtered colimits as well.

Proposition 2.1.32 (Direct sum axiom). Let $\left\{X_{i}\right\}$ be a collection of spectra indexed on a set $I$ and write $X_{\sqcup}$ for its coproduct and $X_{\Pi}$ for its product. Then the natural maps of abelian groups

$$
\bigoplus_{I} \pi_{n} X_{i} \xrightarrow{\simeq} \pi_{n} X_{\sqcup} \quad \pi_{n} X_{\Pi} \rightarrow \prod_{I} \pi_{n} X_{i}
$$

are isomorphisms for all integers $n$.
Lemma 2.1.33. Let $X_{i}$ be a filtered diagram of spectra and write $X$ for its colimit. Then the natural map

$$
\operatorname{colim} \pi_{n} X_{i} \xrightarrow{\simeq} \pi_{n} X
$$

is an isomorphism for all integers $n$.
Proof. Again, this follows from the definition of homotopy groups and this fact for animæ:

$$
\begin{aligned}
\operatorname{colim} \pi_{n} X_{i} \simeq \operatorname{colim} & \pi_{0} \operatorname{Map}_{\mathrm{Sp}}\left(\mathbf{S}, X_{i}[-n]\right) \simeq \operatorname{colim} \pi_{0} \operatorname{Map}_{\mathcal{A}_{\mathrm{In}_{\Phi}}}\left(S^{0}, \Omega^{\infty} X_{i}[-n]\right) \\
& \simeq \pi_{0} \operatorname{Map}_{\mathcal{A}_{\mathrm{In}_{\Phi}}}\left(S^{0}, \Omega^{\infty} X[-n]\right) \simeq \pi_{n} X
\end{aligned}
$$

Proof of Pr.2.1.32. The expression for products immediately from the universal property of limits and the fact that homotopy groups of animæ commute with products. For coproducts, we first note that if $I$ is finite, then the result for products, Cor.2.1.24, and the fact that finite products and coproducts of abelian groups agree yield the desired result. If $I$ is infinite, then we write $I$ as a filtered colimit of finite subsets, and hence write $X_{\sqcup}$ as a filtered colimit of finite sums of spectra, and the result follows from Lm.2.1.33.

Exercise 2.1.34. Let $X$ be a spectrum and $n$ a positive integer. Show that the $n$-fold addition map on $X$, defined as the composite

$$
n: X \xrightarrow{\Delta} X^{\times n} \stackrel{\simeq}{\leftarrow} X^{\sqcup n} \xrightarrow{\nabla} X
$$

induces the $n$-fold addition map on all homotopy groups.
Finally, the exactness axiom.

Proposition 2.1.35 (Exactness axiom). Let $X \rightarrow Y \rightarrow Z$ be a fibre or a cofibre sequence of spectra. Then the diagram of abelian groups

$$
\cdots \rightarrow \pi_{n} X \rightarrow \pi_{n} \rightarrow \pi_{n} Z \rightarrow \pi_{n} X[1] \simeq \pi_{n-1} X \rightarrow \pi_{n-1} Y \rightarrow \cdots
$$

is exact for all integers $n$.
Proof. Again, the follows from the fact that fibre sequences of animæ yield long exact sequences on homotopy groups and Cor.2.1.28.

# End of lecture 8 

### 2.2 Examples of spectra

Now that we have the category Sp and many of its basic properties, let's start working with some examples of spectra.
Example 2.2.1. We have already mentioned an important spectrum, the sphere $\mathbf{S}=\Sigma^{\infty} S^{0}$ in Df.2.1.29. The homotopy groups of $\mathbf{S}$ are called the stable homotopy groups of sphere. If $n \geqslant 0$, then we have a natural equivalence

$$
\mathbf{S}^{n}=\Sigma^{n} \mathbf{S}=\Sigma^{n} \Sigma^{\infty} S^{0} \simeq \Sigma^{\infty} \Sigma^{n} S^{0} \simeq \Sigma^{\infty} S^{n}
$$

from the fact that $\Sigma^{\infty}$ is a left adjoint (Pr.2.1.10), so it commutes with colimits.
Exercise 2.2.2. Show that $\pi_{n} \mathbf{S} \simeq \operatorname{colim} \pi_{n+k} S^{k}$ for $n \geqslant 0$. Show that $\pi_{n} \mathbf{S}=0$ for $n<0$.
Exercise 2.2.3. Show that $\mathbf{S}$ corepresents the functor $\Omega^{\infty}$.
Example 2.2.4. Let $X$ be a based anima. In Pr.2.1.10, we defined the suspension spectrum of $X$, denoted by $\Sigma^{\infty} X$. We can apply many of the arguments used when discussing $\mathbf{S}$ for a more general $\Sigma^{\infty} X$. For example, we can quickly calculate that $\pi_{n} \Sigma^{\infty} X$ vanishes for negative $n$ and is otherwise isomorphic to the colimit

$$
\pi_{n} \Sigma^{\infty} X \simeq \operatorname{colim} \pi_{n+k} \Sigma^{k} X \quad n \geqslant 0
$$

If $X$ is an anima, without a chosen base point, then we write $\Sigma_{+}^{\infty} X$ for the image of $X$ under the composition

$$
\mathscr{A}_{\mathrm{n}} \xrightarrow{(-)_{+}} \mathscr{A}_{\mathrm{n}_{*}} \xrightarrow{\Sigma^{\infty}} \mathrm{Sp}
$$

the first functor adding a disjoint base-point, the left adjoint to the forgetful functor $\mathscr{A}_{\mathrm{n}_{*}} \rightarrow$ $\mathcal{A}_{\mathrm{n}}$.
Exercise 2.2.5. Let $X$ be a pointed anima. Show that $\pi_{n} \Sigma^{\infty} X \simeq \operatorname{colim} \pi_{n+k} \Sigma^{k} X$ for $n \geqslant 0$. Show that $\pi_{n} \Sigma^{\infty} X=0$ for $n<0$.
Exercise 2.2.6 (Cellular approximation). Show that any connective spectrum $X$, so a spectrum with $\pi_{n} X=0$ for $n<0$, can be written as a filtered colimit of suspension spectra. More generally, show that any connective spectrum can be constructed from $\mathbf{S}$ using filtered colimits, direct sums, and cofibres. Even more generally, show that Sp is generated under filtered colimits, direct sums, and cofibres by $\mathbf{S}^{n}$ for all integers $n$.

This form of cellular approximation is wildly useful when studying Sp.
Theorem 2.2.7 (Whitehead theorem for spectra). Let $f: X \rightarrow Y$ be a morphism of spectra. Then $f$ is an equivalence if and only if the induced map on $\pi_{n}$ is an isomorphism for every integer $n$.

Proof. Clearly, if $f$ is an equivalence then it induces an isomorphism on homotopy groups. Conversely, if $f$ induces an isomorphism on all homotopy groups, then for each $Z=\mathbf{S}[n]$ the natural map of pointed animæ

$$
\operatorname{Map}_{\mathrm{Sp}}(Z, X) \rightarrow \operatorname{Map}_{\mathrm{Sp}}(Z, Y)
$$

is an equivalence, as taking homotopy groups yields the desired homotopy groups of spectra. Indeed, our assumption is that (2.2.8) induces an equivalence on $\pi_{0}$ for all $\mathbf{Z}=\mathbf{S}[n]$ for every $n \in \mathbf{Z}$, which under the natural identifications

$$
\begin{aligned}
& \pi_{k} \operatorname{Map}_{\mathrm{Sp}}(\mathbf{S}[n], W) \simeq \pi_{0} \operatorname{Map}_{\mathcal{A} n_{*}}\left(S^{k}, \operatorname{Map}_{\mathrm{Sp}}(\mathbf{S}, W[-n]\right) \\
& \simeq \pi_{0} \operatorname{Map}_{\mathcal{A} n_{*}}\left(S^{k}, \Omega^{\infty} W[-n]\right) \simeq \pi_{0} \operatorname{Map}_{\mathrm{Sp}}(\mathbf{S}[k+n], W)
\end{aligned}
$$

for any $k \in \mathbf{Z}$, using Exc.2.2.3. This shows that (2.2.8) is an equivalence of animæ. The $\infty$-subcategory of Sp spanned by those $Z$ such that (2.2.8) is an equivalence now contains all shifts of the sphere spectrum. Moreover, this $\infty$-subcategory is closed under colimits too from the universal property of a colimit. By the third part of Exc.2.2.6, we then see that this $\infty$-subcategory is in fact all of Sp. The desired the result now follows by the Yoneda lemma. Alternatively, one can set $Z=X$ and $Z=Y$ to find an inverse to $f$ and show it is an inverse.

The process in Eg.2.2.4 is a specific case of a general spectrification procedure, which we quickly discuss now as an exercise.
Exercise 2.2.9. A prespectrum $X$ is a sequence of pointed animæ $\left\{X_{n}\right\}$ together with structure maps $\sigma_{n}: \Sigma X_{n} \rightarrow X_{n+1}$. In Topology II, we defined the homotopy groups of a prespectrum as the colimit

$$
\pi_{n} X=\operatorname{colim} \pi_{n+k} X_{k}
$$

for any integer $n$ and for $k \geqslant-n$. Given a prespectrum $X$, show that its spectrification $X^{\natural}$ defined as the colimit of spectra

$$
X^{\natural}=\operatorname{colim}\left(\Sigma^{\infty} X_{0} \simeq \Omega \Sigma \Sigma^{\infty} X_{0} \simeq \Omega \Sigma^{\infty} \Sigma X_{0} \xrightarrow{\Omega \Sigma^{\infty} \sigma_{0}} \Omega \Sigma^{\infty} X_{1} \rightarrow \Omega^{2} \Sigma^{\infty} X_{2} \rightarrow \cdots\right)
$$

has homotopy groups isomorphic to those of the prespectrum $X$. Also show that the suspension spectrum defined in Eg.2.2.4 is equivalent to the spectrification of the obvious suspension prespectrum of a pointed anima.
Remark 2.2.10. It is not too hard to write down an $\infty$-category of prespectra. Let $\mathbf{N}$ be the natural numbers, considered as a poset with the usual ordering. We then define the $\infty$ category of prespectra PreSp as the $\infty$-subcategory of $\operatorname{Fun}\left(\mathbf{N}^{2}, \mathcal{A} \mathrm{n}_{*}\right)$ given by those functors

$X$ such that $X(i, j)$ is contractible if $i \neq j$, where we suppress the nerve functor on $\mathbf{N}$ for typographical reasons. Actually, this is what we should call the $\infty$-category of preprespectra, as the objects are what we want, but the morphism animæ between objects in this $\infty$-category are incorrect - one reason we don't work with this model explicitly in these lectures. The objects of PreSp are a collection of animæ $\left\{X_{n}\right\}$ for $n \geqslant 0$ and an $\mathbf{N}^{2}$-shaped diagram of pointed animæ of the form
![img-55.jpeg](img-55.jpeg)

By making a cofinality argument, we see a prespectrum is a collection of animæ $\left\{X_{n}\right\}$ and the squares on the diagonal above, which from the universal property of a pushout are precisely a collection of maps of pointed animæ $\Sigma X_{n} \rightarrow X_{n+1}$. There is a functor $\operatorname{PreSp} \rightarrow$ Sp which we informally described by sending $\left\{X_{n}\right\}$ to the spectrum $Y$ with level-wise pointed animæ $Y_{n}=\operatorname{colim} \Omega^{i} X(i+n)$ - we leave it to the reader to show this collection of animæ is in fact a spectrum. Once we have localised PreSp to have the correct mapping animæ, then this functor $\operatorname{PreSp} \rightarrow$ Sp will be a left adjoint to a fully faithful functor $\mathrm{Sp} \rightarrow$ PreSp, which lines up with our intuition that "spectra are prespectra such that the adjoint structure maps are equivalences."
Remark 2.2.11. There are a few good reasons why we like prespectra, mostly due to a number of crucial examples: the suspension spectra of Eg.2.2.4 are a key connection between stable and unstable homotopy theory, and the Thom spectra of Egs.2.2.20 and 2.2.21 provide a link between the category of spectra and differential geometry. However, there are some significant drawbacks to prespectra. From a technical point of view, it is much more difficult to construct an $\infty$-category of prespectra than the $\infty$-category of spectra, as one needs to discuss lax colimits of $\infty$-categories to encode the structure morphisms correctly. From a practical point of view too, and this point has been known since the dawn of stable homotopy theory, see $\S 5$ of Boardman's PhD thesis [Boa64] or [Ada74, §III.2] for an accessible reference, that the correction notion of morphisms of prespectra are "eventual morphisms". For example, we know that the Hopf map $S^{3} \rightarrow S^{2}$ is stably nontrivial, this was proven in Topology II using Steenrod squares, so we expect it to represent an element in $\pi_{1} \mathbf{S}$, in particular, one might assume it ought to be represented by a map of prespectra $\Sigma^{\infty} S^{1} \rightarrow \Sigma^{\infty} S^{0}$. If a map of prespectra is a collection of level-wise maps, then the maps here in degrees 0 and 1 cannot be interesting at all: they are maps of pointed animæ $f_{0}: S^{1} \rightarrow S^{0}$ and $f_{1}: S^{2} \rightarrow S^{1}$, so both are null. However, in degree 2, the map should be the unstable Hopf map $f_{2}: S^{3} \rightarrow S^{2}$ and we would require a

diagram of animæ
![img-56.jpeg](img-56.jpeg)
to commute in some way. However, this diagram can never commute in $\mathrm{h} \mathcal{A} \mathrm{n}_{*}$, as one composite is null and the other not. This is why classically one sets morphisms of prespectra to be these "eventual morphisms", so a coherent collection of $f_{n}$ 's starting at some positive number $n$. This makes it very difficult to play with strict model categories of (pre)spectra, and there are obvious problems. For example, what if we have a sequence of such "eventual morphisms"

$$
X_{0} \xrightarrow{f_{0}} X_{1} \xrightarrow{f_{1}} X_{2} \xrightarrow{f_{2}} \cdots
$$

where $f_{i}$ is only defined after degree $i$ level-wise. Then what would the colimit of these morphisms be, and if so, would there exist an "eventual map" from $X_{0}$ into this colimit? Well, we don't have to worry about these things in our set-up, where all prespectra are converted into spectra. Phew.

Another, rather predicable class of spectra, are those which represent ordinary singular cohomology.
Example 2.2.12. Let $A$ be an abelian group. Then define the Eilenberg-Mac Lane spectrum, simply denoted as $A$, to have $n$th anima the Eilenberg-Mac Lane anima $K(A, n)$ and with structure maps the natural equivalences $\Omega K(A, n+1) \simeq K(A, n)$ as seen in Topology II. We leave it to the reader to calculate the homotopy groups of such spectra.
Exercise 2.2.13. Show that $\pi_{0} A \simeq A$ and that $\pi_{n} A$ vanishes for all nonzero $n$.
In fact, all such spectra with homotopy group concentrated in degree zero are of this type and also form a rather nice subcategory of Sp .

Theorem 2.2.14. Let $\mathrm{Sp}^{\bigcirc}$ denote the $\infty$-subcategory of Sp spanned by those spectra with homotopy groups concentrated in degree 0 . Then the functor $\pi_{0}: \mathrm{Sp}^{\bigcirc} \rightarrow \mathrm{Ab}$ is an equivalence of $\infty$-categories. In particular, $\mathrm{Sp}^{\bigcirc}$ is equivalent to the nerve of a 1-category!

To prove this theorem we need a quick lemma, which will be left as an exercise.
Exercise 2.2.15. Show that for each spectrum $X$ such that $\pi_{n} X=0$ for all $n \neq 0$, there is an equivalence between $X$ and the Eilenberg-Mac Lane spectrum for $\pi_{0} X$.

Proof of Th.2.2.14. The functor is essentially surjective as we know the existence of EilenbergMac Lane spectra from Eg.2.2.12. By Th.1.5.13, it then suffices to show fully faithfulness. This is straight forward using Exc.2.2.15 though as we have natural equivalences

$$
\operatorname{Map}_{\mathrm{Sp}}(A, B) \simeq \lim \operatorname{Map}_{\mathcal{A} n_{*}}(K(A, n), K(B, n)) \simeq \lim \operatorname{Ab}(A, B) \simeq \operatorname{Ab}(A, B)
$$

using the facts that we know mapping animæ between spectra, that $\operatorname{Map}_{\mathcal{A}_{\mathrm{n}_{\mathbf{B}}}}(K(A, n), K(B, n))$ is homotopy discrete and equivalent to the set of map $\mathrm{Ab}(A, B),{ }^{5}$ and that the final filtered limit is constant.

By shifting homotopy groups around, we obtain a version for each integer $n$.
Corollary 2.2.16. Fix an integer $n \in \mathbf{Z}$. The $\infty$-subcategory of spectra with homotopy groups concentrated in degree $n$ is equivalent to the nerve of the 1-category of abelian groups.

Exercise 2.2.17. Show that associated to every spectrum $X$ is a tower of spectra

$$
\cdots \rightarrow \tau_{\leqslant n+1} X \rightarrow \tau_{\leqslant n} X \rightarrow \tau_{\leqslant n-1} X \rightarrow \cdots
$$

under $X$, such that the map $X \rightarrow \tau_{\leqslant n} X$ induces an equivalence on $\pi_{i}$ for $i \leqslant n$ and otherwise $\pi_{i} \tau_{\leqslant n} X$ vanishes. Calculate the fibre of the maps $\tau_{\leqslant n} X \rightarrow \tau_{\leqslant n-1} X$. This is called the Postnikov tower associated to the spectrum $X$, and it turns out to be a functorial construction in $X$-if you know the adjoint functor theorem in higher category theory, see [Lur09b, Cor.5.5.2.9], try to prove this functoriality for yourself. Dually, show that associated to every spectrum $X$ is a tower of spectra

$$
\cdots \rightarrow \tau_{\geqslant n+1} X \rightarrow \tau_{\geqslant n} X \rightarrow \tau_{\geqslant n-1} X \rightarrow \cdots
$$

over $X$, such that the map $X \rightarrow \tau_{\geqslant n} X$ induces an equivalence on $\pi_{i}$ for $i \geqslant n$ and otherwise $\pi_{i} \tau_{\geqslant n} X$ vanishes. Calculate the fibre of the maps $\tau_{\geqslant n} X \rightarrow \tau_{\geqslant n-1} X$. This is called the Whitehead tower associated to the spectrum $X$. Again, if you have the higher categorical know-how, prove that this assignment is functorial in $X$.
Example 2.2.18. Recall that in Topology II we showed that every reduced cohomology theory $E^{*}(-)$ on based connected animæ is represented by an $\Omega$-spectrum $E$, then these also give us plenty of nice example of spectra.
Example 2.2.19. Associated to the cohomology theory of complex (resp. real) topological $K$ theory we have the spectrum KU (resp. KO). These can be constructed either using Brown representability, assuming we have constructed $K$-theory as a cohomology theory, or an $\Omega$ spectrum can be formed rather explicitly by setting $\mathrm{KU}_{2 n}=\mathbf{Z} \times \mathrm{BU}$ and $\mathrm{KU}_{2 n+1}=\mathrm{U}$ and appealing to the formal fact that $\Omega(\mathbf{Z} \times \mathrm{BU}) \simeq \mathrm{U}$ and the Bott periodicity equivalence $\Omega U \simeq$ $\mathbf{Z} \times \mathrm{BU}$; in the case of KO we need to use 8 -fold periodicity. The Brown representability method mentioned above is helpful to conclude that KU and KO are both homotopy commutative ring spectra, the multiplication "coming from" the tensor product of vector bundles. There is also

[^0]
[^0]:    ${ }^{5}$ This is only a slight extension of what we have seen from Topology II. Indeed, we know from Topology II that $\pi_{0} \operatorname{Map}_{\mathcal{A}_{\mathrm{n}_{\mathbf{B}}}}(K(A, n), K(B, n)) \simeq \mathrm{h} \mathcal{A}_{\mathrm{n}_{\mathbf{*}}}(K(A, n), K(B, n))$ is equivalent to maps of abelian groups from $A$ to $B$, so it suffices to calculate the higher homotopy groups. This is formal though, as we have isomorphisms

    $$
    \pi_{k} \operatorname{Map}_{\mathcal{A}_{\mathrm{n}_{\mathbf{B}}}}(K(A, n), K(B, n)) \simeq \mathrm{h} \mathcal{A}_{\mathrm{n}_{\mathbf{*}}}(K(A, n), K(B, n-k)) \simeq H^{n-k}(K(A, n) ; B)=0
    $$

    for positive $k$, where we used the suspension-loop adjunction, the identification $\Omega^{k} K(B, n) \simeq K(B, n-k)$, the representability of cohomology by Eilenberg-Mac Lane animæ, the universal coefficient theorem, and the Hurewicz theorem, all topics from Topology I and II. In particular, the natural map from the Postnikov tower gives an equivalence of animæ $\operatorname{Map}_{\mathcal{A}_{\mathrm{n}_{\mathbf{B}}}}(K(A, n), K(B, n)) \simeq \operatorname{Ab}(A, B)$.

a complexification map $c: \mathrm{KO} \rightarrow \mathrm{KU}$. One can also calculate the homotopy groups of KU as the integral ring of Laurent polynomails

$$
\pi_{*} \mathrm{KU} \simeq \mathbf{Z}\left[u^{ \pm}\right] \quad|u|=2
$$

This is actually fairly easy to see from the Bott periodicty theorem, see [Ati67, §2.2], but our definition of KU also immediately yields this answer, as least additively. Indeed, the homotopy groups are 2-periodic from Bott periodicity, so it suffices to make the calculations

$$
\pi_{0}(\mathbf{Z} \times \mathrm{BU}) \simeq \mathbf{Z} \times \pi_{0}(\mathrm{BU}) \simeq \mathbf{Z} \quad \pi_{1}(\mathbf{Z} \times \mathrm{BU}) \simeq \pi_{0} \mathrm{U}=0
$$

the last equivalence follows from the fact that every $\mathrm{U}(n)$ is path connected; we can diagonalise any unitary matrix by another unitary matrix, which gives us a path from any unitary matrix to the identity. Notice this argument doesn't work for $\mathrm{O}(n)$, which is why $\pi_{1} \mathrm{KO} \neq 0$. In fact, we have an isomorphism of rings

$$
\pi_{*} \mathrm{KO} \simeq \frac{\mathbf{Z}\left[\eta, \alpha, \beta^{ \pm}\right]}{\left(2 \eta, \eta^{3}, \eta \alpha, \alpha^{2}-4 \beta\right)} \quad|\eta|=1,|\alpha|=4,|\beta|=8
$$

where $\eta$ is the image of the stable Hopf map $\mathbf{S}[1] \rightarrow \mathbf{S}$ from $\pi_{1} \mathbf{S}, \alpha$ is mapped to $2 u^{2}$ in $\pi_{4} \mathrm{KU}$, and $\beta$ to $u^{4}$ in $\pi_{8} \mathrm{KU}$. Let us not get into this computation here. There are also explicit higher categorical constructions of topological $K$-theory, using spectral algebraic geometry or multiplicative $\infty$-loop space machines; see [Lur18, §6.5] for any outline of both constructions and an equivalence between them. These higher categorical constructions of KU and KO also make it clear that these spectra are $\mathbf{E}_{\infty}$-ring spectra.
Example 2.2.20. Let MO be the unoriented cobordism spectrum defined as follows. First, we set $T_{n}$ to be the Thom construction of the tautological $n$-dimensional vector bundle $\gamma_{n}$ over $\mathrm{BO}(n)$. As the pullback of $\gamma_{n+1}$ along the inclusion $\mathrm{BO}(n) \rightarrow \mathrm{BO}(n+1)$, induced by inserting a 1 in the bottom right corner of an orthogonal matrix, is the direct sum of $\gamma_{n}$ with a trivial line bundle, we obtain natural maps $\Sigma T_{n} \rightarrow T_{n+1}$ upon taking Thom constructions. We obtain a prespectrum as in Exc.2.2.9. We then set MO to be the spectrification of this prespectrum, a process defined in Exc.2.2.9. By construction, we have

$$
\pi_{k} \mathrm{MO}=\operatorname{colim} \pi_{k+n} T_{n}
$$

which were shown in Algebraic Topology I to be equivalent to the unoriented bordism group $\Omega_{k}^{O}$ for $k \geqslant 0$.
Example 2.2.21. A similar game can be play with $\mathrm{BU}(n)$ to produce the complex cobordism spectrum MU. Indeed, we still have the Thom construction $T_{n}$ of the universal $n$-dimensional complex vector bundles over $\mathrm{BU}(n)$. We then obtain a prespectrum $X$ indexed only on the even natural numbers, so $X_{2 n}=T_{n}$ with structure maps $\Sigma^{2} X_{2 n} \rightarrow X_{2 n+2}$, the doubling of degrees coming from the fact that a complex line bundle has real dimension 2. Using the basics of Exc.2.2.9, we can still spectrify this "doubled prespectrum" to obtain MU:

$$
\mathrm{MU}=\operatorname{colim}\left(\Sigma^{\infty} X_{0} \rightarrow \Omega^{2} \Sigma^{\infty} X_{2} \rightarrow \Omega^{4} \Sigma^{\infty} X_{4} \rightarrow \cdots\right)
$$

The homotopy groups of MU will be of much interest shortly; see $\S 3.3$.
Exercise 2.2.22. Show that MO and MU are connective.
It is worth pointing out that there is also a purely higher categorical approach to Thom spectra such as MO and MU. To outline the idea, one considers the functor of $\infty$-categories

$$
\mathrm{BO} \xrightarrow{J} \mathrm{BGL}_{1} \mathbf{S} \rightarrow \mathrm{Sp}
$$

and then MO is equivalent to the colimit of this functor. Above, the map $J$ is the $J$ homomorphism, $\mathrm{BGL}_{1} \mathbf{S}$ is a classifying space of a commutative monoid $\mathrm{GL}_{1} \mathbf{S}$ in animæ which itself is the submonoid of $\Omega^{\infty} \mathbf{S}$ spanned by the units, and the last functor recognises $\mathrm{BGL}_{1} \mathbf{S}$ as the $\infty$-subgroupoid of Sp spanned by line bundles over $\mathbf{S}$; see $\left[\mathrm{ABG}^{+} 14\right]$ for more details and discussion.

End of lecture 9 and week 5

# 2.3 Homology and cohomology 

To define homology and cohomology for general spectra $E$, we want to have a good tensor product between spectra and good mapping spectra. We will take a rather low-tech approach here; see [Lur17, §4.8.2] for the much stronger, but more complicated, statement.

First, we claim that any $\infty$-category $C$ with all small colimits is tensored over $\mathcal{A}$ n. This means that there is a functor $C \times \mathcal{A} \mathrm{n} \rightarrow C$ which preserves colimits in both variables. One can define this tensor as the adjoint to the left Kan extension of $* \rightarrow \operatorname{Fun}(C, C)$ defined by the identity, along the functor $* \rightarrow \mathcal{A}$ n which is the inclusion of the terminal object. We will write this as $X \boxtimes S$ for an object $X$ of $C$ and an anima $S$. The general formula for $X \boxtimes S$ is simply colim $\left(S \rightarrow * \xrightarrow{X} C\right)$, which falls right out of the left Kan extension description. As this functor preserves colimits in each variable, we immediately see that $X \boxtimes \varnothing$ is the initial object of $C$, for every $X$ in $C$, and the formula above shows that if $S \simeq *$ is contractible, then $X \boxtimes S \simeq X$. These examples are a bit trivial, but we can compute $X \boxtimes S$ now for any anima $S$ by writing $S$ as a colimit of $*$; see Exc.1.8.24.

We are more interested in the pointed case. If $C$ is a pointed $\infty$-category, meaning the natural map from the initial object to the terminal object is an equivalence, with all colimits, then we claim $C$ is naturally tensored over $\mathcal{A} \mathrm{n}_{*}$. This comes in the form of a functor $C \times \mathcal{A} \mathrm{n}_{*} \rightarrow$ $C$, and can be defined using the formula

$$
X \otimes S=\operatorname{cofib}\left(X \simeq X \boxtimes * \xrightarrow{\text { id } \boxtimes s_{0}} X \boxtimes S\right)
$$

where $s_{0}$ is the chosen point in $S$. We then see that $X \otimes * \simeq *$ is the initial/terminal object of $C$, and that $X \otimes S^{0} \simeq X$. By writing $S^{1}$ as the colimit of $* \leftarrow S^{0} \rightarrow *$ in $\mathcal{A} \mathrm{n}_{*}$, we see that $X \otimes S^{1}$ is the pushout of $* \leftarrow X \rightarrow *$, in other words, $X \otimes S^{1} \simeq \Sigma X$ is the suspension of $X$.

Iterating this, we see that $X \otimes S^{n} \simeq \Sigma^{n} X$.
If $C=\mathrm{Sp}$, we have $X \otimes S^{n} \simeq X[n]$ using our shift notation. This can be used to give us a really explicit model for any particular anima you might want to tensor a spectrum with. Let $S$ be a pointed anima with a given cellular filtration, meaning a sequence of animæ $S_{n} \rightarrow S_{n+1}$ for $n \geqslant 0$ together with pushout squares in pointed animæ
![img-57.jpeg](img-57.jpeg)
such that colim $S_{n}=S$. Of course, it helps if $\varphi_{0}$ is the identity. In this case we see that $X \otimes S$ can be written as a colimit of $X \otimes S_{n}$, and each of these levels can be obtained using a pushout
![img-58.jpeg](img-58.jpeg)
with $X \otimes S_{0}=\bigoplus_{i \in I_{0}} X$ if $\varphi_{0}=\mathrm{id}$. The map $\Phi_{n}$ is the stabilisation of the attaching map associated to $\varphi_{n}$, ie, the image of $\varphi_{n}$ under the map

$$
\pi_{0} \operatorname{Map}_{\mathcal{A} n_{*}}\left(\bigvee_{i \in I_{n}} S^{n}, S_{n}\right) \xrightarrow{\Sigma^{\infty}} \pi_{0} \operatorname{Map}_{\mathrm{Sp}}\left(\bigvee_{i \in I_{n}} \mathbf{S}[n], \Sigma^{\infty} S_{n}\right)
$$

In the language of the Topology II and Algebraic Topology I, this is just the inclusion of the colimit

$$
\left[\bigvee_{i \in I_{n}} S^{n}, S_{n}\right]_{*} \xrightarrow{\Sigma^{\infty}} \operatorname{colim}\left[\bigvee_{i \in I_{n}} S^{n+k}, \Sigma^{k} S_{n}\right]_{*}
$$

This process of taking the attaching map $\varphi_{n}$ and producing its associated stabilisation can simplify many computations.
Exercise 2.3.1. Find an example of a nontrivial map of pointed animæ $X \rightarrow Y$ whose stabilisation is zero. Hint: you know an example where $X$ and $Y$ are spheres!

Okay, so cocomplete $\infty$-categories are tensored over $\mathcal{A}$ n, pointed $\infty$-categories are tensored over $\mathcal{A} \mathrm{n}_{*}$, so you can only guess what stable $\infty$-categories are tensored over. First, we need a quick exercise.
Exercise 2.3.2. Let $C$ and $\mathscr{D}$ be two pointed $\infty$-categories with finite limits. Show there is a natural equivalence of $\infty$-categories

$$
\operatorname{Sp}(C \times \mathscr{D}) \xrightarrow{\simeq} \operatorname{Sp}(C) \times \operatorname{Sp}(\mathscr{D})
$$

Let $C$ be a stable $\infty$-category. We obtain a tensoring over Sp over $C$ by applying $\mathrm{Sp}(-)$ to the usual tensoring of $\mathcal{A} \mathrm{n}_{*}$ over $C$ and using Excs.2.1.22 and 2.3.2:

$$
\mathrm{Sp} \times C \simeq \mathrm{Sp}\left(\mathcal{A} \mathrm{n}_{*}\right) \times \mathrm{Sp}(C) \simeq \mathrm{Sp}\left(\mathcal{A} \mathrm{n}_{*} \times C\right) \rightarrow \mathrm{Sp}(C) \simeq C
$$

We will use the same notation $X \otimes S$ for this tensoring over spectra. In more concrete terms, we again point out that such a tensoring over Sp preserve colimits in each variable and satisfies $X \otimes \mathbf{S} \simeq X$. From this we see that $X \otimes \mathbf{S}[n] \simeq X[n]$ using the shift inside $C$ for $n \geqslant 0$, and from the associativity and unitality of this tensoring, we see that this holds for all $n \in \mathbf{Z}$. In particular, if we write a spectrum $S$ as a colimit of $\mathbf{S}[n]$ for various $n$ following Exc.2.2.6, we obtain a formula for $X \otimes S$ in terms of the attaching maps for $X$.
Remark 2.3.3. Notice that this tensoring over spectra behaves well with respect to $\Sigma^{\infty}$ : we would like to show that $X \otimes \Sigma^{\infty} S \simeq X \otimes S$, where the first operation is tensoring with a spectrum $\Sigma^{\infty} S$ and the second is tensoring with the pointed anima $S$. In other words, we would like the show that the diagram of $\infty$-categories
![img-59.jpeg](img-59.jpeg)
commutes, where $\Sigma_{C}^{\infty}$ is an equivalence as $C$ is stable. Notice that in both situations above, $X \otimes$ - has a right adjoint: upstairs, this is given by $\operatorname{Map}_{C}(X,-)$, and downstairs by $\left\{\operatorname{Map}_{C}(X[-n],-\right\}_{n}$. Indeed, to prove this adjunction, use that $\mathcal{A} \mathrm{n}_{*}$ is generated by $S^{0}$ under colimits. We now note that all of the functors in sight are right adjoints, and hence to show that the above square commutes, it suffices to show the diagram of $\infty$-categories
![img-60.jpeg](img-60.jpeg)
commutes. However, this is clear, as the $\Omega^{\infty}$ functors just evaluate the mapping spectrum on its zeroth anima, which is precisely the desired $\operatorname{Map}_{C}(X,-)$.

In particular, $C=\mathrm{Sp}$ is stable, so we obtain a tensoring of Sp over Sp gives us a "handicrafted" tensor product of spectra. Let us unpack the definition a little bit.

Definition 2.3.4. The tensoring of Sp over itself gives a tensor product of spectra. Inspired by the standard presentation of Pr.2.1.15, for spectra $X$ and $Y$, we notice that we can write $X \otimes Y$ as the colimit

$$
X \otimes Y \simeq \operatorname{colim}\left(X \otimes Y_{n}\right)[-n]
$$

where the maps $\left(X \otimes Y_{n}\right)[-n] \rightarrow\left(X \otimes Y_{n+1}\right)[-n-1]$ are induced by the adjoint structure maps $\Sigma Y_{n} \rightarrow Y_{n+1}$ for $Y$, as seen in Pr.2.1.15. Here we are using that the stable tensoring commutes with colimits in each variable.

Remark 2.3.5. Most importantly, notice that the tensor product of spectra as defined above has the characterising properties:

1. For a fixed spectrum $X$, the functor $X \otimes-\mathrm{Sp} \rightarrow \mathrm{Sp}$ preserves colimits; this is essentially by construction.
2. For two pointed animæ $X, Y$, the natural map $\Sigma^{\infty} X \otimes \Sigma^{\infty} Y \rightarrow \Sigma^{\infty}(X \wedge Y)$ is an equivalence; this is Rmk.2.3.3.

Exercise 2.3.6. Show that the above definition of $X \otimes Y$ is equivalent to the following colimit:

$$
\operatorname{colim}_{m, n \geqslant 0}\left(\Sigma^{\infty}\left(X_{n} \otimes Y_{m}\right)\right)[-n-m]
$$

Exercise 2.3.7. Let $n$ be an integer, $X$ be a spectrum, and $X / n$ be the cofibre of the multiplication-by- $n$ map $X \rightarrow X$. Show that there is a natural equivalence of spectra

$$
X \otimes \mathbf{S} / n \simeq X / n
$$

Proposition 2.3.8. Let $X, Y, Z$ be spectra. Then there are equivalences of spectra

$$
\mathbf{S} \otimes X \simeq X \simeq X \otimes \mathbf{S} \quad X \otimes Y \simeq Y \otimes X \quad X \otimes(Y \otimes Z) \simeq(X \otimes Y) \otimes Z
$$

Proof. For the commutativity, we simply look at the definitions, use the facts the colimits commute with the tensoring (by construction) as well as colimits, and the standard presentation of Pr.2.1.15:

$$
\begin{gathered}
X \otimes Y=\operatorname{colim}_{n} \Sigma^{-n} X \otimes Y_{n} \simeq \operatorname{colim}_{n} \Sigma^{-n}\left(\left(\operatorname{colim}_{m} \Sigma^{-m} \Sigma^{\infty} X_{m}\right) \otimes Y_{n}\right) \\
\simeq \operatorname{colim}_{n} \Sigma^{-n}\left(\operatorname{colim}_{m}\left(\left(\Sigma^{-m} \Sigma^{\infty} X_{m}\right) \otimes Y_{n}\right)\right) \simeq \operatorname{colim}_{n} \Sigma^{-n}\left(\operatorname{colim}_{m}\left(\Sigma^{-m} \Sigma^{\infty}\left(X_{m} \wedge Y_{n}\right)\right)\right) \\
\simeq \operatorname{colim}_{m, n} \Sigma^{-n-m} \Sigma^{\infty}\left(X_{m} \wedge Y_{n}\right)
\end{gathered}
$$

As this last term is symmetric in $m$ and $n$, using the symmetries on $\wedge$ in $\mathcal{A} \mathrm{n}_{s}$, obtain an equivalence $X \otimes Y \simeq Y \otimes X$ by undoing the above equivalences with the roles of $X$ and $Y$ now reversed. As we have this commutativity property for the tensor product of spectra, we are done after we show $\mathbf{S} \otimes X \simeq X$ :

$$
\mathbf{S} \otimes X=\operatorname{colim}_{n} \Sigma^{-n}\left(\Sigma^{\infty} S^{0} \otimes X_{n}\right) \simeq \operatorname{colim}_{n} \Sigma^{-n}\left(\Sigma^{\infty}\left(S^{0} \wedge X_{n}\right)\right) \simeq \operatorname{colim}_{n} \Sigma^{-n} \Sigma^{\infty} X_{n} \simeq X
$$

The associativity condition is the same but more arduous - we leave it to the reader, if they want some practice manipulating colimits.

One of the reasons for defining the tensor product of spectra is to define ring spectra, those objects which represent multiplicative cohomology theories.

Definition 2.3.9. A homotopy (commutative) ring spectrum is a spectrum $E$ together with two maps, a multiplicative map $\mu: E \otimes E \rightarrow E$ and unit map $\eta: \mathbf{S} \rightarrow E$, such that $E$ becomes a (commutative) monoid object in hSp , meaning that we only ask that there exist homotopies witnessing the unitality, and associtivity (and commutativity) of these maps
![img-61.jpeg](img-61.jpeg)
where $\tau$ is the map switching the two factors of $E \otimes E$, ie, the second equivalence of Pr.2.3.8.
Exercise 2.3.10. Show that for a commutative ring $R$, the Eilenberg-Mac Lane spectrum $R$ is a homotopy commutative ring spectra.
Remark 2.3.11. A few people asked for some details regarding the above exercise, which we want to give here. We claim that the Eilenberg-Mac Lane spectrum functor $\mathrm{Ab} \rightarrow \mathrm{h} \mathrm{Sp}$ is lax monoidal. Writing this functor as $H$, as is done traditionally, this means that there is a natural collection of maps (not necessarily isomorphisms!) $H A \otimes H B \rightarrow H(A \otimes B)$ and $\mathbf{S} \rightarrow H \mathbf{Z}$ demonstrating that although $H$ might not strictly preserve the monoidal structure in these categories and their units, there are maps between them. This lax monoidality of $H$ is easy to see from Th.2.3.28 to come; also see Exc.2.3.30. In particular, a commutative ring $R$, comes with a map of abelian groups $R \otimes R \rightarrow R$ defining its multiplication and a map $\mathbf{Z} \rightarrow R$ defining its unit. The lax monoidal structure on $H$ gives maps

$$
H R \otimes H R \rightarrow H(R \otimes R) \rightarrow H R \quad \mathbf{S} \rightarrow H \mathbf{Z} \rightarrow H R
$$

giving the $H R$ the structure of a homotopy commutative ring spectrum. In general, lax monoidal functors send (commutative) monoids to (commutative) monoids.
Exercise 2.3.12. Show that $\mathbf{S}$ is a homotopy commutative ring spectrum. More generally, show that for every commutative $H$-space $X$, the suspension spectrum $\Sigma_{+}^{\infty} X$ is a homotopy commutative ring spectrum.
Exercise 2.3.13. For a spectrum $X$ and an integer $n$, let us denote the cofibre of the multiplication by $n$ map $\cdot n: X \rightarrow X$ by $X / n$.

1. Show that for a prime $p$, the spectra $\mathbf{S} / p$ and $\mathbf{S}_{(p)} / p$ are equivalent, where $\mathbf{S}_{(p)}$ denotes the colimit

$$
\mathbf{S} \xrightarrow{p_{1}} \mathbf{S} \xrightarrow{p_{1} p_{2}} \mathbf{S} \xrightarrow{p_{1} p_{2} p_{3}} \mathbf{S} \xrightarrow{p_{1} p_{2} p_{3} p_{4}} \cdots
$$

where $p_{1}, p_{2}, p_{3}, \ldots$ is an enumeration of the collection of all primes different to $p$; we will come back to this in $\S 2.5$.
2. Show that $\mathbf{S} / 2$ cannot be given the structure of a homotopy ring spectrum with unit $\mathbf{S} \rightarrow \mathbf{S} / 2$ coming from the cofibre sequence defining $\mathbf{S} / 2$. For this, you may assume the calculations

$$
\pi_{0} \mathbf{S} \simeq \mathbf{Z}, \quad \pi_{1} \mathbf{S} \simeq \mathbf{Z} / 2 \mathbf{Z}, \quad \pi_{2} \mathbf{S} \simeq \mathbf{Z} / 2 \mathbf{Z}
$$

3. Show that $\mathbf{S} / p$ can be given the structure of a homotopy ring spectrum for all odd primes $p$, and that this is even commutative if $p \geqslant 5$. In this case, you may assume the fact that the first $p$-torsion in $\pi_{*} \mathbf{S}$ appears in degree $2 p-3$ as $\mathbf{Z} / p \mathbf{Z}$.
4. Show that for an odd prime $p$ and a spectrum $X$, the homotopy groups of $X / p$ have the structure of an $\mathbf{F}_{p}$-vector space.
Remark 2.3.14. As mentioned previously, the $\infty$-category Sp actually has the structure of a symmetric monoidal $\infty$-category-as described in [Lur17, §2]. To avoid a digression on operads and $\infty$-operads, we have decided to go with this low-tech approach to the tensor product of spectra, however, there is a lot more that one can do in higher algebra using $\infty$-operads than homotopy commutative ring spectra. The reader is invited to leaf through the introduction to [Lur17], especially the introduction to Chapter 2, if they're interested-we've collected our own summary of this in $\S 1.9$.

On a more historical point, the construction of Sp , even the 1-category SHC, with a symmetric monoidal product was a long and arduous journey for stable homotopy theorists. In [Ada74, p.139], Adams says "...the convenience of having available smash products of spectra is so great that I, for one, would hate to do without it." A handicrafted version of a smash product appears in ibid, and many tried to use the foundations of Quillen to construct a model category of spectra with a symmetric monoidal smash product. In the early 90's, Lewis [Lew91] showed that there is no symmetric monoidal model category of spectra with a decent enough smash product, and this seemed like an unapproachable problem. One of the biggest recent movements in stable homotopy theory was the discovery of some symmetric monoidal model categories of spectra, which of course relaxed some of the assumptions of Lewis; see [EKMM97] and [MMSS01]. The next overhaul of these ideas was due to Lurie's systematic approach to symmetric monoidal $\infty$-categories and $\infty$-operads. In particular, he shows that the $\infty$-category of spectra itself is the initial object in the $\infty$-category of stable presentable symmetric monoidal $\infty$-categories, hence any symmetric monoidal structure on it is necessarily unique (up to contractible choice); see [Lur17, §4.8.2].

Enough of that, let's now observe that Sp also houses a tensor-hom adjunction.
Construction 2.3.15. Let $X, Y$ be two spectra. The mapping spectrum from $X$ to $Y$, written as $Y^{X}$, is defined using the formula

$$
\left(Y^{X}\right)_{n}=\operatorname{Map}_{\mathrm{Sp}}(X, Y[n])
$$

where the structure maps are given by the composite

$$
\Omega\left(Y^{X}\right)_{n+1}=\Omega \operatorname{Map}_{\mathrm{Sp}}(X, Y[n+1]) \simeq \operatorname{Map}_{\mathrm{Sp}}(X, Y[n])=\left(Y^{X}\right)_{n}
$$

where we have (in order) used the universal property of suspension $\Omega$ in a pointed $\infty$-category and the equivalence of Cor.2.1.7. Notice that by construction $\Omega^{\infty} Y^{X}=\operatorname{Map}_{\mathrm{Sp}}(X, Y)$ returns the usual mapping anima of spectra.
Exercise 2.3.16. Show that the above definition is equivalent to the "level-wise" definition, meaning $\left(Y^{X}\right)_{n}=\operatorname{Map}_{\mathcal{A} n_{*}}\left(X_{n}, Y_{0}\right)$ with structure maps similarly defined using the structure maps of $X$.

Exercise 2.3.17. Given a fixed spectrum $E$, show that if $X \rightarrow Y \rightarrow C$ is a cofibre sequence of spectra, then the diagram of spectra $E^{C} \rightarrow E^{Y} \rightarrow E^{X}$ is naturally a (co)fibre sequence.
Exercise 2.3.18. Follow the outline around (0.0.1) and prove both a homological and a cohomology Thom isomorphism inside Sp. How might you extend this to coefficients in a spectrum $E$ ?

Proposition 2.3.19. Let $X, Y, Z$ be spectra. Then there is a natural equivalence of spectra

$$
\left(Z^{Y}\right)^{X} \simeq Z^{X \otimes Y}
$$

This is a kind of tensor-hom adjunction internal to the category of spectra.
Proof. On mapping animæ we have the natural equivalences

$$
\begin{gathered}
\operatorname{Map}_{\mathrm{Sp}}\left(X, Z^{Y}\right) \simeq \lim _{n} \operatorname{Map}_{\mathscr{A} n_{*}}\left(X_{n}, \operatorname{Map}_{\mathrm{Sp}}\left(\Omega^{n} Y, Z\right)\right) \\
\simeq \lim _{n} \operatorname{Map}_{\mathscr{A} n_{*}}\left(X_{n}, \lim _{m} \operatorname{Map}_{\mathscr{A} n_{*}}\left(Y_{m+n}, Z_{m}\right)\right) \simeq \lim _{m, n} \operatorname{Map}_{\mathscr{A} n_{*}}\left(X_{n}, \operatorname{Map}_{\mathscr{A} n_{*}}\left(Y_{m+n}, Z_{m}\right)\right) \\
\simeq \lim _{m, n} \operatorname{Map}_{\mathscr{A} n_{*}}\left(X_{n} \wedge Y_{m+n}, Z_{m}\right) \simeq \lim _{m, n} \operatorname{Map}_{\mathscr{A} n_{*}}\left(\left(X_{n} \otimes Y[-n]\right)_{m}, Z_{m}\right) \\
\lim _{n} \operatorname{Map}_{\mathrm{Sp}}\left(X_{n} \otimes Y[-n], Z\right) \simeq \operatorname{Map}_{\mathrm{Sp}}(X \otimes Y, Z)
\end{gathered}
$$

This proves the equivalence for mapping animæ, ie, a $\Omega^{\infty}$-version of the desired statement. To upgrade this, we simply iterate and use the Yoneda lemma:

$$
\operatorname{Map}_{\mathrm{Sp}}\left(W,\left(Z^{Y}\right)^{X}\right) \simeq \operatorname{Map}_{\mathrm{Sp}}\left(W \otimes X, Z^{Y}\right) \simeq \operatorname{Map}_{\mathrm{Sp}}(W \otimes X \otimes Y, Z) \simeq \operatorname{Map}_{\mathrm{Sp}}\left(W, Z^{X \otimes Y}\right)
$$

The tensor product and internal mapping spectra are $\infty$-categorical versions of homology and cohomology.

Definition 2.3.20. Let $E$ and $X$ be two spectra. We define the $E$-homology of $X$ as the (homologically) Z-graded group

$$
E_{*} X=\pi_{*}(E \otimes X)
$$

and the $E$-cohomology of $X$ as the (cohomologically) $\mathbf{Z}$-graded group

$$
E^{*} X=\pi_{-*} E^{X}
$$

If $X=\Sigma^{\infty} Y_{+}$is the suspension spectrum of an anima $Y$, we will also write $E_{*} X=E_{*} Y$ and $E^{*} X=E^{*} Y$. If $X=\Sigma^{\infty} Y$ for a based anima $Y$, note the lack of a disjoint base-point, then we write $E_{*} X=\widehat{E}_{*} Y$ and $E^{*} X=\widehat{E}^{*} Y$, as these are the reduced variants. More generally, but seldom used again, given a map of animæ $f: X \rightarrow Y$ with cofibre $C f$, we define $E_{*}(X, Y)=\widehat{E}_{*}(C f)$ and $E^{*}(X, Y)=\widehat{E}^{*}(C f)$.

We can unwind the cohomology definition a little: a class $x$ inside $E^{d} X$ is a map of spectra $\mathbf{S}^{-d} \rightarrow E^{X}$, or equivalently a map of spectra $X \rightarrow E[d]$.
Exercise 2.3.21. Show that if $E$ is a spectrum, $X=\Sigma_{+}^{\infty} Y$ the suspension of an anima $Y$, and $x$ a class inside $E^{d} X$ for $d \geqslant 0$, then $x$ can be represented by a map of animæ $Y \rightarrow E_{d}$.

Exercise 2.3.22. Show that if $E$ is a homotopy commutative ring spectrum, then $E^{*}\left(\Sigma_{+}^{x} X\right)$ is a homotopy commutative ring spectrum for all animæ $X$. In particular, taking homotopy groups gives us the ring structure on $E$-cohomology groups.

Proposition 2.3.23. There is a functor of 1 -categories

$$
\mathrm{h} \mathrm{Sp} \rightarrow \text { Cohom }
$$

from the stable homotopy category to the category of cohomology theories, sending a spectrum $E$ to the cohomology theory $E^{*}(-)$ defined by Df.2.3.20. The same holds for reduced cohomology theories and $\widetilde{E}^{*}(-)$.

Proof. This follows from the definitions together with Prs.2.1.31, 2.1.32 and 2.1.35.
Given an abelian group $A$ and an anima $X$, then we see that the definition of the $A$ cohomology of $X$ from Df.2.3.20 matches our definition from Topology II (via Brown representability):

$$
\begin{aligned}
\widetilde{A}^{*}(X)= & \pi_{-n}\left(A^{\Sigma^{x} X}\right) \simeq \pi_{0}\left(A^{\Sigma^{x} X}[n]\right) \simeq \pi_{0} \operatorname{Map}_{\mathrm{Sp}}\left(\Sigma^{x} X, A[n]\right) \\
& \simeq \pi_{0} \operatorname{Map}_{\mathcal{A}_{n_{*}}}(X, K(A, n)) \simeq[X, K(A, n)]_{*}
\end{aligned}
$$

To check agreement with homology, we would rather appeal to the Eilenberg-Steenrod axioms for uniqueness.

We know from previous courses in algebraic topology that cohomology often comes with a ring structure. Let's see that in a more general setting here.

Construction 2.3.24. Let $E$ be a homotopy commutative ${ }^{6}$ ring spectrum. Then we wish to show that $E^{*} X$ has a ring structure when $X=\Sigma^{x} Y$ is the suspension spectrum of an anima, natural in the variable $X$. The naturality of the following construction will be clear, so we will ignore that from now. Let $\mu: E \otimes E \rightarrow E$ be the multiplication on $E$. Then we define a graded multiplication on $E^{*} X$ as the composite

$$
E^{m} X \times E^{n} X \simeq\left[X, \Sigma^{m} E\right] \times\left[X, \Sigma^{n} E\right] \xrightarrow{(f, g) \mapsto f \otimes g}\left[X \otimes X, \Sigma^{m} E \otimes \Sigma^{n} E\right] \xrightarrow{\Delta^{*} \circ \mu_{*}}\left[X, \Sigma^{m+n} E\right]
$$

where $\Delta: X \rightarrow X \otimes X$ only exists as $X \otimes X \simeq \Sigma^{x}(Y \wedge Y)$ and there exists a diagonal map $Y \rightarrow Y \wedge Y$, and we have sneakily shuffled $E$ past a $\mathbf{S}^{n}$.

If $X$ is a spectrum, we only in general obtain a bilinear exterior product map on $E$ cohomology:

$$
\times:[X, E[m]] \times[X, E[n]] \xrightarrow{(f, g) \mapsto f \otimes g}[X \otimes X, E[m] \otimes E[n]] \xrightarrow{\mu_{*}}[X \otimes X, E[m+n]]
$$

[^0]
[^0]:    ${ }^{6}$ We will mostly discuss homotopy commutative ring spectra in these lectures, but one can do quite a bit of work with simply homotopy ring spectra, so associative monoid objects in h Sp . For example, the spherical groups rings $\mathbf{S}[G]=\Sigma^{x} G_{+}$for a nonabelian group $G$ are only associative monoids (in an $x$-categorical sense too). Other, perhaps more surprising examples are perhaps the Morava $K$-theory spectra $K(n)$ at the prime 2 for finite positive $n$.

Even more generally, if $E$ has no assumed multiplicative structure, we have an (other) bilinear exterior product:
$E^{m} X \times E^{n} X=[X, E[m]] \times[X, E[n]] \xrightarrow{(f, g) \mapsto f \otimes g}[X \otimes X, E[m] \otimes E[n]]=(E \otimes E)^{m+n}(X \otimes X)$
In the situation when $E$ has a multiplicative structure, we also obtain a pairing between homology and cohomology.

Definition 2.3.26. Let $E$ and $X$ be spectra and assume that $E$ is a homotopy commutative ring spectrum. Define an $E_{*}$-linear map

$$
\langle-,-\rangle: E_{*} X \underset{E_{*}}{\otimes} E^{*} X \rightarrow E_{*}
$$

by sending a pair of representing maps $f: \mathbf{S}[m] \rightarrow E \otimes X$ and $g: X \rightarrow E[n]$ to the composite

$$
\mathbf{S}[m] \xrightarrow{f} E \otimes X \xrightarrow{E \otimes g} E \otimes E[n] \xrightarrow{\mu} E[n]
$$

now viewed as an element of $E_{m-n}$.
Warning 2.3.27. It is here, with the above pairings and multiplications, that we need to be very careful about our signs and our use of the shifts. For example, just as is the case for ordinary singular cohomology, the multiplication defined on the $E$-cohomology groups of an anima $X$ for a commutative multiplicative cohomology theory $E$ are only commutative up to the Koszul sign rule. This won't play a huge role for us this semester, but it should not generally be overlooked.

End of lecture 10 and week 6

Let us actually prove something about the (co)homology theories above.
Theorem 2.3.28 (Hurewicz theorem for spectra). Let $X$ and $Y$ be connective spectra. Then the natural exterior product map $\pi_{0} X \otimes \pi_{0} Y \rightarrow \pi_{0}(X \otimes Y)$ of (2.3.25) is an equivalence. In particular, if $Y=\mathbf{Z}$, then the natural map $\pi_{0} X \rightarrow \pi_{0}(X \otimes \mathbf{Z})=H_{0}(X ; \mathbf{Z})$ is an isomorphism.

As both homotopy groups of spectra and homology groups are stable under suspension, see Pr.2.1.31, we can rephrase the "in particular" statement above to read: if $X$ is a spectrum and $n$ a minimal integer such that $\pi_{n} X$ is nonzero, then the natural map $\pi_{n} X \rightarrow H_{n}(X ; \mathbf{Z})$ is an isomorphism.

The slogan for the below proof is:
The tensor product of spectra commutes with colimits, the hypotheses of Th.2.3.28 are closed under colimits, and all connective spectra come from $\mathbf{S}$ via colimits.

In more detail:

Proof. Consider $\mathcal{C} \subseteq$ Sp, the full $\infty$-subcategory spanned by those spectra $X$ such that for all connective spectra $Y$, the natural map $\pi_{0} X \otimes \pi_{0} Y \rightarrow \pi_{0}(X \otimes Y)$ is an isomorphism. First, notice that $\mathcal{C}$ contains $\mathbf{S}$, which follows from the fact that $\mathbf{S}$ is a unit for the tensor product of spectra; see Pr.2.3.8. Next, notice that $\mathcal{C}$ is closed under sums, as we have natural isomorphisms

$$
\pi_{0} \oplus X_{i} \otimes \pi_{0} Y \simeq \oplus \pi_{0} X_{i} \otimes \pi_{0} Y \xrightarrow{\simeq} \oplus \pi_{0}\left(X_{i} \otimes Y\right) \simeq \pi_{0}\left(\oplus\left(X_{i} \otimes Y\right)\right) \simeq \pi_{0}\left(\left(\oplus X_{i}\right) \otimes Y\right)
$$

using Pr. 2.1.32, and the facts that the tensor product of spectra and abelian groups both commute with colimits in each variable. Finally, we notice that $\mathcal{C}$ is closed under cofibres. To this end, let $X, X^{\prime}$ lie in $\mathcal{C}$, suppose we have a map $X \rightarrow X^{\prime}$ between them, and write $C$ for the cofibre of this map. As the tensor product of spectra commutes with colimits in each variable, we see that the cofibre sequence defining $C$ yields the cofibre sequence

$$
X \otimes Y \rightarrow X^{\prime} \otimes Y \rightarrow C \otimes Y
$$

Consider the diagram of abelian groups
where the lower row comes from the above cofibre sequence sequence, and hence is exact, and the vertical maps are the canonical maps in question. The map $f$ and $g$ are equivalences as $X$ and $X^{\prime}$ lie in $\mathcal{C}$. We cannot use a five lemma argument, as we do not have any right to assume the upper row is exact-tensoring is not an exact functor-however, the lower row is exact by Pr.2.1.35. As $X$ lies in $\mathcal{C}$, we easily see, using Pr.2.1.31, that $X[1]$ also lies in $\mathcal{C}$, hence we have isomorphisms

$$
\pi_{0}(X[1] \otimes Y) \simeq \pi_{0}(X[1]) \otimes \pi_{0} Y=\pi_{-1} X \otimes \pi_{0} Y=0
$$

as $X$ was assumed to be connective. This means that $\pi_{0}(C \otimes Y)$ is the natural quotient of $\pi_{0}(X \otimes Y)$ by $\pi_{0}\left(X^{\prime} \otimes Y\right)$. Using that $f$ and $g$ are isomorphisms, and that tensor products of abelian groups commute with colimits, we see this is naturally equivalent to $\pi_{0} C \otimes \pi_{0} Y$.

As $\mathcal{C}$ is closed under sums and cofibres and contains $\mathbf{S}$, we see that $\mathcal{C}$ contains all connective spectra by Exc.2.2.6.

Exercise 2.3.29. Show that if two spectra $X$ and $Y$ are connective, then $X \otimes Y$ is also connective. (Hint: there is one argument following the ideas of Th.2.3.28, but there is also another proof using the equivalences

$$
\pi_{n}(X \otimes Y) \simeq \pi_{0}(X[-n] \otimes Y)
$$

and applying the result of the Hurewicz theorem Th.2.3.28.)

Exercise 2.3.30. Show that the Eilenberg-Mac Lane spectrum functor $H: \mathrm{Ab} \rightarrow \mathrm{Sp}$ is lax monoidal, meaning that for any pair of abelian groups $A, B$, there are natural maps of spectra $H A \otimes H B \rightarrow H(A \otimes B)$ and $\mathbf{S} \rightarrow H \mathbf{Z}$ satisfying the appropriate unitality and associativity properties. (Hint: you may think of using Exc.2.2.17 together with Exc.2.3.29).
Exercise 2.3.31. Produce another more categorical proof of Exc.2.3.30 by showing that $H: \mathrm{Ab} \rightarrow$ $\mathrm{Sp}^{\mathrm{cn}}$ into the $\infty$-category of connective spectra has a left adjoint given by $\tau_{\leqslant 0}=\pi_{0}$ and use Th.2.3.28 to show this left adjoint is strong monoidal, meaning the monoidal structure maps are equivalences.

The following is a natural consequence of the Hurewicz theorem for spectra Th.2.3.28.
Theorem 2.3.32 (Homology Whitehead for spectra). A map of bounded below spectra $X \rightarrow Y$ is an equivalence if and only if it induces an isomorphism on $\mathbf{Z}$-homology.

Proof. The "only if" direction is clear, so let us now consider the converse. Let $F$ be the fibre of $X \rightarrow Y$. If $X \rightarrow Y$ is not an equivalence, then $F$ is not the zero spectrum. As both $X$ and $Y$ are bounded below, then there is a minimal integer $n$ such that $\pi_{n} F \neq 0$. In particular, $F[-n]$ is connective, hence from the Hurewicz theorem above (Th.2.3.28), we see that $\pi_{0} F[-n]$ is isomorphic to $H_{0}(F[-n] ; \mathbf{Z})=0$, so in particular $\pi_{0} F[-n] \simeq \pi_{n} F$ vanishes, a contradiction.

# 2.4 Atiyah-Hirzebruch spectral sequence 

In this section we will discuss a kind of spectral sequence which relates singular cohomology to the cohomology of any spectrum $E$. This will take the following form:

Theorem 2.4.1. Let $X$ be a pointed anima and $E$ a spectrum. Then there is a half-plane spectral sequence

$$
E_{2}^{p, q}=\widehat{H}^{p}\left(X ; \pi_{-q} E\right) \Longrightarrow \widehat{E}^{p+q}(X)
$$

If $E$ is a homotopy commutative ring spectrum, then this spectral sequence above is multiplicative. The above spectral sequence is also natural in both $X$ and $E$.

As-per-usual, if one is given an unbased anima $X$, then one can feed $X_{+}$into the above theorem and obtain the spectral sequence

$$
E_{2}^{p, q}=H^{p}\left(X ; \pi_{-q} E\right) \Longrightarrow E^{p+q}(X)
$$

According to Adams [Ada74, p.215], these spectral sequences were essentially folklore until someone found a use for them. Whitehead apparently thought about this only after he wrote [Whi56], so they are not included there, where they would have naturally complemented that work (a review by Wen-tsun Wu can be found on the here). In the end, Atiyah and Hirzebruch used this spectral sequence in [AH61] where they invented topological $K$-theory, one of the first widely used extraordinary cohomology theories.

Here we follow the proof given in [Mau63] using exact couples, as championed by [Mas53].

Proof. Let us drop the "reduced cohomology" notation for this proof, for brevity.
Our construction will make naturality in $X$ clear, and the naturality in $E$ will follow from the functoriality of the Postnikov tower alluded to in Exc.2.2.17. To this end, recall that associated to the spectrum $E$ is a Postnikov tower Exc.2.2.17:

$$
\cdots \rightarrow \tau_{\leqslant n+1} E \rightarrow \tau_{\leqslant n} E \rightarrow \tau_{\leqslant n-1} E \rightarrow \cdots
$$

which you will recall is a tower of spectra under $E$. Also, recall that essentially by construction, the fibre of $\tau_{\leqslant n} E \rightarrow \tau_{\leqslant n-1} E$ is the Eilenberg-Mac Lane spectrum $\left(\pi_{n} E\right)[n]$ associated to the abelian group $\pi_{n} E$ in degree $n$-we'll refer back to this fact a times. We now define an exact couple
![img-62.jpeg](img-62.jpeg)
to have the bigraded groups

$$
C_{p, q}=\left(\pi_{p} E[p+q]\right)^{p}(X) \simeq\left(\pi_{-q} E\right)^{p}(X), \quad A_{p, q}=\left(\tau_{\leqslant p}(E[p+q])\right)^{0}(X) \simeq\left(\tau_{\leqslant 0}(E[q])\right)^{p}(X)
$$

where the map $f$ is induced by the natural map $\tau_{\leqslant p}(E[p+q]) \rightarrow \tau_{\leqslant p-1}(E[p+q])$, the map $g$ is induced by the boundary map $\partial$ in the cofibre sequence

$$
\tau_{\leqslant p}(E[p+q]) \rightarrow \tau_{\leqslant p-1}(E[p+q]) \xrightarrow{\partial}\left(\pi_{p} E[p+q]\right)[p+1] \simeq\left(\pi_{-q} E\right)[p+1]
$$

and $h$ is induced by the natural map $\left(\pi_{p}(E[p+q])\right)[p] \rightarrow \tau_{\leqslant p}(E[p+q])$-keep in mind that $g$ is a map $A_{p-1, q+1} \rightarrow C_{p+1, q}$. Moreover, this is the $E_{2}$-page of our cohomological spectral sequence, which is why is might look a little different in grading as compared to the Serre spectral sequence of Algebraic Topology I. It is clear that the $E_{2}$-page of this spectral sequence is the desired cohomology group

$$
E_{2}^{p, q}=\left(\pi_{p} E[p+q]\right)^{p}(X) \simeq\left(\pi_{-q} E\right)^{p}(X) \simeq H^{p}\left(X ; \pi_{-q} X\right)
$$

and it also follows by construction that the desired filtration on $E^{n}(X)$ is given by the kernel of the map

$$
E^{n}(X)=\mathrm{h} \operatorname{Sp}\left(\Sigma^{\infty} X, E[n]\right) \rightarrow \mathrm{h} \operatorname{Sp}\left(\Sigma^{\infty} X, \tau_{\leqslant p-1} E[n]\right)
$$

induced by the map $E[n] \rightarrow \tau_{\leqslant p-1} E[n]$. For multiplicativity, one has many tedious calculations to perform; see here for a discussion but a much cleaner proof can be obtained using filtered spectra and Day convolution.

Exercise 2.4.2. Show that the filtration of $E_{*}(X)$ used in the above proof can also be obtained from a CW-filtration on $X$. (Hint: this is done explicitly in [Ada74, §III.7].)
Exercise 2.4.3. Formulate an Atiyah-Hirzebruch spectral sequence where $X$ is a spectrum.
Exercise 2.4.4. Formulate and prove a homological version of Th.2.4.1.

Exercise 2.4.5. Construct generalised versions of the Atiyah-Hirzebruch spectral sequences of Th.2.4.1 and Exc.2.4.4 such that if $X \rightarrow Y$ is a map of anima with fibre $F$, then these generalised spectral sequences take the form

$$
E_{p, q}^{2}=H_{p}\left(Y ; E_{q}(F)\right) \Longrightarrow E_{p+q}(X) \quad E_{2}^{p, q}=H^{p}\left(Y ; E^{q}(F)\right) \Longrightarrow E^{p+q}(X)
$$

The following is a simple example which we will see again in $\S 3.1$.
Example 2.4.6. First, we know that $\pi_{*} \mathrm{KU} \simeq \mathbf{Z}\left[u^{ \pm}\right]$from Eg.2.2.19. Second, we know the cohomology ring $H^{*}\left(\mathbf{C P}^{n} ; \mathbf{Z}\right) \simeq \mathbf{Z}[x] / x^{n+1}$ where $|x|=2$ from Topology II. Feeding this into the Atiyah-Hirzebruch spectral sequence for cohomology, we obtain an $E_{2}$-page of the form

$$
E_{2}^{*, *} \simeq \mathbf{Z}\left[u^{ \pm}, x\right] / x^{n+1} \quad|u|=(0,-2),|x|=(2,0)
$$

In particular, notice there cannot be any differentials $d_{r}$ in this spectral sequence, as the total degree of any differential is odd, and this spectral sequence is concentrated in even degrees. We are then left to deal with extension problems, however, there cannot be any extension problems because $\mathbf{Z}$ is projective as an abelian group, so we find that $\mathrm{KU}^{*}\left(\mathbf{C P}^{n}\right) \simeq \mathbf{Z}\left[u^{ \pm}, x\right] / x^{n+1}$ where $|u|=-2$ and $|x|=2$. This argument using the projectivity of $\mathbf{Z}$ is a little lazy-we will see this computation again in Pr.3.1.16.
Exercise 2.4.7. Calculate $\mathrm{KU}^{0}(X)$ and $\mathrm{KU}^{1}(X)$ where $X$ is the oriented genus $g$ surface or real projective space $\mathbf{R P}^{n}$.
Exercise 2.4.8. For a pointed anima $X$ and nonnegative integers $a \leqslant b$, let us write $\tau_{[a, b]} X$ for the fibre of the natural map

$$
\tau_{\leqslant b} X \rightarrow \tau_{\leqslant a-1} X
$$

where $\tau_{-1} X=*$. In other words, the homotopy groups of $\tau_{[a, b]} X$ are concentrated in degree within the interval $[a, b]$. Show that the differentials $d_{r}: E_{r}^{p, q} \rightarrow E_{r}^{p+r, q-r+1}$ in the AtiyahHirzebruch spectral sequence with respect to a spectrum $E$ and an anima $X$ are induced by the cohomology operation defined by the $k$-invariant $k^{p, p+r-2} \in H^{p+r}\left(\tau_{[p, p+r-2]} E_{p+q} ; \pi_{p+r-1}\left(E_{p+q}\right)\right)$. Using this, show that $d_{3}$ is precisely $\mathrm{Sq}^{3}$ when $E=\mathrm{KU}$-this will require some previous knowledge about BU and its $k$-invariants.

End of lecture 11

# 2.5 Rationalisation and Bousfield localisation 

For a given spectrum $E$, the cohomology groups $E^{*}(X)$ can only capture a certain portion of information of the anima (or spectrum) $X$. We have already seen some of these ideas before: the singular cohomology of $\mathbf{R P}^{n}$ is not very interesting with rational coefficients, but it is much more interesting with $\bmod 2$ coefficients. In this section, we will discuss a systematic way of discussing "the part of $X$ seen by $E$ ".

Definition 2.5.1. Let $E$ be a fixed spectrum. We say that:

1. a map of spectra $f: X \rightarrow Y$ is an $E$-equivalence if the induced map $E \otimes f: E \otimes X \rightarrow E \otimes Y$ is an equivalence.

2. a spectrum $L$ is $E$-local if for all $E$-equivalences $f: X \rightarrow Y$, the induced map $L^{Y} \rightarrow L^{X}$ is an equivalence.
3. a map of spectra $X \rightarrow L_{E} X$ is an $E$-localisation if the spectrum $L_{E} X$ is $E$-local and the map is an $E$-equivalence.
4. two spectra $E_{1}$ and $E_{2}$ have the same Bousfield class if the class of $E_{1}$-equivalences is the same the as the class of $E_{2}$-equivalences.

Exercise 2.5.2. Given a fixed spectrum $E$, then we say another spectrum $X$ is $E$-acyclic if $E \otimes X$ is the zero spectrum. Prove that $L$ is $E$-local if and only if for all $E$-acyclic spectra $Y$, the mapping spectrum $L^{Y}$ vanishes.
Example 2.5.3. Consider the rational sphere spectrum $\mathbf{S}_{\mathbf{Q}}$ which we define as the colimit

$$
\mathbf{S}_{\mathbf{Q}}=\operatorname{colim}\left(\mathbf{S} \xrightarrow{2} \mathbf{S} \xrightarrow{2: 3} \mathbf{S} \xrightarrow{2: 3: 5} \mathbf{S} \xrightarrow{2: 3: 5: 7} \cdots\right)
$$

First, we claim that the natural map $\mathbf{S} \rightarrow \mathbf{S}_{\mathbf{Q}}$ given by the inclusion into the zeroth term in the above diagram, is a $\mathbf{Q}$-localisation. In other words, $\mathbf{S}_{\mathbf{Q}}$ is a model for $L_{\mathbf{Q}} \mathbf{S}$, the localisation of the sphere spectrum at the Eilenberg-Mac Lane spectrum $\mathbf{Q}$. To see this, we first calculate $\pi_{n} \mathbf{S}_{\mathbf{Q}} \simeq\left(\pi_{n} \mathbf{S}\right) \otimes \mathbf{Q}$ using the fact that homotopy groups commute with filtered colimits, see Lm.2.1.33, and the fact that the colimit of abelian groups given by the multiplication indicated above yields the rationalisation of that abelian group. In particular, Serre's calculations of the rational homotopy groups of spheres discussed in Algebraic Topology I show us that the homotopy groups of $\mathbf{S}_{\mathbf{Q}}$ are a single $\mathbf{Q}$ concentrated in degree 0 . In particular, by Th.2.2.14, we see that $\mathbf{S}_{\mathbf{Q}}$ is equivalent to the Eilenberg-Mac Lane spectrum $\mathbf{Q}$. It is now clear that our map $\mathbf{S} \rightarrow \mathbf{S}_{\mathbf{Q}}$ is a $\mathbf{Q}$-equivalence, as the map

$$
\mathbf{Q} \simeq \mathbf{S} \otimes \mathbf{Q} \rightarrow \mathbf{S}_{\mathbf{Q}} \otimes \mathbf{Q}
$$

clearly induces an isomorphism on homotopy groups so Whitehead's theorem for spectra Th.2.2.7 now applies. It remains to show that $\mathbf{S}_{\mathbf{Q}}$ is $\mathbf{Q}$-local. To this end, we use Exc.2.5.2 to see that that it is necessary and sufficient to show $\mathbf{S}_{\mathbf{Q}}^{X}$ vanishes for all $\mathbf{Q}$-acyclic spectra $X$. Actually, from the stability of spectra, it suffices to show that $\pi_{0} \mathbf{S}_{\mathbf{Q}}^{X} \simeq\left[X, \mathbf{S}_{\mathbf{Q}}\right]$ vanishes for all $\mathbf{Q}$-acyclic $X$, so each map from a $\mathbf{Q}$-acyclic $X$ to $\mathbf{S}_{\mathbf{Q}}$ is nullhomotopic. To see this, consider the diagram of spectra
![img-63.jpeg](img-63.jpeg)
which commutes from the bilinearity of the tensor product of spectra. The two key facts about this diagram are that the right-hand vertical map is an equivalence, this is easy to see on homotopy groups, and also that the lower-left spectrum vanishes, which is true by assumption. It follows that $f$ itself is nullhomotoptic.

Proposition 2.5.4. Rationalisation is smashing, ie, there is a natural equivalence between $L_{\mathbf{Q}} X$ and $X \otimes \mathbf{S}_{\mathbf{Q}}=X_{\mathbf{Q}}$. From now on, we will call $\mathbf{Q}$-local spectra rational spectra.

Proof. Using the fact that $\mathbf{S}_{\mathbf{Q}} \otimes \mathbf{S}_{\mathbf{Q}} \simeq \mathbf{S}_{\mathbf{Q}} \simeq \mathbf{Q}$, as referred to in Eg.2.5.3, we immediately see that the natural map $X \rightarrow X \otimes \mathbf{S}_{\mathbf{Q}}=X_{\mathbf{Q}}$ is $\mathbf{Q}$-equivalence. We can easily repeat the arguments of Eg.2.5.3 as $X_{\mathbf{Q}} \simeq X \otimes \mathbf{Q}$ can evidently be given the structure of a $\mathbf{Q}$-module.

Example 2.5.5. We see essentially immediately from the fact that filtered colimits commute with homotopy groups Lm.2.1.33 that for an abelian group $A$, the $\mathbf{Q}$-localisation of $A$ as an Eilenberg-Mac Lane spectrum is precisely the Eilenberg-Mac Lane spectrum associated to $A \otimes \mathbf{Q}$.
Example 2.5.6. Using Pr.2.5.4 and our knowledge of the homotopy groups of KU from Eg.2.2.19, we calculate the homotopy groups of $\mathrm{KU}_{\mathbf{Q}}$ to be the ring $\mathbf{Q}\left[\beta^{\pm}\right]$.

Corollary 2.5.7 (Rational Hurewicz). For any spectrum $X$, the natural map of graded $\mathbf{Q}$ vector spaces

$$
\pi_{*} X \otimes \mathbf{Q} \simeq \pi_{*} X_{\mathbf{Q}} \rightarrow H_{*}\left(X_{\mathbf{Q}} ; \mathbf{Z}\right) \simeq H_{*}(X ; \mathbf{Q})
$$

is an isomorphism.
Proof. This follows immediately from the fact that the rationalisation of the sphere is $\mathbf{Q}$ and the identification

$$
H_{*}\left(X_{\mathbf{Q}} ; \mathbf{Z}\right)=\pi_{*}\left(X_{\mathbf{Q}} \otimes \mathbf{Z}\right) \simeq \pi_{*}\left(X \otimes \mathbf{Z}_{\mathbf{Q}}\right) \simeq \pi_{*}(X \otimes \mathbf{Q})=H_{*}(X ; \mathbf{Q})
$$

Corollary 2.5.8. For every rational spectrum $X$, there is an equivalence of spectra

$$
X \simeq \bigoplus_{n \in \mathbf{Z}}\left(\pi_{n} X\right)[n]
$$

Proof. Choosing a graded $\mathbf{Q}$-basis for $\pi_{n} X$, we obtain maps of spectra $\mathbf{Q}[n] \simeq \mathbf{S}_{\mathbf{Q}}[n] \rightarrow X$ from the isomorphism

$$
\pi_{n} X \simeq \pi_{0} \operatorname{Map}_{\mathrm{Sp}}(\mathbf{S}[n], X) \stackrel{\pi_{0}}{\longleftrightarrow} \operatorname{Map}_{\mathrm{Sp}}\left(\mathbf{S}_{\mathbf{Q}}[n], X\right)
$$

where the map of spectra $\mathbf{S} \rightarrow \mathbf{S}_{\mathbf{Q}}$ induces the above isomorphism as $X$ is rational, hence $\mathbf{Q}-$ local. These maps of spectra then assemble to a map $\oplus \mathbf{Q}[n] \simeq\left(\pi_{n} X\right)[n] \rightarrow X$ which when all summed over $n$ yields the desired equivalence; by construction it induces an isomorphism on homotopy groups.

As a further corollary, we can actually control the whole homotopy category of rational spectra.

Corollary 2.5.9. Let us write $\mathrm{Sp}_{\mathbf{Q}}$ for the $\infty$-subcategory of Sp spanned by rational spectra. The functor

$$
\mathrm{h} \mathrm{Sp}_{\mathbf{Q}} \xrightarrow{\pi_{*}} \operatorname{gr}_{\operatorname{Mod}_{\mathbf{Q}}}
$$

into graded $\mathbf{Q}$-vector spaces is an equivalence of 1-categories.

Proof. By Cor.2.5.8 we see this functor is essentially surjective, so it suffices to show it is fully-faithful. To this end, first note that $\operatorname{gr} \operatorname{Mod}_{\mathbf{Q}}$ is defined as the 1-category $\operatorname{Fun}\left(\mathbf{Z}^{\delta}, \operatorname{Mod}_{\mathbf{Q}}\right)$ where $\mathbf{Z}^{\delta}$ refers to the 1-category whose objects are integers and only identity morphisms. The result now follows from Th.2.2.14, more accurately Cor.2.2.16, and Cor.2.5.8:

$$
\begin{aligned}
& \mathrm{h} \operatorname{Sp}_{\mathbf{Q}}(X, Y) \simeq \mathrm{h} \operatorname{Sp}_{\mathbf{Q}}\left(\bigoplus \pi_{n} X, \bigoplus \pi_{m} Y\right) \simeq \prod_{m, n} \mathrm{~h} \operatorname{Sp}\left(\pi_{n} X, \bigoplus \pi_{m} Y\right) \\
& \prod_{n} \mathrm{~h} \operatorname{Sp}\left(\pi_{n} X, \pi_{n} Y\right) \simeq \prod_{n} \operatorname{Mod}_{\mathbf{Q}}\left(\pi_{n} X, \pi_{n} Y\right) \simeq \operatorname{gr} \operatorname{Mod}_{\mathbf{Q}}\left(\pi_{*} X, \pi_{*} Y\right)
\end{aligned}
$$

Above we used the fact that given rational spectra $A, B$ concentrated in degrees $n$ and $m$, respectively, then $\mathrm{h} \operatorname{Sp}_{\mathbf{Q}}(A, B)=0$ if $n \neq m$. This is not true integrally, ${ }^{7}$ but rationally we note that a map $A \rightarrow B$ is automatically zero if $m<n$ from the proof of Th.2.2.14. For $n<m$, actually this argument works for $m<n$ as well, we notice that $A \simeq \bigoplus \mathbf{S}_{\mathbf{Q}}[n]$ from Cor.2.5.8 and the fact that $\pi_{n} A$ is a free $\mathbf{Q}$-vector space. Now we have equivalences

$$
[A, B] \simeq[\bigoplus \mathbf{S}_{\mathbf{Q}}[n], B] \simeq \prod \pi_{n} B
$$

so clearly morphisms $A \rightarrow B$ vanish if $n \neq m$.
Example 2.5.10. The classical Chern character can be viewed in this way. Indeed, by Eg.2.5.6 and Cor.2.5.8, the rationalisation of KU has codomain

$$
\mathrm{KU} \rightarrow \mathrm{KU}_{\mathbf{Q}} \simeq \bigoplus_{n \in \mathbf{Z}} \mathbf{Q}[2 n]
$$

This map then induces the Chern character on cohomology

$$
\mathrm{KU}^{0}(X) \rightarrow H^{2 n}(X ; \mathbf{Q})
$$

for a spectrum $X$.
Exercise 2.5.11. Show that we can copy much of the above discussion by replacing $\mathbf{Q}$ with any subring $R \subseteq \mathbf{Q}$. In particular, $L_{R} X$ can be modelled by the colimit

$$
X \xrightarrow{n_{1}} X \xrightarrow{n_{1} \cdot n_{2}} X \xrightarrow{n_{1} \cdot n_{2} \cdot n_{3}} X \xrightarrow{n_{1} \cdot n_{2} \cdot n_{3} \cdot n_{4}} \cdots
$$

where $n_{1}, n_{2}, n_{3}, \ldots$ is a fixed exhaustive sequence of all integers inverted in $R$ and that $R$ localisation is smashing. Show that Cor.2.5.8 does not hold if $R$ is a proper subring of $\mathbf{Q}$-here you might want to use some facts about the $p$-torsion inside $\pi_{*} \mathbf{S}$ from Topology II or Algebraic Topology I.
Remark 2.5.12. In general, if we are given a (countable, for simplicity) set of elements $S \subseteq \pi_{*} R$ inside a homotopy commutative ring spectrum $R$, we can define $R\left[S^{-1}\right]$ as the colimit of spectra

$$
R \xrightarrow{s_{0}} R\left[-\left|s_{0}\right|\right] \xrightarrow{s_{0} s_{1}} R\left[-2\left|s_{0}\right|-\left|s_{1}\right|\right] \rightarrow \cdots
$$

where $S \simeq\left\{s_{0}, s_{1}, s_{2}, s_{3}, \ldots\right\}$ is some chosen enumeration of $S$, and a map $s_{i}: R\left[\left|s_{i}\right|\right] \rightarrow R$ is defined as the composite

$$
R\left[\left|s_{i}\right|\right] \simeq R \otimes \mathbf{S}\left[\left|s_{i}\right|\right] \xrightarrow{R \otimes s_{i}} R \otimes R \xrightarrow{\mu} R
$$

[^0]
[^0]:    ${ }^{7}$ Indeed, there are interesting, meaning nonzero, maps $\mathbf{F}_{p} \rightarrow \mathbf{F}_{p}[n]$ for $n \geqslant 1$ encoding the Steenrod power operations.

Exercise 2.5.13. If $R$ is a homotopy commutative ring spectrum and $S$ a countable subset of elements $S \subseteq \pi_{*} R$, then calculate the homotopy groups of $R\left[S^{-1}\right]$ and show that $R\left[S^{-1}\right]$ has the structure of a homotopy commutative ring spectrum. Can you adequately generalise the construction of Rmk.2.5.12 for larger cardinalities of $S$ ?

We have discussed rationalisation and localisation at a prime in quite a bit of detail now, but in fact, all $E$-localisation functors exist.

Theorem 2.5.14. Let $E$ be a spectrum. Then the inclusion of the full $\infty$-subcategory of $E$-local spectra $\mathrm{Sp}_{E}$ into Sp has a left adjoint $L_{E}$, called the E-Bousfield localisation functor.

Classically, a hands-on proof is given in the homotopy category h Sp, for example, by Bousfield [Bou79].

We will not prove this theorem, as for us, it involves too many technical set-theoretic issues. The loose argument one wants to make is the following: if we know that Sp is a presentable stable $\infty$-category, and that the inclusion $\mathrm{Sp}_{E} \rightarrow \mathrm{Sp}$ is accessible and preserves all limits, then we obtain our left adjoint $L_{E}$ by an $\infty$-categorical adjoint functor theorem; see [Lur09b, Cor.5.5.2.9]. Ignoring both of the unknown adjectives for now, which is highly nontrivial to check, we can see that the above inclusion does preserve limits; this follow from the universal property of limits, the definition of the internal mapping spectrum, and the definition of an $E$-local object above.

End of lecture 12 and week 7

# 2.6 Completion at a prime 

Fix a prime number $p$. We have discussed rationalisation, or Bousfield localisation at $\mathbf{Q}=\mathbf{S}_{\mathbf{Q}}$, but another very useful maneuver in stable homotopy theory is $p$-completion, or Bousfield localisation at the $\bmod p$ Moore spectrum $\mathbf{S} / p$. This is different to the $p$-localisation, or Bousfield localisation at $\mathbf{S}_{(p)}$ as $p$-completion kills rational information too.

Definition 2.6.1. We call the Bousfield localisation at $\mathbf{S} / p$ p-completion and denote the associated functor as $(-)_{p}^{\wedge}$.

Our first goal is to give a model for this functor without referring to Th.2.5.14.
First we define $\mathbf{S} / p^{\infty}$ as the cofibre of the natural map

$$
\mathbf{S} \rightarrow \mathbf{S}\left[\frac{1}{p}\right]=\operatorname{colim}\left(\mathbf{S} \xrightarrow{p} \mathbf{S} \xrightarrow{p} \mathbf{S} \xrightarrow{p} \cdots\right)
$$

where $\mathbf{S}\left[\frac{1}{p}\right]$ is the localisation of $\mathbf{S}$ away from $p$, as we have killed all potentially interesting $p$-power torsion information. By construction, the $\mathbf{Z}$-homology of $\mathbf{S} / p^{\infty}$ is precisely

$$
H_{*}\left(\mathbf{S} / p^{\infty} ; \mathbf{Z}\right) \simeq \mathbf{Z} / p^{\infty} \simeq \mathbf{Z}\left[\frac{1}{p}\right] / \mathbf{Z} \simeq \operatorname{colim}\left(\mathbf{Z} / p \xrightarrow{p} \mathbf{Z} / p^{2} \xrightarrow{p} \mathbf{Z} / p^{3} \xrightarrow{p} \cdots\right)
$$

so $\mathbf{S} / p^{\infty}$ is a kind of Moore spectrum. In fact, the isomorphisms above also show that $\mathbf{S} / p^{\infty}$ can be written as the colimit

$$
\mathbf{S} / p^{\infty}=\operatorname{colim}\left(\mathbf{S} / p \xrightarrow{p} \mathbf{S} / p^{2} \xrightarrow{p} \mathbf{S} / p^{3} \xrightarrow{p} \cdots\right)
$$

We claim that this spectrum can be used to model the $p$-complete $X_{p}^{\wedge}$ of a spectrum $X$.
Proposition 2.6.2. Let $X$ be a spectrum. The natural map

$$
X \simeq X^{\mathbf{S}} \rightarrow X^{\mathbf{S} / p^{\infty}[-1]}
$$

induced by $\mathbf{S} / p^{\infty}[-1] \rightarrow \mathbf{S}$ is the $p$-completion of $X$, meaning the target is $p$-complete and the map is an $\mathbf{S} / p$-equivalence.

Proof. First, let us show that $X_{p}^{\wedge}=X^{\mathbf{S} / p^{\infty}[-1]}$, suggestive notation, is $p$-complete. In other words, we need to take an $\mathbf{S} / p$-acyclic $Y$ and show that $\left(X_{p}^{\wedge}\right)^{Y}$ is zero. By Pr.2.3.19, we have an equivalence

$$
\left(X_{p}^{\wedge}\right)^{Y} \simeq X^{Y \otimes \mathbf{S} / p^{\infty}[-1]}
$$

so it suffices to show that the spectrum

$$
Y \otimes \mathbf{S} / p^{\infty}[-1] \simeq \operatorname{colim}\left(Y \otimes \mathbf{S} / p \xrightarrow{p} Y \otimes \mathbf{S} / p^{2} \xrightarrow{p} Y \otimes \mathbf{S} / p^{3} \xrightarrow{p} \cdots\right)[-1]
$$

is zero. In fact, we claim that all of the terms in the above colimit are zero. Indeed, we will show this by induction. The base-case of $Y \otimes \mathbf{S} / p=0$ is the assumption that $Y$ is $\mathbf{S} / p$-acyclic. For some $n \geqslant 1$, we see that $Y \otimes \mathbf{S} / p^{n+1}$ vanishes using the octohedral axiom; see Exc.2.6.7:
![img-64.jpeg](img-64.jpeg)

From our assumptions we know that $Y \otimes \mathbf{S} / p=0$ and by induction $Y \otimes \mathbf{S} / p^{n}=0$, so the cofibre sequence above defined by the outer maps shows that $Y \otimes \mathbf{S} / p^{n+1}$ also vanishes.

Next, we want to show that the map in the statement of this proposition is an $\mathbf{S} / p$ equivalence. To see this, notice that its fibre is the mapping spectrum $X^{\mathbf{S}\left[\frac{1}{p}\right]}$, which we claim is $\mathbf{S} / p$-acyclic. To see this, notice that it suffices to show that multiplication by $p$ acts both invertibly and nilpotently on $X^{\mathbf{S}\left[\frac{1}{p}\right]} \otimes \mathbf{S} / p^{n}$, in fact, we will only need the case $n=1$. This will follow from the following two claims.

Claim 2.6.3. If $p$ acts invertibly on $Y$, then $p$ acts invertibly on $Y^{Z}$ for spectra $Y, Z$.
Proof of Claim. This would be true in an stable $\infty$-category with internal homomorphism objects, but let us directly prove the claim above: if the map $\cdot p: Y \rightarrow Y$ is an equivalence, then the induced map

$$
(\cdot p)_{*}: Y^{Z} \xrightarrow{\Delta_{Y}^{Y}}\left(Y^{\oplus p}\right)^{Z} \xrightarrow{\nabla_{Y}^{Y}} Y^{Z}
$$

is an equivalence by functoriality. It is a diagram chase to check that this is the multiplication-by- $p$ map on $Y^{Z}$. Indeed, the diagram of spectra
![img-65.jpeg](img-65.jpeg)
commutes from the naturality of the maps $\Delta^{(-)}$and $\nabla^{(-)}$. The fact that the diagonal map is an equivalence is most easily seen by remembering that finite direct sums of spectra are finite products, and in general we have an equivalence $\left(\lim Y_{i}\right)^{Z} \simeq \lim Y_{i}^{Z}$; see Exc.2.6.8 to come. As the upper-right composition is an equivalence by assumption, then the lower-left composition, ie, the multiplication-by- $p$ map on $Y^{Z}$ is also an equivalence.

Claim 2.6.5. There exists an $N \geqslant n$ such that $p^{N}$ acts by zero on $\mathbf{S} / p^{n}$.
In fact, we will see through the course of the proof below, that we can take $N=n$ when $p$ is odd and $N=n+1$ for even $p$.

Proof of Claim. The cofibre sequence for $\mathbf{S} / p^{n}$ induces the exact sequence of abelian groups

$$
\pi_{1} \mathbf{S} / p^{n} \simeq\left[\mathbf{S}[1], \mathbf{S} / p^{n}\right] \rightarrow\left[\mathbf{S} / p^{n}, \mathbf{S} / p^{n}\right] \rightarrow\left[\mathbf{S}, \mathbf{S} / p^{n}\right] \simeq \pi_{0} \mathbf{S} / p^{n} \simeq \mathbf{Z} / p^{n}
$$

where, as we have done previously, $[-,-]$ denotes mapping groups in hSp. The computation of $\pi_{0} \mathbf{S} / p^{n}$ comes from the same cofibre sequence and the facts that $\pi_{0} \mathbf{S} \simeq \mathbf{Z}$ and $\mathbf{S}$ is connective.

If $p \neq 2$ is odd, then we also can calculate that $\pi_{1} \mathbf{S} / p^{n}=0$ as we known from Algebraic Topology I that the first nontrivial $p$-power torsion in $\pi_{*} \mathbf{S}$ appears in degree $2 p-3$. In particular, we see that $\left[\mathbf{S} / p^{n}, \mathbf{S} / p^{n}\right]$ injects into a $p^{n}$-torsion abelian group, so the identity map on $\mathbf{S} / p^{n}$ is $p^{n}$-torsion. In other words, $p^{n}$ is the zero map on $\mathbf{S} / p^{n}$ when $p$ is odd.

If $p=2$ is even, then we can calculate $\pi_{1} \mathbf{S} / 2^{n} \simeq \mathbf{Z} / 2$ for all $n$ from the same long exact sequences and the fact that $\pi_{1} \mathbf{S} \simeq \mathbf{Z} / 2$ generated by the stable Hopf class $\eta: \mathbf{S}[1] \rightarrow \mathbf{S}$. In particular, from (2.6.6), we see that $\left[\mathbf{S} / 2^{n}, \mathbf{S} / 2^{n}\right]$ is at most a $2^{n+1}$-torsion group, so again, the identity on $\mathbf{S} / 2^{n}$ is $2^{n+1}$-torsion.

And we are done.

Exercise 2.6.7. Prove that given maps of spectra $X \xrightarrow{f} Y \xrightarrow{g} Z$ with $h=g f$, then there exists a natural diagram of spectra
![img-66.jpeg](img-66.jpeg)
where $C(-)$ denotes the obvious cofibre, and the outer circle is a cofibre sequence.
Exercise 2.6.8. Using a Yonda lemma argument, show that for any diagram of spectra $Y_{i}$ and any spectrum $Z$, there are natural equivalences of spectra $\left(\lim Y_{i}\right)^{Z} \simeq \lim Y_{i}^{Z}$ and $Z^{\text {colim } Y_{i}} \simeq$ $\lim Z^{Y_{i}}$.

As a result of the above model for the $p$-completion of a spectrum, we immediately obtain the following two algebrically intuitive corollaries: a criterion for checking if a spectrum is $p$-complete, and another model for the $p$-completion.

Corollary 2.6.9. A spectrum $X$ is p-complete if and only if $\lim \left(\cdots \xrightarrow{p} X \xrightarrow{p} X\right)$ vanishes.
Proof. Using Exc.2.6.8, we can rewrite the above limit as follows:

$$
\lim \left(\cdots \xrightarrow{p} X \xrightarrow{p} X\right) \simeq \lim \left(\cdots \xrightarrow{(\cdot p)^{*}} X^{\mathbf{S}} \xrightarrow{(\cdot p)^{*}} X^{\mathbf{S}}\right) \simeq X^{\operatorname{colim}\left(\mathbf{S} \xrightarrow{p} \mathbf{S} \xrightarrow{p}\right)} \simeq X^{\mathbf{S}\left[\frac{1}{p}\right]}
$$

As this spectrum is the fibre of the map $X \rightarrow X_{p}^{<}$from Pr.2.6.2, we see that $X$ is $p$-complete, ie, equivalent to its $p$-completion, if and only if the above limit vanishes.

Corollary 2.6.10. For any spectrum $X$, the natural map $X \rightarrow \lim X / p^{n}$ is a p-completion.
This hearkens back to the algebraic fact that the $p$-completion of $\mathbf{Z}$, the $p$-adic integers $\mathbf{Z}_{p}^{<}$, can be written as $\lim \mathbf{Z} / p^{n}$.

Proof. Again applying Pr.2.6.2 and Exc.2.6.8, we have the natural equivalences

$$
X_{p}^{<} \simeq X^{\mathbf{S} / p^{c c}[-1]} \simeq \lim X^{\mathbf{S} / p^{n}[-1]} \simeq \lim X / p^{n}
$$

Above we have used the equivalence $X / p^{n} \simeq X^{\mathbf{S} / p^{n}[-1]}$, but this comes from the diagram of spectra
![img-67.jpeg](img-67.jpeg)

The diagram commutes for the same reason that (2.6.4) commutes, let us not repeat the argument here. The upper row is a cofibre sequence by definition, and the lower row is a cofibre sequence induced by the cofibre sequence in the domain variable; see Exc.2.3.17. The diagram is therefore a commutative diagram of cofibre sequences where two maps are equivalences, so the third is by the five-lemma.

We leave it as an exercise to compute the homotopy groups of the $p$-completion of a spectrum in terms of the homotopy groups of the spectrum.
Exercise 2.6.11. Show that for a spectrum $X$, there is a short exact sequence of abelian groups

$$
0 \rightarrow \operatorname{Ext}\left(\mathbf{Z} / p^{\infty}, \pi_{*} X\right) \rightarrow \pi_{*}\left(X_{p}^{\wedge}\right) \rightarrow \operatorname{Ab}\left(\mathbf{Z} / p^{\infty}, \pi_{*-1} X\right) \rightarrow 0
$$

One can now use this to compute the homotopy groups of $\mathbf{S}_{p}^{\wedge}$ and $\mathrm{KU}_{p}^{\wedge}$, for example.
Exercise 2.6.12. Let us say that an abelian group $A$ is derived $p$-complete if the associated Eilenberg-Mac Lane spectrum is $p$-complete in Sp. Show that $A$ is derived $p$-complete if the natural map $A \rightarrow \operatorname{Ext}\left(\mathbf{Z} / p^{\infty}, A\right)$ is an equivalence - the latter is the classical algebraic definition of derived $p$-complete. Then show that a spectrum $X$ is $p$-complete if and only if all of its homotopy groups $\pi_{d} X$ are derived $p$-complete.

One reason why we want to study $p$-completions of spectra, is because in a certain structured sense, all spectra are comprised of their $p$-complete parts and their localisation away from $p$ part, plus a little gluing data. More specifically, we have the following statement.
Theorem 2.6.13. For all spectra $X$, the natural commutative square
![img-68.jpeg](img-68.jpeg)
induced by the natural completion map $X \rightarrow X_{p}^{\wedge}$ and the natural localisation map $X \rightarrow X\left[\frac{1}{p}\right]$, is a pullback and hence also a pushout.

Let us quickly point out that the order of localisation away from $p$ and $p$-completion is important. Using Cor.2.6.10, it is easy to see that the $p$-completion of $X\left[\frac{1}{p}\right]$ vanishes.

Proof. Let us write $X \rightarrow P$ for the natural map from $X$ into the pullback of the above square. We want to show that the fibre of this map, which we will write as $F$, is zero. To see this, let us first note that $F$ is $\mathbf{S} / p$-acyclic. To see this, we first smash all of the data we have so far with $\mathbf{S} / p$ :
![img-69.jpeg](img-69.jpeg)

The fibre sequence remains a fibre sequence, as fibre sequences are cofibre sequences (Th.2.1.18) and tensoring preserves colimits (Rmk.2.3.5), and similarly, the pullback remains a pullback after tensoring with $\mathbf{S} / p$. Notice that the spectra in the lower row of the above square both vanish for the same reasons used in the proof of Pr.2.6.2 to see that $X^{\mathbf{S}\left[\frac{1}{p}\right]} \otimes \mathbf{S} / p^{n}$ vanishes, as $p$ acts both invertibly and nilpotently. As $f$ is an equivalence, and the above square is a pullback, then $g$ is also an equivalence; see Exc.2.6.15. The map $h$ is an equivalence as the map $E \rightarrow E_{p}^{ \pm}$is per-definition a $\mathbf{S} / p$-equivalence, hence we see that $i$ is also an equivalence. It follows that $F \otimes \mathbf{S} / p$ vanishes. The following is a general claim about $\mathbf{S} / p$-acyclic spectra. Claim 2.6.14. If $Y$ is $\mathbf{S} / p$-acyclic, then $p$-acts invertibly on $Y$.

Proof of Claim. This follows immediately from the cofibre sequence

$$
Y \xrightarrow{p} Y \rightarrow Y / p \simeq Y \otimes \mathbf{S} / p=0
$$

It follows that $p$ acts invertibly on $F$, so the natural map $F \rightarrow F\left[\frac{1}{p}\right]$ is an equivalence. However, we will shortly show that $F\left[\frac{1}{p}\right]$ vanishes. Indeed, consider the diagram induces by smashing our desired square and the fibre sequence defining $F$ with $\mathbf{S}\left[\frac{1}{p}\right]$, keeping in mind this is the same as simply localising away from/inverting $p$ :
![img-70.jpeg](img-70.jpeg)

As inverting $p$ is an idempotent operation, this was discussed for rationalisation in Pr.2.5.4 and the preceding discussion, we see that the lower row of the square remains unchanges. The map $f$ is now an equivalence as it is the identity, so by base-change (Exc.2.6.15) $g$ is also an equivalence. By construction, the map $h$ is an equivalence, ie, because $X \rightarrow X\left[\frac{1}{p}\right]$ is the natural map into the localisation of $p$ away from $p$, so $i$ is an equivalence too. As a consequence $F\left[\frac{1}{p}\right]$ and $F$ both vanish, and the desired square is a pullback.

Exercise 2.6.15. Show that given a pullback (equivalently a pushout) of spectra
![img-71.jpeg](img-71.jpeg)
then $f$ is an equivalence if and only if $g$ is an equivalence. Hint: show that there is a MeyerVietoris long exact sequence

$$
\cdots \rightarrow \pi_{*} W \rightarrow \pi_{*} X \oplus \pi_{*} Y \rightarrow \pi_{*} Z \rightarrow \pi_{*-1} W \rightarrow \cdots
$$

There is also the following generalisation of Th.2.6.13; we will see another proof in $\S 3$.

Exercise 2.6.16. For any spectrum $X$, the natural commutative square
![img-72.jpeg](img-72.jpeg)
where the products are taken over all primes numbers $p$, is a pullback.
These kinds of arithmetic fracture squares cut-up spectra into more manageable smaller pieces. One of the main goals of chromatic homotopy theory is to refine this, and further cut $X_{p}^{\wedge}$ into even smaller, and hopefully even more manageable, pieces.

End of lecture 13

# 2.7 Outlook (not discussed in lectures) 

There is so much more we could say about spectra at this stage in these lectures. Rather than try to list all of these potential future directions, let us mention a few places where spectra naturally occur: in algebraic $K$-theory, and as an environment with a deeper base than the integers $\mathbf{Z}$.

The (complex) topological $K$-theory $K(X)$ of a compact Hausdorff space $X$ is defined as the group completion of isomorphism classes of finite dimensional vector bundles on $X$. Group completion is a natural process of taking a commutative monoid $M$ and producing a group $M^{\text {grp }}$ by adding all inverses. For example, the group completion of the natural numbers is precisely the group of integers. ${ }^{8}$ We do this because groups are much nicer to work with than monoids, both theoretically and computationally-maps of monoids with zero kernel need not be injective, such as the addition map $\mathbf{N} \times \mathbf{N} \rightarrow \mathbf{N}$, for example. The addition on $K(X)$ comes from the direct sum of vector bundles of vector bundles, and in fact this group has a ring structure, natural in maps of spaces $Y \rightarrow X$, given by the tensor product of vector bundles.

This definition gives a cohomology theory as there is a "Poincaré lemma" for $K(X)$, meaning that the map induced by the projection $K(X) \rightarrow K\left(X \times \Delta^{1}\right)$ is an isomorphism, and also thanks to Bott periodicity which states that there is a chosen isomorphism $K(X \times$ $\left.S^{2}\right) \simeq K(X) \otimes K\left(S^{2}\right)$. Moreover, the study of vector bundles, as well as Bott periodicity, tell us that the spectrum KU representing this cohomology theory has level-wise animæ ( $\mathbf{Z} \times \mathrm{BU}, \mathrm{U}, \mathbf{Z} \times \mathrm{BU}, \mathrm{U}, \ldots$ ); this was already mentioned in Eg.2.2.19.

There is another, more sophisticated way to construct KU, which naturally produces not just a spectrum KU , but also a natural $\mathbf{E}_{\infty}$-structure on KU -we simply need to apply the

[^0]
[^0]:    ${ }^{8}$ The reader might want to think of some examples of group completions such that the natural map $M \rightarrow$ $M^{\text {grp }}$ is not injective - this construction can be quite destructive.

above procedure in an $\infty$-categorical setting; the reference for this construction is [GGN15]. First, we take the topologically enriched category of finite dimensional complex vector spaces $\operatorname{Vect}_{\mathbf{C}}$. Taking the topological coherent nerve, so simply the simplicial coherent nerve of Df.1.3.17 after applying Sing to all of the mapping spaces, we obtain an $\infty$-category which we will also denote by $\operatorname{Vect}_{\mathbf{C}}$. Keeping track of multiplicative structures, $\operatorname{Vect}_{\mathbf{C}}$ naturally inherits the structure of a symmetric monoidal $\infty$-category á la $\S 1.9$ in two different ways: it has both a monoidal structure coming from the direct sum of vector spaces as well as one coming from the tensor product. Using the direct sum monoidal structure, we see that the core $\operatorname{Vect}_{\mathbf{C}}^{\times}$, so the largest anima inside $\operatorname{Vect}_{\mathbf{C}}$, is actually an $\mathbf{E}_{\infty}$-object in $\mathscr{A} \mathrm{n}$, which are usually called $\mathbf{E}_{\infty}$-monoids. We now want to take a kind of "higher categorical group completion". To do this sensibly, let us note that the group completion functor mentioned above, is the left adjoint to the inclusion of abelian groups into the category of abelian monoids. The inclusion of grouplike $\mathbf{E}_{\infty}$-monoids, so $\mathbf{E}_{\infty}$-monoids $X$ such that the induced monoid structure on $\pi_{0} X$ just happens to be a group structure, ie, inverses happen to exist, into $\mathbf{E}_{\infty}$-monoids also has a left adjoint. We then define the space $\left(\operatorname{Vect}_{\mathbf{C}}^{\times}\right)^{\text {grp }}$ as the application of this higher group completion $(-)^{\text {grp }}$, so the aforementioned left adjoint, to $\operatorname{Vect}_{\mathbf{C}}^{\times}$.

Unwinding everything we have done, one can show that there is an equivalence $\left(\operatorname{Vect}_{\mathbf{C}}^{\times}\right)^{\text {grp }} \simeq$ $\mathbf{Z} \times \mathrm{BU}$, so it does not seem like we have done much. A classical theorem, now in higher categorical disguise, tells us that functor $\Omega^{\infty}: \mathrm{Sp}^{\mathrm{cn}} \rightarrow \operatorname{CAlg}(\mathscr{A} \mathrm{n})^{\text {grp }}$ from the $\infty$-category of connective spectra to that of grouplike $\mathbf{E}_{\infty}$-monoids is actually equivalence. The monoid structure on $\Omega^{\infty} X$ comes from the fact that spectra have a natural $\mathbf{E}_{\infty}$-structure from the fact that Sp is stable and which is grouplike as $\pi_{0} \Omega^{\infty} X \simeq \pi_{0} X$ is an abelian group. The reason we restrict to connective spectra is because $\Omega^{\infty} X$ of a spectrum $X$ can never know about the lower homotopy groups of $X$-for example, $\left.\Omega^{\infty}(\mathbf{Z}[-1]) \simeq * \simeq \Omega^{\infty}\left(\mathbf{F}_{2}[-1]\right)\right)$-so this functor is clearly not conservative on all spectra. The inverse to $\Omega^{\infty}$ in this case is given by deloopings. There is a functor $B: \operatorname{CAlg}(\mathscr{A} \mathrm{n})^{\text {grp }} \rightarrow \operatorname{CAlg}(\mathscr{A} \mathrm{n})^{\text {grp }}$ called the bar construction, which agrees with the classifying space functor on topological groups, with the property that there is a natural equivalence $\Omega B X \simeq X$. The inverse of $\Omega^{\infty}$ then sends $X$ to $\left(X, B X, B^{2} X, \ldots\right)$ with structure maps $\Omega B^{n+1} X \simeq B^{n} X$ coming from the natural equivalence above. All of this applied to $\left(\operatorname{Vect}_{\mathbf{C}}^{\times}\right)^{\text {grp }}$, then leads us to the connective spectrum ku. To obtain KU, we notice that there is a class $\beta \in \pi_{2} \mathrm{ku}$ associated to Bott periodicity, and then $\mathrm{KU}=\mathrm{ku}\left[\beta^{ \pm}\right]$. Moreover, the work of [GGN15] shows that this process can be enhanced to produce $\mathbf{E}_{\infty}$-rings ku and KU. Simply put, we have the following procedure:

$$
\operatorname{Vect}_{\mathbf{C}} \rightsquigarrow \operatorname{Vect}_{\mathbf{C}}^{\times} \rightsquigarrow \rightarrow\left(\operatorname{Vect}_{\mathbf{C}}^{\times}\right)^{\text {grp }} \rightsquigarrow \rightarrow \mathrm{ku}
$$

This is also exactly how one can define algebraic $K$-theory. Simply take a discrete commutative ring $R$, consider it as an $\mathbf{E}_{\infty}$-ring in the $\infty$-category of spectra, let $\operatorname{Perf}_{R}$ be the $\infty$-category ${ }^{9}$ of compact objects in $\operatorname{Mod}_{R}(\mathrm{Sp})=\operatorname{Mod}_{R}$, and define $K(R)$ as the connective spectrum associated to the grouplike $\mathbf{E}_{\infty}$-monoid $\left(\operatorname{Perf}_{R}^{\times}\right)^{\text {grp }}$.

# Chapter 3 

## Chromatic homotopy theory

The $\infty$-category of spectra Sp is much more nicely behaved than the 1-category Cohom of cohomology theories - one cannot even taken quotients in this category!-but is still a complicated object. At the end of the day, chromatic homotopy theory throws a filtration on Sp , denoted by $\mathrm{Sp}_{p, n}$ where $p$ is a prime and $n$ a nonnegative integer, with deep connections to arithmetic geometry. The chromatic perspective goes back to results of Adams [Ada66], Landweber [Lan76], Miller-Ravenel-Wilson [MRW77], Quillen [Qui69], and Morava [Mor85], just to mention a few, but there has been a lot of work in the past 20-25 years or so on the subject as well - one of the biggest theorems in topology and geometry last year is theorem purely in the world of chromatic homotopy theory; see [Har23]!

Our goal of this section is to introduce many of the main characters in chromatic homotopy theory (such as all of the titles of the subsections below) and the foundations of the subject. We will mostly be drawing from [Ada74, §II], [Lura], and [Mei19], but other sources include [Pet19], [Pst21], [Rog23], and [DLS19].
Warning 3.0.1. Similar to how we loosened our $\infty$-categorical arguments in $\S 2$, assuming the reader can fill in, or at least believe the existence of, the missing details, in this section we will loosen our arguments involving spectra, and assume the reader has some familiarity with the content of $\S 2$.

### 3.1 Complex-oriented cohomology theories

It all begins with the following flow of information: from a complex-oriented cohomology theory, we obtain a formal group law. Let's get started with the former.

Definition 3.1.1. Let $E$ be a unital spectrum, meaning a spectrum $E$ equipped with a map $\mathbf{S} \rightarrow E$, or equivalently, an object in the slice $\infty$-category $\mathrm{Sp}_{\mathbf{S} /}$. A complex orientation for $E$ is a choice of factorisation $x_{E}: \Sigma^{\infty} \mathbf{C P}^{\infty}[-2] \rightarrow E$ of this chosen unit map $\mathbf{S} \rightarrow E$ through the natural map

$$
\mathbf{S} \simeq \Sigma^{\infty} \mathbf{C P}^{1}[-2] \rightarrow \Sigma^{\infty} \mathbf{C P}^{\infty}[-2]
$$

induced by the inclusion of animæ $\mathbf{C P}^{1} \rightarrow \mathbf{C P}^{\infty}$. We say that $E$ is complex-orientable if a complex orientation exists, and that $E$ is complex-oriented if it comes with a given $x_{E}$.

If $E$ is a homotopy commutative ring spectrum, then part of this data is a unit map $\mathbf{S} \rightarrow E$. The unital spectra we consider will often come with a chosen homotopy commutative multiplication, and this assumption will also be useful in practice.

There are other definition of complex orientations from the literature, for example in [Ada74, §II.2], which are equivalent to that above. The following exercise gives an example of this.

Exercise 3.1.3. Let $E$ be a homotopy commutative ring spectrum. Show that a complex orientation for $E$ is precisely an element $x_{E} \in \widetilde{E}^{2}\left(\mathbf{C P}^{\infty}\right)$ such that restriction along the inclusion $S^{2} \simeq \mathbf{C P}^{1} \rightarrow \mathbf{C P}^{\infty}$ sends $x_{E}$ to the unit in the ring $\widetilde{E}^{2}\left(S^{2}\right) \simeq \pi_{0} E$.

In light of this exercise, we will freely move between the two interpretations of complex orientations above. Now onto some examples.
Example 3.1.4. Consider the integral Eilenberg-Mac Lane spectrum $H \mathbf{Z}$. We know that the group $H^{2}\left(\mathbf{C P}^{n} ; \mathbf{Z}\right)$, reduced or not, is isomorphic to $\mathbf{Z}$ for each $1 \leqslant n \leqslant \infty$, and we can even see that we can choose a class $x_{\mathbf{Z}} \in H^{2}\left(\mathbf{C P}^{\infty} ; \mathbf{Z}\right)$ which restricts to generators of these $\mathbf{Z}$ for each $n<\infty$. In fact, there is only two potential choices of such an $x_{\mathbf{Z}}$, depending on which orientation we consider for $\mathbf{C P}^{\infty}$. Let us just choose one of them and fix it forever now - it is with this fixed class that we consider $H \mathbf{Z}$ to be complex-oriented. For each commutative ring $R$, there is a unique map $\mathbf{Z} \rightarrow R$ which induces a map of spectra $f: H \mathbf{Z} \rightarrow H R$. We claim that image of $x_{\mathbf{Z}}$ under $f$, which we denote by $x_{R} \in H^{2}\left(\mathbf{C P}^{\infty} ; R\right)$, is a complex-orientation for $H R$-indeed, this follows from the usual computation of $H^{*}\left(\mathbf{C P}^{n} ; R\right)$ for a general ring $R$ from Topology II, for example. It is with these complex-orientations $x_{R}$ that we consider each $H R$ to be complex-oriented.
Example 3.1.5. Although we a priori only know that for a finite CW-complex $X$, the group $\mathrm{KU}^{0}(X)$ can be described as the group completion of the monoid of isomorphism classes of finite dimensional complex vector bundles on $X$ under direct sum. It turns out that this description also holds for $X=\mathbf{C P}^{\infty}$; as an exercise, try to prove this from Pr.3.1.11. In particular, we can pick out an element $\gamma-1$ inside $\mathrm{KU}^{0}\left(\mathbf{C P}^{\infty}\right)$, where $\gamma$ is the tautological line bundle on $\mathbf{C P}^{\infty}$. This element actually lies in $\widetilde{\mathrm{KU}}^{0}\left(\mathbf{C P}^{\infty}\right)$, as both $\gamma$ and 1 are line bundles. Indeed, we can view $\widetilde{\mathrm{KU}}^{0}\left(\mathbf{C P}^{\infty}\right)$ the subgroup of $\mathrm{KU}^{0}\left(\mathbf{C P}^{\infty}\right)$ of virtual vector bundles of virtual dimension zero. ${ }^{1}$ Now, the restriction of $\gamma-1$ inside $\widetilde{\mathrm{KU}}^{0}\left(S^{2}\right) \simeq \pi_{2} \mathrm{KU}$ is precisely the Bott element $u$ by construction; see Eg.2.2.19. Also notice that $\pi_{*} \mathrm{KU} \simeq \mathrm{KU}^{-*}$, so this Bott element lives in cohomological dimension -2 , and its inverse lives in cohomological dimension 2. We finally settle on $x_{\mathrm{KU}}=\frac{\gamma-1}{u}$ inside $\widetilde{\mathrm{KU}}^{2}\left(\mathbf{C P}^{\infty}\right)$ as our complex-orientation for KU , using the fact that

[^0]
[^0]:    ${ }^{1}$ This is not immediately clear, as we defined $\widetilde{\mathrm{KU}}^{0}(X)=\left[\Sigma^{\infty} X, \mathrm{KU}\right]$ for a pointed anima $X$. However, it follows from the definitions that this group can be naturally identified with the kernel of the map $\mathrm{KU}^{0}(X) \rightarrow$ $\mathrm{KU}^{0}(*) \simeq \mathbf{Z}$ induced by the inclusion of the base-point of $X$, and this map can also be identified with the map sending a virtual vector bundle to its virtual dimension.

$\mathrm{KU}^{*}$ acts on $\widetilde{\mathrm{KU}}^{*}\left(\mathbf{C P}^{\infty}\right)$. This restricts correctly, as we have

$$
i^{*}\left(x_{\mathrm{KU}}\right)=\frac{i^{*}(\gamma-1)}{u}=\frac{u}{u}=1
$$

where $i: \mathbf{C P}^{1} \rightarrow \mathbf{C P}^{\infty}$ is the usual inclusion. The first equality from the fact that $i^{*}$ is a map of $\mathrm{KU}^{*}$-modules, so it commutes with the action of $u$, and the second equality from the definition of $u=i^{*}(\gamma)-1$ and the fact that $i^{*}$ is a ring map.
Example 3.1.6. Recall our construction of MU from Eg.2.2.21

$$
\mathrm{MU}=\operatorname{colim}(M(0) \rightarrow M(1) \rightarrow M(2) \rightarrow \cdots) \quad M(n)=\Omega^{2 n} \Sigma^{\infty} T_{n}
$$

where $T_{n}$ is the Thom construction applied to the universal bundle $\gamma_{n}$ living over $\mathrm{BU}(n)$. Notice that $M(0)=\Sigma^{\infty} S^{0}$ is the sphere spectrum, and that $M(1)$ is $\Sigma^{\infty} \mathbf{C P}^{\infty}[-2]$. From this description, it is easy to see that MU has a chosen complex orientation, as by definition the map $M(0) \rightarrow M(1)$ is the map (3.1.2) in the reinterpretation of what a complex orientation is above (Exc.3.1.3)—in Exc.3.3.13 we will discuss why MU is a homotopy commutative ring spectrum.

Not all spectra are complex-orientable though.
Non-example 3.1.7. We claim the sphere spectrum $\mathbf{S}$ is not complex-orientable. Indeed, consider the long exact sequence on $\mathbf{S}$-cohomology induce by the attaching map for $\mathbf{C P}^{2}$, ie, the (unstable) Hopf map $\eta: S^{3} \rightarrow S^{2}$ :

$$
\cdots \rightarrow \widehat{\mathbf{S}}^{2}\left(\mathbf{C P}^{2}\right) \xrightarrow{\iota^{*}} \widehat{\mathbf{S}}^{2}\left(S^{2}\right) \xrightarrow{\eta^{*}} \widehat{\mathbf{S}}^{2}\left(S^{3}\right) \rightarrow \cdots
$$

From Topology II, we know that $\eta \in \pi_{1} \mathbf{S}$, the image of the (unstable) Hopf map $\eta: S^{3} \rightarrow S^{2}$, is nonzero in the stable homotopy groups of spheres. This implies that the right-hand map $\eta^{*}$, which can be identified with the multiplication by $\eta$ map $\pi_{0} \mathbf{S} \rightarrow \pi_{1} \mathbf{S}$ is nonzero. In particular, it sends both of the units $\pm 1$ of

$$
\widehat{\mathbf{S}}^{2}\left(S^{2}\right) \simeq \pi_{0} \mathbf{S} \simeq \mathbf{Z}
$$

to the nonzero elements $\pm \eta$ of $\pi_{1} \mathbf{S}$ (which happens to be $\mathbf{Z} / 2 \mathbf{Z}$, although this is not important right now). By exactness, this means there is no class in $\widehat{\mathbf{S}}^{2}\left(\mathbf{C P}^{2}\right)$ which can hit a unit in $\pi_{0} \mathbf{S}$, hence $\mathbf{S}$ cannot be complex-orientable.
Exercise 3.1.8. Let $E$ be a homotopy commutative ring spectrum such that the unit map $\mathbf{S} \rightarrow E$ sends $\eta$ to a nonzero class in $\pi_{1} E$-we say that $E$ detects $\eta$. Show that $E$ is not complex-orientable.

For example, it can be shown that KO detects $\eta$ (as does TMF, $\mathrm{TMF}_{0}(3)$, any $C_{2}$-fixed points of Morava $E$-theories of positive height with respect to the stable Adams operation $\psi^{-1}$, etc.).

In fact, if we demand that the odd homotopy groups of a homotopy commutative ring spectrum vanish, then we obtain complex-orientablity.

Proposition 3.1.9. Let $E$ be a spectrum with a unit map $\mathbf{S} \rightarrow E$. If $\pi_{d} E$ vanishes for all positive odd $d$, then $E$ is complex-orientable. In particular, even homotopy commutative ring spectra $E$, so spectra with $\pi_{d} E=0$ for all odd integers $d$, are complex orientable.

Note that this proposition does not give us a canonical choice of complex orientation, only the existence of such an orientation.

Exercise 3.1.10. Show that not all complex-oriented cohomology theories $E$ need have $\pi_{d} E=0$ for positive odd $d$.

To prove this statement, we need to know something about the cohomology of a colimit of animæ in terms of the limit of the the cohomology groups. This tool is called the Milnor $\lim ^{1}$ exact sequence, for obvious reasons.

Proposition 3.1.11. Let $X_{0} \rightarrow X_{1} \rightarrow \cdots$ be a sequences of spectra, and write $X$ for its colimit. For any spectrum $E$, there is a natural short exact sequence of graded abelian groups

$$
0 \rightarrow \lim ^{1} E^{*-1}\left(X_{i}\right) \rightarrow E^{*} X \rightarrow \lim E^{*} X_{i} \rightarrow 0
$$

This is most practical if $X=\Sigma^{\infty} C$ or $\Sigma_{+}^{\infty} C$ for an anima $C$ and the filtration $X_{n}$ is given by the suspension spectrum of a CW-filtration of $C$. This is the situation we will consider for $C=\mathbf{C P}^{\infty}$ with its usual CW-filtration given by inclusions of complex projective spaces.

As good students who just took a class on spectral sequences, you might expect a $\lim ^{*}$ spectral sequence or something of this nature. However, all of the higher derived limit terms vanish in the category of abelian groups. If we wanted to play the same sort of game in the category of $R$-modules for some base ring $R$, we would find ourselves in a different situationthis seldom comes up in practice though. ${ }^{2}$

Proof. The first observation to make is that the sequential colimit $X$ can be rewritten as the coequaliser of two maps

$$
\bigoplus_{n \geqslant 0} X_{n} \rightarrow \bigoplus_{n \geqslant 0} X_{n}
$$

the first given by the identity id and the second $\sigma$ given by structure maps $X_{n} \rightarrow X_{n+1}$-the reader is asked to prove this 1-categorically if they haven't seen this before; see Exc.3.1.12 below. As Sp is preadditive (this is what Cor.2.1.24 means) and there exists a $[-1]$-map (see Rmk.2.1.26), we see that there is a cofibre sequence of spectra

$$
\bigoplus_{n \geqslant 0} X_{n} \xrightarrow{\sigma-\mathrm{id}} \bigoplus_{n \geqslant 0} X_{n} \rightarrow X
$$

[^0]
[^0]:    ${ }^{2}$ This does not totally escape stable homotopy theory though. Given an $\mathbf{E}_{1}$-ring $R$ and a left $R$-module $M$ such that $\pi_{*} M$ is flat as a left $\pi_{*} R$-module, then we can write $\pi_{*} M$ as a filtered colimit of finite free $\pi_{*} R$-modules by Lazard's theorem. Trying to reconstruct $M$ from a filtered colimit of finite free $R$-modules seems to involve some intricate interplay between higher limit terms for the associated cofiltered limit in the category of (graded) $R$-modules.

As $E$-cohomology takes cofibre sequences of spectra to long exact sequences and using the product axiom, we obtain the long exact sequence of graded abelian groups

$$
\cdots \rightarrow \prod_{n \geqslant 0} E^{*-1} X_{i} \xrightarrow{\sigma^{*}-\mathrm{id}} \prod_{n \geqslant 0} E^{*-1} X_{i} \rightarrow E^{*} X \rightarrow \prod_{n \geqslant 0} E^{*} X_{i} \xrightarrow{\sigma^{*}-\mathrm{id}} \prod_{n \geqslant 0} E^{*} X_{i} \rightarrow \cdots
$$

Using the dual to our rewriting of a sequential colimit as a cokernel of maps between coproducts, we see the kernel of the right-hand $\sigma^{*}-\mathrm{id}$ is the limit $\lim E^{*} X_{i}$. By definition the cokernel of the left-hand $\sigma^{*}-\mathrm{id}$ is the desired $\lim ^{1}$-term; this is standard homological algebra, have a look at [Wei94, §3.5], if you want some more details.

Exercise 3.1.12. Let $C$ be an additive ${ }^{3}$ category with all colimits. Show that the colimit $X$ of a sequence

$$
X_{0} \rightarrow X_{1} \rightarrow X_{2} \rightarrow X_{3} \rightarrow \cdots
$$

is isomorphic to the coequaliser of the two maps

$$
\bigoplus_{n \geqslant 0} X_{n} \rightarrow \bigoplus_{n \geqslant 0} X_{n}
$$

the first given by the identity id and the second $\sigma$ given by structure maps $X_{n} \rightarrow X_{n+1}$.
Exercise 3.1.13. Show that given a diagram of abelian groups $\cdots A_{n} \rightarrow A_{n-1} \rightarrow \cdots \rightarrow A_{0}$ such that each $A_{i+1} \rightarrow A_{i}$ is surjective, then $\lim ^{1} A_{i}=0$.

Let us quickly remind the reader that such a consideration for homology is not necessary. Exercise 3.1.14. Let $X$ be a filtered colimit of spectra $X_{i}$ and $E$ be another spectrum. Show that the natural map of graded abelian groups

$$
\operatorname{colim} E_{*} X_{i} \rightarrow E_{*} X
$$

is an equivalence.
This is one reason why when people deal with cohomology theories they often insist on using finite CW-complex or impose some other finiteness condition, where as for homology theories, such restrictions are not necessary.

Proof of Pr.3.1.9. Let us think for a second what we have, and what we want. We have a unit, $1 \in \pi_{0} E \simeq \widetilde{E}^{2}\left(\mathbf{C P}^{1}\right)$, and we want to lift this to an element $x_{E}$ in $\widetilde{E}^{2}\left(\mathbf{C P}^{\infty}\right)$. By Pr.2.3.23, we have long exact sequences on (reduced) $E$-cohomology coming from the cofibre sequence of animæ $S^{2 n+1} \rightarrow \mathbf{C P}^{n} \rightarrow \mathbf{C P}^{n+1}$ :

$$
\cdots \rightarrow \widetilde{E}^{2}\left(\mathbf{C P}^{n+1}\right) \rightarrow \widetilde{E}^{2}\left(\mathbf{C P}^{n}\right) \rightarrow \widetilde{E}^{2}\left(S^{2 n+1}\right) \simeq \pi_{2 n-1} E \rightarrow \cdots
$$

[^0]
[^0]:    ${ }^{3} \mathrm{~A}$ category $C$ is preadditive if it has a zero object, finite products and coproducts, and for any pair of objects $X, Y$ in $C$, the natural map $X \sqcup Y \rightarrow X \times Y$ is an equivalence. A preadditive category $C$ is additive if the abelian hom-monoids, with monoidal structure given by Rmk.2.1.25, are in fact abelian groups. Note this these are all conditions on a category, not data.

As the homotopy groups $\pi_{2 n-1} E=0$ for all positive $n$, we see that there is a system of $x_{E}(n)$ inside $\widetilde{E}^{2}\left(\mathbf{C P}^{n}\right)$ which restrict to each other with $x_{E}(1)$ being the unit 1 inside $\widetilde{E}^{2}\left(S^{2}\right) \simeq \pi_{0} E$. We now consider the Milnor $\lim ^{1}$ sequence associated to $\mathbf{C P}^{\infty}$ and $E$ :

$$
0 \rightarrow \lim ^{1} \widetilde{E}^{1}\left(\mathbf{C P}^{n}\right) \rightarrow \widetilde{E}^{2} \mathbf{C P}^{\infty} \rightarrow \lim \widetilde{E}^{2} \mathbf{C P}^{n} \rightarrow 0
$$

We have an element in the right-hand group, so to recover an complex-orientation in the middle group, it suffices to show that the $\lim ^{1}$-term on the left vanishes. This is clear though, as by continuing the sequence (3.1.15) to the left and using induction, we also see that the groups $\widetilde{E}^{1}\left(\mathbf{C P}^{n}\right)$ all vanish, and we are done.

Complex-oriented cohomology theories are really useful to have around, as they allow for various arguments from singular cohomology or $K$-theory to go through unchanged.

Proposition 3.1.16. Let $E$ be a (nonzero) complex-oriented cohomology theory (with implicit complex-orientation $x_{E}$ ). Then for any positive integer $n$, the maps of graded $E^{*}$-algebras

$$
E^{*}[x] / x^{n+1} \xrightarrow{x \mapsto x_{E} \mid \mathbf{C P}^{n}} E^{*}\left(\mathbf{C P}^{n}\right) \quad E^{*}\llbracket x \rrbracket \xrightarrow{x \mapsto x_{E}} E^{*}\left(\mathbf{C P}^{\infty}\right)
$$

are isomorphisms. ${ }^{4}$
There is a canonical warning to make before moving on.
Warning 3.1.17. We learned in Topology II that there is an isomorphism of graded rings $H^{*}\left(\mathbf{C P}^{\infty} ; R\right) \simeq R[x]$ for any ring $R$, where $|x|=2$. This fact is also implied by combining Eg.3.1.4 and Pr.3.1.16. On the other hand, we also claim that $H^{*}\left(\mathbf{C P}^{\infty} ; R\right) \simeq R \llbracket x \rrbracket$. However, we all know that $R[x]$ and $R \llbracket x \rrbracket$ are different rings! What is going on then? Well, both are true, as the two rings $R[x]$ and $R \llbracket x \rrbracket$ are isomorphic as graded rings as long as $x$ is in nonzero degree. This is because there is a map of rings $R[x] \rightarrow R \llbracket x \rrbracket$ which is an isomorphism on each graded piece, ie, each $R$-submodule spanned by monomials of the form $r x^{n}$ for some $r \in R$ and some fixed nonnegative integer $n$. This does not contradict the fact that as rings these two objects differ: the two functors from graded rings to rings $\oplus$ and $\prod$, one given by sending a graded ring to the direct sum of its graded pieces and the other to the product of its graded pieces, send the above isomorphic graded rings to $R[x]$ and $R \llbracket x \rrbracket$, respectively.

This proof is classical; see [Ada74, Lm.2.5] or [Swi02, Th.16.29].
Proof of Pr.3.1.16. To start with the finite dimensional computation, we use the (unreduced) Atiyah-Hirzebruch spectral sequence of Th.2.4.1. In this case we have a spectral sequence of the form

$$
E_{2}^{p, q}=H^{p}\left(\mathbf{C P}^{n} ; \pi_{-q} E\right) \Longrightarrow E^{p+q}\left(\mathbf{C P}^{n}\right)
$$

This is a spectral sequence of $\pi_{*} E$-modules, and taking into account multiplicative structure too, we can write the $E_{2}$-page as the bigraded $\pi_{*} E$-algebra $\pi_{*} E[x] / x^{n+1}$ with $|x|=(2,0)$.

[^0]
[^0]:    ${ }^{4}$ There is a lovely alternative proof of this fact, not relying on the Atiyah-Hirzebruch spectral sequence, which uses the interpretation of a complex-oriented cohomology theory as giving Thom isomorphisms associated to complex vector bundles, and the fact that $\mathbf{C P}^{n+1}$ is the Thom construction of the tautological bundle over $\mathbf{C P}^{n}$; see the proof of [Mei19, Pr.2.29], for example. Lurie also argues without a direct AHSS, but essentially unrolls an AHSS argument with some formal stable homotopy theory; see [Lura, Lec.4].

In particular, if we can show that for this particular $x$ we have $d_{r}(x)=0$ for all $r \geqslant 2$, then we would know that the spectral sequence only has trivial differentials by the Leibniz rule and $\pi_{*} E$-linearity. To see that $x$ is a permanent cycle, we want to argue that this element is the only element that could detect the restriction of the complex orientation $x_{E} \in E^{2}\left(\mathbf{C P}^{\infty}\right)$ to $x_{n} \in E^{2}\left(\mathbf{C P}^{n}\right)$-here we are using unreduced cohomology, but a choice of base-point of an anima $X$ yields a splitting $E^{*}(X) \simeq \widetilde{E}^{*}(X) \oplus E^{*}(*)$. We know that $x_{n}$ is nonzero as it further restricts to the nonzero unit $1 \in E^{0}(*)$.

To see that $x$ has to detect $x_{n}$, we note that the groups $H^{p}\left(\mathbf{C P}^{n} ; \pi_{-p-2} E\right)$ for $p \geqslant 0$ are those converging to $E^{2}\left(\mathbf{C P}^{n}\right)$. The map $i_{n}: \mathbf{C P}^{1} \rightarrow \mathbf{C P}^{n}$ induces a morphism $E^{*}\left(\mathbf{C P}^{n}\right) \rightarrow$ $E^{*}\left(\mathbf{C P}^{1}\right)$ and also a morphism of associated AHSSs, both reduced and unreduced. Since the AHSS for $\widetilde{E}^{*}\left(\mathbf{C P}^{1}\right)$ is concentrated in the 1-line, we see that the element $i_{n}^{*}(x)$ must detect $i_{n}^{*}\left(x_{n}\right)=1 \neq 0$. In particular, $x$ detects $x_{n}$; a more detailed argument for this is given in the proof of [Swi02, Th.16.29]. The AHSS for $E^{*}\left(\mathbf{C P}^{n}\right)$ then degenerates as it cannot have any differentials. There are no extension problems in this spectral sequence too, which we can determine from the multiplicative structure - we leave this as an exercise. Notice that we can take $x$ in the expression for $E^{*}\left(\mathbf{C P}^{n}\right)$ to be the restriction of the complex orientation $x_{n}$, as $x$ in the proof above both defines the isomorphism $E^{*}\left(\mathbf{C P}^{n}\right) \simeq E^{*}[x] / x^{n+1}$ and detects $x_{n}$.

For the $\mathbf{C P}^{\infty}$-case, we refer back to the Milnor $\lim ^{1}$-sequence of Pr.3.1.11:

$$
0 \rightarrow \lim ^{1} E^{*-1}\left(\mathbf{C P}^{n}\right) \rightarrow E^{*}\left(\mathbf{C P}^{\infty}\right) \rightarrow \lim E^{*}\left(\mathbf{C P}^{n}\right) \rightarrow 0
$$

To see that the $\lim ^{1}$-term vanishes, consider the calculations of $E^{*}\left(\mathbf{C P}^{n}\right)$ above. As the $E^{*}$ algebra generator $x_{n} \in E^{*}\left(\mathbf{C P}^{n}\right)$ of hit by $x_{n+1}$ by restriction along the inclusion $\mathbf{C P}^{n} \rightarrow$ $\mathbf{C P}^{n+1}$, as all of the $x_{n}$ 's are defined by restricting from the complex orientation $x_{E}$, we see the morphisms in the system of graded abelian groups in the above $\lim ^{1}$-term are all surjective. By Exc.3.1.13, the $\lim ^{1}$-term above vanishes, and we obtain the desired result, as the limit of all of $x_{n}$ 's converge to the complex orientation $x_{E}$.

Exercise 3.1.18. Show that the AHSS for $E^{*}\left(\mathbf{C P}^{n}\right)$ discussed in the proof of Pr.3.1.16 has no extension problems.
Exercise 3.1.19. Show that for any complex-oriented cohomology theory $E$, any positive integer $m$, and any sequence of positive integers $n_{1}, \ldots, n_{m}$, then the maps of graded $E^{*}$-algebras

$$
\begin{gathered}
E^{*}\left[x_{1}, \ldots, x_{m}\right] /\left(x_{1}^{n_{1}+1}, \ldots, x_{m}^{n_{m}+1}\right) \xrightarrow{x_{i} \mapsto \pi_{i}^{*}\left(x_{E} \mid \mathbf{C P}^{n_{i}}\right)} E^{*}\left(\mathbf{C P}^{n_{1}} \times \cdots \times \mathbf{C P}^{n_{m}}\right) \\
E^{*}\left\|x_{1}, \ldots, x_{m}\right\| \xrightarrow{x_{i} \mapsto \pi_{i}^{*} x_{E}} E^{*}\left(\prod_{m} \mathbf{C P}^{\infty}\right)
\end{gathered}
$$

are isomorphisms, where $\pi_{i}$ indicates the projection onto the $i$ th factor of a product.
End of lecture 14 and week 8

# 3.2 Formal group laws 

In this section, all rings $R$ are (discrete) commutative and unital.
Definition 3.2.1. A formal group law ${ }^{5}$ over a ring $R$ is a power series $f(x, y)=\sum_{i, j \geqslant 0} a_{i j} x^{i} y^{j} \in$ $R \llbracket x, y \rrbracket$ which is unital, so $f(x, 0)=x$ and $f(0, y)=y$, commutative, so $f(x, y)=f(y, x)$, and associative, so $f(x, f(y, z))=f(f(x, y), z)$. If $R$ is a graded ring then we call a formal group law $f(x, y)$ graded if each $\left|a_{i j}\right|=-2 i-2 j$-this is pretending $|x|=|y|=2$. If $\varphi: R \rightarrow S$ is a morphism of rings, then we write $\varphi_{*}(f)$ for the formal group law $\sum_{i, j \geqslant 0} \varphi\left(a_{i j}\right) x^{i} y^{j}$.

At the moment this looks like a "formal monoid law", but inverses actually come for free. Exercise 3.2.2. Show that for all formal group laws $f(x, y)$ over $R$, there is a power series $g(x)$ over $R$ such that $f(x, g(x))=0$.
Exercise 3.2.3. Show that if $f(x, y) \in R \llbracket x, y \rrbracket$ is a formal group law, then it takes the form $f(x, y)=x+y+\sum_{i, j \geqslant 1} a_{i j} x^{i} y^{j}$.
Exercise 3.2.4. Show that a formal group law over a ring $R$ is equivalent to a lift of the functor of points associated to the formal affine line over $R$,

$$
\widehat{\mathbf{A}}_{R}^{1}: \operatorname{CRing}_{R} \rightarrow \text { Set }_{*} \quad R \mapsto(\operatorname{Nil}(R), 0)
$$

through the forgetful functor $\mathrm{Ab} \rightarrow$ Set $_{*}$ from abelian groups to pointed sets.
The following simple observation is the catalyst for all of chromatic homotopy theory:
Proposition 3.2.5. Let $E$ be a complex-oriented cohomology theory and write

$$
m: \mathbf{C P}^{\infty} \times \mathbf{C P}^{\infty} \rightarrow \mathbf{C P}^{\infty}
$$

for the usual multiplication on $\mathbf{C P}^{\infty} .{ }^{6}$ Then the image of $x_{E} \in E^{*}\left(\mathbf{C P}^{\infty}\right)$ inside $E^{*}\left(\mathbf{C P}^{\infty} \times\right.$ $\left.\mathbf{C P}^{\infty}\right) \simeq E^{*} \llbracket x, y \rrbracket$ induced by the map $m$ defines a graded formal group law $f_{E}$ over $E^{*}$.

The proof is simple, but this small insight opens up the Pandora's box/can of worms of chromatic homotopy theory.

Proof. To check unitality, we need to check $f_{E}(x, 0)=x$. Consider the following commutative diagram of graded abelian groups
![img-73.jpeg](img-73.jpeg)

[^0]
[^0]:    ${ }^{5}$ Our attention is restricted to 1-dimensional commutative formal group laws, although we will not use these extra adjectives.
    ${ }^{6}$ This can be done using the tensor product of line bundles as $\mathbf{C P}^{\infty} \simeq \mathrm{BU}(1)$ represented complex line bundles, by hand by considering $\mathbf{C}^{\infty}-\{0\}$ as nonzero polynomials and pass to the $\mathbf{C}^{\times}$-quotient (as done in a Topology II exercise), or using the Segre embedding from algebraic-geometry. Checking that these maps agree up to homotopy is also easy: to compute $\left[\left(\mathbf{C P}^{\infty}\right)^{2}, \mathbf{C P}^{\infty}\right]_{*}$ in pointed animæ, we use the fact that $\mathbf{C P}^{\infty}$ represents $H^{2}(-; \mathbf{Z})$, giving us isomorphisms

    $$
    \left[\left(\mathbf{C P}^{\infty}\right)^{2}, \mathbf{C P}^{\infty}\right]_{*} \simeq H^{2}\left(\left(\mathbf{C P}^{\infty}\right)^{2} ; \mathbf{Z}\right) \simeq(\mathbf{Z}[x, y])_{2}, \quad|x|=|y|=2
    $$

    These multiplications are then all represented by the element $x+y \in H^{2}\left(\left(\mathbf{C P}^{\infty}\right)^{2}, \mathbf{Z}\right)$.

induced by maps of animæ, where $e: * \rightarrow \mathbf{C P}^{\infty}$ is the unit map. We know that the diagram of animæ commutes up to homotopy, that came from the multiplicative structure on $\mathbf{C P}^{\infty}$, hence we obtain the desired conclusion that $f_{E}(x, 0)=x$ for $f_{E}$. The other conditions are the same - they follow from the commutativity and the associativity of the multiplication on $\mathbf{C P}^{\infty}$ up to homotopy.

Let us go through the complex-oriented cohomology theories of Egs.3.1.4 to 3.1.6 and check what their associated formal group laws are.
Example 3.2.6. 1. Let $x_{\mathbf{Z}}$ be the fixed complex orientation of $\mathbf{Z}$. It is easy to calculate $f_{\mathbf{Z}}=m *\left(x_{\mathbf{Z}}\right)$ inside the free abelian group $H^{2}\left(\mathbf{C P}^{\infty} \times \mathbf{C P}^{\infty} ; \mathbf{Z}\right)$ generated by $x=\pi_{1}^{*}\left(x_{\mathbf{Z}}\right)$ and $y=\pi_{2}^{*}\left(x_{\mathbf{Z}}\right)$. Indeed, the unitality of $f_{\mathbf{Z}}$ shows that $f_{\mathbf{Z}}(x, y)=x+y$. This is called the additive formal group law over $\mathbf{Z}$. This argument works over any ring $R$, so $f_{R}$ associated to the complex-orientation $x_{R}$ on $H R$ is isomorphic to the additive formal group law over $R$.
2. For $E=\mathrm{KU}$, we have already fixed $x=x_{\mathrm{KU}}=\frac{\gamma-1}{u} \in \mathrm{KU}^{2}\left(\mathbf{C P}^{\infty}\right)$, but writing $y=x \cdot u$ will simplify our calculations for a moment. Now, we know that $m^{*}(\gamma)=\pi_{1}^{*} \gamma_{1} \cdot \pi_{2}^{*} \gamma$ inside the unreduced $K$-theory of $\mathbf{C P}^{\infty} \times \mathbf{C P}^{\infty}$, as $m$ classifying the tensor product of line bundles. This implies that $m^{*}(y+1)=\left(\pi_{1}^{*} y+1\right)\left(\pi_{2}^{*} y+1\right)$ so

$$
m^{*}(y)=\left(\pi_{1}^{*} y+1\right)\left(\pi_{2}^{*} y+1\right)-1=\pi_{1}^{*} y+\pi_{2}^{*} y+\pi_{1}^{*} y \cdot \pi_{2}^{*} y
$$

as $m^{*}$ is a map of rings. This then shows that

$$
m^{*}(x)=\frac{m^{*}(y)}{m^{*}(u)}=\frac{\pi_{1}^{*} y+\pi_{2}^{*} y+\pi_{1}^{*} y \cdot \pi_{2}^{*} y}{u}=x_{1}+x_{2}+u x_{1} x_{2}
$$

using the facts that $m^{*}$ and $\pi_{i}^{*}$ are $\mathrm{KU}^{*}$-linear and writing $x_{i}=\pi_{i}^{*} x$ for $i=1,2$. We call this formal group law $f_{\mathrm{KU}}\left(x_{1}, x_{2}\right)=x_{1}+x_{2}+u x_{1} x_{2}$ the multiplicative formal group law over $\mathbf{Z}\left[u^{ \pm 1}\right]$.
3. The formal group law $f_{\mathrm{MU}}$ will actually be a big deal later on, a plot twist will not spoil yet; see $\S 3.3$.
4. It is actually very difficult in general to write down other formal group laws. One way very natural source is from elliptic curves - see [Sil86, §IV]. One defines an elliptic cohomology theory as a complex-oriented cohomology theory $E$ such that $f_{E}$ is the formal group law associated to a given elliptic curve $C$ over $\pi_{*} E$; see [Lur09a] for a modern survey on the topic.

This is fantastic. In fact, this is an inspiration to construction many interesting cohomology theories, where interesting means that the associated spectra come from or with interesting formal group laws. There is a way to sometimes reconstruct a complex-oriented cohomology theory from its associated formal group law too - this will be discussed a little later one; see ??.

Let us now see a quick application of complex-oriented cohomology theories and their associated formal group laws back in topology. The following (Cor.3.2.14) is folklore, but we

first learned about these in these lecture notes of Lennart Meier [Mei18].
First, some more formal group law theory.
Definition 3.2.7. Let $R$ be a ring and $f, g \in R \llbracket x, y \rrbracket$ be two formal groups laws. A homomorphism of formal group laws is a power series $\phi(t) \in R \llbracket t \rrbracket$ with $\phi(0)=0$ such that $\phi(f(x, y))=g(\phi(x), \phi(y))$. A homomorphism of formal group laws is called an isomorphism if $\phi^{\prime}(0)$ is a unit in $R$, ie, if the coefficient of $t$ is a unit in $R$. An isomorphism is called strict if $\phi^{\prime}(t)=1 \in R$.

The following exercises contextualise why these kinds of power series are called homomorphisms and isomorphism.
Exercise 3.2.8. Show that a homomorphism of formal group laws from $f$ to $g$ is exactly the data of a natural homomorphism $\operatorname{Nil}(R) \rightarrow \operatorname{Nil}(R)$ which respects the groups structures on each side given by $f$ and $g$, respectively; see Exc.3.2.4. Similarly, show that an isomorphism of formal group laws is precisely a natural isomorphism from $\operatorname{Nil}(R) \rightarrow \operatorname{Nil}(R)$.
Exercise 3.2.9. Show that if $\phi$ is an isomorphism of formal group laws from $f$ to $g$, then there is another isomorphism of formal group laws $\phi^{-1}$ from $g$ to $f$ and $\phi\left(\phi^{-1}(t)\right)=t$ and $\phi^{-1}(\phi(t))=t$.

For example, if $R$ is a $\mathbf{Q}$-algebra, there is a homomorphism from the multiplicative formal group law $f_{m}(x, y)=x+y+u x y$, where $u \in R^{\times}$, to the additive formal group law $f_{a}(x, y)=$ $x+y$; see Eg.3.2.6 for this terminology. This is given by the formula $\log (t)=\sum_{n \geqslant 1} \frac{(-u)^{n-1} t^{n}}{n}$. When $u=1$, this looks just like the Taylor series for $\log (t+1)$ coming from analysis, and (at least partially) justifies why these formula succeeds in mapping $f_{m}$ to $f_{a}$. Notice that this homomorphism is actually a strict isomorphism. Also, notice that we need $R$ to be a Q-algebra to define this formula. In fact, the requirement that $R$ is a $\mathbf{Q}$-algebra is equivalent to the existence of such an isomorphism.
Proposition 3.2.10. Let $R$ be a ring and $u$ be a unit in $R$. Then the formal group laws $f_{a}(x, y)=x+y$ and $f_{m}(x, y)=x+y+u x y$ are isomorphic if and only if $R$ is a $\mathbf{Q}$-algebra.

Recall that the statement that a ring $R$ is a $\mathbf{Q}$-algebra is a property of the ring $R$, not extra structure.

To prove this, we will use a little extra notation.
Definition 3.2.11. Given a positive integer $n$, a formal group law $f$ over a ring $R$, we define $[n]_{f}(x) \in R \llbracket x \rrbracket$ inductively using the formulæ

$$
[1]_{f}(x)=x, \quad[n+1]_{f}(x)=f\left([n]_{f}(x), x\right)
$$

In other words, $[n]_{f}(x)$ is the " $n$-fold product of $f$."
Example 3.2.12. We have $[n]_{f_{a}}(x)=n x$ for the additive formal group law, and for the multiplicative formal group law $f_{m}$ we have

$$
[n]_{f_{m}}(x)=\frac{(1+u x)^{n}-1}{u}
$$

which follows from the expression $1+u f_{m}=(1+u x)(1+u y)$.

We can now prove Pr.3.2.10.
Proof of Pr.3.2.10. We have just discussed one direction above, so let us write $\phi$ for an isomorphism from $f_{a}(x, y)$ and $f_{m}(x, y)$, so in particular, $\phi$ is a power series in $R$ with no constant term and with linear coefficient a unit of $R$. As $\phi$ is a homomorphism of formal group laws, then $\phi\left([n]_{f_{a}}(x)\right)=[n]_{f_{m}}(\phi(x))$ for all $n \geqslant 1$. In particular, for $n \geqslant 2$ and over the ring $R / n$ we have the equality

$$
0 \equiv \phi(n x)=\phi\left([n]_{f_{a}}(x)\right)=[n]_{f_{m}}(x)=\frac{(1+u \phi(x))^{n}-1}{u} \equiv \frac{(u \phi(x))^{n}}{u}=u^{n-1} \phi(x)^{n} \in R / n \llbracket x \rrbracket
$$

As the linear coefficient of $\phi(x)$ is a unit in $R$, we see the coefficient of $x^{n}$ is a unit times $u^{n-1}$ in the above expression. In other words, $u^{n-1}=0$ in $R / n$. As $u$ is a unit in $R$, it is also a unit in $R / n$, so we see that $R / n=0$. As this is true for all $n \geqslant 2$, we see that $R$ is a $\mathbf{Q}$-algebra as each $n \geqslant 2$ is invertible.

We will come back to the above fact in a second, but first, we would like to see a natural occurrence of isomorphisms between formal group laws between complex-oriented cohomology theories.

Proposition 3.2.13. Let $E$ be a spectrum and $x, x^{\prime} \in E^{2}\left(\mathbf{C P}^{\infty}\right)$ be two complex orientations of $E$. Then the associated formal group laws $f_{x}$ and $f_{x^{\prime}}$ are isomorphic. In fact, we can express $x^{\prime}=\phi(x)$ where $\phi(t)$ is a power series with coefficients in $E^{*}$, hence

$$
\phi\left(f_{x}\left(x_{1}, x_{2}\right)\right)=\phi\left(m^{*}(x)\right)=m^{*}(\phi(x))=f_{x^{\prime}}\left(\phi\left(x_{1}\right), \phi\left(x_{2}\right)\right)
$$

Proof. Using Pr.3.1.16, we have $E^{*}\left(\mathbf{C P}^{\infty}\right) \simeq E^{*} \llbracket x \rrbracket$ so there is a power series $\phi(x)$ in $x$ with $\phi(x)=x^{\prime}$. From the fact that these elements agree on $E^{*}\left(\mathbf{C P}^{1}\right)$, we see that the constant term must vanish and the coefficient of the linear term must be a unit.

The following is a rather amazing formal corollary of Prs.3.2.10 and 3.2.13.
Corollary 3.2.14. The maps of rings

$$
H_{*}(\mathrm{KU} ; \mathbf{Z}) \xrightarrow{\simeq} H_{*}(\mathrm{KU} ; \mathbf{Q}) \stackrel{\simeq}{\sim} \pi_{*} \mathrm{KU} \otimes \mathbf{Q} \stackrel{\simeq}{\sim} \mathbf{Q}\left[u^{ \pm 1}\right]
$$

are isomorphisms, where the first is rationalisation and the second is the rational Hurewicz map of Cor.2.5.7. For any integer $n$ the groups $H_{*}(\mathrm{KU} ; \mathbf{Z} / n \mathbf{Z})$ vanish.

In particular, notice that Th.2.3.28 does not hold for spectra which are not bounded below. Indeed, the map

$$
\pi_{k} \mathrm{KU} / n \rightarrow H_{k}(\mathrm{KU} / n ; \mathbf{Z})=\pi_{k}(\mathrm{KU} / n \otimes \mathbf{Z}) \simeq \pi_{k}(\mathrm{KU} \otimes \mathbf{Z} / n)=0
$$

is always the zero map even though $\pi_{k} \mathrm{KU} / n$ is nonzero for all even integers $k$.
Proof. The equivalence of graded rings $H_{*}(\mathrm{KU} ; \mathbf{Q}) \simeq \pi_{*}(\mathrm{KU} \otimes \mathbf{Q})$ immediately show us the second the third maps are equivalences; see Eg.2.5.6. As the first map is simply the rationalisation map, then it would be an equivalence if we could show that $H_{*}(\mathrm{KU} ; \mathbf{Z})$ was rational. This follows immediately from Prs.3.2.10 and 3.2.13, as KU carries the multiplicative formal group and $\mathbf{Z}$ the additive formal group.

As a curious consequence of Cor.3.2.14, we note that the functor $\mathrm{Sp} \rightarrow$ Cohom sending a spectrum $E$ to its associated cohomology theory actually looses quite a lot of information.

Corollary 3.2.15. The functor $\mathrm{Sp} \rightarrow$ Cohom sending a spectrum $E$ to its associated cohomology theory $E^{*}(X)$ as defined in Df.2.3.20 is not faithful, meaning there are nonzero maps of spectrum which induce the zero morphism on associated cohomology theories.

There is a class of cohomology theories upon which "associated cohomology theory" functor is fully-faithful, the so-called two-periodic Landweber exact cohomology theories; see [HS99, $\S 2.1]$.

Proof. Let us show that there are spectra $X$ and $Y$ such that the map

$$
\operatorname{h} \operatorname{Sp}(X, Y) \rightarrow \operatorname{Cohom}\left(X^{*}(-), Y^{*}(-)\right)
$$

induced by taking associated cohomology theories is not injective; for our choices of $X$ and $Y$, we'll see the group on the right will actually be zero. Let $X=\mathrm{KU}$ and $Y=\Sigma \mathbf{Z}$. Notice that a map of cohomology theories $\mathrm{KU}^{*}(-) \rightarrow \Sigma \mathbf{Z}^{*}(-)$ will vanish if and only if the associated natural map $\mathrm{KU}^{2 n}(-) \rightarrow \Sigma \mathbf{Z}^{2 n}(-)$ vanishes for all integers $n$; one direction is tautological, and the other uses the suspension isomorphism to fill in the gaps. It then suffices to show that natural maps of abelian groups $\mathrm{KU}^{2 n}(-) \rightarrow H^{2 n-1}(-; \mathbf{Z})$ vanish for each $n$. As KU-cohomology in even degrees is represented by $\mathbf{Z} \times \mathrm{BU}$, a consequence of Bott periodicity Eg.2.2.19, the Yoneda lemma states that it suffices to show the groups

$$
H^{2 n-1}(\mathbf{Z} \times \mathrm{BU} ; \mathbf{Z}) \simeq \prod_{\mathbf{Z}} H^{2 n-1}(\mathrm{BU} ; \mathbf{Z})
$$

vanish for all $n$. This is true, as it was computed in Algebraic Topology I that $H^{*}(\mathrm{BU}(m) ; \mathbf{Z}) \simeq$ $\mathbf{Z}\left[c_{1}, \ldots, c_{m}\right]$ for each $m \geqslant 1$, where $\left|c_{i}\right|=2 i$, and now we use a Milnor $\lim ^{1}$-sequence Pr.3.1.11; the details are left as an exercise below.

Now we would like to calculate $\mathrm{h} \operatorname{Sp}(\mathrm{KU}, \Sigma \mathbf{Z})$, in other words $H^{1}(\mathrm{KU} ; \mathbf{Z})$, for which we appeal to the universal coefficient sequence

$$
0 \rightarrow \operatorname{Ext}\left(H_{i-1}(\mathrm{KU} ; \mathbf{Z}), \mathbf{Z}\right) \rightarrow H^{i}(\mathrm{KU} ; \mathbf{Z}) \rightarrow \operatorname{Ab}\left(H_{i}(\mathrm{KU} ; \mathbf{Z}), \mathbf{Z}\right) \rightarrow 0
$$

which yields $H^{0}(\mathrm{KU} ; \mathbf{Z})=0$ and $H^{1}(\mathrm{KU} ; \mathbf{Z}) \simeq \operatorname{Ext}^{1}(\mathbf{Q}, \mathbf{Z})$ from Cor.3.2.14; this last group is uncountable, which is a far cry from being zero.

Exercise 3.2.16. Show that the $\lim ^{1}$-term from taking the singular cohomology of the colimit $\mathrm{BU} \simeq \operatorname{colim} \mathrm{BU}(n)$ with coefficients in $\mathbf{Z}$ vanishes.
Exercise 3.2.17. Let $A$ be an abelian group. Formulate and prove a universal coefficient sequence for the singular cohomology of a spectrum $X$ with coefficients in $A$.

# 3.3 The topological universality of MU 

The next step, and the first really deep step, into the relationship between formal group laws and stable homotopy theory comes through MU. There are two halves the this story, which will be explored in $\S 3.3$ and $\S 3.4$. We have already mentioned that MU comes with a canonical complex orientation. In this section, we will discuss how MU is actually the initial complex oriented ring spectrum, as reasonably easy fact to prove-later we will also show that $\mathrm{MU}_{*}$ is houses the universal formal group law, a reasonably hard fact to prove.

Before we study MU in more detail, let us study some orientation theory for complex vector bundles. To study these objects in the $\infty$-category $\mathcal{A}$ n, we will use some slightly different notation to avoid too much point-set topology.
Definition 3.3.1. Let $\xi \rightarrow X$ a complex vector bundle of rank $n \geqslant 0$ over an anima $X$, which means a choice of map of animæ $X \rightarrow \mathrm{BU}(n)$. We write $f: \mathrm{BU}(n-1) \rightarrow \mathrm{BU}(n)$ for the map classified by the sum of the universal rank $(n-1)$ complex vector bundle with the a trivial bundle. Let us write $S \xi$ for the base-change of this map along $X \rightarrow \mathrm{BU}(n)$. We define the Thom construction on $\xi$ as the cofibre $\operatorname{Th}(\xi)=\operatorname{cofib}(S \xi \rightarrow X)$.

If $x \in X$ is a point, so a map $i_{x}: \Delta^{0} \rightarrow X$, then we can also define $\operatorname{Th}\left(\xi \mid{ }_{x}\right)$ and a map $i_{x}: \operatorname{Th}\left(\xi \mid{ }_{x}\right) \rightarrow \operatorname{Th}(\xi)$ through the following diagram of pullbacks and cofibre sequences in $\mathcal{A}$ n:
![img-74.jpeg](img-74.jpeg)

We can actually identify $\left.S \xi\right|_{x}$ with $S^{2 n-1}$, and hence also $\operatorname{Th}\left(\xi \mid x\right)$ with $S^{2 n}$ using the following comparison which we leave as an exercise:
Exercise 3.3.2. Show that the map $f: \mathrm{BU}(n-1) \rightarrow \mathrm{BU}(n)$ used in Df.3.3.1 can be identified with the sphere bundle inside the universal rank $n$ complex vector bundle over $\mathrm{BU}(n)$. In particular, show that the fibre of this map is $S^{2 n-1}$.
Exercise 3.3.3. Show that $\operatorname{Th}(\xi)$ described above agrees with the Thom construction given in Algebraic Topology I.

From this definition we can prove some of the usual properties of this construction.
Exercise 3.3.4. Suppose $\xi$ classifies the rank 0 bundle over $B$. Show that $\operatorname{Th}(\xi) \simeq B$. Show that if $\xi$ is the trivial bundle of rank $n$ over $B$, so $f$ factors through $*$, then $\operatorname{Th}(\xi) \simeq \Sigma^{2 n} B$. More generally, if $\xi$ is isomorphic to the sum of a trivial rank $n$ bundle and another vector bundle $\chi$, then $\operatorname{Th}(\xi) \simeq \Sigma^{2 n} \operatorname{Th}(\chi)$. More generally still, show that if $\xi$ and $\chi$ are two vector bundles over $X$ and $Y$, then the Thom constrution applied to $p_{1}^{*} \xi \times p_{2}^{*} \chi$, which we write as $\xi \times \chi$ over $X \times Y$, so $\operatorname{Th}(\xi \times \chi)$, so equivalent to $\operatorname{Th}(\xi) \otimes \operatorname{Th}(\chi)$ where $\otimes$ denotes the tensor product of based animæ (so the smash product).

Definition 3.3.5. Let $E$ be a homotopy commutative ring spectrum and $\xi \rightarrow X$ be a complex rank $n$ vector bundle. An $E$-orientation on $\xi$ is a choice of $u \in \widetilde{E}^{2 n}(\operatorname{Th}(\xi))$ such that for each $x \in X$, so each map $i_{x}: \Delta^{0} \rightarrow X$, the restriction of $u$ along $i_{x}^{*}: \widetilde{E}^{2 n}(\operatorname{Th}(\xi)) \rightarrow \widetilde{E}^{2 n}\left(S^{2 n}\right) \simeq \pi_{0} E$ is a generator of $\pi_{0} E$.

We will leave the reader to verify that the existence of $E$-Thom classes leads to $E$-Thom isomorphisms.
Exercise 3.3.6. Suppose that $E$ is a homotopy commutative ring spectrum, $\xi \rightarrow B$ is a complex vector bundle of rank $n$, and that $u$ is an $E$-Thom class of $\xi$. Using the generalised form of the AHSS from Exc.2.4.5, show that there is an isomorphism $E^{*}(X) \rightarrow \widetilde{E}^{*+2 n}(\operatorname{Th}(\xi))$ given by multiplication by $u$.

Of course, we would like to see now that we have a large supply of $E$-Thom classes-these will come from the complex orientations we have already considered. Indeed, we will start with the universal example, a Thom class for the universal bundle $\gamma_{n}$ over $\mathrm{BU}(n)$. To this end, we need the following continuation of Pr.3.1.16.

Proposition 3.3.7. Let $E$ be a homotopy commutative ring spectrum with complex orientation $x_{E}$. Then for any $n \geqslant 1$ there is an isomorphism of $E^{*}$-algebras

$$
E^{*} \llbracket c_{1}, \ldots, c_{n} \rrbracket \simeq E^{*}(\mathrm{BU}(n))
$$

where $\left|c_{i}\right|=2 i$-the specific $c_{i}$ 's are described below.
The map $g: \mathrm{BU}(1)^{n} \rightarrow \mathrm{BU}(n)$ classifying the $n$-dimensional complex vector bundle

$$
\prod_{0 \leqslant i \leqslant n} p_{i}^{*} \gamma_{1}
$$

over $\mathrm{BU}^{\times n}$ produces a map $E^{*}(\mathrm{BU}(n)) \rightarrow E^{*}\left(\mathrm{BU}(1)^{n}\right)$. When $E=\mathbf{Z}$, we know this map recognises $H^{*}(\mathrm{BU}(n) ; \mathbf{Z})$ as the subring of $\mathbf{Z}\left[x_{1}, \ldots, x_{n}\right]$, where $\left|x_{i}\right|=2$, spanned by the symmetric polynomials $\sigma_{i}\left(x_{1}, \ldots, x_{n}\right)=c_{i}$. The same will be true for the $E$-cohomology of $\mathrm{BU}(n)$ : writing $x_{i}$ for the restriction of $x_{E}$ along the $i$ th projection $\mathrm{BU}(1)^{n} \rightarrow \mathrm{BU}(1)$, then the classes $c_{i} \in E^{2 i}(\mathrm{BU}(n))$ are given by $\sigma_{i}\left(x_{1}, \ldots, x_{n}\right)$.

Proof. One needs to simply apply the Atiyah-Hirzebruch spectral sequence to a skeletal filtration of these spaces and use the fact from Algebraic Topology I that we know this theorem already for $E=\mathbf{Z}$. In some more detail, the $E_{2}$-page of this spectral sequence takes the form

$$
E_{2} \simeq H^{*}\left(\mathrm{BU}(n) ; E^{*}\right) \simeq E^{*} \llbracket c_{1}, \ldots, c_{n} \rrbracket
$$

To better understand these classes $c_{n}$, we'll use the map $g: \mathrm{BU}(1)^{\times n} \rightarrow \mathrm{BU}(n)$ described just above, and the fact that $g^{*}\left(c_{i}\right)=\sigma_{i}\left(x_{1}, \ldots, x_{n}\right)$ inside the $E_{2}$-page for the Atiyah-Hirzebruch spectral sequence for $\mathrm{BU}(1)^{\times n}$ which takes the form

$$
E_{2} \simeq H^{*}\left(\mathrm{BU}(1)^{\times n} ; E^{*}\right) \simeq E^{*} \llbracket x_{1}, \ldots, x_{n} \rrbracket, \quad\left|x_{i}\right|=2
$$

Here, $\sigma_{i}\left(x_{1}, \ldots, x_{n}\right)$ denotes the $i$ th symmetric polynomial in the $x_{1}, \ldots, x_{n}$, where $x_{i}=p_{i}^{*}\left(x_{E}\right)$ is the pullback of the complex orientation of $E$ along the $i$ th projection $p_{i}: \mathrm{BU}(1)^{\times n} \rightarrow$

$\mathrm{BU}(1)$. In particular, we know from Exc.3.1.19 that the spectral sequence for $\mathrm{BU}(1)^{\times n}$ has no differentials, and since $g$ induces an injection on the $E_{2}$-page, we see that the spectral sequence for $\mathrm{BU}(n)$ also cannot support any nontrivial differentials. We then use the same argument left as an exercise (Exc.3.1.18) to see there are no extension problems as well, and we obtain the desired computation.

These classes $c_{n}$ are $E$-cohomology versions of Chern classes.
Definition 3.3.8. Let $\xi \rightarrow B$ be a complex vector bundle of rank $n$ over $B$ and let $E$ be a complex-oriented cohomology theory. Then we define $c_{n}(\xi) \in E^{2 n}(B)$ as the pullback of $c_{n}$ along the classifying map $B \rightarrow \mathrm{BU}(n)$ of $\xi$.

Exercise 3.3.9. [Properties of $E$-Chern classes] Consider the map $\mu_{m, n}: \mathrm{BU}(m) \times \mathrm{BU}(n) \rightarrow$ $\mathrm{BU}(m+n)$ be the map classifying the direct sum of an $m$-dimensional with an $n$-dimensional complex vector bundle. Show that $c_{m}(\xi) c_{n}(\chi)=c_{m+n}(\xi \oplus \chi)$. Hint: show that the universal formula $\mu_{m, n}^{*}\left(c_{m+n}\right)=c_{m}^{\prime} c_{n}^{\prime \prime}$ holds using the map $g: \mathrm{BU}(1)^{\times(m+n)} \rightarrow \mathrm{BU}(m+n)$ from above.

From this description of $E^{*}(\mathrm{BU}(n))$, notice that the image of $c_{n} \in E^{2 n}(\mathrm{BU}(n))$ maps to zero in $E^{2 n}(\mathrm{BU}(n-1))$ and therefore defines a class $u_{n} \in E^{2 n}\left(\operatorname{Th}\left(\gamma_{n}\right)\right)$. In fact, as $\mathrm{BU}(0)=*$ by definition, we see that $u_{n}$ actually defines a class in $\widetilde{E}^{2 n}\left(\operatorname{Th}\left(\gamma_{n}\right)\right)$ as its restriction to a (or any) base-point of $\mathrm{BU}(n-1)$ vanishes.

Proposition 3.3.10. Let $E$ be complex-oriented and $n \geqslant 1$. The cohomology class $u_{n} \in$ $\widetilde{E}^{2 n}\left(\operatorname{Th}\left(\gamma_{n}\right)\right)$ is a Thom class.

Proof. We have to check that for all points $b \in \mathrm{BU}(n)$, the restriction of $u_{n}=u$ to $b$ in $\widetilde{E}^{2 n}\left(\left.\operatorname{Th}\left(\gamma_{n}\right|_{b}\right)\right)$ is a generator. As $\mathrm{BU}(n)$ is connected, we may choose any point, so we may first pull the class $u_{n}$ back along the map $g: \mathrm{BU}(1)^{\times n} \rightarrow \mathrm{BU}(n)$ used above. In this case, we have

$$
g^{*} \gamma_{n} \simeq \prod_{1 \leqslant i \leqslant n} p_{i}^{*} \gamma_{1}
$$

over $\mathrm{BU}(1)^{\times n}$ by definition. Combing this with the monoidality of Th from Exc.3.3.4, we obtain

$$
\operatorname{Th}\left(g^{*} \gamma_{n}\right) \simeq \operatorname{Th}\left(\prod_{1 \leqslant i \leqslant n} p_{i}^{*} \gamma_{1}\right) \simeq \bigotimes_{1 \leqslant i \leqslant n} \operatorname{Th}\left(\gamma_{1}\right) \simeq \bigotimes_{1 \leqslant i \leqslant n} \mathrm{BU}(1)
$$

the final equivalence of pointed animæ coming from the geometric fact that the Thom construction on $\gamma_{1}$ is precisely $\mathrm{BU}(1)$; we leave this as Exc.3.3.11. Using either a based version of Exc.3.1.19, so an Atiyah-Hirzebruch spectral sequence for reduced $E$-cohomology, or a Künneth formula for spectra, we then compute $\widetilde{E}^{*}\left(\operatorname{Th}\left(g^{*} \gamma_{n}\right)\right)$ to be

$$
\widetilde{E}^{*}\left(\operatorname{Th}\left(f^{*} \gamma_{n}\right)\right) \simeq\left(x_{1} \cdots x_{n}\right) E^{*} \llbracket x_{1}, \ldots, x_{n} \rrbracket \subseteq E^{*} \llbracket x_{1}, \ldots, x_{n} \rrbracket \simeq E^{*}\left(\mathrm{BU}(1)^{n}\right)
$$

In particular, by construction, the image of $u_{n}$, defined to be a lift of $c_{n}$, along this map is precisely the product $x_{1} \cdots x_{n}=\sigma_{n}\left(x_{1}, \ldots, x_{n}\right)$. We are then reduced to showing that for all $i$, each $x_{i}$ restricts to a generator of $\widetilde{E}^{2}\left(\mathbf{C P}^{1}\right) \simeq \pi_{0} E$, which is precisely the definition of each of these $x_{i}$ 's being a complex orientation, so we are done.

Exercise 3.3.11. Show that $\operatorname{Th}\left(\gamma_{1}\right) \simeq \mathrm{BU}(1)$ as based animæ -feel free to use Exc.3.3.3, if you like.

We will now see the interaction of this computation of $E^{*}(\mathrm{BU}(n))$ and the existence of these $E$-Thom classes $c_{n}$ for $\gamma_{n}$ for a complex-oriented theory $E$, with MU.

Construction 3.3.12. Let us show that MU can be given the structure of a homotopy commutative ring spectrum; through more sophisticated methods, one can actually show that MU is an $\mathbf{E}_{\infty}$-ring; see [May77, §IV] for an older reference. Recall from Eg.2.2.21 that MU is given by the colimit of spectra $M(n)=\Sigma^{\infty} \operatorname{Th}\left(\gamma_{n}\right)[-2 n]$; also see Eg.3.1.6. To this end, notice that $M(0)$ can be identified with the sphere spectrum $\mathbf{S}$, so this gives us a choice of unit map $\mathbf{S} \rightarrow \mathrm{MU}$, so next we have to construct a multiplication map. Notice that purely formally, we have equivalences of spectra

$$
\begin{gathered}
M(m) \otimes M(n)=\Sigma^{\infty} \operatorname{Th}\left(\gamma_{m}\right)[-2 m] \otimes \Sigma^{\infty} \operatorname{Th}\left(\gamma_{n}\right)[-2 n] \\
\simeq \Sigma^{\infty}\left(\operatorname{Th}\left(\gamma_{m}\right) \otimes \operatorname{Th}\left(\gamma_{n}\right)\right)[-2(m+n)] \simeq \Sigma^{\infty}\left(\operatorname{Th}\left(p_{1}^{*} \gamma_{m} \times p_{2}^{*} \gamma_{n}\right)\right)
\end{gathered}
$$

using Exc.3.3.4. We now use the collection of maps $\widehat{\mu}_{m, n}: \mathrm{BU}(m) \times \mathrm{BU}(n) \rightarrow \mathrm{BU}(m+n)$ defined by the direct sum of vector bundles, the associated maps on Thom spaces $\operatorname{Th}\left(\gamma_{m}\right) \otimes \operatorname{Th}\left(\gamma_{n}\right) \rightarrow$ $\operatorname{Th}\left(\gamma_{m+n}\right)$, and use them to produce multiplication maps of spectra $\mu_{m, n}: M(m) \otimes M(n) \rightarrow$ $M(m+n)$. We claim that these induce a morphism of $\mathbf{N}$-indexed diagrams in Sp
![img-75.jpeg](img-75.jpeg)
the details of which we leave to the reader. We can now define $\mu$ by taking colimits $\mu: \mathrm{MU} \otimes \mathrm{MU} \simeq \operatorname{colim} M(m) \otimes \operatorname{colim} M(n) \xrightarrow{\operatorname{colim} \mu_{m, n}} \operatorname{colim} M(m+n) \simeq \operatorname{colim} M(n) \simeq \mathrm{MU}$ using that the diagonal $\mathbf{N} \rightarrow \mathbf{N} \times \mathbf{N}$ is cofinal. We again leave it as an exercise to check this actually defines a homotopy commutative ring spectrum MU.
Exercise 3.3.13. Check that $\mu_{n, n}$ combine to form an $\mathbf{N} \times \Delta^{1}$-indexed diagram in Sp using that these maps come from the associated maps on $\mathrm{BU}(n)$. Show that the maps $\mathbf{S} \rightarrow \mathrm{MU}$ and $\mu: \mathrm{MU} \otimes \mathrm{MU} \rightarrow \mathrm{MU}$ described above witness MU as a homotopy commutative ring spectrum.

These multiplication maps interact with the $E$-Chern classes $c_{n}$ of Pr.3.3.7 by design.
Construction 3.3.14. Let $E$ be a homotopy commutative ring specturm and $x_{E}$ a complex orientation. Then each class $c_{n} \in \widehat{E}^{2 n}\left(\operatorname{Th}\left(\gamma_{n}\right)\right)$ defines a map of spectra $c_{n}: M(n)=$ $\Sigma^{\infty} \operatorname{Th}\left(\gamma_{n}\right)[-2 n] \rightarrow E$ by design, such that $c_{1}: \Sigma^{\infty} \operatorname{Th}\left(\gamma_{1}\right)[-2] \simeq \Sigma^{\infty} \mathbf{C P}^{\infty}[-2] \rightarrow E$ is the given complex orientation. Moreover, these maps $c_{n}$ are multiplicative, meaning that the diagram of spectra
![img-76.jpeg](img-76.jpeg)

commutes up to homotopy. To see this, we recall that we have seen $E^{*}(M(t))$ is the ideal of $E^{*}(\mathrm{BU}(t)) \simeq E^{*} \llbracket c_{1}, \ldots, c_{t} \rrbracket$ generated by $c_{t}$, and similarly, and using the same methods, one can calculate that $E^{*}(M(m) \otimes M(n))$ is the ideal of

$$
E^{*}(\mathrm{BU}(m) \times \mathrm{BU}(n)) \simeq E^{*} \llbracket c_{1}, \ldots, c_{m}, c_{1}^{\prime}, \ldots, c_{n}^{\prime} \rrbracket
$$

generated by $c_{m} c_{n}^{\prime}$. The commutativity of the above diagram then comes down to the fact that $c_{m+n}\left(\gamma_{m} \oplus \gamma_{n}\right)=c_{m}\left(\gamma_{m}\right) c_{n}\left(\gamma_{n}\right)$, which is stated precisely in Exc.3.3.9. Setting $m=n$ and taking a colimit, we obtain a map $\mathrm{MU} \rightarrow E$ which commutes with the multiplication on MU and $E$, and one can also check it is unital. Hence, we have constructed a morphism of homotopy commutative ring spectra.

This construction suggests that perhaps there is a relationship between complex orientations on $E$ and maps of homotopy commutative ring spectra $\mathrm{MU} \rightarrow E$. To make this relationship precise, consider the following definition.

Definition 3.3.15. Let $E$ be a spectrum with a unit map $\eta: \mathbf{S} \rightarrow E$. Let us write $\operatorname{Or}(E)$ for the set of complex orientations on $E$, so the set of all morphisms $\left[\Sigma^{\infty} \mathbf{C P}^{\infty}[-2], E\right]$ which restrict to the unit on $E$ along the map $\mathbf{S} \simeq \Sigma^{\infty} S^{2}[-2] \rightarrow \Sigma^{\infty} \mathbf{C P}^{\infty}[-2]$.

This gives us a functor from the 1-category of homotopy commutative ring spectra to sets

$$
\operatorname{Or}(-): \operatorname{CAlg}(\mathrm{h} \mathrm{Sp}) \xrightarrow{E \mapsto(E, \eta: \mathbf{S} \rightarrow E)}(\mathrm{h} \mathbf{S})_{\mathbf{S} /} \rightarrow \operatorname{Set}
$$

where the first functor sends a homotopy commutative ring spectrum to the unital spectrum defined by its given unit map. One interesting fact about MU, and the main topic of this section, is that it corepresents this functor.

Theorem 3.3.16 (Topological Quillen's theorem). For any homotopy commutative ring spectrum $E$, the natural map

$$
\operatorname{CAlg}(\mathrm{h} \mathrm{Sp})(\mathrm{MU}, E) \xrightarrow{\simeq} \operatorname{Or}(E) \quad \varphi \mapsto \varphi\left(x_{\mathrm{MU}}\right)
$$

is a bijection. In other words, MU is the universal homotopy commutative complex-oriented cohomology theory. ${ }^{7}$

This universality of MU as a homotopy commutative ring spectrum gives us lots of maps straight from our examples of complex-oriented cohomology theories from Egs.3.1.4 and 3.1.5

$$
\mathrm{MU} \xrightarrow{x_{R}} R \quad \mathrm{MU} \xrightarrow{x_{\mathrm{KU}}} \mathrm{KU}
$$

where $R$ is any ring. These kinds of maps are the beginning of a study of highly structured maps of spectra from a Thom spectrum, such as MU, into another spectrum whose homotopy groups we have more control over; see [DFHH14, §10] for more on this.

[^0]
[^0]:    ${ }^{7}$ Unlike many of our statements made in class, this statement cannot be enriched to a higher categorical one. In other words, it is not true that maps of $\mathbf{E}_{1}$, or $\mathbf{E}_{\infty}$-rings $\mathrm{MU} \rightarrow E$ coincide with complex orientations on $E$.

As homotopy commutative ring spectra such as $\mathbf{S}$ and KO are not complex-orientable, we see there are no maps of homotopy commutative ring spectra from MU to either $\mathbf{S}$ or KO .

The following is a quick application of Th.3.3.16-we originally stated it as an exercise.
Proposition 3.3.17. Let $E$ be a complex-oriented homotopy commutative ring spectrum and $X$ an anima with a presentation using only even cells. Show that the Atiyah-Hirzebruch spectral sequence converging to $E^{*}(X)$ collapses with no differentials. For this, you may assume that $\pi_{*} \mathrm{MU}$ is concentrated in even degrees.

Proof. First, notice that for $E=\mathrm{MU}$, clearly the AHSS in question has no differentials as $X$ has a presentation using even cells and if we assume that we know $\pi_{*} \mathrm{MU}$ is concentrated in even degrees (see Th.3.4.3 to come), then we see no differentials can fit for degree reasons. For a general complex-oriented $E$, we use Th.3.3.16 to equip $E$ with a multiplicative map $\varphi: \mathrm{MU} \rightarrow E$, which in particular induces a multiplicative morphism between AHSSs. We can compute the $E_{2}$-page for the AHSS converging to $E^{*} X$ as $H^{*}\left(X ; \pi_{*} E\right) \simeq H^{*}(X ; \mathbf{Z}) \otimes \pi_{*} E$, which is a free $\pi_{*} E$-module from our assumptions on $X$. It follows that elements on this $E_{2}$-page can be written as sums of basic tensors $a \otimes b$ with $a \in H^{*}(X: \mathbf{Z})$ and $b \in \pi_{*} E$. As the differentials in this AHSS are $\pi_{*} E$-linear, it suffices to compute differentials on $a \otimes 1$. We now realise that the induced map of AHSSs induces a map

$$
\varphi: H^{*}(X ; \mathbf{Z}) \otimes \pi_{*} \mathrm{MU} \rightarrow H^{*}(X ; \mathbf{Z}) \otimes \pi_{*} E
$$

on $E_{2}$-pages, sending $a \otimes 1$ to $a \otimes 1$, by $H^{*}(X ; \mathbf{Z})$-linearity and unitality. As $\varphi$ also commutes with differentials, we see that

$$
d_{r}(a \otimes 1)=d_{r}(\varphi(a \otimes 1))=\varphi\left(d_{r}(a \otimes 1)\right)=0
$$

as the AHSS converging to $\mathrm{MU}^{*} X$ supports no differentials, and we are done.
Remark 3.3.18. This gives another proof of Pr.3.1.16 and Pr.3.3.7, for example. Indeed, if we define a complex orientation as a map of homotopy commutative ring spectra $\mathrm{MU} \rightarrow E$, then the proposition above follows though and we obtain the desired vanishing of differentials. We would then like to prove Th.3.3.16, to wrap everything up in a nice bow, but that proof mostly involved computations which come from Pr.3.3.17.
Remark 3.3.19. It was incorrectly (then immediately corrected) mentioned in lectures, that $\operatorname{Or}(E)$ is not $\pi_{0}$ of the following anima $\mathcal{O r}(E)$ : given unital spectrum $E$ with unit $\eta: \mathbf{S} \rightarrow E$, let $\mathcal{O}_{\mathrm{r}}(E)$ be the anima of complex orientations on $E$, defined by the pullback
![img-77.jpeg](img-77.jpeg)

The problem is that $\pi_{0} \mathcal{O r}(E)$ contains a complex orientation for $E$ plus a choice of homotopy witnessing that this restricts to the unit in $E$. There is a map $\operatorname{CAlg}(\mathrm{h} \mathrm{Sp})(\mathrm{MU}, E) \rightarrow \pi_{0} \mathcal{O}_{\mathrm{r}}(E)$

as the complex orientation for MU comes with a unique choice of homotopy witnessing that this canonical orientation restricts to the unit, but we claim that in general this map is not surjective. To make this map surjective, we claim that we need to consider a category $C$ of homotopy commutative ring spectra equipped, and where morphisms of such objects have to come with a choice of homotopy witnessing the unitality of such a morphism, so a slightly thicker version of the 1-category $\mathrm{CAlg}(\mathrm{h} \mathrm{Sp})$.

The following exercise shows that for many $E$ we are interested in $\operatorname{Or}(E)=\pi_{0} \mathcal{O}_{\mathrm{r}}(E)$.
Exercise 3.3.20. Show that if $\pi_{1} E=0$, then the natural forgetful map $\pi_{0} \mathcal{O}_{\mathrm{r}}(E) \rightarrow \operatorname{Or}(E)$ is a bijection of sets.
Exercise 3.3.21. For a unital spectrum $E$, construct a spectrum $\underline{\mathcal{O}_{\mathrm{r}}}(E)$ such that there is an equivalence of animæ $\Omega^{\infty} \underline{\mathcal{O}_{\mathrm{r}}}(E) \simeq \mathcal{O}_{\mathrm{r}}(E)$. Show that the set of orientations $\pi_{0} \mathcal{O}_{\mathrm{r}}(E)=\operatorname{Or}(E)$ is an abelian group.

End of lecture 16 and week 9

Okay, let us now prove Th.3.3.16.
Proof of Th.3.3.16. To show the injectivity and surjectivity of this construction, we will go back to the $E$-Thom classes for $E$, which arise from each complex-orientation $x_{E} \in \operatorname{Or}(E)$. The surjectivity follows from Con.3.3.14, and that construction shows how to take a complex orientation $x_{E}$ of $E$ and produce a map $\mathrm{MU} \rightarrow E$ of homotopy commutative ring spectra such that precomposing with $M(1) \rightarrow \mathrm{MU}$ yields the desired complex orientation.

For injectivity, consider two maps of homotopy commutative ring spectra $\varphi, \psi: \mathrm{MU} \rightarrow E$ which agree as maps of spectra when restricted along $M(1) \rightarrow \mathrm{MU}$, meaning they define the same class in $[M(1), E] \simeq E^{2}\left(\mathbf{C P}^{\infty}\right)$. As both these are maps of homotopy commutative ring spectra, then the composites

$$
M(1)^{\otimes n} \xrightarrow{\mu_{1}, \ldots, 1} M(n) \xrightarrow{\left.\varphi\right|_{M(n)},\left.\psi\right|_{M(n)}} E
$$

are simply an $n$-fold product of copies of $\left.\varphi\right|_{M(1)}=\left.\psi\right|_{M(1)}$. However, from our computations done in and around Pr.3.3.7 and Pr.3.3.10, we see that the map

$$
E^{*}(M(n)) \xrightarrow{\mu_{1, \ldots, 1}^{*}} E^{*}\left(M(1)^{\otimes n}\right)
$$

is injective; indeed, this is just a shift (using the $E$-Thom isomorphism of Pr.3.3.10) of the injection

$$
E^{*} \llbracket c_{1}, \ldots, c_{n} \rrbracket \simeq E^{*}(\mathrm{BU}(n)) \rightarrow E^{*}\left(\mathrm{BU}(1)^{n}\right) \simeq E^{*} \llbracket x_{1}, \ldots, x_{n} \rrbracket
$$

from Pr.3.3.7. In particular, we see that $\varphi$ and $\psi$ agree when restricted to $M(n)$, for even $n$. Again combining these $E$-Thom isomorphisms and the Milnor $\lim ^{1}$-sequence of Pr.3.1.11, we obtain

$$
0=\lim ^{1} E^{-1} M(n) \rightarrow E^{0} \mathrm{MU}=[\mathrm{MU}, E] \xrightarrow{\simeq} \lim E^{0} M(n) \rightarrow 0
$$

In other words, as $\varphi$ and $\psi$ agree when restricted to each $M(n)$, then the above isomorphism shows they agree as maps of spectra $\mathrm{MU} \rightarrow E$, so as maps in h Sp. Now, we simply observe

that maps in $\mathrm{CAlg}(\mathrm{h} \mathrm{Sp})$ as simply a subcollection of those maps in h Sp. ${ }^{8}$ Indeed, more generally, for any symmetric monoidal 1-category $\mathcal{C}$ and a pair of commutative monoids $A, B$ in $\mathcal{C}$, then there is an equaliser diagram

$$
\operatorname{CAlg}(A, B) \rightarrow \mathcal{C}(A, B) \rightrightarrows \mathcal{C}\left(A^{\otimes 2}, B\right) \times \mathcal{C}(\mathbf{1}, B)
$$

where the two maps in the equaliser are given by sending $f: A \rightarrow B$ the pairs

$$
\left(A^{\otimes 2} \xrightarrow{\mu_{A}} A \xrightarrow{f} B, \mathbf{1} \xrightarrow{\eta_{A}} A \xrightarrow{f} B\right), \quad\left(A^{\otimes 2} \xrightarrow{f \otimes f} B^{\otimes 2} \xrightarrow{\mu_{B}} B, \mathbf{1} \xrightarrow{\eta_{B}} B\right)
$$

In particular, we see that as $\varphi$ and $\psi$ agree in h Sp , they agree in $\operatorname{CAlg}(\mathrm{h} \mathrm{Sp})$, thus proving injectivity, and finishing the proof.

Remark 3.3.22. There is a slightly more refined version of Th.3.3.16 for "homotopy associative ring spectra such that their homotopy groups form a commutative ring". The proofs of Prs.3.1.16 and 3.3.7 then follow through in the same way, which are the real key ingredients to proving Th.3.3.16. We mention this slight generalisation as the Morava $K$-theories to come are not necessarily homotopy commutative, only homotopy associative, yet we will construct their complex orientations as maps $\mathrm{MU} \rightarrow \mathrm{K}(h)$.

# 3.4 Quillen's theorem and Landweber's exact functor theorem 

We called Th.3.3.16 a "topological Quillen's theorem", as it shows MU to have a certain universal property. Our next goal will be to describe, but not prove, an "algebraic Quillen's theorem", which recognises the homotopy groups of MU also have a certain universal property.

Definition 3.4.1. Let $L$ be the Lazard ring, defined as the quotient $\mathbf{Z}\left[a_{i j}\right]_{i, j \geqslant 0} / I$ where $I$ is the ideal given by the minimal set of the relations between the various $a_{i j}$ 's such that the power series $f_{L}(x, y) \in L \llbracket x, y \rrbracket$ defined by

$$
f_{L}(x, y)=\sum_{i, j \geqslant 0} a_{i j} x^{i} y^{j}
$$

is a formal group law. For example, $a_{i j}=a_{j i}$ to model commutativity, etc.
By construction, the Lazard ring $L$ and the formal group law $f_{L}$ over $L$ corepresent the functor

$$
\text { CRing } \rightarrow \text { Set } \quad R \mapsto \operatorname{FGL}(R)
$$

sending a ring to the set of isomorphism classes of formal group laws over $R$. The reason why we call this the Lazard ring, as opposed to the universal ring of formal group laws, is because of the following result of Lazard.

Theorem 3.4.2 (Lazard's theorem). There is a noncanonical isomorphism of rings

$$
L \simeq \mathbf{Z}\left[x_{1}, x_{2}, x_{3}, x_{4}, \cdots\right]
$$

[^0]
[^0]:    ${ }^{8}$ This is fact from being true higher categorically, where showing that a map of spectra is a map of structured ring spectra involves extra data, but in the homotopy category this is simply a property.

This is quite a nontrivial result. Notice that in particular it does not say that these $x_{i}$ 's are the $a_{i j}$ 's from before, or gives you any sort of recipe to compare the two of them. The point is that it is easy to write down a canonical map of rings $L \rightarrow R$ associated to each formal group law over $R$ and it is easy to describe the image of this map in terms of the $a_{i j}$ 's, however, if we write $L \simeq \mathbf{Z}\left[x_{1}, x_{2}, \ldots\right]$, it is not clear what the image of these $x_{i}$ 's is.
Theorem 3.4.3 (Algebraic Quillen's theorem). For any ring $R$, the natural map

$$
\operatorname{CRing}\left(\pi_{*} \mathrm{MU}, R\right) \xrightarrow{\simeq} \operatorname{FGL}(R) \quad \varphi \mapsto \varphi^{*} f_{\mathrm{MU}}
$$

is a bijection. The same holds if $R$ is graded and $\pi_{*} \mathrm{MU}$ is given the natural grading. In other words, $\pi_{*} \mathrm{MU}$ is naturally isomorphic to the Lazard ring.

Both of these statements are proven in [Ada74, §II], [Lura, Lecs. 2-3], and [Rav04, §A.2].
Quillen's theorem is quite amazing, as it should be surprising to see the universal formal group law in the wild, especially when it comes from an a priori purely geometric object like MU. As MU is already a spectrum representing a cohomology theory, we can use it and Quillen's theorem to try to construct spectra - to date, this is one of the biggest machines for constructing a wide variety of cohomology theories.

Consider the following situation: we have a formal group law $f$ over a graded ring $R_{*}$. This $f$ is classified by a morphism $\mathrm{MU}_{*} \rightarrow R_{*}$ by Quillen's theorem, and we then define the functor from anize to graded abelian groups by the formula

$$
E_{*}^{f}(X)=\mathrm{MU}_{*}(X) \underset{\mathrm{MU}_{*}}{\otimes} R_{*}
$$

This defines a functor such that its value on $X=*$ is precisely $R_{*}$. Moreover, if we assume this functor defines a cohomology theory and hence a spectrum $E_{f}$ which is multiplicative (using a cohomological variant), then actually $E_{f}$ is a complex oriented cohomology theory, with complex orientation given by the natural map $\mathrm{MU} \rightarrow E_{f}$ coming from the definition above.

It suffices then to check that the formula $E_{*}^{f}(X)$ above actually defines a homology theory. It clearly satisfies homotopy invariance, as $\mathrm{MU}_{*}(X)$ is already homotopy invariant, and likewise, tensor products commute with direct sums, so the direct sum axiom also follows from that for $\mathrm{MU}_{*}(X)$. The only axiom in doubt is exactness, as tensor often do not preserve exactness.

If the map $\mathrm{MU}_{*} \rightarrow R_{*}$ was flat, then we'd be done, but let us immediately point out that this condition is quite useless in practice. From Lazard's theorem Th.3.4.2, we see that $\mathrm{MU}_{*}$ is isomorphic to a polynomial ring on infinitely many generators. In particular, $\mathrm{MU}_{*}$ is a domain, so if $\mathrm{MU}_{*} \rightarrow R_{*}$ were flat, it would be injective, so $R_{*}$ itself would contain the Lazard ring as a subring, and we really don't want that.

What is remarkable, is that a much weaker condition is sufficient: we don't ask the map $\mathrm{MU}_{*} \rightarrow R_{*}$ to be flat, we ask for the map $\operatorname{Spec} R_{*}$ into the moduli stack of formal groups to be flat.

Theorem 3.4.4 (Stacky Landweber exact functor theorem). Let $f(x, y)$ be a formal group law over a ring $R$ and write $E_{*}^{f}(X)$ for the functor from anim $\boldsymbol{x}$ to graded abelian groups defined by the formula

$$
E_{*}^{f}(X)=\mathrm{MU}_{*}(X) \underset{\mathrm{MU}_{*}}{\otimes} R
$$

Then $E_{*}^{f}(X)$ defines a homology theory and hence a spectrum $E_{f}$, if the associated map $\operatorname{Spec} R \rightarrow \mathcal{H}_{\text {FGroup }}$ is flat.

We do not want to talk about stacks in class, so we will choose discuss the more classical formulation of this theorem.

Definition 3.4.5. Let $f(x, y)$ be a formal group law over a ring $R$. For a fixed prime number $p$, we write $v_{n}$ for the coefficient of $x^{p^{n}}$ in the $p$-series of $f$. By the unitality of $f$, we always have $v_{0}=p$. Alternatively, we can also define $v_{n}$ inside $L$ using the universal formal group law, and then for each formal group law $f$ over a ring $R$ with associated map $\varphi: L \rightarrow R$, we define $v_{n}$ in $R$ as $\varphi\left(v_{n}\right)$. It is a simple exercise to check these two definitions agree.

These $v_{n}$ 's actually come into our definition of what the height of a formal group law is.
Definition 3.4.6. Fix a prime $p$ and some $1 \leqslant h \leqslant \infty$. For a ring $R$ of characteristic $p$, so $p=0$ in $R$, and a formal group law $f(x, y)$ over $R$ corresponding to a map $f: L \rightarrow R$, we say that $f(x, y)$ has height $\geqslant h$ if $v_{i}=0$ in $R$ for all $i \leqslant h$. We say $f(x, y)$ has height $=n$ if $v_{n}$ is also invertible in $R$.

We know the $p$-series of $f_{a}(x, y)$ and $f_{m}(x, y)$ from Eg.3.2.12, and from this we can easily see that over $\mathbf{F}_{p}$, the height of $f_{a}(x, y)$ is infinity and the height of $f_{m}(x, y)$ is one.
Exercise 3.4.7. Prove that if two formal group laws $f, g$ over a ring $R$ of characteristic $p$ are isomorphic, then $\operatorname{ht}(f)=\operatorname{ht}(g)$. In particular, we see again that over a ring of characteristic $p, f_{a}(x, y)$ and $f_{m}(x, y)$ are not isomorphic.

If we are working over an algebraically closed field, then the height of a formal group law is a complete invariant.

Theorem 3.4.8. Let $R=\kappa$ be an algebraically closed field of characteristic $p$. Then two formal group laws $f(x, y)$ and $g(x, y)$ over $\kappa$ are isomorphic if and only if they have the same height.

As mentioned in Eg.3.2.6, elliptic curves also give us examples of formal groups laws. These curves can sometimes be defined over integral domains $R$ where $R / p$ is nonzero for various different primes $p$. It can also happen that the elliptic curves over these different reductions can have differing heights-some behaviour very different to the formal groups laws $f_{a}(x, y)$ and $f_{m}(x, y)$. In general though, the height of a formal group law coming from an elliptic curve is either 0 (if we are working rationally), 1 (in which case we call the curve ordinary), or 2 (in which case we call the curve supersingular, which means rare and has nothing to do with the curve not being smooth).

Theorem 3.4.9 (Classical Landweber exact functor theorem). Let $f(x, y)$ be a formal group law over a ring $R$. Then the functor $E_{*}^{f}(-)$ of Th.3.4.4 is a cohomology theory if for every prime $p$, the sequence $\left(v_{0}, v_{1}, v_{2}, \ldots\right)$ is regular. ${ }^{9}$

In particular, as $v_{0}=p$, we see that $R$ must be at the very least a torsion-free ring.
We will only give a sketch of a proof, the ideas of which go back to Landweber [Lan76].
Proof sketch. First, an algebraic detour: notice that the unit map $\eta: \mathbf{S} \rightarrow \mathrm{MU}$ induces two different complex orientations on $\mathrm{MU} \otimes \mathrm{MU}$ :

$$
\begin{aligned}
& \eta_{L}: \mathrm{MU} \simeq \mathbf{S} \otimes \mathrm{MU} \xrightarrow{\eta \otimes \mathrm{id}_{\mathrm{MU}}} \mathrm{MU} \otimes \mathrm{MU} \\
& \eta_{R}: \mathrm{MU} \simeq \mathrm{MU} \otimes \mathbf{S} \xrightarrow{\mathrm{id}_{\mathrm{MU}} \otimes \eta} \mathrm{MU} \otimes \mathrm{MU}
\end{aligned}
$$

Let us emphasise again: these are two different complex orientations for $\mathrm{MU} \otimes \mathrm{MU}$. As an exercise, see Exc.3.4.11, one can compute the ring $\pi_{*}(\mathrm{MU} \otimes \mathrm{MU}) \simeq L\left[b_{1}, b_{2}, \ldots\right]$ where $L \simeq \pi_{*} \mathrm{MU}$ is the Lazard ring. The map $\eta_{L}$ is then the obvious map from $L$ to $L\left[b_{1}, b_{2}, \ldots\right]$, and $\eta_{R}$ is the more complicated one: if $L \simeq \mathbf{Z}\left[x_{1}, x_{2}, \ldots\right]$, then

$$
\eta_{R}\left(x_{i}\right)=\sum_{i \geqslant 0} b_{i} x_{n+1}
$$

We call an ideal $I \subseteq \pi_{*} \mathrm{MU}$ invariant if $\eta_{R}(I) \subseteq I \mathrm{MU}_{*} \mathrm{MU}$. A theorem of Landweber now classifies such ideal.

Theorem 3.4.10. The invariant prime ideals $\left(v_{0}, v_{1}, \ldots, v_{n}\right)$ are the finitely generated invariant prime ideals of $\mathrm{MU}_{*}$.

The proof of this theorem is similar to the classification of finitely generated modules over a PID.

There exists a filtration of $\mathrm{MU}_{*}(X)=M_{0} \supseteq M_{1} \supseteq M_{2} \supseteq \cdots$ such that the associated graded $\bigoplus M_{i} / M_{i+1}$ is a sum of $\mathrm{MU}_{*} / I_{n, p}$, where $I_{n, p}$ are the invariant Landweber ideals mentioned above. To show that $\mathrm{MU}_{*}(-) \otimes_{\mathrm{MU}_{*}} R$ is exact is equivalent to the vanishing of $\operatorname{Tor}_{L}^{1}\left(\mathrm{MU}_{*}(X), R\right)$, and by induction on $n$ (and for each $p$ separately) we can use the above filtration to reduce this to computing $\operatorname{Tor}_{L}^{1}\left(\mathrm{MU}_{*} / I_{n, p}, R\right)=0$ for all $p$ and for all $n$, and this is now exactly the kind of condition that appears in the hypotheses of Th.3.4.9.

Exercise 3.4.11. Show that there is an isomorphism of rings $\mathrm{MU}_{*} \mathrm{MU} \simeq \mathrm{MU}_{*}\left[b_{1}, b_{2}, \ldots\right]$; try to use the Thom isomorphisms from Pr.3.3.10. This can be interpreted as saying that $\mathrm{MU}_{*} \mathrm{MU}$ corepresents isomorphism classes of formal group laws.

Let us now see how some of our favourite cohomology theories can be reconstructed using Th.3.4.9.

[^0]
[^0]:    ${ }^{9}$ Recall that a sequence of elements $\left(x_{1}, x_{2}, x_{3}, \ldots\right)$ of a ring $R$ are said to be regular if the multiplication maps $x_{n}: R /\left(x_{1}, \ldots, x_{n-1}\right) \rightarrow R /\left(x_{1}, \ldots, x_{n-1}\right)$ are injective for all $n$.

Example 3.4.12. The additive formal group law over any $\mathbf{Q}$-algebra $R$ is exact, as $v_{0}=p$ for every prime $p$, and the $p$-series of the additive formal group law is $[p](x)=p x$. As long as $p$ is not a zero divisor on $R$ for all primes $p$, then $v_{0}$ is never a zero divisor. In particular, $R$ must be torsion free. We then need $0=v_{1} \in R / p$ to be a nonzero divisor in $R / p$, so we need $R / p$ itself to vanish for all primes $p$, so $R$ must then be rational.
Non-example 3.4.13. The above also shows that $f_{a}(x, y)$ over $\mathbf{Z}$ is not Landweber exact, and we cannot construct singular cohomology $\mathbf{Z}$ out of this theorem. More precisely, as $v_{1}=0$ and multiplication by 0 is not injective on $\mathbf{F}_{p}$, we see that $(p, 0,0, \ldots)$ is not a regular sequence.

End of lecture 17

Example 3.4.14. The multiplicative formal group law over $\mathbf{Z}\left[u^{ \pm 1}\right]$ is Landweber exact, as $v_{0}=p$ always, and the $p$-series modulo $p$ is $x^{p}$, so $v_{1}=1$ and $v_{n}=0$ for $n \geqslant 2$. This gives an equivalence of spectra $E_{f_{\mathrm{KU}}} \simeq \mathrm{KU}$.
Remark 3.4.15. Notice that if $E$ is a complex-oriented cohomology theory such that $\pi_{*} E$ and its associated formal group law $f_{E}$ form a Landweber exact cohomology theory, then the spectrum $E_{f_{E}}$ from the Landweber exact functor theorem is equivalent to $E$. To see this, notice that the complex-orientability of $E$ paired with Th.3.3.16 provide us with a map of homotopy commutative ring spectra $\mathrm{MU} \rightarrow E$ and hence a map of homology theories $\mathrm{MU}_{*}(-) \rightarrow E_{*}(-)$. Base-changing the source of this over the map on coefficient rings gives a map of homology theories

$$
\left(E_{f_{E}}\right)_{*}(-)=E_{*} \otimes_{\mathrm{MU}_{*}} \mathrm{MU}_{*}(-) \xrightarrow{\simeq} E_{*}(-)
$$

which is an isomorphism by construction. Hence this lifts to a morphism of spectra which is an isomorphism on homotopy groups, hence the desired equivalence.

Definition 3.4.16. We say that the spectrum $E_{f}$ coming from a Landweber exact formal group law $f$ over a ring $R$ is a Landweber exact. In fact, the previous remark shows that this is a property of a complex-orientable spectrum.

Remark 3.4.17 (Multiplicative structures on LEFT spectra). Given a Landweber exact formal group law $f(x, y)$ over a graded ring $R$, then the spectrum $E_{f}=E$ representing the functor $X \mapsto \mathrm{MU}_{*}(X) \otimes_{\mathrm{MU}_{*}} R$ has a homotopy commutative multiplication. To see this, we need to use the fact $[\mathrm{HS} 99]$ that the functor sending a spectrum to its associated homology theory is $\underset{\text { (reference) }}{\text { ( }}$ faithful (we already know it is full) on the subcategory of Landweber exact complex-orientable ring spectrum. We would like to construct a multiplication map

$$
\mu: E \otimes E \rightarrow E
$$

From the fullness of the associated homology theory functor, it suffices to construct a map $(E \otimes E)_{*} X \rightarrow E_{*} X$ which is natural in $X$. Using the definition of $E$ from the LEFT a few time, we obtain the equivalences

$$
\begin{aligned}
(E \otimes E)_{*} X \simeq E_{*}(E & \otimes X) \simeq \mathrm{MU}_{*}(E \otimes X) \otimes_{\mathrm{MU}_{*}} R \simeq E_{*}(\mathrm{MU} \otimes X) \otimes_{\mathrm{MU}_{*}} R \\
& \simeq \mathrm{MU}_{*}(\mathrm{MU} \otimes X) \otimes_{\mathrm{MU}_{*}} R \otimes_{\mathrm{MU}_{*}} R
\end{aligned}
$$

The desired map is then a combination of the multiplication map on MU and the $\mathrm{MU}_{*}$-linear multiplication map on $R$. This gives us the multiplication map $\mu$ without any problems, but to check that $\mu$ is unital, associative, and commutative, we need to use faithfulness of the associated homology functor, as we want to argue that a diagram of spectra commutes as the diagram of associated cohomology theories commutes.
Example 3.4.18. Another nice example is the following: let $R=\mathbf{Z}\left[\frac{1}{6}, c_{4}, c_{6}, \Delta^{-1}\right]$ be the ring of integral (weakly holomorphic) modular forms (away from 6), and consider the elliptic curve $C$ defined by the equation $y^{2}=x^{3}+c_{4} x+c_{6}$. We claim that the formal group law $f_{C}$ associated to $C$ is Landweber exact. Indeed, for each prime $p$, the element $p=v_{0}$ is a nonzero divisor in $R$ : for $p=2,3$, the sequence $\left(v_{0}, v_{1}, \ldots\right)$ is automatically regular as $p$ is invertible in this case. Otherwise, we want to check that $v_{1} \in R / p$ is a nonzero divisor, or, as $R / p$ is a domain, that $v_{1}$ is nonzero. To check this, it suffices to show that there exists fields $\kappa$ and a map $R / p \rightarrow \kappa$ such that $C_{\kappa}$ is an ordinary elliptic curve, as $v_{1}$ is the usual Hasse invariant. This is clear though, as there are only finitely many supersingular elliptic curves over $\overline{\mathbf{F}}_{p}$, and yet we can choose infinitely many such curves using the equation defining $C$. Moreover, we see that $v_{2} \in R /\left(p, v_{1}\right)$ is invertible as formal groups from elliptic curves have height $\leqslant 2$. In particular, there exists a cohomology theory $E$ such that $f_{E} \simeq f_{C}$, which we call the universal elliptic cohomology theory away from 6 -to construct an integral universal elliptic cohomology theory takes more work.
Example 3.4.19. Fixing a prime $p$ and choosing some suitable $x_{p^{n}-1}$ as $v_{n}$, we can look at the map $L \rightarrow \mathbf{Z}_{(p)}\left[v_{1}, v_{2}, \ldots\right]$ which sends all of the $x_{i} \neq v_{n}$ to zero and otherwise sends $v_{n}$ to $v_{n}$. It is easy to check that this map of rings is Landweber exact; this is almost true by definition. The associated spectra are called Brown-Peterson spectra and denoted as BP, where the prime $p$ is left implicit.
Example 3.4.20. Fix a prime $p$ and a positive integer $h \geqslant 1$. As a variation on the previous example, consider the ring $A=\mathbf{Z}_{(p)}\left[v_{1}, \ldots, v_{h-1}, v_{h}^{\pm}\right]$. The obvious map $L \rightarrow A$, just like Eg.3.4.19 above, is Landweber exact also by definition. This yields a spectrum denoted by $E(h)$, again the $p$ is implicit, which we called Johnson-Wilson theory.

This final example is supposed to capture chromatic information at a certain primes of heights less than or equal to $h$-in other words, $E(h)$-localisation is supposed to only remember height $\leqslant n$ information about Sp. To specialise to the monochromatic layers of Sp, so to find some spectra which really only understand chromatic information at height precisely $h$, which would like a spectrum similar to $E(h)$, where $v_{0}, \ldots, v_{h-1}$ have all been killed, and only an invertible $v_{h}$ is left. These are the Morava $K$-theories.

# 3.5 The Morava $K$-theory spectra 

For this section, we will use the fact that MU is an $\mathbf{E}_{\infty}$-ring spectrum as well as some formal facts about MU-modules - the theory of structured ring spectra and module spectra was partially created to aid with some of the constructions to come; see [EKMM97, §V.4] for this application and [ABG18, Th.1.7] for the fact that Thom spectra can be given structure multiplications.

Warning 3.5.1. For our construction of Morava $K$-theories, we will use the fact that MU is an $\mathbf{E}_{\infty}$-ring such that there is a stable symmetric monoidal $\infty$-category of MU-modules, which we denote by $\operatorname{Mod}_{\mathrm{MU}}$. We have not discussed symmetric monoidal $\infty$-categories in these lectures, see $\S 1.9$, but we just want to use a few basic facts about $\operatorname{Mod}_{\mathrm{MU}}$ and only higher categorical generalisations of facts from algebra. In particular:

1. The $\infty$-category $\operatorname{Mod}_{\mathrm{MU}}$ is complete and cocomplete
2. The unit map $u: \mathbf{S} \rightarrow \mathrm{MU}$ induces a functor $u^{*}: \mathrm{Sp} \rightarrow \operatorname{Mod}_{\mathrm{MU}}$ sending $X$ to $X \otimes \mathrm{MU}$, which is left adjoint to the forgetful functor $\operatorname{Mod}_{\mathrm{MU}} \rightarrow \mathrm{Sp}$.
3. The $\infty$-category $\operatorname{Mod}_{\mathrm{MU}}$ comes equipped with a monoidal structure, written as $M \otimes_{\mathrm{MU}} N$, such that the functor $u^{*}$ above is strong symmetric monoidal.
4. Given a prime $p$, the localisation construction $\mathrm{MU}_{(p)}$ of Rmk.2.5.12 is also an $\mathbf{E}_{\infty}$-ring.

It is possible to define Morava $K$-theories without monoidal structure, this is how these spectra we originally defined, but the construction is famously tricky.

Recall from Th.3.4.2 that $\pi_{*} \mathrm{MU}$ is isomorphic to a polynomial ring over $\mathbf{Z}$ in variables $x_{i}$ for each $i \geqslant 1$ where $\left|x_{i}\right|=2 i$. If we localise MU at a prime $p$, then we can assume that $x_{p^{i}-1}=v_{i}$ for each $i \geqslant 1$, where the $v_{i}$ 's are the coefficients of $x^{p^{i}}$ in the $p$-series of the universal formal group law.

Definition 3.5.2. Fix a prime $p$. For each $k \geqslant 1$, we represent $x_{k} \in \pi_{2 k} \mathrm{MU}_{(p)}$ by a map of spectra $x_{k}: \mathbf{S}[2 k] \rightarrow \mathrm{MU}_{(p)}$, which is adjoint to a map of MU-modules $\mathrm{MU}[2 k] \rightarrow \mathrm{MU}_{(p)}$ which naturally factors as a map of $\mathrm{MU}_{(p)}$-modules $t_{k}: \mathrm{MU}_{(p)}[2 k] \rightarrow \mathrm{MU}_{(p)}$. We also define $t_{0}=p$. For $k \geqslant 0$, denote the cofibre of $t_{k}$ in the category of $\mathrm{MU}_{(p)}$-modules as $C(k)$. For a positive integer $h$, we then define $\mathrm{K}(h)$ the $h$ th Morava $K$-theory spectrum as the localisation of the infinite $\mathrm{MU}_{(p)}$-relative tensor product

$$
\mathrm{K}(h)=\left(\bigotimes_{\substack{k \geq 0 \\ k \neq p^{h}-1}} C(k)\right)\left[v_{h}^{-1}\right]
$$

where the infinite tensor product above is the filtered colimit of finite tensor products and localisation is defined as in Rmk.2.5.12. Let us also define $\mathrm{K}(0)=\mathbf{Q}$ and $\mathrm{K}(\infty)=\mathbf{F}_{p}$.

It is not clear from this definition that these $\mathrm{K}(h)$ 's are homotopy ring spectra, ${ }^{10}$ but this is true.

[^0]
[^0]:    ${ }^{10}$ At odd primes $p \neq 2, \mathrm{~K}(h)$ cannot even be a homotopy commutative ring spectrum. We do not have a direct proof of this, but rather make the observation, due to Würgler [Wür86], a homotopy commutative ring spectrum with $2=0$ in $\pi_{0}$ is necessarily an Eilenberg-Mac Lane spectrum. This is clearly not true for $\mathrm{K}(h)$. At all primes and all heights $h$, we can also use a related result of Hopkins-Mahowald to show that $\mathrm{K}(h)$ does not admit an $\mathbf{E}_{2}$-structure for any $0<h<\infty$. Indeed, a result of Hopkins-Mahowald, a good reference is [KN22, Th.A.1], states that the initial $\mathbf{E}_{2}$-ring with $p=0$ is $\mathbf{F}_{p}$. In other words, if $\mathrm{K}(h)$ did admit an $\mathbf{E}_{2}$-structure, then it would admit the structure of an $\mathbf{F}_{p}$-module, which is again not true for any $\mathrm{K}(h)$ for $h \neq 0, \infty$. Clearly $\mathrm{K}(0)=\mathbf{Q}$ and $\mathrm{K}(\infty)=\mathbf{F}_{p}$ are both $\mathbf{E}_{\infty}$.

Proposition 3.5.3. For each prime $p$ and each $0 \leqslant n \leqslant \infty$, the spectrum $\mathrm{K}(n)$ is a homotopy ring spectrum.

In fact, all the Morava $K$-theory spectra are $\mathbf{E}_{1}$-rings, so they are associative up to all higher homotopies too; see [Ang08]. We will come back to this multiplicative structure shortly.

Despite it's seemingly complicated definition, it is actually simple to calculate the homotopy groups of $\mathrm{K}(n)$.

Proposition 3.5.4. Let $p$ be a prime and $h$ be a positive integer. Then the suggestive homomorphism $\mathbf{F}_{p}\left[v_{h}^{-1}\right] \rightarrow \pi_{*} \mathrm{~K}(h)$ is an isomorphism of rings, where $\left|v_{h}\right|=2\left(p^{h}-1\right)$.

Proof. First, notice that we can easily calculate $\pi_{*} C(k)$ from the long exact sequence on homotopy groups defining them:

$$
\mathbf{Z}_{(p)}\left[x_{1}, x_{2}, x_{3}, \ldots\right] /\left(x_{k}\right) \simeq \pi_{*} C(k)
$$

It is also easy to calculate the homotopy groups of $C(k) \otimes_{\mathrm{MU}_{(p)}} C\left(k^{\prime}\right)$ from the same cofibre sequence and the fact that the functor $-\otimes_{\mathrm{MU}_{(p)}} C\left(k^{\prime}\right)$ preserves colimits:

$$
\mathbf{Z}_{(p)}\left[x_{1}, x_{2}, x_{3}, \ldots\right] /\left(x_{k}, x_{k}^{\prime}\right) \simeq \pi_{*} C(k) \otimes_{\mathrm{MU}_{(p)}} C\left(k^{\prime}\right)
$$

By induction, we obtain the homotopy groups of finite $\mathrm{MU}_{(p)}$-relative tensor products of the $C(k)$ 's, and as filtered colimits commute with homotopy groups, we also obtain the homotopy groups of the infinite $\mathrm{MU}_{(p)}$-relative tensor product:

$$
\mathbf{F}_{p}\left[v_{h}\right] \simeq \pi_{*} \underset{k \geqslant 0}{\otimes} C(k)
$$

This spectrum $\otimes_{k \geqslant 0, k \neq p^{n}-1} C(k)$ is sometimes called connective Morava $K$-theory. The calculation of $\mathrm{K}(n)$ now follows from Exc.2.5.13.

The homotopy groups of Morava $K$-theory are what are called a graded field, meaning a graded commutative ring $R_{*}$ concentrated in even degrees in which every nonzero homogeneous element is invertible.
Exercise 3.5.5. Show that all graded fields are of the form of either a field $\kappa$ concentrated in degree zero of $\kappa\left[u^{ \pm 1}\right]$ for an element $u$ of positive even degree. Show a graded module $M_{*}$ over a graded field $R_{*}$ is free on a set of homogeneous elements $S \subseteq M_{*}$, meaning the $R_{*}$-module homomorphism defined by $S$

$$
\underset{s \in S}{\bigoplus} R_{*}[|s|] \rightarrow M_{*}
$$

is an isomorphism.
Definition 3.5.6. A field in Sp is a homotopy ring spectrum $E$ such that $\pi_{*} E$ is a graded field.

Exercise 3.5.7. Show that given a field $E$ in Sp and two spectra $X, Y$, then there is homological Künneth isomorphism

$$
E_{*}(X \otimes Y) \simeq E_{*} X \underset{E_{*}}{\otimes} E_{*} Y
$$

of $E_{*}$-modules. What conditions would you need to place on $X$ and $Y$ to obtain a cohomological Künneth isomorphism?

A fundamental property of Morava $K$-theories is that they constitute all possible fields in Sp.

Theorem 3.5.8. If $E$ is a field in $\mathrm{Sp}$, then $E$ is a $\mathrm{K}(h)$-module for some prime $p$ and some $0 \leqslant h \leqslant \infty$.

To prove this theorem, we will need a few preliminaries, which are interesting in their own right. First, recall that the Morava $K$-theories are all homotopy ring spectra by Pr.3.5.3, so we can talk about their left and right modules inside h Sp - we will focus on left modules, just to be consistent. To be more concrete, a left $E$-module structure for a spectrum $M$, where $E$ is a homotopy ring spectrum with multiplication $\mu: E \otimes E \rightarrow E$ and unit $\eta: \mathbf{S} \rightarrow E$, is an action map $\rho: E \otimes M \rightarrow M$ such that the diagrams
![img-78.jpeg](img-78.jpeg)
both commute in h Sp. We say that a spectrum $M$ admits a homotopy $E$-module structure if such an action map $\rho$ as above exists.
Exercise 3.5.9. Show that if $M$ admits an $E$-module structure, where $E$ is a field, then $M$ is a direct sum of shifts of $E$.

A simple corollary of Th.3.5.8 is the following. This might justify to some why Morava $K$-theories are considered the prime fields inside Sp .

Corollary 3.5.10. If $E$ is a field in $\mathrm{Sp}$, then $E$ is a shift of sums of a particular $\mathrm{K}(h)$.
Proof. By Exc.3.5.9 the homotopy groups of $E$ admit the structure of a free $\mathrm{K}(h)_{*}$-module. Choosing maps $\bigoplus \mathrm{K}(h)\left[n_{\alpha}\right] \rightarrow E$ in $\operatorname{LMod}_{\mathrm{K}(h)}(\mathrm{h} \mathrm{Sp})$ for a choice of generators for this free $\mathrm{K}(n)$-module, we obtain a map of spectra which induces an isomorphism on homotopy groups by construction.

End of lecture 18 and week 10

The category of left $\mathrm{K}(h)$-modules is surprisingly robust.
Proposition 3.5.11. Let $f: X \rightarrow Y$ be a map of spectra, and suppose that $X$ and $Y$ both have the structure of a homotopy $\mathrm{K}(h)$-module. Then the induced map $\pi_{*} X \rightarrow \pi_{*} Y$ is a morphism of $\mathbf{F}_{p}\left[v_{h}^{\Sigma}\right]$-modules.

This is a very surprising property! ${ }^{11}$
Proof. First, we write $f$ as the composition

$$
X \rightarrow \mathrm{~K}(h) \otimes X \xrightarrow{\mathrm{id} \otimes f} \mathrm{~K}(h) \otimes Y \rightarrow Y
$$

which follows from the fact that $X$ and $Y$ are both $\mathrm{K}(h)$-modules. As each of the maps above are all $\mathrm{K}(h)$-module maps except the first one, we are reduced to the case where $Y=\mathrm{K}(h) \otimes X$. As $\mathrm{K}(h)$ is a field in Sp and $X$ is hence a free $\mathrm{K}(h)$-module, we are then also reduced to the case where $X=\mathrm{K}(h)$. In this case, we are reduced to showing that the two unit maps

$$
\eta_{L}, \eta_{R}: \mathrm{K}(h) \rightarrow \mathrm{K}(h) \otimes \mathrm{K}(h)
$$

induce the same map on homotopy groups, ie, we need to show $\eta_{L}\left(v_{h}\right)=\eta_{R}\left(v_{h}\right)$. The spectrum $\mathrm{K}(h) \otimes \mathrm{K}(h)$ comes equipped with two complex orientations from $\eta_{L}$ and $\eta_{R}$, which gives two formal group laws over the ring $R=\pi_{\mathrm{ev}}(\mathrm{K}(h) \otimes \mathrm{K}(h))$-we only want to deal with even homotopy groups here to avoid any Koszul sign rules. Both of these formal group laws, written as $f_{L}$ and $f_{R}$, have height $h$, and are moreover strictly isomorphic; see Pr.3.2.13. In particular, by construction we see that the $p$-series of $f_{L}$ is $\eta_{L}\left(v_{h}\right) t^{p^{h}}$ modulo $t^{p^{h}+1}$ and the $p$-series of $f_{R}$ is $\eta_{R}\left(v_{h}\right) t^{p^{h}}$ modulo $t^{p^{h}+1}$. The strict isomorphism between $f_{L}$ and $f_{R}$ then shows that $\eta_{R}\left(v_{h}\right)=\eta_{L}\left(v_{h}\right)$.

Proposition 3.5.12. If $X$ is a homotopy $\mathrm{K}(h)$-module and $Y$ is a retract of $X$, then $Y$ is a homotopy $\mathrm{K}(h)$-module.

Proof. From the hypotheses above, there are maps $Y \rightarrow X \rightarrow Y$ such that their composition is homotopic to the identity. In particular, the other composite $X \rightarrow Y \rightarrow X$ induces a map of $\mathbf{F}_{p}\left[v_{h}^{\pm}\right]$-module on $\pi_{*}$ by Pr.3.5.11, so the image of this composite in $X$ is a $\mathbf{F}_{p}\left[v_{h}^{\pm}\right]$-submodule of $\pi_{*} X$. Choosing generators $\alpha \in \pi_{n_{\alpha}} X$ for this submodule, which is necessarily free as $\mathbf{F}_{p}\left[v_{h}^{\pm}\right]$ is a graded field, we obtain a map $\bigoplus_{\alpha} \mathbf{S}\left[n_{\alpha}\right] \rightarrow X$, which we base-change to $\bigoplus_{\alpha} \mathrm{K}(h)\left[n_{\alpha}\right] \rightarrow X$ which picks out this free submodule. In particular, the composite

$$
\bigoplus_{\alpha} \mathrm{K}(h)\left[n_{\alpha}\right] \rightarrow X \rightarrow Y
$$

induces an isomorphism on homotopy groups by design, which gives $Y$ a $\mathrm{K}(h)$-module structure.

We cannot quite prove the above theorem with the information we've collected so far; another important result has to be used, which we will prove later as a consequence of the nilpotence theorem; see ??.

Proposition 3.5.13. Let $E$ be a nonzero homotopy ring spectrum which is p-local with respect to some prime $p$. Then for some $0 \leqslant h \leqslant \infty$ the spectrum $\mathrm{K}(h) \otimes E$ is also nonzero.

[^0]
[^0]:    ${ }^{11}$ For example, the Adams operation $\psi^{-1}: \mathrm{KU} \rightarrow \mathrm{KU}$ is a map of spectra, even of $\mathbf{E}_{\infty}$-rings, and both the left-hand and right-hand side of this equation are canonically modules over themselves. However, the induced map on homotopy groups cannot be KU-linear, as it sends the Bott class $u \in \pi_{2} \mathrm{KU}$ to $-u$.

Proof of Th.3.5.8. As $E$ is a field it is nonzero. If $E$ is rational, then $E$ is a homotopy $\mathbf{Q}=\mathrm{K}(0)$-module by Cor.2.5.8, and we are done. Otherwise, there is a unique prime number $p$ such that $E$ is $p$-local. By Pr.3.5.13, we see that $\mathrm{K}(n) \otimes E$ is nonzero for some $1 \leqslant n \leqslant \infty$, the $n=0$ case taken by rational argument. As $E$ is a field and $\mathrm{K}(n) \otimes E$ is a nonzero homotopy $E$-module which by Exc.3.5.9 is a sum of shifts of $E$, then we see the unit map $E \rightarrow \mathrm{~K}(n) \otimes E$ recognises $E$ as a retract of $\mathrm{K}(n) \otimes E$. As this spectrum has a natural $\mathrm{K}(n)$-module structure, we see that $E$ also inherits a $\mathrm{K}(n)$-module structure from Pr.3.5.12.

Let us come back now to the problem of constructing the homotopy ring structure on the $\mathrm{K}(h)$ 's.

Proposition 3.5.14. Let $p$ be a prime and $k$ a positive integer. Then $C(k)$ has the natural structure of a homotopy associative $\mathrm{MU}_{(p)}$-algebra, meaning, an object in $\operatorname{Alg}\left(\mathrm{h} \operatorname{Mod}_{\mathrm{MU}_{(p)}}\right)$.
Proof. The unit map for $C(k)$ is the natural quotient map $\eta: \mathrm{MU}_{(p)} \rightarrow C(k)$, so it is left to construct the multiplication map $\mu: C(k) \otimes_{\mathrm{MU}_{(p)}} C(k) \rightarrow C(k)$. The relative tensor product above, which we will write as $X$, can be recognised as the total cofibre of the commutative diagram of $\mathrm{MU}_{(p)}$-modules
![img-79.jpeg](img-79.jpeg)

Here, a total cofibre of a square is obtained by first removing the lower-right corner, taking a pushout, and then taking the cofibre of the natural map from this pushout into the lower-right corner. By Exc.3.5.16 below, this total cofibre can also be computed by taking the cofibres of the horizontal maps, which yields a map

$$
C(k)[2 k] \simeq C(k) \otimes_{\mathrm{MU}_{(p)}} \mathrm{MU}_{(p)}[2 k] \xrightarrow{\mathrm{id}_{C(k)} \otimes x_{k}} C(k) \otimes_{\mathrm{MU}_{(p)}} \mathrm{MU}_{(p)} \simeq C(k)
$$

and then taking another cofibre, which produces the desired $C(k) \otimes_{\mathrm{MU}_{(p)}} C(k)$. Let us also write $Q$ for the total cofibre of the diagram
![img-80.jpeg](img-80.jpeg)

Using the same techniques as above, we can compute $Q$ as the cofibre of the map $\cdot x_{k}: \mathrm{MU}_{(p)}[2 k] \rightarrow$ $C(k)$-even though $x_{k}=0$ inside $\pi_{*} C(k)$, we can still formally act on $C(k)$ by $x_{k}$ as it is an $\mathrm{MU}_{(p)}$-module spectrum. The fact that $x_{k}$ is zero in $C(k)$ means that the cofibre sequence for $Q$ splits, meaning there is a map $\alpha: Q \rightarrow C(k)$ is the diagram
![img-81.jpeg](img-81.jpeg)

recognising that the map $x_{k}: \mathrm{MU}_{(p)}[2 k] \rightarrow C(k)$ is zero as a map of $\mathrm{MU}_{(p)}$-modules. Here $q$ is the canonical map from the cofibre sequence defining $Q$. The relation $\alpha q \simeq \mathrm{id}$ will be used multiple times now.

Now for some translations. So, we are after a $\mu: X \rightarrow C(k)$ in $\mathrm{MU}_{(p)}$-modules such that precomposition with $\eta$ is homotopic to the identity. In other words, we want to find an element $\mu$ in $[X, C(k)]_{\mathrm{MU}_{(p)}}$ which hits the identity under the map

$$
[X, C(k)]_{\mathrm{MU}_{(p)}} \xrightarrow{\left(\eta \otimes \mathrm{id}_{C(k)}\right)^{*}}[C(k), C(k)]_{\mathrm{MU}_{(p)}}
$$

As $\alpha q \simeq$ id, then the map

$$
[C(k), C(k)]_{\mathrm{MU}_{(p)}} \rightarrow[C(k), C(k)]_{\mathrm{MU}_{(p)}}
$$

is injective, so it suffices to find a map $\mu: X \rightarrow C(k)$ such that $\mu(\eta \otimes \mathrm{id}) \alpha \simeq \alpha$ as maps of $\mathrm{MU}_{(p)}-$ modules. Notice that $(\eta \otimes \mathrm{id}) \alpha$ is actually homotopic to the map $\beta: Q \rightarrow X$ induced by the obvious map of squares and then taking cofibres-checking this is an exercise in definitions; see Exc.3.5.17. In other words, we would like a map $\mu: X \rightarrow C(k)$ such that it factors $\alpha: Q \rightarrow C(k)$ as the composite

$$
Q \xrightarrow{\beta} X \xrightarrow{\mu} C(k)
$$

in $\mathrm{MU}_{(p)}$-modules. ${ }^{12}$ To achieve this factorisation, we can equivalently show that the composition of maps of $\mathrm{MU}_{(p)}$-modules

$$
F \rightarrow Q \xrightarrow{\alpha} C(k)
$$

is nullhomotopic, where $F$ is the fibre of $\beta$. Note that $F$ can be computed using the two squares above. In other words, the cofibre of $\beta$ is total cofibre of the cofibre of the natural map between the above diagrams
![img-82.jpeg](img-82.jpeg)
so the cofibre of $\beta$ is precisely $\mathrm{MU}_{(p)}[4 k+2]$ and $F$ is $\mathrm{MU}_{(p)}[4 k+1]$. It is then clear that (3.5.15) is nullhomotopic, as the group it lives in vanishes:

$$
[F, C(k)]_{\mathrm{MU}_{(p)}} \simeq\left[\mathrm{MU}_{(p)}[4 k+1], C(k)\right]_{\mathrm{MU}_{(p)}} \simeq[\mathbf{S}[4 k+1], C(k)] \simeq \pi_{4 k+1} C(k)=0
$$

One should next check that our choice of multiplication map is associative. The argument follows the same pattern as the proof above: recognise the triple $\mathrm{MU}_{(p)}$-relative tensor product of $C(k)$ as a total cofibre of a cube, compare this cube to the same cube where we replace the initial vertex with 0 , and repeat the same sort of formal arguments. This is left as an exercise; see Exc.3.5.18.

[^0]
[^0]:    ${ }^{12}$ Everything we have done above formally implies this, but notice that if we have such a $\mu$ with $\mu \beta \simeq \alpha$, then we have equivalences

    $$
    \mu(\eta \otimes \mathrm{id}) \simeq \mu(\eta \otimes \mathrm{id}) \alpha q \simeq \mu \beta q \simeq \alpha q \simeq \mathrm{id}
    $$

    as desired.

Exercise 3.5.16. Given a commutative diagram
![img-83.jpeg](img-83.jpeg)
in an $\infty$-category $\mathcal{C}$ with finite colimits, show that the total cofibre of $Q$ can be computed by either taking cofibres vertically, then horizontally, or horizontally, then vertically.
Exercise 3.5.17. Show that the map $\beta$ is homotopic (as a map of MU-modules) to the composite $Q \xrightarrow{\alpha} C(k) \xrightarrow{\eta} X$.
Exercise 3.5.18. Show that the multiplication map $\mu$ constructed on $C(k)$ in Pr.3.5.14 is associative in the homotopy category of $\mathrm{MU}_{(p)}$-modules.

This puts us in the position to prove Pr.3.5.3.
Proof of Pr.3.5.3. By Pr.3.5.14, each of the $C(k)$ 's is a homotopy ring spectrum. It follows that finite tensor products of the $C(k)$ 's are homotopy ring spectra, and the infinite tensor product is a filtered colimit of such finite guys which also inherits a homotopy ring spectrum structure. The resulting spectrum $\mathrm{K}(n)$ after inverting $v_{n}$ is also a homotopy ring spectrum; see Exc.2.5.13.

End of lecture 19

# 3.6 Not-yet typed notes 

- Lecture 20 (June 26th) was on Nilpotence I implies Nilpotence II, following [Lura, Lec.25] and [HS98, Th. $3 \& 2$ ].
- Lecture 21 (July 1st) was on Nilpotence II implies Thick subcategory theory, following [Lura, Lec.26], [HS98, Th. $7 \&$ §2], and [DLS19, §3].
- Lecture 22 (July 3rd) was on the Periodicity Theorem following [Lura, Lec.27] and [DLS19, §5]. This is the last lecture with material to be covered on the exam.
- Lecture 23 (July 8th) was finishing up the discussion from the periodicity theorem and the chromatic fracture square following [Lura, Lec.23] and [DLS19, §6].
- Lecture 24 (July 10th) was on the Bousfield classes of $E(n)$ and $K(n)$ and smashing localisations using the previous notes as well as [Lura, Lec.29] and [DFHH14, §6].
- Lecture 25 (July 15) was on Morava $E$-theory and an outlook of applications following [Lura, Lec $21 \& 35$ ].
- Lecture 26 (July 17) was a review and question session before the exam. Good luck!

# 3.7 The Nilpotence theorem 

Now that we have these Morava $K$-theories, we would like to delve into a study of spectra using these extra fields. We will start with one of the most famous theorems in chromatic homotopy theory: the Nilpotence theorem as conjectured by Ravenel [Rav84] proven by Devinatz-Hopkins-Smith [DHS88]. There are a few different forms of this theorem, and our goal for today will be to move from one form to another.

Theorem 3.7.1 (Nilpotence theorem 1). Let $R$

### 3.8 The Thick subcategory theorem

### 3.9 The Periodicity theorem

### 3.10 Bousfield classes of $\mathrm{K}(n)$ and $E(n)$

Theorem 3.10.1 (Chromatic fracture square). Let $p$ be a prime and $0<n<\infty$. Then for any spectrum $X$, there the natural square
![img-84.jpeg](img-84.jpeg)
is a pullback.
Remark 3.10.2. Let us point out that not all Bousfield localisations are smashing. For example, for a fixed prime $p$, the natural map

$$
X \otimes \mathbf{S}_{p}^{\wedge} \rightarrow X_{p}^{\wedge}
$$

is only assured to be an equivalence for finite spectra. This can be seen from the facts that the class of all those spectra $X$ such that the above morphism is an equivalence contains $X$ and is moreover closed under finite sums and cofibres. To see this latter point, we write $X_{p}^{\wedge}=\lim X_{p}^{\wedge}$ and using that finite sums are a limit and cofibres are a shift of a limit, we then commute these operations past the functor $(-)_{p}^{\wedge}$. There are nonfinite spectra such that (3.10.3) is not an equivalence though. For example, for $X=\mathbf{S}\left[\frac{1}{p}\right]$ we quickly see that $\left(\mathbf{S}\left[\frac{1}{p}\right]\right)_{p}^{\wedge}=0$, however, we also have the equivalence $\mathbf{S}\left[\frac{1}{p}\right] \otimes \mathbf{S}_{p}^{\wedge} \simeq \mathbf{Q}_{p} \neq 0$.

### 3.11 Lubin-Tate and Morava $E$-theories

Our applications of the Landweber exact functor theorem have been quite straight-forward, as in each case we have designed a theory, such as BP or $E(n)$, to be Landweber exact from the get-go. What we would like to do here, is to study a different family of Landweber exact theories which occur from formal groups over perfect fields of positive characteristic. Of course,

a formal group over such a field can never be Landweber exact as $p=v_{0}=0$, but Lubin-Tate deformation theory well help us to produce a Landweber exact theory from this data.

For this section, let $\kappa$ be a field of positive characteristic $p>0$.
Definition 3.11.1. An infinitesimal thickening of $\kappa$ is a surjective ring homomorphism $\rho: R \rightarrow$ $\kappa$ from a local ring $R$ with maximal ideal $\mathfrak{m}=\operatorname{ker}(\rho)$ such that $\mathfrak{m}$ is nilpotent and each $\mathfrak{m}^{n} / \mathfrak{m}^{n+1}$ is a finite dimensional $\kappa$-vector space. In other words, $R$ is an Artin local ring with residue field $\kappa$.

Let us now fix a formal group law $f$ of height exactly $n$ over $\kappa$.
Definition 3.11.2. Let $R$ be an infinitesimal thickening of $\kappa$. A deformation of $f$ over $R$ is a choice of formal group law $g$ over $R$ such that $\rho_{*} g$ is isomorphic to $f$ as formal group laws over $\kappa$. An isomorphism between two deformations $f$ and $f^{\prime}$ over $R$ is an isomorphism of formal groups $h(x) \in R \llbracket x \rrbracket$ such that $h(x) \equiv x$ modulo $\mathfrak{m}$. We will write $\operatorname{Def}(R)$ for the set of isomorphism classes of deformations of $f$ over $R .{ }^{13}$

We will now define a very specific "deformation" of $f$-it will not be a literal deformation, as our $R$ will be a complete local ring which is decidably not Artin, but we will see why it is interesting shortly.

Construction 3.11.3. Let $A$ be the ring

$$
A=W(\kappa) \llbracket v_{1}, \ldots, v_{n-1} \rrbracket
$$

where $W(\kappa)$ is the Witt vectors of $\kappa$, so the universal characteristic zero ring over $\kappa$ such that its quotient by the ideal generated by $p$ recovers $\kappa$. In particular, we have a canonical isomorphism $W(\kappa) / p \simeq \kappa$. For $\kappa=\mathbf{F}_{p}$ we have $W\left(\mathbf{F}_{p}\right) \simeq \mathbf{Z}_{p}$, so this is the example that one should keep in mind. The ring $A$ is complete and local with respect to the ideal $\mathfrak{m}=\left(p, v_{1}, \ldots, v_{n-1}\right)$ and we clearly have $A / \mathfrak{m} \simeq \kappa$.

We now want to define a formal group law $g$ over this $A$. Recall that $f$ is classified by a map of rings $\varphi_{0}: L_{(p)} \rightarrow \kappa$, where there is a noncanonical isomorphism $L_{(p)} \simeq \mathbf{Z}_{(p)}[t_{1}, t_{2}, \ldots]$ where we can choose $t_{p^{n}-1}=v_{n}^{\text {uni }}$ to be the coefficient of $x^{p^{n}}$ in the $p$-series of the universal $p$-typical formal group law over $L_{(p)}$. As $f$ has height precisely $n$, we see that $\varphi_{0}\left(v_{i}\right)=0$ for all $0 \leqslant i \leqslant n-1$. Let $g$ be the formal group law over $A$ defined by any homomorphism $\varphi: L_{(p)} \rightarrow A$ which lifts $\varphi_{0}$ through the quotient by $\mathfrak{m}$, denoted by $\rho$, in other words, such that the diagram
![img-85.jpeg](img-85.jpeg)
commutes, and which also sends $v_{i}^{\text {uni }}$ to $v_{i}$ for $0 \leqslant i \leqslant n-1$. As $L_{(p)} \simeq \mathbf{Z}_{(p)}\left[t_{1}, t_{2}, \ldots\right]$, it is easy to construct such a factorisation $\varphi$.

[^0]
[^0]:    ${ }^{13}$ Notice that we do not require that a deformation keeps track of the isomorphism connecting $\rho_{*} g$ and $f$.

The following theorem of Lubin-Tate [LT66] shows that this construction does not (up to isomorphism) depend on the choice of factorisation $\varphi$.

Theorem 3.11.4 (Lubin-Tate theory). Let us further assume that $\kappa$ is perfect. The functor $\operatorname{Def}(-)$ from the category of infinitesimal thickenings of $\kappa$, thought of as a full subcategory of $\mathrm{CRing}_{/ \kappa}$ of commutative rings augmented over $\kappa$, to sets is corepresented by the pair $(A, g)$ from above, ie, for each infinitesimal thickening $(R, \rho)$ the natural map

$$
\operatorname{CRing}_{/ \kappa}(A, R) \rightarrow \operatorname{Def}(R), \quad(\psi: A \rightarrow R) \mapsto \psi_{*} g
$$

is a bijection.
We will not see a proof of this in this course, the proof in [LT66] is not difficult but would lead us too far astray; there is another distillation of Lubin-Tate's proof in [Lura, Lec.21].

Let us now observe that the pair $(A, g)$ is Landweber exact. Indeed, we only need to check that $\left(p, v_{1}, \ldots\right)$ is a regular ideal in $A$ for the fixed $p$ we are given, as $A$ is $p$-local. The fact that this ideal is regular is clear from our construction of $g$ and $\varphi: A$ is a domain so $p$ is a nonzero divisor, then $A / p \simeq \kappa\left[\left[v_{1}, \ldots, v_{n-1}\right]\right]$ and $\left(v_{1}, \ldots, v_{n-1}\right)$ is clearly a regular ideal in this ring. The assumption that $\varphi$ factored $\varphi_{0}$ and the fact that $f$ has height exactly $n$ tells us that $\varphi_{0}\left(v_{n}^{\text {uni }}\right)$ is a unit in $\kappa$, hence $v_{n}$ (of $g$ ) is also a unit in $A / \mathfrak{m} \simeq \kappa$, which finishes our check of the Landweber criterion.

Definition 3.11.5. Suppose $\kappa$ is a field ${ }^{14}$ of characteristic $p>0$ and $f$ is a formal group law of height exactly $n$ over $\kappa$. Let $A\left[u^{\pm}\right]$be the graded ring with $|u|=2$ and define a formal group law $G$ over $A\left[u^{\pm}\right]$as the gradification ${ }^{15}$ of $g$, so

$$
G(x, y)=\sum_{i, j \geqslant 0} a_{i j} u^{-i-j} x^{i} y^{i}, \quad g(x, y)=\sum_{i, j \geqslant 0} a_{i j} x^{i} y^{j}
$$

We then define $E(\kappa, f)$, the Lubin-Tate theory or Morava $E$-theory associated to $(\kappa, f)$, to be the spectrum associated to this Landweber exact pair $\left(A\left[u^{\pm}\right], G\right)$.

Remark 3.11.6. Notice that we did not need to use Th.3.11.4 to construct $E(\kappa, f)$, we only state it to justify that our construction of $(A, g)$ is a natural one.

Let us now summarise some facts about $E(\kappa, f)$ :

1. We can calculate the homotopy groups of $E(\kappa, f)$ directly from its definition

$$
\pi_{*} E(\kappa, f) \simeq A\left[u^{\pm}\right]=W(\kappa)\left\llbracket v_{1}, \ldots, v_{n-1} \rrbracket\left[u^{\pm}\right]\right.
$$

[^0]
[^0]:    ${ }^{14}$ For the construction of $E(\kappa, f)$ which we see below, it is not necessary that $\kappa$ be perfect, however, in all applications and for the greater theory to come together, see Th.3.11.7, we will need this assumption.
    ${ }^{15}$ Notice that this gradification process is necessary in this example. If we try to say that $A$ is graded by saying that $W(\kappa)$ sits in degree 0 and the $v_{i}$ 's all have degree $2\left(p^{i}-1\right)$, as they do topologically, then we notice that $v_{n}$ has the incorrect degree, as it is well defined inside $\kappa=A / \mathfrak{m}$ which is in degree 0 . In some sense, we could try to make $(A, g)$ and hence $E(\kappa, f)$ into a $2\left(p^{n}-1\right)$-periodic theory, but this would simply be a summand of the more standard 2-periodic theory we define here.

2. There is an equality of Bousfield classes $\langle E(\kappa, f)\rangle=\langle E(n)\rangle$, so we do not have any more interesting Bousfield localisations by constructing these Morava $E$-theories over the Johnson-Wilson theories we are already used to.
3. There is a homotopy commutative ring spectrum structure on $E(\kappa, f)$. This comes from the general machinery of the Landweber exact functor theorem; see Rmk.3.4.17.

This last point, that $E(\kappa, f)$ can be quite radically refined. In fact, the following theory is one of two main facts about $E(\kappa, f)$, the other being Th.3.11.9 to come, which show these theories are more robust that the Johnson-Wilson theories $E(n)$.

Theorem 3.11.7 (Goerss-Hopkins, Lurie). The Landweber exact functor theorem construction of $E(\kappa, f)$ above can be refined to a functor of $\infty$-categories

$$
\text { FGL } / \operatorname{Perf} \rightarrow \operatorname{CAlg}(\mathrm{Sp}), \quad(\kappa, f) \mapsto E(\kappa, f)
$$

where FGL / Perf is the 1-category of perfect field equipped with a formal group law over them and $\operatorname{CAlg}(\mathrm{Sp})$ is the $\infty$-category of $\mathbf{E}_{\infty}$-rings; see $\S 1.9$.

For this theorem, it is crucial that we only work over perfect fields. The proof of GoerssHopkins uses their famous obstruction theory; a proof can be found in [GH04] with a correction in [PV22, §7]. The proof of Lurie uses the idea that we can just try to directly prove Th.3.11.4 in spectral algebraic geometry, which leads to a very natural definition which is easy to manipulate, generalise, and compare with other definitions; see [Lur18, §5].

A formal consequence of Th.3.11.7, is that all automorphisms of a pair $(\kappa, f)$ act upon the $\mathbf{E}_{\infty}$-ring $E(\kappa, f)$ (just think of this as a spectrum for now, if you want) in an $\infty$-categorical sense.

Definition 3.11.8. We define the Morava stabiliser group of $(\kappa, f)$ to be $\mathbf{G}=\operatorname{Aut}(\kappa, f)$ the set of automorphisms of the pair $(\kappa, f)$ in the category FGL / Perf.

In the literature, one often fixes a formal group law $f$ over $\mathbf{F}_{p^{h}}$ such that $[p]_{f}(x)=x^{p^{h}}$ exactly, such as the Honda formal group law of In this case, one often just writes $E\left(\mathbf{F}_{p^{h}}, f\right)=E_{h}$ (ref) and likewise $\mathbf{G}\left(\mathbf{F}_{p^{h}}, f\right)=\mathbf{G}_{h}$. Using this notation, we have an action of $\mathbf{G}_{h}$ on the spectrum $E_{h}$. We will see some explicit examples of this towards the end of this lecture for $h=1$. It is important in general to note that the group $\mathbf{G}_{h}$ is profinite and that this group action is actually a continuous group action - we will continue to say this, as it is an important point in this area, although we will not discuss this in detail.

The following result of Devinatz-Hopkins is the second big reason why we like to work (ref) with these Morava $E$-theories.

Theorem 3.11.9 ([?]). The spectrum $E_{n}$ is $K(n)$-local ${ }^{16}$ and the natural map

$$
L_{\mathrm{K}(n)} \mathbf{S} \xrightarrow{\approx} E_{n}^{h \mathbf{G}_{h}}
$$

[^0]
[^0]:    ${ }^{16}$ This is not hard to see at all.

is an equivalence, where the right-hand side is the continuous homotopy fixed points ${ }^{17}$ of $E_{n}$ with respect to the $\mathbf{G}_{n}$-action. In particular, there is a spectral sequence

$$
E_{2} \simeq H^{s}\left(\mathbf{G}_{n} ; \pi_{t} E_{n}\right) \Longrightarrow \pi_{t-s} L_{\mathrm{K}(n)} \mathbf{S}
$$

whose $E_{2}$-page is the continuous group cohomology of $\mathbf{G}_{n}$ with coeffficients in the homotopy groups of $E_{n}$.

It seems rather straight forward then to try to compute the homotopy groups of the $\mathrm{K}(n)$ local sphere: one needs to first understand the Morava stabiliser group action on $\pi_{*} E_{n},{ }^{18}$ and we already know what these homotopy groups are, and then compute some group cohomology, and then compute some differentials - as we are well aware of, this is often easier said than done in practice. One we have a potential computation of the $\mathrm{K}(n)$-local sphere, then we can further leverage this to compute the stable homotopy groups of spheres - this is one of the most productive lines of thought in understanding large scale phenomena in the stable homotopy groups of spheres:

1. First, assume we have used Th.3.11.9 to understand $L_{\mathrm{K}(n)} \mathbf{S}$ to some extent.
2. Now, suppose by induction we understand $L_{E_{n-1}} \mathbf{S}$ to whatever extent and that we can also similarly understand $L_{E_{n-1}} L_{\mathrm{K}(n)} \mathbf{S}$. We can then inductively try to further understand $L_{E_{n}} \mathbf{S}$ using the pullback square
![img-86.jpeg](img-86.jpeg)
of Th.3.10.1.
3. The chromatic convergence theorem of Hopkins-Ravenel states that the natural map $\mathcal{F}^{(\text {ref })}$

$$
\mathbf{S}_{(p)} \xrightarrow{\simeq} \lim L_{E_{n}} \mathbf{S}
$$

is an equivalence, so we can use a Bousfield-Kan spectral sequence to try to understand $\pi_{*} \mathbf{S}_{(p)}$ from all of these $\pi_{*} L_{E_{n}} \mathbf{S}$ 's.
4. Finally, there is another pullback square
![img-87.jpeg](img-87.jpeg)

[^0]
[^0]:    ${ }^{17}$ The usual homotopy-fixed points of an object $X$ in an $\infty$-category $C$ with an action by a group $G$, so a functor $B G \rightarrow C$ which hits $X$, is simply $X^{B G}=\lim (B G \rightarrow C)$. To define these continuous homotopy-fixed points, one has to either work with the explicit model of such fixed points as Devinatz-Hopkins do or perhaps to use the condensed mathematical formalism of Clausen-Scholze; for example, see [Mor23].
    ${ }^{18}$ Apart from the case of $n=1$, we do not know a closed formula for the action of $\mathbf{G}_{n}$ on $\pi_{*} E_{n}$.

from Exc.2.6.16 which allows us to glue together all of the information about different primes.

Of course, each one of these steps (except the last one) is difficult, to say the least. To highlight this, let us study a low dimensional example in more detail.

For $n=1$, we can take $\kappa=\mathbf{F}_{p}$ and $f(x, y)=f_{m}(x, y)=x+y+x y$, which has height one as

$$
[p]_{f_{m}}(x, y)=(1+x)^{p}-1=\sum_{1 \leqslant i \leqslant p}\binom{p}{i} x^{i}=x^{p}
$$

As we said above, there is an isomorphism $W\left(\mathbf{F}_{p}\right) \simeq \mathbf{Z}_{p}$, so the homotopy groups of $E_{1}$ takes the form

$$
\pi_{*} E_{1} \simeq \mathbf{Z}_{p}\left[u^{ \pm}\right]
$$

This looks just like the homotopy groups of $\mathrm{KU}_{p}^{\times}$, the $p$-completion of complex $K$-theory; here we use Exc.2.6.11 to compute $\pi_{*} \mathrm{KU}_{p}^{\times} \simeq \mathbf{Z}_{p}\left[u^{ \pm}\right]$. In fact, as both of these complexoriented homotopy commutative ring spectra have an associated formal group law given by $F_{m}(x, y)=x+y+u x y$ over $\mathbf{Z}_{p}\left[u^{ \pm}\right]$, which by Rmk.3.4.15 gives us equivalences of spectra

$$
E_{1} \simeq E_{F_{m}} \simeq \mathrm{KU}_{p}^{\times}
$$

The group $\mathbf{G}_{1}$ in this case is $\mathbf{Z}_{p}^{\times}$, the group of units of the $p$-adic integers. The action of $\mathbf{Z}_{p}^{\times}$on $E_{1}$ is given by the stable Adams operations, which we write as $\psi^{\lambda}: E_{1} \rightarrow E_{1}$ for each $\lambda \in \mathbf{Z}_{p}^{\times}$. Just as the classical stable Adams operations, these are maps of $\mathbf{E}_{\infty}$-rings, so in particular, of homotopy commutative ring spectra, such that $\psi^{\lambda}(u)=\lambda u$.

Let us now restrict to the odd prime case, so $p \neq 2$. In this situation there is a split short exact sequence of abelian groups

$$
0 \rightarrow \mathbf{Z}_{p} \simeq\left(1+\mathbf{Z}_{p}\right) \rightarrow \mathbf{Z}_{p}^{\times} \rightarrow \mathbf{F}_{p}^{\times} \rightarrow 0
$$

given by including those $p$-adic integers with leading term 1 into $\mathbf{Z}_{p}^{\times}$. The splitting is the multiplicative lift $\mathbf{F}_{p}^{\times} \rightarrow \mathbf{Z}_{p}^{\times}$. In particular, we can now compute $E_{1}^{h \mathbf{Z}_{p}^{\times}}$in two steps: first, we take the $\mathbf{F}_{p}^{\times}$-fixed points, followed by the remaining $\mathbf{Z}_{p}$-fixed points. One usually calls $\mathrm{L}=E_{1}^{h \mathbf{F}_{p}^{\times}}$the periodic Adams summand, as the homotopy fixed point spectral sequence

$$
E_{2} \simeq H^{s}\left(\mathbf{F}_{p}^{\times}, \pi_{t} E_{1}\right) \Longrightarrow \pi_{t-s} \mathrm{~L}
$$

in concentrated in degree zero as $\left|\mathbf{F}_{p}^{\times}\right|=p-1$ is coprime to $p$, which immediately gives the isomorphism

$$
\pi_{*} \mathrm{~L} \simeq \mathbf{Z}_{p}\left[v_{1}^{ \pm}\right] \quad\left|v_{1}\right|=2(p-1)
$$

and the fact that $E_{1} \simeq \bigoplus_{0 \leqslant d \leqslant p-1} \mathrm{~L}[2 d]$. The group $\mathbf{Z}_{p}^{\times} / \mathbf{F}_{p}^{\times} \simeq \mathbf{Z}_{p}$ now has a topological generator given by $p+1$, which means that the fixed points $E_{1}^{h \mathbf{Z}_{p}^{\times}}$can be computed as the

fixed points of L by the action of $\psi^{p+1}$. More precisely, we can compute $E_{1}^{h \mathbf{Z}_{p}^{\times}}$as the equaliser of the two maps id, $\psi^{p+1}: \mathrm{L} \rightarrow \mathrm{L}$, or simply the fibre of the self-map $\psi^{p+1}-1$ on L . Let us now make some computations using this fibre sequence

$$
L_{\mathrm{K}(1)} \mathbf{S} \rightarrow \mathrm{L} \xrightarrow{\psi^{p+1}-1} \mathrm{~L}
$$

In degree 0 , the map $\psi^{p+1}-1$ is zero, as $\psi^{p+1}$ is a map of rings hence is the identity on $\mathbf{Z}_{p}$. This means that $\pi_{0} L_{\mathrm{K}(1)} \mathbf{S} \simeq \mathbf{Z}_{p}$ and $\pi_{-1} L_{\mathrm{K}(1)} \mathbf{S} \simeq \mathbf{Z}_{p}$-notice that localisations of connective things need not be connective. The next interesting degree is $2(p-1)$, where $\psi^{p+1}-1$ acts by multiplication by $(p+1)^{p-1}-1$ which is equal to $p \cdot m$ where $m$ is a unit in $\mathbf{Z}_{p}$. In particular, the effect on homotopy groups in degree $2(p-1)$ is injective, and we obtain $\pi_{2(p-1)} L_{\mathrm{K}(1)} \mathbf{S}=0$ and $\pi_{2(p-1)-1} L_{\mathrm{K}(1)} \mathbf{S} \simeq \mathbf{Z} / p \mathbf{Z}$. In general, we see that in degree $2(p-1) p^{r} s$ where $s \not \equiv 0$ modulo $p$, the map $\psi^{p+1}-1$ induces multiplication by $p^{r+1}$ up to a unit in $\mathbf{Z}_{p}$. In total, we obtain the following expression for the homotopy groups of $L_{\mathrm{K}(1)} \mathbf{S}$ at odd primes $p \neq 2$ :

$$
\pi_{d} L_{\mathrm{K}(1)} \mathbf{S} \simeq \begin{cases}\mathbf{Z}_{p} & d=0,-1 \\ \mathbf{Z} / p^{r+1} & d+1=2(p-1) p^{r} s, s \not p 0 \\ 0 & \text { else }\end{cases}
$$

Notice that the above expression holds for all $d \in \mathbf{Z}$, so we see that the $\mathrm{K}(1)$-local sphere has a many negative homotopy groups.

For $p=2$, the computation is more difficult. We still have a splitting

$$
\mathbf{Z}_{2}^{\times} \simeq\{ \pm 1\} \times\left(1+4 \mathbf{Z}_{2}\right) \simeq \mu_{2} \times \mathbf{Z}_{2}
$$

but in this case $E_{1}^{h \mu_{2}}$ is not a summand of $E_{1}$-in this case $E_{1}^{h \mu_{2}} \simeq \mathrm{KO}_{2}^{\wedge}$, which has much more complication homotopy groups. Nevertheless, one can still compute $\pi_{*} L_{\mathrm{K}(1)} \mathbf{S}$, which we draw in Fig.3.1. These homotopy groups are very closely related to the image of the $J$-homomorphism, a map $\pi_{*} O \rightarrow \pi_{*} \mathbf{S}$ from the (unstable) homotopy groups of the infinite orthogonal group to the (stable) homotopy groups of $\mathbf{S}$; see [Ada66] for starters. These kinds of periodic patterns occurring in the stable homotopy groups of spheres were first observed in the 1960 's, and one of the original goals of chromatic homotopy theory was the come up with other periodic families.

Let us now apply Th.3.10.1 to try to compute $L_{E_{1}} \mathbf{S}$ as well. There is a pullback square of
![img-88.jpeg](img-88.jpeg)
spectra
![img-89.jpeg](img-89.jpeg)

We know that $E(0) \simeq \mathbf{Q}$, so the upper-right spectrum is simply $\mathbf{S}_{\mathbf{Q}} \simeq \mathbf{Q}$.

![img-90.jpeg](img-90.jpeg)

Figure 3.1: Homotopy groups of $L_{\mathrm{K}(1)} \mathbf{S}$ at $p=2$. A tower of height $r$ represents a group $\mathbf{Z} / 2^{r} \mathbf{Z}$ and an infinite tower is a $\mathbf{Z}_{2}$. The blue part of the tower comes from the homotopy groups of $\mathrm{KO}_{2}^{<}$and the red part from $\mathrm{KO}_{2}^{<}[-1]$.

The last lecture was a question-and-answer session.
End of lecture 27 and the course

# Bibliography 

[ABG+14] Matthew Ando, Andrew J. Blumberg, David Gepner, Michael J. Hopkins, and Charles Rezk. An $\infty$ categorical approach to $R$-line bundles, $R$-module thom spectra, and twisted $R$-homology. J. Topol., 7(3):869893, 2014.
[ABG18] Matthew Ando, Andrew J. Blumberg, and David Gepner. Parametrized spectra, multiplicative Thom spectra and the twisted Umkehr map. Geom. Topol., 22(7):3761-3825, 2018.
[Ada66] John Frank Adams. On the groups J(X). (IV). Topology, 5:21-71, 1966.
[Ada74] J. F. Adams. Stable homotopy and generalised homology. Chicago Lectures in Mathematics. Chicago London: The University of Chicago Press. X, 373 p. $£ 3.00$ (1974)., 1974.
[AH61] Michael F. Atiyah and Friedrich Hirzebruch. Vector bundles and homogeneous spaces. Proc. Sympos. Pure Math. 3, 7-38 (1961)., 1961.
[Ang08] V. Angeltveit. Topological Hochschild homology and cohomology of A-infty ring spectra. Geometry \& Topology, 12(2):987-1032, 2008.
[Ati67] Michael F. Atiyah. $K$-theory. Lecture notes by D. W. Anderson. Fall 1964. With reprints of M. F. Atiyah: Power operations in $K$-theory; $K$-theory and reality. New York-Amsterdam: W.A. Benjamin, Inc. 166 p. (1967)., 1967.
[Boa64] Michael Boardman. On Stable Homotopy Theory and Some Applications. PhD thesis, University of Cambridge, 1964.
[Bou79] A. K. Bousfield. The localization of spectra with respect to homology. Topology, 18:257-281, 1979.
[BR20] David Barnes and Constanze Roitzheim. Foundations of stable homotopy theory, volume 185 of Camb. Stud. Adv. Math. Cambridge: Cambridge University Press, 2020.
[BV73] J. M. Boardman and R. M. Vogt. Homotopy invariant algebraic structures on topological spaces, volume 347 of Lect. Notes Math. Springer, Cham, 1973.
[DFHH14] Christopher L. Douglas, John Francis, André G. Henriques, and Michael A. Hill, editors. Topological modular forms. Based on the Talbot workshop, North Conway, NH, USA, March 25-31, 2007, volume 201. Providence, RI: American Mathematical Society (AMS), 2014.
[DHS88] Ethan S. Devinatz, Michael J. Hopkins, and Jeffrey H. Smith. Nilpotence and stable homotopy theory. I. Ann. Math. (2), 128(2):207-241, 1988.
[DLS19] Jack Morgan Davies, Tommy Lundemo, and Yuqing Shi. Chromatic homotopy theory reading group. Available at https://www.jmdavies.org/seminars/utrecht-2018-22/cht-i, 2019.
[EKMM97] A. D. Elmendorf, Igor Kříž, Michael A. Mandell, and J. P. May. Rings, modules, and algebras in stable homotopy theory. With an appendix by M. Cole., volume 47. Providence, RI: American Mathematical Society, 1997.
[GGN15] David Gepner, Moritz Groth, and Thomas Nikolaus. Universality of multiplicative infinite loop space machines. Algebr. Geom. Topol., 15(6):3107-3153, 2015.

[GH04] P. G. Goerss and M. J. Hopkins. Moduli spaces of commutative ring spectra. In Structured ring spectra, pages 151-200. Cambridge: Cambridge University Press, 2004.
[Goo90] Thomas G. Goodwillie. Calculus. I: The first derivative of pseudoisotopy theory. K-Theory, 4(1):1-27, 1990.
[Har23] Kevin Hartnett. An old conjecture falls, making spheres a lot more complicated. Quanta Magazine, 2023.
[Hat02] Allen Hatcher. Algebraic topology. Cambridge: Cambridge University Press, 2002.
[HS98] Michael J. Hopkins and Jeffrey H. Smith. Nilpotence and stable homotopy theory. II. Ann. Math. (2), 148(1):1-49, 1998.
[HS99] Mark Hovey and Neil P. Strickland. Morava K-theories and localisation., volume 666. Providence, RI: American Mathematical Society (AMS), 1999.
[Joy02] A. Joyal. Quasi-categories and Kan complexes. J. Pure Appl. Algebra, 175(1-3):207-222, 2002.
[KN22] Achim Krause and Thomas Nikolaus. Bökstedt periodicity and quotients of DVRs. Compos. Math., 158(8):1683-1712, 2022.
[Lan76] Peter S. Landweber. Homological properties of comodules over $M U_{\#}(M U)$ and $B P_{\#}(B P)$. Am. J. Math., $98: 591-610,1976$.
[Lan21] Markus Land. Introduction to infinity-categories. Compact Textb. Math. Cham: Birkhäuser, 2021.
[Lew91] L.G.jr. Lewis. Is there a convenient category of spectra? J. Pure Appl. Algebra, 73(3):233-246, 1991.
[LT66] J. Lubin and J. Tate. Formal moduli for one-parameter formal Lie groups. Bull. Soc. Math. Fr., 94:49-59, 1966 .
[Lura] Jacob Lurie. Chromatic homotopy theory (for Math 252x (offered Spring 2010 at Harvard)). Available at https://www.math.ias.edu/ lurie/, from 2010.
[Lurb] Jacob Lurie. Kerodon. https://kerodon.net.
[Lur04] Jacob Lurie. Derived algebraic geometry. PhD thesis, Massachusetts Institute of Technology, 2004.
[Lur09a] Jacob Lurie. A survey of elliptic cohomology. In Algebraic topology. The Abel symposium 2007. Proceedings of the fourth Abel symposium, Oslo, Norway, August 5-10, 2007, pages 219-277. Berlin: Springer, 2009.
[Lur09b] Jacob Lurie. Higher topos theory, volume 170. Princeton, NJ: Princeton University Press, 2009.
[Lur17] Jacob Lurie. Higher algebra. Available at https://www.math.ias.edu/ lurie/, 2017.
[Lur18] Jacob Lurie. Elliptic Cohomology II: Orientations. Available at https://www.math.ias.edu/ lurie/, April 2018 version, 2018.
[Mas53] W. S. Massey. Exact couples in algebraic topology. I.-V. Ann. Math. (2), 56:363-396, 1953.
[Mau63] C. R. F. Maunder. The spectral sequence of an extraordinary cohomology theory. Proc. Camb. Philos. Soc., $59: 567-574,1963$.
[May77] J. Peter May. $E_{\infty}$ ring spaces and $E_{\infty}$ ring spectra. With contributions by Frank Quinn, Nigel Ray, and Jorgen Tornehave, volume 577 of Lect. Notes Math. Springer, Cham, 1977.
[Mei18] Lennart Meier. Introduction to stable homotopy theory. Lecture notes, available at https://webspace. science.uu.nl/ meier007/IntroStable.pdf, 2018.
[Mei19] Lennart Meier. Elliptic Homology and Topological Modular Forms. Available at http://www.staff.science. uu.nl/ meier007/TMF-Lecture.pdf, January 2019.
[MMSS01] M. A. Mandell, J. P. May, S. Schwede, and B. Shipley. Model categories of diagram spectra. Proc. Lond. Math. Soc. (3), 82(2):441-512, 2001.

[Mor85] Jack Morava. Noetherian localisations of categories of cobordism comodules. Ann. Math. (2), 121:1-39, 1985 .
[Mor23] Itamar Mor. Picard and brauer groups of $\mathrm{k}(\mathrm{n})$-local spectra via profinite galois descent, 2023.
[MRW77] Haynes R. Miller, Douglas C. Ravenel, and W. Stephen Wilson. Periodic phenomena in the Adams-Novikov spectral sequence. Ann. Math. (2), 106:469-516, 1977.
[Pet19] Eric Peterson. Formal geometry and bordism operations. With appendices by Nathaniel Stapleton and Michael Hopkins., volume 177 of Camb. Stud. Adv. Math. Cambridge: Cambridge University Press, 2019.
[Pst21] Piotr Petragowski. Finite height chromatic homotopy theory. Lecture notes, available at https://people. math.harvard.edu/ piotr/252y_notes.pdf, 2021.
[PV22] Piotr Petragowski and Paul VanKoughnett. Abstract Goerss-Hopkins theory. Adv. Math., 395:51, 2022. Id/No 108098.
[Qui69] D. Quillen. On the formal group laws of unoriented and complex cobordism theory. Bull. Am. Math. Soc., $75: 1293-1298,1969$.
[Rav84] Douglas C. Ravenel. Localization with respect to certain periodic homology theories. Am. J. Math., 106:351$414,1984$.
[Rav04] Douglas C. Ravenel. Complex cobordism and stable homotopy groups of spheres. 2nd ed. Providence, RI: AMS Chelsea Publishing, 2nd ed. edition, 2004.
[Rog23] John Rognes. MAT4580/MAT9580 Spring 2023, Chromatic Homotopy Theory. Lecture notes, available at https://www.uio.no/studier/emner/matnat/math/MAT9580/v23/documents/chromatic.pdf, 2023.
[Sch12] Stefan Schwede. Symmetric spectra. available at http://www.math.uni-bonn.de/people/schwede/ SymSpec-v3.pdf, 2012.
[Shu08] Michael A. Shulman. Set theory for category theory, 2008.
[Sil86] Joseph H. Silverman. The arithmetic of elliptic curves., volume 106. Springer, New York, NY, 1986.
[Swi02] Robert M. Switzer. Algebraic topology - homology and homotopy. Class. Math. Berlin: Springer, reprint of the 1975 edition edition, 2002.
[Wei94] Charles A. Weibel. An introduction to homological algebra., volume 38. Cambridge: Cambridge University Press, 1994.
[Whi56] George W. Whitehead. Homotopy groups of joins and unions. Trans. Am. Math. Soc., 83:55-69, 1956.
[Wür86] Urs Würgler. Commutative ring-spectra of characteristic 2. Comment. Math. Helv., 61:33-45, 1986.