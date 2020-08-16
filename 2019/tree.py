class Tree:
    parent = ""
    children = []
    name = ""

    def __init__(self, name, parent="", children=[]):
        self.name = name
        self.children = [child for child in children if isinstance(child, Tree)]
        self.parent = parent

    def __repr__(self):
        return self.name

    def add_child(self, child):
        if isinstance(child, Tree):
            self.children.append(child)

    def count_children(self):
        return len(self.children)

    def count_descendants(self):
        return len(self.children) + sum(
            [child.count_descendants() for child in self.children]
        )

    def get_descendants(self):
        return self.children + [child.get_descendants() for child in self.children]

    def get_ancestors(self):
        if self.parent == "":
            return []
        else:
            result = self.parent.get_ancestors()
            result.insert(0, self.parent)
            return result

    def get_common_ancestor(self, other):
        my_parents = [self] + self.get_ancestors()
        his_parents = [other] + other.get_ancestors()
        common = [x for x in my_parents if x in his_parents]
        if not common:
            return None
        return common[0]

    def get_degree_of_separation(self, other):
        my_parents = [self] + self.get_ancestors()
        his_parents = [other] + other.get_ancestors()
        common = self.get_common_ancestor(other)
        return my_parents.index(common) + his_parents.index(common)
