from unittest import TestCase

from colosseum import engine as css_engine
from colosseum.constants import AUTO, INLINE, BLOCK, TABLE, Choices
from colosseum.declaration import CSS, validated_property
from colosseum.dimensions import Box
from colosseum.units import px, percent

from .utils import Display, TestNode


class PropertyChoiceTests(TestCase):
    def test_no_choices(self):
        class MyObject:
            prop = validated_property('prop', choices=Choices())

        obj = MyObject()

        with self.assertRaises(ValueError):
            obj.prop = 10
        with self.assertRaises(ValueError):
            obj.prop = 20 * px
        with self.assertRaises(ValueError):
            obj.prop = 30 * percent
        with self.assertRaises(ValueError):
            obj.prop = 'a'
        with self.assertRaises(ValueError):
            obj.prop = 'b'
        with self.assertRaises(ValueError):
            obj.prop = None

        # Check the error message
        try:
            obj.prop = 'invalid'
            self.fail('Should raise ValueError')
        except ValueError as v:
            self.assertEqual(str(v), "Invalid value 'invalid' for CSS property 'prop'; Valid values are: ")

    def test_allow_length(self):
        class MyObject:
            prop = validated_property('prop', choices=Choices(length=True))

        obj = MyObject()

        obj.prop = 10
        obj.prop = 20 * px
        obj.prop = 30 * percent
        with self.assertRaises(ValueError):
            obj.prop = 'a'
        with self.assertRaises(ValueError):
            obj.prop = 'b'
        with self.assertRaises(ValueError):
            obj.prop = None

        # Check the error message
        try:
            obj.prop = 'invalid'
            self.fail('Should raise ValueError')
        except ValueError as v:
            self.assertEqual(str(v), "Invalid value 'invalid' for CSS property 'prop'; Valid values are: <length>")

    def test_allow_percentage(self):
        class MyObject:
            prop = validated_property('prop', choices=Choices(percentage=True))

        obj = MyObject()

        with self.assertRaises(ValueError):
            obj.prop = 10
        with self.assertRaises(ValueError):
            obj.prop = 20 * px
        obj.prop = 30 * percent
        with self.assertRaises(ValueError):
            obj.prop = 'a'
        with self.assertRaises(ValueError):
            obj.prop = 'b'
        with self.assertRaises(ValueError):
            obj.prop = None

        # Check the error message
        try:
            obj.prop = 'invalid'
            self.fail('Should raise ValueError')
        except ValueError as v:
            self.assertEqual(str(v), "Invalid value 'invalid' for CSS property 'prop'; Valid values are: <percentage>")

    def test_allow_integer(self):
        class MyObject:
            prop = validated_property('prop', choices=Choices(integer=True))

        obj = MyObject()

        obj.prop = 10
        with self.assertRaises(ValueError):
            obj.prop = 20 * px
        with self.assertRaises(ValueError):
            obj.prop = 30 * percent
        with self.assertRaises(ValueError):
            obj.prop = 'a'
        with self.assertRaises(ValueError):
            obj.prop = 'b'
        with self.assertRaises(ValueError):
            obj.prop = None

        # Check the error message
        try:
            obj.prop = 'invalid'
            self.fail('Should raise ValueError')
        except ValueError as v:
            self.assertEqual(str(v), "Invalid value 'invalid' for CSS property 'prop'; Valid values are: <integer>")

    def test_values(self):
        class MyObject:
            prop = validated_property('prop', choices=Choices('a', 'b', None))

        obj = MyObject()

        with self.assertRaises(ValueError):
            obj.prop = 10
        with self.assertRaises(ValueError):
            obj.prop = 20 * px
        with self.assertRaises(ValueError):
            obj.prop = 30 * percent
        obj.prop = 'a'
        obj.prop = 'b'
        obj.prop = None

        # Check the error message
        try:
            obj.prop = 'invalid'
            self.fail('Should raise ValueError')
        except ValueError as v:
            self.assertEqual(str(v), "Invalid value 'invalid' for CSS property 'prop'; Valid values are: a, b, none")

    def test_all_choices(self):
        class MyObject:
            prop = validated_property('prop', choices=Choices(
                'a', 'b', None, integer=True, length=True, percentage=True
            ))

        obj = MyObject()

        obj.prop = 10
        obj.prop = 20 * px
        obj.prop = 30 * percent
        obj.prop = 'a'
        obj.prop = 'b'

        # Check the error message
        try:
            obj.prop = 'invalid'
            self.fail('Should raise ValueError')
        except ValueError as v:
            self.assertEqual(str(v), "Invalid value 'invalid' for CSS property 'prop'; Valid values are: <integer>, <length>, <percentage>, a, b, none")


