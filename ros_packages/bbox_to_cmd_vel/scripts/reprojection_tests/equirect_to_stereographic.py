import cv2
import math
import numpy as np
import numpy.matlib as nplib

def d1(x,y):
    return np.sqrt(np.add(np.multiply(x,x),np.multiply(y,y)))

def d2(r):
    return 2*math.atan2(r,2*1)

def asin_elt(a):
    return math.asin(a)

def atan_elt(a,b):
    return math.atan2(a,b)

def compute_phi(x, y, phi_1, R):
    rho = d1(x,y)
    c = np.asarray(map(d2,rho.flatten()))
    c = np.reshape(c,(x.shape[0], x.shape[1]))
    mult = np.cos(c)*np.sin(phi_1)+y*np.sin(c)*np.cos(phi_1)/rho
    phi = np.asarray(map(asin_elt, mult.flatten()))
    phi = np.reshape(phi,(x.shape[0], x.shape[1]))
    return phi

def compute_lambda(x,y,phi_1,lambda_0, R):
    rho = d1(x,y)
    c = np.asarray(map(d2,rho.flatten()))
    c = np.reshape(c,(x.shape[0], x.shape[1]))

    num = np.multiply(x,np.sin(c))
    denum = np.multiply(np.multiply(rho,np.cos(phi_1)),np.cos(c))-np.multiply(np.multiply(y,np.sin(phi_1)),np.sin(c))

    lambd = lambda_0 + np.asarray(map(atan_elt, num.flatten(), denum.flatten()))
    lambd = np.reshape(lambd,(x.shape[0], x.shape[1]))
    return lambd

def build_map(im):
    h, w, _ = im.shape
    x, y = np.meshgrid(range(-w/2,w/2),range(-w/2,w/2))
    rads = 2*math.pi/w

    R = 1
    phi = compute_phi(x,y,0,R).astype('float32')
    lbda = compute_lambda(x,y,0,0,R).astype('float32')
    print phi, lbda
    return phi/rads, lbda/rads

if __name__ == '__main__':

    im = cv2.imread('equirect.jpg')

    phi, lbda = build_map(im)
    print phi, lbda
    im = cv2.remap(im, phi, lbda, cv2.INTER_CUBIC)
    cv2.imshow('Equirectangular image', im)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
