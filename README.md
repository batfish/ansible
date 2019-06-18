# Ansible roles for Batfish

Intentionet has created this Ansible role to allow users to embed [Batfish](https://www.github.com/batfish/batfish) pre-deployment validation into any Ansible playbook. This role is hosted on Ansible Galaxy as `batfish.base`. The role includes a set of Ansible modules that analyze configuration files for an entire (or subset of a) network, allowing users to extract configuration data and perform network-wide validation tests in a completely vendor agnostic manner.

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

## Dependencies

This module requires the following packages to be installed on the Ansible control machine:

- Python >= 2.7
- Ansible 2.7 or later
- PyYAML >= 3.1, < 4.3 (these requirements are inherited from the Docker module; latest version works if you are not using that)

- Running Batfish service and Pybatfish

   - To install Batfish and Pybatfish, you may use the [batfish setup playbook](tutorials/playbooks/batfish_setup.yml) or run the following commands:
      ```
      docker pull batfish/allinone
      docker run -v batfish-data:/data -p 8888:8888 -p 9997:9997 -p 9996:9996 batfish/allinone
      python -m pip install --upgrade git+https://github.com/batfish/pybatfish.git
      ```

## Installation  

Ensure that the [dependencies](#dependencies) above are met, and then get the latest version of the role from Ansible galaxy. 

```
ansible-galaxy install --force batfish.base
```


## License
Apache 2.0

## Support
For bug reports and feature requests, you may:

- Open a Github [issue](https://github.com/batfish/ansible/issues)
- Join our [Slack Group](https://join.slack.com/t/batfish-org/shared_invite/enQtMzA0Nzg2OTAzNzQ1LTUxOTJlY2YyNTVlNGQ3MTJkOTIwZTU2YjY3YzRjZWFiYzE4ODE5ODZiNjA4NGI5NTJhZmU2ZTllOTMwZDhjMzA) and post a question

## Contributors
Intentionet is contributing to and maintaining this repository.
