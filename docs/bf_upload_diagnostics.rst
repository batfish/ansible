.. _bf_upload_diagnostics:

bf_upload_diagnostics
+++++++++++++++++++++
Upload anonymized diagnostic information about a Batfish snapshot

.. contents::
   :local:
   :depth: 2


Synopsis
--------


* Fetches, anonymizes, and uploads diagnostic information about a Batfish snapshot.  This runs a series of diagnostic questions on the specified snapshot, which are then anonymized with Netconan (`https://github.com/intentionet/netconan <https://github.com/intentionet/netconan>`_), and optionally uploaded to the Batfish developers.



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
    <td>contact_info<br/><div style="font-size: small;"></div></td>
    <td>str</td>
    <td>no</td>
    <td></td>
    <td>
        <div>Contact information associated with this upload.</div>
    </td>
    </tr>

    <tr>
    <td>dry_run<br/><div style="font-size: small;"></div></td>
    <td>bool</td>
    <td>no</td>
    <td>True</td>
    <td>
        <div>Whether or not to skip upload. If <code>true</code>, upload is skipped and the anonymized files will be stored locally for review. If <code>false</code>, anonymized files will be uploaded to the Batfish developers.</div>
    </td>
    </tr>

    <tr>
    <td>netconan_config<br/><div style="font-size: small;"></div></td>
    <td>bool</td>
    <td>no</td>
    <td>Anonymize passwords and IP addresses.</td>
    <td>
        <div>Path to Netconan (<a href='https://github.com/intentionet/netconan'>https://github.com/intentionet/netconan</a>) configuration file, containing settings used for information anonymization.</div>
    </td>
    </tr>

    <tr>
    <td>network<br/><div style="font-size: small;"></div></td>
    <td>str</td>
    <td>no</td>
    <td>Value in the <code>bf_network</code> fact.</td>
    <td>
        <div>Name of the network to collect diagnostic information from.</div>
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
        <div>Name of the snapshot to collect diagnostic information about.</div>
    </td>
    </tr>

    </table>
    </br>

.. _bf_upload_diagnostics-examples-label:

Examples
--------

::

    
    # Generate diagnostic information about the specified snapshot and save locally (do not upload)
    - bf_upload_diagnostics
        network: datacenter_sea
        snapshot: 2019-01-01
        dry_run: true
        contact_info: my.email@example.com
    # Generate diagnostic information about the specified snapshot and upload to the Batfish developers
    - bf_upload_diagnostics
        network: datacenter_sea
        snapshot: 2019-01-01
        dry_run: false
        contact_info: my.email@example.com



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


