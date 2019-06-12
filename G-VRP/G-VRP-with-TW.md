# Mixed-integer Linear Programming Model for Green Vehicle Routing Problem with Time Window

## keywords

### most important words
- TSP(Traveling Salesman Problem)
- G-VRP(Green Vehicle Routing Problem)
- Time windows

### concerning word
- distribution
  - WMS => Web Map Service
  - TMS => Transport Management System
- logistics 

## 1. INTRODUCTION
  Many sectors in the world especially of transportation and distribution logistics interesting on decreasing greenhouse gas (GHG) emissions on fossil fuels motivates focus on the Green Vehicle
Routing Problem (GVRP). 
  Dekker et al [1] indicates the main optimization goals of green logistics activities because of its Vehicle routing problem (VRP) that is a problem related business of transportation and service which affects customer satisfaction. This problem is a widely used in the field of operational research that finding optimization routes for vehicles form original (one or more depots to customers. ) VRP generalizes from Traveling Salesman Problem (TSP) and its variants that is NP-hard Problem then Capacitated vehicle routing problem (CVRP) was first defined by Dantzig and Ramser in 1959 [2]. This problem used distance as a surrogate for the cost function, the cost of traveling from node *i* to node *j*, i.e., *cij* , has usually been taken as the distance between each nodes (for recent publications, see e.g. Baldacci et al. [1], Letchford and Salazar-Gonzalez [14], Yaman [21]) The transportation cost of a vehicle has various variables. However, the most of attributes are actually distance or travel time.

## 2. METHODOLOGY FOR CALCULATING TRANSPORTATION EMISSIONS AND ENERGY CONSUMPTION
  Hickman et al (1999) describes MEET that is methodology for calculating transportation emissions and energy consumption. This method classified the classes of CO2 emission for light duty diesel vehicles for classes weighing less 3.5 tons. It can estimate by using a speed dependent regression function for calculating the rate of emission follow: 

$$
e_{(v)} = 0.0617v^2-7.8227v+429.51
$$

The fuel consumption gathers into The Capacitated Vehicle Routing Problem (CVPR) was defined by Xiao et al (2012) [4]. They are using a regression model based on statistical data proposed by the Ministry of Land, Infrastructure, Transport and Tourism of Japan. The fuel consumption between node i and j for given load yij is calculated as
$$
p_{ij} = p_0 + \frac{p^* - p_0}{Q} y_{ij}
$$
Where p_0 is the fuel consumption rate for empty vehicle, p^* is the fuel consumption rate for fully loaded vehicle and Q is maximum weight. 

## 3. OPTIMIZATION MODEL
  This section, we describe the mathematical model for solve the problem. Traveling salesman problem to minimize the distance traveled that the salesman has to visit each one city stating from one city and returning to the same city. Let (G,V)  be a complete graph, where V is the set of n vertices (nodes) including a depot and A is the set of arcs (edges). Each arc (i,j) ∈ A has a non-negative length of dij. If there are m salesmen, the aim is to determine a tour for each I such that it starts and ends at the depot and at least one node is visited, and all nodes are visited once by any salesman. The objective function can be either minsum or minmax. The assignment based Type equation here.formulation of the minsum mTSP with Miller–Tucker–Zemlin (MTZ) (Miller, Tucker, & Zemlin, 1960) subtour elimination constraints is given as follows (Bektas, 2006; Gavish, 1976; Kara & Bektas, 2006; Sarin et al., 2014; Svestka & Huckfeldt, 1973):
$$
min\,z = \sum^n_{i=1}\sum^n_{i=1\\j\neq1}d_{ij}x_{ij}
$$
Subject to
$$
\sum_{j=2}^nx_{1j}=1\\
\sum_{i=2}^nx_{i1}=1\\
\sum_{i=1\\i\neq j}^nx_{ij}=1\ \forall \ j=2,...,n\\
\sum_{j=1\\j\neq i}^nx_{ij}=1\ \forall \ i=2,...,n\\
\sum_{i=1}^nx_{ij}-x_{ji}=0\ \forall \ j=\in n\\
T_i + t_{ij} - T_{j} \leq M(1 - x_{ij})\\
a_i + t_{ij} \leq b_j\\
x_{ij} \in \{0, 1\}\  \forall \ i, j = 1,2,...,n,i \neq j
$$
Here we assume that node 1 is the depot and the visiting rank of node 1, u1, is 0. Constraints (2) and (3) ensure that exactly m salesmen depart from and return to the depot. Constraint sets (4) and (5) are the assignment constraints requiring that each node (except the depot) should be preceded by and precedes exactly one another node. Constraint sets (6) and (7) are the MTZ subtour elimination constraints where 2 6 p 6 n m denotes the maximum number of cities that can be visited by any salesman. 
  Vehicle Routing Problem (VRPs) [4] is family of problems encountered notably in transportation. These problems are designing the vehicle routes for the most efficient way to dispatch either passengers or goods. The Capacitated Vehicle Routing Problem (CVPR) is defined on graph G = (V, A) be a graph where V = {1 .... , n} is a set of vertices representing cities (nodes) with the depot located at vertex 0, and A = {(i,j): i,j ∈V, i≠j} is the set of edge (arcs). 
