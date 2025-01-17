## 4.3. Direct runtime model theft
> Category: runtime application security threat  

Impact: Confidentiality breach of model parameters, which can result in intellectual model theft and/or allowing to perform model attacks on the stolen model that normally would be mitigated by rate limiting, access control, or detection mechanisms.

Stealing model parameters from a live system by breaking into it (e.g. by gaining access to executables, memory or other storage/transfer of  parameter data in the production environment). This is different from model theft through use which goes through a number of steps to steal a model through normal use, hence the use of the word 'direct'. It is also different from model theft development-time from a lifecylce and attack surface perspective.

This category also includes _side-channel attacks_, where attackers do not necessarily steal the entire model but instead extract specific details about the model’s behaviour or internal state. By observing characteristics like response times, power consumption, or electromagnetic emissions during inference, attackers can infer sensitive information about the model. This type of attack can provide insights into the model's structure, the type of data it processes, or even specific parameter values, which may be leveraged for subsequent attacks or to replicate the model.