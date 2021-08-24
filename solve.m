%%
timer = tic;
[x,flag,relres,iter,resvec] = minres(sparse_matrix,rhs,1e-12,1000);

time = toc(timer)

%%
timer = tic;
x = sparse_matrix\rhs;
time_LU = toc(timer)
relres_LU = normest(rhs-sparse_matrix*x)/normest(rhs)

if time_LU < time
   disp("LU Faster"); 
else
   disp("Krylov Faster"); 
end

%%