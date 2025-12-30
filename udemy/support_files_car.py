'''
LICENSE AGREEMENT

In relation to this Python file:

1. Copyright of this Python file is owned by the author: Mark Misin
2. This Python code can be freely used and distributed
3. The copyright label in this Python file such as

copyright=ax_main.text(x,y,'© Mark Misin Engineering',size=z)
that indicate that the Copyright is owned by Mark Misin MUST NOT be removed.

WARRANTY DISCLAIMER!

This Python file comes with absolutely NO WARRANTY! In no event can the author
of this Python file be held responsible for whatever happens in relation to this Python file.
For example, if there is a bug in the code and because of that a project, invention,
or anything else it was used for fails - the author is NOT RESPONSIBLE!

'''

import numpy as np
import matplotlib.pyplot as plt


from scipy.linalg import block_diag
from scipy import signal, integrate

class SupportFilesCar:
    ''' The following functions interact with the main file'''

    def __init__(self):
        ''' Load the constants that do not change'''

        # Constants
        m=1500
        Iz=3000
        Caf=19000
        Car=33000
        lf=2
        lr=3
        Ts=0.02

        # Parameters for the lane change: [psi_ref 0;0 Y_ref]
        # Higher psi reduces the overshoot
        # Matrix weights for the cost function (They must be diagonal)
        Q=np.matrix('100 0;0 1') # weights for outputs (all samples, except the last one)
        S=np.matrix('100 0;0 1') # weights for the final horizon period outputs
        R=np.matrix('1') # weights for inputs (only 1 input in our case)

        outputs=2 # number of outputs
        hz = 20 # horizon period
        x_dot=20 # car's longitudinal velocity
        lane_width=7 # [m]
        nr_lanes=5 # 6 lanes [m]
        # r=14*np.random.randint(2)-7 # amplitude for sinusoidal functions
        # f=0.01*np.random.randint(2)+0.01 # frequency
        r=4
        f=0.01
        time_length = 10 # [s] - duration of the entire manoeuvre

        ### PID ###
        PID_switch=0 # Turn PID function ON/OFF (ON=1, OFF=0)

        Kp_yaw=7
        Kd_yaw=3
        Ki_yaw=5

        Kp_Y=7
        Kd_Y=3
        Ki_Y=5

        ### PID END ###

        trajectory=1 # You should only choose 1,2,3

        self.constants={'m':m, 'Iz':Iz, 'Caf':Caf, 'Car':Car, 'lf':lf, 'lr':lr,\
            'Ts':Ts, 'Q':Q, 'S':S, 'R':R, 'outputs':outputs, 'hz':hz, 'x_dot':x_dot,\
            'r':r, 'f':f, 'time_length':time_length, 'lane_width':lane_width,\
            'PID_switch':PID_switch, 'Kp_yaw':Kp_yaw, 'Kd_yaw':Kd_yaw, 'Ki_yaw':Ki_yaw,\
            'Kp_Y':Kp_Y, 'Kd_Y':Kd_Y, 'Ki_Y':Ki_Y, 'trajectory':trajectory}

        return None

    def trajectory_generator(self,t,r,f):
        '''This method creates the trajectory for a car to follow'''

        Ts=self.constants['Ts']
        x_dot=self.constants['x_dot']
        trajectory=self.constants['trajectory']

        # Define the x length, depends on the car's longitudinal velocity
        x=np.linspace(0,x_dot*t[-1],num=len(t))

        # Define trajectories

        if trajectory==1:
            y=-9*np.ones(len(t))
        elif trajectory==2:
            y=9*np.tanh(t-t[-1]/2)
        elif trajectory==3:
            aaa=-28/100**2
            aaa=aaa/1.1
            if aaa<0:
                bbb=14
            else:
                bbb=-14
            y_1=aaa*(x+self.constants['lane_width']-100)**2+bbb
            y_2=2*r*np.sin(2*np.pi*f*x)
            y=(y_1+y_2)/2
        else:
            print("For trajectories, only choose 1, 2, or 3 as an integer value")
            exit()

        # Vector of x and y changes per sample time
        dx=x[1:len(x)]-x[0:len(x)-1]
        dy=y[1:len(y)]-y[0:len(y)-1]

        # Define the reference yaw angles
        psi=np.zeros(len(x))
        psiInt=psi
        psi[0]=np.arctan2(dy[0],dx[0])
        psi[1:len(psi)]=np.arctan2(dy[0:len(dy)],dx[0:len(dx)])

        # We want the yaw angle to keep track the amount of rotations
        dpsi=psi[1:len(psi)]-psi[0:len(psi)-1]
        psiInt[0]=psi[0]
        for i in range(1,len(psiInt)):
            if dpsi[i-1]<-np.pi:
                psiInt[i]=psiInt[i-1]+(dpsi[i-1]+2*np.pi)
            elif dpsi[i-1]>np.pi:
                psiInt[i]=psiInt[i-1]+(dpsi[i-1]-2*np.pi)
            else:
                psiInt[i]=psiInt[i-1]+dpsi[i-1]

        return psiInt,x,y

    def state_space(self):
        '''This function forms the state space matrices and transforms them in the discrete form'''

        # Get the necessary constants
        m=self.constants['m']
        Iz=self.constants['Iz']
        Caf=self.constants['Caf']
        Car=self.constants['Car']
        lf=self.constants['lf']
        lr=self.constants['lr']
        Ts=self.constants['Ts']
        x_dot=self.constants['x_dot']

        # Get the state space matrices for the control
        A1=-(2*Caf+2*Car)/(m*x_dot)
        A2=-x_dot-(2*Caf*lf-2*Car*lr)/(m*x_dot)
        A3=-(2*lf*Caf-2*lr*Car)/(Iz*x_dot)
        A4=-(2*lf**2*Caf+2*lr**2*Car)/(Iz*x_dot)

        A=np.array([[A1, 0, A2, 0],[0, 0, 1, 0],[A3, 0, A4, 0],[1, x_dot, 0, 0]])
        B=np.array([[2*Caf/m],[0],[2*lf*Caf/Iz],[0]])
        C=np.array([[0, 1, 0, 0],[0, 0, 0, 1]])
        D=np.zeros((C.shape[0], B.shape[1]))

        # Discretise the system (forward Euler)
        sys = signal.StateSpace(A, B, C, D)
        dis = sys.to_discrete(Ts, method = 'euler')

        # Discretise the system (forward Euler)
        # Ad=np.identity(np.size(A,1))+Ts*A
        # Bd=Ts*B
        # Cd=C
        # Dd=D
        # return Ad, Bd, Cd, Dd

        return dis.A, dis.B, dis.C, dis.D

    def mpc_simplification(self, Ad, Bd, Cd, Dd, hz):
        '''This function creates the compact matrices for Model Predictive Control'''
        # db - double bar
        # dbt - double bar transpose
        # dc - double circumflex

        A_aug = np.block([
            [Ad                                  , Bd                       ],
            [np.zeros((Bd.shape[1], Ad.shape[1])), np.identity(Bd.shape[1]) ],
        ])
        # TODO: decide whether to use concat or block for cases like this
        B_aug = np.block([
            [Bd                      ],
            [np.identity(Bd.shape[1])],
        ])
        C_aug = np.block([
            Cd, np.zeros((Cd.shape[0],Bd.shape[1]))
        ])
        D_aug=Dd

        Q=self.constants['Q']
        S=self.constants['S']
        R=self.constants['R']

        CQC = C_aug.T @ Q @ C_aug
        CSC = C_aug.T @ S @ C_aug
        QC = Q @ C_aug
        SC = S @ C_aug

        blocks = [[
            np.linalg.matrix_power(A_aug,((i+1)-(j+1))) @ B_aug
            if i >= j else np.zeros((B_aug.shape))
        for j in range(0, hz)] for i in range(0, hz)]
        Cdb = np.block(blocks)

        # TODO: concat would be much more readable here
        Adc = np.block([[np.linalg.matrix_power(A_aug, i+1)] for i in range(0, hz)])

        Qdb = block_diag( *([CQC]*(hz-1) + [CSC]) )
        Tdb = block_diag( *([QC ]*(hz-1) + [SC ]) )
        Rdb = block_diag( *([R  ]*(hz  )        ) )
        Hdb= Cdb.T @ Qdb @ Cdb + Rdb
        Fdbt = np.concat((
            Adc.T @ Qdb @ Cdb,
            -Tdb @ Cdb,
        ))

        return Hdb,Fdbt,Cdb,Adc

    def de(self, t, states, U1):
        # Get the necessary constants
        m=self.constants['m']
        Iz=self.constants['Iz']
        Caf=self.constants['Caf']
        Car=self.constants['Car']
        lf=self.constants['lf']
        lr=self.constants['lr']
        x_dot=self.constants['x_dot']

        y_dot, psi, psi_dot, Y = states

        # Compute the the derivatives of the states
        y_dot_dot=-(2*Caf+2*Car)/(m*x_dot)*y_dot+(-x_dot-(2*Caf*lf-2*Car*lr)/(m*x_dot))*psi_dot+2*Caf/m*U1
        psi_dot=psi_dot
        psi_dot_dot=-(2*lf*Caf-2*lr*Car)/(Iz*x_dot)*y_dot-(2*lf**2*Caf+2*lr**2*Car)/(Iz*x_dot)*psi_dot+2*lf*Caf/Iz*U1
        Y_dot=np.sin(psi)*x_dot+np.cos(psi)*y_dot

        return np.array([y_dot_dot, psi_dot, psi_dot_dot, Y_dot])

    def open_loop_new_states(self,states,U1):
        '''This function computes the new state vector for one sample time later'''

        # Get the necessary constants
        Ts=self.constants['Ts']

        # integrate system over one time-step
        result = integrate.solve_ivp(self.de, (0, Ts), y0=states, args=(U1,))
        return result.y[:, -1]