$$
min\sum_{k=1}^m\sum_{i=0}^n\sum^n_{j=0}d_{ij}x_{ijk}
$$
Subject to..
$$
\sum_{k \in \ V}\sum_{j \in \ N}x_{ij} = 1\ \forall \ i \in C\\
\sum_{i \in V}d_{ij}\sum_{j \in V}x_{ijk} \leq q \ \forall \ k \in V\\
\sum_{j \in N}x_{0jk} = 1 \ \forall \ k \ \in V\\
\sum_{i \in N}x_{i0k} = 1 \ \forall \ k \ \in V\\
\sum_{i \in N}x_{ihk} - \sum_{j \in N}x_{hjk}= \forall \ h \in C \ ,k \in V\\
\sum_{i \in N}x_{i, n+1,k}=1\\
a_i \leq s_{ki} \leq b_i \ \forall \ i \in N, \ \forall \ k \in V\\
s_{ik} + T_{ij} - M(1-x_{ij}) \leq s_{jk} \ \forall \ i, j \in N, \ \forall \ k \in V
$$
  The objective function (3.1) minimizes the total travel cost. The constraints (3.2) ensure that each customer is visited exactly once, and (3.3) state that a vehicle can only be loaded up to it's capacity. Next, equations (3.4), (3.5) and (3.6) indicate that each vehicle must leave the depot 0; after a vehicle arrives at a customer it has to leave for another destination; and finally, all vehicles must arrive at the depot n + 1. The inequalities (3.7) establish the relationship between the vehicle departure time from a customer and its immediate successor. Finally constraints (3.8) affirm that the time windows are observed, and (3.9) are the integrality constraints. Note that an unused vehicle is modeled by driving the "empty" route (0,n + 1).
Bektas et al. [3] describe for calculating of pollution routing problem considering speed and effect of various variable the model. 
Assume that there are n customers with demand D_(i,) i=1,..n, one depot denoted as 0, and m homogeneous vehicles with limited capacity. Each vehicle departs and returns to the depot after serving all the customers. The fixed cost and capacity of each vehicle is F and Q, respectively. The FCVRP optimization model can be developed as follow:


## 1. 概要
　化石燃料から発生する温室効果ガス(GHG)の排出量の削減に興味を持っている多くの部門、特に交通、物流などの部門はGreen Vehicle Routing Problem (G-VRP)に注目しています。　交通や顧客満足に影響するサービスのビジネスに関係するVehicle routing problem(VRP)の問題のためだと、Dekker et alは主なグリーンロジスティクス活動の最適化の目的を示しています。この問題はもともと一つ、もしくはそれ以上の拠点から顧客までのルートの最適化の応用研究の分野で広く使われています。NP困難であるTraveling Salesman Problem(TSP)から一般化されたVRPにおいて、更に可積容量を考慮した問題であるCapacitated vehicle routing problem (CVRP)がDantzig and Ramserらによって最初に定義されたのは1959 [2]年のことです。 この問題ではコスト関数の代理として、ノードiからノードjのノード間距離cijを用いました。Baldacci et al. [1], Letchford and Salazar-Gonzalez[14], Yaman [21]らによる最近の発表を参照のこと。その移動のコストは様々な変数を持ちます。しかしながらそのほとんどの属性は実際には距離もしくは移動にかかる時間です。

## 2. 移動時のCO2排出量及びエネルギー消費量の計算方法
  Hickman et al (1999)　はMEET、つまり移動時の二酸化炭素排出量及びエネルギー消費量の計算方法を以下のように説明しています。このメソッドではCO2の排出量重量を分類し、重量が3.5トン未満の小型ディーゼル車であれば、そのスピードに基づいて、回帰分析で次のように排出量レートを計算することができます。
$$
e_{(v)} = 0.0617v^2-7.8227v+429.51
$$
CVPRでの燃料消費量はXiao et alによって2004年に定義されました[4]。彼らは日本の国土交通省による統計データを元にした回帰モデルを用いました。ノードiとノードjの間の燃料消費量は負荷 *y_ij* を用いて以下のように表されます。
$$
p_{ij} = p_0 + \frac{p^* - p_0}{Q} y_{ij}
$$
p_0は空の車両の燃料消費率であり、p^*は完全に満たされている車両の燃料消費率、Qは最大重量のことです。

## 3.最適化
 このセクションでは、問題を解決するための数学モデルについて説明します。移動距離を最小にするためのTSP(巡回セールスマン問題)では、セールスマンがある都市から出発して同じ都市に戻ってくる間に各都市を一度ずつ訪問しなければならないことはすでに述べました。（G、V）を完全グラフ、Vはデポを含むn個の頂点（ノード）の集合、Aは円弧（辺）の集合です。各エッジ(i, j)  Ａは、非負の長さdijをもちます。 m人のセールスマンがいる場合、目的はデポで開始および終了し、少なくとも1つのノードを訪問し、すべてのノードがいずれかのセールスマンによって1回訪問されるように、経路を決定することです。目的関数はminsumまたはminmaxのいずれかになります。代入に基づくMiller–Tucker–Zemlin (MTZ)サブツアーを排除した制約下でのminsum mTSP目的関数は以下で与えられています。（Minour、Tucker、＆Zemlin、1960）（Bektas 2006; Gavish 1976; Kara & Bektas, 2006; Sarin et al 2014; Svestka＆Huckfeldt 1973;): 
