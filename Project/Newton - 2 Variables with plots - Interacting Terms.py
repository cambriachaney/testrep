import numpy as np
import math
import sympy as sym
from numpy.linalg import inv 
from numpy.linalg import norm
import matplotlib.pyplot as plt

def driver():

    x0 = [10,10]
    variables = ['a', 'b']
    Nmax = 100
    tol = 10**(-6)
    [xstar, ier, it, xvec, yvec, zvec] = NewtonDescent(x0, tol, Nmax, variables)

    gval = evalF(xstar)

    print("The optimal x_vector from this method is:", xstar)
    print("The optimal function value from this method is:", gval)
    print("The number of iterations this method took is:", it)

    # plotting the 3D function
    
    ax = plt.axes(projection = "3d")
    
    ax.scatter3D(xvec, yvec, zvec, c = zvec, cmap = 'rainbow_r')
    
    x = np.linspace(-100,100,100)
    y = np.linspace(-100,100,100)
    X,Y = np.meshgrid(x,y)
    Z = function(X,Y)
    ax.plot_surface(X,Y,Z, alpha = 0.5,rstride =1, cstride =1, cmap = 'viridis', edgecolor = 'none')
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')
    
    plt.show()

def function(x,y):
    return -112.593 + 6.666219*x - 0.03746*x**2 + 5.396958*y - 0.08621*y**2 -0.09402*x*y

def eval_hessian(x, variables):

    M = len(variables)

    a = sym.Symbol('a')
    b = sym.Symbol('b')

    #### MUST CHANGE FUNCTION HERE TOO!!!!!
    
    function = -112.593 + 6.666219*a - 0.03746*a**2 + 5.396958*b - 0.08621*b**2 -0.09402*a*b
    
    matrix = np.zeros([M,M])

    for i in range(M): #rows
        for j in range(M): #variables
            first = sym.diff(function,variables[j])
            #print(first)
            second = sym.diff(first,variables[i])
            #print(second)
            evaluate = second.subs({a:x[0], b:x[1]})
            matrix[i][j] = evaluate    

    return matrix

def evalF(x):

    F = -112.593 + 6.666219*x[0] - 0.03746*x[0]**2 + 5.396958*x[1] - 0.08621*x[1]**2 -0.09402*x[0]*x[1]
    return F

def eval_grad(x):
    F = evalF(x)
    grad = np.array([6.666219 - 2*0.03746*x[0]-0.09403*x[1],5.396958 - 2*0.08621*x[1]-0.09402*x[0]])
    return grad

def NewtonDescent(x0,tol,Nmax, variables):

    hessian = eval_hessian(x0, variables)
    hessian_inv = inv(hessian)
    gradient = eval_grad(x0)
    p = hessian_inv.dot(gradient)
    x1 = x0 - p

    it = 1

    x_vec = [x0[0],x1[0]] # for plotting
    y_vec = [x0[1],x1[1]]  # for plotting
    z_vec = [function(x0[0], x0[1]),function(x1[0], x1[1])]
    
    while norm(x1 - x0)>tol:

        x0 = x1
        hessian = eval_hessian(x0, variables)
        hessian_inv = inv(hessian)
        gradient = eval_grad(x0)
        p = hessian_inv.dot(gradient)
        x1 = x0 - p
        it = it + 1

        x_vec.append(x1[0])
        y_vec.append(x1[1])
        z_vec.append(function(x1[0], x1[1]))

        if it >= Nmax:
            xstar = x1
            ier = 1
            print("The Max Number of Iterations was Met")
            return [xstar, ier, it, x_vec, y_vec, z_vec]

    xstar = x1
    ier = 0

    print(x_vec)
    return [xstar, ier, it, x_vec, y_vec, z_vec]

driver()
