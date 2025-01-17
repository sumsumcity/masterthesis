## 4.5. Leak sensitive input data
> Category: runtime application security threat  

Impact: Confidentiality breach of sensitive input data.

Input data can be sensitive (e.g. GenAI prompts) and can either leak through a failure or through an attack, such as a man-in-the-middle attack.  

GenAI models mostly live in the cloud - often managed by an external party, which may increase the risk of leaking training data and leaking prompts. This issue is not limited to GenAI, but GenAI has 2 particular risks here: 1) model use involves user interaction through prompts, adding user data and corresponding privacy/sensitivity issues, and 2) GenAI model input (prompts) can contain rich context information with sensitive data (e.g. company secrets). The latter issue occurs with *in context learning* or *Retrieval Augmented Generation(RAG)* (adding background information to a prompt): for example data from all reports ever written at a consultancy firm. First of all, this context information will travel with the prompt to the cloud, and second: the context information may likely leak to the output, so it's important to apply the access rights of the user to the retrieval of the context. For example: if a user from department X asks a question to an LLM - it should not retrieve context that department X has no access to, because that information may leak in the output. 
