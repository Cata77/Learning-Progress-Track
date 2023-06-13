import unittest
import task


class TestTask(unittest.TestCase):
    def test_name(self):
        self.assertEqual(task.check_name('Jean-Claude'), True)
        self.assertEqual(task.check_name("O'Neill"), True)
        self.assertEqual(task.check_name("StanisławOğuz"), False)
        self.assertEqual(task.check_name('Robert Jemison Van de Graaff'), True)
        self.assertEqual(task.check_name('John Ronald Reuel Tolkien'), True)
        self.assertEqual(task.check_name('D'), False)
        self.assertEqual(task.check_name('D.'), False)
        self.assertEqual(task.check_name("O'Neill'"), False)
        self.assertEqual(task.check_name("'O'Neill"), False)
        self.assertEqual(task.check_name("'O'Neill'"), False)
        self.assertEqual(task.check_name("-O'Neill"), False)
        self.assertEqual(task.check_name("O'Neill-"), False)
        self.assertEqual(task.check_name("-O'Neill-"), False)
        self.assertEqual(task.check_name("-'O'Neill-'"), False)

    def test_email(self):
        self.assertEqual(task.check_email('jdoe@mail.net'), True)
        self.assertEqual(task.check_email('jdoemail.net'), False)
        self.assertEqual(task.check_email('jdoemailnet'), False)
        self.assertEqual(task.check_email('jdoe@mailnet'), False)
        self.assertEqual(task.check_email('@mailnet'), False)
        self.assertEqual(task.check_email('@mail.net'), False)

    def test_check_points_format(self):
        self.assertEqual(task.check_points_format(['1', '2', '3', '4']), True)
        self.assertEqual(task.check_points_format(['1', '2', '3']), False)
        self.assertEqual(task.check_points_format(['?', '2', '3', '4']), False)
        self.assertEqual(task.check_points_format(['-1', '2', '3', '4']), False)
