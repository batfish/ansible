#   Copyright 2019 The Batfish Open Source Project
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
import os
import yaml
from collections import OrderedDict, Mapping
from copy import deepcopy
from pybatfish.client.session import Session
from pybatfish.datamodel.primitives import DataModelElement, ListWrapper

BATFISH_FACT_VERSION = "batfish_v0"

# Map of property name to new parent key
NODE_PROPERTIES_REORG = dict([
    ('DNS_Servers', 'DNS'),
    ('DNS_Source_Interface', 'DNS'),
    ('IKE_Phase1_Keys', 'IPsec'),
    ('IKE_Phase1_Policies', 'IPsec'),
    ('IKE_Phase1_Proposals', 'IPsec'),
    ('IPsec_Peer_Configs', 'IPsec'),
    ('IPsec_Phase2_Policies', 'IPsec'),
    ('IPsec_Phase2_Proposals', 'IPsec'),
    ('NTP_Servers', 'NTP'),
    ('NTP_Source_Interface', 'NTP'),
    ('Logging_Servers', 'Syslog'),
    ('Logging_Source_Interface', 'Syslog'),
    ('SNMP_Source_Interface', 'SNMP'),
    ('SNMP_Trap_Servers', 'SNMP'),
    ('TACACS_Servers', 'TACACS'),
    ('TACACS_Source_Interface', 'TACACS'),
])

def create_session(network=None, snapshot=None, **params):
    """Create session with the supplied params."""
    # TODO dynamically determine which session we want to use based on
    # available modules w/Sessions
    s = Session(**params)
    if network:
        s.set_network(network)
        if snapshot:
            s.set_snapshot(snapshot)
    return s


def get_facts(session, nodes_specifier):
    """Get current-snapshot facts from the specified session for nodes matching the nodes specifier."""
    # TODO assert questions exist
    args = {}
    if nodes_specifier:
        args['nodes'] = nodes_specifier

    node_properties = session.q.nodeProperties(**args).answer()
    interface_properties = session.q.interfaceProperties(**args).answer()
    bgp_process_properties = session.q.bgpProcessConfiguration(**args).answer()
    bgp_peer_properties = session.q.bgpPeerConfiguration(**args).answer()

    return _encapsulate_nodes_facts(_process_facts(node_properties,
                                                   interface_properties,
                                                   bgp_process_properties,
                                                   bgp_peer_properties),
                                    BATFISH_FACT_VERSION)


def load_facts(input_directory):
    """Load facts from text files in the specified directory."""
    out = {'version': None, 'nodes': {}}
    out_nodes = out['nodes']

    for filename in os.listdir(input_directory):
        with open(os.path.join(input_directory, filename), 'r') as f:
            dict_ = yaml.safe_load(f.read())
            assert 'version' in dict_
            assert 'nodes' in dict_
            version = dict_['version']
            nodes = dict_['nodes']

            if out['version'] and version != out['version']:
                raise ValueError('Input file version mismatch!')
            out['version'] = version

            # We allow a single input file to specify more than one node
            for node in nodes:
                out_nodes[node] = nodes[node]
    return out


def _process_facts(node_props, iface_props, bgp_process_props, bgp_peer_props):
    """Process properties answers into a fact dict."""
    # out = {}
    out = _process_nodes(node_props)
    _process_interfaces(out, iface_props)
    _process_bgp_processes(out, bgp_process_props)
    _process_bgp_peers(out, bgp_peer_props)

    # For some reason, Ansible tries to remove values from returned JSON
    # elements. This will cause an exception for ListWrapper (FrozenList), so
    # convert to a list to get around this.
    return _convert_listwrapper(out)


def _convert_listwrapper(dict_):
    """Convert ListWrapper objects in the specified dict into plain lists so Ansible can perform post-processing."""
    # TODO handle list wrappers inside of lists?
    out = {}
    for k in dict_:
        val = dict_[k]
        if isinstance(val, Mapping):
            out[k] = _convert_listwrapper(val)
        elif isinstance(val, ListWrapper):
            out[k] = list(val)
        else:
            out[k] = val
    return out


