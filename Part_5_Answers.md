1. Reachability vs. Feasibility

Reachability checks whether a cell can be entered physically. In the implementation, get_neighbors() excludes cells outside the grid boundaries and cells containing walls. Feasibility checks whether entering a physically reachable cell is permitted by the logical safety rules.
For each candidate neighbor, A* clears the previous facts, loads that tile’s facts, and calls forward_chain(). If the Knowledge Base deduces Retreat, the continue statement skips the neighbor before it enters the priority queue. Therefore, a tile can be physically reachable but logically infeasible. For example, (1, 0) is rejected because its facts lead to Retreat.


2. Declarative vs. Procedural Paradigms

The KnowledgeBase separates the game’s rules from the agent’s movement algorithm. Rules describe which conclusions follow from particular premises, while the general forward_chain() method applies those rules. This also supports deductions where one rule’s conclusion becomes another rule’s premise.
If 50 new game rules are added, they can be registered using tell_rule() without adding corresponding conditional branches inside A*. A procedural approach would require more conditions and careful handling of their dependencies, making the movement code harder to maintain. The declarative approach keeps the search code stable, although processing more rules increases inference work.


3. Modus Ponens & Horn Clauses

The rule TargetVisible ∧ HasDust ⇒ SafeToEngage is a definite Horn clause because it contains a conjunction of premises and one positive conclusion. Modus Ponens allows the conclusion to be inferred when the implication is known and its premises are true.
The implementation checks the premises using all(premise in self.facts for premise in premises). When every premise is present, it adds the conclusion to the fact set. The while loop repeats until no new facts are added, allowing SafeToEngage to combine with BloodseekerMissing and deduce Retreat.