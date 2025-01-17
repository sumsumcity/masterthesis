### Threat model
We distinguish three types of threats:
1. during development-time (when data is obtained and prepared, and the model is trained/obtained),
2. through using the model (providing input and reading the output), and
3. by attacking the system during runtime (in production).

In AI we distinguish 6 types of impacts, for three types of attacker goals (disrupt, deceive and disclose):
1. disclose: hurt confidentiality of train/test data
2. disclose: hurt confidentiality of model Intellectual property (the _model parameters_ or the process and data that led to them)
3. disclose: hurt confidentiality of input data
4. deceive: hurt integrity of model behaviour (the model is manipulated to behave in an unwanted way to deceive)
5. disrupt: hurt availability of the model (the model either doesn't work or behaves in an unwanted way - not to deceive but to disrupt)
6. confidentiality, integrity, and availability of non AI-specific assets

The threats that create these impacts use different attack surfaces. For example: the confidentiality of train data can be compromised by hacking into the database during development-time, but it can also leak by a _membership inference attack_ that can find out whether a certain individual was in the train data, simply by feeding that person's data into the model and looking at the details of the model output.

The diagram shows the threats as arrows. Each threat has a specific impact, indicated by letters referring to the Impact legend. The control overview section contains this diagram with groups of controls added.
[![](/images/threats.png)](/images/threats.png)

### AI Security Matrix
>Category: discussion  
>Permalink: https://owaspai.org/goto/aisecuritymatrix/

The AI security matrix below (click to enlarge) shows all threats and risks, ordered by type and impact.
[![](/images/OwaspAIsecuritymatix.png)](/images/OwaspAIsecuritymatix.png)