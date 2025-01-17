## 2.1. Evasion
>Category: group of threats through use  

Evasion: an attacker fools the model by crafting input to mislead it into performing its task incorrectly. 

Impact: Integrity of model behaviour is affected, leading to issues from unwanted model output (e.g. failing fraud detection, decisions leading to safety issues, reputation damage, liability).

A typical attacker goal with Evasion is to find out how to slightly change a certain input (say an image, or a text) to fool the model. The advantage of slight change is that it is harder to detect by humans or by an automated detection of unusual input, and it is typically easier to perform (e.g. slightly change an email message by adding a word so it still sends the same message, but it fools the model in for example deciding it is not a phishing message).  
Such small changes (call 'perturbations') lead to a large (and false) modification of its outputs. The modified inputs are often called *adversarial examples*.  

Evasion attacks can be categorized into physical (e.g. changing the real world to influence for example a camera image) and digital (e.g. changing a digital image). Furthermore, they can be categorized in either untargeted (any wrong output) and targeted (a specific wrong output). Note that Evasion of a binary classifier (i.e. yes/no) belongs to both categories.

Example 1: slightly changing traffic signs so that self-driving cars may be fooled.


Example 2: through a special search process it is determined how a digital input image can be changed undetectably leading to a completely different classification.

Example 3: crafting an e-mail text by carefully choosing words to avoid triggering a spam detection algorithm.

Example 4: by altering a few words, an attacker succeeds in posting an offensive message on a public forum, despite a filter with a large language model being in place

AI models that take a prompt as input (e.g. GenAI) suffer from an additional threat where manipulative instructions are provided - not to let the model perform its task correctly but for other goals, such as getting offensive answers by bypassing certain protections. This is typically referred to as direct prompt injection
