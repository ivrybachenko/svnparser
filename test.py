import unittest
import status


class TestColumn(unittest.TestCase):

    def test_fit_to_width_1(self):
        col = status.Column(width=4, alignment='<')
        actual = col.fit_to_width('abcd')
        expected = 'abcd'
        self.assertEqual(expected, actual)

    def test_fit_to_width_2(self):
        col = status.Column(width=4, alignment='<')
        actual = col.fit_to_width('abc')
        expected = 'abc '
        self.assertEqual(expected, actual)

    def test_fit_to_width_3(self):
        col = status.Column(width=4, alignment='<')
        actual = col.fit_to_width('abc')
        expected = 'abc '
        self.assertEqual(expected, actual)

    def test_fit_to_width_4(self):
        col = status.Column(width=4, alignment='>')
        actual = col.fit_to_width('abc')
        expected = ' abc'
        self.assertEqual(expected, actual)

    def test_fit_to_width_5(self):
        col = status.Column(width=4, alignment='^')
        actual = col.fit_to_width('ab')
        expected = ' ab '
        self.assertEqual(expected, actual)


class TestStatusColumn(unittest.TestCase):
    col = status.StatusColumn()

    def test_build_1(self):
        actual = self.col.build_value(r' ML+SKC *    58416    48101 goncharov    _cntl\win32\altpubserv.vcproj')
        self.assertEqual(' ', actual)

    def test_build_2(self):
        actual = self.col.build_value(r'MML+SKC *    58416    48101 goncharov    _cntl\win32\altpubserv.vcproj')
        self.assertEqual('Modified', actual)

    def test_build_3(self):
        actual = self.col.build_value(r'DML+SKC *    58416    48101 goncharov    _cntl\win32\altpubserv.vcproj')
        self.assertEqual('Deleted', actual)

    def test_build_4(self):
        actual = self.col.build_value(r'AML+SKC *    58416    48101 goncharov    _cntl\win32\altpubserv.vcproj')
        self.assertEqual('Added', actual)

    def test_build_5(self):
        actual = self.col.build_value(r'RML+SKC *    58416    48101 goncharov    _cntl\win32\altpubserv.vcproj')
        self.assertEqual('Replaced', actual)

    def test_build_6(self):
        actual = self.col.build_value(r'CML+SKC *    58416    48101 goncharov    _cntl\win32\altpubserv.vcproj')
        self.assertEqual('Conflicts', actual)

    def test_build_7(self):
        actual = self.col.build_value(r'XML+SKC *    58416    48101 goncharov    _cntl\win32\altpubserv.vcproj')
        self.assertEqual('External', actual)

    def test_build_8(self):
        actual = self.col.build_value(r'I                                        svn.txt')
        self.assertEqual('Ignored', actual)

    def test_build_9(self):
        actual = self.col.build_value(r'?                                        svn.txt')
        self.assertEqual('Not controlled', actual)

    def test_build_10(self):
        actual = self.col.build_value(r'!                -    48101 goncharov    _cntl\win32\altpubserv.vcproj')
        self.assertEqual('Missed', actual)

    def test_build_11(self):
        actual = self.col.build_value(r'~ML+SKC *    58416    48101 goncharov    _cntl\win32\altpubserv.vcproj')
        self.assertEqual('Kind replaced', actual)

    def test_build_incorrect_1(self):
        with self.assertRaises(status.ParseException, msg='missed columns'):
            self.col.build_value('')

    def test_is_controlled_1(self):
        actual = self.col.is_controlled(r' ML+SKC *    58416    48101 goncharov    _cntl\win32\altpubserv.vcproj')
        self.assertEqual(True, actual)

    def test_is_controlled_2(self):
        actual = self.col.is_controlled(r'MML+SKC *    58416    48101 goncharov    _cntl\win32\altpubserv.vcproj')
        self.assertEqual(True, actual)

    def test_is_controlled_3(self):
        actual = self.col.is_controlled(r'DML+SKC *    58416    48101 goncharov    _cntl\win32\altpubserv.vcproj')
        self.assertEqual(True, actual)

    def test_is_controlled_4(self):
        actual = self.col.is_controlled(r'AML+SKC *    58416    48101 goncharov    _cntl\win32\altpubserv.vcproj')
        self.assertEqual(True, actual)

    def test_is_controlled_5(self):
        actual = self.col.is_controlled(r'RML+SKC *    58416    48101 goncharov    _cntl\win32\altpubserv.vcproj')
        self.assertEqual(True, actual)

    def test_is_controlled_6(self):
        actual = self.col.is_controlled(r'CML+SKC *    58416    48101 goncharov    _cntl\win32\altpubserv.vcproj')
        self.assertEqual(True, actual)

    def test_is_controlled_7(self):
        actual = self.col.is_controlled(r'XML+SKC *    58416    48101 goncharov    _cntl\win32\altpubserv.vcproj')
        self.assertEqual(True, actual)

    def test_is_controlled_8(self):
        actual = self.col.is_controlled(r'!                -    48101 goncharov    _cntl\win32\altpubserv.vcproj')
        self.assertEqual(True, actual)

    def test_is_controlled_9(self):
        actual = self.col.is_controlled(r'!ML+SKC *    58416    48101 goncharov    _cntl\win32\altpubserv.vcproj')
        self.assertEqual(True, actual)

    def test_is_controlled_10(self):
        actual = self.col.is_controlled(r'?                                        _cntl\win32\altpubserv.vcproj')
        self.assertEqual(False, actual)

    def test_is_controlled_11(self):
        actual = self.col.is_controlled(r'I                                        _cntl\win32\altpubserv.vcproj')
        self.assertEqual(False, actual)

    def test_is_controlled_incorrect_1(self):
        with self.assertRaises(status.ParseException, msg='missed columns'):
            self.col.is_controlled('')


