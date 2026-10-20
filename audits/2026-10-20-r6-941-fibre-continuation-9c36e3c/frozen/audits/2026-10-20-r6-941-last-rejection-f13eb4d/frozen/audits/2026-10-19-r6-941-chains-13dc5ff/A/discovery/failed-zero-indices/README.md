# Invalid discovery receipt

This archived certificate used G zero indices (0,3,5), not the required 941 zero indices (1,4,6). Its C11 closure counts are invalid for the named source. Root independent review caught the error before integration. The actual partition and short-pocket classifications did not depend on these zero indices. The current A/check.py binds the full mask to 941 and rejects this drift. This directory is provenance only, never a source certificate.
