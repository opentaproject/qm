from unittest import TestCase
from .fockspace import FiniteBosonFockSpace;
from .qm import qm_compare, com
from sympy import expand;

class Test1_QM(TestCase):

    def test_intro(self):
        global_text = 'f = FiniteBosonFockSpace(\"a\"); a = f.B; ad = dagger(a); n = var(\"n\")  ; ket = f.ket; bra = f.bra; ';
        self.assertTrue(qm_compare("a ad ", "1 +   ad a ", global_text)['correct'])
        self.assertTrue(qm_compare("2 ad a + ad^2 a^2 ", "a ad^2 a", global_text)['correct'])
        self.assertTrue(qm_compare("bra(n) a ad^2 a ket(n)  ", "n*(n+1)", global_text)['correct'])

    def test_single_particle_boson_fock_space(self):
        global_text = "f = FiniteBosonFockSpace(\"a\"); \
            a = f.B; \
            ad = f.Bd;  \
            n = var(\"n\")  ; \
            ket = f.ket; \
            bra = f.bra; \
            omega =  var(\"omega\") ; \
            hbar =  var(\"hbar\"); \
            N = ad * a;  \
            H = hbar * omega * ( N + 1/2 ) ; "
        # N ket(n)
        self.assertTrue(qm_compare("N ket(n)  ", "n  ket(n)  ", global_text)['correct'])
        # N ad ket(n) 
        s1 = "sqrt( n+1)^3 ket(n+1)";
        s2 = "N * ad * ket(n)";
        self.assertTrue(qm_compare(s1,s2, global_text)['correct'])
        # N a ket(n) 
        s1 = "sqrt( n ) * ( n-1) *  ket(n-1)";
        s2 = "N * a * ket(n)";
        self.assertTrue(qm_compare(s1,s2, global_text)['correct'])
        # N^2 ket(n)
        s1 = "n^2 ket(n)";
        s2 = "N^2 ket(n)";
        self.assertTrue(qm_compare(s1,s2, global_text)['correct'])
        # H ket(n)
        s1 =" hbar omega ( n + 1/2 )   ket(n)";
        s2 = "H ket(n)";
        self.assertTrue(qm_compare(s1,s2, global_text)['correct'])
        # H a ket(n)
        s1 =" hbar omega ( n - 1/2 ) a   ket(n)";
        s2 = "H a ket(n)";
        self.assertTrue(qm_compare(s1,s2, global_text)['correct'])
        s1 =" hbar omega ( n - 1/2 ) sqrt(n)   ket(n-1)";
        s2 = "H a ket(n)";
        self.assertTrue(qm_compare(s1,s2, global_text)['correct'])

    def test_single_particle_boson_commutator(self):
        global_text = "f = FiniteBosonFockSpace(\"a\"); \
            hbar = var(\"hbar\"); \
            omega = var(\"omega\"); \
            a = f.B; \
            ad = dagger(a);  \
            n = var(\"n\")  ; \
            ket = f.ket; \
            bra = f.bra; \
            N  = ad * a ;  \
            H= hbar * omega * ( ad * a + 1/2 ); \
            "
        # N ad ket(n) 
        s1 = "( a * ad - ad * a ) "
        s2 = "( 1 )";
        self.assertTrue(qm_compare(s1,s2, global_text)['correct'])
        s1 = "com(a,N)"
        s2 = "a"
        self.assertTrue(qm_compare(s1,s2, global_text)['correct'])
        s1 = "com(ad,a^2)"
        s2 = " - 2 a "
        self.assertTrue(qm_compare(s1,s2, global_text)['correct'])
        s1 = "com(a,ad^3)";
        s2 = " 3 ad^2" ;
        self.assertTrue(qm_compare(s1,s2, global_text)['correct'])
        s1 = "com(a,ad^3)";
        s2 = " 3 ad^2 "
        self.assertTrue(qm_compare(s1,s2, global_text)['correct'])
        s1 = "com(H,ad)";
        s2 = "hbar omega ad " ;
        self.assertTrue(qm_compare(s1,s2, global_text)['correct'])

    def test_commutative_and_noncommutative_operators(self) : 
        # TEST NONCOMMUTATIVE SYMBOLS  DEFINED BY "op" ;
        # AND COMMUTATIVE SYMBOLS DEFINED BY "var";
        global_text = f"a = var(\"a\") ; b = var(\"b\") ;"
        self.assertTrue( qm_compare( "a b ", "b a ", global_text )['correct']);
        self.assertTrue( qm_compare( "com(a,b)", "0 ", global_text )['correct']);
        global_text = f"a = op(\"a\") ; b = op(\"b\")  ; c = op(\"c\") ;" 
        self.assertFalse( qm_compare( "a b ", "b a ", global_text )['correct']);
        self.assertFalse( qm_compare( "com(a,b)", "0 ", global_text )['correct']);
        # test jacobi identity
        self.assertTrue( qm_compare( "com(a,com(b,c)) + com(b,com(c,a)) + com(c,com(a,b))" , '0' , global_text)['correct']);
        self.assertFalse( qm_compare( "com(a,com(b,c)) + com(b,com(c,a)) - com(c,com(a,b))" , '0' , global_text)['correct']);










    #def test_always_fails(self):
    #    self.assertTrue(False)
