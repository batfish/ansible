.. _bf_init_snapshot:

bf_init_snapshot
++++++++++++++++
Initializes a Batfish snapshot with provided snapshot data

.. contents::
   :local:
   :depth: 2


Synopsis
--------


* Initializes a Batfish snapshot with provided snapshot data and populates ``bf_network`` and ``bf_snapshot`` facts.



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
    <td></td>
    <td>yes</td>
    <td></td>
    <td>
        <div>Name of the network in which to initialize the snapshot.</div>
    </td>
    </tr>

    <tr>
    <td>overwrite<br/><div style="font-size: small;"></div></td>
    <td></td>
    <td>no</td>
    <td></td>
    <td>
        <div>Boolean indicating if the snapshot name already exists in the specified network.</div>
    </td>
    </tr>

    <tr>
    <td>session<br/><div style="font-size: small;"></div></td>
    <td></td>
    <td>no</td>
    <td>Value in <code>bf_session</code> fact.</td>
    <td>
        <div>Batfish session object required to connect to the Batfish service.</div>
    </td>
    </tr>

    <tr>
    <td>snapshot<br/><div style="font-size: small;"></div></td>
    <td></td>
    <td>yes</td>
    <td></td>
    <td>
        <div>Name of the snapshot to initialize.</div>
    </td>
    </tr>

    <tr>
    <td>snapshot_data<br/><div style="font-size: small;"></div></td>
    <td></td>
    <td>yes</td>
    <td></td>
    <td>
        <div>Path to snapshot data directory or zip. See <a href='https://github.com/batfish/batfish/wiki/Packaging-snapshots-for-analysis'>https://github.com/batfish/batfish/wiki/Packaging-snapshots-for-analysis</a> for more details on packaging your snapshot for analysis.</div>
    </td>
    </tr>

    </table>
    </br>

.. _bf_init_snapshot-examples-label:

Examples
--------

::

    
    # Initialize a snapshot with specified snapshot data
    - bf_init_snapshot
        network: datacenter_sea
        snapshot: 2019-01-01
        snapshot_data: /path/to/snapshot/data/
    # Initialize a snapshot, replacing same named snapshot if it exists
    - bf_init_snapshot
        network: network_name
        snapshot: duplicate_snapshot_name
        snapshot_data: /path/to/snapshot/data.zip
        overwrite: true



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
        <div>Information about the snapshot created.</div>
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
        <td>snapshot</td>
        <td>
            <div>Name of the snapshot created.</div>
        </td>
        <td align=center>always</td>
        <td align=center>str</td>
        <td align=center></td>
        </tr>

        <tr>
        <td>network</td>
        <td>
            <div>Name of the network created.</div>
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


