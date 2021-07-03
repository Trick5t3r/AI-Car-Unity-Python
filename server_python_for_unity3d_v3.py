# -*- coding: utf-8 -*-
"""
network.py
~~~~~~~~~~

A module to implement the stochastic gradient descent learning
algorithm for a feedforward neural network.  Gradients are calculated
using backpropagation.  Note that I have focused on making the code
simple, easily readable, and easily modifiable.  It is not optimized,
and omits many desirable features.
"""

#### Libraries
# Standard library
import random

# Third-party libraries
import numpy as np
from tempfile import TemporaryFile

class Network(object):

    def __init__(self, sizes):
        """The list ``sizes`` contains the number of neurons in the
        respective layers of the network.  For example, if the list
        was [2, 3, 1] then it would be a three-layer network, with the
        first layer containing 2 neurons, the second layer 3 neurons,
        and the third layer 1 neuron.  The biases and weights for the
        network are initialized randomly, using a Gaussian
        distribution with mean 0, and variance 1.  Note that the first
        layer is assumed to be an input layer, and by convention we
        won't set any biases for those neurons, since biases are only
        ever used in computing the outputs from later layers."""
        self.num_layers = len(sizes)
        self.sizes = sizes
        self.biases = [np.random.randn(y, 1) for y in sizes[1:]]
        self.weights = [np.random.randn(y, x)
                        for x, y in zip(sizes[:-1], sizes[1:])]
    
    def load_precedent_net(self):
        try:
            self.biases = np.load("net_save_biases.npy")
            self.weights = np.load("net_save_weights.npy")
            print("Loaded Successfully")
        except Exception as e:
            print(e)
    
    def save_the_net(self, what_of_net="all"):
        try:
            if what_of_net == "all":
                np.save("net_save_biases.npy", self.biases)
                np.save("net_save_weights.npy", self.weights)
            elif what_of_net == "biases":
                np.save("net_save_biases.npy", self.biases)
            elif what_of_net == "weights":
                np.save("net_save_weights.npy", self.weights)
            print("Saved Successfully")
        except Exception as e:
            print(e)
    
    def normalize_input_for_SGD(self, list_number=[]):
        """Get number and normalize it as an input of net"""
        current_array = np.array([np.float32(list_number[0])])
        #del(list_number[0])
        for x in list_number[1:]:
            current_array = np.vstack((current_array, np.array([np.float32(x)])))#np.float32(x)
        return current_array
    
    def normalize_output_for_SGD(self, list_number=[]):
        """Get number and normalize it as an output of net"""
        current_array = np.array([np.array([float(list_number[0])])])
        for x in list_number[1:]:
            current_array = np.vstack((current_array, np.array([float(x)])))#np.float32(x)
        return current_array
    
    def get_prediction(self, list_number=[]):
        """Get number and send it to feedfoward"""
        current_array = np.array([np.float32(list_number[0])])
        #del(list_number[0])
        for x in list_number[1:]:
            current_array = np.vstack((current_array, np.array([np.float32(x)])))#np.float32(x)
        return self.feedforward(current_array)
    
    def get_prediction_save(self, v, c,list_number=[]):
        """Get number and send it to feedfoward"""
        return self.feedforward(np.array([np.array([np.float32(c)]),np.array([np.float32(v)]),np.array([np.float32(1)]),np.array([np.float32(1)]),np.array([np.float32(1)]),np.array([np.float32(1)]),np.array([np.float32(1)]),np.array([np.float32(1)])]))

    def feedforward(self, a):
        """Return the output of the network if ``a`` is input."""
        for b, w in zip(self.biases, self.weights):
            a = sigmoid(np.dot(w, a)+b)
        return a

    def SGD(self, training_data, epochs, mini_batch_size, eta, test_data=None):
        """Train the neural network using mini-batch stochastic
        gradient descent.  The ``training_data`` is a list of tuples
        ``(x, y)`` representing the training inputs and the desired
        outputs.  The other non-optional parameters are
        self-explanatory.  If ``test_data`` is provided then the
        network will be evaluated against the test data after each
        epoch, and partial progress printed out.  This is useful for
        tracking progress, but slows things down substantially."""
        if test_data: n_test = len(test_data)
        n = len(training_data)
        for j in range(epochs):
            random.shuffle(training_data)
            mini_batches = [
                training_data[k:k+mini_batch_size]
                for k in range(0, n, mini_batch_size)]
            for mini_batch in mini_batches:
                self.update_mini_batch(mini_batch, eta)
            if test_data:
                print(("Epoch {0}: {1} / {2}".format(
                    j, self.evaluate(test_data), n_test)))
            else:
                print(("Epoch {0} complete".format(j)))

    def update_mini_batch(self, mini_batch, eta):
        """Update the network's weights and biases by applying
        gradient descent using backpropagation to a single mini batch.
        The ``mini_batch`` is a list of tuples ``(x, y)``, and ``eta``
        is the learning rate."""
        nabla_b = [np.zeros(b.shape) for b in self.biases]
        nabla_w = [np.zeros(w.shape) for w in self.weights]
        for x, y in mini_batch:
            delta_nabla_b, delta_nabla_w = self.backprop(x, y)
            nabla_b = [nb+dnb for nb, dnb in zip(nabla_b, delta_nabla_b)]
            nabla_w = [nw+dnw for nw, dnw in zip(nabla_w, delta_nabla_w)]
        self.weights = [w-(eta/len(mini_batch))*nw
                        for w, nw in zip(self.weights, nabla_w)]
        self.biases = [b-(eta/len(mini_batch))*nb
                       for b, nb in zip(self.biases, nabla_b)]

    def backprop(self, x, y):
        """Return a tuple ``(nabla_b, nabla_w)`` representing the
        gradient for the cost function C_x.  ``nabla_b`` and
        ``nabla_w`` are layer-by-layer lists of numpy arrays, similar
        to ``self.biases`` and ``self.weights``."""
        nabla_b = [np.zeros(b.shape) for b in self.biases]
        nabla_w = [np.zeros(w.shape) for w in self.weights]
        # feedforward
        activation = x
        activations = [x] # list to store all the activations, layer by layer
        zs = [] # list to store all the z vectors, layer by layer
        for b, w in zip(self.biases, self.weights):
            z = np.dot(w, activation)+b
            zs.append(z)
            activation = sigmoid(z)
            activations.append(activation)
        # backward pass
        delta = self.cost_derivative(activations[-1], y) * \
            sigmoid_prime(zs[-1])
        nabla_b[-1] = delta
        nabla_w[-1] = np.dot(delta, activations[-2].transpose())
        # Note that the variable l in the loop below is used a little
        # differently to the notation in Chapter 2 of the book.  Here,
        # l = 1 means the last layer of neurons, l = 2 is the
        # second-last layer, and so on.  It's a renumbering of the
        # scheme in the book, used here to take advantage of the fact
        # that Python can use negative indices in lists.
        for l in range(2, self.num_layers):
            z = zs[-l]
            sp = sigmoid_prime(z)
            delta = np.dot(self.weights[-l+1].transpose(), delta) * sp
            nabla_b[-l] = delta
            nabla_w[-l] = np.dot(delta, activations[-l-1].transpose())
        return (nabla_b, nabla_w)

    def evaluate(self, test_data):
        """Return the number of test inputs for which the neural
        network outputs the correct result. Note that the neural
        network's output is assumed to be the index of whichever
        neuron in the final layer has the highest activation."""
        test_results = [(np.argmax(self.feedforward(x)), y)
                        for (x, y) in test_data]
        return sum(int(x == y) for (x, y) in test_results)

    def cost_derivative(self, output_activations, y):
        """Return the vector of partial derivatives \partial C_x /
        \partial a for the output activations."""
        return (output_activations-y)

