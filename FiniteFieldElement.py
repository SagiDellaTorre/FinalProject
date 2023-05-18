import galois
import numpy as np

class FiniteFieldElement:

    # constructor
    def __init__(self, l, a):
        """
        l : FiniteField 
        a : array of polynomial coefficients
        """

        if max(a) >= l.p or min(a) < 0:
            raise Exception(f"a must be element in the prime field p={l.p}")

        self.l = l
        self.a_poly = galois.Poly(a[::-1], field=self.l.GFP)
        self.a_coeff = a
        self.n_coeff = len(a)
        self.n_poly = self.n_coeff - 1

        if not self.n_poly == self.l.n_poly_fx - 1:
            raise Exception("The degree of the polynomial illegal in the corresponding field extension l") 

        self.a_mat = self.mat_represent()

    def __str__(self):
        """
        return instance as polynomials
        """
        return f"{self.a_poly}"

    def get_matrix(self):
        """
        return instance as matrix
        """
        return f"{self.a_mat}"

    def get_vector(self):
        """
        return instance as vector: for a_n*x^n+...+a_1*x+a_0 -> [a_0, a_1, ...]
        """
        return f"{self.a_coeff}"

    def mat_represent(self):
        """
        this method calculate the matrix representation of an instance
        """

        mat = self.l.GFP(np.zeros((self.n_coeff,self.n_coeff), dtype=int))
        for i in range(self.n_coeff):
            mat = mat + self.a_poly.coeffs[-i-1]*self.l.basis[i]

        return mat
    
    def mat_to_poly(self, a_mat): #TODO continue

        """
        this method translate from matrix representation to vector representation
        """
        pass
 
    # adding two objects  
    def __add__(self, other):

        return self.a_poly + other.a_poly
    
    # substract two objects  
    def __sub__(self, other):

        return self.a_poly - other.a_poly
    
    # multiply two objects 
    def __mul__(self, other):

        return (self.a_poly * other.a_poly) % self.l.fx_poly # multiply poly, and then modulo fx
    
    # adding two objects  
    def __truediv__(self, other):

        if all(num == 0 for num in other.a_coeff):
            raise Exception("Divide by zero is not allowed") 

        #option 1: 
        return (self.a_mat // other.a_poly) % self.l.fx_poly
    
        #option 2:
        c_mat = self.a_mat @ np.linalg.inv(other.a_mat)
        return self.mat_to_poly(c_mat)