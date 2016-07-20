from pulp import (LpProblem, LpAffineExpression, LpVariable, LpBinary,
                  LpMaximize, LpStatus, LpStatusOptimal, lpSum)
from bson import ObjectId
from dal import get_collection

# Constant
BIG_M = 9999999
SLACK = 1


class Product:
    def __init__(self, name, lower_limit, sale_price):
        self.name = name
        self.lower_limit = lower_limit
        self.sale_price = sale_price
        self.discounts = []
        # decision variables
        self.x = []
        self.y = []


def run(scenario_id):
    # read data from scenario_id
    coll = get_collection('scenario').find_one(
        {'_id': ObjectId(scenario_id)})
    fund = coll['fund']
    products = []
    for prod_dict in coll['products']:
        product = Product(prod_dict['name'], prod_dict['lowerLimit'],
                          prod_dict['salePrice'])
        product.discounts.append({'threshold': 0, 'discount': 1})
        for discount in prod_dict['discounts']:
            product.discounts.append(discount)

        products.append(product)

    for prod in products:
        prod.x = [LpVariable('x_{0}{1}'.format(prod.name, i + 1), 0)
                  for i in range(len(prod.discounts))]
        prod.y = [LpVariable('y_{0}{1}'.format(prod.name, i + 1), cat=LpBinary)
                  for i in range(len(prod.discounts))]

    problem = LpProblem('MVP_{0}'.format(scenario_id), sense=LpMaximize)

    mv_obj_var = LpVariable('MV_Obj')
    y_obj_var = LpVariable('y_Obj')
    problem += mv_obj_var - y_obj_var

    # Objective functions
    problem += lpSum([prod.sale_price * prod.x[i] for prod in products
                      for i in range(len(prod.x))]) == mv_obj_var
    problem += lpSum([prod.y[i] for prod in products
                      for i in range(len(prod.y))]) == y_obj_var
    # End of Obj

    # Constraints
    # sum(b_ij * X_ij) == fund
    problem += lpSum(
        [prod.sale_price * prod.discounts[i]['discount'] * prod.x[i]
         for prod in products for i in range(len(prod.discounts))]) == fund

    for prod in products:
        expr = LpAffineExpression()
        n = len(prod.discounts)
        for i in range(n):
            expr += prod.x[i]

            # M * y_ij >= x_ij
            problem += BIG_M * prod.y[i] >= prod.x[i]

            if i + 1 < n:
                rhs = prod.discounts[i + 1]['threshold'] \
                      - prod.discounts[i]['threshold'] - SLACK
                # x_ij <= C_ij+1 - C_ij - 1
                problem += prod.x[i] <= rhs

            if i > 0:
                rhs = prod.discounts[i]['threshold'] \
                      - prod.discounts[i - 1]['threshold'] - SLACK
                # M * (1 - y_ij) >= C_ij - C_ij-1 - X_ij-1 - 1
                problem += BIG_M * (1 - prod.y[i]) >= rhs - prod.x[i - 1]

        if len(expr) > 0:
            # sum(X_i) >= lower_limit
            problem += expr >= prod.lower_limit

        problem.writeLP('C:\\Projects\Python\{0}.lp'.format(problem.name))
        problem.solve()
        if problem.status == LpStatusOptimal:
            with open('C:\\Projects\Python\{0}.sol'.format(problem.name),
                      'w') as sol:
                sol.write('Solution of {0}\n'.format(problem.name))
                sol.write('Obj value: {0}\n'.format(problem.objective.value()))
                sol.writelines(['{0} = {1}\n'.format(v.name, v.value())
                                for v in problem.variables()])

    return LpStatus[problem.status]


if __name__ == '__main__':
    run('578e0038389cb5179c757502')
