## 3.1. Broad model poisoning development-time
> Category: group of development-time threats  

Development-time model poisoning in the broad sense is when an attacker manipulates development elements (the engineering environment and the supply chain), to alter the behavior of the model. There are three types, each covered in a subsection:
1. data poisoning: an attacker manipulates training data, or data used for in-context learning.
2. development-environment model poisoning: an attacker manipulates model parameters, or other engineering elements that take part in creating the model, such as code, configuration or libraries.
3. supply-chain model poisoning: using a supplied trained model which has been manipulated by an attacker.

Impact: Integrity of model behaviour is affected, leading to issues from unwanted model output (e.g. failing fraud detection, decisions leading to safety issues, reputation damage, liability).

Data and model poisoning can occur at various stages, as illustrated in the threat model below.  
- Supplied data or a supplied model can have been poisoned
- Poisoning in the development environment can occur in the data preparation domain, or in the training environment. If the training environment is separated security-wise, then it is possible to implement certain controls (including tests) against data poisoning that took place at the supplier or during preparation time.
- In the case that training data is collected runtime, then this data is under poisoning threat.
- Model poisoning alters the model directly, either at the supplier, or development-time, or during runtime.