class TestPropertiesColumn(unittest.TestCase):
    col = status.PropertiesColumn()

    def test_build_1(self):
        actual = self.col.build_value(r'A L+SKC *    58416    48101 goncharov    _cntl\win32\altpubserv.vcproj')
        self.assertEqual(' ', actual)

    def test_build_2(self):
        actual = self.col.build_value(r'AML+SKC *    58416    48101 goncharov    _cntl\win32\altpubserv.vcproj')
        self.assertEqual('Modified', actual)

    def test_build_3(self):
        actual = self.col.build_value(r'ACL+SKC *    58416    48101 goncharov    _cntl\win32\altpubserv.vcproj')
        self.assertEqual('Conflict', actual)

    def test_build_4(self):
        actual = self.col.build_value(r'?                                        svn.txt')
        self.assertEqual('', actual)

    def test_build_5(self):
        actual = self.col.build_value(r'I                                        svn.txt')
        self.assertEqual('', actual)

    def test_build_incorrect_1(self):
        with self.assertRaises(status.ParseException, msg='missed columns'):
            self.col.build_value('')


class TestIsLockedColumn(unittest.TestCase):
    col = status.IsLockedColumn()

    def test_build_1(self):
        actual = self.col.build_value(r'AM +SKC *    58416    48101 goncharov    _cntl\win32\altpubserv.vcproj')
        self.assertEqual(' ', actual)

    def test_build_2(self):
        actual = self.col.build_value(r'AML+SKC *    58416    48101 goncharov    _cntl\win32\altpubserv.vcproj')
        self.assertEqual('Locked', actual)

    def test_build_3(self):
        actual = self.col.build_value(r'?                                        svn.txt')
        self.assertEqual('', actual)

    def test_build_4(self):
        actual = self.col.build_value(r'I                                        svn.txt')
        self.assertEqual('', actual)

    def test_build_incorrect_1(self):
        with self.assertRaises(status.ParseException, msg='missed columns'):
            self.col.build_value('')


class TestAddWithHistColumn(unittest.TestCase):
    col = status.AddWithHistColumn()

    def test_build_1(self):
        actual = self.col.build_value(r'AML SKC *    58416    48101 goncharov    _cntl\win32\altpubserv.vcproj')
        self.assertEqual(' ', actual)

    def test_build_2(self):
        actual = self.col.build_value(r'AML+SKC *    58416    48101 goncharov    _cntl\win32\altpubserv.vcproj')
        self.assertEqual('+', actual)

    def test_build_3(self):
        actual = self.col.build_value(r'?                                        svn.txt')
        self.assertEqual('', actual)

    def test_build_4(self):
        actual = self.col.build_value(r'I                                        svn.txt')
        self.assertEqual('', actual)

    def test_build_incorrect_1(self):
        with self.assertRaises(status.ParseException, msg='missed columns'):
            self.col.build_value('')


