### 3.2.1. Development-time data leak
>Category: development-time threat  

Unauthorized access to train or test data through a data leak of the development environment.

Impact: Confidentiality breach of sensitive train/test data.

Training data or test data can be confidential because it's sensitive data (e.g. personal data) or intellectual property. An attack or an unintended failure can lead to this training data leaking.  
Leaking can happen from the development environment, as engineers need to work with real data to train the model.  
Sometimes training data is collected at runtime, so a live system can become attack surface for this attack.  
GenAI models are often hosted in the cloud, sometimes managed by an external party. Therefore, if you train or fine tune these models, the training data (e.g. company documents) needs to travel to that cloud.
