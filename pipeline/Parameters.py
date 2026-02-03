#klasa przechowująca parametry fizyczne

class PhysicsParameters:
    def __init__(self):
        self.alpha = 19 * 10 ** (-6) #dyfuzyjność powietrza
        self.c = 1005.0 #ciepło właściwe
        self.p = 101325.0 #ciśnienie atmosferyczne
        self.P = 1000.0 #moc grzejnika
        self.r = 287.05 #stała gazowa

        self.lambda_window = 0.96
        self.lambda_air = 0.0262
        self.lambda_wall = 0.4

        self.beta_window = self.lambda_window / self.lambda_air
        self.beta_wall = self.lambda_wall / self.lambda_air

        self.T_out = 263.0
        self.T_initial = 290.0
        self.T_target = 295.0