class TestSwitchedToParentColumn(unittest.TestCase):
    col = status.SwitchedToParentColumn()

    def test_build_1(self):
        actual = self.col.build_value(r'AML+ KC *    58416    48101 goncharov    _cntl\win32\altpubserv.vcproj')
        self.assertEqual(' ', actual)

    def test_build_2(self):
        actual = self.col.build_value(r'AML+SKC *    58416    48101 goncharov    _cntl\win32\altpubserv.vcproj')
        self.assertEqual('Switched', actual)

    def test_build_3(self):
        actual = self.col.build_value(r'?                                        svn.txt')
        self.assertEqual('', actual)

    def test_build_4(self):
        actual = self.col.build_value(r'I                                        svn.txt')
        self.assertEqual('', actual)

    def test_build_incorrect_1(self):
        with self.assertRaises(status.ParseException, msg='missed columns'):
            self.col.build_value('')


class TestLockInfoColumn(unittest.TestCase):
    col = status.LockInfoColumn()

    def test_build_1(self):
        actual = self.col.build_value(r'AML+S C *    58416    48101 goncharov    _cntl\win32\altpubserv.vcproj')
        self.assertEqual(' ', actual)

    def test_build_2(self):
        actual = self.col.build_value(r'AML+SKC *    58416    48101 goncharov    _cntl\win32\altpubserv.vcproj')
        self.assertEqual('Token', actual)

    def test_build_3(self):
        actual = self.col.build_value(r'AML+SOC *    58416    48101 goncharov    _cntl\win32\altpubserv.vcproj')
        self.assertEqual('Other', actual)

    def test_build_4(self):
        actual = self.col.build_value(r'AML+STC *    58416    48101 goncharov    _cntl\win32\altpubserv.vcproj')
        self.assertEqual('Stolen', actual)

    def test_build_5(self):
        actual = self.col.build_value(r'AML+SBC *    58416    48101 goncharov    _cntl\win32\altpubserv.vcproj')
        self.assertEqual('Broken', actual)

    def test_build_6(self):
        actual = self.col.build_value(r'?                                        svn.txt')
        self.assertEqual('', actual)

    def test_build_7(self):
        actual = self.col.build_value(r'I                                        svn.txt')
        self.assertEqual('', actual)

    def test_build_incorrect_1(self):
        with self.assertRaises(status.ParseException, msg='missed columns'):
            self.col.build_value('')


class TestConflictColumn(unittest.TestCase):
    col = status.ConflictColumn()

    def test_build_1(self):
        actual = self.col.build_value(r'AML+SK  *    58416    48101 goncharov    _cntl\win32\altpubserv.vcproj')
        self.assertEqual(' ', actual)

    def test_build_2(self):
        actual = self.col.build_value(r'AML+SKC *    58416    48101 goncharov    _cntl\win32\altpubserv.vcproj')
        self.assertEqual('Conflict', actual)

    def test_build_3(self):
        actual = self.col.build_value(r'?                                        svn.txt')
        self.assertEqual('', actual)

    def test_build_4(self):
        actual = self.col.build_value(r'I                                        svn.txt')
        self.assertEqual('', actual)

    def test_build_incorrect_1(self):
        with self.assertRaises(status.ParseException, msg='missed columns'):
            self.col.build_value('')

    def test_is_conflict_description_1(self):
        actual = self.col.is_conflict_description(r'      >  Conflict dscription')
        self.assertEqual(True, actual)

    def test_is_conflict_description_2(self):
        actual = self.col.is_conflict_description(
            r'AML+SKC *    58416    48101 goncharov    _cntl\win32\altpubserv.vcproj')
        self.assertEqual(False, actual)

    def test_is_conflict_description_incorrect_1(self):
        with self.assertRaises(status.ParseException, msg='missed columns'):
            self.col.is_conflict_description('')


class TestOutOfDateColumn(unittest.TestCase):
    col = status.OutOfDateColumn()

    def test_build_1(self):
        actual = self.col.build_value(r'AML+SKC      58416    48101 goncharov    _cntl\win32\altpubserv.vcproj')
        self.assertEqual(' ', actual)

    def test_build_2(self):
        actual = self.col.build_value(r'AML+SKC *    58416    48101 goncharov    _cntl\win32\altpubserv.vcproj')
        self.assertEqual('Out of date', actual)

    def test_build_3(self):
        actual = self.col.build_value(r'?                                        svn.txt')
        self.assertEqual('', actual)

    def test_build_4(self):
        actual = self.col.build_value(r'I                                        svn.txt')
        self.assertEqual('', actual)

    def test_build_incorrect_1(self):
        with self.assertRaises(status.ParseException, msg='missed columns'):
            self.col.build_value('')


