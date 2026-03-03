## Repository Structure (v0.2)

### Module Manifest Standard  
The Module Manifest Standard allows for module manifests to be located in the following paths:
- `<AgentName>/module.json`
- `<AgentName>/modules/<AgentName>/module.json`  
These locations will be searched canonically, ensuring that agents can effectively utilize the module manifests for their operations.

For more details on the policy, refer to [module manifest policy](core/governance/module-manifest-policy.md).

- Updated bullet about `/modules`: The `/modules` directory now adheres to the Module Manifest Standard for consistent organization and access.  

## Update Log  
- 2026-03-03: Added module manifest location policy and standardized manifest search patterns.