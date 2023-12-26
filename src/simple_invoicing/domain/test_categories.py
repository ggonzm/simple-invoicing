from model import Category


def test_subcategory_assignation_to_category():
    root = Category("Raíz desnuda")
    subcategory1 = Category("Hueso", parent=root)
    subcategory2 = Category("Pepita", parent=root)

    assert root._subcategories["HUESO"] == subcategory1
    assert root._subcategories["PEPITA"] == subcategory2


def test_get_root_category():
    root = Category("Raíz desnuda")
    subcategory1 = Category("Hueso", parent=root)
    subcategory2 = Category("Primera", parent=subcategory1)

    assert root == subcategory2.get_root()


def test_get_final_subcategories():
    root = Category("Raíz desnuda")
    subcategory1 = Category("Hueso", parent=root)
    subcategory2 = Category("Pepita", parent=root)
    subcategory3 = Category("Primera", parent=subcategory1)
    subcategory4 = Category("Primera", parent=subcategory2)
    
    assert root.get_leaves() == set([subcategory3, subcategory4])

def test_category_deletion_given_one_subcategory():
    root = Category("Raíz desnuda")
    subcategory1 = Category("Hueso", parent=root)
    subcategory2 = Category("Pepita", parent=root)
    subcategory3 = Category("Primera", parent=subcategory1)
    subcategory4 = Category("Primera", parent=subcategory2)
    
    subcategory2.delete()

    assert root.get_leaves() == set([subcategory3])

