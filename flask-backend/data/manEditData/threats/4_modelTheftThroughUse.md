## 2.4. Model theft through use
>Category: threat through use  

Impact: Confidentiality breach of model parameters, which can result in intellectual model theft and/or allowing to perform model attacks on the stolen model that normally would be mitigated by rate limiting, access control, or detection mechanisms.

This attack is known as model stealing attack or model extraction attack or model exfiltration attack. It occurs when an attacker collects inputs and outputs of an existing model and uses those combinations to train a new model, in order to replicate the original model. Alternative ways of model theft are development time model theft and direct runtime model theft.