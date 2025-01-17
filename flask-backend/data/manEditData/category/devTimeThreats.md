## 3.0 Development-time threats - Introduction
> Category: group of development-time threats  
> Permalink: https://owaspai.org/goto/developmenttime/

This section discusses the AI security threats during the development of the AI system, which includes the engineering environment and the supply chain as attack surfaces.

**Background:**

Data science (data engineering and model engineering - for machine learning often referred to as _training phase_) introduces new elements and therefore new attack surface into the engineering environment. Data engineering (collecting, storing, and preparing data) is typically a large and important part of machine learning engineering. Together with model engineering, it requires appropriate security to protect against data leaks, data poisoning, leaks of intellectual property, and supply chain attacks (see further below). In addition, data quality assurance can help reduce risks of intended and unintended data issues.

**Particularities:**

- Particularity 1: the data in the AI development environment is real data that is typically sensitive, because it is needed to train the model and that obviously needs to happen on real data, instead of fake data that you typically see in standard development environment situations (e.g. for testing). Therefore, data protection activities need to be extended from the live system to the development environment.
- Particularity 2: elements in the AI development environment (data, code, configuration & parameters) require extra protection as they are prone to attacks to manipulate model behaviour (called _poisoning_)
- Particularity 3: source code, configuration, and parameters are typically critical intellectual property in AI
- Particularity 4: the supply chain for AI systems introduces two new elements: data and models
- Particularity 5: external software components may run within the engineering environments, for example to train models, introducing a new threat of malicious components gaining access to assets in that environment (e.g. to poison training data)