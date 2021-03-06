import unittest
import random

from datastore.core.key import Key


def random_string():
    string = ''
    length = random.randint(5, 50)
    for i in range(0, length):
        string += chr(random.randint(ord('0'), ord('Z')))
    return string


def random_key():
    return Key('/herp/' + random_string() + '/derp')


class KeyTests(unittest.TestCase):

    def __subtest_basic(self, string):
        fixed_string = Key.remove_duplicate_slashes(string)
        last_namespace = fixed_string.rsplit('/')[-1].split(':')
        k_type = last_namespace[0] if len(last_namespace) > 1 else ''
        name = last_namespace[-1]
        path = fixed_string.rsplit('/', 1)[0] + '/' + k_type
        instance = fixed_string + ':' + 'c'

        self.assertEqual(Key(string)._string, fixed_string)
        self.assertEqual(Key(string), Key(string))
        self.assertEqual(str(Key(string)), fixed_string)
        self.assertEqual(repr(Key(string)), "Key('%s')" % fixed_string)
        self.assertEqual(Key(string).name, name)
        self.assertEqual(Key(string).type, k_type)
        self.assertEqual(Key(string).instance('c'), Key(instance))
        self.assertEqual(Key(string).path, Key(path))
        self.assertEqual(Key(string), eval(repr(Key(string))))

        self.assertTrue(Key(string).child('a') > Key(string))
        self.assertTrue(Key(string).child('a') < Key(string).child('b'))
        self.assertTrue(Key(string) == Key(string))

        split_string = fixed_string.split('/')
        if len(split_string) > 1:
            self.assertEqual(Key('/'.join(split_string[:-1])), Key(string).parent)
        else:
            self.assertRaises(ValueError, lambda: Key(string).parent)

        namespace = split_string[-1].split(':')
        if len(namespace) > 1:
            self.assertEqual(namespace[0], Key(string).type)
        else:
            self.assertEqual('', Key(string).type)

    def test_basic(self):
        self.__subtest_basic('')
        self.__subtest_basic('abcde')
        self.__subtest_basic('disahfidsalfhduisaufidsail')
        self.__subtest_basic('/fdisahfodisa/fdsa/fdsafdsafdsafdsa/fdsafdsa/')
        self.__subtest_basic(u'4215432143214321432143214321')
        self.__subtest_basic('/fdisaha////fdsa////fdsafdsafdsafdsa/fdsafdsa/')
        self.__subtest_basic('abcde:fdsfd')
        self.__subtest_basic('disahfidsalfhduisaufidsail:fdsa')
        self.__subtest_basic('/fdisahfodisa/fdsa/fdsafdsafdsafdsa/fdsafdsa/:')
        self.__subtest_basic(u'4215432143214321432143214321:')
        self.__subtest_basic('/fdisaha////fdsa////fdsafdsafdsafdsa/fdsafdsa/f:fdaf')

    def test_ancestry(self):
        k1 = Key('/A/B/C')
        k2 = Key('/A/B/C/D')

        self.assertEqual(k1._string, '/A/B/C')
        self.assertEqual(k2._string, '/A/B/C/D')
        self.assertTrue(k1.is_ancestor_of(k2))
        self.assertTrue(k2.is_descendant_of(k1))
        self.assertTrue(Key('/A').is_ancestor_of(k2))
        self.assertTrue(Key('/A').is_ancestor_of(k1))
        self.assertFalse(Key('/A').is_descendant_of(k2))
        self.assertFalse(Key('/A').is_descendant_of(k1))
        self.assertTrue(k2.is_descendant_of(Key('/A')))
        self.assertTrue(k1.is_descendant_of(Key('/A')))
        self.assertFalse(k2.is_ancestor_of(Key('/A')))
        self.assertFalse(k1.is_ancestor_of(Key('/A')))
        self.assertFalse(k2.is_ancestor_of(k2))
        self.assertFalse(k1.is_ancestor_of(k1))
        self.assertEqual(k1.child('D'), k2)
        self.assertEqual(k1, k2.parent)
        self.assertEqual(k1.path, k2.parent.path)

    def test_type(self):
        k1 = Key('/A/B/C:c')
        k2 = Key('/A/B/C:c/D:d')

        self.assertRaises(TypeError, k1.is_ancestor_of, str(k2))
        self.assertTrue(k1.is_ancestor_of(k2))
        self.assertTrue(k2.is_descendant_of(k1))
        self.assertEqual(k1.type, 'C')
        self.assertEqual(k2.type, 'D')
        self.assertEqual(k1.type, k2.parent.type)

    def test_hashing(self):
        keys = {}

        for i in range(0, 200):
            key = random_key()
            while key in keys.values():
                key = random_key()

            hstr = str(hash(key))
            self.assertFalse(hstr in keys)
            keys[hstr] = key

        for key in keys.values():
            hstr = str(hash(key))
            self.assertTrue(hstr in keys)
            self.assertEqual(key, keys[hstr])

    # do we need this?
    # def test_random(self):
    #     keys = set()
    #     for i in range(0, 1000):
    #         rand = random_key()
    #         self.assertFalse(rand in keys)
    #         keys.add(rand)
    #     self.assertEqual(len(keys), 1000)


if __name__ == '__main__':
    unittest.main()