#### Miscellaneous functions
def sigmoid(z):
    """The sigmoid function."""
    return 1.0/(1.0+np.exp(-z))

def sigmoid_prime(z):
    """Derivative of the sigmoid function."""
    return sigmoid(z)*(1-sigmoid(z))

#net = Network([784, 100, 10]) # -> image
net = Network([8, 3, 2]) # my first ia with 2 output
iter_train = 50

do_i_load_a_net = input("Load a Network ? [Y/n]").lower()
if do_i_load_a_net == '' or do_i_load_a_net == "y":
    net.load_precedent_net()






import socket

host = 'localhost' 
port = 50000
backlog = 5 
size = 1024 
server_is_running = True

def reset_variable():
    global lastEffectKillTheCar,list_data,last_list_data,do_it_respawn
    lastEffectKillTheCar = 0; #if True the car is kill
    list_data = []
    last_list_data = []
    do_it_respawn = 0

reset_variable()
all_good_data = []
is_training = False # mettre true si on veut entrainer le model sinon si on veut juste utiliser le model mettre false
nb_client_connecte_for_a_net = 1
nb_client_already_connected_for_this_net = 0

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
s.bind((host,port)) 
s.listen(backlog)

print("Ready")

while server_is_running:
    client, address = s.accept() 
    print("Client connected.")
    client.send(b"0#0#")
    while 1:
        try:
            data = client.recv(size).decode('utf-8')
        except ConnectionAbortedError:
            data = "connectionAborted"
            
        if data == "ping":
            #print("Unity Sent: " + str(data))
            #sleep(1)
            
            #m = net.feeforward(data)
            #m[0]*2-1; m[1]*2-1;
            client.send(b"0#0#") # rotation#avance
        elif data == "" or data == "connectionAborted":
            if data == "":
                client.send(b"Bye!")
                print("Client disconnected!")
                client.close()
            do_i_save_the_net = input("Save the Network ? [Y/n]").lower()
            if do_i_save_the_net == '' or do_i_save_the_net == "y":
                net.save_the_net()
            if nb_client_already_connected_for_this_net >= nb_client_connecte_for_a_net-1:
                server_is_running = False
            else:
                nb_client_already_connected_for_this_net+=1
            break
        else:            
            print("get data")
            list_data = data.split("#")
            print(list_data)
            for i in range(0,len(list_data)):#range(0,8):
                list_data[i] = float(list_data[i].replace(",", "."))
                
            # Traitement des donnees avant celle recues
            if lastEffectKillTheCar ==0 and last_list_data:
                #print(len(all_good_data))
                all_good_data.append(last_list_data)
                #pass
            elif lastEffectKillTheCar==1.0:
                last_good_data = all_good_data[-215:] #-200#-220
                del(all_good_data[-215:])#-170#-220
                
                new_data = []
                new_data.append(last_list_data[0])
                if last_list_data[1][0] > 0.5:
                    jyvjvjy = 0
                elif last_list_data[1][0] < 0.5:
                    jyvjvjy = 1
                else:
                    jyvjvjy = 0.5
                #jyvjvjy = float(1-last_list_data[1][0])
                new_data.append([jyvjvjy,last_list_data[1][1]])#-last_list_data[0][0]*2+1)
                all_good_data.append(new_data)
                
                for last_good_data_each in last_good_data:
                    new_data = []
                    new_data.append(last_good_data_each[0])
                    if last_good_data_each[1][0] > 0.5:
                        jyvjvjy = 0
                    elif last_good_data_each[1][0] < 0.5:
                        jyvjvjy = 1
                    else:
                        jyvjvjy = 0.5
                    #jyvjvjy = float(1-last_list_data[1][0])
                    new_data.append([jyvjvjy,last_good_data_each[1][1]])#-last_list_data[0][0]*2+1)
                    all_good_data.append(new_data)
                
                do_it_respawn = 1
            #
            if do_it_respawn:
                reset_variable()
                do_it_respawn = 0
                # respawn
                print("respawn")
                client.send(b"127#127#")
                training_data = []
                is_training = True
                #if len(all_good_data[:-10]) > :#iter_train:
                #    for good_data in all_good_data[:100]:
                #        training_data.append((net.normalize_input_for_SGD(good_data[0]),net.normalize_output_for_SGD(good_data[1])))
                #    #print(training_data)
                #else:
                for good_data in all_good_data[:-10]:
                    training_data.append((net.normalize_input_for_SGD(good_data[0]),net.normalize_output_for_SGD(good_data[1])))
                    #print(training_data)
                #quantity_train = int(len(training_data)*2/3)
                #net.SGD(training_data[:quantity_train], iter_train, 10, 13.0)#, test_data=all_good_data[-10:])
                net.SGD(training_data, iter_train, 10, 3.5)#, test_data=all_good_data[-10:])
                all_good_data = []
                is_training = False
            else:
                if not is_training:
                    lastEffectKillTheCar = list_data[0]
                    del(list_data[0])
                    
                    
                    my_predictions = net.get_prediction(list_number=list_data)
                    
                    # Sauvegarde des donnees recues 
                    #last_list_data = [list_data,my_predictions]
                    last_list_data = [list_data,[my_predictions[0][0],my_predictions[1][0]]]
        
                    message = str(my_predictions[0][0]*2-1)[:6] + "#"+ str(my_predictions[1][0])[:6]+"#"
                    
                    message = message.replace(".", ",")
                    client.send(message.encode('utf-8')) # rotation#avance
                else:
                    lastEffectKillTheCar = list_data[0]
                    message = "0#0#"
                    client.send(message.encode('utf-8')) # rotation#avance 
                    