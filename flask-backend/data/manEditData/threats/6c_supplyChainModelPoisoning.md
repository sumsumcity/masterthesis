### 3.1.3 Supply-chain model poisoning
>Category: development-time threat  

An attacker manipulates a third-party (pre-)trained model which is then supplied, obtained and unknowingly further used and/or trained/fine tuned, with still having the unwanted behaviour (see the attack surface diagram in the broad model poisoning section). If the supplied model is used for urther training, then the attack is called a _transfer learning attack_.

AI models are sometimes obtained elsewhere (e.g. open source) and then further trained or fine-tuned. These models may have been manipulated(poisoned) at the source, or in transit. See OWASP for LLM 03: Supply Chain.

The type of manipulation can be through data poisoning, or by specifically changing the model parameters. Therefore, the same controls apply that help against those attacks. Since changing the model parameters requires protection of the parameters at the moment they are manipulated, this is not in the hands of the one who obtained the model. What remains are the controls against data poisoning, the controls against model poisoning in general (e.g. model ensembles), plus of course good supply chain management.
