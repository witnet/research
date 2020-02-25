# Dynamic Threshold in RePoE
## RePoE
RePoE, Reputation Proof of Eligibility, allows us to decide which witnesses are selected 
to solve the data request. This proof utilizes the influence of the node operator, in terms 
of its reputation weight, 
<a href="https://www.codecogs.com/eqnedit.php?latex=r_i" target="_blank"><img src="https://latex.codecogs.com/gif.latex?r_i" title="r_i" /></a>
, to calculate the odds to become eligible for a data request in the active reputation system, 
having total reputation _R_:

<a href="https://www.codecogs.com/eqnedit.php?latex=P&space;=&space;\frac{r_i}{R}*&space;N" target="_blank"><img src="https://latex.codecogs.com/gif.latex?P&space;=&space;\frac{r_i}{R}*&space;N" title="P = \frac{r_i}{R}* N ," /></a>

where _N_ denotes the minimum number of witnesses needed to resolve a specific data request.

This probability will be translated in a static threshold that provides the maximum value  
to obtain a valid RePoE. That limit will be compared with the output of a [VRF][vrf] (Verifiable 
Random Function) provided by the node operator which takes as seed the data request hash 
and the last CheckpointBeacon of the chain.

## Why do we need a dynamic threshold?

Because of how our reputation system works, the reputation distribution is unpredictable and 
the probability described above may not guarantee eligibility for the number of nodes required 
in the data request. This situation could interrupt the data request resolution, let's see an example.

Example:\
Address A: 1000 rep\
Address B: 1000 rep\
Address C: 1000 rep\
Address D: 10 rep\
Address E: 10 rep\
-----------------------------\
Total Rep _R_ = 3020 rep

In this case, for a data request which requires 4 witnesses, the probabilities for the first 
three will be 1 (actually it is 1.32 but it is not possible to have a probability bigger than 
1 for a single node), while the last two will have probability 0.0132. So in most of the cases 
we only obtain 3 valid witnesses, A, B and C, that are not enough to solve the data request.

This problem appears when the probability of at least one witness exceeds 1, because that implies
the remaining nodes have not enough probability. In other words, most of the times not enough 
witnesses will be eligible to resolve the data request. In the example, we expected 4 but adding 
all the probabilities we obtain 3.0264 (1+1+1+0.0132+0.0132).

## Proposed solution

The idea is to calculate a specific factor, alpha, related to the state of the reputation system 
and the witnesses required which, multiplied by the older threshold, adjusts the probabilities 
to obtain the witnesses number required:

<a href="https://www.codecogs.com/eqnedit.php?latex=P&space;=&space;\frac{r_i}{R}*&space;N&space;*\alpha" target="_blank"><img src="https://latex.codecogs.com/gif.latex?P&space;=&space;\frac{r_i}{R}*&space;N&space;*\alpha" title="P = \frac{r_i}{R}* N ," /></a>

When the reputation of a node operator 
<a href="https://www.codecogs.com/eqnedit.php?latex=r_i" target="_blank"><img src="https://latex.codecogs.com/gif.latex?r_i" title="r_i" /></a> 
multiplied by the witnesses number (_N_) is bigger than the 
total active reputation _R_, the error explained appears. So, to calculate the new factor value, 
we have to find the subset of nodes reputation R[n,...,l-1], where it doesn't happen. Let's suppose 
_n_ is the smallest index such that the probability is smallest than one:

<a href="https://www.codecogs.com/eqnedit.php?latex=n&space;\in&space;\mathbb{N}&space;:&space;\forall&space;i&space;\geq&space;n&space;\text{,&space;}&space;\frac{r_i&space;\cdot&space;(N-i))}{R_{i}}&space;<&space;1" target="_blank"><img src="https://latex.codecogs.com/gif.latex?n&space;\in&space;\mathbb{N}&space;:&space;\forall&space;i&space;\geq&space;n&space;\text{,&space;}&space;\frac{r_i&space;\cdot&space;(N-i))}{R_{i}}&space;<&space;1" title="n \in \mathbb{N} : \forall i \geq n \text{, } \frac{r_i \cdot (N-i))}{R_{i}} < 1" /></a>

Then the factor alpha is calculated as follows:

<a href="https://www.codecogs.com/eqnedit.php?latex=\alpha&space;=&space;\frac{R&space;\cdot&space;(N-n)}{R_{n}&space;\cdot&space;N}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?\alpha&space;=&space;\frac{R&space;\cdot&space;(N-n)}{R_{n}&space;\cdot&space;N}" title="\alpha = \frac{R \cdot (N-n)}{R_{n} \cdot N}" /></a>

To achieve it we just need to follow the next procedure:
* Step 1: sort all the actives nodes by reputation.
* Step 2: check if the first node's reputation (
<a href="https://www.codecogs.com/eqnedit.php?latex=r_0" target="_blank"><img src="https://latex.codecogs.com/gif.latex?r_0" title="r_0" /></a>)
 multiplied by witnesses number required (N) is bigger than total active reputation.
  * If it is bigger, remove that reputation from the total active reputation, reduce the witnesses 
  number by 1 and repeat step 2.
  * If it is not, we calculate alpha as in the previous equation and exit.

Moving back to the previous example:\
Required witnesses: 4, _N_ = 4\
Address A: 1000 rep\
Address B: 1000 rep\
Address C: 1000 rep\
Address D: 10 rep\
Address E: 10 rep\
-----------------------------\
Total Rep _R_ = 3020 rep

 - First, reputation is already sorted. _R_ = 3020, n = 0
 - Second, 1000 * (4-0) = 4000 > 3020 -> _R_1_ = 2020, _n_ = 1
 - Third, 1000 * (4-1) = 3000 > 2020 -> _R_2_ = 1020, _n_ = 2
 - Fourth, 1000 * (4-2) = 2000 > 1020 -> _R_3_ = 20, _n_ = 3  
 - Fifth, 10 * (4-3) = 10 < 20 -> Subset reached!
 
 So the final value for alpha is 37.75, that multiplied by the older probability produces 4 (1+1+1+0.5+0.5).
 
[vrf]: https://github.com/witnet/vrf-rs
