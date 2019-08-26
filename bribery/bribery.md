
# Deterring Bribery Attacks on Decentralized Oracle Networks

<p align=center>
<img src="https://miro.medium.com/max/981/0*dVWrWdyk3KLMhQoV" width="550">
</p>
<p align=center>
<em>Fig. 1:Bribery by https://tumonispost.com/2019/05/14/best-time-to-bribe/.</em>
</p>


The theory behind SchellingCoin[[1]](https://blog.ethereum.org/2014/03/28/schellingcoin-a-minimal-trust-universal-data-feed/) systems is that if everyone is expected to vote honestly, the incentive is to follow suit to be part of the majority. Bribery attacks aim at breaking this *Nash equilibrium* by influencing the direction in which voters vote. However, the briber’s success depends on the specific motivations of each participant:

* __Selfish voters__: those that aim at achieving the highest profit of the game.

* __Altruist voters__: those voters that vote honestly regardless of potential higher pots.


<p align=center>
<img src="https://cdn-images-1.medium.com/max/2000/1*YBQjef-6RZLf2dV7FUi4fg.png" width="450">
</p>
<p align=center>
<em>Fig. 2: A briber specifies in a smart contract an additional reward that is payed out under certain conditions.</em>
</p>

Bribery attacks on Decentralized Oracle Networks (DONs), if considered practical, can have consequences on the client smart contracts. As opposed to an attack in Bitcoin/Ethereum, in which the loss of confidence in the network reduces the attractiveness of launching an attack, a potential attack in a DON might lead to off-chain profit (e.g. in an different sidechain/protocol). In the following paragraphs we discuss bribery attacks and how these can be addressed through different countermeasures.

We utilize a SchellingCoin framework to simplify the analysis, although most DONs feature more complicated schemes that decrease the practicality of the attack . For instance, voters in a DON might provide a very wide range of answers upon which requester-defined aggregation and consensus functions are executed. Instead, in **a typical SchellingCoin example voters need to decide among two options, e.g., 0 and 1** and only obtain a reward if they vote with the majority. The following matrix represents the options and rewards for a certain voter.

<p align=center>
<img src="https://cdn-images-1.medium.com/max/2000/1*ios5oc9BrmLxjMZCArOTtg.png" width="450">
</p>
<p align=center>
<em>Fig. 3: Payout matrix in a SchellingCoin framework.</em>
</p>

For a further explanation on this kind of framework, we suggest the reader to take a look at:

[**On Oracles and Schelling Points**
*Schelling schemes and seeking consensus in a Decentralized Oracle Network*](https://medium.com/witnet/on-oracles-and-schelling-points-2a1807c29b73)

We proceed to explain how these options can be altered by a briber promising a reward for voting according to their interest. We will use the following nomenclature:

* *N*: number of voters.

* ε: additional reward offered by the briber.

* *α*: percentage of participants that voted for the majority option.

* *S*: collateral that needs to be put as deposit.

* *V*: aggregated stake of parties involved in a smart contract.

* *h*: percentage of altruist participants in the network.

## P+epsilon attacks

P+epsilon attacks[[2]](https://blog.ethereum.org/2015/01/28/p-epsilon-attack/)[[3]](https://kleros.io/assets/whitepaper.pdf)[[4]](https://github.com/kleros/kleros-attacks/files/2322312/kleroscountercoordination3.pdf) are those in which an attacker promises a bribe slightly higher than the reward obtained by honest participants (those that they did not manipulate their votes). Bribes could be specified in a smart contract in which additional rewards ε are promised for those proving to have voted for the briber-chosen option. However, in P+epsilon attacks, **the bribe is only paid out when the briber-chosen option does not win**. This is important: **if somehow voters achieve consensus on the option specified by the attacker, the briber’s attack has succeeded at zero cost**. That converts the SchellingCoin matrix into the following one, being 1 the true fact:

<p align=center>
<img src="https://cdn-images-1.medium.com/max/2000/1*R71rgwz2lqSO5AgaWyDRPQ.png" width="450">
</p>
<p align=center>
<em>Fig. 4: Payout matrix with P+epsilon attack.</em>
</p>

For the sake of simplicity, we will assume for now that all voters are selfish. In that worst case scenario, they all have an interest in voting for 0, as they will win regardless of the outcome. However, note that **there is some counter-coordination game voters can play here**. Since the briber only pays when the attack fails, participants could vote 1 with a 51% probability and 0 with 49% probability to **maximize the benefit obtained**. In this way 51% of the participants obtain the reward and 49% the attackers bribe, while the consensus is still maintained.

**This counter-coordination game could look like a defense but it is actually not**. Imagine the situation where the attacker chooses to bribe on the honest option instead. The aforementioned selfish behavior still applies and voters will achieve a 51% consensus on the dishonest option, thus rendering the counter-coordination game completely malleable at *0.49 * N(P+ε)* cost.

**At this point it seems the only possible defense is to make the attack more expensive for the briber**. We can increase the bribe the attacker needs to promise by just defining the reward in a group-basis and not individually. This means the reward *P* will be distributed among those voters that voted with the consensus. In fact, the fewer voters that achieve consensus (α), the more reward they individually obtain. This leaves the table as follows:

<p align=center>
<img src="https://cdn-images-1.medium.com/max/2000/1*k9r32JKql_j8f9guxHklxA.png" width="450">
</p>
<p align=center>
<em>Fig. 5: Payout matrix in a P+epsilon attack with aggregated reward.</em>
</p>

This further gives incentives to the probabilistic game in which voters vote 1 with probability α while they vote 0 with probability *(1-α)*, being α>50%. Note that if everybody votes 0 the reward for each of the voters will be *P/N*. Thus, it is expected that the attacker at least pays an amount bigger than *P/αN*. There are two options:

* If such amount is substantially bigger, it might achieve the effect in which selfish participants vote for the bribed fact. However, in order to achieve a zero-cost attack, the briber should be willing to risk a significant stake.

* The closer the bribe gets to *P/αN*, the more the briber is favoring the counter-coordination game, in which case the briber would need to bribe the true fact.

By making the reward groupal we doubled the lowest acceptable bribe from P/N to *P/(0.51N)*. In order to further increase it, **voters could be required to stake a deposit substantially bigger than the reward**, a strategy conceived by [Paul Storcz](http://www.truthcoin.info/papers/truthcoin-whitepaper.pdf). This stake (*S*) could be specified by the voting creators. **Under this scheme, if a node does not vote with the consensus, it loses its stake which is distributed among the nodes who voted for the winning option**.

<p align=center>
<img src="https://cdn-images-1.medium.com/max/2000/1*gMwSknmmEQyyRnRzGVucCg.png" width="450">
</p>
<p align=center>
<em>Fig. 6: Payout matrix in a P+epsilon attack with additional stake.</em>
</p>

In this particular case **the briber needs to offer a price bigger than the stake each voter needs to deposit** plus the maximum reward possibly obtained. We are making the attacker promise to pay a minimum ε of S to cover stake losses. The previous scheme leads to the following options:

* If all participants vote for the same option, *α=1* and the reward they obtain is *P/N*;

* If the attacker’s bribe covers the **stake loss plus the maximum reward** it is expected that 51% participants vote for the non-bribed option and 49% vote for the other. In this case the briber needs to bribe the true fact promising *bribe = (P/αN + S(1-α)/α + ε)*. Note that epsilon is now ε>S instead of 0. The total payout of the briber would be Eq.1, which for *α ≈ 0.5* and *S ≫ P* would be of a total of around *S * N*.

<p align=center>
<img src="https://cdn-images-1.medium.com/max/2000/1*RaPApBM9FkI4Zmkl9LMzwg.png" width="200">
</p>
<p align=center>
<em>Eq. 1: Total briber payout.</em>
</p>

### Bribery attacks

The idea of the Bribery attack is very similar to the P+epsilon attack. **However, this time, if nodes vote for the option chosen by the briber they get the briber reward, no matter what the majority voted for**. Similar to the analysis made for P+epsilon attacks, a way to make the bribe more expensive is to force the participants to pay a deposit *S*. Again, the briber needs to offer a minimum ε of S.

<p align=center>
<img src="https://cdn-images-1.medium.com/max/2000/1*-gNULBMJfP9HT_AiGRETZw.png" width="450">
</p>
<p align=center>
<em>Fig. 7: Payout m atrix with bribery attack, assuming aggregated reward and stake.</em>
</p>

In this case all selfish participants will undoubtfully (α = 1) vote for the bribed option, and the attacker will succeed influencing the result at the mininum cost of *P + N * S*. Again if *S ≫ P*,  would be of a total of around *S * N*.

### On the influence of external stakes

So far we have defined the lowest amount that the briber needs to devote to perform a successful attack. However, once the result of the voting is used as an oracle to resolve a smart contract, we can assume the attacker will not want to risk an amount higher than its own stake in the contract (V). From the point of view of the smart contract creator (voting proposer) requiring a stake of *S = V/N* would be sufficient to secure the voting. This means that **such a scheme can only completely secure votings up to the total value of the network at time *t***.

### Closing thoughts

We have analyzed the potential threats that P+epsilon and bribery attacks might have on voting schemes. However, these attacks might turn impractical when they are mounted against a DON like [Witnet](https://witnet.io/static/witnet-whitepaper.pdf) for the following facts:

* **These attacks have mostly being described in the case of human voting**, but DONs like Witnet have pure software nodes performing the tasks. We believe **it should not be easy to convince a person of trusting and using an altered version of the software,** which may lead to a complete loss of funds.

* Specifically in Witnet, nodes are randomly chosen and thus, even if an attacker is able to bribe more than half of the network, there is no guarantee that the committee will be compromised. In addition **Witnet biases probabilities based on past behavior, so it is expected that the majority of the committee is composed of honest peers (those that have the highest interest on the healthiness of the network).**

Even with those impediments in mind, we decided to implement the explained staking countermeasure in Witnet, letting **the smart contract creator decide the amount nodes need to deposit**. For each Witnet data request, we expect the required stake to be proportional to the value of the consuming smart contract divided by the number of participants. Further, keep in mind that Witnet has been designed with the goal of favouring non-professional miners, and as such, we expect a non-negligible level of altruism. In this sense, **Witnet’s core values, specially the decentralization and low barriers to entry, are key factors to prevent bribing attacks**. You can check the main goals of our design here:

[**Designing a Decentralized Oracle Network**
*The insights of how Witnet wants to serve your unstoppable smart contracts*medium.com](https://medium.com/witnet/designing-a-decentralized-oracle-network-cad5c5855ba2)

## References

[1] [SchellingCoin: A Minimal-Trust Universal Data Feed](https://blog.ethereum.org/2014/03/28/schellingcoin-a-minimal-trust-universal-data-feed/)

[2] [The P + epsilon Attack](https://blog.ethereum.org/2015/01/28/p-epsilon-attack/)

[3] [Kleros whitepaper](https://kleros.io/assets/whitepaper.pdf)

[4] [p + epsilon and counter-coordination comments](https://github.com/kleros/kleros-attacks/files/2322312/kleroscountercoordination3.pdf)

