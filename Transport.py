""" Transport.py : 輸送問題

問題のベースとなっているサイト
http://www.nct9.ne.jp/m_hiroi/light/pulp01.html

サンプルとさせていただいたコード
https://github.com/KJMAN678/solver/blob/main/solver.ipynb

問題
工場 (x, y) から商品を店 (a, b, c) に配送します。供給量、需要量、輸送コストが下表で与えられているとき、総輸送コストが最小となる配送の仕方を求めてください。

"""
import cvxpy as cp
import pandas as pd

df = pd.DataFrame(
    [
        [10, 6, 16, 8],
        [8, 8, 4, 16],
        [12, 4, 8, ]
    ],
    columns=["店a", "店b", "店c", "供給量"],
    index=["工場x", "工場y", "需要量"]
)
print(df)

shop_list = ["a", "b", "c"]

# 変数の設定
fact_x = cp.Variable(
    len(shop_list),  # 要素数。2次元の場合は(x, y)と設定する
    integer=False,  # 整数の場合はTrueとする
    boolean=False,  # Binary値の場合はTrueとする
    pos=True  # 正の数
)

fact_y = cp.Variable(
    len(shop_list),  # 要素数。2次元の場合は(x, y)と設定する
    integer=False,  # 整数の場合はTrueとする
    boolean=False,  # Binary値の場合はTrueとする
    pos=True  # 正の数
)

# 目的変数の設定
exp = cp.sum(fact_x * df.iloc[:1, :3].squeeze() +
             fact_y * df.iloc[1:2, :3].squeeze())
obj = cp.Minimize(exp)

# 制約条件の設定
# 需要量の設定
const = []
for i in range(3):
    const += [fact_x[i] + fact_y[i] >= df.iloc[2, i]]

# 供給量の設定
const += [cp.sum(fact_x) <= df["供給量"][0]]
const += [cp.sum(fact_y) <= df["供給量"][1]]

# 問題の設定と実行
prob = cp.Problem(obj, const)
status = prob.solve(verbose=True)
status

# 結果
pd.options.display.precision = 15

result = pd.DataFrame(
    [
        [fact_x[i].value for i in range(3)],
        [fact_y[i].value for i in range(3)],
    ],
    columns=["店a", "店b", "店c"],
    index=["工場x", "工場y"]
)

print(result)
print(prob.value)
