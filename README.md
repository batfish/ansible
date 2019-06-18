# Ansible roles for Batfish

Intentionet has created this Ansible role to allow users to embed pre-deployment validation into any Ansible playbook. This role is hosted on Ansible Galaxy as `batfish.base`. The role includes a set of Ansible modules that analyze configuration files for an entire (or subset of a) network, allowing users to extract configuration data and perform network-wide validation tests in a completely vendor agnostic manner.

## Overview of Modules

Some of the modules included in the role are:

* **[bf_session](docs/bf_session.rst)** - Setup the connection to the server running Batfish or Batfish Enterprise

* **[bf_init_snapshot](docs/bf_init_snapshot.rst)** - Initialize a network snapshot

* **[bf_extract_facts](docs/bf_extract_facts.rst)** - Retrieve configuration facts for devices in the snapshot

* **[bf_validate_facts](docs/bf_validate_facts.rst)** - Validate configuration facts for devices in the snapshot

* **[bf_assert](docs/bf_assert.rst)** - Validate network behavior

See [docs](docs) for a complete list of modules and documentation. 

## Examples
The example playbook below outlines how to use the `batfish.base` role to extract the list of interfaces for all devices in the network.

```yaml
---
- name: Extract network device facts using Batfish and Ansible
  hosts: localhost
  connection: local
  gather_facts: no
  roles:
    - batfish.base

  tasks:

  - name: Setup connection to Batfish service
    bf_session:
      host: localhost
      name: local_batfish
  
  - name: Initialize the example network
    bf_init_snapshot:
      network: example_network
      snapshot: example_snapshot
      snapshot_data: ../networks/example
      overwrite: true

  - name: Retrieve Batfish Facts
    bf_extract_facts:
      output_directory: data/bf_facts
    register: bf_facts
    
  - name: Display configuration for all interfaces on all nodes
    debug: msg=" {{item.value.Interfaces}} "
    with_dict: "{{bf_facts.result.nodes}}"
    loop_control:
      label: " {{item.key}}.Interfaces "
    when: bf_facts.failed|bool == false
```

Check out the [tutorials](tutorials) for additional examples.

## Installation  
You must have the [Dependencies](#dependencies) installed on the system before you can use the role.

### Ansible Galaxy Role
To download the latest released version of the Batfish role to the Ansible server, execute the ansible-galaxy install command, and specify batfish.base

```
ansible-galaxy install batfish.base
```

## Dependencies

This module requires the following packages to be installed on the Ansible control machine:

- Python >= 2.7
- Ansible 2.7 or later
- Pybatfish >= 0.36
- PyYAML >= 3.10

## License
Apache 2.0

## Support
Support for this role is provided by the community and Intentionet. If you have an issue with a module in this role, you may:

- Open a Github [issue](https://github.com/batfish/ansible/issues)
- Join our [Slack Group](https://join.slack.com/t/batfish-org/shared_invite/enQtMzA0Nzg2OTAzNzQ1LTUxOTJlY2YyNTVlNGQ3MTJkOTIwZTU2YjY3YzRjZWFiYzE4ODE5ODZiNjA4NGI5NTJhZmU2ZTllOTMwZDhjMzA) and post a question

## Contributors
Intentionet is contributing to and maintaining this repository.
