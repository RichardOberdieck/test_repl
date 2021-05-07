# %% [markdown]
# # Introduction
# The `gurobipy` API is Gurobi's own Python API. It is generally the recommended way of interacting with Gurobi, 
# as it is optimized for performance and contains all the latest features of the product.
#
# In this example, we will see how to formulate a very simple transportation problem using `gurobipy`:
# \begin{equation}
# \begin{array}{lll}
# \underset{x}{\text{minimize}} & c_{i,j}x_{i,j} & \text{Minimizing cost}\\
# \text{subject to} & \sum \limits_i x_{i,j} \geq D_j & \text{Satisfy demand }D_j \text{ for each fulfillment center } j \\
# & \sum \limits_j x_{i,j} \leq S_i & \text{Do not exceed supply }S_i \text{ from each distribution center } i \\
# & x_{i,j} \geq 0 & \text{Transported amounts have to be positive} \\
# \end{array}
# \end{equation}
#
# ## Data
# We use some very simple data to get started:

# %%
import gurobipy as gp


DC = ['seattle','san-diego']
FC = ['new-york','chicago', 'topeka']
Capacity = {'seattle':350,'san-diego':600}
Demand = {'new-york':325,'chicago':300,'topeka':275}
Distances = {
    ('seattle',  'new-york') : 2.5,
    ('seattle',  'chicago')  : 1.7,
    ('seattle',  'topeka')   : 1.8,
    ('san-diego','new-york') : 2.5,
    ('san-diego','chicago')  : 1.8,
    ('san-diego','topeka')   : 1.4,
}
Price = 90

# %% [markdown]
# ## gurobipy implementation

# %%
model = gp.Model("Transportation")
x = model.addVars(DC, FC, name='x')
model.addConstrs((x.sum('*',j) >= Demand[j] for j in FC), name='Demand')
model.addConstrs((x.sum(i,'*') <= Capacity[i] for i in DC), name='Supply')
model.setObjective(x.prod(Distances) * Price/1000)

# The optimization
model.optimize()
