from src.simple_invoicing.domain.TreeStruct import Node
import pytest

@pytest.fixture
def tree():
    '''
                 1
                / \
               2   3
              /     \
             4       5  
    '''
    n1 = Node("1")
    n2 = Node("2", parent=n1)
    n3 = Node("3", parent=n1)
    n4 = Node("4", parent=n2)
    n5 = Node("5", parent=n3)

    return (n1, n2, n3, n4, n5)



def test_child_assignation_to_node(tree):
    n1, n2, n3, n4, n5 = tree

    assert n2 in n1
    assert n3 in n1
    assert n4 not in n1
    assert n5 not in n1
    assert n4 in n2
    assert n5 in n3
    assert n5 not in n2

def test_leaves_property(tree):
    n1, n2, n3, n4, n5 = tree

    assert n2 not in n1.leaves
    assert n3 not in n1.leaves
    assert n4 in n1.leaves
    assert n5 in n1.leaves
    assert n4 in n2.leaves
    assert n5 in n3.leaves

def test_path_property(tree):
    n1, n2, n3, n4, n5 = tree

    assert n1.path == "1"
    assert n2.path == "1.2"
    assert n3.path == "1.3"
    assert n4.path == "1.2.4"
    assert n5.path == "1.3.5"

def test_get_root_and_parent_of_nodes(tree):
    n1, n2, _, n4, _ = tree

    assert n1 == n4.root
    assert n1 == n2.parent
    assert n1.parent is None
    assert n1.is_internal()
    assert n2.is_internal()
    assert not n4.is_internal()


def test_node_deletion_given_one_child(tree):
    n1, n2, n3, n4, n5 = tree

    assert n1.leaves == set([n4, n5])

    n3.delete()

    assert n1.leaves == set([n4])


def test_node_assignation_is_idempotent(tree):
    n1, n2, n3, n4, n5 = tree

    assert n4 in n1.leaves
    assert len(n1.leaves) == 2

    child4 = Node("4", parent=n2)

    assert n4 in n1.leaves
    assert child4 in n1.leaves
    assert len(n1.leaves) == 2
    assert n4 == child4
    assert n4 is not child4
    assert n1.leaves == set([n4, n5])