class TestWorkingRevisionColumn(unittest.TestCase):
    col = status.WorkingRevisionColumn()

    def test_build_1(self):
        actual = self.col.build_value(r'AML+SKC *    58416    48101 goncharov    _cntl\win32\altpubserv.vcproj')
        self.assertEqual('58416', actual)

    def test_build_2(self):
        actual = self.col.build_value(r'AML+SKC *    38412    48101 goncharov    _cntl\win32\altpubserv.vcproj')
        self.assertEqual('38412', actual)

    def test_build_3(self):
        actual = self.col.build_value(r'AML+SKC *    -    48101 goncharov    _cntl\win32\altpubserv.vcproj')
        self.assertEqual('-', actual)

    def test_build_4(self):
        actual = self.col.build_value(r'?                                        svn.txt')
        self.assertEqual('', actual)

    def test_build_5(self):
        actual = self.col.build_value(r'I                                        svn.txt')
        self.assertEqual('', actual)

    def test_build_incorrect_1(self):
        with self.assertRaises(status.ParseException, msg='missed columns'):
            self.col.build_value('')


class TestCommittedRevisionColumn(unittest.TestCase):
    col = status.CommittedRevisionColumn()

    def test_build_1(self):
        actual = self.col.build_value(r'AML+SKC *    58416    48101 goncharov    _cntl\win32\altpubserv.vcproj')
        self.assertEqual('48101', actual)

    def test_build_2(self):
        actual = self.col.build_value(r'AML+SKC *    38412    42141 goncharov    _cntl\win32\altpubserv.vcproj')
        self.assertEqual('42141', actual)

    def test_build_3(self):
        actual = self.col.build_value(r'?                                        svn.txt')
        self.assertEqual('', actual)

    def test_build_4(self):
        actual = self.col.build_value(r'I                                        svn.txt')
        self.assertEqual('', actual)

    def test_build_incorrect_1(self):
        with self.assertRaises(status.ParseException, msg='missed columns'):
            self.col.build_value('')


class TestCommittedAuthorColumn(unittest.TestCase):
    col = status.CommittedAuthorColumn()

    def test_build_1(self):
        actual = self.col.build_value(r'AML+SKC *    58416    48101 goncharov    _cntl\win32\altpubserv.vcproj')
        self.assertEqual('goncharov', actual)

    def test_build_2(self):
        actual = self.col.build_value(r'AML+SKC *    58416    48101 ivanov    _cntl\win32\altpubserv.vcproj')
        self.assertEqual('ivanov', actual)

    def test_build_incorrect_1(self):
        with self.assertRaises(status.ParseException, msg='missed columns'):
            self.col.build_value('')


class TestWorkingCopyPathColumn(unittest.TestCase):
    col = status.WorkingCopyPathColumn()

    def test_build_1(self):
        actual = self.col.build_value(r'AML+SKC *    58416    48101 goncharov    _cntl\win32\altpubserv.vcproj')
        self.assertEqual(r'_cntl\win32\altpubserv.vcproj', actual)

    def test_build_2(self):
        actual = self.col.build_value(r'?                                        svn.txt')
        self.assertEqual('svn.txt', actual)

    def test_build_3(self):
        actual = self.col.build_value(r'I                                        svn.txt')
        self.assertEqual('svn.txt', actual)

    def test_build_incorrect_1(self):
        with self.assertRaises(status.ParseException, msg='missed columns'):
            self.col.build_value('')

    def test_build_incorrect_2(self):
        with self.assertRaises(status.ParseException, msg='missed columns'):
            self.col.build_value(r'AML+SKC *    58416    48101 goncharov    ')