class CssDeclarationTests(TestCase):
    def test_engine(self):
        node = TestNode(CSS())
        self.assertEqual(node.style.engine(), css_engine)

    def test_auto_default_property(self):
        node = TestNode(CSS())
        node.layout.dirty = None

        # Default value is AUTO
        self.assertIs(node.style.width, AUTO)
        self.assertIsNone(node.style.dirty)

        # Modify the value
        node.style.width = 10

        self.assertEqual(node.style.width, 10)
        self.assertTrue(node.style.dirty)

        # Clean the layout
        node.layout.dirty = False

        # Set the value to the same value.
        # Dirty flag is not set.
        node.style.width = 10
        self.assertEqual(node.style.width, 10)
        self.assertFalse(node.style.dirty)

        # Set the value to something new
        # Dirty flag is set.
        node.style.width = 20
        self.assertEqual(node.style.width, 20)
        self.assertTrue(node.style.dirty)

        # Clean the layout
        node.layout.dirty = False

        # Clear the property
        del node.style.width
        self.assertIs(node.style.width, AUTO)
        self.assertTrue(node.style.dirty)

        # Clean the layout
        node.layout.dirty = False

        # Clear the property again.
        # The underlying attribute won't exist, so this
        # should be a no-op.
        del node.style.width
        self.assertIs(node.style.width, AUTO)
        self.assertFalse(node.style.dirty)

    def test_0_default_property(self):
        node = TestNode(CSS())
        node.layout.dirty = None

        # Default value is 0
        self.assertEqual(node.style.min_width, 0)
        self.assertIsNone(node.style.dirty)

        # Modify the value
        node.style.min_width = 10

        self.assertEqual(node.style.min_width, 10)
        self.assertTrue(node.style.dirty)

        # Clean the layout
        node.layout.dirty = False

        # Set the value to the same value.
        # Dirty flag is not set.
        node.style.min_width = 10
        self.assertEqual(node.style.min_width, 10)
        self.assertFalse(node.style.dirty)

        # Set the value to something new
        # Dirty flag is set.
        node.style.min_width = 20
        self.assertEqual(node.style.min_width, 20)
        self.assertTrue(node.style.dirty)

        # Clean the layout
        node.layout.dirty = False

        # Clear the property
        del node.style.min_width
        self.assertEqual(node.style.min_width, 0)
        self.assertTrue(node.style.dirty)

    def test_None_default_property(self):
        node = TestNode(CSS())
        node.layout.dirty = None

        # Default value is None
        self.assertIsNone(node.style.max_width)
        self.assertIsNone(node.style.dirty)

        # Modify the value
        node.style.max_width = 10

        self.assertEqual(node.style.max_width, 10)
        self.assertTrue(node.style.dirty)

        # Clean the layout
        node.layout.dirty = False

        # Set the value to the same value.
        # Dirty flag is not set.
        node.style.max_width = 10
        self.assertEqual(node.style.max_width, 10)
        self.assertFalse(node.style.dirty)

        # Set the value to something new
        # Dirty flag is set.
        node.style.max_width = 20
        self.assertEqual(node.style.max_width, 20)
        self.assertTrue(node.style.dirty)

        # Clean the layout
        node.layout.dirty = False

        # Clear the property
        del node.style.max_width
        self.assertIsNone(node.style.max_width)
        self.assertTrue(node.style.dirty)

    def test_property_with_choices(self):
        node = TestNode(CSS())
        node.layout.dirty = None

        # Default value is INLINE
        self.assertIs(node.style.display, INLINE)
        self.assertIsNone(node.style.dirty)

        # Try to provide a value that isn't on the choices list
        with self.assertRaises(ValueError):
            node.style.display = 10

        # Use a valid value
        node.style.display = BLOCK
        self.assertIs(node.style.display, BLOCK)
        self.assertTrue(node.style.dirty)

        # Clean the layout
        node.layout.dirty = False

        # Set the value to the same value.
        # Dirty flag is not set.
        node.style.display = BLOCK
        self.assertIs(node.style.display, BLOCK)
        self.assertFalse(node.style.dirty)

        # Set the value to something new
        # Dirty flag is set.
        node.style.display = TABLE
        self.assertIs(node.style.display, TABLE)
        self.assertTrue(node.style.dirty)

        # Clean the layout
        node.layout.dirty = False

        # Clear the property
        del node.style.display
        self.assertIs(node.style.display, INLINE)
        self.assertTrue(node.style.dirty)

    def test_directional_property(self):
        node = TestNode(CSS())
        node.layout.dirty = None

        # Default value is 0
        self.assertEqual(node.style.margin, (0, 0, 0, 0))
        self.assertEqual(node.style.margin_top, 0)
        self.assertEqual(node.style.margin_right, 0)
        self.assertEqual(node.style.margin_bottom, 0)
        self.assertEqual(node.style.margin_left, 0)
        self.assertIsNone(node.style.dirty)

        # Set a value in one axis
        node.style.margin_top = 10

        self.assertEqual(node.style.margin, (10, 0, 0, 0))
        self.assertEqual(node.style.margin_top, 10)
        self.assertEqual(node.style.margin_right, 0)
        self.assertEqual(node.style.margin_bottom, 0)
        self.assertEqual(node.style.margin_left, 0)
        self.assertTrue(node.style.dirty)

        # Clean the layout
        node.layout.dirty = False

        # Set a value directly with a single item
        node.style.margin = (10,)

        self.assertEqual(node.style.margin, (10, 10, 10, 10))
        self.assertEqual(node.style.margin_top, 10)
        self.assertEqual(node.style.margin_right, 10)
        self.assertEqual(node.style.margin_bottom, 10)
        self.assertEqual(node.style.margin_left, 10)
        self.assertTrue(node.style.dirty)

        # Clean the layout
        node.layout.dirty = False

        # Set a value directly with a single item
        node.style.margin = 30

        self.assertEqual(node.style.margin, (30, 30, 30, 30))
        self.assertEqual(node.style.margin_top, 30)
        self.assertEqual(node.style.margin_right, 30)
        self.assertEqual(node.style.margin_bottom, 30)
        self.assertEqual(node.style.margin_left, 30)
        self.assertTrue(node.style.dirty)

        # Clean the layout
        node.layout.dirty = False

        # Set a value directly with a 2 values
        node.style.margin = (10, 20)

        self.assertEqual(node.style.margin, (10, 20, 10, 20))
        self.assertEqual(node.style.margin_top, 10)
        self.assertEqual(node.style.margin_right, 20)
        self.assertEqual(node.style.margin_bottom, 10)
        self.assertEqual(node.style.margin_left, 20)
        self.assertTrue(node.style.dirty)

        # Clean the layout
        node.layout.dirty = False

        # Set a value directly with a 3 values
        node.style.margin = (10, 20, 30)

        self.assertEqual(node.style.margin, (10, 20, 30, 20))
        self.assertEqual(node.style.margin_top, 10)
        self.assertEqual(node.style.margin_right, 20)
        self.assertEqual(node.style.margin_bottom, 30)
        self.assertEqual(node.style.margin_left, 20)
        self.assertTrue(node.style.dirty)

        # Clean the layout
        node.layout.dirty = False

        # Set a value directly with a 4 values
        node.style.margin = (10, 20, 30, 40)

        self.assertEqual(node.style.margin, (10, 20, 30, 40))
        self.assertEqual(node.style.margin_top, 10)
        self.assertEqual(node.style.margin_right, 20)
        self.assertEqual(node.style.margin_bottom, 30)
        self.assertEqual(node.style.margin_left, 40)
        self.assertTrue(node.style.dirty)

        # Set a value directly with an invalid number of values
        with self.assertRaises(ValueError):
            node.style.margin = ()

        with self.assertRaises(ValueError):
            node.style.margin = (10, 20, 30, 40, 50)

        # Clean the layout
        node.layout.dirty = False

        # Clear a value on one axis
        del node.style.margin_top

        self.assertEqual(node.style.margin, (0, 20, 30, 40))
        self.assertEqual(node.style.margin_top, 0)
        self.assertEqual(node.style.margin_right, 20)
        self.assertEqual(node.style.margin_bottom, 30)
        self.assertEqual(node.style.margin_left, 40)
        self.assertTrue(node.style.dirty)

        # Restore the top margin
        node.style.margin_top = 10

        # Clean the layout
        node.layout.dirty = False

        # Clear a value directly
        del node.style.margin

        self.assertEqual(node.style.margin, (0, 0, 0, 0))
        self.assertEqual(node.style.margin_top, 0)
        self.assertEqual(node.style.margin_right, 0)
        self.assertEqual(node.style.margin_bottom, 0)
        self.assertEqual(node.style.margin_left, 0)
        self.assertTrue(node.style.dirty)

    def test_set_multiple_properties(self):
        node = TestNode(CSS())
        node.layout.dirty = None

        node.style.set(width=10, height=20)

        self.assertEqual(node.style.width, 10)
        self.assertEqual(node.style.height, 20)
        self.assertIs(node.style.top, AUTO)
        self.assertTrue(node.style.dirty)

        # Clear properties
        node.style.set(width=None, top=30)

        self.assertIs(node.style.width, AUTO)
        self.assertEqual(node.style.height, 20)
        self.assertEqual(node.style.top, 30)
        self.assertTrue(node.style.dirty)

        # Clean the layout
        node.layout.dirty = False

        # Setting a non-property
        with self.assertRaises(NameError):
            node.style.set(not_a_property=10)

        self.assertFalse(node.style.dirty)

    def test_str(self):
        node = TestNode(CSS())
        node.layout.dirty = None

        node.style.set(
            width=10,
            height=20,
            margin=(30, 40, 50, 60),
            display=BLOCK
        )

        self.assertEqual(
            str(node.style),
            "display: block; height: 20px; "
            "margin-bottom: 50px; margin-left: 60px; "
            "margin-right: 40px; margin-top: 30px; width: 10px"
        )
