import pandas as pd
from sklearn.metrics import mean_squared_error, make_scorer
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.cross_decomposition import PLSRegression
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import train_test_split


class Hw2Script():
    def __init__(self,data_frame):
        self.df = data_frame
        self.sc = StandardScaler()
    
    def define_variables(self,x_values,y_values,apply_sc=True):
        if apply_sc:
            self.X = self.sc.fit_transform(x_values.values)
            self.Y = self.sc.fit_transform(y_values.values.reshape(-1,1))
        else:
            self.X = x_values.values
            self.Y = y_values.values.reshape(-1,1)

    def define_train_test_set(self,train_test_size=(0.7,0.3)):
        self.X_train,self.X_test,self.Y_train,self.Y_test = train_test_split(self.X,self.Y, 
                                        train_size=train_test_size[0],
                                        test_size=train_test_size[1],random_state=42)
        
        
    def model_select(self,Model_name,model_parameters=None):
        if Model_name=='linear_reg':
            Model = make_pipeline(LinearRegression())
        
        if Model_name=='lasso':
            Model = make_pipeline(
                                  Lasso(alpha=model_parameters)
                                  )
        
        if Model_name=='ridge':
            Model = make_pipeline(
                                  Ridge(alpha=model_parameters)
                                  )
        if Model_name=='pcr':
            Model = make_pipeline(
                                  PCA(n_components=model_parameters),
                                  LinearRegression()
                                 )
        if Model_name=='pls':
            Model = make_pipeline(
                                PLSRegression(n_components=model_parameters)
                                 )        
        
        return Model
        
    
    def model_test(self,Model,X_train,Y_train,X_test,Y_test):  
        Model.fit(X_train,
                  Y_train)

        r2 =Model.score(X_test,
                        Y_test)
        
        Y_predict = Model.predict(X_test)
        
        rmse = mean_squared_error(Y_test,Y_predict)**0.5

        return r2,rmse
    
    
    def model_cv(self,fold_size,model,X,Y):
       
        rmse_cv= (-1*cross_val_score(model,X,
                           Y,cv=fold_size,
                           scoring= 'neg_root_mean_squared_error').mean())
            
        r2_cv= cross_val_score(model,X,
                        Y,cv=fold_size,
                        scoring= 'r2').mean()

        return r2_cv,rmse_cv
    
    def cross_val(self,model_name,parameter_values,X,Y):
        r2_cv5_values = []
        r2_cv10_values = []
        
        rmse_cv5_values = []
        rmse_cv10_values = []
        
        for x in parameter_values:
            model = self.model_select(model_name,x)
            
            
            r2_cv5,rmse_cv5 =   self.model_cv(5,model,X,Y)
            r2_cv10,rmse_cv10 = self.model_cv(10,model,X,Y)
            
            r2_cv5_values.append(r2_cv5)
            r2_cv10_values.append(r2_cv10)
            
            rmse_cv5_values.append(rmse_cv5)
            rmse_cv10_values.append(rmse_cv10)
        
        return (r2_cv5_values,r2_cv10_values,
                rmse_cv5_values,rmse_cv10_values)
    
    def pc_cv_vectors(self,number_of_components):
        
        return (self.cross_val('pls',number_of_components+1),
                self.cross_val('pcr',number_of_components))
    
    def best_pc_numbers(self,number_of_components):
        pls_cv,pcr = self.pc_cv_vectors(number_of_components)
        pls_n_components = pls_cv.index(np.max(pls_cv))
        pcr_n_components = pcr_cv.index(np.max(pls_cv))     
        return pls_n_components+1,pcr_n_components+1
    