class TestTable(unittest.TestCase):

    def create_frull_table(self):
        columns = [
            status.StatusColumn(),
            status.PropertiesColumn(),
            status.IsLockedColumn(),
            status.AddWithHistColumn(),
            status.SwitchedToParentColumn(),
            status.LockInfoColumn(),
            status.ConflictColumn(),
            status.OutOfDateColumn(),
            status.WorkingRevisionColumn(),
            status.CommittedRevisionColumn(),
            status.CommittedAuthorColumn(),
            status.WorkingCopyPathColumn()
        ]
        table = status.Table(columns)
        return table

    def test_header_1(self):
        table = status.Table([status.Column(title='col1', alignment='<', width=4),
                              status.Column(title='col2', alignment='<', width=4)],
                             column_separator='|', left_separator='', right_separator='')
        actual = table.build_header()
        expected = 'col1|col2'
        self.assertEqual(expected, actual)

    def test_header_2(self):
        table = status.Table([status.Column(title='col1', alignment='<', width=6),
                              status.Column(title='col2', alignment='<', width=6)],
                             column_separator='|', left_separator='', right_separator='')
        actual = table.build_header()
        expected = 'col1  |col2  '
        self.assertEqual(expected, actual)

    def test_header_3(self):
        table = status.Table([status.Column(title='col1'), status.Column(title='col2')],
                             column_separator='|', left_separator='|', right_separator='|')
        actual = table.build_header()
        expected = '|col1|col2|'
        self.assertEqual(expected, actual)

    def test_header_4(self):
        table = status.Table([status.Column(title='col1', alignment='<', width=-1),
                              status.Column(title='col2', alignment='<', width=2)],
                             column_separator='|', left_separator='|', right_separator='|')
        actual = table.build_header()
        expected = '|col1|co|\n|    |l2|'
        self.assertEqual(expected, actual)

    def test_row_1(self):
        line = r'AML+SKC *    58416    48101 goncharov    _cntl\win32\altpubserv.vcproj'
        table = status.Table([status.WorkingRevisionColumn(title='col1', alignment='<', width=4),
                              status.CommittedRevisionColumn(title='col2', alignment='<', width=4)],
                             column_separator='|', left_separator='|', right_separator='|')
        actual = table.build_row(line)
        expected = '|5841|4810|\n|6   |1   |'
        self.assertEqual(expected, actual)

    def test_row_2(self):
        line = r'AML+SKC *    58416    48101 goncharov    _cntl\win32\altpubserv.vcproj'
        table = status.Table([status.WorkingRevisionColumn(title='col1', alignment='>', width=4),
                              status.CommittedRevisionColumn(title='col2', alignment='>', width=4)],
                             column_separator='|', left_separator='', right_separator='')
        actual = table.build_row(line)
        expected = '5841|4810\n   6|   1'
        self.assertEqual(expected, actual)

    def test_row_3(self):
        line = r'AML+SKC *    58416    48101 goncharov    _cntl\win32\altpubserv.vcproj'
        table = status.Table([status.WorkingRevisionColumn(title='col1', alignment='^', width=6),
                              status.CommittedRevisionColumn(title='col2', alignment='^', width=6)],
                             column_separator='|', left_separator='', right_separator='')
        actual = table.build_row(line)
        expected = '58416 |48101 '
        self.assertEqual(expected, actual)

    def test_row_4(self):
        line = r'AML+SKC *    58416    48101 goncharov    _cntl\win32\altpubserv.vcproj'
        table = status.Table([status.WorkingRevisionColumn(title='col1', alignment='^', width=7),
                              status.CommittedRevisionColumn(title='col2', alignment='^', width=7)],
                             column_separator='|', left_separator='', right_separator='')
        actual = table.build_row(line)
        expected = ' 58416 | 48101 '
        self.assertEqual(expected, actual)

    def test_head_sep(self):
        table = status.Table([status.WorkingRevisionColumn(title='col1', alignment='^', width=7),
                              status.CommittedRevisionColumn(title='col2', alignment='^', width=7)],
                             header_separator='=', column_separator='', left_separator='', right_separator='')
        actual = table.build_header_separator()
        expected = '=' * 14
        self.assertEqual(expected, actual)

    def test_row_sep(self):
        table = status.Table([status.WorkingRevisionColumn(title='col1', alignment='^', width=7),
                              status.CommittedRevisionColumn(title='col2', alignment='^', width=7)],
                             row_separator='=', column_separator='', left_separator='', right_separator='')
        actual = table.build_row_separator()
        expected = '=' * 14
        self.assertEqual(expected, actual)

    def test_incorrect_1(self):
        table = self.create_frull_table()
        line = r'AML+SKC *    58416    48101    _cntl\win32\altpubserv.vcproj'
        with self.assertRaises(status.ParseException, msg='missed commited author'):
            table.build_row(line)

    def test_incorrect_2(self):
        table = self.create_frull_table()
        line = r'AML+SKC *    58416    48101 goncharov    '
        with self.assertRaises(status.ParseException, msg='missed WorkingCopyPathColumn'):
            table.build_row(line)

    def test_incorrect_3(self):
        table = self.create_frull_table()
        line = r'AML+SKC '
        with self.assertRaises(status.ParseException, msg='missed columns'):
            table.build_row(line)

    def test_incorrect_4(self):
        table = self.create_frull_table()
        line = r''
        with self.assertRaises(status.ParseException, msg='missed columns'):
            table.build_row(line)


if __name__ == '__main__':
    unittest.main()
