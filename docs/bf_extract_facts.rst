.. _bf_extract_facts:

bf_extract_facts
++++++++++++++++
Extracts facts for a Batfish snapshot

.. contents::
   :local:
   :depth: 2


Synopsis
--------


* Extracts and returns facts for a Batfish snapshot and saves them (one YAML file node) to the output directory if specified.



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
    <td>network<br/><div style="font-size: small;"></div></td>
    <td>str</td>
    <td>no</td>
    <td>Value in the <code>bf_network</code> fact.</td>
    <td>
        <div>Name of the network to extract facts for.</div>
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
    <td>output_directory<br/><div style="font-size: small;"></div></td>
    <td>str</td>
    <td>no</td>
    <td><code>null</code></td>
    <td>
        <div>Directory to save facts to.</div>
    </td>
    </tr>

    <tr>
    <td>session<br/><div style="font-size: small;"></div></td>
    <td>dict</td>
    <td>no</td>
    <td>Value in <code>bf_session</code> fact.</td>
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
        <div>Name of the snapshot to extract facts for.</div>
    </td>
    </tr>

    </table>
    </br>

.. _bf_extract_facts-examples-label:

Examples
--------

::

    
    # Extract facts and save to an output directory
    - bf_extract_facts:
        output_directory: output/facts/
    # Extract facts for nodes whose names contain as1border or host
    - bf_extract_facts:
        nodes: /as1border|host/



Return Values
-------------

.. raw:: html

    <table border=1 cellpadding=4>

    <tr>
    <th class="head">name</th>
    <th class="head">description</th>
    <th class="head">returned</th>
    <th class="head">type</th>
    <th class="head">sample</th>
    </tr>


    <tr>
    <td>result</td>
    <td>
        <div>Dictionary of extracted facts.</div>
    </td>
    <td align=center>always</td>
    <td align=center>complex</td>
    <td align=center></td>
    </tr>

    <tr>
    <td>contains:</td>
    <td colspan=4>
        <table border=1 cellpadding=2>

        <tr>
        <th class="head">name</th>
        <th class="head">description</th>
        <th class="head">returned</th>
        <th class="head">type</th>
        <th class="head">sample</th>
        </tr>

        <tr>
        <td>nodes</td>
        <td>
            <div>Dictionary of node-name to node-facts for each node.</div>
        </td>
        <td align=center>always</td>
        <td align=center>complex</td>
        <td align=center></td>
        </tr>

        <tr>
        <td>version</td>
        <td>
            <div>Fact-format version of the returned facts.</div>
        </td>
        <td align=center>always</td>
        <td align=center>str</td>
        <td align=center></td>
        </tr>

        </table>
    </td>
    </tr>

    <tr>
    <td>summary</td>
    <td>
        <div>Summary of action(s) performed.</div>
    </td>
    <td align=center>always</td>
    <td align=center>str</td>
    <td align=center></td>
    </tr>

    </table>
    </br>
    </br>





Status
~~~~~~

This module is flagged as **preview** which means that it is not guaranteed to have a backwards compatible interface.


