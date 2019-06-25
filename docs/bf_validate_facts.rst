.. _bf_validate_facts:

bf_validate_facts
+++++++++++++++++
Validates facts for the current Batfish snapshot against the facts in the supplied directory

.. contents::
   :local:
   :depth: 2


Synopsis
--------


* Validates facts for the current Batfish snapshot against the facts in the ``expected_facts`` directory



Requirements
------------
The following software packages must be installed on hosts that execute this module:

* pybatfish



.. _module-specific-options-label:

Module-specific Options
-----------------------
The following options may be specified for this module:

.. raw:: html

    <table border=1 cellpadding=4>

    <tr>
    <th class="head">parameter</th>
    <th class="head">type</th>
    <th class="head">required</th>
    <th class="head">default</th>
    <th class="head">comments</th>
    </tr>

    <tr>
    <td>expected_facts<br/><div style="font-size: small;"></div></td>
    <td>str</td>
    <td>yes</td>
    <td></td>
    <td>
        <div>Directory to read expected facts from.</div>
    </td>
    </tr>

    <tr>
    <td>network<br/><div style="font-size: small;"></div></td>
    <td>str</td>
    <td>no</td>
    <td>Value in the <code>bf_network</code> fact.</td>
    <td>
        <div>Name of the network to validate facts for.</div>
    </td>
    </tr>

    <tr>
    <td>nodes<br/><div style="font-size: small;"></div></td>
    <td>str</td>
    <td>no</td>
    <td>All nodes</td>
    <td>
        <div>Nodes to extract facts for. See <a href='https://github.com/batfish/batfish/blob/master/questions/Parameters.md#node-specifier'>https://github.com/batfish/batfish/blob/master/questions/Parameters.md#node-specifier</a> for more details on node specifiers.</div>
    </td>
    </tr>

    <tr>
    <td>session<br/><div style="font-size: small;"></div></td>
    <td>dict</td>
    <td>no</td>
    <td>Value in the <code>bf_session</code> fact.</td>
    <td>
        <div>Batfish session object required to connect to the Batfish service.</div>
    </td>
    </tr>

    <tr>
    <td>snapshot<br/><div style="font-size: small;"></div></td>
    <td>str</td>
    <td>no</td>
    <td>Value in the <code>bf_snapshot</code> fact.</td>
    <td>
        <div>Name of the snapshot to validate facts for.</div>
    </td>
    </tr>

    </table>
    </br>

.. _bf_validate_facts-examples-label:

Examples
--------

::

    
    # Validate current snapshot facts against local YAML facts
    - bf_validate_facts:
        expected_facts: /path/to/local/YAML/files/
    # Validate current snapshot facts for nodes whose names contain as1border against local YAML facts
    - bf_validate_facts:
        nodes: '/as1border/'
        expected_facts: /path/to/local/YAML/files/



Return Values
-------------

.. raw:: html

    <table border=1 cellpadding=4>

    <tr>
    <th class="head">name</th>
    <th class="head">description</th>
    <th class="head">returned</th>
    <th class="head">type</th>
    </tr>


    <tr>
    <td>result</td>
    <td>
        <div>Contains a map of node-name to dictionary of failures for that node.</div>
    </td>
    <td align=center>when validation does not pass</td>
    <td align=center>dict</td>
    </tr>

    <tr>
    <td>summary</td>
    <td>
        <div>Summary of action(s) performed.</div>
    </td>
    <td align=center>always</td>
    <td align=center>str</td>
    </tr>

    </table>
    </br>
    </br>





Status
~~~~~~

This module is flagged as **preview** which means that it is not guaranteed to have a backwards compatible interface.


