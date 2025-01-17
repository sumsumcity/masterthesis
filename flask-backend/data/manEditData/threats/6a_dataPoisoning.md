### 3.1.1. Data poisoning
> Category: development-time threat  

An attacker manipulates data that the model uses to learn, in order to affect the algorithm's behavior. Also called _causative attacks_. There are multiple ways to do this (see the attack surface diagram in the broad model poisoning section):
- Changing the data while in storage during development-time (e.g. by hacking the database)
- Changing the data while in transit to the storage (e.g. by hacking into a data transfer)
- Changing the data while at the supplier, before the data is obtained from the supplier
- Changing the data while at the supplier, where a model is trained and then that model is obtained from the supplier
- Manipulating data entry in operation, feeding into training data, for example by creating fake accounts to enter positieve reviews for products, making these products get recommended more often

The manipulated data can be training data, but also in-context-learning data that is used to augment the input (e.g. a prompt) to a model with information to use.

Example 1: an attacker breaks into a training set database to add images of houses and labels them as 'fighter plane', to mislead the camera system of an autonomous missile. The missile is then manipulated to attack houses. With a good test set this unwanted behaviour may be detected. However, the attacker can make the poisoned data represent input that normally doesn't occur and therefore would not be in a testset. The attacker can then create that abnormal input in practice. In the previous example this could be houses with white crosses on the door.  

Example 2: a malicious supplier poisons data that is later obtained by another party to train a model. 

Example 3: unwanted information (e.g. false facts) in documents on the internet causes a Large Language Model (GenAI) to output unwanted results. That unwanted information can be planted by an attacker, but of course also by accident. The latter case is a real GenAI risk, but technically comes down to the issue of having false data in a training set which falls outside of the security scope. Planted unwanted information in GenAI training data falls under the category of Sabotage attack as the intention is to make the model behave in unwanted ways for regular input.


There are roughly two categories of data poisoning: 

- Backdoors - which trigger unwanted responses to specific inputs (e.g. a money transaction is wrongfully marked as NOT fraud because it has a specific amount of money for which the model has been manipulated to ignore). Other name: Trojan attack
- Sabotage: data poisoning leads to unwanted results for regular inputs, leading to e.g. business continuity problems or safety issues.

Sabotage data poisoning attacks are relatively easy to detect because they occur for regular inputs, but backdoor data posoning only occurs for really specific inputs and is therefore hard to detect: there is no code to review in a model to look for backdoors, the model parameters cannot be reviewed as they make no sense to the human eye, and testing is typically done using normal cases, with blind spots for backdoors. This is the intention of attackers - to bypass regular testing.