import unittest

from task1.solution import sum_two, strict


class TestStrict(unittest.TestCase):
    def test_correct_types(self):
        """Тест на правильные типы аргументов.
        """
        self.assertEqual(sum_two(1, 2), 3)

    def test_incorrect_first_argument(self):
        """Тест на некорректный тип первого аргумента.
        """
        with self.assertRaises(TypeError) as ctx:
            sum_two("1", 2)
        self.assertIn("Аргумент 'a' имеет тип str.", str(ctx.exception))

    def test_incorrect_second_argument(self):
        """Тест на некорректный тип второго аргумента.
        """
        with self.assertRaises(TypeError) as ctx:
            sum_two(1, 2.4)
        self.assertIn("Аргумент 'b' имеет тип float.", str(ctx.exception))

    def test_no_annotations(self):
        """Тест функции без аннотаций (декоратор не должен ломаться).
        """
        @strict
        def no_annotation_func(a, b):
            return a + b

        self.assertEqual(no_annotation_func(1, 2), 3)

        with self.assertRaises(TypeError) as ctx:
            sum_two(1, 2.4)
        self.assertIn("Аргумент 'b' имеет тип float.", str(ctx.exception))

    def test_partial_annotations(self):
        """Тест функции с частичными аннотациями 
        (не все параметры аннотированы).
        """
        @strict
        def partial_annotation_func(a: int, b):
            return a + b

        self.assertEqual(partial_annotation_func(1, 2), 3)
        self.assertEqual(partial_annotation_func(1, 2.4), 3.4)


if __name__ == "__main__":
    unittest.main()