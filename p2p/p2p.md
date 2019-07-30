
# The P2P Bucketing System in Witnet



Research conducted over the last years has shown us the consequences that a poorly designed P2P system might suffer, specially on a blockchain-based decentralized network. Not in vain, Bitcoin and Ethereum have changed the way peers connect to each other to become less susceptible to such an attack [[1]](https://www.usenix.org/node/190891)[[2]](https://www.cs.bu.edu/~goldbe/projects/eclipseEth.pdf). Imagine a node whose connections are entirely monopolized by an attacker. The attacker could, among others:

* Perform a double spending attack, by sending one transaction to the victim peer and another to the network.

* Eliminate the effect of the mining power of the victim nodes in the network.

<p align=center>
<img src="https://cdn-images-1.medium.com/max/2000/1*4HS0jShccYUFiAbCH0Hg-w.png" width="450">
</p>
<p align=center>
<em>Fig. 1:Eclipsing implies monopolizing all the connections made by a peer.</em>
</p>

In this case, the attacker has launched an **Eclipse Attack**. For an introductory explanation on how eclipse attacks are performed, we suggest the reader to take a look at [this article](https://medium.com/speaking-frankly/eclipse-attacks-on-bitcoin-s-peer-to-peer-network-e0da797302c2). Usually, in order to perform selfish mining or double spend attacks on an eclipsed node **an attacker needs to monopolize all its connections (incoming and outgoing)**. In Witnet, the aforementioned attack scenarios also require that an attacker monopolizes all the connections from the victim. However, **as Witnet does not implement a PoW consensus mechanism, any malicious actor can easily pre-construct a chain bigger than the one already in the network** and convince an eclipsed node it is the real chain. We observe two scenarios in which this might happen:

* Bootstrapping, i.e., when the node syncs for the first time. In this case, the node will likely start establishing outgoing connections through the DNS seeders.

* Disconnections due to reboot, power failures, DOS attacks, etc.

In these cases, **the blockchain tip in Witnet is decided by consensus**. The first outcome when designing the Witnet P2P network is clear then: **incoming connections do not play a role at synchronizing**. Otherwise, we would be giving a big advantage to the attacker. Still, in the case of pure majority consensus, **an attacker only needs to monopolize half plus one of the outbound connections made by the peer**. In the following we will refer as eclipsing to the action of monopolizing enough connections to convince a node to synchronize to a wrong chain tip.

There is a further reflection we can make at this point. At bootstrapping, it is expected that the IP addresses to which the outgoing connections will be made are obtained through a seeding process. In consequence, **we expect the connections made at this point to be honest, and thus, that a new node synchronizes with the correct chain tip** . If not, this would most likely imply that the attacker has polluted the bootstrap nodes from which we are getting addresses.

We focus in the case where an already synchronized node reboots, for whatever reason, and has to synchronize again. In this case, in order to avoid performing the seeding process again, the node should utilize the information it gathered from previous connections. The node uses tables that act like caches to store information about peers it has previously established successful connections with.

Remember that, upon reboot, the node will start syncing to the blockchain tip that the majority of the outgoing connections dictates. If an attacker is trying to *eclipse* a rebooted node it would need to control at least *n/2+1* of its outgoing connections. Our design will focus on this latter case, i.e. making costly for an attacker to monopolize *n/2+1* outgoing connections from a victim. Note that, by extension, monopolizing the *n*outgoing connections (which is necessary to perform double spend or selfish mining attacks) becomes increasingly difficult.

## Using buckets to store network information

Each node stores addresses it has already seen, serving as a cache for network information. We base our analysis on the same structure as in [[1]](https://www.usenix.org/node/190891), where network state is stored in two tables tried, *new*. The *tried* table stores peer addresses the node has already connected to, while the *new* table stores those of potential peer candidates.

<p align=center>
<img src="https://cdn-images-1.medium.com/max/2000/1*l54b71_eDook6LN-LCAn8Q.png" width="450">
</p>
<p align=center>
<em>Fig. 2:Bucketing system example for tried and new tables</em>
</p>

Similarly to how memory chunks are stored in caches, tables can be divided into buckets, each containing 64 slots. There are two main advantages of using bucketing systems for address storage:

* **Checking the existence of an address in a table distributed in buckets is more efficient**, as we do not have to go over the whole table, but rather the bucket maps to.

* A bucketing system prevents an adversary from polluting all the buckets with addresses from the same IP network range.

The aforementioned advantages are achieved thanks to the way the bucket to which each IP maps to is selected. For instance, in the *tried* table, an IP group (/16 address) can only map to 4 buckets in *tried*, while each specific IP maps to a single bucket. The following picture defines how the bucket to which an IP maps is selected.


<p align=center>
<img src="https://cdn-images-1.medium.com/max/2000/1*XHyinPlC5uc5-Ver7SWMJw.png" width="250">
</p>
<p align=center>
<em>Fig. 3:Bucket mapping for tried table as implemented in Bitcoin core</em>
</p>

In contrast, the bucket mapping in the *new* table is substantially different, as it also takes into account the source IP group notifying the addresses to be inserted. In this case, each (Source group, IP group) pair maps to up to 32 buckets, while each (Source group, IP) maps to a single bucket.

<p align=center>
<img src="https://cdn-images-1.medium.com/max/2000/1*-FO5YNGFxusknHLdOig7cw.png" width="250">
</p>
<p align=center>
<em>Fig. 4:Bucket mapping for new table as implemented in Bitcoin core</em>
</p>

When the node needs additional outgoing connections, addresses are selected from one of these tables. Initially our analysis will put a special focus in the *tried* table. Note that, when addresses are chosen randomly from both tables, extrapolating the results to both tables means, in the best scenario, increasing the number of buckets that need to be filled.

## Difficulty on eclipsing connections from the `tried` table

We start by adopting the first two countermeasures proposed by [[1]](https://www.usenix.org/node/190891), i.e. **addresses are randomly evicted and selected from the *tried* table**. Assuming all outgoing connections come from the *tried* table, we start analyzing the portion of the *tried* table the attacker would need to fill, for different maximum number of outgoing connection sizes. We model the outgoing connections monopolized by the attacker with the random variable *X*, which corresponds to a binomial with probability *T_a*, i.e. the proportion of the *tried* table he owns.

<p align=center>
<img src="https://cdn-images-1.medium.com/max/2000/1*XP2yrLGAQgRnpvUe1l5nXw.png" width="100">
</p>
<p align=center>
<em>Eq. 1:X refers to the number of outgoing connections monopolized by the attacker</em>
</p>

<p align=center>
<img src="https://cdn-images-1.medium.com/max/2000/1*KRyCkM5fM9D2ngk_yGDCdw.png" width="400">
</p>
<p align=center>
<em>Eq. 2:Probability of an attacker eclipsing a node at synchronization time</em>
</p>


The following graph represents the success rate an attacker would obtain for different proportions of the *tried* table controlled and different number of outgoing connections.

<p align=center>
<img src="https://cdn-images-1.medium.com/max/3586/1*IR1SiL3SU-6KELzzm3yQZQ.png" width="600">
</p>
<p align=center>
<em>Fig .5: Success rate of an attacker with random eviction/selection for different proportions of the tried table controlled and different number of outgoing connections</em>
</p>

As expected, the attacker gains a big advantage when it monopolizes an amount of addresses bigger than 50% of the table. In fact, the more outgoing connections we put in place the more advantage the attacker will have. Therefore, **an attacker can easily pollute the *tried* table through the incoming connections**.

But how many addresses would an attacker need to monopolize, e.g. 50% of the *tried* table? We adopt the model specified by [[1]](https://www.usenix.org/node/190891) in this case, where the number of attacker addresses in the *tried* table is modeled by the random variable *Y* while the number of addresses he possesses is *t* and *table_size* is the total size of the table.

<p align=center>
<img src="https://cdn-images-1.medium.com/max/2000/1*Au2NDc6bQ4ZwmPYSKCGybQ.png" width="250">
</p>
<p align=center>
<em>Eq. 3:Expected number of addresses in tried when t addresses are trying to be inserted. Equation taken from [1].</em>
</p>


The following graph presents the number of adversarial addresses that need to be owned to actually fill different percentages of the *tried* table, for different sizes of it. In this case, we assume the *tried* table has *m* buckets, each of which has 64 available slots.

<p align=center>
<img src="https://cdn-images-1.medium.com/max/3706/1*p5iKCi8e8-erNymjMoF1Gw.png" width="600">
</p>
<p align=center>
<em>Fig .6: Number of adversarial addresses needed to fill the table for different table sizes</em>
</p>

As it can be observed, filling an 60% of the *tried* table with a considerable size like 64 buckets would take 3750 addresses. As this number of addresses seems rather low for a powerful attacker, we need to adopt further countermeasures to prevent an Eclipse Attack from happening. In consequence, we introduce the 3rd countermeasure proposed by [[1]](https://www.usenix.org/node/190891): the ***test-before-evict* procedure**. Before evicting an address from the *tried* table, we perform a connection to it. If this is successful, the address is not evicted.

Note that one could think that increasing the size of the *tried* table requires the attacker to own a bigger number of addresses. Although this statement is true, with *test-before-evict*, it seems almost more important that the table is capable of fitting the number of honest peers, as this would be the worst case for the attacker. If the table is substantially bigger than the number of honest peers, this means the attacker already gained several slots for itself (those not occupied by honest peers), biasing the probability in its favor. **In consequence, *test-before-evict* suggests that increasing the number of buckets might indeed benefit the attacker.**

One of the most important facts that this countermeasure brings to P2P networks is the bound that it imposes to attackers’ success probability. As analyzed in [[1]](https://www.usenix.org/node/190891), assuming *h* honest addresses exist in the *tried* table with a responsiveness of *p*, the attacker is bounded by:

<p align=center>
<img src="https://cdn-images-1.medium.com/max/2000/1*T9UglL0rqyBfkHkJMYpqyw.png" width="150">
</p>
<p align=center>
<em>Eq. 4:The probability X is bounded by the number of honest addresses this time.</em>
</p>

<p align=center>
<img src="https://cdn-images-1.medium.com/max/2000/1*kLPdCrF-2FT4TP2J_WQ1gQ.png" width="350">
</p>
<p align=center>
<em>Eq. 5:Probability of eclipsing with test-before-evict</em>
</p>

We tested, for different number of outgoing connections and probability bounds, the proportion of the table (*ph/table_size*) that on average will need to be unevictable by an attacker (even with infinite number of addresses under his control). The results are the following:

<p align=center>
<img src="https://cdn-images-1.medium.com/max/3542/1*MFflep90KWZ7AYnuGDuFFw.png" width="600">
</p>
<p align=center>
<em>Fig .7: Attacker probability bound for different honest address proportions and maximum outgoing peers</em>
</p>

As expected, the lower we want to bound an attackers probability (upper line), the more responsive addresses we need to have already in the table. According to [[1]](https://www.usenix.org/node/190891), a 28% responsiveness is a good estimate for fairly recent addresses. Taking that into account, we can already say the results are not very optimistic, as even when the table is full of honest addresses the low responsiveness bounds the attacker to a success probability of 80% with 10 outgoing peers. In order to further protect from such a highly bounded attacker, we incorporate the following countermeasure: **parameterize the consensus percentage needed to synchronize a chain**. We call this parameter *c*. **This time, an attacker needs to own at least *c*** percentage of the outgoing connections to convince a node to synchronize with the wrong tip.

<p align=center>
<img src="https://cdn-images-1.medium.com/max/2000/1*xrIG14x3if8eL2QkdEsRAA.png" width="450">
</p>
<p align=center>
<em>Eq. 6:Probability of eclipsing when c*n monopolized connections are needed with the test-before-evict countermeasure</em>
</p>

The following graph represents the bound for the attackers probability for different proportions of unevictable address when 80% consensus is required to synchronize with the correct chain tip.

<p align=center>
<img src="https://cdn-images-1.medium.com/max/3600/1*oNGq56ORjsX_vLC9x34rMg.png" width="600">
</p>
<p align=center>
<em>Fig .8: Attacker bounded probability for different number of outgoing peers requiring at least 80%.</em>
</p>


Although the results look better, we still need further countermeasures to lower even more the attackers probability. Aiming at providing better protection, we **add the anchor connections countermeasure**: a table that stores the currently established outgoing connections. Upon reboot, the node reserves some of its outgoing connections to the anchor table. These are expected to be honest, assuming the previous outgoing connections were legitimate. We test the same scenario as before, but adding a 20% more connections that come from the anchor table.

<p align=center>
<img src="https://cdn-images-1.medium.com/max/3546/1*3xubcjfM8FHnPlO7d28aGQ.png" width="600">
</p>
<p align=center>
<em>Fig .9: Attacker bounded probability for different number of outgoing peers requiring at least 80% consensus with 20% anchor connections.</em>
</p>

This time we observe much nicer results. For instance, we observe that with 15 outgoing connections (thus 3 anchors), a 45% rightfully full *tried* table with a 28% responsiveness already bounds the attacker to 10% success probability. This is already better than what was reported in [[1]](https://www.usenix.org/node/190891), where to bound an attacker to a 10% probability a 67% filled table was needed. However, **we can make the attackers’ life even harder by protecting the *new* table.**

## The `new` table comes into consideration

We just spoke about the *tried* table, arguing that if addresses are selected from *tried* and *new* at random the only effect this would have is increasing the number of buckets (thus requiring more addresses from the attacker). **The former is true as long as the *new* table behaves similarly to the *tried* table**. The truth is we can restrict an attacker even more with two additional countermeasures in the *new* table:

* **Incoming connections are not allowed to send addresses to be inserted into the *new* table** (ADDR messages). That is, it is the peer itself who can request these messages (whenever it realizes the *new* table is sufficiently empty) and only to the outgoing connections. This prevents the pollution of the *tried* table as long as the outgoing connections are honest.

* A **feeler connection** is in charge of establishing short-lived connections with addresses in the *new* table. If those succeed, they are inserted in *tried* (if *test-before-evict* permits).

While the first countermeasure prevents an incoming malicious connection from polluting the *new* table with his own addresses, the second one validates the healthiness of the connections hosted in *new*. These two countermeasures have an impact on the approach selected by the attacker. Note that, under the assumption that addresses in *new* are legitimate, **an attacker not only needs to pollute the *tried* table but it needs to be lucky enough so that at least *c* per cent of the outgoing connections are selected from *tried***, being *c* the consensus percentage needed to synchronize. Modelling the selection from the tables as a binomial *Z* with probability 0.5, the success probability for an attacker becomes:

<p align=center>
<img src="https://cdn-images-1.medium.com/max/2000/1*8A3H2ar6xgdubNvcVPC3Bw.png" width="100">
</p>
<p align=center>
<em>Eq. 7:Z represents the number of connections selected from tried</em>
</p>

<p align=center>
<img src="https://cdn-images-1.medium.com/max/2000/1*D_jhNNIO0oTesWZY0PMXzg.png" width="400">
</p>
<p align=center>
<em>Eq. 8:Probability of eclipsing when addresses are selected from tried and new randomly and addresses in new are honest</em>
</p>

As before, we plot the bounded probability for the attacker in such a scenario for different number of outgoing peers, *c=0.8* and additional 20% anchor connections.

<p align=center>
<img src="https://cdn-images-1.medium.com/max/3546/1*3xubcjfM8FHnPlO7d28aGQ.png" width="600">
</p>
<p align=center>
<em>Fig .10: Attacker bounded probability for different number of outgoing peers requiring at least 80% consensus with 20% anchor connections and addresses randomly selected from tried and new.</em>
</p>

We observe a much nicer probability bound here. Indeed, with 10 outgoing connections (plus 2 anchors), we observe that an attacker can be bounded to a 0.1% probability with as few as 3% of the table filled with honest addresses.

The aforementioned analysis was made assuming addresses coming from *new* are honest. We argue that this is likely to be true for the following reasons:

- **Addresses in *new* are only inserted upon request, and this solicitation is only made to the outgoing connections**. It is thus likely that although the *tried* table can be easily polluted, the *new* table contains a significant amount of legitimate addresses.

- If an attacker wants to execute a multi-round (several reboot attack) it will face two major challenges. First, the *new* table needs to be empty enough so that the node asks the outgoing connections for addresses to be inserted. The former already requires that an attacker monopolizes a big portion of the outgoing connections, even in the case that honest peers report repeated addresses, as **the bucket selection in *new* also takes into account the source IP addresses**. Second, **if the *new* table is empty enough is because the feeler connection has succeeded to insert sufficient responsive honest addresses into the *tried* table**. Thus, honest addresses monopolize now the *tried* table.

- The cost, time and IP addresses to fill a majority of both tables with attacker addresses should already discourage the attacker from even trying it!

Table 1 shows the bounded attack probability with just 0.01 addresses (*ph/tablesize*) for different consensus percentage parameters.

<p align=center>
<img src="https://cdn-images-1.medium.com/max/2000/1*YurZigknBZ4-M_F6vfl_CA.png" width="600">
</p>
<p align=center>
<em>Table .1: Consensus required vs probability of an attacker being able to make eclipsed node fork.</em>
</p>

As the consensus is parametric, we recommend a minimum consensus percentage of 60%.

## Takeaways — Witnet bucketing parameters

Taking into account the former discussions, at Witnet we are considering to adopt the bucketing system as follows:

- **Three tables** are implemented, *new*, *tried* and anchor.

- The ***new* table contains addresses that have not been *tried*** (or that have previously been evicted from *tried*). The *tried* contains addresses to which the peer has recently established a connection. The anchor table contains references to the outgoing connections established.

- The ***new* table can only be populated upon requests from the peer** to its outgoing connections, which will only happen if the *new* table is sufficiently empty. The number of addresses that are sent is specified in [[1]](https://www.usenix.org/node/190891).

- **64 buckets will be featured in *tried***, while **256 buckets will be featured in *new***. Each will contain 64 slots, and the IP-bucket mapping will be made as in [[1]](https://www.usenix.org/node/190891). The anchor table will only contain the outgoing addresses.

- **12 outgoing connections** will be featured, 2 of which come from the anchor table.

- **Eviction and selection of addresses**, both from tables and buckets, **are chosen at random**.

- **Before evicting an address from *tried*, the potentially evicted addresses is tested**. If successful, the address is not evicted.

- **A single feeler connection will establish short lived connections with addresses in *new***. Upon success, these will be inserted in *tried*.

- The number of incoming connections will remain as in Bitcoin.

If the aforementioned countermeasures are not sufficient to deter a malicious attacker, we can limit the rate at which addresses are inserted into *tried*. This reduces the rate at which the *tried* table is populated, but offers higher security guarantees.

We hope our analysis clarifies the reasons behind the decisions made with respect to our P2P bucketing system. In following posts we will explain our decisions related to other aspects of the Witnet protocol.

### References

[1] [Eclipse attacks on Bitcoin’s P2P network](https://www.usenix.org/node/190891)

[2] [Low-resource eclipse attacks on Ethereum’s P2P network](https://www.cs.bu.edu/~goldbe/projects/eclipseEth.pdf)