$$
min\,z = \sum^n_{i=1}\sum^n_{i=1\\j\neq1}d_{ij}x_{ij}
$$
Subject to
$$
\sum_{j=2}^nx_{1j}=1
$$

$$
\sum_{i=2}^nx_{i1}=1\\
\sum_{i=1\\i\neq j}^nx_{ij}=1\ \forall \ j=2,...,n\\
\sum_{j=1\\j\neq i}^nx_{ij}=1\ \forall \ i=2,...,n\\
\sum_{i=1}^nx_{ij}-x_{ji}=0\ \forall \ j=\in n\\
T_i + t_{ij} - T_{j} \leq M(1 - x_{ij})\\
a_i + t_{ij} \leq b_j\\
x_{ij} \in \{0, 1\}\  \forall \ i, j = 1,2,...,n,i \neq j
$$
ノード1をデポ、訪れるランクu1、0とす仮定する。また、制約(2)(3)は、厳密にセールスマンがデポから出発し、戻ってくると保証する。
代入制約(4)(5)ではそれぞれのノード(デポを除く)が異なる一つのノードにつながる必要がある。
制約条件(6)(7)では、MTZサブツアーの排除の制約を示しています。26p6nmにどのセールスマンも訪れられる最大の街の数を示してあります。
  VRPsは得に移動手段の問題として知られています。これらの問題は車両の経路を最も効率的にどの乗客、荷物にも配送できるように設計します。CVPRはグラフG=(V, A)で定義され、V = {1,...,n}はそれぞれの頂点0で示されるデポを含む街(ノード)を表現する頂点、A = {(i, j): i,j ∈V, i≠j}は辺(アーク)の集合です。
$$
min\sum_{k=1}^m\sum_{i=0}^n\sum^n_{j=0}d_{ij}x_{ijk}
$$
に従って、
$$
\sum_{k \in \ V}\sum_{j \in \ N}x_{ij} = 1\ \forall \ i \in C\\
\sum_{i \in V}d_{ij}\sum_{j \in V}x_{ijk} \leq q \ \forall \ k \in V\\
\sum_{j \in N}x_{0jk} = 1 \ \forall \ k \ \in V\\
\sum_{i \in N}x_{i0k} = 1 \ \forall \ k \ \in V\\
\sum_{i \in N}x_{ihk} - \sum_{j \in N}x_{hjk}= \forall \ h \in C \ ,k \in V\\
\sum_{i \in N}x_{i, n+1,k}=1\\
a_i \leq s_{ki} \leq b_i \ \forall \ i \in N, \ \forall \ k \in V\\
s_{ik} + T_{ij} - M(1-x_{ij}) \leq s_{jk} \ \forall \ i, j \in N, \ \forall \ k \in V
$$
目的関数(3.1)は経路のコストを最小にします。さらに、制約(3.2)は客がそれぞれ最低でも一度ずつ訪れられることを保証します。同様、制約(3.3)は各車両はその容量まで荷物を積むことができることを示しています。
制約(3.4)や(3.5)、(3.6)ではそれぞれ各車両は必ずデポ0を出発しなければならないこと、客を訪問した後はほかの一つの目的地に向けて主発しなければならないこと、これらより不等式(3.7)が導出され、車両の客先からの出発と即時の後継車の間の関係が示される。最後に制約(3.8)では時間窓が観察されていいることが示され。制約(3.9)に最終的な制約条件が集約されている。
$$
min \ C=\sum_{k=1}^m\sum_{j=1}^nfx_{ijk} + \sum_{k=0}^m\sum_{i=0}^n\sum_{j=0}^nc_{ijk}d_{ijk}(\rho_0x_{ijk} + \alpha y_{ij})
$$

 immediate successor.

 all vehicles must arrive at the depot n + 1. The inequalities (3.7) establish the relationship between the vehicle departure time from a customer and its immediate successor. 

Finally constraints (3.8) affirm that the time windows are observed, and (3.9) are the integrality constraints. Note that an unused vehicle is modeled by driving the "empty" route (0,n + 1).
Bektas et al. [3] describe for calculating of pollution routing problem considering speed and effect of various variable the model. 
Assume that there are n customers with demand D_(i,) i=1,..n, one depot denoted as 0, and m homogeneous vehicles with limited capacity. Each vehicle departs and returns to the depot after serving all the customers. The fixed cost and capacity of each vehicle is F and Q, respectively. The FCVRP optimization model can be developed as follow:





$$
xy^2+y+z-xz^2\\
\leftrightarrow x(y^2-z^2)+y+z\\
\leftrightarrow x(y+z)(y-z)+y+z\\
\leftrightarrow (y+z)\bigl\{ x(y-z) + 1 \bigr\}\\
$$