def _process_bgp_processes(node_dict, bgp_proc_props):
    """Return fact dict with processed bgp process properties answer added to it."""
    bgp_proc_dict = bgp_proc_props.frame().to_dict(orient='records')
    for r in bgp_proc_dict:
        node = r.pop('Node')
        # These will be replaced by bgp peers when we process them
        r['Neighbors'] = {}
        node_dict[node]['BGP'] = r


def _process_bgp_peers(node_dict, bgp_peer_props):
    """Return fact dict with processed bgp peer properties answer added to it."""
    bgp_peer_dict = bgp_peer_props.frame().to_dict(orient='records')
    for r in bgp_peer_dict:
        node = r.pop('Node')
        ip = r.get('Remote_IP')
        node_dict[node]['BGP']['Neighbors'][str(ip)] = r


def _process_interfaces(node_dict, iface_props):
    """Return fact dict with processed interface properties answer added to it."""
    iface_dict = iface_props.frame().to_dict(orient='records')
    for i in iface_dict:
        node = i['Interface'].hostname
        if node in node_dict:
            _add_interface(node_dict[node], i)
        else:
            # Should be impossible for ifaceProps to have node not in nodeProps
            raise ValueException(
                'Interface belongs to non-existent node {}'.format(node)
            )


def _process_nodes(node_props):
    """Return fact dict corresponding to processed node properties answer."""
    out = {}
    node_dict = node_props.frame().to_dict(orient='records')
    # print(node_dict)
    for record in node_dict:
        node = record.pop('Node')
        record.pop('Interfaces')
        # Add properties as children of node
        out[node] = record
        _reorg_dict(out[node], NODE_PROPERTIES_REORG)
    return out



def _add_interface(node_dict, iface_dict_in):
    """Update and add interface dict to the specified node dict."""
    if 'Interfaces' not in node_dict:
        node_dict['Interfaces'] = {}
    iface_dict = deepcopy(iface_dict_in)

    iface_name = iface_dict_in['Interface'].interface
    iface_dict.pop('Interface')

    node_dict['Interfaces'][iface_name] = iface_dict


def _reorg_dict(dict, reorg_map):
    """Reorganize top-level keys in the input dict based on the supplied reorg map."""
    for key in reorg_map:
        new_parent = reorg_map[key]
        if new_parent not in dict:
            dict[new_parent] = {}
        dict[new_parent][key] = dict.pop(key)


def _write_yaml_file(dict_, filepath):
    # TODO write stream instead of dumping and writing dump

    y = yaml.safe_dump(dict_, default_flow_style=False,
                       sort_keys=False)
    with open(filepath, 'w') as f:
        f.write(y)


def write_facts(output_directory, facts):
    """Write facts to YAML files in the supplied output directory."""
    version = facts['version']
    for node in facts['nodes']:
        filepath = os.path.join(output_directory, '{}.yml'.format(node))
        node_facts = _encapsulate_nodes_facts({node:facts['nodes'][node]},
                                              version)
        _write_yaml_file(node_facts, filepath)


def _encapsulate_nodes_facts(nodes_facts, version):
    """Format raw node(s) facts in the way they are written to file."""
    return {
        'nodes': nodes_facts,
        'version': version,
    }


def assert_dict_subset(actual, expected, prefix="", diffs=None):
    """Assert that the expected dictionary is a subset of the actual dictionary.

    :param actual: the dictionary tested
    :param expected: the expected value of a dictionary
    """
    if diffs is None:
        diffs = []
    for k in expected:
        key_name = '{}{}'.format(prefix, k)
        if k not in actual:
            # TODO need to differentiate between
            diffs.append({
                key_name: {
                    'key_present': False,
                    'expected': expected[k],
                }
            })
        else:
            if isinstance(expected[k], Mapping):
                assert_dict_subset(actual[k], expected[k], key_name + '.', diffs)
            else:
                if expected[k] != actual[k]:
                    #diffs.append('{}: expected: {}, actual: {}'
                    #             .format(key_name, expected[k], actual[k]))
                    diffs.append({
                        key_name: {
                            'expected': expected[k],
                            'actual': actual[k],
                        }
                    })
    return diffs
